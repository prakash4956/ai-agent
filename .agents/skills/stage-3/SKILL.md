---
name: stage-3
description: Course notes for stage 3 of the agent course (stage3.py): what the stage adds, the predict question, the expected behaviour and the common fixes. Load when the learner asks about stage 3, stage3.py, the tool descriptions or JSON actions.
metadata:
  opencode/autoinvoke: "true"
---
# Stage 3: stage3.py

## What this stage adds

The model lines are back. The tool descriptions go into the system entry, with today's date as the first sentence because the model does not know the date. The model replies with one action written as JSON, the program parses it with json.loads, and the branch under label 4c runs the one tool the action names and prints the observation. One step only. Part 4 of the seven, the model deciding. The model sees only the description text and never the two functions; the description and the branch must agree word for word.

## The predict question

Which action will the model choose, search_web or read_webpage, and with what query or url?

## What the learner should see

'The model wrote:' followed by one line of JSON, then 'Observation: 5 results' and the first 300 characters of the results. The first action is a search with a query close to the goal, because the descriptions say that read_webpage needs a url from a search result and the list has none. If the learner changes the goal line to a question of their own, the model turns that goal into search words with no rule in the program saying how.

## Common messages and what they mean

- 'The model did not answer with an action. Run again.' means the model wrote text instead of JSON, or wrapped the JSON in a code fence; run again, and if it happens twice, look at the raw reply printed on the line above.
- 'No tool is called' followed by a name means the model wrote an action name that is not in the descriptions; no tool runs, and the observation says so.
- 'KeyError: query' or 'KeyError: url' means the model wrote the action name without the field that tool needs; run again.
- 'The provider refused the request' with 429 means the free model's per-minute limit; wait one minute.
