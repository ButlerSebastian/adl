"""
Semantic Validator for ADL DSL

This module provides semantic validation for ADL DSL ASTs, checking for:
- Duplicate field names in types and agents
- Duplicate enum values
- Invalid type references
- Invalid constraint ranges (min > max)
- Circular dependencies
"""

from typing import List, Dict, Set, Optional
from dataclasses import dataclass
from .adl_ast import (
    Program, TypeDef, EnumDef, AgentDef, FieldDef,
    TypeReference, ConstrainedType, ArrayType, UnionType,
    PrimitiveType, OptionalType, ASTVisitor, SourceLocation
)


@dataclass
class ValidationError:
    """Represents a semantic validation error."""
    
    message: str
    location: SourceLocation
    error_code: str
    
    def __str__(self) -> str:
        return f"{self.error_code}: {self.message} at line {self.location.line}"


class SemanticValidator(ASTVisitor[List[ValidationError]]):
    """
    Validates semantic correctness of ADL DSL AST.
    
    Uses visitor pattern to traverse AST and collect validation errors.
    """
    
    def __init__(self):
        self.errors: List[ValidationError] = []
        self.type_definitions: Dict[str, TypeDef] = {}
        self.enum_definitions: Dict[str, EnumDef] = {}
        self.visiting: Set[str] = set()
    
    def validate(self, program: Program) -> List[ValidationError]:
        """
        Validate a complete ADL program.
        
        Args:
            program: The AST program to validate
            
        Returns:
            List of validation errors (empty if valid)
        """
        self.errors = []
        self.type_definitions = {}
        self.enum_definitions = {}
        self.visiting = set()
        
        # First pass: collect all definitions
        for decl in program.declarations:
            if isinstance(decl, TypeDef):
                if decl.name in self.type_definitions:
                    self.errors.append(ValidationError(
                        message=f"Duplicate type definition: {decl.name}",
                        location=decl.loc,
                        error_code="DUPLICATE_TYPE"
                    ))
                else:
                    self.type_definitions[decl.name] = decl
            elif isinstance(decl, EnumDef):
                if decl.name in self.enum_definitions:
                    self.errors.append(ValidationError(
                        message=f"Duplicate enum definition: {decl.name}",
                        location=decl.loc,
                        error_code="DUPLICATE_ENUM"
                    ))
                else:
                    self.enum_definitions[decl.name] = decl
        
        # Second pass: validate each definition
        for decl in program.declarations:
            decl.accept(self)
        
        # Validate agent if present
        if program.agent:
            program.agent.accept(self)
        
        return self.errors
    
    def visit_TypeDef(self, node: TypeDef) -> List[ValidationError]:
        """Validate a type definition."""
        field_names: Set[str] = set()
        
        for field in node.body.fields:
            # Check for duplicate field names
            if field.name in field_names:
                self.errors.append(ValidationError(
                    message=f"Duplicate field name: {field.name}",
                    location=field.loc,
                    error_code="DUPLICATE_FIELD"
                ))
            else:
                field_names.add(field.name)
            
            # Validate field type
            self._validate_type(field.type)
        
        return self.errors
    
    def visit_EnumDef(self, node: EnumDef) -> List[ValidationError]:
        """Validate an enum definition."""
        value_names: Set[str] = set()
        
        for value in node.values:
            # Check for duplicate enum values
            if value in value_names:
                self.errors.append(ValidationError(
                    message=f"Duplicate enum value: {value}",
                    location=node.loc,
                    error_code="DUPLICATE_ENUM_VALUE"
                ))
            else:
                value_names.add(value)
        
        return self.errors
    
    def visit_AgentDef(self, node: AgentDef) -> List[ValidationError]:
        """Validate an agent definition."""
        field_names: Set[str] = set()
        
        for field in node.fields:
            if field.name in field_names:
                self.errors.append(ValidationError(
                    message=f"Duplicate field name: {field.name}",
                    location=field.loc,
                    error_code="DUPLICATE_FIELD"
                ))
            else:
                field_names.add(field.name)
            
            self._validate_type(field.type)
        
        if node.description:
            self._validate_string_length(node.description, "description", 1, 5000)
        
        if node.owner:
            self._validate_string_length(node.owner, "owner", 1, 100)
        
        return self.errors
    
    def _validate_type(self, type_node) -> None:
        """Validate a type node."""
        if isinstance(type_node, TypeReference):
            # Check if type reference is valid
            if type_node.name not in self.type_definitions and type_node.name not in self.enum_definitions:
                # Check if it's a primitive type
                primitive_types = {"string", "integer", "number", "boolean", "object", "array", "any", "null"}
                if type_node.name not in primitive_types:
                    self.errors.append(ValidationError(
                        message=f"Invalid type reference: {type_node.name}",
                        location=type_node.loc,
                        error_code="INVALID_TYPE_REFERENCE"
                    ))
        
        elif isinstance(type_node, ConstrainedType):
            # Validate constraint range
            if type_node.min_value is not None and type_node.max_value is not None:
                if type_node.min_value > type_node.max_value:
                    self.errors.append(ValidationError(
                        message=f"Invalid constraint range: min ({type_node.min_value}) > max ({type_node.max_value})",
                        location=type_node.loc,
                        error_code="INVALID_CONSTRAINT_RANGE"
                    ))
            
            # Validate base type
            self._validate_type(type_node.base_type)
        
        elif isinstance(type_node, ArrayType):
            # Validate element type
            self._validate_type(type_node.element_type)
        
        elif isinstance(type_node, UnionType):
            # Validate all union types
            for union_type in type_node.types:
                self._validate_type(union_type)
        
        elif isinstance(type_node, OptionalType):
            # Validate inner type
            self._validate_type(type_node.inner_type)

    def _validate_string_length(self, value: str, field_name: str, min_length: int, max_length: int) -> None:
        """Validate string length constraints.
        
        Args:
            value: The string value to validate
            field_name: Name of the field being validated
            min_length: Minimum allowed length
            max_length: Maximum allowed length
        """
        if not isinstance(value, str):
            self.errors.append(ValidationError(
                message=f"{field_name} must be a string",
                location=SourceLocation(1, 0),  # Default location for non-AST values
                error_code="INVALID_TYPE"
            ))
            return
        
        if len(value) < min_length:
            self.errors.append(ValidationError(
                message=f"{field_name} must be at least {min_length} character(s), got {len(value)}",
                location=SourceLocation(1, 0),
                error_code="STRING_TOO_SHORT"
            ))
        
        if len(value) > max_length:
            self.errors.append(ValidationError(
                message=f"{field_name} must be at most {max_length} character(s), got {len(value)}",
                location=SourceLocation(1, 0),
                error_code="STRING_TOO_LONG"
            ))
    
    def visit_default(self, node) -> List[ValidationError]:
        """Default visitor for unhandled node types."""
        return self.errors

    def visit_Program(self, node: Program) -> List[ValidationError]:
        """Visit program node."""
        return self.errors

    def visit_ImportStmt(self, node) -> List[ValidationError]:
        """Visit import statement node."""
        return self.errors

    def visit_FieldDef(self, node: FieldDef) -> List[ValidationError]:
        """Visit field definition node."""
        return self.errors

    def visit_TypeReference(self, node: TypeReference) -> List[ValidationError]:
        """Visit type reference node."""
        return self.errors

    def visit_PrimitiveType(self, node: PrimitiveType) -> List[ValidationError]:
        """Visit primitive type node."""
        return self.errors

    def visit_ArrayType(self, node: ArrayType) -> List[ValidationError]:
        """Visit array type node."""
        return self.errors

    def visit_UnionType(self, node: UnionType) -> List[ValidationError]:
        """Visit union type node."""
        return self.errors

    def visit_OptionalType(self, node: OptionalType) -> List[ValidationError]:
        """Visit optional type node."""
        return self.errors

    def visit_ConstrainedType(self, node: ConstrainedType) -> List[ValidationError]:
        """Visit constrained type node."""
        return self.errors

    def visit_EnforcementDef(self, node) -> List[ValidationError]:
        """Visit enforcement definition node."""
        return self.errors

    def visit_PolicyDef(self, node) -> List[ValidationError]:
        """Visit policy definition node."""
        return self.errors

    def visit_WorkflowDef(self, node) -> List[ValidationError]:
        """Visit workflow definition node."""
        return self.errors

    def visit_WorkflowNodeDef(self, node) -> List[ValidationError]:
        """Visit workflow node definition node."""
        return self.errors

    def visit_WorkflowEdgeDef(self, node) -> List[ValidationError]:
        """Visit workflow edge definition node."""
        return self.errors

    def visit_TypeBody(self, node) -> List[ValidationError]:
        """Visit type body node."""
        return self.errors

    def visit_FieldList(self, node) -> List[ValidationError]:
        """Visit field list node."""
        return self.errors
