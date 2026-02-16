"""
Lark-to-AST Transformer for ADL DSL

This module provides the ADLTransformer class that converts Lark parse trees
into typed AST nodes according to the grammar defined in grammar.lark.
"""

from lark import Transformer, Token, Tree, v_args
from lark.tree import Meta
from typing import List, Optional, Union, Any

# Import all AST node types from ast module
from .ast import (
    SourceLocation,
    Program,
    ImportStmt,
    EnumDef,
    TypeDef,
    TypeBody,
    FieldDef,
    PrimitiveType,
    TypeReference,
    ArrayType,
    UnionType,
    OptionalType,
    ConstrainedType,
    AgentDef,
    TypeExpr,
)


class ADLTransformer(Transformer):
    """
    Transformer that converts Lark parse trees to AST nodes.

    This class extends Lark's Transformer and implements transform methods
    for each grammar rule, extracting SourceLocation information from Lark meta.
    """

    def __init__(self, file_path: Optional[str] = None):
        super().__init__()
        self.file_path = file_path

    def _get_loc(self, meta: Meta) -> SourceLocation:
        """
        Extract SourceLocation from Lark meta.

        Args:
            meta: Lark meta object containing position information

        Returns:
            SourceLocation object with line, column, end_line, end_column
        """
        # Safely get attributes with defaults
        line = getattr(meta, 'line', 1)
        column = getattr(meta, 'column', 1)
        end_line = getattr(meta, 'end_line', line)
        end_column = getattr(meta, 'end_column', column)
        file = getattr(meta, 'filename', None)
        
        return SourceLocation(
            line=line,
            column=column,
            end_line=end_line,
            end_column=end_column,
            file=file,
        )

    def start(self, children: List) -> Program:
        """
        Transform the start symbol (program).

        Args:
            children: List of child nodes [program]

        Returns:
            Program AST node
        """
        # start just returns the program node
        return children[0]

    @v_args(meta=True)
    def program(self, meta, children: List) -> Program:
        """
        Transform the program rule.

        Args:
            meta: Lark meta object
            children: List of child nodes [imports, declarations, agent]

        Returns:
            Program AST node
        """
        imports = []
        declarations = []
        agent = None

        for child in children:
            if isinstance(child, list):
                imports.extend(child)
            elif isinstance(child, ImportStmt):
                imports.append(child)
            elif isinstance(child, (EnumDef, TypeDef)):
                declarations.append(child)
            elif isinstance(child, AgentDef):
                agent = child

        return Program(
            imports=imports,
            declarations=declarations,
            agent=agent,
            loc=self._get_loc(meta),
        )

    def declaration(self, children: List) -> Union[EnumDef, TypeDef]:
        """
        Transform a declaration.

        Args:
            children: List containing either enum_def or type_def

        Returns:
            The declaration node
        """
        return children[0]

    @v_args(meta=True)
    def import_stmt(self, meta, children: List) -> ImportStmt:
        """
        Transform an import statement.

        Args:
            meta: Lark meta object
            children: List of child nodes [import_token, import_path, (as_token, alias)]

        Returns:
            ImportStmt AST node
        """
        import_path = children[1]
        alias = None
        if len(children) > 2:
            alias = children[3]

        return ImportStmt(
            path=import_path,
            alias=alias,
            loc=self._get_loc(meta),
        )

    def import_path(self, children: List) -> str:
        """
        Transform an import path.

        Args:
            children: List of path components (already transformed by absolute_path or relative_path)

        Returns:
            String representation of the path
        """
        # The child is already a string from absolute_path or relative_path
        return children[0] if children else ""

    def absolute_path(self, children: List) -> str:
        """
        Transform an absolute path.

        Args:
            children: List of IDENTIFIER tokens and SLASH/DOT tokens

        Returns:
            String representation of the path
        """
        # Build path from tokens
        parts = []
        for child in children:
            if isinstance(child, Token):
                if child.type == "SLASH":
                    parts.append("/")
                elif child.type == "DOT":
                    parts.append(".")
                elif child.type == "DOTDOT":
                    parts.append("..")
                else:
                    parts.append(child.value)
            else:
                # Already a string
                parts.append(child)
        return "".join(parts)

    def relative_path(self, children: List) -> str:
        """
        Transform a relative path.

        Args:
            children: List of path components including ".."

        Returns:
            String representation of the path
        """
        parts = []
        for child in children:
            if isinstance(child, Token):
                if child.type == "SLASH":
                    parts.append("/")
                elif child.type == "DOT":
                    parts.append(".")
                elif child.type == "DOTDOT":
                    parts.append("..")
                else:
                    parts.append(child.value)
            else:
                # Already a string
                parts.append(child)
        return "".join(parts)

    @v_args(meta=True)
    def enum_def(self, meta, children: List) -> EnumDef:
        """
        Transform an enum definition.

        Args:
            meta: Lark meta object
            children: List of child nodes [ENUM, IDENTIFIER, LBRACE, enum_body, RBRACE]

        Returns:
            EnumDef AST node
        """
        name = children[1].value
        values = children[3]

        return EnumDef(
            name=name,
            values=values,
            loc=SourceLocation(1, 1, 1, 1),  # TODO: Get actual location
        )

    def COMMA(self, token: Token) -> None:
        """
        Transform COMMA token - return None to filter it out.

        Args:
            token: COMMA token

        Returns:
            None (will be filtered out)
        """
        return None

    def enum_body(self, children: List) -> List[str]:
        """
        Transform an enum body.

        Args:
            children: List of enum_value nodes (strings) and None (from COMMA)

        Returns:
            List of enum value names
        """
        # Filter out None values (from COMMA tokens), keep only enum_value strings
        return [child for child in children if child is not None]

    def enum_value(self, children: List) -> str:
        """
        Transform an enum value.

        Args:
            children: List containing IDENTIFIER token

        Returns:
            Enum value name as string
        """
        # children[0] is the IDENTIFIER token, return its value
        if isinstance(children[0], Token):
            return children[0].value
        # If it's already a string, return it
        return str(children[0])

    @v_args(meta=True)
    def type_def(self, meta, children: List) -> TypeDef:
        """
        Transform a type definition.

        Args:
            meta: Lark meta object
            children: List of child nodes [TYPE, IDENTIFIER, (type_body)]

        Returns:
            TypeDef AST node
        """
        name = children[1].value
        body = children[2] if len(children) > 2 and children[2] else None

        return TypeDef(
            name=name,
            body=body,
            loc=self._get_loc(meta),
        )

    @v_args(meta=True)
    def type_body(self, meta, children: List) -> TypeBody:
        """
        Transform a type body.

        Args:
            meta: Lark meta object
            children: List of field_def nodes and brace tokens

        Returns:
            TypeBody AST node
        """
        # Filter out brace tokens, keep only field_def nodes
        fields = []
        for child in children:
            if isinstance(child, FieldDef):
                fields.append(child)
            elif isinstance(child, list):
                # Flatten nested lists
                for subchild in child:
                    if isinstance(subchild, FieldDef):
                        fields.append(subchild)

        return TypeBody(
            fields=fields,
            loc=self._get_loc(meta),
        )

    @v_args(meta=True)
    def field_def(self, meta, children: List) -> FieldDef:
        """
        Transform a field definition.

        Args:
            meta: Lark meta object
            children: List of child nodes [IDENTIFIER, ("?"), ":", type_expr]

        Returns:
            FieldDef AST node
        """
        name = children[0].value
        optional = False
        type_expr = None

        # Find the type_expr (last non-Token child)
        for child in reversed(children):
            if not isinstance(child, Token):
                type_expr = child
                break

        # Check for optional marker
        for child in children:
            if isinstance(child, Token) and child.value == "?":
                optional = True
                break

        return FieldDef(
            name=name,
            type=type_expr,
            optional=optional,
            loc=self._get_loc(meta),
        )

    def field_list(self, children: List) -> List[FieldDef]:
        """
        Transform a field list.

        Args:
            children: List of field_def nodes

        Returns:
            List of FieldDef nodes
        """
        return children

    def type_expr(self, children: List) -> Union[UnionType, ArrayType, OptionalType, ConstrainedType]:
        """
        Transform a type expression.

        Args:
            children: List containing union_type node

        Returns:
            Type expression node
        """
        return children[0]

    @v_args(meta=True)
    def union_type(self, meta, children: List) -> TypeExpr:
        """
        Transform a union type.

        Args:
            meta: Lark meta object
            children: List of postfix_type nodes and PIPE tokens

        Returns:
            UnionType AST node (or single type if only one child)
        """
        # Filter out PIPE tokens, keep only postfix_type nodes
        types = [child for child in children if not isinstance(child, Token) or child.type != "PIPE"]

        # If only one type, return it directly (not wrapped in UnionType)
        if len(types) == 1:
            return types[0]

        return UnionType(
            types=types,
            loc=self._get_loc(meta),
        )

    @v_args(meta=True)
    def postfix_type(self, meta, children: List) -> Union[PrimitiveType, TypeReference, ArrayType, OptionalType, ConstrainedType]:
        """
        Transform a postfix type.

        Args:
            meta: Lark meta object
            children: List of [primary_type, suffix*]

        Returns:
            Type node with suffixes applied
        """
        base_type = children[0]
        suffixes = children[1:]

        # Apply suffixes from right to left
        result = base_type
        for suffix in reversed(suffixes):
            result = self._apply_suffix(meta, result, suffix)

        return result

    def _apply_suffix(self, meta: Meta, base_type: TypeExpr, suffix: Union[Token, TypeExpr, str]) -> TypeExpr:
        """
        Apply a type suffix to a base type.

        Args:
            meta: Lark meta object
            base_type: The base type to apply suffix to
            suffix: The suffix token, transformed suffix node, or string marker

        Returns:
            Type node with suffix applied
        """
        if isinstance(suffix, Token):
            if suffix.value == "[]":
                return ArrayType(
                    element_type=base_type,
                    loc=self._get_loc(meta),
                )
            elif suffix.value == "?":
                return OptionalType(
                    inner_type=base_type,
                    loc=self._get_loc(meta),
                )
            elif suffix.value == "(":
                # This is the start of a constraint, handled by constraint_suffix
                return base_type
            else:
                raise ValueError(f"Unknown suffix: {suffix.value}")
        elif isinstance(suffix, str):
            # Handle string suffix markers from suffix transformers
            if suffix == "[]":
                return ArrayType(
                    element_type=base_type,
                    loc=self._get_loc(meta),
                )
            elif suffix == "?":
                return OptionalType(
                    inner_type=base_type,
                    loc=self._get_loc(meta),
                )
            elif suffix == "(":
                # This is the start of a constraint, handled by constraint_suffix
                return base_type
            elif ".." in suffix:
                # This is a range constraint string (e.g., "1..100", "1..", "..100", or "..")
                # Parse the range
                parts = suffix.split("..")
                min_val = int(parts[0]) if parts[0] else None
                max_val = int(parts[1]) if len(parts) > 1 and parts[1] else None
                return ConstrainedType(
                    base_type=base_type,
                    min_value=min_val,
                    max_value=max_val,
                    loc=self._get_loc(meta),
                )
            else:
                raise ValueError(f"Unknown suffix string: {suffix}")
        elif isinstance(suffix, (ArrayType, OptionalType, ConstrainedType)):
            # Already transformed
            return suffix
        else:
            raise ValueError(f"Unknown suffix type: {type(suffix)}")

    def suffix(self, children: List) -> Union[Token, str]:
        """
        Transform a suffix.

        Args:
            children: List containing array_suffix, optional_suffix, or constraint_suffix

        Returns:
            Suffix token or string
        """
        return children[0]

    def array_suffix(self, children: List) -> str:
        """
        Transform an array suffix.

        Args:
            children: Empty list (terminals "[" and "]" are not passed as children)

        Returns:
            "[]" string to indicate array type
        """
        return "[]"

    def optional_suffix(self, children: List) -> str:
        """
        Transform an optional suffix.

        Args:
            children: Empty list (terminal "?" is not passed as child)

        Returns:
            "?" string to indicate optional type
        """
        return "?"

    def constraint_suffix(self, children: List) -> str:
        """
        Transform a constraint suffix.

        Args:
            children: List containing LPAREN, range_constraint, and RPAREN tokens

        Returns:
            The range_constraint string (e.g., "1..100" or "1..")
        """
        # Return the range_constraint (middle child)
        return children[1] if len(children) > 1 else children[0]

    def range_constraint(self, children: List) -> str:
        """
        Transform a range constraint.

        Args:
            children: List containing NUMBER, DOTDOT, and optional NUMBER tokens

        Returns:
            String representation like "5..10", "5..", "..10", or ".."
        """
        if len(children) == 1:
            # Just DOTDOT: ".."
            return ".."
        elif len(children) == 2:
            # Check if first is DOTDOT (max only) or NUMBER (min only)
            if isinstance(children[0], Token) and children[0].type == "DOTDOT":
                # Max only: "..100"
                return f"..{children[1].value}"
            else:
                # Min only: "1.."
                return f"{children[0].value}.."
        elif len(children) == 3:
            # Both min and max: "min..max"
            return f"{children[0].value}..{children[2].value}"
        else:
            return ""

    @v_args(meta=True)
    def primary_type(self, meta, children: List) -> Union[PrimitiveType, TypeReference]:
        """
        Transform a primary type.

        Args:
            meta: Lark meta object
            children: List containing primitive type token or IDENTIFIER token

        Returns:
            PrimitiveType or TypeReference AST node
        """
        primitive_types = {"PRIMITIVE_STRING", "PRIMITIVE_INTEGER", "PRIMITIVE_NUMBER", "PRIMITIVE_BOOLEAN", "PRIMITIVE_OBJECT", "PRIMITIVE_ARRAY", "PRIMITIVE_ANY", "PRIMITIVE_NULL"}
        if isinstance(children[0], Token) and children[0].type in primitive_types:
            return PrimitiveType(
                name=children[0].value,
                loc=self._get_loc(meta),
            )
        elif isinstance(children[0], Token) and children[0].type == "IDENTIFIER":
            return TypeReference(
                name=children[0].value,
                loc=self._get_loc(meta),
            )
        elif isinstance(children[0], Token) and children[0].value == "(":
            # Parenthesized type expression
            return children[1]
        else:
            raise ValueError(f"Unknown primary type: {children[0]}")

    @v_args(meta=True)
    def agent_def(self, meta, children: List) -> AgentDef:
        """
        Transform an agent definition.

        Args:
            meta: Lark meta object
            children: List of child nodes [AGENT, IDENTIFIER, LBRACE, field_list, RBRACE]

        Returns:
            AgentDef AST node
        """
        name = children[1].value
        fields = children[3]

        return AgentDef(
            name=name,
            fields=fields,
            loc=self._get_loc(meta),
        )

    # Default handler for any unmatched tokens
    def DEFAULT(self, token: Token) -> Token:
        """
        Default handler for unmatched tokens.

        Args:
            token: The token to return

        Returns:
            The token itself
        """
        return token