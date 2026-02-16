# Advanced RAG (Retrieval-Augmented Generation)

## Overview

ADL v2 introduces advanced RAG capabilities with hierarchical indexing, hybrid search (vector + keyword), cross-file references, and advanced filtering. This enables more sophisticated knowledge retrieval for agents.

## Hierarchical RAG

### Index Hierarchy

Organize RAG indices in a hierarchical structure:

```json
{
  "rag_hierarchy": {
    "root_index": "knowledge_base",
    "sub_indices": [
      {
        "name": "technical_docs",
        "parent": "knowledge_base",
        "type": "vector"
      },
      {
        "name": "user_guides",
        "parent": "knowledge_base",
        "type": "keyword"
      },
      {
        "name": "api_docs",
        "parent": "technical_docs",
        "type": "vector"
      }
    ]
  }
}
```

### Index Relationships

Define relationships between indices:

```json
{
  "index_relationships": [
    {
      "source": "api_docs",
      "target": "user_guides",
      "relationship": "references",
      "weight": 0.7
    },
    {
      "source": "technical_docs",
      "target": "api_docs",
      "relationship": "contains",
      "weight": 1.0
    }
  ]
}
```

## Hybrid Search

### Vector Search

Semantic search using embeddings:

```json
{
  "vector_search": {
    "enabled": true,
    "embedding_model": "text-embedding-ada-002",
    "similarity_metric": "cosine",
    "top_k": 10,
    "min_score": 0.7
  }
}
```

### Keyword Search

Exact match search using BM25:

```json
{
  "keyword_search": {
    "enabled": true,
    "algorithm": "bm25",
    "top_k": 20,
    "min_score": 0.5
  }
}
```

### Hybrid Fusion

Combine vector and keyword results:

```json
{
  "hybrid_search": {
    "enabled": true,
    "fusion_method": "rrf",
    "vector_weight": 0.7,
    "keyword_weight": 0.3,
    "top_k": 15
  }
}
```

**Fusion Methods**:
- `rrf`: Reciprocal Rank Fusion
- `weighted`: Weighted average
- `concat`: Concatenate results

## Cross-File References

### Reference Types

#### 1. Internal References

References within the same index:

```json
{
  "internal_references": {
    "enabled": true,
    "auto_link": true,
    "max_depth": 3
  }
}
```

#### 2. External References

References to other indices:

```json
{
  "external_references": {
    "enabled": true,
    "allowed_indices": ["technical_docs", "user_guides"],
    "max_references": 5
  }
}
```

#### 3. Web References

References to external web resources:

```json
{
  "web_references": {
    "enabled": true,
    "allowed_domains": ["docs.example.com", "api.example.com"],
    "follow_redirects": true,
    "timeout_ms": 5000
  }
}
```

## Advanced Filtering

### Metadata Filters

Filter by document metadata:

```json
{
  "metadata_filters": {
    "enabled": true,
    "filters": [
      {
        "field": "category",
        "operator": "equals",
        "value": "technical"
      },
      {
        "field": "created_at",
        "operator": "greater_than",
        "value": "2024-01-01"
      }
    ]
  }
}
```

### Content Filters

Filter by content patterns:

```json
{
  "content_filters": {
    "enabled": true,
    "filters": [
      {
        "type": "regex",
        "pattern": "\\bAPI\\b",
        "case_sensitive": false
      },
      {
        "type": "contains",
        "pattern": "authentication"
      }
    ]
  }
}
```

### Temporal Filters

Filter by time-based criteria:

```json
{
  "temporal_filters": {
    "enabled": true,
    "filters": [
      {
        "field": "created_at",
        "operator": "within_last",
        "value": "30d"
      },
      {
        "field": "updated_at",
        "operator": "between",
        "value": ["2024-01-01", "2024-12-31"]
      }
    ]
  }
}
```

## RAG Pipelines

### Pipeline Stages

Define multi-stage retrieval pipelines:

```json
{
  "rag_pipeline": {
    "stages": [
      {
        "name": "initial_search",
        "type": "hybrid",
        "config": {
          "top_k": 20
        }
      },
      {
        "name": "rerank",
        "type": "rerank",
        "config": {
          "model": "cross-encoder",
          "top_k": 10
        }
      },
      {
        "name": "deduplicate",
        "type": "deduplicate",
        "config": {
          "method": "similarity"
        }
      }
    ]
  }
}
```

