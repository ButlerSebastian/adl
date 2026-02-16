"""
Memory Extensions Validation

Validates memory_extensions field in ADL v2 agent definitions.
"""

from typing import List, Dict, Any, Optional
from dataclasses import dataclass


@dataclass
class ValidationError:
    """Represents a validation error."""

    field: str
    message: str
    severity: str = "error"


class MemoryExtensionsValidator:
    """Validator for memory extensions configurations."""

    VALID_MEMORY_TYPES = ["episodic", "semantic", "working", "hybrid"]
    VALID_BACKENDS = ["sqlite", "postgresql", "mongodb", "redis", "chromadb", "pinecone", "weaviate", "custom"]
    VALID_LIFECYCLE_STAGES = ["creation", "access", "update", "eviction", "consolidation", "archival"]
    VALID_EVICTION_POLICIES = ["lru", "lfu", "fifo", "random", "time_based", "custom"]
    VALID_CONSOLIDATION_STRATEGIES = ["summarization", "clustering", "hierarchical", "custom"]
    VALID_PRIVACY_LEVELS = ["public", "private", "confidential", "restricted"]
    VALID_ENCRYPTION_TYPES = ["aes256", "rsa", "custom"]

    def __init__(self):
        self.errors: List[ValidationError] = []

    def validate(self, memory_extensions: Dict[str, Any]) -> List[ValidationError]:
        """Validate memory extensions configuration."""
        self.errors = []

        if not memory_extensions:
            return []

        self._validate_memory_types(memory_extensions)
        self._validate_lifecycle(memory_extensions)
        self._validate_eviction_policy(memory_extensions)
        self._validate_consolidation(memory_extensions)
        self._validate_privacy(memory_extensions)

        return self.errors

    def _validate_memory_types(self, memory_extensions: Dict[str, Any]) -> None:
        """Validate memory_types field."""
        memory_types = memory_extensions.get("memory_types")

        if not memory_types:
            return

        if not isinstance(memory_types, list):
            self.errors.append(ValidationError(
                field="memory_types",
                message="Memory types must be an array"
            ))
            return

        for i, memory_type in enumerate(memory_types):
            if not isinstance(memory_type, dict):
                self.errors.append(ValidationError(
                    field=f"memory_types[{i}]",
                    message="Memory type must be an object"
                ))
                continue

            if "type" not in memory_type:
                self.errors.append(ValidationError(
                    field=f"memory_types[{i}]",
                    message="Memory type must have a 'type' field"
                ))
                continue

            type_name = memory_type["type"]
            if type_name not in self.VALID_MEMORY_TYPES:
                self.errors.append(ValidationError(
                    field=f"memory_types[{i}].type",
                    message=f"Invalid memory type: {type_name}. Must be one of {self.VALID_MEMORY_TYPES}"
                ))

            if "backend" in memory_type:
                backend = memory_type["backend"]
                if backend not in self.VALID_BACKENDS:
                    self.errors.append(ValidationError(
                        field=f"memory_types[{i}].backend",
                        message=f"Invalid backend: {backend}. Must be one of {self.VALID_BACKENDS}"
                    ))

            if "max_size_mb" in memory_type:
                max_size = memory_type["max_size_mb"]
                if not isinstance(max_size, (int, float)) or max_size <= 0:
                    self.errors.append(ValidationError(
                        field=f"memory_types[{i}].max_size_mb",
                        message="max_size_mb must be a positive number"
                    ))

            if "retention_days" in memory_type:
                retention = memory_type["retention_days"]
                if not isinstance(retention, int) or retention < 0:
                    self.errors.append(ValidationError(
                        field=f"memory_types[{i}].retention_days",
                        message="retention_days must be a non-negative integer"
                    ))

    def _validate_lifecycle(self, memory_extensions: Dict[str, Any]) -> None:
        """Validate lifecycle field."""
        lifecycle = memory_extensions.get("lifecycle")

        if not lifecycle:
            return

        if not isinstance(lifecycle, dict):
            self.errors.append(ValidationError(
                field="lifecycle",
                message="Lifecycle must be an object"
            ))
            return

        for stage in self.VALID_LIFECYCLE_STAGES:
            if stage in lifecycle:
                stage_config = lifecycle[stage]
                if not isinstance(stage_config, dict):
                    self.errors.append(ValidationError(
                        field=f"lifecycle.{stage}",
                        message=f"{stage} configuration must be an object"
                    ))
                    continue

                if "enabled" in stage_config and stage_config["enabled"]:
                    if "handler" not in stage_config:
                        self.errors.append(ValidationError(
                            field=f"lifecycle.{stage}",
                            message=f"Enabled {stage} must have a 'handler' field"
                        ))

    def _validate_eviction_policy(self, memory_extensions: Dict[str, Any]) -> None:
        """Validate eviction_policy field."""
        eviction_policy = memory_extensions.get("eviction_policy")

        if not eviction_policy:
            return

        if not isinstance(eviction_policy, dict):
            self.errors.append(ValidationError(
                field="eviction_policy",
                message="Eviction policy must be an object"
            ))
            return

        if "policy" not in eviction_policy:
            self.errors.append(ValidationError(
                field="eviction_policy",
                message="Eviction policy must have a 'policy' field"
            ))
            return

        policy = eviction_policy["policy"]
        if policy not in self.VALID_EVICTION_POLICIES:
            self.errors.append(ValidationError(
                field="eviction_policy.policy",
                message=f"Invalid eviction policy: {policy}. Must be one of {self.VALID_EVICTION_POLICIES}"
            ))

        if "threshold_percentage" in eviction_policy:
            threshold = eviction_policy["threshold_percentage"]
            if not isinstance(threshold, (int, float)) or threshold <= 0 or threshold > 100:
                self.errors.append(ValidationError(
                    field="eviction_policy.threshold_percentage",
                    message="threshold_percentage must be between 0 and 100"
                ))

        if "min_entries" in eviction_policy:
            min_entries = eviction_policy["min_entries"]
            if not isinstance(min_entries, int) or min_entries < 0:
                self.errors.append(ValidationError(
                    field="eviction_policy.min_entries",
                    message="min_entries must be a non-negative integer"
                ))

    def _validate_consolidation(self, memory_extensions: Dict[str, Any]) -> None:
        """Validate consolidation field."""
        consolidation = memory_extensions.get("consolidation")

        if not consolidation:
            return

        if not isinstance(consolidation, dict):
            self.errors.append(ValidationError(
                field="consolidation",
                message="Consolidation must be an object"
            ))
            return

        if "enabled" in consolidation and consolidation["enabled"]:
            if "strategy" not in consolidation:
                self.errors.append(ValidationError(
                    field="consolidation",
                    message="Enabled consolidation must have a 'strategy' field"
                ))
            else:
                strategy = consolidation["strategy"]
                if strategy not in self.VALID_CONSOLIDATION_STRATEGIES:
                    self.errors.append(ValidationError(
                        field="consolidation.strategy",
                        message=f"Invalid consolidation strategy: {strategy}. Must be one of {self.VALID_CONSOLIDATION_STRATEGIES}"
                    ))

            if "interval_hours" in consolidation:
                interval = consolidation["interval_hours"]
                if not isinstance(interval, (int, float)) or interval <= 0:
                    self.errors.append(ValidationError(
                        field="consolidation.interval_hours",
                        message="interval_hours must be a positive number"
                    ))

            if "min_entries" in consolidation:
                min_entries = consolidation["min_entries"]
                if not isinstance(min_entries, int) or min_entries < 1:
                    self.errors.append(ValidationError(
                        field="consolidation.min_entries",
                        message="min_entries must be a positive integer"
                    ))

    def _validate_privacy(self, memory_extensions: Dict[str, Any]) -> None:
        """Validate privacy field."""
        privacy = memory_extensions.get("privacy")

        if not privacy:
            return

        if not isinstance(privacy, dict):
            self.errors.append(ValidationError(
                field="privacy",
                message="Privacy must be an object"
            ))
            return

        if "enabled" in privacy and privacy["enabled"]:
            if "level" not in privacy:
                self.errors.append(ValidationError(
                    field="privacy",
                    message="Enabled privacy must have a 'level' field"
                ))
            else:
                level = privacy["level"]
                if level not in self.VALID_PRIVACY_LEVELS:
                    self.errors.append(ValidationError(
                        field="privacy.level",
                        message=f"Invalid privacy level: {level}. Must be one of {self.VALID_PRIVACY_LEVELS}"
                    ))

        if "encryption" in privacy and privacy["encryption"]:
            if "encryption_type" not in privacy:
                self.errors.append(ValidationError(
                    field="privacy",
                    message="Enabled encryption must have an 'encryption_type' field"
                ))
            else:
                encryption_type = privacy["encryption_type"]
                if encryption_type not in self.VALID_ENCRYPTION_TYPES:
                    self.errors.append(ValidationError(
                        field="privacy.encryption_type",
                        message=f"Invalid encryption type: {encryption_type}. Must be one of {self.VALID_ENCRYPTION_TYPES}"
                    ))

        if "pii_detection" in privacy and privacy["pii_detection"]:
            if "pii_types" not in privacy:
                self.errors.append(ValidationError(
                    field="privacy",
                    message="Enabled PII detection must have a 'pii_types' field"
                ))
            elif not isinstance(privacy["pii_types"], list):
                self.errors.append(ValidationError(
                    field="privacy.pii_types",
                    message="pii_types must be an array"
                ))

        if "access_control" in privacy and privacy["access_control"]:
            if "allowed_roles" not in privacy:
                self.errors.append(ValidationError(
                    field="privacy",
                    message="Enabled access control must have an 'allowed_roles' field"
                ))
            elif not isinstance(privacy["allowed_roles"], list):
                self.errors.append(ValidationError(
                    field="privacy.allowed_roles",
                    message="allowed_roles must be an array"
                ))


def validate_memory_extensions(memory_extensions: Dict[str, Any]) -> List[ValidationError]:
    """Validate memory extensions configuration."""
    validator = MemoryExtensionsValidator()
    return validator.validate(memory_extensions)
