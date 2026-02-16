<p align="center">
  <img src="https://img.shields.io/badge/License-Apache_2.0-blue.svg" alt="License"/>
  <a href="https://github.com/nextmoca/adl">
    <img src="https://img.shields.io/badge/ADL-GitHub-black?logo=github" alt="GitHub Repo"/>
  </a>
  <img src="https://img.shields.io/badge/Schema-Validated-brightgreen" alt="Schema Status"/>
</p>

<h1 align="center">ADL — Agent Definition Language</h1>
<p align="center"><strong>A vendor-neutral, open standard for defining AI agents.</strong></p>

---

## 🚀 Overview

For questions or contributions, visit: https://github.com/nextmoca/adl/issues

## Getting Started
**ADL (Agent Definition Language)** is an open, declarative, vendor-neutral specification for defining AI agents in a consistent, auditable, and interoperable way.  
It provides a shared language for describing:

- an agent’s identity and purpose  
- its tools and capabilities  
- its LLM configuration  
- its access to knowledge (RAG)  
- its permissions and sandbox  
- its dependencies  
- its governance metadata  

If **OpenAPI defines APIs**, **ADL defines agents**.

---

## 🧠 Why ADL Exists

Enterprises adopting AI agents face several systemic challenges:

- Each vendor defines “agents” differently  
- Tool contracts are inconsistent  
- RAG pipelines are wired differently across apps  
- Permissions are rarely explicit  
- Governance teams have no centralized visibility  
- Agents are not portable across platforms  
- Vendor lock-in slows enterprise adoption  
- Compliance and auditability are fragile or impossible  

**ADL solves these problems** by introducing a single, declarative, versioned artifact that describes what an agent *is* and what it is *allowed* to do.

---

## 🧩 What ADL *Is*

ADL defines:

- **Identity** — name, description, role, owner, version
- **LLM Settings** — provider, model, temperature, max tokens
- **Tools & Actions** — typed parameters, descriptions, return schemas
- **Tool Categories** — hierarchical taxonomy with pattern validation
- **Parameter Constraints** — enhanced type system with validation
- **Return Types** — standardized return schemas with 15 patterns
- **RAG Inputs** — indices, types, metadata, paths
- **Memory** — type, scope, backend, retention, policies, privacy settings
- **Permissions** — file I/O, network, env vars
- **Dependencies** — Python packages with optional version pins
- **Governance** — lifecycle, compatibility, change logs, version notes  

This makes agents:

- portable  
- predictable  
- auditable  
- reproducible  
- interoperable across vendors  

---

## 🚫 What ADL *Is Not*

To avoid confusion, ADL explicitly does **not** define:

- ❌ A2A (agent-to-agent) communication protocols  
- ❌ runtime tool invocation semantics (e.g., MCP)  
- ❌ prompt templating or formatting  
- ❌ workflow orchestration (Airflow, Temporal, Dagster)  
- ❌ API schemas (OpenAPI already solves that)  
- ❌ message transport (HTTP, gRPC, JSON-RPC)  

**ADL is laser-focused on definition — not execution.**

---

## 🔍 ADL vs AI App Definition  
**ADL is an Agent Definition Language - not a general AI App definition format.**

AI apps are broad and may include UI, API layers, deployments, data stores, or business logic.

Agents are specific:

- they reason  
- they call tools  
- they retrieve knowledge  
- they act autonomously  
- they require permission boundaries  

ADL models **agent competencies**, not app-level infrastructure.

This is a key strategic distinction.

---

## 🔄 Comparing ADL to Other Standards

### **ADL vs A2A**
- **A2A**: defines how agents communicate  
- **ADL**: defines *what* an agent is  

### **ADL vs MCP**
- **MCP**: runtime tool protocol  
- **ADL**: declarative definition of tools and capabilities  

### **ADL vs OpenAPI**
- **OpenAPI**: describes HTTP services  
- **ADL**: describes agent behavior, boundaries, and capabilities  

### **ADL vs Workflow Engines**
- Workflows = *when & how tasks execute*  
- ADL = *which agent executes them*  

---

## 🌐 Why Next Moca Open Sourced ADL

Next Moca open-sourced ADL under **Apache 2.0** to enable:

### ✔ Ecosystem-wide interoperability  
### ✔ Enterprise trust and transparency  
### ✔ Neutral governance  
### ✔ Community-driven evolution  
### ✔ Vendor adoption without lock-in  
### ✔ Safe, compliant, standards-based agent deployment  

Open sourcing ensures ADL becomes a **true standard**, not a proprietary configuration format.

---

