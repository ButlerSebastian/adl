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
        self.warnings: List[ValidationError] = []

    def _is_hierarchical_id(self, id_str: str) -> bool:
        """Check if ID follows hierarchical format (e.g., 'org.team.component')."""
        import re
        pattern = r'^[a-zA-Z_][a-zA-Z0-9_]*(\.[a-zA-Z_][a-zA-Z0-9_]*)*$'
        return bool(re.match(pattern, id_str))

    def _add_deprecation_warning(self, field: str, old_field: str, new_field: str) -> None:
        """Add deprecation warning for old field name."""
        self.warnings.append(ValidationError(
            field=field,
            message=f"Field '{old_field}' is deprecated. Use '{new_field}' instead.",
            severity="warning"
        ))

    def validate(self, workflow: Dict[str, Any]) -> tuple[List[ValidationError], List[ValidationError]]:
        """Validate workflow configuration. Returns (errors, warnings)."""
        self.errors = []

        if not workflow:
            return [], []

        self._validate_structure(workflow)
        self._validate_nodes(workflow)
        self._validate_edges(workflow)
        self._validate_cycles(workflow)
        self._validate_connections(workflow)

        return self.errors, self.warnings

    def _validate_structure(self, workflow: Dict[str, Any]) -> None:
        """Validate workflow structure."""
        workflow_id = workflow.get("workflow_id") or workflow.get("id")
        if not workflow_id:
            self.errors.append(ValidationError(
                field="workflow_id",
                message="Workflow must have a 'workflow_id' field (or 'id' for backward compatibility)"
            ))
        else:
            if "id" in workflow and "workflow_id" not in workflow:
                self._add_deprecation_warning("workflow", "id", "workflow_id")

            if not self._is_hierarchical_id(workflow_id):
                self.warnings.append(ValidationError(
                    field="workflow_id",
                    message=f"Workflow ID '{workflow_id}' does not follow hierarchical format (e.g., 'org.team.component'). Consider using hierarchical IDs for better organization.",
                    severity="warning"
                ))

            required_fields = ["name", "version", "nodes", "edges"]
            for field in required_fields:
                if field not in workflow:
                    self.errors.append(ValidationError(
                        field=field,
                        message=f"Workflow must have a '{field}' field"
                    ))

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

            if node_id in node_ids:
                self.errors.append(ValidationError(
                    field=f"nodes.{node_id}",
                    message=f"Duplicate node ID: '{node_id}'"
                ))
            node_ids.add(node_id)

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
            self.errors.append(ValidationError(
                field="edges",
                message="Workflow must have an 'edges' field"
            ))
            return

        if not isinstance(edges, list):
            self.errors.append(ValidationError(
                field="edges",
                message="Edges must be an array"
            ))
            return

        if len(edges) == 0:
            self.errors.append(ValidationError(
                field="edges",
                message="Workflow must have at least one edge"
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

            edge_id = edge.get("edge_id") or edge.get("id")
            if edge_id:
                if edge_id in edge_ids:
                    self.errors.append(ValidationError(
                        field=f"edges[{i}].edge_id",
                        message=f"Duplicate edge ID: '{edge_id}'"
                    ))
                edge_ids.add(edge_id)

                if "id" in edge and "edge_id" not in edge:
                    self._add_deprecation_warning(f"edges[{i}]", "id", "edge_id")

                if not self._is_hierarchical_id(edge_id):
                    self.warnings.append(ValidationError(
                        field=f"edges[{i}].edge_id",
                        message=f"Edge ID '{edge_id}' does not follow hierarchical format (e.g., 'org.team.component'). Consider using hierarchical IDs for better organization.",
                        severity="warning"
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

            if "relation" in edge:
                relation = edge["relation"]
                if relation not in self.VALID_EDGE_RELATIONS:
                    self.errors.append(ValidationError(
                        field=f"edges[{i}].relation",
                        message=f"Invalid edge relation: '{relation}'. Must be one of {self.VALID_EDGE_RELATIONS}"
                    ))

    def _validate_cycles(self, workflow: Dict[str, Any]) -> None:
        """Detect cycles using DFS and report detailed cycle paths."""
        nodes = workflow.get("nodes", {})
        edges = workflow.get("edges", [])

        if not nodes or not edges:
            return

        # Build adjacency list from edges
        adj = {node_id: [] for node_id in nodes}
        for edge in edges:
            source = edge.get("source")
            target = edge.get("target")

            if source and target and source in nodes and target in nodes:
                adj[source].append(target)

        # DFS with visited and recursion stack to detect cycles
        visited = set()
        rec_stack = set()
        path = []

        def dfs(node):
            """DFS traversal to detect cycles."""
            visited.add(node)
            rec_stack.add(node)
            path.append(node)

            for neighbor in adj.get(node, []):
                if neighbor not in visited:
                    if dfs(neighbor):
                        return True
                elif neighbor in rec_stack:
                    # Cycle found - extract the cycle path
                    cycle_start = path.index(neighbor)
                    cycle = path[cycle_start:] + [neighbor]
                    self.errors.append(ValidationError(
                        field="workflow",
                        message=f"Cycle detected in workflow: {' -> '.join(cycle)}"
                    ))
                    return True

            rec_stack.remove(node)
            path.pop()
            return False

        # Run DFS from each unvisited node
        for node in nodes:
            if node not in visited:
                dfs(node)

        # Also check for cycles in the reverse direction (edges might be bidirectional)
        # Build reverse adjacency list
        reverse_adj = defaultdict(list)
        for edge in edges:
            source = edge.get("source")
            target = edge.get("target")

            if source and target and source in nodes and target in nodes:
                reverse_adj[target].append(source)

        # Reset visited for reverse traversal
        visited = set()
        rec_stack = set()
        path = []

        def dfs_reverse(node):
            """DFS traversal on reverse graph to detect cycles."""
            visited.add(node)
            rec_stack.add(node)
            path.append(node)

            for neighbor in reverse_adj.get(node, []):
                if neighbor not in visited:
                    if dfs_reverse(neighbor):
                        return True
                elif neighbor in rec_stack:
                    # Cycle found in reverse direction
                    cycle_start = path.index(neighbor)
                    cycle = path[cycle_start:] + [neighbor]
                    self.errors.append(ValidationError(
                        field="workflow",
                        message=f"Cycle detected in workflow (reverse): {' -> '.join(cycle)}"
                    ))
                    return True

            rec_stack.remove(node)
            path.pop()
            return False

        # Run DFS on reverse graph
        for node in nodes:
            if node not in visited:
                dfs_reverse(node)

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

            if source and target:
                source_node = nodes.get(source, {})
                target_node = nodes.get(target, {})

                source_type = source_node.get("type")
                target_type = target_node.get("type")

                if target_type == "trigger":
                    self.errors.append(ValidationError(
                        field=f"edges[{i}]",
                        message=f"Trigger node '{target}' cannot have incoming edges"
                    ))

                if source_type == "output":
                    self.errors.append(ValidationError(
                        field=f"edges[{i}]",
                        message=f"Output node '{source}' cannot have outgoing edges"
                    ))

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
