"""
Comprehensive test suite for ADL DSL Formatter

Tests all formatting features, configuration options, AST node types,
edge cases, and convenience functions for the ADL DSL formatter.
"""

import unittest
from pathlib import Path
from tools.dsl.formatter import (
    DSLFormatter,
    FormatterConfig,
    format_dsl,
    format_dsl_file
)
from tools.dsl.parser import GrammarParser
from tools.dsl.ast import (
    Program,
    ImportStmt,
    EnumDef,
    TypeDef,
    TypeBody,
    FieldDef,
    AgentDef,
    PrimitiveType,
    TypeReference,
    ArrayType,
    UnionType,
    OptionalType,
    ConstrainedType,
    SourceLocation
)


# ============================================
# Test Fixtures
# ============================================

def create_source_location(line: int = 1, column: int = 1) -> SourceLocation:
    """Create a SourceLocation object for testing."""
    return SourceLocation(
        line=line,
        column=column,
        end_line=line,
        end_column=column,
        file=None
    )


class TestFixtures:
    """Common test fixtures for formatter tests."""

    @staticmethod
    def create_simple_type(name: str, fields: list) -> TypeDef:
        """Create a simple type definition."""
        field_defs = [
            FieldDef(
                loc=create_source_location(),
                name=field['name'],
                type=field['type'],
                optional=field.get('optional', False)
            )
            for field in fields
        ]
        return TypeDef(
            loc=create_source_location(),
            name=name,
            body=TypeBody(loc=create_source_location(), fields=field_defs)
        )

    @staticmethod
    def create_simple_enum(name: str, values: list) -> EnumDef:
        """Create a simple enum definition."""
        return EnumDef(loc=create_source_location(), name=name, values=values)

    @staticmethod
    def create_simple_agent(name: str, fields: list) -> AgentDef:
        """Create a simple agent definition."""
        field_defs = [
            FieldDef(
                loc=create_source_location(),
                name=field['name'],
                type=field['type'],
                optional=field.get('optional', False)
            )
            for field in fields
        ]
        return AgentDef(loc=create_source_location(), name=name, fields=field_defs)

    @staticmethod
    def create_import_stmt(path: str, alias: str = None) -> ImportStmt:
        """Create an import statement."""
        return ImportStmt(loc=create_source_location(), path=path, alias=alias or "")


# ============================================
# Test Class: TestFormatterConfig
# ============================================

class TestFormatterConfig(unittest.TestCase):
    """Test formatter configuration options."""

    def setUp(self):
        """Set up test fixtures."""
        self.default_config = FormatterConfig()

    def test_default_indent_size(self):
        """Test default indent size is 2."""
        self.assertEqual(self.default_config.indent_size, 2)

    def test_default_max_line_length(self):
        """Test default max line length is 100."""
        self.assertEqual(self.default_config.max_line_length, 100)

    def test_default_trailing_commas(self):
        """Test default trailing commas is False."""
        self.assertFalse(self.default_config.trailing_commas)

    def test_default_sort_imports(self):
        """Test default sort imports is True."""
        self.assertTrue(self.default_config.sort_imports)

    def test_default_preserve_comments(self):
        """Test default preserve comments is True."""
        self.assertTrue(self.default_config.preserve_comments)

    def test_default_newline_after_declaration(self):
        """Test default newline after declaration is True."""
        self.assertTrue(self.default_config.newline_after_declaration)

    def test_custom_indent_size(self):
        """Test custom indent size configuration."""
        config = FormatterConfig(indent_size=4)
        self.assertEqual(config.indent_size, 4)

    def test_custom_max_line_length(self):
        """Test custom max line length configuration."""
        config = FormatterConfig(max_line_length=120)
        self.assertEqual(config.max_line_length, 120)

    def test_custom_trailing_commas(self):
        """Test custom trailing commas configuration."""
        config = FormatterConfig(trailing_commas=True)
        self.assertTrue(config.trailing_commas)

    def test_custom_sort_imports(self):
        """Test custom sort imports configuration."""
        config = FormatterConfig(sort_imports=False)
        self.assertFalse(config.sort_imports)

    def test_custom_preserve_comments(self):
        """Test custom preserve comments configuration."""
        config = FormatterConfig(preserve_comments=False)
        self.assertFalse(config.preserve_comments)

    def test_custom_newline_after_declaration(self):
        """Test custom newline after declaration configuration."""
        config = FormatterConfig(newline_after_declaration=False)
        self.assertFalse(config.newline_after_declaration)

    def test_config_override(self):
        """Test that config can override default values."""
        config = FormatterConfig(
            indent_size=8,
            max_line_length=80,
            trailing_commas=True,
            sort_imports=False,
            preserve_comments=False,
            newline_after_declaration=False
        )
        self.assertEqual(config.indent_size, 8)
        self.assertEqual(config.max_line_length, 80)
        self.assertTrue(config.trailing_commas)
        self.assertFalse(config.sort_imports)
        self.assertFalse(config.preserve_comments)
        self.assertFalse(config.newline_after_declaration)

    def test_none_config_uses_defaults(self):
        """Test that None config uses default values."""
        formatter = DSLFormatter(config=None)
        self.assertEqual(formatter.config.indent_size, 2)
        self.assertEqual(formatter.config.max_line_length, 100)
        self.assertFalse(formatter.config.trailing_commas)
        self.assertTrue(formatter.config.sort_imports)
        self.assertTrue(formatter.config.preserve_comments)


# ============================================
# Test Class: TestBasicFormatting
# ============================================

