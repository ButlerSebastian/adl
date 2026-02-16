# ADL Schema Redundant Fields Migration Guide

## Overview

This guide helps you migrate your ADL files to remove redundant fields from the schema. The changes were made to improve schema clarity, reduce redundancy, and provide a more consistent naming convention.

### Why the Changes Were Made

1. **Redundancy**: Multiple fields served similar purposes
2. **Ambiguity**: Inconsistent naming made it unclear which field to use
3. **Clarity**: Single, consistent field names provide better documentation

### What Changed

#### Field 1: `id` → `agent_id`
- **Before**: Generic `id` field for agent identification
- **After**: Specific `agent_id` field for agent identification
- **Impact**: Clearer intent, better IDE autocomplete

#### Field 2: `version` → `version_string`
- **Before**: Integer `version` field for versioning
- **After**: String `version_string` field for semantic versioning
- **Impact**: Supports semantic versioning (e.g., "1.2.0"), better for version comparisons

#### Field 3: `document_index_id` → `index_id` (in RAG)
- **Before**: `document_index_id` field for RAG index identification
- **After**: `index_id` field for RAG index identification
- **Impact**: Consistent naming with other entity IDs (workflow_id, policy_id, etc.)

---

## Detailed Changes

### Change 1: `id` → `agent_id`

#### Before
```json
{
  "id": "agent-001",
  "name": "My Agent",
  "version": 1,
  "version_string": "1.0.0"
}
```

#### After
```json
{
  "agent_id": "agent-001",
  "name": "My Agent",
  "version_string": "1.0.0"
}
```

#### Migration Steps
1. Rename top-level `id` field to `agent_id`
2. Remove `version` field (use `version_string` instead)
3. Update any code that references `agent.id` to use `agent.agent_id`

---

### Change 2: `version` → `version_string`

#### Before
```json
{
  "id": "agent-001",
  "name": "My Agent",
  "version": 1,
  "version_string": "1.0.0"
}
```

#### After
```json
{
  "agent_id": "agent-001",
  "name": "My Agent",
  "version_string": "1.0.0"
}
```

#### Migration Steps
1. Remove integer `version` field
2. Ensure `version_string` field is present with semantic version format (e.g., "1.2.0")
3. Update any code that compares versions to use string comparison

---

### Change 3: `document_index_id` → `index_id` (in RAG)

#### Before
```json
{
  "agent_id": "agent-001",
  "name": "My Agent",
  "rag": [
    {
      "id": "my-docs-index",
      "type": "vector"
    }
  ]
}
```

#### After
```json
{
  "agent_id": "agent-001",
  "name": "My Agent",
  "rag": [
    {
      "index_id": "my-docs-index",
      "type": "vector"
    }
  ]
}
```

#### Migration Steps
1. Find all RAG index objects with `id` field
2. Rename `id` to `index_id`
3. Update any code that references `rag[0].id` to use `rag[0].index_id`

---

## Complete Migration Example

### Before (Old Structure)
```json
{
  "id": "agent-001",
  "name": "data-processing-agent",
  "version": 1,
  "version_string": "1.0.0",
  "llm": "openai",
  "llm_settings": {
    "temperature": 0.7,
    "max_tokens": 4096
  },
  "rag": [
    {
      "id": "company-docs",
      "type": "vector"
    }
  ]
}
```

### After (New Structure)
```json
{
  "agent_id": "data-processing-agent",
  "name": "data-processing-agent",
  "version_string": "1.0.0",
  "llm": "openai",
  "llm_settings": {
    "temperature": 0.7,
    "max_tokens": 4096
  },
  "rag": [
    {
      "index_id": "company-docs",
      "type": "vector"
    }
  ]
}
```

---

## Backward Compatibility

### Old Field Names Still Supported

The ADL schema, validators, and generators maintain backward compatibility:

- Old `id` field is still accepted (deprecated)
- Old `version` field is still accepted (deprecated)
- Old `document_index_id` field is still accepted (deprecated)
- Deprecation warnings are shown when old field names are used
- New field names are preferred and recommended

### Deprecation Timeline

- **v1.5**: New field names introduced, old names deprecated
- **v2.0**: Old field names will be removed (planned)

### Deprecation Warnings

When using old field names, you'll see warnings like:

```
WARNING: Field 'id' is deprecated. Use 'agent_id' instead.
WARNING: Field 'version' is deprecated. Use 'version_string' instead.
WARNING: Field 'document_index_id' is deprecated. Use 'index_id' instead.
```

---

## Automated Migration

### Migration Script

We provide a Python script to automatically migrate your ADL files:

