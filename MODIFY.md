# After the session: make one change, and post it

## The take-home menu

Four items, in any order. Each names the file it touches and what finished means. Post what
you did in the class channel with a note of three sentences: what you changed, what you
kept, and what the trace or the checks showed afterwards.

1. **Make one change to what the agent may do.** In `stage6.py`, add one of the three
   changes below, A, B or C, then run `python stage6.py` again.
   - A, a list of allowed sites: a list of site names near the top of the file, and one
     `if` in the `read_webpage` branch that refuses an address whose site is not on the list
     and makes the observation say so.
   - B, a line that asks you before each page is read: one `input` line in the
     `read_webpage` branch that waits for Enter before the page is fetched.
   - C, a rule that refuses finish until two pages were read: one `if` in the finish branch
     that, when fewer than two addresses are in `urls_read`, makes the observation "Read two
     pages before you finish" and continues the loop instead of breaking.
   Finished means: the check record after the change, and one line on what moved in the
   trace.
2. **Run the framework file.** Inside the virtual environment, run
   `pip install -r requirements-frameworks.txt`, then
   `python 05_frameworks/langchain_agent.py` from the repository root. Finished means: the
   report printed. If the run ends
   with "Recursion limit of 20 reached", that is the hidden stop condition firing; run again
   or raise the number in the config line.
3. **Put the agent behind your chatbot's route and deploy it.** Copy your chatbot's
   `app.py`, replace the model call inside the chat route with the stage 6 loop, return the
   brief as the reply, and deploy it the way the chatbot was deployed, with the three LLM
   values in the host's environment settings. Finished means: a link that answers one
   research question. The chatbot course's deploy steps apply unchanged; the agent's run takes
   longer than one chat reply, so the first request may wait up to a minute.
4. **Add a third tool of your own.** In `stage6.py`, write one function that takes text and
   returns text, add one line for it to the tool descriptions with its JSON shape, add one
   branch that runs it, and run the agent with a goal that needs it. Finished means: a trace
   in which the model asked for your tool and the observation came from it.

Optional, after the four: a smaller or larger `MAX_STEPS`; a larger `PAGE_LIMIT`; a fourth
check of your own, written first as a sentence about the state; a different fixed question.

## The reusable-code map

| File | Lines to change | Lines to keep |
|---|---|---|
| `stage6.py` | The goal; the tool descriptions when you add a tool; `MAX_STEPS`; `PAGE_LIMIT`; the source list line | The client lines; the two tool functions; the parse line and the branch; the two append lines; the finish branch and the break; the three checks |
| `.env` | The provider's three values | The names of the three values; the `USE_FIXTURES` switch |
| `05_frameworks/langchain_agent.py` | The system prompt; the recursion limit; a third tool with its decorator | The model line; the `create_agent` call; the `invoke` call |
| A copy of the chatbot's `app.py` | The chat route's body, which becomes the loop | The client lines; the route line; the passphrase check; the run lines |
