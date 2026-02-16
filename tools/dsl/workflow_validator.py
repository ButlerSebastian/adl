"""
Workflow Validation

Validates workflow field in ADL v3 agent definitions.
"""

from typing import List, Dict, Any, Set, Tuple
from dataclasses import dataclass
from collections import defaultdict, deque


@dataclass
class ValidationError:
    """Represents a validation error."""

    field: str
    message: str
    severity: str = "error"


class WorkflowValidator:
    """Validator for workflow configurations."""

    VALID_NODE_TYPES = [
        "trigger", "input", "transform", "action",
        "condition", "loop", "output", "sub_workflow", "annotation"
    ]
    VALID_EDGE_RELATIONS = [
        "data_flow", "control_flow", "error_flow",
        "ai_languageModel", "ai_tool", "dependency"
    ]

    def __init__(self):
        self.errors: List[ValidationError] = []

    def validate(self, workflow: Dict[str, Any]) -> List[ValidationError]:
        """Validate workflow configuration."""
        self.errors = []

        if not workflow:
            return []

        self._validate_structure(workflow)
        self._validate_nodes(workflow)
        self._validate_edges(workflow)
        self._validate_cycles(workflow)
        self._validate_connections(workflow)

        return self.errors

    def _validate_structure(self, workflow: Dict[str, Any]) -> None:
        """Validate workflow structure."""
        required_fields = ["id", "name", "version", "nodes", "edges"]
        for field in required_fields:
            if field not in workflow:
                self.errors.append(ValidationError(
                    field=field,
                    message=f"Workflow must have a '{field}' field"
                ))

        # Validate version format
        if "version" in workflow:
            version = workflow["version"]
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

    def _validate_nodes(self, workflow: Dict[str, Any]) -> None:
        """Validate nodes field."""
        nodes = workflow.get("nodes")

        if not nodes:
            self.errors.append(ValidationError(
                field="nodes",
                message="Workflow must have a 'nodes' field"
            ))
            return

        if not isinstance(nodes, dict):
            self.errors.append(ValidationError(
                field="nodes",
                message="Nodes must be an object"
            ))
            return

        if len(nodes) == 0:
            self.errors.append(ValidationError(
                field="nodes",
                message="Workflow must have at least one node"
            ))
            return

        node_ids = set()
        for node_id, node in nodes.items():
            if not isinstance(node, dict):
                self.errors.append(ValidationError(
                    field=f"nodes.{node_id}",
                    message=f"Node '{node_id}' must be an object"
                ))
                continue

            # Check for duplicate IDs
            if node_id in node_ids:
                self.errors.append(ValidationError(
                    field=f"nodes.{node_id}",
                    message=f"Duplicate node ID: '{node_id}'"
                ))
            node_ids.add(node_id)

            # Validate node structure
            if "id" not in node:
                self.errors.append(ValidationError(
                    field=f"nodes.{node_id}",
                    message=f"Node '{node_id}' must have an 'id' field"
                ))

            if "type" not in node:
                self.errors.append(ValidationError(
                    field=f"nodes.{node_id}",
                    message=f"Node '{node_id}' must have a 'type' field"
                ))
            else:
                node_type = node["type"]
                if node_type not in self.VALID_NODE_TYPES:
                    self.errors.append(ValidationError(
                        field=f"nodes.{node_id}.type",
                        message=f"Invalid node type: '{node_type}'. Must be one of {self.VALID_NODE_TYPES}"
                    ))

            if "label" not in node:
                self.errors.append(ValidationError(
                    field=f"nodes.{node_id}",
                    message=f"Node '{node_id}' must have a 'label' field"
                ))

            # Validate position if present
            if "position" in node:
                position = node["position"]
                if not isinstance(position, dict):
                    self.errors.append(ValidationError(
                        field=f"nodes.{node_id}.position",
                        message="Position must be an object"
                    ))
                else:
                    if "x" in position and not isinstance(position["x"], (int, float)):
                        self.errors.append(ValidationError(
                            field=f"nodes.{node_id}.position.x",
                            message="Position x must be a number"
                        ))
                    if "y" in position and not isinstance(position["y"], (int, float)):
                        self.errors.append(ValidationError(
                            field=f"nodes.{node_id}.position.y",
                            message="Position y must be a number"
                        ))

    def _validate_edges(self, workflow: Dict[str, Any]) -> None:
        """Validate edges field."""
        edges = workflow.get("edges")

        if not edges:
            return

        if not isinstance(edges, list):
            self.errors.append(ValidationError(
                field="edges",
                message="Edges must be an array"
            ))
            return

        edge_ids = set()
        for i, edge in enumerate(edges):
            if not isinstance(edge, dict):
                self.errors.append(ValidationError(
                    field=f"edges[{i}]",
                    message="Edge must be an object"
                ))
                continue

            # Check for duplicate IDs
            edge_id = edge.get("id")
            if edge_id:
                if edge_id in edge_ids:
                    self.errors.append(ValidationError(
                        field=f"edges[{i}].id",
                        message=f"Duplicate edge ID: '{edge_id}'"
                    ))
                edge_ids.add(edge_id)

            # Validate edge structure
            if "id" not in edge:
                self.errors.append(ValidationError(
                    field=f"edges[{i}]",
                    message="Edge must have an 'id' field"
                ))

            if "source" not in edge:
                self.errors.append(ValidationError(
                    field=f"edges[{i}]",
                    message="Edge must have a 'source' field"
                ))

            if "target" not in edge:
                self.errors.append(ValidationError(
                    field=f"edges[{i}]",
                    message="Edge must have a 'target' field"
                ))

            # Validate relation if present
            if "relation" in edge:
                relation = edge["relation"]
                if relation not in self.VALID_EDGE_RELATIONS:
                    self.errors.append(ValidationError(
                        field=f"edges[{i}].relation",
                        message=f"Invalid edge relation: '{relation}'. Must be one of {self.VALID_EDGE_RELATIONS}"
                    ))

    def _validate_cycles(self, workflow: Dict[str, Any]) -> None:
        """Detect cycles using Kahn's algorithm."""
        nodes = workflow.get("nodes", {})
        edges = workflow.get("edges", [])

        if not nodes or not edges:
            return

        # Build adjacency list and in-degree count
        adjacency = defaultdict(list)
        in_degree = {node_id: 0 for node_id in nodes}

        for edge in edges:
            source = edge.get("source")
            target = edge.get("target")

            if source and target and source in nodes and target in nodes:
                adjacency[source].append(target)
                in_degree[target] += 1

        # Find all nodes with no incoming edges
        queue = deque([node_id for node_id, degree in in_degree.items() if degree == 0])
        result = []

        while queue:
            current = queue.popleft()
            result.append(current)

            for neighbor in adjacency[current]:
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:
                    queue.append(neighbor)

        # If we didn't process all nodes, there's a cycle
        if len(result) != len(nodes):
            # Find nodes in the cycle
            cycle_nodes = set(nodes.keys()) - set(result)
            self.errors.append(ValidationError(
                field="workflow",
                message=f"Workflow contains a cycle involving nodes: {', '.join(sorted(cycle_nodes))}"
            ))

    def _validate_connections(self, workflow: Dict[str, Any]) -> None:
        """Validate edge connections."""
        nodes = workflow.get("nodes", {})
        edges = workflow.get("edges", [])

        if not nodes or not edges:
            return

        node_ids = set(nodes.keys())

        for i, edge in enumerate(edges):
            source = edge.get("source")
            target = edge.get("target")

            # Check if source and target exist
            if source and source not in node_ids:
                self.errors.append(ValidationError(
                    field=f"edges[{i}].source",
                    message=f"Edge source '{source}' does not exist in nodes"
                ))

            if target and target not in node_ids:
                self.errors.append(ValidationError(
                    field=f"edges[{i}].target",
                    message=f"Edge target '{target}' does not exist in nodes"
                ))

            # Validate trigger nodes (no incoming edges)
            if source and target:
                source_node = nodes.get(source, {})
                target_node = nodes.get(target, {})

                source_type = source_node.get("type")
                target_type = target_node.get("type")

                # Trigger nodes should not have incoming edges
                if target_type == "trigger":
                    self.errors.append(ValidationError(
                        field=f"edges[{i}]",
                        message=f"Trigger node '{target}' cannot have incoming edges"
                    ))

                # Output nodes should not have outgoing edges
                if source_type == "output":
                    self.errors.append(ValidationError(
                        field=f"edges[{i}]",
                        message=f"Output node '{source}' cannot have outgoing edges"
                    ))

                # Condition nodes should have at least 2 outgoing edges
                if source_type == "condition":
                    outgoing_edges = [
                        e for e in edges
                        if e.get("source") == source
                    ]
                    if len(outgoing_edges) < 2:
                        self.errors.append(ValidationError(
                            field=f"nodes.{source}",
                            message=f"Condition node '{source}' must have at least 2 outgoing edges"
                        ))

    def _is_semantic_version(self, version: str) -> bool:
        """Check if version follows semantic versioning."""
        import re
        pattern = r'^\d+\.\d+\.\d+(-[a-zA-Z0-9.]+)?$'
        return bool(re.match(pattern, version))


def validate_workflow(workflow: Dict[str, Any]) -> List[ValidationError]:
    """Validate workflow configuration."""
    validator = WorkflowValidator()
    return validator.validate(workflow)
