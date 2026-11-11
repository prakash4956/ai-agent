---
name: explain
description: Walk one stage file of the agent course line by line in plain English, ending with one question. Use when the learner asks what a stage does or how a line works.
metadata:
  opencode/slash: "true"
---
# Explain a stage file

1. If the learner did not name a file, ask which stage they are on and name the file from the
   stage table in AGENTS.md.
2. Read the file. Start with its header comment: say in two sentences what this stage adds
   and why, and name the part of the seven that the stage adds.
3. Walk the code in the order it runs. For each line that carries the stage's idea, give
   one bullet that starts with the line itself in backticks, then one plain sentence on
   what the line does and why it is there. A block of a few lines that does one thing, such
   as the tool descriptions or the branch that runs a tool, gets one bullet with its first
   line and the line numbers of the block. A single line with several parts, such as a
   dictionary with two keys or a call with three arguments, gets one bullet per part, each
   starting with that part in backticks, for example `"role": "system"` and then
   `"content"`. Group the bullets under the script's numbered labels. Skip lines the learner
   already knows from earlier stages, such as the two tool functions after stage 2, unless
   they ask. The one-line-of-code limit from the course rules does not apply here; the
   six-bullet limit does not apply either, but every bullet still holds one line and one
   sentence.
4. Point out the lines marked `NEW in stage N`: these are the only lines that changed from
   the previous stage. Where a line is shaped for reading rather than for the computer, say
   so in one sentence, for example that two quoted pieces inside parentheses join into one
   string and are split across lines only so that the code is easier to read.
5. Close with two sentences before the question: one that says in everyday language what
   the block means, for example "Here are the instructions for answering, and here is the
   question to answer", and one that says what the block does not do yet, for example that
   it only prepares the list and does not send it to the model.
6. End with one optional question that checks understanding, such as which line the model
   receives the tool descriptions from, what the list holds after step 2, or what would
   happen if one of the new lines were removed. If the learner asks a question instead of
   answering, answer it, and do not ask the same checking question again.

Do not paste the whole file back. Do not write new code. Define every technical term the
first time it appears, using the course's own words: system entry, user entry, messages
list, action, observation, state. Quote every value from the file as it is written there;
never invent an example value, because the learner will look for it in the file. The goal
in every stage is "What is driving the gold price this month?" and the explanation uses
that line. If the learner asks what a Python word or line means, answer it directly.
