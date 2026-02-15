# ADL DSL Revamp Plan: Making DSL the Primary Schema Definition Format

## Executive Summary

This document outlines a comprehensive plan to revamp ADL (Agent Definition Language) to use DSL (Domain-Specific Language) as the primary schema definition format, replacing JSON Schema as the source of truth. JSON Schema will become a generated artifact from DSL, not the primary definition format.

**Current State:** JSON Schema is primary, DSL is experimental  
**Target State:** DSL is primary, JSON Schema is generated from DSL  
**Timeline:** 6 months (24 weeks) across 5 phases

---

## 1. Current State Analysis

### 1.1 JSON Schema Usage

**Primary Schema Files:**
- `schema/agent-definition.schema.json` - Main schema (136 lines, v1.x compatible)
- `schema/agent-definition-dsl.schema.json` - DSL-generated schema (1231 lines, v2.0)
- `schema/multi-model.schema.json` - Multi-model extensions
- `schema/components/` - Modular component schemas:
  - `tool/definition.json`, `parameter.json`
  - `rag/index.json`
  - `memory/config.json`, `definition.json`
  - `agent/role.json`
  - `common/types.json`, `key-schema.json`

**Validation Tools:**
- `tools/validate.py` - Python-based validation using jsonschema
- `tools/validate.js` - Node.js validation using AJV
- `validate_examples.js` - Batch validation script
- `tools/validate-model-routing.py` - Model routing validation
- `tools/validate-external.py` - External validation

**Documentation:**
- `docs/schema-reference.md` - JSON Schema field reference
- `docs/adl-dsl-design.md` - DSL design document
- `docs/migration-v1.5.md` - v1.5 migration guide

### 1.2 DSL Implementation Status

**Existing DSL Infrastructure:**
- `schema/agent-definition.adl` - Complete DSL schema definition (441 lines)
- `tools/adl_dsl_compiler.py` - DSL to JSON Schema compiler (473 lines)
- `tools/adl_dsl_validator.py` - DSL-based validator (144 lines)

**DSL Capabilities:**
- ✅ Enum definitions
- ✅ Type definitions with properties
- ✅ Array types with constraints
- ✅ Optional fields (using `?` suffix)
- ✅ Union types (using `|` operator)
- ✅ Range constraints (e.g., `integer (1..10)`)
- ✅ Import system for modularization
- ✅ Generates JSON Schema with `$defs`
- ✅ Generates TypeScript type definitions

**DSL Limitations:**
- ❌ No validation rules section implementation
- ❌ Limited error messages
- ❌ No DSL linter
- ❌ No DSL formatter
- ❌ Import resolution not fully implemented
- ❌ Type expansion needs improvement for complex nested types
- ❌ No IDE support (syntax highlighting, autocomplete)

### 1.3 Example Files

11 example files in `examples/`:
- `minimal_agent.json`
- `multi_agent_team.json`
- `memory_agent.json`
- `advanced_rag_agent.json`
- `multi_model_agent.json`
- `event_driven_agent.json`
- `constrained_agent.json`
- `research_assistant_agent.json`
- `product_advisor_agent.json`
- `customer_support_agent.json`
- `creative_producer_agent.json`

All examples currently validate against JSON Schema.

---

## 2. Revamp Goals

### 2.1 Primary Goals

1. **Make DSL the Source of Truth**
   - All schema definitions written in DSL
   - JSON Schema generated automatically from DSL
   - No manual editing of JSON Schema files

2. **Improve Developer Experience**
   - Better error messages from DSL compiler
   - IDE support with syntax highlighting
   - Auto-formatting and linting
   - Interactive validation

3. **Enable True Modularization**
   - Import/export system for schema components
   - Reusable type definitions across projects
   - Versioned module system

4. **Maintain Backward Compatibility**
   - Existing JSON Schema files continue to work
   - Migration path for existing users
   - Gradual deprecation of JSON Schema editing

### 2.2 Success Criteria

- [ ] All 11 example files validate against DSL-generated schema
- [ ] DSL compiler produces identical JSON Schema to current manual version
- [ ] CI/CD pipeline uses DSL for validation
- [ ] Documentation updated to use DSL as primary format
- [ ] IDE extensions available for at least VS Code
- [ ] Zero breaking changes for existing users
- [ ] Migration guide published and tested

---

## 3. Phased Migration Plan

### Phase 1: Foundation (Weeks 1-4)

**Goal:** Stabilize DSL compiler and establish tooling infrastructure

