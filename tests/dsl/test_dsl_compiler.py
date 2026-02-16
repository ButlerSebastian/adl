#!/usr/bin/env python3
"""
Tests for the ADL DSL Compiler.

These tests verify that the compiler correctly transforms DSL AST into
JSON Schema and TypeScript types.
"""

import unittest
import json
from pathlib import Path
from typing import Dict, Any

# Import the compiler
from tools.adl_dsl_compiler_v2 import ADLDSLCompilerV2


class TestADLDSLCompiler(unittest.TestCase):
    """Test cases for the ADL DSL Compiler."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.compiler = ADLDSLCompilerV2()
        self.test_dir = Path(__file__).parent.parent / "fixtures" / "dsl"
        self.test_dir.mkdir(parents=True, exist_ok=True)
    
    def test_compile_minimal_agent(self):
        """Test compiling a minimal agent definition."""
        dsl_content = """
agent MinimalAgent {
  name: string
  description: string
}
"""
        # Parse the DSL
        agent_def = self.compiler.parse_file_from_content(dsl_content)
        
        # Compile to JSON Schema
        schema = self.compiler.compile_to_json_schema(agent_def)
        
        # Verify the schema structure
        self.assertEqual(schema["$schema"], "https://json-schema.org/draft/2020-12/schema")
        self.assertEqual(schema["title"], "MinimalAgent")
        self.assertEqual(schema["type"], "object")
        self.assertIn("properties", schema)
        self.assertIn("required", schema)
        self.assertIn("additionalProperties", schema)
        
        # Verify properties
        self.assertIn("name", schema["properties"])
        self.assertIn("description", schema["properties"])
        
        # Verify required fields
        self.assertIn("name", schema["required"])
        self.assertIn("description", schema["required"])
        
        # Verify additionalProperties
        self.assertFalse(schema["additionalProperties"])
    
    def test_compile_with_enums(self):
        """Test compiling with enum definitions."""
        dsl_content = """
enum Status {
  active
  inactive
  pending
}

agent AgentWithEnum {
  status: Status
}
"""
        # Parse the DSL
        agent_def = self.compiler.parse_file_from_content(dsl_content)
        
        # Compile to JSON Schema
        schema = self.compiler.compile_to_json_schema(agent_def)
        
        # Verify the schema structure
        self.assertIn("$defs", schema)
        self.assertIn("Status", schema["$defs"])
        
        # Verify enum schema
        status_schema = schema["$defs"]["Status"]
        self.assertEqual(status_schema["type"], "string")
        self.assertIn("enum", status_schema)
        self.assertEqual(set(status_schema["enum"]), {"active", "inactive", "pending"})
    
    def test_compile_with_types(self):
        """Test compiling with type definitions."""
        dsl_content = """
type User {
  id: string
  name: string
  email: string?
}

agent AgentWithType {
  user: User
}
"""
        # Parse the DSL
        agent_def = self.compiler.parse_file_from_content(dsl_content)
        
        # Compile to JSON Schema
        schema = self.compiler.compile_to_json_schema(agent_def)
        
        # Verify the schema structure
        self.assertIn("$defs", schema)
        self.assertIn("User", schema["$defs"])
        
        # Verify type schema
        user_schema = schema["$defs"]["User"]
        self.assertEqual(user_schema["type"], "object")
        self.assertIn("properties", user_schema)
        self.assertIn("required", user_schema)
        
        # Verify User properties
        self.assertIn("id", user_schema["properties"])
        self.assertIn("name", user_schema["properties"])
        self.assertIn("email", user_schema["properties"])
        
        # Verify required fields
        self.assertIn("id", user_schema["required"])
        self.assertIn("name", user_schema["required"])
        self.assertNotIn("email", user_schema["required"])
    
    def test_compile_with_arrays(self):
        """Test compiling with array types."""
        dsl_content = """
agent AgentWithArray {
  tags: string[]
  numbers: integer[]
}
"""
        # Parse the DSL
        agent_def = self.compiler.parse_file_from_content(dsl_content)
        
        # Compile to JSON Schema
        schema = self.compiler.compile_to_json_schema(agent_def)
        
        # Verify array properties
        tags_schema = schema["properties"]["tags"]
        self.assertEqual(tags_schema["type"], "array")
        self.assertIn("items", tags_schema)
        self.assertEqual(tags_schema["items"]["type"], "string")
        
        numbers_schema = schema["properties"]["numbers"]
        self.assertEqual(numbers_schema["type"], "array")
        self.assertIn("items", numbers_schema)
        self.assertEqual(numbers_schema["items"]["type"], "integer")
    
    def test_compile_with_unions(self):
        """Test compiling with union types."""
        dsl_content = """
