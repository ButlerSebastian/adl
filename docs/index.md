# Agent Definition Language (ADL)
### The Open Standard for Defining Enterprise-Grade AI Agents

---

## 🚀 What is ADL?

**ADL (Agent Definition Language)** is a vendor-neutral, declarative JSON schema for defining AI agents, their tools, retrieval indices (RAG), capabilities, dependencies, and execution boundaries.  
It is designed to bring interoperability, governance, and structure to enterprise AI systems.

ADL provides a formal, machine-validated structure for:

- Agent identity & metadata  
- Tools & function parameters  
- LLM configuration  
- RAG indices  
- Sandbox permissions  
- Runtime dependencies  
- Versioning & audit logs  

---

## 🧩 Why ADL?

As enterprises deploy agentic systems across their organizations, they face:

- Fragmented tool definitions  
- Proprietary agent formats  
- Limited portability  
- Governance & compliance friction  
- Inconsistent RAG structures  
- Vendor lock-in concerns  

ADL solves these challenges by providing a **single, open, declarative standard**.

---

## 🏛 ADL is to Agents what OpenAPI is to REST

With ADL:

- Agents become portable across platforms  
- Definitions can be version-controlled  
- Schemas can be validated in CI/CD  
- Tooling ecosystems can emerge  
- Enterprises can adopt agents without vendor lock-in  

---

## 🔧 Example: Simple ADL Agent

```json
{
  "name": "campaign_image_generator",
  "description": "Generate a 1024x1024 marketing image via prompt.",
  "role": "Creative Producer",
  "llm": "openai",
  "llm_settings": { "temperature": 0, "max_tokens": 4096 },
  "tools": [
    {
      "name": "generate_campaign_image",
      "description": "Generate a Gemini 2.5 Flash image",
      "parameters": [
        { "name": "prompt", "type": "string", "required": true }
      ],
      "invocation": { "type": "python_function" }
    }
  ],
  "rag": [
    {
      "id": "marketing-index",
      "name": "Campaign Image Input",
      "rag_type": "doc",
      "virtual_index_path": "/rags/marketing-index"
    }
  ]
}
```

## 📦 Getting Started
``` bash
pip install jsonschema
jsonschema -i example.json schema/agent-definition.schema.json
```

## 🌐 Join the ADL Community
- GitHub Issues — Request features
- Discussions — Propose extensions
- Contributors — Submit tools, validators, bindings
- Standards Group — Help shape ADL v2

## 🤝 Brought to you by Next Moca
## Building the enterprise system-of-record for AI Agents and Workflows.