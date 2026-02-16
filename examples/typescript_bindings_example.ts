/**
 * TypeScript Binding Example - Phase 4 Workflow & Policy Types
 *
 * This example demonstrates how to use the generated TypeScript bindings
 * for ADL workflow and policy definitions. It shows type safety benefits,
 * practical usage patterns, and integration with TypeScript projects.
 *
 * Generated from ADL definitions using: adl-generate --typescript
 */

// ============================================================================
// IMPORT GENERATED TYPES
// ============================================================================

// Import the generated workflow and policy types
import type {
  Workflow,
  WorkflowNode,
  WorkflowEdge,
  Policy,
  Enforcement,
  PolicyData
} from './generated/adl-types';

// ============================================================================
// WORKFLOW USAGE EXAMPLES
// ============================================================================

/**
 * Example 1: Create a workflow from generated types
 *
 * This demonstrates how to construct a workflow using the generated
 * Workflow interface with full type safety.
 */
function createSequentialWorkflow(): Workflow {
  const workflow: Workflow = {
    id: 'sequential-data-processing',
    name: 'Sequential Data Processing',
    version: '1.0.0',
    description: 'Sequential workflow for processing data through multiple stages',
    nodes: {
      'input-node': {
        id: 'input-node',
        type: 'input',
        label: 'Read Data',
        config: {
          source: 'api',
          endpoint: '/data',
          method: 'GET'
        },
        position: { x: 100, y: 100 }
      },
      'transform-node': {
        id: 'transform-node',
        type: 'transform',
        label: 'Transform Data',
        config: {
          operation: 'map',
          expression: 'data.map(x => x * 2)'
        },
        position: { x: 300, y: 100 }
      },
      'validate-node': {
        id: 'validate-node',
        type: 'transform',
        label: 'Validate Data',
        config: {
          operation: 'filter',
          expression: 'data.filter(x => x > 0)'
        },
        position: { x: 500, y: 100 }
      },
      'output-node': {
        id: 'output-node',
        type: 'output',
        label: 'Save Results',
        config: {
          destination: 'database',
          table: 'processed_data',
          mode: 'append'
        },
        position: { x: 700, y: 100 }
      }
    },
    edges: [
      {
        id: 'edge-1',
        source: 'input-node',
        target: 'transform-node',
        relation: 'data_flow'
      },
      {
        id: 'edge-2',
        source: 'transform-node',
        target: 'validate-node',
        relation: 'data_flow'
      },
      {
        id: 'edge-3',
        source: 'validate-node',
        target: 'output-node',
        relation: 'data_flow'
      }
    ],
    metadata: {
      author: 'data-team',
      tags: ['etl', 'sequential', 'data-processing']
    }
  };

  return workflow;
}

/**
 * Example 2: Access workflow nodes and edges with type safety
 *
 * This demonstrates how to safely access workflow structure using
 * the generated types.
 */
function analyzeWorkflow(workflow: Workflow) {
  console.log(`Workflow: ${workflow.name}`);
  console.log(`Version: ${workflow.version}`);
  console.log(`Number of nodes: ${Object.keys(workflow.nodes).length}`);
  console.log(`Number of edges: ${workflow.edges.length}`);

  // Type-safe node access
  const inputNode = workflow.nodes['input-node'];
  if (inputNode) {
    console.log(`Input node type: ${inputNode.type}`);
    console.log(`Input node label: ${inputNode.label}`);
    console.log(`Source endpoint: ${inputNode.config.source}`);
  }

  // Type-safe edge iteration
  workflow.edges.forEach(edge => {
    console.log(`Edge: ${edge.id} -> ${edge.target}`);
    console.log(`Relation: ${edge.relation}`);
  });
}

/**
 * Example 3: Validate workflow structure
 *
 * This demonstrates how to validate workflow structure using type guards.
 */
function validateWorkflow(workflow: unknown): workflow is Workflow {
  // Type guard to ensure the object is a valid Workflow
  if (
    typeof workflow === 'object' &&
    workflow !== null &&
    'id' in workflow &&
    'name' in workflow &&
    'version' in workflow &&
    'nodes' in workflow &&
    'edges' in workflow
  ) {
    const w = workflow as Workflow;
    // Additional validation
    return (
      typeof w.id === 'string' &&
      typeof w.name === 'string' &&
      typeof w.version === 'string' &&
      typeof w.description === 'string' &&
      typeof w.nodes === 'object' &&
      typeof w.edges === 'object'
    );
  }
  return false;
}

