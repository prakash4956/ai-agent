---
name: stage-6
description: Course notes for stage 6 of the agent course (stage6.py): what the stage adds, the predict question, the three checks, the Modify and the common fixes. Load when the learner asks about stage 6, stage6.py, the checks or the source list.
metadata:
  opencode/autoinvoke: "true"
---
# Stage 6: stage6.py

## What this stage adds

A record of which pages the agent opened and got text from, urls_read, and three checks printed after the run: 'Check 1, finished by itself'; 'Check 2, pages read (needs at least 2)'; 'Check 3, every listed source was read'. Each check is a sentence about the state that the program tests and prints as PASS or FAIL. The evaluation, which the glossary card lists as the seventh part. Check 3 counts pages read; counting addresses listed would pass and would agree with the mistake it exists to catch.

## The predict question

Will check 3, every listed source was read, pass or fail?

## What the learner should see

The three checks print under the heading 'Checks', between two rule lines of equals signs. Check 1 PASS when the agent chose finish; check 2 PASS when it read two or more pages; check 3 FAIL with 'listed 5, read 3' or similar, because the source list holds every address seen. The Modify changes the line sources = urls_seen to sources = urls_read; check 3 then passes and the brief lists fewer sources, and nothing about the report text changed.

## Common messages and what they mean

- 'Check 1, finished by itself: FAIL' means the model never chose finish; the other two checks still print, and the learner fills the record with what printed.
- 'Check 3 ... PASS' without the Modify means the agent read every address it listed on that run, which is rare; another run will list addresses it did not open.
- 'NameError: name urls_read is not defined' means the line that creates the empty list before the loop is missing.
- If the brief lists zero sources after the Modify, the agent read no page with text; check 2 says so.
