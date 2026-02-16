"""
Tests for ADL DSL TypeScript Generator
"""

import pytest
from tools.dsl.parser import GrammarParser


class TestTypeScriptGenerator:
    """Test TypeScript type generation from ADL DSL."""

    @pytest.fixture
    def parser(self):
        """Create a parser instance."""
        return GrammarParser()

    def test_primitive_types(self, parser):
        """Test generation of primitive types."""
        content = """
agent TestAgent {
  str_field: string
  int_field: integer
  num_field: number
  bool_field: boolean
  obj_field: object
  arr_field: array
  any_field: any
  null_field: null
}
"""
        program = parser.parse(content)
        ts_code = parser.generate_typescript(program)

        assert "str_field: string;" in ts_code
        assert "int_field: number;" in ts_code
        assert "num_field: number;" in ts_code
        assert "bool_field: boolean;" in ts_code
        assert "obj_field: Record<string, any>;" in ts_code
        assert "arr_field: any[];" in ts_code
        assert "any_field: any;" in ts_code
        assert "null_field: null;" in ts_code

    def test_type_reference(self, parser):
        """Test generation of type references."""
        content = """
type Person {
  name: string
}

agent TestAgent {
  person: Person
}
"""
        program = parser.parse(content)
        ts_code = parser.generate_typescript(program)

        assert "export interface Person" in ts_code
        assert "person: Person;" in ts_code

    def test_array_type(self, parser):
        """Test generation of array types."""
        content = """
agent TestAgent {
  names: string[]
  ages: integer[]
}
"""
        program = parser.parse(content)
        ts_code = parser.generate_typescript(program)

        assert "names: string[];" in ts_code
        assert "ages: number[];" in ts_code

    def test_union_type(self, parser):
        """Test generation of union types."""
        content = """
agent TestAgent {
  value: string | integer
}
"""
        program = parser.parse(content)
        ts_code = parser.generate_typescript(program)

        assert "value: string | number;" in ts_code

    def test_optional_type(self, parser):
        """Test generation of optional types."""
        content = """
agent TestAgent {
  required_field: string
  optional_field?: string
}
"""
        program = parser.parse(content)
        ts_code = parser.generate_typescript(program)

        assert "required_field: string;" in ts_code
        assert "optional_field?: string;" in ts_code

    def test_enum_definition(self, parser):
        """Test generation of enum definitions."""
        content = """
enum Status {
  active
  inactive
}

agent TestAgent {
  status: Status
}
"""
        program = parser.parse(content)
        ts_code = parser.generate_typescript(program)

        assert "export enum Status {" in ts_code
        assert "active," in ts_code
        assert "inactive," in ts_code
        assert "status: Status;" in ts_code

    def test_type_definition(self, parser):
        """Test generation of type definitions."""
        content = """
type Person {
  name: string
  age: integer
}

agent TestAgent {
  person: Person
}
"""
        program = parser.parse(content)
        ts_code = parser.generate_typescript(program)

        assert "export interface Person {" in ts_code
        assert "name: string;" in ts_code
        assert "age: number;" in ts_code
        assert "person: Person;" in ts_code

    def test_nested_type_reference(self, parser):
        """Test generation of nested type references."""
        content = """
type Address {
  street: string
  city: string
}

type Person {
  name: string
  address: Address
}

agent TestAgent {
  person: Person
}
"""
        program = parser.parse(content)
        ts_code = parser.generate_typescript(program)

        assert "export interface Address {" in ts_code
        assert "export interface Person {" in ts_code
        assert "address: Address;" in ts_code

    def test_array_of_type_reference(self, parser):
        """Test generation of array of type references."""
        content = """
type Person {
  name: string
}

agent TestAgent {
  people: Person[]
}
"""
        program = parser.parse(content)
        ts_code = parser.generate_typescript(program)

        assert "people: Person[];" in ts_code

    def test_complex_schema(self, parser):
        """Test generation of complex schema with all features."""
        content = """
enum Status {
  active
  inactive
}

type Person {
  name: string
  age: integer
  status: Status
  tags: string[]
  optional_field?: string
}

agent TestAgent {
  id: string
  name: string
  person: Person
  scores: number[]
}
"""
        program = parser.parse(content)
        ts_code = parser.generate_typescript(program)

        assert "export enum Status {" in ts_code
        assert "export interface Person {" in ts_code
        assert "export type TestAgent = {" in ts_code
        assert "status: Status;" in ts_code
        assert "tags: string[];" in ts_code
        assert "optional_field?: string;" in ts_code
        assert "scores: number[];" in ts_code

    def test_export_keywords(self, parser):
        """Test that export keywords are present."""
        content = """
type Person {
  name: string
}

enum Status {
  active
}

agent TestAgent {
  id: string
}
"""
        program = parser.parse(content)
        ts_code = parser.generate_typescript(program)

        assert "export interface Person" in ts_code
        assert "export enum Status" in ts_code
        assert "export type TestAgent" in ts_code

    def test_required_fields(self, parser):
        """Test that required fields don't have ? operator."""
        content = """
agent TestAgent {
  required1: string
  required2: integer
  optional1?: string
  optional2?: integer
}
"""
        program = parser.parse(content)
        ts_code = parser.generate_typescript(program)

        assert "required1: string;" in ts_code
        assert "required2: number;" in ts_code
        assert "optional1?: string;" in ts_code
        assert "optional2?: number;" in ts_code

    def test_typescript_syntax(self, parser):
        """Test that generated TypeScript is syntactically valid."""
        content = """
type Person {
  name: string
  age: integer
}

agent TestAgent {
  id: string
  person: Person
}
"""
        program = parser.parse(content)
        ts_code = parser.generate_typescript(program)

        assert "export interface Person {" in ts_code
        assert "export type TestAgent = {" in ts_code
        assert ts_code.count("{") == ts_code.count("}")
        assert ts_code.count(";") >= 2