class TestBasicFormatting(unittest.TestCase):
    """Test basic formatting features."""

    def setUp(self):
        """Set up test fixtures."""
        self.parser = GrammarParser()
        self.formatter = DSLFormatter(FormatterConfig())

    def test_simple_type_formatting(self):
        """Test formatting of a simple type definition."""
        content = """
type Person {
  name: string
  age: integer
}
"""
        formatted = self.formatter.format(content)
        self.assertIn("type Person {", formatted)
        self.assertIn("name: string", formatted)
        self.assertIn("age: integer", formatted)

    def test_enum_formatting(self):
        """Test formatting of an enum definition."""
        content = """
enum Status {
  active
  inactive
}
"""
        formatted = self.formatter.format(content)
        self.assertIn("enum Status {", formatted)
        self.assertIn("active", formatted)
        self.assertIn("inactive", formatted)

    def test_agent_formatting(self):
        """Test formatting of an agent definition."""
        content = """
agent MyAgent {
  name: string
  tools: Tool[]
}
"""
        formatted = self.formatter.format(content)
        self.assertIn("agent MyAgent {", formatted)
        self.assertIn("name: string", formatted)
        self.assertIn("tools: Tool[]", formatted)

    def test_import_formatting(self):
        """Test formatting of an import statement."""
        content = """
import schema.components.memory
import schema.components.rag as tools
"""
        formatted = self.formatter.format(content)
        self.assertIn("import schema.components.memory", formatted)
        self.assertIn("import schema.components.rag as tools", formatted)

    def test_multiple_declarations_formatting(self):
        """Test formatting of multiple declarations."""
        content = """
type Person {
  name: string
  age: integer
}

enum Status {
  active
  inactive
}
"""
        formatted = self.formatter.format(content)
        self.assertIn("type Person {", formatted)
        self.assertIn("enum Status {", formatted)

    def test_import_with_alias_formatting(self):
        """Test formatting of import with alias."""
        content = """
import schema.components.memory as mem
"""
        formatted = self.formatter.format(content)
        self.assertIn("import schema.components.memory as mem", formatted)

    def test_empty_type_formatting(self):
        """Test formatting of an empty type."""
        content = """
type EmptyType {
}
"""
        formatted = self.formatter.format(content)
        self.assertIn("type EmptyType {", formatted)
        self.assertIn("}", formatted)

    def test_empty_enum_formatting(self):
        """Test formatting of an empty enum."""
        content = """
enum EmptyEnum {
}
"""
        formatted = self.formatter.format(content)
        self.assertIn("enum EmptyEnum {", formatted)
        self.assertIn("}", formatted)

    def test_empty_agent_formatting(self):
        """Test formatting of an empty agent."""
        content = """
agent EmptyAgent {
}
"""
        formatted = self.formatter.format(content)
        self.assertIn("agent EmptyAgent {", formatted)
        self.assertIn("}", formatted)


# ============================================
# Test Class: TestIndentation
# ============================================

class TestIndentation(unittest.TestCase):
    """Test indentation features."""

    def setUp(self):
        """Set up test fixtures."""
        self.parser = GrammarParser()

    def test_indent_size_2(self):
        """Test formatting with indent size 2."""
        config = FormatterConfig(indent_size=2)
        formatter = DSLFormatter(config)
        content = """
type Person {
  name: string
  age: integer
}
"""
        formatted = formatter.format(content)
        # Check that lines are indented with 2 spaces
        lines = formatted.split('\n')
        self.assertTrue(lines[1].startswith('  name: string'))
        self.assertTrue(lines[2].startswith('  age: integer'))

    def test_indent_size_4(self):
        """Test formatting with indent size 4."""
        config = FormatterConfig(indent_size=4)
        formatter = DSLFormatter(config)
        content = """
type Person {
  name: string
  age: integer
}
"""
        formatted = formatter.format(content)
        # Check that lines are indented with 4 spaces
        lines = formatted.split('\n')
        self.assertTrue(lines[1].startswith('    name: string'))
        self.assertTrue(lines[2].startswith('    age: integer'))

    def test_indent_size_8(self):
        """Test formatting with indent size 8."""
        config = FormatterConfig(indent_size=8)
        formatter = DSLFormatter(config)
        content = """
type Person {
  name: string
  age: integer
}
"""
        formatted = formatter.format(content)
        # Check that lines are indented with 8 spaces
        lines = formatted.split('\n')
        self.assertTrue(lines[1].startswith('        name: string'))
        self.assertTrue(lines[2].startswith('        age: integer'))

    def test_nested_indentation_type_body(self):
        """Test nested indentation in type body."""
        config = FormatterConfig(indent_size=2)
        formatter = DSLFormatter(config)
        content = """
type ComplexType {
  name: string
  nested: NestedType {
    field1: string
    field2: integer
  }
}
"""
        formatted = formatter.format(content)
        lines = formatted.split('\n')
        # Check nested indentation
        self.assertTrue(lines[3].startswith('  nested: NestedType {'))
        self.assertTrue(lines[4].startswith('    field1: string'))
        self.assertTrue(lines[5].startswith('    field2: integer'))

    def test_nested_indentation_enum_body(self):
        """Test nested indentation in enum body."""
        config = FormatterConfig(indent_size=2)
        formatter = DSLFormatter(config)
        content = """
enum Status {
  active
  inactive
  pending
}
"""
        formatted = formatter.format(content)
        lines = formatted.split('\n')
        # Check enum values are indented
        self.assertTrue(lines[1].startswith('  active,'))
        self.assertTrue(lines[2].startswith('  inactive,'))
        self.assertTrue(lines[3].startswith('  pending,'))

    def test_nested_indentation_agent_body(self):
        """Test nested indentation in agent body."""
        config = FormatterConfig(indent_size=2)
        formatter = DSLFormatter(config)
        content = """
agent MyAgent {
  name: string
  tools: Tool[]
  config: Config {
    setting1: string
    setting2: integer
  }
}
"""
        formatted = formatter.format(content)
        lines = formatted.split('\n')
        # Check nested indentation
        self.assertTrue(lines[3].startswith('  config: Config {'))
        self.assertTrue(lines[4].startswith('    setting1: string'))
        self.assertTrue(lines[5].startswith('    setting2: integer'))

    def test_indentation_consistency(self):
        """Test that indentation is consistent across all levels."""
        config = FormatterConfig(indent_size=2)
        formatter = DSLFormatter(config)
        content = """
type OuterType {
  field1: string
  field2: integer
  nested: NestedType {
    nestedField1: string
    nestedField2: integer
  }
}
"""
        formatted = formatter.format(content)
        lines = formatted.split('\n')
        # Check consistent indentation
        self.assertTrue(lines[1].startswith('  field1: string'))
        self.assertTrue(lines[2].startswith('  field2: integer'))
        self.assertTrue(lines[3].startswith('  nested: NestedType {'))
        self.assertTrue(lines[4].startswith('    nestedField1: string'))
        self.assertTrue(lines[5].startswith('    nestedField2: integer'))


