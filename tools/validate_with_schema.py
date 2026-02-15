#!/usr/bin/env python3
import json
import sys
from pathlib import Path

from jsonschema import Draft202012Validator

def main(schema_path: str, instance_path: str) -> None:
    schema = json.loads(Path(schema_path).read_text())
    instance = json.loads(Path(instance_path).read_text())

    validator = Draft202012Validator(schema)
    errors = sorted(validator.iter_errors(instance), key=lambda e: e.path)

    if errors:
        print(f"❌ {instance_path} is NOT valid:")
        for err in errors:
            loc = ".".join(str(x) for x in err.path) or "<root>"
            print(f"  - {loc}: {err.message}")
        sys.exit(1)
    else:
        print(f"✅ {instance_path} is valid against {schema_path}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python validate_with_schema.py <schema-path> <instance-path>")
        sys.exit(1)
    main(sys.argv[1], sys.argv[2])
