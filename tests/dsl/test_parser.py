"""
Parser Tests for ADL DSL

Comprehensive tests for the GrammarParser.parse() method covering:
- Import statements
- Enum definitions
- Type definitions
- Agent definitions
- Type expressions
- Error cases
"""

import pytest
from pathlib import Path
from tools.dsl.parser import GrammarParser, ParseError
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
)


# ============================================
# Fixtures
# ============================================

@pytest.fixture
def parser():
    """Create a parser instance for testing."""
    return GrammarParser()


@pytest.fixture
def minimal_adl():
    """Minimal ADL content for testing."""
    return """
type Person {
  name: string
  age: integer
}

type Address {
  street: string
  city: string
  zip: string
}

agent MinimalAgent {
  id: string
  name: string
  version: integer
}
"""


# ============================================
# Import Statement Tests
# ============================================

class TestImportStatements:
    """Test import statement parsing."""

    def test_absolute_import(self, parser):
        """Test absolute import path."""
        content = "import schema/components/rag"
        result = parser.parse(content)
        assert isinstance(result, Program)
        assert len(result.imports) == 1
        assert result.imports[0].path == "schema/components/rag"
        assert result.imports[0].alias is None

    def test_import_with_alias(self, parser):
        """Test import with alias."""
        content = "import schema/components/tool as tools"
        result = parser.parse(content)
        assert isinstance(result, Program)
        assert len(result.imports) == 1
        assert result.imports[0].path == "schema/components/tool"
        assert result.imports[0].alias == "tools"

    def test_multiple_imports(self, parser):
        """Test multiple import statements."""
        content = """
import schema/components/rag
import schema/components/tool as tools
import schema.components.memory
"""
        result = parser.parse(content)
        assert isinstance(result, Program)
        assert len(result.imports) == 3
        assert result.imports[0].path == "schema/components/rag"
        assert result.imports[1].path == "schema/components/tool"
        assert result.imports[1].alias == "tools"
        assert result.imports[2].path == "schema.components.memory"

    def test_relative_imports(self, parser):
        """Test relative import paths."""
        content = """
import .utils
import ..config
import schema.components.rag
import schema.components.tool as t
"""
        result = parser.parse(content)
        assert isinstance(result, Program)
        assert len(result.imports) == 4
        assert result.imports[0].path == ".utils"
        assert result.imports[1].path == "..config"
        assert result.imports[2].path == "schema.components.rag"
        assert result.imports[3].path == "schema.components.tool"
        assert result.imports[3].alias == "t"

    def test_import_with_type_definitions(self, parser):
        """Test imports followed by type definitions."""
        content = """
import schema/components/rag
import schema/components/tool as tools

type Config {
  api_key: string
  timeout: integer
}

agent TestAgent {
  id: string
  name: string
}
"""
        result = parser.parse(content)
        assert isinstance(result, Program)
        assert len(result.imports) == 2
        assert len(result.declarations) == 1  # TypeDef
        assert isinstance(result.agent, AgentDef)


# ============================================
# Enum Definition Tests
# ============================================

class TestEnumDefinitions:
    """Test enum definition parsing."""

    def test_simple_enum(self, parser):
        """Test simple enum definition."""
        content = "enum Lifecycle { stable, beta, deprecated, experimental }"
        result = parser.parse(content)
        assert isinstance(result, Program)
        assert len(result.declarations) == 1
        enum_def = result.declarations[0]
        assert isinstance(enum_def, EnumDef)
        assert enum_def.name == "Lifecycle"
        assert enum_def.values == ["stable", "beta", "deprecated", "experimental"]

    def test_enum_with_values(self, parser):
        """Test enum with multiple values."""
        content = """
enum ChangeType {
  breaking
  non-breaking
  patch
}
"""
        result = parser.parse(content)
        assert isinstance(result, Program)
        enum_def = result.declarations[0]
        assert enum_def.name == "ChangeType"
        assert enum_def.values == ["breaking", "non-breaking", "patch"]

    def test_multiple_enums(self, parser):
        """Test multiple enum definitions."""
        content = """
enum Lifecycle {
  stable
  beta
  deprecated
}

enum ChangeType {
  breaking
  non-breaking
  patch
}

enum MemoryType {
  episodic
  semantic
  working
  hybrid
}
"""
        result = parser.parse(content)
        assert isinstance(result, Program)
        assert len(result.declarations) == 3
        assert result.declarations[0].name == "Lifecycle"
        assert result.declarations[1].name == "ChangeType"
        assert result.declarations[2].name == "MemoryType"

    def test_enum_with_imports(self, parser):
        """Test enums with imports."""
        content = """
import schema/components/rag

enum Lifecycle {
  stable
  beta
  deprecated
}

type Config {
  api_key: string
}
"""
        result = parser.parse(content)
        assert isinstance(result, Program)
        assert len(result.imports) == 1
        assert len(result.declarations) == 2
        assert result.declarations[0].name == "Lifecycle"
        assert result.declarations[1].name == "Config"


