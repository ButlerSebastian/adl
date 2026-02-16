"""
Comprehensive test suite for ADL DSL Linter

Tests all linting rules, autofix functionality, rule enable/disable,
and severity filtering for the ADL DSL linter.
"""

import unittest
from pathlib import Path
from tools.dsl.linter import ADLLinter, LintIssue


class TestTypeNamePascalCase(unittest.TestCase):
    """Test type name PascalCase validation."""

    def setUp(self):
        """Set up test fixtures."""
        self.linter = ADLLinter()

    def test_valid_pascal_case(self):
        """Test valid PascalCase type names."""
        content = """
type Person {
  name: string
  age: integer
}

type UserProfile {
  id: string
  email: string
}
"""
        issues = self.linter.lint_content(content)
        pascal_case_issues = [i for i in issues if i.rule_name == 'type-name-pascal-case']
        self.assertEqual(len(pascal_case_issues), 0, "Valid PascalCase should not trigger issues")

    def test_invalid_snake_case(self):
        """Test invalid snake_case type names."""
        content = """
type person_name {
  name: string
}

type user_profile {
  email: string
}
"""
        issues = self.linter.lint_content(content)
        pascal_case_issues = [i for i in issues if i.rule_name == 'type-name-pascal-case']
        self.assertGreater(len(pascal_case_issues), 0, "Snake_case should trigger issues")

    def test_invalid_camel_case(self):
        """Test invalid camelCase type names."""
        content = """
type personName {
  name: string
}

type userProfile {
  email: string
}
"""
        issues = self.linter.lint_content(content)
        pascal_case_issues = [i for i in issues if i.rule_name == 'type-name-pascal-case']
        self.assertGreater(len(pascal_case_issues), 0, "camelCase should trigger issues")

    def test_valid_agent_name(self):
        """Test valid PascalCase agent names."""
        content = """
agent UserProfileAgent {
  id: string
  name: string
}
"""
        issues = self.linter.lint_content(content)
        pascal_case_issues = [i for i in issues if i.rule_name == 'type-name-pascal-case']
        self.assertEqual(len(pascal_case_issues), 0, "Valid PascalCase agent should not trigger issues")

    def test_valid_enum_name(self):
        """Test valid PascalCase enum names."""
        content = """
enum UserStatus {
  active
  inactive
}
"""
        issues = self.linter.lint_content(content)
        pascal_case_issues = [i for i in issues if i.rule_name == 'type-name-pascal-case']
        self.assertEqual(len(pascal_case_issues), 0, "Valid PascalCase enum should not trigger issues")


class TestFieldNameSnakeCase(unittest.TestCase):
    """Test field name snake_case validation."""

    def setUp(self):
        """Set up test fixtures."""
        self.linter = ADLLinter()

    def test_valid_snake_case(self):
        """Test valid snake_case field names."""
        content = """
type Person {
  first_name: string
  last_name: string
  age_in_years: integer
}
"""
        issues = self.linter.lint_content(content)
        snake_case_issues = [i for i in issues if i.rule_name == 'field-name-snake-case']
        self.assertEqual(len(snake_case_issues), 0, "Valid snake_case should not trigger issues")

    def test_invalid_camel_case(self):
        """Test invalid camelCase field names."""
        content = """
type Person {
  firstName: string
  lastName: string
  ageInYears: integer
}
"""
        issues = self.linter.lint_content(content)
        snake_case_issues = [i for i in issues if i.rule_name == 'field-name-snake-case']
        self.assertGreater(len(snake_case_issues), 0, "camelCase should trigger issues")

    def test_invalid_pascal_case(self):
        """Test invalid PascalCase field names."""
        content = """
type Person {
  FirstName: string
  LastName: string
  AgeInYears: integer
}
"""
        issues = self.linter.lint_content(content)
        snake_case_issues = [i for i in issues if i.rule_name == 'field-name-snake-case']
        self.assertGreater(len(snake_case_issues), 0, "PascalCase should trigger issues")

    def test_valid_with_optional(self):
        """Test valid snake_case with optional fields."""
        content = """
type Person {
  first_name: string
  last_name?: string
  age_in_years?: integer
}
"""
        issues = self.linter.lint_content(content)
        snake_case_issues = [i for i in issues if i.rule_name == 'field-name-snake-case']
        self.assertEqual(len(snake_case_issues), 0, "Valid snake_case with optional should not trigger issues")


