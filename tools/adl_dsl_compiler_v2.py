#!/usr/bin/env python3
"""
ADL DSL Compiler v2

Enhanced compiler with proper import resolution system.
Supports importing from both DSL and JSON component files.
"""

import re
import json
from pathlib import Path
from typing import Dict, List, Any, Optional, Union, Set
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


class ADLDSLCompilerV2:
    """Enhanced ADL DSL compiler with import resolution."""
    
    def __init__(self):
        self.types: Dict[str, TypeDefinition] = {}
        self.enums: Dict[str, List[str]] = {}
        self.imports: List[str] = []
        self.current_module: Optional[str] = None
        self.import_cache: Dict[str, Dict[str, Any]] = {}  # Cache for resolved imports
        self.resolving: Set[str] = set()  # Track currently resolving imports (for circular dependency detection)
        self.project_root: Optional[Path] = None
        
    def parse_file(self, file_path: str) -> Dict[str, Any]:
        """Parse DSL file and return AST."""
        file_path_obj = Path(file_path)
        self.project_root = file_path_obj.parent.parent  # Assume project root is 2 levels up
        
        with open(file_path, 'r') as f:
            content = f.read()
        
        content = re.sub(r'#.*$', '', content, flags=re.MULTILINE)
        
        self._parse_imports(content)
        self._resolve_imports(file_path_obj)
        self._parse_enums(content)
        self._parse_types(content)
        agent_def = self._parse_agent(content)
        
        return agent_def
    
    def _parse_imports(self, content: str):
        """Parse import statements."""
        import_pattern = r'import\s+(.+)'
        for match in re.finditer(import_pattern, content):
            import_path = match.group(1).strip()
            self.imports.append(import_path)
    
    def _resolve_imports(self, current_file: Path):
        """Resolve all imports and merge types/enums from imported modules."""
        for import_path in self.imports:
            if import_path in self.import_cache:
                self._merge_imported_types(self.import_cache[import_path])
                continue
            
            if import_path in self.resolving:
                raise ValueError(f"Circular dependency detected: {import_path}")
            
            self.resolving.add(import_path)
            
            try:
                imported_data = self._load_import(import_path, current_file)
                self.import_cache[import_path] = imported_data
                self._merge_imported_types(imported_data)
                
            finally:
                self.resolving.remove(import_path)
    
    def _load_import(self, import_path: str, current_file: Path) -> Dict[str, Any]:
        """Load an imported module (DSL or JSON)."""
        if import_path.startswith('./') or import_path.startswith('../'):
            resolved_path = (current_file.parent / import_path).resolve()
        else:
            resolved_path = (self.project_root / import_path).resolve()
        
        imported_data = {'types': {}, 'enums': {}}
        
        if resolved_path.is_dir():
            for index_file in ['index.adl', 'index.json']:
                index_path = resolved_path / index_file
                if index_path.exists():
                    if index_file == 'index.adl':
                        imported_data = self._load_dsl_import(index_path)
                    elif index_file == 'index.json':
                        imported_data = self._load_json_import(index_path)
                    break
            
            if imported_data['types'] or imported_data['enums']:
                return imported_data
            
            for json_file in resolved_path.glob('*.json'):
                file_imported_data = self._load_json_import(json_file)
                imported_data['types'].update(file_imported_data['types'])
                imported_data['enums'].update(file_imported_data['enums'])
            
            if imported_data['types'] or imported_data['enums']:
                return imported_data
        
        # Try different file extensions
        possible_extensions = ['.adl', '.json']
        
        for ext in possible_extensions:
            file_with_ext = resolved_path.with_suffix(ext)
            if file_with_ext.exists():
                if ext == '.adl':
                    imported_data = self._load_dsl_import(file_with_ext)
                elif ext == '.json':
                    imported_data = self._load_json_import(file_with_ext)
                break
        
        if not imported_data['types'] and not imported_data['enums']:
            raise ValueError(f"Could not resolve import: {import_path} (tried: {possible_extensions}, index.adl, index.json)")
        
        return imported_data
    
    def _load_dsl_import(self, file_path: Path) -> Dict[str, Any]:
        """Load types and enums from a DSL file."""
        with open(file_path, 'r') as f:
            content = f.read()
        
        content = re.sub(r'#.*$', '', content, flags=re.MULTILINE)
        
        imported_data = {'types': {}, 'enums': {}}
        
        enum_pattern = r'enum\s+(\w+)\s*\{([^}]+)\}'
        for match in re.finditer(enum_pattern, content, re.MULTILINE | re.DOTALL):
            enum_name = match.group(1)
            enum_values = [v.strip() for v in match.group(2).split('\n') if v.strip()]
            imported_data['enums'][enum_name] = enum_values
        
        simple_type_pattern = r'type\s+(\w+)\s*\{([^}]+)\}'
        for match in re.finditer(simple_type_pattern, content, re.MULTILINE | re.DOTALL):
            type_name = match.group(1)
            type_body = match.group(2)
            
            if ':' in type_body:
                imported_data['types'][type_name] = {
                    'base_type': 'object',
                    'properties': {},
                    'required': [],
                    'optional': []
                }
                
                lines = [line.strip() for line in type_body.split('\n') if line.strip()]
                for line in lines:
                    if ':' in line:
                        parts = line.split(':', 1)
                        field_name = parts[0].strip()
                        field_type = parts[1].strip()
                        
                        is_optional = field_name.endswith('?')
                        if is_optional:
                            field_name = field_name[:-1]
                            imported_data['types'][type_name]['optional'].append(field_name)
                        else:
                            imported_data['types'][type_name]['required'].append(field_name)
                        
                        imported_data['types'][type_name]['properties'][field_name] = field_type
        
        return imported_data
    
    def _load_json_import(self, file_path: Path) -> Dict[str, Any]:
        """Load types from a JSON component file."""
        with open(file_path, 'r') as f:
            json_data = json.load(f)
        
        imported_data = {'types': {}, 'enums': {}}
        
        type_name = file_path.stem
        
        if json_data.get('type') == 'object':
            imported_data['types'][type_name] = {
                'base_type': 'object',
                'properties': {},
                'required': json_data.get('required', []),
                'optional': []
            }
            
            properties = json_data.get('properties', {})
            for prop_name, prop_schema in properties.items():
                imported_data['types'][type_name]['properties'][prop_name] = prop_schema
                
                if prop_name not in json_data.get('required', []):
                    imported_data['types'][type_name]['optional'].append(prop_name)
        
        return imported_data
    
    def _merge_imported_types(self, imported_data: Dict[str, Any]):
        for enum_name, enum_values in imported_data.get('enums', {}).items():
            if enum_name not in self.enums:
                self.enums[enum_name] = enum_values
        
        for type_name, type_data in imported_data.get('types', {}).items():
            if type_name not in self.types:
                self.types[type_name] = TypeDefinition(
                    name=type_name,
                    base_type=type_data.get('base_type', 'object'),
                    properties=type_data.get('properties', {}),
                    required=type_data.get('required', []),
                    optional=type_data.get('optional', [])
                )
    
    def _parse_enums(self, content: str):
        """Parse enum definitions."""
        enum_pattern = r'enum\s+(\w+)\s*\{([^}]+)\}'
        for match in re.finditer(enum_pattern, content, re.MULTILINE | re.DOTALL):
            enum_name = match.group(1)
            enum_values = [v.strip() for v in match.group(2).split('\n') if v.strip()]
            self.enums[enum_name] = enum_values
    
    def _parse_types(self, content: str):
        simple_type_pattern = r'type\s+(\w+)\s*\{([^}]+)\}'
        for match in re.finditer(simple_type_pattern, content, re.MULTILINE | re.DOTALL):
            type_name = match.group(1)
            type_body = match.group(2)
            
            if ':' in type_body:
                self._parse_object_type(type_name, type_body)
            else:
                base_type = type_body.strip()
                if re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*$', base_type):
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
            if ':' in line:
                parts = line.split(':', 1)
                field_name = parts[0].strip()
                field_type = parts[1].strip()
                
                is_optional = field_name.endswith('?')
                if is_optional:
                    field_name = field_name[:-1]
                    optional.append(field_name)
                else:
                    required.append(field_name)
                
                properties[field_name] = self._parse_field_type(field_type)
        
        self.types[type_name] = TypeDefinition(
            name=type_name,
            base_type='object',
            properties=properties,
            required=required,
            optional=optional
        )
    
    def _parse_field_type(self, field_type: str) -> Dict[str, Any]:
        if field_type.endswith('[]'):
            item_type = field_type[:-2]
            return {
                'type': 'array',
                'items': {'_type_ref': item_type}
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
        
        constraint_match = re.match(r'(\w+)\s*\(\s*(\d+)\.\.(\d*)\s*\)', field_type)
        if constraint_match:
            base_type = constraint_match.group(1)
            min_val = int(constraint_match.group(2))
            schema = {'_type_ref': base_type, '_constraints': {'minimum': min_val}}
            if constraint_match.group(3):
                schema['_constraints']['maximum'] = int(constraint_match.group(3))
            return schema
        
        constraint_match = re.match(r'(\w+)\s*\(\s*(\d+)\.\.\s*\)', field_type)
        if constraint_match:
            base_type = constraint_match.group(1)
            min_val = int(constraint_match.group(2))
            return {'_type_ref': base_type, '_constraints': {'minimum': min_val}}
        
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
        if '_type_ref' not in type_ref:
            return type_ref
        
        type_name = type_ref['_type_ref']
        constraints = type_ref.get('_constraints', {})
        
        schema = self._get_type_schema(type_name, defs)
        schema.update(constraints)
        
        return schema
    
    def _get_type_schema(self, type_name: str, defs: Dict[str, Any]) -> Dict[str, Any]:
        if type_name in self.enums:
            return {
                'type': 'string',
                'enum': self.enums[type_name]
            }
        
        if type_name in self.types:
            if type_name not in defs:
                self._add_type_to_defs(type_name, defs)
            return {'$ref': f'#/$defs/{type_name}'}
        
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
        
        return {'type': 'string'}
    
    def _add_type_to_defs(self, type_name: str, defs: Dict[str, Any]):
        if type_name in defs:
            return
        
        type_def = self.types[type_name]
        
        if type_def.base_type == 'object':
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
            defs[type_name] = {'type': type_def.base_type}
    
    def _expand_schema_recursive(self, schema: Dict[str, Any], defs: Dict[str, Any]) -> Dict[str, Any]:
        if not isinstance(schema, dict):
            return schema
        
        if '_type_ref' in schema:
            expanded = self._expand_type_schema(schema, defs)
            return self._expand_schema_recursive(expanded, defs)
        
        result = {}
        for key, value in schema.items():
            if key == 'type' and value == 'array' and 'items' in schema:
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
        defs = {}
        
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
        
        if defs:
            schema["$defs"] = defs
        
        return schema
    
    def generate_typescript_types(self, schema: Dict[str, Any]) -> str:
        ts_types = []
        
        if "$defs" in schema:
            for def_name, def_schema in schema["$defs"].items():
                ts_type = self._generate_ts_type(def_name, def_schema)
                ts_types.append(ts_type)
        
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
        if "$ref" in schema:
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
        print("Usage: python adl_dsl_compiler_v2.py <dsl-file> [output-file]")
        sys.exit(1)
    
    dsl_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None
    
    compiler = ADLDSLCompilerV2()
    agent_def = compiler.parse_file(dsl_file)
    schema = compiler.compile_to_json_schema(agent_def)
    
    if output_file:
        with open(output_file, 'w') as f:
            json.dump(schema, f, indent=2)
        print(f"✅ Generated JSON Schema: {output_file}")
    else:
        print(json.dumps(schema, indent=2))
    
    ts_types = compiler.generate_typescript_types(schema)
    ts_file = output_file.replace('.json', '.d.ts') if output_file else 'types/agent-definition.d.ts'
    
    with open(ts_file, 'w') as f:
        f.write(ts_types)
    print(f"✅ Generated TypeScript types: {ts_file}")


if __name__ == '__main__':
    main()
