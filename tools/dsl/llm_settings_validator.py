"""
LLM Settings Extensions Validation

Validates llm_extensions field in ADL v2 agent definitions.
"""

from typing import List, Dict, Any, Optional
from dataclasses import dataclass


@dataclass
class ValidationError:
    """Represents a validation error."""

    field: str
    message: str
    severity: str = "error"


class LLMSettingsValidator:
    """Validator for LLM settings extensions configurations."""

    VALID_PROVIDERS = ["openai", "anthropic", "cohere", "google", "huggingface", "custom"]
    VALID_ROUTING_STRATEGIES = ["direct", "task_based", "cost_based", "performance_based", "adaptive"]
    VALID_BACKOFF_STRATEGIES = ["exponential", "linear", "fixed", "custom"]
    VALID_TIMEOUT_ACTIONS = ["fallback", "retry", "fail", "custom"]
    VALID_METRICS = ["response_time_ms", "tokens_per_second", "cost_per_task_usd", "success_rate", "fallback_rate"]
    VALID_QUALITY_METRICS = ["coherence_score", "relevance_score", "accuracy_score", "user_satisfaction"]
    VALID_OPERATORS = ["equals", "not_equals", "greater_than", "less_than", "greater_than_or_equal", "less_than_or_equal"]
    VALID_CHANNELS = ["slack", "email", "webhook", "custom"]

    def __init__(self):
        self.errors: List[ValidationError] = []

    def validate(self, llm_extensions: Dict[str, Any]) -> List[ValidationError]:
        """Validate LLM settings extensions configuration."""
        self.errors = []

        if not llm_extensions:
            return []

        self._validate_primary_model(llm_extensions)
        self._validate_fallback_models(llm_extensions)
        self._validate_specialized_models(llm_extensions)
        self._validate_routing(llm_extensions)
        self._validate_model_constraints(llm_extensions)
        self._validate_model_configuration(llm_extensions)
        self._validate_monitoring(llm_extensions)
        self._validate_alerting(llm_extensions)

        return self.errors

    def _validate_primary_model(self, llm_extensions: Dict[str, Any]) -> None:
        """Validate primary_model field."""
        primary_model = llm_extensions.get("primary_model")

        if not primary_model:
            return

        if not isinstance(primary_model, dict):
            self.errors.append(ValidationError(
                field="primary_model",
                message="Primary model must be an object"
            ))
            return

        if "provider" not in primary_model:
            self.errors.append(ValidationError(
                field="primary_model",
                message="Primary model must have a 'provider' field"
            ))
        elif primary_model["provider"] not in self.VALID_PROVIDERS:
            self.errors.append(ValidationError(
                field="primary_model.provider",
                message=f"Invalid provider: {primary_model['provider']}. Must be one of {self.VALID_PROVIDERS}"
            ))

        if "model" not in primary_model:
            self.errors.append(ValidationError(
                field="primary_model",
                message="Primary model must have a 'model' field"
            ))

        if "temperature" in primary_model:
            temp = primary_model["temperature"]
            if not isinstance(temp, (int, float)) or temp < 0 or temp > 2:
                self.errors.append(ValidationError(
                    field="primary_model.temperature",
                    message="Temperature must be between 0 and 2"
                ))

        if "max_tokens" in primary_model:
            max_tokens = primary_model["max_tokens"]
            if not isinstance(max_tokens, int) or max_tokens < 1:
                self.errors.append(ValidationError(
                    field="primary_model.max_tokens",
                    message="max_tokens must be a positive integer"
                ))

    def _validate_fallback_models(self, llm_extensions: Dict[str, Any]) -> None:
        """Validate fallback_models field."""
        fallback_models = llm_extensions.get("fallback_models")

        if not fallback_models:
            return

        if not isinstance(fallback_models, list):
            self.errors.append(ValidationError(
                field="fallback_models",
                message="Fallback models must be an array"
            ))
            return

        for i, model in enumerate(fallback_models):
            if not isinstance(model, dict):
                self.errors.append(ValidationError(
                    field=f"fallback_models[{i}]",
                    message="Fallback model must be an object"
                ))
                continue

            if "provider" not in model:
                self.errors.append(ValidationError(
                    field=f"fallback_models[{i}]",
                    message="Fallback model must have a 'provider' field"
                ))
            elif model["provider"] not in self.VALID_PROVIDERS:
                self.errors.append(ValidationError(
                    field=f"fallback_models[{i}].provider",
                    message=f"Invalid provider: {model['provider']}. Must be one of {self.VALID_PROVIDERS}"
                ))

            if "model" not in model:
                self.errors.append(ValidationError(
                    field=f"fallback_models[{i}]",
                    message="Fallback model must have a 'model' field"
                ))

            if "priority" in model:
                priority = model["priority"]
                if not isinstance(priority, int) or priority < 1:
                    self.errors.append(ValidationError(
                        field=f"fallback_models[{i}].priority",
                        message="Priority must be a positive integer"
                    ))

            if "trigger_conditions" in model:
                conditions = model["trigger_conditions"]
                if not isinstance(conditions, list):
                    self.errors.append(ValidationError(
                        field=f"fallback_models[{i}].trigger_conditions",
                        message="Trigger conditions must be an array"
                    ))

    def _validate_specialized_models(self, llm_extensions: Dict[str, Any]) -> None:
        """Validate specialized_models field."""
        specialized_models = llm_extensions.get("specialized_models")

        if not specialized_models:
            return

        if not isinstance(specialized_models, list):
            self.errors.append(ValidationError(
                field="specialized_models",
                message="Specialized models must be an array"
            ))
            return

        for i, model in enumerate(specialized_models):
            if not isinstance(model, dict):
                self.errors.append(ValidationError(
                    field=f"specialized_models[{i}]",
                    message="Specialized model must be an object"
                ))
                continue

            if "name" not in model:
                self.errors.append(ValidationError(
                    field=f"specialized_models[{i}]",
                    message="Specialized model must have a 'name' field"
                ))

            if "provider" not in model:
                self.errors.append(ValidationError(
                    field=f"specialized_models[{i}]",
                    message="Specialized model must have a 'provider' field"
                ))
            elif model["provider"] not in self.VALID_PROVIDERS:
                self.errors.append(ValidationError(
                    field=f"specialized_models[{i}].provider",
                    message=f"Invalid provider: {model['provider']}. Must be one of {self.VALID_PROVIDERS}"
                ))

            if "model" not in model:
                self.errors.append(ValidationError(
                    field=f"specialized_models[{i}]",
                    message="Specialized model must have a 'model' field"
                ))

            if "task_types" in model:
                task_types = model["task_types"]
                if not isinstance(task_types, list):
                    self.errors.append(ValidationError(
                        field=f"specialized_models[{i}].task_types",
                        message="Task types must be an array"
                    ))

            if "cost_multiplier" in model:
                multiplier = model["cost_multiplier"]
                if not isinstance(multiplier, (int, float)) or multiplier <= 0:
                    self.errors.append(ValidationError(
                        field=f"specialized_models[{i}].cost_multiplier",
                        message="Cost multiplier must be a positive number"
                    ))

    def _validate_routing(self, llm_extensions: Dict[str, Any]) -> None:
        """Validate routing field."""
        routing = llm_extensions.get("routing")

        if not routing:
            return

        if not isinstance(routing, dict):
            self.errors.append(ValidationError(
                field="routing",
                message="Routing must be an object"
            ))
            return

        if "strategy" not in routing:
            self.errors.append(ValidationError(
                field="routing",
                message="Routing must have a 'strategy' field"
            ))
        else:
            strategy = routing["strategy"]
            if strategy not in self.VALID_ROUTING_STRATEGIES:
                self.errors.append(ValidationError(
                    field="routing.strategy",
                    message=f"Invalid routing strategy: {strategy}. Must be one of {self.VALID_ROUTING_STRATEGIES}"
                ))

        if "task_mappings" in routing:
            mappings = routing["task_mappings"]
            if not isinstance(mappings, dict):
                self.errors.append(ValidationError(
                    field="routing.task_mappings",
                    message="Task mappings must be an object"
                ))

        if "factors" in routing:
            factors = routing["factors"]
            if not isinstance(factors, dict):
                self.errors.append(ValidationError(
                    field="routing.factors",
                    message="Factors must be an object"
                ))
            else:
                total = sum(factors.values())
                if abs(total - 1.0) > 0.01:
                    self.errors.append(ValidationError(
                        field="routing.factors",
                        message=f"Factors must sum to 1.0, got {total}"
                    ))

    def _validate_model_constraints(self, llm_extensions: Dict[str, Any]) -> None:
        """Validate model_constraints field."""
        constraints = llm_extensions.get("model_constraints")

        if not constraints:
            return

        if not isinstance(constraints, dict):
            self.errors.append(ValidationError(
                field="model_constraints",
                message="Model constraints must be an object"
            ))
            return

        if "token_limits" in constraints:
            token_limits = constraints["token_limits"]
            if not isinstance(token_limits, dict):
                self.errors.append(ValidationError(
                    field="model_constraints.token_limits",
                    message="Token limits must be an object"
                ))
            else:
                if "max_input_tokens" in token_limits:
                    max_input = token_limits["max_input_tokens"]
                    if not isinstance(max_input, int) or max_input < 1:
                        self.errors.append(ValidationError(
                            field="model_constraints.token_limits.max_input_tokens",
                            message="max_input_tokens must be a positive integer"
                        ))

                if "max_output_tokens" in token_limits:
                    max_output = token_limits["max_output_tokens"]
                    if not isinstance(max_output, int) or max_output < 1:
                        self.errors.append(ValidationError(
                            field="model_constraints.token_limits.max_output_tokens",
                            message="max_output_tokens must be a positive integer"
                        ))

        if "cost_limits" in constraints:
            cost_limits = constraints["cost_limits"]
            if not isinstance(cost_limits, dict):
                self.errors.append(ValidationError(
                    field="model_constraints.cost_limits",
                    message="Cost limits must be an object"
                ))
            else:
                for limit_field in ["max_cost_per_task_usd", "max_cost_per_hour_usd", "max_cost_per_day_usd"]:
                    if limit_field in cost_limits:
                        limit = cost_limits[limit_field]
                        if not isinstance(limit, (int, float)) or limit <= 0:
                            self.errors.append(ValidationError(
                                field=f"model_constraints.cost_limits.{limit_field}",
                                message=f"{limit_field} must be a positive number"
                            ))

        if "rate_limits" in constraints:
            rate_limits = constraints["rate_limits"]
            if not isinstance(rate_limits, dict):
                self.errors.append(ValidationError(
                    field="model_constraints.rate_limits",
                    message="Rate limits must be an object"
                ))
            else:
                if "backoff_strategy" in rate_limits:
                    backoff = rate_limits["backoff_strategy"]
                    if backoff not in self.VALID_BACKOFF_STRATEGIES:
                        self.errors.append(ValidationError(
                            field="model_constraints.rate_limits.backoff_strategy",
                            message=f"Invalid backoff strategy: {backoff}. Must be one of {self.VALID_BACKOFF_STRATEGIES}"
                        ))

        if "timeout_limits" in constraints:
            timeout_limits = constraints["timeout_limits"]
            if not isinstance(timeout_limits, dict):
                self.errors.append(ValidationError(
                    field="model_constraints.timeout_limits",
                    message="Timeout limits must be an object"
                ))
            else:
                if "timeout_action" in timeout_limits:
                    action = timeout_limits["timeout_action"]
                    if action not in self.VALID_TIMEOUT_ACTIONS:
                        self.errors.append(ValidationError(
                            field="model_constraints.timeout_limits.timeout_action",
                            message=f"Invalid timeout action: {action}. Must be one of {self.VALID_TIMEOUT_ACTIONS}"
                        ))

    def _validate_model_configuration(self, llm_extensions: Dict[str, Any]) -> None:
        """Validate model_configuration field."""
        config = llm_extensions.get("model_configuration")

        if not config:
            return

        if not isinstance(config, dict):
            self.errors.append(ValidationError(
                field="model_configuration",
                message="Model configuration must be an object"
            ))
            return

        for param in ["temperature", "top_p", "frequency_penalty", "presence_penalty"]:
            if param in config:
                param_config = config[param]
                if not isinstance(param_config, dict):
                    self.errors.append(ValidationError(
                        field=f"model_configuration.{param}",
                        message=f"{param} configuration must be an object"
                    ))
                else:
                    if "default" in param_config:
                        default = param_config["default"]
                        if not isinstance(default, (int, float)) or default < 0 or default > 2:
                            self.errors.append(ValidationError(
                                field=f"model_configuration.{param}.default",
                                message=f"{param} default must be between 0 and 2"
                            ))

    def _validate_monitoring(self, llm_extensions: Dict[str, Any]) -> None:
        """Validate monitoring fields."""
        monitoring = llm_extensions.get("model_monitoring")

        if monitoring:
            if not isinstance(monitoring, dict):
                self.errors.append(ValidationError(
                    field="model_monitoring",
                    message="Model monitoring must be an object"
                ))
            elif "metrics" in monitoring:
                metrics = monitoring["metrics"]
                if not isinstance(metrics, list):
                    self.errors.append(ValidationError(
                        field="model_monitoring.metrics",
                        message="Metrics must be an array"
                    ))
                else:
                    for metric in metrics:
                        if metric not in self.VALID_METRICS:
                            self.errors.append(ValidationError(
                                field="model_monitoring.metrics",
                                message=f"Invalid metric: {metric}. Must be one of {self.VALID_METRICS}"
                            ))

        quality_monitoring = llm_extensions.get("quality_monitoring")

        if quality_monitoring:
            if not isinstance(quality_monitoring, dict):
                self.errors.append(ValidationError(
                    field="quality_monitoring",
                    message="Quality monitoring must be an object"
                ))
            elif "metrics" in quality_monitoring:
                metrics = quality_monitoring["metrics"]
                if not isinstance(metrics, list):
                    self.errors.append(ValidationError(
                        field="quality_monitoring.metrics",
                        message="Metrics must be an array"
                    ))
                else:
                    for metric in metrics:
                        if metric not in self.VALID_QUALITY_METRICS:
                            self.errors.append(ValidationError(
                                field="quality_monitoring.metrics",
                                message=f"Invalid quality metric: {metric}. Must be one of {self.VALID_QUALITY_METRICS}"
                            ))

    def _validate_alerting(self, llm_extensions: Dict[str, Any]) -> None:
        """Validate alerting field."""
        alerting = llm_extensions.get("alerting")

        if not alerting:
            return

        if not isinstance(alerting, dict):
            self.errors.append(ValidationError(
                field="alerting",
                message="Alerting must be an object"
            ))
            return

        if "enabled" in alerting and alerting["enabled"]:
            if "alerts" not in alerting:
                self.errors.append(ValidationError(
                    field="alerting",
                    message="Enabled alerting must have an 'alerts' field"
                ))
            elif not isinstance(alerting["alerts"], list):
                self.errors.append(ValidationError(
                    field="alerting.alerts",
                    message="Alerts must be an array"
                ))
            else:
                for i, alert in enumerate(alerting["alerts"]):
                    if not isinstance(alert, dict):
                        self.errors.append(ValidationError(
                            field=f"alerting.alerts[{i}]",
                            message="Alert must be an object"
                        ))
                        continue

                    if "metric" not in alert:
                        self.errors.append(ValidationError(
                            field=f"alerting.alerts[{i}]",
                            message="Alert must have a 'metric' field"
                        ))

                    if "threshold" not in alert:
                        self.errors.append(ValidationError(
                            field=f"alerting.alerts[{i}]",
                            message="Alert must have a 'threshold' field"
                        ))

                    if "operator" in alert:
                        operator = alert["operator"]
                        if operator not in self.VALID_OPERATORS:
                            self.errors.append(ValidationError(
                                field=f"alerting.alerts[{i}].operator",
                                message=f"Invalid operator: {operator}. Must be one of {self.VALID_OPERATORS}"
                            ))

                    if "channels" in alert:
                        channels = alert["channels"]
                        if not isinstance(channels, list):
                            self.errors.append(ValidationError(
                                field=f"alerting.alerts[{i}].channels",
                                message="Channels must be an array"
                            ))
                        else:
                            for channel in channels:
                                if channel not in self.VALID_CHANNELS:
                                    self.errors.append(ValidationError(
                                        field=f"alerting.alerts[{i}].channels",
                                        message=f"Invalid channel: {channel}. Must be one of {self.VALID_CHANNELS}"
                                    ))


def validate_llm_extensions(llm_extensions: Dict[str, Any]) -> List[ValidationError]:
    """Validate LLM settings extensions configuration."""
    validator = LLMSettingsValidator()
    return validator.validate(llm_extensions)
