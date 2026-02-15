#!/usr/bin/env python3
"""
Validate model routing configuration in ADL agent definitions.
"""
import json
import sys
from pathlib import Path

def validate_model_routing(agent_data):
    """Validate model routing configuration."""
    errors = []
    
    # Check if llm_settings exists
    if 'llm_settings' not in agent_data:
        errors.append("Missing 'llm_settings' field")
        return errors
    
    llm_settings = agent_data['llm_settings']
    
    # Check if model_routing exists
    if 'model_routing' not in llm_settings:
        # This is OK - model routing is optional
        return errors
    
    model_routing = llm_settings['model_routing']
    
    # Check if enabled is true
    if model_routing.get('enabled', False):
        # Validate primary model
        if 'primary_model' not in model_routing:
            errors.append("When model_routing.enabled is true, 'primary_model' must be specified")
        
        # Validate fallback models if specified
        if 'fallback_models' in model_routing:
            fallback_models = model_routing['fallback_models']
            if not isinstance(fallback_models, list):
                errors.append("'fallback_models' must be a list")
            elif len(fallback_models) > 3:
                errors.append("Maximum of 3 fallback models allowed (scope guardrail)")
        
        # Validate specialized models if specified
        if 'specialized_models' in model_routing:
            specialized_models = model_routing['specialized_models']
            if not isinstance(specialized_models, list):
                errors.append("'specialized_models' must be a list")
            elif len(specialized_models) > 3:
                errors.append("Maximum of 3 specialized models allowed (scope guardrail)")
            else:
                for i, model in enumerate(specialized_models):
                    if not isinstance(model, dict):
                        errors.append(f"specialized_models[{i}] must be an object")
                        continue
                    
                    if 'model' not in model:
                        errors.append(f"specialized_models[{i}] missing 'model' field")
                    
                    if 'task_types' in model:
                        task_types = model['task_types']
                        if not isinstance(task_types, list):
                            errors.append(f"specialized_models[{i}].task_types must be a list")
                    
                    if 'priority' in model:
                        priority = model['priority']
                        if not isinstance(priority, int) or priority < 1 or priority > 10:
                            errors.append(f"specialized_models[{i}].priority must be an integer between 1 and 10")
    
    # Validate model constraints if specified
    if 'model_constraints' in llm_settings:
        constraints = llm_settings['model_constraints']
        
        # Check token limits
        if 'max_tokens_per_request' in constraints:
            tokens = constraints['max_tokens_per_request']
            if not isinstance(tokens, int) or tokens < 1:
                errors.append("'max_tokens_per_request' must be a positive integer")
        
        # Check cost limits
        if 'cost_limit_per_hour' in constraints:
            cost = constraints['cost_limit_per_hour']
            if not isinstance(cost, (int, float)) or cost < 0:
                errors.append("'cost_limit_per_hour' must be a non-negative number")
        
        # Check timeout
        if 'timeout_seconds' in constraints:
            timeout = constraints['timeout_seconds']
            if not isinstance(timeout, int) or timeout < 1:
                errors.append("'timeout_seconds' must be a positive integer")
    
    return errors

def main():
    if len(sys.argv) != 2:
        print("Usage: python tools/validate-model-routing.py <path-to-agent-json>")
        sys.exit(1)
    
    file_path = Path(sys.argv[1])
    if not file_path.exists():
        print(f"Error: File not found: {file_path}")
        sys.exit(1)
    
    try:
        with open(file_path, 'r') as f:
            agent_data = json.load(f)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON: {e}")
        sys.exit(1)
    
    errors = validate_model_routing(agent_data)
    
    if errors:
        print(f"❌ Model routing validation failed for {file_path}:")
        for error in errors:
            print(f"  - {error}")
        sys.exit(1)
    else:
        print(f"✅ Model routing configuration is valid in {file_path}")

if __name__ == "__main__":
    main()