# Schema Migration Guide v2.0

**Date**: 2026-02-16
**Version**: 2.0
**Status**: Recommended for adoption

---

## Overview

The ADL schema has been reorganized to reduce complexity and improve developer experience. The new schema uses grouped fields with `$ref` references, reducing the top-level properties from 25 to 5 logical groups.

## Key Changes

### Before (v1.x - Flat Structure)

```json
{
  "agent_id": "...",
  "id": "...",
  "version": 1,
  "version_string": "1.0.0",
  "lifecycle": "...",
  "compatibility": { ... },
  "change_log": { ... },
  "name": "...",
  "description": "...",
  "role": "...",
  "agent_roles": { ... },
  "llm": "...",
  "llm_settings": { ... },
  "owner": "...",
  "document_index_id": "...",
  "rag": [ ... ],
  "tools": [ ... ],
  "memory": { ... },
  "execution_constraints": { ... },
  "events": [ ... ],
  "rag_extensions": { ... },
  "memory_extensions": { ... },
  "llm_extensions": { ... },
  "workflow": { ... },
  "policy": { ... }
}
```

### After (v2.0 - Grouped Structure)

```json
{
  "identity": {
    "agent_id": "...",
    "name": "...",
    "description": "...",
    "version": "1.0.0",
    "lifecycle": "...",
    "owner": "..."
  },
  "llm": {
    "provider": "...",
    "settings": { ... },
    "extensions": { ... }
  },
  "capabilities": {
    "tools": [ ... ],
    "rag": [ ... ],
    "memory": { ... },
    "document_index_id": "...",
    "execution_constraints": { ... },
    "events": { ... },
    "rag_extensions": { ... },
    "memory_extensions": { ... }
  },
  "governance": {
    "permissions": { ... },
    "audit": true,
    "compatibility": { ... },
    "change_log": { ... },
    "policy": { ... }
  },
  "orchestration": {
    "workflow": { ... },
    "policy": { ... },
    "role": "...",
    "agent_roles": { ... }
  }
}
```

## Migration Strategy

### Option 1: Use New Structure (Recommended)

The new grouped structure is recommended for all new ADL definitions. It provides:

- **Better organization**: Logical grouping of related fields
- **Improved readability**: Easier to understand the structure
- **Reduced cognitive load**: Fewer top-level properties to navigate
- **Future-proof**: Easier to extend and maintain

### Option 2: Maintain Old Structure (Backward Compatible)

The old flat structure is still supported for backward compatibility. Existing ADL files will continue to work without modification.

## Field Mapping

### Identity Group

| Old Field | New Field | Notes |
|-----------|-----------|-------|
| `agent_id` | `identity.agent_id` | Required |
| `id` | `identity.id` | Deprecated, use `agent_id` |
| `version` | `identity.version` | Integer version |
| `version_string` | `identity.version_string` | Semantic version |
| `lifecycle` | `identity.lifecycle` | Lifecycle status |
| `name` | `identity.name` | Required |
| `description` | `identity.description` | Required |
| `owner` | `identity.owner` | Optional |

### LLM Group

| Old Field | New Field | Notes |
|-----------|-----------|-------|
| `llm` | `llm.provider` | Required |
| `llm_settings` | `llm.settings` | Required |
| `llm_extensions` | `llm.extensions` | Optional |

### Capabilities Group

| Old Field | New Field | Notes |
|-----------|-----------|-------|
| `tools` | `capabilities.tools` | Required |
| `rag` | `capabilities.rag` | Optional |
| `memory` | `capabilities.memory` | Optional |
| `document_index_id` | `capabilities.document_index_id` | Optional |
| `execution_constraints` | `capabilities.execution_constraints` | Optional |
| `events` | `capabilities.events` | Optional |
| `rag_extensions` | `capabilities.rag_extensions` | Optional |
| `memory_extensions` | `capabilities.memory_extensions` | Optional |

### Governance Group

| Old Field | New Field | Notes |
|-----------|-----------|-------|
| `compatibility` | `governance.compatibility` | Optional |
| `change_log` | `governance.change_log` | Optional |
| `policy` | `governance.policy` | Optional |
| `permissions` | `governance.permissions` | Optional (new) |
| `audit` | `governance.audit` | Optional (new) |

### Orchestration Group

