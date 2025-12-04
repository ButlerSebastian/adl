# Contributing to Agent Definition Language

Thanks for your interest in contributing! This project aims to provide a stable, vendor-neutral JSON schema
for defining AI agents, tools, and RAG indices.

## How to Contribute

1. **Fork** the repository.
2. **Create a branch** for your change:
   ```bash
   git checkout -b feature/my-change
   ```
3. Update or add:
   - Schema changes in `schema/agent-definition.schema.json`
   - Documentation in `docs/`
   - Examples in `examples/` (ensure they validate)
4. Run validation locally:
   ```bash
   pip install jsonschema
   for f in examples/*.json; do
       python tools/validate.py "$f"
   done
   ```
5. **Open a Pull Request** with a clear description and rationale for the change.

## Versioning Policy

We use **semantic versioning (semver)** for the repository:

- **MAJOR** version: Breaking changes to the schema (existing valid documents may become invalid or change meaning).
- **MINOR** version: Backwards-compatible additions (new optional fields, new `$defs`, new examples, docs).
- **PATCH** version: Backwards-compatible bug fixes, typo fixes, or doc-only changes.

Examples: `v0.1.0`, `v0.2.3`, `v1.0.0`.

### When to bump versions

- **Breaking schema changes** → bump **MAJOR**.
- **New optional fields or new definitions** → bump **MINOR**.
- **Docs, examples, or tooling-only** changes → bump **PATCH**.

### Agent document `version` field

Each agent JSON instance can include its own integer `version` field:

```json
{
  "id": "483fa0f5-7854-48e4-9347-25d5e47d7e2b",
  "version": 3,
  "name": "generate campaign image",
  "...": "..."
}
```

This field is **not tied** to the repository version. It represents the evolution of an individual agent definition
within your own system.

### Schema Stability

- The project aims to keep backwards compatibility where possible.
- Deprecated fields should be documented in `docs/schema-reference.md` and, where appropriate, marked in the JSON Schema via `description` notes.
- Breaking changes should be rare and well-justified in the PR description and release notes.

## Coding Style for Tools

- Python: prefer Python 3.10+ and standard library where possible.
- JavaScript/Node: use modern syntax, keep dependencies minimal.

## Adding New Examples

- Place new examples in `examples/`.
- Ensure they validate against the schema using `tools/validate.py` or `tools/validate.js`.
- Keep them small and focused; large real-world agents can be hosted elsewhere and linked from docs.
