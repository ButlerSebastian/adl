# ADL ID Field Refactoring - Migration Guide

## Overview

This guide helps you migrate your ADL files to the new ID field structure introduced in ADL v3.1. The refactoring implements three solutions to improve clarity, reduce redundancy, and provide better entity identification.

### Why the Changes Were Made

1. **Redundancy**: Workflow nodes had `id` fields that duplicated the object key
2. **Ambiguity**: All entities used the generic `id` field name, making it unclear what type of entity was referenced
3. **Clarity**: Entity-specific field names and hierarchical IDs provide better context and traceability

### What Changed

#### Solution 1: Remove Redundant Node IDs
- **Before**: Node objects had an `id` field that duplicated the object key
- **After**: Node keys serve as the identifier, no redundant `id` field

#### Solution 2: Use Hierarchical IDs
- **Before**: Simple IDs like `"workflow-001"`, `"policy-001"`
- **After**: Hierarchical IDs like `"agent-001:workflow-001"`, `"agent-001:policy-001"`

#### Solution 3: Use Entity-Specific Field Names
- **Before**: Generic `id` field for all entities
- **After**: Entity-specific field names:
  - `agent_id` for agents
  - `workflow_id` for workflows
  - `edge_id` for workflow edges
  - `policy_id` for policies
  - `index_id` for RAG indices

---

## Detailed Changes

### Solution 1: Remove Redundant Node IDs

#### Before
```json
{
  "workflow": {
    "id": "sequential-data-processing",
    "nodes": {
      "input-node": {
        "id": "input-node",  // ← Redundant!
        "type": "input",
        "label": "Read Data"
      },
      "transform-node": {
        "id": "transform-node",  // ← Redundant!
        "type": "transform",
        "label": "Transform Data"
      }
    }
  }
}
```

#### After
```json
{
  "workflow": {
    "workflow_id": "sequential-workflow-agent:workflow-sequential",
    "nodes": {
      "input-node": {
        "type": "input",  // ← No id field, key is the ID
        "label": "Read Data"
      },
      "transform-node": {
        "type": "transform",  // ← No id field, key is the ID
        "label": "Transform Data"
      }
    }
  }
}
```

#### Migration Steps
1. Remove all `id` fields from workflow node objects
2. Ensure node keys are unique and descriptive
3. Update any code that references `node.id` to use the node key instead

---

### Solution 2: Use Hierarchical IDs

#### Before
```json
{
  "id": "agent-001",
  "workflow": {
    "id": "workflow-001",
    "edges": [
      {
        "id": "edge-1",
        "source": "input-node",
        "target": "transform-node"
      }
    ]
  },
  "policy": {
    "id": "policy-001"
  }
}
```

#### After
```json
{
  "agent_id": "agent-001",
  "workflow": {
    "workflow_id": "agent-001:workflow-sequential",
    "edges": [
      {
        "edge_id": "agent-001:workflow-sequential:edge-1",
        "source": "input-node",
        "target": "transform-node"
      }
    ]
  },
  "policy": {
    "policy_id": "agent-001:policy-rbac"
  }
}
```

#### Migration Steps
1. Update workflow IDs to format: `agent-name:workflow-name`
2. Update policy IDs to format: `agent-name:policy-name`
3. Update edge IDs to format: `agent-name:workflow-name:edge-N`
4. Use consistent naming conventions across all IDs

#### Benefits
- Clear hierarchy shows entity relationships
- Easy to trace which workflow/policy belongs to which agent
- Natural uniqueness guarantees
- Better for distributed systems

---

### Solution 3: Use Entity-Specific Field Names

#### Before
```json
{
  "id": "agent-001",
  "workflow": {
    "id": "workflow-001",
    "nodes": { ... },
    "edges": [
      {
        "id": "edge-1",
        "source": "input-node",
        "target": "transform-node"
      }
    ]
  },
  "policy": {
    "id": "policy-001"
  },
  "rag": [
    {
      "id": "index-001"
    }
  ]
}
```

#### After
```json
{
  "agent_id": "agent-001",
  "workflow": {
    "workflow_id": "agent-001:workflow-sequential",
    "nodes": { ... },
    "edges": [
      {
        "edge_id": "agent-001:workflow-sequential:edge-1",
        "source": "input-node",
        "target": "transform-node"
      }
    ]
  },
  "policy": {
    "policy_id": "agent-001:policy-rbac"
  },
  "rag": [
    {
      "index_id": "agent-001:index-docs"
    }
  ]
}
```

#### Migration Steps
1. Rename top-level `id` to `agent_id`
2. Rename workflow `id` to `workflow_id`
3. Rename edge `id` to `edge_id`
4. Rename policy `id` to `policy_id`
5. Rename RAG index `id` to `index_id`

#### Benefits
- Clear intent when reading code
- Better IDE autocomplete
- Easier to understand entity type at a glance
- Self-documenting code

---

## Complete Migration Example

