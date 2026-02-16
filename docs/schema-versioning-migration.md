# ADL Schema Versioning

## Current Version: 2.0.0

This document describes the ADL schema versioning strategy and provides migration guidance for version upgrades.

## Versioning Strategy

ADL uses **semantic versioning** (MAJOR.MINOR.PATCH) to track schema evolution:

- **MAJOR (X.0.0)**: Breaking changes that require migration
  - Schema structure changes
  - Field renames or removals
  - Type changes that break compatibility
  - Required field additions

- **MINOR (x.Y.0)**: New features, backward compatible
  - New optional fields
  - New property groups
  - New validation rules that don't break existing schemas
  - New $defs definitions

- **PATCH (x.y.Z)**: Bug fixes, backward compatible
  - Schema validation improvements
  - Documentation updates
  - Minor type refinements

## Version Field

Every ADL agent definition must include a `schema_version` field at the top level:

```json
{
  "schema_version": "2.0.0",
  "identity": { ... },
  "llm": { ... },
  ...
}
```

### Schema Version Field Specification

```json
"schema_version": {
  "type": "string",
  "pattern": "^\\d+\\.\\d+\\.\\d+$",
  "description": "Version of the ADL schema used for this agent definition",
  "default": "2.0.0"
}
```

**Requirements:**
- Must be a string following semantic versioning format
- Must be included in all agent definitions
- Default value is "2.0.0" for new definitions
- Must be added to the `required` fields array

## Migration Guide

### From v1.x to v2.0.0

The v2.0.0 schema introduces several significant changes:

#### Breaking Changes

1. **Grouped Structure (Recommended)**
   - New recommended structure with grouped fields
   - Old flat structure still supported for backward compatibility

2. **Required Fields**
   - Added `schema_version` as a required field
   - All agent definitions must include version information

3. **Identity Field Changes**
   - `agent_id` is now required (replaces deprecated `id`)
   - `version_string` added for semantic versioning
   - `lifecycle` field added for version status

#### Migration Steps

**Step 1: Add schema_version Field**

```json
{
  "schema_version": "2.0.0",
  "agent_id": "550e8400-e29b-41d4-a716-446655440000",
  "name": "My Agent",
  "description": "Agent description",
  "llm": { ... },
  "tools": [ ... ]
}
```

**Step 2: Update Identity Structure**

```json
{
  "identity": {
    "agent_id": "550e8400-e29b-41d4-a716-446655440000",
    "name": "My Agent",
    "description": "Agent description",
    "version_string": "1.0.0",
    "lifecycle": "stable"
  },
  "llm": { ... },
  "tools": [ ... ]
}
```

**Step 3: Choose Structure Type**

**Option A: Grouped Structure (Recommended)**
```json
{
  "schema_version": "2.0.0",
  "identity": { ... },
  "llm": { ... },
  "capabilities": { ... },
  "governance": { ... },
  "orchestration": { ... },
  "metadata": { ... }
}
```

**Option B: Flat Structure (Deprecated)**
```json
{
  "schema_version": "2.0.0",
  "agent_id": "...",
  "name": "...",
  "description": "...",
  "llm": { ... },
  "tools": [ ... ],
  "rag": [ ... ],
  "memory": { ... },
  ...
}
```

### Future Version Migrations

When a new major version is released (e.g., v3.0.0), follow these steps:

#### 1. Review Breaking Changes

Check the release notes for:
- New required fields
- Deprecated fields
- Type changes
- Structure modifications

#### 2. Update schema_version

```json
{
  "schema_version": "3.0.0",
  ...
}
```

#### 3. Apply Migration Rules

**For Required Field Additions:**
```json
{
  "schema_version": "3.0.0",
  "new_required_field": "value",
  ...
}
```

**For Field Renames:**
```json
{
  "schema_version": "3.0.0",
  "old_field_name": "value",  // Deprecated
  "new_field_name": "value"   // New field
}
```

**For Type Changes:**
```json
{
  "schema_version": "3.0.0",
  "field": {
    "type": "new_type",
    "properties": { ... }
  }
}
```

#### 4. Validate

Use the ADL validator to ensure compliance:
```bash
adl-validate my-agent.json
```

#### 5. Test

Test your agent definition with the new schema version to ensure:
- All required fields are present
- Type constraints are met
- Validation rules pass
- Agent behavior is correct

## Version Compatibility

### Minimum ADL Spec Version

The `governance.compatibility.adl_spec` field specifies the minimum ADL spec version required:

```json
{
  "governance": {
    "compatibility": {
      "adl_spec": ">=2.0.0"
    }
  }
}
```

### Version Compatibility Matrix

| Schema Version | Minimum ADL Spec | Notes |
|----------------|------------------|-------|
| 2.0.0 | 2.0.0 | Current version |
| 1.x.x | 1.0.0 | Legacy versions |

## Best Practices

1. **Always Include schema_version**
   - Never omit the version field
   - Use the latest stable version

2. **Use Semantic Versioning**
   - Follow MAJOR.MINOR.PATCH format
   - Communicate breaking changes clearly

3. **Document Changes**
   - Update CHANGELOG for each version
   - Provide migration guides for major versions

4. **Test Thoroughly**
   - Validate after each migration
   - Test agent behavior with new schema

5. **Plan for Deprecation**
   - Announce deprecated fields in advance
   - Provide migration paths
   - Remove deprecated fields in next major version

## Version History

### v2.0.0 (Current)
- Added schema_version field
- Introduced grouped structure (recommended)
- Maintained flat structure for backward compatibility
- Enhanced identity field with lifecycle status
- Added governance compatibility checks

### v1.x.x (Legacy)
- Flat structure only
- No schema versioning
- Basic identity and capabilities

## Support

For questions about schema versioning or migration:
- Check the [ADL Documentation](../README.md)
- Review [Migration Guides](./migration-v1.5.md)
- Open an issue on [GitHub](https://github.com/nextmoca/adl/issues)