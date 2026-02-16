export interface Compatibility {
  adl_spec?: string
  previous_versions?: string[]
}

export interface ChangeLog {
  type: "breaking" | "non-breaking" | "patch"
  summary?: string
  details?: string[]
}

export interface SpecializedModel {
  model: string
  task_types: string[]
  priority: number
}

export interface ModelRouting {
  enabled: boolean
  primary_model: string
  fallback_models: string[]
  specialized_models: SpecializedModel[]
  routing_strategy: "round_robin" | "least_loaded" | "priority_based" | "task_based"
}

export interface ModelConstraints {
  max_tokens_per_request: number
  max_requests_per_minute: number
  cost_limit_per_hour: number
  timeout_seconds: number
}

export interface LlmSettings {
  temperature: number
  max_tokens: number
  model_routing?: ModelRouting
  model_constraints?: ModelConstraints
}

export interface ToolParameter {
  name: string
  type: string
  description: string
  required?: boolean
  default?: string | number | boolean | Record<string, unknown> | unknown[] | unknown
  enum?: unknown[]
  minimum?: number
  maximum?: number
  exclusiveMinimum?: number
  exclusiveMaximum?: number
  minLength?: number
  maxLength?: number
  minItems?: number
  maxItems?: number
  multipleOf?: number
  pattern?: string
  format?: string
  properties?: Record<string, unknown>
  required_properties?: string[]
  uniqueItems?: boolean
}

export interface ToolReturnSchema {
  type: string
  description: string
  content_type?: string
  schema: unknown
  examples?: unknown[]
}

export interface ToolInvocation {
  type: string
  function?: string
}

export interface KeySchemaItem {
  name: string
  key_type: string
  description: string
}

export interface ToolPermissions {
  file_read: string[]
  file_write: string[]
  network: boolean
  env_vars: string[]
}

export interface ToolDefinition {
  id?: string
  tool_id?: string
  version?: number
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
  status?: string
  visibility?: string
  created_at?: string
  created_by?: string
  code_file?: string
}

export interface HierarchicalLevel {
  level: number
  chunk_size: number
  overlap: number
  parent_index?: string
}

export interface HierarchicalConfig {
  enabled: boolean
  levels: HierarchicalLevel[]
}

export interface VectorSearchConfig {
  enabled: boolean
  top_k: number
  similarity_threshold: number
}

export interface KeywordSearchConfig {
  enabled: boolean
  top_k: number
  bm25_weight: number
}

export interface SearchConfig {
  vector_search?: VectorSearchConfig
  keyword_search?: KeywordSearchConfig
  hybrid_strategy?: "weighted" | "reciprocal_rank_fusion" | "rrf"
  fusion_weight?: number
}

export interface CrossFileReferences {
  enabled: boolean
  reference_types: string[]
  max_depth: number
}

export interface RagIndex {
  id: string
  name: string
  rag_type: string
  virtual_index_path: string
  location_type: string
  remote_path?: string | unknown
  metadata: Record<string, unknown>
  hierarchical_config?: HierarchicalConfig
  search_config?: SearchConfig
  cross_file_references?: CrossFileReferences
}

export interface RetentionPolicyConfig {
  policy: string
  duration?: string
}

export interface PrivacySettings {
  pii: boolean
  encryption: boolean
}

export interface LifecycleManagement {
  auto_cleanup: boolean
  cleanup_interval_hours: number
  max_entries: number
}

export interface EvictionPolicyConfig {
  policy: "lru" | "lfu" | "fifo" | "random"
  threshold_percentage: number
  preserve_recent: boolean
  preserve_important: boolean
}

export interface StorageStrategy {
  compression: boolean
  indexing: boolean
  caching: boolean
}

export interface MemoryDefinition {
  type: "episodic" | "semantic" | "working" | "hybrid"
  scope: string
  backend: string
  retention: RetentionPolicyConfig
  write_policy: string
  read_policy: string
  privacy: PrivacySettings
  lifecycle_management?: LifecycleManagement
  eviction_policy?: EvictionPolicyConfig
  storage_strategy?: StorageStrategy
}

export interface RoleConstraints {
  max_concurrent_tasks: number
  allowed_tools: string[]
  forbidden_tools: string[]
}

export interface CommunicationProtocol {
  can_receive_from: "Coordinator" | "Worker" | "Supervisor" | "Critic"[]
  can_send_to: "Coordinator" | "Worker" | "Supervisor" | "Critic"[]
}

export interface AgentRole {
  role_id: string
  role_type: "Coordinator" | "Worker" | "Supervisor" | "Critic"
  capabilities: string[]
  constraints: RoleConstraints
  communication: CommunicationProtocol
}

export interface TimeLimits {
  max_execution_time_seconds: number
  timeout_seconds: number
  idle_timeout_seconds: number
}

export interface MemoryLimits {
  max_memory_mb: number
  memory_quota_mb: number
  max_context_tokens: number
}

export interface ResourceQuotas {
  max_api_calls_per_hour: number
  max_tokens_per_request: number
  max_tool_calls_per_task: number
  max_concurrent_tasks: number
}

export interface CapabilityNegotiation {
  enabled: boolean
  allowed_capabilities: string[]
  forbidden_capabilities: string[]
  escalation_policy: "none" | "manual" | "automatic"
}

export interface ExecutionConstraints {
  time_limits: TimeLimits
  memory_limits: MemoryLimits
  resource_quotas: ResourceQuotas
  capability_negotiation: CapabilityNegotiation
}

export interface TriggerConfig {
  condition?: string
  source?: string
  filters?: Record<string, unknown>
}

export interface Action {
  action_type: "invoke_tool" | "update_memory" | "send_message" | "log_event"
  target: string
  parameters?: Record<string, unknown>
  priority: number
}

export interface RetryPolicy {
  max_retries: number
  backoff_ms: number
}

export interface SubscriptionConfig {
  enabled: boolean
  handler?: string
  retry_policy: RetryPolicy
}

export interface EventDefinition {
  event_id: string
  event_type: "tool_invocation" | "task_completion" | "error_occurred" | "memory_update" | "state_change"
  trigger: TriggerConfig
  actions: Action[]
  subscription: SubscriptionConfig
}

export interface AgentDefinition {
  id: string
  version: number
  version_string?: string
  lifecycle?: "stable" | "beta" | "deprecated" | "experimental"
  compatibility?: Compatibility
  change_log?: ChangeLog
  name: string
  description: string
  role: string
  llm: string
  llm_settings: LlmSettings
  tools: ToolDefinition[]
  rag: RagIndex[]
  memory?: MemoryDefinition
  owner?: string
  document_index_id?: string
  agent_roles?: AgentRole[]
  execution_constraints?: ExecutionConstraints
  events?: EventDefinition[]
}