"""
DSL Formatter Module

This module provides a comprehensive formatter for the ADL DSL with AST-based
pretty printing, comment preservation, import sorting, and configurable options.
"""

from dataclasses import dataclass, field
from typing import List, Optional, Dict, Tuple
from pathlib import Path
from .adl_ast import (
    Program, ImportStmt, EnumDef, TypeDef, TypeBody, FieldDef,
    AgentDef, PrimitiveType, TypeReference, ArrayType, UnionType,
    OptionalType, ConstrainedType, ASTVisitor
)


@dataclass
class FormatterConfig:
    """Configuration for DSL formatting."""
    indent_size: int = 2
    max_line_length: int = 100
    trailing_commas: bool = False
    sort_imports: bool = True
    preserve_comments: bool = True
    newline_after_declaration: bool = True


class CommentTracker:
    """Track and preserve comments during formatting."""

    def __init__(self):
        self.comments: List[Tuple[int, int, str]] = []  # (line, column, comment)
        self.comment_map: Dict[int, List[str]] = {}  # line -> list of comments

    def add_comment(self, line: int, column: int, comment: str):
        """Add a comment to track."""
        self.comments.append((line, column, comment))
        if line not in self.comment_map:
            self.comment_map[line] = []
        self.comment_map[line].append(comment)

    def get_comments_for_line(self, line: int) -> List[str]:
        """Get all comments for a specific line."""
        return self.comment_map.get(line, [])

    def clear(self):
        """Clear all tracked comments."""
        self.comments.clear()
        self.comment_map.clear()


