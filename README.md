# Build an autonomous AI agent in Python

This course builds a research agent in stages, from one call to a language model to a
program that searches the web, reads pages, stops when it has read enough, and measures its
own run. It continues the chatbot course: the same `.env`, the same client lines, the same
tutor.

> **Licence:** [PolyForm Noncommercial 1.0.0](LICENSE). You may use this repository freely for your own learning and for non-commercial teaching; you may not use it as the curriculum of a fee-charging course. [NOTICE.md](NOTICE.md) explains in plain English what is allowed.

Every command below is typed at this folder, the root of the repository. There is one `.env`
file, here at the root; `check.py` creates it on the first run, and every stage finds it.

## Before the session

Your laptop already has most of what this course needs from the chatbot course. The Python
packages are the exception, and the four commands at the end install them. Confirm each
line below, then run the four commands. Allow twenty minutes.

Confirm that you have:

- Windows only: WSL (Windows Subsystem for Linux) works, and VS Code opens a folder in it so
  that the bottom-left corner of the window reads "WSL: Ubuntu". Everything in this course
  happens inside WSL. A path that starts with `/mnt/c/` is the Windows side; do not use it.
- Python 3.10 or newer and git in the terminal you will use. `python3 --version` and
  `git --version` print their versions; `check.py` stops any older Python.
- A GitHub account, and a browser that is signed in to it.
- This repository, created from the course template with "Use this template" and cloned
  into your home folder: `/home/<you>/` in WSL, `/Users/<you>/` on macOS.
- A key for the provider named in `pre-session-note.md`, saved where you can copy it.
  `.env.example` has three provider blocks; exactly one is active, and the note says which
  and how to switch.
- The stage guide page, `stage-guide.html`, which you receive before the session, saved in
  this folder next to `check.py`. It is the worksheet for every stage, and `.gitignore`
  keeps it out of your pushes. Read its first section, the glossary, before the session.
- The four questions in `pre-session-quiz.md` answered and sent, as that file says.
- OpenCode version 2.2.5 installed in the same terminal (WSL for Windows), with the Google
  provider connected to a Gemini key, as `pre-session-note.md` says. `opencode --version`
  must print `opencode v2.2.5`; if it does not, install that version with this one command:
  `curl -fsSL https://opencode.ai/v2/install | bash -s -- --version 2.2.5`
  The tutor's rules are in `AGENTS.md` in this repository, and `opencode` once at this
  folder starts it.

This folder has its own virtual environment, so the packages you installed for the chatbot
course are not available in it. The third command below installs them again and adds two
new packages: `ddgs`, which searches the web, and `beautifulsoup4`, which turns a web page
into plain text.

Then, at this folder, one command at a time:

`python3 -m venv .venv`
`source .venv/bin/activate`
`pip install -r requirements.txt`
`python check.py`

`check.py` creates `.env` and prints one line for each thing it found. Open `.env`, paste
your key after `LLM_API_KEY=` in the active block, and run `python check.py` again. Post a
screenshot of those lines in the class channel at least two days before the session. If a
line says what to fix, fix it and run `check.py` again.

The virtual environment is on only in the terminal where you switched it on, and only
until that terminal is closed. The prompt starts with `(.venv)` while it is on. Every new
terminal tab needs the command `source .venv/bin/activate` again before any `python`
command; without it, macOS answers "command not found: python" and WSL answers "No module
named openai" or "No module named ddgs". A terminal that still has the chatbot course's virtual
environment on shows the same `(.venv)` prompt after you change folder; `check.py` reports
it, and the fix is `deactivate`, then the activate command again in this folder.

## The stages

| Stage | Run | What it adds |
|---|---|---|
| 0 | `python check.py` | Checks Python, the folder, the five packages and the key |
| 1 | `python stage1.py` | The research question as the only user entry; the model answers from its training data |
| 2 | `python stage2.py` | Two tools, `search_web` and `read_webpage`, called by the script itself, with no call to a model |
| 3 | `python stage3.py` | The model writes one action; the program runs it once |
| 4 | `python stage4.py` | The loop and the state; the run uses every step and writes no report |
| 5 | `python stage5.py` | The finish action; the brief with its source list |
| 6 | `python stage6.py` | Three checks on the run; one changed line makes the list honest |
| 7 | `05_frameworks/langchain_agent.py` | The same agent with LangChain, read in the session and run at home after `pip install -r requirements-frameworks.txt` |

Every stage from 1 works on the same question: "What is driving the gold price this month?"

Open `stage-guide.html` in your browser: it is the worksheet for every stage, with the
learning moment, the mental model, the new lines, the predict question with a reveal, and
the record you fill for that stage.

Each stage script starts with a header that says what the stage adds, why, and the question
to predict before you run. The lines marked `NEW in stage N` are the only lines that changed
from the previous stage. The script pauses once for your prediction, then runs.

## If the web is not available

`fixtures/` holds one saved search and the five saved pages on the course's question, in two files. If the
search service refuses your laptop, or the instructor says so, remove the `#` from the
`USE_FIXTURES=1` line in `.env`; both tools then read from that folder instead of the web.
The saved search returns the same five results whatever the query.

## After the session

`MODIFY.md` holds the take-home menu: make one of three changes to stage 6, run the
framework file, put the agent behind your chatbot's route and deploy it, and add a third tool
of your own.
