"""
AST Tests for ADL DSL

Tests for all AST node types, SourceLocation, visitor pattern, and PrintVisitor.
"""

import pytest
from tools.dsl.ast import (
    SourceLocation,
    ASTNode,
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
    ASTVisitor,
    PrintVisitor,
)


# ============================================
# SourceLocation Tests
# ============================================

def test_source_location_basic():
    """Test basic SourceLocation creation"""
    loc = SourceLocation(line=1, column=1, end_line=1, end_column=10)
    assert loc.line == 1
    assert loc.column == 1
    assert loc.end_line == 1
    assert loc.end_column == 10
    assert loc.file is None


def test_source_location_with_file():
    """Test SourceLocation with file path"""
    loc = SourceLocation(line=5, column=10, end_line=5, end_column=20, file="test.adl")
    assert loc.file == "test.adl"


# ============================================
# ASTNode Tests
# ============================================

def test_ast_node_accept():
    """Test ASTNode accept method"""
    loc = SourceLocation(line=1, column=1, end_line=1, end_column=10)
    node = ASTNode(loc)

    class TestVisitor(ASTVisitor[str]):
        def visit_default(self, node):
            return "default"

        # Implement all abstract methods
        def visit_Program(self, node):
            return "program"

        def visit_ImportStmt(self, node):
            return "import"

        def visit_EnumDef(self, node):
            return "enum"

        def visit_TypeDef(self, node):
            return "type"

        def visit_TypeBody(self, node):
            return "type_body"

        def visit_FieldDef(self, node):
            return "field"

        def visit_PrimitiveType(self, node):
            return "primitive"

        def visit_TypeReference(self, node):
            return "reference"

        def visit_ArrayType(self, node):
            return "array"

        def visit_UnionType(self, node):
            return "union"

        def visit_OptionalType(self, node):
            return "optional"

        def visit_ConstrainedType(self, node):
            return "constrained"

        def visit_AgentDef(self, node):
            return "agent"

    visitor = TestVisitor()
    result = node.accept(visitor)
    assert result == "default"


# ============================================
# Program Tests
# ============================================

def test_program_creation():
    """Test Program node creation"""
    loc = SourceLocation(line=1, column=1, end_line=1, end_column=10)
    program = Program(
        loc=loc,
        imports=[],
        declarations=[],
        agent=AgentDef(loc=loc, name="test_agent", fields=[])
    )
    assert program.agent.name == "test_agent"
    assert len(program.imports) == 0
    assert len(program.declarations) == 0


def test_program_with_imports():
    """Test Program with imports"""
    loc = SourceLocation(line=1, column=1, end_line=1, end_column=10)
    import_stmt = ImportStmt(loc=loc, path="some/path")
    program = Program(
        loc=loc,
        imports=[import_stmt],
        declarations=[],
        agent=AgentDef(loc=loc, name="test_agent", fields=[])
    )
    assert len(program.imports) == 1
    assert program.imports[0].path == "some/path"


# ============================================
# ImportStmt Tests
# ============================================

def test_import_stmt_basic():
    """Test ImportStmt basic creation"""
    loc = SourceLocation(line=1, column=1, end_line=1, end_column=10)
    import_stmt = ImportStmt(loc=loc, path="some/path")
    assert import_stmt.path == "some/path"
    assert import_stmt.alias is None


def test_import_stmt_with_alias():
    """Test ImportStmt with alias"""
    loc = SourceLocation(line=1, column=1, end_line=1, end_column=10)
    import_stmt = ImportStmt(loc=loc, path="some/path", alias="sp")
    assert import_stmt.path == "some/path"
    assert import_stmt.alias == "sp"


# ============================================
# EnumDef Tests
# ============================================

def test_enum_def_basic():
    """Test EnumDef basic creation"""
    loc = SourceLocation(line=1, column=1, end_line=1, end_column=10)
    enum_def = EnumDef(loc=loc, name="Status", values=["active", "inactive", "pending"])
    assert enum_def.name == "Status"
    assert len(enum_def.values) == 3
    assert enum_def.values == ["active", "inactive", "pending"]


# ============================================
# TypeDef Tests
# ============================================

def test_type_def_basic():
    """Test TypeDef basic creation"""
    loc = SourceLocation(line=1, column=1, end_line=1, end_column=10)
    type_def = TypeDef(loc=loc, name="User")
    assert type_def.name == "User"
    assert type_def.body is None
    assert type_def.alias is None


