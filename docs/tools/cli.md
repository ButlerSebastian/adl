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

---

## adl-format

Format ADL files according to style guidelines.

### Usage

```bash
adl-format [OPTIONS] INPUT_FILE
```

### Options

- `-o, --output FILE` - Output file path (default: overwrite input)
- `-c, --check` - Check if file is formatted (no changes)
- `--indent-size N` - Indentation size (default: 2)
- `--insert-spaces` - Use spaces instead of tabs (default: true)
- `--use-tabs` - Use tabs instead of spaces
- `--max-line-length N` - Maximum line length (default: 100)
- `-v, --verbose` - Enable verbose output
- `-h, --help` - Show help message

### Examples

#### Format ADL file (in-place)

```bash
adl-format my-agent.adl
```

#### Format to new file

```bash
adl-format my-agent.adl -o formatted-agent.adl
```

#### Check if file is formatted

```bash
adl-format my-agent.adl --check
```

#### Format with custom indentation

```bash
adl-format my-agent.adl --indent-size 4
```

#### Format with tabs

```bash
adl-format my-agent.adl --use-tabs
```

#### Format with custom line length

```bash
adl-format my-agent.adl --max-line-length 120
```

### Formatting Rules

The formatter applies the following rules:

1. **Indentation**
   - Consistent indentation (2 spaces by default)
   - Nested structures indented properly
   - No mixed tabs and spaces

2. **Spacing**
   - Spaces around operators
   - Spaces after commas
   - No trailing whitespace
   - Single blank line between sections

3. **Line Length**
   - Maximum 100 characters per line (configurable)
   - Long lines wrapped appropriately
   - Break at logical points

4. **Ordering**
   - Fields in consistent order
   - Imports sorted alphabetically
   - Sections in standard order

5. **Comments**
   - Consistent comment style
   - Proper indentation
   - No orphaned comments

### Output

#### Success

```bash
adl-format my-agent.adl
# Formatted: my-agent.adl
# Exit code: 0
```

#### Check - Formatted

```bash
adl-format my-agent.adl --check
# Formatted: my-agent.adl
# Exit code: 0
```

#### Check - Not Formatted

```bash
adl-format my-agent.adl --check
# Not formatted: my-agent.adl
# Exit code: 1
```

#### Verbose Output

```bash
adl-format my-agent.adl -v
# Formatting my-agent.adl...
# - Fixed indentation
# - Removed trailing whitespace
# - Wrapped long lines
# Formatted: my-agent.adl
```

### Exit Codes

- `0` - Formatted successfully (or already formatted in check mode)
- `1` - Not formatted (in check mode)
- `4` - File not found
- `5` - Parse error

### Best Practices

1. **Format before committing** - Keep code clean
2. **Use check mode in CI** - Ensure consistent formatting
3. **Configure team standards** - Use config file for team settings
4. **Auto-format on save** - Configure editor to format on save

### Editor Integration

#### VS Code

Add to `.vscode/settings.json`:

```json
{
  "editor.formatOnSave": true,
  "[adl]": {
    "editor.defaultFormatter": "adl.formatter",
    "editor.formatOnSave": true
  }
}
```

#### Vim

Add to `.vimrc`:

```vim
autocmd BufWritePre *.adl :!adl-format %
```

#### Emacs

Add to `.emacs`:

```elisp
(add-hook 'before-save-hook
          (lambda ()
            (when (eq major-mode 'adl-mode)
              (shell-command (concat "adl-format " (buffer-file-name))))))
```

### CI/CD Integration

```bash
#!/bin/bash
set -e

# Check formatting of all ADL files
for file in $(find . -name "*.adl"); do
    echo "Checking formatting of $file..."
    adl-format "$file" --check
done

echo "All ADL files are properly formatted!"
```

### Use Cases

- **Pre-commit Hooks**: Format before committing
- **CI/CD Pipelines**: Ensure consistent formatting
- **Team Collaboration**: Maintain code style
- **Code Review**: Reduce formatting noise
- **Refactoring**: Clean up code style

---

## adl-lint

Lint ADL files for code quality issues.

### Usage

```bash
adl-lint [OPTIONS] INPUT_FILE
```

### Options

