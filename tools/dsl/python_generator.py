"""
Python Code Generator for ADL DSL

This module generates Python type definitions from ADL DSL ASTs.
"""

from typing import List, Dict, Any
from .adl_ast import (
    Program, TypeDef, EnumDef, AgentDef, FieldDef,
    TypeReference, ConstrainedType, ArrayType, UnionType,
    PrimitiveType, OptionalType, ASTVisitor,
    WorkflowDef, WorkflowNodeDef, WorkflowEdgeDef,
    PolicyDef, EnforcementDef, PolicyDataDef
)


class PythonGenerator(ASTVisitor[str]):
    """
    Generates Python type definitions from ADL DSL AST.

    Uses visitor pattern to traverse AST and build Python code.
    """

    def __init__(self):
        self.indent_level = 0
        self.lines: List[str] = []

    def generate(self, program: Program) -> str:
        """
        Generate Python code from a complete ADL program.

        Args:
            program: The AST program to convert

        Returns:
            Python code as a string
        """
        self.indent_level = 0
        self.lines = []

        self.lines.append("from typing import List, Optional, Union, TypedDict, Any")
        self.lines.append("")

        # Process all declarations
        for decl in program.declarations:
            if isinstance(decl, EnumDef):
                self.lines.append(decl.accept(self))
                self.lines.append("")
            elif isinstance(decl, TypeDef):
                self.lines.append(decl.accept(self))
                self.lines.append("")
            elif isinstance(decl, WorkflowDef):
                self.lines.append(decl.accept(self))
                self.lines.append("")
            elif isinstance(decl, PolicyDef):
                self.lines.append(decl.accept(self))
                self.lines.append("")

        # Process agent if present
        if program.agent:
            self.lines.append(program.agent.accept(self))
            self.lines.append("")

        return "\n".join(self.lines).strip()

    def visit_EnumDef(self, node: EnumDef) -> str:
        """Generate Python enum from an enum definition."""
        values = "\n    ".join([f'"{value}",' for value in node.values])
        return f"class {node.name}(str):\n    {values}"

    def visit_TypeDef(self, node: TypeDef) -> str:
        """Generate Python TypedDict from a type definition."""
        if not node.body:
            return f"class {node.name}(TypedDict):"
        
        fields = []
        for field in node.body.fields:
            field_type = field.type.accept(self)
            optional = "NotRequired" if field.optional else "Required"
            fields.append(f'    {field.name}: {optional}[{field_type}]')

        fields_str = "\n".join(fields)
        return f"class {node.name}(TypedDict):\n{fields_str}"

    def visit_AgentDef(self, node: AgentDef) -> str:
        """Generate Python TypedDict from an agent definition.

        Note: The agent_id field is required for unique identification.
        Use hierarchical ID format (e.g., "namespace.agent_name") for better organization.

        DEPRECATED: The 'id' field is deprecated in favor of 'agent_id'.
        """
        fields = [
            '    agent_id: Required[str]',
            '    id: NotRequired[str]',  # DEPRECATED: Use agent_id instead
            '    name: Required[str]',
            '    description: Required[str]',
            '    role: Required[str]',
            '    llm: Required[str]',
            '    llm_settings: Required[Dict[str, Any]]',
            '    tools: Required[List[Dict[str, Any]]]',
            '    rag: Required[List[Dict[str, Any]]]',
            '    memory: Required[Dict[str, Any]]',
            '    execution_constraints: Required[Dict[str, Any]]',
            '    events: Required[Dict[str, Any]]',
            '    lifecycle: Required[str]',
            '    version: Required[int]',
            '    version_string: Required[str]',
            '    owner: Required[str]',
            '    metadata: Required[Dict[str, Any]]'
        ]
        fields_str = "\n".join(fields)
        return f"class {node.name}(TypedDict):\n{fields_str}"

    def visit_WorkflowDef(self, node: WorkflowDef) -> str:
        """Generate Python TypedDict for a workflow definition.

        Note: The workflow_id field is required for unique identification.
        Use hierarchical ID format (e.g., "namespace.workflow_name") for better organization.

        DEPRECATED: The 'id' field is deprecated in favor of 'workflow_id'.
        """
        fields = [
            '    workflow_id: Required[str]',
            '    id: NotRequired[str]',  # DEPRECATED: Use workflow_id instead
            '    name: Required[str]',
            '    version: Required[str]',
            '    description: Required[str]',
            '    nodes: Required[Dict[str, WorkflowNodeDef]]',
            '    edges: Required[List[WorkflowEdgeDef]]',
            '    metadata: Required[Dict[str, Any]]'
        ]
        fields_str = "\n".join(fields)
        # Sanitize class name to be valid Python identifier
        class_name = node.name.replace(" ", "_").replace("-", "_")
        return f"class {class_name}(TypedDict):\n{fields_str}"

    def visit_WorkflowNodeDef(self, node: WorkflowNodeDef) -> str:
        """Generate Python TypedDict for a workflow node definition.

        Note: The node key in the nodes dictionary serves as the node ID.
        Use hierarchical ID format (e.g., "namespace.node_name") for better organization.

        DEPRECATED: The 'id' field is deprecated as node keys serve as IDs.
        """
        fields = [
            '    type: Required[str]',
            '    label: Required[str]',
            '    config: Required[Dict[str, Any]]',
            '    position: Required[Dict[str, int]]',
            '    id: NotRequired[str]'  # DEPRECATED: Use node key instead
        ]
        fields_str = "\n".join(fields)
        # Use id as class name (nodes don't have a name field)
        class_name = node.id.replace(" ", "_").replace("-", "_")
        return f"class {class_name}(TypedDict):\n{fields_str}"

    def visit_WorkflowEdgeDef(self, node: WorkflowEdgeDef) -> str:
        """Generate Python TypedDict for a workflow edge definition.

        Note: The edge_id field is required for unique identification.
        Use hierarchical ID format (e.g., "namespace.edge_name") for better organization.

        DEPRECATED: The 'id' field is deprecated in favor of 'edge_id'.
        """
        fields = [
            '    edge_id: Required[str]',
            '    id: NotRequired[str]',  # DEPRECATED: Use edge_id instead
            '    source: Required[str]',
            '    target: Required[str]',
            '    relation: Required[str]',
            '    condition: NotRequired[Dict[str, Any]]',
            '    metadata: NotRequired[Dict[str, Any]]'
        ]
        fields_str = "\n".join(fields)
        # Use id as class name (edges don't have a name field)
        class_name = node.id.replace(" ", "_").replace("-", "_")
        return f"class {class_name}(TypedDict):\n{fields_str}"

    def visit_PolicyDef(self, node: PolicyDef) -> str:
        """Generate Python TypedDict for a policy definition.

        Note: The policy_id field is required for unique identification.
        Use hierarchical ID format (e.g., "namespace.policy_name") for better organization.

        DEPRECATED: The 'id' field is deprecated in favor of 'policy_id'.
        """
        fields = [
            '    policy_id: Required[str]',
            '    id: NotRequired[str]',  # DEPRECATED: Use policy_id instead
            '    name: Required[str]',
            '    version: Required[str]',
            '    description: Required[str]',
            '    rego: Required[str]',
            '    enforcement: Required[EnforcementDef]',
            '    data: Required[Dict[str, Any]]',
            '    metadata: Required[Dict[str, Any]]'
        ]
        fields_str = "\n".join(fields)
        return f"class {node.name}(TypedDict):\n{fields_str}"

    def visit_EnforcementDef(self, node: EnforcementDef) -> str:
        """Generate Python TypedDict for an enforcement definition."""
        fields = [
            '    mode: Required[str]',
            '    action: Required[str]',
            '    audit_log: Required[bool]'
        ]
        fields_str = "\n".join(fields)
        # Use enforcement as class name
        class_name = "Enforcement"
        return f"class {class_name}(TypedDict):\n{fields_str}"

    def visit_PolicyDataDef(self, node: PolicyDataDef) -> str:
        """Generate Python TypedDict for a policy data definition."""
        fields = [
            '    roles: Required[Dict[str, List[str]]]',
            '    permissions: Required[Dict[str, Any]]'
        ]
        fields_str = "\n".join(fields)
        # Use policy_data as class name
        class_name = "PolicyData"
        return f"class {class_name}(TypedDict):\n{fields_str}"

    def visit_PrimitiveType(self, node: PrimitiveType) -> str:
        """Generate Python type for a primitive type."""
        type_mapping = {
            "string": "str",
            "integer": "int",
            "number": "float",
            "boolean": "bool",
            "object": "Dict[str, Any]",
            "array": "List[Any]",
            "any": "Any",
            "null": "None"
        }
        return type_mapping.get(node.name, "str")

    def visit_TypeReference(self, node: TypeReference) -> str:
        """Generate Python type for a type reference."""
        return node.name

    def visit_ArrayType(self, node: ArrayType) -> str:
        """Generate Python type for an array type."""
        element_type = node.element_type.accept(self)
        return f"List[{element_type}]"

    def visit_UnionType(self, node: UnionType) -> str:
        """Generate Python type for a union type."""
        types = ", ".join([union_type.accept(self) for union_type in node.types])
        return f"Union[{types}]"

    def visit_OptionalType(self, node: OptionalType) -> str:
        """Generate Python type for an optional type."""
        inner_type = node.inner_type.accept(self)
        return f"Optional[{inner_type}]"

    def visit_ConstrainedType(self, node: ConstrainedType) -> str:
        """Generate Python type for a constrained type."""
        base_type = node.base_type.accept(self)
        return base_type

    def visit_default(self, node) -> str:
        """Default visitor for unhandled node types."""
        return "Any"

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