## 📘 Documentation

- 📄 ADL Spec (JSON Schema) — `/schema/adl.schema.json`
- 📚 Examples — `/examples/`
- 🛠 CLI Reference — `/docs/tools/cli.md`
- 🏛 Governance — `/GOVERNANCE.md`
- 🤝 Contributing — `/CONTRIBUTING.md`
- 📖 Tool Category Taxonomy — `/docs/tool-category-taxonomy.md`
- 📖 Enhanced Type System — `/docs/enhanced-type-system.md`
- 📖 Return Type System — `/docs/return-type-system.md`
- 📖 Schema Reference — `/docs/schema-reference.md`
- 📖 Migration Guide v1.5 — `/docs/migration-v1.5.md`

---

## ✨ What's New in v1.5

ADL v1.5 introduces three major enhancements:

- **Tool Category Taxonomy**: A hierarchical taxonomy for tools with pattern validation, ensuring consistency and interoperability across agents.
- **Enhanced Type System**: Advanced parameter constraints with validation, enabling stricter and more expressive type definitions.
- **Return Type System**: Standardized return schemas with 15 predefined patterns, improving predictability and usability.

For detailed migration instructions and examples, refer to the [Migration Guide v1.5](/docs/migration-v1.5.md).

## 🎯 Phase 2: DSL Tooling (Complete)

Phase 2 provides a comprehensive toolchain for working with ADL:

### CLI Tools
- **adl-compile**: Compile ADL files to JSON, YAML, Python, TypeScript
- **adl-validate**: Validate ADL files against schema with strict mode
- **adl-format**: Format ADL files with configurable options
- **adl-lint**: Lint ADL files for code quality with autofix
- **adl-generate**: Generate code from ADL definitions

### IDE Support
- **VS Code Extension**: Full-featured extension with syntax highlighting, diagnostics, auto-completion, go-to-definition, hover, and format-on-save
- **LSP Server**: Language Server Protocol support for multiple editors

### Documentation & Testing
- Comprehensive CLI reference documentation
- Integration tests for all CLI commands
- Package installation via pip

See [CLI Reference](docs/tools/cli.md) for complete documentation.

---

## 🛠 Getting Started

```bash
git clone https://github.com/nextmoca/adl.git
cd adl
pip install -e .
```

### CLI Tools

ADL provides a comprehensive CLI toolchain:

```bash
# Validate ADL file
adl-validate my-agent.adl

# Compile to JSON
adl-compile my-agent.adl -o my-agent.json

# Format ADL file
adl-format my-agent.adl

# Lint ADL file
adl-lint my-agent.adl

# Generate code
adl-generate my-agent.adl -f python -o my_agent.py
```

See [CLI Reference](docs/tools/cli.md) for complete documentation.

### VS Code Extension

Install the ADL VS Code extension for:
- Syntax highlighting
- Error diagnostics
- Auto-completion
- Go to definition
- Hover information
- Format on save

Available in the `editors/vscode/` directory.

### LSP Server

ADL provides a Language Server Protocol server for editor integration:
- Diagnostics
- Completion
- Definition
- Hover
- Formatting

See `tools/dsl/lsp_server.py` for implementation.

---

## Minimal Example

```json
{
  "name": "campaign_image_generator",
  "description": "Generate a 1024x1024 marketing image from a creative brief.",
  "role": "Creative Producer",
  "llm": "openai",
  "llm_settings": {
    "temperature": 0,
    "max_tokens": 4096
  },
  "tools": [
    {
      "name": "generate_campaign_image",
      "description": "Generate a high-quality image from a prompt.",
      "category": "ai_ml.image_generation.text_to_image",
      "subcategory": "dalle",
      "parameters": [
        {
          "name": "prompt",
          "type": "string",
          "description": "Image prompt",
          "minLength": 1,
          "maxLength": 2000,
          "required": true
        }
      ],
      "returns": {
        "type": "MediaResult",
        "schema": { "$ref": "#/$defs/StandardReturnTypes/MediaResult" },
        "description": "Returns generated image with metadata"
      },
      "invocation": { "type": "python_function" }
    }
  ],
  "rag": []
}
```

---

## Contributing

We welcome contributions!  
Please see **CONTRIBUTING.md** for guidelines on RFCs, schema updates, and tooling improvements.

---

## License

Licensed under the **Apache License, Version 2.0**.

---

## About Next Moca

Next Moca is the enterprise platform for multi-agent workflows, agent orchestration, RAG pipelines, governance, and AI system observability. ADL is the foundation for how agents are defined consistently across the ecosystem.
