import * as vscode from 'vscode';

export class ADLFormatter implements vscode.DocumentFormattingEditProvider, vscode.DocumentRangeFormattingEditProvider {
    provideDocumentFormattingEdits(
        document: vscode.TextDocument,
        options: vscode.FormattingOptions,
        token: vscode.CancellationToken
    ): vscode.ProviderResult<vscode.TextEdit[]> {
        const content = document.getText();
        const lines = content.split('\n');

        const formattedLines = lines.map((line, index) => {
            const trimmedLine = line.trim();
            if (!trimmedLine || trimmedLine.startsWith('#')) {
                return line;
            }

            let formattedLine = trimmedLine;

            const indentSize = options.insertSpaces ? options.tabSize : 0;
            const indent = ' '.repeat(indentSize);

            if (formattedLine.includes('{') && !formattedLine.endsWith('{')) {
                const parts = formattedLine.split('{');
                const beforeBrace = parts[0].trim();
                const afterBrace = parts[1].trim();

                if (afterBrace) {
                    formattedLine = `${beforeBrace} {\n${indent}${afterBrace}`;
                }
            }

            if (formattedLine.includes('}') && !formattedLine.startsWith('}')) {
                const parts = formattedLine.split('}');
                const beforeBrace = parts[0].trim();
                const afterBrace = parts[1].trim();

                if (beforeBrace) {
                    formattedLine = `${beforeBrace}\n${indent}}`;
                }

                if (afterBrace) {
                    formattedLine = `${formattedLine}\n${indent}${afterBrace}`;
                }
            }

            if (formattedLine.includes(',') && !formattedLine.endsWith(',')) {
                formattedLine = formattedLine.replace(/,\s*([^\s])/g, ', $1');
            }

            if (formattedLine.includes(':') && !formattedLine.startsWith('#')) {
                const colonIndex = formattedLine.indexOf(':');
                const beforeColon = formattedLine.substring(0, colonIndex).trim();
                const afterColon = formattedLine.substring(colonIndex + 1).trim();

                if (beforeColon && afterColon) {
                    formattedLine = `${beforeColon}: ${afterColon}`;
                }
            }

            if (formattedLine.includes('[') && !formattedLine.endsWith('[')) {
                const parts = formattedLine.split('[');
                const beforeBracket = parts[0].trim();
                const afterBracket = parts[1].trim();

                if (afterBracket) {
                    formattedLine = `${beforeBracket} [\n${indent}${afterBracket}`;
                }
            }

            if (formattedLine.includes(']') && !formattedLine.startsWith(']')) {
                const parts = formattedLine.split(']');
                const beforeBracket = parts[0].trim();
                const afterBracket = parts[1].trim();

                if (beforeBracket) {
                    formattedLine = `${beforeBracket}\n${indent}]`;
                }

                if (afterBracket) {
                    formattedLine = `${formattedLine}\n${indent}${afterBracket}`;
                }
            }

            if (formattedLine.includes('(') && !formattedLine.endsWith('(')) {
                const parts = formattedLine.split('(');
                const beforeParen = parts[0].trim();
                const afterParen = parts[1].trim();

                if (afterParen) {
                    formattedLine = `${beforeParen} (\n${indent}${afterParen}`;
                }
            }

            if (formattedLine.includes(')') && !formattedLine.startsWith(')')) {
                const parts = formattedLine.split(')');
                const beforeParen = parts[0].trim();
                const afterParen = parts[1].trim();

                if (beforeParen) {
                    formattedLine = `${beforeParen}\n${indent})`;
                }

                if (afterParen) {
                    formattedLine = `${formattedLine}\n${indent}${afterParen}`;
                }
            }

            if (formattedLine.endsWith(',')) {
                formattedLine = formattedLine.slice(0, -1);
            }

            return formattedLine;
        });

        const formattedContent = formattedLines.join('\n');
        const fullRange = new vscode.Range(
            new vscode.Position(0, 0),
            new vscode.Position(document.lineCount, 0)
        );

        return [new vscode.TextEdit(fullRange, formattedContent)];
    }

