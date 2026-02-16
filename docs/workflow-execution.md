# Workflow Execution Guide

## Overview

This guide explains how ADL v3 workflows are executed, including execution semantics, error handling, retry logic, and best practices for production use.

## Execution Model

### 1. Topological Execution Order

Workflows are executed in topological order to ensure dependencies are satisfied:

```python
# Execution order for sequential workflow
# Input → Transform → Validate → Output

# Execution order for parallel workflow
# Input → [Process A, Process B, Process C] → Merge → Output
# (A, B, C execute in parallel)
```

### 2. Parallel Execution Levels

Nodes with no dependencies execute in parallel:

```python
# Parallel levels for parallel workflow
# Level 0: [Input]
# Level 1: [Process A, Process B, Process C]  # Parallel
# Level 2: [Merge]
# Level 3: [Output]
```

### 3. Conditional Execution

Edges with conditions control execution flow:

```python
# Conditional execution
# Condition node evaluates expression
# Only matching edges are traversed
# Other branches are skipped
```

## Execution Semantics

### 1. Node Execution

Each node executes independently:

```python
def execute_node(node, input_data):
    """Execute a single workflow node."""
    node_type = node["type"]
    config = node["config"]
    
    if node_type == "input":
        return execute_input(config, input_data)
    elif node_type == "transform":
        return execute_transform(config, input_data)
    elif node_type == "action":
        return execute_action(config, input_data)
    elif node_type == "condition":
        return execute_condition(config, input_data)
    # ... other node types
```

### 2. Data Flow

Data flows through edges:

```python
def propagate_data(source_node, target_node, edge, data):
    """Propagate data from source to target."""
    relation = edge.get("relation", "data_flow")
    
    if relation == "data_flow":
        # Pass data directly
        return data
    elif relation == "control_flow":
        # No data flow, just control
        return None
    elif relation == "error_flow":
        # Pass error data
        return {"error": data.get("error")}
    # ... other relations
```

### 3. State Management

Workflow state is tracked during execution:

```python
class WorkflowState:
    """Track workflow execution state."""
    
    def __init__(self, workflow):
        self.workflow = workflow
        self.completed_nodes = set()
        self.failed_nodes = set()
        self.node_outputs = {}
        self.execution_order = []
    
    def mark_completed(self, node_id, output):
        """Mark node as completed."""
        self.completed_nodes.add(node_id)
        self.node_outputs[node_id] = output
        self.execution_order.append(node_id)
    
    def mark_failed(self, node_id, error):
        """Mark node as failed."""
        self.failed_nodes.add(node_id)
        self.node_outputs[node_id] = {"error": str(error)}
```

## Error Handling

### 1. Error Flow Edges

Error-flow edges handle failures:

```json
{
  "id": "edge-error",
  "source": "process-node",
  "target": "error-handler",
  "relation": "error_flow"
}
```

### 2. Error Propagation

Errors propagate through error-flow edges:

```python
def handle_error(node_id, error, state):
    """Handle node execution error."""
    # Find error-flow edges from this node
    error_edges = [
        edge for edge in state.workflow["edges"]
        if edge["source"] == node_id and edge["relation"] == "error_flow"
    ]
    
    if error_edges:
        # Propagate to error handlers
        for edge in error_edges:
            target_id = edge["target"]
            execute_node(target_id, {"error": str(error)})
    else:
        # No error handler, fail workflow
        raise WorkflowError(f"Node {node_id} failed: {error}")
```

### 3. Error Recovery

Error handlers can recover from failures:

```python
def execute_error_handler(node, error_data):
    """Execute error handler node."""
    config = node["config"]
    action = config.get("action", "log")
    
    if action == "retry":
        # Retry the failed operation
        max_retries = config.get("max_retries", 3)
        return retry_operation(error_data, max_retries)
    elif action == "alert":
        # Send alert
        send_alert(config, error_data)
    elif action == "skip":
        # Skip and continue
        return None
```

## Retry Logic

### 1. Retry Configuration

Nodes can have retry policies:

```json
{
  "id": "retry-node",
  "type": "action",
  "label": "API Call",
  "config": {
    "action": "api_call",
    "retry_policy": {
      "max_retries": 3,
      "backoff_ms": 1000,
      "backoff_multiplier": 2
    }
  }
}
```

