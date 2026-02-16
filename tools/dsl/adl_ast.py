"""
AST Module for ADL DSL

This module defines the Abstract Syntax Tree (AST) for the ADL DSL,
including all node types and the visitor pattern for AST traversal.
"""

from dataclasses import dataclass, field
from typing import List, Optional, Union, Dict, Any, Generic, TypeVar
from abc import ABC, abstractmethod

T = TypeVar('T')

# ============================================
# Base Classes
# ============================================

@dataclass(eq=False)
class SourceLocation:
    """Source location information for error reporting"""
    line: int
    column: int
    end_line: int
    end_column: int
    file: Optional[str] = None


@dataclass(eq=False)
class ASTNode:
    """Base class for all AST nodes"""
    loc: SourceLocation

    def accept(self, visitor: 'ASTVisitor[T]') -> T:
        """Visitor pattern accept method"""
        method_name = f'visit_{self.__class__.__name__}'
        visitor_method = getattr(visitor, method_name, visitor.visit_default)
        return visitor_method(self)

    def __eq__(self, other: object) -> bool:
        """
        Compare AST nodes for equality, excluding source location.

        This allows comparing AST nodes based on their structure and content
        regardless of where they appear in the source file.

        Args:
            other: Object to compare with

        Returns:
            True if nodes have the same structure and content (excluding location)
        """
        if not isinstance(other, self.__class__):
            return False

        # Compare all fields except 'loc'
        self_dict = self.__dict__.copy()
        other_dict = other.__dict__.copy()
        del self_dict['loc']
        del other_dict['loc']
        return self_dict == other_dict


# ============================================
# Program Structure
# ============================================

@dataclass(eq=False)
class Program(ASTNode):
    """Root node representing entire ADL file"""
    imports: List['ImportStmt']
    declarations: List['Declaration']
    agent: Optional['AgentDef'] = None


@dataclass(eq=False)
class ImportStmt(ASTNode):
    """Import statement"""
    path: str
    alias: Optional[str] = None


# ============================================
# Declarations
# ============================================

Declaration = Union['EnumDef', 'TypeDef']


@dataclass(eq=False)
class EnumDef(ASTNode):
    """Enum definition"""
    name: str
    values: List[str]


@dataclass(eq=False)
class TypeDef(ASTNode):
    """Type definition"""
    name: str
    body: Optional['TypeBody'] = None
    alias: Optional['TypeExpr'] = None


@dataclass(eq=False)
class TypeBody(ASTNode):
    """Object type body containing fields"""
    fields: List['FieldDef']


@dataclass(eq=False)
class FieldDef(ASTNode):
    """Field definition within a type"""
    name: str
    type: 'TypeExpr'
    optional: bool = False


# ============================================
# Type Expressions
# ============================================

TypeExpr = Union[
    'PrimitiveType',
    'TypeReference',
    'ArrayType',
    'UnionType',
    'OptionalType',
    'ConstrainedType'
]


@dataclass(eq=False)
class PrimitiveType(ASTNode):
    """Primitive type (string, integer, etc.)"""
    name: str  # "string", "integer", "number", "boolean", "object", "array", "any", "null"


@dataclass(eq=False)
class TypeReference(ASTNode):
    """Reference to a user-defined type"""
    name: str


@dataclass(eq=False)
class ArrayType(ASTNode):
    """Array type: Type[]"""
    element_type: TypeExpr


@dataclass(eq=False)
class UnionType(ASTNode):
    """Union type: Type1 | Type2"""
    types: List[TypeExpr]


@dataclass(eq=False)
class OptionalType(ASTNode):
    """Optional type: Type?"""
    inner_type: TypeExpr


@dataclass(eq=False)
class ConstrainedType(ASTNode):
    """Type with constraints: Type(min..max)"""
    base_type: TypeExpr
    min_value: Optional[int] = None
    max_value: Optional[int] = None


# ============================================
# Agent Definition
# ============================================

@dataclass(eq=False)
class AgentDef(ASTNode):
    """Agent definition"""
    name: str
    description: Optional[str] = None
    owner: Optional[str] = None
    fields: List[FieldDef] = field(default_factory=list)


# ============================================
# Phase 4: Workflow and Policy Definitions
# ============================================

@dataclass(eq=False)
class WorkflowDef(ASTNode):
    """Workflow definition"""
    id: str
    name: str
    version: str
    description: str
    nodes: Dict[str, 'WorkflowNodeDef']
    edges: List['WorkflowEdgeDef']
    metadata: Dict[str, Any]


@dataclass(eq=False)
class WorkflowNodeDef(ASTNode):
    """Workflow node definition"""
    id: str
    type: str
    label: str
    config: Dict[str, Any]
    position: Dict[str, int]


@dataclass(eq=False)
class WorkflowEdgeDef(ASTNode):
    """Workflow edge definition"""
    id: str
    source: str
    target: str
    relation: str
    condition: Optional[Dict[str, Any]] = None
    metadata: Optional[Dict[str, Any]] = None


@dataclass(eq=False)
class PolicyDef(ASTNode):
    """Policy definition"""
    id: str
    name: str
    version: str
    description: str
    rego: str
    enforcement: 'EnforcementDef'
    data: Dict[str, Any]
    metadata: Dict[str, Any]