    provideDocumentRangeFormattingEdits(
        document: vscode.TextDocument,
        range: vscode.Range,
        options: vscode.FormattingOptions,
        token: vscode.CancellationToken
    ): vscode.ProviderResult<vscode.TextEdit[]> {
        const content = document.getText();
        const lines = content.split('\n');

        const startLine = range.start.line;
        const endLine = range.end.line;

        const formattedLines = lines.map((line, index) => {
            if (index < startLine || index > endLine) {
                return line;
            }

            const trimmedLine = line.trim();
            if (!trimmedLine || trimmedLine.startsWith('#')) {
                return line;
            }

            let formattedLine = trimmedLine;

            const indentSize = options.insertSpaces ? options.tabSize : 0;
            const indent = ' '.repeat(indentSize);

            if (formattedLine.includes('{') && !formattedLine.endsWith('{')) {
                const parts = formattedLine.split('{');
                const beforeBrace = parts[0].trim();
                const afterBrace = parts[1].trim();

                if (afterBrace) {
                    formattedLine = `${beforeBrace} {\n${indent}${afterBrace}`;
                }
            }

            if (formattedLine.includes('}') && !formattedLine.startsWith('}')) {
                const parts = formattedLine.split('}');
                const beforeBrace = parts[0].trim();
                const afterBrace = parts[1].trim();

                if (beforeBrace) {
                    formattedLine = `${beforeBrace}\n${indent}}`;
                }

                if (afterBrace) {
                    formattedLine = `${formattedLine}\n${indent}${afterBrace}`;
                }
            }

            if (formattedLine.includes(',') && !formattedLine.endsWith(',')) {
                formattedLine = formattedLine.replace(/,\s*([^\s])/g, ', $1');
            }

            if (formattedLine.includes(':') && !formattedLine.startsWith('#')) {
                const colonIndex = formattedLine.indexOf(':');
                const beforeColon = formattedLine.substring(0, colonIndex).trim();
                const afterColon = formattedLine.substring(colonIndex + 1).trim();

                if (beforeColon && afterColon) {
                    formattedLine = `${beforeColon}: ${afterColon}`;
                }
            }

            if (formattedLine.includes('[') && !formattedLine.endsWith('[')) {
                const parts = formattedLine.split('[');
                const beforeBracket = parts[0].trim();
                const afterBracket = parts[1].trim();

                if (afterBracket) {
                    formattedLine = `${beforeBracket} [\n${indent}${afterBracket}`;
                }
            }

            if (formattedLine.includes(']') && !formattedLine.startsWith(']')) {
                const parts = formattedLine.split(']');
                const beforeBracket = parts[0].trim();
                const afterBracket = parts[1].trim();

                if (beforeBracket) {
                    formattedLine = `${beforeBracket}\n${indent}]`;
                }

                if (afterBracket) {
                    formattedLine = `${formattedLine}\n${indent}${afterBracket}`;
                }
            }

            if (formattedLine.includes('(') && !formattedLine.endsWith('(')) {
                const parts = formattedLine.split('(');
                const beforeParen = parts[0].trim();
                const afterParen = parts[1].trim();

                if (afterParen) {
                    formattedLine = `${beforeParen} (\n${indent}${afterParen}`;
                }
            }

            if (formattedLine.includes(')') && !formattedLine.startsWith(')')) {
                const parts = formattedLine.split(')');
                const beforeParen = parts[0].trim();
                const afterParen = parts[1].trim();

                if (beforeParen) {
                    formattedLine = `${beforeParen}\n${indent})`;
                }

                if (afterParen) {
                    formattedLine = `${formattedLine}\n${indent}${afterParen}`;
                }
            }

            if (formattedLine.endsWith(',')) {
                formattedLine = formattedLine.slice(0, -1);
            }

            return formattedLine;
        });

        const formattedContent = formattedLines.join('\n');
        const fullRange = new vscode.Range(
            new vscode.Position(startLine, 0),
            new vscode.Position(endLine + 1, 0)
        );

        return [new vscode.TextEdit(fullRange, formattedContent)];
    }
}