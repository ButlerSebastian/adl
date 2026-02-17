"""
Python Code Generator for ADL DSL

This module generates Python type definitions from ADL DSL ASTs.
"""

from typing import List, Dict, Any, Optional, Tuple
from .adl_ast import (
    Program, TypeDef, EnumDef, AgentDef, FieldDef,
    TypeReference, ConstrainedType, ArrayType, UnionType,
    PrimitiveType, OptionalType, ASTVisitor,
    WorkflowDef, WorkflowNodeDef, WorkflowEdgeDef,
    PolicyDef, EnforcementDef, PolicyDataDef
)
import ast
import subprocess
import tempfile
import os


class PythonGenerator(ASTVisitor[str]):
    """
    Generates Python type definitions from ADL DSL AST.

    Uses visitor pattern to traverse AST and build Python code.
    """

    def __init__(self):
        self.indent_level = 0
        self.lines: List[str] = []

    def validate_python_syntax(self, code: str) -> Tuple[bool, Optional[str]]:
        """
        Validate Python syntax using ast.parse().

        Args:
            code: Python code to validate

        Returns:
            Tuple of (is_valid, error_message)
        """
        try:
            ast.parse(code)
            return True, None
        except SyntaxError as e:
            return False, f"Syntax error: {e.msg} at line {e.lineno}, column {e.offset}"

    def validate_python_types(self, code: str) -> List[str]:
        """
        Validate Python types using mypy if available, otherwise skip.

        Args:
            code: Python code to validate

        Returns:
            List of type checking errors (empty if no errors)
        """
        errors = []

        # Try to use mypy for type checking
        try:
            # Create a temporary file with the code
            with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
                f.write(code)
                temp_file = f.name

            try:
                # Run mypy on the temporary file
                result = subprocess.run(
                    ['mypy', '--no-error-summary', '--show-error-codes', temp_file],
                    capture_output=True,
                    text=True,
                    timeout=10
                )

                if result.returncode != 0 and result.stdout:
                    # Parse mypy output
                    for line in result.stdout.split('\n'):
                        if line.strip():
                            errors.append(line.strip())

            except subprocess.TimeoutExpired:
                errors.append("Type checking timed out (10s)")
            except FileNotFoundError:
                # mypy not available, skip type checking
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
        Validate generated Python code for syntax and types.

        Args:
            code: Python code to validate

        Returns:
            Tuple of (is_valid, list_of_errors)
        """
        errors = []

        # Validate syntax
        is_valid, syntax_error = self.validate_python_syntax(code)
        if not is_valid:
            errors.append(syntax_error)

        # Validate types
        type_errors = self.validate_python_types(code)
        errors.extend(type_errors)

        return len(errors) == 0, errors

    def generate(self, program: Program) -> str:
        """
        Generate Python code from a complete ADL program.

        Args:
            program: The AST program to convert

        Returns:
            Python code as a string

        Raises:
            ValueError: If generated code fails validation
        """
        self.indent_level = 0
        self.lines = []

        self.lines.append("from typing import List, Optional, Union, TypedDict, Any")
        self.lines.append("")

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

        code = "\n".join(self.lines).strip()

        # Validate generated code
        is_valid, errors = self.validate_generated_code(code)
        if not is_valid:
            error_msg = "Generated code validation failed:\n" + "\n".join(f"  - {err}" for err in errors)
            raise ValueError(error_msg)

        return code

    def visit_EnumDef(self, node: EnumDef) -> str:
        """Generate Python enum from an enum definition.

        Args:
            node: The enum definition node to generate code for

        Returns:
            Python code defining the enum as a string subclass of str

        Example:
            >>> node = EnumDef("Color", ["red", "green", "blue"])
            >>> generator.visit_EnumDef(node)
            'class Color(str):\\n    "red",\\n    "green",\\n    "blue",\\n'
        """
        values = "\\\\n    ".join([f'"{value}",' for value in node.values])
        return f"class {node.name}(str):\\\\n    {values}\\\\n"

    def visit_TypeDef(self, node: TypeDef) -> str:
        """Generate Python TypedDict from a type definition.

        Args:
            node: The type definition node to generate code for

        Returns:
            Python code defining the TypedDict class

        Example:
            >>> node = TypeDef("User", [FieldDef("name", TypeReference("string"), False)])
            >>> generator.visit_TypeDef(node)
            'class User(TypedDict):\\n    name: Required[str]\\n'
        """
        if not node.body:
            return f"class {node.name}(TypedDict):\\\\n"

        fields = []
        for field in node.body.fields:
            field_type = field.type.accept(self)
            optional = "NotRequired" if field.optional else "Required"
            fields.append(f'    {field.name}: {optional}[{field_type}]')

        fields_str = "\\\\n".join(fields)
        return f"class {node.name}(TypedDict):\\\\n{fields_str}\\\\n"

    def visit_AgentDef(self, node: AgentDef) -> str:
        """Generate Python TypedDict from an agent definition.

        Note: The agent_id field is required for unique identification.
        Use hierarchical ID format (e.g., "namespace.agent_name") for better organization.

        DEPRECATED: The 'id' field is deprecated in favor of 'agent_id'.

        Args:
            node: The agent definition node to generate code for

        Returns:
            Python code defining the agent TypedDict class

        Example:
            >>> node = AgentDef("MyAgent", [FieldDef("agent_id", TypeReference("string"), False)])
            >>> generator.visit_AgentDef(node)
            'class MyAgent(TypedDict):\\n    agent_id: Required[str]\\n    id: NotRequired[str]\\n...'
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
        fields_str = "\\\\n".join(fields)
        return f"class {node.name}(TypedDict):\\\\n{fields_str}\\\\n"

    def visit_WorkflowDef(self, node: WorkflowDef) -> str:
        """Generate Python TypedDict for a workflow definition.

        Note: The workflow_id field is required for unique identification.
        Use hierarchical ID format (e.g., "namespace.workflow_name") for better organization.

        DEPRECATED: The 'id' field is deprecated in favor of 'workflow_id'.

        Args:
            node: The workflow definition node to generate code for

        Returns:
            Python code defining the workflow TypedDict class

        Example:
            >>> node = WorkflowDef("MyWorkflow", [WorkflowNodeDef("input", "input")])
            >>> generator.visit_WorkflowDef(node)
            'class My_Workflow(TypedDict):\\n    workflow_id: Required[str]\\n...'
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
        fields_str = "\\\\n".join(fields)
        # Sanitize class name to be valid Python identifier
        class_name = node.name.replace(" ", "_").replace("-", "_")
        return f"class {class_name}(TypedDict):\\\\n{fields_str}\\\\n"

    def visit_WorkflowNodeDef(self, node: WorkflowNodeDef) -> str:
        """Generate Python TypedDict for a workflow node definition.

        Note: The node key in the nodes dictionary serves as the node ID.
        Use hierarchical ID format (e.g., "namespace.node_name") for better organization.

        DEPRECATED: The 'id' field is deprecated as node keys serve as IDs.

        Args:
            node: The workflow node definition node to generate code for

        Returns:
            Python code defining the workflow node TypedDict class

        Example:
            >>> node = WorkflowNodeDef("input-node", "input")
            >>> generator.visit_WorkflowNodeDef(node)
            'class input_node(TypedDict):\\n    type: Required[str]\\n...'
        """
        fields = [
            '    type: Required[str]',
            '    label: Required[str]',
            '    config: Required[Dict[str, Any]]',
            '    position: Required[Dict[str, int]]',
            '    id: NotRequired[str]'  # DEPRECATED: Use node key instead
        ]
        fields_str = "\\\\n".join(fields)
        # Use id as class name (nodes don't have a name field)
        class_name = node.id.replace(" ", "_").replace("-", "_")
        return f"class {class_name}(TypedDict):\\\\n{fields_str}\\\\n"

    def visit_WorkflowEdgeDef(self, node: WorkflowEdgeDef) -> str:
        """Generate Python TypedDict for a workflow edge definition.

        Note: The edge_id field is required for unique identification.
        Use hierarchical ID format (e.g., "namespace.edge_name") for better organization.

        DEPRECATED: The 'id' field is deprecated in favor of 'edge_id'.

        Args:
            node: The workflow edge definition node to generate code for

        Returns:
            Python code defining the workflow edge TypedDict class

        Example:
            >>> node = WorkflowEdgeDef("edge-1", "input-node", "process-node", "next")
            >>> generator.visit_WorkflowEdgeDef(node)
            'class edge_1(TypedDict):\\n    edge_id: Required[str]\\n...'
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
        fields_str = "\\\\n".join(fields)
        # Use id as class name (edges don't have a name field)
        class_name = node.id.replace(" ", "_").replace("-", "_")
        return f"class {class_name}(TypedDict):\\\\n{fields_str}\\\\n"

    def visit_PolicyDef(self, node: PolicyDef) -> str:
        """Generate Python TypedDict for a policy definition.

        Note: The policy_id field is required for unique identification.
        Use hierarchical ID format (e.g., "namespace.policy_name") for better organization.

        DEPRECATED: The 'id' field is deprecated in favor of 'policy_id'.

        Args:
            node: The policy definition node to generate code for

        Returns:
            Python code defining the policy TypedDict class

        Example:
            >>> node = PolicyDef("MyPolicy", EnforcementDef("strict", "deny", True))
            >>> generator.visit_PolicyDef(node)
            'class MyPolicy(TypedDict):\\n    policy_id: Required[str]\\n...'
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
        fields_str = "\\\\n".join(fields)
        return f"class {node.name}(TypedDict):\\\\n{fields_str}\\\\n"

    def visit_EnforcementDef(self, node: EnforcementDef) -> str:
        """Generate Python TypedDict for an enforcement definition.

        Args:
            node: The enforcement definition node to generate code for

        Returns:
            Python code defining the enforcement TypedDict class

        Example:
            >>> node = EnforcementDef("strict", "deny", True)
            >>> generator.visit_EnforcementDef(node)
            'class Enforcement(TypedDict):\\n    mode: Required[str]\\n...'
        """
        fields = [
            '    mode: Required[str]',
            '    action: Required[str]',
            '    audit_log: Required[bool]'
        ]
        fields_str = "\\\\n".join(fields)
        # Use enforcement as class name
        class_name = "Enforcement"
        return f"class {class_name}(TypedDict):\\\\n{fields_str}\\\\n"

    def visit_PolicyDataDef(self, node: PolicyDataDef) -> str:
        """Generate Python TypedDict for a policy data definition.

        Args:
            node: The policy data definition node to generate code for

        Returns:
            Python code defining the policy data TypedDict class

        Example:
            >>> node = PolicyDataDef({"roles": {"admin": ["read", "write"]}})
            >>> generator.visit_PolicyDataDef(node)
            'class PolicyData(TypedDict):\\n    roles: Required[Dict[str, List[str]]]\\n...'
        """
        fields = [
            '    roles: Required[Dict[str, List[str]]]',
            '    permissions: Required[Dict[str, Any]]'
        ]
        fields_str = "\\\\n".join(fields)
        # Use policy_data as class name
        class_name = "PolicyData"
        return f"class {class_name}(TypedDict):\\\\n{fields_str}\\\\n"

    def visit_PrimitiveType(self, node: PrimitiveType) -> str:
        """Generate Python type for a primitive type.

        Args:
            node: The primitive type node to generate code for

        Returns:
            Python type string for the primitive type

        Example:
            >>> node = PrimitiveType("string")
            >>> generator.visit_PrimitiveType(node)
            'str'
        """
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
        """Generate Python type for a type reference.

        Args:
            node: The type reference node to generate code for

        Returns:
            Python type string for the type reference

        Example:
            >>> node = TypeReference("User")
            >>> generator.visit_TypeReference(node)
            'User'
        """
        return node.name

    def visit_ArrayType(self, node: ArrayType) -> str:
        """Generate Python type for an array type.

        Args:
            node: The array type node to generate code for

        Returns:
            Python type string for the array type

        Example:
            >>> node = ArrayType(PrimitiveType("string"))
            >>> generator.visit_ArrayType(node)
            'List[str]'
        """
        element_type = node.element_type.accept(self)
        return f"List[{element_type}]"

    def visit_UnionType(self, node: UnionType) -> str:
        """Generate Python type for a union type.

        Args:
            node: The union type node to generate code for

        Returns:
            Python type string for the union type

        Example:
            >>> node = UnionType([PrimitiveType("string"), PrimitiveType("number")])
            >>> generator.visit_UnionType(node)
            'Union[str, number]'
        """
        types = ", ".join([union_type.accept(self) for union_type in node.types])
        return f"Union[{types}]"

    def visit_OptionalType(self, node: OptionalType) -> str:
        """Generate Python type for an optional type.

        Args:
            node: The optional type node to generate code for

        Returns:
            Python type string for the optional type

        Example:
            >>> node = OptionalType(PrimitiveType("string"))
            >>> generator.visit_OptionalType(node)
            'Optional[str]'
        """
        inner_type = node.inner_type.accept(self)
        return f"Optional[{inner_type}]"

    def visit_ConstrainedType(self, node: ConstrainedType) -> str:
        """Generate Python type for a constrained type.

        Args:
            node: The constrained type node to generate code for

        Returns:
            Python type string for the constrained type

        Example:
            >>> node = ConstrainedType(PrimitiveType("string"))
            >>> generator.visit_ConstrainedType(node)
            'str'
        """
        base_type = node.base_type.accept(self)
        return base_type

    def visit_default(self, node) -> str:
        """Default visitor for unhandled node types.

        Args:
            node: The unhandled node type

        Returns:
            Python type string for unhandled types

        Example:
            >>> generator.visit_default(AnyNode())
            'Any'
        """
        return "Any"

    def visit_Program(self, node: Program) -> str:
        """Visit program node.

        Args:
            node: The program node to visit

        Returns:
            Empty string (program is handled in generate method)
        """
        return ""

    def visit_ImportStmt(self, node) -> str:
        """Visit import statement node.

        Args:
            node: The import statement node to visit

        Returns:
            Empty string (imports are handled in generate method)
        """
        return ""

    def visit_FieldDef(self, node: FieldDef) -> str:
        """Visit field definition node.

        Args:
            node: The field definition node to visit

        Returns:
            Empty string (field definitions are handled in visit_TypeDef)
        """
        return ""

    def visit_TypeBody(self, node) -> str:
        """Visit type body node.

        Args:
            node: The type body node to visit

        Returns:
            Empty string (type bodies are handled in visit_TypeDef)
        """
        return ""

    def visit_FieldList(self, node) -> str:
        """Visit field list node.

        Args:
            node: The field list node to visit

        Returns:
            Empty string (field lists are handled in visit_TypeDef)
        """
        return ""
