"use strict";
var __createBinding = (this && this.__createBinding) || (Object.create ? (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    var desc = Object.getOwnPropertyDescriptor(m, k);
    if (!desc || ("get" in desc ? !m.__esModule : desc.writable || desc.configurable)) {
      desc = { enumerable: true, get: function() { return m[k]; } };
    }
    Object.defineProperty(o, k2, desc);
}) : (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    o[k2] = m[k];
}));
var __setModuleDefault = (this && this.__setModuleDefault) || (Object.create ? (function(o, v) {
    Object.defineProperty(o, "default", { enumerable: true, value: v });
}) : function(o, v) {
    o["default"] = v;
});
var __importStar = (this && this.__importStar) || (function () {
    var ownKeys = function(o) {
        ownKeys = Object.getOwnPropertyNames || function (o) {
            var ar = [];
            for (var k in o) if (Object.prototype.hasOwnProperty.call(o, k)) ar[ar.length] = k;
            return ar;
        };
        return ownKeys(o);
    };
    return function (mod) {
        if (mod && mod.__esModule) return mod;
        var result = {};
        if (mod != null) for (var k = ownKeys(mod), i = 0; i < k.length; i++) if (k[i] !== "default") __createBinding(result, mod, k[i]);
        __setModuleDefault(result, mod);
        return result;
    };
})();
Object.defineProperty(exports, "__esModule", { value: true });
exports.ADLCompletionProvider = void 0;
const vscode = __importStar(require("vscode"));
class ADLCompletionProvider {
    constructor() {
        this.keywords = [
            'import', 'enum', 'type', 'agent', 'as', 'module', 'export', 'validation'
        ];
        this.primitiveTypes = [
            'string', 'integer', 'number', 'boolean', 'object', 'array', 'any', 'null'
        ];
        this.booleanLiterals = ['true', 'false'];
    }
    provideCompletionItems(document, position, token, context) {
        const items = [];
        const line = document.lineAt(position).text;
        const linePrefix = line.substring(0, position.character);
        if (this.shouldProvideKeywords(linePrefix)) {
            items.push(...this.getKeywordCompletions());
        }
        if (this.shouldProvideTypes(linePrefix)) {
            items.push(...this.getTypeCompletions());
        }
        if (this.shouldProvideBooleans(linePrefix)) {
            items.push(...this.getBooleanCompletions());
        }
        if (this.shouldProvideFields(linePrefix)) {
            items.push(...this.getFieldCompletions());
        }
        return items;
    }
    shouldProvideKeywords(linePrefix) {
        const trimmed = linePrefix.trim();
        return trimmed === '' || trimmed.endsWith(' ') || trimmed === '#';
    }
    shouldProvideTypes(linePrefix) {
        const trimmed = linePrefix.trim();
        return trimmed.endsWith(':') || trimmed.endsWith(': ');
    }
    shouldProvideBooleans(linePrefix) {
        const trimmed = linePrefix.trim();
        return trimmed.endsWith(':') || trimmed.endsWith(': ') || trimmed.endsWith('=');
    }
    shouldProvideFields(linePrefix) {
        const trimmed = linePrefix.trim();
        return trimmed.startsWith('type ') || trimmed.startsWith('agent ') || trimmed.startsWith('enum ');
    }
    getKeywordCompletions() {
        return this.keywords.map(keyword => {
            const item = new vscode.CompletionItem(keyword, vscode.CompletionItemKind.Keyword);
            item.detail = 'ADL Keyword';
            item.documentation = new vscode.MarkdownString(`ADL keyword: \`${keyword}\``);
            return item;
        });
    }
    getTypeCompletions() {
        const items = [];
        this.primitiveTypes.forEach(type => {
            const item = new vscode.CompletionItem(type, vscode.CompletionItemKind.Class);
            item.detail = 'Primitive Type';
            item.documentation = new vscode.MarkdownString(`ADL primitive type: \`${type}\``);
            items.push(item);
        });
        items.push(...this.getArrayTypeCompletions());
        items.push(...this.getOptionalTypeCompletions());
        return items;
    }
    getArrayTypeCompletions() {
        const arrayTypes = this.primitiveTypes.map(type => `${type}[]`);
        return arrayTypes.map(type => {
            const item = new vscode.CompletionItem(type, vscode.CompletionItemKind.Class);
            item.detail = 'Array Type';
            item.documentation = new vscode.MarkdownString(`Array of \`${type}\``);
            return item;
        });
    }
    getOptionalTypeCompletions() {
        const optionalTypes = this.primitiveTypes.map(type => `${type}?`);
        return optionalTypes.map(type => {
            const item = new vscode.CompletionItem(type, vscode.CompletionItemKind.Class);
            item.detail = 'Optional Type';
            item.documentation = new vscode.MarkdownString(`Optional \`${type}\``);
            return item;
        });
    }
    getBooleanCompletions() {
        return this.booleanLiterals.map(literal => {
            const item = new vscode.CompletionItem(literal, vscode.CompletionItemKind.Value);
            item.detail = 'Boolean Literal';
            item.documentation = new vscode.MarkdownString(`Boolean value: \`${literal}\``);
            return item;
        });
    }
    getFieldCompletions() {
        const commonFields = [
            { name: 'name', type: 'string', description: 'Name of the entity' },
            { name: 'description', type: 'string', description: 'Description of the entity' },
            { name: 'version', type: 'integer', description: 'Version number' },
            { name: 'id', type: 'string', description: 'Unique identifier' },
            { name: 'config', type: 'Config', description: 'Configuration object' },
            { name: 'parameters', type: 'Parameter[]', description: 'List of parameters' },
            { name: 'returns', type: 'ReturnType', description: 'Return type definition' },
            { name: 'required', type: 'boolean', description: 'Whether the field is required' },
            { name: 'default', type: 'any', description: 'Default value' },
            { name: 'minLength', type: 'integer', description: 'Minimum length for strings' },
            { name: 'maxLength', type: 'integer', description: 'Maximum length for strings' },
            { name: 'minimum', type: 'number', description: 'Minimum numeric value' },
            { name: 'maximum', type: 'number', description: 'Maximum numeric value' },
            { name: 'pattern', type: 'string', description: 'Regex pattern for validation' },
            { name: 'enum', type: 'string[]', description: 'List of allowed values' },
        ];
        return commonFields.map(field => {
            const item = new vscode.CompletionItem(field.name, vscode.CompletionItemKind.Field);
            item.detail = `Field: ${field.type}`;
            item.documentation = new vscode.MarkdownString(`${field.description}\n\nType: \`${field.type}\``);
            item.insertText = new vscode.SnippetString(`${field.name}: ${field.type}`);
            return item;
        });
    }
}
exports.ADLCompletionProvider = ADLCompletionProvider;
//# sourceMappingURL=completion.js.map