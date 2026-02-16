# ADL Naming Conventions

## Overview

This document defines the strict naming conventions for all ADL schema fields, ensuring consistency, readability, and interoperability across the ecosystem.

## Core Convention: Snake Case

All schema field names MUST follow **snake_case** naming convention:

- Use only lowercase letters
- Use underscores (`_`) to separate words
- No camelCase, PascalCase, or kebab-case
- No abbreviations unless they are industry-standard (e.g., `llm`, `rag`, `api`)

### Examples

✅ **Correct:**
```json
{
  "agent_id": "abc-123",
  "llm_settings": {
    "temperature": 0.7,
    "max_tokens": 4096
  },
  "rag_index_id": "index-001"
}
```

❌ **Incorrect:**
```json
{
  "agentId": "abc-123",           // camelCase
  "LLMSettings": {...},           // PascalCase
  "rag-index-id": "index-001",    // kebab-case
  "agentID": "abc-123"            // mixed case
}
```

## Field Naming Rules

### 1. Entity Fields

Fields representing entities or identifiers:
- Use `entity_id` or `id` for unique identifiers
- Use `entity_name` for human-readable names
- Use `entity_type` for classification

```json
{
  "agent_id": "agent-001",
  "agent_name": "Creative Producer",
  "agent_type": "producer"
}
```

### 2. Configuration Fields

Fields for configuration and settings:
- Use `config_` prefix for configuration objects
- Use `setting_` prefix for individual settings
- Use `options_` prefix for optional parameters

```json
{
  "llm_settings": {
    "temperature": 0.7,
    "max_tokens": 4096
  },
  "memory_config": {
    "type": "semantic",
    "scope": "user"
  }
}
```

### 3. Status and Lifecycle Fields

Fields representing status or lifecycle:
- Use `status` for current state
- Use `lifecycle` for lifecycle phase
- Use `state` for internal state

```json
{
  "status": "active",
  "lifecycle": "stable",
  "state": "ready"
}
```

### 4. Time and Date Fields

Fields for timestamps and durations:
- Use `_at` suffix for timestamps
- Use `_since` suffix for start times
- Use `_until` suffix for end times
- Use `_duration` suffix for durations

```json
{
  "created_at": "2026-02-15T10:30:00Z",
  "updated_at": "2026-02-15T11:45:00Z",
  "expires_at": "2026-03-15T00:00:00Z",
  "duration": "30d"
}
```

### 5. Collection Fields

Fields representing collections or arrays:
- Use plural nouns (e.g., `tools`, `rag_indices`)
- Use `items_` prefix for item-specific fields
- Use `count_` prefix for counts

```json
{
  "tools": [...],
  "rag_indices": [...],
  "item_count": 10,
  "items": [...]
}
```

### 6. Relationship Fields

Fields representing relationships:
- Use `_to_` or `_from_` for directional relationships
- Use `_related_` for related entities
- Use `_parent_` or `_child_` for hierarchy

```json
{
  "parent_id": "parent-001",
  "child_ids": ["child-001", "child-002"],
  "related_agents": [...]
}
```

### 7. Boolean Fields

Fields representing boolean values:
- Use `is_` or `has_` prefix for boolean checks
- Use `can_` prefix for capabilities
- Use `should_` prefix for recommendations

```json
{
  "is_active": true,
  "has_permissions": true,
  "can_execute": false,
  "should_encrypt": true
}
```

### 8. Type and Category Fields

Fields for type or category information:
- Use `_type` suffix for type
- Use `_category` suffix for categories
- Use `_kind` suffix for kinds

```json
{
  "agent_type": "producer",
  "memory_type": "semantic",
  "rag_type": "doc",
  "category": "ai_ml.image_generation"
}
```

### 9. Path and Location Fields

Fields for paths and locations:
- Use `_path` suffix for file paths
- Use `_location` suffix for locations
- Use `_uri` suffix for URIs

```json
{
  "code_path": "/path/to/code.py",
  "index_location": "s3://bucket/index",
  "api_uri": "https://api.example.com"
}
```

### 10. Metadata Fields

Fields for metadata:
- Use `metadata_` prefix for metadata objects
- Use `meta_` prefix for individual metadata items

```json
{
  "metadata": {
    "author": "John Doe",
    "version": "1.0.0"
  },
  "meta_author": "John Doe"
}
```

## Schema Definition Rules

### Property Names

- All property names in schema definitions MUST follow snake_case
- No camelCase or PascalCase in schema definitions
- Use descriptive, unambiguous names

### Required Fields

- Use `required` array for required fields
- Field names in `required` array MUST match property names exactly

### Reference Names

- `$defs` and `$ref` names MUST follow snake_case
- No camelCase or PascalCase in definition names

### Pattern Constraints

- Pattern strings MUST use snake_case for field names
- No camelCase in pattern definitions

## Validation Rules

### Field Name Validation

All field names MUST:
1. Be lowercase
2. Use only alphanumeric characters and underscores
3. Not start or end with an underscore
4. Not contain consecutive underscores
5. Not be empty

