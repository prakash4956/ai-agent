---
name: stage-0
description: Course notes for stage 0 of the agent course (check.py): what the stage adds, the predict question, the expected behaviour and the common fixes. Load when the learner asks about stage 0 or about check.py.
metadata:
  opencode/autoinvoke: "true"
---
# Stage 0: check.py

## What this stage adds

Create .env on the first run and check Python, the folder, the five packages and the key. Two packages are new in this course: ddgs searches the web with no key, and beautifulsoup4 (imported as bs4) turns a web page into plain text.

## The predict question

Which line will the script print last: A, the key reaches a model and the model list is printed; B, a package is missing; C, a value in .env is empty?

## What the learner should see

'Your laptop is ready. Models available:' followed by five model names. If the name in .env is not one of them, the learner changes it to one that is. Exactly one provider block in .env has no # signs; the instructor's note says which block to use.

## Common messages and what they mean

- 'the virtual environment is not on' means the Python that ran is not the one in .venv. Run source .venv/bin/activate, then python check.py again.
- 'a virtual environment is on, but it belongs to another folder' means the terminal still has the chatbot course's .venv switched on; the prompt shows (.venv) for both. Run deactivate, then source .venv/bin/activate in this folder, then python check.py again.
- 'too old. The course needs Python 3.10 or newer' means the Python in the virtual environment is older than 3.10.
- 'this is the Windows side' means the repository is under /mnt/c/; it must be in the WSL home folder.
- 'Package missing: ddgs' or 'bs4' means the two new packages are not installed in this environment: pip install -r requirements.txt inside the virtual environment.
- 'LLM_API_KEY is not set yet' means the key line in the active block still reads paste-.
- 'The provider refused the key' means the key is wrong or expired, or the three active lines belong to two different blocks.
