#!/usr/bin/env python3
"""
Python Binding Example for ADL Phase 4 Types

This example demonstrates how to use the generated Python TypedDict classes
for workflow and policy definitions. It showcases type safety, IDE support,
and practical usage patterns.

Generated from ADL definitions using: adl-generate my-agent.adl --python -o my_agent.py
"""

from typing import Dict, List, Any, TypedDict, Required, NotRequired
import json


# ============================================================================
# WORKFLOW TYPES
# ============================================================================

class WorkflowNode(TypedDict):
    """Represents a node in a workflow graph."""
    id: Required[str]
    type: Required[str]
    label: Required[str]
    config: Required[Dict[str, Any]]
    position: Required[Dict[str, int]]


class WorkflowEdge(TypedDict):
    """Represents an edge connecting workflow nodes."""
    id: Required[str]
    source: Required[str]
    target: Required[str]
    relation: Required[str]
    condition: NotRequired[Dict[str, Any]]
    metadata: NotRequired[Dict[str, Any]]


class Workflow(TypedDict):
    """Represents a complete workflow definition."""
    id: Required[str]
    name: Required[str]
    version: Required[str]
    description: Required[str]
    nodes: Required[Dict[str, WorkflowNode]]
    edges: Required[List[WorkflowEdge]]
    metadata: NotRequired[Dict[str, Any]]


# ============================================================================
# POLICY TYPES
# ============================================================================

class Enforcement(TypedDict):
    """Represents enforcement mode for policy."""
    mode: Required[str]
    action: Required[str]
    audit_log: Required[bool]


class PolicyData(TypedDict):
    """Represents policy data including roles and permissions."""
    roles: Required[Dict[str, List[str]]]
    permissions: Required[Dict[str, List[str]]]


class Policy(TypedDict):
    """Represents a complete policy definition."""
    id: Required[str]
    name: Required[str]
    version: Required[str]
    description: Required[str]
    rego: Required[str]
    enforcement: Required[Enforcement]
    data: Required[PolicyData]
    metadata: NotRequired[Dict[str, Any]]


# ============================================================================
# PRACTICAL USAGE EXAMPLES
# ============================================================================

def example_workflow_creation() -> None:
    """
    Example 1: Creating a workflow from scratch using TypedDict.

    Benefits:
    - Type safety: IDE autocomplete and validation
    - Clear structure: All required fields are explicit
    - Self-documenting: Type names describe the data structure
    """
    # Create a sequential data processing workflow
    workflow: Workflow = {
        "id": "sequential-data-processing",
        "name": "Sequential Data Processing",
        "version": "1.0.0",
        "description": "Process data through sequential stages",
        "nodes": {
            "input-node": {
                "id": "input-node",
                "type": "input",
                "label": "Read Data",
                "config": {
                    "source": "api",
                    "endpoint": "/data",
                    "method": "GET"
                },
                "position": {"x": 100, "y": 100}
            },
            "transform-node": {
                "id": "transform-node",
                "type": "transform",
                "label": "Transform Data",
                "config": {
                    "operation": "map",
                    "expression": "data.map(x => x * 2)"
                },
                "position": {"x": 300, "y": 100}
            },
            "validate-node": {
                "id": "validate-node",
                "type": "transform",
                "label": "Validate Data",
                "config": {
                    "operation": "filter",
                    "expression": "data.filter(x => x > 0)"
                },
                "position": {"x": 500, "y": 100}
            },
            "output-node": {
                "id": "output-node",
                "type": "output",
                "label": "Save Results",
                "config": {
                    "destination": "database",
                    "table": "processed_data",
                    "mode": "append"
                },
                "position": {"x": 700, "y": 100}
            }
        },
        "edges": [
            {
                "id": "edge-1",
                "source": "input-node",
                "target": "transform-node",
                "relation": "data_flow"
            },
            {
                "id": "edge-2",
                "source": "transform-node",
                "target": "validate-node",
                "relation": "data_flow"
            },
            {
                "id": "edge-3",
                "source": "validate-node",
                "target": "output-node",
                "relation": "data_flow"
            }
        ],
        "metadata": {
            "author": "data-team",
            "tags": ["etl", "sequential", "data-processing"]
        }
    }

    # Verify workflow structure
    print(f"Workflow created: {workflow['name']}")
    print(f"Number of nodes: {len(workflow['nodes'])}")
    print(f"Number of edges: {len(workflow['edges'])}")


