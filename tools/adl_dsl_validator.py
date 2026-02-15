#!/usr/bin/env python3
"""
ADL DSL Validator

Validates ADL agent definitions against DSL-generated schema.
"""

import json
import sys
from pathlib import Path
from typing import Dict, List, Any

# Import jsonschema for validation
try:
    import jsonschema
    from jsonschema import validate, Draft202012Validator
except ImportError:
    print("Error: jsonschema not installed. Run: pip install jsonschema")
    sys.exit(1)


class ADLDSLValidator:
    """Validates ADL agent definitions against DSL-generated schema."""
    
    def __init__(self, schema_path: str):
        self.schema_path = Path(schema_path)
        self.schema = self._load_schema()
        self.validator = Draft202012Validator(self.schema)
    
    def _load_schema(self) -> Dict[str, Any]:
        """Load schema from file."""
        with open(self.schema_path, 'r') as f:
            return json.load(f)
    
    def validate_file(self, agent_path: str) -> bool:
        """Validate a single agent file."""
        agent_path = Path(agent_path)
        
        if not agent_path.exists():
            print(f"❌ File not found: {agent_path}")
            return False
        
        with open(agent_path, 'r') as f:
            agent = json.load(f)
        
        try:
            validate(instance=agent, schema=self.schema, cls=Draft202012Validator)
            print(f"✅ {agent_path} is valid against {self.schema_path.name}")
            return True
        except jsonschema.ValidationError as e:
            print(f"❌ {agent_path} is NOT valid:")
            print(f"   Path: {'.'.join(str(p) for p in e.path)}")
            print(f"   Message: {e.message}")
            return False
        except jsonschema.SchemaError as e:
            print(f"❌ Schema error: {e.message}")
            return False
        except Exception as e:
            print(f"❌ Validation error: {e}")
            return False
    
    def validate_directory(self, directory: str) -> Dict[str, bool]:
        """Validate all JSON files in a directory."""
        dir_path = Path(directory)
        
        if not dir_path.exists():
            print(f"❌ Directory not found: {directory}")
            return {}
        
        json_files = list(dir_path.glob("*.json"))
        
        if not json_files:
            print(f"❌ No JSON files found in {directory}")
            return {}
        
        results = {}
        all_valid = True
        
        print(f"Validating {len(json_files)} files from {directory}...\n")
        
        for json_file in sorted(json_files):
            result = self.validate_file(str(json_file))
            results[json_file.name] = result
            if not result:
                all_valid = False
        
        print(f"\n{'='*60}")
        if all_valid:
            print(f"✅ All {len(json_files)} files are valid!")
        else:
            invalid_count = sum(1 for r in results.values() if not r)
            print(f"❌ {invalid_count}/{len(json_files)} files are invalid")
        
        return results
    
    def validate_schema(self) -> bool:
        """Validate the schema itself against meta-schema."""
        try:
            Draft202012Validator.check_schema(self.schema)
            print(f"✅ {self.schema_path.name} is valid JSON Schema Draft 2020-12")
            return True
        except jsonschema.SchemaError as e:
            print(f"❌ Schema validation failed: {e.message}")
            return False


def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        print("Usage: python tools/adl_dsl_validator.py <schema-file> [agent-file-or-directory]")
        print("\nExamples:")
        print("  python tools/adl_dsl_validator.py schema/agent-definition.schema.json examples/multi_agent_team.json")
        print("  python tools/adl_dsl_validator.py schema/agent-definition.schema.json examples/")
        sys.exit(1)
    
    schema_file = sys.argv[1]
    target = sys.argv[2] if len(sys.argv) > 2 else None
    
    # Initialize validator
    validator = ADLDSLValidator(schema_file)
    
    # Validate schema first
    if not validator.validate_schema():
        sys.exit(1)
    
    print()
    
    # Validate target
    if target:
        target_path = Path(target)
        if target_path.is_file():
            validator.validate_file(target)
        elif target_path.is_dir():
            validator.validate_directory(target)
        else:
            print(f"❌ Target not found: {target}")
            sys.exit(1)
    else:
        print("No target specified. Validating schema only.")


if __name__ == '__main__':
    main()
