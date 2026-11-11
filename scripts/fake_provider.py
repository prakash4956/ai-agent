"""Instructor script: a local stand-in for the model provider.

It answers the two requests the course makes, the model list and chat
completions, with scripted replies, so that every stage script can be run with
no key and no network. Used with USE_FIXTURES=1, nothing leaves the laptop.

Start it in one terminal:
    python scripts/fake_provider.py
Then, in another terminal, point .env at it:
    LLM_BASE_URL=http://127.0.0.1:8765/v1
    LLM_API_KEY=anything
    LLM_MODEL=fake
    USE_FIXTURES=1

What it replies, decided from what the request contains:
- No tool descriptions (stage 1): a stale answer about gold, dated last year.
- Descriptions without a finish action (stages 3 and 4): search on the first
  step, then a read of each saved page in turn, for ever.
- Descriptions with a finish action (stages 5 and 6): search, read, read, then
  finish with a report. With LLM_MODEL=fake-weak it finishes after one read.
  With LLM_MODEL=fake-prose it searches, reads three pages, writes its answer as
  plain text at step 5, and at step 6 chooses finish only if the program said
  that one step is left; without that warning it searches again.
- A request with native tools (the framework file): one tool call for search,
  one for read, then a final text answer.
"""
import json
import os
from http.server import BaseHTTPRequestHandler, HTTPServer

SEARCH = json.load(open("fixtures/search.json"))
PAGES = json.load(open("fixtures/pages.json"))

# Pages with saved text come first, so the scripted reads get real pages.
URLS = sorted((r["url"] for r in SEARCH), key=lambda url: not PAGES.get(url))
STALE = (
    "Gold prices are driven by interest rates, the US dollar, inflation and central "
    "bank buying. As of my most recent information, from early 2025, gold traded "
    "near 2,900 dollars an ounce."
)
REPORT = (
    "Gold has risen this month on expectations of lower interest rates, a weaker "
    "dollar and continued central bank buying, according to the pages I read "
    "(the-world-now.com, investopedia.com). Safe-haven demand during market stress "
    "added to the move."
)
PROSE = (
    "The main drivers of gold this month are interest rates, the dollar and central "
    "bank buying, according to the pages I read."
)


def count_steps(messages):
    """How many actions the model has already written in this run."""
    return sum(1 for m in messages if m.get("role") == "assistant")


def scripted_action(messages, weak, prose=False):
    system = messages[0]["content"] if messages and messages[0]["role"] == "system" else ""
    done = count_steps(messages)
    has_finish = '"finish"' in system
    if done == 0:
        return {"action": "search_web", "query": "gold price drivers this month"}
    reads = done - 1
    if prose and has_finish:
        if done == 4:
            return PROSE          # step 5: the answer, but not as an action
        if done == 5:             # step 6: finish only if the warning arrived
            warned = "Only one step is left" in str(messages[-1].get("content", ""))
            if warned:
                return {"action": "finish", "report": REPORT}
            return {"action": "search_web", "query": "gold price drivers and yields"}
        return {"action": "read_webpage", "url": URLS[reads % len(URLS)]}
    if has_finish and (reads >= 2 or (weak and reads >= 1)):
        return {"action": "finish", "report": REPORT}
    return {"action": "read_webpage", "url": URLS[reads % len(URLS)]}


def native_tool_reply(messages):
    calls = sum(1 for m in messages if m.get("role") == "assistant" and m.get("tool_calls"))
    if calls == 0:
        call = {"name": "search_web", "arguments": json.dumps({"query": "gold price this month"})}
    elif calls == 1:
        call = {"name": "read_webpage", "arguments": json.dumps({"url": URLS[0]})}
    else:
        return {"role": "assistant", "content": REPORT}
    return {
        "role": "assistant",
        "content": None,
        "tool_calls": [{"id": f"call_{calls}", "type": "function", "function": call}],
    }


class Handler(BaseHTTPRequestHandler):
    def log_message(self, *args):
        pass

    def send(self, body):
        data = json.dumps(body).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        self.send({"object": "list", "data": [{"id": "fake", "object": "model"}]})

    def do_POST(self):
        length = int(self.headers.get("Content-Length", 0))
        request = json.loads(self.rfile.read(length) or b"{}")
        messages = request.get("messages", [])
        system = messages[0]["content"] if messages and messages[0]["role"] == "system" else ""
        if request.get("tools"):
            message = native_tool_reply(messages)
        elif "Actions:" in system:
            weak = request.get("model") == "fake-weak"
            prose = request.get("model") == "fake-prose"
            reply = scripted_action(messages, weak, prose)
            content = reply if isinstance(reply, str) else json.dumps(reply)
            message = {"role": "assistant", "content": content}
        else:
            message = {"role": "assistant", "content": STALE}
        self.send({
            "id": "fake", "object": "chat.completion", "model": "fake",
            "choices": [{"index": 0, "message": message, "finish_reason": "stop"}],
            "usage": {"prompt_tokens": sum(len(str(m.get("content", ""))) // 4 for m in messages), "completion_tokens": 50, "total_tokens": 0},
        })


if __name__ == "__main__":
    print("Fake provider listening on http://127.0.0.1:8765/v1 - press Ctrl+C to stop")
    HTTPServer(("127.0.0.1", 8765), Handler).serve_forever()