#### 3.1.1 DSL Compiler Improvements

**Tasks:**
- [ ] Implement proper import resolution system
  - Resolve relative imports (`import schema/components/rag`)
  - Support absolute imports from project root
  - Handle circular dependency detection
  - Cache resolved modules

- [ ] Enhance type expansion
  - Fix nested type reference resolution
  - Support deeply nested object types
  - Handle recursive type definitions
  - Optimize type expansion performance

- [ ] Add validation rules section
  - Parse `validation { ... }` blocks
  - Generate JSON Schema validation keywords
  - Support custom validation functions
  - Implement cross-field validation

- [ ] Improve error reporting
  - Line and column numbers for errors
  - Contextual error messages
  - Suggestions for fixes
  - Error codes for documentation

**Deliverables:**
- `tools/adl_dsl_compiler_v2.py` - Enhanced compiler
- `tests/test_dsl_compiler.py` - Comprehensive test suite
- `docs/dsl-compiler-errors.md` - Error reference

#### 3.1.2 DSL Parser Enhancement

**Tasks:**
- [ ] Implement formal grammar (using PLY or Lark)
  - Define complete DSL grammar
  - Generate parser from grammar
  - Add syntax error recovery

- [ ] Add AST (Abstract Syntax Tree) generation
  - Structured representation of DSL
  - Visitor pattern for transformations
  - Source location tracking

- [ ] Support for comments and documentation
  - Docstring extraction
  - Comment preservation in AST
  - Generate schema descriptions from comments

**Deliverables:**
- `tools/dsl/parser.py` - Formal parser
- `tools/dsl/ast.py` - AST definitions
- `tools/dsl/grammar.lark` - Grammar specification

#### 3.1.3 Testing Infrastructure

**Tasks:**
- [ ] Create DSL test suite
  - Unit tests for parser
  - Unit tests for compiler
  - Integration tests for full pipeline
  - Property-based tests for type system

- [ ] Set up test fixtures
  - Minimal DSL files for each feature
  - Edge cases and error conditions
  - Complex real-world examples

- [ ] Add CI integration
  - GitHub Actions workflow
  - Automated testing on PR
  - Coverage reporting

**Deliverables:**
- `tests/dsl/` - Test directory
- `.github/workflows/dsl-tests.yml` - CI workflow
- `tests/fixtures/dsl/` - Test fixtures

**Milestone 1:** DSL compiler v2 passes all tests and generates valid JSON Schema

---

### Phase 2: Tooling (Weeks 5-10)

**Goal:** Build complete DSL toolchain

#### 3.2.1 DSL CLI Tool

**Tasks:**
- [ ] Create unified CLI: `adl` command
  ```bash
  adl compile <file.adl> -o <output.json>
  adl validate <file.json> --schema <file.adl>
  adl format <file.adl>
  adl lint <file.adl>
  adl generate-types <file.adl> -o <types.d.ts>
  adl generate-docs <file.adl> -o <docs.md>
  ```

- [ ] Implement `adl compile`
  - Compile DSL to JSON Schema
  - Watch mode for development
  - Source map generation
  - Multiple output formats

- [ ] Implement `adl validate`
  - Validate JSON against DSL schema
  - Batch validation
  - Custom validation rules
  - Exit codes for CI

- [ ] Implement `adl format`
  - Consistent formatting
  - Configurable style rules
  - Check mode for CI
  - In-place formatting

- [ ] Implement `adl lint`
  - Style guidelines
  - Best practices
  - Deprecation warnings
  - Custom rules support

**Deliverables:**
- `tools/adl/cli.py` - CLI implementation
- `tools/adl/__main__.py` - Entry point
- `setup.py` - Package installation

#### 3.2.2 DSL Linter

**Tasks:**
- [ ] Define linting rules
  - Naming conventions
  - Required documentation
  - Type usage best practices
  - Import organization

- [ ] Implement rule engine
  - Configurable rules
  - Severity levels (error, warning, info)
  - Rule suppression
  - Custom rule plugins

- [ ] Add autofix capabilities
  - Auto-fixable rules
  - Safe vs unsafe fixes
  - Dry-run mode

**Deliverables:**
- `tools/adl/linter.py` - Linter implementation
- `tools/adl/rules/` - Rule definitions
- `.adllintrc` - Configuration file

#### 3.2.3 DSL Formatter

**Tasks:**
- [ ] Implement pretty printer
  - Consistent indentation
  - Line wrapping
  - Comment preservation
  - Import sorting

