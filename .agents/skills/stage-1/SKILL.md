---
name: stage-1
description: Course notes for stage 1 of the agent course (stage1.py): what the stage adds, the predict question, the expected behaviour and the common fixes. Load when the learner asks about stage 1 or about stage1.py.
metadata:
  opencode/autoinvoke: "true"
---
# Stage 1: stage1.py

## What this stage adds

The goal, "What is driving the gold price this month?", as the one user entry, and one call to the model with the chatbot's own client lines. The system entry asks the model to give the date of the most recent information it used. Parts 1 and 2 of the seven, the goal and the model, are labelled on the script.

## Two lines a learner often asks about

- The system entry's content is two quoted pieces inside parentheses. Python joins them into one string; they are split across two lines only so that the code is easier to read.
- The list has two entries: the system entry saved above, and a user entry whose content is the value of GOAL, the line near the top of the file. The list only prepares the messages; the call under label 2c sends them.

## The predict question

Will the reply give a gold price with this month's date? Write yes or no.

## What the learner should see

The usual drivers named: interest rates, the dollar, inflation, central-bank buying, geopolitical risk. A date before today, or a statement that the model has no current data, or a confident date that is wrong. No page, no address, no source. The reply came from the model's training data, because the list held only the question. The model does not know today's date, so "this month" means whatever month its training suggested.

## Common messages and what they mean

- 'The provider refused the request' with 401 or 'API key' means the key in the active block is wrong or expired. With 429 or 'rate limit' it means too many requests in the last minute, or the day's allowance is used; the script's own last line says to wait one minute.
- If nothing happens after the run command, the script is waiting at the predict gate for Enter.
- A reply that gives a current-looking price with no date still came from training; the investigate question asks where that number could have come from.
