"""Stage 4: the observation joins the state and the model is asked again, until
the steps run out.

What this stage adds: the call is inside a loop with a fixed number of steps.
After every step the model's action and the tool's observation join the list,
so the next call sees them. A reply that is not an action now spends the step
instead of ending the run.
What it does not add: a way to finish. The model has two actions and neither
one is stopping, so the run uses every step and writes no report.
Why: parts 5 and 6 of the seven, the loop and the state, are here. Part 7 is
missing on purpose.
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

# 4. The model decides. The tool descriptions, unchanged from stage 3.
TOOL_DESCRIPTIONS = (
    "Today is " + date.today().isoformat() + ". "
    "You are a research agent working on one question. You cannot search or read "
    "anything yourself. On each step, reply with one action as JSON and nothing else.\n"
    "Actions:\n"
    '{"action": "search_web", "query": "<the words to search for>"} returns up to 5 '
    "results, each with a title, a url and a snippet.\n"
    '{"action": "read_webpage", "url": "<a url from a search result>"} returns the '
    "text of that page, up to 2000 characters.\n"
    "The program runs your action and sends you the result as the next message."
)

# 2b. The list, unchanged.
history = [
    {"role": "system", "content": TOOL_DESCRIPTIONS},
    {"role": "user", "content": GOAL},
]

input("Predict first: at which step, from 1 to 6, will the agent stop? Write it down, then press Enter only.\n")

# NEW in stage 4
# 5. The loop. The program asks, runs the action, and asks again.
MAX_STEPS = 6
for step in range(1, MAX_STEPS + 1):
    print("\n" + "-" * 60)   # a rule line, so that each step is easy to find
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

    # 4b. The program reads the action. A reply that is not an action now
    #     spends the step: the reply and a correction join the list, and the
    #     model is asked again.
    reply = response.choices[0].message.content
    print("The model wrote:", reply)
    try:
        action = json.loads(reply)
    except json.JSONDecodeError:
        # NEW in stage 4
        correction = ("That was not an action. "
                      "Reply with one action as JSON and nothing else.")
        print("The program replied:", correction)
        history.append({"role": "assistant", "content": reply})
        history.append({"role": "user", "content": correction})
        continue

    # 4c. The program runs the one tool the action names, unchanged.
    if action["action"] == "search_web":
        results = search_web(action["query"])
        observation = json.dumps(results)
        print("Observation:", len(results), "results")
    elif action["action"] == "read_webpage":
        observation = read_webpage(action["url"])
        print("Observation:", len(observation), "characters from", action["url"])
    else:
        observation = "No tool is called " + action.get("action", "nothing")
    print(observation[:300])

    # NEW in stage 4
    # 6. The state. The observation is labelled, then the action and the
    #    observation join the list, so the next call sees them. Remove the two
    #    append lines and every step is the first step.
    observation = "Observation: " + observation
    history.append({"role": "assistant", "content": reply})
    history.append({"role": "user", "content": observation})

print(f"\nUsed all {MAX_STEPS} steps. No report was written.")