# ============================================
# Type Definition Tests
# ============================================

class TestTypeDefinitions:
    """Test type definition parsing."""

    def test_simple_type(self, parser):
        """Test simple type definition."""
        content = """
type Person {
  name: string
  age: integer
}
"""
        result = parser.parse(content)
        assert isinstance(result, Program)
        assert len(result.declarations) == 1
        type_def = result.declarations[0]
        assert isinstance(type_def, TypeDef)
        assert type_def.name == "Person"
        assert isinstance(type_def.body, TypeBody)
        assert len(type_def.body.fields) == 2
        assert type_def.body.fields[0].name == "name"
        assert type_def.body.fields[0].type.name == "string"
        assert type_def.body.fields[1].name == "age"
        assert type_def.body.fields[1].type.name == "integer"

    def test_type_with_optional_fields(self, parser):
        """Test type with optional fields."""
        content = """
type OptionalFields {
  required: string
  optional?: string
  optional_number?: number
  optional_array?: array
}
"""
        result = parser.parse(content)
        assert isinstance(result, Program)
        type_def = result.declarations[0]
        assert len(type_def.body.fields) == 4
        assert type_def.body.fields[0].optional is False
        assert type_def.body.fields[1].optional is True
        assert type_def.body.fields[2].optional is True
        assert type_def.body.fields[3].optional is True

    def test_nested_type(self, parser):
        """Test nested type references."""
        content = """
type Person {
  name: string
  age: integer
}

type Address {
  street: string
  city: string
  zip: string
}

type User {
  person: Person
  addresses: Address[]
  config: Config
  metadata: object
}
"""
        result = parser.parse(content)
        assert isinstance(result, Program)
        assert len(result.declarations) == 3
        user_type = result.declarations[2]
        assert user_type.name == "User"
        assert len(user_type.body.fields) == 4
        assert isinstance(user_type.body.fields[0].type, TypeReference)
        assert user_type.body.fields[0].type.name == "Person"
        assert isinstance(user_type.body.fields[1].type, ArrayType)
        assert isinstance(user_type.body.fields[1].type.element_type, TypeReference)
        assert user_type.body.fields[1].type.element_type.name == "Address"
        assert isinstance(user_type.body.fields[2].type, TypeReference)
        assert user_type.body.fields[2].type.name == "Config"
        assert isinstance(user_type.body.fields[3].type, PrimitiveType)
        assert user_type.body.fields[3].type.name == "object"

    def test_complex_type(self, parser):
        """Test complex type with all features."""
        content = """
type ComplexType {
  id: string
  name: string
  count: integer (1..)
  price: number (0..1000)
  tags: string[] (1..5)
  optional_field?: string
  value: string | integer | boolean
  nested: NestedConfig
  metadata: object
}
"""
        result = parser.parse(content)
        assert isinstance(result, Program)
        type_def = result.declarations[0]
        assert type_def.name == "ComplexType"
        assert len(type_def.body.fields) == 9

        # Check count field with constraint
        count_field = type_def.body.fields[2]
        assert count_field.name == "count"
        assert isinstance(count_field.type, ConstrainedType)
        assert count_field.type.min_value == 1

        # Check price field with constraint
        price_field = type_def.body.fields[3]
        assert price_field.name == "price"
        assert isinstance(price_field.type, ConstrainedType)
        assert price_field.type.min_value == 0
        assert price_field.type.max_value == 1000

        # Check tags field with array and constraint
        tags_field = type_def.body.fields[4]
        assert tags_field.name == "tags"
        assert isinstance(tags_field.type, ArrayType)
        assert isinstance(tags_field.type.element_type, ConstrainedType)
        assert isinstance(tags_field.type.element_type.base_type, PrimitiveType)
        assert tags_field.type.element_type.base_type.name == "string"
        assert tags_field.type.element_type.min_value == 1
        assert tags_field.type.element_type.max_value == 5

        # Check optional field
        optional_field = type_def.body.fields[5]
        assert optional_field.name == "optional_field"
        assert optional_field.optional is True

        # Check union type
        value_field = type_def.body.fields[6]
        assert value_field.name == "value"
        assert isinstance(value_field.type, UnionType)
        assert len(value_field.type.types) == 3

        # Check nested type reference
        nested_field = type_def.body.fields[7]
        assert nested_field.name == "nested"
        assert isinstance(nested_field.type, TypeReference)
        assert nested_field.type.name == "NestedConfig"

        # Check object type
        metadata_field = type_def.body.fields[8]
        assert metadata_field.name == "metadata"
        assert isinstance(metadata_field.type, PrimitiveType)
        assert metadata_field.type.name == "object"