| Old Field | New Field | Notes |
|-----------|-----------|-------|
| `workflow` | `orchestration.workflow` | Optional |
| `policy` | `orchestration.policy` | Optional |
| `role` | `orchestration.role` | Optional |
| `agent_roles` | `orchestration.agent_roles` | Optional |

## Migration Examples

### Example 1: Simple Agent

**Before:**
```json
{
  "agent_id": "agent-123",
  "name": "My Agent",
  "description": "A simple agent",
  "llm": "openai",
  "llm_settings": {
    "temperature": 0.7,
    "max_tokens": 4096
  },
  "tools": [
    {
      "name": "tool1",
      "type": "function"
    }
  ]
}
```

**After:**
```json
{
  "identity": {
    "agent_id": "agent-123",
    "name": "My Agent",
    "description": "A simple agent"
  },
  "llm": {
    "provider": "openai",
    "settings": {
      "temperature": 0.7,
      "max_tokens": 4096
    }
  },
  "capabilities": {
    "tools": [
      {
        "name": "tool1",
        "type": "function"
      }
    ]
  }
}
```

### Example 2: Agent with Workflow

**Before:**
```json
{
  "agent_id": "agent-456",
  "name": "Workflow Agent",
  "description": "Agent with workflow",
  "llm": "openai",
  "llm_settings": {
    "temperature": 0.5,
    "max_tokens": 2048
  },
  "tools": [
    {
      "name": "tool1",
      "type": "function"
    }
  ],
  "workflow": {
    "name": "My Workflow",
    "version": "1.0.0",
    "nodes": { ... },
    "edges": [ ... ]
  }
}
```

**After:**
```json
{
  "identity": {
    "agent_id": "agent-456",
    "name": "Workflow Agent",
    "description": "Agent with workflow"
  },
  "llm": {
    "provider": "openai",
    "settings": {
      "temperature": 0.5,
      "max_tokens": 2048
    }
  },
  "capabilities": {
    "tools": [
      {
        "name": "tool1",
        "type": "function"
      }
    ]
  },
  "orchestration": {
    "workflow": {
      "name": "My Workflow",
      "version": "1.0.0",
      "nodes": { ... },
      "edges": [ ... ]
    }
  }
}
```

## Validation

### Using adl-validate

```bash
# Validate old structure (still supported)
adl-validate my-agent.json

# Validate new structure (recommended)
adl-validate my-agent-v2.json
```

### Using JSON Schema Validator

```bash
# Validate against v2 schema
python3 -c "
import json
from jsonschema import validate, ValidationError

with open('my-agent-v2.json') as f:
    agent = json.load(f)

# Validate against v2 schema
with open('schema/agent-definition.schema.json') as f:
    schema = json.load(f)

try:
    validate(instance=agent, schema=schema)
    print('✓ Valid')
except ValidationError as e:
    print(f'✗ Invalid: {e.message}')
"
```

## Breaking Changes

### Deprecated Fields

The following fields are deprecated but still supported:

- `id` - Use `agent_id` instead
- `version` - Use `version_string` for semantic versioning

### New Fields

The following new fields have been added:

- `governance.permissions` - Permissions and access control
- `governance.audit` - Audit logging flag

## Benefits

### For Developers

1. **Better Organization**: Fields are grouped logically
2. **Improved Readability**: Easier to scan and understand
3. **Reduced Cognitive Load**: Fewer top-level properties
4. **Better IDE Support**: Autocomplete and navigation improved

### For Maintainers

1. **Easier Maintenance**: Clear separation of concerns
2. **Better Documentation**: Each group has clear purpose
3. **Future-Proof**: Easier to extend and evolve
4. **Reduced Complexity**: Simpler schema structure

## Migration Timeline

### Phase 1: Backward Compatibility (Current)
- Old flat structure still supported
- New grouped structure available
- Migration guide provided

### Phase 2: Gradual Migration (Recommended)
- Update new ADL definitions to use grouped structure
- Update examples and templates
- Provide migration tools

### Phase 3: Deprecation (Future)
- Mark old structure as deprecated
- Provide deprecation warnings
- Plan for removal

## Support

For questions or issues related to schema migration:

1. Check this migration guide
2. Review the [ADL Documentation](../docs/)
3. Open an issue on GitHub
4. Contact the ADL team

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 2.0 | 2026-02-16 | Introduced grouped structure, backward compatibility |
| 1.x | Previous | Flat structure (deprecated) |

---

**Last Updated**: 2026-02-16
**Next Review**: After Phase 2 completion