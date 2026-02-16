#!/usr/bin/env python3
"""
Unit tests for the ADL DSL Parser.

Tests the formal grammar and AST generation for ADL DSL files.
"""

import os
import sys
import unittest
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from tools.dsl.parser import parse_adl, parse_adl_file
from tools.dsl.ast import (
    Program, ImportStmt, EnumDef, TypeDef, AgentDef,
    FieldDef, PrimitiveType, TypeReference, ArrayType, UnionType, ConstrainedType
)


class TestADLParser(unittest.TestCase):
    """Test cases for the ADL DSL parser."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.test_dir = Path(__file__).parent.parent / "fixtures" / "dsl"
        self.test_dir.mkdir(parents=True, exist_ok=True)
        
    def test_parse_minimal_adl(self):
        """Test parsing a minimal ADL file."""
        dsl_content = """
agent MinimalAgent {
    name: string
    description: string
}
"""
        ast = parse_adl(dsl_content)
        self.assertIsInstance(ast, Program)
        self.assertEqual(len(ast.imports), 0)
        self.assertEqual(len(ast.enums), 0)
        self.assertEqual(len(ast.types), 0)
        self.assertIsInstance(ast.agent, AgentDef)
        self.assertEqual(ast.agent.name, "MinimalAgent")
        self.assertEqual(len(ast.agent.fields), 2)
        
    def test_parse_import(self):
        """Test parsing import statements."""
        dsl_content = """
import schema/components/rag
import schema/components/tool
import schema/components/memory
import schema/components/common
"""
        ast = parse_adl(dsl_content)
        self.assertIsInstance(ast, Program)
        self.assertEqual(len(ast.imports), 4)
        self.assertEqual(ast.imports[0].path, "schema/components/rag")
        self.assertEqual(ast.imports[1].path, "schema/components/tool")
        
    def test_parse_enum(self):
        """Test parsing enum definitions."""
        dsl_content = """
enum Status {
    active
    inactive
    pending
}
"""
        ast = parse_adl(dsl_content)
        self.assertIsInstance(ast, Program)
        self.assertEqual(len(ast.enums), 1)
        enum = ast.enums[0]
        self.assertEqual(enum.name, "Status")
        self.assertEqual(len(enum.values), 3)
        self.assertEqual(enum.values[0], "active")
        
    def test_parse_type(self):
        """Test parsing type definitions."""
        dsl_content = """
type User {
    id: string
    name: string
    email: string?
}
"""
        ast = parse_adl(dsl_content)
        self.assertIsInstance(ast, Program)
        self.assertEqual(len(ast.types), 1)
        type_def = ast.types[0]
        self.assertEqual(type_def.name, "User")
        self.assertEqual(len(type_def.fields), 3)
        
    def test_parse_complex_type(self):
        """Test parsing complex type definitions."""
        dsl_content = """
type ComplexType {
    id: string
    name: string
    tags: string[]
    metadata: object
    optional_field: string?
    array_of_types: TypeReference[]
    union_type: string | number
    constrained_int: integer (1..10)
    optional_array: string[]?
}
"""
        ast = parse_adl(dsl_content)
        self.assertIsInstance(ast, Program)
        
    def test_parse_file(self):
        """Test parsing an ADL file from disk."""
        test_file = self.test_dir / "minimal.adl"
        test_content = """
agent TestAgent {
    field1: string
    field2: integer?
}
"""
        test_file.write_text(test_content)
        
        try:
            ast = parse_adl_file(str(test_file))
            self.assertIsInstance(ast, Program)
            self.assertEqual(ast.agent.name, "TestAgent")
        finally:
            test_file.unlink()
            
    def test_parse_error(self):
        """Test parsing error handling."""
        invalid_dsl = """
agent InvalidAgent {
    missing_colon string  # Missing colon
}
"""
        with self.assertRaises(Exception):
            parse_adl(invalid_dsl)
            
    def test_parse_with_comments(self):
        """Test parsing with comments."""
        dsl_with_comments = """
# This is a comment
import schema/components/rag  # Another comment

# Enum definition
enum Status {
    active  # Active status
    inactive  # Inactive status
}

agent TestAgent {
    name: string
    age: integer?
}
"""
        ast = parse_adl(dsl_with_comments)
        self.assertIsInstance(ast, Program)
        self.assertEqual(ast.agent.name, "TestAgent")
        
    def test_parse_all_constructs(self):
        """Test parsing all DSL constructs together."""
        dsl_content = """
# Import statements
import schema/components/rag
import schema/components/tool

# Enum definitions
enum Lifecycle {
    stable
    beta
    deprecated
    experimental
}

enum Status {
    active
    inactive
    pending
}



# Type definitions
type User {
    id: string
    name: string
    email: string?
}

type Product {
    id: string
    name: string
    price: number
    tags: string[]
}



# Agent definition
agent ECommerceAgent {
    id: string
    name: string
    description: string
    users: User[]
    products: Product[]
}
"""
        ast = parse_adl(dsl_content)
        self.assertIsInstance(ast, Program)
        self.assertEqual(len(ast.imports), 2)
        self.assertEqual(len(ast.enums), 2)
        self.assertEqual(len(ast.types), 2)
        self.assertEqual(ast.agent.name, "ECommerceAgent")
        
    def test_parse_empty_file(self):
        """Test parsing an empty file."""
        empty_content = ""
        ast = parse_adl(empty_content)
        self.assertIsInstance(ast, Program)
        self.assertEqual(len(ast.imports), 0)
        self.assertEqual(len(ast.enums), 0)
        self.assertEqual(len(ast.types), 0)
        self.assertIsNone(ast.agent)
        
    def test_parse_only_imports(self):
        """Test parsing a file with only import statements."""
        dsl_content = """
import schema/components/rag
import schema/components/tool
import schema/components/memory
"""
        ast = parse_adl(dsl_content)
        self.assertIsInstance(ast, Program)
        self.assertEqual(len(ast.imports), 3)
        
    def test_parse_only_enums(self):
        """Test parsing a file with only enum definitions."""
        dsl_content = """
enum Lifecycle {
    stable
    beta
    deprecated
    experimental
}
"""
        ast = parse_adl(dsl_content)
        self.assertIsInstance(ast, Program)
        self.assertEqual(len(ast.enums), 1)
        
    def test_parse_only_types(self):
        """Test parsing a file with only type definitions."""
        dsl_content = """
type User {
    id: string
    name: string
    email: string?
}
"""
        ast = parse_adl(dsl_content)
        self.assertIsInstance(ast, Program)
        self.assertEqual(len(ast.types), 1)
        
    def test_parse_only_agent(self):
        """Test parsing a file with only agent definition."""
        dsl_content = """
agent MinimalAgent {
    name: string
}
"""
        ast = parse_adl(dsl_content)
        self.assertIsInstance(ast, Program)
        self.assertEqual(ast.agent.name, "MinimalAgent")
        

if __name__ == '__main__':
    unittest.main()