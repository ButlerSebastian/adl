"""
Tests for ADL DSL Python Generator
"""

import pytest
from tools.dsl.parser import GrammarParser


class TestPythonGenerator:
    """Test Python type generation from ADL DSL."""

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
        py_code = parser.generate_python(program)

        assert "str_field: Required[str]" in py_code
        assert "int_field: Required[int]" in py_code
        assert "num_field: Required[float]" in py_code
        assert "bool_field: Required[bool]" in py_code
        assert "obj_field: Required[Dict[str, Any]]" in py_code
        assert "arr_field: Required[List[Any]]" in py_code
        assert "any_field: Required[Any]" in py_code
        assert "null_field: Required[None]" in py_code

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
        py_code = parser.generate_python(program)

        assert "class Person(TypedDict):" in py_code
        assert "person: Required[Person]" in py_code

    def test_array_type(self, parser):
        """Test generation of array types."""
        content = """
agent TestAgent {
  names: string[]
  ages: integer[]
}
"""
        program = parser.parse(content)
        py_code = parser.generate_python(program)

        assert "names: Required[List[str]]" in py_code
        assert "ages: Required[List[int]]" in py_code

    def test_union_type(self, parser):
        """Test generation of union types."""
        content = """
agent TestAgent {
  value: string | integer
}
"""
        program = parser.parse(content)
        py_code = parser.generate_python(program)

        assert "value: Required[Union[str, int]]" in py_code

    def test_optional_type(self, parser):
        """Test generation of optional types."""
        content = """
agent TestAgent {
  required_field: string
  optional_field?: string
}
"""
        program = parser.parse(content)
        py_code = parser.generate_python(program)

        assert "required_field: Required[str]" in py_code
        assert "optional_field: NotRequired[str]" in py_code

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
        py_code = parser.generate_python(program)

        assert "class Status(str):" in py_code
        assert '"active",' in py_code
        assert '"inactive",' in py_code
        assert "status: Required[Status]" in py_code

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
        py_code = parser.generate_python(program)

        assert "class Person(TypedDict):" in py_code
        assert "name: Required[str]" in py_code
        assert "age: Required[int]" in py_code
        assert "person: Required[Person]" in py_code

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
        py_code = parser.generate_python(program)

        assert "class Address(TypedDict):" in py_code
        assert "class Person(TypedDict):" in py_code
        assert "address: Required[Address]" in py_code

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
        py_code = parser.generate_python(program)

        assert "people: Required[List[Person]]" in py_code

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
        py_code = parser.generate_python(program)

        assert "class Status(str):" in py_code
        assert "class Person(TypedDict):" in py_code
        assert "class TestAgent(TypedDict):" in py_code
        assert "status: Required[Status]" in py_code
        assert "tags: Required[List[str]]" in py_code
        assert "optional_field: NotRequired[str]" in py_code
        assert "scores: Required[List[float]]" in py_code

    def test_imports(self, parser):
        """Test that proper imports are included."""
        content = """
type Person {
  name: string
}

agent TestAgent {
  id: string
}
"""
        program = parser.parse(content)
        py_code = parser.generate_python(program)

        assert "from typing import List, Optional, Union, TypedDict, Any" in py_code

    def test_typed_dict_syntax(self, parser):
        """Test that TypedDict syntax is correct."""
        content = """
type Person {
  name: string
  age: integer
}

agent TestAgent {
  id: string
}
"""
        program = parser.parse(content)
        py_code = parser.generate_python(program)

        assert "class Person(TypedDict):" in py_code
        assert "class TestAgent(TypedDict):" in py_code
        assert "name: Required[str]" in py_code
        assert "age: Required[int]" in py_code
        assert "id: Required[str]" in py_code

    def test_required_fields(self, parser):
        """Test that required fields use Required."""
        content = """
agent TestAgent {
  required1: string
  required2: integer
  optional1?: string
  optional2?: integer
}
"""
        program = parser.parse(content)
        py_code = parser.generate_python(program)

        assert "required1: Required[str]" in py_code
        assert "required2: Required[int]" in py_code
        assert "optional1: NotRequired[str]" in py_code
        assert "optional2: NotRequired[int]" in py_code

    def test_python_syntax(self, parser):
        """Test that generated Python is syntactically valid."""
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
        py_code = parser.generate_python(program)

        assert "from typing import List, Optional, Union, TypedDict, Any" in py_code
        assert "class Person(TypedDict):" in py_code
        assert "class TestAgent(TypedDict):" in py_code
        assert "name: Required[str]" in py_code
        assert "age: Required[int]" in py_code
        assert "id: Required[str]" in py_code
        assert "person: Required[Person]" in py_code
        assert py_code.count("class ") == 2
