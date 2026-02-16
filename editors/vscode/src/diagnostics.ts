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