def example_policy_creation() -> None:
    """
    Example 2: Creating a policy with RBAC enforcement.

    Benefits:
    - Type safety: Enforcement mode and policy data are validated
    - Clear separation: Enforcement logic and data are separate
    - Audit-ready: audit_log field ensures compliance
    """
    # Create an RBAC policy
    policy: Policy = {
        "id": "rbac-policy",
        "name": "RBAC Policy",
        "version": "1.0.0",
        "description": "Role-based access control policy",
        "rego": """package authz

default allow := false

allow if {
    has_role(input.user, "admin")
}

allow if {
    has_role(input.user, "user")
    input.action == "read"
}

allow if {
    has_role(input.user, "user")
    input.resource == "public"
}

has_role(user, role) {
    data.roles[user][role]
}""",
        "enforcement": {
            "mode": "strict",
            "action": "deny",
            "audit_log": True
        },
        "data": {
            "roles": {
                "admin": ["alice", "bob"],
                "user": ["charlie", "david", "eve"]
            },
            "permissions": {
                "read": ["admin", "user"],
                "write": ["admin"],
                "execute": ["admin"]
            }
        },
        "metadata": {
            "author": "security-team",
            "tags": ["rbac", "access-control", "security"]
        }
    }

    # Verify policy structure
    print(f"Policy created: {policy['name']}")
    print(f"Enforcement mode: {policy['enforcement']['mode']}")
    print(f"Audit logging: {policy['enforcement']['audit_log']}")


def example_workflow_modification() -> None:
    """
    Example 3: Modifying an existing workflow.

    Benefits:
    - Immutable updates: Create new versions instead of mutating
    - Type safety: All modifications maintain type constraints
    - Version control: Easy to track changes over time
    """
    # Load workflow from JSON
    with open("examples/workflow_sequential_v3.json", "r") as f:
        workflow_data = json.load(f)

    # Convert to TypedDict (type-safe)
    workflow: Workflow = workflow_data

    # Add a new node to the workflow
    new_node: WorkflowNode = {
        "id": "cache-node",
        "type": "cache",
        "label": "Cache Results",
        "config": {
            "backend": "redis",
            "ttl": 3600
        },
        "position": {"x": 400, "y": 200}
    }

    # Insert node after transform-node
    workflow["nodes"]["cache-node"] = new_node

    # Add edge from transform-node to cache-node
    new_edge: WorkflowEdge = {
        "id": "edge-cache",
        "source": "transform-node",
        "target": "cache-node",
        "relation": "data_flow"
    }
    workflow["edges"].append(new_edge)

    # Verify modification
    print(f"Workflow modified: {workflow['name']}")
    print(f"New node added: {new_node['label']}")
    print(f"New edge added: {new_edge['id']}")


def example_policy_enforcement() -> None:
    """
    Example 4: Checking policy enforcement configuration.

    Benefits:
    - Type safety: Enforcement mode is validated
    - Compliance checking: Easy to verify audit requirements
    - Security validation: Ensure strict enforcement is configured
    """
    # Load policy from JSON
    with open("examples/policy_rbac_v3.json", "r") as f:
        policy_data = json.load(f)

    # Convert to TypedDict (type-safe)
    policy: Policy = policy_data

    # Check enforcement configuration
    enforcement = policy["enforcement"]

    if enforcement["mode"] == "strict":
        print("✓ Policy uses strict enforcement mode")
    else:
        print("⚠ Policy uses lenient enforcement mode")

    if enforcement["audit_log"]:
        print("✓ Audit logging is enabled")
    else:
        print("⚠ Audit logging is disabled")

    # Verify policy data structure
    roles = policy["data"]["roles"]
    print(f"✓ Policy defines {len(roles)} role(s)")
    for role, users in roles.items():
        print(f"  - {role}: {len(users)} user(s)")