class TestEnumValueLowercase(unittest.TestCase):
    """Test enum value lowercase validation."""

    def setUp(self):
        """Set up test fixtures."""
        self.linter = ADLLinter()

    def test_valid_lowercase(self):
        """Test valid lowercase enum values."""
        content = """
enum UserStatus {
  active
  inactive
  pending
  deleted
}
"""
        issues = self.linter.lint_content(content)
        lowercase_issues = [i for i in issues if i.rule_name == 'enum-value-lowercase']
        self.assertEqual(len(lowercase_issues), 0, "Valid lowercase should not trigger issues")

    def test_invalid_uppercase(self):
        """Test invalid uppercase enum values."""
        content = """
enum UserStatus {
  Active
  Inactive
  Pending
  Deleted
}
"""
        issues = self.linter.lint_content(content)
        lowercase_issues = [i for i in issues if i.rule_name == 'enum-value-lowercase']
        self.assertGreater(len(lowercase_issues), 0, "Uppercase should trigger issues")

    def test_invalid_mixed_case(self):
        """Test invalid mixed case enum values."""
        content = """
enum UserStatus {
  Active
  inactive
  Pending
  deleted
}
"""
        issues = self.linter.lint_content(content)
        lowercase_issues = [i for i in issues if i.rule_name == 'enum-value-lowercase']
        self.assertGreater(len(lowercase_issues), 0, "Mixed case should trigger issues")

    def test_valid_with_description(self):
        """Test valid lowercase enum values with descriptions."""
        content = """
enum UserStatus {
  active "User is active"
  inactive "User is inactive"
}
"""
        issues = self.linter.lint_content(content)
        lowercase_issues = [i for i in issues if i.rule_name == 'enum-value-lowercase']
        self.assertEqual(len(lowercase_issues), 0, "Valid lowercase with description should not trigger issues")


class TestTypeDescription(unittest.TestCase):
    """Test type description validation."""

    def setUp(self):
        """Set up test fixtures."""
        self.linter = ADLLinter()

    def test_type_with_description(self):
        """Test type with description comment."""
        content = """
# Represents a person in the system
type Person {
  name: string
  age: integer
}
"""
        issues = self.linter.lint_content(content)
        desc_issues = [i for i in issues if i.rule_name == 'missing-type-description']
        self.assertEqual(len(desc_issues), 0, "Type with description should not trigger issues")

    def test_type_without_description(self):
        """Test type without description comment."""
        content = """
type Person {
  name: string
  age: integer
}
"""
        issues = self.linter.lint_content(content)
        desc_issues = [i for i in issues if i.rule_name == 'missing-type-description']
        self.assertGreater(len(desc_issues), 0, "Type without description should trigger issues")

    def test_agent_with_description(self):
        """Test agent with description comment."""
        content = """
# Agent for processing user requests
agent RequestProcessor {
  id: string
  name: string
}
"""
        issues = self.linter.lint_content(content)
        desc_issues = [i for i in issues if i.rule_name == 'missing-type-description']
        self.assertEqual(len(desc_issues), 0, "Agent with description should not trigger issues")

    def test_enum_with_description(self):
        """Test enum with description comment."""
        content = """
# Possible states of a user account
enum UserStatus {
  active
  inactive
}
"""
        issues = self.linter.lint_content(content)
        desc_issues = [i for i in issues if i.rule_name == 'missing-type-description']
        self.assertEqual(len(desc_issues), 0, "Enum with description should not trigger issues")


class TestFieldDescription(unittest.TestCase):
    """Test field description validation."""

    def setUp(self):
        """Set up test fixtures."""
        self.linter = ADLLinter()

    def test_field_with_description(self):
        """Test field with description comment."""
        content = """
type Person {
  name: string "Full name of the person"
  age: integer "Age in years"
}
"""
        issues = self.linter.lint_content(content)
        desc_issues = [i for i in issues if i.rule_name == 'missing-field-description']
        self.assertEqual(len(desc_issues), 0, "Field with description should not trigger issues")

    def test_field_without_description(self):
        """Test field without description comment."""
        content = """
type Person {
  name: string
  age: integer
}
"""
        issues = self.linter.lint_content(content)
        desc_issues = [i for i in issues if i.rule_name == 'missing-field-description']
        self.assertGreater(len(desc_issues), 0, "Field without description should trigger issues")

    def test_field_with_inline_description(self):
        """Test field with inline description."""
        content = """
type Person {
  name: string # Full name
  age: integer # Age in years
}
"""
        issues = self.linter.lint_content(content)
        desc_issues = [i for i in issues if i.rule_name == 'missing-field-description']
        self.assertEqual(len(desc_issues), 0, "Field with inline description should not trigger issues")