- `-s, --severity LEVEL` - Minimum severity: error, warning, info (default: warning)
- `-r, --rules RULES` - Comma-separated list of rules to enable
- `-d, --disable RULES` - Comma-separated list of rules to disable
- `--fix` - Automatically fix fixable issues
- `--check` - Check only (no fixes)
- `-o, --output FILE` - Output file for lint results (default: stdout)
- `-f, --format FORMAT` - Output format: text, json, yaml (default: text)
- `-v, --verbose` - Enable verbose output
- `-h, --help` - Show help message

### Examples

#### Lint ADL file

```bash
adl-lint my-agent.adl
```

#### Lint with error severity only

```bash
adl-lint my-agent.adl --severity error
```

#### Lint with specific rules

```bash
adl-lint my-agent.adl --rules type-name-pascal-case,field-name-snake-case
```

#### Lint and disable specific rules

```bash
adl-lint my-agent.adl --disable trailing-whitespace,max-line-length
```

#### Lint and auto-fix

```bash
adl-lint my-agent.adl --fix
```

#### Lint and output to JSON

```bash
adl-lint my-agent.adl -f json -o lint-results.json
```

#### Lint in check mode

```bash
adl-lint my-agent.adl --check
```

### Linting Rules

#### Naming Conventions

- `type-name-pascal-case` - Type names should use PascalCase
- `field-name-snake-case` - Field names should use snake_case
- `enum-value-lowercase` - Enum values should use lowercase

#### Documentation

- `missing-type-description` - Type definitions should have descriptions
- `missing-field-description` - Fields should have descriptions

#### Imports

- `import-order` - Imports should be ordered alphabetically
- `unused-import` - Imports should be used

#### Style

- `trailing-whitespace` - Lines should not have trailing whitespace
- `no-tabs` - Use spaces instead of tabs
- `max-line-length` - Lines should not exceed max length

### Output

#### Text Format (default)

```bash
adl-lint my-agent.adl
# warning: type-name-pascal-case - Type name should use PascalCase: myType (line 5)
# warning: missing-field-description - Field should have a description comment (line 12)
# error: no-tabs - Use spaces instead of tabs (line 20)
```

#### JSON Format

```bash
adl-lint my-agent.adl -f json
{
  "file": "my-agent.adl",
  "issues": [
    {
      "rule": "type-name-pascal-case",
      "severity": "warning",
      "line": 5,
      "column": 1,
      "message": "Type name should use PascalCase: myType",
      "fixable": false
    }
  ]
}
```

#### YAML Format

```bash
adl-lint my-agent.adl -f yaml
file: my-agent.adl
issues:
  - rule: type-name-pascal-case
    severity: warning
    line: 5
    column: 1
    message: Type name should use PascalCase: myType
    fixable: false
```

### Exit Codes

- `0` - No issues (or only warnings below severity threshold)
- `1` - Issues found
- `3` - Linting error
- `4` - File not found
- `5` - Parse error

### Best Practices

1. **Lint before committing** - Catch issues early
2. **Use severity filters** - Focus on important issues
3. **Enable auto-fix** - Fix simple issues automatically
4. **Configure team rules** - Use config file for team standards
5. **Check in CI** - Enforce quality in CI/CD

### Configuration

Create a `.adlrc` file:

```toml
[lint]
severity = "warning"
enable_rules = ["type-name-pascal-case", "field-name-snake-case"]
disable_rules = ["max-line-length"]
```

### CI/CD Integration

```bash
#!/bin/bash
set -e

# Lint all ADL files
for file in $(find . -name "*.adl"); do
    echo "Linting $file..."
    adl-lint "$file" --severity error --check
done

echo "No linting errors found!"
```

### Use Cases

- **Pre-commit Hooks**: Lint before committing
- **CI/CD Pipelines**: Enforce code quality
- **Code Review**: Identify issues early
- **Refactoring**: Clean up code style
- **Team Standards**: Enforce naming conventions

---

## adl-generate

Generate code from ADL definitions.

### Usage

```bash
adl-generate [OPTIONS] INPUT_FILE
```

### Options

