"""
Semantic Validator for ADL DSL

This module provides semantic validation for ADL DSL ASTs, checking for:
- Duplicate field names in types and agents
- Duplicate enum values
- Invalid type references
- Invalid constraint ranges (min > max)
- Circular dependencies
"""

from typing import List, Dict, Set, Optional, Literal
from dataclasses import dataclass
from enum import Enum
from functools import lru_cache
import re
from datetime import datetime
from .adl_ast import (
    Program, TypeDef, EnumDef, AgentDef, FieldDef,
    TypeReference, ConstrainedType, ArrayType, UnionType,
    PrimitiveType, OptionalType, ASTVisitor, SourceLocation,
    WorkflowDef, WorkflowNodeDef, WorkflowEdgeDef, PolicyDef, EnforcementDef
)


class ErrorCategory(Enum):
    """Categories for validation errors."""
    SYNTAX = "syntax"
    SEMANTIC = "semantic"
    VALIDATION = "validation"
    TYPE = "type"


@dataclass
class ValidationError:
    """Represents a semantic validation error."""

    message: str
    location: SourceLocation
    error_code: str
    category: ErrorCategory = ErrorCategory.SEMANTIC

    def __str__(self) -> str:
        return f"{self.error_code}: {self.message} at line {self.location.line}"


@dataclass
class ValidationErrorSummary:
    """Summary of validation errors grouped by category."""

    total_errors: int
    syntax_errors: List[ValidationError]
    semantic_errors: List[ValidationError]
    validation_errors: List[ValidationError]
    type_errors: List[ValidationError]

    def get_summary(self) -> str:
        """Get human-readable summary."""
        return f"""
Validation Errors: {self.total_errors}
- Syntax: {len(self.syntax_errors)}
- Semantic: {len(self.semantic_errors)}
- Validation: {len(self.validation_errors)}
- Type: {len(self.type_errors)}
"""

    def get_errors_by_category(self) -> Dict[ErrorCategory, List[ValidationError]]:
        """Get errors grouped by category."""
        return {
            ErrorCategory.SYNTAX: self.syntax_errors,
            ErrorCategory.SEMANTIC: self.semantic_errors,
            ErrorCategory.VALIDATION: self.validation_errors,
            ErrorCategory.TYPE: self.type_errors,
        }

    def has_errors(self) -> bool:
        """Check if there are any errors."""
        return self.total_errors > 0

    def get_most_common_errors(self, n: int = 5) -> List[tuple[str, int]]:
        """Get most common error messages with counts."""
        error_counts = {}
        for error in self.semantic_errors + self.validation_errors:
            error_counts[error.message] = error_counts.get(error.message, 0) + 1

        return sorted(error_counts.items(), key=lambda x: x[1], reverse=True)[:n]


