/**
 * ADL Agent Definition TypeScript Types
 *
 * This file provides TypeScript type definitions for the ADL Agent Definition schema.
 * All types are explicitly defined following unified typing rules.
 */

// ==================== Base Types ====================

/**
 * UUID or similar unique identifier
 */
export type UUID = string;

/**
 * Semantic version string (e.g., '1.2.0')
 */
export type SemanticVersion = string;

/**
 * ISO-8601 timestamp
 */
export type ISOTimestamp = string;

// ==================== Enums ====================

/**
 * Lifecycle status of an agent version
 */
export type Lifecycle = "stable" | "beta" | "deprecated" | "experimental";

/**
 * Type of change in a version
 */
export type ChangeType = "breaking" | "non-breaking" | "patch";

/**
 * Retention policy type
 */
export type RetentionPolicyType = "ttl" | "versioned" | "append-only";

/**
 * Memory system type
 */
export type MemoryType = "episodic" | "semantic" | "working" | "hybrid";

/**
 * Memory visibility and sharing scope
 */
export type MemoryScope = "session" | "user" | "org" | "global";

/**
 * Backend storage type for memory
 */
export type MemoryBackend = "vector" | "kv" | "graph" | "external";

/**
 * Memory write policy
 */
export type MemoryWritePolicy = "explicit" | "implicit";

/**
 * Memory read policy
 */
export type MemoryReadPolicy = "on_demand" | "always";

/**
 * Return type category
 */
export type ReturnTypeCategory =
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

/**
 * Tool lifecycle status
 */
export type ToolStatus = "active" | "deprecated" | "experimental";

/**
 * Tool visibility
 */
export type ToolVisibility = "public" | "private" | "internal";

/**
 * Key type for environment variables
 */
export type KeyType = "environment_variable" | "api_key" | "secret_key" | "access_token";

// ==================== Interfaces ====================

/**
 * Privacy and security settings for memory
 */
export interface MemoryPrivacy {
  /** Whether memory may contain personally identifiable information */
  pii?: boolean;
  
  /** Whether memory data should be encrypted at rest */
  encryption?: boolean;
}

/**
 * Retention policy for memory data
 */
export interface MemoryRetention {
  /** Retention policy type */
  policy: RetentionPolicyType;
  
  /** Duration for retention (e.g., '30d', '7d', '1h') */
  duration?: string;
}

/**
 * Memory configuration for the agent
 */
export interface MemoryDefinition {
  /** Type of memory system */
  type?: MemoryType;
  
  /** Scope of memory visibility and sharing */
  scope?: MemoryScope;
  
  /** Backend storage type for memory */
  backend?: MemoryBackend;
  
  /** Retention policy for memory data */
  retention?: MemoryRetention;
  
  /** When memory writes occur */
  write_policy?: MemoryWritePolicy;
  
  /** When memory reads occur */
  read_policy?: MemoryReadPolicy;
  
  /** Privacy and security settings for memory */
  privacy?: MemoryPrivacy;
}

/**
 * RAG index definition
 */
export interface RagIndex {
  /** Unique ID of the RAG index */
  id: string;
  
  /** Human-readable name for the RAG index */
  name: string;
  
  /** Type of RAG index (e.g., 'doc', 'code', 'image') */
  rag_type: string;
  
  /** Virtual path or logical mount point under which this index is exposed */
  virtual_index_path: string;
  
  /** Location type, e.g., 'local', 's3', 'gcs', etc. */
  location_type: string;
  
  /** Optional remote path or bucket/key for the index */
  remote_path: string | null;
  
  /** Arbitrary metadata associated with this RAG index */
  metadata: Record<string, any>;
}

/**
 * Key schema item
 */
export interface KeySchemaItem {
  name: string;
  key_type: string;
  description: string;
}

/**
 * Tool invocation configuration
 */
export interface ToolInvocation {
  type: string;
  function?: string;
}

/**
 * Tool permissions
 */
export interface ToolPermissions {
  file_read: string[];
  file_write: string[];
  network: boolean;
  env_vars: string[];
}

/**
 * Tool return schema
 */
export interface ToolReturnSchema {
  type: string;
  description: string;
  content_type?: string;
  schema: Record<string, unknown> | string;
  examples?: unknown[];
}

/**
 * Tool definition
 */
export interface ToolDefinition {
  id?: string;
  tool_id?: string;
  version?: number;
  name: string;
  display_name?: string;
  description: string;
  category?: string;
  subcategory?: string;
  parameters: ToolParameter[];
  returns?: ToolReturnSchema;
  invocation?: ToolInvocation;
  keys_schema?: KeySchemaItem[];
  permissions?: ToolPermissions;
  sources?: string[];
  dependencies?: string[];
  status?: ToolStatus;
  visibility?: ToolVisibility;
  created_at?: string;
  created_by?: string;
  code_file?: string;
}

/**
 * Tool parameter
 */
export interface ToolParameter {
  name: string;
  type: string;
  description: string;
  required: boolean;
  default?: string | number | boolean | object | unknown[] | null;
  enum?: unknown[];
  minimum?: number;
  maximum?: number;
  exclusiveMinimum?: number;
  exclusiveMaximum?: number;
  minLength?: number;
  maxLength?: number;
  minItems?: number;
  maxItems?: number;
  multipleOf?: number;
  pattern?: string;
  format?: string;
  properties?: Record<string, unknown>;
  required_properties?: string[];
  uniqueItems?: boolean;
  oneOf?: unknown[];
  anyOf?: unknown[];
  allOf?: unknown[];
}

/**
 * Change log
 */
export interface ChangeLog {
  type: ChangeType;
  summary?: string;
  details?: string[];
}

/**
 * Compatibility information
 */
export interface Compatibility {
  adl_spec?: string;
  previous_versions?: string[];
}

/**
 * LLM settings
 */
export interface LlmSettings {
  temperature: number;
  max_tokens: number;
}

/**
 * Agent definition
 */
export interface AgentDefinition {
  id: string;
  version: number;
  version_string?: string;
  lifecycle?: Lifecycle;
  compatibility?: Compatibility;
  change_log?: ChangeLog;
  name: string;
  description: string;
  role: string;
  llm: string;
  llm_settings: LlmSettings;
  tools: ToolDefinition[];
  rag: RagIndex[];
  memory?: MemoryDefinition;
  owner?: string;
  document_index_id?: string;
}
