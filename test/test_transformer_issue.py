#!/usr/bin/env python3
"""Test script to debug transformer issues"""

import sys
sys.path.insert(0, '.')

from lark import Lark
from tools.dsl.transformer import ADLTransformer

# Load grammar
with open('tools/dsl/grammar.lark', 'r') as f:
    grammar = f.read()

# Create parser without transformer first
parser = Lark(grammar, parser='lalr', start='start')

# Test simple import
test_code = 'import schema/components/rag'
print(f"Testing: {test_code}")

try:
    # Parse to see the tree structure
    tree = parser.parse(test_code)
    print("\nParse tree structure:")
    print(tree.pretty())
    
    # Now transform
    transformer = ADLTransformer()
    result = transformer.transform(tree)
    print("\nTransformed result:")
    print(result)
    
except Exception as e:
    print(f"\nError: {e}")
    import traceback
    traceback.print_exc()