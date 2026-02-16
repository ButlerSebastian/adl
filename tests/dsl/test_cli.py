#!/usr/bin/env python3
"""
Integration tests for ADL CLI commands.

Tests all CLI commands: compile, validate, format, lint, generate.
"""

import unittest
import subprocess
import tempfile
import json
import os
from pathlib import Path


class TestCLICompile(unittest.TestCase):
    """Test adl-compile command."""

    def setUp(self):
        """Set up test fixtures."""
        self.test_dir = Path(__file__).parent.parent / "fixtures" / "cli"
        self.test_dir.mkdir(parents=True, exist_ok=True)

    def test_compile_to_json(self):
        """Test compiling ADL file to JSON."""
        adl_content = """
agent TestAgent {
  name: "test_agent"
  description: "Test agent"
  role: "Tester"
  llm: "openai"
  llm_settings: {
    temperature: 0.7
    max_tokens: 1000
  }
  tools: []
  rag: []
}
"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.adl', delete=False) as f:
            f.write(adl_content)
            adl_file = f.name

        try:
            result = subprocess.run(
                ['python', '-m', 'tools.dsl.cli', 'compile', adl_file],
                capture_output=True,
                text=True
            )
            self.assertEqual(result.returncode, 0)
            output = json.loads(result.stdout)
            self.assertEqual(output['name'], 'test_agent')
        finally:
            os.unlink(adl_file)

    def test_compile_to_yaml(self):
        """Test compiling ADL file to YAML."""
        adl_content = """
agent TestAgent {
  name: "test_agent"
  description: "Test agent"
  role: "Tester"
  llm: "openai"
  llm_settings: {
    temperature: 0.7
    max_tokens: 1000
  }
  tools: []
  rag: []
}
"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.adl', delete=False) as f:
            f.write(adl_content)
            adl_file = f.name

        try:
            result = subprocess.run(
                ['python', '-m', 'tools.dsl.cli', 'compile', adl_file, '-f', 'yaml'],
                capture_output=True,
                text=True
            )
            self.assertEqual(result.returncode, 0)
            self.assertIn('name: test_agent', result.stdout)
        finally:
            os.unlink(adl_file)

    def test_compile_to_python(self):
        """Test compiling ADL file to Python."""
        adl_content = """
agent TestAgent {
  name: "test_agent"
  description: "Test agent"
  role: "Tester"
  llm: "openai"
  llm_settings: {
    temperature: 0.7
    max_tokens: 1000
  }
  tools: []
  rag: []
}
"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.adl', delete=False) as f:
            f.write(adl_content)
            adl_file = f.name

        try:
            result = subprocess.run(
                ['python', '-m', 'tools.dsl.cli', 'compile', adl_file, '-f', 'python'],
                capture_output=True,
                text=True
            )
            self.assertEqual(result.returncode, 0)
            self.assertIn('class TestAgent', result.stdout)
        finally:
            os.unlink(adl_file)

    def test_compile_to_typescript(self):
        """Test compiling ADL file to TypeScript."""
        adl_content = """
agent TestAgent {
  name: "test_agent"
  description: "Test agent"
  role: "Tester"
  llm: "openai"
  llm_settings: {
    temperature: 0.7
    max_tokens: 1000
  }
  tools: []
  rag: []
}
"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.adl', delete=False) as f:
            f.write(adl_content)
            adl_file = f.name

        try:
            result = subprocess.run(
                ['python', '-m', 'tools.dsl.cli', 'compile', adl_file, '-f', 'typescript'],
                capture_output=True,
                text=True
            )
            self.assertEqual(result.returncode, 0)
            self.assertIn('interface TestAgent', result.stdout)
        finally:
            os.unlink(adl_file)

    def test_compile_with_output_file(self):
        """Test compiling ADL file to output file."""
        adl_content = """
agent TestAgent {
  name: "test_agent"
  description: "Test agent"
  role: "Tester"
  llm: "openai"
  llm_settings: {
    temperature: 0.7
    max_tokens: 1000
  }
  tools: []
  rag: []
}
"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.adl', delete=False) as f:
            f.write(adl_content)
            adl_file = f.name

        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            output_file = f.name

        try:
            result = subprocess.run(
                ['python', '-m', 'tools.dsl.cli', 'compile', adl_file, '-o', output_file],
                capture_output=True,
                text=True
            )
            self.assertEqual(result.returncode, 0)
            self.assertTrue(os.path.exists(output_file))
            with open(output_file, 'r') as f:
                output = json.load(f)
            self.assertEqual(output['name'], 'test_agent')
        finally:
            os.unlink(adl_file)
            if os.path.exists(output_file):
                os.unlink(output_file)

    def test_compile_invalid_file(self):
        """Test compiling invalid ADL file."""
        adl_content = """
agent TestAgent {
  name: "test_agent"
  description: "Test agent"
  role: "Tester"
  llm: "openai"
  llm_settings: {
    temperature: 0.7
    max_tokens: 1000
  }
  tools: []
  rag: []
"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.adl', delete=False) as f:
            f.write(adl_content)
            adl_file = f.name

        try:
            result = subprocess.run(
                ['python', '-m', 'tools.dsl.cli', 'compile', adl_file],
                capture_output=True,
                text=True
            )
            self.assertNotEqual(result.returncode, 0)
        finally:
            os.unlink(adl_file)


if __name__ == '__main__':
    unittest.main()
