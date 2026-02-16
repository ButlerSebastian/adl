"""
ADL DSL Linter

Comprehensive linting tool for ADL DSL files with configurable rules.
"""

from typing import List, Dict, Set, Optional, Callable, Any, Union
from dataclasses import dataclass
from pathlib import Path
import re
import importlib.util
import json
import yaml
from .parser import GrammarParser
from .adl_ast import Program, TypeDef, EnumDef, AgentDef, FieldDef


@dataclass
class LintRule:
    """Represents a linting rule."""
    
    name: str
    description: str
    severity: str  # error, warning, info
    check: Callable[[str, int], bool]
    fix: Optional[Callable[[str], str]] = None
    message: Optional[Union[str, Callable[[str], str]]] = None


@dataclass
class LintIssue:
    """Represents a linting issue."""

    rule_name: str
    line_number: int
    severity: str
    message: str
    fixable: bool = False


@dataclass
class Suppression:
    """Represents a rule suppression directive."""

    rule_name: str
    line_number: int
    scope: str  # 'next-line', 'line', 'file'
    source_line: str


class ADLLinter:
    """
    Linter for ADL DSL files.

    Provides comprehensive linting with configurable rules and autofix capabilities.
    """

    def __init__(self):
        self.rules: Dict[str, LintRule] = {}
        self.enabled_rules: Set[str] = set()
        self.severity_filter: str = 'warning'
        self.suppressions: List[Suppression] = []
        self._register_default_rules()
    
    def _register_default_rules(self):
        """Register default linting rules."""

        # Naming convention rules
        self.register_rule(LintRule(
            name='type-name-pascal-case',
            description='Type names should use PascalCase',
            severity='warning',
            check=lambda line, line_num: self._check_type_name_pascal_case(line),
            message=lambda line: f"Type name should use PascalCase: {self._extract_type_name(line)}"
        ))

        self.register_rule(LintRule(
            name='field-name-snake-case',
            description='Field names should use snake_case',
            severity='warning',
            check=lambda line, line_num: self._check_field_name_snake_case(line),
            message=lambda line: f"Field name should use snake_case: {self._extract_field_name(line)}"
        ))

        self.register_rule(LintRule(
            name='enum-value-lowercase',
            description='Enum values should use lowercase',
            severity='warning',
            check=lambda line, line_num: self._check_enum_value_lowercase(line),
            message=lambda line: f"Enum value should use lowercase: {self._extract_enum_value(line)}"
        ))

        # Documentation rules
        self.register_rule(LintRule(
            name='missing-type-description',
            description='Type definitions should have descriptions',
            severity='info',
            check=lambda line, line_num: self._check_type_description(line, line_num),
            message="Type definition should have a description comment"
        ))

        self.register_rule(LintRule(
            name='missing-field-description',
            description='Fields should have descriptions',
            severity='info',
            check=lambda line, line_num: self._check_field_description(line, line_num),
            message="Field should have a description comment"
        ))

        # Import rules
        self.register_rule(LintRule(
            name='import-order',
            description='Imports should be ordered alphabetically',
            severity='info',
            check=lambda line, line_num: self._check_import_order(line, line_num),
            message="Imports should be ordered alphabetically"
        ))

        self.register_rule(LintRule(
            name='unused-import',
            description='Imports should be used',
            severity='warning',
            check=lambda line, line_num: self._check_unused_import(line, line_num),
            message="Import is not used in the file"
        ))

        # Style rules
        self.register_rule(LintRule(
            name='trailing-whitespace',
            description='Lines should not have trailing whitespace',
            severity='warning',
            check=lambda line, line_num: line.rstrip() != line,
            fix=lambda line: line.rstrip(),
            message="Line has trailing whitespace"
        ))

        self.register_rule(LintRule(
            name='no-tabs',
            description='Use spaces instead of tabs',
            severity='error',
            check=lambda line, line_num: '\t' in line,
            fix=lambda line: line.replace('\t', '  '),
            message="Use spaces instead of tabs"
        ))

        self.register_rule(LintRule(
            name='max-line-length',
            description='Lines should not exceed max length',
            severity='warning',
            check=lambda line, line_num: len(line) > 100,
            message=lambda line: f"Line too long ({len(line)} > 100)"
        ))

        self.register_rule(LintRule(
            name='empty-line-with-whitespace',
            description='Empty lines should not contain whitespace',
            severity='info',
            check=lambda line, line_num: line.strip() == '' and line != '',
            fix=lambda line: '',
            message="Empty line contains whitespace"
        ))

        # Structure rules
        self.register_rule(LintRule(
            name='duplicate-field',
            description='Duplicate field names in type/agent',
            severity='error',
            check=lambda line, line_num: self._check_duplicate_field(line, line_num),
            message="Duplicate field name detected"
        ))

        self.register_rule(LintRule(
            name='missing-required-fields',
            description='Type/agent should have at least one field',
            severity='error',
            check=lambda line, line_num: self._check_required_fields(line, line_num),
            message="Type/agent should have at least one field"
        ))
    
    def register_rule(self, rule: LintRule):
        """Register a linting rule."""
        self.rules[rule.name] = rule
        self.enabled_rules.add(rule.name)
    
    def enable_rule(self, rule_name: str):
        """Enable a specific rule."""
        if rule_name in self.rules:
            self.enabled_rules.add(rule_name)
    
    def disable_rule(self, rule_name: str):
        """Disable a specific rule."""
        self.enabled_rules.discard(rule_name)
    
    def set_severity_filter(self, severity: str):
        """Set minimum severity level."""
        severity_order = {'error': 0, 'warning': 1, 'info': 2}
        self.severity_filter = severity
    
    def lint_file(self, file_path: Path) -> List[LintIssue]:
        """Lint a DSL file and return issues."""
        with open(file_path, 'r') as f:
            content = f.read()
        
        parser = GrammarParser()
        try:
            program = parser.parse(content)
            return self.lint_content_with_ast(content, program)
        except Exception:
            return self.lint_content(content)
    
    def lint_content(self, content: str) -> List[LintIssue]:
        """Lint DSL content and return issues."""
        # Parse suppression comments first
        self.suppressions = self._parse_suppression_comments(content)

        parser = GrammarParser()
        try:
            program = parser.parse(content)
            return self.lint_content_with_ast(content, program)
        except Exception:
            return self._lint_content_simple(content)
    
    def _lint_content_simple(self, content: str) -> List[LintIssue]:
        """Lint content without AST (fallback for syntax errors)."""
        # Parse suppression comments first
        self.suppressions = self._parse_suppression_comments(content)

        lines = content.split('\n')
        issues = []
        severity_order = {'error': 0, 'warning': 1, 'info': 2}
        min_severity = severity_order[self.severity_filter]

        # Track suppression state
        suppressed_rules = set()
        next_line_suppression = None

        # Add file suppressions (apply to all lines)
        for suppression in self.suppressions:
            if suppression.scope == 'file':
                suppressed_rules.add(suppression.rule_name)

        for line_num, line in enumerate(lines, 1):
            # Check for next-line suppression from previous line
            for suppression in self.suppressions:
                if suppression.line_number == line_num - 1 and suppression.scope == 'next-line':
                    next_line_suppression = suppression.rule_name

            # Check for line suppression
            for suppression in self.suppressions:
                if suppression.line_number == line_num and suppression.scope == 'line':
                    suppressed_rules.add(suppression.rule_name)

            # Apply next-line suppression
            if next_line_suppression:
                suppressed_rules.add(next_line_suppression)
                next_line_suppression = None

            for rule_name in self.enabled_rules:
                # Skip if rule is suppressed
                if rule_name in suppressed_rules:
                    continue

                rule = self.rules[rule_name]

                if severity_order[rule.severity] < min_severity:
                    continue

                if rule.check(line, line_num):
                    message = rule.message(line) if callable(rule.message) else (rule.message or rule.description)
                    fixable = rule.fix is not None

                    issues.append(LintIssue(
                        rule_name=rule_name,
                        line_number=line_num,
                        severity=rule.severity,
                        message=message,
                        fixable=fixable
                    ))

        return issues
    
    def lint_content_with_ast(self, content: str, program: Program) -> List[LintIssue]:
        """Lint DSL content with AST context for better analysis."""
        # Parse suppression comments first
        self.suppressions = self._parse_suppression_comments(content)

        lines = content.split('\n')
        issues = []
        severity_order = {'error': 0, 'warning': 1, 'info': 2}
        min_severity = severity_order[self.severity_filter]

        # Track context for AST-based rules
        imports = []
        import_lines = {}
        type_fields = {}
        current_type = None
        field_names = set()

        # Track suppression state
        suppressed_rules = set()
        next_line_suppression = None

        # Add file suppressions (apply to all lines)
        for suppression in self.suppressions:
            if suppression.scope == 'file':
                suppressed_rules.add(suppression.rule_name)

        for line_num, line in enumerate(lines, 1):
            # Check for next-line suppression from previous line
            for suppression in self.suppressions:
                if suppression.line_number == line_num - 1 and suppression.scope == 'next-line':
                    next_line_suppression = suppression.rule_name

            # Check for line suppression
            for suppression in self.suppressions:
                if suppression.line_number == line_num and suppression.scope == 'line':
                    suppressed_rules.add(suppression.rule_name)

            # Apply next-line suppression
            if next_line_suppression:
                suppressed_rules.add(next_line_suppression)
                next_line_suppression = None

            # Track imports
            if line.strip().startswith('import '):
                import_name = line.strip().replace('import ', '').strip()
                imports.append(import_name)
                import_lines[import_name] = line_num

            # Track current type/agent for field checking
            if line.strip().startswith(('type ', 'agent ')):
                current_type = line.strip().split()[1]
                field_names = set()
                type_fields[current_type] = []

            # Track field names
            if ':' in line and not line.strip().startswith('#'):
                match = re.search(r'(\w+)\s*:', line)
                if match and current_type:
                    field_name = match.group(1)
                    if field_name in field_names:
                        issues.append(LintIssue(
                            rule_name='duplicate-field',
                            line_number=line_num,
                            severity='error',
                            message=f"Duplicate field '{field_name}' in {current_type}",
                            fixable=False
                        ))
                    field_names.add(field_name)
                    type_fields[current_type].append(field_name)

            # Check all rules (skip suppressed rules)
            for rule_name in self.enabled_rules:
                # Skip if rule is suppressed
                if rule_name in suppressed_rules:
                    continue

                rule = self.rules[rule_name]

                if severity_order[rule.severity] < min_severity:
                    continue

                if rule.check(line, line_num):
                    message = rule.message(line) if callable(rule.message) else (rule.message or rule.description)
                    fixable = rule.fix is not None

                    issues.append(LintIssue(
                        rule_name=rule_name,
                        line_number=line_num,
                        severity=rule.severity,
                        message=message,
                        fixable=fixable
                    ))

        # Check for unused imports
        used_imports = set()
        for line in lines:
            for imp in imports:
                if imp in line:
                    used_imports.add(imp)

        for imp, line_num in import_lines.items():
            if imp not in used_imports:
                issues.append(LintIssue(
                    rule_name='unused-import',
                    line_number=line_num,
                    severity='warning',
                    message=f"Import '{imp}' is not used",
                    fixable=False
                ))

