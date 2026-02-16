import * as vscode from 'vscode';
import * as path from 'path';
import * as fs from 'fs';
import { exec } from 'child_process';
import { promisify } from 'util';

const execAsync = promisify(exec);

export class ADLDiagnosticsProvider {
    private context: vscode.ExtensionContext;
    private outputChannel: vscode.OutputChannel;

    constructor(context: vscode.ExtensionContext) {
        this.context = context;
        this.outputChannel = vscode.window.createOutputChannel('ADL Diagnostics');
    }

    provideDiagnostics(document: vscode.TextDocument): vscode.Diagnostic[] {
        const diagnostics: vscode.Diagnostic[] = [];
        const content = document.getText();

        try {
            const syntaxErrors = this.detectSyntaxErrors(content, document);
            diagnostics.push(...syntaxErrors);

            const validationErrors = this.detectValidationErrors(content, document);
            diagnostics.push(...validationErrors);

            const workflowErrors = this.detectWorkflowValidation(content, document);
            diagnostics.push(...workflowErrors);

            const policyErrors = this.detectPolicyValidation(content, document);
            diagnostics.push(...policyErrors);
        } catch (error) {
            this.outputChannel.appendLine(`Error during diagnostics: ${error}`);
        }

        return diagnostics;
    }

    private detectSyntaxErrors(content: string, document: vscode.TextDocument): vscode.Diagnostic[] {
        const diagnostics: vscode.Diagnostic[] = [];
        const lines = content.split('\n');

        for (let i = 0; i < lines.length; i++) {
            const line = lines[i];
            const lineNum = i + 1;

            const unmatchedBrace = this.checkUnmatchedBraces(line);
            if (unmatchedBrace) {
                const range = new vscode.Range(
                    new vscode.Position(i, unmatchedBrace.column),
                    new vscode.Position(i, unmatchedBrace.column + 1)
                );
                diagnostics.push(new vscode.Diagnostic(
                    range,
                    `Unmatched ${unmatchedBrace.brace}`,
                    vscode.DiagnosticSeverity.Error
                ));
            }

            const invalidIdentifier = this.checkInvalidIdentifier(line);
            if (invalidIdentifier) {
                const range = new vscode.Range(
                    new vscode.Position(i, invalidIdentifier.start),
                    new vscode.Position(i, invalidIdentifier.end)
                );
                diagnostics.push(new vscode.Diagnostic(
                    range,
                    'Invalid identifier: must start with letter or underscore',
                    vscode.DiagnosticSeverity.Error
                ));
            }

            const invalidString = this.checkInvalidString(line);
            if (invalidString) {
                const range = new vscode.Range(
                    new vscode.Position(i, invalidString.start),
                    new vscode.Position(i, line.length)
                );
                diagnostics.push(new vscode.Diagnostic(
                    range,
                    'Unterminated string literal',
                    vscode.DiagnosticSeverity.Error
                ));
            }

            const invalidNumber = this.checkInvalidNumber(line);
            if (invalidNumber) {
                const range = new vscode.Range(
                    new vscode.Position(i, invalidNumber.start),
                    new vscode.Position(i, invalidNumber.end)
                );
                diagnostics.push(new vscode.Diagnostic(
                    range,
                    'Invalid number format',
                    vscode.DiagnosticSeverity.Error
                ));
            }
        }

        return diagnostics;
    }

    private detectValidationErrors(content: string, document: vscode.TextDocument): vscode.Diagnostic[] {
        const diagnostics: vscode.Diagnostic[] = [];
        const lines = content.split('\n');

        for (let i = 0; i < lines.length; i++) {
            const line = lines[i].trim();

            if (line.startsWith('import ')) {
                const importPath = line.substring(7).trim();
                if (!importPath) {
                    const range = new vscode.Range(
                        new vscode.Position(i, 0),
                        new vscode.Position(i, line.length)
                    );
                    diagnostics.push(new vscode.Diagnostic(
                        range,
                        'Import statement requires a path',
                        vscode.DiagnosticSeverity.Error
                    ));
                }
            }

            if (line.startsWith('enum ') || line.startsWith('type ') || line.startsWith('agent ')) {
                const parts = line.split(/\s+/);
                if (parts.length < 2) {
                    const range = new vscode.Range(
                        new vscode.Position(i, 0),
                        new vscode.Position(i, line.length)
                    );
                    diagnostics.push(new vscode.Diagnostic(
                        range,
                        `${parts[0]} definition requires a name`,
                        vscode.DiagnosticSeverity.Error
                    ));
                }
            }

            if (line.includes(':') && !line.startsWith('#')) {
                const colonIndex = line.indexOf(':');
                const beforeColon = line.substring(0, colonIndex).trim();
                const afterColon = line.substring(colonIndex + 1).trim();

                if (beforeColon && !afterColon) {
                    const range = new vscode.Range(
                        new vscode.Position(i, colonIndex),
                        new vscode.Position(i, line.length)
                    );
                    diagnostics.push(new vscode.Diagnostic(
                        range,
                        'Type annotation requires a type',
                        vscode.DiagnosticSeverity.Error
                    ));
                }
            }
        }

        return diagnostics;
    }

