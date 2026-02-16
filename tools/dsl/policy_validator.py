"""
Policy Validation

Validates policy field in ADL v3 agent definitions.
"""

from typing import List, Dict, Any
from dataclasses import dataclass


@dataclass
class ValidationError:
    """Represents a validation error."""

    field: str
    message: str
    severity: str = "error"


class PolicyValidator:
    """Validator for policy configurations."""

    VALID_ENFORCEMENT_MODES = ["strict", "moderate", "lenient"]
    VALID_ENFORCEMENT_ACTIONS = ["deny", "warn", "log", "allow"]

    def __init__(self):
        self.errors: List[ValidationError] = []

    def validate(self, policy: Dict[str, Any]) -> List[ValidationError]:
        """Validate policy configuration."""
        self.errors = []

        if not policy:
            return []

        self._validate_structure(policy)
        self._validate_rego(policy)
        self._validate_enforcement(policy)
        self._validate_data(policy)

        return self.errors

    def _validate_structure(self, policy: Dict[str, Any]) -> None:
        """Validate policy structure."""
        required_fields = ["id", "name", "version", "rego", "enforcement"]
        for field in required_fields:
            if field not in policy:
                self.errors.append(ValidationError(
                    field=field,
                    message=f"Policy must have a '{field}' field"
                ))

        # Validate version format
        if "version" in policy:
            version = policy["version"]
            if not isinstance(version, str):
                self.errors.append(ValidationError(
                    field="version",
                    message="Version must be a string"
                ))
            elif not self._is_semantic_version(version):
                self.errors.append(ValidationError(
                    field="version",
                    message=f"Version must follow semantic versioning (e.g., '1.0.0'), got '{version}'"
                ))

    def _validate_rego(self, policy: Dict[str, Any]) -> None:
        """Validate Rego policy code."""
        rego = policy.get("rego")

        if not rego:
            self.errors.append(ValidationError(
                field="rego",
                message="Policy must have a 'rego' field"
            ))
            return

        if not isinstance(rego, str):
            self.errors.append(ValidationError(
                field="rego",
                message="Rego must be a string"
            ))
            return

        # Check for required Rego elements
        if "package" not in rego:
            self.errors.append(ValidationError(
                field="rego",
                message="Rego policy must define a package"
            ))

        # Check for default deny pattern (security best practice)
        if "default allow := false" not in rego and "default allow := true" not in rego:
            self.errors.append(ValidationError(
                field="rego",
                message="Rego policy should define a default allow rule (prefer 'default allow := false' for security)"
            ))

        # Check for allow rule
        if "allow if" not in rego:
            self.errors.append(ValidationError(
                field="rego",
                message="Rego policy should define at least one allow rule"
            ))

    def _validate_enforcement(self, policy: Dict[str, Any]) -> None:
        """Validate enforcement configuration."""
        enforcement = policy.get("enforcement")

        if not enforcement:
            self.errors.append(ValidationError(
                field="enforcement",
                message="Policy must have an 'enforcement' field"
            ))
            return

        if not isinstance(enforcement, dict):
            self.errors.append(ValidationError(
                field="enforcement",
                message="Enforcement must be an object"
            ))
            return

        # Validate mode
        if "mode" not in enforcement:
            self.errors.append(ValidationError(
                field="enforcement.mode",
                message="Enforcement must have a 'mode' field"
            ))
        else:
            mode = enforcement["mode"]
            if mode not in self.VALID_ENFORCEMENT_MODES:
                self.errors.append(ValidationError(
                    field="enforcement.mode",
                    message=f"Invalid enforcement mode: '{mode}'. Must be one of {self.VALID_ENFORCEMENT_MODES}"
                ))

        # Validate action
        if "action" not in enforcement:
            self.errors.append(ValidationError(
                field="enforcement.action",
                message="Enforcement must have an 'action' field"
            ))
        else:
            action = enforcement["action"]
            if action not in self.VALID_ENFORCEMENT_ACTIONS:
                self.errors.append(ValidationError(
                    field="enforcement.action",
                    message=f"Invalid enforcement action: '{action}'. Must be one of {self.VALID_ENFORCEMENT_ACTIONS}"
                ))

        # Validate audit_log if present
        if "audit_log" in enforcement:
            audit_log = enforcement["audit_log"]
            if not isinstance(audit_log, bool):
                self.errors.append(ValidationError(
                    field="enforcement.audit_log",
                    message="audit_log must be a boolean"
                ))

    def _validate_data(self, policy: Dict[str, Any]) -> None:
        """Validate policy data."""
        data = policy.get("data")

        if not data:
            return

        if not isinstance(data, dict):
            self.errors.append(ValidationError(
                field="data",
                message="Policy data must be an object"
            ))
            return

        # Validate common data structures
        if "roles" in data:
            roles = data["roles"]
            if not isinstance(roles, dict):
                self.errors.append(ValidationError(
                    field="data.roles",
                    message="Roles must be an object"
                ))
            else:
                for user, user_roles in roles.items():
                    if not isinstance(user_roles, list):
                        self.errors.append(ValidationError(
                            field="data.roles." + user,
                            message="Roles for user '" + user + "' must be an array"
                        ))

        if "permissions" in data:
            permissions = data["permissions"]
            if not isinstance(permissions, dict):
                self.errors.append(ValidationError(
                    field="data.permissions",
                    message="Permissions must be an object"
                ))

        if "resources" in data:
            resources = data["resources"]
            if not isinstance(resources, dict):
                self.errors.append(ValidationError(
                    field="data.resources",
                    message="Resources must be an object"
                ))
            else:
                for resource, actions in resources.items():
                    if not isinstance(actions, list):
                        self.errors.append(ValidationError(
                            field="data.resources." + resource,
                            message="Actions for resource '" + resource + "' must be an array"
                        ))

    def _is_semantic_version(self, version: str) -> bool:
        """Check if version follows semantic versioning."""
        import re
        pattern = r'^\d+\.\d+\.\d+(-[a-zA-Z0-9.]+)?$'
        return bool(re.match(pattern, version))


def validate_policy(policy: Dict[str, Any]) -> List[ValidationError]:
    """Validate policy configuration."""
    validator = PolicyValidator()
    return validator.validate(policy)