class TestImportOrder(unittest.TestCase):
    """Test import order validation."""

    def setUp(self):
        """Set up test fixtures."""
        self.linter = ADLLinter()

    def test_alphabetical_order(self):
        """Test imports in alphabetical order."""
        content = """
import schema.components.memory
import schema.components.rag
import schema.components.tool as tools
import schema.components.utils
"""
        issues = self.linter.lint_content(content)
        import_order_issues = [i for i in issues if i.rule_name == 'import-order']
        self.assertEqual(len(import_order_issues), 0, "Alphabetical imports should not trigger issues")

    def test_non_alphabetical_order(self):
        """Test imports not in alphabetical order."""
        content = """
import schema.components.rag
import schema.components.memory
import schema.components.tool as tools
"""
        issues = self.linter.lint_content(content)
        import_order_issues = [i for i in issues if i.rule_name == 'import-order']
        self.assertGreater(len(import_order_issues), 0, "Non-alphabetical imports should trigger issues")

    def test_mixed_with_types(self):
        """Test import order with type definitions."""
        content = """
import schema.components.memory
import schema.components.rag

type Person {
  name: string
}
"""
        issues = self.linter.lint_content(content)
        import_order_issues = [i for i in issues if i.rule_name == 'import-order']
        self.assertEqual(len(import_order_issues), 0, "Alphabetical imports with types should not trigger issues")


class TestUnusedImport(unittest.TestCase):
    """Test unused import detection."""

    def setUp(self):
        """Set up test fixtures."""
        self.linter = ADLLinter()

    def test_unused_import(self):
        """Test detection of unused imports."""
        content = """
import schema.components.memory
import schema.components.rag

type Person {
  name: string
}
"""
        issues = self.linter.lint_content(content)
        unused_issues = [i for i in issues if i.rule_name == 'unused-import']
        self.assertGreater(len(unused_issues), 0, "Unused import should trigger issues")

    def test_used_import(self):
        """Test that used imports don't trigger issues."""
        content = """
import schema.components.memory

type MemoryConfig {
  type: string
}
"""
        issues = self.linter.lint_content(content)
        unused_issues = [i for i in issues if i.rule_name == 'unused-import']
        self.assertEqual(len(unused_issues), 0, "Used import should not trigger issues")

    def test_import_used_in_type(self):
        """Test import used in type definition."""
        content = """
import schema.components.memory

type MemoryConfig {
  type: string
  scope: string
}
"""
        issues = self.linter.lint_content(content)
        unused_issues = [i for i in issues if i.rule_name == 'unused-import']
        self.assertEqual(len(unused_issues), 0, "Import used in type should not trigger issues")


class TestTrailingWhitespace(unittest.TestCase):
    """Test trailing whitespace detection."""

    def setUp(self):
        """Set up test fixtures."""
        self.linter = ADLLinter()

    def test_no_trailing_whitespace(self):
        """Test file without trailing whitespace."""
        content = """
type Person {
  name: string
  age: integer
}
"""
        issues = self.linter.lint_content(content)
        trailing_issues = [i for i in issues if i.rule_name == 'trailing-whitespace']
        self.assertEqual(len(trailing_issues), 0, "No trailing whitespace should not trigger issues")

    def test_trailing_whitespace(self):
        """Test detection of trailing whitespace."""
        content = """
type Person {
  name: string  
  age: integer  
}
"""
        issues = self.linter.lint_content(content)
        trailing_issues = [i for i in issues if i.rule_name == 'trailing-whitespace']
        self.assertGreater(len(trailing_issues), 0, "Trailing whitespace should trigger issues")

    def test_trailing_whitespace_in_empty_line(self):
        """Test trailing whitespace in empty line."""
        content = """
type Person {
  name: string
  

  age: integer
}
"""
        issues = self.linter.lint_content(content)
        trailing_issues = [i for i in issues if i.rule_name == 'trailing-whitespace']
        self.assertGreater(len(trailing_issues), 0, "Trailing whitespace in empty line should trigger issues")


class TestNoTabs(unittest.TestCase):
    """Test tab detection."""

    def setUp(self):
        """Set up test fixtures."""
        self.linter = ADLLinter()

    def test_no_tabs(self):
        """Test file without tabs."""
        content = """
type Person {
  name: string
  age: integer
}
"""
        issues = self.linter.lint_content(content)
        tab_issues = [i for i in issues if i.rule_name == 'no-tabs']
        self.assertEqual(len(tab_issues), 0, "No tabs should not trigger issues")

    def test_tabs_detected(self):
        """Test detection of tabs."""
        content = "\ttype Person {\n\t  name: string\n\t  age: integer\n\t}\n"
        issues = self.linter.lint_content(content)
        tab_issues = [i for i in issues if i.rule_name == 'no-tabs']
        self.assertGreater(len(tab_issues), 0, "Tabs should trigger issues")

    def test_tabs_in_field(self):
        """Test tabs in field definitions."""
        content = """
type Person {
\tname: string
\tage: integer
}
"""
        issues = self.linter.lint_content(content)
        tab_issues = [i for i in issues if i.rule_name == 'no-tabs']
        self.assertGreater(len(tab_issues), 0, "Tabs in fields should trigger issues")