@dataclass(eq=False)
class EnforcementDef(ASTNode):
    """Enforcement definition"""
    mode: str  # "strict" | "moderate" | "lenient"
    action: str  # "deny" | "warn" | "log" | "allow"
    audit_log: bool


@dataclass(eq=False)
class PolicyDataDef(ASTNode):
    """Policy data definition"""
    roles: Dict[str, List[str]]
    permissions: Dict[str, Any]


# ============================================
# Visitor Pattern
# ============================================

class ASTVisitor(ABC, Generic[T]):
    """Base visitor class for AST traversal"""

    def visit(self, node: ASTNode) -> T:
        """Visit a node"""
        return node.accept(self)

    def visit_default(self, node: ASTNode) -> T:
        """Default visitor for unhandled node types"""
        raise NotImplementedError(f"No visitor for {type(node).__name__}")

    # Program structure
    @abstractmethod
    def visit_Program(self, node: Program) -> T: ...

    @abstractmethod
    def visit_ImportStmt(self, node: ImportStmt) -> T: ...

    # Declarations
    @abstractmethod
    def visit_EnumDef(self, node: EnumDef) -> T: ...

    @abstractmethod
    def visit_TypeDef(self, node: TypeDef) -> T: ...

    @abstractmethod
    def visit_TypeBody(self, node: TypeBody) -> T: ...

    @abstractmethod
    def visit_FieldDef(self, node: FieldDef) -> T: ...

    # Type expressions
    @abstractmethod
    def visit_PrimitiveType(self, node: PrimitiveType) -> T: ...

    @abstractmethod
    def visit_TypeReference(self, node: TypeReference) -> T: ...

    @abstractmethod
    def visit_ArrayType(self, node: ArrayType) -> T: ...

    @abstractmethod
    def visit_UnionType(self, node: UnionType) -> T: ...

    @abstractmethod
    def visit_OptionalType(self, node: OptionalType) -> T: ...

    @abstractmethod
    def visit_ConstrainedType(self, node: ConstrainedType) -> T: ...

    # Agent
    @abstractmethod
    def visit_AgentDef(self, node: AgentDef) -> T: ...

    # Phase 4: Workflow and Policy
    @abstractmethod
    def visit_WorkflowDef(self, node: WorkflowDef) -> T: ...

    @abstractmethod
    def visit_WorkflowNodeDef(self, node: WorkflowNodeDef) -> T: ...

    @abstractmethod
    def visit_WorkflowEdgeDef(self, node: WorkflowEdgeDef) -> T: ...

    @abstractmethod
    def visit_PolicyDef(self, node: PolicyDef) -> T: ...

    @abstractmethod
    def visit_EnforcementDef(self, node: EnforcementDef) -> T: ...


class PrintVisitor(ASTVisitor[str]):
    """Example visitor that prints AST structure"""

    def __init__(self):
        self.indent = 0

    def _indent(self) -> str:
        return "  " * self.indent

    def visit_Program(self, node: Program) -> str:
        lines = [f"{self._indent()}Program"]
        self.indent += 1
        for imp in node.imports:
            lines.append(self.visit(imp))
        for decl in node.declarations:
            lines.append(self.visit(decl))
        if node.agent:
            lines.append(self.visit(node.agent))
        self.indent -= 1
        return "\n".join(lines)

    def visit_ImportStmt(self, node: ImportStmt) -> str:
        alias = f" as {node.alias}" if node.alias else ""
        return f"{self._indent()}Import: {node.path}{alias}"

    def visit_EnumDef(self, node: EnumDef) -> str:
        return f"{self._indent()}Enum: {node.name} = [{', '.join(node.values)}]"

    def visit_TypeDef(self, node: TypeDef) -> str:
        lines = [f"{self._indent()}Type: {node.name}"]
        if node.body:
            self.indent += 1
            lines.append(self.visit(node.body))
            self.indent -= 1
        return "\n".join(lines)

    def visit_TypeBody(self, node: TypeBody) -> str:
        lines = [f"{self._indent()}Fields:"]
        self.indent += 1
        for field in node.fields:
            lines.append(self.visit(field))
        self.indent -= 1
        return "\n".join(lines)

    def visit_FieldDef(self, node: FieldDef) -> str:
        opt = "?" if node.optional else ""
        return f"{self._indent()}{node.name}{opt}: {self.visit(node.type)}"

    def visit_PrimitiveType(self, node: PrimitiveType) -> str:
        return node.name

    def visit_TypeReference(self, node: TypeReference) -> str:
        return node.name

    def visit_ArrayType(self, node: ArrayType) -> str:
        return f"{self.visit(node.element_type)}[]"

    def visit_UnionType(self, node: UnionType) -> str:
        return " | ".join(self.visit(t) for t in node.types)

    def visit_OptionalType(self, node: OptionalType) -> str:
        return f"{self.visit(node.inner_type)}?"

    def visit_ConstrainedType(self, node: ConstrainedType) -> str:
        base = self.visit(node.base_type)
        if node.max_value:
            return f"{base}({node.min_value}..{node.max_value})"
        return f"{base}({node.min_value}..)"

    def visit_AgentDef(self, node: AgentDef) -> str:
        lines = [f"{self._indent()}Agent: {node.name}"]
        self.indent += 1
        for field in node.fields:
            lines.append(self.visit(field))
        self.indent -= 1
        return "\n".join(lines)