- [ ] Add configuration options
  - Indent size (2/4 spaces)
  - Max line length
  - Trailing commas
  - Quote style

- [ ] IDE integration
  - Format on save
  - Format selection
  - Format check in CI

**Deliverables:**
- `tools/adl/formatter.py` - Formatter implementation
- `.adlformatrc` - Configuration file

#### 3.2.4 IDE Support

**Tasks:**
- [ ] VS Code Extension
  - Syntax highlighting
  - Error diagnostics
  - Auto-completion
  - Go to definition
  - Hover information
  - Format on save

- [ ] Language Server Protocol (LSP)
  - LSP server implementation
  - Diagnostics provider
  - Completion provider
  - Definition provider
  - Hover provider

- [ ] Other editors (optional)
  - Vim plugin
  - Emacs mode
  - Sublime Text package

**Deliverables:**
- `editors/vscode/` - VS Code extension
- `tools/adl/lsp_server.py` - LSP implementation
- Published extension on marketplace

**Milestone 2:** Complete toolchain available with IDE support

---

### Phase 3: Migration (Weeks 11-16)

**Goal:** Migrate existing schemas and examples to DSL

#### 3.3.1 Schema Conversion

**Tasks:**
- [ ] Convert component schemas to DSL
  - `schema/components/tool/definition.adl`
  - `schema/components/tool/parameter.adl`
  - `schema/components/rag/index.adl`
  - `schema/components/memory/config.adl`
  - `schema/components/agent/role.adl`
  - `schema/components/common/types.adl`

- [ ] Create modular DSL structure
  ```
  schema/
  ├── agent-definition.adl          # Main schema
  ├── components/
  │   ├── tool/
  │   │   ├── definition.adl
  │   │   └── parameter.adl
  │   ├── rag/
  │   │   └── index.adl
  │   ├── memory/
  │   │   └── config.adl
  │   ├── agent/
  │   │   └── role.adl
  │   └── common/
  │       └── types.adl
  └── generated/
      └── agent-definition.schema.json  # Generated
  ```

- [ ] Implement module system
  - Export declarations
  - Import resolution
  - Namespace handling
  - Version management

**Deliverables:**
- All component schemas in DSL format
- Module system implementation
- Import/export documentation

#### 3.3.2 Build System Integration

**Tasks:**
- [ ] Create build scripts
  - `scripts/build-schema.py` - Generate JSON Schema from DSL
  - `scripts/validate-examples.py` - Validate all examples
  - `scripts/check-dsl.sh` - CI check script

- [ ] Update package.json / setup.py
  - Build commands
  - Pre-commit hooks
  - Development scripts

- [ ] GitHub Actions workflow
  - Validate DSL on PR
  - Generate and commit JSON Schema
  - Check examples validation
  - Lint DSL files

**Deliverables:**
- `scripts/build-schema.py`
- `.github/workflows/dsl-ci.yml`
- `Makefile` with common tasks

#### 3.3.3 Documentation Migration

**Tasks:**
- [ ] Update README.md
  - DSL as primary format
  - Quick start with DSL
  - Installation instructions

- [ ] Create DSL tutorial
  - Getting started guide
  - Syntax reference
  - Examples walkthrough
  - Best practices

- [ ] Update schema-reference.md
  - DSL-first documentation
  - Generated from DSL comments
  - Interactive examples

- [ ] Create migration guide
  - For JSON Schema users
  - Step-by-step migration
  - Common patterns
  - Troubleshooting

**Deliverables:**
- `docs/dsl-tutorial.md`
- `docs/dsl-reference.md`
- `docs/migrating-from-json-schema.md`
- Updated README.md

#### 3.3.4 Example Conversion

**Tasks:**
- [ ] Create DSL versions of examples
  - `examples/minimal_agent.adl`
  - `examples/multi_agent_team.adl`
  - All 11 examples

- [ ] Add example validation
  - Validate DSL examples compile
  - Validate JSON examples against DSL schema
  - Round-trip testing

**Deliverables:**
- All examples in DSL format
- `examples/README.md` with both formats

**Milestone 3:** All schemas migrated, documentation updated, CI passing

---

### Phase 4: Enhancement (Weeks 17-20)

**Goal:** Add advanced features and optimizations

#### 3.4.1 Advanced DSL Features

**Tasks:**
- [ ] Schema versioning
  - Version declarations in DSL
  - Migration scripts between versions
  - Compatibility checking

