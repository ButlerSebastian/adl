# Agent Definition Language Overview

The Agent Definition Language (ADL) is a JSON-based format for:

- Defining agents (`name`, `role`, `description`, `llm`, `llm_settings`)
- Declaring tools the agent can call, including:
  - Parameters and return types
  - Runtime dependencies
  - Permissions (network, file IO, env vars)
- Registering RAG indices the agent can query

## Core Concepts

### Agent

An **agent** wraps:

- Identity (`id`, `name`, `description`, `role`)
- Runtime model config (`llm`, `llm_settings`)
- Optional RAG indices (`rag`)
- Tools it can invoke (`tools`)

### Tool

A **tool** is a callable capability the agent can use during reasoning and execution.

- `name` — machine-readable identifier used to invoke the tool
- `description` — natural language description used in prompts
- `parameters` — structured input schema
- `returns` (optional) — description of the output
- `dependencies` (optional) — runtime dependencies, e.g., pip packages
- `permissions` (optional) — sandbox and security boundaries
- `invocation` — how to call the tool (e.g., `python_function`)

### RAG Index

A **RAG index** represents a logical corpus the agent may query, with type (`rag_type`), virtual path,
and optional remote backing store.

See `schema/agent-definition.schema.json` for the canonical specification.
