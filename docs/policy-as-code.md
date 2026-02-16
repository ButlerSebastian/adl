# Policy-as-Code Integration

## Overview

ADL v3 introduces policy-as-code integration using Open Policy Agent (OPA) and Rego language. This enables declarative policy management for agent permissions, resource access, and security controls.

## Architecture

### Core Concepts

#### 1. Policy-as-Code

Policies are defined as code (Rego) rather than configuration:
- **Declarative**: Define what is allowed, not how to check
- **Version Controlled**: Policies in git, auditable and reviewable
- **Testable**: Unit tests for policy logic
- **Composable**: Reusable policy modules

#### 2. OPA Integration

OPA is deployed as a sidecar service:
- **REST API**: Query OPA via HTTP POST
- **Input Document**: Send context (user, resource, action) to OPA
- **Decision**: OPA returns allow/deny decision
- **Fast**: Local queries, low latency

#### 3. Rego Language

Rego is OPA's policy language:
- **Datalog-based**: Logic programming language
- **Declarative**: Define rules, not procedures
- **Composable**: Import and reuse policy modules
- **Type-safe**: Modern Rego v1 with type checking

## JSON Schema

### Policy Definition

```json
{
  "policy": {
    "id": "policy-id",
    "name": "My Policy",
    "version": "1.0.0",
    "description": "Policy description",
    "rego": "package authz\n\ndefault allow := false\n\nallow if {\n    input.user == \"alice\"\n    input.action == \"read\"\n}",
    "enforcement": {
      "mode": "strict",
      "action": "deny"
    },
    "data": {
      "roles": {
        "admin": ["alice"],
        "user": ["bob", "charlie"]
      },
      "resources": {
        "database": ["read", "write"],
        "api": ["read"]
      }
    },
    "metadata": {
      "author": "security-team",
      "tags": ["rbac", "access-control"]
    }
  }
}
```

### Policy Schema

```typescript
interface PolicyDefinition {
  id: string;
  name: string;
  version: string;
  description?: string;
  rego: string;
  enforcement: PolicyEnforcement;
  data?: Record<string, unknown>;
  metadata?: Record<string, unknown>;
}

interface PolicyEnforcement {
  mode: EnforcementMode;
  action: EnforcementAction;
  audit_log?: boolean;
}

type EnforcementMode = "strict" | "moderate" | "lenient";

type EnforcementAction = "deny" | "warn" | "log" | "allow";
```

## Rego Language Patterns

### 1. Default Deny Pattern

Always start with default deny for security:

```rego
package authz

default allow := false

allow if {
    input.user == "alice"
    input.action == "read"
}
```

### 2. Role-Based Access Control (RBAC)

```rego
package authz

default allow := false

allow if {
    has_role(input.user, "admin")
}

allow if {
    has_role(input.user, "user")
    input.action == "read"
}

has_role(user, role) {
    data.roles[user][role]
}
```

### 3. Resource-Based Access Control

```rego
package authz

default allow := false

allow if {
    input.resource == "database"
    input.action in data.resources["database"]
    has_permission(input.user, input.resource, input.action)
}

has_permission(user, resource, action) {
    data.permissions[user][resource][action]
}
```

### 4. Hierarchical Roles with Graph Traversal

```rego
package authz

default allow := false

allow if {
    some role in graph.reachable(data.role_hierarchy, {input.role})
    input.action in data.role_permissions[role]
}

# Role hierarchy
role_hierarchy := {
    "manager": {"supervisor", "security"},
    "supervisor": {"assistant"},
    "security": set(),
    "assistant": set(),
}

# Role permissions
role_permissions := {
    "manager": {"read", "write", "delete"},
    "supervisor": {"read", "write"},
    "security": {"read", "audit"},
    "assistant": {"read"},
}
```

### 5. Conditional Policies

```rego
package authz

default allow := false

allow if {
    input.action == "read"
    input.resource == "sensitive_data"
    input.user_clearance >= data.resource_clearance[input.resource]
}

allow if {
    input.action == "read"
    input.resource != "sensitive_data"
}
```

