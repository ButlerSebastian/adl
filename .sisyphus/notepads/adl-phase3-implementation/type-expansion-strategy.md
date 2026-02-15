# ADL DSL Compiler - Type Expansion Strategy

## 1. Overview

The ADL DSL compiler needs to transform ADL DSL files (`.adl`) into complete JSON Schema definitions. The current schema structure is complex with deeply nested types, requiring a systematic expansion strategy to resolve all type references and produce fully expanded schemas.

## 2. Current Schema Structure Analysis

### 2.1 Core Agent Definition
The main `AgentDefinition` type contains:
- **Basic metadata**: id, version, lifecycle, compatibility, change_log
- **Agent properties**: name, description, role, llm, llm_settings
- **Capabilities**: tools, rag, memory, agent_roles, execution_constraints, events

### 2.2 Complex Type Hierarchy

#### 2.2.1 LlmSettings
- `temperature`: number
- `max_tokens`: integer
- `model_routing?`: ModelRouting
- `model_constraints?`: ModelConstraints

#### 2.2.2 ToolDefinition
- `id?`: string
- `tool_id?`: string
- `version?`: integer
- `name`: string
- `display_name?`: string
- `description`: string
- `category?`: string
- `subcategory?`: string
- `parameters`: ToolParameter[]
- `returns?`: ToolReturnSchema
- `invocation?`: ToolInvocation
- `keys_schema?`: KeySchemaItem[]
- `permissions?`: ToolPermissions
- `sources?`: string[]
- `dependencies?`: string[]
- `status?`: ToolStatus
- `visibility?`: ToolVisibility
- `created_at?`: string
- `created_by?`: string
- `code_file?`: string

#### 2.2.3 RagIndex
- `id`: string
- `name`: string
- `rag_type`: string
- `virtual_index_path`: string
- `location_type`: string
- `remote_path?`: string | null
- `metadata`: object
- `hierarchical_config?`: HierarchicalConfig
- `search_config?`: SearchConfig
- `cross_file_references?`: CrossFileReferences

#### 2.2.4 MemoryDefinition
- `type`: MemoryType
- `scope`: MemoryScope
- `backend`: MemoryBackend
- `retention`: RetentionPolicyConfig
- `write_policy`: MemoryWritePolicy
- `read_policy`: MemoryReadPolicy
- `privacy`: PrivacySettings
- `lifecycle_management?`: LifecycleManagement
- `eviction_policy?`: EvictionPolicyConfig
- `storage_strategy?`: StorageStrategy

### 2.3 Enum Types
- `Lifecycle`: stable, beta, deprecated, experimental
- `ChangeType`: breaking, non-breaking, patch
- `MemoryType`: episodic, semantic, working, hybrid
- `RoleType`: Coordinator, Worker, Supervisor, Critic
- `EventType`: tool_invocation, task_completion, error_occurred, memory_update, state_change
- `ActionType`: invoke_tool, update_memory, send_message, log_event
- `RoutingStrategy`: round_robin, least_loaded, priority_based, task_based
- `EvictionPolicy`: lru, lfu, fifo, random
- `HybridStrategy`: weighted, reciprocal_rank_fusion, rrf
- `EscalationPolicy`: none, manual, automatic

## 3. Type Expansion Strategy

### 3.1 Expansion Phases

#### Phase 1: Parse DSL Structure
- Parse imports, enums, types, and agent definitions
- Build internal type registry with references
- Handle nested type definitions and constraints

#### Phase 2: Resolve Type References
- Create a dependency graph of type references
- Topologically sort types for expansion
- Handle circular references with detection

#### Phase 3: Expand Nested Types
- Recursively expand all type references
- Apply constraints and validation rules
- Handle unions, arrays, and optional fields

#### Phase 4: Generate Output Schemas
- Produce fully expanded JSON Schema
- Generate TypeScript type definitions
- Validate output against schema

### 3.2 Type Resolution Algorithm

```
1. Parse DSL file into AST
2. Build type registry:
   - Enums: name -> [values]
   - Types: name -> TypeDefinition
3. Create reference graph:
   - For each type, find all _type_ref references
   - Build adjacency list
4. Detect cycles in reference graph
5. Topologically sort types (if no cycles)
6. For each type in topological order:
   - Expand all nested type references
   - Apply constraints and validation
   - Generate JSON Schema definition
7. Add all definitions to $defs
8. Generate main agent schema with references
```

### 3.3 Handling Different Type Categories

#### 3.3.1 Primitive Types
- Direct mapping to JSON Schema types
- No further expansion needed

#### 3.3.2 Enum Types
- Convert to JSON Schema `enum` property
- Store in definitions for reuse

#### 3.3.3 Object Types
- Expand all property types recursively
- Handle optional vs required properties
- Manage additionalProperties setting

#### 3.3.4 Array Types
- Expand item types recursively
- Handle array-specific constraints

#### 3.3.5 Union Types
- Expand each union member type
- Handle `null` as nullable types
- Support complex union structures

#### 3.3.6 Optional Fields
- Mark with `?` in DSL
- Remove from required list
- Keep in properties

### 3.4 Constraint Application

#### 3.4.1 Type Constraints
- Numeric: minimum, maximum, exclusiveMinimum, exclusiveMaximum, multipleOf
- String: minLength, maxLength, pattern, format
- Array: minItems, maxItems, uniqueItems
- Object: properties, required_properties

#### 3.4.2 Validation Rules
- Required field validation
- Type compatibility checks
- Constraint satisfaction verification

## 4. Implementation Plan

### 4.1 Current Compiler Analysis

The existing `ADLDSLCompiler` class has:
1. **Basic parsing**: imports, enums, types, agent definitions
2. **Type registry**: stores TypeDefinition objects
3. **Recursive expansion**: `_expand_schema_recursive` method
4. **JSON Schema generation**: `compile_to_json_schema` method
5. **TypeScript generation**: `generate_typescript_types` method

