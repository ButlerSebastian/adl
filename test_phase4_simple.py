#!/usr/bin/env python3
"""Simple test script for Python generator with Phase 4 types"""

import sys
from pathlib import Path

# Add the tools directory to the path
sys.path.insert(0, str(Path(__file__).parent))

from tools.dsl.parser import GrammarParser
from tools.dsl.python_generator import PythonGenerator

def test_phase4_generator():
    """Test Python generator with Phase 4 types from ADL DSL"""
    print("=" * 60)
    print("Testing Python Generator with Phase 4 Types")
    print("=" * 60)

    # Parse the ADL DSL file with workflow and policy types
    adl_file = Path(__file__).parent / "test_phase4.adl"
    parser = GrammarParser()
    try:
        program = parser.parse_file(str(adl_file))
        print(f"✓ Parsed ADL file successfully")
    except Exception as e:
        print(f"✗ Failed to parse ADL file: {e}")
        import traceback
        traceback.print_exc()
        return False

    # Generate Python code
    generator = PythonGenerator()
    try:
        py_code = generator.generate(program)
        print(f"✓ Generated Python code successfully")
    except Exception as e:
        print(f"✗ Failed to generate Python code: {e}")
        import traceback
        traceback.print_exc()
        return False

    # Print the generated code
    print("\nGenerated Python Code:")
    print("-" * 60)
    print(py_code)
    print("-" * 60)

    # Check if workflow and policy TypedDicts are present
    checks = [
        ("class Workflow(TypedDict):", "Workflow TypedDict"),
        ("class WorkflowNode(TypedDict):", "WorkflowNode TypedDict"),
        ("class WorkflowEdge(TypedDict):", "WorkflowEdge TypedDict"),
        ("class Policy(TypedDict):", "Policy TypedDict"),
        ("class Enforcement(TypedDict):", "Enforcement TypedDict"),
    ]

    all_passed = True
    for check_str, check_name in checks:
        if check_str in py_code:
            print(f"✓ {check_name} generated")
        else:
            print(f"✗ {check_name} NOT generated")
            all_passed = False

    # Check for required fields
    field_checks = [
        ("id: Required[str]", "Workflow.id field"),
        ("name: Required[str]", "Workflow.name field"),
        ("version: Required[str]", "Workflow.version field"),
        ("description: Required[str]", "Workflow.description field"),
        ("nodes: Required[Dict[str, Any]]", "Workflow.nodes field"),
        ("edges: Required[List[WorkflowEdge]]", "Workflow.edges field"),
        ("metadata: Required[Dict[str, Any]]", "Workflow.metadata field"),
        ("rego: Required[str]", "Policy.rego field"),
        ("enforcement: Required[Enforcement]", "Policy.enforcement field"),
        ("data: Required[Dict[str, Any]]", "Policy.data field"),
        ("mode: Required[str]", "Enforcement.mode field"),
        ("action: Required[str]", "Enforcement.action field"),
        ("audit_log: Required[bool]", "Enforcement.audit_log field"),
    ]

    for check_str, check_name in field_checks:
        if check_str in py_code:
            print(f"✓ {check_name} field generated")
        else:
            print(f"✗ {check_name} field NOT generated")
            all_passed = False

    return all_passed

def main():
    """Run the test"""
    print("\n" + "=" * 60)
    print("Python Generator - Phase 4 Simple Test")
    print("=" * 60)

    passed = test_phase4_generator()

    print("\n" + "=" * 60)
    print("Test Results")
    print("=" * 60)
    print(f"Test: {'PASSED ✓' if passed else 'FAILED ✗'}")
    print("=" * 60)

    if passed:
        print("\n✓ All tests passed!")
        return 0
    else:
        print("\n✗ Some tests failed!")
        return 1

if __name__ == "__main__":
    sys.exit(main())