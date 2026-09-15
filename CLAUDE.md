# CLAUDE.md

Guidance for Claude Code in this repo.

## Repo

Teaching material, GenAI/LLM foundations course (University of Buckingham). OpenAI API basics through LangGraph agent.

- `presentation/demo.ipynb` — single live-teaching notebook, only content in repo. Run top-to-bottom, one kernel session: later sections reuse `client` and vars (`system_prompt`, `messages`) from earlier ones, not independently runnable.
- `presentation/images/` — diagrams, shown inline via `<img>` markdown cells.

No test suite, no lint config, no deploy target.

## Commands

Poetry, `package-mode = false`, Python >=3.12,<3.14.

```bash
poetry install
poetry run jupyter lab   # presentation/demo.ipynb
```

## Notebook sections

Prompts are inline Python string literals in the cell that uses them, not loaded from files — keep it that way.

1. **Basic call** — `client.responses.create`, no system prompt.
2. **Advanced prompting** — system prompt (math tutor persona, chain-of-thought) + `messages` list.
3. **Structured outputs** — Pydantic `LectureSchedule`, `client.responses.parse(text_format=LectureSchedule)`.
4. **Tool use** — `get_weather` tool schema, dispatch on `function_call` items in `response.output`, feed `function_call_output` back via `input_list`. Model also emits `ResponseReasoningItem` alongside the function call; dispatch loop only acts on `function_call`, passes the rest through unchanged — correct as is.
5. **State graphs** — same tutor persona as a one-node LangGraph `StateGraph` (`TutorState` → `answer_question` → `END`), using `langchain_openai.ChatOpenAI`. Current API: `graph.add_edge(START, "answer_question")`, `ChatOpenAI` built once at cell scope and reused.

Model throughout: `gpt-5.6-luna`.
