# Python Binding Generator

Generate type-safe Python TypedDict classes from ADL definitions.

## Overview

The Python binding generator converts ADL DSL definitions into Python TypedDict classes, providing full type safety and IDE support for Python developers. It supports all ADL features including Phase 4 workflow and policy types.

## Installation

The Python generator is included with the ADL CLI:

```bash
pip install adl
```

Or install from source:

```bash
git clone https://github.com/nextmoca/adl.git
cd adl
pip install -e .
```

## Usage

### Basic Usage

Generate Python TypedDict classes from an ADL file:

```bash
adl-generate my-agent.adl --python -o my_agent.py
```

Or using the format flag:

```bash
adl-generate my-agent.adl --format python -o my_agent.py
```

### With Documentation

Include docstrings in generated code:

```bash
adl-generate my-agent.adl --python --docs -o my_agent.py
```

### Watch Mode

Automatically regenerate when the ADL file changes:

```bash
adl-generate my-agent.adl --python --watch
```

## Generated Python Types

### Basic Types

The generator maps ADL primitive types to Python types:

| ADL Type | Python Type |
|----------|-------------|
| `string` | `str` |
| `integer` | `int` |
| `number` | `float` |
| `boolean` | `bool` |
| `object` | `Dict[str, Any]` |
| `array` | `List[Any]` |
| `any` | `Any` |
| `null` | `None` |

### Type Definitions

ADL type definitions become Python TypedDict classes:

```adl
# Input ADL
type Person {
  name: string
  age: integer
  email?: string
  tags: string[]
}
```

```python
# Generated Python
from typing import List, Optional, Union, TypedDict, Any, Required, NotRequired

class Person(TypedDict):
    name: Required[str]
    age: Required[int]
    email: NotRequired[str]
    tags: Required[List[str]]
```

### Enum Definitions

ADL enums become Python string classes:

```adl
# Input ADL
enum Lifecycle {
  stable
  beta
  deprecated
  experimental
}
```

```python
# Generated Python
class Lifecycle(str):
    "stable"
    "beta"
    "deprecated"
    "experimental"
```

### Agent Definitions

ADL agent definitions become Python TypedDict classes:

```adl
# Input ADL
agent MyAgent {
  id: string
  name: string
  version: integer
  config: Config
}
```

```python
# Generated Python
class MyAgent(TypedDict):
    id: Required[str]
    name: Required[str]
    version: Required[int]
    config: Required[Config]
```

## Phase 4 Types

### Workflow Types

The generator supports Phase 4 workflow definitions:

```python
# Generated Workflow TypedDict
class Workflow(TypedDict):
    id: Required[str]
    name: Required[str]
    version: Required[str]
    description: Required[str]
    nodes: Required[Dict[str, WorkflowNode]]
    edges: Required[List[WorkflowEdge]]
    metadata: NotRequired[Dict[str, Any]]

class WorkflowNode(TypedDict):
    id: Required[str]
    type: Required[str]
    label: Required[str]
    config: Required[Dict[str, Any]]
    position: Required[Dict[str, int]]

class WorkflowEdge(TypedDict):
    id: Required[str]
    source: Required[str]
    target: Required[str]
    relation: Required[str]
    condition: NotRequired[Dict[str, Any]]
    metadata: NotRequired[Dict[str, Any]]
```

### Policy Types

The generator supports Phase 4 policy definitions:

```python
# Generated Policy TypedDict
class Policy(TypedDict):
    id: Required[str]
    name: Required[str]
    version: Required[str]
    description: Required[str]
    rego: Required[str]
    enforcement: Required[Enforcement]
    data: Required[PolicyData]
    metadata: NotRequired[Dict[str, Any]]

class Enforcement(TypedDict):
    mode: Required[str]
    action: Required[str]
    audit_log: Required[bool]

class PolicyData(TypedDict):
    roles: Required[Dict[str, List[str]]]
    permissions: Required[Dict[str, List[str]]]
```

## Advanced Features

### Optional Fields

Optional ADL fields become `NotRequired` fields in Python:

```adl
type Config {
  required: string
  optional?: string
}
```

```python
class Config(TypedDict):
    required: Required[str]
    optional: NotRequired[str]
```

### Union Types

ADL union types become Python `Union` types:

```adl
type Result = string | integer
```

```python
from typing import Union

class Result(TypedDict):
    value: Required[Union[str, int]]
```

### Array Types

ADL array types become Python `List` types:

```adl
type List {
  items: string[]
}
```

```python
class List(TypedDict):
    items: Required[List[str]]
```

## Examples

### Complete Example

Input ADL file (`my-agent.adl`):

```adl
enum Lifecycle {
  stable
  beta
  deprecated
}

type Config {
  timeout: integer
  retries: integer
}

type Tool {
  name: string
  description: string
  parameters: object
}

agent MyAgent {
  id: string
  name: string
  version: integer
  lifecycle: Lifecycle
  config: Config
  tools: Tool[]
}
```

Generated Python (`my_agent.py`):

```python
from typing import List, Optional, Union, TypedDict, Any, Required, NotRequired

class Lifecycle(str):
    "stable"
    "beta"
    "deprecated"

class Config(TypedDict):
    timeout: Required[int]
    retries: Required[int]

class Tool(TypedDict):
    name: Required[str]
    description: Required[str]
    parameters: Required[Dict[str, Any]]

class MyAgent(TypedDict):
    id: Required[str]
    name: Required[str]
    version: Required[int]
    lifecycle: Required[Lifecycle]
    config: Required[Config]
    tools: Required[List[Tool]]
```

### Phase 4 Workflow Example