# ============================================
# Agent Definition Tests
# ============================================

class TestAgentDefinitions:
    """Test agent definition parsing."""

    def test_simple_agent(self, parser):
        """Test simple agent definition."""
        content = """
agent MinimalAgent {
  id: string
  name: string
  version: integer
}
"""
        result = parser.parse(content)
        assert isinstance(result, Program)
        assert isinstance(result.agent, AgentDef)
        assert result.agent.name == "MinimalAgent"
        assert len(result.agent.fields) == 3
        assert result.agent.fields[0].name == "id"
        assert result.agent.fields[1].name == "name"
        assert result.agent.fields[2].name == "version"

    def test_agent_with_all_fields(self, parser):
        """Test agent with all common fields."""
        content = """
agent CompleteAgent {
  id: string
  version: integer
  version_string?: string
  lifecycle?: Lifecycle
  compatibility?: Compatibility
  change_log?: ChangeLog
  name: string
  description: string
  role: string
  llm: string
  llm_settings: LlmSettings
  tools: ToolDefinition[]
  rag: RagIndex[]
  memory?: MemoryDefinition
  owner?: string
  document_index_id?: string
  agent_roles?: AgentRole[]
  execution_constraints?: ExecutionConstraints
  events?: EventDefinition[]
}
"""
        result = parser.parse(content)
        assert isinstance(result, Program)
        agent = result.agent
        assert agent.name == "CompleteAgent"
        assert len(agent.fields) == 19

        # Check required fields
        assert agent.fields[0].name == "id"
        assert agent.fields[1].name == "version"
        assert agent.fields[6].name == "name"
        assert agent.fields[7].name == "description"
        assert agent.fields[8].name == "role"
        assert agent.fields[9].name == "llm"

        # Check optional fields
        assert agent.fields[2].optional is True
        assert agent.fields[3].optional is True
        assert agent.fields[4].optional is True
        assert agent.fields[5].optional is True
        assert agent.fields[10].optional is False  # llm_settings
        assert agent.fields[11].optional is False  # tools
        assert agent.fields[12].optional is False  # rag
        assert agent.fields[13].optional is True
        assert agent.fields[14].optional is True
        assert agent.fields[15].optional is True
        assert agent.fields[16].optional is True
        assert agent.fields[17].optional is True
        assert agent.fields[18].optional is True

    def test_agent_with_types(self, parser):
        """Test agent with typed fields."""
        content = """
type LlmSettings {
  temperature: number
  max_tokens: integer
}

type ToolDefinition {
  name: string
  description: string
  parameters: ToolParameter[]
}

type RagIndex {
  index_id: string
  type: string
}

type MemoryDefinition {
  type: MemoryType
  scope: MemoryScope
}

agent TypedAgent {
  id: string
  name: string
  version: integer
  description: string
  role: string
  llm: string
  llm_settings: LlmSettings
  tools: ToolDefinition[]
  rag: RagIndex[]
  memory: MemoryDefinition
  owner: string
}
"""
        result = parser.parse(content)
        assert isinstance(result, Program)
        agent = result.agent
        assert agent.name == "TypedAgent"
        assert len(agent.fields) == 11

        # Check typed fields
        llm_settings_field = agent.fields[6]
        assert isinstance(llm_settings_field.type, TypeReference)
        assert llm_settings_field.type.name == "LlmSettings"

        tools_field = agent.fields[7]
        assert isinstance(tools_field.type, ArrayType)
        assert isinstance(tools_field.type.element_type, TypeReference)
        assert tools_field.type.element_type.name == "ToolDefinition"

        rag_field = agent.fields[8]
        assert isinstance(rag_field.type, ArrayType)
        assert isinstance(rag_field.type.element_type, TypeReference)
        assert rag_field.type.element_type.name == "RagIndex"

        memory_field = agent.fields[9]
        assert isinstance(memory_field.type, TypeReference)
        assert memory_field.type.name == "MemoryDefinition"

        owner_field = agent.fields[10]
        assert isinstance(owner_field.type, PrimitiveType)
        assert owner_field.type.name == "string"


