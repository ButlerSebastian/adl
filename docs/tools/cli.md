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
