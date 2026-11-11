---
name: stage-5
description: Course notes for stage 5 of the agent course (stage5.py): what the stage adds, the predict question, the expected behaviour, the counts read from the trace and the common fixes. Load when the learner asks about stage 5, stage5.py, the finish action or the brief.
metadata:
  opencode/autoinvoke: "true"
---
# Stage 5: stage5.py

## What this stage adds

A third action, finish, carrying the report, and a break that ends the loop when the model chooses it. Before the last step, the observation also says 'Only one step is left. Choose finish on your next step.'; the correction for a reply that is not an action says the same at that step. After the loop the brief is printed: the question, the report, and 'Sources seen during this run' with every address that appeared in any search result. Part 7 of the seven, the stop condition. The model may choose finish only because the description offers it; the program stops only because the break line exists.

## The predict question

At which step will the agent finish, and how many pages will it have read by then?

## What the learner should see

'Finished at step N of 6', then the heading 'Research brief' between two rule lines of equals signs, then the brief with about five addresses under it. In the dry run the agent searched once, read three pages, finished at step 5 and listed five sources; two of the five were never opened. The source list is larger than the pages read on purpose; stage 6 measures that.

## Counting from the trace

Three counts can be read from the learner's own screen: the steps the agent used, the pages it read (the read_webpage actions) and the sources the brief lists. Help the learner count from their trace; do not count for them unless they ask.

## Common messages and what they mean

- 'Used all 6 steps. No report was written.' in this stage means the model never chose finish; run again, and if it happens twice, use the trace so far. Free models differ in whether they follow the finish instruction; the instructor tested the model named in .env.example.
- 'KeyError: report' means the model wrote the finish action without the report field; run again.
- A brief that finishes at step 1 or 2 having read nothing is possible and is the clearest case for stage 6; keep that trace.
