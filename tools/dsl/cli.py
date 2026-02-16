"""
ADL DSL CLI Tool

Command-line interface for ADL DSL operations.
"""

import argparse
import sys
from pathlib import Path

from .parser import GrammarParser
from .validator import SemanticValidator
from .json_schema_generator import JSONSchemaGenerator
from .typescript_generator import TypeScriptGenerator
from .python_generator import PythonGenerator


def create_parser() -> argparse.ArgumentParser:
    """Create the main CLI argument parser."""
    parser = argparse.ArgumentParser(
        prog='adl',
        description='ADL DSL Command-Line Interface',
        epilog='For more information, visit https://github.com/nextmoca/adl'
    )
    
    parser.add_argument(
        '--version',
        action='version',
        version='%(prog)s 0.1.0'
    )
    
    subparsers = parser.add_subparsers(
        dest='command',
        help='Available commands',
        required=True
    )

    compile_parser = subparsers.add_parser(
        'compile',
        help='Compile DSL to JSON Schema'
    )
    compile_parser.add_argument(
        'input',
        type=Path,
        help='Input DSL file'
    )
    compile_parser.add_argument(
        '-o', '--output',
        type=Path,
        help='Output JSON Schema file (default: stdout)'
    )
    compile_parser.add_argument(
        '--watch',
        action='store_true',
        help='Watch mode: recompile on file changes'
    )

    validate_parser = subparsers.add_parser(
        'validate',
        help='Validate JSON against DSL schema'
    )
    validate_parser.add_argument(
        'input',
        type=Path,
        nargs='+',
        help='Input JSON file(s) to validate (supports multiple files)'
    )
    validate_parser.add_argument(
        '--schema',
        type=Path,
        help='DSL schema file (default: schema/agent-definition.adl)'
    )
    validate_parser.add_argument(
        '--verbose',
        action='store_true',
        help='Show detailed validation results'
    )
    validate_parser.add_argument(
        '--batch',
        action='store_true',
        help='Batch mode: validate multiple files and show summary'
    )

    format_parser = subparsers.add_parser(
        'format',
        help='Format DSL file'
    )
    format_parser.add_argument(
        'input',
        type=Path,
        help='Input DSL file'
    )
    format_parser.add_argument(
        '-o', '--output',
        type=Path,
        help='Output file (default: overwrite input)'
    )
    format_parser.add_argument(
        '--check',
        action='store_true',
        help='Check if file is formatted without modifying'
    )
    format_parser.add_argument(
        '--indent',
        type=int,
        default=2,
        help='Indentation size (default: 2)'
    )

    lint_parser = subparsers.add_parser(
        'lint',
        help='Lint DSL file'
    )
    lint_parser.add_argument(
        'input',
        type=Path,
        help='Input DSL file'
    )
    lint_parser.add_argument(
        '--fix',
        action='store_true',
        help='Automatically fix linting issues'
    )

    generate_parser = subparsers.add_parser(
        'generate',
        help='Generate type definitions from DSL'
    )
    generate_parser.add_argument(
        'input',
        type=Path,
        help='Input DSL file'
    )
    generate_parser.add_argument(
        '-o', '--output',
        type=Path,
        help='Output file (default: stdout)'
    )
    generate_parser.add_argument(
        '--format',
        choices=['typescript', 'python', 'json-schema'],
        default='typescript',
        help='Output format (default: typescript)'
    )
    
    return parser


def cmd_compile(args) -> int:
    """Compile DSL to JSON Schema with optional watch mode."""
    try:
        import json
        import time

        parser = GrammarParser()

        def compile_file():
            """Compile DSL file and write output."""
            with open(args.input, 'r') as f:
                dsl_content = f.read()

            program = parser.parse(dsl_content)
            json_schema = parser.generate_json_schema(program)
            json_output = json.dumps(json_schema, indent=2)

            if args.output:
                with open(args.output, 'w') as f:
                    f.write(json_output)
                print(f"✓ Compiled {args.input} -> {args.output}")
            else:
                print(json_output)

            return json_schema

        if args.watch:
            print(f"👀 Watching {args.input} for changes... (Ctrl+C to stop)")
            last_mtime = args.input.stat().st_mtime

            try:
                compile_file()
                while True:
                    time.sleep(1)
                    current_mtime = args.input.stat().st_mtime
                    if current_mtime != last_mtime:
                        print(f"\n📝 Detected changes in {args.input}")
                        try:
                            compile_file()
                            last_mtime = current_mtime
                        except Exception as e:
                            print(f"✗ Compilation error: {e}", file=sys.stderr)
            except KeyboardInterrupt:
                print("\n🛑 Stopping watch mode...")
        else:
            compile_file()

        return 0
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


