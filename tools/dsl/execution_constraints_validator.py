"""
Execution Constraints Validation

Validates execution_constraints field in ADL v2 agent definitions.
"""

from typing import List, Dict, Any, Optional
from dataclasses import dataclass


@dataclass
class ValidationError:
    """Represents a validation error."""

    field: str
    message: str
    severity: str = "error"


class ExecutionConstraintsValidator:
    """Validator for execution constraints configurations."""

    VALID_TIMEOUT_ACTIONS = ["terminate", "continue", "warn"]
    VALID_EVICTION_POLICIES = ["lru", "fifo", "random"]
    VALID_NEGOTIATION_PROTOCOLS = ["handshake", "discovery", "declaration"]
    VALID_FALLBACK_STRATEGIES = ["degrade", "fail", "warn"]
    VALID_ENFORCEMENT_LEVELS = ["strict", "moderate", "lenient"]
    VALID_VIOLATION_ACTIONS = ["terminate", "continue", "degrade"]

    def __init__(self):
        self.errors: List[ValidationError] = []

    def validate(self, execution_constraints: Dict[str, Any]) -> List[ValidationError]:
        """Validate execution_constraints configuration."""
        self.errors = []

        if not execution_constraints:
            return []

        self._validate_time_constraints(execution_constraints)
        self._validate_memory_constraints(execution_constraints)
        self._validate_resource_quotas(execution_constraints)
        self._validate_cost_constraints(execution_constraints)
        self._validate_security_constraints(execution_constraints)
        self._validate_capability_negotiation(execution_constraints)
        self._validate_capability_requirements(execution_constraints)
        self._validate_enforcement(execution_constraints)

        return self.errors

    def _validate_time_constraints(self, execution_constraints: Dict[str, Any]) -> None:
        """Validate time_constraints field."""
        time_constraints = execution_constraints.get("time_constraints")

        if not time_constraints:
            return

        if not isinstance(time_constraints, dict):
            self.errors.append(ValidationError(
                field="time_constraints",
                message="Time constraints must be an object"
            ))
            return

        if "max_execution_time_ms" in time_constraints:
            max_time = time_constraints["max_execution_time_ms"]
            if not isinstance(max_time, int) or max_time < 1:
                self.errors.append(ValidationError(
                    field="time_constraints.max_execution_time_ms",
                    message="max_execution_time_ms must be a positive integer"
                ))

        if "max_tool_invocation_time_ms" in time_constraints:
            max_time = time_constraints["max_tool_invocation_time_ms"]
            if not isinstance(max_time, int) or max_time < 1:
                self.errors.append(ValidationError(
                    field="time_constraints.max_tool_invocation_time_ms",
                    message="max_tool_invocation_time_ms must be a positive integer"
                ))

        if "max_llm_inference_time_ms" in time_constraints:
            max_time = time_constraints["max_llm_inference_time_ms"]
            if not isinstance(max_time, int) or max_time < 1:
                self.errors.append(ValidationError(
                    field="time_constraints.max_llm_inference_time_ms",
                    message="max_llm_inference_time_ms must be a positive integer"
                ))

        if "timeout_action" in time_constraints:
            action = time_constraints["timeout_action"]
            if action not in self.VALID_TIMEOUT_ACTIONS:
                self.errors.append(ValidationError(
                    field="time_constraints.timeout_action",
                    message=f"Invalid timeout_action: {action}. Must be one of {self.VALID_TIMEOUT_ACTIONS}"
                ))

    def _validate_memory_constraints(self, execution_constraints: Dict[str, Any]) -> None:
        """Validate memory_constraints field."""
        memory_constraints = execution_constraints.get("memory_constraints")

        if not memory_constraints:
            return

        if not isinstance(memory_constraints, dict):
            self.errors.append(ValidationError(
                field="memory_constraints",
                message="Memory constraints must be an object"
            ))
            return

        if "max_memory_mb" in memory_constraints:
            max_memory = memory_constraints["max_memory_mb"]
            if not isinstance(max_memory, int) or max_memory < 1:
                self.errors.append(ValidationError(
                    field="memory_constraints.max_memory_mb",
                    message="max_memory_mb must be a positive integer"
                ))

        if "max_context_tokens" in memory_constraints:
            max_tokens = memory_constraints["max_context_tokens"]
            if not isinstance(max_tokens, int) or max_tokens < 1:
                self.errors.append(ValidationError(
                    field="memory_constraints.max_context_tokens",
                    message="max_context_tokens must be a positive integer"
                ))

        if "max_tool_output_size_mb" in memory_constraints:
            max_size = memory_constraints["max_tool_output_size_mb"]
            if not isinstance(max_size, int) or max_size < 1:
                self.errors.append(ValidationError(
                    field="memory_constraints.max_tool_output_size_mb",
                    message="max_tool_output_size_mb must be a positive integer"
                ))

        if "memory_eviction_policy" in memory_constraints:
            policy = memory_constraints["memory_eviction_policy"]
            if policy not in self.VALID_EVICTION_POLICIES:
                self.errors.append(ValidationError(
                    field="memory_constraints.memory_eviction_policy",
                    message=f"Invalid memory_eviction_policy: {policy}. Must be one of {self.VALID_EVICTION_POLICIES}"
                ))

    def _validate_resource_quotas(self, execution_constraints: Dict[str, Any]) -> None:
        """Validate resource_quotas field."""
        resource_quotas = execution_constraints.get("resource_quotas")

        if not resource_quotas:
            return

        if not isinstance(resource_quotas, dict):
            self.errors.append(ValidationError(
                field="resource_quotas",
                message="Resource quotas must be an object"
            ))
            return

        quota_fields = [
            "max_llm_calls_per_hour",
            "max_tool_invocations_per_task",
            "max_network_requests_per_minute",
            "max_file_operations_per_task"
        ]

        for field in quota_fields:
            if field in resource_quotas:
                value = resource_quotas[field]
                if not isinstance(value, int) or value < 1:
                    self.errors.append(ValidationError(
                        field=f"resource_quotas.{field}",
                        message=f"{field} must be a positive integer"
                    ))

    def _validate_cost_constraints(self, execution_constraints: Dict[str, Any]) -> None:
        """Validate cost_constraints field."""
        cost_constraints = execution_constraints.get("cost_constraints")

        if not cost_constraints:
            return

        if not isinstance(cost_constraints, dict):
            self.errors.append(ValidationError(
                field="cost_constraints",
                message="Cost constraints must be an object"
            ))
            return

        if "max_cost_per_task_usd" in cost_constraints:
            max_cost = cost_constraints["max_cost_per_task_usd"]
            if not isinstance(max_cost, (int, float)) or max_cost < 0:
                self.errors.append(ValidationError(
                    field="cost_constraints.max_cost_per_task_usd",
                    message="max_cost_per_task_usd must be a non-negative number"
                ))

        if "max_cost_per_hour_usd" in cost_constraints:
            max_cost = cost_constraints["max_cost_per_hour_usd"]
            if not isinstance(max_cost, (int, float)) or max_cost < 0:
                self.errors.append(ValidationError(
                    field="cost_constraints.max_cost_per_hour_usd",
                    message="max_cost_per_hour_usd must be a non-negative number"
                ))

        if "cost_alert_threshold_usd" in cost_constraints:
            threshold = cost_constraints["cost_alert_threshold_usd"]
            if not isinstance(threshold, (int, float)) or threshold < 0:
                self.errors.append(ValidationError(
                    field="cost_constraints.cost_alert_threshold_usd",
                    message="cost_alert_threshold_usd must be a non-negative number"
                ))

    def _validate_security_constraints(self, execution_constraints: Dict[str, Any]) -> None:
        """Validate security_constraints field."""
        security_constraints = execution_constraints.get("security_constraints")

        if not security_constraints:
            return

        if not isinstance(security_constraints, dict):
            self.errors.append(ValidationError(
                field="security_constraints",
                message="Security constraints must be an object"
            ))
            return

        if "allowed_domains" in security_constraints:
            domains = security_constraints["allowed_domains"]
            if not isinstance(domains, list):
                self.errors.append(ValidationError(
                    field="security_constraints.allowed_domains",
                    message="allowed_domains must be an array"
                ))

        if "blocked_domains" in security_constraints:
            domains = security_constraints["blocked_domains"]
            if not isinstance(domains, list):
                self.errors.append(ValidationError(
                    field="security_constraints.blocked_domains",
                    message="blocked_domains must be an array"
                ))

        if "max_file_size_mb" in security_constraints:
            max_size = security_constraints["max_file_size_mb"]
            if not isinstance(max_size, int) or max_size < 1:
                self.errors.append(ValidationError(
                    field="security_constraints.max_file_size_mb",
                    message="max_file_size_mb must be a positive integer"
                ))

        if "allowed_file_types" in security_constraints:
            file_types = security_constraints["allowed_file_types"]
            if not isinstance(file_types, list):
                self.errors.append(ValidationError(
                    field="security_constraints.allowed_file_types",
                    message="allowed_file_types must be an array"
                ))

    def _validate_capability_negotiation(self, execution_constraints: Dict[str, Any]) -> None:
        """Validate capability_negotiation field."""
        capability_negotiation = execution_constraints.get("capability_negotiation")

        if not capability_negotiation:
            return

        if not isinstance(capability_negotiation, dict):
            self.errors.append(ValidationError(
                field="capability_negotiation",
                message="Capability negotiation must be an object"
            ))
            return

        if "protocol" in capability_negotiation:
            protocol = capability_negotiation["protocol"]
            if protocol not in self.VALID_NEGOTIATION_PROTOCOLS:
                self.errors.append(ValidationError(
                    field="capability_negotiation.protocol",
                    message=f"Invalid protocol: {protocol}. Must be one of {self.VALID_NEGOTIATION_PROTOCOLS}"
                ))

        if "timeout_ms" in capability_negotiation:
            timeout = capability_negotiation["timeout_ms"]
            if not isinstance(timeout, int) or timeout < 1:
                self.errors.append(ValidationError(
                    field="capability_negotiation.timeout_ms",
                    message="timeout_ms must be a positive integer"
                ))

        if "fallback_strategy" in capability_negotiation:
            strategy = capability_negotiation["fallback_strategy"]
            if strategy not in self.VALID_FALLBACK_STRATEGIES:
                self.errors.append(ValidationError(
                    field="capability_negotiation.fallback_strategy",
                    message=f"Invalid fallback_strategy: {strategy}. Must be one of {self.VALID_FALLBACK_STRATEGIES}"
                ))

    def _validate_capability_requirements(self, execution_constraints: Dict[str, Any]) -> None:
        """Validate capability_requirements field."""
        capability_requirements = execution_constraints.get("capability_requirements")

        if not capability_requirements:
            return

        if not isinstance(capability_requirements, dict):
            self.errors.append(ValidationError(
                field="capability_requirements",
                message="Capability requirements must be an object"
            ))
            return

        for req_type in ["required", "optional"]:
            if req_type in capability_requirements:
                requirements = capability_requirements[req_type]
                if not isinstance(requirements, list):
                    self.errors.append(ValidationError(
                        field=f"capability_requirements.{req_type}",
                        message=f"{req_type} must be an array"
                    ))
                    continue

                for i, req in enumerate(requirements):
                    if not isinstance(req, dict):
                        self.errors.append(ValidationError(
                            field=f"capability_requirements.{req_type}[{i}]",
                            message="Capability requirement must be an object"
                        ))
                        continue

                    if "name" not in req:
                        self.errors.append(ValidationError(
                            field=f"capability_requirements.{req_type}[{i}]",
                            message="Capability requirement must have a 'name' field"
                        ))

    def _validate_enforcement(self, execution_constraints: Dict[str, Any]) -> None:
        """Validate enforcement field."""
        enforcement = execution_constraints.get("enforcement")

        if not enforcement:
            return

        if not isinstance(enforcement, dict):
            self.errors.append(ValidationError(
                field="enforcement",
                message="Enforcement must be an object"
            ))
            return

        if "level" in enforcement:
            level = enforcement["level"]
            if level not in self.VALID_ENFORCEMENT_LEVELS:
                self.errors.append(ValidationError(
                    field="enforcement.level",
                    message=f"Invalid level: {level}. Must be one of {self.VALID_ENFORCEMENT_LEVELS}"
                ))

        if "violation_action" in enforcement:
            action = enforcement["violation_action"]
            if action not in self.VALID_VIOLATION_ACTIONS:
                self.errors.append(ValidationError(
                    field="enforcement.violation_action",
                    message=f"Invalid violation_action: {action}. Must be one of {self.VALID_VIOLATION_ACTIONS}"
                ))


def validate_execution_constraints(execution_constraints: Dict[str, Any]) -> List[ValidationError]:
    """Validate execution_constraints configuration."""
    validator = ExecutionConstraintsValidator()
    return validator.validate(execution_constraints)