agent AgentWithUnion {
  value: string | integer | boolean
  nullable: string | null
}
"""
        # Parse the DSL
        agent_def = self.compiler.parse_file_from_content(dsl_content)
        
        # Compile to JSON Schema
        schema = self.compiler.compile_to_json_schema(agent_def)
        
        # Verify union properties
        value_schema = schema["properties"]["value"]
        self.assertIn("type", value_schema)
        self.assertEqual(set(value_schema["type"]), {"string", "integer", "boolean"})
        
        nullable_schema = schema["properties"]["nullable"]
        self.assertIn("type", nullable_schema)
        self.assertEqual(set(nullable_schema["type"]), {"string", "null"})
    
    def test_compile_with_constraints(self):
        """Test compiling with type constraints."""
        dsl_content = """
agent AgentWithConstraints {
  age: integer (0..120)
  score: number (0..100)
  positive: integer (1..)
}
"""
        # Parse the DSL
        agent_def = self.compiler.parse_file_from_content(dsl_content)
        
        # Compile to JSON Schema
        schema = self.compiler.compile_to_json_schema(agent_def)
        
        # Verify constraint properties
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
    
    def test_compile_with_imports(self):
        """Test compiling with import statements."""
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
        # Parse the DSL
        agent_def = self.compiler.parse_file_from_content(dsl_content)
        
        # Compile to JSON Schema
        schema = self.compiler.compile_to_json_schema(agent_def)
        
        # Verify import resolution
        self.assertIn("$defs", schema)
        self.assertIn("ImportedEnum", schema["$defs"])
        
        # Clean up
        imported_file.unlink()
    
    def test_generate_typescript_types(self):
        """Test generating TypeScript type definitions."""
        dsl_content = """
enum Status {
  active
  inactive
}

type User {
  id: string
  name: string
  email: string?
}

agent TestAgent {
  status: Status
  user: User
  tags: string[]
}
"""
        # Parse the DSL
        agent_def = self.compiler.parse_file_from_content(dsl_content)
        
        # Compile to JSON Schema
        schema = self.compiler.compile_to_json_schema(agent_def)
        
        # Generate TypeScript types
        ts_types = self.compiler.generate_typescript_types(schema)
        
        # Verify TypeScript types are generated
        self.assertIsInstance(ts_types, str)
        self.assertIn("export interface TestAgent", ts_types)
        self.assertIn("export type Status", ts_types)
        self.assertIn("export interface User", ts_types)
        
        # Verify the structure
        self.assertIn("status: Status", ts_types)
        self.assertIn("user: User", ts_types)
        self.assertIn("tags: string[]", ts_types)
    
    def test_compile_complex_example(self):
        """Test compiling a complex example."""
        dsl_content = """
import schema/components/common

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
  completed: boolean?
}