### 2. Exponential Backoff

Retries use exponential backoff:

```python
def execute_with_retry(node, input_data):
    """Execute node with retry logic."""
    config = node["config"]
    retry_policy = config.get("retry_policy", {})
    
    max_retries = retry_policy.get("max_retries", 0)
    backoff_ms = retry_policy.get("backoff_ms", 1000)
    multiplier = retry_policy.get("backoff_multiplier", 2)
    
    for attempt in range(max_retries + 1):
        try:
            return execute_node(node, input_data)
        except Exception as e:
            if attempt < max_retries:
                delay = backoff_ms * (multiplier ** attempt)
                time.sleep(delay / 1000)
            else:
                raise
```

## Execution Modes

### 1. Synchronous Execution

Default mode - execute sequentially:

```python
def execute_workflow_sync(workflow, input_data):
    """Execute workflow synchronously."""
    state = WorkflowState(workflow)
    execution_order = topological_sort(workflow)
    
    for node_id in execution_order:
        node = workflow["nodes"][node_id]
        input_for_node = get_input_for_node(node_id, state)
        
        try:
            output = execute_node(node, input_for_node)
            state.mark_completed(node_id, output)
        except Exception as e:
            state.mark_failed(node_id, e)
            handle_error(node_id, e, state)
    
    return state
```

### 2. Asynchronous Execution

Execute nodes concurrently:

```python
async def execute_workflow_async(workflow, input_data):
    """Execute workflow asynchronously."""
    state = WorkflowState(workflow)
    levels = get_parallel_levels(workflow)
    
    for level in levels:
        # Execute all nodes in this level in parallel
        tasks = [
            execute_node_async(workflow["nodes"][node_id], input_data)
            for node_id in level
        ]
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        for node_id, result in zip(level, results):
            if isinstance(result, Exception):
                state.mark_failed(node_id, result)
                handle_error(node_id, result, state)
            else:
                state.mark_completed(node_id, result)
    
    return state
```

### 3. Batch Execution

Execute multiple workflows in batch:

```python
def execute_workflow_batch(workflows, input_data):
    """Execute multiple workflows in batch."""
    results = []
    
    for workflow in workflows:
        try:
            state = execute_workflow_sync(workflow, input_data)
            results.append({
                "workflow_id": workflow["id"],
                "status": "success",
                "state": state
            })
        except Exception as e:
            results.append({
                "workflow_id": workflow["id"],
                "status": "failed",
                "error": str(e)
            })
    
    return results
```

## Monitoring and Observability

### 1. Execution Logging

Log all execution events:

```python
def log_execution_event(event_type, node_id, data):
    """Log workflow execution event."""
    log_entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "event_type": event_type,
        "node_id": node_id,
        "data": data
    }
    
    logger.info(json.dumps(log_entry))
```

### 2. Metrics Collection

Collect execution metrics:

```python
class WorkflowMetrics:
    """Track workflow execution metrics."""
    
    def __init__(self):
        self.start_time = None
        self.end_time = None
        self.node_durations = {}
        self.node_statuses = {}
    
    def record_node_start(self, node_id):
        """Record node start time."""
        self.node_durations[node_id] = {"start": time.time()}
    
    def record_node_end(self, node_id, status):
        """Record node end time and status."""
        if node_id in self.node_durations:
            self.node_durations[node_id]["end"] = time.time()
            self.node_durations[node_id]["duration"] = (
                self.node_durations[node_id]["end"] - 
                self.node_durations[node_id]["start"]
            )
        self.node_statuses[node_id] = status
```

### 3. Progress Tracking

Track workflow progress:

```python
def get_workflow_progress(state):
    """Get workflow execution progress."""
    total_nodes = len(state.workflow["nodes"])
    completed_nodes = len(state.completed_nodes)
    failed_nodes = len(state.failed_nodes)
    
    return {
        "total": total_nodes,
        "completed": completed_nodes,
        "failed": failed_nodes,
        "progress_percent": (completed_nodes / total_nodes) * 100,
        "status": "running" if completed_nodes < total_nodes else "completed"
    }
```

## Best Practices