    private detectWorkflowValidation(content: string, document: vscode.TextDocument): vscode.Diagnostic[] {
        const diagnostics: vscode.Diagnostic[] = [];
        const lines = content.split('\n');

        try {
            const workflow = this.parseJSON(content);
            if (!workflow || !workflow.workflow) {
                return diagnostics;
            }

            const workflowData = workflow.workflow;

            const requiredFields = ['workflow_id', 'id', 'name', 'version', 'nodes', 'edges'];
            for (const field of requiredFields) {
                if (!(field in workflowData)) {
                    const range = this.findFieldRange(content, 'workflow', field);
                    if (range) {
                        diagnostics.push(new vscode.Diagnostic(
                            range,
                            `Workflow must have a '${field}' field`,
                            vscode.DiagnosticSeverity.Error
                        ));
                    }
                }
            }

            if ('id' in workflowData && !('workflow_id' in workflowData)) {
                const range = this.findFieldRange(content, 'workflow', 'id');
                if (range) {
                    diagnostics.push(new vscode.Diagnostic(
                        range,
                        'Deprecated: Use workflow_id instead of id for workflows',
                        vscode.DiagnosticSeverity.Warning
                    ));
                }
            }

            // Validate version format
            if ('version' in workflowData) {
                const version = workflowData.version;
                if (typeof version !== 'string') {
                    const range = this.findFieldRange(content, 'workflow', 'version');
                    if (range) {
                        diagnostics.push(new vscode.Diagnostic(
                            range,
                            'Version must be a string',
                            vscode.DiagnosticSeverity.Error
                        ));
                    }
                } else if (!this.isSemanticVersion(version)) {
                    const range = this.findFieldRange(content, 'workflow', 'version');
                    if (range) {
                        diagnostics.push(new vscode.Diagnostic(
                            range,
                            `Version must follow semantic versioning (e.g., '1.0.0'), got '${version}'`,
                            vscode.DiagnosticSeverity.Error
                        ));
                    }
                }
            }

            // Validate nodes
            if ('nodes' in workflowData) {
                const nodes = workflowData.nodes;
                if (!nodes || typeof nodes !== 'object') {
                    const range = this.findFieldRange(content, 'workflow', 'nodes');
                    if (range) {
                        diagnostics.push(new vscode.Diagnostic(
                            range,
                            'Nodes must be an object',
                            vscode.DiagnosticSeverity.Error
                        ));
                    }
                } else if (Object.keys(nodes).length === 0) {
                    const range = this.findFieldRange(content, 'workflow', 'nodes');
                    if (range) {
                        diagnostics.push(new vscode.Diagnostic(
                            range,
                            'Workflow must have at least one node',
                            vscode.DiagnosticSeverity.Error
                        ));
                    }
                } else {
                    const nodeIds = new Set<string>();
                    for (const [nodeId, node] of Object.entries(nodes)) {
                        if (typeof node !== 'object') {
                            const range = this.findFieldRange(content, 'workflow', 'nodes', nodeId);
                            if (range) {
                                diagnostics.push(new vscode.Diagnostic(
                                    range,
                                    `Node '${nodeId}' must be an object`,
                                    vscode.DiagnosticSeverity.Error
                                ));
                            }
                            continue;
                        }

                        // Check for duplicate IDs
                        if (nodeIds.has(nodeId)) {
                            const range = this.findFieldRange(content, 'workflow', 'nodes', nodeId);
                            if (range) {
                                diagnostics.push(new vscode.Diagnostic(
                                    range,
                                    `Duplicate node ID: '${nodeId}'`,
                                    vscode.DiagnosticSeverity.Error
                                ));
                            }
                        }
                        nodeIds.add(nodeId);

                        if (!('type' in node)) {
                            const range = this.findFieldRange(content, 'workflow', 'nodes', nodeId, 'type');
                            if (range) {
                                diagnostics.push(new vscode.Diagnostic(
                                    range,
                                    `Node '${nodeId}' must have a 'type' field`,
                                    vscode.DiagnosticSeverity.Error
                                ));
                            }
                        }

                        if ('id' in node) {
                            const range = this.findFieldRange(content, 'workflow', 'nodes', nodeId, 'id');
                            if (range) {
                                diagnostics.push(new vscode.Diagnostic(
                                    range,
                                    'Warning: Node should not have an id field (use node key instead)',
                                    vscode.DiagnosticSeverity.Warning
                                ));
                            }
                        } else {
                            const nodeType = node.type;
                            const validNodeTypes = ['trigger', 'input', 'transform', 'action', 'condition', 'loop', 'output', 'sub_workflow', 'annotation'];
                            if (!validNodeTypes.includes(nodeType)) {
                                const range = this.findFieldRange(content, 'workflow', 'nodes', nodeId, 'type');
                                if (range) {
                                    diagnostics.push(new vscode.Diagnostic(
                                        range,
                                        `Invalid node type: '${nodeType}'. Must be one of ${validNodeTypes.join(', ')}`,
                                        vscode.DiagnosticSeverity.Error
                                    ));
                                }
                            }
                        }

                        if (!('label' in node)) {
                            const range = this.findFieldRange(content, 'workflow', 'nodes', nodeId, 'label');
                            if (range) {
                                diagnostics.push(new vscode.Diagnostic(
                                    range,
                                    `Node '${nodeId}' must have a 'label' field`,
                                    vscode.DiagnosticSeverity.Error
                                ));
                            }
                        }
                    }
                }
            }

            // Validate edges
            if ('edges' in workflowData) {
                const edges = workflowData.edges;
                if (!Array.isArray(edges)) {
                    const range = this.findFieldRange(content, 'workflow', 'edges');
                    if (range) {
                        diagnostics.push(new vscode.Diagnostic(
                            range,
                            'Edges must be an array',
                            vscode.DiagnosticSeverity.Error
                        ));
                    }
                } else if (edges.length === 0) {
                    const range = this.findFieldRange(content, 'workflow', 'edges');
                    if (range) {
                        diagnostics.push(new vscode.Diagnostic(
                            range,
                            'Workflow must have at least one edge',
                            vscode.DiagnosticSeverity.Error
                        ));
                    }
                } else {
                    const edgeIds = new Set<string>();
                    for (let i = 0; i < edges.length; i++) {
                        const edge = edges[i];
                        if (typeof edge !== 'object') {
                            const range = this.findFieldRange(content, 'workflow', 'edges', i);
                            if (range) {
                                diagnostics.push(new vscode.Diagnostic(
                                    range,
                                    `Edge at index ${i} must be an object`,
                                    vscode.DiagnosticSeverity.Error
                                ));
                            }
                            continue;
                        }

const edgeId = edge.edge_id || edge.id;
                        if (edgeId && edgeIds.has(edgeId)) {
                            const range = this.findFieldRange(content, 'workflow', 'edges', i, 'edge_id');
                            if (range) {
                                diagnostics.push(new vscode.Diagnostic(
                                    range,
                                    `Duplicate edge ID: '${edgeId}'`,
                                    vscode.DiagnosticSeverity.Error
                                ));
                            }
                        }
                        if (edgeId) {
                            edgeIds.add(edgeId);
                        }

                        if (!('edge_id' in edge) && !('id' in edge)) {
                            const range = this.findFieldRange(content, 'workflow', 'edges', i, 'edge_id');
                            if (range) {
                                diagnostics.push(new vscode.Diagnostic(
                                    range,
                                    `Edge at index ${i} must have an 'edge_id' field`,
                                    vscode.DiagnosticSeverity.Error
                                ));
                            }
                        }

                        if ('id' in edge && !('edge_id' in edge)) {
                            const range = this.findFieldRange(content, 'workflow', 'edges', i, 'id');
                            if (range) {
                                diagnostics.push(new vscode.Diagnostic(
                                    range,
                                    'Deprecated: Use edge_id instead of id for edges',
                                    vscode.DiagnosticSeverity.Warning
                                ));
                            }
                        }

                        // Validate edge structure
                        if (!('id' in edge)) {
                            const range = this.findFieldRange(content, 'workflow', 'edges', i, 'id');
                            if (range) {
                                diagnostics.push(new vscode.Diagnostic(
                                    range,
                                    `Edge at index ${i} must have an 'id' field`,
                                    vscode.DiagnosticSeverity.Error
                                ));
                            }
                        }

                        if (!('source' in edge)) {
                            const range = this.findFieldRange(content, 'workflow', 'edges', i, 'source');
                            if (range) {
                                diagnostics.push(new vscode.Diagnostic(
                                    range,
                                    `Edge at index ${i} must have a 'source' field`,
                                    vscode.DiagnosticSeverity.Error
                                ));
                            }
                        }

                        if (!('target' in edge)) {
                            const range = this.findFieldRange(content, 'workflow', 'edges', i, 'target');
                            if (range) {
                                diagnostics.push(new vscode.Diagnostic(
                                    range,
                                    `Edge at index ${i} must have a 'target' field`,
                                    vscode.DiagnosticSeverity.Error
                                ));
                            }
                        }

                        // Validate relation if present
                        if ('relation' in edge) {
                            const relation = edge.relation;
                            const validRelations = ['data_flow', 'control_flow', 'error_flow', 'ai_languageModel', 'ai_tool', 'dependency'];
                            if (!validRelations.includes(relation)) {
                                const range = this.findFieldRange(content, 'workflow', 'edges', i, 'relation');
                                if (range) {
                                    diagnostics.push(new vscode.Diagnostic(
                                        range,
                                        `Invalid edge relation: '${relation}'. Must be one of ${validRelations.join(', ')}`,
                                        vscode.DiagnosticSeverity.Error
                                    ));
                                }
                            }
                        }
                    }
                }
            }

            // Detect cycles (basic check)
            if ('nodes' in workflowData && 'edges' in workflowData) {
                const nodes = workflowData.nodes;
                const edges = workflowData.edges;

                if (nodes && edges && Object.keys(nodes).length > 0 && edges.length > 0) {
                    const nodeIds = new Set(Object.keys(nodes));
                    const adjacency = new Map<string, string[]>();

                    for (const edge of edges) {
                        const source = edge.source;
                        const target = edge.target;
                        if (source && target && nodeIds.has(source) && nodeIds.has(target)) {
                            if (!adjacency.has(source)) {
                                adjacency.set(source, []);
                            }
                            adjacency.get(source)!.push(target);
                        }
                    }

                    // Check for cycles using DFS
                    const visited = new Set<string>();
                    const recursionStack = new Set<string>();

                    const hasCycle = (nodeId: string): boolean => {
                        if (recursionStack.has(nodeId)) {
                            return true;
                        }
                        if (visited.has(nodeId)) {
                            return false;
                        }

                        visited.add(nodeId);
                        recursionStack.add(nodeId);

                        const neighbors = adjacency.get(nodeId) || [];
                        for (const neighbor of neighbors) {
                            if (hasCycle(neighbor)) {
                                return true;
                            }
                        }

                        recursionStack.delete(nodeId);
                        return false;
                    };

                    for (const nodeId of nodeIds) {
                        if (hasCycle(nodeId)) {
                            const range = this.findFieldRange(content, 'workflow', 'nodes', nodeId);
                            if (range) {
                                diagnostics.push(new vscode.Diagnostic(
                                    range,
                                    `Workflow contains a cycle involving node '${nodeId}'`,
                                    vscode.DiagnosticSeverity.Error
                                ));
                            }
                            break;
                        }
                    }
                }
            }

        } catch (error) {
            this.outputChannel.appendLine(`Error during workflow validation: ${error}`);
        }

        return diagnostics;
    }

