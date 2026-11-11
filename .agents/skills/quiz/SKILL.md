---
name: quiz
description: Ask the learner three predict-the-output questions about a stage file before they run it, one at a time. Use before a run, or when the learner asks to be quizzed.
metadata:
  opencode/slash: "true"
---
# Quiz before the run

1. Ask which stage the learner is about to run, if not stated, and read that file.
2. Ask three questions, one at a time, and wait for each answer before asking the next:
   - The Predict question from the file's header comment or its `input` line.
   - A question about one line marked `NEW in stage N`: what will this line do on the
     second step, or when the model writes an action that is not in the descriptions?
   - A question about what the model receives: which entries are in the list when the call
     is made on step 1, and which on step 3?
3. After each answer, say whether it matches what the code will do and why, in two
   sentences. If the learner says they do not know or asks for the answer, give it with the
   reasoning and move to the next question. Do not show the actual printed trace; the
   learner runs the script to see it, and the search results differ from run to run.
4. Close with: "Now run it, and tell me whether the trace matched your prediction."

Ask once before each answer, then answer. Do not write code.