# ============================================
# Test Class: TestImportSorting
# ============================================

class TestImportSorting(unittest.TestCase):
    """Test import sorting features."""

    def setUp(self):
        """Set up test fixtures."""
        self.parser = GrammarParser()

    def test_alphabetical_sorting(self):
        """Test alphabetical sorting of imports."""
        config = FormatterConfig(sort_imports=True)
        formatter = DSLFormatter(config)
        content = """
import schema.components.rag
import schema.components.memory
import schema.components.tool as tools
import schema.components.utils
"""
        formatted = formatter.format(content)
        lines = formatted.split('\n')
        # Check imports are sorted alphabetically
        self.assertIn("import schema.components.memory", lines[0])
        self.assertIn("import schema.components.rag", lines[1])
        self.assertIn("import schema.components.tool as tools", lines[2])
        self.assertIn("import schema.components.utils", lines[3])

    def test_absolute_vs_relative_import_grouping(self):
        """Test absolute imports come before relative imports."""
        config = FormatterConfig(sort_imports=True)
        formatter = DSLFormatter(config)
        content = """
import .local.module
import schema.components.memory
import schema.components.rag
import .local.utils
"""
        formatted = formatter.format(content)
        lines = formatted.split('\n')
        # Check absolute imports first, then relative
        self.assertIn("import schema.components.memory", lines[0])
        self.assertIn("import schema.components.rag", lines[1])
        self.assertIn("import .local.module", lines[2])
        self.assertIn("import .local.utils", lines[3])

    def test_import_sorting_disabled(self):
        """Test that import sorting can be disabled."""
        config = FormatterConfig(sort_imports=False)
        formatter = DSLFormatter(config)
        content = """
import schema.components.rag
import schema.components.memory
import schema.components.tool as tools
"""
        formatted = formatter.format(content)
        # Check imports are in original order
        self.assertIn("import schema.components.rag", formatted)
        self.assertIn("import schema.components.memory", formatted)
        self.assertIn("import schema.components.tool as tools", formatted)

    def test_imports_with_aliases_sorting(self):
        """Test sorting of imports with aliases."""
        config = FormatterConfig(sort_imports=True)
        formatter = DSLFormatter(config)
        content = """
import schema.components.rag as rag
import schema.components.memory as mem
import schema.components.tool as tools
"""
        formatted = formatter.format(content)
        lines = formatted.split('\n')
        # Check imports are sorted by path, not alias
        self.assertIn("import schema.components.memory as mem", lines[0])
        self.assertIn("import schema.components.rag as rag", lines[1])
        self.assertIn("import schema.components.tool as tools", lines[2])

    def test_single_import_formatting(self):
        """Test formatting of a single import."""
        config = FormatterConfig(sort_imports=True)
        formatter = DSLFormatter(config)
        content = """
import schema.components.memory
"""
        formatted = formatter.format(content)
        self.assertIn("import schema.components.memory", formatted)

    def test_no_imports_formatting(self):
        """Test formatting with no imports."""
        config = FormatterConfig(sort_imports=True)
        formatter = DSLFormatter(config)
        content = """
type Person {
  name: string
}
"""
        formatted = formatter.format(content)
        self.assertIn("type Person {", formatted)


# ============================================
# Test Class: TestTypeExpressionFormatting
# ============================================