/**
 * Example 4: Transform workflow data
 *
 * This demonstrates how to transform workflow data while maintaining type safety.
 */
function transformWorkflow(workflow: Workflow): Workflow {
  // Create a deep copy with modifications
  const transformed: Workflow = {
    ...workflow,
    version: '2.0.0',
    metadata: {
      ...workflow.metadata,
      transformed: true,
      transformer: 'typescript-example'
    }
  };

  // Transform nodes
  transformed.nodes = Object.entries(workflow.nodes).reduce((acc, [key, node]) => {
    acc[key] = {
      ...node,
      config: {
        ...node.config,
        transformed: true
      }
    };
    return acc;
  }, {} as Record<string, WorkflowNode>);

  return transformed;
}

// ============================================================================
// POLICY USAGE EXAMPLES
// ============================================================================

/**
 * Example 5: Create a policy from generated types
 *
 * This demonstrates how to construct a policy using the generated
 * Policy interface with full type safety.
 */
function createRBACPolicy(): Policy {
  const policy: Policy = {
    id: 'rbac-policy',
    name: 'RBAC Policy',
    version: '1.0.0',
    description: 'Role-based access control policy with admin and user roles',
    rego: `package authz

default allow := false

allow if {
    has_role(input.user, "admin")
}

allow if {
    has_role(input.user, "user")
    input.action == "read"
}

allow if {
    has_role(input.user, "user")
    input.resource == "public"
}

has_role(user, role) {
    data.roles[user][role]
}`,
    enforcement: {
      mode: 'strict',
      action: 'deny',
      audit_log: true
    },
    data: {
      roles: {
        admin: ['alice', 'bob'],
        user: ['charlie', 'david', 'eve']
      },
      permissions: {
        read: ['admin', 'user'],
        write: ['admin'],
        execute: ['admin']
      }
    },
    metadata: {
      author: 'security-team',
      tags: ['rbac', 'access-control', 'security']
    }
  };

  return policy;
}

/**
 * Example 6: Access policy data with type safety
 *
 * This demonstrates how to safely access policy structure using
 * the generated types.
 */
function analyzePolicy(policy: Policy) {
  console.log(`Policy: ${policy.name}`);
  console.log(`Version: ${policy.version}`);
  console.log(`Enforcement mode: ${policy.enforcement.mode}`);
  console.log(`Audit logging: ${policy.enforcement.audit_log}`);

  // Type-safe role access
  const adminRoles = policy.data.roles.admin || [];
  console.log(`Admin users: ${adminRoles.join(', ')}`);

  const userRoles = policy.data.roles.user || [];
  console.log(`User users: ${userRoles.join(', ')}`);

  // Type-safe permission access
  const readPermissions = policy.data.permissions.read || [];
  console.log(`Read permissions: ${readPermissions.join(', ')}`);
}

/**
 * Example 7: Validate policy structure
 *
 * This demonstrates how to validate policy structure using type guards.
 */
function validatePolicy(policy: unknown): policy is Policy {
  // Type guard to ensure the object is a valid Policy
  if (
    typeof policy === 'object' &&
    policy !== null &&
    'id' in policy &&
    'name' in policy &&
    'version' in policy &&
    'rego' in policy &&
    'enforcement' in policy &&
    'data' in policy
  ) {
    const p = policy as Policy;
    // Additional validation
    return (
      typeof p.id === 'string' &&
      typeof p.name === 'string' &&
      typeof p.version === 'string' &&
      typeof p.description === 'string' &&
      typeof p.rego === 'string' &&
      typeof p.enforcement === 'object' &&
      typeof p.data === 'object'
    );
  }
  return false;
}

/**
 * Example 8: Transform policy data
 *
 * This demonstrates how to transform policy data while maintaining type safety.
 */
function transformPolicy(policy: Policy): Policy {
  // Create a deep copy with modifications
  const transformed: Policy = {
    ...policy,
    version: '2.0.0',
    metadata: {
      ...policy.metadata,
      transformed: true,
      transformer: 'typescript-example'
    }
  };

  // Transform enforcement settings
  transformed.enforcement = {
    ...policy.enforcement,
    audit_log: true
  };

  return transformed;
}

