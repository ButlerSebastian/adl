# ADL DSL Support for VS Code

Syntax highlighting and language support for ADL (Agent Definition Language).

## Features

- **Syntax Highlighting**: Full syntax highlighting for ADL files (.adl)
- **Color Theme**: Custom dark theme optimized for ADL development
- **Language Configuration**: Auto-closing brackets, comments, and more

## Installation

### From Source

1. Clone this repository
2. Open VS Code
3. Press `F5` to launch a new Extension Development Host window
4. Open an `.adl` file to test the extension

### From VS Code Marketplace (Coming Soon)

The extension will be published to the VS Code Marketplace for easy installation.

## Supported Syntax

### Keywords
- `import`, `enum`, `type`, `agent`, `as`, `module`, `export`, `validation`

### Primitive Types
- `string`, `integer`, `number`, `boolean`, `object`, `array`, `any`, `null`

### Boolean Literals
- `true`, `false`

### Comments
- Line comments starting with `#`

### Identifiers
- Alphanumeric identifiers with underscores and hyphens: `[a-zA-Z_][a-zA-Z0-9_-]*`

### Numeric Literals
- Integers: `42`, `-10`
- Decimals: `3.14`, `-0.5`
- Scientific notation: `1.5e10`, `-2.5E-5`

### Strings
- Double-quoted strings: `"hello world"`

### Structural Symbols
- Brackets: `{ } [ ] ( )`
- Separators: `: , ? | . /`

## Example

```adl
# Import statements
import schema/components/rag
import schema/components/tool as tools

# Enum definitions
enum Lifecycle {
  stable
  beta
  deprecated
  experimental
}

# Type definitions
type Person {
  name: string
  age: integer
  email?: string
  tags: string[]
}

# Agent definitions
agent MyAgent {
  id: string
  name: string
  version: integer
  config: Config
}
```

## Development

### Project Structure

```
editors/vscode/
├── package.json                    # Extension manifest
├── language-configuration.json     # Language configuration
├── syntaxes/
│   └── adl.tmLanguage.json        # TextMate grammar
├── themes/
│   └── adl-color-theme.json       # Color theme
└── README.md                       # This file
```

### Building

No build step required. The extension uses TextMate grammar for syntax highlighting.

### Testing

1. Open an `.adl` file in VS Code
2. Verify syntax highlighting works correctly
3. Test with various ADL code examples

## Contributing

Contributions are welcome! Please see the main [ADL repository](https://github.com/nextmoca/adl) for contribution guidelines.

## License

Apache License 2.0

## Links

- [ADL Specification](https://github.com/nextmoca/adl)
- [ADL Documentation](https://github.com/nextmoca/adl/tree/main/docs)
- [Issue Tracker](https://github.com/nextmoca/adl/issues)