class TestTypeExpressionFormatting(unittest.TestCase):
    """Test type expression formatting."""

    def setUp(self):
        """Set up test fixtures."""
        self.parser = GrammarParser()
        self.formatter = DSLFormatter(FormatterConfig())

    def test_primitive_type_string(self):
        """Test formatting of string primitive type."""
        content = """
type Person {
  name: string
}
"""
        formatted = self.formatter.format(content)
        self.assertIn("string", formatted)

    def test_primitive_type_integer(self):
        """Test formatting of integer primitive type."""
        content = """
type Person {
  age: integer
}
"""
        formatted = self.formatter.format(content)
        self.assertIn("integer", formatted)

    def test_primitive_type_number(self):
        """Test formatting of number primitive type."""
        content = """
type Person {
  score: number
}
"""
        formatted = self.formatter.format(content)
        self.assertIn("number", formatted)

    def test_primitive_type_boolean(self):
        """Test formatting of boolean primitive type."""
        content = """
type Person {
  isActive: boolean
}
"""
        formatted = self.formatter.format(content)
        self.assertIn("boolean", formatted)

    def test_primitive_type_object(self):
        """Test formatting of object primitive type."""
        content = """
type Person {
  data: object
}
"""
        formatted = self.formatter.format(content)
        self.assertIn("object", formatted)

    def test_primitive_type_array(self):
        """Test formatting of array primitive type."""
        content = """
type Person {
  tags: array
}
"""
        formatted = self.formatter.format(content)
        self.assertIn("array", formatted)

    def test_primitive_type_any(self):
        """Test formatting of any type."""
        content = """
type Person {
  data: any
}
"""
        formatted = self.formatter.format(content)
        self.assertIn("any", formatted)

    def test_primitive_type_null(self):
        """Test formatting of null type."""
        content = """
type Person {
  data: null
}
"""
        formatted = self.formatter.format(content)
        self.assertIn("null", formatted)

    def test_type_reference(self):
        """Test formatting of type reference."""
        content = """
type Person {
  address: Address
}
"""
        formatted = self.formatter.format(content)
        self.assertIn("Address", formatted)

    def test_array_type_string(self):
        """Test formatting of string[] array type."""
        content = """
type Person {
  tags: string[]
}
"""
        formatted = self.formatter.format(content)
        self.assertIn("string[]", formatted)

    def test_array_type_integer(self):
        """Test formatting of integer[][] array type."""
        content = """
type Matrix {
  data: integer[][]
}
"""
        formatted = self.formatter.format(content)
        self.assertIn("integer[][]", formatted)

    def test_union_type_string_integer(self):
        """Test formatting of string | integer union type."""
        content = """
type Person {
  status: string | integer
}
"""
        formatted = self.formatter.format(content)
        self.assertIn("string | integer", formatted)

    def test_union_type_multiple(self):
        """Test formatting of string | integer | boolean union type."""
        content = """
type Person {
  status: string | integer | boolean
}
"""
        formatted = self.formatter.format(content)
        self.assertIn("string | integer | boolean", formatted)

    def test_optional_type_string(self):
        """Test formatting of string? optional type."""
        content = """
type Person {
  middleName?: string
}
"""
        formatted = self.formatter.format(content)
        self.assertIn("middleName?: string", formatted)

    def test_optional_type_integer(self):
        """Test formatting of integer? optional type."""
        content = """
type Person {
  age?: integer
}
"""
        formatted = self.formatter.format(content)
        self.assertIn("age?: integer", formatted)

    def test_constrained_type_min_max(self):
        """Test formatting of integer(0..100) constrained type."""
        content = """
type Person {
  age: integer(0..150)
}
"""
        formatted = self.formatter.format(content)
        self.assertIn("integer(0..150)", formatted)

    def test_constrained_type_min_only(self):
        """Test formatting of integer(1..) constrained type."""
        content = """
type Person {
  count: integer(1..)
}
"""
        formatted = self.formatter.format(content)
        self.assertIn("integer(1..)", formatted)

    def test_constrained_type_max_only(self):
        """Test formatting of integer(..100) constrained type."""
        content = """
type Person {
  score: integer(..100)
}
"""
        formatted = self.formatter.format(content)
        self.assertIn("integer(..100)", formatted)

    def test_constrained_type_no_bounds(self):
        """Test formatting of integer(..) unconstrained type."""
        content = """
type Person {
  count: integer(..)
}
"""
        formatted = self.formatter.format(content)
        self.assertIn("integer(..)", formatted)

    def test_complex_type_expression(self):
        """Test formatting of complex type expression."""
        content = """
type Person {
  name: string
  age: integer(0..150)
  email: string?
  tags: string[]
  status: Status | string
}
"""
        formatted = self.formatter.format(content)
        self.assertIn("string", formatted)
        self.assertIn("integer(0..150)", formatted)
        self.assertIn("string?", formatted)
        self.assertIn("string[]", formatted)
        self.assertIn("Status | string", formatted)


# ============================================
# Test Class: TestCommentPreservation
# ============================================

