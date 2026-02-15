# ADL DSL Design Document

## Overview

ADL DSL (Domain-Specific Language) is a custom language for defining agent schemas that enables true modularization without JSON Schema constraints.

## Why DSL?

### JSON Schema Limitations
- Vocabulary system prevents external `$ref` resolution
- Complex meta-schema dependencies
- Network requirements for validation
- Memory issues with large schemas
- Limited extensibility

### DSL Benefits
- True modularization with imports
- Self-contained validation
- Better error messages
- Custom syntax for ADL concepts
- No external dependencies
- Easier to read and write

## DSL Syntax

### Basic Structure

```adl
# Import modules
import schema/components/rag
import schema/components/tool
import schema/components/memory

# Define agent schema
agent AgentDefinition {
  # Core fields
  id: string
  version: integer
  version_string: string
  name: string
  description: string
  role: string
  llm: string
  
  # Optional fields
  lifecycle?: Lifecycle
  compatibility?: Compatibility
  change_log?: ChangeLog
  
  # Complex fields
  llm_settings: LlmSettings
  tools: ToolDefinition[]
  rag: RagIndex[]
  memory?: MemoryDefinition
  
  # v2 fields
  agent_roles?: AgentRole[]
  execution_constraints?: ExecutionConstraints
  events?: EventDefinition[]
}
```

### Type Definitions

```adl
# Primitive types
type string
type integer
type number
type boolean

# Enum types
enum Lifecycle {
  stable
  beta
  deprecated
  experimental
}

enum ChangeType {
  breaking
  non-breaking
  patch
}

enum MemoryType {
  episodic
  semantic
  working
  hybrid
}

enum RoleType {
  Coordinator
  Worker
  Supervisor
  Critic
}

enum EventType {
  tool_invocation
  task_completion
  error_occurred
  memory_update
  state_change
}

enum ActionType {
  invoke_tool
  update_memory
  send_message
  log_event
}

enum RoutingStrategy {
  round_robin
  least_loaded
  priority_based
  task_based
}

enum EvictionPolicy {
  lru
  lfu
  fifo
  random
}

enum HybridStrategy {
  weighted
  reciprocal_rank_fusion
  rrf
}

enum EscalationPolicy {
  none
  manual
  automatic
}
```

### Complex Types