class TestMaxLineLength(unittest.TestCase):
    """Test max line length validation."""

    def setUp(self):
        """Set up test fixtures."""
        self.linter = ADLLinter()

    def test_lines_within_limit(self):
        """Test lines within 100 character limit."""
        content = """
type Person {
  name: string
  age: integer
  email: string
}
"""
        issues = self.linter.lint_content(content)
        length_issues = [i for i in issues if i.rule_name == 'max-line-length']
        self.assertEqual(len(length_issues), 0, "Lines within limit should not trigger issues")

    def test_lines_exceeding_limit(self):
        """Test lines exceeding 100 character limit."""
        content = """
type Person {
  name: string
  very_long_field_name_that_exceeds_the_maximum_allowed_line_length_of_100_characters: string
  age: integer
}
"""
        issues = self.linter.lint_content(content)
        length_issues = [i for i in issues if i.rule_name == 'max-line-length']
        self.assertGreater(len(length_issues), 0, "Lines exceeding limit should trigger issues")

    def test_import_exceeding_limit(self):
        """Test import lines exceeding limit."""
        content = """
import schema.components.very_long_module_name_that_exceeds_the_maximum_allowed_line_length_of_100_characters
"""
        issues = self.linter.lint_content(content)
        length_issues = [i for i in issues if i.rule_name == 'max-line-length']
        self.assertGreater(len(length_issues), 0, "Import exceeding limit should trigger issues")


class TestEmptyLineWhitespace(unittest.TestCase):
    """Test empty line whitespace detection."""

    def setUp(self):
        """Set up test fixtures."""
        self.linter = ADLLinter()

    def test_empty_line_without_whitespace(self):
        """Test empty line without whitespace."""
        content = """
type Person {
  name: string

  age: integer
}
"""
        issues = self.linter.lint_content(content)
        whitespace_issues = [i for i in issues if i.rule_name == 'empty-line-with-whitespace']
        self.assertEqual(len(whitespace_issues), 0, "Empty line without whitespace should not trigger issues")

    def test_empty_line_with_whitespace(self):
        """Test empty line with whitespace."""
        content = """
type Person {
  name: string
    age: integer
}
"""
        issues = self.linter.lint_content(content)
        whitespace_issues = [i for i in issues if i.rule_name == 'empty-line-with-whitespace']
        self.assertGreater(len(whitespace_issues), 0, "Empty line with whitespace should trigger issues")

    def test_multiple_empty_lines(self):
        """Test multiple empty lines with whitespace."""
        content = """
type Person {
  name: string
  

  
  age: integer
}
"""
        issues = self.linter.lint_content(content)
        whitespace_issues = [i for i in issues if i.rule_name == 'empty-line-with-whitespace']
        self.assertGreater(len(whitespace_issues), 0, "Multiple empty lines with whitespace should trigger issues")


class TestDuplicateField(unittest.TestCase):
    """Test duplicate field detection."""

    def setUp(self):
        """Set up test fixtures."""
        self.linter = ADLLinter()

    def test_no_duplicate_fields(self):
        """Test file without duplicate fields."""
        content = """
type Person {
  name: string
  age: integer
}
"""
        issues = self.linter.lint_content(content)
        duplicate_issues = [i for i in issues if i.rule_name == 'duplicate-field']
        self.assertEqual(len(duplicate_issues), 0, "No duplicate fields should not trigger issues")

    def test_duplicate_fields_detected(self):
        """Test detection of duplicate fields."""
        content = """
type Person {
  name: string
  age: integer
  name: string
}
"""
        issues = self.linter.lint_content(content)
        duplicate_issues = [i for i in issues if i.rule_name == 'duplicate-field']
        self.assertGreater(len(duplicate_issues), 0, "Duplicate fields should trigger issues")

    def test_duplicate_in_agent(self):
        """Test duplicate fields in agent."""
        content = """
agent TestAgent {
  id: string
  name: string
  name: string
}
"""
        issues = self.linter.lint_content(content)
        duplicate_issues = [i for i in issues if i.rule_name == 'duplicate-field']
        self.assertGreater(len(duplicate_issues), 0, "Duplicate fields in agent should trigger issues")

    def test_duplicate_in_enum(self):
        """Test duplicate enum values."""
        content = """
enum UserStatus {
  active
  inactive
  active
}
"""
        issues = self.linter.lint_content(content)
        duplicate_issues = [i for i in issues if i.rule_name == 'duplicate-field']
        self.assertGreater(len(duplicate_issues), 0, "Duplicate enum values should trigger issues")


