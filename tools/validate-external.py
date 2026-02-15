#!/usr/bin/env python3
"""
Validate ADL agent definitions against the schema with external $ref support.
"""
import json
import sys
from pathlib import Path
from urllib.parse import urljoin
import jsonschema

def load_schema_with_refs(schema_path):
    """Load schema and resolve all $ref references."""
    schema_path = Path(schema_path).resolve()
    base_uri = schema_path.as_uri()

    with open(schema_path, 'r') as f:
        schema = json.load(f)

    # Create a custom resolver
    class LocalResolver(jsonschema.RefResolver):
        def resolve_remote(self, uri):
            # Handle meta-schema reference
            if uri == 'https://json-schema.org/draft/2020-12/schema':
                return {
                    "$schema": "https://json-schema.org/draft/2020-12/schema",
                    "$id": "https://json-schema.org/draft/2020-12/schema",
                    "$vocabulary": {
                        "https://json-schema.org/draft/2020-12/vocab/core": True,
                        "https://json-schema.org/draft/2020-12/vocab/applicator": True,
                        "https://json-schema.org/draft/2020-12/vocab/unevaluated": True,
                        "https://json-schema.org/draft/2020-12/vocab/validation": True,
                        "https://json-schema.org/draft/2020-12/vocab/meta-data": True,
                        "https://json-schema.org/draft/2020-12/vocab/format-annotation": True,
                        "https://json-schema.org/draft/2020-12/vocab/content": True
                    },
                    "$dynamicAnchor": "meta"
                }
            # Handle local file references
            elif uri.startswith('file://'):
                file_path = Path(uri.replace('file://', ''))
                if file_path.exists():
                    with open(file_path, 'r') as f:
                        return json.load(f)
            # Handle relative references
            elif not uri.startswith(('http://', 'https://')):
                # Try to resolve relative to base URI
                resolved = urljoin(base_uri, uri)
                file_path = Path(resolved.replace('file://', ''))
                if file_path.exists():
                    with open(file_path, 'r') as f:
                        return json.load(f)
            # Fall back to default behavior
            return super().resolve_remote(uri)

    return schema, LocalResolver.from_schema(schema)

def main(agent_path):
    """Validate an agent definition against the schema."""
    schema_path = Path(__file__).parent.parent / 'schema' / 'agent-definition.schema.json'
    agent_path = Path(agent_path).resolve()

    if not schema_path.exists():
        print(f"❌ Schema not found: {schema_path}")
        sys.exit(1)

    if not agent_path.exists():
        print(f"❌ Agent file not found: {agent_path}")
        sys.exit(1)

    # Load schema with external $ref support
    schema, resolver = load_schema_with_refs(schema_path)

    # Load agent definition
    with open(agent_path, 'r') as f:
        agent = json.load(f)

    # Validate
    validator = jsonschema.Draft202012Validator(schema, resolver=resolver)
    errors = sorted(validator.iter_errors(agent), key=lambda e: e.path)

    if errors:
        print(f"❌ {agent_path} is NOT valid:")
        for error in errors:
            print(f"  - {error.path[0] if error.path else 'root'}: {error.message}")
        sys.exit(1)
    else:
        print(f"✅ {agent_path} is valid against agent-definition.schema.json")

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python tools/validate-external.py <path-to-agent-json>")
        sys.exit(1)
    main(sys.argv[1])