class SemanticValidator(ASTVisitor[ValidationErrorSummary]):
    """
    Validates semantic correctness of ADL DSL AST.
    
    Uses visitor pattern to traverse AST and collect validation errors.
    """
    
    MAX_CRITICAL_ERRORS = 10
    
    def __init__(self):
        self.errors: List[ValidationError] = []
        self.type_definitions: Dict[str, TypeDef] = {}
        self.enum_definitions: Dict[str, EnumDef] = {}
        self.visiting: Set[str] = set()
        self._cache: Dict[str, ValidationErrorSummary] = {}
        self._cache_key: Optional[str] = None
    
    def validate(self, program: Program) -> ValidationErrorSummary:
        """
        Validate a complete ADL program and return grouped errors.

        Args:
            program: The AST program to validate

        Returns:
            ValidationErrorSummary with all errors grouped by category
        """
        self.errors = []
        self.type_definitions = {}
        self.enum_definitions = {}
        self.visiting = set()

        cache_key = self._generate_cache_key(program)
        if cache_key in self._cache:
            return self._cache[cache_key]

        critical_errors = 0

        # First pass: collect all definitions
        for decl in program.declarations:
            if isinstance(decl, TypeDef):
                if decl.name in self.type_definitions:
                    self.errors.append(ValidationError(
                        message=f"Duplicate type definition: {decl.name}",
                        location=decl.loc,
                        error_code="DUPLICATE_TYPE",
                        category=ErrorCategory.SEMANTIC
                    ))
                else:
                    self.type_definitions[decl.name] = decl
            elif isinstance(decl, EnumDef):
                if decl.name in self.enum_definitions:
                    self.errors.append(ValidationError(
                        message=f"Duplicate enum definition: {decl.name}",
                        location=decl.loc,
                        error_code="DUPLICATE_ENUM",
                        category=ErrorCategory.SEMANTIC
                    ))
                else:
                    self.enum_definitions[decl.name] = decl

        # Second pass: validate each definition
        for decl in program.declarations:
            decl.accept(self)

        # Validate agent if present
        if program.agent:
            program.agent.accept(self)

        if len(self.errors) >= self.MAX_CRITICAL_ERRORS:
            self.errors.append(ValidationError(
                message=f"Validation terminated early: {self.MAX_CRITICAL_ERRORS} critical errors found",
                location=SourceLocation(1, 0, 1, 0),
                error_code="VALIDATION_TERMINATED",
                category=ErrorCategory.VALIDATION
            ))

        self._cache[cache_key] = self._create_error_summary()

        return self._create_error_summary()
    
    def visit_TypeDef(self, node: TypeDef) -> ValidationErrorSummary:
        """Validate a type definition."""
        field_names: Set[str] = set()

        if node.body is None:
            return self._create_error_summary()

        for field in node.body.fields:
            # Check for duplicate field names
            if field.name in field_names:
                self.errors.append(ValidationError(
                    message=f"Duplicate field name: {field.name}",
                    location=field.loc,
                    error_code="DUPLICATE_FIELD",
                    category=ErrorCategory.SEMANTIC
                ))
            else:
                field_names.add(field.name)

            # Validate field type
            self._validate_type(field.type)

        return self._create_error_summary()
    
    def visit_EnumDef(self, node: EnumDef) -> ValidationErrorSummary:
        """Validate an enum definition."""
        value_names: Set[str] = set()

        for value in node.values:
            # Check for duplicate enum values
            if value in value_names:
                self.errors.append(ValidationError(
                    message=f"Duplicate enum value: {value}",
                    location=node.loc,
                    error_code="DUPLICATE_ENUM_VALUE",
                    category=ErrorCategory.SEMANTIC
                ))
            else:
                value_names.add(value)

            # Validate enum value is a valid string
            if not isinstance(value, str):
                self.errors.append(ValidationError(
                    message=f"Enum value must be a string, got {type(value).__name__}",
                    location=node.loc,
                    error_code="INVALID_ENUM_VALUE_TYPE",
                    category=ErrorCategory.VALIDATION
                ))

            # Validate enum value follows naming convention (is a valid identifier)
            if not value.isidentifier():
                self.errors.append(ValidationError(
                    message=f"Enum value '{value}' is not a valid identifier",
                    location=node.loc,
                    error_code="INVALID_ENUM_VALUE_NAME",
                    category=ErrorCategory.VALIDATION
                ))

        return self._create_error_summary()
    
    def visit_AgentDef(self, node: AgentDef) -> ValidationErrorSummary:
        """Validate an agent definition."""
        field_names: Set[str] = set()

        for field in node.fields:
            if field.name in field_names:
                self.errors.append(ValidationError(
                    message=f"Duplicate field name: {field.name}",
                    location=field.loc,
                    error_code="DUPLICATE_FIELD",
                    category=ErrorCategory.SEMANTIC
                ))
            else:
                field_names.add(field.name)

            self._validate_type(field.type)

        if node.description:
            self._validate_string_length(node.description, "description", 1, 5000)

        if node.owner:
            self._validate_string_length(node.owner, "owner", 1, 100)

        return self._create_error_summary()
    
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
                        error_code="INVALID_TYPE_REFERENCE",
                        category=ErrorCategory.TYPE
                    ))
        
        elif isinstance(type_node, ConstrainedType):
            # Validate constraint range
            if type_node.min_value is not None and type_node.max_value is not None:
                if type_node.min_value > type_node.max_value:
                    self.errors.append(ValidationError(
                        message=f"Invalid constraint range: min ({type_node.min_value}) > max ({type_node.max_value})",
                        location=type_node.loc,
                        error_code="INVALID_CONSTRAINT_RANGE",
                        category=ErrorCategory.TYPE
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
                location=SourceLocation(1, 0, 1, 0),  # Default location for non-AST values
                error_code="INVALID_TYPE",
                category=ErrorCategory.TYPE
            ))
            return
        
        if len(value) < min_length:
            self.errors.append(ValidationError(
                message=f"{field_name} must be at least {min_length} character(s), got {len(value)}",
                location=SourceLocation(1, 0, 1, 0),
                error_code="STRING_TOO_SHORT",
                category=ErrorCategory.TYPE
            ))
        
        if len(value) > max_length:
            self.errors.append(ValidationError(
                message=f"{field_name} must be at most {max_length} character(s), got {len(value)}",
                location=SourceLocation(1, 0, 1, 0),
                error_code="STRING_TOO_LONG",
                category=ErrorCategory.TYPE
            ))
    
    def visit_default(self, node) -> ValidationErrorSummary:
        """Default visitor for unhandled node types."""
        return self._create_error_summary()

    def visit_Program(self, node: Program) -> ValidationErrorSummary:
        """Visit program node."""
        return self._create_error_summary()

    def visit_ImportStmt(self, node) -> ValidationErrorSummary:
        """Visit import statement node."""
        return self._create_error_summary()

    def visit_FieldDef(self, node: FieldDef) -> ValidationErrorSummary:
        """Visit field definition node."""
        return self._create_error_summary()

    def visit_TypeReference(self, node: TypeReference) -> ValidationErrorSummary:
        """Visit type reference node."""
        return self._create_error_summary()

    def visit_PrimitiveType(self, node: PrimitiveType) -> ValidationErrorSummary:
        """Visit primitive type node."""
        return self._create_error_summary()

    def visit_ArrayType(self, node: ArrayType) -> ValidationErrorSummary:
        """Visit array type node."""
        return self._create_error_summary()

    def visit_UnionType(self, node: UnionType) -> ValidationErrorSummary:
        """Visit union type node."""
        return self._create_error_summary()

    def visit_OptionalType(self, node: OptionalType) -> ValidationErrorSummary:
        """Visit optional type node."""
        return self._create_error_summary()

    def visit_ConstrainedType(self, node: ConstrainedType) -> ValidationErrorSummary:
        """Visit constrained type node."""
        # Validate numeric range constraints
        if node.min_value is not None and node.max_value is not None:
            if node.min_value > node.max_value:
                self.errors.append(ValidationError(
                    message=f"Invalid range: minimum ({node.min_value}) > maximum ({node.max_value})",
                    location=node.loc,
                    error_code="INVALID_RANGE",
                    category=ErrorCategory.VALIDATION
                ))

        # Validate date/time format constraints for string types
        if isinstance(node.base_type, PrimitiveType) and node.base_type.name == "string":
            # Check if min_value is a valid date/time string
            if node.min_value is not None:
                if not self._validate_date_time(str(node.min_value), "min_value", node.loc):
                    pass

            # Check if max_value is a valid date/time string
            if node.max_value is not None:
                if not self._validate_date_time(str(node.max_value), "max_value", node.loc):
                    pass

            # Check if pattern is a valid date/time format
            if node.pattern is not None:
                if not self._validate_date_time_pattern(node.pattern, "pattern", node.loc):
                    pass

        return self._create_error_summary()

    def _validate_date_time(self, value: str, field_name: str, location: SourceLocation) -> bool:
        """Validate that a string is a valid date/time format."""
        date_formats = [
            "%Y-%m-%d",
            "%Y/%m/%d",
            "%m/%d/%Y",
            "%d/%m/%Y",
            "%Y%m%d",
            "%Y-%m-%d %H:%M:%S",
            "%Y-%m-%d %H:%M",
            "%Y/%m/%d %H:%M:%S",
            "%H:%M:%S",
            "%H:%M",
        ]

        for fmt in date_formats:
            try:
                datetime.strptime(value, fmt)
                return True
            except ValueError:
                continue

        self.errors.append(ValidationError(
            message=f"Invalid {field_name} for date/time constraint: '{value}'. Must be a valid date/time format (YYYY-MM-DD, YYYY/MM/DD, YYYY-MM-DD HH:MM:SS, etc.)",
            location=location,
            error_code="INVALID_DATE_TIME_FORMAT",
            category=ErrorCategory.VALIDATION
        ))
        return False

    def _validate_date_time_pattern(self, pattern: str, field_name: str, location: SourceLocation) -> bool:
        """Validate that a pattern string is a valid date/time format pattern."""
        valid_specifiers = {
            "%Y", "%y", "%m", "%d", "%H", "%I", "%M", "%S", "%f",
            "%a", "%A", "%b", "%B", "%p", "%z", "%Z"
        }

        for specifier in pattern:
            if specifier in valid_specifiers:
                continue
            if specifier == "\\":
                continue

        if not pattern or not any(spec in pattern for spec in valid_specifiers):
            self.errors.append(ValidationError(
                message=f"Invalid {field_name} for date/time pattern: '{pattern}'. Must contain valid date/time format specifiers (e.g., %Y-%m-%d, %H:%M:%S)",
                location=location,
                error_code="INVALID_DATE_TIME_PATTERN",
                category=ErrorCategory.VALIDATION
            ))
            return False

        return True

    def visit_EnforcementDef(self, node: EnforcementDef) -> ValidationErrorSummary:
        """Validate enforcement definition."""
        # Validate enforcement mode
        valid_modes = {"strict", "moderate", "lenient"}
        if node.mode not in valid_modes:
            self.errors.append(ValidationError(
                message=f"Invalid enforcement mode: {node.mode}. Must be one of {valid_modes}",
                location=node.loc,
                error_code="INVALID_ENFORCEMENT_MODE",
                category=ErrorCategory.VALIDATION
            ))

        # Validate enforcement action
        valid_actions = {"deny", "warn", "log", "allow"}
        if node.action not in valid_actions:
            self.errors.append(ValidationError(
                message=f"Invalid enforcement action: {node.action}. Must be one of {valid_actions}",
                location=node.loc,
                error_code="INVALID_ENFORCEMENT_ACTION",
                category=ErrorCategory.VALIDATION
            ))

        return self._create_error_summary()

    def visit_PolicyDef(self, node: PolicyDef) -> ValidationErrorSummary:
        """Validate policy definition."""
        policy_ids: Set[str] = set()

        # Check for duplicate policy IDs
        if node.id in policy_ids:
            self.errors.append(ValidationError(
                message=f"Duplicate policy ID: {node.id}",
                location=node.loc,
                error_code="DUPLICATE_POLICY_ID",
                category=ErrorCategory.SEMANTIC
            ))
        else:
            policy_ids.add(node.id)

        # Validate enforcement definition
        self._validate_enforcement(node.enforcement)

        return self._create_error_summary()

    def visit_WorkflowNodeDef(self, node: WorkflowNodeDef) -> ValidationErrorSummary:
        """Validate workflow node definition."""
        return self._create_error_summary()

    def visit_WorkflowEdgeDef(self, node: WorkflowEdgeDef) -> ValidationErrorSummary:
        """Validate workflow edge definition."""
        return self._create_error_summary()

    def visit_TypeBody(self, node) -> ValidationErrorSummary:
        """Visit type body node."""
        return self._create_error_summary()

    def visit_FieldList(self, node) -> ValidationErrorSummary:
        """Visit field list node."""
        return self._create_error_summary()

    def visit_WorkflowDef(self, node: WorkflowDef) -> ValidationErrorSummary:
        """Validate workflow definition."""
        node_ids: Set[str] = set()
        edge_errors: List[ValidationError] = []

        # Check for duplicate node IDs
        for node_id, node_obj in node.nodes.items():
            if node_id in node_ids:
                self.errors.append(ValidationError(
                    message=f"Duplicate node ID: {node_id}",
                    location=node_obj.loc,
                    error_code="DUPLICATE_NODE_ID",
                    category=ErrorCategory.SEMANTIC
                ))
            else:
                node_ids.add(node_id)

        # Check for invalid edge references
        for edge in node.edges:
            if edge.source not in node.nodes:
                edge_errors.append(ValidationError(
                    message=f"Edge references non-existent source node: {edge.source}",
                    location=edge.loc,
                    error_code="INVALID_EDGE_REFERENCE",
                    category=ErrorCategory.SEMANTIC
                ))
            if edge.target not in node.nodes:
                edge_errors.append(ValidationError(
                    message=f"Edge references non-existent target node: {edge.target}",
                    location=edge.loc,
                    error_code="INVALID_EDGE_REFERENCE",
                    category=ErrorCategory.SEMANTIC
                ))

        self.errors.extend(edge_errors)
        return self._create_error_summary()

    def _validate_enforcement(self, enforcement: EnforcementDef) -> None:
        """Validate enforcement definition."""
        # This is a helper method that calls the visitor
        enforcement.accept(self)

    def validate_workflow(self, workflow: WorkflowDef) -> ValidationErrorSummary:
        """Validate workflow definition."""
        return workflow.accept(self)

    def validate_policy(self, policy: PolicyDef) -> ValidationErrorSummary:
        """Validate policy definition."""
        return policy.accept(self)

    def _generate_cache_key(self, program: Program) -> str:
        import hashlib
        import json

        program_data = {
            'declarations': [
                {
                    'type': type(decl).__name__,
                    'name': getattr(decl, 'name', None),
                    'fields': [f.name for f in getattr(decl, 'fields', [])] if hasattr(decl, 'fields') else None
                }
                for decl in program.declarations
            ],
            'agent': {
                'name': getattr(program.agent, 'name', None) if program.agent else None,
                'fields': [f.name for f in getattr(program.agent, 'fields', [])] if program.agent and hasattr(program.agent, 'fields') else None
            }
        }

        program_str = json.dumps(program_data, sort_keys=True)
        return hashlib.md5(program_str.encode()).hexdigest()

    def _create_error_summary(self) -> ValidationErrorSummary:
        return ValidationErrorSummary(
            total_errors=len(self.errors),
            syntax_errors=[e for e in self.errors if e.category == ErrorCategory.SYNTAX],
            semantic_errors=[e for e in self.errors if e.category == ErrorCategory.SEMANTIC],
            validation_errors=[e for e in self.errors if e.category == ErrorCategory.VALIDATION],
            type_errors=[e for e in self.errors if e.category == ErrorCategory.TYPE]
        )
