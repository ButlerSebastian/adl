"""
Tests for ADL DSL JSON Schema Generator
"""

import pytest
import json
from tools.dsl.parser import GrammarParser


class TestJSONSchemaGenerator:
    """Test JSON Schema generation from ADL DSL."""

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
        schema = parser.generate_json_schema(program)

        assert schema["properties"]["str_field"]["type"] == "string"
        assert schema["properties"]["int_field"]["type"] == "integer"
        assert schema["properties"]["num_field"]["type"] == "number"
        assert schema["properties"]["bool_field"]["type"] == "boolean"
        assert schema["properties"]["obj_field"]["type"] == "object"
        assert schema["properties"]["arr_field"]["type"] == "array"
        assert schema["properties"]["any_field"] == {}
        assert schema["properties"]["null_field"]["type"] == "null"

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
        schema = parser.generate_json_schema(program)

        assert schema["properties"]["person"]["$ref"] == "#/$defs/Person"
        assert "Person" in schema["$defs"]
        assert schema["$defs"]["Person"]["type"] == "object"

    def test_array_type(self, parser):
        """Test generation of array types."""
        content = """
agent TestAgent {
  names: string[]
  ages: integer[]
}
"""
        program = parser.parse(content)
        schema = parser.generate_json_schema(program)

        assert schema["properties"]["names"]["type"] == "array"
        assert schema["properties"]["names"]["items"]["type"] == "string"
        assert schema["properties"]["ages"]["type"] == "array"
        assert schema["properties"]["ages"]["items"]["type"] == "integer"

    def test_union_type(self, parser):
        """Test generation of union types."""
        content = """
agent TestAgent {
  value: string | integer
}
"""
        program = parser.parse(content)
        schema = parser.generate_json_schema(program)

        assert "anyOf" in schema["properties"]["value"]
        assert len(schema["properties"]["value"]["anyOf"]) == 2
        assert schema["properties"]["value"]["anyOf"][0]["type"] == "string"
        assert schema["properties"]["value"]["anyOf"][1]["type"] == "integer"

    def test_optional_type(self, parser):
        """Test generation of optional types."""
        content = """
agent TestAgent {
  required_field: string
  optional_field?: string
}
"""
        program = parser.parse(content)
        schema = parser.generate_json_schema(program)

        assert "required_field" in schema["required"]
        assert "optional_field" not in schema["required"]
        assert schema["properties"]["optional_field"]["type"] == "string"
        assert schema["properties"]["optional_field"]["nullable"] is True

    def test_constrained_type_min_only(self, parser):
        """Test generation of constrained type with min only."""
        content = """
agent TestAgent {
  value: integer (1..)
}
"""
        program = parser.parse(content)
        schema = parser.generate_json_schema(program)

        assert schema["properties"]["value"]["type"] == "integer"
        assert schema["properties"]["value"]["minimum"] == 1
        assert "maximum" not in schema["properties"]["value"]

    def test_constrained_type_max_only(self, parser):
        """Test generation of constrained type with max only."""
        content = """
agent TestAgent {
  value: integer (..100)
}
"""
        program = parser.parse(content)
        schema = parser.generate_json_schema(program)

        assert schema["properties"]["value"]["type"] == "integer"
        assert schema["properties"]["value"]["maximum"] == 100
        assert "minimum" not in schema["properties"]["value"]

    def test_constrained_type_min_and_max(self, parser):
        """Test generation of constrained type with min and max."""
        content = """
agent TestAgent {
  value: integer (1..100)
}
"""
        program = parser.parse(content)
        schema = parser.generate_json_schema(program)

        assert schema["properties"]["value"]["type"] == "integer"
        assert schema["properties"]["value"]["minimum"] == 1
        assert schema["properties"]["value"]["maximum"] == 100

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
        schema = parser.generate_json_schema(program)

        assert "Status" in schema["$defs"]
        assert schema["$defs"]["Status"]["type"] == "string"
        assert schema["$defs"]["Status"]["enum"] == ["active", "inactive"]
        assert schema["properties"]["status"]["$ref"] == "#/$defs/Status"

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
        schema = parser.generate_json_schema(program)

        assert "Person" in schema["$defs"]
        assert schema["$defs"]["Person"]["type"] == "object"
        assert schema["$defs"]["Person"]["properties"]["name"]["type"] == "string"
        assert schema["$defs"]["Person"]["properties"]["age"]["type"] == "integer"
        assert schema["$defs"]["Person"]["required"] == ["name", "age"]
        assert schema["$defs"]["Person"]["additionalProperties"] is False

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
        schema = parser.generate_json_schema(program)

        assert "Address" in schema["$defs"]
        assert "Person" in schema["$defs"]
        assert schema["$defs"]["Person"]["properties"]["address"]["$ref"] == "#/$defs/Address"

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
        schema = parser.generate_json_schema(program)

        assert schema["properties"]["people"]["type"] == "array"
        assert schema["properties"]["people"]["items"]["$ref"] == "#/$defs/Person"

    def test_complex_schema(self, parser):
        """Test generation of complex schema with all features."""
        content = """
enum Status {
  active
  inactive
}

type Person {
  name: string
  age: integer (0..150)
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
        schema = parser.generate_json_schema(program)

        # Check enum
        assert "Status" in schema["$defs"]
        assert schema["$defs"]["Status"]["enum"] == ["active", "inactive"]

        # Check type definition
        assert "Person" in schema["$defs"]
        assert schema["$defs"]["Person"]["properties"]["age"]["minimum"] == 0
        assert schema["$defs"]["Person"]["properties"]["age"]["maximum"] == 150
        assert schema["$defs"]["Person"]["properties"]["tags"]["type"] == "array"
        assert schema["$defs"]["Person"]["properties"]["tags"]["items"]["type"] == "string"
        assert "optional_field" not in schema["$defs"]["Person"]["required"]

        # Check agent
        assert schema["properties"]["id"]["type"] == "string"
        assert schema["properties"]["person"]["$ref"] == "#/$defs/Person"
        assert schema["properties"]["scores"]["type"] == "array"
        assert schema["properties"]["scores"]["items"]["type"] == "number"

    def test_schema_metadata(self, parser):
        """Test that schema includes proper metadata."""
        content = """
agent TestAgent {
  id: string
}
"""
        program = parser.parse(content)
        schema = parser.generate_json_schema(program)

        assert schema["$schema"] == "https://json-schema.org/draft/2020-12/schema"
        assert schema["$id"] == "https://example.com/schemas/agent-definition.json"
        assert schema["title"] == "Agent Definition"
        assert schema["type"] == "object"
        assert schema["additionalProperties"] is False

    def test_required_fields(self, parser):
        """Test that required fields are correctly identified."""
        content = """
agent TestAgent {
  required1: string
  required2: integer
  optional1?: string
  optional2?: integer
}
"""
        program = parser.parse(content)
        schema = parser.generate_json_schema(program)

        assert "required1" in schema["required"]
        assert "required2" in schema["required"]
        assert "optional1" not in schema["required"]
        assert "optional2" not in schema["required"]

    def test_json_schema_serialization(self, parser):
        """Test that schema can be serialized to JSON."""
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
        schema = parser.generate_json_schema(program)

        json_str = json.dumps(schema)
        assert json_str is not None
        assert len(json_str) > 0

        parsed_schema = json.loads(json_str)
        assert parsed_schema == schema
