---
name: stage-4
description: Course notes for stage 4 of the agent course (stage4.py): what the stage adds, the predict question, the expected behaviour and the common fixes. Load when the learner asks about stage 4, stage4.py, the loop or the state.
metadata:
  opencode/autoinvoke: "true"
---
# Stage 4: stage4.py

## What this stage adds

The call is inside a loop with MAX_STEPS = 6. After every step the model's reply joins the list as an assistant entry and the observation joins it as a user entry that starts with 'Observation:'. A reply that is not an action spends the step: the reply and a correction join the list and the model is asked again. There is no way to finish, so the run uses every step and prints 'Used all 6 steps. No report was written.' Parts 5 and 6 of the seven, the loop and the state.

## The predict question

At which step, from 1 to 6, will the agent stop?

## What the learner should see

Six steps, each under a rule line of hyphens and each with 'The model wrote:' and an observation line, then 'Used all 6 steps. No report was written.' After step 3 the list holds eight entries, three of them written by the model. The model may write a paragraph instead of an action when it has read enough; the program records that as not an action and asks again. With the two append lines under label 6 commented out, step 2 repeats step 1, because the model receives the same list every time; the part that was removed is the state. The learner puts the # signs back before stage 5.

## Common messages and what they mean

- 'Used all 6 steps. No report was written.' is the designed behaviour of this stage, because the descriptions offer no way to stop.
- 'The program replied: That was not an action. Reply with one action as JSON and nothing else.' is the correction the program puts into the list when the model wrote text instead of JSON; it is not an error, the step is spent, and no observation follows.
- 'NameError: name observation is not defined' means the else branch under label 4c is missing; it sets the observation when the action name matches no tool.
- 'The provider refused the request' with 429 part way through a run ends the run; the trace so far is used for the questions.
- If the same search repeats on every step with the append lines present, the two lines may be indented into the except branch; they belong at the end of the loop body.
