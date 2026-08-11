# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project overview

This is an early-stage LLM experimentation project. Despite the repo name (`aws_bedrock`), the current code does not call AWS Bedrock — it uses `langchain_google_genai` (Gemini) via LangChain. The `requirements.txt` includes `boto3`, `bedrock-agentcore`, `chromadb`, `langgraph`, `streamlit`, and other libraries not yet wired into any code, suggesting the project is expected to grow into a broader agentic/RAG setup.

## Running the code

There is no build step, test suite, or linter configured yet.

```bash
python main.py
```

Note: `main.py` only imports `call_google_genai` from `SimpleLlmCall/call_llm.py` — it does not currently invoke it. The module-level call at the bottom of `SimpleLlmCall/call_llm.py` (`call_google_genai()`) executes on import, so simply importing that module runs the LLM call.

### Environment

- Dependencies are pinned in `requirements.txt` (install with `pip install -r requirements.txt`). A `env/` virtualenv directory exists locally but is gitignored.
- Secrets live in `.env` (gitignored) and are loaded via `python-dotenv`. Required keys: `GOOGLE_API_KEY` (used by `SimpleLlmCall/call_llm.py`), `HF_TOKEN` (present but not yet referenced in code).

## Architecture

- `main.py` — entry point; loads `.env` and imports the LLM call module.
- `SimpleLlmCall/call_llm.py` — builds a `ChatGoogleGenerativeAI` client (model `gemini-flash-latest`) and invokes it with a system/user message pair. It reads user content from `datas/sample_blood_test.txt` via `file_open()`, which truncates input to the first 900 characters.
- `Prompts/prompts_call_llm.py` — holds prompt strings (`SYSTEM_PROMPT`, `USER_PROMPTS`) separately from the calling code, so prompts can be edited without touching call logic. Follow this separation when adding new prompts.
- `datas/` — sample input files (e.g. a synthetic blood test report) used as LLM input during local testing.

When adding a new LLM call, mirror the existing pattern: define prompts in `Prompts/`, put the call logic in its own module (like `SimpleLlmCall/`), and load config/secrets via `dotenv` + `os.getenv`.
