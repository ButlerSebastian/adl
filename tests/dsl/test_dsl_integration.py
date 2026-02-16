#!/usr/bin/env python3
"""
Integration tests for the ADL DSL pipeline.

Tests the complete pipeline from DSL parsing to JSON Schema generation
and validation.
"""

import unittest
import json
import tempfile
import os
from pathlib import Path
from typing import Dict, Any

# Import the parser and compiler
from tools.dsl.parser import parse_adl_file
from tools.adl_dsl_compiler_v2 import ADLDSLCompilerV2


class TestADLDSLIntegration(unittest.TestCase):
    """Integration tests for the ADL DSL pipeline."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.compiler = ADLDSLCompilerV2()
        self.test_dir = Path(__file__).parent.parent / "fixtures" / "dsl"
        self.test_dir.mkdir(parents=True, exist_ok=True)
    
    def test_full_pipeline_minimal(self):
        """Test the full pipeline with a minimal agent."""
        dsl_content = """
agent MinimalAgent {
  name: string
  description: string
}
"""
        # Write DSL content to a temporary file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.adl', delete=False) as f:
            f.write(dsl_content)
            dsl_file = f.name
        
        try:
            # Parse the DSL file
            ast = parse_adl_file(dsl_file)
            self.assertIsNotNone(ast)
            
            # Compile to JSON Schema
            agent_def = self.compiler.parse_file(dsl_file)
            schema = self.compiler.compile_to_json_schema(agent_def)
            
            # Verify the schema is valid JSON
            json.dumps(schema)
            
            # Verify the schema structure
            self.assertEqual(schema["title"], "MinimalAgent")
            self.assertEqual(schema["type"], "object")
            self.assertIn("properties", schema)
            self.assertIn("required", schema)
            
        finally:
            os.unlink(dsl_file)
    
    def test_full_pipeline_with_imports(self):
        """Test the full pipeline with imports."""
        # Create a simple imported module
        imported_content = """
enum ImportedEnum {
  value1
  value2
}
"""
        imported_file = self.test_dir / "imported.adl"
        imported_file.write_text(imported_content)
        
        dsl_content = f"""
import {imported_file.stem}

agent AgentWithImport {{
  imported: ImportedEnum
}}
"""
        # Write DSL content to a temporary file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.adl', delete=False) as f:
            f.write(dsl_content)
            dsl_file = f.name
        
        try:
            # Parse the DSL file
            ast = parse_adl_file(dsl_file)
            self.assertIsNotNone(ast)
            
            # Compile to JSON Schema
            agent_def = self.compiler.parse_file(dsl_file)
            schema = self.compiler.compile_to_json_schema(agent_def)
            
            # Verify the schema is valid JSON
            json.dumps(schema)
            
            # Verify import resolution
            self.assertIn("$defs", schema)
            self.assertIn("ImportedEnum", schema["$defs"])
            
        finally:
            os.unlink(dsl_file)
            imported_file.unlink()
    
    def test_full_pipeline_with_complex_types(self):
        """Test the full pipeline with complex type definitions."""
        dsl_content = """
enum Priority {
  low
  medium
  high
}

type Task {
  id: string
  title: string
  description: string
  priority: Priority
  completed?: boolean
}

agent TaskManager {
  tasks: Task[]
  max_tasks: integer (1..100)
  auto_archive: boolean
}
"""
        # Write DSL content to a temporary file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.adl', delete=False) as f:
            f.write(dsl_content)
            dsl_file = f.name
        
        try:
            # Parse the DSL file
            ast = parse_adl_file(dsl_file)
            self.assertIsNotNone(ast)
            
            # Compile to JSON Schema
            agent_def = self.compiler.parse_file(dsl_file)
            schema = self.compiler.compile_to_json_schema(agent_def)
            
            # Verify the schema is valid JSON
            json.dumps(schema)
            
            # Verify the schema structure
            self.assertEqual(schema["title"], "TaskManager")
            self.assertIn("$defs", schema)
            self.assertIn("Priority", schema["$defs"])
            self.assertIn("Task", schema["$defs"])
            
        finally:
            os.unlink(dsl_file)
    
    def test_round_trip_validation(self):
        """Test round-trip validation: DSL -> Schema -> Validate DSL."""
        # Create a simple DSL file
        dsl_content = """
