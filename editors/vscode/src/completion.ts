import * as vscode from 'vscode';

export class ADLCompletionProvider implements vscode.CompletionItemProvider {
    private keywords = [
        'import', 'enum', 'type', 'agent', 'as', 'module', 'export', 'validation'
    ];

    private primitiveTypes = [
        'string', 'integer', 'number', 'boolean', 'object', 'array', 'any', 'null'
    ];

    private booleanLiterals = ['true', 'false'];

    provideCompletionItems(
        document: vscode.TextDocument,
        position: vscode.Position,
        token: vscode.CancellationToken,
        context: vscode.CompletionContext
    ): vscode.ProviderResult<vscode.CompletionItem[]> {
        const items: vscode.CompletionItem[] = [];
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

    private shouldProvideKeywords(linePrefix: string): boolean {
        const trimmed = linePrefix.trim();
        return trimmed === '' || trimmed.endsWith(' ') || trimmed === '#';
    }

    private shouldProvideTypes(linePrefix: string): boolean {
        const trimmed = linePrefix.trim();
        return trimmed.endsWith(':') || trimmed.endsWith(': ');
    }

    private shouldProvideBooleans(linePrefix: string): boolean {
        const trimmed = linePrefix.trim();
        return trimmed.endsWith(':') || trimmed.endsWith(': ') || trimmed.endsWith('=');
    }

    private shouldProvideFields(linePrefix: string): boolean {
        const trimmed = linePrefix.trim();
        return trimmed.startsWith('type ') || trimmed.startsWith('agent ') || trimmed.startsWith('enum ');
    }

    private getKeywordCompletions(): vscode.CompletionItem[] {
        return this.keywords.map(keyword => {
            const item = new vscode.CompletionItem(keyword, vscode.CompletionItemKind.Keyword);
            item.detail = 'ADL Keyword';
            item.documentation = new vscode.MarkdownString(`ADL keyword: \`${keyword}\``);
            return item;
        });
    }

    private getTypeCompletions(): vscode.CompletionItem[] {
        const items: vscode.CompletionItem[] = [];

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

    private getArrayTypeCompletions(): vscode.CompletionItem[] {
        const arrayTypes = this.primitiveTypes.map(type => `${type}[]`);
        return arrayTypes.map(type => {
            const item = new vscode.CompletionItem(type, vscode.CompletionItemKind.Class);
            item.detail = 'Array Type';
            item.documentation = new vscode.MarkdownString(`Array of \`${type}\``);
            return item;
        });
    }

    private getOptionalTypeCompletions(): vscode.CompletionItem[] {
        const optionalTypes = this.primitiveTypes.map(type => `${type}?`);
        return optionalTypes.map(type => {
            const item = new vscode.CompletionItem(type, vscode.CompletionItemKind.Class);
            item.detail = 'Optional Type';
            item.documentation = new vscode.MarkdownString(`Optional \`${type}\``);
            return item;
        });
    }

    private getBooleanCompletions(): vscode.CompletionItem[] {
        return this.booleanLiterals.map(literal => {
            const item = new vscode.CompletionItem(literal, vscode.CompletionItemKind.Value);
            item.detail = 'Boolean Literal';
            item.documentation = new vscode.MarkdownString(`Boolean value: \`${literal}\``);
            return item;
        });
    }

    private getFieldCompletions(): vscode.CompletionItem[] {
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