# ============================================
# Type Expression Tests
# ============================================

class TestTypeExpressions:
    """Test all type expression patterns."""

    def test_primitive_types(self, parser):
        """Test primitive type expressions."""
        content = """
type BasicTypes {
  name: string
  count: integer
  price: number
  active: boolean
  data: object
  items: array
  any_value: any
  null_value: null
}
"""
        result = parser.parse(content)
        type_def = result.declarations[0]
        assert type_def.name == "BasicTypes"
        assert len(type_def.body.fields) == 8

        field_types = [f.type for f in type_def.body.fields]
        assert field_types[0].name == "string"
        assert field_types[1].name == "integer"
        assert field_types[2].name == "number"
        assert field_types[3].name == "boolean"
        assert field_types[4].name == "object"
        assert field_types[5].name == "array"
        assert field_types[6].name == "any"
        assert field_types[7].name == "null"

    def test_optional_types(self, parser):
        """Test optional type expressions."""
        content = """
type OptionalFields {
  required: string
  optional?: string
  optional_number?: number
  optional_array?: array
}
"""
        result = parser.parse(content)
        type_def = result.declarations[0]
        assert type_def.name == "OptionalFields"
        assert len(type_def.body.fields) == 4

        # Check that optional fields have the optional flag set
        assert type_def.body.fields[0].name == "required"
        assert type_def.body.fields[0].optional == False
        assert type_def.body.fields[1].name == "optional"
        assert type_def.body.fields[1].optional == True
        assert type_def.body.fields[2].name == "optional_number"
        assert type_def.body.fields[2].optional == True
        assert type_def.body.fields[3].name == "optional_array"
        assert type_def.body.fields[3].optional == True

    def test_array_types(self, parser):
        """Test array type expressions."""
        content = """
type ArrayTypes {
  names: string[]
  counts: integer[]
  mixed: array
  nested: array[]
}
"""
        result = parser.parse(content)
        type_def = result.declarations[0]
        assert type_def.name == "ArrayTypes"
        assert len(type_def.body.fields) == 4

        field_types = [f.type for f in type_def.body.fields]
        assert isinstance(field_types[0], ArrayType)
        assert isinstance(field_types[0].element_type, PrimitiveType)
        assert field_types[0].element_type.name == "string"

        assert isinstance(field_types[1], ArrayType)
        assert isinstance(field_types[1].element_type, PrimitiveType)
        assert field_types[1].element_type.name == "integer"

        # "array" is a primitive type, so it's parsed as PrimitiveType, not ArrayType
        assert isinstance(field_types[2], PrimitiveType)
        assert field_types[2].name == "array"

        assert isinstance(field_types[3], ArrayType)
        assert isinstance(field_types[3].element_type, PrimitiveType)
        assert field_types[3].element_type.name == "array"

    def test_union_types(self, parser):
        """Test union type expressions."""
        content = """
type UnionTypes {
  value: string | integer | boolean
  mixed: string | number | object | array
  optional_union?: string | integer | null
}
"""
        result = parser.parse(content)
        type_def = result.declarations[0]
        assert type_def.name == "UnionTypes"
        assert len(type_def.body.fields) == 3

        field_types = [f.type for f in type_def.body.fields]
        assert isinstance(field_types[0], UnionType)
        assert len(field_types[0].types) == 3

        assert isinstance(field_types[1], UnionType)
        assert len(field_types[1].types) == 4

        # The optional marker applies to the field, not the type
        # So the type is UnionType, and the field has optional=True
        assert isinstance(field_types[2], UnionType)
        assert len(field_types[2].types) == 3
        assert type_def.body.fields[2].optional == True

    def test_constrained_types(self, parser):
        """Test constrained type expressions."""
        content = """
type ConstrainedTypes {
  min_value: integer (1..)
  max_value: integer (..100)
  range_value: number (0..1)
  exclusive_min: integer (1..)
  exclusive_max: integer (..100)
  min_length: string (1..10)
  max_length: string (..50)
  min_items: array (1..)
  max_items: array (..10)
  multiple_of: number (..)
  pattern_value: string
}
"""
        result = parser.parse(content)
        type_def = result.declarations[0]
        assert type_def.name == "ConstrainedTypes"
        assert len(type_def.body.fields) == 11

        field_types = [f.type for f in type_def.body.fields]
        assert isinstance(field_types[0], ConstrainedType)
        assert field_types[0].min_value == 1
        assert field_types[0].max_value is None

        assert isinstance(field_types[1], ConstrainedType)
        assert field_types[1].min_value is None
        assert field_types[1].max_value == 100

        assert isinstance(field_types[2], ConstrainedType)
        assert field_types[2].min_value == 0
        assert field_types[2].max_value == 1

        assert isinstance(field_types[3], ConstrainedType)
        assert field_types[3].min_value == 1

        assert isinstance(field_types[4], ConstrainedType)
        assert field_types[4].max_value == 100

    def test_nested_type_expressions(self, parser):
        """Test nested type expressions."""
        content = """
type Person {
  name: string
  age: integer
}

type Address {
  street: string
  city: string
  zip: string
}

type Config {
  api_key: string
  timeout: integer
}

type NestedTypes {
  user: Person
  addresses: Address[]
  config: Config
  metadata: object
}
"""
        result = parser.parse(content)
        type_def = result.declarations[3]
        assert type_def.name == "NestedTypes"
        assert len(type_def.body.fields) == 4

        field_types = [f.type for f in type_def.body.fields]
        assert isinstance(field_types[0], TypeReference)
        assert field_types[0].name == "Person"

        assert isinstance(field_types[1], ArrayType)
        assert isinstance(field_types[1].element_type, TypeReference)
        assert field_types[1].element_type.name == "Address"

        assert isinstance(field_types[2], TypeReference)
        assert field_types[2].name == "Config"

        assert isinstance(field_types[3], PrimitiveType)
        assert field_types[3].name == "object"


