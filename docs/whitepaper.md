# Agent Definition Language (ADL)
### A Vendor-Neutral Open Standard for Enterprise AI Agents

---

## **Abstract**

This whitepaper introduces **ADL (Agent Definition Language)**, a declarative, vendor-neutral schema designed to define AI agents, their tools, retrieval indices, LLM configurations, dependencies, and security boundaries. ADL allows enterprises to standardize how agents are represented, governed, audited, and exchanged across platforms.

ADL aims to become the **OpenAPI for AI agents**, enabling interoperability, portability, and governance in enterprise agent systems.

---

## **1. Introduction**

The rise of AI agents across industries has created a fragmented ecosystem with incompatible formats and proprietary tool contracts.  
Enterprises require:

- consistent definitions  
- auditable models  
- permission boundaries  
- portable agent configurations  
- vendor neutrality  

ADL provides the first open, formal schema addressing these requirements.

---

## **2. Motivation**

Existing agent frameworks lack:

- standardized tool definitions  
- consistent LLM configuration formats  
- RAG index definitions  
- permission and sandbox metadata  
- dependency models  
- governance and lifecycle transparency  

ADL solves these systemic gaps by aligning with the ecosystem’s best practices in declarative configuration standards such as Kubernetes YAML, OpenAPI, and Terraform HCL.

---

## **3. Design Goals**

ADL is guided by the following design principles:

- **Vendor-neutral**: No platform lock-in  
- **LLM-agnostic**: Works with all models  
- **Declarative**: Pure JSON schema  
- **Portable**: Valid across runtimes  
- **Governable**: Suitable for enterprise audit  
- **Safe**: Clear permissions & boundaries  
- **Composable**: Tools and RAG indices as modular units  

---

## **4. ADL Schema Overview**

The ADL schema includes:

### 4.1 Agent Metadata
- name
- description
- version (integer and semantic version string)
- lifecycle status
- role
- ownership
- compatibility information
- change log

### 4.2 LLM Configuration
- model provider
- temperature
- max tokens
- parameters
- generation policies

### 4.3 Tools
Each tool includes:
- name, description
- parameters (typed)
- return schemas
- dependencies
- invocation types
- permissions

### 4.4 Retrieval (RAG) Indices
- index type (doc/code/image)
- metadata
- virtual paths
- location type

### 4.5 Memory Configuration
- memory type (episodic, semantic, working, hybrid)
- scope (session, user, org, global)
- backend (vector, kv, graph, external)
- retention policies
- read/write policies
- privacy settings (PII, encryption)

### 4.6 Sandbox Permissions
- network
- file_read/file_write
- env variables

### 4.7 Dependencies & Metadata
- Pip packages
- Version pinning
- Code file mapping  

---

## **5. Governance Model**

ADL follows a governance structure similar to CNCF and IETF standards:

- Steering Committee  
- Working Groups  
- RFC process  
- Semver versioning  
- Compatibility guarantees  
- Security and ethical guidelines  

---

## **6. ADL v2 and Beyond**

Future versions introduce:

- Multi-agent definitions  
- Workflow & DAG modeling  
- Memory schemas  
- Advanced RAG semantics  
- Pluggable tooling  
- Secure packaging (ADLX)  
- Policy-as-code integration  

---

## **7. Reference Implementation**

Next Moca provides:

- JSON schema  
- Validators  
- Sample agents  
- CI/CD templates  
- Code generators  

These serve as the canonical reference implementation of ADL.

---

## **8. Conclusion**

ADL provides the foundational structure for the future of enterprise AI agents. By making the standard open and vendor-neutral, we encourage interoperability, governance, and long-term stability in agentic systems.

ADL is the next major building block in the enterprise AI stack — a shared language for defining intelligent systems.

---

## **Appendix**

- Full JSON schema available at GitHub  
- Example agents (creative, RAG, code assistants, workflow agents)  
- Contribution guidelines and RFC templates  
