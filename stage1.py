"""Stage 1: the model answers the research question from its training data only.

What this stage adds: the goal, which is the research question, as the only
user entry, and one call to the model. These are the chatbot's own lines with a
new question and a new system entry.
Why: the reply shows where the model's facts come from when the list holds only
the question. Two of the seven parts of an agent are here: the goal and the
model.
"""
import os
from dotenv import load_dotenv
from openai import OpenAI, APIError

# 1. The goal. This is the question the agent works on. Every stage uses it.
GOAL = "What is driving the gold price this month?"

# 2. The model. The same three values and the same client as the chatbot.
load_dotenv()
client = OpenAI(
    base_url=os.getenv("LLM_BASE_URL"),   # where the requests go
    api_key=os.getenv("LLM_API_KEY"),     # the account that is charged
)

# 2b. The list. The model receives only what is in this list.
system_entry = {
    "role": "system",
    "content": (
        "You are a research assistant. Answer the question in at most five "
        "sentences. State the date of the most recent information you used."
    ),
}
history = [system_entry, {"role": "user", "content": GOAL}]

input("Predict first: will the reply give a gold price with this month's date? Write yes or no, then press Enter only.\n")

# 2c. Call the model, and handle the one error this stage teaches: a refused
#     request.
try:
    response = client.chat.completions.create(
        model=os.getenv("LLM_MODEL"),   # which model answers
        messages=history,
    )
except APIError as refused:
    print("The provider refused the request:", refused)
    print("Check the three LLM values in .env. If the message says rate limit, wait one minute and run again.")
    raise SystemExit

# 2d. Print the reply. Nothing else was in the list, so the reply came from the
#     model's training data.
print(response.choices[0].message.content)