class TestRequiredFields(unittest.TestCase):
    """Test required fields validation."""

    def setUp(self):
        """Set up test fixtures."""
        self.linter = ADLLinter()

    def test_type_with_fields(self):
        """Test type with at least one field."""
        content = """
type Person {
  name: string
}
"""
        issues = self.linter.lint_content(content)
        required_issues = [i for i in issues if i.rule_name == 'missing-required-fields']
        self.assertEqual(len(required_issues), 0, "Type with fields should not trigger issues")

    def test_empty_type(self):
        """Test empty type without fields."""
        content = """
type Person {
}
"""
        issues = self.linter.lint_content(content)
        required_issues = [i for i in issues if i.rule_name == 'missing-required-fields']
        self.assertGreater(len(required_issues), 0, "Empty type should trigger issues")

    def test_empty_agent(self):
        """Test empty agent without fields."""
        content = """
agent TestAgent {
}
"""
        issues = self.linter.lint_content(content)
        required_issues = [i for i in issues if i.rule_name == 'missing-required-fields']
        self.assertGreater(len(required_issues), 0, "Empty agent should trigger issues")

    def test_agent_with_fields(self):
        """Test agent with at least one field."""
        content = """
agent TestAgent {
  id: string
}
"""
        issues = self.linter.lint_content(content)
        required_issues = [i for i in issues if i.rule_name == 'missing-required-fields']
        self.assertEqual(len(required_issues), 0, "Agent with fields should not trigger issues")


class TestRuleEnableDisable(unittest.TestCase):
    """Test rule enable and disable functionality."""

    def setUp(self):
        """Set up test fixtures."""
        self.linter = ADLLinter()

    def test_enable_specific_rule(self):
        """Test enabling a specific rule."""
        self.linter.enable_rule('type-name-pascal-case')
        content = """
type person_name {
  name: string
}
"""
        issues = self.linter.lint_content(content)
        pascal_case_issues = [i for i in issues if i.rule_name == 'type-name-pascal-case']
        self.assertGreater(len(pascal_case_issues), 0, "Enabled rule should trigger issues")

    def test_disable_specific_rule(self):
        """Test disabling a specific rule."""
        self.linter.disable_rule('type-name-pascal-case')
        content = """
type person_name {
  name: string
}
"""
        issues = self.linter.lint_content(content)
        pascal_case_issues = [i for i in issues if i.rule_name == 'type-name-pascal-case']
        self.assertEqual(len(pascal_case_issues), 0, "Disabled rule should not trigger issues")

    def test_enable_multiple_rules(self):
        """Test enabling multiple rules."""
        self.linter.enable_rule('type-name-pascal-case')
        self.linter.enable_rule('field-name-snake-case')
        content = """
type person_name {
  firstName: string
}
"""
        issues = self.linter.lint_content(content)
        pascal_case_issues = [i for i in issues if i.rule_name == 'type-name-pascal-case']
        snake_case_issues = [i for i in issues if i.rule_name == 'field-name-snake-case']
        self.assertGreater(len(pascal_case_issues), 0, "Enabled rule should trigger issues")
        self.assertGreater(len(snake_case_issues), 0, "Enabled rule should trigger issues")

    def test_disable_multiple_rules(self):
        """Test disabling multiple rules."""
        self.linter.disable_rule('type-name-pascal-case')
        self.linter.disable_rule('field-name-snake-case')
        content = """
type person_name {
  firstName: string
}
"""
        issues = self.linter.lint_content(content)
        pascal_case_issues = [i for i in issues if i.rule_name == 'type-name-pascal-case']
        snake_case_issues = [i for i in issues if i.rule_name == 'field-name-snake-case']
        self.assertEqual(len(pascal_case_issues), 0, "Disabled rule should not trigger issues")
        self.assertEqual(len(snake_case_issues), 0, "Disabled rule should not trigger issues")

    def test_enable_all_rules(self):
        """Test enabling all rules."""
        for rule_name in self.linter.rules.keys():
            self.linter.enable_rule(rule_name)
        content = """
type person_name {
  firstName: string
}
"""
        issues = self.linter.lint_content(content)
        self.assertGreater(len(issues), 0, "All enabled rules should trigger issues")

    def test_disable_all_rules(self):
        """Test disabling all rules."""
        for rule_name in self.linter.rules.keys():
            self.linter.disable_rule(rule_name)
        content = """
type person_name {
  firstName: string
}
"""
        issues = self.linter.lint_content(content)
        self.assertEqual(len(issues), 0, "All disabled rules should not trigger issues")