# Check import order
        if imports != sorted(imports):
            issues.append(LintIssue(
                rule_name='import-order',
                line_number=import_lines.get(imports[0], 1) if imports else 1,
                severity='info',
                message="Imports should be ordered alphabetically",
                fixable=False
            ))

        return issues
    
    def fix_file(self, file_path: Path, issues: List[LintIssue]) -> int:
        """Apply fixes to a file."""
        with open(file_path, 'r') as f:
            content = f.read()
        
        fixed_content = self.fix_content(content, issues)
        
        if fixed_content != content:
            with open(file_path, 'w') as f:
                f.write(fixed_content)
            return len(issues)
        
        return 0
    
    def fix_content(self, content: str, issues: List[LintIssue]) -> str:
        """Apply fixes to content."""
        lines = content.split('\n')
        fixes_by_line = {}
        
        for issue in issues:
            if issue.fixable and issue.rule_name in self.rules:
                rule = self.rules[issue.rule_name]
                line_idx = issue.line_number - 1
                if line_idx < len(lines):
                    if line_idx not in fixes_by_line:
                        fixes_by_line[line_idx] = rule.fix(lines[line_idx]) if callable(rule.fix) else lines[line_idx]
        
        for line_idx, fixed_line in fixes_by_line.items():
            lines[line_idx] = fixed_line
        
        return '\n'.join(lines)
    
    # Helper methods for rule checks
    def _check_type_name_pascal_case(self, line: str) -> bool:
        """Check if type name uses PascalCase."""
        match = re.search(r'\b(type|agent|enum)\s+(\w+)', line, re.IGNORECASE)
        if match:
            name = match.group(2)
            return not (name[0].isupper() and '_' not in name)
        return False
    
    def _check_field_name_snake_case(self, line: str) -> bool:
        """Check if field name uses snake_case."""
        match = re.search(r'(\w+)\s*:', line)
        if match:
            name = match.group(1)
            return '_' in name and not name.islower()
        return False
    
    def _check_enum_value_lowercase(self, line: str) -> bool:
        """Check if enum value uses lowercase."""
        match = re.search(r'^\s*(\w+)\s*$', line)
        if match:
            value = match.group(1)
            return not value.islower()
        return False
    
    def _check_type_description(self, line: str, line_num: int) -> bool:
        """Check if type has description."""
        return line.strip().startswith(('type ', 'agent ', 'enum '))
    
    def _check_field_description(self, line: str, line_num: int) -> bool:
        """Check if field has description."""
        return ':' in line and '#' not in line
    
    def _check_import_order(self, line: str, line_num: int) -> bool:
        """Check if imports are ordered."""
        return False  # Handled in lint_content_with_ast
    
    def _check_unused_import(self, line: str, line_num: int) -> bool:
        """Check if import is unused."""
        return False  # Handled in lint_content_with_ast
    
    def _check_duplicate_field(self, line: str, line_num: int) -> bool:
        """Check for duplicate fields."""
        return False  # Handled in lint_content_with_ast
    
    def _check_required_fields(self, line: str, line_num: int) -> bool:
        """Check for required fields."""
        return False  # Handled in lint_content_with_ast
    
    def _extract_type_name(self, line: str) -> str:
        """Extract type name from line."""
        match = re.search(r'\b(type|agent|enum)\s+(\w+)', line, re.IGNORECASE)
        return match.group(2) if match else ''
    
    def _extract_field_name(self, line: str) -> str:
        """Extract field name from line."""
        match = re.search(r'(\w+)\s*:', line)
        return match.group(1) if match else ''
    
    def _extract_enum_value(self, line: str) -> str:
        """Extract enum value from line."""
        match = re.search(r'^\s*(\w+)\s*$', line)
        return match.group(1) if match else ''

    def _parse_suppression_comments(self, content: str) -> List[Suppression]:
        """Parse suppression comments from content.

        Supports three suppression types:
        - # adl-disable-next-line rule-name (suppresses next line only)
        - # adl-disable-line rule-name (suppresses current line only)
        - # adl-disable rule-name (suppresses entire file)

        Returns:
            List of Suppression objects
        """
        suppressions = []
        lines = content.split('\n')

        for line_num, line in enumerate(lines, 1):
            # Check for suppression comments
            if '# adl-disable' in line:
                # Extract rule name(s)
                match = re.search(r'#\s*adl-disable(?:-(next-line|line))?\s+([\w-]+)', line)
                if match:
                    scope = match.group(1) or 'file'
                    rule_name = match.group(2)

                    # Validate scope
                    if scope not in ('next-line', 'line', 'file'):
                        continue

                    suppressions.append(Suppression(
                        rule_name=rule_name,
                        line_number=line_num,
                        scope=scope,
                        source_line=line.strip()
                    ))

        return suppressions

    def load_rules_from_file(self, file_path: Union[str, Path]) -> List[LintRule]:
        """Load custom rules from a Python file.

        Args:
            file_path: Path to Python file containing rule definitions

        Returns:
            List of loaded LintRule objects

        Raises:
            FileNotFoundError: If file doesn't exist
            ImportError: If file can't be imported
        """
        file_path = Path(file_path)

        if not file_path.exists():
            raise FileNotFoundError(f"Rule file not found: {file_path}")

        # Load module from file
        spec = importlib.util.spec_from_file_location("custom_rules", file_path)
        if spec is None or spec.loader is None:
            raise ImportError(f"Cannot load module from: {file_path}")

        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        # Find and load rules from module
        rules = []
        for attr_name in dir(module):
            attr = getattr(module, attr_name)
            if isinstance(attr, LintRule):
                rules.append(attr)

        return rules

    def load_rules_from_dict(self, rules_config: Union[Dict, List[Dict]]) -> List[LintRule]:
        """Load custom rules from a dictionary or list of dictionaries.

        Args:
            rules_config: Dictionary or list of rule configurations

        Returns:
            List of loaded LintRule objects

        Example:
            rules_config = [
                {
                    'name': 'no-todos',
                    'description': 'No TODO comments allowed',
                    'severity': 'warning',
                    'check': lambda line, line_num: 'TODO' in line,
                    'message': 'Remove TODO comment'
                }
            ]
        """
        rules = []

        if isinstance(rules_config, dict):
            rules_config = [rules_config]

        for rule_config in rules_config:
            # Validate required fields
            if 'name' not in rule_config or 'check' not in rule_config:
                raise ValueError(f"Rule config missing required fields: {rule_config}")

            # Create LintRule from config
            rule = LintRule(
                name=rule_config['name'],
                description=rule_config.get('description', ''),
                severity=rule_config.get('severity', 'warning'),
                check=rule_config['check'],
                fix=rule_config.get('fix'),
                message=rule_config.get('message', rule_config['name'])
            )

            rules.append(rule)

        return rules

    def load_rules_from_module(self, module_name: str) -> List[LintRule]:
        """Load custom rules from a Python module.

        Args:
            module_name: Name of Python module (e.g., 'my_rules')

        Returns:
            List of loaded LintRule objects

        Raises:
            ImportError: If module can't be imported
        """
        try:
            module = importlib.import_module(module_name)
        except ImportError as e:
            raise ImportError(f"Cannot import module: {module_name}") from e

        # Find and load rules from module
        rules = []
        for attr_name in dir(module):
            attr = getattr(module, attr_name)
            if isinstance(attr, LintRule):
                rules.append(attr)

        return rules

    def load_rules_from_json(self, file_path: Union[str, Path]) -> List[LintRule]:
        """Load custom rules from a JSON file.

        Args:
            file_path: Path to JSON file containing rule configurations

        Returns:
            List of loaded LintRule objects

        Example JSON format:
            [
                {
                    "name": "no-todos",
                    "description": "No TODO comments allowed",
                    "severity": "warning",
                    "check": "lambda line, line_num: 'TODO' in line",
                    "message": "Remove TODO comment"
                }
            ]
        """
        file_path = Path(file_path)

        if not file_path.exists():
            raise FileNotFoundError(f"Rule file not found: {file_path}")

        with open(file_path, 'r') as f:
            rules_config = json.load(f)

        return self.load_rules_from_dict(rules_config)

    def load_rules_from_yaml(self, file_path: Union[str, Path]) -> List[LintRule]:
        """Load custom rules from a YAML file.

        Args:
            file_path: Path to YAML file containing rule configurations

        Returns:
            List of loaded LintRule objects

        Example YAML format:
            - name: no-todos
              description: No TODO comments allowed
              severity: warning
              check: "lambda line, line_num: 'TODO' in line"
              message: Remove TODO comment
        """
        file_path = Path(file_path)

        if not file_path.exists():
            raise FileNotFoundError(f"Rule file not found: {file_path}")

        with open(file_path, 'r') as f:
            rules_config = yaml.safe_load(f)

        return self.load_rules_from_dict(rules_config)
