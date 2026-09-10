# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo is

Teaching material for a GenAI/LLM foundations course (University of Buckingham), covering the OpenAI API from a single completion call up to a LangGraph agent.

- `presentation/demo.ipynb` — the single live-teaching notebook, and the only content left in this repo. This is the primary artifact: one continuous, sequential notebook meant to be run top-to-bottom in one kernel session (later sections reuse `client`, and variable names like `system_prompt`/`messages` from earlier sections — don't assume a section is independently runnable).
- `presentation/images/` — diagrams shown inline in `demo.ipynb` via `<img>` markdown cells.

There used to be a `notebooks/` folder with numbered standalone lesson scripts (`L1.py`–`L7.py`) that `demo.ipynb` was originally assembled from, and a `presentation/solution/` folder of separate worked-example notebooks — both have been deleted as redundant. `demo.ipynb` is now the only copy of this content — don't recreate the old per-lesson `.py` files or a separate solutions folder.

## Commands

Dependency management is Poetry (`pyproject.toml` + `poetry.lock`, `package-mode = false`, Python >=3.12,<3.14).

```bash
poetry install                # install/sync dependencies
poetry run jupyter lab        # open presentation/demo.ipynb
```


## Architecture: `presentation/demo.ipynb` section by section

Prompts are defined inline as Python string literals in the cell that uses them (not loaded from files) — that's deliberate for a presentation, keep it that way rather than reintroducing a `prompts/*.txt` + file-loader pattern.

1. **Basic LLM Interaction** — bare `client.responses.create(model=..., input=...)` call, no system prompt.
2. **Advanced Prompting** — introduces a system prompt (inline "Advanced Mathematics Tutor" persona with explicit chain-of-thought instructions) via `messages = [{"role": "system", ...}, {"role": "user", ...}]`, then `client.responses.create(input=messages)`.
3. **Structured Outputs** — a different inline system prompt (meeting-request extraction) + a Pydantic `LectureSchedule` model, called via `client.responses.parse(text_format=LectureSchedule)`.
4. **Tool Use** — defines a `tools` schema (`get_weather`), calls `client.responses.create(tools=tools, ...)`, dispatches on `response.output` items of type `function_call`, feeds `function_call_output` back into `input_list` for a follow-up call. `gpt-5.6-luna` is a reasoning model, so `response.output` also contains a `ResponseReasoningItem` alongside the function call — the dispatch loop only acts on `function_call` items and passes the rest through unchanged, which is correct.
5. **State Graphs** — the same math-tutor persona rebuilt as a one-node LangGraph `StateGraph` (`TutorState` → `answer_question` → `END`) using `langchain_openai.ChatOpenAI` instead of the raw `openai` client. Uses current LangGraph API conventions: `graph.add_edge(START, "answer_question")` (not the older `set_entry_point`), and the `ChatOpenAI` instance is built once at module/cell scope and reused by the node function rather than reconstructed per invocation. A markdown cell ahead of this section explains what LangGraph/`StateGraph` are for readers new to it.

The model used throughout is `gpt-5.6-luna`.