agent TaskManager {
  tasks: Task[]
  max_tasks: integer (1..100)
  auto_archive: boolean
}
"""
        # Parse the DSL
        agent_def = self.compiler.parse_file_from_content(dsl_content)
        
        # Compile to JSON Schema
        schema = self.compiler.compile_to_json_schema(agent_def)
        
        # Verify the schema
        self.assertEqual(schema["title"], "TaskManager")
        self.assertIn("$defs", schema)
        self.assertIn("Priority", schema["$defs"])
        self.assertIn("Task", schema["$defs"])
        
        # Verify Task properties
        task_schema = schema["$defs"]["Task"]
        self.assertIn("priority", task_schema["properties"])
        self.assertEqual(task_schema["properties"]["priority"]["$ref"], "#/$defs/Priority")
    
    def test_compile_with_nested_types(self):
        """Test compiling with nested type references."""
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

agent AgentWithNestedTypes {
  person: Person
}
"""
        # Parse the DSL
        agent_def = self.compiler.parse_file_from_content(dsl_content)
        
        # Compile to JSON Schema
        schema = self.compiler.compile_to_json_schema(agent_def)
        
        # Verify nested type references
        self.assertIn("$defs", schema)
        self.assertIn("Address", schema["$defs"])
        self.assertIn("Person", schema["$defs"])
        
        # Verify Person references Address
        person_schema = schema["$defs"]["Person"]
        address_ref = person_schema["properties"]["address"]
        self.assertEqual(address_ref["$ref"], "#/$defs/Address")
    
    def test_compile_with_optional_fields(self):
        """Test compiling with optional fields."""
        dsl_content = """
agent AgentWithOptionalFields {
  required: string
  optional1?: string
  optional2?: integer
  optional3?: boolean
}
"""
        # Parse the DSL
        agent_def = self.compiler.parse_file_from_content(dsl_content)
        
        # Compile to JSON Schema
        schema = self.compiler.compile_to_json_schema(agent_def)
        
        # Verify required and optional fields
        self.assertIn("required", schema["required"])
        self.assertNotIn("optional1", schema["required"])
        self.assertNotIn("optional2", schema["required"])
        self.assertNotIn("optional3", schema["required"])
        
        # Verify optional fields are in properties
        self.assertIn("optional1", schema["properties"])
        self.assertIn("optional2", schema["properties"])
        self.assertIn("optional3", schema["properties"])
    
    def test_compile_with_mixed_types(self):
        """Test compiling with mixed type expressions."""
        dsl_content = """
agent AgentWithMixedTypes {
  simple: string
  array: string[]
  union: string | integer | boolean
  constrained: integer (0..100)
  optional_array?: string[]
  optional_union?: string | integer | null
}
"""
        # Parse the DSL
        agent_def = self.compiler.parse_file_from_content(dsl_content)
        
        # Compile to JSON Schema
        schema = self.compiler.compile_to_json_schema(agent_def)
        
        # Verify all properties are present
        properties = schema["properties"]
        self.assertIn("simple", properties)
        self.assertIn("array", properties)
        self.assertIn("union", properties)
        self.assertIn("constrained", properties)
        self.assertIn("optional_array", properties)
        self.assertIn("optional_union", properties)
        
        # Verify required fields
        required = schema["required"]
        self.assertIn("simple", required)
        self.assertIn("array", required)
        self.assertIn("union", required)
        self.assertIn("constrained", required)
        self.assertNotIn("optional_array", required)
        self.assertNotIn("optional_union", required)
    
    def test_compile_with_comments(self):
        """Test compiling with comments."""
        dsl_content = """
# This is a comment
agent CommentedAgent {
  # Field comment
  name: string
  # Another comment
  description?: string
}
"""
        # Parse the DSL
        agent_def = self.compiler.parse_file_from_content(dsl_content)
        
        # Compile to JSON Schema
        schema = self.compiler.compile_to_json_schema(agent_def)
        
        # Verify the schema is generated correctly
        self.assertEqual(schema["title"], "CommentedAgent")
        self.assertIn("name", schema["properties"])
        self.assertIn("description", schema["properties"])
        
        # Verify required fields
        self.assertIn("name", schema["required"])
        self.assertNotIn("description", schema["required"])
    
    def test_compile_empty_file(self):
        """Test compiling an empty file."""
        dsl_content = ""
        
        # Parse the DSL
        agent_def = self.compiler.parse_file_from_content(dsl_content)
        
        # Compile to JSON Schema
        schema = self.compiler.compile_to_json_schema(agent_def)
        
        # Verify the schema has basic structure
        self.assertIn("$schema", schema)
        self.assertIn("title", schema)
        self.assertIn("type", schema)
        self.assertIn("properties", schema)
        self.assertIn("required", schema)
        self.assertIn("additionalProperties", schema)
        
        # Verify properties and required are empty
        self.assertEqual(schema["properties"], {})
        self.assertEqual(schema["required"], [])
    
    def test_compile_with_whitespace(self):
        """Test compiling with various whitespace."""
        dsl_content = """


agent WhitespaceAgent {


  name: string


  description?: string


}


"""
        # Parse the DSL
        agent_def = self.compiler.parse_file_from_content(dsl_content)
        
        # Compile to JSON Schema
        schema = self.compiler.compile_to_json_schema(agent_def)
        
        # Verify the schema is generated correctly
        self.assertEqual(schema["title"], "WhitespaceAgent")
        self.assertIn("name", schema["properties"])
        self.assertIn("description", schema["properties"])
        
        # Verify required fields
        self.assertIn("name", schema["required"])
        self.assertNotIn("description", schema["required"])
    
    def test_compile_with_multiple_enums_and_types(self):
        """Test compiling with multiple enums and types."""
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
  email: string?
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
        # Parse the DSL
        agent_def = self.compiler.parse_file_from_content(dsl_content)
        
        # Compile to JSON Schema
        schema = self.compiler.compile_to_json_schema(agent_def)
        
        # Verify all definitions are present
        self.assertIn("Priority", schema["$defs"])
        self.assertIn("Status", schema["$defs"])
        self.assertIn("User", schema["$defs"])
        self.assertIn("Task", schema["$defs"])
        
        # Verify Task references Priority and Status
        task_schema = schema["$defs"]["Task"]
        priority_ref = task_schema["properties"]["priority"]
        status_ref = task_schema["properties"]["status"]
        
        self.assertEqual(priority_ref["$ref"], "#/$defs/Priority")
        self.assertEqual(status_ref["$ref"], "#/$defs/Status")


if __name__ == '__main__':
    unittest.main()