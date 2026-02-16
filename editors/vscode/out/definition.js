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
exports.ADLDefinitionProvider = void 0;
const vscode = __importStar(require("vscode"));
const path = __importStar(require("path"));
const fs = __importStar(require("fs"));
class ADLDefinitionProvider {
    constructor() {
        this.typeDefinitions = new Map();
        this.enumDefinitions = new Map();
        this.importedTypes = new Map();
    }
    provideDefinition(document, position, token) {
        const wordRange = document.getWordRangeAtPosition(position);
        if (!wordRange) {
            return null;
        }
        const word = document.getText(wordRange);
        if (this.typeDefinitions.has(word)) {
            return this.typeDefinitions.get(word);
        }
        if (this.enumDefinitions.has(word)) {
            return this.enumDefinitions.get(word);
        }
        const importedType = this.importedTypes.get(word);
        if (importedType) {
            return this.findDefinitionInFile(importedType, word);
        }
        return null;
    }
    findDefinitionInFile(filePath, typeName) {
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
    updateDefinitions(document, workspaceRoot) {
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
            }
            else if (line.startsWith('type ')) {
                const match = line.match(/type\s+(\w+)/);
                if (match) {
                    const typeName = match[1];
                    const position = new vscode.Position(i, line.indexOf(typeName));
                    this.typeDefinitions.set(typeName, new vscode.Location(document.uri, position));
                }
            }
            else if (line.startsWith('enum ')) {
                const match = line.match(/enum\s+(\w+)/);
                if (match) {
                    const enumName = match[1];
                    const position = new vscode.Position(i, line.indexOf(enumName));
                    this.enumDefinitions.set(enumName, new vscode.Location(document.uri, position));
                }
            }
        }
    }
    parseImportStatement(line, currentFilePath, workspaceRoot) {
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
exports.ADLDefinitionProvider = ADLDefinitionProvider;
//# sourceMappingURL=definition.js.map