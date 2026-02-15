import json
import os

# Test loading a component file
component_path = 'schema/components/agent/role.json'
try:
    with open(component_path, 'r') as f:
        component = json.load(f)
    print(f"✅ Component {component_path} loads successfully")
    print(f"   Content: {component}")
except Exception as e:
    print(f"❌ Component {component_path} failed to load: {e}")

# Test loading main schema
schema_path = 'schema/agent-definition.schema.json'
try:
    with open(schema_path, 'r') as f:
        schema = json.load(f)
    print(f"\n✅ Main schema loads successfully")
    
    # Check for $ref in role property
    role_prop = schema['properties'].get('role')
    if role_prop and '$ref' in role_prop:
        print(f"   Role property uses $ref: {role_prop['$ref']}")
        
        # Try to resolve it
        ref_path = os.path.join(os.path.dirname(schema_path), role_prop['$ref'])
        print(f"   Resolved path: {ref_path}")
        print(f"   Path exists: {os.path.exists(ref_path)}")
        
except Exception as e:
    print(f"❌ Main schema failed to load: {e}")