- `-f, --format FORMAT` - Output format: python, typescript, json-schema, openapi (required)
- `-o, --output FILE` - Output file path (default: stdout)
- `--package-name NAME` - Package name for generated code
- `--class-prefix PREFIX` - Prefix for generated classes
- `--include-docs` - Include documentation in generated code
- `--no-docs` - Exclude documentation from generated code
- `--include-validators` - Include validation functions
- `--no-validators` - Exclude validation functions
- `-v, --verbose` - Enable verbose output
- `-h, --help` - Show help message

### Examples

#### Generate Python code

```bash
adl-generate my-agent.adl -f python -o my_agent.py
```

#### Generate TypeScript code

```bash
adl-generate my-agent.adl -f typescript -o my_agent.ts
```

#### Generate JSON Schema

```bash
adl-generate my-agent.adl -f json-schema -o schema.json
```

#### Generate OpenAPI specification

```bash
adl-generate my-agent.adl -f openapi -o openapi.yaml
```

#### Generate with package name

```bash
adl-generate my-agent.adl -f python --package-name my_package -o my_agent.py
```

#### Generate with class prefix

```bash
adl-generate my-agent.adl -f typescript --class-prefix ADL -o my_agent.ts
```

#### Generate with documentation

```bash
adl-generate my-agent.adl -f python --include-docs -o my_agent.py
```

#### Generate with validators

```bash
adl-generate my-agent.adl -f python --include-validators -o my_agent.py
```

### Output Formats

#### Python

Generates Python dataclasses with type hints:

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

Generates TypeScript interfaces:

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

#### JSON Schema

Generates JSON Schema for validation:

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "properties": {
    "name": {
      "type": "string",
      "description": "Agent name"
    },
    "description": {
      "type": "string",
      "description": "Agent description"
    }
  },
  "required": ["name", "description"]
}
```

#### OpenAPI

Generates OpenAPI specification:

```yaml
openapi: 3.0.0
info:
  title: Campaign Image Generator API
  version: 1.0.0
paths:
  /generate:
    post:
      summary: Generate campaign image
      requestBody:
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/GenerateRequest'
```

### Output

#### Success

```bash
adl-generate my-agent.adl -f python -o my_agent.py
# Generated: my_agent.py
# Exit code: 0
```

#### Error

```bash
adl-generate invalid.adl -f python
# Error: Parse error at line 5
# Exit code: 5
```

#### Verbose Output

```bash
adl-generate my-agent.adl -f python -v
# Parsing my-agent.adl...
# Generating Python code...
# - Generated 5 classes
# - Generated 10 functions
# Generated: my_agent.py
```

### Exit Codes

- `0` - Generated successfully
- `1` - Generation error
- `4` - File not found
- `5` - Parse error

### Best Practices

1. **Validate before generating** - Ensure ADL is valid
2. **Use appropriate format** - Match your target platform
3. **Include documentation** - For better code readability
4. **Include validators** - For runtime validation
5. **Version control generated code** - Track changes

### Use Cases

- **Python Projects**: Generate type-safe Python code
- **TypeScript Projects**: Generate TypeScript interfaces
- **API Documentation**: Generate OpenAPI specs
- **Validation**: Generate JSON schemas
- **Code Generation**: Automate boilerplate code

### Advanced Usage

#### Generate Multiple Formats

```bash
adl-generate my-agent.adl -f python -o my_agent.py
adl-generate my-agent.adl -f typescript -o my_agent.ts
adl-generate my-agent.adl -f json-schema -o schema.json
```

#### Generate with Custom Package

```bash
adl-generate my-agent.adl -f python --package-name myapp.models -o models.py
```

#### Generate for Multiple Agents

```bash
for file in agents/*.adl; do
    name=$(basename "$file" .adl)
    adl-generate "$file" -f python -o "generated/${name}.py"
done
```

---

## Summary

The ADL CLI provides a comprehensive toolchain for working with Agent Definition Language files:

| Command | Purpose |
|---------|---------|
| `adl-compile` | Compile ADL to various formats |
| `adl-validate` | Validate ADL against schema |
| `adl-format` | Format ADL files |
| `adl-lint` | Lint ADL for code quality |
| `adl-generate` | Generate code from ADL |

For more information, see:
- [ADL DSL Design](../adl-dsl-design.md)
- [Examples](../../examples/)
- [Schema Reference](../schema-reference.md)
