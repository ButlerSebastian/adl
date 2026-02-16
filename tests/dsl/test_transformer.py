"""
Tests for ADLTransformer

This module contains unit tests for the ADLTransformer class,
testing all transform methods, token extraction, and location handling.
"""

import pytest
from lark import Token
from lark.tree import Meta

from tools.dsl.transformer import ADLTransformer
from tools.dsl.ast import (
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
)


class TestADLTransformer:
    """Test suite for ADLTransformer"""

    @pytest.fixture
    def transformer(self):
        """Create a fresh transformer instance for each test"""
        return ADLTransformer()

    @pytest.fixture
    def sample_meta(self):
        """Sample Lark meta object for testing"""
        return Meta(
            line=1,
            column=1,
            end_line=1,
            end_column=10,
            filename="test.adl",
        )

    # ============================================
    # Location Extraction Tests
    # ============================================

    def test_get_loc_extracts_correctly(self, transformer, sample_meta):
        """Test that _get_loc extracts correct location information"""
        loc = transformer._get_loc(sample_meta)

        assert isinstance(loc, SourceLocation)
        assert loc.line == 1
        assert loc.column == 1
        assert loc.end_line == 1
        assert loc.end_column == 10
        assert loc.file == "test.adl"

    def test_get_loc_with_default_file(self, transformer):
        """Test location extraction without filename"""
        meta = Meta(line=5, column=10, end_line=5, end_column=20)
        loc = transformer._get_loc(meta)

        assert loc.file is None

    # ============================================
    # Program Transformation Tests
    # ============================================

    def test_transform_start_with_program(self, transformer):
        """Test transforming start symbol with program"""
        children = [
            [],  # imports
            [],  # declarations
            AgentDef(name="test_agent", fields=[], loc=SourceLocation(1, 1, 1, 10, "test.adl")),
        ]

        result = transformer.start(children)

        assert isinstance(result, Program)
        assert result.imports == []
        assert result.declarations == []
        assert isinstance(result.agent, AgentDef)
        assert result.agent.name == "test_agent"

    def test_transform_program(self, transformer):
        """Test transforming program rule"""
        children = [
            [],
            [],
            AgentDef(name="test_agent", fields=[], loc=SourceLocation(1, 1, 1, 10, "test.adl")),
        ]

        result = transformer.program(children)

        assert isinstance(result, Program)
        assert result.agent.name == "test_agent"

    def test_transform_program_with_imports(self, transformer):
        """Test transforming program with imports"""
        import_stmt = ImportStmt(path="std", alias=None, loc=SourceLocation(1, 1, 1, 10, "test.adl"))
        children = [
            [import_stmt],
            [],
            AgentDef(name="test_agent", fields=[], loc=SourceLocation(1, 1, 1, 10, "test.adl")),
        ]

        result = transformer.program(children)

        assert len(result.imports) == 1
        assert result.imports[0].path == "std"
        assert result.imports[0].alias is None

    def test_transform_program_with_declarations(self, transformer):
        """Test transforming program with declarations"""
        enum_def = EnumDef(name="Status", values=["ACTIVE", "INACTIVE"], loc=SourceLocation(1, 1, 1, 10, "test.adl"))
        children = [
            [],
            [enum_def],
            AgentDef(name="test_agent", fields=[], loc=SourceLocation(1, 1, 1, 10, "test.adl")),
        ]

        result = transformer.program(children)

        assert len(result.declarations) == 1
        assert result.declarations[0].name == "Status"

    # ============================================
    # Import Transformation Tests
    # ============================================

    def test_transform_import_stmt(self, transformer):
        """Test transforming import statement"""
        children = [
            Token("IMPORT", "import"),
            Token("IDENTIFIER", "std"),
            Token("AS", "as"),
            Token("IDENTIFIER", "s"),
        ]

        result = transformer.import_stmt(children)

        assert isinstance(result, ImportStmt)
        assert result.path == "std"
        assert result.alias == "s"

    def test_transform_import_stmt_without_alias(self, transformer):
        """Test transforming import statement without alias"""
        children = [
            Token("IMPORT", "import"),
            Token("IDENTIFIER", "std"),
        ]

        result = transformer.import_stmt(children)

        assert isinstance(result, ImportStmt)
        assert result.path == "std"
        assert result.alias is None

    def test_transform_import_path_slash(self, transformer):
        """Test transforming import path with slash notation"""
        children = [
            Token("IDENTIFIER", "std"),
            Token("SLASH", "/"),
            Token("IDENTIFIER", "types"),
        ]

        result = transformer.import_path(children)

        assert result == "std/types"

    def test_transform_import_path_dot(self, transformer):
        """Test transforming import path with dot notation"""
        children = [
            Token("IDENTIFIER", "std"),
            Token("IDENTIFIER", "types"),
        ]

        result = transformer.import_path(children)

        assert result == "std.types"

    def test_transform_absolute_path_slash(self, transformer):
        """Test transforming absolute path with slash notation"""
        children = [
            Token("IDENTIFIER", "std"),
            Token("SLASH", "/"),
            Token("IDENTIFIER", "types"),
        ]

        result = transformer.absolute_path(children)

        assert result == "std/types"

    def test_transform_absolute_path_dot(self, transformer):
        """Test transforming absolute path with dot notation"""
        children = [
            Token("IDENTIFIER", "std"),
            Token("IDENTIFIER", "types"),
        ]

        result = transformer.absolute_path(children)

        assert result == "std.types"

    def test_transform_relative_path(self, transformer):
        """Test transforming relative path"""
        children = [
            Token("IDENTIFIER", ".."),
            Token("IDENTIFIER", "types"),
        ]

        result = transformer.relative_path(children)

        assert result == "..types"

    # ============================================
    # Enum Transformation Tests
    # ============================================

    def test_transform_enum_def(self, transformer):
        """Test transforming enum definition"""
        children = [
            Token("ENUM", "enum"),
            Token("IDENTIFIER", "Status"),
            Token("{", "{"),
            Token("IDENTIFIER", "ACTIVE"),
            Token("IDENTIFIER", "INACTIVE"),
            Token("}", "}"),
        ]

        result = transformer.enum_def(children)

        assert isinstance(result, EnumDef)
        assert result.name == "Status"
        assert result.values == ["ACTIVE", "INACTIVE"]

    def test_transform_enum_body(self, transformer):
        """Test transforming enum body"""
        children = [
            Token("IDENTIFIER", "ACTIVE"),
            Token("IDENTIFIER", "INACTIVE"),
            Token("IDENTIFIER", "PENDING"),
        ]

        result = transformer.enum_body(children)

        assert result == ["ACTIVE", "INACTIVE", "PENDING"]

    def test_transform_enum_value(self, transformer):
        """Test transforming enum value"""
        children = [Token("IDENTIFIER", "ACTIVE")]

        result = transformer.enum_value(children)

        assert isinstance(result, Token)
        assert result.value == "ACTIVE"

    # ============================================
    # Type Transformation Tests
    # ============================================

    def test_transform_type_def(self, transformer):
        """Test transforming type definition"""
        children = [
            Token("TYPE", "type"),
            Token("IDENTIFIER", "User"),
            Token("{", "{"),
            Token("IDENTIFIER", "name"),
            Token(":", Token("PRIMITIVE_TYPE", "string")),
            Token("}", "}"),
        ]

        result = transformer.type_def(children)

        assert isinstance(result, TypeDef)
        assert result.name == "User"
        assert isinstance(result.body, TypeBody)
        assert len(result.body.fields) == 1
        assert result.body.fields[0].name == "name"

    def test_transform_type_def_without_body(self, transformer):
        """Test transforming type definition without body"""
        children = [
            Token("TYPE", "type"),
            Token("IDENTIFIER", "Config"),
        ]

        result = transformer.type_def(children)

        assert isinstance(result, TypeDef)
        assert result.name == "Config"
        assert result.body is None

    def test_transform_type_body(self, transformer):
        """Test transforming type body"""
        field1 = FieldDef(name="id", type=PrimitiveType(name="integer"), optional=False, loc=SourceLocation(1, 1, 1, 10, "test.adl"))
        field2 = FieldDef(name="name", type=PrimitiveType(name="string"), optional=False, loc=SourceLocation(1, 1, 1, 10, "test.adl"))

        children = [field1, field2]

        result = transformer.type_body(children)

        assert isinstance(result, TypeBody)
        assert len(result.fields) == 2
        assert result.fields[0].name == "id"
        assert result.fields[1].name == "name"

    def test_transform_field_list(self, transformer):
        """Test transforming field list"""
        field1 = FieldDef(name="id", type=PrimitiveType(name="integer"), optional=False, loc=SourceLocation(1, 1, 1, 10, "test.adl"))
        field2 = FieldDef(name="name", type=PrimitiveType(name="string"), optional=False, loc=SourceLocation(1, 1, 1, 10, "test.adl"))

        children = [field1, field2]

        result = transformer.field_list(children)

        assert result == [field1, field2]

    def test_transform_field_def(self, transformer):
        """Test transforming field definition"""
        children = [
            Token("IDENTIFIER", "name"),
            Token("?", "?"),
            Token(":", Token("PRIMITIVE_TYPE", "string")),
        ]

        result = transformer.field_def(children)

        assert isinstance(result, FieldDef)
        assert result.name == "name"
        assert result.optional is True
        assert isinstance(result.type, PrimitiveType)
        assert result.type.name == "string"

    def test_transform_field_def_without_optional(self, transformer):
        """Test transforming field definition without optional marker"""
        children = [
            Token("IDENTIFIER", "id"),
            Token(":", Token("PRIMITIVE_TYPE", "integer")),
        ]

        result = transformer.field_def(children)

        assert isinstance(result, FieldDef)
        assert result.name == "id"
        assert result.optional is False

    def test_transform_optional_marker(self, transformer):
        """Test transforming optional marker"""
        children = [Token("?", "?")]

        result = transformer.optional_marker(children)

        assert isinstance(result, Token)
        assert result.value == "?"

    # ============================================
    # Type Expression Tests
    # ============================================

    def test_transform_type_expr(self, transformer):
        """Test transforming type expression"""
        primitive_type = PrimitiveType(name="string", loc=SourceLocation(1, 1, 1, 10, "test.adl"))
        children = [primitive_type]

        result = transformer.type_expr(children)

        assert result == primitive_type

    def test_transform_union_type(self, transformer):
        """Test transforming union type"""
        type1 = PrimitiveType(name="string", loc=SourceLocation(1, 1, 1, 10, "test.adl"))
        type2 = PrimitiveType(name="integer", loc=SourceLocation(1, 1, 1, 10, "test.adl"))
        children = [type1, type2]

        result = transformer.union_type(children)

        assert isinstance(result, UnionType)
        assert len(result.types) == 2
        assert result.types[0].name == "string"
        assert result.types[1].name == "integer"

    def test_transform_postfix_type_array(self, transformer):
        """Test transforming postfix type with array suffix"""
        base_type = PrimitiveType(name="string", loc=SourceLocation(1, 1, 1, 10, "test.adl"))
        children = [base_type, Token("[", "["), Token("]", "]")]

        result = transformer.postfix_type(children)

        assert isinstance(result, ArrayType)
        assert isinstance(result.element_type, PrimitiveType)
        assert result.element_type.name == "string"

    def test_transform_postfix_type_optional(self, transformer):
        """Test transforming postfix type with optional suffix"""
        base_type = PrimitiveType(name="string", loc=SourceLocation(1, 1, 1, 10, "test.adl"))
        children = [base_type, Token("?", "?")]

        result = transformer.postfix_type(children)

        assert isinstance(result, OptionalType)
        assert isinstance(result.inner_type, PrimitiveType)
        assert result.inner_type.name == "string"

    def test_transform_postfix_type_multiple_suffixes(self, transformer):
        """Test transforming postfix type with multiple suffixes"""
        base_type = PrimitiveType(name="string", loc=SourceLocation(1, 1, 1, 10, "test.adl"))
        children = [base_type, Token("[", "["), Token("]", "]"), Token("?", "?")]

        result = transformer.postfix_type(children)

        assert isinstance(result, OptionalType)
        assert isinstance(result.inner_type, ArrayType)
        assert isinstance(result.inner_type.element_type, PrimitiveType)

    def test_transform_array_suffix(self, transformer):
        """Test transforming array suffix"""
        children = [Token("[", "["), Token("]", "]")]

        result = transformer.array_suffix(children)

        assert isinstance(result, Token)
        assert result.value == "["

    def test_transform_optional_suffix(self, transformer):
        """Test transforming optional suffix"""
        children = [Token("?", "?")]

        result = transformer.optional_suffix(children)

        assert isinstance(result, Token)
        assert result.value == "?"

    def test_transform_constraint_suffix(self, transformer):
        """Test transforming constraint suffix"""
        children = [Token("(", "("), Token("NUMBER", "1"), Token("NUMBER", "10"), Token(")", ")")]

        result = transformer.constraint_suffix(children)

        assert isinstance(result, Token)
        assert result.value == "("

    def test_transform_range_constraint(self, transformer):
        """Test transforming range constraint"""
        children = [Token("NUMBER", "1"), Token("NUMBER", "10")]

        result = transformer.range_constraint(children)

        assert result == "1..10"

    def test_transform_range_constraint_single_value(self, transformer):
        """Test transforming range constraint with single value"""
        children = [Token("NUMBER", "5")]

        result = transformer.range_constraint(children)

        assert result == "5.."

    def test_transform_primary_type_primitive(self, transformer):
        """Test transforming primitive type"""
        children = [Token("PRIMITIVE_TYPE", "string")]

        result = transformer.primary_type(children)

        assert isinstance(result, PrimitiveType)
        assert result.name == "string"

    def test_transform_primary_type_reference(self, transformer):
        """Test transforming type reference"""
        children = [Token("IDENTIFIER", "User")]

        result = transformer.primary_type(children)

        assert isinstance(result, TypeReference)
        assert result.name == "User"

    def test_transform_primary_type_parenthesized(self, transformer):
        """Test transforming parenthesized type expression"""
        inner_type = PrimitiveType(name="string", loc=SourceLocation(1, 1, 1, 10, "test.adl"))
        children = [Token("(", "("), inner_type, Token(")", ")")]

        result = transformer.primary_type(children)

        assert result == inner_type

    # ============================================
    # Agent Transformation Tests
    # ============================================

    def test_transform_agent_def(self, transformer):
        """Test transforming agent definition"""
        field1 = FieldDef(name="name", type=PrimitiveType(name="string"), optional=False, loc=SourceLocation(1, 1, 1, 10, "test.adl"))
        field2 = FieldDef(name="role", type=PrimitiveType(name="string"), optional=False, loc=SourceLocation(1, 1, 1, 10, "test.adl"))

        children = [
            Token("AGENT", "agent"),
            Token("IDENTIFIER", "test_agent"),
            Token("{", "{"),
            field1,
            field2,
            Token("}", "}"),
        ]

        result = transformer.agent_def(children)

        assert isinstance(result, AgentDef)
        assert result.name == "test_agent"
        assert len(result.fields) == 2
        assert result.fields[0].name == "name"
        assert result.fields[1].name == "role"

    # ============================================
    # Default Handler Tests
    # ============================================

    def test_transform_default_handler(self, transformer):
        """Test default handler for unmatched tokens"""
        token = Token("IDENTIFIER", "test")

        result = transformer.DEFAULT(token)

        assert result == token
        assert result.value == "test"

    def test_transform_default_handler_for_tokens(self, transformer):
        """Test default handler for various token types"""
        tokens = [
            Token("IDENTIFIER", "test"),
            Token("PRIMITIVE_TYPE", "string"),
            Token("NUMBER", "42"),
        ]

        for token in tokens:
            result = transformer.DEFAULT(token)
            assert result == token

    # ============================================
    # Tree Traversal Tests
    # ============================================

    def test_transformer_tree_structure(self, transformer):
        """Test that transformer produces correct tree structure"""
        import_stmt = ImportStmt(path="std", alias=None, loc=SourceLocation(1, 1, 1, 10, "test.adl"))
        enum_def = EnumDef(name="Status", values=["ACTIVE", "INACTIVE"], loc=SourceLocation(1, 1, 1, 10, "test.adl"))
        agent_def = AgentDef(name="test_agent", fields=[], loc=SourceLocation(1, 1, 1, 10, "test.adl"))

        children = [
            [import_stmt],
            [enum_def],
            agent_def,
        ]

        result = transformer.start(children)

        assert isinstance(result, Program)
        assert len(result.imports) == 1
        assert isinstance(result.imports[0], ImportStmt)
        assert len(result.declarations) == 1
        assert isinstance(result.declarations[0], EnumDef)
        assert isinstance(result.agent, AgentDef)

    def test_transformer_nested_types(self, transformer):
        """Test transformer with nested type expressions"""
        array_type = ArrayType(
            element_type=PrimitiveType(name="string", loc=SourceLocation(1, 1, 1, 10, "test.adl")),
            loc=SourceLocation(1, 1, 1, 10, "test.adl"),
        )
        optional_type = OptionalType(
            inner_type=array_type,
            loc=SourceLocation(1, 1, 1, 10, "test.adl"),
        )

        children = [optional_type]

        result = transformer.type_expr(children)

        assert isinstance(result, OptionalType)
        assert isinstance(result.inner_type, ArrayType)
        assert isinstance(result.inner_type.element_type, PrimitiveType)

    def test_transformer_union_types(self, transformer):
        """Test transformer with union types"""
        type1 = PrimitiveType(name="string", loc=SourceLocation(1, 1, 1, 10, "test.adl"))
        type2 = PrimitiveType(name="integer", loc=SourceLocation(1, 1, 1, 10, "test.adl"))
        type3 = PrimitiveType(name="boolean", loc=SourceLocation(1, 1, 1, 10, "test.adl"))

        children = [type1, type2, type3]

        result = transformer.union_type(children)

        assert isinstance(result, UnionType)
        assert len(result.types) == 3
        assert all(isinstance(t, PrimitiveType) for t in result.types)

    # ============================================
    # Edge Cases Tests
    # ============================================

    def test_transform_empty_import_list(self, transformer):
        """Test transforming empty import list"""
        children = [
            [],
            [],
            AgentDef(name="test_agent", fields=[], loc=SourceLocation(1, 1, 1, 10, "test.adl")),
        ]

        result = transformer.start(children)

        assert result.imports == []

    def test_transform_empty_declaration_list(self, transformer):
        """Test transforming empty declaration list"""
        children = [
            [],
            [],
            AgentDef(name="test_agent", fields=[], loc=SourceLocation(1, 1, 1, 10, "test.adl")),
        ]

        result = transformer.start(children)

        assert result.declarations == []

    def test_transform_type_with_multiple_fields(self, transformer):
        """Test transforming type with multiple fields"""
        field1 = FieldDef(name="id", type=PrimitiveType(name="integer"), optional=False, loc=SourceLocation(1, 1, 1, 10, "test.adl"))
        field2 = FieldDef(name="name", type=PrimitiveType(name="string"), optional=False, loc=SourceLocation(1, 1, 1, 10, "test.adl"))
        field3 = FieldDef(name="email", type=PrimitiveType(name="string"), optional=True, loc=SourceLocation(1, 1, 1, 10, "test.adl"))

        children = [
            Token("TYPE", "type"),
            Token("IDENTIFIER", "User"),
            Token("{", "{"),
            field1,
            field2,
            field3,
            Token("}", "}"),
        ]

        result = transformer.type_def(children)

        assert isinstance(result, TypeDef)
        assert len(result.body.fields) == 3
        assert result.body.fields[0].name == "id"
        assert result.body.fields[1].name == "name"
        assert result.body.fields[2].name == "email"
        assert result.body.fields[2].optional is True

    def test_transform_agent_with_multiple_fields(self, transformer):
        """Test transforming agent with multiple fields"""
        field1 = FieldDef(name="name", type=PrimitiveType(name="string"), optional=False, loc=SourceLocation(1, 1, 1, 10, "test.adl"))
        field2 = FieldDef(name="role", type=PrimitiveType(name="string"), optional=False, loc=SourceLocation(1, 1, 1, 10, "test.adl"))
        field3 = FieldDef(name="description", type=PrimitiveType(name="string"), optional=True, loc=SourceLocation(1, 1, 1, 10, "test.adl"))

        children = [
            Token("AGENT", "agent"),
            Token("IDENTIFIER", "test_agent"),
            Token("{", "{"),
            field1,
            field2,
            field3,
            Token("}", "}"),
        ]

        result = transformer.agent_def(children)

        assert isinstance(result, AgentDef)
        assert len(result.fields) == 3
        assert result.fields[0].name == "name"
        assert result.fields[1].name == "role"
        assert result.fields[2].name == "description"
        assert result.fields[2].optional is True