```python
#!/usr/bin/env python3
"""
ADL Schema Redundant Fields Migration Script

Automatically migrates ADL files to remove redundant fields.
"""

import json
import sys
from pathlib import Path
from typing import Dict, Any
import shutil
from datetime import datetime


def migrate_agent_id(data: Dict[str, Any]) -> Dict[str, Any]:
    """Migrate agent id to agent_id."""
    if 'id' in data and 'agent_id' not in data:
        print(f"WARNING: Field 'id' is deprecated. Use 'agent_id' instead.")
        data['agent_id'] = data.pop('id')
    return data


def migrate_version(data: Dict[str, Any]) -> Dict[str, Any]:
    """Migrate version to version_string."""
    if 'version' in data and 'version_string' not in data:
        print(f"WARNING: Field 'version' is deprecated. Use 'version_string' instead.")
        version = data.pop('version')
        # Convert integer version to semantic version
        version_string = f"{version}.0.0"
        data['version_string'] = version_string
    return data


def migrate_rag_index_id(data: Dict[str, Any]) -> Dict[str, Any]:
    """Migrate RAG index id to index_id."""
    if 'rag' not in data:
        return data

    for index in data['rag']:
        if 'id' in index and 'index_id' not in index:
            print(f"WARNING: Field 'id' in RAG index is deprecated. Use 'index_id' instead.")
            index['index_id'] = index.pop('id')
    return data


def migrate_file(input_path: Path, output_path: Path = None) -> None:
    """Migrate a single ADL file."""
    print(f"Migrating {input_path}...")

    # Read input file
    with open(input_path, 'r') as f:
        data = json.load(f)

    # Apply migrations
    data = migrate_agent_id(data)
    data = migrate_version(data)
    data = migrate_rag_index_id(data)

    # Determine output path
    if output_path is None:
        output_path = input_path

    # Write output file
    with open(output_path, 'w') as f:
        json.dump(data, f, indent=2)
        f.write('\n')

    print(f"✓ Migrated to {output_path}")


def migrate_directory(input_dir: Path, output_dir: Path = None, backup: bool = True) -> None:
    """Migrate all ADL files in a directory."""
    if output_dir is None:
        output_dir = input_dir

    # Create backup if requested
    if backup:
        backup_dir = input_dir.parent / f"{input_dir.name}_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        print(f"Creating backup at {backup_dir}...")
        shutil.copytree(input_dir, backup_dir)
        print(f"✓ Backup created")

    # Find all JSON files
    json_files = list(input_dir.glob('*.json'))

    if not json_files:
        print("No JSON files found to migrate")
        return

    print(f"Found {len(json_files)} JSON files to migrate")

    # Migrate each file
    for json_file in json_files:
        relative_path = json_file.relative_to(input_dir)
        output_file = output_dir / relative_path

        # Create output directory if needed
        output_file.parent.mkdir(parents=True, exist_ok=True)

        migrate_file(json_file, output_file)

    print(f"\n✓ All files migrated successfully")


def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        print("Usage: python migrate_redundant_fields.py <input-file-or-directory> [output-directory]")
        print("\nExamples:")
        print("  python migrate_redundant_fields.py my-agent.json")
        print("  python migrate_redundant_fields.py examples/ migrated_examples/")
        print("  python migrate_redundant_fields.py examples/ --no-backup")
        sys.exit(1)

    input_path = Path(sys.argv[1])

    if not input_path.exists():
        print(f"Error: {input_path} does not exist")
        sys.exit(1)

    # Check for --no-backup flag
    backup = '--no-backup' not in sys.argv

    if input_path.is_file():
        migrate_file(input_path)
    elif input_path.is_dir():
        output_dir = None
        if len(sys.argv) > 2 and not sys.argv[2].startswith('--'):
            output_dir = Path(sys.argv[2])
        migrate_directory(input_path, output_dir, backup=backup)
    else:
        print(f"Error: {input_path} is not a file or directory")
        sys.exit(1)


if __name__ == '__main__':
    main()
```

### Using the Migration Script

#### Migrate a Single File
```bash
python migrate_redundant_fields.py my-agent.json
```

#### Migrate a Directory
```bash
python migrate_redundant_fields.py examples/
```

#### Migrate to a Different Directory
```bash
python migrate_redundant_fields.py examples/ migrated_examples/
```

#### Skip Backup
```bash
python migrate_redundant_fields.py examples/ --no-backup
```

### What the Script Does

1. **Creates a backup** of the original files (unless `--no-backup` is specified)
2. **Renames fields**:
   - `id` → `agent_id` (top-level)
   - `version` → `version_string` (converts integer to semantic version)
   - RAG index `id` → `index_id`
3. **Preserves all other data** unchanged
4. **Validates JSON syntax** after migration