### 6. Time-Based Policies

```rego
package authz

default allow := false

allow if {
    input.action == "admin"
    is_business_hours()
}

is_business_hours() if {
    hour := time.clock(input.time).hour
    hour >= 9
    hour < 17
}
```

### 7. JWT Token Verification

```rego
package authz

default allow := false

allow if {
    verify_token(input.token)
    token.payload.user == input.user
    token.payload.exp > time.now_ns() / 1000000
}

token := {"payload": payload} if {
    [header, payload, signature] := io.jwt.decode(input.token)
}

verify_token(token) if {
    io.jwt.verify_hs256(token, data.jwt_secret)
}
```

### 8. Incremental Validation

```rego
package validation

validations contains message if {
    some field in {"title", "content"}
    object.get(input, field, "") == ""
    message := sprintf("Value missing for field '%s'", [field])
}

validations contains "Title must start with a capital" if {
    not regex.match(`^[A-Z]`, input.title)
}
```

## Python Integration

### 1. REST API Integration

```python
import requests
import json

class OPAClient:
    """OPA client for policy evaluation."""
    
    def __init__(self, opa_url="http://localhost:8181"):
        self.opa_url = opa_url
    
    def check_policy(self, package, rule, input_data):
        """Check policy against input data."""
        url = f"{self.opa_url}/v1/data/{package}/{rule}"
        
        response = requests.post(
            url,
            json={"input": input_data},
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code != 200:
            raise Exception(f"OPA query failed: {response.text}")
        
        return response.json()
    
    def allow(self, package, input_data):
        """Check if action is allowed."""
        result = self.check_policy(package, "allow", input_data)
        return result.get("result", False)
```

### 2. Flask Middleware

```python
from flask import Flask, request, abort

app = Flask(__name__)
opa = OPAClient()

@app.before_request
def check_authorization():
    """Check authorization before each request."""
    try:
        input_data = {
            "user": get_user(request),
            "method": request.method,
            "path": request.path.split("/")[1:],
            "action": get_action(request)
        }
        
        allowed = opa.allow("authz", input_data)
        
        if not allowed:
            abort(403)
    except Exception as e:
        app.logger.error(f"Authorization check failed: {e}")
        abort(500)

def get_user(request):
    """Extract user from request."""
    # Implement user extraction logic
    return request.headers.get("X-User", "anonymous")

def get_action(request):
    """Map HTTP method to action."""
    method_to_action = {
        "GET": "read",
        "POST": "write",
        "PUT": "write",
        "DELETE": "delete"
    }
    return method_to_action.get(request.method, "unknown")
```

### 3. Async Integration

```python
import aiohttp
import asyncio

class AsyncOPAClient:
    """Async OPA client."""
    
    def __init__(self, opa_url="http://localhost:8181"):
        self.opa_url = opa_url
    
    async def check_policy(self, package, rule, input_data):
        """Check policy asynchronously."""
        url = f"{self.opa_url}/v1/data/{package}/{rule}"
        
        async with aiohttp.ClientSession() as session:
            async with session.post(
                url,
                json={"input": input_data},
                headers={"Content-Type": "application/json"}
            ) as response:
                if response.status != 200:
                    text = await response.text()
                    raise Exception(f"OPA query failed: {text}")
                
                return await response.json()
    
    async def allow(self, package, input_data):
        """Check if action is allowed asynchronously."""
        result = await self.check_policy(package, "allow", input_data)
        return result.get("result", False)
```

## Policy Testing

### 1. Unit Tests with OPA Test Framework

**Policy file** (`authz.rego`):
```rego
package authz

default allow := false

allow if {
    input.user == "alice"
    input.action == "read"
}
```

**Test file** (`authz_test.rego`):
```rego
package authz_test

import data.authz

test_alice_can_read if {
    authz.allow with input as {"user": "alice", "action": "read"}
}

test_bob_cannot_read if {
    not authz.allow with input as {"user": "bob", "action": "read"}
}
```

**Run tests**:
```bash
opa test . -v
```

### 2. Data Mocking

