"""Stage 2: a tool is an ordinary function that returns text.

What this stage adds: two functions, search_web and read_webpage, and four
lines that call them. No line sends anything to a model: the program calls
both tools itself.
Why: a tool is a function the program can run. The model never runs one. In the
next stage the model asks for one, and the program runs it. The model lines
return in stage 3.
"""
import json
import os
import requests
from bs4 import BeautifulSoup
from ddgs import DDGS
from dotenv import load_dotenv

# 1. The goal, unchanged.
GOAL = "What is driving the gold price this month?"

load_dotenv()   # only for the offline switch, USE_FIXTURES, in this stage

# NEW in stage 2
# 3. The tools. A tool is a function the program can run. Each one takes text
#    and returns text or a list. Web servers answer a browser and often refuse
#    a program, so every request carries a browser's User-Agent header.
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

input("Predict first: will the first page's text reach the limit of 2,000 characters? Write yes or no, then press Enter only.\n")

# NEW in stage 2
# 3b. The program runs the search, then reads the first result. No model saw
#     any of this; the program chose the query and the page.
print("Search results for:", GOAL)
results = search_web(GOAL)
for number, result in enumerate(results, start=1):
    print(f"{number}. {result['title']} - {result['url']}")

print("Reading result 1:", results[0]["url"])
text = read_webpage(results[0]["url"])
print("Page text:", len(text), "characters. The first 300:")
print(text[:300])
