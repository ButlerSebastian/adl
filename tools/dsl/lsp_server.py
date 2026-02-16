"""
ADL Language Server Protocol (LSP) Server

Provides language features for ADL files in multiple editors.
"""

import logging
from typing import List, Optional, Dict, Any
from pathlib import Path

try:
    from pygls.server import LanguageServer
    from pygls.protocol import LanguageServerProtocol
    from pygls.workspace import Document
    from pygls.lsp import (
        InitializeParams,
        InitializeResult,
        ServerCapabilities,
        TextDocumentSyncKind,
        CompletionOptions,
        CompletionParams,
        CompletionItem,
        CompletionItemKind,
        DefinitionParams,
        Location,
        HoverParams,
        Hover,
        Diagnostic,
        DiagnosticSeverity,
        Position,
        Range,
        DidOpenTextDocumentParams,
        DidChangeTextDocumentParams,
        DidCloseTextDocumentParams,
        PublishDiagnosticsParams,
    )
    from pygls.protocol import default_language_server_protocol
except ImportError:
    raise ImportError(
        "pygls is required for LSP server. Install with: pip install pygls"
    )

from .parser import ADLParser
from .linter import ADLLinter
from .formatter import ADLFormatter


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ADLLanguageServer(LanguageServer):
    """ADL Language Server implementation."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.parser: Optional[ADLParser] = None
        self.linter: Optional[ADLLinter] = None
        self.formatter: Optional[ADLFormatter] = None
        self.documents: Dict[str, Document] = {}

    def initialize(self, params: InitializeParams) -> InitializeResult:
        """Initialize the language server."""
        logger.info("Initializing ADL Language Server")

        self.parser = ADLParser()
        self.linter = ADLLinter()
        self.formatter = ADLFormatter()

        capabilities = ServerCapabilities(
            text_document_sync=TextDocumentSyncKind.FULL,
            completion_provider=CompletionOptions(
                trigger_characters=[":", " ", "\n"],
                resolve_provider=False,
            ),
            definition_provider=True,
            hover_provider=True,
            document_formatting_provider=True,
            document_range_formatting_provider=True,
        )

        return InitializeResult(capabilities=capabilities)

    @default_language_server_protocol.feature("textDocument/didOpen")
    async def did_open(self, params: DidOpenTextDocumentParams):
        """Handle document open event."""
        document = self.workspace.get_document(params.text_document.uri)
        logger.info(f"Document opened: {document.uri}")
        self.documents[document.uri] = document
        diagnostics = self.validate_document(document)
        self.lsp.publish_diagnostics(
            PublishDiagnosticsParams(uri=document.uri, diagnostics=diagnostics)
        )

    @default_language_server_protocol.feature("textDocument/didChange")
    async def did_change(self, params: DidChangeTextDocumentParams):
        """Handle document change event."""
        document = self.workspace.get_document(params.text_document.uri)
        logger.debug(f"Document changed: {document.uri}")
        self.documents[document.uri] = document
        diagnostics = self.validate_document(document)
        self.lsp.publish_diagnostics(
            PublishDiagnosticsParams(uri=document.uri, diagnostics=diagnostics)
        )

    @default_language_server_protocol.feature("textDocument/didClose")
    async def did_close(self, params: DidCloseTextDocumentParams):
        """Handle document close event."""
        document = self.workspace.get_document(params.text_document.uri)
        logger.info(f"Document closed: {document.uri}")
        if document.uri in self.documents:
            del self.documents[document.uri]
        self.lsp.publish_diagnostics(
            PublishDiagnosticsParams(uri=document.uri, diagnostics=[])
        )

    def get_document(self, uri: str) -> Optional[Document]:
        """Get document by URI."""
        return self.documents.get(uri)

    def parse_document(self, document: Document) -> Optional[Any]:
        """Parse ADL document."""
        if not self.parser:
            return None

        try:
            return self.parser.parse(document.source)
        except Exception as e:
            logger.error(f"Failed to parse document {document.uri}: {e}")
            return None

    def validate_document(self, document: Document) -> List[Diagnostic]:
        """Validate ADL document and return diagnostics."""
        if not self.linter:
            return []

        try:
            issues = self.linter.lint_content(document.source)
            diagnostics = []

            for issue in issues:
                severity = DiagnosticSeverity.Error if issue.severity == "error" else DiagnosticSeverity.Warning
                diagnostics.append(
                    Diagnostic(
                        range=Range(
                            start=Position(line=issue.line_number - 1, character=0),
                            end=Position(line=issue.line_number - 1, character=100),
                        ),
                        message=issue.message,
                        severity=severity,
                        source="adl-linter",
                        code=issue.rule_name,
                    )
                )

            return diagnostics
        except Exception as e:
            logger.error(f"Failed to validate document {document.uri}: {e}")
            return []

    def format_document(self, document: Document) -> str:
        """Format ADL document."""
        if not self.formatter:
            return document.source

        try:
            return self.formatter.format(document.source)
        except Exception as e:
            logger.error(f"Failed to format document {document.uri}: {e}")
            return document.source

    @default_language_server_protocol.feature("textDocument/completion")
    async def completion(self, params: CompletionParams) -> List[CompletionItem]:
        """Provide completion items."""
        document = self.workspace.get_document(params.text_document.uri)
        if not document:
            return []

        line = document.lines[params.position.line]
        char_before = line[:params.position.character]

        items = []

        if char_before.endswith(":"):
            items.extend(self._get_type_completions())
        elif char_before.endswith(" ") or char_before.endswith("\n"):
            items.extend(self._get_keyword_completions())
            items.extend(self._get_boolean_completions())
        else:
            items.extend(self._get_all_completions())

        return items

    def _get_keyword_completions(self) -> List[CompletionItem]:
        """Get keyword completions."""
        keywords = [
            "type", "enum", "agent", "import", "description",
            "fields", "values", "tools", "rag", "llm", "llm_settings",
            "permissions", "dependencies", "governance", "name",
            "role", "owner", "version", "category", "subcategory",
            "parameters", "returns", "invocation", "type", "required",
            "minLength", "maxLength", "minimum", "maximum", "pattern",
            "enum", "default", "description"
        ]

        return [
            CompletionItem(
                label=keyword,
                kind=CompletionItemKind.Keyword,
                detail="ADL keyword"
            )
            for keyword in keywords
        ]

    def _get_type_completions(self) -> List[CompletionItem]:
        """Get type completions."""
        types = [
            "string", "number", "integer", "boolean", "array",
            "object", "any", "null", "datetime", "uri", "email"
        ]

        return [
            CompletionItem(
                label=type_name,
                kind=CompletionItemKind.Class,
                detail="ADL type"
            )
            for type_name in types
        ]

    def _get_boolean_completions(self) -> List[CompletionItem]:
        """Get boolean completions."""
        return [
            CompletionItem(
                label="true",
                kind=CompletionItemKind.Value,
                detail="Boolean value"
            ),
            CompletionItem(
                label="false",
                kind=CompletionItemKind.Value,
                detail="Boolean value"
            )
        ]

    def _get_all_completions(self) -> List[CompletionItem]:
        """Get all completions."""
        items = []
        items.extend(self._get_keyword_completions())
        items.extend(self._get_type_completions())
        items.extend(self._get_boolean_completions())
        return items

    @default_language_server_protocol.feature("textDocument/definition")
    async def definition(self, params: DefinitionParams) -> Optional[List[Location]]:
        """Provide go-to-definition support."""
        document = self.workspace.get_document(params.text_document.uri)
        if not document:
            return None

        ast = self.parse_document(document)
        if not ast:
            return None

        word = self._get_word_at_position(document, params.position)
        if not word:
            return None

        locations = []

        for type_def in getattr(ast, 'types', []):
            if type_def.name == word:
                locations.append(
                    Location(
                        uri=document.uri,
                        range=Range(
                            start=Position(line=type_def.line - 1, character=0),
                            end=Position(line=type_def.line - 1, character=100),
                        )
                    )
                )

        for enum_def in getattr(ast, 'enums', []):
            if enum_def.name == word:
                locations.append(
                    Location(
                        uri=document.uri,
                        range=Range(
                            start=Position(line=enum_def.line - 1, character=0),
                            end=Position(line=enum_def.line - 1, character=100),
                        )
                    )
                )

        return locations if locations else None

    def _get_word_at_position(self, document: Document, position: Position) -> Optional[str]:
        """Get word at cursor position."""
        line = document.lines[position.line]
        if position.character >= len(line):
            return None

        start = position.character
        while start > 0 and (line[start - 1].isalnum() or line[start - 1] == '_'):
            start -= 1

        end = position.character
        while end < len(line) and (line[end].isalnum() or line[end] == '_'):
            end += 1

        return line[start:end]


def create_server() -> ADLLanguageServer:
    """Create and return ADL Language Server instance."""
    return ADLLanguageServer(protocol_cls=LanguageServerProtocol)


if __name__ == "__main__":
    import sys

    server = create_server()
    server.start_io()