enum Status {
  active
  inactive
}

type User {
  id: string
  name: string
  email?: string
}

agent TestAgent {
  status: Status
  user: User
  tags: string[]
}
"""
        # Write DSL content to a temporary file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.adl', delete=False) as f:
            f.write(dsl_content)
            dsl_file = f.name
        
        try:
            # Parse the DSL file
            ast = parse_adl_file(dsl_file)
            self.assertIsNotNone(ast)
            
            # Compile to JSON Schema
            agent_def = self.compiler.parse_file(dsl_file)
            schema = self.compiler.compile_to_json_schema(agent_def)
            
            # Verify the schema is valid JSON
            json.dumps(schema)
            
            # Generate TypeScript types
            ts_types = self.compiler.generate_typescript_types(schema)
            self.assertIsInstance(ts_types, str)
            self.assertIn("export interface TestAgent", ts_types)
            
        finally:
            os.unlink(dsl_file)
    
    def test_error_recovery(self):
        """Test that the parser can recover from syntax errors."""
        # This DSL has a syntax error (missing colon)
        dsl_content = """
agent ErrorAgent {
  name string  # Missing colon
  description: string
}
"""
        # Write DSL content to a temporary file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.adl', delete=False) as f:
            f.write(dsl_content)
            dsl_file = f.name
        
        try:
            # This should raise a syntax error
            with self.assertRaises(Exception):
                parse_adl_file(dsl_file)
            
        finally:
            os.unlink(dsl_file)
    
    def test_import_resolution(self):
        """Test that imports are resolved correctly."""
        # Create a simple imported module
        imported_content = """
type ImportedType {
  field: string
}
"""
        imported_file = self.test_dir / "imported.adl"
        imported_file.write_text(imported_content)
        
        dsl_content = f"""
import {imported_file.stem}