```rego
package authz_test

import data.authz

# Mock data
roles := {"admin": ["alice"], "user": ["bob"]}

test_admin_can_write if {
    authz.allow with input as {"user": "alice", "action": "write"}
        with data.roles as roles
}
```

### 3. Coverage Reporting

```bash
opa test --coverage --format=json authz.rego authz_test.rego
```

## Best Practices

### 1. Policy Design

- **Default deny**: Always start with `default allow := false`
- **Keep policies simple**: One rule per concern
- **Use helper functions**: Reuse logic across rules
- **Document policies**: Add comments explaining intent
- **Test thoroughly**: Unit tests for all policy paths

### 2. Performance

- **Use bundles**: Pre-compile policies for faster loading
- **Cache decisions**: Cache OPA responses when possible
- **Minimize input**: Send only necessary data to OPA
- **Use local OPA**: Deploy OPA as sidecar for low latency
- **Monitor performance**: Track query times

### 3. Security

- **Validate input**: Sanitize data before sending to OPA
- **Secure OPA API**: Use authentication and TLS
- **Audit decisions**: Log all policy decisions
- **Version policies**: Track policy changes
- **Test policies**: Ensure policies work as intended

### 4. Maintainability

- **Use modules**: Organize policies into reusable modules
- **Follow naming conventions**: Consistent naming for rules and data
- **Document dependencies**: Explain what policies depend on
- **Version control**: Store policies in git
- **Code review**: Review policy changes like code

## Examples

### Example 1: Simple RBAC Policy

```rego
package authz

default allow := false

allow if {
    has_role(input.user, "admin")
}

allow if {
    has_role(input.user, "user")
    input.action == "read"
}

has_role(user, role) {
    data.roles[user][role]
}
```

### Example 2: Resource-Based Policy

```rego
package authz

default allow := false

allow if {
    input.resource == "database"
    input.action in data.resources["database"]
    has_permission(input.user, input.resource, input.action)
}

has_permission(user, resource, action) {
    data.permissions[user][resource][action]
}
```

### Example 3: Time-Based Policy

```rego
package authz

default allow := false

allow if {
    input.action == "admin"
    is_business_hours()
}

is_business_hours() if {
    hour := time.clock(input.time).hour
    hour >= 9
    hour < 17
}
```

### Example 4: JWT Token Policy

```rego
package authz

default allow := false

allow if {
    verify_token(input.token)
    token.payload.user == input.user
    token.payload.exp > time.now_ns() / 1000000
}

token := {"payload": payload} if {
    [header, payload, signature] := io.jwt.decode(input.token)
}

verify_token(token) if {
    io.jwt.verify_hs256(token, data.jwt_secret)
}
```

## Integration with ADL

Policies are integrated into ADL agent definitions via the `policy` field:

```json
{
  "name": "policy-protected-agent",
  "description": "Agent with policy-based access control",
  "role": "Secure Agent",
  "llm": "openai",
  "llm_settings": {
    "temperature": 0.7,
    "max_tokens": 2000
  },
  "policy": {
    "id": "rbac-policy",
    "name": "RBAC Policy",
    "version": "1.0.0",
    "rego": "package authz\n\ndefault allow := false\n\nallow if {\n    has_role(input.user, \"admin\")\n}\n\nhas_role(user, role) {\n    data.roles[user][role]\n}",
    "enforcement": {
      "mode": "strict",
      "action": "deny",
      "audit_log": true
    },
    "data": {
      "roles": {
        "admin": ["alice"],
        "user": ["bob", "charlie"]
      }
    }
  },
  "tools": [/* ... */],
  "rag": [],
  "memory": { /* ... */ }
}
```

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

- [OPA Official Documentation](https://openpolicyagent.org/docs)
- [Policy Language Guide](https://openpolicyagent.org/docs/policy-language)
- [Policy Reference](https://openpolicyagent.org/docs/policy-reference)
- [Integration Guide](https://openpolicyagent.org/docs/integration)
- [Policy Testing](https://openpolicyagent.org/docs/policy-testing)
- [Python Integration](https://www.openpolicyagent.org/docs/comparisons/languages/python)