---

## Testing Your Migration

### Validation

After migration, validate your ADL files:

```bash
# Validate agent files
python3 tools/dsl/validator.py examples/*.json

# Check for deprecation warnings
python3 tools/dsl/validator.py my-agent.json
```

You should see warnings like:
```
WARNING: Field 'id' is deprecated. Use 'agent_id' instead.
WARNING: Field 'version' is deprecated. Use 'version_string' instead.
WARNING: Field 'document_index_id' is deprecated. Use 'index_id' instead.
```

### Generate Code

Test that generators work with the new structure:

```bash
# Generate TypeScript
adl-generate my-agent.json --typescript -o my-agent.ts

# Generate Python
adl-generate my-agent.json --python -o my-agent.py
```

---

## Common Issues and Solutions

### Issue 1: Missing version_string

**Problem**: After migration, validators complain about missing `version_string`.

**Solution**: Ensure `version_string` field is present with semantic version format:

```json
{
  "agent_id": "agent-001",
  "version_string": "1.0.0"  // ← Required
}
```

### Issue 2: Code References Old Field Names

**Problem**: Your code references `agent.id` instead of `agent.agent_id`.

**Solution**: Update your code to use new field names:

**Before**:
```python
agent_id = agent['id']
```

**After**:
```python
agent_id = agent.get('agent_id') or agent.get('id')  # Support both
```

Or better:
```python
agent_id = agent['agent_id']  # Use new field name
```

### Issue 3: Version Comparison Issues

**Problem**: Your code compares versions using integer comparison.

**Solution**: Use string comparison for semantic versions:

**Before**:
```python
if agent['version'] < 2:
    # Do something
```

**After**:
```python
if agent['version_string'] < "2.0.0":
    # Do something
```

### Issue 4: RAG Index References

**Problem**: Your code references `rag[0]['id']` instead of `rag[0]['index_id']`.

**Solution**: Update your code to use new field names:

**Before**:
```python
index_id = rag[0]['id']
```

**After**:
```python
index_id = rag[0]['index_id']
```

---

## Best Practices

### 1. Use Semantic Versioning

Always use semantic versioning format (e.g., "1.2.0") for `version_string`:

- ✅ Good: "1.0.0", "2.1.3", "1.2.0-beta"
- ❌ Bad: "1", "2", "v1.0.0"

### 2. Use Consistent Naming Conventions

- Use kebab-case for agent names: `data-processing-agent`
- Use descriptive names: `company-docs` instead of `docs-001`
- Avoid generic names: `my-agent`, `test-index`

### 3. Keep IDs Human-Readable

- ✅ Good: `data-pipeline-agent`, `company-docs`
- ❌ Bad: `a1b2c3d4`, `index-001`

### 4. Document Your ID Structure

Add comments explaining your ID naming convention:

```json
{
  "agent_id": "data-pipeline-agent",
  "rag": [
    {
      "index_id": "company-docs",
      "type": "vector"
    }
  ]
}
```

---

## Rollback

If you need to rollback after migration:

### From Backup

If you used the migration script with backup:

```bash
# Find your backup directory
ls -la *_backup_*

# Restore from backup
cp -r backup_20250216_120000/* examples/
```

### Manual Rollback

If you didn't create a backup, you can manually rollback:

1. Rename `agent_id` back to `id`
2. Rename `version_string` back to `version` (convert semantic version to integer)
3. Rename RAG index `index_id` back to `id`

---

## Summary

### Changes Summary

| Field | Old Name | New Name | Type Change | Hierarchical Format |
|-------|----------|----------|-------------|---------------------|
| Agent ID | `id` | `agent_id` | N/A | `agent-name` |
| Version | `version` | `version_string` | Integer → String | N/A |
| RAG Index | `document_index_id` | `index_id` | N/A | `agent-name:index-name` |

### Benefits

1. **No Redundancy**: Single field for each purpose
2. **Clear Intent**: Entity-specific field names make code self-documenting
3. **Semantic Versioning**: Supports proper version comparison
4. **Backward Compatible**: Old field names still work with deprecation warnings
5. **Future-Proof**: Better structure for versioning and entity identification

### Next Steps

1. Run the migration script on your ADL files
2. Validate migrated files
3. Update any code that references old field names
4. Test with generators and validators
5. Commit your changes

---

## Support

If you encounter issues during migration:

1. Check the [ADL Documentation](https://github.com/nextmoca/adl)
2. Review [Migration Examples](../examples/)
3. Open an issue on [GitHub](https://github.com/nextmoca/adl/issues)

---

**Version**: 1.0
**Last Updated**: 2026-02-16
**ADL Version**: 1.5+