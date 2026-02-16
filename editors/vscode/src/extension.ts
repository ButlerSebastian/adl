import * as vscode from 'vscode';
import { ADLDiagnosticsProvider } from './diagnostics';
import { ADLCompletionProvider } from './completion';
import { ADLDefinitionProvider } from './definition';
import { ADLHoverProvider } from './hover';
import { ADLFormatter } from './formatter';

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

    const completionProvider = new ADLCompletionProvider();
    context.subscriptions.push(
        vscode.languages.registerCompletionItemProvider(
            'adl',
            completionProvider,
            ':',
            ' ',
            '\n'
        )
    );

    const definitionProvider = new ADLDefinitionProvider();
    context.subscriptions.push(
        vscode.languages.registerDefinitionProvider(
            'adl',
            definitionProvider
        )
    );

    const hoverProvider = new ADLHoverProvider();
    context.subscriptions.push(
        vscode.languages.registerHoverProvider(
            'adl',
            hoverProvider
        )
    );

    const formatterProvider = new ADLFormatter();
    context.subscriptions.push(
        vscode.languages.registerDocumentFormattingEditProvider(
            'adl',
            formatterProvider
        )
    );

    context.subscriptions.push(
        vscode.languages.registerDocumentRangeFormattingEditProvider(
            'adl',
            formatterProvider
        )
    );

    const updateDefinitions = (document: vscode.TextDocument) => {
        if (document.languageId === 'adl') {
            definitionProvider.updateDefinitions(document, vscode.workspace.rootPath || '');
            hoverProvider.updateDefinitions(document);
        }
    };

    context.subscriptions.push(
        vscode.workspace.onDidOpenTextDocument(updateDiagnostics)
    );

    context.subscriptions.push(
        vscode.workspace.onDidChangeTextDocument(event => {
            updateDiagnostics(event.document);
            updateDefinitions(event.document);
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