- [ ] Generic types
  - `type Container<T> { items: T[] }`
  - Type parameters
  - Constraints on generics

- [ ] Conditional types
  - `type X = if (condition) then A else B`
  - Schema composition

- [ ] Decorators/annotations
  - `@deprecated`
  - `@experimental`
  - `@since(version)`
  - Custom annotations

**Deliverables:**
- Enhanced DSL grammar
- Updated compiler
- Feature documentation

#### 3.4.2 Code Generation

**Tasks:**
- [ ] TypeScript generation
  - Interfaces and types
  - Validation functions
  - Runtime type checking

- [ ] Python generation
  - Dataclasses
  - Pydantic models
  - Validation functions

- [ ] Go generation
  - Structs
  - JSON tags
  - Validation methods

- [ ] OpenAPI generation
  - Convert DSL to OpenAPI spec
  - Component schemas
  - Documentation

**Deliverables:**
- `tools/adl/generators/typescript.py`
- `tools/adl/generators/python.py`
- `tools/adl/generators/go.py`
- `tools/adl/generators/openapi.py`

#### 3.4.3 Performance Optimization

**Tasks:**
- [ ] Compiler performance
  - Incremental compilation
  - Parallel processing
  - Caching

- [ ] Validation performance
  - Compiled validators
  - Lazy validation
  - Streaming validation

- [ ] Memory optimization
  - Efficient AST representation
  - Shared immutable structures

**Deliverables:**
- Performance benchmarks
- Optimization documentation
- Profiling tools

**Milestone 4:** Advanced features complete, performance optimized

---

### Phase 5: Deprecation & Adoption (Weeks 21-24)

**Goal:** Deprecate JSON Schema editing, drive adoption

#### 3.5.1 Deprecation Strategy

**Tasks:**
- [ ] Mark JSON Schema as generated
  - Add header comment: "GENERATED FILE - DO NOT EDIT"
  - Update file permissions (read-only)
  - Git hooks to prevent manual edits

- [ ] Deprecation warnings
  - Warning in validation tools
  - Migration notices in documentation
  - Console warnings when using old tools

- [ ] Sunset timeline
  - Phase 1: Warning (months 1-3)
  - Phase 2: Deprecation (months 4-6)
  - Phase 3: Removal (month 7+)

**Deliverables:**
- Deprecation notices
- Migration timeline document
- Automated migration tools

#### 3.5.2 Community Adoption

**Tasks:**
- [ ] Release management
  - Version 2.0.0 announcement
  - Release notes
  - Migration webinar

- [ ] Community support
  - FAQ document
  - Troubleshooting guide
  - Discord/Slack channel
  - Office hours

- [ ] External integrations
  - Partner outreach
  - Integration guides
  - Case studies

**Deliverables:**
- Release announcement
- Community resources
- Partner integrations

#### 3.5.3 Monitoring & Feedback

**Tasks:**
- [ ] Analytics
  - DSL adoption metrics
  - Error tracking
  - Performance monitoring

- [ ] Feedback collection
  - User surveys
  - Issue tracking
  - Feature requests

- [ ] Continuous improvement
  - Regular releases
  - Bug fixes
  - Feature enhancements

**Deliverables:**
- Analytics dashboard
- Feedback system
- Improvement roadmap

**Milestone 5:** JSON Schema editing deprecated, community actively using DSL

---

## 4. Tooling Requirements

### 4.1 Required Tools

| Tool | Purpose | Priority | Phase |
|------|---------|----------|-------|
| DSL Compiler | Compile DSL to JSON Schema | Critical | 1 |
| DSL Validator | Validate agents against DSL | Critical | 1 |
| DSL Linter | Check DSL style/best practices | High | 2 |
| DSL Formatter | Format DSL consistently | High | 2 |
| CLI Tool | Unified command interface | Critical | 2 |
| VS Code Extension | IDE support | High | 2 |
| LSP Server | Language server protocol | Medium | 2 |
| TypeScript Generator | Generate TS types | Medium | 4 |
| Python Generator | Generate Python types | Medium | 4 |
| Documentation Generator | Generate docs from DSL | Medium | 3 |