### 1. Workflow Design

- **Keep workflows focused**: Single responsibility per workflow
- **Use parallel execution**: Maximize concurrency where possible
- **Handle errors gracefully**: Always include error handlers
- **Add logging**: Log all execution events for debugging
- **Test thoroughly**: Test all branches and error paths

### 2. Node Configuration

- **Use descriptive labels**: Make workflows easy to understand
- **Validate inputs**: Validate data before processing
- **Handle edge cases**: Consider null/empty data
- **Set timeouts**: Prevent infinite loops
- **Add metadata**: Track workflow provenance

### 3. Error Handling

- **Always include error handlers**: For critical nodes
- **Use appropriate retry policies**: Don't retry indefinitely
- **Log errors with context**: Include node ID and input data
- **Alert on failures**: Notify operators of critical failures
- **Provide recovery paths**: Allow workflows to recover from errors

### 4. Performance

- **Minimize data transfer**: Pass only necessary data between nodes
- **Use caching**: Cache expensive operations
- **Optimize parallelism**: Balance parallelism with resource usage
- **Monitor execution time**: Track and optimize slow nodes
- **Use appropriate execution mode**: Sync vs async based on use case

### 5. Security

- **Validate all inputs**: Sanitize data from external sources
- **Use least privilege**: Minimize permissions for each node
- **Encrypt sensitive data**: Protect data in transit and at rest
- **Audit execution logs: Track who executed what and when
- **Implement rate limiting**: Prevent abuse of workflow execution

## Examples

### Example 1: Execute Sequential Workflow

```python
from tools.dsl.workflow_validator import validate_workflow

# Load workflow
with open('examples/workflow_sequential_v3.json', 'r') as f:
    agent = json.load(f)

workflow = agent['workflow']

# Validate workflow
errors = validate_workflow(workflow)
if errors:
    print(f"Validation failed: {errors}")
    exit(1)

# Execute workflow
state = execute_workflow_sync(workflow, {"data": "input"})

# Check results
print(f"Completed nodes: {state.completed_nodes}")
print(f"Failed nodes: {state.failed_nodes}")
print(f"Execution order: {state.execution_order}")
```

### Example 2: Execute Parallel Workflow

```python
import asyncio

# Load workflow
with open('examples/workflow_parallel_v3.json', 'r') as f:
    agent = json.load(f)

workflow = agent['workflow']

# Execute asynchronously
async def run():
    state = await execute_workflow_async(workflow, {"data": "input"})
    return state

state = asyncio.run(run())

# Check results
print(f"Completed nodes: {state.completed_nodes}")
print(f"Execution time: {state.end_time - state.start_time}s")
```

### Example 3: Handle Errors

```python
# Execute workflow with error handling
try:
    state = execute_workflow_sync(workflow, {"data": "input"})
except WorkflowError as e:
    print(f"Workflow failed: {e}")
    
    # Check which nodes failed
    for node_id in state.failed_nodes:
        error = state.node_outputs[node_id].get("error")
        print(f"Node {node_id} failed: {error}")
```

## Troubleshooting

### Common Issues

**Issue**: Workflow contains a cycle
- **Solution**: Remove circular dependencies or use sub-workflows

**Issue**: Node execution timeout
- **Solution**: Increase timeout or optimize node logic

**Issue**: Parallel execution fails
- **Solution**: Check for shared state conflicts, use proper synchronization

**Issue**: Error handler not triggered
- **Solution**: Ensure error-flow edges are properly configured

**Issue**: Data not propagating correctly
- **Solution**: Check edge relations and data flow configuration

## Migration from v2

v2 agents without workflows default to a simple single-node workflow:

```json
{
  "workflow": {
    "id": "default",
    "name": "Default Workflow",
    "version": "1.0.0",
    "nodes": {
      "default": {
        "id": "default",
        "type": "action",
        "label": "Default Action",
        "config": {}
      }
    },
    "edges": []
  }
}
```

This ensures backward compatibility while enabling v3 workflow features.

## References

- [Workflow & DAG Definitions](workflow-dag.md)
- [Workflow Validator](../tools/dsl/workflow_validator.py)
- [Workflow Examples](../examples/workflow_sequential_v3.json)
