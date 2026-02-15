# ADL Phase 3 (v2) Implementation Plan

## TL;DR

> **Quick Summary**: Implement ADL v2 by documenting schema modularization, applying strict naming conventions, unified typing rules, then adding multi-agent coordination, execution constraints, event-driven tools, advanced RAG, memory extensions, and LLM settings extensions.
>
> **Deliverables**:
> - Documented schema architecture (components/ directory)
> - Multi-agent role definitions (4 role types max)
> - Execution constraints system
> - Event-driven tool invocation (local sync only)
> - Advanced RAG (vector + keyword search)
> - Memory extensions (episodic + semantic)
> - LLM settings extensions (multi-model support, routing, constraints)
> - Strict field naming conventions
> - Unified typing rules
>
> **Estimated Effort**: Large (9-11 months with parallelization)
> **Parallel Execution**: YES - 3 waves
> **Critical Path**: Schema Documentation → Multi-Agent Roles → Execution Constraints → Event-Driven Tools

---

## Context

### Original Request
"base on the roadmap.md phase 3 choose which has higher priority follow to the least priority, focus on the current implementation and break down into atomic task using 5w2h use category 'deep' or 'ultrabrain' for decoupling task into atomic task. after decoupling into atomic task, create the plan base on that."

### Current State
- **ADL v1.5**: Complete (37/37 tasks), monolithic schema (665 lines), all examples validate
- **Phase 3 Goal**: Prioritize features and break into atomic tasks using 5W2H methodology
- **Methodology**: Use "deep" or "ultrabrain" categories for task decomposition

### Key Finding: JSON Schema Vocabulary Limitations
During implementation, we discovered that JSON Schema 2020-12's vocabulary system prevents easy modularization with external `$ref`. This is a fundamental limitation of the JSON Schema specification, not an implementation issue.

**Recommendation**: Consider a Domain-Specific Language (DSL) approach for future ADL versions to avoid JSON Schema constraints.

---

## Work Objectives

### Core Objective
Transform ADL from a monolithic v1.5 schema to a documented v2 architecture with multi-agent coordination, execution constraints, event-driven tools, advanced RAG, and memory extensions while maintaining backward compatibility.

### Concrete Deliverables
- `schema/components/` directory with documented component files
- `schema/agent-definition.schema.json` (v2) with multi-agent, events, constraints
- Updated examples demonstrating new features
- TypeScript type definitions for schema
- Comprehensive documentation

### Definition of Done
- [x] Schema components documented
- [x] Strict field naming conventions applied
- [x] Unified typing rules implemented
- [ ] Multi-agent role definitions (4 types: Coordinator, Worker, Supervisor, Critic)
- [ ] Execution constraints system
- [ ] Event-driven tool invocation (local sync)
- [ ] LLM settings extensions (multi-model support, routing, constraints)
- [ ] Advanced RAG (vector + keyword)
- [ ] Memory extensions (episodic + semantic)
- [ ] All existing v1.5 examples validate unchanged
- [ ] New examples demonstrate all v2 features

---

## Execution Strategy

### Parallel Execution Waves

```
Wave 1 (COMPLETED - Foundation):
├── Task 1: Schema Modularization (Documented) ✓
├── Task 2: Strict Field Naming (Completed) ✓
└── Task 3: Unified Typing Rules (Completed) ✓

Wave 2 (IN PROGRESS - Core Features):
├── Task 4: Multi-Agent Roles
└── Task 5: Execution Constraints

Wave 3 (PENDING - Advanced Features):
├── Task 6: Event-Driven Tools
├── Task 7: Advanced RAG [PARALLEL]
├── Task 8: Memory Extensions [PARALLEL]
└── Task 9: LLM Settings Extensions [PARALLEL]

Critical Path: Task 4 → Task 5 → Task 6
Parallel Speedup: ~40% faster than sequential
```

---

## TODOs

### Wave 1: Foundation (COMPLETED)

- [x] 1. Schema Modularization (Documented)
  - Created component directory structure
  - Extracted 5 component files as documentation
  - All examples validate with original schema
  - Documented JSON Schema vocabulary limitations

- [x] 2. Strict Field Naming Conventions
  - Created `docs/naming-conventions.md`
  - Created `scripts/check-naming-conventions.sh`
  - All fields follow snake_case convention
  - All examples validate successfully

- [x] 3. Unified Typing Rules
  - Created `types/agent-definition.d.ts`
  - Created `docs/typing-rules.md`
  - Verified no "any" types in schema
  - All examples validate successfully

### Wave 2: Core Features (IN PROGRESS)

- [ ] 4. Multi-Agent Role Definitions
  - Define multi-agent role system with 4 role types: Coordinator, Worker, Supervisor, Critic
  - Add `agent_roles` field to schema
  - Define role capabilities, constraints, and communication protocols
  - Create examples demonstrating multi-agent coordination
  - Implement role validation and enforcement

- [ ] 5. Execution Constraints & Capability Negotiation
  - Define execution constraints system (time limits, memory limits, resource quotas)
  - Add `execution_constraints` field to schema
  - Define capability negotiation protocols
  - Implement constraint validation and enforcement
  - Create examples demonstrating constraints

### Wave 3: Advanced Features (PENDING)

- [ ] 6. Event-Driven Tool Invocation
  - Define event system for tool invocation
  - Add `events` field to schema
  - Define trigger configurations
  - Define subscription models
  - Implement event routing and handling
  - Create examples demonstrating event-driven tools

- [ ] 7. Advanced RAG Schema
  - Extend RAG schema with advanced features
  - Add hierarchical RAG support
  - Add cross-file reference mechanisms
  - Implement vector search + keyword search (hybrid)
  - Create examples demonstrating advanced RAG

- [ ] 8. Memory Extensions
  - Extend memory schema with episodic and semantic memory
  - Define memory lifecycle management
  - Define memory eviction policies
  - Implement memory storage and retrieval
  - Create examples demonstrating memory extensions

- [ ] 9. LLM Settings Extensions
  - Extend LLM settings schema with multi-model support
  - Define primary, fallback, and specialized models
  - Add model routing configuration (task-based routing)
  - Add LLM-specific execution constraints (token limits, cost limits)
  - Create examples demonstrating LLM extensions

---

## Success Criteria

### Verification Commands
```bash
# Validate all examples against schema
python3 tools/validate.py examples/*.json

# Check naming conventions
./scripts/check-naming-conventions.sh schema/

# Check for any types
grep -r '"type": "any"' schema/

# Validate TypeScript definitions (if tsc available)
# tsc --noEmit types/agent-definition.d.ts
```

### Final Checklist
- [x] Schema components documented
- [x] All fields follow strict naming conventions
- [x] All types are consistent with no any types
- [ ] Multi-agent roles defined (4 types max)
- [ ] Execution constraints implemented
- [ ] Event-driven tools implemented (local sync only)
- [ ] Advanced RAG implemented (vector + keyword)
- [ ] Memory extensions implemented (episodic + semantic)
- [ ] LLM settings extensions implemented (multi-model, routing, constraints)
- [ ] All existing v1.5 examples validate unchanged
- [ ] All new v2 examples validate successfully
- [ ] Documentation updated
