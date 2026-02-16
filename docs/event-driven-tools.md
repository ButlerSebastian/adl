# Event-Driven Tool Invocation

## Overview

ADL v2 introduces an event-driven architecture for tool invocation, enabling agents to respond to events, trigger actions based on conditions, and subscribe to event streams. This enables reactive, event-based agent behavior.

## Event System

### Event Types

#### 1. Tool Events

Events triggered by tool invocations:

```json
{
  "event_type": "tool_invocation",
  "source": "tool_name",
  "data": {
    "tool_name": "search_web",
    "parameters": {...},
    "result": {...},
    "status": "success"
  }
}
```

#### 2. State Events

Events triggered by state changes:

```json
{
  "event_type": "state_change",
  "source": "agent",
  "data": {
    "previous_state": "idle",
    "new_state": "processing",
    "timestamp": "2026-02-16T10:00:00Z"
  }
}
```

#### 3. Error Events

Events triggered by errors:

```json
{
  "event_type": "error",
  "source": "tool_name",
  "data": {
    "error_type": "timeout",
    "error_message": "Tool invocation timed out",
    "error_code": "TIMEOUT_001"
  }
}
```

#### 4. Custom Events

User-defined events:

```json
{
  "event_type": "custom",
  "source": "user_defined",
  "data": {
    "custom_field": "custom_value"
  }
}
```

## Triggers

### Trigger Types

#### 1. Event Triggers

Trigger on specific events:

```json
{
  "trigger_type": "event",
  "event_name": "tool_invocation",
  "condition": {
    "field": "tool_name",
    "operator": "equals",
    "value": "search_web"
  }
}
```

#### 2. Time Triggers

Trigger at specific times:

```json
{
  "trigger_type": "time",
  "schedule": "cron",
  "expression": "0 * * * *"
}
```

#### 3. Condition Triggers

Trigger when conditions are met:

```json
{
  "trigger_type": "condition",
  "condition": {
    "field": "memory_usage",
    "operator": "greater_than",
    "value": 0.9
  }
}
```

#### 4. Composite Triggers

Combine multiple triggers:

```json
{
  "trigger_type": "composite",
  "operator": "and",
  "triggers": [
    {
      "trigger_type": "event",
      "event_name": "tool_invocation"
    },
    {
      "trigger_type": "condition",
      "condition": {
        "field": "success",
        "operator": "equals",
        "value": true
      }
    }
  ]
}
```

## Event Handlers

### Handler Types

#### 1. Tool Invocation Handlers

Invoke tools on events:

```json
{
  "handler_type": "tool_invocation",
  "tool_name": "log_result",
  "parameters": {
    "event_data": "${event.data}"
  }
}
```

#### 2. State Update Handlers

Update agent state:

```json
{
  "handler_type": "state_update",
  "state_field": "last_tool_invocation",
  "value": "${event.timestamp}"
}
```

#### 3. Notification Handlers

Send notifications:

```json
{
  "handler_type": "notification",
  "notification_type": "alert",
  "message": "Tool invocation failed: ${event.data.error_message}"
}
```

#### 4. Custom Handlers

User-defined handlers:

```json
{
  "handler_type": "custom",
  "handler_name": "custom_handler",
  "parameters": {
    "event_data": "${event.data}"
  }
}
```

## Event Subscriptions

### Subscription Models

#### 1. Direct Subscription

Subscribe to specific events:

```json
{
  "subscription_type": "direct",
  "event_name": "tool_invocation",
  "handler": {
    "handler_type": "tool_invocation",
    "tool_name": "log_result"
  }
}
```

#### 2. Pattern Subscription

Subscribe to event patterns:

```json
{
  "subscription_type": "pattern",
  "event_pattern": "tool_*",
  "handler": {
    "handler_type": "notification",
    "notification_type": "alert"
  }
}
```

#### 3. Filtered Subscription

Subscribe with filters:

```json
{
  "subscription_type": "filtered",
  "event_name": "tool_invocation",
  "filter": {
    "field": "status",
    "operator": "equals",
    "value": "error"
  },
  "handler": {
    "handler_type": "notification",
    "notification_type": "alert"
  }
}
```