```adl
# Object types
type LlmSettings {
  temperature: number
  max_tokens: integer
  model_routing?: ModelRouting
  model_constraints?: ModelConstraints
}

type ModelRouting {
  enabled: boolean
  primary_model: string
  fallback_models: string[]
  specialized_models: SpecializedModel[]
  routing_strategy: RoutingStrategy
}

type SpecializedModel {
  model: string
  task_types: string[]
  priority: integer (1..10)
}

type ModelConstraints {
  max_tokens_per_request: integer
  max_requests_per_minute: integer
  cost_limit_per_hour: number
  timeout_seconds: integer
}

type ToolDefinition {
  id?: string
  tool_id?: string
  version?: integer
  name: string
  display_name?: string
  description: string
  category?: string
  subcategory?: string
  parameters: ToolParameter[]
  returns?: ToolReturnSchema
  invocation?: ToolInvocation
  keys_schema?: KeySchemaItem[]
  permissions?: ToolPermissions
  sources?: string[]
  dependencies?: string[]
  status?: ToolStatus
  visibility?: ToolVisibility
  created_at?: string
  created_by?: string
  code_file?: string
}

type ToolParameter {
  name: string
  type: string
  description: string
  required: boolean
  default?: string | number | boolean | object | array | null
  enum?: any[]
  minimum?: number
  maximum?: number
  exclusiveMinimum?: number
  exclusiveMaximum?: number
  minLength?: integer
  maxLength?: integer
  minItems?: integer
  maxItems?: integer
  multipleOf?: number
  pattern?: string
  format?: string
  properties?: object
  required_properties?: string[]
  uniqueItems?: boolean
  oneOf?: any[]
  anyOf?: any[]
  allOf?: any[]
}

type ToolReturnSchema {
  type: string
  description: string
  content_type?: string
  schema: object | string
  examples?: any[]
}

type ToolInvocation {
  type: string
  function?: string
}

type KeySchemaItem {
  name: string
  key_type: string
  description: string
}

type ToolPermissions {
  file_read: string[]
  file_write: string[]
  network: boolean
  env_vars: string[]
}

type ToolStatus {
  active
  deprecated
  experimental
}

type ToolVisibility {
  public
  private
  internal
}

type RagIndex {
  id: string
  name: string
  rag_type: string
  virtual_index_path: string
  location_type: string
  remote_path?: string | null
  metadata: object
  hierarchical_config?: HierarchicalConfig
  search_config?: SearchConfig
  cross_file_references?: CrossFileReferences
}

type HierarchicalConfig {
  enabled: boolean
  levels: HierarchicalLevel[]
}

type HierarchicalLevel {
  level: integer (1..)
  chunk_size: integer (1..)
  overlap: integer (0..)
  parent_index?: string
}

type SearchConfig {
  vector_search?: VectorSearchConfig
  keyword_search?: KeywordSearchConfig
  hybrid_strategy?: HybridStrategy
  fusion_weight?: number (0..1)
}

type VectorSearchConfig {
  enabled: boolean
  top_k: integer (1..)
  similarity_threshold: number (0..1)
}

type KeywordSearchConfig {
  enabled: boolean
  top_k: integer (1..)
  bm25_weight: number (0..1)
}

type CrossFileReferences {
  enabled: boolean
  reference_types: ReferenceType[]
  max_depth: integer (1..)
}

type ReferenceType {
  citation
  hyperlink
  semantic
  custom
}

type MemoryDefinition {
  type: MemoryType
  scope: MemoryScope
  backend: MemoryBackend
  retention: RetentionPolicyConfig
  write_policy: MemoryWritePolicy
  read_policy: MemoryReadPolicy
  privacy: PrivacySettings
  lifecycle_management?: LifecycleManagement
  eviction_policy?: EvictionPolicyConfig
  storage_strategy?: StorageStrategy
}

type MemoryScope {
  session
  user
  org
  global
}

type MemoryBackend {
  vector
  kv
  graph
  external
}

type RetentionPolicyConfig {
  policy: RetentionPolicyType
  duration?: string
}

type RetentionPolicyType {
  ttl
  versioned
  append_only
}

type MemoryWritePolicy {
  explicit
  implicit
}

type MemoryReadPolicy {
  on_demand
  always
}

type PrivacySettings {
  pii: boolean
  encryption: boolean
}

type LifecycleManagement {
  auto_cleanup: boolean
  cleanup_interval_hours: integer (1..)
  max_entries: integer (1..)
}

type EvictionPolicyConfig {
  policy: EvictionPolicy
  threshold_percentage: integer (1..100)
  preserve_recent: boolean
  preserve_important: boolean
}

type StorageStrategy {
  compression: boolean
  indexing: boolean
  caching: boolean
}

type AgentRole {
  role_id: string
  role_type: RoleType
  capabilities: string[]
  constraints: RoleConstraints
  communication: CommunicationProtocol
}

type RoleConstraints {
  max_concurrent_tasks: integer (1..)
  allowed_tools: string[]
  forbidden_tools: string[]
}

type CommunicationProtocol {
  can_receive_from: RoleType[]
  can_send_to: RoleType[]
}

type ExecutionConstraints {
  time_limits: TimeLimits
  memory_limits: MemoryLimits
  resource_quotas: ResourceQuotas
  capability_negotiation: CapabilityNegotiation
}

type TimeLimits {
  max_execution_time_seconds: integer (1..)
  timeout_seconds: integer (1..)
  idle_timeout_seconds: integer (1..)
}

type MemoryLimits {
  max_memory_mb: integer (1..)
  memory_quota_mb: integer (1..)
  max_context_tokens: integer (1..)
}

type ResourceQuotas {
  max_api_calls_per_hour: integer (1..)
  max_tokens_per_request: integer (1..)
  max_tool_calls_per_task: integer (1..)
  max_concurrent_tasks: integer (1..)
}

type CapabilityNegotiation {
  enabled: boolean
  allowed_capabilities: string[]
  forbidden_capabilities: string[]
  escalation_policy: EscalationPolicy
}

type EventDefinition {
  event_id: string
  event_type: EventType
  trigger: TriggerConfig
  actions: Action[]
  subscription: SubscriptionConfig
}

type TriggerConfig {
  condition?: string
  source?: string
  filters?: object
}

type Action {
  action_type: ActionType
  target: string
  parameters?: object
  priority: integer (1..10)
}

type SubscriptionConfig {
  enabled: boolean
  handler?: string
  retry_policy: RetryPolicy
}

type RetryPolicy {
  max_retries: integer (0..)
  backoff_ms: integer (0..)
}

type Compatibility {
  adl_spec?: string
  previous_versions?: string[]
}

type ChangeLog {
  type: ChangeType
  summary?: string
  details?: string[]
}
```