class TestSeverityFilter(unittest.TestCase):
    """Test severity filtering functionality."""

    def setUp(self):
        """Set up test fixtures."""
        self.linter = ADLLinter()

    def test_error_severity_filter(self):
        """Test filtering by error severity."""
        self.linter.set_severity_filter('error')
        content = """
type person_name {
  firstName: string
}
"""
        issues = self.linter.lint_content(content)
        error_issues = [i for i in issues if i.severity == 'error']
        self.assertGreater(len(error_issues), 0, "Error severity should be included")

    def test_warning_severity_filter(self):
        """Test filtering by warning severity."""
        self.linter.set_severity_filter('warning')
        content = """
type person_name {
  firstName: string
}
"""
        issues = self.linter.lint_content(content)
        warning_issues = [i for i in issues if i.severity == 'warning']
        self.assertGreater(len(warning_issues), 0, "Warning severity should be included")

    def test_info_severity_filter(self):
        """Test filtering by info severity."""
        self.linter.set_severity_filter('info')
        content = """
type person_name {
  firstName: string
}
"""
        issues = self.linter.lint_content(content)
        info_issues = [i for i in issues if i.severity == 'info']
        self.assertGreater(len(info_issues), 0, "Info severity should be included")

    def test_error_excludes_warning_and_info(self):
        """Test that error filter excludes warning and info."""
        self.linter.set_severity_filter('error')
        content = """
type person_name {
  firstName: string
}
"""
        issues = self.linter.lint_content(content)
        for issue in issues:
            self.assertEqual(issue.severity, 'error', "Only error severity should be included")

    def test_warning_excludes_info(self):
        """Test that warning filter excludes info."""
        self.linter.set_severity_filter('warning')
        content = """
type person_name {
  firstName: string
}
"""
        issues = self.linter.lint_content(content)
        for issue in issues:
            self.assertIn(issue.severity, ['error', 'warning'], "Error and warning should be included")

    def test_all_severities_included(self):
        """Test that all severities are included when no filter is set."""
        content = """
type person_name {
  firstName: string
}
"""
        issues = self.linter.lint_content(content)
        severity_types = set(issue.severity for issue in issues)
        self.assertIn('error', severity_types, "Error should be included")
        self.assertIn('warning', severity_types, "Warning should be included")
        self.assertIn('info', severity_types, "Info should be included")


class TestLintFile(unittest.TestCase):
    """Test lint_file method."""

    def setUp(self):
        """Set up test fixtures."""
        self.linter = ADLLinter()

    def test_lint_valid_file(self):
        """Test linting a valid file."""
        # Create a temporary file
        test_file = Path('/tmp/test_valid.adl')
        test_file.write_text("""
# Person type definition
type Person {
  first_name: string
  last_name: string
  age: integer
}

# User agent
agent UserAgent {
  id: string
  name: string
}
""")
        try:
            issues = self.linter.lint_file(test_file)
            self.assertIsInstance(issues, list, "lint_file should return a list")
            self.assertGreater(len(issues), 0, "Valid file should have some issues")
        finally:
            test_file.unlink()

    def test_lint_invalid_file(self):
        """Test linting an invalid file."""
        # Create a temporary file
        test_file = Path('/tmp/test_invalid.adl')
        test_file.write_text("""
type person_name {
  firstName: string
}
""")
        try:
            issues = self.linter.lint_file(test_file)
            self.assertIsInstance(issues, list, "lint_file should return a list")
            self.assertGreater(len(issues), 0, "Invalid file should have issues")
        finally:
            test_file.unlink()

    def test_lint_nonexistent_file(self):
        """Test linting a nonexistent file."""
        test_file = Path('/tmp/nonexistent_file.adl')
        issues = self.linter.lint_file(test_file)
        self.assertIsInstance(issues, list, "lint_file should return a list")
        self.assertEqual(len(issues), 0, "Nonexistent file should return no issues")


