# Workflow & DAG Definitions

## Overview

ADL v3 introduces workflow and DAG (Directed Acyclic Graph) definitions for multi-agent orchestration. This enables complex multi-step agent workflows with dependencies, parallel execution, and conditional branching.

## Architecture

### Core Concepts

#### 1. Workflow Definition

A workflow is a directed acyclic graph (DAG) that defines:
- **Nodes**: Individual steps or tasks in the workflow
- **Edges**: Connections between nodes representing dependencies or data flow
- **Execution Order**: Determined by topological sorting of the DAG

#### 2. Node Types

| Type | Description | Use Case |
|------|-------------|----------|
| **trigger** | Entry point for workflow execution | Webhook, schedule, manual trigger |
| **input** | Data ingestion nodes | File upload, API request, database query |
| **transform** | Data processing nodes | Map, filter, aggregate, join |
| **action** | External system operations | HTTP request, email send, Slack message |
| **condition** | Branching logic | IF/Switch, route, filter |
| **loop** | Iteration patterns | For each, while, repeat |
| **output** | Data export nodes | File save, database write, API response |
| **sub-workflow** | Nested workflow execution | Call workflow, subgraph |
| **annotation** | Documentation nodes | Sticky note, comment |

#### 3. Edge Types

| Type | Description | Use Case |
|------|-------------|----------|
| **data-flow** | Primary data passing | Standard node-to-node connection |
| **control-flow** | Execution order | Conditional branches, loops |
| **error-flow** | Error handling | Try-catch patterns |
| **ai_languageModel** | AI model connection | Agent → Model |
| **ai_tool** | AI tool connection | Tool → Agent |
| **dependency** | Execution dependency without data | Setup/teardown patterns |

## JSON Schema

### Workflow Definition

```json
{
  "id": "workflow-id",
  "name": "My Workflow",
  "version": "1.0.0",
  "description": "Workflow description",
  "schedule": "0 0 * * *",
  "nodes": {
    "node-1": {
      "id": "node-1",
      "type": "trigger",
      "label": "Webhook Trigger",
      "config": {
        "webhook_url": "/api/webhook"
      },
      "position": { "x": 100, "y": 100 }
    },
    "node-2": {
      "id": "node-2",
      "type": "transform",
      "label": "Process Data",
      "config": {
        "operation": "map",
        "expression": "data.map(x => x * 2)"
      },
      "position": { "x": 300, "y": 100 }
    },
    "node-3": {
      "id": "node-3",
      "type": "output",
      "label": "Save Results",
      "config": {
        "destination": "database",
        "table": "results"
      },
      "position": { "x": 500, "y": 100 }
    }
  },
  "edges": [
    {
      "id": "edge-1",
      "source": "node-1",
      "target": "node-2",
      "relation": "data-flow"
    },
    {
      "id": "edge-2",
      "source": "node-2",
      "target": "node-3",
      "relation": "data-flow"
    }
  ],
  "metadata": {
    "author": "team",
    "tags": ["etl", "data-processing"]
  }
}
```

### Node Schema

```typescript
interface WorkflowNode {
  id: string;
  type: NodeType;
  label: string;
  config: Record<string, unknown>;
  position?: { x: number; y: number };
  metadata?: Record<string, unknown>;
}

type NodeType =
  | 'trigger'
  | 'input'
  | 'transform'
  | 'action'
  | 'condition'
  | 'loop'
  | 'output'
  | 'sub-workflow'
  | 'annotation';
```

### Edge Schema

```typescript
interface WorkflowEdge {
  id: string;
  source: string;
  target: string;
  relation?: EdgeRelation;
  condition?: string;
  metadata?: Record<string, unknown>;
}

type EdgeRelation =
  | 'data-flow'
  | 'control-flow'
  | 'error-flow'
  | 'ai_languageModel'
  | 'ai_tool'
  | 'dependency';
```

## Execution Semantics

### 1. Topological Sorting

Workflows are executed in topological order to ensure dependencies are satisfied:

```python
def topological_sort(nodes, edges):
    """Kahn's algorithm for topological sorting."""
    # Build adjacency list and in-degree count
    adjacency = {node_id: [] for node_id in nodes}
    in_degree = {node_id: 0 for node_id in nodes}

    for edge in edges:
        adjacency[edge['source']].append(edge['target'])
        in_degree[edge['target']] += 1

    # Find all nodes with no incoming edges
    queue = [node_id for node_id, degree in in_degree.items() if degree == 0]
    result = []

    while queue:
        current = queue.pop(0)
        result.append(current)

        for neighbor in adjacency[current]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)

    # Check for cycles
    if len(result) != len(nodes):
        raise ValueError("Workflow contains a cycle")

    return result
```