### Before (Old Structure)
```json
{
  "version": 3,
  "name": "sequential_workflow_agent",
  "id": "agent-001",
  "workflow": {
    "id": "sequential-data-processing",
    "name": "Sequential Data Processing",
    "nodes": {
      "input-node": {
        "id": "input-node",
        "type": "input",
        "label": "Read Data"
      },
      "transform-node": {
        "id": "transform-node",
        "type": "transform",
        "label": "Transform Data"
      }
    },
    "edges": [
      {
        "id": "edge-1",
        "source": "input-node",
        "target": "transform-node",
        "relation": "data_flow"
      }
    ]
  },
  "policy": {
    "id": "rbac-policy",
    "name": "RBAC Policy"
  }
}
```

### After (New Structure)
```json
{
  "version": 3,
  "name": "sequential_workflow_agent",
  "agent_id": "sequential-workflow-agent",
  "workflow": {
    "workflow_id": "sequential-workflow-agent:workflow-sequential",
    "name": "Sequential Data Processing",
    "nodes": {
      "input-node": {
        "type": "input",
        "label": "Read Data"
      },
      "transform-node": {
        "type": "transform",
        "label": "Transform Data"
      }
    },
    "edges": [
      {
        "edge_id": "sequential-workflow-agent:workflow-sequential:edge-1",
        "source": "input-node",
        "target": "transform-node",
        "relation": "data_flow"
      }
    ]
  },
  "policy": {
    "policy_id": "sequential-workflow-agent:policy-rbac",
    "name": "RBAC Policy"
  }
}
```

---

## Backward Compatibility

### Old Field Names Still Supported

The ADL schema, validators, and generators maintain backward compatibility:

- Old `id` fields are still accepted
- Deprecation warnings are shown when old field names are used
- New field names are preferred and recommended

### Deprecation Timeline

- **v3.1**: New field names introduced, old names deprecated
- **v4.0**: Old field names will be removed (planned)

### Deprecation Warnings

When using old field names, you'll see warnings like:

```
WARNING: Field 'id' is deprecated. Use 'workflow_id' instead.
WARNING: Field 'id' is deprecated. Use 'edge_id' instead.
WARNING: Field 'id' is deprecated. Use 'policy_id' instead.
WARNING: Redundant 'id' field in node. Node keys serve as identifiers.
```

---

## Automated Migration

### Migration Script

We provide a Python script to automatically migrate your ADL files:

```python
#!/usr/bin/env python3
"""
ADL ID Field Migration Script

Automatically migrates ADL files to the new ID field structure.
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
        data['agent_id'] = data.pop('id')
    return data


def migrate_workflow(data: Dict[str, Any]) -> Dict[str, Any]:
    """Migrate workflow id to workflow_id and remove redundant node ids."""
    if 'workflow' not in data:
        return data
    
    workflow = data['workflow']
    
    # Migrate workflow id
    if 'id' in workflow and 'workflow_id' not in workflow:
        workflow['workflow_id'] = workflow.pop('id')
    
    # Remove redundant node ids
    if 'nodes' in workflow:
        for node_key, node in workflow['nodes'].items():
            if 'id' in node:
                # Warn if id doesn't match key
                if node['id'] != node_key:
                    print(f"WARNING: Node id '{node['id']}' doesn't match key '{node_key}'")
                del node['id']
    
    # Migrate edge ids
    if 'edges' in workflow:
        for edge in workflow['edges']:
            if 'id' in edge and 'edge_id' not in edge:
                edge['edge_id'] = edge.pop('id')
    
    return data


def migrate_policy(data: Dict[str, Any]) -> Dict[str, Any]:
    """Migrate policy id to policy_id."""
    if 'policy' not in data:
        return data
    
    policy = data['policy']
    
    if 'id' in policy and 'policy_id' not in policy:
        policy['policy_id'] = policy.pop('id')
    
    return data


def migrate_rag(data: Dict[str, Any]) -> Dict[str, Any]:
    """Migrate RAG index ids to index_id."""
    if 'rag' not in data:
        return data
    
    for index in data['rag']:
        if 'id' in index and 'index_id' not in index:
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
    data = migrate_workflow(data)
    data = migrate_policy(data)
    data = migrate_rag(data)
    
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
        print("Usage: python migrate_ids.py <input-file-or-directory> [output-directory]")
        print("\nExamples:")
        print("  python migrate_ids.py my-agent.json")
        print("  python migrate_ids.py examples/ migrated_examples/")
        print("  python migrate_ids.py examples/ --no-backup")
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
python migrate_ids.py my-agent.json
```

#### Migrate a Directory
```bash
python migrate_ids.py examples/
```

#### Migrate to a Different Directory
```bash
python migrate_ids.py examples/ migrated_examples/
```

#### Skip Backup
```bash
python migrate_ids.py examples/ --no-backup
```

### What the Script Does

1. **Creates a backup** of the original files (unless `--no-backup` is specified)
2. **Renames ID fields**:
   - `id` → `agent_id` (top-level)
   - `id` → `workflow_id` (workflow)
   - `id` → `edge_id` (edges)
   - `id` → `policy_id` (policy)
   - `id` → `index_id` (RAG indices)
