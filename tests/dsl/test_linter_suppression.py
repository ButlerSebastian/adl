"""Test rule suppression and custom rule plugin support."""

import pytest
from pathlib import Path
from tools.dsl.linter import ADLLinter, LintRule, Suppression


class TestRuleSuppression:
    """Test rule suppression functionality."""

    def test_parse_suppression_next_line(self):
        """Test parsing # adl-disable-next-line suppression."""
        linter = ADLLinter()
        content = """type myType {
  # adl-disable-next-line type-name-pascal-case
  myField: string
}"""

        suppressions = linter._parse_suppression_comments(content)

        assert len(suppressions) == 1
        assert suppressions[0].rule_name == 'type-name-pascal-case'
        assert suppressions[0].line_number == 2
        assert suppressions[0].scope == 'next-line'

    def test_parse_suppression_line(self):
        """Test parsing # adl-disable-line suppression."""
        linter = ADLLinter()
        content = """type myType {
  # adl-disable-line field-name-snake-case
  myField: string
}"""

        suppressions = linter._parse_suppression_comments(content)

        assert len(suppressions) == 1
        assert suppressions[0].rule_name == 'field-name-snake-case'
        assert suppressions[0].line_number == 2
        assert suppressions[0].scope == 'line'

    def test_parse_suppression_file(self):
        """Test parsing # adl-disable suppression."""
        linter = ADLLinter()
        content = """# adl-disable max-line-length
type myType {
  myField: string
}"""

        suppressions = linter._parse_suppression_comments(content)

        assert len(suppressions) == 1
        assert suppressions[0].rule_name == 'max-line-length'
        assert suppressions[0].line_number == 1
        assert suppressions[0].scope == 'file'

    def test_parse_suppression_multiple_rules(self):
        """Test parsing multiple suppression directives."""
        linter = ADLLinter()
        content = """# adl-disable type-name-pascal-case
# adl-disable-next-line field-name-snake-case
type myType {
  # adl-disable-line duplicate-field
  myField: string
}"""

        suppressions = linter._parse_suppression_comments(content)

        assert len(suppressions) == 3
        assert suppressions[0].rule_name == 'type-name-pascal-case'
        assert suppressions[0].scope == 'file'
        assert suppressions[1].rule_name == 'field-name-snake-case'
        assert suppressions[1].scope == 'next-line'
        assert suppressions[2].rule_name == 'duplicate-field'
        assert suppressions[2].scope == 'line'

    def test_suppress_next_line(self):
        """Test that next-line suppression works."""
        linter = ADLLinter()
        content = """type myType {
  # adl-disable-next-line type-name-pascal-case
  myField: string
}"""

        issues = linter.lint_content(content)

        # Should not have type-name-pascal-case issue
        type_name_issues = [i for i in issues if i.rule_name == 'type-name-pascal-case']
        assert len(type_name_issues) == 0

    def test_suppress_line(self):
        """Test that line suppression works."""
        linter = ADLLinter()
        content = """type myType {
  # adl-disable-line field-name-snake-case
  myField: string
}"""

        issues = linter.lint_content(content)

        # Should not have field-name-snake-case issue
        field_name_issues = [i for i in issues if i.rule_name == 'field-name-snake-case']
        assert len(field_name_issues) == 0

    def test_suppress_file(self):
        """Test that file suppression works."""
        linter = ADLLinter()
        content = """# adl-disable max-line-length
type myType {
  myField: string
}"""

        issues = linter.lint_content(content)

        # Should not have max-line-length issue
        max_line_issues = [i for i in issues if i.rule_name == 'max-line-length']
        assert len(max_line_issues) == 0

    def test_suppress_multiple_rules(self):
        """Test suppressing multiple rules."""
        linter = ADLLinter()
        content = """# adl-disable type-name-pascal-case
# adl-disable-next-line field-name-snake-case
type myType {
  # adl-disable-line duplicate-field
  myField: string
}"""

        issues = linter.lint_content(content)

        # Should not have suppressed issues
        type_name_issues = [i for i in issues if i.rule_name == 'type-name-pascal-case']
        field_name_issues = [i for i in issues if i.rule_name == 'field-name-snake-case']
        duplicate_field_issues = [i for i in issues if i.rule_name == 'duplicate-field']

        assert len(type_name_issues) == 0
        assert len(field_name_issues) == 0
        assert len(duplicate_field_issues) == 0