### 2. Cycle Detection

Workflows must be acyclic. Cycle detection uses DFS with a recursion stack:

```python
def detect_cycle(nodes, edges):
    """Detect cycles using DFS with recursion stack."""
    # Build adjacency list
    graph = {node_id: [] for node_id in nodes}
    for edge in edges:
        graph[edge['source']].append(edge['target'])

    visited = set()
    rec_stack = set()

    def dfs(node):
        visited.add(node)
        rec_stack.add(node)

        for neighbor in graph[node]:
            if neighbor not in visited:
                if dfs(neighbor):
                    return True
            elif neighbor in rec_stack:
                return True

        rec_stack.remove(node)
        return False

    for node in nodes:
        if node not in visited:
            if dfs(node):
                return True

    return False
```

### 3. Parallel Execution

Nodes with no dependencies can execute in parallel:

```python
def get_parallel_levels(nodes, edges):
    """Determine parallel execution levels."""
    execution_order = topological_sort(nodes, edges)

    # Build dependency graph
    dependencies = {node_id: set() for node_id in nodes}
    for edge in edges:
        dependencies[edge['target']].add(edge['source'])

    levels = []
    remaining = set(execution_order)

    while remaining:
        # Find nodes with all dependencies satisfied
        ready = [
            node for node in remaining
            if dependencies[node].issubset(set().union(*levels))
        ]

        if not ready:
            raise ValueError("Circular dependency detected")

        levels.append(set(ready))
        remaining -= set(ready)

    return levels
```

### 4. Conditional Execution

Edges can have conditions for conditional branching:

```json
{
  "id": "edge-3",
  "source": "node-2",
  "target": "node-4",
  "relation": "control-flow",
  "condition": "data.status == 'success'"
}
```

### 5. Error Handling

Error-flow edges handle failures:

```json
{
  "id": "edge-error",
  "source": "node-2",
  "target": "node-error-handler",
  "relation": "error-flow"
}
```

## Validation Rules

### 1. Structural Validation

- Workflow must have at least one node
- All node IDs must be unique
- All edge IDs must be unique
- All edge sources and targets must reference existing nodes

### 2. Cycle Validation

- Workflow must be acyclic
- No circular dependencies allowed

### 3. Connection Validation

- Trigger nodes cannot have incoming edges
- Output nodes cannot have outgoing edges
- Condition nodes must have at least 2 outgoing edges
- Loop nodes must have a loop-back edge

### 4. Type Validation

- Node types must be valid
- Edge relations must be valid
- Config must match node type requirements

## Best Practices

### 1. Node Naming

- Use descriptive, lowercase names with hyphens
- Example: `process-data`, `send-email`, `validate-input`

### 2. Edge Naming

- Use descriptive names indicating flow
- Example: `data-to-process`, `error-handler`

### 3. Workflow Structure

- Start with trigger nodes
- End with output nodes
- Use condition nodes for branching
- Use loop nodes for iteration
- Keep workflows focused and modular

### 4. Error Handling

- Always include error-flow edges for critical nodes
- Use dedicated error handler nodes
- Log errors for debugging

### 5. Documentation

- Use annotation nodes for documentation
- Add descriptions to nodes and edges
- Include metadata for workflow tracking

## Examples

### Example 1: Sequential Workflow

```json
{
  "id": "sequential-workflow",
  "name": "Sequential Data Processing",
  "version": "1.0.0",
  "nodes": {
    "input": {
      "id": "input",
      "type": "input",
      "label": "Read Data",
      "config": {
        "source": "api",
        "endpoint": "/data"
      }
    },
    "transform": {
      "id": "transform",
      "type": "transform",
      "label": "Transform Data",
      "config": {
        "operation": "map",
        "expression": "x => x * 2"
      }
    },
    "output": {
      "id": "output",
      "type": "output",
      "label": "Save Data",
      "config": {
        "destination": "database",
        "table": "processed_data"
      }
    }
  },
  "edges": [
    {
      "id": "edge-1",
      "source": "input",
      "target": "transform",
      "relation": "data-flow"
    },
    {
      "id": "edge-2",
      "source": "transform",
      "target": "output",
      "relation": "data-flow"
    }
  ]
}
```

