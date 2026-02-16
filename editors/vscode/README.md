# ADL DSL Support for VS Code

Syntax highlighting and language support for ADL (Agent Definition Language).

## Features

- **Syntax Highlighting**: Full syntax highlighting for ADL files (.adl)
- **Error Diagnostics**: Real-time syntax and validation error detection
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

## Error Diagnostics

The extension provides real-time error detection for ADL files:

### Syntax Errors
- **Unmatched braces**: Detects missing or extra `{ } [ ] ( )`
- **Invalid identifiers**: Identifiers must start with a letter or underscore
- **Unterminated strings**: Detects missing closing quotes
- **Invalid number formats**: Detects malformed numeric literals

### Validation Errors
- **Missing import paths**: Import statements require a path
- **Missing definition names**: `enum`, `type`, and `agent` definitions require names
- **Missing type annotations**: Type annotations require a type

### Error Display
Errors are displayed in:
- Red squiggle underlines in the editor
- Problems panel (View → Problems)
- Output channel (View → Output → ADL Diagnostics)

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
├── tsconfig.json                   # TypeScript configuration
├── language-configuration.json     # Language configuration
├── syntaxes/
│   └── adl.tmLanguage.json        # TextMate grammar
├── themes/
│   └── adl-color-theme.json       # Color theme
├── src/
│   ├── extension.ts               # Extension entry point
│   └── diagnostics.ts             # Diagnostics provider
└── README.md                       # This file
```

### Building

```bash
npm install
npm run compile
```

### Testing

1. Press `F5` to launch Extension Development Host
2. Open an `.adl` file
3. Verify syntax highlighting works correctly
4. Test error detection by introducing syntax errors
5. Check the Problems panel for error messages

## Contributing

Contributions are welcome! Please see the main [ADL repository](https://github.com/nextmoca/adl) for contribution guidelines.

## License

Apache License 2.0

## Links

- [ADL Specification](https://github.com/nextmoca/adl)
- [ADL Documentation](https://github.com/nextmoca/adl/tree/main/docs)
- [Issue Tracker](https://github.com/nextmoca/adl/issues)
