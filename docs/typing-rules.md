# Unified Typing Rules

## Overview

ADL enforces strict typing rules across all schema components to ensure consistency, type safety, and predictability.

## Core Principles

1. **No "any" Types**: All types must be explicitly defined
2. **Type Consistency**: Same concepts use the same types across the schema
3. **Union Types**: Use union types for multiple valid values (e.g., `string | null`)
4. **Enum Types**: Use enums for fixed sets of values
5. **Array Types**: Always specify item types for arrays

## Type Categories

### Primitive Types

- `string`: Text values
- `number`: Numeric values (integer or float)
- `integer`: Whole numbers only
- `boolean`: true/false values
- `null`: Explicit null values

### Complex Types

- `object`: Key-value pairs with defined structure
- `array`: Ordered lists with defined item types

### Special Types

- `string | null`: Optional string values
- `string | number`: Multiple primitive types
- `object | string`: Flexible schema references

## Type Definitions

### Lifecycle Types

```typescript
type Lifecycle = "stable" | "beta" | "deprecated" | "experimental";
```

### Memory Types

```typescript
type MemoryType = "episodic" | "semantic" | "working" | "hybrid";
type MemoryScope = "session" | "user" | "org" | "global";
type MemoryBackend = "vector" | "kv" | "graph" | "external";
```

### Tool Types

```typescript
type ToolStatus = "active" | "deprecated" | "experimental";
type ToolVisibility = "public" | "private" | "internal";
```

### Return Types

```typescript
type ReturnTypeCategory =
  | "ObjectResult"
  | "EntityResult"
  | "OperationStatus"
  | "StringValue"
  | "NumberValue"
  | "BooleanValue"
  | "IdentifierValue"
  | "ListResult"
  | "BatchResult"
  | "FileResult"
  | "MediaResult"
  | "EventStream"
  | "ChunkedData"
  | "VoidResult"
  | "Custom";
```

## Type Validation Rules

### 1. No "any" Types

❌ **Invalid**:
```json
{
  "type": "any"
}
```

✅ **Valid**:
```json
{
  "type": "string"
}
```

### 2. Explicit Array Item Types

❌ **Invalid**:
```json
{
  "type": "array"
}
```

✅ **Valid**:
```json
{
  "type": "array",
  "items": {
    "type": "string"
  }
}
```

### 3. Use Enums for Fixed Values

❌ **Invalid**:
```json
{
  "type": "string",
  "description": "Lifecycle status"
}
```

✅ **Valid**:
```json
{
  "type": "string",
  "enum": ["stable", "beta", "deprecated", "experimental"],
  "description": "Lifecycle status"
}
```

### 4. Union Types for Optional Values

❌ **Invalid**:
```json
{
  "type": "string"
}
```

✅ **Valid**:
```json
{
  "type": ["string", "null"]
}
```

## TypeScript Definitions

TypeScript type definitions are provided in `types/agent-definition.d.ts` for:

- Type checking in TypeScript projects
- IDE autocomplete and IntelliSense
- Compile-time type validation
- Documentation of type structure

## Verification

To verify typing rules compliance:

```bash
# Check for "any" types
grep -r '"type": "any"' schema/

# Should return no results
```

## Benefits

1. **Type Safety**: Catch type errors at validation time
2. **Predictability**: Clear expectations for data types
3. **Documentation**: Types serve as inline documentation
4. **Tooling Support**: Better IDE support with TypeScript definitions
5. **Consistency**: Uniform type usage across the schema
