#!/usr/bin/env python3
"""Debug script to see what's being generated."""

from tools.dsl.parser import GrammarParser
from tools.dsl.python_generator import PythonGenerator

parser = GrammarParser()
with open('test_phase4.adl', 'r') as f:
    content = f.read()
program = parser.parse(content)

generator = PythonGenerator()

try:
    generator.generate(program)
except ValueError as e:
    print('Lines in generator:')
    for i, line in enumerate(generator.lines):
        print(f'{i}: {repr(line)}')

    print('\nJoined code:')
    code = "\n".join(generator.lines).strip()
    print(repr(code))
    print('\nError:', e)