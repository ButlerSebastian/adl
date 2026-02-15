# Schema Reference

This document summarizes the main fields from `schema/agent-definition.schema.json`.

## Agent (root object)

- `id` (string, optional): Unique identifier for this agent (e.g., UUID).
- `version` (integer, optional): Version number of this specific agent definition. For semantic versioning, use `version_string`.
- `version_string` (string, optional): Semantic version string (e.g., '1.2.0') for the agent definition.
- `lifecycle` (string, optional): Lifecycle status of this agent version. Values: `stable`, `beta`, `deprecated`, `experimental`.
- `compatibility` (object, optional): Compatibility information for this agent version.
  - `adl_spec` (string, optional): Minimum ADL spec version required (e.g., '>=1.0.0').
  - `previous_versions` (array of string, optional): List of compatible previous version patterns.
- `change_log` (object, optional): Change log information for this version.
  - `type` (string, **required**): Type of change. Values: `breaking`, `non-breaking`, `patch`.
  - `summary` (string, optional): Human-readable summary of changes.
  - `details` (array of string, optional): Detailed list of changes.
- `name` (string, **required**): Human-readable name of the agent.
- `description` (string, **required**): Long-form description of the agent's purpose.
- `role` (string, **required**): Short role label (e.g., "Creative Producer").
- `llm` (string, **required**): LLM provider or family (e.g., "openai").
- `llm_settings` (object, **required**):
  - `temperature` (number): Sampling temperature (>= 0).
  - `max_tokens` (integer): Maximum tokens to generate.
- `owner` (string, optional): Owner or namespace.
- `document_index_id` (string, optional): Primary RAG index ID.
- `rag` (array of `RagIndex`, optional): Associated indices.
- `tools` (array of `ToolDefinition`, **required**): Tools this agent can call.
- `memory` (object, optional): Memory configuration for the agent.
  - `type` (string, optional): Type of memory system. Values: `episodic`, `semantic`, `working`, `hybrid`.
  - `scope` (string, optional): Scope of memory visibility. Values: `session`, `user`, `org`, `global`.
  - `backend` (string, optional): Backend storage type. Values: `vector`, `kv`, `graph`, `external`.
  - `retention` (object, optional): Retention policy for memory data.
    - `policy` (string, **required**): Retention policy type. Values: `ttl`, `versioned`, `append-only`.
    - `duration` (string, optional): Duration for retention (e.g., '30d', '7d', '1h').
  - `write_policy` (string, optional): When memory writes occur. Values: `explicit`, `implicit`.
  - `read_policy` (string, optional): When memory reads occur. Values: `on_demand`, `always`.
  - `privacy` (object, optional): Privacy and security settings.
    - `pii` (boolean, optional): Whether memory may contain PII.
    - `encryption` (boolean, optional): Whether memory data should be encrypted at rest.

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
- `category` (string, optional): Optional hierarchical category ID following taxonomy specification (e.g., 'data_access.database.query', 'ai_ml.image_generation.text_to_image'). Pattern: `^[a-z_]+(?:\.[a-z_]+){1,3}$`
- `subcategory` (string, optional): Optional subcategory for specific implementation (e.g., 'sql', 'dalle', 'postgresql'). Pattern: `^[a-z0-9_-]+$`
- `parameters` (array of `ToolParameter`, **required**):
  - `name` (string, **required**)
  - `type` (string, **required**)
  - `description` (string, **required**)
  - `required` (boolean, optional, default false)
  - `default` (any, optional)
  - `format` (string, optional): String format validation (email, uri, uuid, date-time, ipv4, ipv6)
  - `pattern` (string, optional): Regex pattern for string validation
  - `minLength` (integer, optional): Minimum string length
  - `maxLength` (integer, optional): Maximum string length
  - `minimum` (number, optional): Minimum numeric value
  - `maximum` (number, optional): Maximum numeric value
  - `exclusiveMinimum` (number, optional): Exclusive minimum bound
  - `exclusiveMaximum` (number, optional): Exclusive maximum bound
  - `multipleOf` (number, optional): Value must be multiple of this number
  - `enum` (array, optional): Allowed values
  - `items` (object, optional): Schema for array items
  - `minItems` (integer, optional): Minimum array length
  - `maxItems` (integer, optional): Maximum array length
  - `uniqueItems` (boolean, optional): Array items must be unique
  - `properties` (object, optional): Object property schemas
  - `required_properties` (array of string, optional): Required object properties
  - `additionalProperties` (boolean, optional): Allow extra properties in objects
  - `anyOf` (array, optional): Schema must match at least one
  - `oneOf` (array, optional): Schema must match exactly one
  - `allOf` (array, optional): Schema must match all
- `returns` (object, optional): Standardized return type schema
  - `type` (string, **required**): Return type category. Values: ObjectResult, EntityResult, OperationStatus, StringValue, NumberValue, BooleanValue, IdentifierValue, ListResult, BatchResult, FileResult, MediaResult, EventStream, ChunkedData, VoidResult, Custom
  - `schema` (object or string, **required**): JSON Schema or URI reference to schema definition
  - `description` (string, optional): Human-readable description of the return value
  - `examples` (array, optional): Example return values
  - `content_type` (string, optional): MIME type of the return value (default: application/json)
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

## v1.5 New Features

This version introduces three major enhancements to the ADL specification:

1. **Tool Category Taxonomy**: Hierarchical categorization system for tools with pattern validation. See [Tool Category Taxonomy](tool-category-taxonomy.md).

2. **Enhanced Type System**: Comprehensive parameter constraints including string formats, numeric ranges, array constraints, and object schemas. See [Enhanced Type System](enhanced-type-system.md).

3. **Return Type System**: Standardized return type schemas with 15 predefined categories and structured error handling. See [Return Type System](return-type-system.md).

## Versioning Guidelines (Summary)

- Use **semantic versioning** for repository tags (MAJOR.MINOR.PATCH).
- Use the agent-level `version` field to track revisions of your own agent definitions.
- Avoid breaking changes where possible; when necessary, document them clearly and bump MAJOR.

For detailed contribution and versioning workflow, see `CONTRIBUTING.md`.