class TestCommentPreservation(unittest.TestCase):
    """Test comment preservation features."""

    def setUp(self):
        """Set up test fixtures."""
        self.parser = GrammarParser()

    def test_standalone_comment(self):
        """Test preservation of standalone comments."""
        config = FormatterConfig(preserve_comments=True)
        formatter = DSLFormatter(config)
        content = """
# Represents a person in the system
type Person {
  name: string
  age: integer
}
"""
        formatted = formatter.format(content)
        self.assertIn("# Represents a person in the system", formatted)
        self.assertIn("type Person {", formatted)

    def test_inline_comment(self):
        """Test preservation of inline comments."""
        config = FormatterConfig(preserve_comments=True)
        formatter = DSLFormatter(config)
        content = """
type Person {
  name: string # Full name
  age: integer # Age in years
}
"""
        formatted = formatter.format(content)
        self.assertIn("# Full name", formatted)
        self.assertIn("# Age in years", formatted)

    def test_comment_preservation_disabled(self):
        """Test that comments can be disabled."""
        config = FormatterConfig(preserve_comments=False)
        formatter = DSLFormatter(config)
        content = """
# Represents a person in the system
type Person {
  name: string # Full name
  age: integer # Age in years
}
"""
        formatted = formatter.format(content)
        # Comments should be removed
        self.assertNotIn("# Represents a person in the system", formatted)
        self.assertNotIn("# Full name", formatted)

    def test_multiple_comments_on_same_line(self):
        """Test preservation of multiple comments on same line."""
        config = FormatterConfig(preserve_comments=True)
        formatter = DSLFormatter(config)
        content = """
type Person {
  name: string # First name # Full name
  age: integer # Age in years
}
"""
        formatted = formatter.format(content)
        self.assertIn("# First name # Full name", formatted)
        self.assertIn("# Age in years", formatted)

    def test_comment_after_import(self):
        """Test preservation of comment after import."""
        config = FormatterConfig(preserve_comments=True)
        formatter = DSLFormatter(config)
        content = """
import schema.components.memory # Memory module
type Person {
  name: string
}
"""
        formatted = formatter.format(content)
        self.assertIn("# Memory module", formatted)

    def test_comment_before_type(self):
        """Test preservation of comment before type."""
        config = FormatterConfig(preserve_comments=True)
        formatter = DSLFormatter(config)
        content = """
# Person type definition
type Person {
  name: string
}
"""
        formatted = formatter.format(content)
        self.assertIn("# Person type definition", formatted)

    def test_multiple_comments(self):
        """Test preservation of multiple comments."""
        config = FormatterConfig(preserve_comments=True)
        formatter = DSLFormatter(config)
        content = """
# Import statements
import schema.components.memory

# Type definitions
type Person {
  name: string # Full name
  age: integer # Age in years
}
"""
        formatted = formatter.format(content)
        self.assertIn("# Import statements", formatted)
        self.assertIn("# Type definitions", formatted)
        self.assertIn("# Full name", formatted)
        self.assertIn("# Age in years", formatted)


# ============================================
# Test Class: TestTrailingCommas
# ============================================

class TestTrailingCommas(unittest.TestCase):
    """Test trailing comma features."""

    def setUp(self):
        """Set up test fixtures."""
        self.parser = GrammarParser()

    def test_trailing_commas_enabled(self):
        """Test formatting with trailing commas enabled."""
        config = FormatterConfig(trailing_commas=True)
        formatter = DSLFormatter(config)
        content = """
type Person {
  name: string,
  age: integer,
  email: string
}
"""
        formatted = formatter.format(content)
        self.assertIn("name: string,", formatted)
        self.assertIn("age: integer,", formatted)
        self.assertIn("email: string", formatted)

    def test_trailing_commas_disabled(self):
        """Test formatting with trailing commas disabled."""
        config = FormatterConfig(trailing_commas=False)
        formatter = DSLFormatter(config)
        content = """
type Person {
  name: string,
  age: integer,
  email: string
}
"""
        formatted = formatter.format(content)
        self.assertIn("name: string", formatted)
        self.assertIn("age: integer", formatted)
        self.assertIn("email: string", formatted)

    def test_trailing_commas_on_last_field(self):
        """Test trailing comma on last field when enabled."""
        config = FormatterConfig(trailing_commas=True)
        formatter = DSLFormatter(config)
        content = """
type Person {
  name: string,
  age: integer
}
"""
        formatted = formatter.format(content)
        self.assertIn("name: string,", formatted)
        self.assertIn("age: integer", formatted)

    def test_trailing_commas_in_enum(self):
        """Test trailing commas in enum values."""
        config = FormatterConfig(trailing_commas=True)
        formatter = DSLFormatter(config)
        content = """
enum Status {
  active,
  inactive,
  pending
}
"""
        formatted = formatter.format(content)
        self.assertIn("active,", formatted)
        self.assertIn("inactive,", formatted)
        self.assertIn("pending", formatted)

    def test_trailing_commas_in_agent(self):
        """Test trailing commas in agent fields."""
        config = FormatterConfig(trailing_commas=True)
        formatter = DSLFormatter(config)
        content = """
agent MyAgent {
  name: string,
  tools: Tool[],
  config: Config
}
"""
        formatted = formatter.format(content)
        self.assertIn("name: string,", formatted)
        self.assertIn("tools: Tool[],", formatted)
        self.assertIn("config: Config", formatted)


# ============================================
# Test Class: TestComplexDSL
# ============================================

