# Testing agent PYTHON

## High level idea:

- Prepare custom env with preinstalled python, repo and packages
- Run the code
- Report errors to LLM
- Edit files
- Repeat 2nd step

## Packages
- Pytest
- OpenAI GPT-4

## Detailed steps for the agent loop:
- Run the code
- Collect failed tests with errors (function body + errors)
- Pass failed tests to GPT-4 and ask for files to get for debugging
- Send files to LLM for review and apply code from LLM
- Save files
- Run code again