// ============================================================================
// INTEGRATION EXAMPLES
// ============================================================================

/**
 * Example 9: Combine workflow and policy in an agent
 *
 * This demonstrates how to combine workflow and policy types in a
 * comprehensive agent definition.
 */
interface AgentDefinition {
  id: string;
  name: string;
  version: string;
  workflow: Workflow;
  policy: Policy;
  llmSettings: {
    temperature: number;
    maxTokens: number;
  };
}

function createAgentDefinition(): AgentDefinition {
  const agent: AgentDefinition = {
    id: 'sequential-agent-001',
    name: 'Sequential Data Processing Agent',
    version: '1.0.0',
    workflow: createSequentialWorkflow(),
    policy: createRBACPolicy(),
    llmSettings: {
      temperature: 0.7,
      maxTokens: 2000
    }
  };

  return agent;
}

/**
 * Example 10: Type-safe workflow execution
 *
 * This demonstrates how to execute workflows with type safety.
 */
interface WorkflowContext {
  data: any;
  metadata: Record<string, any>;
}

async function executeWorkflow(workflow: Workflow, context: WorkflowContext) {
  console.log(`Executing workflow: ${workflow.name}`);

  // Type-safe node execution
  for (const [nodeId, node] of Object.entries(workflow.nodes)) {
    console.log(`Processing node: ${node.label} (${node.type})`);

    // Execute node logic based on type
    switch (node.type) {
      case 'input':
        console.log(`Input node: ${node.config.source}`);
        break;
      case 'transform':
        console.log(`Transform node: ${node.config.operation}`);
        break;
      case 'output':
        console.log(`Output node: ${node.config.destination}`);
        break;
    }
  }

  return context;
}

/**
 * Example 11: Type-safe policy evaluation
 *
 * This demonstrates how to evaluate policies with type safety.
 */
interface PolicyInput {
  user: string;
  action: string;
  resource: string;
}

function evaluatePolicy(policy: Policy, input: PolicyInput): boolean {
  console.log(`Evaluating policy: ${policy.name}`);
  console.log(`User: ${input.user}, Action: ${input.action}, Resource: ${input.resource}`);

  // Type-safe role checking
  const roles = policy.data.roles[input.user] || [];
  const hasAdminRole = roles.includes('admin');
  const hasUserRole = roles.includes('user');

  // Type-safe permission checking
  const permissions = policy.data.permissions[input.action] || [];

  // Policy evaluation logic
  if (hasAdminRole) {
    return true;
  }

  if (hasUserRole && input.action === 'read') {
    return true;
  }

  if (hasUserRole && input.resource === 'public') {
    return true;
  }

  return false;
}

// ============================================================================
// TYPE SAFETY BENEFITS DEMONSTRATION
// ============================================================================

/**
 * Example 12: Type safety catches errors at compile time
 *
 * This demonstrates how TypeScript's type system catches errors
 * before runtime.
 */
function demonstrateTypeSafety() {
  // This will cause a TypeScript error - uncomment to see the error
  // const invalidWorkflow: Workflow = {
  //   id: 'invalid',
  //   name: 'Invalid',
  //   version: '1.0.0',
  //   description: 'Invalid',
  //   nodes: {}, // Missing required 'edges' field
  //   edges: [] // This is required
  // };

  // This is valid - all required fields are present
  const validWorkflow: Workflow = {
    id: 'valid',
    name: 'Valid',
    version: '1.0.0',
    description: 'Valid',
    nodes: {},
    edges: []
  };

  console.log('Type safety demonstration complete');
}

/**
 * Example 13: IDE autocomplete and documentation
 *
 * This demonstrates how generated types provide IDE support.
 */
function demonstrateIDESupport() {
  // With generated types, IDE provides:
  // - Autocomplete for all properties
  // - Type hints for all methods
  // - Documentation for all interfaces
  // - Error detection for invalid property access

  const workflow: Workflow = createSequentialWorkflow();

  // IDE will show all available properties:
  // workflow.id
  // workflow.name
  // workflow.version
  // workflow.description
  // workflow.nodes
  // workflow.edges
  // workflow.metadata

  // Type-safe property access
  const nodeName = workflow.name; // Type: string
  const nodeCount = Object.keys(workflow.nodes).length; // Type: number
  const edgeCount = workflow.edges.length; // Type: number

  console.log(`Node count: ${nodeCount}`);
  console.log(`Edge count: ${edgeCount}`);
}