class TestComplexDSL(unittest.TestCase):
    """Test complex DSL files with all features."""

    def setUp(self):
        """Set up test fixtures."""
        self.parser = GrammarParser()
        self.formatter = DSLFormatter(FormatterConfig())

    def test_complete_dsl_file(self):
        """Test formatting of a complete DSL file."""
        content = """
# Import statements
import schema.components.memory
import schema.components.rag as tools

# Type definitions
type Person {
  name: string
  age: integer(0..150)
  email: string?
  tags: string[]
  status: Status | string
}

type Address {
  street: string
  city: string
  zipCode: integer(10000..99999)
}

# Enum definitions
enum Status {
  active
  inactive
  pending
  deleted
}

# Agent definition
agent UserProfileAgent {
  id: string
  name: string
  profile: Person
  address: Address
  status: Status
}
"""
        formatted = self.formatter.format(content)
        self.assertIn("type Person {", formatted)
        self.assertIn("type Address {", formatted)
        self.assertIn("enum Status {", formatted)
        self.assertIn("agent UserProfileAgent {", formatted)

    def test_multiple_type_definitions(self):
        """Test formatting of multiple type definitions."""
        content = """
type User {
  name: string
  email: string
}

type Admin {
  name: string
  permissions: string[]
}

type Guest {
  name: string
  maxRequests: integer(1..100)
}
"""
        formatted = self.formatter.format(content)
        self.assertIn("type User {", formatted)
        self.assertIn("type Admin {", formatted)
        self.assertIn("type Guest {", formatted)

    def test_multiple_enum_definitions(self):
        """Test formatting of multiple enum definitions."""
        content = """
enum Status {
  active
  inactive
}

enum Role {
  admin
  user
  guest
}

enum Priority {
  low
  medium
  high
  critical
}
"""
        formatted = self.formatter.format(content)
        self.assertIn("enum Status {", formatted)
        self.assertIn("enum Role {", formatted)
        self.assertIn("enum Priority {", formatted)

    def test_agent_with_complex_fields(self):
        """Test formatting of agent with complex fields."""
        content = """
agent DataProcessor {
  name: string
  input: InputData
  output: OutputData
  config: ProcessingConfig {
    batchSize: integer(1..100)
    timeout: integer(1..3600)
    retryCount: integer(0..10)
  }
  status: ProcessingStatus
}
"""
        formatted = self.formatter.format(content)
        self.assertIn("agent DataProcessor {", formatted)
        self.assertIn("input: InputData", formatted)
        self.assertIn("output: OutputData", formatted)
        self.assertIn("config: ProcessingConfig {", formatted)


# ============================================
# Test Class: TestEdgeCases
# ============================================

class TestEdgeCases(unittest.TestCase):
    """Test edge cases and error handling."""

    def setUp(self):
        """Set up test fixtures."""
        self.parser = GrammarParser()
        self.formatter = DSLFormatter(FormatterConfig())

    def test_empty_dsl_file(self):
        """Test formatting of an empty DSL file."""
        content = ""
        formatted = self.formatter.format(content)
        self.assertEqual(formatted, "")

    def test_dsl_with_only_imports(self):
        """Test formatting of DSL with only imports."""
        content = """
import schema.components.memory
import schema.components.rag
"""
        formatted = self.formatter.format(content)
        self.assertIn("import schema.components.memory", formatted)
        self.assertIn("import schema.components.rag", formatted)

    def test_dsl_with_only_comments(self):
        """Test formatting of DSL with only comments."""
        content = """
# This is a comment
# Another comment
# Third comment
"""
        formatted = self.formatter.format(content)
        self.assertIn("# This is a comment", formatted)
        self.assertIn("# Another comment", formatted)
        self.assertIn("# Third comment", formatted)

    def test_dsl_with_only_whitespace(self):
        """Test formatting of DSL with only whitespace."""
        content = """
    \n\n\n
"""
        formatted = self.formatter.format(content)
        self.assertEqual(formatted, "")

    def test_single_line_type(self):
        """Test formatting of single-line type."""
        content = """
type Person { name: string, age: integer }
"""
        formatted = self.formatter.format(content)
        self.assertIn("type Person {", formatted)
        self.assertIn("name: string", formatted)
        self.assertIn("age: integer", formatted)

    def test_single_line_enum(self):
        """Test formatting of single-line enum."""
        content = """
enum Status { active, inactive, pending }
"""
        formatted = self.formatter.format(content)
        self.assertIn("enum Status {", formatted)
        self.assertIn("active", formatted)
        self.assertIn("inactive", formatted)

    def test_single_line_agent(self):
        """Test formatting of single-line agent."""
        content = """
agent MyAgent { name: string, tools: Tool[] }
"""
        formatted = self.formatter.format(content)
        self.assertIn("agent MyAgent {", formatted)
        self.assertIn("name: string", formatted)

    def test_nested_type_with_no_fields(self):
        """Test formatting of nested type with no fields."""
        content = """
type Outer {
  nested: Nested
}

type Nested {
}
"""
        formatted = self.formatter.format(content)
        self.assertIn("type Outer {", formatted)
        self.assertIn("nested: Nested", formatted)
        self.assertIn("type Nested {", formatted)

    def test_deeply_nested_types(self):
        """Test formatting of deeply nested types."""
        content = """
type Level1 {
  level2: Level2
}

type Level2 {
  level3: Level3
}

type Level3 {
  level4: Level4
}

type Level4 {
  value: string
}
"""
        formatted = self.formatter.format(content)
        self.assertIn("type Level1 {", formatted)
        self.assertIn("type Level2 {", formatted)
        self.assertIn("type Level3 {", formatted)
        self.assertIn("type Level4 {", formatted)

    def test_import_with_empty_path(self):
        """Test formatting of import with empty path."""
        content = """
import
"""
        formatted = self.formatter.format(content)
        self.assertIn("import", formatted)

    def test_type_with_no_body(self):
        """Test formatting of type with no body."""
        content = """
type Empty
"""
        formatted = self.formatter.format(content)
        self.assertIn("type Empty", formatted)

    def test_enum_with_no_values(self):
        """Test formatting of enum with no values."""
        content = """
enum Empty
"""
        formatted = self.formatter.format(content)
        self.assertIn("enum Empty", formatted)

    def test_agent_with_no_fields(self):
        """Test formatting of agent with no fields."""
        content = """
agent Empty
"""
        formatted = self.formatter.format(content)
        self.assertIn("agent Empty", formatted)


# ============================================
# Test Class: TestConvenienceFunctions
# ============================================

