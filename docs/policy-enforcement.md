# Policy Enforcement Guide

## Overview

This guide explains how ADL v3 policies are enforced, including enforcement modes, actions, audit logging, and integration with agent execution.

## Enforcement Model

### 1. Enforcement Modes

#### Strict Mode

Deny access immediately when policy fails:

```python
def enforce_strict(policy, input_data):
    """Enforce policy in strict mode."""
    allowed = check_policy(policy, input_data)
    
    if not allowed:
        raise PolicyDeniedError(
            f"Access denied by policy '{policy['id']}'"
        )
    
    return True
```

**Use cases**: High-security environments, critical resources

#### Moderate Mode

Warn but allow access when policy fails:

```python
def enforce_moderate(policy, input_data):
    """Enforce policy in moderate mode."""
    allowed = check_policy(policy, input_data)
    
    if not allowed:
        logger.warning(
            f"Policy '{policy['id']}' would deny access, "
            f"but allowing in moderate mode"
        )
    
    return True
```

**Use cases**: Development environments, non-critical resources

#### Lenient Mode

Log policy violations but allow access:

```python
def enforce_lenient(policy, input_data):
    """Enforce policy in lenient mode."""
    allowed = check_policy(policy, input_data)
    
    if not allowed:
        logger.info(
            f"Policy '{policy['id']}' would deny access, "
            f"but allowing in lenient mode"
        )
    
    return True
```

**Use cases**: Testing, debugging, low-risk operations

### 2. Enforcement Actions

#### Deny Action

Block access and return error:

```python
def action_deny(policy, input_data):
    """Deny access and return error."""
    error = {
        "error": "Access denied",
        "policy_id": policy["id"],
        "policy_name": policy["name"],
        "reason": "Policy evaluation returned false"
    }
    
    raise PolicyDeniedError(error)
```

#### Warn Action

Log warning but continue:

```python
def action_warn(policy, input_data):
    """Log warning and continue."""
    warning = {
        "warning": "Policy violation",
        "policy_id": policy["id"],
        "policy_name": policy["name"],
        "input": input_data
    }
    
    logger.warning(json.dumps(warning))
```

#### Log Action

Log policy decision without blocking:

```python
def action_log(policy, input_data):
    """Log policy decision."""
    decision = {
        "policy_id": policy["id"],
        "policy_name": policy["name"],
        "allowed": check_policy(policy, input_data),
        "input": input_data,
        "timestamp": datetime.utcnow().isoformat()
    }
    
    logger.info(json.dumps(decision))
```

#### Allow Action

Allow access without additional checks:

```python
def action_allow(policy, input_data):
    """Allow access without blocking."""
    return True
```

## Policy Evaluation

### 1. OPA Query

Query OPA for policy decision:

```python
import requests

def check_policy(policy, input_data):
    """Check policy against input data."""
    opa_url = os.environ.get("OPA_URL", "http://localhost:8181")
    
    # Construct input document
    input_doc = {
        "input": input_data,
        "data": policy.get("data", {})
    }
    
    # Query OPA
    response = requests.post(
        f"{opa_url}/v1/data/{policy['package']}/allow",
        json=input_doc,
        headers={"Content-Type": "application/json"}
    )
    
    if response.status_code != 200:
        raise Exception(f"OPA query failed: {response.text}")
    
    result = response.json()
    return result.get("result", False)
```

### 2. Input Document Construction

Build input document from context:

```python
def build_input_document(user, action, resource, context):
    """Build input document for policy evaluation."""
    return {
        "user": user,
        "action": action,
        "resource": resource,
        "time": datetime.utcnow().isoformat(),
        "context": context
    }
```

### 3. Policy Package Resolution

Resolve policy package from Rego code:

```python
def get_policy_package(rego_code):
    """Extract package name from Rego code."""
    import re
    
    match = re.search(r'package\s+(\S+)', rego_code)
    if match:
        return match.group(1)
    
    return "authz"  # Default package
```

## Audit Logging

### 1. Audit Log Format

Structured audit log entries:

