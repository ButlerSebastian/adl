#!/usr/bin/env python3
import json
import os

def test_schema():
    # Load the main schema
    schema_path = 'schema/agent-definition.schema.json'
    with open(schema_path, 'r') as f:
        schema = json.load(f)
    
    print("Schema loaded successfully")
    print(f"Schema has {len(schema.get('properties', {}))} properties")
    
    # Check if the schema has $defs
    if '$defs' in schema:
        print(f"Schema has {len(schema['$defs'])} definitions in $defs")
        
        # List the definitions
        for def_name in schema['$defs']:
            print(f"  - {def_name}")
    
    # Test with a simple example
    example_path = 'examples/minimal_agent.json'
    if os.path.exists(example_path):
        with open(example_path, 'r') as f:
            example = json.load(f)
        
        print(f"\nExample loaded successfully: {example.get('name')}")
    
    return True

if __name__ == '__main__':
    test_schema()