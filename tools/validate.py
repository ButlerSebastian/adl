#!/usr/bin/env python3
import json
import sys
from pathlib import Path

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "schema" / "agent-definition.schema.json"


def main(path: str) -> None:
    schema = json.loads(SCHEMA_PATH.read_text())
    instance = json.loads(Path(path).read_text())

    validator = Draft202012Validator(schema)
    errors = sorted(validator.iter_errors(instance), key=lambda e: e.path)

    if errors:
        print(f"❌ {path} is NOT valid:")
        for err in errors:
            loc = ".".join(str(x) for x in err.path) or "<root>"
            print(f"  - {loc}: {err.message}")
        sys.exit(1)
    else:
        print(f"✅ {path} is valid against agent-definition.schema.json")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python tools/validate.py <path-to-agent-json>")
        sys.exit(1)
    main(sys.argv[1])