    private detectPolicyValidation(content: string, document: vscode.TextDocument): vscode.Diagnostic[] {
        const diagnostics: vscode.Diagnostic[] = [];
        const lines = content.split('\n');

        try {
            const policy = this.parseJSON(content);
            if (!policy || !policy.policy) {
                return diagnostics;
            }

            const policyData = policy.policy;

            const requiredFields = ['policy_id', 'id', 'name', 'version', 'rego', 'enforcement'];
            for (const field of requiredFields) {
                if (!(field in policyData)) {
                    const range = this.findFieldRange(content, 'policy', field);
                    if (range) {
                        diagnostics.push(new vscode.Diagnostic(
                            range,
                            `Policy must have a '${field}' field`,
                            vscode.DiagnosticSeverity.Error
                        ));
                    }
                }
            }

            if ('id' in policyData && !('policy_id' in policyData)) {
                const range = this.findFieldRange(content, 'policy', 'id');
                if (range) {
                    diagnostics.push(new vscode.Diagnostic(
                        range,
                        'Deprecated: Use policy_id instead of id for policies',
                        vscode.DiagnosticSeverity.Warning
                    ));
                }
            }

            // Validate version format
            if ('version' in policyData) {
                const version = policyData.version;
                if (typeof version !== 'string') {
                    const range = this.findFieldRange(content, 'policy', 'version');
                    if (range) {
                        diagnostics.push(new vscode.Diagnostic(
                            range,
                            'Version must be a string',
                            vscode.DiagnosticSeverity.Error
                        ));
                    }
                } else if (!this.isSemanticVersion(version)) {
                    const range = this.findFieldRange(content, 'policy', 'version');
                    if (range) {
                        diagnostics.push(new vscode.Diagnostic(
                            range,
                            `Version must follow semantic versioning (e.g., '1.0.0'), got '${version}'`,
                            vscode.DiagnosticSeverity.Error
                        ));
                    }
                }
            }

            // Validate Rego
            if ('rego' in policyData) {
                const rego = policyData.rego;
                if (typeof rego !== 'string') {
                    const range = this.findFieldRange(content, 'policy', 'rego');
                    if (range) {
                        diagnostics.push(new vscode.Diagnostic(
                            range,
                            'Rego must be a string',
                            vscode.DiagnosticSeverity.Error
                        ));
                    }
                } else {
                    // Check for required Rego elements
                    if (!rego.includes('package ')) {
                        const range = this.findFieldRange(content, 'policy', 'rego');
                        if (range) {
                            diagnostics.push(new vscode.Diagnostic(
                                range,
                                'Rego policy must define a package',
                                vscode.DiagnosticSeverity.Error
                            ));
                        }
                    }

                    // Check for default deny pattern (security best practice)
                    if (!rego.includes('default allow := false') && !rego.includes('default allow := true')) {
                        const range = this.findFieldRange(content, 'policy', 'rego');
                        if (range) {
                            diagnostics.push(new vscode.Diagnostic(
                                range,
                                'Rego policy should define a default allow rule (prefer \'default allow := false\' for security)',
                                vscode.DiagnosticSeverity.Warning
                            ));
                        }
                    }

                    // Check for allow rule
                    if (!rego.includes('allow if')) {
                        const range = this.findFieldRange(content, 'policy', 'rego');
                        if (range) {
                            diagnostics.push(new vscode.Diagnostic(
                                range,
                                'Rego policy should define at least one allow rule',
                                vscode.DiagnosticSeverity.Error
                            ));
                        }
                    }
                }
            }

            // Validate enforcement
            if ('enforcement' in policyData) {
                const enforcement = policyData.enforcement;
                if (typeof enforcement !== 'object') {
                    const range = this.findFieldRange(content, 'policy', 'enforcement');
                    if (range) {
                        diagnostics.push(new vscode.Diagnostic(
                            range,
                            'Enforcement must be an object',
                            vscode.DiagnosticSeverity.Error
                        ));
                    }
                } else {
                    // Validate mode
                    if (!('mode' in enforcement)) {
                        const range = this.findFieldRange(content, 'policy', 'enforcement', 'mode');
                        if (range) {
                            diagnostics.push(new vscode.Diagnostic(
                                range,
                                'Enforcement must have a \'mode\' field',
                                vscode.DiagnosticSeverity.Error
                            ));
                        }
                    } else {
                        const mode = enforcement.mode;
                        const validModes = ['strict', 'moderate', 'lenient'];
                        if (!validModes.includes(mode)) {
                            const range = this.findFieldRange(content, 'policy', 'enforcement', 'mode');
                            if (range) {
                                diagnostics.push(new vscode.Diagnostic(
                                    range,
                                    `Invalid enforcement mode: '${mode}'. Must be one of ${validModes.join(', ')}`,
                                    vscode.DiagnosticSeverity.Error
                                ));
                            }
                        }
                    }

                    // Validate action
                    if (!('action' in enforcement)) {
                        const range = this.findFieldRange(content, 'policy', 'enforcement', 'action');
                        if (range) {
                            diagnostics.push(new vscode.Diagnostic(
                                range,
                                'Enforcement must have an \'action\' field',
                                vscode.DiagnosticSeverity.Error
                            ));
                        }
                    } else {
                        const action = enforcement.action;
                        const validActions = ['deny', 'warn', 'log', 'allow'];
                        if (!validActions.includes(action)) {
                            const range = this.findFieldRange(content, 'policy', 'enforcement', 'action');
                            if (range) {
                                diagnostics.push(new vscode.Diagnostic(
                                    range,
                                    `Invalid enforcement action: '${action}'. Must be one of ${validActions.join(', ')}`,
                                    vscode.DiagnosticSeverity.Error
                                ));
                            }
                        }
                    }

                    // Validate audit_log if present
                    if ('audit_log' in enforcement) {
                        const auditLog = enforcement.audit_log;
                        if (typeof auditLog !== 'boolean') {
                            const range = this.findFieldRange(content, 'policy', 'enforcement', 'audit_log');
                            if (range) {
                                diagnostics.push(new vscode.Diagnostic(
                                    range,
                                    'audit_log must be a boolean',
                                    vscode.DiagnosticSeverity.Error
                                ));
                            }
                        }
                    }
                }
            }

        } catch (error) {
            this.outputChannel.appendLine(`Error during policy validation: ${error}`);
        }

        return diagnostics;
    }

