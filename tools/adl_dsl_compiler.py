#!/usr/bin/env python3
"""
ADL DSL Compiler

Compiles ADL DSL files to JSON Schema.
"""

import re
import json
from pathlib import Path
from typing import Dict, List, Any, Optional, Union
from dataclasses import dataclass, field


@dataclass
class TypeDefinition:
    name: str
    base_type: str
    properties: Dict[str, Any] = field(default_factory=dict)
    required: List[str] = field(default_factory=list)
    optional: List[str] = field(default_factory=list)
    enum_values: List[str] = field(default_factory=list)
    constraints: Dict[str, Any] = field(default_factory=dict)
    is_array: bool = False
    array_item_type: Optional[str] = None


class ADLDSLCompiler:
    """Compiles ADL DSL to JSON Schema."""
    
    def __init__(self):
        self.types: Dict[str, TypeDefinition] = {}
        self.enums: Dict[str, List[str]] = {}
        self.imports: List[str] = []
        self.current_module: Optional[str] = None
        
    def parse_file(self, file_path: str) -> Dict[str, Any]:
        """Parse DSL file and return AST."""
        with open(file_path, 'r') as f:
            content = f.read()
        
        # Remove comments
        content = re.sub(r'#.*$', '', content, flags=re.MULTILINE)
        
        # Parse imports
        self._parse_imports(content)
        
        # Parse enums
        self._parse_enums(content)
        
        # Parse type definitions
        self._parse_types(content)
        
        # Parse agent definition
        agent_def = self._parse_agent(content)
        
        return agent_def
    
    def _parse_imports(self, content: str):
        """Parse import statements."""
        import_pattern = r'import\s+(.+)'
        for match in re.finditer(import_pattern, content):
            import_path = match.group(1).strip()
            self.imports.append(import_path)
    
    def _parse_enums(self, content: str):
        """Parse enum definitions."""
        enum_pattern = r'enum\s+(\w+)\s*\{([^}]+)\}'
        for match in re.finditer(enum_pattern, content, re.MULTILINE | re.DOTALL):
            enum_name = match.group(1)
            enum_values = [v.strip() for v in match.group(2).split('\n') if v.strip()]
            self.enums[enum_name] = enum_values
    
    def _parse_types(self, content: str):
        """Parse type definitions."""
        # Simple type aliases
        simple_type_pattern = r'type\s+(\w+)\s*\{([^}]+)\}'
        for match in re.finditer(simple_type_pattern, content, re.MULTILINE | re.DOTALL):
            type_name = match.group(1)
            type_body = match.group(2)
            
            # Check if it's an object type
            if ':' in type_body:
                self._parse_object_type(type_name, type_body)
            else:
                # Simple type alias - could be enum-like or primitive
                base_type = type_body.strip()
                # Check if it's an enum-like type (single word without special chars)
                if re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*$', base_type):
                    # This might be an inline enum - check if we have values defined elsewhere
                    self.types[type_name] = TypeDefinition(
                        name=type_name,
                        base_type=base_type
                    )
    
    def _parse_object_type(self, type_name: str, type_body: str):
        """Parse object type definition."""
        properties = {}
        required = []
        optional = []
        
        lines = [line.strip() for line in type_body.split('\n') if line.strip()]
        
        for line in lines:
            # Parse field: name: type
            if ':' in line:
                parts = line.split(':', 1)
                field_name = parts[0].strip()
                field_type = parts[1].strip()
                
                # Check if optional
                is_optional = field_name.endswith('?')
                if is_optional:
                    field_name = field_name[:-1]
                    optional.append(field_name)
                else:
                    required.append(field_name)
                
                # Parse the field type and store it for later expansion
                properties[field_name] = self._parse_field_type(field_type)
        
        self.types[type_name] = TypeDefinition(
            name=type_name,
            base_type='object',
            properties=properties,
            required=required,
            optional=optional
        )
    
    def _parse_field_type(self, field_type: str) -> Dict[str, Any]:
        """Parse a field type and return its schema representation."""
        # Check if it's an array type
        if field_type.endswith('[]'):
            item_type = field_type[:-2]
            return {
                'type': 'array',
                'items': {'_type_ref': item_type}  # Mark for later expansion
            }
        
        if '|' in field_type:
            union_types = [t.strip() for t in field_type.split('|')]
            if 'null' in union_types:
                non_null_types = [t for t in union_types if t != 'null']
                if len(non_null_types) == 1:
                    return {
                        'type': ['string', 'null'] if non_null_types[0] == 'string' else 
                               ['object', 'null'] if non_null_types[0] == 'object' else
                               ['array', 'null'] if non_null_types[0] == 'array' else
                               ['string', 'null']
                    }
            if 'object' in union_types and 'string' in union_types and len(union_types) == 2:
                return {
                    'oneOf': [
                        {'type': 'object'},
                        {'type': 'string'}
                    ]
                }
            primitive_types = ['string', 'number', 'boolean', 'object', 'array', 'integer']
            json_schema_types = []
            for t in union_types:
                if t in primitive_types:
                    json_schema_types.append(t)
                elif t == 'null':
                    json_schema_types.append('null')
                elif t == 'any':
                    return {}
            if json_schema_types:
                if len(json_schema_types) == 1:
                    return {'type': json_schema_types[0]}
                return {'type': json_schema_types}
            return {'type': 'string'}
        
        # Check for inline constraints like integer (1..10)
        constraint_match = re.match(r'(\w+)\s*\(\s*(\d+)\.\.(\d*)\s*\)', field_type)
        if constraint_match:
            base_type = constraint_match.group(1)
            min_val = int(constraint_match.group(2))
            schema = {'_type_ref': base_type, '_constraints': {'minimum': min_val}}
            if constraint_match.group(3):
                schema['_constraints']['maximum'] = int(constraint_match.group(3))
            return schema
        
        # Check for open-ended constraints like integer (1..)
        constraint_match = re.match(r'(\w+)\s*\(\s*(\d+)\.\.\s*\)', field_type)
        if constraint_match:
            base_type = constraint_match.group(1)
            min_val = int(constraint_match.group(2))
            return {'_type_ref': base_type, '_constraints': {'minimum': min_val}}
        
        # Store as type reference for later expansion
        return {'_type_ref': field_type}
    
    def _parse_agent(self, content: str) -> Dict[str, Any]:
        """Parse agent definition."""
        agent_pattern = r'agent\s+(\w+)\s*\{([^}]+)\}'
        match = re.search(agent_pattern, content, re.MULTILINE | re.DOTALL)
        
        if not match:
            raise ValueError("No agent definition found")
        
        agent_name = match.group(1)
        agent_body = match.group(2)
        
        properties = {}
        required = []
        
        lines = [line.strip() for line in agent_body.split('\n') if line.strip()]
        
        for line in lines:
            if ':' in line:
                parts = line.split(':', 1)
                field_name = parts[0].strip()
                field_type = parts[1].strip()
                
                # Check if optional
                is_optional = field_name.endswith('?')
                if is_optional:
                    field_name = field_name[:-1]
                else:
                    required.append(field_name)
                
                properties[field_name] = self._parse_field_type(field_type)
        
        return {
            'name': agent_name,
            'properties': properties,
            'required': required
        }
    
    def _expand_type_schema(self, type_ref: Dict[str, Any], defs: Dict[str, Any]) -> Dict[str, Any]:
        """Expand a type reference to its full JSON Schema."""
        if '_type_ref' not in type_ref:
            return type_ref
        
        type_name = type_ref['_type_ref']
        constraints = type_ref.get('_constraints', {})
        
        schema = self._get_type_schema(type_name, defs)
        
        # Apply constraints
        schema.update(constraints)
        
        return schema
    
    def _get_type_schema(self, type_name: str, defs: Dict[str, Any]) -> Dict[str, Any]:
        """Get JSON Schema for a type."""
        # Check if it's an enum
        if type_name in self.enums:
            return {
                'type': 'string',
                'enum': self.enums[type_name]
            }
        
        # Check if it's a defined type - use $ref
        if type_name in self.types:
            # Add to defs if not already there
            if type_name not in defs:
                self._add_type_to_defs(type_name, defs)
            return {'$ref': f'#/$defs/{type_name}'}
        
        # Primitive types
        primitive_types = {
            'string': {'type': 'string'},
            'integer': {'type': 'integer'},
            'number': {'type': 'number'},
            'boolean': {'type': 'boolean'},
            'object': {'type': 'object', 'additionalProperties': True},
            'array': {'type': 'array'},
            'any': {}
        }
        
        if type_name in primitive_types:
            return primitive_types[type_name]
        
        # Default to string for unknown types
        return {'type': 'string'}
    
    def _add_type_to_defs(self, type_name: str, defs: Dict[str, Any]):
        """Add a type definition to $defs, expanding all nested types."""
        if type_name in defs:
            return
        
        type_def = self.types[type_name]
        
        if type_def.base_type == 'object':
            # Expand all properties
            expanded_properties = {}
            for prop_name, prop_schema in type_def.properties.items():
                expanded_properties[prop_name] = self._expand_schema_recursive(prop_schema, defs)
            
            defs[type_name] = {
                'type': 'object',
                'properties': expanded_properties,
                'required': type_def.required,
                'additionalProperties': False
            }
        else:
            # Simple type alias
            defs[type_name] = {'type': type_def.base_type}
    
    def _expand_schema_recursive(self, schema: Dict[str, Any], defs: Dict[str, Any]) -> Dict[str, Any]:
        """Recursively expand a schema, resolving all type references."""
        if not isinstance(schema, dict):
            return schema
        
        # If it's a type reference, expand it
        if '_type_ref' in schema:
            expanded = self._expand_type_schema(schema, defs)
            # Recursively expand any nested references
            return self._expand_schema_recursive(expanded, defs)
        
        result = {}
        for key, value in schema.items():
            if key == 'type' and value == 'array' and 'items' in schema:
                # Expand array items
                result[key] = value
                result['items'] = self._expand_schema_recursive(schema['items'], defs)
            elif isinstance(value, dict):
                result[key] = self._expand_schema_recursive(value, defs)
            elif isinstance(value, list):
                result[key] = [self._expand_schema_recursive(item, defs) if isinstance(item, dict) else item for item in value]
            else:
                result[key] = value
        
        return result
    
    def compile_to_json_schema(self, agent_def: Dict[str, Any]) -> Dict[str, Any]:
        """Compile agent definition to JSON Schema."""
        defs = {}
        
        # Expand agent properties
        expanded_properties = {}
        for prop_name, prop_schema in agent_def['properties'].items():
            expanded_properties[prop_name] = self._expand_schema_recursive(prop_schema, defs)
        
        schema = {
            "$schema": "https://json-schema.org/draft/2020-12/schema",
            "$id": "https://example.com/schemas/agent-definition.json",
            "title": agent_def['name'],
            "type": "object",
            "properties": expanded_properties,
            "required": agent_def['required'],
            "additionalProperties": False
        }
        
        # Add all definitions
        if defs:
            schema["$defs"] = defs
        
        return schema
    
    def generate_typescript_types(self, schema: Dict[str, Any]) -> str:
        """Generate TypeScript type definitions from schema."""
        ts_types = []
        
        # Generate type for each definition
        if "$defs" in schema:
            for def_name, def_schema in schema["$defs"].items():
                ts_type = self._generate_ts_type(def_name, def_schema)
                ts_types.append(ts_type)
        
        # Generate main agent type
        agent_type = self._generate_ts_type("AgentDefinition", schema)
        ts_types.append(agent_type)
        
        return "\n\n".join(ts_types)
    
    def _generate_ts_type(self, name: str, schema: Dict[str, Any]) -> str:
        """Generate TypeScript type definition."""
        if schema.get("type") == "object":
            properties = []
            if "properties" in schema:
                for prop_name, prop_schema in schema["properties"].items():
                    is_required = prop_name in schema.get("required", [])
                    prop_type = self._schema_to_ts_type(prop_schema)
                    optional = "" if is_required else "?"
                    properties.append(f"  {prop_name}{optional}: {prop_type}")
            
            return f"export interface {name} {{\n" + "\n".join(properties) + "\n}"
        
        elif schema.get("type") == "array":
            item_type = self._schema_to_ts_type(schema.get("items", {}))
            return f"export type {name} = {item_type}[]"
        
        elif "enum" in schema:
            enum_values = schema["enum"]
            return f"export type {name} = {' | '.join(f'\"{v}\"' for v in enum_values)}"
        
        else:
            ts_type = self._schema_to_ts_type(schema)
            return f"export type {name} = {ts_type}"
    
    def _schema_to_ts_type(self, schema: Dict[str, Any]) -> str:
        """Convert JSON Schema type to TypeScript type."""
        if "$ref" in schema:
            # Extract type name from $ref
            ref = schema["$ref"]
            if "/" in ref:
                return ref.split("/")[-1]
            return ref
        
        if "enum" in schema:
            return " | ".join(f'"{v}"' for v in schema["enum"])
        
        elif schema.get("type") == "string":
            return "string"
        
        elif schema.get("type") == "integer":
            return "number"
        
        elif schema.get("type") == "number":
            return "number"
        
        elif schema.get("type") == "boolean":
            return "boolean"
        
        elif schema.get("type") == "array":
            item_type = self._schema_to_ts_type(schema.get("items", {}))
            return f"{item_type}[]"
        
        elif schema.get("type") == "object":
            if "properties" in schema:
                props = []
                for prop_name, prop_schema in schema["properties"].items():
                    is_required = prop_name in schema.get("required", [])
                    prop_type = self._schema_to_ts_type(prop_schema)
                    optional = "" if is_required else "?"
                    props.append(f"{prop_name}{optional}: {prop_type}")
                return "{" + ", ".join(props) + "}"
            return "Record<string, unknown>"
        
        elif isinstance(schema.get("type"), list):
            return " | ".join(self._schema_to_ts_type({"type": t}) for t in schema["type"])
        
        return "unknown"


def main():
    """Main entry point."""
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python adl_dsl_compiler.py <dsl-file> [output-file]")
        sys.exit(1)
    
    dsl_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None
    
    # Compile DSL
    compiler = ADLDSLCompiler()
    agent_def = compiler.parse_file(dsl_file)
    schema = compiler.compile_to_json_schema(agent_def)
    
    # Output JSON Schema
    if output_file:
        with open(output_file, 'w') as f:
            json.dump(schema, f, indent=2)
        print(f"✅ Generated JSON Schema: {output_file}")
    else:
        print(json.dumps(schema, indent=2))
    
    # Generate TypeScript types
    ts_types = compiler.generate_typescript_types(schema)
    ts_file = output_file.replace('.json', '.d.ts') if output_file else 'types/agent-definition.d.ts'
    
    with open(ts_file, 'w') as f:
        f.write(ts_types)
    print(f"✅ Generated TypeScript types: {ts_file}")


if __name__ == '__main__':
    main()
