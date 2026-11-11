---
name: stage-2
description: Course notes for stage 2 of the agent course (stage2.py): what the stage adds, the predict question, the expected behaviour and the common fixes. Load when the learner asks about stage 2 or about stage2.py, search_web or read_webpage.
metadata:
  opencode/autoinvoke: "true"
---
# Stage 2: stage2.py

## What this stage adds

Two functions, search_web and read_webpage, and four lines that call them. No line in this file sends anything to a model: the program calls both tools itself, and the model lines return in stage 3. search_web returns up to five results, each a dictionary with title, url and snippet. read_webpage fetches one page with a browser User-Agent header, removes the script, style, navigation, header and footer parts, and returns the visible text up to 2,000 characters. Part 3 of the seven, the tools. The thing a tool returns is called the observation.

## The predict question

Will the first page's text reach the limit of 2,000 characters? Write yes or no.

## What the learner should see

Five numbered results with a title and an address each, then 'Reading result 1' and 'Page text: 2000 characters' on most days, followed by the first 300 characters. A smaller number means the page refused the program or has little text; that is a result and not a fault. The model saw nothing of this run, because no line in the file sends anything to a model. The Modify changes results[0] to results[1] on the reading line to read the second result instead.

## Common messages and what they mean

- 'Search failed' means the search service refused this laptop for the moment, or timed out. Set USE_FIXTURES=1 in .env and run again; the search then returns the same five saved results whatever the query.
- 'Could not fetch that page' with 401, 402 or 403 means the site refuses programs; the function returns empty text and the run continues.
- 'IndexError: list index out of range' on the reading line means the search returned no results, so results[0] does not exist; run again or set USE_FIXTURES=1.
- If nothing happens after the run command, the script is waiting at the predict gate for Enter.