def test_type_def_with_body():
    """Test TypeDef with body"""
    loc = SourceLocation(line=1, column=1, end_line=1, end_column=10)
    field1 = FieldDef(loc=loc, name="id", type=PrimitiveType(loc=loc, name="integer"))
    field2 = FieldDef(loc=loc, name="name", type=PrimitiveType(loc=loc, name="string"))
    body = TypeBody(loc=loc, fields=[field1, field2])
    type_def = TypeDef(loc=loc, name="User", body=body)
    assert type_def.name == "User"
    assert type_def.body is not None
    assert len(type_def.body.fields) == 2


def test_type_def_with_alias():
    """Test TypeDef with alias"""
    loc = SourceLocation(line=1, column=1, end_line=1, end_column=10)
    type_def = TypeDef(loc=loc, name="User", alias=TypeReference(loc=loc, name="Person"))
    assert type_def.name == "User"
    assert type_def.alias is not None
    assert type_def.alias.name == "Person"


# ============================================
# TypeBody Tests
# ============================================

def test_type_body_basic():
    """Test TypeBody basic creation"""
    loc = SourceLocation(line=1, column=1, end_line=1, end_column=10)
    field = FieldDef(loc=loc, name="id", type=PrimitiveType(loc=loc, name="integer"))
    body = TypeBody(loc=loc, fields=[field])
    assert len(body.fields) == 1
    assert body.fields[0].name == "id"


# ============================================
# FieldDef Tests
# ============================================

def test_field_def_basic():
    """Test FieldDef basic creation"""
    loc = SourceLocation(line=1, column=1, end_line=1, end_column=10)
    field = FieldDef(loc=loc, name="id", type=PrimitiveType(loc=loc, name="integer"))
    assert field.name == "id"
    assert field.type.name == "integer"
    assert field.optional is False


def test_field_def_optional():
    """Test FieldDef with optional flag"""
    loc = SourceLocation(line=1, column=1, end_line=1, end_column=10)
    field = FieldDef(loc=loc, name="name", type=PrimitiveType(loc=loc, name="string"), optional=True)
    assert field.name == "name"
    assert field.optional is True


# ============================================
# PrimitiveType Tests
# ============================================

def test_primitive_type_basic():
    """Test PrimitiveType basic creation"""
    loc = SourceLocation(line=1, column=1, end_line=1, end_column=10)
    primitive = PrimitiveType(loc=loc, name="string")
    assert primitive.name == "string"


def test_primitive_type_variations():
    """Test various primitive types"""
    loc = SourceLocation(line=1, column=1, end_line=1, end_column=10)
    types = ["string", "integer", "number", "boolean", "object", "array", "any", "null"]
    for type_name in types:
        primitive = PrimitiveType(loc=loc, name=type_name)
        assert primitive.name == type_name


# ============================================
# TypeReference Tests
# ============================================

def test_type_reference_basic():
    """Test TypeReference basic creation"""
    loc = SourceLocation(line=1, column=1, end_line=1, end_column=10)
    ref = TypeReference(loc=loc, name="User")
    assert ref.name == "User"


# ============================================
# ArrayType Tests
# ============================================

def test_array_type_basic():
    """Test ArrayType basic creation"""
    loc = SourceLocation(line=1, column=1, end_line=1, end_column=10)
    element_type = PrimitiveType(loc=loc, name="string")
    array_type = ArrayType(loc=loc, element_type=element_type)
    assert array_type.element_type.name == "string"


# ============================================
# UnionType Tests
# ============================================

def test_union_type_basic():
    """Test UnionType basic creation"""
    loc = SourceLocation(line=1, column=1, end_line=1, end_column=10)
    type1 = PrimitiveType(loc=loc, name="string")
    type2 = PrimitiveType(loc=loc, name="integer")
    union_type = UnionType(loc=loc, types=[type1, type2])
    assert len(union_type.types) == 2


# ============================================
# OptionalType Tests
# ============================================

def test_optional_type_basic():
    """Test OptionalType basic creation"""
    loc = SourceLocation(line=1, column=1, end_line=1, end_column=10)
    inner_type = PrimitiveType(loc=loc, name="string")
    optional_type = OptionalType(loc=loc, inner_type=inner_type)
    assert optional_type.inner_type.name == "string"


# ============================================
# ConstrainedType Tests
# ============================================

