# Memory Extensions

## Overview

ADL v2 introduces advanced memory capabilities with episodic and semantic memory types, lifecycle management, and intelligent eviction policies. This enables agents to maintain context and learn from interactions.

## Memory Types

### Episodic Memory

Stores specific episodes and experiences:

```json
{
  "episodic_memory": {
    "enabled": true,
    "backend": "vector",
    "max_episodes": 1000,
    "retention_policy": "importance_based",
    "compression": true
  }
}
```

**Use Cases**:
- Remembering specific user interactions
- Storing task execution history
- Maintaining conversation context
- Learning from past experiences

### Semantic Memory

Stores abstract concepts and knowledge:

```json
{
  "semantic_memory": {
    "enabled": true,
    "backend": "graph",
    "max_concepts": 5000,
    "retention_policy": "usage_based",
    "knowledge_graph": true
  }
}
```

**Use Cases**:
- Storing learned patterns
- Maintaining domain knowledge
- Building concept relationships
- Generalizing from experiences

### Working Memory

Short-term memory for current context:

```json
{
  "working_memory": {
    "enabled": true,
    "max_items": 50,
    "retention_policy": "session",
    "auto_clear": true
  }
}
```

**Use Cases**:
- Maintaining current task context
- Storing temporary data
- Managing conversation state
- Tracking intermediate results

## Memory Lifecycle

### Lifecycle Stages

#### 1. Creation

When memories are created:

```json
{
  "lifecycle": {
    "creation": {
      "auto_create": true,
      "creation_triggers": [
        "tool_invocation",
        "user_interaction",
        "error_occurrence"
      ],
      "metadata_required": ["timestamp", "source", "importance"]
    }
  }
}
```

#### 2. Storage

How memories are stored:

```json
{
  "lifecycle": {
    "storage": {
      "backend": "vector",
      "indexing": "automatic",
      "compression": "lossless",
      "encryption": true
    }
  }
}
```

#### 3. Retrieval

How memories are retrieved:

```json
{
  "lifecycle": {
    "retrieval": {
      "method": "semantic_search",
      "max_results": 10,
      "min_similarity": 0.7,
      "context_aware": true
    }
  }
}
```

#### 4. Update

How memories are updated:

```json
{
  "lifecycle": {
    "update": {
      "auto_update": true,
      "update_triggers": [
        "access",
        "related_event",
        "time_based"
      ],
      "merge_strategy": "weighted_average"
    }
  }
}
```

#### 5. Deletion

How memories are deleted:

```json
{
  "lifecycle": {
    "deletion": {
      "auto_delete": true,
      "deletion_triggers": [
        "expired",
        "low_importance",
        "manual"
      ],
      "soft_delete": true,
      "retention_period": "30d"
    }
  }
}
```

## Eviction Policies

### Eviction Strategies

#### 1. LRU (Least Recently Used)

Evict least recently accessed memories:

```json
{
  "eviction_policy": {
    "strategy": "lru",
    "check_interval_ms": 60000,
    "eviction_batch_size": 10,
    "min_memories": 100
  }
}
```

#### 2. LFU (Least Frequently Used)

Evict least frequently accessed memories:

```json
{
  "eviction_policy": {
    "strategy": "lfu",
    "check_interval_ms": 60000,
    "eviction_batch_size": 10,
    "min_memories": 100
  }
}
```

#### 3. Importance-Based

Evict least important memories:

```json
{
  "eviction_policy": {
    "strategy": "importance",
    "importance_metric": "composite",
    "factors": {
      "access_count": 0.4,
      "recency": 0.3,
      "relevance": 0.3
    },
    "check_interval_ms": 60000,
    "eviction_batch_size": 10,
    "min_memories": 100
  }
}
```

#### 4. TTL (Time To Live)

Evict memories based on age:

```json
{
  "eviction_policy": {
    "strategy": "ttl",
    "default_ttl_seconds": 86400,
    "per_type_ttl": {
      "episodic": 604800,
      "semantic": 2592000,
      "working": 3600
    },
    "check_interval_ms": 300000
  }
}
```

## Memory Privacy

### Privacy Controls

#### 1. PII Detection

Detect and protect PII:

```json
{
  "privacy": {
    "pii_detection": {
      "enabled": true,
      "auto_redact": true,
      "redaction_method": "mask",
      "pii_types": [
        "email",
        "phone",
        "ssn",
        "credit_card"
      ]
    }
  }
}
```

