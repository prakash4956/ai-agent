# Before the session: what to have ready

In this session you build a research agent in Python: a program that gives a language
model a question, lets the model choose a web search or a page to read, runs that choice,
and repeats until the model decides it has read enough. It continues the chatbot course and
uses the same habits: the terminal, the virtual environment, one `.env` file and the
OpenCode tutor. The question the agent works on all session is "What is driving the gold
price this month?"

Everything below happens before the day. Allow twenty minutes, plus the quiz. Send the
`check.py` screenshot and the quiz answers at least two days before the session, so that
any problem is fixed before you arrive.

## 1. The repository

1. Open the course template: https://github.com/SwarupSG/ai-agent-cohort. Click "Use this
   template", then "Create a new repository", and give it a name such as `ai-agent`.
2. Clone it into your home folder, the same place as your chatbot repository: `/home/<you>/`
   in WSL (Windows Subsystem for Linux) on Windows, `/Users/<you>/` on macOS. On Windows,
   everything in this course happens inside WSL, as in the chatbot course; a path that
   starts with `/mnt/c/` is the Windows side and will not work.
3. Save `stage-guide.html`, which comes with this note, in that folder next to `check.py`.
   It is the worksheet for every stage. It is not part of the repository, and the
   repository's `.gitignore` keeps it out of your pushes.

## 2. The key and the provider

The course uses OpenRouter. Create a free key at https://openrouter.ai/keys and save it
where you can copy it. The free allowance is 50 requests a day, which covers one run of
every stage; a rerun of a stage spends more. If you want room for reruns, OpenRouter sells
10 credits as a one-time purchase, and that raises the allowance to 1,000 requests a day.
The purchase is optional.

`.env.example` in the repository has three provider blocks, and the OpenCode Zen block is
the active one when you receive it. In step 3 below, after `check.py` has created `.env`,
make the OpenRouter block the active one:

1. Put a `#` at the start of the three `LLM_` lines in the OpenCode Zen block.
2. Remove the `#` from the start of the three `LLM_` lines in the OpenRouter block.
3. Paste your key after `LLM_API_KEY=` in that block. Leave the model name as it is:
   `nvidia/nemotron-3.5-lightning:free`.

Exactly one block has lines without a `#` when you are done.

## 3. The packages and the check

This folder has its own virtual environment, so the packages you installed for the chatbot
course are not available in it. The third command below installs them again and adds two
new packages: `ddgs`, which searches the web, and `beautifulsoup4`, which turns a web page
into plain text.

At the repository folder, one command at a time:

`python3 -m venv .venv`
`source .venv/bin/activate`
`pip install -r requirements.txt`
`python check.py`

The first run of `check.py` creates `.env`. Edit it as step 2 says, then run
`python check.py` again. The last line should read "Your laptop is ready. Models
available:" followed by model names. Post a screenshot of the `check.py` lines in the class
channel at least two days before the session. If a line says what to fix, the README's
"Before the session" section has the fix for each line; fix it and run `check.py` again.

The virtual environment is on only in the terminal where you switched it on. The prompt
starts with `(.venv)` while it is on. If a terminal still has the chatbot course's virtual
environment on, `check.py` says so; run `deactivate`, then `source .venv/bin/activate` in
this folder.

## 4. The glossary and the quiz

1. Open `stage-guide.html` in your browser and read its first section, the glossary. It
   defines the words the session uses, and the session does not test you on them.
2. Answer the four questions in `pre-session-quiz.md` and send them as that file says.

## 5. The tutor

OpenCode is the course tutor. It answers questions, explains the scripts and reads errors
with you; it does not write code. `ask-the-tutor.md` in the repository shows how to ask.

The course runs on OpenCode version 2.2.5. Open a terminal, inside WSL on Windows, and run
`opencode --version`. If it prints `opencode v2.2.5`, the tutor is installed. If it prints
nothing, or a number that starts with 1, install version 2.2.5 with this one command:

`curl -fsSL https://opencode.ai/v2/install | bash -s -- --version 2.2.5`

The command replaces an older OpenCode. If Homebrew installed your OpenCode for the chatbot
course, run `brew uninstall opencode` first. Install with the command above; the Download
buttons on the OpenCode website install a desktop application that the course does not
use. Close the terminal, open a new one, and run `opencode --version` again.

The tutor runs on Gemini: create a free key at https://aistudio.google.com/app/apikey,
run `opencode auth login`, choose Google, choose API key and paste the key. If you
connected the Google provider for the chatbot course, it is still connected. This key is
separate from the OpenRouter key in section 2.

Start the tutor with `opencode` at the repository folder. Inside it, `/explain`, `/quiz`
and `/error` are the three course commands.

## On the day

Bring the laptop charged, with the repository folder open in VS Code and a terminal whose
prompt shows `(.venv)` at that folder. The session starts with `python check.py`.
