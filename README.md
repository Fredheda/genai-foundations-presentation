# GenAI Foundations Presentation

Teaching material for a GenAI/LLM foundations course (University of Buckingham), covering the OpenAI API from a single completion call up to a LangGraph agent.

## Contents

- `presentation/demo.ipynb` — the single live-teaching notebook. Meant to be run top-to-bottom in one kernel session; later sections reuse variables (`client`, `system_prompt`, `messages`) from earlier ones.
- `presentation/images/` — diagrams shown inline in the notebook.

## Notebook sections

1. **Basic LLM Interaction** — a bare `client.responses.create(...)` call, no system prompt.
2. **Advanced Prompting** — a system prompt (math tutor persona) + chat-style `messages`.
3. **Structured Outputs** — extracting a Pydantic model (`LectureSchedule`) from a meeting request via `client.responses.parse(...)`.
4. **Tool Use** — a `get_weather` tool schema, dispatched via `response.output` and fed back through `input_list`.
5. **State Graphs** — the math tutor rebuilt as a one-node LangGraph `StateGraph`.

## Setup

Dependencies are managed with Poetry (Python >=3.12,<3.14):

```bash
poetry install
```

Create a `.env` file in the repo root with:

```
OPENAI_API_KEY=...
```

## Running

```bash
poetry run jupyter lab        # open presentation/demo.ipynb
```