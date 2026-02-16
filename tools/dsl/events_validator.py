"""
Event-Driven Tool Invocation Validation

Validates events field in ADL v2 agent definitions.
"""

from typing import List, Dict, Any, Optional
from dataclasses import dataclass


@dataclass
class ValidationError:
    """Represents a validation error."""

    field: str
    message: str
    severity: str = "error"


class EventsValidator:
    """Validator for event-driven tool invocation configurations."""

    VALID_TRIGGER_TYPES = ["event", "time", "condition", "composite"]
    VALID_CONDITION_OPERATORS = ["equals", "not_equals", "greater_than", "less_than", "contains"]
    VALID_COMPOSITE_OPERATORS = ["and", "or"]
    VALID_HANDLER_TYPES = ["tool_invocation", "state_update", "notification", "custom"]
    VALID_NOTIFICATION_TYPES = ["alert", "info", "warning", "error"]
    VALID_SUBSCRIPTION_TYPES = ["direct", "pattern", "filtered"]
    VALID_ROUTING_STRATEGIES = ["direct", "broadcast", "conditional"]
    VALID_PROCESSING_MODES = ["synchronous", "asynchronous", "batch"]
    VALID_PERSISTENCE_TYPES = ["memory", "file", "database"]
    VALID_ROTATION_POLICIES = ["daily", "weekly", "monthly"]

    def __init__(self):
        self.errors: List[ValidationError] = []

    def validate(self, events: Dict[str, Any]) -> List[ValidationError]:
        """Validate events configuration."""
        self.errors = []

        if not events:
            return []

        self._validate_triggers(events)
        self._validate_handlers(events)
        self._validate_subscriptions(events)
        self._validate_routing_strategy(events)
        self._validate_processing_mode(events)
        self._validate_persistence(events)

        return self.errors

    def _validate_triggers(self, events: Dict[str, Any]) -> None:
        """Validate triggers field."""
        triggers = events.get("triggers")

        if not triggers:
            return

        if not isinstance(triggers, list):
            self.errors.append(ValidationError(
                field="triggers",
                message="Triggers must be an array"
            ))
            return

        for i, trigger in enumerate(triggers):
            if not isinstance(trigger, dict):
                self.errors.append(ValidationError(
                    field=f"triggers[{i}]",
                    message="Trigger must be an object"
                ))
                continue

            if "trigger_type" not in trigger:
                self.errors.append(ValidationError(
                    field=f"triggers[{i}]",
                    message="Trigger must have a 'trigger_type' field"
                ))
                continue

            trigger_type = trigger["trigger_type"]
            if trigger_type not in self.VALID_TRIGGER_TYPES:
                self.errors.append(ValidationError(
                    field=f"triggers[{i}].trigger_type",
                    message=f"Invalid trigger_type: {trigger_type}. Must be one of {self.VALID_TRIGGER_TYPES}"
                ))

            if trigger_type == "event" and "event_name" not in trigger:
                self.errors.append(ValidationError(
                    field=f"triggers[{i}]",
                    message="Event trigger must have an 'event_name' field"
                ))

            if trigger_type == "time" and "schedule" not in trigger:
                self.errors.append(ValidationError(
                    field=f"triggers[{i}]",
                    message="Time trigger must have a 'schedule' field"
                ))

            if trigger_type == "condition" and "condition" not in trigger:
                self.errors.append(ValidationError(
                    field=f"triggers[{i}]",
                    message="Condition trigger must have a 'condition' field"
                ))

            if "condition" in trigger:
                self._validate_condition(f"triggers[{i}].condition", trigger["condition"])

            if trigger_type == "composite":
                if "operator" not in trigger:
                    self.errors.append(ValidationError(
                        field=f"triggers[{i}]",
                        message="Composite trigger must have an 'operator' field"
                    ))
                elif trigger["operator"] not in self.VALID_COMPOSITE_OPERATORS:
                    self.errors.append(ValidationError(
                        field=f"triggers[{i}].operator",
                        message=f"Invalid operator: {trigger['operator']}. Must be one of {self.VALID_COMPOSITE_OPERATORS}"
                    ))

                if "triggers" not in trigger:
                    self.errors.append(ValidationError(
                        field=f"triggers[{i}]",
                        message="Composite trigger must have a 'triggers' field"
                    ))

    def _validate_condition(self, field: str, condition: Dict[str, Any]) -> None:
        """Validate condition object."""
        if not isinstance(condition, dict):
            self.errors.append(ValidationError(
                field=field,
                message="Condition must be an object"
            ))
            return

        if "field" not in condition:
            self.errors.append(ValidationError(
                field=field,
                message="Condition must have a 'field' field"
            ))

        if "operator" not in condition:
            self.errors.append(ValidationError(
                field=field,
                message="Condition must have an 'operator' field"
            ))
        elif condition["operator"] not in self.VALID_CONDITION_OPERATORS:
            self.errors.append(ValidationError(
                field=f"{field}.operator",
                message=f"Invalid operator: {condition['operator']}. Must be one of {self.VALID_CONDITION_OPERATORS}"
            ))

    def _validate_handlers(self, events: Dict[str, Any]) -> None:
        """Validate handlers field."""
        handlers = events.get("handlers")

        if not handlers:
            return

        if not isinstance(handlers, list):
            self.errors.append(ValidationError(
                field="handlers",
                message="Handlers must be an array"
            ))
            return

        for i, handler in enumerate(handlers):
            if not isinstance(handler, dict):
                self.errors.append(ValidationError(
                    field=f"handlers[{i}]",
                    message="Handler must be an object"
                ))
                continue

            if "handler_type" not in handler:
                self.errors.append(ValidationError(
                    field=f"handlers[{i}]",
                    message="Handler must have a 'handler_type' field"
                ))
                continue

            handler_type = handler["handler_type"]
            if handler_type not in self.VALID_HANDLER_TYPES:
                self.errors.append(ValidationError(
                    field=f"handlers[{i}].handler_type",
                    message=f"Invalid handler_type: {handler_type}. Must be one of {self.VALID_HANDLER_TYPES}"
                ))

            if handler_type == "tool_invocation" and "tool_name" not in handler:
                self.errors.append(ValidationError(
                    field=f"handlers[{i}]",
                    message="Tool invocation handler must have a 'tool_name' field"
                ))

            if handler_type == "state_update" and "state_field" not in handler:
                self.errors.append(ValidationError(
                    field=f"handlers[{i}]",
                    message="State update handler must have a 'state_field' field"
                ))

            if handler_type == "notification":
                if "notification_type" not in handler:
                    self.errors.append(ValidationError(
                        field=f"handlers[{i}]",
                        message="Notification handler must have a 'notification_type' field"
                    ))
                elif handler["notification_type"] not in self.VALID_NOTIFICATION_TYPES:
                    self.errors.append(ValidationError(
                        field=f"handlers[{i}].notification_type",
                        message=f"Invalid notification_type: {handler['notification_type']}. Must be one of {self.VALID_NOTIFICATION_TYPES}"
                    ))

                if "message" not in handler:
                    self.errors.append(ValidationError(
                        field=f"handlers[{i}]",
                        message="Notification handler must have a 'message' field"
                    ))

    def _validate_subscriptions(self, events: Dict[str, Any]) -> None:
        """Validate subscriptions field."""
        subscriptions = events.get("subscriptions")

        if not subscriptions:
            return

        if not isinstance(subscriptions, list):
            self.errors.append(ValidationError(
                field="subscriptions",
                message="Subscriptions must be an array"
            ))
            return

        for i, subscription in enumerate(subscriptions):
            if not isinstance(subscription, dict):
                self.errors.append(ValidationError(
                    field=f"subscriptions[{i}]",
                    message="Subscription must be an object"
                ))
                continue

            if "subscription_type" not in subscription:
                self.errors.append(ValidationError(
                    field=f"subscriptions[{i}]",
                    message="Subscription must have a 'subscription_type' field"
                ))
                continue

            subscription_type = subscription["subscription_type"]
            if subscription_type not in self.VALID_SUBSCRIPTION_TYPES:
                self.errors.append(ValidationError(
                    field=f"subscriptions[{i}].subscription_type",
                    message=f"Invalid subscription_type: {subscription_type}. Must be one of {self.VALID_SUBSCRIPTION_TYPES}"
                ))

            if subscription_type == "direct" and "event_name" not in subscription:
                self.errors.append(ValidationError(
                    field=f"subscriptions[{i}]",
                    message="Direct subscription must have an 'event_name' field"
                ))

            if subscription_type == "pattern" and "event_pattern" not in subscription:
                self.errors.append(ValidationError(
                    field=f"subscriptions[{i}]",
                    message="Pattern subscription must have an 'event_pattern' field"
                ))

            if "filter" in subscription:
                self._validate_condition(f"subscriptions[{i}].filter", subscription["filter"])

            if "handler" not in subscription:
                self.errors.append(ValidationError(
                    field=f"subscriptions[{i}]",
                    message="Subscription must have a 'handler' field"
                ))

    def _validate_routing_strategy(self, events: Dict[str, Any]) -> None:
        """Validate routing_strategy field."""
        routing_strategy = events.get("routing_strategy")

        if not routing_strategy:
            return

        if routing_strategy not in self.VALID_ROUTING_STRATEGIES:
            self.errors.append(ValidationError(
                field="routing_strategy",
                message=f"Invalid routing_strategy: {routing_strategy}. Must be one of {self.VALID_ROUTING_STRATEGIES}"
            ))

    def _validate_processing_mode(self, events: Dict[str, Any]) -> None:
        """Validate processing_mode field."""
        processing_mode = events.get("processing_mode")

        if not processing_mode:
            return

        if processing_mode not in self.VALID_PROCESSING_MODES:
            self.errors.append(ValidationError(
                field="processing_mode",
                message=f"Invalid processing_mode: {processing_mode}. Must be one of {self.VALID_PROCESSING_MODES}"
            ))

    def _validate_persistence(self, events: Dict[str, Any]) -> None:
        """Validate persistence field."""
        persistence = events.get("persistence")

        if not persistence:
            return

        if not isinstance(persistence, dict):
            self.errors.append(ValidationError(
                field="persistence",
                message="Persistence must be an object"
            ))
            return

        if "type" not in persistence:
            self.errors.append(ValidationError(
                field="persistence",
                message="Persistence must have a 'type' field"
            ))
            return

        persistence_type = persistence["type"]
        if persistence_type not in self.VALID_PERSISTENCE_TYPES:
            self.errors.append(ValidationError(
                field="persistence.type",
                message=f"Invalid persistence type: {persistence_type}. Must be one of {self.VALID_PERSISTENCE_TYPES}"
            ))

        if persistence_type == "memory" and "max_events" in persistence:
            max_events = persistence["max_events"]
            if not isinstance(max_events, int) or max_events < 1:
                self.errors.append(ValidationError(
                    field="persistence.max_events",
                    message="max_events must be a positive integer"
                ))

        if persistence_type == "file":
            if "file_path" not in persistence:
                self.errors.append(ValidationError(
                    field="persistence",
                    message="File persistence must have a 'file_path' field"
                ))

            if "rotation" in persistence and persistence["rotation"] not in self.VALID_ROTATION_POLICIES:
                self.errors.append(ValidationError(
                    field="persistence.rotation",
                    message=f"Invalid rotation policy: {persistence['rotation']}. Must be one of {self.VALID_ROTATION_POLICIES}"
                ))

        if persistence_type == "database":
            if "connection_string" not in persistence:
                self.errors.append(ValidationError(
                    field="persistence",
                    message="Database persistence must have a 'connection_string' field"
                ))

            if "table_name" not in persistence:
                self.errors.append(ValidationError(
                    field="persistence",
                    message="Database persistence must have a 'table_name' field"
                ))


def validate_events(events: Dict[str, Any]) -> List[ValidationError]:
    """Validate events configuration."""
    validator = EventsValidator()
    return validator.validate(events)