# ============================================
# Error Case Tests
# ============================================

class TestErrorCases:
    """Test parser error handling."""

    def test_missing_closing_brace(self, parser):
        """Test error for missing closing brace."""
        content = """
type InvalidType {
  name: string
  count: integer
"""
        with pytest.raises(ParseError) as exc_info:
            parser.parse(content)

        assert "line" in str(exc_info.value).lower()
        assert "column" in str(exc_info.value).lower()

    def test_invalid_constraint_syntax(self, parser):
        """Test error for invalid constraint syntax."""
        content = """
type InvalidConstraint {
  value: integer (1..100..200)
}
"""
        with pytest.raises(ParseError) as exc_info:
            parser.parse(content)

        assert "line" in str(exc_info.value).lower()

    def test_invalid_array_syntax(self, parser):
        """Test error for invalid array syntax."""
        content = """
type InvalidArray {
  value: string[10]
}
"""
        with pytest.raises(ParseError) as exc_info:
            parser.parse(content)

        assert "line" in str(exc_info.value).lower()

    def test_missing_colon_in_field(self, parser):
        """Test error for missing colon in field."""
        content = """
type MissingColon {
  name string
  count: integer
}
"""
        with pytest.raises(ParseError) as exc_info:
            parser.parse(content)

        assert "line" in str(exc_info.value).lower()

    def test_missing_agent_body(self, parser):
        """Test error for missing agent body."""
        content = """
agent MissingBody
"""
        with pytest.raises(ParseError) as exc_info:
            parser.parse(content)

        assert "line" in str(exc_info.value).lower()

    def test_invalid_field_name(self, parser):
        """Test error for invalid field name."""
        content = """
type InvalidFieldName {
  123invalid: string
  valid_name: string
}
"""
        with pytest.raises(ParseError) as exc_info:
            parser.parse(content)

        assert "line" in str(exc_info.value).lower()

    def test_invalid_optional_marker_placement(self, parser):
        """Test error for invalid optional marker placement."""
        content = """
type InvalidOptional {
  value: string? integer
}
"""
        with pytest.raises(ParseError) as exc_info:
            parser.parse(content)

        assert "line" in str(exc_info.value).lower()

    def test_missing_enum_values(self, parser):
        """Test error for missing enum values."""
        content = """
enum EmptyEnum {
}
"""
        with pytest.raises(ParseError) as exc_info:
            parser.parse(content)

        assert "line" in str(exc_info.value).lower()

    def test_invalid_constraint_operator(self, parser):
        """Test error for invalid constraint operator."""
        content = """
type InvalidOperator {
  value: integer (1<10)
}
"""
        with pytest.raises(ParseError) as exc_info:
            parser.parse(content)

        assert "line" in str(exc_info.value).lower()

    def test_invalid_import_with_as(self, parser):
        """Test error for invalid import with AS."""
        content = """
import schema/components/rag as
"""
        with pytest.raises(ParseError) as exc_info:
            parser.parse(content)

        assert "line" in str(exc_info.value).lower()

    def test_missing_type_body(self, parser):
        """Test error for missing type body."""
        content = """
type MissingBody
"""
        with pytest.raises(ParseError) as exc_info:
            parser.parse(content)

        assert "line" in str(exc_info.value).lower()

    def test_unexpected_character(self, parser):
        """Test error for unexpected character."""
        content = """
type Test {
  name: string
  count: integer
}
"""
        # Add unexpected character
        content += " @"
        with pytest.raises(ParseError) as exc_info:
            parser.parse(content)

        assert "line" in str(exc_info.value).lower()
        assert "column" in str(exc_info.value).lower()

    def test_unexpected_token(self, parser):
        """Test error for unexpected token."""
        content = """
type Test {
  name: string
  count: integer
}
"""
        # Add unexpected token
        content += " invalid_token"
        with pytest.raises(ParseError) as exc_info:
            parser.parse(content)

        assert "line" in str(exc_info.value).lower()
        assert "column" in str(exc_info.value).lower()


