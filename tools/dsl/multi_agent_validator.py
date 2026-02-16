"""
Multi-Agent Role Validation

Validates agent_roles field in ADL v2 agent definitions.
"""

from typing import List, Dict, Any, Optional
from dataclasses import dataclass


@dataclass
class ValidationError:
    """Represents a validation error."""

    field: str
    message: str
    severity: str = "error"


class MultiAgentRoleValidator:
    """Validator for multi-agent role configurations."""

    VALID_ROLES = ["coordinator", "worker", "supervisor", "critic"]
    VALID_CAPABILITY_TYPES = ["management", "coordination", "execution", "validation", "advisory"]
    VALID_CHANNELS = ["direct", "broadcast", "pubsub"]
    VALID_MESSAGE_FORMATS = ["json", "protobuf", "avro"]
    VALID_PRIORITIES = ["low", "medium", "high", "critical"]
    VALID_RETRY_POLICIES = ["none", "fixed", "exponential_backoff"]

    ROLE_INCOMPATIBILITIES = {
        "coordinator": ["worker"],
        "worker": ["coordinator"],
        "supervisor": ["critic"],
        "critic": ["supervisor"]
    }

    ROLE_CONSTRAINTS = {
        "coordinator": {
            "can_execute_tasks": False,
            "can_modify_configuration": True
        },
        "worker": {
            "can_execute_tasks": True,
            "can_modify_configuration": False
        },
        "supervisor": {
            "can_execute_tasks": False,
            "can_modify_configuration": False
        },
        "critic": {
            "can_execute_tasks": False,
            "can_modify_configuration": False
        }
    }

    def __init__(self):
        self.errors: List[ValidationError] = []

    def validate(self, agent_roles: Dict[str, Any]) -> List[ValidationError]:
        """Validate agent_roles configuration."""
        self.errors = []

        if not agent_roles:
            return []

        self._validate_primary_role(agent_roles)
        self._validate_secondary_roles(agent_roles)
        self._validate_role_compatibility(agent_roles)
        self._validate_capabilities(agent_roles)
        self._validate_constraints(agent_roles)
        self._validate_communication_protocols(agent_roles)

        return self.errors

    def _validate_primary_role(self, agent_roles: Dict[str, Any]) -> None:
        """Validate primary_role field."""
        primary_role = agent_roles.get("primary_role")

        if not primary_role:
            self.errors.append(ValidationError(
                field="primary_role",
                message="Primary role is required"
            ))
            return

        if primary_role not in self.VALID_ROLES:
            self.errors.append(ValidationError(
                field="primary_role",
                message=f"Invalid primary role: {primary_role}. Must be one of {self.VALID_ROLES}"
            ))

    def _validate_secondary_roles(self, agent_roles: Dict[str, Any]) -> None:
        """Validate secondary_roles field."""
        secondary_roles = agent_roles.get("secondary_roles", [])

        if not isinstance(secondary_roles, list):
            self.errors.append(ValidationError(
                field="secondary_roles",
                message="Secondary roles must be an array"
            ))
            return

        if len(secondary_roles) > 2:
            self.errors.append(ValidationError(
                field="secondary_roles",
                message=f"Maximum 2 secondary roles allowed, got {len(secondary_roles)}"
            ))

        for role in secondary_roles:
            if role not in self.VALID_ROLES:
                self.errors.append(ValidationError(
                    field="secondary_roles",
                    message=f"Invalid secondary role: {role}. Must be one of {self.VALID_ROLES}"
                ))

    def _validate_role_compatibility(self, agent_roles: Dict[str, Any]) -> None:
        """Validate role compatibility."""
        primary_role = agent_roles.get("primary_role")
        secondary_roles = agent_roles.get("secondary_roles", [])

        if not primary_role:
            return

        incompatible_roles = self.ROLE_INCOMPATIBILITIES.get(primary_role, [])

        for secondary_role in secondary_roles:
            if secondary_role in incompatible_roles:
                self.errors.append(ValidationError(
                    field="secondary_roles",
                    message=f"Primary role '{primary_role}' is incompatible with secondary role '{secondary_role}'"
                ))

    def _validate_capabilities(self, agent_roles: Dict[str, Any]) -> None:
        """Validate capabilities field."""
        capabilities = agent_roles.get("capabilities", [])

        if not isinstance(capabilities, list):
            self.errors.append(ValidationError(
                field="capabilities",
                message="Capabilities must be an array"
            ))
            return

        for i, capability in enumerate(capabilities):
            if not isinstance(capability, dict):
                self.errors.append(ValidationError(
                    field=f"capabilities[{i}]",
                    message="Capability must be an object"
                ))
                continue

            if "name" not in capability:
                self.errors.append(ValidationError(
                    field=f"capabilities[{i}]",
                    message="Capability must have a 'name' field"
                ))

            if "type" not in capability:
                self.errors.append(ValidationError(
                    field=f"capabilities[{i}]",
                    message="Capability must have a 'type' field"
                ))
            elif capability["type"] not in self.VALID_CAPABILITY_TYPES:
                self.errors.append(ValidationError(
                    field=f"capabilities[{i}].type",
                    message=f"Invalid capability type: {capability['type']}. Must be one of {self.VALID_CAPABILITY_TYPES}"
                ))

    def _validate_constraints(self, agent_roles: Dict[str, Any]) -> None:
        """Validate constraints field."""
        constraints = agent_roles.get("constraints", {})
        primary_role = agent_roles.get("primary_role")

        if not isinstance(constraints, dict):
            self.errors.append(ValidationError(
                field="constraints",
                message="Constraints must be an object"
            ))
            return

        if primary_role and primary_role in self.ROLE_CONSTRAINTS:
            expected_constraints = self.ROLE_CONSTRAINTS[primary_role]

            for key, expected_value in expected_constraints.items():
                if key in constraints and constraints[key] != expected_value:
                    self.errors.append(ValidationError(
                        field=f"constraints.{key}",
                        message=f"For role '{primary_role}', constraint '{key}' must be {expected_value}, got {constraints[key]}"
                    ))

        if "max_coordinators" in constraints:
            max_coordinators = constraints["max_coordinators"]
            if not isinstance(max_coordinators, int) or max_coordinators < 1:
                self.errors.append(ValidationError(
                    field="constraints.max_coordinators",
                    message="max_coordinators must be a positive integer"
                ))

        if "communication_channels" in constraints:
            channels = constraints["communication_channels"]
            if not isinstance(channels, list):
                self.errors.append(ValidationError(
                    field="constraints.communication_channels",
                    message="communication_channels must be an array"
                ))
            else:
                for channel in channels:
                    if channel not in self.VALID_CHANNELS:
                        self.errors.append(ValidationError(
                            field="constraints.communication_channels",
                            message=f"Invalid channel: {channel}. Must be one of {self.VALID_CHANNELS}"
                        ))

    def _validate_communication_protocols(self, agent_roles: Dict[str, Any]) -> None:
        """Validate communication_protocols field."""
        protocols = agent_roles.get("communication_protocols", {})

        if not isinstance(protocols, dict):
            self.errors.append(ValidationError(
                field="communication_protocols",
                message="Communication protocols must be an object"
            ))
            return

        if "message_format" in protocols:
            message_format = protocols["message_format"]
            if message_format not in self.VALID_MESSAGE_FORMATS:
                self.errors.append(ValidationError(
                    field="communication_protocols.message_format",
                    message=f"Invalid message format: {message_format}. Must be one of {self.VALID_MESSAGE_FORMATS}"
                ))

        if "channels" in protocols:
            channels = protocols["channels"]
            if not isinstance(channels, list):
                self.errors.append(ValidationError(
                    field="communication_protocols.channels",
                    message="Channels must be an array"
                ))
            else:
                for channel in channels:
                    if channel not in self.VALID_CHANNELS:
                        self.errors.append(ValidationError(
                            field="communication_protocols.channels",
                            message=f"Invalid channel: {channel}. Must be one of {self.VALID_CHANNELS}"
                        ))

        if "latency_requirements" in protocols:
            latency = protocols["latency_requirements"]
            if not isinstance(latency, dict):
                self.errors.append(ValidationError(
                    field="communication_protocols.latency_requirements",
                    message="Latency requirements must be an object"
                ))
            else:
                if "max_latency_ms" in latency:
                    max_latency = latency["max_latency_ms"]
                    if not isinstance(max_latency, int) or max_latency < 0:
                        self.errors.append(ValidationError(
                            field="communication_protocols.latency_requirements.max_latency_ms",
                            message="max_latency_ms must be a non-negative integer"
                        ))

                if "priority" in latency:
                    priority = latency["priority"]
                    if priority not in self.VALID_PRIORITIES:
                        self.errors.append(ValidationError(
                            field="communication_protocols.latency_requirements.priority",
                            message=f"Invalid priority: {priority}. Must be one of {self.VALID_PRIORITIES}"
                        ))

        if "reliability" in protocols:
            reliability = protocols["reliability"]
            if not isinstance(reliability, dict):
                self.errors.append(ValidationError(
                    field="communication_protocols.reliability",
                    message="Reliability must be an object"
                ))
            else:
                if "retry_policy" in reliability:
                    retry_policy = reliability["retry_policy"]
                    if retry_policy not in self.VALID_RETRY_POLICIES:
                        self.errors.append(ValidationError(
                            field="communication_protocols.reliability.retry_policy",
                            message=f"Invalid retry policy: {retry_policy}. Must be one of {self.VALID_RETRY_POLICIES}"
                        ))


def validate_agent_roles(agent_roles: Dict[str, Any]) -> List[ValidationError]:
    """Validate agent_roles configuration."""
    validator = MultiAgentRoleValidator()
    return validator.validate(agent_roles)
