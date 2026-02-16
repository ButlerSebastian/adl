"""
TypeScript Code Generator for ADL DSL

This module generates TypeScript type definitions from ADL DSL ASTs.
"""

from typing import List, Dict, Any, Optional, Tuple
from .adl_ast import (
    Program, TypeDef, EnumDef, AgentDef, FieldDef,
    TypeReference, ConstrainedType, ArrayType, UnionType,
    PrimitiveType, OptionalType, ASTVisitor,
    WorkflowDef, WorkflowNodeDef, WorkflowEdgeDef,
    PolicyDef, EnforcementDef
)
import subprocess
import tempfile
import os


class TypeScriptGenerator(ASTVisitor[str]):
    """
    Generates TypeScript type definitions from ADL DSL AST.

    Uses visitor pattern to traverse AST and build TypeScript code.
    """

    def __init__(self):
        self.indent_level = 0
        self.lines: List[str] = []

    def validate_typescript_syntax(self, code: str) -> Tuple[bool, Optional[str]]:
        """
        Validate TypeScript syntax using tsc.

        Args:
            code: TypeScript code to validate

        Returns:
            Tuple of (is_valid, error_message)
        """
        try:
            # Create a temporary file with the code
            with tempfile.NamedTemporaryFile(mode='w', suffix='.ts', delete=False) as f:
                f.write(code)
                temp_file = f.name

            try:
                # Run tsc --noEmit to check syntax without generating output
                result = subprocess.run(
                    ['tsc', '--noEmit', '--skipLibCheck', temp_file],
                    capture_output=True,
                    text=True,
                    timeout=10
                )

                if result.returncode != 0 and result.stdout:
                    # Parse tsc output
                    error_lines = []
                    for line in result.stdout.split('\n'):
                        if line.strip():
                            error_lines.append(line.strip())

                    if error_lines:
                        return False, "\n".join(error_lines)

                return True, None

            except subprocess.TimeoutExpired:
                return False, "TypeScript compilation timed out (10s)"
            except FileNotFoundError:
                # tsc not available, skip syntax validation
                return True, None
            finally:
                # Clean up temp file
                if os.path.exists(temp_file):
                    os.unlink(temp_file)

        except Exception as e:
            return False, f"TypeScript validation error: {str(e)}"

    def validate_typescript_types(self, code: str) -> List[str]:
        """
        Validate TypeScript types using tsc --noEmit.

        Args:
            code: TypeScript code to validate

        Returns:
            List of type checking errors (empty if no errors)
        """
        errors = []

        # Try to use tsc for type checking
        try:
            # Create a temporary file with the code
            with tempfile.NamedTemporaryFile(mode='w', suffix='.ts', delete=False) as f:
                f.write(code)
                temp_file = f.name

            try:
                # Run tsc --noEmit to check types without generating output
                result = subprocess.run(
                    ['tsc', '--noEmit', '--skipLibCheck', '--strict', temp_file],
                    capture_output=True,
                    text=True,
                    timeout=10
                )

                if result.returncode != 0 and result.stdout:
                    # Parse tsc output
                    for line in result.stdout.split('\n'):
                        if line.strip():
                            errors.append(line.strip())

            except subprocess.TimeoutExpired:
                errors.append("Type checking timed out (10s)")
            except FileNotFoundError:
                # tsc not available, skip type checking
                pass
            finally:
                # Clean up temp file
                if os.path.exists(temp_file):
                    os.unlink(temp_file)

        except Exception as e:
            errors.append(f"Type checking error: {str(e)}")

        return errors

    def validate_generated_code(self, code: str) -> Tuple[bool, List[str]]:
        """
        Validate generated TypeScript code for syntax and types.

        Args:
            code: TypeScript code to validate

        Returns:
            Tuple of (is_valid, list_of_errors)
        """
        errors = []

        # Validate syntax
        is_valid, syntax_error = self.validate_typescript_syntax(code)
        if not is_valid:
            errors.append(syntax_error)

        # Validate types
        type_errors = self.validate_typescript_types(code)
        errors.extend(type_errors)

        return len(errors) == 0, errors

    def generate(self, program: Program) -> str:
        """
        Generate TypeScript code from a complete ADL program.

        Args:
            program: The AST program to convert

        Returns:
            TypeScript code as a string

        Raises:
            ValueError: If generated code fails validation
        """
        self.indent_level = 0
        self.lines = []

        # Process all declarations
        for decl in program.declarations:
            if isinstance(decl, EnumDef):
                self.lines.append(decl.accept(self))
                self.lines.append("")
            elif isinstance(decl, TypeDef):
                self.lines.append(decl.accept(self))
                self.lines.append("")

        # Process agent if present
        if program.agent:
            self.lines.append(program.agent.accept(self))
            self.lines.append("")

        code = "\n".join(self.lines).strip()

        # Validate generated code
        is_valid, errors = self.validate_generated_code(code)
        if not is_valid:
            error_msg = "Generated code validation failed:\n" + "\n".join(f"  - {err}" for err in errors)
            raise ValueError(error_msg)

        return code

    def visit_EnumDef(self, node: EnumDef) -> str:
        """Generate TypeScript enum from an enum definition."""
        values = "\n".join([f"  {value}," for value in node.values])
        return f"export enum {node.name} {{\n{values}\n}}"

    def visit_TypeDef(self, node: TypeDef) -> str:
        """Generate TypeScript interface from a type definition."""
        if not node.body:
            return f"export interface {node.name} {{}}"
        fields = []
        for field in node.body.fields:
            field_type = field.type.accept(self)
            optional = "?" if field.optional else ""
            fields.append(f"  {field.name}{optional}: {field_type};")

        fields_str = "\n".join(fields)
        return f"export interface {node.name} {{\n{fields_str}\n}}"

    def visit_AgentDef(self, node: AgentDef) -> str:
        """Generate TypeScript type from an agent definition."""
        fields = []
        for field in node.fields:
            field_type = field.type.accept(self)
            optional = "?" if field.optional else ""
            fields.append(f"  {field.name}{optional}: {field_type};")

        fields_str = "\n".join(fields)
        return f"export type {node.name} = {{\n{fields_str}\n}};"

    def visit_PrimitiveType(self, node: PrimitiveType) -> str:
        """Generate TypeScript type for a primitive type."""
        type_mapping = {
            "string": "string",
            "integer": "number",
            "number": "number",
            "boolean": "boolean",
            "object": "Record<string, any>",
            "array": "any[]",
            "any": "any",
            "null": "null"
        }
        return type_mapping.get(node.name, "string")

    def visit_TypeReference(self, node: TypeReference) -> str:
        """Generate TypeScript type for a type reference."""
        return node.name

    def visit_ArrayType(self, node: ArrayType) -> str:
        """Generate TypeScript type for an array type."""
        element_type = node.element_type.accept(self)
        return f"{element_type}[]"

    def visit_UnionType(self, node: UnionType) -> str:
        """Generate TypeScript type for a union type."""
        types = " | ".join([union_type.accept(self) for union_type in node.types])
        return types

    def visit_OptionalType(self, node: OptionalType) -> str:
        """Generate TypeScript type for an optional type."""
        inner_type = node.inner_type.accept(self)
        return f"{inner_type} | null"

    def visit_ConstrainedType(self, node: ConstrainedType) -> str:
        """Generate TypeScript type for a constrained type."""
        base_type = node.base_type.accept(self)
        return base_type

    def visit_default(self, node) -> str:
        """Default visitor for unhandled node types."""
        return "any"

    def visit_Program(self, node: Program) -> str:
        """Visit program node."""
        return ""

    def visit_ImportStmt(self, node) -> str:
        """Visit import statement node."""
        return ""

    def visit_FieldDef(self, node: FieldDef) -> str:
        """Visit field definition node."""
        return ""

    def visit_TypeBody(self, node) -> str:
        """Visit type body node."""
        return ""

    def visit_FieldList(self, node) -> str:
        """Visit field list node."""
        return ""

    # Phase 4: Workflow and Policy visitor methods
    def visit_WorkflowDef(self, node: WorkflowDef) -> str:
        """Generate TypeScript interface for workflow definition."""
        # Generate nested interfaces first
        node_interface = self.visit_WorkflowNodeDef(node.nodes["input-node"])
        edge_interface = self.visit_WorkflowEdgeDef(node.edges[0])

        # Generate workflow interface
        fields = [
            f"  /**\n   * Unique identifier for this workflow.\n   * Recommended format: 'namespace/workflow-name'\n   * Example: 'marketing/campaign-creator'\n   */",
            f"  workflow_id: string;",
            f"  /**\n   * Human-readable name of the workflow.\n   */",
            f"  name: string;",
            f"  /**\n   * Version number of this workflow definition.\n   */",
            f"  version: string;",
            f"  /**\n   * Detailed description of the workflow's purpose and behavior.\n   */",
            f"  description: string;",
            f"  /**\n   * Map of node identifiers to node configurations.\n   * Note: Node keys serve as unique identifiers.\n   */",
            f"  nodes: Record<string, WorkflowNode>;",
            f"  /**\n   * List of edges connecting nodes in the workflow.\n   */",
            f"  edges: WorkflowEdge[];",
            f"  /**\n   * Optional metadata for this workflow.\n   */",
            f"  metadata?: Record<string, any>;",
            f"  /**\n   * @deprecated Use workflow_id instead.\n   */",
            f"  id?: string;"
        ]
        fields_str = "\n".join(fields)
        return f"{node_interface}\n\n{edge_interface}\n\nexport interface Workflow {{\n{fields_str}\n}}"

    def visit_WorkflowNodeDef(self, node: WorkflowNodeDef) -> str:
        """Generate TypeScript interface for workflow node."""
        fields = [
            f"  /**\n   * Type of this node (e.g., 'input', 'process', 'output').\n   */",
            f"  type: string;",
            f"  /**\n   * Human-readable label for this node.\n   */",
            f"  label: string;",
            f"  /**\n   * Configuration for this node.\n   */",
            f"  config: Record<string, any>;",
            f"  /**\n   * Position of this node in the workflow canvas.\n   */",
            f"  position: {{ x: number; y: number }};"
        ]
        fields_str = "\n".join(fields)
        return f"export interface WorkflowNode {{\n{fields_str}\n}}"

    def visit_WorkflowEdgeDef(self, node: WorkflowEdgeDef) -> str:
        """Generate TypeScript interface for workflow edge."""
        fields = [
            f"  /**\n   * Unique identifier for this edge.\n   * Recommended format: 'source-node-target-node'\n   * Example: 'input-node-process-node'\n   */",
            f"  edge_id: string;",
            f"  /**\n   * Source node identifier.\n   */",
            f"  source: string;",
            f"  /**\n   * Target node identifier.\n   */",
            f"  target: string;",
            f"  /**\n   * Relationship type between source and target nodes.\n   */",
            f"  relation: string;",
            f"  /**\n   * Optional condition for edge execution.\n   */",
            f"  condition?: Record<string, any>;",
            f"  /**\n   * Optional metadata for this edge.\n   */",
            f"  metadata?: Record<string, any>;",
            f"  /**\n   * @deprecated Use edge_id instead.\n   */",
            f"  id?: string;"
        ]
        fields_str = "\n".join(fields)
        return f"export interface WorkflowEdge {{\n{fields_str}\n}}"

    def visit_PolicyDef(self, node: PolicyDef) -> str:
        """Generate TypeScript interface for policy definition."""
        # Generate enforcement interface first
        enforcement_interface = self.visit_EnforcementDef(node.enforcement)

        # Generate policy interface
        fields = [
            f"  /**\n   * Unique identifier for this policy.\n   * Recommended format: 'namespace/policy-name'\n   * Example: 'security/data-access-policy'\n   */",
            f"  policy_id: string;",
            f"  /**\n   * Human-readable name of the policy.\n   */",
            f"  name: string;",
            f"  /**\n   * Version number of this policy definition.\n   */",
            f"  version: string;",
            f"  /**\n   * Detailed description of the policy's purpose and behavior.\n   */",
            f"  description: string;",
            f"  /**\n   * Rego policy rules.\n   */",
            f"  rego: string;",
            f"  /**\n   * Enforcement settings for this policy.\n   */",
            f"  enforcement: Enforcement;",
            f"  /**\n   * Additional data for this policy.\n   */",
            f"  data: Record<string, any>;",
            f"  /**\n   * Optional metadata for this policy.\n   */",
            f"  metadata?: Record<string, any>;",
            f"  /**\n   * @deprecated Use policy_id instead.\n   */",
            f"  id?: string;"
        ]
        fields_str = "\n".join(fields)
        return f"{enforcement_interface}\n\nexport interface Policy {{\n{fields_str}\n}}"

    def visit_EnforcementDef(self, node: EnforcementDef) -> str:
        """Generate TypeScript interface for enforcement settings."""
        fields = [
            f"  mode: 'strict' | 'moderate' | 'lenient';",
            f"  action: 'deny' | 'warn' | 'log' | 'allow';",
            f"  audit_log: boolean;"
        ]
        fields_str = "\n".join(fields)
        return f"export interface Enforcement {{\n{fields_str}\n}}"