### 4.2 Tool Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                         CLI (adl)                           │
├─────────────┬─────────────┬─────────────┬───────────────────┤
│   compile   │   validate  │    lint     │      format       │
├─────────────┴─────────────┴─────────────┴───────────────────┤
│                      DSL Parser (AST)                       │
├─────────────────────────────────────────────────────────────┤
│                    Import Resolution                        │
├─────────────────────────────────────────────────────────────┤
│              Type System & Validation Engine                │
├─────────────────────────────────────────────────────────────┤
│  JSON Schema Generator  │  Code Generators  │  Doc Generator│
└─────────────────────────────────────────────────────────────┘
```

---

## 5. Documentation Requirements

### 5.1 Required Documentation

| Document | Purpose | Priority | Phase |
|----------|---------|----------|-------|
| DSL Tutorial | Getting started with DSL | Critical | 3 |
| DSL Reference | Complete syntax reference | Critical | 3 |
| Migration Guide | JSON Schema → DSL | Critical | 3 |
| API Documentation | Tool API reference | High | 2 |
| Best Practices | DSL style guide | High | 3 |
| Error Reference | Error codes and fixes | Medium | 1 |
| IDE Setup | Editor configuration | Medium | 2 |
| Advanced Topics | Generics, versioning | Low | 4 |

### 5.2 Documentation Structure

```
docs/
├── README.md                    # Documentation index
├── dsl/
│   ├── tutorial.md              # Getting started
│   ├── reference.md             # Syntax reference
│   ├── best-practices.md        # Style guide
│   └── examples.md              # Example gallery
├── migration/
│   ├── from-json-schema.md      # Migration guide
│   ├── changelog.md             # DSL changes
│   └── troubleshooting.md       # Common issues
├── tools/
│   ├── cli.md                   # CLI reference
│   ├── compiler.md              # Compiler docs
│   ├── linter.md                # Linter rules
│   └── ide-setup.md             # Editor setup
└── advanced/
    ├── versioning.md            # Schema versioning
    ├── generics.md              # Generic types
    └── code-generation.md       # Generators
