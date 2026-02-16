"""
TypeScript Code Generator for ADL DSL

This module generates TypeScript type definitions from ADL DSL ASTs.
"""

from typing import List, Dict, Any
from .ast import (
    Program, TypeDef, EnumDef, AgentDef, FieldDef,
    TypeReference, ConstrainedType, ArrayType, UnionType,
    PrimitiveType, OptionalType, ASTVisitor,
    WorkflowDef, WorkflowNodeDef, WorkflowEdgeDef,
    PolicyDef, EnforcementDef
)


class TypeScriptGenerator(ASTVisitor[str]):
    """
    Generates TypeScript type definitions from ADL DSL AST.
    
    Uses visitor pattern to traverse AST and build TypeScript code.
    """

    def __init__(self):
        self.indent_level = 0
        self.lines: List[str] = []

    def generate(self, program: Program) -> str:
        """
        Generate TypeScript code from a complete ADL program.

        Args:
            program: The AST program to convert

        Returns:
            TypeScript code as a string
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

        return "\n".join(self.lines).strip()

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
            f"  id: string;",
            f"  name: string;",
            f"  version: string;",
            f"  description: string;",
            f"  nodes: Record<string, WorkflowNode>;",
            f"  edges: WorkflowEdge[];",
            f"  metadata?: Record<string, any>;"
        ]
        fields_str = "\n".join(fields)
        return f"{node_interface}\n\n{edge_interface}\n\nexport interface Workflow {{\n{fields_str}\n}}"

    def visit_WorkflowNodeDef(self, node: WorkflowNodeDef) -> str:
        """Generate TypeScript interface for workflow node."""
        fields = [
            f"  id: string;",
            f"  type: string;",
            f"  label: string;",
            f"  config: Record<string, any>;",
            f"  position: {{ x: number; y: number }};"
        ]
        fields_str = "\n".join(fields)
        return f"export interface WorkflowNode {{\n{fields_str}\n}}"

    def visit_WorkflowEdgeDef(self, node: WorkflowEdgeDef) -> str:
        """Generate TypeScript interface for workflow edge."""
        fields = [
            f"  id: string;",
            f"  source: string;",
            f"  target: string;",
            f"  relation: string;",
            f"  condition?: Record<string, any>;",
            f"  metadata?: Record<string, any>;"
        ]
        fields_str = "\n".join(fields)
        return f"export interface WorkflowEdge {{\n{fields_str}\n}}"

    def visit_PolicyDef(self, node: PolicyDef) -> str:
        """Generate TypeScript interface for policy definition."""
        # Generate enforcement interface first
        enforcement_interface = self.visit_EnforcementDef(node.enforcement)

        # Generate policy interface
        fields = [
            f"  id: string;",
            f"  name: string;",
            f"  version: string;",
            f"  description: string;",
            f"  rego: string;",
            f"  enforcement: Enforcement;",
            f"  data: Record<string, any>;",
            f"  metadata?: Record<string, any>;"
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