3. **Removes redundant node IDs** from workflow nodes
4. **Preserves all other data** unchanged
5. **Validates JSON syntax** after migration

---

## Testing Your Migration

### Validation

After migration, validate your ADL files:

```bash
# Validate workflow files
python3 tools/dsl/workflow_validator.py examples/workflow_*.json

# Validate policy files
python3 tools/dsl/policy_validator.py examples/policy_*.json

# Validate all files
python3 tools/dsl/validator.py examples/*.json
```

### Check for Deprecation Warnings

Run validators to see if you're still using old field names:

```bash
python3 tools/dsl/workflow_validator.py my-agent.json
```

You should see warnings like:
```
WARNING: Field 'id' is deprecated. Use 'workflow_id' instead.
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

### Issue 1: Node ID Doesn't Match Key

**Problem**: Node has `id` field that doesn't match the object key.

**Before**:
```json
"nodes": {
  "input-node": {
    "id": "different-id",  // ← Doesn't match key
    "type": "input"
  }
}
```

**Solution**: Remove the `id` field and use the key as the identifier:

**After**:
```json
"nodes": {
  "input-node": {
    "type": "input"  // ← Key is the ID
  }
}
```

### Issue 2: Duplicate Edge IDs

**Problem**: Multiple edges have the same `edge_id`.

**Solution**: Ensure each edge has a unique `edge_id`:

```json
"edges": [
  {
    "edge_id": "agent-001:workflow-001:edge-1",  // ← Unique
    "source": "input-node",
    "target": "transform-node"
  },
  {
    "edge_id": "agent-001:workflow-001:edge-2",  // ← Unique
    "source": "transform-node",
    "target": "output-node"
  }
]
```

### Issue 3: Missing Required Fields

**Problem**: After migration, validators complain about missing required fields.

**Solution**: Ensure all required fields are present:

```json
{
  "agent_id": "agent-001",  // ← Required
  "workflow": {
    "workflow_id": "agent-001:workflow-001",  // ← Required
    "nodes": { ... },
    "edges": [
      {
        "edge_id": "agent-001:workflow-001:edge-1",  // ← Required
        "source": "input-node",
        "target": "transform-node"
      }
    ]
  }
}
```

### Issue 4: Code References Old Field Names

**Problem**: Your code references `workflow.id` instead of `workflow.workflow_id`.

**Solution**: Update your code to use new field names:

**Before**:
```python
workflow_id = workflow['id']
```

**After**:
```python
workflow_id = workflow.get('workflow_id') or workflow.get('id')  # Support both
```

Or better:
```python
workflow_id = workflow['workflow_id']  # Use new field name
```

---

## Best Practices

### 1. Use Consistent Naming Conventions

- Use kebab-case for agent names: `sequential-workflow-agent`
- Use descriptive names: `workflow-sequential` instead of `workflow-001`
- Avoid generic names: `my-agent`, `test-workflow`

### 2. Follow Hierarchical ID Format

Use the format: `parent-entity:child-entity[:grandchild-entity]`

Examples:
- `my-agent:workflow-main`
- `my-agent:workflow-main:edge-1`
- `my-agent:policy-rbac`
- `my-agent:index-docs`

### 3. Keep IDs Human-Readable

- ✅ Good: `data-pipeline-agent:workflow-etl`
- ❌ Bad: `a1b2c3d4:e5f6g7h8`

### 4. Use Version Numbers in IDs (Optional)

For versioned entities:
- `my-agent:workflow-main:v1`
- `my-agent:workflow-main:v2`

### 5. Document Your ID Structure

Add comments explaining your ID naming convention:

```json
{
  "agent_id": "data-pipeline-agent",
  "workflow": {
    "workflow_id": "data-pipeline-agent:workflow-etl",
    "description": "ETL workflow for data processing pipeline"
  }
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
2. Rename `workflow_id` back to `id`
3. Rename `edge_id` back to `id`
4. Rename `policy_id` back to `id`
5. Rename `index_id` back to `id`
6. Add `id` fields back to workflow nodes (matching the key)

---

## Summary

### Changes Summary

| Entity | Old Field | New Field | Hierarchical Format |
|--------|-----------|-----------|---------------------|
| Agent | `id` | `agent_id` | `agent-name` |
| Workflow | `id` | `workflow_id` | `agent-name:workflow-name` |
| Workflow Node | `id` (redundant) | None (key is ID) | N/A |
| Workflow Edge | `id` | `edge_id` | `agent-name:workflow-name:edge-N` |
| Policy | `id` | `policy_id` | `agent-name:policy-name` |
| RAG Index | `id` | `index_id` | `agent-name:index-name` |

### Benefits

1. **No Redundancy**: Node IDs are no longer duplicated
2. **Clear Hierarchy**: Hierarchical IDs show entity relationships
3. **Better Clarity**: Entity-specific field names make code self-documenting
4. **Backward Compatible**: Old field names still work with deprecation warnings
5. **Future-Proof**: Better structure for distributed systems and multi-agent workflows

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
**Last Updated**: 2025-02-16  
**ADL Version**: 3.1+
