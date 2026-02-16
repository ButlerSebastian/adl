# ADL CLI Reference

Complete reference for all ADL command-line interface tools.

## Overview

The ADL CLI provides a comprehensive toolchain for working with Agent Definition Language files. It includes commands for compiling, validating, formatting, linting, and generating code from ADL definitions.

## Installation

### From Source

```bash
git clone https://github.com/nextmoca/adl.git
cd adl
pip install -e .
```

### From PyPI (Coming Soon)

```bash
pip install adl
```

### Verify Installation

```bash
adl-validate --version
```

## Available Commands

- `adl-compile` - Compile ADL files to various output formats
- `adl-validate` - Validate ADL files against the schema
- `adl-format` - Format ADL files according to style guidelines
- `adl-lint` - Lint ADL files for code quality issues
- `adl-generate` - Generate code from ADL definitions

## Common Options

All commands support the following options:

- `-h, --help` - Show help message and exit
- `-v, --verbose` - Enable verbose output
- `-q, --quiet` - Suppress non-error output
- `--version` - Show version information

## File Extensions

The ADL CLI recognizes the following file extensions:

- `.adl` - ADL DSL files
- `.json` - JSON schema files
- `.yaml`, `.yml` - YAML files

## Exit Codes

- `0` - Success
- `1` - General error
- `2` - Validation error
- `3` - Linting error
- `4` - File not found
- `5` - Parse error

## Configuration

The ADL CLI can be configured using:

1. **Command-line arguments** - Highest priority
2. **Environment variables** - Medium priority
3. **Configuration file** - Lowest priority

### Configuration File

Create a `.adlrc` file in your project root:

```toml
[format]
indent_size = 2
insert_spaces = true
max_line_length = 100

[lint]
severity = "warning"
enable_rules = ["type-name-pascal-case", "field-name-snake-case"]
disable_rules = []

[compile]
output_format = "json"
include_source = false
```

### Environment Variables

- `ADL_FORMAT_INDENT_SIZE` - Default indentation size
- `ADL_FORMAT_INSERT_SPACES` - Use spaces instead of tabs (true/false)
- `ADL_LINT_SEVERITY` - Minimum lint severity (error/warning/info)
- `ADL_COMPILE_OUTPUT_FORMAT` - Default output format

## Troubleshooting

### Command Not Found

If you get `command not found` after installation:

```bash
# Check if pip installed to user directory
pip show adl

# Add user bin to PATH (if needed)
export PATH="$HOME/.local/bin:$PATH"
```

### Import Errors

If you get import errors:

```bash
# Reinstall with dependencies
pip install --force-reinstall adl

# Or install from source
pip install -e .
```

### Permission Errors

If you get permission errors:

```bash
# Install to user directory
pip install --user adl

# Or use virtual environment
python -m venv venv
source venv/bin/activate
pip install adl
```

## Best Practices

1. **Always validate** before compiling or generating code
2. **Use linting** to maintain code quality
3. **Format files** before committing to version control
4. **Use verbose mode** when debugging issues
5. **Check exit codes** in scripts and CI/CD pipelines

## Examples

### Basic Workflow

```bash
# Validate ADL file
adl-validate my-agent.adl

# Format ADL file
adl-format my-agent.adl

# Lint ADL file
adl-lint my-agent.adl

# Compile to JSON
adl-compile my-agent.adl -o my-agent.json

# Generate Python code
adl-generate my-agent.adl -f python -o my_agent.py
```

### CI/CD Integration

```bash
#!/bin/bash
set -e

# Validate all ADL files
for file in $(find . -name "*.adl"); do
    adl-validate "$file"
    adl-lint "$file" --severity=error
done

# Format all ADL files
for file in $(find . -name "*.adl"); do
    adl-format "$file" --check
done
```

## Next Steps

- See individual command documentation for detailed usage
- Check [examples/](../../examples/) for sample ADL files
- Read [DSL Design](../adl-dsl-design.md) for language specification

---

## adl-compile

Compile ADL files to various output formats.

### Usage

```bash
adl-compile [OPTIONS] INPUT_FILE
```

### Options

- `-o, --output FILE` - Output file path (default: stdout)
- `-f, --format FORMAT` - Output format: json, yaml, python, typescript (default: json)
- `--include-source` - Include source ADL in output
- `--validate` - Validate before compiling (default: true)
- `--no-validate` - Skip validation
- `-v, --verbose` - Enable verbose output
- `-h, --help` - Show help message

### Examples

#### Compile to JSON

```bash
adl-compile my-agent.adl -o my-agent.json
```

#### Compile to YAML

```bash
adl-compile my-agent.adl -f yaml -o my-agent.yaml
```

#### Compile to Python

```bash
adl-compile my-agent.adl -f python -o my_agent.py
```

#### Compile to TypeScript

```bash
adl-compile my-agent.adl -f typescript -o my_agent.ts
```

#### Compile with source included

```bash
adl-compile my-agent.adl --include-source -o my-agent.json
```

#### Compile without validation

```bash
adl-compile my-agent.adl --no-validate -o my-agent.json
```