### Module System

```adl
# schema/components/rag.adl
module rag {
  export RagIndex
  export HierarchicalConfig
  export SearchConfig
  export CrossFileReferences
}

# schema/components/tool.adl
module tool {
  export ToolDefinition
  export ToolParameter
  export ToolReturnSchema
  export ToolInvocation
  export KeySchemaItem
  export ToolPermissions
}

# schema/components/memory.adl
module memory {
  export MemoryDefinition
  export LifecycleManagement
  export EvictionPolicyConfig
  export StorageStrategy
}

# schema/components/common.adl
module common {
  export PrivacySettings
  export RetentionPolicyConfig
}
```

### Validation Rules

```adl
# Validation rules
validation {
  # Required fields
  required: [id, version, name, description, role, llm, llm_settings, tools]
  
  # Field constraints
  id: pattern("^[a-zA-Z0-9_-]+$")
  version: minimum(1)
  name: minLength(1), maxLength(100)
  description: minLength(10)
  
  # Array constraints
  tools: minItems(0)
  rag: minItems(0)
  
  # Custom validations
  validate_agent_roles: max_roles(4)
  validate_events: no_cycles()
  validate_rag: hierarchical_levels(3)
}
```

## DSL to JSON Schema Generation

The DSL compiler will generate JSON Schema from DSL definitions:

```python
# Pseudocode
def compile_dsl_to_json_schema(dsl_file):
    # Parse DSL
    ast = parse_dsl(dsl_file)
    
    # Resolve imports
    modules = resolve_imports(ast.imports)
    
    # Build type definitions
    types = build_type_definitions(ast, modules)
    
    # Generate JSON Schema
    schema = {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "$id": "https://example.com/schemas/agent-definition.json",
        "title": "Agent Definition",
        "type": "object",
        "properties": build_properties(ast),
        "required": build_required(ast),
        "additionalProperties": False
    }
    
    # Add definitions
    schema["$defs"] = build_definitions(types)
    
    return schema
```

## Benefits

1. **True Modularization**: Import modules without JSON Schema constraints
2. **Better Error Messages**: Custom error messages for ADL concepts
3. **Type Safety**: Compile-time type checking
4. **Self-Contained**: No external dependencies for validation
5. **Extensible**: Easy to add new features
6. **Readable**: More readable than JSON Schema
7. **Maintainable**: Easier to maintain and update

## Migration Path

1. **Phase 1**: Create DSL compiler
2. **Phase 2**: Convert existing schema to DSL
3. **Phase 3**: Generate JSON Schema from DSL
4. **Phase 4**: Validate examples against generated schema
5. **Phase 5**: Deprecate direct JSON Schema editing

## Example Usage

```bash
# Compile DSL to JSON Schema
adl compile schema/agent-definition.adl -o schema/agent-definition.schema.json

# Validate agent against DSL
adl validate examples/multi_agent_team.json --schema schema/agent-definition.adl

# Generate TypeScript types
adl generate-types schema/agent-definition.adl -o types/agent-definition.d.ts

# Format DSL
adl format schema/agent-definition.adl

# Lint DSL
adl lint schema/agent-definition.adl
```
