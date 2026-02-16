#!/usr/bin/env python3
"""Test script to debug transformer issues with various import patterns"""

import sys
sys.path.insert(0, '.')

from lark import Lark
from tools.dsl.transformer import ADLTransformer

# Load grammar
with open('tools/dsl/grammar.lark', 'r') as f:
    grammar = f.read()

# Create parser without transformer first
parser = Lark(grammar, parser='lalr', start='start')

test_cases = [
    'import schema/components/rag',
    'import schema.components.rag',
    'import schema/components/tool as tools',
    'import .utils',
    'import ..config',
    'import schema.components.tool as t',
]

for test_code in test_cases:
    print(f"\n{'='*60}")
    print(f"Testing: {test_code}")
    print('='*60)
    
    try:
        # Parse first to see the tree
        tree = parser.parse(test_code)
        print("\nParse tree:")
        print(tree.pretty())
        
        # Now transform
        transformer = ADLTransformer()
        result = transformer.transform(tree)
        print(f"\nTransformed result path: {result.imports[0].path}")
        if result.imports[0].alias:
            print(f"Alias: {result.imports[0].alias}")
            
    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()