### 4.2 Key Improvements Needed

#### 4.2.1 Enhanced Type Resolution
- Implement proper topological sorting
- Add cycle detection
- Support forward references

#### 4.2.2 Constraint Propagation
- Apply numeric constraints to expanded types
- Validate string patterns and formats
- Enforce array size limits

#### 4.2.3 Validation Integration
- Add schema validation after expansion
- Include constraint satisfaction checks
- Provide detailed error reporting

#### 4.2.4 Module System Support
- Handle imports from other DSL files
- Resolve cross-module type references
- Support circular imports with detection

### 4.3 Expansion Pipeline

```
DSL File (.adl)
    ↓
[Phase 1: Parsing]
    ↓
AST with Type References
    ↓
[Phase 2: Resolution]
    ↓
Dependency Graph
    ↓
[Phase 3: Expansion]
    ↓
Fully Expanded Types
    ↓
[Phase 4: Generation]
    ↓
JSON Schema (.json)
    ↓
TypeScript Types (.d.ts)
```

## 5. Edge Cases and Complex Scenarios

### 5.1 Nested Object Structures
- Objects within objects within arrays
- Recursive type definitions
- Deeply nested constraints

### 5.2 Union Type Complexity
- Unions of objects with different properties
- Nullable nested types
- Mixed primitive and object unions

### 5.3 Circular References
- Direct circular references (A -> A)
- Indirect circular references (A -> B -> A)
- Complex dependency cycles

### 5.4 Constraint Inheritance
- Constraints on type references
- Overriding constraints
- Constraint validation across expansions

## 6. Verification Strategy

### 6.1 Schema Validation
- Validate expanded JSON Schema against JSON Schema draft
- Check for unresolved references
- Verify constraint satisfaction

### 6.2 TypeScript Compatibility
- Ensure generated TypeScript types compile
- Verify type safety with sample data
- Test with TypeScript strict mode

### 6.3 Round-trip Testing
- Compile DSL to JSON Schema
- Validate sample data against schema
- Generate TypeScript types and test type inference

### 6.4 Edge Case Coverage
- Test deeply nested structures
- Validate union type handling
- Verify circular reference detection

## 7. Risk Assessment

### 7.1 Technical Risks
1. **Infinite recursion**: Unhandled circular references
2. **Constraint conflicts**: Overlapping or contradictory constraints
3. **Performance issues**: Deeply nested expansions

### 7.2 Mitigation Strategies
1. **Depth limiting**: Maximum expansion depth
2. **Constraint validation**: Early detection of conflicts
3. **Caching**: Memoize expanded type definitions

## 8. Next Steps

### 8.1 Immediate Actions
1. **Implement topological sorting** for type resolution
2. **Add cycle detection** to prevent infinite recursion
3. **Enhance constraint propagation** across nested types

### 8.2 Short-term Goals
1. **Complete type expansion** for all complex types
2. **Generate fully expanded JSON Schema**
3. **Produce TypeScript type definitions**

### 8.3 Long-term Vision
1. **Support for cross-module type references**
2. **Advanced constraint validation**
3. **Integration with broader ADL ecosystem**

---

## Appendix A: Type Reference Examples

### A.1 Simple Type Reference
```adl
type LlmSettings {
  temperature: number
  max_tokens: integer
  model_routing?: ModelRouting
}
```

### A.2 Array Type Reference
```adl
type AgentDefinition {
  tools: ToolDefinition[]
}
```

### A.3 Union Type Reference
```adl
type ToolParameter {
  default?: string | number | boolean | object | array | null
}
```

### A.4 Constrained Type Reference
```adl
type SpecializedModel {
  priority: integer (1..10)
}
```

## Appendix B: Expansion Examples

### B.1 Before Expansion
```json
{
  "type": "object",
  "properties": {
    "llm_settings": {
      "_type_ref": "LlmSettings"
    }
  }
}
```

### B.2 After Expansion
```json
{
  "type": "object",
  "properties": {
    "llm_settings": {
      "type": "object",
      "properties": {
        "temperature": {"type": "number"},
        "max_tokens": {"type": "integer"},
        "model_routing": {
          "type": "object",
          "properties": {
            "enabled": {"type": "boolean"},
            "primary_model": {"type": "string"},
            "fallback_models": {
              "type": "array",
              "items": {"type": "string"}
            },
            "specialized_models": {
              "type": "array",
              "items": {
                "type": "object",
                "properties": {
                  "model": {"type": "string"},
                  "task_types": {
                    "type": "array",
                    "items": {"type": "string"}
                  },
                  "priority": {
                    "type": "integer",
                    "minimum": 1,
                    "maximum": 10
                  }
                },
                "required": ["model", "task_types", "priority"]
              }
            },
            "routing_strategy": {
              "type": "string",
              "enum": ["round_robin", "least_loaded", "priority_based", "task_based"]
            }
          },
          "required": ["enabled", "primary_model", "routing_strategy"]
        }
      },
      "required": ["temperature", "max_tokens"]
    }
  }
}
```

## Appendix C: Constraint Propagation Rules

### C.1 Numeric Constraints
- `minimum`: Must be ≤ `maximum` if both present
- `exclusiveMinimum`: Must be < `exclusiveMaximum` if both present
- `multipleOf`: Must be positive number

### C.2 String Constraints
- `pattern`: Valid regex pattern
- `format`: Supported JSON Schema format (date-time, email, etc.)
- `minLength`: Must be ≤ `maxLength` if both present

### C.3 Array Constraints
- `minItems`: Must be ≤ `maxItems` if both present
- `uniqueItems`: Boolean constraint only