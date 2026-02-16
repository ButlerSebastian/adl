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
exports.ADLFormatter = void 0;
const vscode = __importStar(require("vscode"));
class ADLFormatter {
    provideDocumentFormattingEdits(document, options, token) {
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
        const fullRange = new vscode.Range(new vscode.Position(0, 0), new vscode.Position(document.lineCount, 0));
        return [new vscode.TextEdit(fullRange, formattedContent)];
    }
    provideDocumentRangeFormattingEdits(document, range, options, token) {
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
        const fullRange = new vscode.Range(new vscode.Position(startLine, 0), new vscode.Position(endLine + 1, 0));
        return [new vscode.TextEdit(fullRange, formattedContent)];
    }
}
exports.ADLFormatter = ADLFormatter;
//# sourceMappingURL=formatter.js.map