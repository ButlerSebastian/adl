# ADL DSL Support for VS Code

Syntax highlighting and language support for ADL (Agent Definition Language).

## Features

- **Syntax Highlighting**: Full syntax highlighting for ADL files (.adl)
- **Error Diagnostics**: Real-time syntax and validation error detection
- **Auto-completion**: Intelligent code completion for keywords, types, and fields
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

## Auto-completion

The extension provides intelligent code completion for ADL files:

### Completion Triggers
- Type `:` to trigger type completions
- Type ` ` (space) to trigger keyword completions
- Press `Ctrl+Space` to manually trigger completions

### Completion Items

#### Keywords
- `import`, `enum`, `type`, `agent`, `as`, `module`, `export`, `validation`

#### Primitive Types
- `string`, `integer`, `number`, `boolean`, `object`, `array`, `any`, `null`

#### Array Types
- `string[]`, `integer[]`, `number[]`, `boolean[]`, etc.

#### Optional Types
- `string?`, `integer?`, `number?`, `boolean?`, etc.

#### Boolean Literals
- `true`, `false`

#### Common Fields
- `name`, `description`, `version`, `id`, `config`, `parameters`, `returns`, `required`, `default`, `minLength`, `maxLength`, `minimum`, `maximum`, `pattern`, `enum`

### Example Usage

```adl
type Person {
  name: string    # Type completion after ':'
  age: integer    # Type completion after ':'
  email?: string  # Optional type completion
  tags: string[]  # Array type completion
  active: true    # Boolean literal completion
}
```

## Go to Definition

The extension provides navigation to type and enum definitions:

### Usage
- Press `F12` on a type or enum reference to navigate to its definition
- Works with types defined in the current file
- Handles cross-file references from import statements

### Supported References
- Type definitions: `type Person { ... }`
- Enum definitions: `enum Status { active, inactive }`
- Import statements: `import { Person } from './types'`

### Example
```adl
# Import type from another file
import { User } from './user'

# Use the imported type
type Profile {
  user: User
  metadata: Metadata
}

# Navigate to User definition with F12
```

## Hover Information

The extension provides hover information for types, enums, and fields:

### Usage
- Hover over a type name to see its fields
- Hover over an enum name to see its values
- Hover over a field name to see its type

### Supported Hovers
- **Type Hovers**: Show type name and all fields with their types
- **Enum Hovers**: Show enum name and all possible values
- **Field Hovers**: Show field name and its type

### Example
```adl
type Person {
  name: string
  age: integer
  email?: string
}

# Hover over 'Person' to see:
# **Type**: `Person`
#
# **Fields**:
# **name**: `string`
# **age**: `integer`
# **email**: `string?`

# Hover over 'name' to see:
# **Field**: `name`
#
# **Type**: `string`
```

## Format on Save

The extension provides automatic formatting for ADL files:

### Format on Save
- Automatically formats the entire document when you save the file
- Can be enabled/disabled via settings

### Format Selection
- Format only the selected text with `Shift+Alt+F`
- Applies the same formatting rules to the selected range

### Format on Paste
- Automatically formats pasted content
- Ensures consistent formatting when pasting code

### Configuration

The extension provides the following configuration options:

```json
{
  "adl.format.enable": true,
  "adl.format.indentSize": 2,
  "adl.format.insertSpaces": true
}
```

#### Settings

- **adl.format.enable** (boolean, default: true)
  - Enable or disable formatting for ADL files

- **adl.format.indentSize** (number, default: 2)
  - Number of spaces to use for indentation

- **adl.format.insertSpaces** (boolean, default: true)
  - Use spaces instead of tabs for indentation

### Formatting Rules

The formatter applies the following rules:

- Consistent indentation (2 or 4 spaces based on configuration)
- Consistent spacing around colons and commas
- Consistent line breaks for braces, brackets, and parentheses
- Trailing whitespace removal
- Proper spacing in type annotations

### Example

```adl
type Person {
  name: string
  age: integer
  email?: string
  tags: string[]
}

# After formatting:
type Person {
  name: string
  age: integer
  email?: string
  tags: string[]
}
```

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