## Event Routing

### Routing Strategies

#### 1. Direct Routing

Route to specific handler:

```json
{
  "routing_strategy": "direct",
  "target_handler": "handler_name"
}
```

#### 2. Broadcast Routing

Route to all handlers:

```json
{
  "routing_strategy": "broadcast",
  "target_handlers": ["handler_1", "handler_2", "handler_3"]
}
```

#### 3. Conditional Routing

Route based on conditions:

```json
{
  "routing_strategy": "conditional",
  "routes": [
    {
      "condition": {
        "field": "priority",
        "operator": "equals",
        "value": "high"
      },
      "target_handler": "urgent_handler"
    },
    {
      "condition": {
        "field": "priority",
        "operator": "equals",
        "value": "low"
      },
      "target_handler": "normal_handler"
    }
  ]
}
```

## Event Processing

### Processing Modes

#### 1. Synchronous Processing

Process events synchronously:

```json
{
  "processing_mode": "synchronous",
  "timeout_ms": 5000
}
```

#### 2. Asynchronous Processing

Process events asynchronously:

```json
{
  "processing_mode": "asynchronous",
  "queue_size": 100,
  "worker_count": 5
}
```

#### 3. Batch Processing

Process events in batches:

```json
{
  "processing_mode": "batch",
  "batch_size": 10,
  "batch_timeout_ms": 1000
}
```

## Event Persistence

### Persistence Options

#### 1. In-Memory

Store events in memory:

```json
{
  "persistence": {
    "type": "memory",
    "max_events": 1000
  }
}
```

#### 2. File-Based

Store events in files:

```json
{
  "persistence": {
    "type": "file",
    "file_path": "/var/log/adl/events.json",
    "rotation": "daily"
  }
}
```

#### 3. Database

Store events in database:

```json
{
  "persistence": {
    "type": "database",
    "connection_string": "postgresql://user:pass@localhost/adl",
    "table_name": "events"
  }
}
```

## Examples

### Simple Event Handler

```json
{
  "events": {
    "subscriptions": [
      {
        "subscription_type": "direct",
        "event_name": "tool_invocation",
        "filter": {
          "field": "status",
          "operator": "equals",
          "value": "error"
        },
        "handler": {
          "handler_type": "notification",
          "notification_type": "alert",
          "message": "Tool invocation failed: ${event.data.error_message}"
        }
      }
    ]
  }
}
```

### Complex Event Flow

```json
{
  "events": {
    "triggers": [
      {
        "trigger_type": "event",
        "event_name": "tool_invocation",
        "condition": {
          "field": "tool_name",
          "operator": "equals",
          "value": "search_web"
        }
      }
    ],
    "handlers": [
      {
        "handler_type": "tool_invocation",
        "tool_name": "log_search",
        "parameters": {
          "query": "${event.data.parameters.query}"
        }
      },
      {
        "handler_type": "state_update",
        "state_field": "last_search_time",
        "value": "${event.timestamp}"
      }
    ],
    "routing_strategy": "broadcast",
    "processing_mode": "asynchronous",
    "persistence": {
      "type": "file",
      "file_path": "/var/log/adl/events.json"
    }
  }
}
```

## Best Practices

1. **Use Specific Events**: Subscribe to specific events rather than patterns when possible
2. **Handle Errors Gracefully**: Always include error event handlers
3. **Use Filters**: Filter events to reduce handler load
4. **Set Timeouts**: Set appropriate timeouts for synchronous processing
5. **Monitor Performance**: Monitor event processing performance

## Migration from v1.5

v1.5 agents without `events` field default to:

```json
{
  "events": {
    "subscriptions": [],
    "triggers": [],
    "handlers": [],
    "routing_strategy": "direct",
    "processing_mode": "synchronous",
    "persistence": {
      "type": "memory",
      "max_events": 100
    }
  }
}
```

This ensures backward compatibility while enabling v2 features.