# ============================================
# Integration Tests
# ============================================

class TestIntegration:
    """Test integration of all parser features."""

    def test_complete_file_parsing(self, parser):
        """Test parsing a complete ADL file with all features."""
        content = """
import schema/components/rag
import schema/components/tool as tools

enum Lifecycle {
  stable
  beta
  deprecated
}

enum MemoryType {
  episodic
  semantic
  working
  hybrid
}

type Person {
  name: string
  age: integer
}

type Address {
  street: string
  city: string
  zip: string
}

type Config {
  api_key: string
  timeout: integer
}

type LlmSettings {
  temperature: number
  max_tokens: integer
}

type ToolDefinition {
  name: string
  description: string
  parameters: ToolParameter[]
}

type RagIndex {
  index_id: string
  type: string
}

type MemoryDefinition {
  type: MemoryType
  scope: string
}

enum MemoryScope {
  session
  user
  org
  global
}

agent CompleteAgent {
  id: string
  version: integer
  name: string
  description: string
  role: string
  llm: string
  llm_settings: LlmSettings
  tools: ToolDefinition[]
  rag: RagIndex[]
  memory: MemoryDefinition
  owner: string
}
"""
        result = parser.parse(content)
        assert isinstance(result, Program)
        assert len(result.imports) == 2
        assert len(result.declarations) == 10  # 3 enums + 7 types
        assert isinstance(result.agent, AgentDef)

    def test_file_parsing_from_disk(self, parser):
        """Test parsing ADL files from disk."""
        fixture_path = Path(__file__).parent.parent.parent / "tests/fixtures/dsl/types.adl"
        result = parser.parse_file(str(fixture_path))
        assert isinstance(result, Program)
        assert len(result.declarations) > 0
        assert isinstance(result.declarations[0], TypeDef)

    def test_complex_file_parsing(self, parser):
        """Test parsing complex ADL file."""
        fixture_path = Path(__file__).parent.parent.parent / "tests/fixtures/dsl/complex.adl"
        result = parser.parse_file(str(fixture_path))
        assert isinstance(result, Program)
        assert len(result.declarations) > 20  # Many nested types
        assert isinstance(result.agent, AgentDef)

    def test_error_messages_include_location(self, parser):
        """Test that error messages include line and column information."""
        content = """
type Test {
  name: string
  count: integer
}
"""
        # Add syntax error
        content += " invalid_syntax"

        with pytest.raises(ParseError) as exc_info:
            parser.parse(content)

        error = exc_info.value
        assert error.line is not None
        assert error.column is not None
        assert error.line > 0
        assert error.column > 0


