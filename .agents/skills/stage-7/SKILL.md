---
name: stage-7
description: Course notes for stage 7 of the agent course (05_frameworks/langchain_agent.py): what the file shows, where each of the seven parts is, how to run it at home and the common fixes. Load when the learner asks about stage 7, LangChain, the framework file or create_agent.
metadata:
  opencode/autoinvoke: "true"
---
# Stage 7: 05_frameworks/langchain_agent.py

## What this stage adds

The same agent written with LangChain in about 25 lines, read in the session and run at home. The model comes from init_chat_model with the three .env values. The two tools are the same functions with the @tool decorator, and the docstring is the description the model reads. create_agent holds the model deciding, the loop, the state and the stop condition in one call. The goal is the one message passed to invoke, and the recursion limit is 20. Evaluation is absent. The framework calls the model with the provider's native tool-calling feature. The descriptions are sent as a field of the request, and the action comes back as a field; that is the mechanism from stage 3 moved into the request format.

## Where the seven parts are

Model: the init_chat_model line. Goal: the message passed to invoke. Tools: the two @tool functions and the tools argument. State: hidden, the framework's own list, readable afterwards as result["messages"]. Loop: hidden, inside create_agent and invoke. Stop condition: hidden, partly visible as recursion_limit. Evaluation: absent. What the learner cannot see when a run goes wrong: the trace, the step count and the state, unless the framework's messages list is printed.

## Running it at home

pip install -r requirements-frameworks.txt inside the virtual environment, then python 05_frameworks/langchain_agent.py from the repository root. The versions are pinned to the ones that ran in the dry run.

## Common messages and what they mean

- 'ModuleNotFoundError: No module named langchain' means the framework requirements are not installed in this environment, or the virtual environment is not on.
- 'GraphRecursionError: Recursion limit of 20 reached without hitting a stop condition' means the model kept asking for tools; each model call and each tool run counts as one. Run again, or raise the number in the config line; that is the hidden stop condition firing.
- A report about a wrong month means the system prompt's date line is missing or the model ignored it; the stage scripts have the same line.
- An error that names tool_calls or function calling means the chosen model does not support native tool calling; pick another model name from the check.py list.
