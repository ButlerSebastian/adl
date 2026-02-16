# LLM Settings Extensions

## Overview

ADL v2 introduces advanced LLM settings with multi-model support, task-based routing, and execution constraints. This enables agents to use the best model for each task while managing costs and performance.

## Multi-Model Support

### Model Types

#### 1. Primary Model

Main model for general tasks:

```json
{
  "primary_model": {
    "provider": "openai",
    "model": "gpt-4",
    "api_key": "${OPENAI_API_KEY}",
    "endpoint": "https://api.openai.com/v1/chat/completions"
  }
}
```

#### 2. Fallback Models

Backup models when primary fails:

```json
{
  "fallback_models": [
    {
      "provider": "anthropic",
      "model": "claude-3-opus",
      "priority": 1,
      "trigger_conditions": ["timeout", "rate_limit", "error"]
    },
    {
      "provider": "openai",
      "model": "gpt-3.5-turbo",
      "priority": 2,
      "trigger_conditions": ["timeout", "rate_limit", "error"]
    }
  ]
}
```

#### 3. Specialized Models

Models for specific tasks:

```json
{
  "specialized_models": [
    {
      "name": "code_generation",
      "provider": "openai",
      "model": "gpt-4",
      "task_types": ["code_generation", "code_review", "debugging"],
      "cost_multiplier": 1.5
    },
    {
      "name": "summarization",
      "provider": "anthropic",
      "model": "claude-3-haiku",
      "task_types": ["summarization", "extraction"],
      "cost_multiplier": 0.5
    },
    {
      "name": "math",
      "provider": "openai",
      "model": "gpt-4",
      "task_types": ["math", "calculation", "analysis"],
      "cost_multiplier": 1.2
    }
  ]
}
```

## Model Routing

### Routing Strategies

#### 1. Task-Based Routing

Route based on task type:

```json
{
  "routing": {
    "strategy": "task_based",
    "default_model": "primary",
    "task_mappings": {
      "code_generation": "code_generation",
      "summarization": "summarization",
      "math": "math",
      "general": "primary"
    }
  }
}
```

#### 2. Cost-Based Routing

Route based on cost constraints:

```json
{
  "routing": {
    "strategy": "cost_based",
    "max_cost_per_task_usd": 0.5,
    "model_hierarchy": [
      "gpt-3.5-turbo",
      "claude-3-haiku",
      "gpt-4"
    ]
  }
}
```

#### 3. Performance-Based Routing

Route based on performance requirements:

```json
{
  "routing": {
    "strategy": "performance_based",
    "performance_requirements": {
      "latency_ms": 1000,
      "quality_score": 0.8
    },
    "model_hierarchy": [
      "gpt-4",
      "claude-3-opus",
      "gpt-3.5-turbo"
    ]
  }
}
```

#### 4. Adaptive Routing

Route based on dynamic conditions:

```json
{
  "routing": {
    "strategy": "adaptive",
    "factors": {
      "task_complexity": 0.4,
      "cost_budget": 0.3,
      "performance_requirement": 0.3
    },
    "learning_enabled": true,
    "feedback_interval_hours": 24
  }
}
```

## Model Constraints

### Execution Constraints

#### 1. Token Limits

Limit token usage:

```json
{
  "model_constraints": {
    "token_limits": {
      "max_input_tokens": 4000,
      "max_output_tokens": 2000,
      "max_total_tokens": 6000,
      "enforce_strict": true
    }
  }
}
```

#### 2. Cost Limits

Limit monetary costs:

```json
{
  "model_constraints": {
    "cost_limits": {
      "max_cost_per_task_usd": 1.0,
      "max_cost_per_hour_usd": 10.0,
      "max_cost_per_day_usd": 50.0,
      "alert_threshold_usd": 0.8
    }
  }
}
```

#### 3. Rate Limits

Limit API call rates:

```json
{
  "model_constraints": {
    "rate_limits": {
      "max_calls_per_minute": 60,
      "max_calls_per_hour": 1000,
      "max_concurrent_calls": 5,
      "backoff_strategy": "exponential"
    }
  }
}
```

#### 4. Timeout Limits

Limit execution time:

```json
{
  "model_constraints": {
    "timeout_limits": {
      "max_inference_time_ms": 30000,
      "max_total_time_ms": 60000,
      "timeout_action": "fallback"
    }
  }
}
```

## Model Configuration

### Temperature Settings

Control randomness:

```json
{
  "model_configuration": {
    "temperature": {
      "default": 0.7,
      "task_specific": {
        "creative": 0.9,
        "analytical": 0.3,
        "code_generation": 0.2,
        "summarization": 0.5
      }
    }
  }
}
```

### Top-P Settings

Control diversity:

```json
{
  "model_configuration": {
    "top_p": {
      "default": 0.9,
      "task_specific": {
        "creative": 0.95,
        "analytical": 0.8,
        "code_generation": 0.7
      }
    }
  }
}
```

### Frequency Penalty

Control repetition:

```json
{
  "model_configuration": {
    "frequency_penalty": {
      "default": 0.0,
      "task_specific": {
        "creative": 0.5,
        "analytical": 0.0,
        "code_generation": 0.3
      }
    }
  }
}
```

### Presence Penalty

Control topic introduction:

```json
{
  "model_configuration": {
    "presence_penalty": {
      "default": 0.0,
      "task_specific": {
        "creative": 0.3,
        "analytical": 0.0,
        "code_generation": 0.1
      }
    }
  }
}
```

## Model Monitoring

### Performance Metrics

Track model performance:

```json
{
  "model_monitoring": {
    "enabled": true,
    "metrics": [
      "response_time_ms",
      "tokens_per_second",
      "cost_per_task_usd",
      "success_rate",
      "fallback_rate"
    ],
    "sampling_rate": 0.1
  }
}
```

### Quality Metrics

Track output quality:

```json
{
  "quality_monitoring": {
    "enabled": true,
    "metrics": [
      "coherence_score",
      "relevance_score",
      "accuracy_score",
      "user_satisfaction"
    ],
    "feedback_collection": "automatic"
  }
}
```

### Alerting

Set up alerts for issues:

```json
{
    "alerting": {
      "enabled": true,
      "alerts": [
        {
          "metric": "success_rate",
          "threshold": 0.9,
          "operator": "less_than",
          "channels": ["slack", "email"]
        },
        {
          "metric": "response_time_ms",
          "threshold": 5000,
          "operator": "greater_than",
          "channels": ["slack"]
        }
      ]
    }
  }
}
```

## Examples

### Simple Multi-Model Setup

```json
{
  "llm_settings": {
    "primary_model": {
      "provider": "openai",
      "model": "gpt-4"
    },
    "fallback_models": [
      {
        "provider": "anthropic",
        "model": "claude-3-opus",
        "priority": 1
      }
    ],
    "routing": {
      "strategy": "task_based",
      "default_model": "primary"
    }
  }
}
```

### Advanced Multi-Model with Routing

```json
{
  "llm_settings": {
    "primary_model": {
      "provider": "openai",
      "model": "gpt-4",
      "temperature": 0.7,
      "max_tokens": 2000
    },
    "fallback_models": [
      {
        "provider": "anthropic",
        "model": "claude-3-opus",
        "priority": 1,
        "trigger_conditions": ["timeout", "rate_limit"]
      },
      {
        "provider": "openai",
        "model": "gpt-3.5-turbo",
        "priority": 2,
        "trigger_conditions": ["timeout", "rate_limit"]
      }
    ],
    "specialized_models": [
      {
        "name": "code_generation",
        "provider": "openai",
        "model": "gpt-4",
        "task_types": ["code_generation", "code_review"],
        "cost_multiplier": 1.5
      },
      {
        "name": "summarization",
        "provider": "anthropic",
        "model": "claude-3-haiku",
        "task_types": ["summarization", "extraction"],
        "cost_multiplier": 0.5
      }
    ],
    "routing": {
      "strategy": "adaptive",
      "factors": {
        "task_complexity": 0.4,
        "cost_budget": 0.3,
        "performance_requirement": 0.3
      },
      "learning_enabled": true
    },
    "model_constraints": {
      "token_limits": {
        "max_input_tokens": 4000,
        "max_output_tokens": 2000
      },
      "cost_limits": {
        "max_cost_per_task_usd": 2.0,
        "max_cost_per_hour_usd": 20.0
      },
      "rate_limits": {
        "max_calls_per_minute": 60,
        "max_calls_per_hour": 1000
      }
    },
    "model_monitoring": {
      "enabled": true,
      "metrics": ["response_time_ms", "cost_per_task_usd", "success_rate"]
    }
  }
}
```

## Best Practices

1. **Use Specialized Models**: Use specialized models for specific tasks
2. **Set Appropriate Limits**: Set realistic token, cost, and rate limits
3. **Monitor Performance**: Track metrics and set up alerts
4. **Use Fallback Models**: Ensure reliability with fallback models
5. **Optimize Routing**: Use adaptive routing for best performance

## Migration from v1.5

v1.5 agents without LLM extensions default to:

```json
{
  "llm_settings": {
    "primary_model": {
      "provider": "openai",
      "model": "gpt-4",
      "temperature": 0.7,
      "max_tokens": 2000
    },
    "routing": {
      "strategy": "direct",
      "default_model": "primary"
    },
    "model_constraints": {
      "token_limits": {
        "max_input_tokens": 4000,
        "max_output_tokens": 2000
      }
    }
  }
}
```

This ensures backward compatibility while enabling v2 features.