# ============================================
# Parametrized Tests
# ============================================

class TestParametrized:
    """Test parser with parametrized test cases."""

    @pytest.mark.parametrize("content,expected_count", [
        ("import a", 1),
        ("import a\nimport b", 2),
        ("import a\nimport b\nimport c", 3),
    ])
    def test_import_count(self, parser, content, expected_count):
        """Test that correct number of imports are parsed."""
        result = parser.parse(content)
        assert len(result.imports) == expected_count

    @pytest.mark.parametrize("enum_name,values", [
        ("Lifecycle", ["stable", "beta", "deprecated", "experimental"]),
        ("ChangeType", ["breaking", "non-breaking", "patch"]),
        ("MemoryType", ["episodic", "semantic", "working", "hybrid"]),
    ])
    def test_enum_values(self, parser, enum_name, values):
        """Test enum value parsing."""
        content = f"enum {enum_name} {{ {', '.join(values)} }}"
        result = parser.parse(content)
        enum_def = result.declarations[0]
        assert enum_def.name == enum_name
        assert enum_def.values == values

    @pytest.mark.parametrize("field_name,field_type,optional", [
        ("name", "string", False),
        ("age", "integer", False),
        ("optional_field", "string", True),
        ("count", "integer (1..)", False),
    ])
    def test_field_types(self, parser, field_name, field_type, optional):
        """Test field type parsing."""
        optional_marker = "?" if optional else ""
        content = f"""
type Test {{
  {field_name}{optional_marker}: {field_type}
}}
"""
        result = parser.parse(content)
        type_def = result.declarations[0]
        field = type_def.body.fields[0]
        assert field.name == field_name
        assert field.optional == optional


# ============================================
# AST Structure Verification
# ============================================