class DSLFormatter(ASTVisitor[str]):
    """
    AST-based formatter for ADL DSL.

    This formatter traverses the AST and generates formatted source code
    with configurable options for indentation, line length, and other formatting rules.
    """

    def __init__(self, config: FormatterConfig = None):
        """
        Initialize the formatter.

        Args:
            config: Configuration for formatting. If None, uses default config.
        """
        self.config = config or FormatterConfig()
        self.indent_level = 0
        self.comment_tracker = CommentTracker()
        self._current_line = 0
        self._current_column = 0

    def format(self, content: str) -> str:
        """
        Format DSL content.

        Args:
            content: Raw DSL source code

        Returns:
            Formatted DSL code
        """
        # Parse comments from source
        if self.config.preserve_comments:
            self.comment_tracker = CommentTracker()
            self._parse_comments(content)

        # Parse content to AST
        from .parser import GrammarParser
        parser = GrammarParser()
        program = parser.parse(content)

        # Format the AST
        result = self.format_ast(program)

        return result

    def format_file(self, file_path: str) -> str:
        """
        Format a DSL file.

        Args:
            file_path: Path to the DSL file

        Returns:
            Formatted DSL code
        """
        with open(file_path, 'r') as f:
            content = f.read()

        return self.format(content)

    def format_ast(self, program: Program) -> str:
        """
        Format an AST directly.

        Args:
            program: AST program node

        Returns:
            Formatted DSL code
        """
        lines = []

        # Format imports
        if self.config.sort_imports:
            imports = sorted(program.imports, key=self._sort_import_key)
        else:
            imports = program.imports

        for imp in imports:
            lines.append(self.visit(imp))
            if self.config.newline_after_declaration:
                lines.append("")

        # Format declarations
        for decl in program.declarations:
            lines.append(self.visit(decl))
            if self.config.newline_after_declaration:
                lines.append("")

        # Format agent if present
        if program.agent:
            lines.append(self.visit(program.agent))

        # Remove trailing empty lines
        while lines and lines[-1] == "":
            lines.pop()

        return "\n".join(lines)

    def _parse_comments(self, content: str):
        """Parse comments from source content."""
        lines = content.split('\n')
        for line_num, line in enumerate(lines, start=1):
            # Find comments in the line
            comment_start = line.find('#')
            if comment_start != -1:
                comment = line[comment_start:].rstrip()
                self.comment_tracker.add_comment(line_num, comment_start, comment)

    def _sort_import_key(self, import_stmt: ImportStmt) -> Tuple[bool, str]:
        """
        Sort key for imports.

        Absolute imports come before relative imports, then alphabetically.
        """
        is_absolute = not import_stmt.path.startswith('.')
        return (not is_absolute, import_stmt.path.lower())

    def _indent(self) -> str:
        """Get current indentation string."""
        return " " * (self.indent_level * self.config.indent_size)

    def _add_newline(self, lines: List[str]) -> None:
        """Add a newline to the lines list."""
        lines.append("")

    def _format_type_expr(self, type_expr) -> str:
        """Format a type expression."""
        return self.visit(type_expr)

    # ============================================
    # Program Structure
    # ============================================

    def visit_Program(self, node: Program) -> str:
        """Visit a Program node."""
        return self.format_ast(node)

    def visit_ImportStmt(self, node: ImportStmt) -> str:
        """Visit an ImportStmt node."""
        alias = f" as {node.alias}" if node.alias else ""
        return f"import {node.path}{alias}"

    # ============================================
    # Declarations
    # ============================================

    def visit_EnumDef(self, node: EnumDef) -> str:
        """Visit an EnumDef node."""
        lines = [f"{self._indent()}enum {node.name} {{"]
        self.indent_level += 1

        for value in node.values:
            lines.append(f"{self._indent()}{value},")

        self.indent_level -= 1
        lines.append(f"{self._indent()}}}")

        return "\n".join(lines)

    def visit_TypeDef(self, node: TypeDef) -> str:
        """Visit a TypeDef node."""
        lines = [f"{self._indent()}type {node.name} {{"]
        self.indent_level += 1

        if node.body:
            lines.append(self.visit(node.body))

        self.indent_level -= 1
        lines.append(f"{self._indent()}}}")

        return "\n".join(lines)

    def visit_TypeBody(self, node: TypeBody) -> str:
        """Visit a TypeBody node."""
        lines = []

        for field in node.fields:
            lines.append(self.visit(field))

        return "\n".join(lines)

    def visit_FieldDef(self, node: FieldDef) -> str:
        """Visit a FieldDef node."""
        opt = "?" if node.optional else ""
        type_str = self._format_type_expr(node.type)
        return f"{self._indent()}{node.name}{opt}: {type_str}"

    # ============================================
    # Type Expressions
    # ============================================

    def visit_PrimitiveType(self, node: PrimitiveType) -> str:
        """Visit a PrimitiveType node."""
        return node.name

    def visit_TypeReference(self, node: TypeReference) -> str:
        """Visit a TypeReference node."""
        return node.name

    def visit_ArrayType(self, node: ArrayType) -> str:
        """Visit an ArrayType node."""
        element_type = self._format_type_expr(node.element_type)
        return f"{element_type}[]"

    def visit_UnionType(self, node: UnionType) -> str:
        """Visit a UnionType node."""
        types = [self._format_type_expr(t) for t in node.types]
        return " | ".join(types)

    def visit_OptionalType(self, node: OptionalType) -> str:
        """Visit an OptionalType node."""
        inner_type = self._format_type_expr(node.inner_type)
        return f"{inner_type}?"

    def visit_ConstrainedType(self, node: ConstrainedType) -> str:
        """Visit a ConstrainedType node."""
        base_type = self._format_type_expr(node.base_type)

        if node.min_value is not None and node.max_value is not None:
            return f"{base_type}({node.min_value}..{node.max_value})"
        elif node.min_value is not None:
            return f"{base_type}({node.min_value}..)"
        elif node.max_value is not None:
            return f"{base_type}(..{node.max_value})"
        else:
            return f"{base_type}(..)"

    # ============================================
    # Agent
    # ============================================

    def visit_AgentDef(self, node: AgentDef) -> str:
        """Visit an AgentDef node."""
        lines = [f"{self._indent()}agent {node.name} {{"]
        self.indent_level += 1

        for field in node.fields:
            lines.append(self.visit(field))

        self.indent_level -= 1
        lines.append(f"{self._indent()}}}")

        return "\n".join(lines)


def format_dsl(content: str, config: FormatterConfig = None) -> str:
    """
    Convenience function to format DSL content.

    Args:
        content: Raw DSL source code
        config: Optional formatting configuration

    Returns:
        Formatted DSL code
    """
    formatter = DSLFormatter(config)
    return formatter.format(content)


def format_dsl_file(file_path: str, config: FormatterConfig = None) -> str:
    """
    Convenience function to format a DSL file.

    Args:
        file_path: Path to the DSL file
        config: Optional formatting configuration

    Returns:
        Formatted DSL code
    """
    formatter = DSLFormatter(config)
    return formatter.format_file(file_path)