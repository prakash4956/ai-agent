"""Stage 3: the model writes the request, and the program runs it.

What this stage adds: the model lines are back. The tool descriptions go into
the system entry, the model replies with one action written as JSON, and the
program runs that one tool once and prints the observation.
Why: the model never runs anything. It reads a text description of the tools,
writes a request in the shape that text asks for, and the program runs it. Part
4 of the seven, the model deciding, is here. One step only; the loop is stage 4.
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

# 2. The model, back from stage 1.
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

# NEW in stage 3
# 4. The model decides. This text is all the model ever sees about the tools.
#    It never sees the two functions above. The shape of each action is given
#    here, and the program below matches that shape word for word. The model
#    does not know today's date; the program does, so the first line says it.
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

# NEW in stage 3
# 2b. The list, now with the descriptions as the system entry.
history = [
    {"role": "system", "content": TOOL_DESCRIPTIONS},
    {"role": "user", "content": GOAL},
]

input("Predict first: which action will the model choose, search_web or read_webpage, and with what query or url? Write it down, then press Enter only.\n")

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

# NEW in stage 3
# 4b. The program reads the action. The raw reply is printed first, so that you
#     see exactly what the model wrote. The one error this stage teaches: a
#     reply that is not an action.
reply = response.choices[0].message.content
print("The model wrote:", reply)
try:
    action = json.loads(reply)
except json.JSONDecodeError:
    print("The model did not answer with an action. Run again.")
    raise SystemExit

# NEW in stage 3
# 4c. The program runs the one tool the action names, and prints the
#     observation. Nothing the model wrote ran anything; these lines did.
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