Input ADL file (`workflow.adl`):

```adl
workflow SequentialProcessing {
  id: "workflow-001"
  name: "Sequential Data Processing"
  version: "1.0.0"
  description: "Process data through sequential stages"

  nodes: {
    "input-node": {
      id: "input-node"
      type: "input"
      label: "Data Input"
      config: {}
      position: { x: 100, y: 100 }
    }
  }

  edges: [
    {
      id: "edge-001"
      source: "input-node"
      target: "transform-node"
      relation: "data_flow"
    }
  ]
}
```

Generated Python (`workflow.py`):

```python
from typing import List, Optional, Union, TypedDict, Any, Required, NotRequired

class WorkflowNode(TypedDict):
    id: Required[str]
    type: Required[str]
    label: Required[str]
    config: Required[Dict[str, Any]]
    position: Required[Dict[str, int]]

class WorkflowEdge(TypedDict):
    id: Required[str]
    source: Required[str]
    target: Required[str]
    relation: Required[str]
    condition: NotRequired[Dict[str, Any]]
    metadata: NotRequired[Dict[str, Any]]

class Workflow(TypedDict):
    id: Required[str]
    name: Required[str]
    version: Required[str]
    description: Required[str]
    nodes: Required[Dict[str, WorkflowNode]]
    edges: Required[List[WorkflowEdge]]
    metadata: NotRequired[Dict[str, Any]]
```

## Best Practices

### 1. Use Semantic Versioning

Always use semantic versioning for agent definitions:

```adl
agent MyAgent {
  version_string: "1.2.3"
  # ...
}
```

### 2. Document Your Types

Use the `--docs` flag to include docstrings:

```bash
adl-generate my-agent.adl --python --docs -o my_agent.py
```

### 3. Use Watch Mode During Development

Enable watch mode to automatically regenerate Python when ADL changes:

```bash
adl-generate my-agent.adl --python --watch
```

### 4. Organize Your ADL Files

Keep related types in separate files and use imports:

```adl
# types.adl
type Config { ... }
type Tool { ... }

# agent.adl
import { Config, Tool } from './types'

agent MyAgent {
  config: Config
  tools: Tool[]
}
```

### 5. Validate Before Generating

Always validate your ADL files before generating Python:

```bash
adl-validate my-agent.adl
adl-generate my-agent.adl --python -o my_agent.py
```

## Troubleshooting

### Issue: "Type not found" error

**Cause**: The ADL file has a type reference that doesn't exist.

**Solution**: Ensure all referenced types are defined or imported:

```adl
# Correct
import { Config } from './config'

agent MyAgent {
  config: Config  # Config is imported
}
```

### Issue: Generated code has syntax errors

**Cause**: The ADL file has invalid syntax or structure.

**Solution**: Validate the ADL file first:

```bash
adl-validate my-agent.adl --verbose
```

### Issue: Optional fields are not optional

**Cause**: The field is marked as required in the ADL definition.

**Solution**: Use the `?` modifier for optional fields:

```adl
type Config {
  required: string
  optional?: string  # This will be optional in Python
}
```

### Issue: Union types not working

**Cause**: Union types require proper syntax in ADL.

**Solution**: Use the `|` operator for union types:

```adl
type Result = string | integer | boolean
```

## Integration with Python Projects

### Using Generated Types

Import the generated types in your Python project:

```python
from my_agent import MyAgent, Config, Tool

agent: MyAgent = {
    "id": "agent-001",
    "name": "My Agent",
    "version": 1,
    "config": {
        "timeout": 30,
        "retries": 3
    },
    "tools": []
}
```

### Type Checking

The generated types provide full type checking with mypy:

```python
from my_agent import MyAgent

def process_agent(agent: MyAgent) -> None:
    # mypy will enforce type safety
    print(agent["name"])
    print(agent["config"]["timeout"])

# This will cause a type error with mypy
invalid_agent: MyAgent = {
    "id": "agent-001",
    # Missing required fields
}
```

### IDE Support

The generated types work with all Python IDEs:
- PyCharm
- VS Code with Python extension
- IntelliJ IDEA
- Vim/Neovim with Python plugins

### Type Validation

Use mypy to validate your code against the generated types:

```bash
pip install mypy
mypy my_script.py
```

## Advanced Usage

### Custom Type Validators

Create custom validators for your generated types:

```python
from my_agent import MyAgent
from typing import Dict, Any

def validate_agent(agent: Dict[str, Any]) -> bool:
    """Validate agent data against MyAgent schema."""
    try:
        # Check required fields
        required_fields = ["id", "name", "version", "config", "tools"]
        for field in required_fields:
            if field not in agent:
                return False

        # Check field types
        if not isinstance(agent["id"], str):
            return False
        if not isinstance(agent["version"], int):
            return False

        return True
    except Exception:
        return False

# Usage
agent_data = {"id": "agent-001", "name": "My Agent", "version": 1, ...}
if validate_agent(agent_data):
    agent: MyAgent = agent_data
```

### Serialization/Deserialization

Use the generated types with JSON serialization:

```python
import json
from my_agent import MyAgent

# Deserialize JSON to TypedDict
with open("agent.json", "r") as f:
    agent_data = json.load(f)
    agent: MyAgent = agent_data

# Serialize TypedDict to JSON
agent_json = json.dumps(agent)
```

## See Also

- [TypeScript Binding Generator](typescript-generator.md)
- [CLI Reference](tools/cli.md)
- [ADL Schema Reference](schema-reference.md)
- [Phase 4: Workflow & DAG](workflow-dag.md)
- [Phase 4: Policy-as-Code](policy-as-code.md)