class TestConvenienceFunctions(unittest.TestCase):
    """Test convenience functions for formatting."""

    def setUp(self):
        """Set up test fixtures."""
        self.parser = GrammarParser()

    def test_format_dsl_function(self):
        """Test format_dsl() convenience function."""
        content = """
type Person {
  name: string
  age: integer
}
"""
        formatted = format_dsl(content)
        self.assertIn("type Person {", formatted)
        self.assertIn("name: string", formatted)

    def test_format_dsl_with_custom_config(self):
        """Test format_dsl() with custom configuration."""
        content = """
type Person {
  name: string
  age: integer
}
"""
        config = FormatterConfig(indent_size=4, trailing_commas=True)
        formatted = format_dsl(content, config)
        self.assertIn("type Person {", formatted)
        self.assertIn("name: string,", formatted)

    def test_format_dsl_file_function(self):
        """Test format_dsl_file() convenience function."""
        # Create a temporary file
        test_file = Path('/tmp/test_formatter.adl')
        test_file.write_text("""
type Person {
  name: string
  age: integer
}
""")
        try:
            formatted = format_dsl_file(str(test_file))
            self.assertIn("type Person {", formatted)
            self.assertIn("name: string", formatted)
        finally:
            test_file.unlink()

    def test_format_dsl_file_with_custom_config(self):
        """Test format_dsl_file() with custom configuration."""
        # Create a temporary file
        test_file = Path('/tmp/test_formatter_config.adl')
        test_file.write_text("""
type Person {
  name: string
  age: integer
}
""")
        try:
            config = FormatterConfig(indent_size=8, trailing_commas=True)
            formatted = format_dsl_file(str(test_file), config)
            self.assertIn("type Person {", formatted)
            self.assertIn("name: string,", formatted)
        finally:
            test_file.unlink()

    def test_format_dsl_empty_content(self):
        """Test format_dsl() with empty content."""
        formatted = format_dsl("")
        self.assertEqual(formatted, "")

    def test_format_dsl_file_nonexistent(self):
        """Test format_dsl_file() with nonexistent file."""
        formatted = format_dsl_file('/tmp/nonexistent_file.adl')
        self.assertEqual(formatted, "")


# ============================================
# Test Class: TestNewlineAfterDeclaration
# ============================================

class TestNewlineAfterDeclaration(unittest.TestCase):
    """Test newline after declaration feature."""

    def setUp(self):
        """Set up test fixtures."""
        self.parser = GrammarParser()

    def test_newline_after_declaration_enabled(self):
        """Test formatting with newlines after declarations."""
        config = FormatterConfig(newline_after_declaration=True)
        formatter = DSLFormatter(config)
        content = """
type Person {
  name: string
}

type Address {
  street: string
}
"""
        formatted = formatter.format(content)
        lines = formatted.split('\n')
        # Check for empty lines between declarations
        self.assertEqual(lines[2], "")
        self.assertEqual(lines[5], "")

    def test_newline_after_declaration_disabled(self):
        """Test formatting without newlines after declarations."""
        config = FormatterConfig(newline_after_declaration=False)
        formatter = DSLFormatter(config)
        content = """
type Person {
  name: string
}

type Address {
  street: string
}
"""
        formatted = formatter.format(content)
        lines = formatted.split('\n')
        # Check no empty lines between declarations
        self.assertNotEqual(lines[2], "")
        self.assertNotEqual(lines[5], "")

    def test_newline_after_import(self):
        """Test newline after import statement."""
        config = FormatterConfig(newline_after_declaration=True)
        formatter = DSLFormatter(config)
        content = """
import schema.components.memory
import schema.components.rag
"""
        formatted = formatter.format(content)
        lines = formatted.split('\n')
        # Check for empty lines between imports
        self.assertEqual(lines[1], "")

    def test_newline_after_enum(self):
        """Test newline after enum declaration."""
        config = FormatterConfig(newline_after_declaration=True)
        formatter = DSLFormatter(config)
        content = """
enum Status {
  active
  inactive
}

enum Role {
  admin
  user
}
"""
        formatted = formatter.format(content)
        lines = formatted.split('\n')
        # Check for empty lines between enums
        self.assertEqual(lines[4], "")

    def test_newline_after_agent(self):
        """Test newline after agent declaration."""
        config = FormatterConfig(newline_after_declaration=True)
        formatter = DSLFormatter(config)
        content = """
agent MyAgent {
  name: string
}

agent OtherAgent {
  name: string
}
"""
        formatted = formatter.format(content)
        lines = formatted.split('\n')
        # Check for empty lines between agents
        self.assertEqual(lines[4], "")


# ============================================
# Test Class: TestAllASTNodeTypes
# ============================================