### Example 2: Parallel Workflow

```json
{
  "id": "parallel-workflow",
  "name": "Parallel Processing",
  "version": "1.0.0",
  "nodes": {
    "input": {
      "id": "input",
      "type": "input",
      "label": "Read Data"
    },
    "process-1": {
      "id": "process-1",
      "type": "transform",
      "label": "Process A"
    },
    "process-2": {
      "id": "process-2",
      "type": "transform",
      "label": "Process B"
    },
    "process-3": {
      "id": "process-3",
      "type": "transform",
      "label": "Process C"
    },
    "output": {
      "id": "output",
      "type": "output",
      "label": "Merge Results"
    }
  },
  "edges": [
    {
      "id": "edge-1",
      "source": "input",
      "target": "process-1",
      "relation": "data-flow"
    },
    {
      "id": "edge-2",
      "source": "input",
      "target": "process-2",
      "relation": "data-flow"
    },
    {
      "id": "edge-3",
      "source": "input",
      "target": "process-3",
      "relation": "data-flow"
    },
    {
      "id": "edge-4",
      "source": "process-1",
      "target": "output",
      "relation": "data-flow"
    },
    {
      "id": "edge-5",
      "source": "process-2",
      "target": "output",
      "relation": "data-flow"
    },
    {
      "id": "edge-6",
      "source": "process-3",
      "target": "output",
      "relation": "data-flow"
    }
  ]
}
```

### Example 3: Conditional Workflow

```json
{
  "id": "conditional-workflow",
  "name": "Conditional Processing",
  "version": "1.0.0",
  "nodes": {
    "input": {
      "id": "input",
      "type": "input",
      "label": "Read Data"
    },
    "condition": {
      "id": "condition",
      "type": "condition",
      "label": "Check Status",
      "config": {
        "expression": "data.status"
      }
    },
    "process-success": {
      "id": "process-success",
      "type": "action",
      "label": "Handle Success"
    },
    "process-failure": {
      "id": "process-failure",
      "type": "action",
      "label": "Handle Failure"
    },
    "output": {
      "id": "output",
      "type": "output",
      "label": "Save Result"
    }
  },
  "edges": [
    {
      "id": "edge-1",
      "source": "input",
      "target": "condition",
      "relation": "data-flow"
    },
    {
      "id": "edge-2",
      "source": "condition",
      "target": "process-success",
      "relation": "control-flow",
      "condition": "data.status == 'success'"
    },
    {
      "id": "edge-3",
      "source": "condition",
      "target": "process-failure",
      "relation": "control-flow",
      "condition": "data.status == 'failure'"
    },
    {
      "id": "edge-4",
      "source": "process-success",
      "target": "output",
      "relation": "data-flow"
    },
    {
      "id": "edge-5",
      "source": "process-failure",
      "target": "output",
      "relation": "data-flow"
    }
  ]
}
```

## Integration with ADL

Workflows are integrated into ADL agent definitions via the `workflow` field:

```json
{
  "name": "workflow-agent",
  "description": "Agent with workflow capabilities",
  "role": "Workflow Orchestrator",
  "llm": "openai",
  "llm_settings": {
    "temperature": 0.7,
    "max_tokens": 2000
  },
  "workflow": {
    "id": "agent-workflow",
    "name": "Agent Workflow",
    "version": "1.0.0",
    "nodes": { /* ... */ },
    "edges": [ /* ... */ ]
  },
  "tools": [ /* ... */ ],
  "rag": [],
  "memory": { /* ... */ }
}
```

## Migration from v2

v2 agents without workflows default to a simple single-node workflow:

```json
{
  "workflow": {
    "id": "default",
    "name": "Default Workflow",
    "version": "1.0.0",
    "nodes": {
      "default": {
        "id": "default",
        "type": "action",
        "label": "Default Action",
        "config": {}
      }
    },
    "edges": []
  }
}
```

This ensures backward compatibility while enabling v3 workflow features.

## References

- [JSON Graph Specification](https://github.com/jsongraph/json-graph-specification)
- [Airflow DAGs](https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/dags.html)
- [GitHub Actions Workflows](https://docs.github.com/actions/using-workflows/workflow-syntax-for-github-actions)
- [Dagster Op Graphs](https://docs.dagster.io/guides/build/ops/graphs)
