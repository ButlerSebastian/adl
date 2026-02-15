# Agent Definition Language Overview

The Agent Definition Language (ADL) is a JSON-based format for:

- Defining agents (`name`, `role`, `description`, `llm`, `llm_settings`)
- Declaring tools the agent can call, including:
  - Parameters and return types
  - Runtime dependencies
  - Permissions (network, file IO, env vars)
- Registering RAG indices the agent can query
- Configuring memory for stateful agent behavior
- Managing agent versioning and lifecycle

## Core Concepts

### Agent

An **agent** wraps:

- Identity (`id`, `name`, `description`, `role`)
- Runtime model config (`llm`, `llm_settings`)
- Optional RAG indices (`rag`)
- Tools it can invoke (`tools`)
- Optional memory configuration (`memory`)
- Versioning and lifecycle metadata (`version`, `version_string`, `lifecycle`, `compatibility`, `change_log`)

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

### Memory

**Memory** defines how an agent stores, retrieves, and governs state across interactions.

- `type` — memory system type: `episodic`, `semantic`, `working`, or `hybrid`
- `scope` — visibility and sharing: `session`, `user`, `org`, or `global`
- `backend` — storage type: `vector`, `kv`, `graph`, or `external`
- `retention` — data retention policy (TTL, versioned, append-only)
- `write_policy` — when writes occur: `explicit` or `implicit`
- `read_policy` — when reads occur: `on_demand` or `always`
- `privacy` — PII and encryption settings

Memory enables long-running agents, personalization, context continuity, and enterprise governance.

### Versioning

**Versioning** provides first-class support for agent evolution and lifecycle management.

- `version` — integer version number
- `version_string` — semantic version string (e.g., '1.2.0')
- `lifecycle` — status: `stable`, `beta`, `deprecated`, or `experimental`
- `compatibility` — ADL spec requirements and compatible previous versions
- `change_log` — change type (`breaking`, `non-breaking`, `patch`), summary, and details

Versioning enables safe upgrades, rollbacks, parallel deployments, and auditability.

See `schema/agent-definition.schema.json` for the canonical specification.