class TestAllASTNodeTypes(unittest.TestCase):
    """Test all AST node types are formatted correctly."""

    def setUp(self):
        """Set up test fixtures."""
        self.parser = GrammarParser()
        self.formatter = DSLFormatter(FormatterConfig())

    def test_program_node_formatting(self):
        """Test Program node formatting."""
        content = """
import schema.components.memory
type Person {
  name: string
}
"""
        formatted = self.formatter.format(content)
        self.assertIn("import schema.components.memory", formatted)
        self.assertIn("type Person {", formatted)

    def test_import_stmt_node_formatting(self):
        """Test ImportStmt node formatting."""
        content = """
import schema.components.memory as mem
"""
        formatted = self.formatter.format(content)
        self.assertIn("import schema.components.memory as mem", formatted)

    def test_enum_def_node_formatting(self):
        """Test EnumDef node formatting."""
        content = """
enum Status {
  active
  inactive
}
"""
        formatted = self.formatter.format(content)
        self.assertIn("enum Status {", formatted)
        self.assertIn("active", formatted)
        self.assertIn("inactive", formatted)

    def test_type_def_node_formatting(self):
        """Test TypeDef node formatting."""
        content = """
type Person {
  name: string
  age: integer
}
"""
        formatted = self.formatter.format(content)
        self.assertIn("type Person {", formatted)
        self.assertIn("name: string", formatted)
        self.assertIn("age: integer", formatted)

    def test_type_body_node_formatting(self):
        """Test TypeBody node formatting."""
        content = """
type Person {
  name: string
  age: integer
}
"""
        formatted = self.formatter.format(content)
        self.assertIn("name: string", formatted)
        self.assertIn("age: integer", formatted)

    def test_field_def_node_formatting(self):
        """Test FieldDef node formatting."""
        content = """
type Person {
  name: string
  age: integer
}
"""
        formatted = self.formatter.format(content)
        self.assertIn("name: string", formatted)
        self.assertIn("age: integer", formatted)

    def test_agent_def_node_formatting(self):
        """Test AgentDef node formatting."""
        content = """
agent MyAgent {
  name: string
  tools: Tool[]
}
"""
        formatted = self.formatter.format(content)
        self.assertIn("agent MyAgent {", formatted)
        self.assertIn("name: string", formatted)
        self.assertIn("tools: Tool[]", formatted)

    def test_primitive_type_node_formatting(self):
        """Test PrimitiveType node formatting."""
        content = """
type Person {
  name: string
}
"""
        formatted = self.formatter.format(content)
        self.assertIn("string", formatted)

    def test_type_reference_node_formatting(self):
        """Test TypeReference node formatting."""
        content = """
type Person {
  address: Address
}
"""
        formatted = self.formatter.format(content)
        self.assertIn("Address", formatted)

    def test_array_type_node_formatting(self):
        """Test ArrayType node formatting."""
        content = """
type Person {
  tags: string[]
}
"""
        formatted = self.formatter.format(content)
        self.assertIn("string[]", formatted)

    def test_union_type_node_formatting(self):
        """Test UnionType node formatting."""
        content = """
type Person {
  status: string | integer
}
"""
        formatted = self.formatter.format(content)
        self.assertIn("string | integer", formatted)

    def test_optional_type_node_formatting(self):
        """Test OptionalType node formatting."""
        content = """
type Person {
  middleName?: string
}
"""
        formatted = self.formatter.format(content)
        self.assertIn("middleName?: string", formatted)

    def test_constrained_type_node_formatting(self):
        """Test ConstrainedType node formatting."""
        content = """
type Person {
  age: integer(0..150)
}
"""
        formatted = self.formatter.format(content)
        self.assertIn("integer(0..150)", formatted)


# ============================================
# Test Class: TestMixedFeatures
# ============================================

class TestMixedFeatures(unittest.TestCase):
    """Test combination of multiple formatting features."""

    def setUp(self):
        """Set up test fixtures."""
        self.parser = GrammarParser()

    def test_all_features_combined(self):
        """Test all formatting features combined."""
        config = FormatterConfig(
            indent_size=2,
            max_line_length=100,
            trailing_commas=True,
            sort_imports=True,
            preserve_comments=True,
            newline_after_declaration=True
        )
        formatter = DSLFormatter(config)
        content = """
# Import statements
import schema.components.memory
import schema.components.rag as tools

# Type definitions
type Person {
  name: string,
  age: integer(0..150),
  email: string?,
  tags: string[],
  status: Status | string
}

type Address {
  street: string,
  city: string,
  zipCode: integer(10000..99999)
}

# Enum definitions
enum Status {
  active,
  inactive,
  pending,
  deleted
}

# Agent definition
agent UserProfileAgent {
  id: string,
  name: string,
  profile: Person,
  address: Address,
  status: Status
}
"""
        formatted = formatter.format(content)
        # Check all features are applied
        self.assertIn("# Import statements", formatted)
        self.assertIn("import schema.components.memory", formatted)
        self.assertIn("import schema.components.rag as tools", formatted)
        self.assertIn("type Person {", formatted)
        self.assertIn("name: string,", formatted)
        self.assertIn("age: integer(0..150),", formatted)
        self.assertIn("email: string?,", formatted)
        self.assertIn("tags: string[],", formatted)
        self.assertIn("status: Status | string", formatted)
        self.assertIn("type Address {", formatted)
        self.assertIn("enum Status {", formatted)
        self.assertIn("active,", formatted)
        self.assertIn("inactive,", formatted)
        self.assertIn("agent UserProfileAgent {", formatted)
        self.assertIn("id: string,", formatted)

    def test_complex_nested_structure(self):
        """Test complex nested structure with all features."""
        config = FormatterConfig(
            indent_size=2,
            trailing_commas=True,
            preserve_comments=True
        )
        formatter = DSLFormatter(config)
        content = """
# Complex nested structure
type Outer {
  name: string
  nested: Inner {
    value: string
    nested2: Inner2 {
      data: string
    }
  }
}

type Inner {
  field1: string
  field2: integer
}

type Inner2 {
  data: string
}
"""
        formatted = formatter.format(content)
        self.assertIn("type Outer {", formatted)
        self.assertIn("nested: Inner {", formatted)
        self.assertIn("nested2: Inner2 {", formatted)
        self.assertIn("data: string", formatted)


if __name__ == '__main__':
    unittest.main()