class TestLintContent(unittest.TestCase):
    """Test lint_content method."""

    def setUp(self):
        """Set up test fixtures."""
        self.linter = ADLLinter()

    def test_lint_valid_content(self):
        """Test linting valid content."""
        content = """
# Person type definition
type Person {
  first_name: string
  last_name: string
  age: integer
}
"""
        issues = self.linter.lint_content(content)
        self.assertIsInstance(issues, list, "lint_content should return a list")
        self.assertGreater(len(issues), 0, "Valid content should have some issues")

    def test_lint_invalid_content(self):
        """Test linting invalid content."""
        content = """
type person_name {
  firstName: string
}
"""
        issues = self.linter.lint_content(content)
        self.assertIsInstance(issues, list, "lint_content should return a list")
        self.assertGreater(len(issues), 0, "Invalid content should have issues")

    def test_lint_empty_content(self):
        """Test linting empty content."""
        content = ""
        issues = self.linter.lint_content(content)
        self.assertIsInstance(issues, list, "lint_content should return a list")
        self.assertEqual(len(issues), 0, "Empty content should return no issues")


class TestFixFile(unittest.TestCase):
    """Test fix_file method."""

    def setUp(self):
        """Set up test fixtures."""
        self.linter = ADLLinter()

    def test_fix_trailing_whitespace(self):
        """Test fixing trailing whitespace."""
        # Create a temporary file
        test_file = Path('/tmp/test_fix_whitespace.adl')
        test_file.write_text("""
type Person {
  name: string  
  age: integer  
}
""")
        try:
            content_before = test_file.read_text()
            issues = self.linter.lint_file(test_file)
            fixed_count = self.linter.fix_file(test_file, issues)
            content_after = test_file.read_text()
            self.assertGreater(fixed_count, 0, "Should fix some issues")
            self.assertNotEqual(content_before, content_after, "Content should change")
            self.assertNotIn('  ', content_after, "Trailing whitespace should be removed")
        finally:
            test_file.unlink()

    def test_fix_tabs(self):
        """Test fixing tabs."""
        # Create a temporary file
        test_file = Path('/tmp/test_fix_tabs.adl')
        test_file.write_text("\ttype Person {\n\t  name: string\n\t  age: integer\n\t}\n")
        try:
            content_before = test_file.read_text()
            issues = self.linter.lint_file(test_file)
            fixed_count = self.linter.fix_file(test_file, issues)
            content_after = test_file.read_text()
            self.assertGreater(fixed_count, 0, "Should fix some issues")
            self.assertNotEqual(content_before, content_after, "Content should change")
            self.assertNotIn('\t', content_after, "Tabs should be removed")
        finally:
            test_file.unlink()

    def test_fix_empty_line_whitespace(self):
        """Test fixing empty line whitespace."""
        # Create a temporary file
        test_file = Path('/tmp/test_fix_empty_line.adl')
        test_file.write_text("""
type Person {
  name: string
  

  age: integer
}
""")
        try:
            content_before = test_file.read_text()
            issues = self.linter.lint_file(test_file)
            fixed_count = self.linter.fix_file(test_file, issues)
            content_after = test_file.read_text()
            self.assertGreater(fixed_count, 0, "Should fix some issues")
            self.assertNotEqual(content_before, content_after, "Content should change")
        finally:
            test_file.unlink()

    def test_fix_no_fixable_issues(self):
        """Test fix_file with no fixable issues."""
        # Create a temporary file
        test_file = Path('/tmp/test_no_fix.adl')
        test_file.write_text("""
type Person {
  name: string
  age: integer
}
""")
        try:
            content_before = test_file.read_text()
            issues = self.linter.lint_file(test_file)
            fixed_count = self.linter.fix_file(test_file, issues)
            content_after = test_file.read_text()
            self.assertEqual(fixed_count, 0, "Should not fix any issues")
            self.assertEqual(content_before, content_after, "Content should not change")
        finally:
            test_file.unlink()


class TestFixContent(unittest.TestCase):
    """Test fix_content method."""

    def setUp(self):
        """Set up test fixtures."""
        self.linter = ADLLinter()

    def test_fix_trailing_whitespace_content(self):
        """Test fixing trailing whitespace in content."""
        content = """
type Person {
  name: string  
  age: integer  
}
"""
        issues = self.linter.lint_content(content)
        fixed_content = self.linter.fix_content(content, issues)
        self.assertNotIn('  ', fixed_content, "Trailing whitespace should be removed")
        self.assertNotEqual(content, fixed_content, "Content should change")

    def test_fix_tabs_content(self):
        """Test fixing tabs in content."""
        content = "\ttype Person {\n\t  name: string\n\t  age: integer\n\t}\n"
        issues = self.linter.lint_content(content)
        fixed_content = self.linter.fix_content(content, issues)
        self.assertNotIn('\t', fixed_content, "Tabs should be removed")
        self.assertNotEqual(content, fixed_content, "Content should change")

    def test_fix_empty_line_whitespace_content(self):
        """Test fixing empty line whitespace in content."""
        content = """
type Person {
  name: string
  

  age: integer
}
"""
        issues = self.linter.lint_content(content)
        fixed_content = self.linter.fix_content(content, issues)
        self.assertNotEqual(content, fixed_content, "Content should change")

    def test_fix_no_fixable_issues_content(self):
        """Test fix_content with no fixable issues."""
        content = """
type Person {
  name: string
  age: integer
}
"""
        issues = self.linter.lint_content(content)
        fixed_content = self.linter.fix_content(content, issues)
        self.assertEqual(content, fixed_content, "Content should not change")