```python
def log_policy_decision(policy, input_data, allowed, enforcement_mode, action):
    """Log policy decision to audit log."""
    log_entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "event_type": "policy_decision",
        "policy_id": policy["id"],
        "policy_name": policy["name"],
        "policy_version": policy["version"],
        "enforcement_mode": enforcement_mode,
        "enforcement_action": action,
        "allowed": allowed,
        "input_data": input_data,
        "user": input_data.get("user"),
        "action": input_data.get("action"),
        "resource": input_data.get("resource")
    }
    
    logger.info(json.dumps(log_entry))
```

### 2. Audit Log Storage

Store audit logs for compliance:

```python
class AuditLogger:
    """Audit logger for policy decisions."""
    
    def __init__(self, storage_backend="database"):
        self.storage_backend = storage_backend
    
    def log(self, log_entry):
        """Store audit log entry."""
        if self.storage_backend == "database":
            self._log_to_database(log_entry)
        elif self.storage_backend == "file":
            self._log_to_file(log_entry)
        elif self.storage_backend == "elasticsearch":
            self._log_to_elasticsearch(log_entry)
    
    def _log_to_database(self, log_entry):
        """Store log in database."""
        # Implementation depends on database
        pass
    
    def _log_to_file(self, log_entry):
        """Store log in file."""
        with open("audit.log", "a") as f:
            f.write(json.dumps(log_entry) + "\n")
    
    def _log_to_elasticsearch(self, log_entry):
        """Store log in Elasticsearch."""
        # Implementation depends on Elasticsearch
        pass
```

### 3. Audit Log Query

Query audit logs for compliance:

```python
def query_audit_logs(filters, start_time, end_time):
    """Query audit logs for compliance reporting."""
    # Implementation depends on storage backend
    pass
```

## Integration with Agent Execution

### 1. Tool Invocation Policy Check

Check policy before tool invocation:

```python
def invoke_tool_with_policy(agent, tool_name, parameters):
    """Invoke tool with policy check."""
    # Build input document
    input_data = {
        "user": agent.user,
        "action": "invoke_tool",
        "resource": tool_name,
        "parameters": parameters
    }
    
    # Check policy
    policy = agent.policy
    allowed = check_policy(policy, input_data)
    
    # Enforce based on mode
    enforcement = policy["enforcement"]
    mode = enforcement["mode"]
    action = enforcement["action"]
    
    if mode == "strict":
        if not allowed:
            action_deny(policy, input_data)
    elif mode == "moderate":
        if not allowed:
            action_warn(policy, input_data)
    elif mode == "lenient":
        action_log(policy, input_data)
    
    # Invoke tool
    return tool.invoke(parameters)
```

### 2. Resource Access Policy Check

Check policy before resource access:

```python
def access_resource_with_policy(agent, resource, action):
    """Access resource with policy check."""
    input_data = {
        "user": agent.user,
        "action": action,
        "resource": resource
    }
    
    # Check policy
    policy = agent.policy
    allowed = check_policy(policy, input_data)
    
    # Enforce
    enforcement = policy["enforcement"]
    mode = enforcement["mode"]
    action = enforcement["action"]
    
    if mode == "strict":
        if not allowed:
            action_deny(policy, input_data)
    elif mode == "moderate":
        if not allowed:
            action_warn(policy, input_data)
    elif mode == "lenient":
        action_log(policy, input_data)
    
    # Access resource
    return resource.access(action)
```

### 3. Agent-to-Agent Communication Policy Check

Check policy for agent communication:

```python`
def communicate_with_policy(agent, target_agent, message):
    """Communicate with another agent with policy check."""
    input_data = {
        "user": agent.user,
        "action": "send_message",
        "resource": f"agent:{target_agent}",
        "message": message
    }
    
    # Check policy
    policy = agent.policy
    allowed = check_policy(policy, input_data)
    
    # Enforce
    enforcement = policy["enforcement"]
    mode = enforcement["mode"]
    action = enforcement["action"]
    
    if mode == "strict":
        if not allowed:
            action_deny(policy, input_data)
    elif mode == "moderate":
        if not allowed:
            action_warn(policy, input_data)
    elif mode == "lenient":
        action_log(policy, input_data)
    
    # Send message
    return target_agent.receive(message)
