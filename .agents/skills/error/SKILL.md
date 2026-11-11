---
name: error
description: Read an error message, a traceback or a failed run with the learner, explain it in plain English, point to the line, and ask what they will change. Use whenever the learner pastes an error or says a script stopped.
metadata:
  opencode/slash: "true"
---
# Read an error with the learner

1. Ask the learner to paste the last ten lines the script printed, if they have not.
2. Find the error type and the message. Reply in bullets: one for what that type of error
   means, one for what the message says.
3. One bullet points to the line: the file, the line number from the traceback, and the
   line itself in backticks. If the script printed one of the course's own messages, explain
   that message and the action it names. The course's own messages are: "LLM_API_KEY is not
   set yet"; "The provider refused the request"; "Search failed"; "Could not fetch that
   page"; "The model did not answer with an action"; "That was not an action"; "Used all 6
   steps. No report was written."; and "No tool is called" followed by a name.
4. One bullet says in words what change would fix it, for example "put the two append lines
   back under label 6" or "set USE_FIXTURES=1 in .env and run again". A last bullet asks
   whether that matches what they see; if the learner proposes a different change, say
   whether it would work.

Three of the course's messages are results and not faults, and say so: "Could not fetch
that page" means the site refused the program and the run continues with empty text; "Used
all 6 steps" in stage 4 is the designed behaviour, because the script has no way to
finish; "That was not an action", printed after "The program replied:", means the model
wrote text instead of JSON and the step was spent.

Do not type the corrected line; the learner types it. Never ask for or display the
contents of `.env` or a key.
