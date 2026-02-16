#!/usr/bin/env python3
"""Test script for TypeScript generator with Phase 4 types"""

import json
import sys
from pathlib import Path

# Add the tools directory to the path
sys.path.insert(0, str(Path(__file__).parent))

from tools.dsl.typescript_generator import TypeScriptGenerator
from tools.dsl.parser import GrammarParser

def test_workflow_generator():
    """Test TypeScript generator with workflow example"""
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

    # Generate TypeScript code
    generator = TypeScriptGenerator()
    try:
        ts_code = generator.generate(ast)
        print(f"✓ Generated TypeScript code successfully")
    except Exception as e:
        print(f"✗ Failed to generate TypeScript code: {e}")
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
    """Test TypeScript generator with policy example"""
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

    # Generate TypeScript code
    generator = TypeScriptGenerator()
    try:
        ts_code = generator.generate(ast)
        print(f"✓ Generated TypeScript code successfully")
    except Exception as e:
        print(f"✗ Failed to generate TypeScript code: {e}")
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

def main():
    """Run all tests"""
    print("\n" + "=" * 60)
    print("TypeScript Generator - Phase 4 Tests")
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