### Pattern Examples

✅ **Valid:**
- `agent_id`
- `llm_settings`
- `rag_index_id`
- `memory_config`
- `tool_parameters`

❌ **Invalid:**
- `agentID`
- `LLMSettings`
- `rag-index-id`
- `agent_id_`
- `_agent_id`
- `agent__id`

## Examples

### Complete Agent Definition

```json
{
  "agent_id": "agent-001",
  "agent_name": "Creative Producer",
  "agent_description": "Generates marketing images from creative briefs",
  "agent_role": "Creative Producer",
  "llm_provider": "openai",
  "llm_settings": {
    "temperature": 0.7,
    "max_tokens": 4096
  },
  "owner": "admin",
  "version": 1,
  "version_string": "1.0.0",
  "lifecycle": "stable",
  "compatibility": {
    "adl_spec": ">=1.0.0",
    "previous_versions": ["1.0.0"]
  },
  "change_log": {
    "type": "non-breaking",
    "summary": "Initial release",
    "details": ["Added basic image generation capabilities"]
  },
  "rag": [
    {
      "rag_index_id": "index-001",
      "rag_index_name": "Marketing Assets",
      "rag_type": "doc",
      "virtual_index_path": "/marketing",
      "location_type": "local",
      "remote_path": null,
      "metadata": {
        "category": "marketing"
      }
    }
  ],
  "tools": [
    {
      "tool_id": "tool-001",
      "tool_name": "generate_campaign_image",
      "tool_display_name": "Generate Campaign Image",
      "tool_description": "Generate high-quality images from prompts",
      "tool_category": "ai_ml.image_generation.text_to_image",
      "tool_subcategory": "dalle",
      "tool_parameters": [
        {
          "param_name": "prompt",
          "param_type": "string",
          "param_description": "Image prompt",
          "param_required": true,
          "param_min_length": 1,
          "param_max_length": 2000
        }
      ],
      "tool_returns": {
        "return_type": "MediaResult",
        "return_schema": { "$ref": "#/$defs/StandardReturnTypes/MediaResult" },
        "return_description": "Returns generated image with metadata"
      },
      "tool_invocation": {
        "invocation_type": "python_function",
        "invocation_function": "generate_image"
      }
    }
  ],
  "memory_config": {
    "memory_type": "semantic",
    "memory_scope": "user",
    "memory_backend": "vector",
    "memory_retention": {
      "retention_policy": "ttl",
      "retention_duration": "30d"
    },
    "memory_write_policy": "implicit",
    "memory_read_policy": "on_demand",
    "memory_privacy": {
      "memory_pii": false,
      "memory_encryption": true
    }
  }
}
```

## Compliance Checklist

When reviewing schema files:

- [ ] All property names use snake_case
- [ ] All `$defs` names use snake_case
- [ ] All `$ref` names use snake_case
- [ ] All pattern strings use snake_case
- [ ] No camelCase or PascalCase in field names
- [ ] No kebab-case in field names
- [ ] Required field names match property names exactly
- [ ] Field names are descriptive and unambiguous
- [ ] Field names follow the naming conventions above

## Tools and Validation

### Validation Scripts

- `./scripts/check-naming-conventions.sh` - Validates all schema files
- `jq` - JSON query tool for checking field names
- `ajv-cli` - JSON Schema validator

### Running Validation

```bash
# Check naming conventions
./scripts/check-naming-conventions.sh schema/

# Validate schema with ajv
ajv validate -s schema/agent-definition.schema.json -d examples/minimal_agent.json
```

## Migration Notes

### Breaking Changes

This naming convention is part of the ADL v1.5 specification. Existing implementations should:

1. Update field names to snake_case
2. Update all references and code
3. Test thoroughly after migration
4. Document breaking changes

### Backward Compatibility

For backward compatibility, consider providing:
- Field aliases for renamed fields
- Deprecation warnings for old field names
- Migration scripts to convert old field names

## References

- JSON Schema Specification: https://json-schema.org/
- Python Naming Conventions: https://peps.python.org/pep-0008/#naming-conventions
- JavaScript/TypeScript Naming Conventions: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Control_flow_and_error_handling#Statements

## Version History

- **v1.5** (2026-02-15): Initial naming convention specification
- **v1.5.1** (2026-02-16): Added specific analysis of agent-definition.schema.json naming patterns and inconsistencies

## Current Schema Analysis

### Agent Definition Schema (`schema/agent-definition.schema.json`)

The main agent definition schema follows these naming patterns:

#### ID Fields (Pattern: `*_id`)
- `agent_id` - Unique agent identifier
- `document_index_id` - RAG index identifier
- `workflow_id` - Workflow identifier
- `policy_id` - Policy identifier
- `node_id` - Workflow node identifier

#### Version Fields (Pattern: `version` or `version_string`)
- `version` - Integer version number
- `version_string` - Semantic version string
- `schema_version` - Schema version

