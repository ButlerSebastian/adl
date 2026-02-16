#!/usr/bin/env python3
"""Simple test script for TypeScript generator with Phase 4 types"""

import sys
from pathlib import Path

# Add the tools directory to the path
sys.path.insert(0, str(Path(__file__).parent))

from tools.dsl.typescript_generator import TypeScriptGenerator
from tools.dsl.ast import (
    WorkflowDef, WorkflowNodeDef, WorkflowEdgeDef,
    PolicyDef, EnforcementDef
)

def test_workflow_generator():
    """Test TypeScript generator with workflow AST"""
    print("=" * 60)
    print("Testing Workflow Generator")
    print("=" * 60)

    # Create workflow AST nodes
    workflow = WorkflowDef(
        loc=None,
        id="sequential-data-processing",
        name="Sequential Data Processing",
        version="1.0.0",
        description="Sequential workflow for processing data through multiple stages",
        nodes={
            "input-node": WorkflowNodeDef(
                loc=None,
                id="input-node",
                type="input",
                label="Read Data",
                config={"source": "api", "endpoint": "/data", "method": "GET"},
                position={"x": 100, "y": 100}
            ),
            "transform-node": WorkflowNodeDef(
                loc=None,
                id="transform-node",
                type="transform",
                label="Transform Data",
                config={"operation": "map", "expression": "data.map(x => x * 2)"},
                position={"x": 300, "y": 100}
            ),
            "validate-node": WorkflowNodeDef(
                loc=None,
                id="validate-node",
                type="transform",
                label="Validate Data",
                config={"operation": "filter", "expression": "data.filter(x => x > 0)"},
                position={"x": 500, "y": 100}
            ),
            "output-node": WorkflowNodeDef(
                loc=None,
                id="output-node",
                type="output",
                label="Save Results",
                config={"destination": "database", "table": "processed_data", "mode": "append"},
                position={"x": 700, "y": 100}
            )
        },
        edges=[
            WorkflowEdgeDef(
                loc=None,
                id="edge-1",
                source="input-node",
                target="transform-node",
                relation="data_flow"
            ),
            WorkflowEdgeDef(
                loc=None,
                id="edge-2",
                source="transform-node",
                target="validate-node",
                relation="data_flow"
            ),
            WorkflowEdgeDef(
                loc=None,
                id="edge-3",
                source="validate-node",
                target="output-node",
                relation="data_flow"
            )
        ],
        metadata={"author": "data-team", "tags": ["etl", "sequential", "data-processing"]}
    )

    # Generate TypeScript code
    generator = TypeScriptGenerator()
    try:
        ts_code = generator.visit_WorkflowDef(workflow)
        print(f"✓ Generated TypeScript code successfully")
    except Exception as e:
        print(f"✗ Failed to generate TypeScript code: {e}")
        import traceback
        traceback.print_exc()
        return False

    # Print the generated code
    print("\nGenerated TypeScript Code:")
    print("-" * 60)
    print(ts_code)
    print("-" * 60)

    # Check if workflow interfaces are present
    if "export interface Workflow" in ts_code:
        print("✓ Workflow interface generated")
    else:
        print("✗ Workflow interface NOT generated")
        return False

    if "export interface WorkflowNode" in ts_code:
        print("✓ WorkflowNode interface generated")
    else:
        print("✗ WorkflowNode interface NOT generated")
        return False

    if "export interface WorkflowEdge" in ts_code:
        print("✓ WorkflowEdge interface generated")
    else:
        print("✗ WorkflowEdge interface NOT generated")
        return False

    return True

def test_policy_generator():
    """Test TypeScript generator with policy AST"""
    print("\n" + "=" * 60)
    print("Testing Policy Generator")
    print("=" * 60)

    # Create policy AST nodes
    enforcement = EnforcementDef(
        loc=None,
        mode="strict",
        action="deny",
        audit_log=True
    )

    policy = PolicyDef(
        loc=None,
        id="rbac-policy",
        name="RBAC Policy",
        version="1.0.0",
        description="Role-based access control policy with admin and user roles",
        rego="package authz\ndefault allow := false\n\nallow if {\n    has_role(input.user, \"admin\")\n}\n\nallow if {\n    has_role(input.user, \"user\")\n    input.action == \"read\"\n}\n\nallow if {\n    has_role(input.user, \"user\")\n    input.resource == \"public\"\n}\n\nhas_role(user, role) {\n    data.roles[user][role]\n}",
        enforcement=enforcement,
        data={
            "roles": {
                "admin": ["alice", "bob"],
                "user": ["charlie", "david", "eve"]
            }
        },
        metadata={"author": "security-team", "tags": ["rbac", "access-control", "security"]}
    )

    # Generate TypeScript code
    generator = TypeScriptGenerator()
    try:
        ts_code = generator.visit_PolicyDef(policy)
        print(f"✓ Generated TypeScript code successfully")
    except Exception as e:
        print(f"✗ Failed to generate TypeScript code: {e}")
        import traceback
        traceback.print_exc()
        return False

    # Print the generated code
    print("\nGenerated TypeScript Code:")
    print("-" * 60)
    print(ts_code)
    print("-" * 60)

    # Check if policy interfaces are present
    if "export interface Policy" in ts_code:
        print("✓ Policy interface generated")
    else:
        print("✗ Policy interface NOT generated")
        return False

    if "export interface Enforcement" in ts_code:
        print("✓ Enforcement interface generated")
    else:
        print("✗ Enforcement interface NOT generated")
        return False

    return True