### Pipeline Configuration

Configure pipeline behavior:

```json
{
  "pipeline_config": {
    "parallel_stages": true,
    "timeout_ms": 10000,
    "fallback_on_error": true,
    "cache_results": true,
    "cache_ttl_seconds": 3600
  }
}
```

## RAG Caching

### Cache Types

#### 1. Query Cache

Cache query results:

```json
{
  "query_cache": {
    "enabled": true,
    "max_size": 1000,
    "ttl_seconds": 3600,
    "eviction_policy": "lru"
  }
}
```

#### 2. Document Cache

Cache retrieved documents:

```json
{
  "document_cache": {
    "enabled": true,
    "max_size_mb": 100,
    "ttl_seconds": 86400,
    "compression": true
  }
}
```

#### 3. Embedding Cache

Cache computed embeddings:

```json
{
  "embedding_cache": {
    "enabled": true,
    "max_size": 10000,
    "ttl_seconds": 604800,
    "storage": "redis"
  }
}
```

## RAG Analytics

### Metrics Collection

Track RAG performance:

```json
{
  "rag_analytics": {
    "enabled": true,
    "metrics": [
      "query_latency_ms",
      "retrieval_count",
      "hit_rate",
      "avg_similarity_score",
      "cache_hit_rate"
    ],
    "sampling_rate": 0.1
  }
}
```

### Performance Monitoring

Monitor RAG system health:

```json
{
  "performance_monitoring": {
    "enabled": true,
    "alert_thresholds": {
      "query_latency_ms": 5000,
      "hit_rate": 0.5,
      "cache_hit_rate": 0.3
    },
    "alert_channels": ["slack", "email"]
  }
}
```

## Examples

### Simple Hybrid Search

```json
{
  "rag": [
    {
      "index_id": "knowledge_base",
      "type": "hybrid",
      "config": {
        "vector_search": {
          "enabled": true,
          "top_k": 10
        },
        "keyword_search": {
          "enabled": true,
          "top_k": 20
        },
        "hybrid_search": {
          "enabled": true,
          "fusion_method": "rrf",
          "vector_weight": 0.7,
          "keyword_weight": 0.3
        }
      }
    }
  ]
}
```

### Advanced Hierarchical RAG

```json
{
  "rag": [
    {
      "index_id": "knowledge_base",
      "type": "hierarchical",
      "config": {
        "root_index": "knowledge_base",
        "sub_indices": [
          {
            "name": "technical_docs",
            "type": "vector"
          },
          {
            "name": "user_guides",
            "type": "keyword"
          }
        ],
        "cross_references": {
          "enabled": true,
          "max_depth": 2
        },
        "hybrid_search": {
          "enabled": true,
          "fusion_method": "weighted"
        }
      }
    }
  ]
}
```

### RAG with Pipeline

```json
{
  "rag": [
    {
      "index_id": "knowledge_base",
      "type": "pipeline",
      "config": {
        "pipeline": {
          "stages": [
            {
              "name": "initial_search",
              "type": "hybrid",
              "top_k": 20
            },
            {
              "name": "rerank",
              "type": "rerank",
              "top_k": 10
            }
          ]
        },
        "caching": {
          "query_cache": {
            "enabled": true,
            "ttl_seconds": 3600
          }
        }
      }
    }
  ]
}
```

## Best Practices

1. **Use Hybrid Search**: Combine vector and keyword for better results
2. **Implement Caching**: Cache queries and documents to improve performance
3. **Monitor Performance**: Track metrics and set up alerts
4. **Use Hierarchical Indices**: Organize knowledge logically
5. **Filter Early**: Apply filters early in the pipeline to reduce load

## Migration from v1.5

v1.5 agents without advanced RAG features default to:

```json
{
  "rag": [
    {
      "index_id": "default",
      "type": "vector",
      "config": {
        "vector_search": {
          "enabled": true,
          "top_k": 10
        }
      }
    }
  ]
}
```

This ensures backward compatibility while enabling v2 features.
