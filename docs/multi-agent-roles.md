# Multi-Agent Role System

## Overview

ADL v2 introduces a multi-agent coordination system with defined role types, capabilities, and communication protocols. This enables agents to work together in structured, predictable ways.

## Role Types

ADL defines 4 core role types:

### 1. Coordinator

**Purpose**: Orchestrates and coordinates multiple agents.

**Capabilities**:
- Agent lifecycle management (start, stop, restart)
- Task delegation and assignment
- Resource allocation and scheduling
- Agent communication routing
- Conflict resolution

**Constraints**:
- Maximum 1 coordinator per agent group
- Cannot execute domain-specific tasks
- Must have visibility into all agent states

**Use Cases**:
- Multi-agent workflow orchestration
- Complex task decomposition
- Resource management
- Agent team coordination

### 2. Worker

**Purpose**: Executes domain-specific tasks.

**Capabilities**:
- Tool invocation
- Data processing
- Domain-specific reasoning
- Result generation

**Constraints**:
- Cannot coordinate other agents
- Limited to assigned tasks
- Must report status to coordinator
- Cannot modify agent group configuration

**Use Cases**:
- Data processing
- API interactions
- Document analysis
- Code generation

### 3. Supervisor

**Purpose**: Monitors and validates agent outputs.

**Capabilities**:
- Output validation
- Quality assurance
- Error detection
- Performance monitoring
- Compliance checking

**Constraints**:
- Cannot modify agent behavior
- Cannot execute tasks
- Must provide feedback to coordinator
- Cannot override coordinator decisions

**Use Cases**:
- Quality control
- Compliance verification
- Error detection
- Performance monitoring

### 4. Critic

**Purpose**: Provides critical feedback and improvement suggestions.

**Capabilities**:
- Output critique
- Suggestion generation
- Alternative approaches
- Risk assessment
- Optimization recommendations

**Constraints**:
- Cannot block execution
- Must provide constructive feedback
- Cannot modify agent behavior
- Limited to advisory role

**Use Cases**:
- Code review
- Strategy optimization
- Risk assessment
- Process improvement

## Role System Structure

### Agent Roles Field

```json
{
  "agent_roles": {
    "primary_role": "coordinator",
    "secondary_roles": ["supervisor"],
    "capabilities": [...],
    "constraints": {...},
    "communication_protocols": {...}
  }
}
```

### Role Capabilities

Each role defines specific capabilities:

```json
{
  "capabilities": [
    {
      "name": "agent_lifecycle_management",
      "type": "management",
      "scope": ["start", "stop", "restart"],
      "targets": ["worker", "supervisor", "critic"]
    },
    {
      "name": "task_delegation",
      "type": "coordination",
      "scope": ["assign", "reassign", "cancel"],
      "targets": ["worker"]
    }
  ]
}
```

### Role Constraints

Each role has specific constraints:

```json
{
  "constraints": {
    "max_coordinators": 1,
    "can_execute_tasks": false,
    "can_modify_configuration": false,
    "must_report_to": ["coordinator"],
    "communication_channels": ["direct", "broadcast"]
  }
}
```

### Communication Protocols

Agents communicate through defined protocols:

```json
{
  "communication_protocols": {
    "message_format": "json",
    "channels": ["direct", "broadcast", "pubsub"],
    "latency_requirements": {
      "max_latency_ms": 100,
      "priority": "high"
    },
    "reliability": {
      "ack_required": true,
      "retry_policy": "exponential_backoff"
    }
  }
}
```

## Role Hierarchy

```
Coordinator (Level 1)
├── Worker (Level 2)
├── Supervisor (Level 2)
└── Critic (Level 2)
```

- **Level 1**: Coordinator (highest authority)
- **Level 2**: Worker, Supervisor, Critic (equal authority, different responsibilities)

## Role Assignment Rules

1. **Primary Role**: Each agent must have exactly one primary role
2. **Secondary Roles**: Agents can have 0-2 secondary roles
3. **Role Compatibility**: Some roles cannot be combined:
   - Coordinator + Worker (conflict of interest)
   - Supervisor + Critic (redundant)
4. **Group Composition**: Each agent group must have exactly 1 coordinator

## Communication Patterns

### Direct Communication

Agent-to-agent direct messaging:

```json
{
  "type": "direct_message",
  "from": "agent_1",
  "to": "agent_2",
  "message": {...},
  "timestamp": "2026-02-16T10:00:00Z"
}
```

### Broadcast Communication

One-to-many messaging:

```json
{
  "type": "broadcast",
  "from": "coordinator",
  "to": ["worker_1", "worker_2", "supervisor"],
  "message": {...},
  "timestamp": "2026-02-16T10:00:00Z"
}
```

### PubSub Communication

Publish-subscribe pattern:

```json
{
  "type": "publish",
  "topic": "task_updates",
  "message": {...},
  "timestamp": "2026-02-16T10:00:00Z"
}
```

## Role Validation

### Validation Rules

1. **Primary Role Required**: Every agent must have a primary role
2. **Role Existence**: All roles must be one of the 4 defined types
3. **Role Compatibility**: Secondary roles must be compatible with primary role
4. **Group Constraints**: Agent group must have exactly 1 coordinator
5. **Capability Matching**: Capabilities must match role type

### Validation Example

```python
def validate_agent_roles(agent_roles):
    errors = []

    # Check primary role
    if not agent_roles.get("primary_role"):
        errors.append("Primary role is required")

    # Check role type
    valid_roles = ["coordinator", "worker", "supervisor", "critic"]
    if agent_roles["primary_role"] not in valid_roles:
        errors.append(f"Invalid primary role: {agent_roles['primary_role']}")

    # Check role compatibility
    primary = agent_roles["primary_role"]
    secondary = agent_roles.get("secondary_roles", [])
    if primary == "coordinator" and "worker" in secondary:
        errors.append("Coordinator cannot have Worker as secondary role")

    return errors
```

## Examples

### Simple Multi-Agent Setup

```json
{
  "name": "multi_agent_team",
  "agent_roles": {
    "primary_role": "coordinator",
    "capabilities": [
      {
        "name": "agent_lifecycle_management",
        "type": "management"
      }
    ],
    "constraints": {
      "max_coordinators": 1,
      "can_execute_tasks": false
    }
  }
}
```

### Worker Agent

```json
{
  "name": "data_processor",
  "agent_roles": {
    "primary_role": "worker",
    "capabilities": [
      {
        "name": "tool_invocation",
        "type": "execution"
      }
    ],
    "constraints": {
      "can_execute_tasks": true,
      "must_report_to": ["coordinator"]
    }
  }
}
```

## Best Practices

1. **Single Responsibility**: Each agent should have a clear, focused role
2. **Clear Communication**: Use defined communication protocols
3. **Proper Delegation**: Coordinators should delegate, not execute
4. **Validation**: Always validate role assignments
5. **Documentation**: Document role responsibilities and capabilities

## Migration from v1.5

v1.5 agents without `agent_roles` field default to:

```json
{
  "agent_roles": {
    "primary_role": "worker",
    "secondary_roles": [],
    "capabilities": [],
    "constraints": {}
  }
}
```

This ensures backward compatibility while enabling v2 features.