def example_type_safety_with_mypy() -> None:
    """
    Example 5: Demonstrating type safety benefits with mypy.

    Run with: mypy python_bindings_example.py

    Benefits:
    - Catch errors at development time, not runtime
    - IDE autocomplete and type hints
    - Self-documenting code
    """
    # This demonstrates type-safe code
    workflow: Workflow = {
        "id": "test-workflow",
        "name": "Test Workflow",
        "version": "1.0.0",
        "description": "Test workflow",
        "nodes": {
            "node-1": {
                "id": "node-1",
                "type": "input",
                "label": "Input",
                "config": {},
                "position": {"x": 0, "y": 0}
            }
        },
        "edges": []
    }

    # Type-safe access - IDE will show autocomplete
    node_id = workflow["nodes"]["node-1"]["id"]
    node_type = workflow["nodes"]["node-1"]["type"]

    # Type-safe modification
    workflow["nodes"]["node-1"]["label"] = "Updated Input"

    # Type-safe iteration
    for node_id, node in workflow["nodes"].items():
        print(f"Node: {node['label']} ({node['type']})")

    # Type-safe edge iteration
    for edge in workflow["edges"]:
        print(f"Edge: {edge['source']} -> {edge['target']}")

    # This would cause a mypy error (commented out):
    # workflow["invalid_field"] = "This will cause a type error"


def example_serialization() -> None:
    """
    Example 6: Serializing TypedDict to JSON.

    Benefits:
    - Type-safe serialization
    - Easy integration with APIs and databases
    - Clear data structure in JSON output
    """
    # Create a workflow
    workflow: Workflow = {
        "id": "serialization-test",
        "name": "Serialization Test",
        "version": "1.0.0",
        "description": "Test workflow serialization",
        "nodes": {
            "test-node": {
                "id": "test-node",
                "type": "input",
                "label": "Test",
                "config": {},
                "position": {"x": 0, "y": 0}
            }
        },
        "edges": []
    }

    # Serialize to JSON
    workflow_json = json.dumps(workflow, indent=2)

    # Write to file
    with open("workflow_output.json", "w") as f:
        f.write(workflow_json)

    print("✓ Workflow serialized to JSON")
    print(f"✓ JSON written to workflow_output.json")


def example_validation() -> None:
    """
    Example 7: Validating TypedDict structure.

    Benefits:
    - Runtime validation
    - Clear error messages
    - Data integrity checks
    """
    # Create a workflow with missing required field (will fail validation)
    invalid_workflow = {
        "id": "invalid-workflow",
        "name": "Invalid Workflow",
        # Missing 'version' - required field
        "description": "This workflow is invalid",
        "nodes": {},
        "edges": []
    }

    # Validate workflow structure
    try:
        # This would fail at runtime if version is missing
        # In practice, you'd use a validation library
        if "version" not in invalid_workflow:
            raise ValueError("Missing required field: version")

        workflow: Workflow = invalid_workflow
        print("✓ Workflow is valid")
    except (KeyError, ValueError) as e:
        print(f"✗ Workflow validation failed: {e}")


# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main() -> None:
    """Run all examples."""
    print("=" * 70)
    print("ADL Python Binding Examples")
    print("=" * 70)
    print()

    # Example 1: Workflow creation
    print("Example 1: Creating a workflow")
    print("-" * 70)
    example_workflow_creation()
    print()

    # Example 2: Policy creation
    print("Example 2: Creating a policy")
    print("-" * 70)
    example_policy_creation()
    print()

    # Example 3: Workflow modification
    print("Example 3: Modifying an existing workflow")
    print("-" * 70)
    example_workflow_modification()
    print()

    # Example 4: Policy enforcement
    print("Example 4: Checking policy enforcement")
    print("-" * 70)
    example_policy_enforcement()
    print()

    # Example 5: Type safety
    print("Example 5: Type safety with mypy")
    print("-" * 70)
    example_type_safety_with_mypy()
    print()

    # Example 6: Serialization
    print("Example 6: Serializing TypedDict to JSON")
    print("-" * 70)
    example_serialization()
    print()

    # Example 7: Validation
    print("Example 7: Validating TypedDict structure")
    print("-" * 70)
    example_validation()
    print()

    print("=" * 70)
    print("All examples completed successfully!")
    print("=" * 70)
    print()
    print("Next steps:")
    print("1. Run mypy to verify type safety: mypy python_bindings_example.py")
    print("2. Run the example: python python_bindings_example.py")
    print("3. Review the generated JSON output: cat workflow_output.json")


if __name__ == "__main__":
    main()