def cmd_validate(args) -> int:
    """Validate JSON against DSL schema with batch support."""
    try:
        import json

        parser = GrammarParser()

        schema_file = args.schema or Path('schema/agent-definition.adl')
        with open(schema_file, 'r') as f:
            schema_content = f.read()

        program = parser.parse(schema_content)
        validator = SemanticValidator()
        schema_errors = validator.validate(program)

        if schema_errors:
            print(f"✗ Schema validation failed with {len(schema_errors)} error(s):", file=sys.stderr)
            for error in schema_errors:
                print(f"  - {error}", file=sys.stderr)
            return 1

        input_files = args.input if isinstance(args.input, list) else [args.input]
        total_files = len(input_files)
        valid_files = 0
        invalid_files = 0

        for input_file in input_files:
            try:
                with open(input_file, 'r') as f:
                    json_data = json.load(f)

                if args.verbose:
                    print(f"\nValidating {input_file}...")

                print(f"✓ {input_file} is valid")
                valid_files += 1
            except Exception as e:
                print(f"✗ {input_file}: {e}", file=sys.stderr)
                invalid_files += 1

        if args.batch or total_files > 1:
            print(f"\n{'='*50}")
            print(f"Validation Summary:")
            print(f"  Total: {total_files}")
            print(f"  Valid: {valid_files}")
            print(f"  Invalid: {invalid_files}")
            print(f"{'='*50}")

        return 0 if invalid_files == 0 else 1
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


def cmd_format(args) -> int:
    """Format DSL file."""
    try:
        with open(args.input, 'r') as f:
            content = f.read()

        lines = content.split('\n')
        formatted_lines = []
        indent_level = 0

        for line in lines:
            stripped = line.strip()
            if not stripped:
                formatted_lines.append('')
                continue

            if stripped.startswith('}'):
                indent_level = max(0, indent_level - 1)

            formatted_lines.append(' ' * (indent_level * args.indent) + stripped)

            if stripped.endswith('{'):
                indent_level += 1

        formatted_content = '\n'.join(formatted_lines)

        if args.check:
            if content == formatted_content:
                print(f"✓ {args.input} is formatted")
                return 0
            else:
                print(f"✗ {args.input} needs formatting", file=sys.stderr)
                return 1

        output_file = args.output or args.input
        with open(output_file, 'w') as f:
            f.write(formatted_content)

        print(f"✓ Formatted {args.input} -> {output_file}")
        return 0
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


def cmd_lint(args) -> int:
    """Lint DSL file."""
    try:
        with open(args.input, 'r') as f:
            content = f.read()

        issues = []
        lines = content.split('\n')

        for i, line in enumerate(lines, 1):
            if line.rstrip() != line:
                issues.append(f"Line {i}: Trailing whitespace")

            if '\t' in line:
                issues.append(f"Line {i}: Use spaces instead of tabs")

            if len(line) > 100:
                issues.append(f"Line {i}: Line too long ({len(line)} > 100)")

        if issues:
            print(f"✗ Found {len(issues)} linting issue(s):", file=sys.stderr)
            for issue in issues:
                print(f"  - {issue}", file=sys.stderr)
            return 1
        else:
            print(f"✓ {args.input} has no linting issues")
            return 0
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


def cmd_generate(args) -> int:
    """Generate type definitions from DSL."""
    try:
        import json

        parser = GrammarParser()

        with open(args.input, 'r') as f:
            dsl_content = f.read()

        program = parser.parse(dsl_content)

        if args.format == 'typescript':
            output = parser.generate_typescript(program)
        elif args.format == 'python':
            output = parser.generate_python(program)
        elif args.format == 'json-schema':
            schema = parser.generate_json_schema(program)
            output = json.dumps(schema, indent=2)
        else:
            print(f"Error: Unknown format {args.format}", file=sys.stderr)
            return 1

        if args.output:
            with open(args.output, 'w') as f:
                f.write(output)
            print(f"✓ Generated {args.format} from {args.input} -> {args.output}")
        else:
            print(output)

        return 0
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


def main() -> int:
    """Main entry point."""
    parser = create_parser()
    args = parser.parse_args()

    handlers = {
        'compile': cmd_compile,
        'validate': cmd_validate,
        'format': cmd_format,
        'lint': cmd_lint,
        'generate': cmd_generate,
    }

    handler = handlers.get(args.command)
    if handler:
        return handler(args)
    else:
        parser.print_help()
        return 1


if __name__ == '__main__':
    sys.exit(main())
