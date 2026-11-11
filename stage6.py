"""Stage 6: three checks measure the run.

What this stage adds: a record of which pages the agent read, and three checks
printed after the run: it finished by itself, it read at least two pages, and
every source it listed is one it read.
Why: part 7 of the seven as the glossary names it, evaluation, is here. The
brief is well written whether or not the agent read anything; a check is a
sentence about the state that the program can test.
Modify: change the line "sources = urls_seen" to "sources = urls_read" and run
again. Check 3 then passes, and the brief lists fewer sources.
"""
import json
import os
from datetime import date
import requests
from bs4 import BeautifulSoup
from ddgs import DDGS
from dotenv import load_dotenv
from openai import OpenAI, APIError

# 1. The goal, unchanged.
GOAL = "What is driving the gold price this month?"

# 2. The model, unchanged.
load_dotenv()
client = OpenAI(
    base_url=os.getenv("LLM_BASE_URL"),
    api_key=os.getenv("LLM_API_KEY"),
)

# 3. The tools, unchanged from stage 2.
HEADERS = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36"}
PAGE_LIMIT = 2000   # characters kept from a page, so the trace stays readable

def search_web(query):
    """Search the web; return up to 5 results with title, url and snippet."""
    if os.getenv("USE_FIXTURES"):   # offline: return the saved search instead
        return json.load(open("fixtures/search.json"))
    try:
        found = DDGS().text(query, max_results=5)
    except Exception as failed:
        print("Search failed:", failed)   # the search service refused for now
        return []
    results = []
    for r in found:
        results.append(
            {"title": r["title"], "url": r["href"], "snippet": r["body"]}
        )
    return results

def read_webpage(url):
    """Fetch one page; return its visible text, up to PAGE_LIMIT characters."""
    if os.getenv("USE_FIXTURES"):   # offline: return the saved page instead
        return json.load(open("fixtures/pages.json")).get(url, "")
    try:
        page = requests.get(url, headers=HEADERS, timeout=20)
        page.raise_for_status()
    except requests.RequestException as failed:
        print("Could not fetch that page:", failed)
        return ""
    soup = BeautifulSoup(page.text, "html.parser")
    for part in soup(["script", "style", "nav", "header", "footer"]):
        part.decompose()   # remove the parts that are not the article
    return " ".join(soup.get_text(" ", strip=True).split())[:PAGE_LIMIT]

# 4. The model decides. The tool descriptions, unchanged from stage 5.
TOOL_DESCRIPTIONS = (
    "Today is " + date.today().isoformat() + ". "
    "You are a research agent working on one question. You cannot search or read "
    "anything yourself. On each step, reply with one action as JSON and nothing else.\n"
    "Actions:\n"
    '{"action": "search_web", "query": "<the words to search for>"} returns up to 5 '
    "results, each with a title, a url and a snippet.\n"
    '{"action": "read_webpage", "url": "<a url from a search result>"} returns the '
    "text of that page, up to 2000 characters.\n"
    '{"action": "finish", "report": "<your answer in about 150 words, naming the '
    'pages you used>"} ends the run. Choose it when you have read enough to answer.\n'
    "The program runs your action and sends you the result as the next message."
)

# 2b. The list, unchanged.
history = [
    {"role": "system", "content": TOOL_DESCRIPTIONS},
    {"role": "user", "content": GOAL},
]

input("Predict first: will check 3, every listed source was read, pass or fail? Write it down, then press Enter only.\n")

# 5. The loop, unchanged, except that the pages read are now recorded.
MAX_STEPS = 6
report = None
urls_seen = []
urls_read = []      # NEW in stage 6: pages the agent opened and got text from
for step in range(1, MAX_STEPS + 1):
    print("\n" + "-" * 60)
    print(f"Step {step} of {MAX_STEPS}")

    # 2c. Call the model, unchanged.
    try:
        response = client.chat.completions.create(
            model=os.getenv("LLM_MODEL"),
            messages=history,
        )
    except APIError as refused:
        print("The provider refused the request:", refused)
        print("Check the three LLM values in .env. If the message says rate limit, wait one minute and run again.")
        raise SystemExit

    # 4b. The program reads the action, unchanged.
    reply = response.choices[0].message.content
    print("The model wrote:", reply)
    try:
        action = json.loads(reply)
    except json.JSONDecodeError:
        correction = ("That was not an action. "
                      "Reply with one action as JSON and nothing else.")
        if step == MAX_STEPS - 1:
            correction += " Only one step is left."
            correction += " Choose finish on your next step."
        print("The program replied:", correction)
        history.append({"role": "assistant", "content": reply})
        history.append({"role": "user", "content": correction})
        continue

    # 7. The stop condition, unchanged.
    if action["action"] == "finish":
        report = action["report"]
        print(f"\nFinished at step {step} of {MAX_STEPS}.")
        break

    # 4c. The program runs the one tool the action names. The read branch now
    #     also records the pages that returned text.
    if action["action"] == "search_web":
        results = search_web(action["query"])
        for r in results:
            if r["url"] not in urls_seen:
                urls_seen.append(r["url"])
        observation = json.dumps(results)
        print("Observation:", len(results), "results")
    elif action["action"] == "read_webpage":
        observation = read_webpage(action["url"])
        if observation and action["url"] not in urls_read:   # NEW in stage 6
            urls_read.append(action["url"])
        print("Observation:", len(observation), "characters from", action["url"])
    else:
        observation = "No tool is called " + action.get("action", "nothing")
    print(observation[:300])

    # 6. The state, unchanged.
    if step == MAX_STEPS - 1:
        observation += " Only one step is left."
        observation += " Choose finish on your next step."
    observation = "Observation: " + observation
    history.append({"role": "assistant", "content": reply})
    history.append({"role": "user", "content": observation})

# 8. The brief, unchanged, except that the source list line now sits above the
#    if, so that the checks below can read it. The Modify is that line.
sources = urls_seen
if report is None:
    print(f"\nUsed all {MAX_STEPS} steps. No report was written.")
else:
    print("\n" + "=" * 60)
    print("Research brief")
    print("=" * 60)
    print("Question:", GOAL)
    print()
    print(report)
    print()
    print("Sources seen during this run:")
    for number, url in enumerate(sources, start=1):
        print(f"{number}. {url}")

# NEW in stage 6
# 9. The evaluation. Three checks on the state, after the run. Each check is a
#    sentence about the state that the program can test.
unread = [url for url in sources if url not in urls_read]
print("\n" + "=" * 60)
print("Checks")
print("=" * 60)
print("Check 1, finished by itself:", "PASS" if report is not None else "FAIL")
print(f"Check 2, pages read (needs at least 2): {len(urls_read)},", "PASS" if len(urls_read) >= 2 else "FAIL")
print(f"Check 3, every listed source was read: listed {len(sources)}, read {len(urls_read)},", "PASS" if not unread else "FAIL")
