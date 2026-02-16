"""
Tests for ADL DSL Semantic Validator
"""

import pytest
from tools.dsl.parser import GrammarParser
from tools.dsl.validator import ValidationError


class TestSemanticValidator:
    """Test semantic validation of ADL DSL."""

    @pytest.fixture
    def parser(self):
        """Create a parser instance."""
        return GrammarParser()

    def test_valid_type_definition(self, parser):
        """Test validation of valid type definition."""
        content = """
type Test {
  name: string
  age: integer
}
"""
        program = parser.parse(content)
        errors = parser.validate(program)
        assert len(errors) == 0

    def test_duplicate_field_names_in_type(self, parser):
        """Test detection of duplicate field names in type."""
        content = """
type Test {
  name: string
  name: integer
}
"""
        program = parser.parse(content)
        errors = parser.validate(program)
        assert len(errors) == 1
        assert errors[0].error_code == "DUPLICATE_FIELD"
        assert "name" in errors[0].message

    def test_duplicate_field_names_in_agent(self, parser):
        """Test detection of duplicate field names in agent."""
        content = """
agent TestAgent {
  id: string
  id: integer
}
"""
        program = parser.parse(content)
        errors = parser.validate(program)
        assert len(errors) == 1
        assert errors[0].error_code == "DUPLICATE_FIELD"
        assert "id" in errors[0].message

    def test_duplicate_enum_values(self, parser):
        """Test detection of duplicate enum values."""
        content = """
enum Test {
  value1
  value2
  value1
}
"""
        program = parser.parse(content)
        errors = parser.validate(program)
        assert len(errors) == 1
        assert errors[0].error_code == "DUPLICATE_ENUM_VALUE"
        assert "value1" in errors[0].message

    def test_duplicate_type_definitions(self, parser):
        """Test detection of duplicate type definitions."""
        content = """
type Test {
  name: string
}

type Test {
  age: integer
}
"""
        program = parser.parse(content)
        errors = parser.validate(program)
        assert len(errors) == 1
        assert errors[0].error_code == "DUPLICATE_TYPE"
        assert "Test" in errors[0].message

    def test_duplicate_enum_definitions(self, parser):
        """Test detection of duplicate enum definitions."""
        content = """
enum Test {
  value1
}

enum Test {
  value2
}
"""
        program = parser.parse(content)
        errors = parser.validate(program)
        assert len(errors) == 1
        assert errors[0].error_code == "DUPLICATE_ENUM"
        assert "Test" in errors[0].message

    def test_invalid_type_reference(self, parser):
        """Test detection of invalid type reference."""
        content = """
type Test {
  value: InvalidType
}
"""
        program = parser.parse(content)
        errors = parser.validate(program)
        assert len(errors) == 1
        assert errors[0].error_code == "INVALID_TYPE_REFERENCE"
        assert "InvalidType" in errors[0].message

    def test_valid_primitive_type_reference(self, parser):
        """Test that primitive type references are valid."""
        content = """
type Test {
  str: string
  int: integer
  num: number
  bool: boolean
  obj: object
  arr: array
  any_val: any
  null_val: null
}
"""
        program = parser.parse(content)
        errors = parser.validate(program)
        assert len(errors) == 0

    def test_valid_type_reference_to_defined_type(self, parser):
        """Test that references to defined types are valid."""
        content = """
type Person {
  name: string
}

type Test {
  person: Person
}
"""
        program = parser.parse(content)
        errors = parser.validate(program)
        assert len(errors) == 0

    def test_valid_type_reference_to_defined_enum(self, parser):
        """Test that references to defined enums are valid."""
        content = """
enum Status {
  active
  inactive
}

type Test {
  status: Status
}
"""
        program = parser.parse(content)
        errors = parser.validate(program)
        assert len(errors) == 0

    def test_invalid_constraint_range_min_greater_than_max(self, parser):
        """Test detection of invalid constraint range (min > max)."""
        content = """
type Test {
  value: integer (100..1)
}
"""
        program = parser.parse(content)
        errors = parser.validate(program)
        assert len(errors) == 1
        assert errors[0].error_code == "INVALID_CONSTRAINT_RANGE"
        assert "100" in errors[0].message
        assert "1" in errors[0].message

    def test_valid_constraint_range_min_only(self, parser):
        """Test that min-only constraint is valid."""
        content = """
type Test {
  value: integer (1..)
}
"""
        program = parser.parse(content)
        errors = parser.validate(program)
        assert len(errors) == 0

    def test_valid_constraint_range_max_only(self, parser):
        """Test that max-only constraint is valid."""
        content = """
type Test {
  value: integer (..100)
}
"""
        program = parser.parse(content)
        errors = parser.validate(program)
        assert len(errors) == 0

    def test_valid_constraint_range_min_and_max(self, parser):
        """Test that min-max constraint is valid."""
        content = """
type Test {
  value: integer (1..100)
}
"""
        program = parser.parse(content)
        errors = parser.validate(program)
        assert len(errors) == 0

    def test_invalid_type_reference_in_array(self, parser):
        """Test detection of invalid type reference in array."""
        content = """
type Test {
  values: InvalidType[]
}
"""
        program = parser.parse(content)
        errors = parser.validate(program)
        assert len(errors) == 1
        assert errors[0].error_code == "INVALID_TYPE_REFERENCE"
        assert "InvalidType" in errors[0].message

    def test_invalid_type_reference_in_union(self, parser):
        """Test detection of invalid type reference in union."""
        content = """
type Test {
  value: string | InvalidType
}
"""
        program = parser.parse(content)
        errors = parser.validate(program)
        assert len(errors) == 1
        assert errors[0].error_code == "INVALID_TYPE_REFERENCE"
        assert "InvalidType" in errors[0].message

    def test_invalid_type_reference_in_optional(self, parser):
        """Test detection of invalid type reference in optional."""
        content = """
type Test {
  value?: InvalidType
}
"""
        program = parser.parse(content)
        errors = parser.validate(program)
        assert len(errors) == 1
        assert errors[0].error_code == "INVALID_TYPE_REFERENCE"
        assert "InvalidType" in errors[0].message

    def test_invalid_type_reference_in_constrained(self, parser):
        """Test detection of invalid type reference in constrained type."""
        content = """
type Test {
  value: InvalidType (1..100)
}
"""
        program = parser.parse(content)
        errors = parser.validate(program)
        assert len(errors) == 1
        assert errors[0].error_code == "INVALID_TYPE_REFERENCE"
        assert "InvalidType" in errors[0].message

    def test_multiple_errors(self, parser):
        """Test detection of multiple errors."""
        content = """
type Test {
  name: string
  name: integer
  age: InvalidType
}
"""
        program = parser.parse(content)
        errors = parser.validate(program)
        assert len(errors) == 2
        error_codes = {e.error_code for e in errors}
        assert "DUPLICATE_FIELD" in error_codes
        assert "INVALID_TYPE_REFERENCE" in error_codes

    def test_complex_valid_program(self, parser):
        """Test validation of complex valid program."""
        content = """
enum Status {
  active
  inactive
}

type Person {
  name: string
  age: integer
}

type Config {
  timeout: integer (1..60)
  enabled: boolean
}

agent TestAgent {
  id: string
  name: string
  status: Status
  config: Config
}
"""
        program = parser.parse(content)
        errors = parser.validate(program)
        assert len(errors) == 0

    def test_error_location_information(self, parser):
        """Test that errors include location information."""
        content = """
type Test {
  name: string
  name: integer
}
"""
        program = parser.parse(content)
        errors = parser.validate(program)
        assert len(errors) == 1
        assert errors[0].location.line is not None
        assert errors[0].location.column is not None
