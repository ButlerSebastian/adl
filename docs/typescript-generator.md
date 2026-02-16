# TypeScript Binding Generator

Generate type-safe TypeScript interfaces from ADL definitions.

## Overview

The TypeScript binding generator converts ADL DSL definitions into TypeScript interfaces, providing full type safety and IDE support for TypeScript developers. It supports all ADL features including Phase 4 workflow and policy types.

## Installation

The TypeScript generator is included with the ADL CLI:

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

Generate TypeScript interfaces from an ADL file:

```bash
adl-generate my-agent.adl --typescript -o my-agent.ts
```

Or using the format flag:

```bash
adl-generate my-agent.adl --format typescript -o my-agent.ts
```

### With Documentation

Include JSDoc comments in generated code:

```bash
adl-generate my-agent.adl --typescript --docs -o my-agent.ts
```

### Watch Mode

Automatically regenerate when the ADL file changes:

```bash
adl-generate my-agent.adl --typescript --watch
```

## Generated TypeScript Types

### Basic Types

The generator maps ADL primitive types to TypeScript types:

| ADL Type | TypeScript Type |
|----------|-----------------|
| `string` | `string` |
| `integer` | `number` |
| `number` | `number` |
| `boolean` | `boolean` |
| `object` | `Record<string, any>` |
| `array` | `any[]` |
| `any` | `any` |
| `null` | `null` |

### Type Definitions

ADL type definitions become TypeScript interfaces:

```adl
# Input ADL
type Person {
  name: string
  age: integer
  email?: string
  tags: string[]
}
```

```typescript
// Generated TypeScript
export interface Person {
  name: string;
  age: number;
  email?: string;
  tags: string[];
}
```

### Enum Definitions

ADL enums become TypeScript enums:

```adl
# Input ADL
enum Lifecycle {
  stable
  beta
  deprecated
  experimental
}
```

```typescript
// Generated TypeScript
export enum Lifecycle {
  stable,
  beta,
  deprecated,
  experimental
}
```

### Agent Definitions

ADL agent definitions become TypeScript types:

```adl
# Input ADL
agent MyAgent {
  id: string
  name: string
  version: integer
  config: Config
}
```

```typescript
// Generated TypeScript
export type MyAgent = {
  id: string;
  name: string;
  version: number;
  config: Config;
};
```

## Phase 4 Types

### Workflow Types

The generator supports Phase 4 workflow definitions:

```typescript
// Generated Workflow interface
export interface Workflow {
  id: string;
  name: string;
  version: string;
  description: string;
  nodes: Record<string, WorkflowNode>;
  edges: WorkflowEdge[];
  metadata?: Record<string, any>;
}

export interface WorkflowNode {
  id: string;
  type: string;
  label: string;
  config: Record<string, any>;
  position: { x: number; y: number };
}

export interface WorkflowEdge {
  id: string;
  source: string;
  target: string;
  relation: string;
  condition?: Record<string, any>;
  metadata?: Record<string, any>;
}
```

### Policy Types

The generator supports Phase 4 policy definitions:

```typescript
// Generated Policy interface
export interface Policy {
  id: string;
  name: string;
  version: string;
  description: string;
  rego: string;
  enforcement: Enforcement;
  data: PolicyData;
  metadata?: Record<string, any>;
}

export interface Enforcement {
  mode: "strict" | "moderate" | "lenient";
  action: "deny" | "warn" | "log" | "allow";
  audit_log: boolean;
}

export interface PolicyData {
  roles: Record<string, string[]>;
  permissions: Record<string, string[]>;
}
```

## Advanced Features

### Optional Fields

Optional ADL fields become optional TypeScript fields:

```adl
type Config {
  required: string
  optional?: string
}
```

```typescript
export interface Config {
  required: string;
  optional?: string;
}
```

### Union Types

ADL union types become TypeScript union types:

```adl
type Result = string | integer
```

```typescript
export type Result = string | number;
```

### Array Types

ADL array types become TypeScript array types:

```adl
type List {
  items: string[]
}
```

```typescript
export interface List {
  items: string[];
}
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

Generated TypeScript (`my-agent.ts`):

```typescript
export enum Lifecycle {
  stable,
  beta,
  deprecated
}

export interface Config {
  timeout: number;
  retries: number;
}

export interface Tool {
  name: string;
  description: string;
  parameters: Record<string, any>;
}

export type MyAgent = {
  id: string;
  name: string;
  version: number;
  lifecycle: Lifecycle;
  config: Config;
  tools: Tool[];
};
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

Generated TypeScript (`workflow.ts`):

```typescript
export interface WorkflowNode {
  id: string;
  type: string;
  label: string;
  config: Record<string, any>;
  position: { x: number; y: number };
}

export interface WorkflowEdge {
  id: string;
  source: string;
  target: string;
  relation: string;
  condition?: Record<string, any>;
  metadata?: Record<string, any>;
}

export interface Workflow {
  id: string;
  name: string;
  version: string;
  description: string;
  nodes: Record<string, WorkflowNode>;
  edges: WorkflowEdge[];
  metadata?: Record<string, any>;
}
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

Use the `--docs` flag to include JSDoc comments:

```bash
adl-generate my-agent.adl --typescript --docs -o my-agent.ts
```

### 3. Use Watch Mode During Development

Enable watch mode to automatically regenerate TypeScript when ADL changes:

```bash
adl-generate my-agent.adl --typescript --watch
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

Always validate your ADL files before generating TypeScript:

```bash
adl-validate my-agent.adl
adl-generate my-agent.adl --typescript -o my-agent.ts
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
  optional?: string  # This will be optional in TypeScript
}
```

### Issue: Union types not working

**Cause**: Union types require proper syntax in ADL.

**Solution**: Use the `|` operator for union types:

```adl
type Result = string | integer | boolean
```

## Integration with TypeScript Projects

### Using Generated Types

Import the generated types in your TypeScript project:

```typescript
import { MyAgent, Config, Tool } from './my-agent';

const agent: MyAgent = {
  id: "agent-001",
  name: "My Agent",
  version: 1,
  config: {
    timeout: 30,
    retries: 3
  },
  tools: []
};
```

### Type Checking

The generated types provide full type checking:

```typescript
function processAgent(agent: MyAgent) {
  // TypeScript will enforce type safety
  console.log(agent.name);
  console.log(agent.config.timeout);
}

// This will cause a type error
const invalidAgent: MyAgent = {
  id: "agent-001",
  // Missing required fields
};
```

### IDE Support

The generated types work with all TypeScript IDEs:
- VS Code
- WebStorm
- IntelliJ IDEA
- Vim/Neovim with TypeScript plugins

## See Also

- [Python Binding Generator](python-generator.md)
- [CLI Reference](tools/cli.md)
- [ADL Schema Reference](schema-reference.md)
- [Phase 4: Workflow & DAG](workflow-dag.md)
- [Phase 4: Policy-as-Code](policy-as-code.md)