def test_constrained_type_basic():
    """Test ConstrainedType basic creation"""
    loc = SourceLocation(line=1, column=1, end_line=1, end_column=10)
    base_type = PrimitiveType(loc=loc, name="integer")
    constrained_type = ConstrainedType(loc=loc, base_type=base_type, min_value=0, max_value=100)
    assert constrained_type.base_type.name == "integer"
    assert constrained_type.min_value == 0
    assert constrained_type.max_value == 100


def test_constrained_type_min_only():
    """Test ConstrainedType with min only"""
    loc = SourceLocation(line=1, column=1, end_line=1, end_column=10)
    base_type = PrimitiveType(loc=loc, name="integer")
    constrained_type = ConstrainedType(loc=loc, base_type=base_type, min_value=0)
    assert constrained_type.base_type.name == "integer"
    assert constrained_type.min_value == 0
    assert constrained_type.max_value is None


# ============================================
# AgentDef Tests
# ============================================

def test_agent_def_basic():
    """Test AgentDef basic creation"""
    loc = SourceLocation(line=1, column=1, end_line=1, end_column=10)
    field = FieldDef(loc=loc, name="id", type=PrimitiveType(loc=loc, name="integer"))
    agent = AgentDef(loc=loc, name="test_agent", fields=[field])
    assert agent.name == "test_agent"
    assert len(agent.fields) == 1


# ============================================
# Visitor Pattern Tests
# ============================================

def test_visitor_accept():
    """Test ASTVisitor accept method"""
    loc = SourceLocation(line=1, column=1, end_line=1, end_column=10)
    node = ASTNode(loc)

    class TestVisitor(ASTVisitor[str]):
        def visit_default(self, node):
            return "default"

        # Implement all abstract methods
        def visit_Program(self, node):
            return "program"

        def visit_ImportStmt(self, node):
            return "import"

        def visit_EnumDef(self, node):
            return "enum"

        def visit_TypeDef(self, node):
            return "type"

        def visit_TypeBody(self, node):
            return "type_body"

        def visit_FieldDef(self, node):
            return "field"

        def visit_PrimitiveType(self, node):
            return "primitive"

        def visit_TypeReference(self, node):
            return "reference"

        def visit_ArrayType(self, node):
            return "array"

        def visit_UnionType(self, node):
            return "union"

        def visit_OptionalType(self, node):
            return "optional"

        def visit_ConstrainedType(self, node):
            return "constrained"

        def visit_AgentDef(self, node):
            return "agent"

    visitor = TestVisitor()
    result = visitor.visit(node)
    assert result == "default"


def test_visitor_default_method():
    """Test visitor's visit_default method is called for unhandled node types"""
    loc = SourceLocation(line=1, column=1, end_line=1, end_column=10)
    node = ASTNode(loc)

    class DefaultVisitor(ASTVisitor[str]):
        def visit_default(self, node):
            return "default"

        # Implement all abstract methods
        def visit_Program(self, node):
            return "program"

        def visit_ImportStmt(self, node):
            return "import"

        def visit_EnumDef(self, node):
            return "enum"

        def visit_TypeDef(self, node):
            return "type"

        def visit_TypeBody(self, node):
            return "type_body"

        def visit_FieldDef(self, node):
            return "field"

        def visit_PrimitiveType(self, node):
            return "primitive"

        def visit_TypeReference(self, node):
            return "reference"

        def visit_ArrayType(self, node):
            return "array"

        def visit_UnionType(self, node):
            return "union"

        def visit_OptionalType(self, node):
            return "optional"

        def visit_ConstrainedType(self, node):
            return "constrained"

        def visit_AgentDef(self, node):
            return "agent"

    visitor = DefaultVisitor()
    result = visitor.visit(node)
    assert result == "default"


# ============================================
# PrintVisitor Tests
# ============================================

def test_print_visitor_program():
    """Test PrintVisitor on Program"""
    loc = SourceLocation(line=1, column=1, end_line=1, end_column=10)
    program = Program(
        loc=loc,
        imports=[],
        declarations=[],
        agent=AgentDef(loc=loc, name="test_agent", fields=[])
    )
    visitor = PrintVisitor()
    output = visitor.visit(program)
    assert "Program" in output
    assert "test_agent" in output


def test_print_visitor_import():
    """Test PrintVisitor on ImportStmt"""
    loc = SourceLocation(line=1, column=1, end_line=1, end_column=10)
    import_stmt = ImportStmt(loc=loc, path="some/path")
    visitor = PrintVisitor()
    output = visitor.visit(import_stmt)
    assert "Import:" in output
    assert "some/path" in output


