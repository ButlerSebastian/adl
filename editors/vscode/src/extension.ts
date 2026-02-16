import * as vscode from 'vscode';
import { ADLDiagnosticsProvider } from './diagnostics';

export function activate(context: vscode.ExtensionContext) {
    console.log('ADL DSL extension is now active!');

    const diagnosticsProvider = new ADLDiagnosticsProvider(context);
    const diagnosticCollection = vscode.languages.createDiagnosticCollection('adl');
    context.subscriptions.push(diagnosticCollection);

    const updateDiagnostics = (document: vscode.TextDocument) => {
        if (document.languageId === 'adl') {
            const diagnostics = diagnosticsProvider.provideDiagnostics(document);
            diagnosticCollection.set(document.uri, diagnostics);
        }
    };

    context.subscriptions.push(
        vscode.workspace.onDidOpenTextDocument(updateDiagnostics)
    );

    context.subscriptions.push(
        vscode.workspace.onDidChangeTextDocument(event => {
            updateDiagnostics(event.document);
        })
    );

    context.subscriptions.push(
        vscode.workspace.onDidSaveTextDocument(updateDiagnostics)
    );

    vscode.workspace.textDocuments.forEach(updateDiagnostics);
}

export function deactivate() {
    console.log('ADL DSL extension is now deactivated!');
}