class TestASTStructure:
    """Test AST structure correctness."""

    def test_program_structure(self, parser):
        """Test that Program has correct structure."""
        content = """
import a
import b as tools

enum E { a, b }

type T {
  f: string
}

agent A {
  id: string
}
"""
        result = parser.parse(content)
        assert hasattr(result, 'imports')
        assert hasattr(result, 'declarations')
        assert hasattr(result, 'agent')
        assert isinstance(result.imports, list)
        assert isinstance(result.declarations, list)
        assert isinstance(result.agent, AgentDef)

    def test_import_stmt_structure(self, parser):
        """Test ImportStmt structure."""
        content = "import schema/components/rag as tools"
        result = parser.parse(content)
        import_stmt = result.imports[0]
        assert hasattr(import_stmt, 'path')
        assert hasattr(import_stmt, 'alias')
        assert import_stmt.path == "schema/components/rag"
        assert import_stmt.alias == "tools"

    def test_enum_def_structure(self, parser):
        """Test EnumDef structure."""
        content = "enum Lifecycle { stable, beta, deprecated }"
        result = parser.parse(content)
        enum_def = result.declarations[0]
        assert hasattr(enum_def, 'name')
        assert hasattr(enum_def, 'values')
        assert enum_def.name == "Lifecycle"
        assert enum_def.values == ["stable", "beta", "deprecated"]

    def test_type_def_structure(self, parser):
        """Test TypeDef structure."""
        content = """
type Person {
  name: string
  age: integer
}
"""
        result = parser.parse(content)
        type_def = result.declarations[0]
        assert hasattr(type_def, 'name')
        assert hasattr(type_def, 'body')
        assert type_def.name == "Person"
        assert isinstance(type_def.body, TypeBody)
        assert hasattr(type_def.body, 'fields')
        assert isinstance(type_def.body.fields, list)

    def test_field_def_structure(self, parser):
        """Test FieldDef structure."""
        content = """
type Test {
  name: string
  age: integer (1..)
}
"""
        result = parser.parse(content)
        field = result.declarations[0].body.fields[0]
        assert hasattr(field, 'name')
        assert hasattr(field, 'type')
        assert hasattr(field, 'optional')
        assert field.name == "name"
        assert field.optional is False

    def test_agent_def_structure(self, parser):
        """Test AgentDef structure."""
        content = """
agent TestAgent {
  id: string
  name: string
}
"""
        result = parser.parse(content)
        agent = result.agent
        assert hasattr(agent, 'name')
        assert hasattr(agent, 'fields')
        assert agent.name == "TestAgent"
        assert isinstance(agent.fields, list)

    def test_primitive_type_structure(self, parser):
        """Test PrimitiveType structure."""
        content = """
type Test {
  name: string
}
"""
        result = parser.parse(content)
        field_type = result.declarations[0].body.fields[0].type
        assert hasattr(field_type, 'name')
        assert field_type.name == "string"

    def test_type_reference_structure(self, parser):
        """Test TypeReference structure."""
        content = """
type Person {
  name: string
}

type User {
  person: Person
}
"""
        result = parser.parse(content)
        field_type = result.declarations[1].body.fields[0].type
        assert hasattr(field_type, 'name')
        assert field_type.name == "Person"

    def test_array_type_structure(self, parser):
        """Test ArrayType structure."""
        content = """
type Test {
  names: string[]
}
"""
        result = parser.parse(content)
        field_type = result.declarations[0].body.fields[0].type
        assert hasattr(field_type, 'element_type')
        assert isinstance(field_type.element_type, PrimitiveType)
        assert field_type.element_type.name == "string"

    def test_union_type_structure(self, parser):
        """Test UnionType structure."""
        content = """
type Test {
  value: string | integer
}
"""
        result = parser.parse(content)
        field_type = result.declarations[0].body.fields[0].type
        assert hasattr(field_type, 'types')
        assert isinstance(field_type.types, list)
        assert len(field_type.types) == 2

    def test_optional_type_structure(self, parser):
        """Test optional field structure."""
        content = """
type Test {
  optional?: string
}
"""
        result = parser.parse(content)
        field = result.declarations[0].body.fields[0]
        assert field.optional == True
        assert isinstance(field.type, PrimitiveType)
        assert field.type.name == "string"

    def test_constrained_type_structure(self, parser):
        """Test ConstrainedType structure."""
        content = """
type Test {
  count: integer (1..)
}
"""
        result = parser.parse(content)
        field_type = result.declarations[0].body.fields[0].type
        assert hasattr(field_type, 'base_type')
        assert hasattr(field_type, 'min_value')
        assert hasattr(field_type, 'max_value')
        assert field_type.min_value == 1
        assert field_type.max_value is None