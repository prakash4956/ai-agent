# Questions to ask the tutor at each stage

The tutor is OpenCode, started with the command `opencode` at the root of your repository.
It has read every file in the folder and the course notes for each stage. It answers
questions about Python and about the scripts directly, in short bullet points. Before it
tells you what a stage will print, it asks for your prediction once; if you write "just tell
me", it tells you. It explains errors and says the fix in words, it reads your trace with
you step by step, and it never writes or rewrites a stage, because the course keeps the
writing with you.

Three commands cover most of what you will ask: `/explain` walks a stage file line by line,
`/quiz` asks you three predict-the-output questions before a run, and `/error` reads an
error message with you. You can also ask in plain words. The questions below are the ones
that teach the most at each stage; ask them in your own words, and ask any other question
that comes up.

## Stage 0: check.py

1. Explain check.py line by line.
2. Which two packages are new in this course, and what does each one do?
3. What does "exactly one provider block is active" mean, and how do I switch blocks?
4. Where does my key go, and why is it never written in the code?

## Stage 1: the model answers from its training data

1. Where is the goal in the code, and why is it the only user entry?
2. What does the system entry ask the model to do, and why does it ask for a date?
3. Why did the reply give a date before today, or no date at all?
4. Could the model have looked anything up? What would it need?
5. Quiz me on stage 1.

## Stage 2: a tool is a function

1. Explain search_web line by line, and then read_webpage.
2. What is a dictionary, and why is each search result one?
3. What does the User-Agent header do, and why does read_webpage send one?
4. Why does read_webpage keep only the first 2,000 characters?
5. What does "Could not fetch that page" mean, and why does the run continue?
6. What does the model see of this run?

## Stage 3: the model writes the request

1. Explain the tool descriptions line by line. What does the model see, and what does it
   never see?
2. Why is today's date the first sentence of the descriptions?
3. What does `json.loads` do, and what happens when the reply is not JSON?
4. Which line runs the tool, and why is it a branch on the action name?
5. What happens if the model writes an action name that is not in the descriptions?
6. Quiz me on stage 3.

## Stage 4: the loop and the state

1. What does `for step in range(1, MAX_STEPS + 1)` do, one piece at a time?
2. Which two lines make the state, and what is in the list after step 3?
3. Why did my agent not stop before step 6?
4. My model wrote a paragraph at step 4 instead of an action. What happened next, and why?
5. With the two append lines commented out, why does step 2 repeat step 1?
6. Read this trace with me: paste your six steps.

## Stage 5: the finish action

1. What does `break` do when the model writes finish, and why is the description also
   needed?
2. What does the line about "Only one step is left" do, and why is it before the last step?
3. How is the source list built, and why can it be longer than the pages read?
4. Read this trace with me and help me count: how many steps, how many pages read, how many
   sources listed?
5. What made this run stop when the stage 4 run did not?

## Stage 6: the three checks

1. Explain the three checks line by line. What does each one test?
2. Why does check 3 count pages read instead of addresses listed?
3. My check 3 passed without the change. Is that good?
4. What does changing `sources = urls_seen` to `sources = urls_read` change, and what does
   it not change?
5. A claim in my brief is not on the page it cites. Where could it have come from?
6. For the change I chose, A, B or C, which lines would it need, in words?

## Stage 7: the framework file

1. Explain 05_frameworks/langchain_agent.py line by line, naming the part of the seven on
   each line.
2. Where did the loop, the state and the stop condition go?
3. What does the `@tool` line do, and what does the model read from the function?
4. What does "Recursion limit of 20 reached without hitting a stop condition" mean?
5. What is native tool calling, and how is it the same as stage 3?
6. How do I install and run this file at home?
