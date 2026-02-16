import * as vscode from 'vscode';
import * as path from 'path';
import * as fs from 'fs';

export class ADLDefinitionProvider implements vscode.DefinitionProvider {
    private typeDefinitions: Map<string, vscode.Location> = new Map();
    private enumDefinitions: Map<string, vscode.Location> = new Map();
    private importedTypes: Map<string, string> = new Map();

    provideDefinition(
        document: vscode.TextDocument,
        position: vscode.Position,
        token: vscode.CancellationToken
    ): vscode.ProviderResult<vscode.Location | vscode.Location[]> {
        const wordRange = document.getWordRangeAtPosition(position);
        if (!wordRange) {
            return null;
        }

        const word = document.getText(wordRange);

        if (this.typeDefinitions.has(word)) {
            return this.typeDefinitions.get(word)!;
        }

        if (this.enumDefinitions.has(word)) {
            return this.enumDefinitions.get(word)!;
        }

        const importedType = this.importedTypes.get(word);
        if (importedType) {
            return this.findDefinitionInFile(importedType, word);
        }

        return null;
    }

    private findDefinitionInFile(filePath: string, typeName: string): vscode.Location | null {
        if (!fs.existsSync(filePath)) {
            return null;
        }

        const content = fs.readFileSync(filePath, 'utf-8');
        const lines = content.split('\n');

        for (let i = 0; i < lines.length; i++) {
            const line = lines[i].trim();

            if (line.startsWith(`type ${typeName}`)) {
                const position = new vscode.Position(i, line.indexOf(typeName));
                return new vscode.Location(vscode.Uri.file(filePath), position);
            }

            if (line.startsWith(`enum ${typeName}`)) {
                const position = new vscode.Position(i, line.indexOf(typeName));
                return new vscode.Location(vscode.Uri.file(filePath), position);
            }
        }

        return null;
    }

    updateDefinitions(document: vscode.TextDocument, workspaceRoot: string) {
        this.typeDefinitions.clear();
        this.enumDefinitions.clear();
        this.importedTypes.clear();

        const content = document.getText();
        const lines = content.split('\n');
        const currentFilePath = document.uri.fsPath;

        for (let i = 0; i < lines.length; i++) {
            const line = lines[i].trim();

            if (line.startsWith('import ')) {
                this.parseImportStatement(line, currentFilePath, workspaceRoot);
            } else if (line.startsWith('type ')) {
                const match = line.match(/type\s+(\w+)/);
                if (match) {
                    const typeName = match[1];
                    const position = new vscode.Position(i, line.indexOf(typeName));
                    this.typeDefinitions.set(typeName, new vscode.Location(document.uri, position));
                }
            } else if (line.startsWith('enum ')) {
                const match = line.match(/enum\s+(\w+)/);
                if (match) {
                    const enumName = match[1];
                    const position = new vscode.Position(i, line.indexOf(enumName));
                    this.enumDefinitions.set(enumName, new vscode.Location(document.uri, position));
                }
            }
        }
    }

    private parseImportStatement(
        line: string,
        currentFilePath: string,
        workspaceRoot: string
    ): void {
        const match = line.match(/import\s+{([^}]+)}\s+from\s+['"]([^'"]+)['"]/);
        if (!match) {
            return;
        }

        const importedNames = match[1].split(',').map(n => n.trim());
        const importPath = match[2];

        const currentDir = path.dirname(currentFilePath);
        const absolutePath = path.resolve(currentDir, importPath);

        importedNames.forEach(name => {
            this.importedTypes.set(name, absolutePath);
        });
    }
}