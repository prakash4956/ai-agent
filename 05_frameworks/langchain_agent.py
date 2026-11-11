"""The same seven parts, written with a framework.

This file is read in the session and run at home. It is the stage 6 agent
written with LangChain. The labels are the same seven numbers as the stage
scripts, so that you can find each part. Three parts are hidden inside one
function call, and one part is absent.
Install first:   pip install -r requirements-frameworks.txt
Run:             python 05_frameworks/langchain_agent.py
"""
import os
from datetime import date
import requests
from bs4 import BeautifulSoup
from ddgs import DDGS
from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain.chat_models import init_chat_model
from langchain_core.tools import tool

load_dotenv()

# 1. The goal, unchanged.
GOAL = "What is driving the gold price this month?"

# 2. The model. The three .env values, through the framework's own function.
#    The framework calls the model with the provider's native tool-calling
#    feature: the tool descriptions are sent as a field of the request instead
#    of in the system entry, and the model's action comes back as a field, not as
#    JSON text. The mechanism is the one from stage 3.
model = init_chat_model(
    "openai:" + os.getenv("LLM_MODEL"),
    base_url=os.getenv("LLM_BASE_URL"),
    api_key=os.getenv("LLM_API_KEY"),
)

# 3. The tools. The same two functions, with a decorator that turns each into
#    a tool. The docstring is the description the model reads.
HEADERS = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36"}

@tool
def search_web(query: str) -> list:
    """Search the web and return up to 5 results, each with title, url and snippet."""
    found = DDGS().text(query, max_results=5)
    return [{"title": r["title"], "url": r["href"], "snippet": r["body"]} for r in found]

@tool
def read_webpage(url: str) -> str:
    """Fetch one page and return its visible text, up to 2000 characters."""
    page = requests.get(url, headers=HEADERS, timeout=20)
    soup = BeautifulSoup(page.text, "html.parser")
    for part in soup(["script", "style", "nav", "header", "footer"]):
        part.decompose()
    return " ".join(soup.get_text(" ", strip=True).split())[:2000]

# 4, 5, 6 and 7. The model deciding, the loop, the state and the stop
#    condition are all inside this one call. You cannot see the loop, the list
#    or the break; the framework owns them. The stop condition is partly
#    visible: the run ends when the model answers without asking for a tool,
#    or when the recursion limit below is reached.
agent = create_agent(
    model,
    tools=[search_web, read_webpage],
    system_prompt="Today is " + date.today().isoformat() + ". You are a research agent working on one question. Read at least two pages before you answer. Name the pages you used.",
)

# 1 again. The goal goes in as the one message; the limit caps the steps. Each
#    model call and each tool run counts as one; the dry run needed more than
#    12 on a free model, so the limit is 20.
result = agent.invoke(
    {"messages": [{"role": "user", "content": GOAL}]},
    config={"recursion_limit": 20},
)

# The final message is the report. The state is in result["messages"], which
# is the framework's own list; the trace is not printed unless you print it.
print(result["messages"][-1].content)

# 8. Evaluation: absent. Nothing in this file checks what the agent read.