def test_combined_generator():
    """Test TypeScript generator with combined workflow and policy"""
    print("\n" + "=" * 60)
    print("Testing Combined Generator")
    print("=" * 60)

    # Create workflow AST nodes
    workflow = WorkflowDef(
        loc=None,
        id="sequential-data-processing",
        name="Sequential Data Processing",
        version="1.0.0",
        description="Sequential workflow for processing data through multiple stages",
        nodes={
            "input-node": WorkflowNodeDef(
                loc=None,
                id="input-node",
                type="input",
                label="Read Data",
                config={"source": "api", "endpoint": "/data", "method": "GET"},
                position={"x": 100, "y": 100}
            )
        },
        edges=[
            WorkflowEdgeDef(
                loc=None,
                id="edge-1",
                source="input-node",
                target="input-node",
                relation="data_flow"
            )
        ],
        metadata={"author": "data-team"}
    )

    # Create policy AST nodes
    enforcement = EnforcementDef(
        loc=None,
        mode="strict",
        action="deny",
        audit_log=True
    )

    policy = PolicyDef(
        loc=None,
        id="rbac-policy",
        name="RBAC Policy",
        version="1.0.0",
        description="Role-based access control policy",
        rego="package authz\ndefault allow := false",
        enforcement=enforcement,
        data={"roles": {"admin": ["alice"]}},
        metadata={"author": "security-team"}
    )

    # Generate TypeScript code for both
    generator = TypeScriptGenerator()
    try:
        workflow_code = generator.visit_WorkflowDef(workflow)
        policy_code = generator.visit_PolicyDef(policy)
        print(f"✓ Generated TypeScript code for both workflow and policy")
    except Exception as e:
        print(f"✗ Failed to generate TypeScript code: {e}")
        import traceback
        traceback.print_exc()
        return False

    # Combine the code
    combined_code = f"{workflow_code}\n\n{policy_code}"

    # Print the combined code
    print("\nCombined TypeScript Code:")
    print("-" * 60)
    print(combined_code)
    print("-" * 60)

    # Check if all interfaces are present
    if "export interface Workflow" in combined_code:
        print("✓ Workflow interface generated")
    else:
        print("✗ Workflow interface NOT generated")
        return False

    if "export interface WorkflowNode" in combined_code:
        print("✓ WorkflowNode interface generated")
    else:
        print("✗ WorkflowNode interface NOT generated")
        return False

    if "export interface WorkflowEdge" in combined_code:
        print("✓ WorkflowEdge interface generated")
    else:
        print("✗ WorkflowEdge interface NOT generated")
        return False

    if "export interface Policy" in combined_code:
        print("✓ Policy interface generated")
    else:
        print("✗ Policy interface NOT generated")
        return False

    if "export interface Enforcement" in combined_code:
        print("✓ Enforcement interface generated")
    else:
        print("✗ Enforcement interface NOT generated")
        return False

    return True

def main():
    """Run all tests"""
    print("\n" + "=" * 60)
    print("TypeScript Generator - Phase 4 Tests")
    print("=" * 60)

    workflow_passed = test_workflow_generator()
    policy_passed = test_policy_generator()
    combined_passed = test_combined_generator()

    print("\n" + "=" * 60)
    print("Test Results")
    print("=" * 60)
    print(f"Workflow Tests: {'PASSED ✓' if workflow_passed else 'FAILED ✗'}")
    print(f"Policy Tests: {'PASSED ✓' if policy_passed else 'FAILED ✗'}")
    print(f"Combined Tests: {'PASSED ✓' if combined_passed else 'FAILED ✗'}")
    print("=" * 60)

    if workflow_passed and policy_passed and combined_passed:
        print("\n✓ All tests passed!")
        return 0
    else:
        print("\n✗ Some tests failed!")
        return 1

if __name__ == "__main__":
    sys.exit(main())