// ============================================================================
// PRACTICAL USAGE PATTERNS
// ============================================================================

/**
 * Example 14: Workflow builder pattern
 *
 * This demonstrates a practical pattern for building workflows
 * incrementally.
 */
class WorkflowBuilder {
  private workflow: Workflow = {
    id: '',
    name: '',
    version: '1.0.0',
    description: '',
    nodes: {},
    edges: []
  };

  withId(id: string): this {
    this.workflow.id = id;
    return this;
  }

  withName(name: string): this {
    this.workflow.name = name;
    return this;
  }

  withDescription(description: string): this {
    this.workflow.description = description;
    return this;
  }

  addNode(node: WorkflowNode): this {
    this.workflow.nodes[node.id] = node;
    return this;
  }

  addEdge(edge: WorkflowEdge): this {
    this.workflow.edges.push(edge);
    return this;
  }

  build(): Workflow {
    return this.workflow;
  }
}

function buildWorkflowExample(): Workflow {
  return new WorkflowBuilder()
    .withId('builder-example')
    .withName('Builder Pattern Workflow')
    .withDescription('Workflow built using builder pattern')
    .addNode({
      id: 'node-1',
      type: 'input',
      label: 'Input',
      config: {},
      position: { x: 0, y: 0 }
    })
    .addNode({
      id: 'node-2',
      type: 'output',
      label: 'Output',
      config: {},
      position: { x: 200, y: 0 }
    })
    .addEdge({
      id: 'edge-1',
      source: 'node-1',
      target: 'node-2',
      relation: 'data_flow'
    })
    .build();
}

/**
 * Example 15: Policy registry pattern
 *
 * This demonstrates a practical pattern for managing multiple policies.
 */
class PolicyRegistry {
  private policies: Map<string, Policy> = new Map();

  register(policy: Policy): void {
    this.policies.set(policy.id, policy);
  }

  get(policyId: string): Policy | undefined {
    return this.policies.get(policyId);
  }

  getAll(): Policy[] {
    return Array.from(this.policies.values());
  }

  getByRole(role: string): Policy[] {
    return this.getAll().filter(policy => {
      const roles = policy.data.roles[role] || [];
      return roles.length > 0;
    });
  }
}

function buildPolicyRegistryExample(): PolicyRegistry {
  const registry = new PolicyRegistry();
  registry.register(createRBACPolicy());
  return registry;
}

// ============================================================================
// MAIN EXECUTION
// ============================================================================

async function main() {
  console.log('=== TypeScript Binding Example ===\n');

  // Demonstrate workflow usage
  console.log('1. Workflow Examples:');
  const workflow = createSequentialWorkflow();
  analyzeWorkflow(workflow);
  console.log('');

  // Demonstrate policy usage
  console.log('2. Policy Examples:');
  const policy = createRBACPolicy();
  analyzePolicy(policy);
  console.log('');

  // Demonstrate type safety
  console.log('3. Type Safety:');
  demonstrateTypeSafety();
  console.log('');

  // Demonstrate IDE support
  console.log('4. IDE Support:');
  demonstrateIDESupport();
  console.log('');

  // Demonstrate builder patterns
  console.log('5. Builder Patterns:');
  const builderWorkflow = buildWorkflowExample();
  console.log(`Builder workflow: ${builderWorkflow.name}`);
  console.log('');

  const registry = buildPolicyRegistryExample();
  console.log(`Policy registry: ${registry.getAll().length} policies registered`);
  console.log('');

  // Demonstrate integration
  console.log('6. Integration:');
  const agent = createAgentDefinition();
  console.log(`Agent: ${agent.name}`);
  console.log(`Workflow nodes: ${Object.keys(agent.workflow.nodes).length}`);
  console.log(`Policy enforcement: ${agent.policy.enforcement.mode}`);
  console.log('');

  console.log('=== Example Complete ===');
}

// Run the example if this file is executed directly
if (require.main === module) {
  main().catch(console.error);
}

// Export types for use in other modules
export type {
  Workflow,
  WorkflowNode,
  WorkflowEdge,
  Policy,
  Enforcement,
  PolicyData
};