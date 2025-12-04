# Schema Reference

This document summarizes the main fields from `schema/agent-definition.schema.json`.

## Agent (root object)

- `id` (string, optional): Unique identifier for this agent (e.g., UUID).
- `version` (integer, optional): Version number of this specific agent definition.
- `name` (string, **required**): Human-readable name of the agent.
- `description` (string, **required**): Long-form description of the agent’s purpose.
- `role` (string, **required**): Short role label (e.g., "Creative Producer").
- `llm` (string, **required**): LLM provider or family (e.g., "openai").
- `llm_settings` (object, **required**):
  - `temperature` (number): Sampling temperature (>= 0).
  - `max_tokens` (integer): Maximum tokens to generate.
- `owner` (string, optional): Owner or namespace.
- `document_index_id` (string, optional): Primary RAG index ID.
- `rag` (array of `RagIndex`, optional): Associated indices.
- `tools` (array of `ToolDefinition`, **required**): Tools this agent can call.

## RagIndex

- `id` (string, **required**): RAG index ID.
- `name` (string, **required**): Human-readable name.
- `rag_type` (string, **required**): Type of index (e.g., `doc`, `code`, `image`).
- `virtual_index_path` (string, **required**): Logical mount path.
- `location_type` (string, **required**): Location type (e.g., `local`, `s3`).
- `remote_path` (string or null, optional): Remote bucket/path.
- `metadata` (object, **required**): Free-form metadata map.

## ToolDefinition

- `id` (string, optional): Internal UUID for the tool.
- `tool_id` (string, optional): External catalog ID.
- `version` (integer, optional): Tool definition version.
- `name` (string, **required**): Code-facing name, used in invocation.
- `display_name` (string, optional): Human-friendly UI label.
- `description` (string, **required**): Rich description of what the tool does.
- `category` (string, optional): Category (e.g., "File Operations", "RAG").
- `parameters` (array of `ToolParameter`, **required**):
  - `name` (string, **required**)
  - `type` (string, **required**)
  - `description` (string, **required**)
  - `required` (boolean, optional, default false)
  - `default` (any, optional)
- `returns` (object, optional):
  - `type` (string, optional)
  - `description` (string, optional)
- `dependencies` (array of string, optional): e.g., pip packages.
- `keys_schema` (array of `KeySchemaItem`, optional):
  - `name` (string, **required**)
  - `description` (string, **required**)
  - `key_type` (string, **required**)
- `sources` (array of string, optional): Arbitrary sources, such as docs or URLs.
- `permissions` (object, optional):
  - `network` (boolean, optional)
  - `file_read` (array of string, optional)
  - `file_write` (array of string, optional)
  - `env_vars` (array of string, optional)
- `visibility` (string, optional): e.g., `public`, `private`.
- `status` (string, optional): e.g., `active`, `deprecated`.
- `code_file` (string, optional): Implementation file path.
- `created_by` (string, optional): Author or system.
- `created_at` (string, date-time, optional): ISO 8601 timestamp.
- `invocation` (object, required):
  - `type` (string, **required**): e.g., `python_function`.
  - `function` (string, optional): Name of the function to call.

## Versioning Guidelines (Summary)

- Use **semantic versioning** for repository tags (MAJOR.MINOR.PATCH).
- Use the agent-level `version` field to track revisions of your own agent definitions.
- Avoid breaking changes where possible; when necessary, document them clearly and bump MAJOR.

For detailed contribution and versioning workflow, see `CONTRIBUTING.md`.
