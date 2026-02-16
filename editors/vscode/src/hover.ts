import * as vscode from 'vscode';

export class ADLHoverProvider implements vscode.HoverProvider {
    private typeDefinitions: Map<string, vscode.Location> = new Map();
    private enumDefinitions: Map<string, vscode.Location> = new Map();
    private fieldDefinitions: Map<string, vscode.Location> = new Map();

    provideHover(
        document: vscode.TextDocument,
        position: vscode.Position,
        token: vscode.CancellationToken
    ): vscode.ProviderResult<vscode.Hover> {
        const wordRange = document.getWordRangeAtPosition(position);
        if (!wordRange) {
            return null;
        }

        const word = document.getText(wordRange);

        if (this.typeDefinitions.has(word)) {
            return this.getTypeHover(word, document);
        }

        if (this.enumDefinitions.has(word)) {
            return this.getEnumHover(word, document);
        }

        if (this.fieldDefinitions.has(word)) {
            return this.getFieldHover(word, document);
        }

        return null;
    }

    private getTypeHover(typeName: string, document: vscode.TextDocument): vscode.Hover {
        const location = this.typeDefinitions.get(typeName)!;
        const content = document.getText();
        const lines = content.split('\n');
        const typeLine = lines[location.range.start.line];

        const match = typeLine.match(/type\s+(\w+)\s*\{([^}]*)\}/);
        if (match) {
            const fields = match[2].trim();
            const fieldList = fields ? fields.split(',').map(f => f.trim()) : [];
            const fieldDocs = fieldList.map(field => {
                const fieldMatch = field.match(/(\w+):\s*(\w+)/);
                if (fieldMatch) {
                    return `**${fieldMatch[1]}**: \`${fieldMatch[2]}\``;
                }
                return field;
            });

            const markdown = new vscode.MarkdownString(
                `**Type**: \`${typeName}\`\n\n` +
                `**Fields**:\n${fieldDocs.join('\n')}`
            );

            return new vscode.Hover(markdown, location.range);
        }

        return new vscode.Hover(new vscode.MarkdownString(`**Type**: \`${typeName}\``), location.range);
    }

    private getEnumHover(enumName: string, document: vscode.TextDocument): vscode.Hover {
        const location = this.enumDefinitions.get(enumName)!;
        const content = document.getText();
        const lines = content.split('\n');
        const enumLine = lines[location.range.start.line];

        const match = enumLine.match(/enum\s+(\w+)\s*\{([^}]*)\}/);
        if (match) {
            const values = match[2].trim().split(',').map(v => v.trim());
            const markdown = new vscode.MarkdownString(
                `**Enum**: \`${enumName}\`\n\n` +
                `**Values**:\n${values.map(v => `- \`${v}\``).join('\n')}`
            );

            return new vscode.Hover(markdown, location.range);
        }

        return new vscode.Hover(new vscode.MarkdownString(`**Enum**: \`${enumName}\``), location.range);
    }

    private getFieldHover(fieldName: string, document: vscode.TextDocument): vscode.Hover {
        const location = this.fieldDefinitions.get(fieldName)!;
        const content = document.getText();
        const lines = content.split('\n');

        for (let i = location.range.start.line; i < Math.min(location.range.start.line + 5, lines.length); i++) {
            const line = lines[i].trim();
            const match = line.match(/(\w+):\s*(\w+)/);
            if (match && match[1] === fieldName) {
                const type = match[2];
                const markdown = new vscode.MarkdownString(
                    `**Field**: \`${fieldName}\`\n\n` +
                    `**Type**: \`${type}\``
                );

                return new vscode.Hover(markdown, location.range);
            }
        }

        return new vscode.Hover(new vscode.MarkdownString(`**Field**: \`${fieldName}\``), location.range);
    }

    updateDefinitions(document: vscode.TextDocument) {
        this.typeDefinitions.clear();
        this.enumDefinitions.clear();
        this.fieldDefinitions.clear();

        const content = document.getText();
        const lines = content.split('\n');

        for (let i = 0; i < lines.length; i++) {
            const line = lines[i].trim();

            if (line.startsWith('type ')) {
                const match = line.match(/type\s+(\w+)/);
                if (match) {
                    const typeName = match[1];
                    const position = new vscode.Position(i, line.indexOf(typeName));
                    this.typeDefinitions.set(typeName, new vscode.Location(document.uri, position));
                }
            }

            if (line.startsWith('enum ')) {
                const match = line.match(/enum\s+(\w+)/);
                if (match) {
                    const enumName = match[1];
                    const position = new vscode.Position(i, line.indexOf(enumName));
                    this.enumDefinitions.set(enumName, new vscode.Location(document.uri, position));
                }
            }

            if (line.includes(':') && !line.startsWith('#')) {
                const colonIndex = line.indexOf(':');
                const beforeColon = line.substring(0, colonIndex).trim();
                const afterColon = line.substring(colonIndex + 1).trim();

                if (beforeColon && afterColon) {
                    const match = beforeColon.match(/(\w+)\s*$/);
                    if (match) {
                        const fieldName = match[1];
                        const position = new vscode.Position(i, colonIndex - fieldName.length);
                        this.fieldDefinitions.set(fieldName, new vscode.Location(document.uri, position));
                    }
                }
            }
        }
    }
}