#### 2. Encryption

Encrypt sensitive memories:

```json
{
  "privacy": {
    "encryption": {
      "enabled": true,
      "algorithm": "aes-256",
      "key_rotation_days": 30,
      "at_rest": true,
      "in_transit": true
    }
  }
}
```

#### 3. Access Control

Control memory access:

```json
{
  "privacy": {
    "access_control": {
      "enabled": true,
      "default_permission": "read",
      "permissions": {
        "episodic": "read_write",
        "semantic": "read_write",
        "working": "read_write_delete"
      }
    }
  }
}
```

## Memory Consolidation

### Consolidation Strategies

#### 1. Temporal Consolidation

Consolidate memories over time:

```json
{
  "consolidation": {
    "enabled": true,
    "strategy": "temporal",
    "interval_hours": 24,
    "method": "clustering",
    "cluster_threshold": 0.8
  }
}
```

#### 2. Semantic Consolidation

Consolidate similar memories:

```json
{
  "consolidation": {
    "enabled": true,
    "strategy": "semantic",
    "similarity_threshold": 0.9,
    "method": "merge",
    "preserve_metadata": true
  }
}
```

#### 3. Hierarchical Consolidation

Consolidate into hierarchical structure:

```json
{
  "consolidation": {
    "enabled": true,
    "strategy": "hierarchical",
    "max_depth": 3,
    "min_cluster_size": 5
  }
}
```

## Memory Analytics

### Metrics Collection

Track memory performance:

```json
{
  "memory_analytics": {
    "enabled": true,
    "metrics": [
      "total_memories",
      "memory_usage_mb",
      "access_frequency",
      "hit_rate",
      "eviction_rate",
      "consolidation_rate"
    ],
    "sampling_rate": 0.1
  }
}
```

### Performance Monitoring

Monitor memory system health:

```json
{
  "performance_monitoring": {
    "enabled": true,
    "alert_thresholds": {
      "memory_usage_mb": 1024,
      "access_latency_ms": 100,
      "eviction_rate": 0.1
    },
    "alert_channels": ["slack", "email"]
  }
}
```

## Examples

### Simple Episodic Memory

```json
{
  "memory": {
    "type": "episodic",
    "scope": "session",
    "backend": "vector",
    "retention": {
      "policy": "ttl",
      "duration": "7d"
    },
    "write_policy": "implicit",
    "read_policy": "on_demand",
    "privacy": {
      "pii": false,
      "encryption": true
    }
  }
}
```

### Advanced Memory with Extensions

```json
{
  "memory": {
    "type": "hybrid",
    "episodic": {
      "enabled": true,
      "backend": "vector",
      "max_episodes": 1000,
      "retention_policy": "importance_based"
    },
    "semantic": {
      "enabled": true,
      "backend": "graph",
      "max_concepts": 5000,
      "retention_policy": "usage_based"
    },
    "working": {
      "enabled": true,
      "max_items": 50,
      "retention_policy": "session"
    },
    "lifecycle": {
      "creation": {
        "auto_create": true,
        "creation_triggers": ["tool_invocation", "user_interaction"]
      },
      "eviction": {
        "policy": "importance",
        "check_interval_ms": 60000
      }
    },
    "consolidation": {
      "enabled": true,
      "strategy": "semantic",
      "similarity_threshold": 0.9
    },
    "privacy": {
      "pii_detection": {
        "enabled": true,
        "auto_redact": true
      },
      "encryption": {
        "enabled": true,
        "algorithm": "aes-256"
      }
    }
  }
}
```

## Best Practices

1. **Use Appropriate Memory Types**: Choose episodic for events, semantic for knowledge
2. **Implement Eviction Policies**: Prevent memory bloat with smart eviction
3. **Enable Privacy Controls**: Protect sensitive information
4. **Monitor Performance**: Track metrics and set up alerts
5. **Consolidate Regularly**: Reduce memory footprint through consolidation

## Migration from v1.5

v1.5 agents without memory extensions default to:

```json
{
  "memory": {
    "type": "episodic",
    "scope": "session",
    "backend": "vector",
    "retention": {
      "policy": "ttl",
      "duration": "7d"
    },
    "write_policy": "implicit",
    "read_policy": "on_demand",
    "privacy": {
      "pii": false,
      "encryption": true
    }
  }
}
```

This ensures backward compatibility while enabling v2 features.
