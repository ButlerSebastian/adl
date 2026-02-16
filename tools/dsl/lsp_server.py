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
    )
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

    def did_open(self, document: Document):
        """Handle document open event."""
        logger.info(f"Document opened: {document.uri}")
        self.documents[document.uri] = document

    def did_change(self, document: Document):
        """Handle document change event."""
        logger.debug(f"Document changed: {document.uri}")
        self.documents[document.uri] = document

    def did_close(self, document: Document):
        """Handle document close event."""
        logger.info(f"Document closed: {document.uri}")
        if document.uri in self.documents:
            del self.documents[document.uri]

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
            issues = self.linter.lint(document.source)
            diagnostics = []

            for issue in issues:
                severity = DiagnosticSeverity.Error if issue.severity == "error" else DiagnosticSeverity.Warning
                diagnostics.append(
                    Diagnostic(
                        range=Range(
                            start=Position(line=issue.line - 1, character=issue.column - 1),
                            end=Position(line=issue.line - 1, character=issue.column - 1 + len(issue.text) if issue.text else 0),
                        ),
                        message=issue.message,
                        severity=severity,
                        source="adl-linter",
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


def create_server() -> ADLLanguageServer:
    """Create and return ADL Language Server instance."""
    return ADLLanguageServer(protocol_cls=LanguageServerProtocol)


if __name__ == "__main__":
    import sys

    server = create_server()
    server.start_io()