```

---

## 6. Testing Requirements

### 6.1 Test Categories

| Category | Description | Coverage Target |
|----------|-------------|-----------------|
| Unit Tests | Parser, compiler, validators | 90% |
| Integration Tests | End-to-end workflows | 80% |
| Property Tests | Type system properties | 70% |
| Performance Tests | Compilation speed | Benchmarks |
| Compatibility Tests | JSON Schema equivalence | 100% |

### 6.2 Test Requirements

**DSL Compiler Tests:**
- [ ] Parse all valid DSL constructs
- [ ] Reject invalid DSL with proper errors
- [ ] Generate valid JSON Schema
- [ ] Handle all edge cases
- [ ] Performance benchmarks

**Validation Tests:**
- [ ] All 11 examples validate
- [ ] Invalid examples are rejected
- [ ] Error messages are helpful
- [ ] Custom validation rules work

**Integration Tests:**
- [ ] Full pipeline: DSL → JSON → Validation
- [ ] Import resolution
- [ ] Module system
- [ ] CLI commands

**Regression Tests:**
- [ ] Generated schema matches current JSON Schema
- [ ] All existing tests pass
- [ ] No breaking changes

---

## 7. Backward Compatibility Strategy

### 7.1 Compatibility Levels

**Level 1: Full Compatibility (Months 1-6)**
- JSON Schema files remain editable
- DSL is opt-in
- All existing tools work
- No breaking changes

**Level 2: Soft Deprecation (Months 7-12)**
- JSON Schema marked as generated
- Warnings when editing JSON Schema
- DSL recommended for new work
- Migration tools available

**Level 3: Hard Deprecation (Months 13-18)**
- JSON Schema is read-only
- CI rejects manual JSON Schema edits
- DSL is default
- Legacy support mode available

**Level 4: Removal (Month 19+)**
- JSON Schema editing no longer supported
- DSL is the only format
- Legacy tools removed

### 7.2 Migration Path

**For Schema Authors:**
1. Install new DSL toolchain
2. Convert existing JSON Schema to DSL (automated tool)
3. Validate DSL compiles to identical JSON Schema
4. Update workflows to use DSL
5. Commit both DSL and generated JSON Schema

**For Tool Users:**
1. No immediate changes required
2. Gradual migration to new CLI
3. Old tools supported during deprecation period

**For CI/CD:**
1. Add DSL validation step
2. Generate JSON Schema in build
3. Eventually remove JSON Schema from repo

---

## 8. Success Criteria

### 8.1 Technical Success Criteria

- [ ] **Schema Equivalence**: DSL-generated JSON Schema is byte-for-byte identical to current schema (or documented differences)
- [ ] **Validation Parity**: All 11 examples validate against DSL-generated schema
- [ ] **Performance**: DSL compilation < 1 second for main schema
- [ ] **Test Coverage**: > 90% code coverage for DSL tools
- [ ] **Zero Breaking Changes**: All existing usage patterns continue to work

### 8.2 Adoption Success Criteria

- [ ] **Documentation**: All docs updated to use DSL as primary format
- [ ] **Examples**: All examples available in DSL format
- [ ] **IDE Support**: VS Code extension with > 1000 downloads
- [ ] **Community**: Active community using DSL
- [ ] **Deprecation**: JSON Schema editing deprecated within 6 months

### 8.3 Business Success Criteria

- [ ] **Developer Satisfaction**: Positive feedback on DSL experience
- [ ] **Adoption Rate**: > 80% of new schemas written in DSL
- [ ] **Migration Completion**: > 90% of existing schemas migrated
- [ ] **Support Burden**: No increase in support tickets

---

## 9. Risk Assessment

### 9.1 Risks and Mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| DSL compiler bugs | Medium | High | Extensive testing, gradual rollout |
| Community resistance | Medium | Medium | Clear benefits, gradual migration |
| Performance issues | Low | Medium | Benchmarking, optimization phase |
| IDE adoption slow | Medium | Low | Multiple editor support |
| Breaking changes | Low | Critical | Compatibility testing, deprecation period |
| Resource constraints | Medium | Medium | Phased approach, priority features |

### 9.2 Contingency Plans

**If DSL compiler has critical bugs:**
- Extend JSON Schema editing period
- Fix bugs before proceeding
- Maintain parallel systems

**If community resists migration:**
- Gather feedback
- Improve tooling
- Extend deprecation timeline
- Consider hybrid approach

**If performance is unacceptable:**
- Optimize compiler
- Add caching
- Consider incremental compilation

---

## 10. Timeline Summary

| Phase | Duration | Key Deliverables | Milestone |
|-------|----------|------------------|-----------|
| 1. Foundation | Weeks 1-4 | Enhanced compiler, parser, tests | Compiler v2 |
| 2. Tooling | Weeks 5-10 | CLI, linter, formatter, IDE | Complete toolchain |
| 3. Migration | Weeks 11-16 | Schema migration, docs, CI | All migrated |
| 4. Enhancement | Weeks 17-20 | Advanced features, generators | Feature complete |
| 5. Deprecation | Weeks 21-24 | Deprecation, adoption, monitoring | DSL primary |

**Total Duration:** 24 weeks (6 months)

---

## 11. Resource Requirements

### 11.1 Team Requirements

| Role | Effort | Responsibilities |
|------|--------|------------------|
| DSL Language Designer | 20% | Grammar design, language features |
| Compiler Engineer | 60% | Parser, compiler, type system |
| Tooling Engineer | 40% | CLI, linter, formatter |
| IDE Developer | 30% | VS Code extension, LSP |
| Technical Writer | 30% | Documentation, tutorials |
| QA Engineer | 20% | Testing, validation |
| DevOps Engineer | 10% | CI/CD, automation |

### 11.2 Infrastructure Requirements

- CI/CD pipeline (GitHub Actions)
- Package registry (PyPI, npm)
- VS Code marketplace account
- Documentation hosting
- Analytics platform

---

## 12. Appendix

### 12.1 Glossary

- **DSL**: Domain-Specific Language - ADL's custom schema definition language
- **AST**: Abstract Syntax Tree - Structured representation of parsed DSL
- **LSP**: Language Server Protocol - Standard for IDE features
- **JSON Schema**: JSON-based schema format (current primary format)
- **ADL**: Agent Definition Language - The overall specification

### 12.2 References

- Current DSL Design: `docs/adl-dsl-design.md`
- DSL Compiler: `tools/adl_dsl_compiler.py`
- DSL Validator: `tools/adl_dsl_validator.py`
- DSL Schema: `schema/agent-definition.adl`
- JSON Schema: `schema/agent-definition.schema.json`

### 12.3 Related Documents

- `ROADMAP.md` - Project roadmap
- `CONTRIBUTING.md` - Contribution guidelines
- `GOVERNANCE.md` - Project governance

---

## 13. Approval

This plan requires approval from:

- [ ] Project Lead
- [ ] Technical Lead
- [ ] Community Review

**Approved by:** _________________ **Date:** _________________

---

*Document Version: 1.0*  
*Last Updated: 2026-02-15*  
*Status: Draft*