#### Boolean Fields (Pattern: `is_*`, `has_*`, `can_*`)
- `is_active` - Active status
- `has_permissions` - Permission presence
- `can_execute` - Execution capability
- `enabled` - Enable/disable flag
- `audit` - Audit logging flag
- `require_encryption` - Encryption requirement
- `cost_tracking_enabled` - Cost tracking flag

#### Timestamp Fields (Pattern: `*_at`, `*_on`)
- `created_at` - Creation timestamp
- `updated_on` - Last update timestamp
- `expires_at` - Expiration timestamp

#### Array Fields (Pattern: Plural Nouns)
- `tools` - Array of tool definitions
- `rag` - Array of RAG index configurations
- `events` - Array of event definitions
- `permissions` - Array of permission definitions
- `constraints` - Array of constraint definitions
- `subscriptions` - Array of event subscriptions

#### Object Fields (Pattern: Descriptive Nouns)
- `identity` - Agent identity information
- `llm` - LLM configuration
- `capabilities` - Agent capabilities
- `governance` - Governance settings
- `orchestration` - Orchestration configuration
- `workflow` - Workflow definition
- `policy` - Policy definition

### Naming Inconsistencies Identified

#### 1. Boolean Field Pattern Variations
**Issue**: Boolean fields use multiple prefixes
- `is_*` prefix: `is_active`, `is_active` (in execution_constraints)
- `has_*` prefix: `has_permissions`, `has_permissions` (in execution_constraints)
- `can_*` prefix: `can_execute`, `can_execute` (in execution_constraints)
- Simple names: `enabled`, `audit`, `require_encryption`, `cost_tracking_enabled`

**Impact**: Inconsistent autocomplete and harder to predict field names

**Recommendation**: Standardize on one pattern for new fields:
- Use `is_*` for boolean checks (preferred)
- Use `has_*` for possession/capability checks
- Use `can_*` for permission checks
- Use simple names for enable/disable flags (e.g., `enabled`)

#### 2. Timestamp Field Pattern Variations
**Issue**: Timestamp fields use both `*_at` and `*_on` suffixes
- `*_at` suffix: `created_at`, `expires_at`, `updated_at`
- `*_on` suffix: `updated_on`

**Impact**: Inconsistent naming makes it harder to predict timestamp field names

**Recommendation**: Standardize on `*_at` suffix for all timestamp fields

#### 3. Deprecated Fields
**Issue**: The schema maintains deprecated fields for backward compatibility
- `id` (deprecated) → `agent_id` (current)
- `version` (in Identity) → `version_string` (current)

**Impact**: Confusion for users about which field to use

**Recommendation**: Mark deprecated fields clearly and provide migration guidance

### Field Naming Patterns Summary

| Pattern | Examples | Usage |
|---------|----------|-------|
| `*_id` | `agent_id`, `document_index_id`, `workflow_id` | Unique identifiers |
| `version` / `version_string` | `version`, `version_string`, `schema_version` | Version information |
| `is_*` | `is_active`, `is_active` | Boolean checks |
| `has_*` | `has_permissions`, `has_permissions` | Possession/capability |
| `can_*` | `can_execute`, `can_execute` | Permission checks |
| `*_at` | `created_at`, `expires_at` | Timestamps |
| `*_on` | `updated_on` | Timestamps (deprecated) |
| Plural nouns | `tools`, `rag`, `events` | Arrays |
| Descriptive nouns | `identity`, `llm`, `capabilities` | Objects |

### Guidelines for Future Additions

When adding new fields to the schema:

1. **Choose the Right Pattern**:
   - Use `*_id` for unique identifiers
   - Use `version` or `version_string` for version information
   - Use `is_*`, `has_*`, or `can_*` for boolean flags
   - Use `*_at` for timestamps (not `*_on`)
   - Use plural nouns for arrays

2. **Follow Snake Case**:
   - Use lowercase letters
   - Separate words with underscores
   - No camelCase or PascalCase

3. **Be Descriptive**:
   - Field names should clearly indicate their purpose
   - Include units in field names (e.g., `*_ms`, `*_mb`, `*_usd`)

4. **Consider Deprecated Fields**:
   - If renaming an existing field, mark the old field as deprecated
   - Provide a clear migration path
   - Document the deprecation in the schema

### Examples of Good Field Names

```json
{
  "agent_id": "uuid",
  "version_string": "1.2.0",
  "is_active": true,
  "has_permissions": true,
  "can_execute": false,
  "created_at": "2024-01-15T10:30:00Z",
  "max_execution_time_ms": 5000,
  "tools": [],
  "permissions": {}
}
```

### Examples of Bad Field Names

```json
{
  "agentID": "uuid",           // ❌ Should be snake_case
  "version": "1.2.0",          // ⚠️ Use version_string for semantic versions
  "active": true,              // ❌ Should be is_active
  "created": "2024-01-15",     // ❌ Should be created_at
  "maxTime": 5000,             // ❌ Should be max_execution_time_ms
  "toolList": [],              // ❌ Should be tools
  "perm": {}                   // ❌ Should be permissions
}
```