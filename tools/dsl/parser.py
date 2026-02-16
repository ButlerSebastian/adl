"""
ADL DSL Parser Module

This module provides a grammar-based parser for the ADL DSL using Lark.
It converts ADL source code into an AST representation.
"""

import os
from pathlib import Path
from typing import Optional, Union, List, Dict, Any
from lark import Lark, UnexpectedInput
from lark.exceptions import UnexpectedCharacters, UnexpectedToken, ParseError as LarkParseError

from .ast import Program
from .transformer import ADLTransformer
from .validator import SemanticValidator, ValidationError
from .json_schema_generator import JSONSchemaGenerator
from .typescript_generator import TypeScriptGenerator
from .python_generator import PythonGenerator


class GrammarParser:
    """
    Grammar-based parser for ADL DSL.

    Uses Lark LALR(1) parser with the ADL grammar specification.
    """

    def __init__(self, grammar_path: Optional[str] = None):
        """
        Initialize the parser.

        Args:
            grammar_path: Optional path to the grammar file. If not provided,
                         uses the default grammar.lark in the same directory.
        """
        if grammar_path is None:
            # Use the grammar file in the same directory
            grammar_path = str(Path(__file__).parent / "grammar.lark")

        self.grammar_path = grammar_path
        self._parser: Optional[Lark] = None
        
    @property
    def parser(self) -> Lark:
        """Lazy initialization of the Lark parser."""
        if self._parser is None:
            with open(self.grammar_path, 'r') as f:
                grammar = f.read()
            
            self._parser = Lark(
                grammar,
                parser='lalr',
                start='start',
                maybe_placeholders=False,
                propagate_positions=True
            )
        
        return self._parser
    
    def parse(self, content: str, file_path: Optional[str] = None) -> Program:
        """
        Parse ADL content into an AST.
        
        Args:
            content: ADL source code as a string
            file_path: Optional path to the source file for error reporting
            
        Returns:
            Program: Root AST node representing the entire ADL file
            
        Raises:
            ParseError: If the content cannot be parsed
        """
        try:
            # Parse the content
            parse_tree = self.parser.parse(content)
            
            # Transform the parse tree into AST
            transformer = ADLTransformer(file_path)
            ast = transformer.transform(parse_tree)
            
            return ast
            
        except UnexpectedCharacters as e:
            # Handle unexpected characters
            raise ParseError(
                f"Unexpected character '{e.char}' at line {e.line}, column {e.column}",
                line=e.line,
                column=e.column
            )

        except UnexpectedToken as e:
            # Handle unexpected tokens
            raise ParseError(
                f"Unexpected token '{e.token}' at line {e.line}, column {e.column}",
                line=e.line,
                column=e.column
            )

        except UnexpectedInput as e:
            # Handle other unexpected input
            raise ParseError(
                f"Parse error at line {e.line}, column {e.column}: {e}",
                line=e.line,
                column=e.column
            )

        except LarkParseError as e:
            # Handle Lark parse errors
            raise ParseError(
                f"Parse error: {e}",
                line=getattr(e, 'line', None),
                column=getattr(e, 'column', None)
            )
    
    def parse_file(self, file_path: str) -> Program:
        """
        Parse an ADL file.
        
        Args:
            file_path: Path to the ADL file
            
        Returns:
            Program: Root AST node representing the entire ADL file
            
        Raises:
            ParseError: If the file cannot be parsed
            FileNotFoundError: If the file does not exist
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        
        with open(file_path, 'r') as f:
            content = f.read()
        
        return self.parse(content, file_path)

    def validate(self, program: Program) -> List[ValidationError]:
        """
        Validate a parsed ADL program for semantic correctness.

        Args:
            program: The AST program to validate

        Returns:
            List of validation errors (empty if valid)
        """
        validator = SemanticValidator()
        return validator.validate(program)

    def generate_json_schema(self, program: Program) -> Dict[str, Any]:
        """
        Generate JSON Schema from a parsed ADL program.

        Args:
            program: The AST program to convert

        Returns:
            JSON Schema as a dictionary
        """
        generator = JSONSchemaGenerator()
        return generator.generate(program)

    def generate_typescript(self, program: Program) -> str:
        """
        Generate TypeScript type definitions from a parsed ADL program.

        Args:
            program: The AST program to convert

        Returns:
            TypeScript code as a string
        """
        generator = TypeScriptGenerator()
        return generator.generate(program)

    def generate_python(self, program: Program) -> str:
        """
        Generate Python type definitions from a parsed ADL program.

        Args:
            program: The AST program to convert

        Returns:
            Python code as a string
        """
        generator = PythonGenerator()
        return generator.generate(program)


class ParseError(Exception):
    """Custom exception for parse errors."""
    
    def __init__(self, message: str, line: Optional[int] = None, column: Optional[int] = None):
        super().__init__(message)
        self.line = line
        self.column = column


def parse_adl(content: str, file_path: Optional[str] = None) -> Program:
    """
    Convenience function to parse ADL content.

    Args:
        content: ADL source code as a string
        file_path: Optional path to the source file for error reporting

    Returns:
        Program: Root AST node representing the entire ADL file
    """
    parser = GrammarParser()
    return parser.parse(content, file_path)


def parse_adl_file(file_path: str) -> Program:
    """
    Convenience function to parse an ADL file.

    Args:
        file_path: Path to the ADL file

    Returns:
        Program: Root AST node representing the entire ADL file
    """
    parser = GrammarParser()
    return parser.parse_file(file_path)