    private parseJSON(content: string): any {
        try {
            return JSON.parse(content);
        } catch (error) {
            return null;
        }
    }

    private isSemanticVersion(version: string): boolean {
        const pattern = /^(\d+)\.(\d+)\.(\d+)(?:-([a-zA-Z0-9.]+))?$/;
        return pattern.test(version);
    }

    private checkUnmatchedBraces(line: string): { brace: string, column: number } | null {
        const openBraces = ['{', '[', '('];
        const closeBraces = ['}', ']', ')'];
        const stack: string[] = [];

        for (let i = 0; i < line.length; i++) {
            const char = line[i];
            const openIndex = openBraces.indexOf(char);
            const closeIndex = closeBraces.indexOf(char);

            if (openIndex !== -1) {
                stack.push(char);
            } else if (closeIndex !== -1) {
                const expectedOpen = openBraces[closeIndex];
                if (stack.length === 0 || stack.pop() !== expectedOpen) {
                    return { brace: char, column: i };
                }
            }
        }

        if (stack.length > 0) {
            return { brace: stack[stack.length - 1], column: line.lastIndexOf(stack[stack.length - 1]) };
        }

        return null;
    }

    private checkInvalidIdentifier(line: string): { start: number, end: number } | null {
        const identifierRegex = /([a-zA-Z_][a-zA-Z0-9_-]*)/g;
        let match;

        while ((match = identifierRegex.exec(line)) !== null) {
            const identifier = match[1];
            if (!/^[a-zA-Z_]/.test(identifier)) {
                return { start: match.index, end: match.index + identifier.length };
            }
        }

        return null;
    }

    private checkInvalidString(line: string): { start: number } | null {
        const stringRegex = /"/g;
        let match;
        let count = 0;
        let lastStart = -1;

        while ((match = stringRegex.exec(line)) !== null) {
            count++;
            if (count === 1) {
                lastStart = match.index;
            }
        }

        if (count % 2 !== 0 && lastStart !== -1) {
            return { start: lastStart };
        }

        return null;
    }

    private checkInvalidNumber(line: string): { start: number, end: number } | null {
        const numberRegex = /(\d+\.\d+\.?\d*|\.\d+\.?\d*|\d+e[+-]?\d*\.?\d*)/g;
        let match;

        while ((match = numberRegex.exec(line)) !== null) {
            const number = match[1];
            if (/\.\./.test(number) || /e[+-]?\d*\./.test(number)) {
                return { start: match.index, end: match.index + number.length };
            }
        }

        return null;
    }
}