def test_print_visitor_enum():
    """Test PrintVisitor on EnumDef"""
    loc = SourceLocation(line=1, column=1, end_line=1, end_column=10)
    enum_def = EnumDef(loc=loc, name="Status", values=["active", "inactive"])
    visitor = PrintVisitor()
    output = visitor.visit(enum_def)
    assert "Enum:" in output
    assert "Status" in output
    assert "active" in output


def test_print_visitor_type():
    """Test PrintVisitor on TypeDef"""
    loc = SourceLocation(line=1, column=1, end_line=1, end_column=10)
    type_def = TypeDef(loc=loc, name="User")
    visitor = PrintVisitor()
    output = visitor.visit(type_def)
    assert "Type:" in output
    assert "User" in output


def test_print_visitor_type_with_body():
    """Test PrintVisitor on TypeDef with body"""
    loc = SourceLocation(line=1, column=1, end_line=1, end_column=10)
    field = FieldDef(loc=loc, name="id", type=PrimitiveType(loc=loc, name="integer"))
    body = TypeBody(loc=loc, fields=[field])
    type_def = TypeDef(loc=loc, name="User", body=body)
    visitor = PrintVisitor()
    output = visitor.visit(type_def)
    assert "Type:" in output
    assert "User" in output
    assert "Fields:" in output


def test_print_visitor_field():
    """Test PrintVisitor on FieldDef"""
    loc = SourceLocation(line=1, column=1, end_line=1, end_column=10)
    field = FieldDef(loc=loc, name="id", type=PrimitiveType(loc=loc, name="integer"))
    visitor = PrintVisitor()
    output = visitor.visit(field)
    assert "id:" in output
    assert "integer" in output


def test_print_visitor_primitive():
    """Test PrintVisitor on PrimitiveType"""
    loc = SourceLocation(line=1, column=1, end_line=1, end_column=10)
    primitive = PrimitiveType(loc=loc, name="string")
    visitor = PrintVisitor()
    output = visitor.visit(primitive)
    assert output == "string"


def test_print_visitor_type_reference():
    """Test PrintVisitor on TypeReference"""
    loc = SourceLocation(line=1, column=1, end_line=1, end_column=10)
    ref = TypeReference(loc=loc, name="User")
    visitor = PrintVisitor()
    output = visitor.visit(ref)
    assert output == "User"


def test_print_visitor_array():
    """Test PrintVisitor on ArrayType"""
    loc = SourceLocation(line=1, column=1, end_line=1, end_column=10)
    element_type = PrimitiveType(loc=loc, name="string")
    array_type = ArrayType(loc=loc, element_type=element_type)
    visitor = PrintVisitor()
    output = visitor.visit(array_type)
    assert "string[]" in output


def test_print_visitor_union():
    """Test PrintVisitor on UnionType"""
    loc = SourceLocation(line=1, column=1, end_line=1, end_column=10)
    type1 = PrimitiveType(loc=loc, name="string")
    type2 = PrimitiveType(loc=loc, name="integer")
    union_type = UnionType(loc=loc, types=[type1, type2])
    visitor = PrintVisitor()
    output = visitor.visit(union_type)
    assert "string" in output
    assert "integer" in output


def test_print_visitor_optional():
    """Test PrintVisitor on OptionalType"""
    loc = SourceLocation(line=1, column=1, end_line=1, end_column=10)
    inner_type = PrimitiveType(loc=loc, name="string")
    optional_type = OptionalType(loc=loc, inner_type=inner_type)
    visitor = PrintVisitor()
    output = visitor.visit(optional_type)
    assert "string?" in output


def test_print_visitor_constrained():
    """Test PrintVisitor on ConstrainedType"""
    loc = SourceLocation(line=1, column=1, end_line=1, end_column=10)
    base_type = PrimitiveType(loc=loc, name="integer")
    constrained_type = ConstrainedType(loc=loc, base_type=base_type, min_value=0, max_value=100)
    visitor = PrintVisitor()
    output = visitor.visit(constrained_type)
    assert "integer(0..100)" in output


def test_print_visitor_agent():
    """Test PrintVisitor on AgentDef"""
    loc = SourceLocation(line=1, column=1, end_line=1, end_column=10)
    field = FieldDef(loc=loc, name="id", type=PrimitiveType(loc=loc, name="integer"))
    agent = AgentDef(loc=loc, name="test_agent", fields=[field])
    visitor = PrintVisitor()
    output = visitor.visit(agent)
    assert "Agent:" in output
    assert "test_agent" in output