```

## Best Practices

### 1. Policy Design

- **Default deny**: Always use `default allow := false` for security
- **Keep policies simple**: One rule per concern
- **Test thoroughly**: Unit tests for all policy paths
- **Document policies**: Add comments explaining intent
- **Version control**: Store policies in git

### 2. Enforcement Configuration

- **Use strict mode** for production environments
- **Use moderate mode** for development environments
- **Use lenient mode** for testing and debugging
- **Enable audit logging** for compliance
- **Monitor policy decisions** for security incidents

### 3. Performance

- **Cache policy decisions**: Cache OPA responses when possible
- **Use local OPA**: Deploy OPA as sidecar for low latency
- **Minimize input data**: Send only necessary data to OPA
- **Batch policy checks**: Check multiple policies in one query
- **Monitor query times**: Track and optimize slow policies

### 4. Security

- **Validate input**: Sanitize data before sending to OPA
- **Secure OPA API**: Use authentication and TLS
- **Audit all decisions**: Log all policy decisions
- **Version policies**: Track policy changes
- **Test policies**: Ensure policies work as intended

### 5. Compliance

- **Retain audit logs**: Keep logs for required retention period
- **Regular audits**: Review policy decisions for compliance
- **Policy reviews**: Review and update policies regularly
- **Incident response**: Have process for policy violations
- **Documentation**: Document policy rationale and changes

## Examples

### Example 1: Enforce Policy Before Tool Invocation

```python
from tools.dsl.policy_validator import validate_policy

# Load agent
with open('examples/policy_rbac_v3.json', 'r') as f:
    agent = json.load(f)

policy = agent['policy']

# Validate policy
errors = validate_policy(policy)
if errors:
    print(f"Policy validation failed: {errors}")
    exit(1)

# Invoke tool with policy check
tool_name = "read_data"
parameters = {"resource": "database"}

try:
    result = invoke_tool_with_policy(agent, tool_name, parameters)
    print(f"Tool invocation succeeded: {result}")
except PolicyDeniedError as e:
    print(f"Tool invocation denied: {e}")
```

### Example 2: Query Audit Logs

```python
from datetime import datetime, timedelta

# Query audit logs for last 24 hours
end_time = datetime.utcnow()
start_time = end_time - timedelta(hours=24)

filters = {
    "policy_id": "rbac-policy",
    "user": "alice"
}

logs = query_audit_logs(filters, start_time, end_time)

for log in logs:
    print(f"{log['timestamp']}: {log['user']} {log['action']} {log['allowed']}")
```

### Example 3: Test Policy with OPA

```bash
# Load policy into OPA
opa eval -f examples/policy_rbac_v3.json "data.policy.rego"

# Test policy
opa eval -i examples/policy_rbac_v3.json "data.authz.allow" \
  --input '{"user": "alice", "action": "read", "resource": "database"}'

# Expected output: true
```

## Troubleshooting

### Common Issues

**Issue**: Policy evaluation fails
- **Solution**: Check OPA is running, verify Rego syntax, check input document format

**Issue**: Policy always denies access
- **Solution**: Check policy logic, verify data structure, test with OPA CLI

**Issue**: Audit logs not being written
- **Solution**: Check audit_log configuration, verify storage backend, check permissions

**Issue**: Performance is slow
- **Solution**: Cache policy decisions, use local OPA, optimize Rego code

**Issue**: Policy not being enforced
- **Solution**: Check enforcement mode, verify policy is loaded, check integration code

## Migration from v2

v2 agents without policies default to permissive access:

```json
{
  "policy": {
    "id": "default",
    "name": "Default Policy",
    "version": "1.0.0",
    "rego": "package authz\n\ndefault allow := true",
    "enforcement": {
      "mode": "lenient",
      "action": "allow"
    }
  }
}
```

This ensures backward compatibility while enabling v3 policy features.

## References

- [Policy-as-Code Architecture](policy-as-code.md)
- [Policy Validator](../tools/dsl/policy_validator.py)
- [Policy Examples](../examples/policy_rbac_v3.json)
- [OPA Documentation](https://openpolicyagent.org/docs)
