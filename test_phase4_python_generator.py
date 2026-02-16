#!/usr/bin/env python3
"""Test script for Python generator with Phase 4 types"""

import json
import sys
from pathlib import Path

# Add the tools directory to the path
sys.path.insert(0, str(Path(__file__).parent))

from tools.dsl.python_generator import PythonGenerator
from tools.dsl.parser import GrammarParser

def test_workflow_generator():
    """Test Python generator with workflow example"""
    print("=" * 60)
    print("Testing Workflow Generator")
    print("=" * 60)

    # Load workflow example
    workflow_file = Path(__file__).parent / "examples" / "workflow_sequential_v3.json"
    with open(workflow_file, 'r') as f:
        workflow_data = json.load(f)

    # Create parser and generate AST
    parser = GrammarParser()
    try:
        ast = parser.parse(workflow_data)
        print(f"✓ Parsed workflow successfully")
    except Exception as e:
        print(f"✗ Failed to parse workflow: {e}")
        return False

    # Generate Python code
    generator = PythonGenerator()
    try:
        py_code = generator.generate(ast)
        print(f"✓ Generated Python code successfully")
    except Exception as e:
        print(f"✗ Failed to generate Python code: {e}")
        return False

    # Print the generated code
    print("\nGenerated Python Code:")
    print("-" * 60)
    print(py_code)
    print("-" * 60)

    # Check if workflow TypedDicts are present
    if "class Workflow(TypedDict):" in py_code:
        print("✓ Workflow TypedDict generated")
    else:
        print("✗ Workflow TypedDict NOT generated")
        return False

    if "class WorkflowNode(TypedDict):" in py_code:
        print("✓ WorkflowNode TypedDict generated")
    else:
        print("✗ WorkflowNode TypedDict NOT generated")
        return False

    if "class WorkflowEdge(TypedDict):" in py_code:
        print("✓ WorkflowEdge TypedDict generated")
    else:
        print("✗ WorkflowEdge TypedDict NOT generated")
        return False

    # Check for required fields
    if "id: Required[str]" in py_code:
        print("✓ Workflow.id field generated")
    else:
        print("✗ Workflow.id field NOT generated")
        return False

    if "nodes: Required[Dict[str, WorkflowNode]]" in py_code:
        print("✓ Workflow.nodes field generated")
    else:
        print("✗ Workflow.nodes field NOT generated")
        return False

    if "edges: Required[List[WorkflowEdge]]" in py_code:
        print("✓ Workflow.edges field generated")
    else:
        print("✗ Workflow.edges field NOT generated")
        return False

    return True

def test_policy_generator():
    """Test Python generator with policy example"""
    print("\n" + "=" * 60)
    print("Testing Policy Generator")
    print("=" * 60)

    # Load policy example
    policy_file = Path(__file__).parent / "examples" / "policy_rbac_v3.json"
    with open(policy_file, 'r') as f:
        policy_data = json.load(f)

    # Create parser and generate AST
    parser = GrammarParser()
    try:
        ast = parser.parse(policy_data)
        print(f"✓ Parsed policy successfully")
    except Exception as e:
        print(f"✗ Failed to parse policy: {e}")
        return False

    # Generate Python code
    generator = PythonGenerator()
    try:
        py_code = generator.generate(ast)
        print(f"✓ Generated Python code successfully")
    except Exception as e:
        print(f"✗ Failed to generate Python code: {e}")
        return False

    # Print the generated code
    print("\nGenerated Python Code:")
    print("-" * 60)
    print(py_code)
    print("-" * 60)

    # Check if policy TypedDicts are present
    if "class Policy(TypedDict):" in py_code:
        print("✓ Policy TypedDict generated")
    else:
        print("✗ Policy TypedDict NOT generated")
        return False

    if "class Enforcement(TypedDict):" in py_code:
        print("✓ Enforcement TypedDict generated")
    else:
        print("✗ Enforcement TypedDict NOT generated")
        return False

    # Check for required fields
    if "id: Required[str]" in py_code:
        print("✓ Policy.id field generated")
    else:
        print("✗ Policy.id field NOT generated")
        return False

    if "rego: Required[str]" in py_code:
        print("✓ Policy.rego field generated")
    else:
        print("✗ Policy.rego field NOT generated")
        return False

    if "enforcement: Required[Enforcement]" in py_code:
        print("✓ Policy.enforcement field generated")
    else:
        print("✗ Policy.enforcement field NOT generated")
        return False

    return True

def main():
    """Run all tests"""
    print("\n" + "=" * 60)
    print("Python Generator - Phase 4 Tests")
    print("=" * 60)

    workflow_passed = test_workflow_generator()
    policy_passed = test_policy_generator()

    print("\n" + "=" * 60)
    print("Test Results")
    print("=" * 60)
    print(f"Workflow Tests: {'PASSED ✓' if workflow_passed else 'FAILED ✗'}")
    print(f"Policy Tests: {'PASSED ✓' if policy_passed else 'FAILED ✗'}")
    print("=" * 60)

    if workflow_passed and policy_passed:
        print("\n✓ All tests passed!")
        return 0
    else:
        print("\n✗ Some tests failed!")
        return 1

if __name__ == "__main__":
    sys.exit(main())