#### Compile to stdout

```bash
adl-compile my-agent.adl
```

### Output Formats

#### JSON

Standard JSON format with full ADL schema compliance:

```json
{
  "name": "campaign_image_generator",
  "description": "Generate a 1024x1024 marketing image from a creative brief.",
  "role": "Creative Producer",
  "llm": "openai",
  "llm_settings": {
    "temperature": 0,
    "max_tokens": 4096
  },
  "tools": [...]
}
```

#### YAML

Human-readable YAML format:

```yaml
name: campaign_image_generator
description: Generate a 1024x1024 marketing image from a creative brief.
role: Creative Producer
llm: openai
llm_settings:
  temperature: 0
  max_tokens: 4096
tools: [...]
```

#### Python

Python class definitions:

```python
from typing import List, Optional
from dataclasses import dataclass

@dataclass
class CampaignImageGenerator:
    name: str = "campaign_image_generator"
    description: str = "Generate a 1024x1024 marketing image from a creative brief."
    role: str = "Creative Producer"
    llm: str = "openai"
    llm_settings: dict = None
    tools: List[dict] = None
```

#### TypeScript

TypeScript interface definitions:

```typescript
export interface CampaignImageGenerator {
  name: string;
  description: string;
  role: string;
  llm: string;
  llm_settings: {
    temperature: number;
    max_tokens: number;
  };
  tools: Tool[];
}
```

### Error Handling

The compiler will exit with error code 2 if validation fails:

```bash
adl-compile invalid.adl
# Error: Validation failed
# Exit code: 2
```

### Best Practices

1. **Always validate** before compiling (default behavior)
2. **Use appropriate format** for your target platform
3. **Include source** for debugging and traceability
4. **Check exit codes** in scripts

### Use Cases

- **API Integration**: Compile to JSON for REST APIs
- **Configuration**: Compile to YAML for deployment configs
- **Python Projects**: Compile to Python for type-safe code
- **TypeScript Projects**: Compile to TypeScript for frontend apps
- **Documentation**: Compile to human-readable formats

---

## adl-validate

Validate ADL files against the schema.

### Usage

```bash
adl-validate [OPTIONS] INPUT_FILE
```

### Options

- `-s, --schema FILE` - Custom schema file (default: built-in schema)
- `--strict` - Enable strict validation mode
- `--no-warnings` - Suppress warnings
- `-v, --verbose` - Enable verbose output
- `-h, --help` - Show help message

### Examples

#### Validate ADL file

```bash
adl-validate my-agent.adl
```

#### Validate with custom schema

```bash
adl-validate my-agent.adl -s custom-schema.json
```

#### Validate in strict mode

```bash
adl-validate my-agent.adl --strict
```

#### Validate without warnings

```bash
adl-validate my-agent.adl --no-warnings
```

#### Validate with verbose output

```bash
adl-validate my-agent.adl -v
```

### Validation Rules

The validator checks for:

1. **Schema Compliance**
   - Required fields present
   - Field types match schema
   - Enum values valid
   - Numeric constraints satisfied

2. **Syntax Validation**
   - Valid ADL syntax
   - Proper nesting
   - No duplicate keys

3. **Semantic Validation**
   - Type references exist
   - Import paths valid
   - Tool categories valid
   - Return types defined

4. **Best Practices** (in strict mode)
   - Descriptions present
   - Naming conventions followed
   - No unused imports
   - No circular dependencies

### Output

#### Success

```bash
adl-validate my-agent.adl
# Valid: my-agent.adl
# Exit code: 0
```

#### Error

```bash
adl-validate invalid.adl
# Error: Missing required field 'name' at line 5
# Exit code: 2
```

#### Warning

```bash
adl-validate my-agent.adl
# Warning: Missing description for field 'user_id'
# Valid: my-agent.adl (with warnings)
# Exit code: 0
```

#### Strict Mode Error

```bash
adl-validate my-agent.adl --strict
# Error: Type name should use PascalCase: 'myType'
# Exit code: 2
```

### Error Messages

The validator provides detailed error messages:

- **Location**: Line and column number
- **Issue**: Description of the problem
- **Suggestion**: How to fix (when available)
- **Context**: Relevant code snippet

### Exit Codes

- `0` - Valid (with or without warnings)
- `2` - Validation error
- `4` - File not found
- `5` - Parse error

### Best Practices

1. **Validate early** - Validate before compiling or generating
2. **Use strict mode** - Enforce best practices in CI/CD
3. **Check exit codes** - Handle validation errors in scripts
4. **Fix warnings** - Address warnings before deployment

### CI/CD Integration

```bash
#!/bin/bash
set -e

# Validate all ADL files
for file in $(find . -name "*.adl"); do
    echo "Validating $file..."
    adl-validate "$file" --strict --no-warnings
done

echo "All ADL files are valid!"
```

### Use Cases

- **Pre-commit Hooks**: Validate before committing
- **CI/CD Pipelines**: Ensure quality before deployment
- **Development**: Catch errors early
- **Code Review**: Validate changes
- **Documentation**: Verify examples are valid