class TestCustomRulePlugins:
    """Test custom rule plugin support."""

    def test_load_rules_from_dict(self):
        """Test loading rules from dictionary."""
        linter = ADLLinter()

        rules_config = [
            {
                'name': 'no-todos',
                'description': 'No TODO comments allowed',
                'severity': 'warning',
                'check': lambda line, line_num: 'TODO' in line,
                'message': 'Remove TODO comment'
            }
        ]

        rules = linter.load_rules_from_dict(rules_config)

        assert len(rules) == 1
        assert rules[0].name == 'no-todos'
        assert rules[0].description == 'No TODO comments allowed'
        assert rules[0].severity == 'warning'
        assert rules[0].check('TODO comment', 1) == True
        assert rules[0].message == 'Remove TODO comment'

    def test_load_rules_from_dict_invalid(self):
        """Test loading rules from dictionary with missing fields."""
        linter = ADLLinter()

        rules_config = [
            {
                'name': 'invalid-rule',
                # Missing 'check' field
            }
        ]

        with pytest.raises(ValueError):
            linter.load_rules_from_dict(rules_config)

    def test_load_rules_from_file(self, tmp_path):
        """Test loading rules from Python file."""
        linter = ADLLinter()

        # Create a custom rules file
        rules_file = tmp_path / 'custom_rules.py'
        rules_file.write_text('''
from tools.dsl.linter import LintRule

def custom_check(line, line_num):
    return 'TODO' in line

custom_rule = LintRule(
    name='no-todos',
    description='No TODO comments allowed',
    severity='warning',
    check=custom_check,
    message="Remove TODO comment"
)
''')

        rules = linter.load_rules_from_file(rules_file)

        assert len(rules) == 1
        assert rules[0].name == 'no-todos'
        assert rules[0].description == 'No TODO comments allowed'
        assert rules[0].severity == 'warning'

    def test_load_rules_from_file_not_found(self, tmp_path):
        """Test loading rules from non-existent file."""
        linter = ADLLinter()

        rules_file = tmp_path / 'nonexistent.py'

        with pytest.raises(FileNotFoundError):
            linter.load_rules_from_file(rules_file)

    def test_load_rules_from_json(self, tmp_path):
        """Test loading rules from JSON file."""
        linter = ADLLinter()

        # Create a JSON rules file
        rules_file = tmp_path / 'rules.json'
        rules_file.write_text('''
[
    {
        "name": "no-todos",
        "description": "No TODO comments allowed",
        "severity": "warning",
        "check": "lambda line, line_num: 'TODO' in line",
        "message": "Remove TODO comment"
    }
]
''')

        rules = linter.load_rules_from_json(rules_file)

        assert len(rules) == 1
        assert rules[0].name == 'no-todos'
        assert rules[0].description == 'No TODO comments allowed'
        assert rules[0].severity == 'warning'

    def test_load_rules_from_yaml(self, tmp_path):
        """Test loading rules from YAML file."""
        linter = ADLLinter()

        # Create a YAML rules file
        rules_file = tmp_path / 'rules.yaml'
        rules_file.write_text('''
- name: no-todos
  description: No TODO comments allowed
  severity: warning
  check: "lambda line, line_num: 'TODO' in line"
  message: Remove TODO comment
''')

        rules = linter.load_rules_from_yaml(rules_file)

        assert len(rules) == 1
        assert rules[0].name == 'no-todos'
        assert rules[0].description == 'No TODO comments allowed'
        assert rules[0].severity == 'warning'

    def test_load_rules_from_module(self):
        """Test loading rules from Python module."""
        linter = ADLLinter()

        # Create a temporary module
        import sys
        import tempfile
        import importlib.util

        with tempfile.TemporaryDirectory() as tmpdir:
            module_path = Path(tmpdir) / 'test_module.py'
            module_path.write_text('''
from tools.dsl.linter import LintRule

def custom_check(line, line_num):
    return 'TODO' in line

custom_rule = LintRule(
    name='no-todos',
    description='No TODO comments allowed',
    severity='warning',
    check=custom_check,
    message="Remove TODO comment"
)
''')

            # Add tmpdir to sys.path
            sys.path.insert(0, tmpdir)

            try:
                rules = linter.load_rules_from_module('test_module')

                assert len(rules) == 1
                assert rules[0].name == 'no-todos'
                assert rules[0].description == 'No TODO comments allowed'
                assert rules[0].severity == 'warning'
            finally:
                sys.path.remove(tmpdir)

    def test_load_rules_from_module_not_found(self):
        """Test loading rules from non-existent module."""
        linter = ADLLinter()

        with pytest.raises(ImportError):
            linter.load_rules_from_module('nonexistent_module')


class TestSuppressionDataclass:
    """Test Suppression dataclass."""

    def test_suppression_creation(self):
        """Test creating Suppression objects."""
        suppression = Suppression(
            rule_name='test-rule',
            line_number=1,
            scope='next-line',
            source_line='# adl-disable-next-line test-rule'
        )

        assert suppression.rule_name == 'test-rule'
        assert suppression.line_number == 1
        assert suppression.scope == 'next-line'
        assert suppression.source_line == '# adl-disable-next-line test-rule'

    def test_suppression_scopes(self):
        """Test all valid suppression scopes."""
        for scope in ['next-line', 'line', 'file']:
            suppression = Suppression(
                rule_name='test-rule',
                line_number=1,
                scope=scope,
                source_line=f'# adl-disable-{scope} test-rule'
            )
            assert suppression.scope == scope


if __name__ == '__main__':
    pytest.main([__file__, '-v'])