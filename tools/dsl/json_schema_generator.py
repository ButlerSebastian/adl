"""
JSON Schema Generator for ADL DSL

This module generates JSON Schema from ADL DSL ASTs.
"""

from typing import Dict, Any, List
from .ast import (
    Program, TypeDef, EnumDef, AgentDef, FieldDef,
    TypeReference, ConstrainedType, ArrayType, UnionType,
    PrimitiveType, OptionalType, ASTVisitor
)


class JSONSchemaGenerator(ASTVisitor[Dict[str, Any]]):
    """
    Generates JSON Schema from ADL DSL AST.
    
    Uses visitor pattern to traverse AST and build JSON Schema.
    """

    def __init__(self):
        self.definitions: Dict[str, Any] = {}
        self.enums: Dict[str, Any] = {}

    def generate(self, program: Program) -> Dict[str, Any]:
        """
        Generate JSON Schema from a complete ADL program.

        Args:
            program: The AST program to convert

        Returns:
            JSON Schema as a dictionary
        """
        self.definitions = {}
        self.enums = {}

        schema = {
            "$schema": "https://json-schema.org/draft/2020-12/schema",
            "$id": "https://example.com/schemas/agent-definition.json",
            "title": "Agent Definition",
            "type": "object",
            "properties": {},
            "required": [],
            "additionalProperties": False,
            "$defs": {}
        }

        # Process all declarations
        for decl in program.declarations:
            if isinstance(decl, TypeDef):
                decl.accept(self)
            elif isinstance(decl, EnumDef):
                decl.accept(self)

        # Process agent if present
        if program.agent:
            agent_schema = program.agent.accept(self)
            schema["properties"] = agent_schema["properties"]
            schema["required"] = agent_schema["required"]

        # Add definitions to schema
        schema["$defs"] = {**self.definitions, **self.enums}

        return schema

    def visit_TypeDef(self, node: TypeDef) -> Dict[str, Any]:
        """Generate JSON Schema for a type definition."""
        properties = {}
        required = []

        for field in node.body.fields:
            field_schema = field.type.accept(self)
            properties[field.name] = field_schema

            if field.optional:
                field_schema["nullable"] = True
            else:
                required.append(field.name)

        type_schema = {
            "type": "object",
            "properties": properties,
            "required": required,
            "additionalProperties": False
        }

        self.definitions[node.name] = type_schema
        return type_schema

    def visit_EnumDef(self, node: EnumDef) -> Dict[str, Any]:
        """Generate JSON Schema for an enum definition."""
        enum_schema = {
            "type": "string",
            "enum": node.values
        }

        self.enums[node.name] = enum_schema
        return enum_schema

    def visit_AgentDef(self, node: AgentDef) -> Dict[str, Any]:
        """Generate JSON Schema for an agent definition."""
        properties = {}
        required = []

        for field in node.fields:
            field_schema = field.type.accept(self)
            properties[field.name] = field_schema

            if field.optional:
                field_schema["nullable"] = True
            else:
                required.append(field.name)

        return {
            "properties": properties,
            "required": required
        }

    def visit_PrimitiveType(self, node: PrimitiveType) -> Dict[str, Any]:
        """Generate JSON Schema for a primitive type."""
        type_mapping = {
            "string": {"type": "string"},
            "integer": {"type": "integer"},
            "number": {"type": "number"},
            "boolean": {"type": "boolean"},
            "object": {"type": "object"},
            "array": {"type": "array"},
            "any": {},
            "null": {"type": "null"}
        }

        return type_mapping.get(node.name, {"type": "string"})

    def visit_TypeReference(self, node: TypeReference) -> Dict[str, Any]:
        """Generate JSON Schema for a type reference."""
        return {"$ref": f"#/$defs/{node.name}"}

    def visit_ArrayType(self, node: ArrayType) -> Dict[str, Any]:
        """Generate JSON Schema for an array type."""
        items_schema = node.element_type.accept(self)
        return {
            "type": "array",
            "items": items_schema
        }

    def visit_UnionType(self, node: UnionType) -> Dict[str, Any]:
        """Generate JSON Schema for a union type."""
        any_of = [union_type.accept(self) for union_type in node.types]
        return {"anyOf": any_of}

    def visit_OptionalType(self, node: OptionalType) -> Dict[str, Any]:
        """Generate JSON Schema for an optional type."""
        inner_schema = node.inner_type.accept(self)
        return {
            **inner_schema,
            "nullable": True
        }

    def visit_ConstrainedType(self, node: ConstrainedType) -> Dict[str, Any]:
        """Generate JSON Schema for a constrained type."""
        base_schema = node.base_type.accept(self)

        if node.min_value is not None:
            base_schema["minimum"] = node.min_value

        if node.max_value is not None:
            base_schema["maximum"] = node.max_value

        return base_schema

    def visit_default(self, node) -> Dict[str, Any]:
        """Default visitor for unhandled node types."""
        return {}

    def visit_Program(self, node: Program) -> Dict[str, Any]:
        """Visit program node."""
        return {}

    def visit_ImportStmt(self, node) -> Dict[str, Any]:
        """Visit import statement node."""
        return {}

    def visit_FieldDef(self, node: FieldDef) -> Dict[str, Any]:
        """Visit field definition node."""
        return {}

    def visit_TypeBody(self, node) -> Dict[str, Any]:
        """Visit type body node."""
        return {}

    def visit_FieldList(self, node) -> Dict[str, Any]:
        """Visit field list node."""
        return {}