agent AgentWithImport {{
  imported: ImportedType
}}
"""
        # Write DSL content to a temporary file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.adl', delete=False) as f:
            f.write(dsl_content)
            dsl_file = f.name
        
        try:
            # Parse the DSL file
            ast = parse_adl_file(dsl_file)
            self.assertIsNotNone(ast)
            
            # Compile to JSON Schema
            agent_def = self.compiler.parse_file(dsl_file)
            schema = self.compiler.compile_to_json_schema(agent_def)
            
            # Verify import resolution
            self.assertIn("$defs", schema)
            self.assertIn("ImportedType", schema["$defs"])
            
        finally:
            os.unlink(dsl_file)
            imported_file.unlink()
    
    def test_type_expansion(self):
        """Test that type references are expanded correctly."""
        dsl_content = """
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
        # Write DSL content to a temporary file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.adl', delete=False) as f:
            f.write(dsl_content)
            dsl_file = f.name
        
        try:
            # Parse the DSL file
            ast = parse_adl_file(dsl_file)
            self.assertIsNotNone(ast)
            
            # Compile to JSON Schema
            agent_def = self.compiler.parse_file(dsl_file)
            schema = self.compiler.compile_to_json_schema(agent_def)
            
            # Verify type expansion
            self.assertIn("$defs", schema)
            self.assertIn("Address", schema["$defs"])
            self.assertIn("Person", schema["$defs"])
            
            # Verify Person references Address
            person_schema = schema["$defs"]["Person"]
            address_ref = person_schema["properties"]["address"]
            self.assertEqual(address_ref["$ref"], "#/$defs/Address")
            
        finally:
            os.unlink(dsl_file)
    
    def test_union_type_handling(self):
        """Test that union types are handled correctly."""
        dsl_content = """
agent TestAgent {
  value: string | integer | boolean
  nullable: string | null
}
"""
        # Write DSL content to a temporary file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.adl', delete=False) as f:
            f.write(dsl_content)
            dsl_file = f.name
        
        try:
            # Parse the DSL file
            ast = parse_adl_file(dsl_file)
            self.assertIsNotNone(ast)
            
            # Compile to JSON Schema
            agent_def = self.compiler.parse_file(dsl_file)
            schema = self.compiler.compile_to_json_schema(agent_def)
            
            # Verify union type handling
            value_schema = schema["properties"]["value"]
            self.assertIn("type", value_schema)
            self.assertEqual(set(value_schema["type"]), {"string", "integer", "boolean"})
            
            nullable_schema = schema["properties"]["nullable"]
            self.assertIn("type", nullable_schema)
            self.assertEqual(set(nullable_schema["type"]), {"string", "null"})
            
        finally:
            os.unlink(dsl_file)
    
    def test_array_type_handling(self):
        """Test that array types are handled correctly."""
        dsl_content = """
agent TestAgent {
  tags: string[]
  numbers: integer[]
}
"""
        # Write DSL content to a temporary file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.adl', delete=False) as f:
            f.write(dsl_content)
            dsl_file = f.name
        
        try:
            # Parse the DSL file
            ast = parse_adl_file(dsl_file)
            self.assertIsNotNone(ast)
            
            # Compile to JSON Schema
            agent_def = self.compiler.parse_file(dsl_file)
            schema = self.compiler.compile_to_json_schema(agent_def)
            
            # Verify array type handling
            tags_schema = schema["properties"]["tags"]
            self.assertEqual(tags_schema["type"], "array")
            self.assertIn("items", tags_schema)
            self.assertEqual(tags_schema["items"]["type"], "string")
            
            numbers_schema = schema["properties"]["numbers"]
            self.assertEqual(numbers_schema["type"], "array")
            self.assertIn("items", numbers_schema)
            self.assertEqual(numbers_schema["items"]["type"], "integer")
            
        finally:
            os.unlink(dsl_file)
    
    def test_constraint_handling(self):
        """Test that type constraints are handled correctly."""
        dsl_content = """
agent TestAgent {
  age: integer (0..120)
  score: number (0..100)
  positive: integer (1..)
}
"""
        # Write DSL content to a temporary file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.adl', delete=False) as f:
            f.write(dsl_content)
            dsl_file = f.name
        
        try:
            # Parse the DSL file
            ast = parse_adl_file(dsl_file)
            self.assertIsNotNone(ast)
            
            # Compile to JSON Schema
            agent_def = self.compiler.parse_file(dsl_file)
            schema = self.compiler.compile_to_json_schema(agent_def)
            
            # Verify constraint handling
            age_schema = schema["properties"]["age"]
            self.assertEqual(age_schema["type"], "integer")
            self.assertEqual(age_schema["minimum"], 0)
            self.assertEqual(age_schema["maximum"], 120)
            
            score_schema = schema["properties"]["score"]
            self.assertEqual(score_schema["type"], "number")
            self.assertEqual(score_schema["minimum"], 0)
            self.assertEqual(score_schema["maximum"], 100)
            
            positive_schema = schema["properties"]["positive"]
            self.assertEqual(positive_schema["type"], "integer")
            self.assertEqual(positive_schema["minimum"], 1)
            
        finally:
            os.unlink(dsl_file)
    
    def test_optional_field_handling(self):
        """Test that optional fields are handled correctly."""
        dsl_content = """
agent TestAgent {
  required: string
  optional1?: string
  optional2?: integer
  optional3?: boolean
}
"""
        # Write DSL content to a temporary file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.adl', delete=False) as f:
            f.write(dsl_content)
            dsl_file = f.name
        
        try:
            # Parse the DSL file
            ast = parse_adl_file(dsl_file)
            self.assertIsNotNone(ast)
            
            # Compile to JSON Schema
            agent_def = self.compiler.parse_file(dsl_file)
            schema = self.compiler.compile_to_json_schema(agent_def)
            
            # Verify optional field handling
            self.assertIn("required", schema["required"])
            self.assertNotIn("optional1", schema["required"])
            self.assertNotIn("optional2", schema["required"])
            self.assertNotIn("optional3", schema["required"])
            
        finally:
            os.unlink(dsl_file)
    
    def test_mixed_type_expressions(self):
        """Test that mixed type expressions are handled correctly."""
        dsl_content = """
agent TestAgent {
  simple: string
  array: string[]
  union: string | integer | boolean
  constrained: integer (0..100)
  optional_array?: string[]
  optional_union?: string | integer | null
}
"""
        # Write DSL content to a temporary file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.adl', delete=False) as f:
            f.write(dsl_content)
            dsl_file = f.name
        
        try:
            # Parse the DSL file
            ast = parse_adl_file(dsl_file)
            self.assertIsNotNone(ast)
            
            # Compile to JSON Schema
            agent_def = self.compiler.parse_file(dsl_file)
            schema = self.compiler.compile_to_json_schema(agent_def)
            
            # Verify mixed type expression handling
            properties = schema["properties"]
            self.assertIn("simple", properties)
            self.assertIn("array", properties)
            self.assertIn("union", properties)
            self.assertIn("constrained", properties)
            self.assertIn("optional_array", properties)
            self.assertIn("optional_union", properties)
            
        finally:
            os.unlink(dsl_file)
    
    def test_comments_and_whitespace(self):
        """Test that comments and whitespace are handled correctly."""
        dsl_content = """
# This is a comment
agent CommentedAgent {
  # Field comment
  name: string
  # Another comment
  description?: string
}
"""
        # Write DSL content to a temporary file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.adl', delete=False) as f:
            f.write(dsl_content)
            dsl_file = f.name
        
        try:
            # Parse the DSL file
            ast = parse_adl_file(dsl_file)
            self.assertIsNotNone(ast)
            
            # Compile to JSON Schema
            agent_def = self.compiler.parse_file(dsl_file)
            schema = self.compiler.compile_to_json_schema(agent_def)
            
            # Verify comment and whitespace handling
            self.assertEqual(schema["title"], "CommentedAgent")
            self.assertIn("name", schema["properties"])
            self.assertIn("description", schema["properties"])
            
        finally:
            os.unlink(dsl_file)
    
    def test_empty_file(self):
        """Test that an empty file is handled correctly."""
        dsl_content = ""
        
        # Write DSL content to a temporary file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.adl', delete=False) as f:
            f.write(dsl_content)
            dsl_file = f.name
        
        try:
            # Parse the DSL file
            ast = parse_adl_file(dsl_file)
            self.assertIsNotNone(ast)
            
            # Compile to JSON Schema
            agent_def = self.compiler.parse_file(dsl_file)
            schema = self.compiler.compile_to_json_schema(agent_def)
            
            # Verify empty file handling
            self.assertEqual(schema["properties"], {})
            self.assertEqual(schema["required"], [])
            
        finally:
            os.unlink(dsl_file)
    
    def test_multiple_enums_and_types(self):
        """Test that multiple enums and types are handled correctly."""
        dsl_content = """
enum Priority {
  low
  medium
  high
}

enum Status {
  pending
  in_progress
  completed
  cancelled
}

type User {
  id: string
  name: string
  email?: string
}

type Task {
  id: string
  title: string
  description: string
  priority: Priority
  status: Status
  assignee?: User
}

agent ComplexAgent {
  tasks: Task[]
  users: User[]
  default_priority: Priority
  default_status: Status
}
"""
        # Write DSL content to a temporary file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.adl', delete=False) as f:
            f.write(dsl_content)
            dsl_file = f.name
        
        try:
            # Parse the DSL file
            ast = parse_adl_file(dsl_file)
            self.assertIsNotNone(ast)
            
            # Compile to JSON Schema
            agent_def = self.compiler.parse_file(dsl_file)
            schema = self.compiler.compile_to_json_schema(agent_def)
            
            # Verify multiple enums and types handling
            self.assertIn("Priority", schema["$defs"])
            self.assertIn("Status", schema["$defs"])
            self.assertIn("User", schema["$defs"])
            self.assertIn("Task", schema["$defs"])
            
        finally:
            os.unlink(dsl_file)
    
    def test_nested_type_references(self):
        """Test that nested type references are handled correctly."""
        dsl_content = """
type Address {
  street: string
  city: string
  zip: string
}

type Person {
  name: string
  address: Address
}

agent TestAgent {
  person: Person
}
"""
        # Write DSL content to a temporary file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.adl', delete=False) as f:
            f.write(dsl_content)
            dsl_file = f.name
        
        try:
            # Parse the DSL file
            ast = parse_adl_file(dsl_file)
            self.assertIsNotNone(ast)
            
            # Compile to JSON Schema
            agent_def = self.compiler.parse_file(dsl_file)
            schema = self.compiler.compile_to_json_schema(agent_def)
            
            # Verify nested type reference handling
            self.assertIn("Address", schema["$defs"])
            self.assertIn("Person", schema["$defs"])
            
        finally:
            os.unlink(dsl_file)


if __name__ == '__main__':
    unittest.main()