class TestIntegration(unittest.TestCase):
    """Test integration of all linter features."""

    def setUp(self):
        """Set up test fixtures."""
        self.linter = ADLLinter()

    def test_complete_lint_and_fix_workflow(self):
        """Test complete lint and fix workflow."""
        # Create a temporary file
        test_file = Path('/tmp/test_integration.adl')
        test_file.write_text("""
type person_name {
  firstName: string  
  lastName: string
  

  age: integer
}
""")
        try:
            # Step 1: Lint the file
            issues = self.linter.lint_file(test_file)
            self.assertGreater(len(issues), 0, "Should have issues before fix")

            # Step 2: Fix the file
            fixed_count = self.linter.fix_file(test_file, issues)
            self.assertGreater(fixed_count, 0, "Should fix some issues")

            # Step 3: Re-lint to verify fixes
            issues_after_fix = self.linter.lint_file(test_file)
            self.assertLess(len(issues_after_fix), len(issues), "Should have fewer issues after fix")

            # Step 4: Verify no fixable issues remain
            fixable_issues = [i for i in issues_after_fix if i.fixable]
            self.assertEqual(len(fixable_issues), 0, "Should have no fixable issues remaining")
        finally:
            test_file.unlink()

    def test_rule_enable_disable_and_lint(self):
        """Test enabling/disabling rules and linting."""
        # Create a temporary file
        test_file = Path('/tmp/test_rule_toggle.adl')
        test_file.write_text("""
type person_name {
  firstName: string
}
""")
        try:
            # Test with rule enabled
            self.linter.enable_rule('type-name-pascal-case')
            issues_enabled = self.linter.lint_file(test_file)
            self.assertGreater(len(issues_enabled), 0, "Should have issues with rule enabled")

            # Test with rule disabled
            self.linter.disable_rule('type-name-pascal-case')
            issues_disabled = self.linter.lint_file(test_file)
            self.assertEqual(len(issues_disabled), 0, "Should have no issues with rule disabled")
        finally:
            test_file.unlink()

    def test_severity_filter_and_lint(self):
        """Test severity filtering and linting."""
        # Create a temporary file
        test_file = Path('/tmp/test_severity_filter.adl')
        test_file.write_text("""
type person_name {
  firstName: string
}
""")
        try:
            # Test with error filter
            self.linter.set_severity_filter('error')
            issues_error = self.linter.lint_file(test_file)
            error_count = len(issues_error)

            # Test with warning filter
            self.linter.set_severity_filter('warning')
            issues_warning = self.linter.lint_file(test_file)
            warning_count = len(issues_warning)

            # Test with info filter
            self.linter.set_severity_filter('info')
            issues_info = self.linter.lint_file(test_file)
            info_count = len(issues_info)

            # Error should be subset of warning, which should be subset of info
            self.assertLessEqual(error_count, warning_count, "Error count should be <= warning count")
            self.assertLessEqual(warning_count, info_count, "Warning count should be <= info count")
        finally:
            test_file.unlink()

    def test_multiple_rules_in_single_file(self):
        """Test multiple rules in a single file."""
        content = """
type person_name {
  firstName: string  
  lastName: string
  

  age: integer
}
"""
        issues = self.linter.lint_content(content)

        # Check for issues from different rules
        has_type_name_issue = any(i.rule_name == 'type-name-pascal-case' for i in issues)
        has_field_name_issue = any(i.rule_name == 'field-name-snake-case' for i in issues)
        has_trailing_issue = any(i.rule_name == 'trailing-whitespace' for i in issues)
        has_empty_line_issue = any(i.rule_name == 'empty-line-with-whitespace' for i in issues)

        self.assertTrue(has_type_name_issue, "Should have type name issue")
        self.assertTrue(has_field_name_issue, "Should have field name issue")
        self.assertTrue(has_trailing_issue, "Should have trailing whitespace issue")
        self.assertTrue(has_empty_line_issue, "Should have empty line whitespace issue")


if __name__ == '__main__':
    unittest.main()