# ADL Tool Category Taxonomy Specification

## Overview

The ADL Tool Category Taxonomy provides a standardized, hierarchical system for organizing and discovering AI agent tools. This taxonomy enables:

- **Tool Discovery**: Find tools by category and subcategory
- **Organization**: Group related tools logically
- **Governance**: Apply policies based on tool categories
- **Documentation**: Provide clear tool classification
- **Interoperability**: Standard categorization across platforms

## Design Philosophy

The taxonomy follows **Kubernetes-style hierarchical labels** with the pattern:

```
domain.category.subcategory.specific
```

**Example**: `data_access.database.query`

This approach provides:
- **Hierarchical Structure**: 3-4 levels of categorization
- **Discoverability**: Easy to browse and search
- **Extensibility**: New categories can be added without breaking existing ones
- **Backward Compatibility**: Existing tools remain valid
- **Semantic Clarity**: Category names convey purpose

---

## Category Hierarchy

### Level 1: Domain (Broad Functional Area)

The top-level domain represents the broad functional area of a tool.

| Domain ID | Name | Description |
|-----------|------|-------------|
| `data_access` | Data Access | Tools for reading, writing, and querying data |
| `data_manipulation` | Data Manipulation | Tools for transforming and processing data |
| `computation` | Computation | Tools for calculations and computations |
| `communication` | Communication | Tools for messaging and notifications |
| `file_operations` | File Operations | Tools for file system operations |
| `system` | System | Tools for system-level operations |
| `ai_ml` | AI/ML | Tools for AI and machine learning operations |
| `security` | Security | Tools for security and authentication |
| `monitoring` | Monitoring | Tools for monitoring and logging |
| `testing` | Testing | Tools for testing and validation |
| `integration` | Integration | Tools for third-party service integration |
| `ui_ux` | UI/UX | Tools for user interface and experience |
| `workflow` | Workflow | Tools for workflow and orchestration |
| `content` | Content | Tools for content generation and management |

### Level 2: Category (Specific Function)

Each domain contains multiple categories representing specific functions.

#### data_access
| Category ID | Name | Description |
|-------------|------|-------------|
| `database` | Database | Database operations |
| `api` | API | API calls and web services |
| `storage` | Storage | Cloud storage operations |
| `cache` | Cache | Cache operations |
| `search` | Search | Search and indexing |
| `stream` | Stream | Data streaming |

#### data_manipulation
| Category ID | Name | Description |
|-------------|------|-------------|
| `transformation` | Transformation | Data transformation |
| `aggregation` | Aggregation | Data aggregation |
| `validation` | Validation | Data validation |
| `formatting` | Formatting | Data formatting |
| `parsing` | Parsing | Data parsing |
| `filtering` | Filtering | Data filtering |

#### computation
| Category ID | Name | Description |
|-------------|------|-------------|
| `math` | Math | Mathematical operations |
| `statistics` | Statistics | Statistical calculations |
| `logic` | Logic | Logical operations |
| `optimization` | Optimization | Optimization algorithms |
| `simulation` | Simulation | Simulations and modeling |

#### communication
| Category ID | Name | Description |
|-------------|------|-------------|
| `email` | Email | Email operations |
| `sms` | SMS | SMS messaging |
| `chat` | Chat | Chat and messaging |
| `notification` | Notification | Push notifications |
| `webhook` | Webhook | Webhook operations |
| `voice` | Voice | Voice and telephony |

#### file_operations
| Category ID | Name | Description |
|-------------|------|-------------|
| `read` | Read | File reading |
| `write` | Write | File writing |
| `delete` | Delete | File deletion |
| `copy` | Copy | File copying |
| `move` | Move | File moving |
| `archive` | Archive | File archiving |
| `convert` | Convert | File conversion |

#### system
| Category ID | Name | Description |
|-------------|------|-------------|
| `process` | Process | Process management |
| `network` | Network | Network operations |
| `environment` | Environment | Environment variables |
| `logging` | Logging | Logging operations |
| `scheduling` | Scheduling | Task scheduling |
| `configuration` | Configuration | Configuration management |

#### ai_ml
| Category ID | Name | Description |
|-------------|------|-------------|
| `llm` | LLM | Large Language Model operations |
| `image_generation` | Image Generation | AI image generation |
| `text_analysis` | Text Analysis | NLP and text analysis |
| `classification` | Classification | ML classification |
| `recommendation` | Recommendation | Recommendation systems |
| `embedding` | Embedding | Vector embeddings |

#### security
| Category ID | Name | Description |
|-------------|------|-------------|
| `authentication` | Authentication | Authentication operations |
| `authorization` | Authorization | Authorization checks |
| `encryption` | Encryption | Encryption and decryption |
| `audit` | Audit | Security auditing |
| `compliance` | Compliance | Compliance checks |

#### monitoring
| Category ID | Name | Description |
|-------------|------|-------------|
| `metrics` | Metrics | Metrics collection |
| `logging` | Logging | Log aggregation |
| `tracing` | Tracing | Distributed tracing |
| `alerting` | Alerting | Alert management |
| `dashboard` | Dashboard | Dashboard operations |

#### testing
| Category ID | Name | Description |
|-------------|------|-------------|
| `unit` | Unit | Unit testing |
| `integration` | Integration | Integration testing |
| `e2e` | E2E | End-to-end testing |
| `performance` | Performance | Performance testing |
| `validation` | Validation | Data validation |

#### integration
| Category ID | Name | Description |
|-------------|------|-------------|
| `crm` | CRM | CRM integration |
| `erp` | ERP | ERP integration |
| `payment` | Payment | Payment processing |
| `social` | Social | Social media integration |
| `analytics` | Analytics | Analytics platforms |

#### ui_ux
| Category ID | Name | Description |
|-------------|------|-------------|
| `rendering` | Rendering | UI rendering |
| `interaction` | Interaction | User interaction |
| `accessibility` | Accessibility | Accessibility features |
| `localization` | Localization | Localization and i18n |

#### workflow
| Category ID | Name | Description |
|-------------|------|-------------|
| `orchestration` | Orchestration | Workflow orchestration |
| `automation` | Automation | Task automation |
| `scheduling` | Scheduling | Workflow scheduling |
| `approval` | Approval | Approval workflows |

#### content
| Category ID | Name | Description |
|-------------|------|-------------|
| `generation` | Generation | Content generation |
| `editing` | Editing | Content editing |
| `translation` | Translation | Content translation |
| `summarization` | Summarization | Content summarization |

### Level 3: Subcategory (Specific Operation)

Each category contains subcategories for specific operations.

#### Example: data_access.database
| Subcategory ID | Name | Description |
|----------------|------|-------------|
| `query` | Query | Database queries |
| `insert` | Insert | Data insertion |
| `update` | Update | Data updates |
| `delete` | Delete | Data deletion |
| `schema` | Schema | Schema operations |
| `migration` | Migration | Database migrations |

#### Example: ai_ml.image_generation
| Subcategory ID | Name | Description |
|----------------|------|-------------|
| `text_to_image` | Text to Image | Generate images from text |
| `image_to_image` | Image to Image | Transform images |
| `inpainting` | Inpainting | Image inpainting |
| `upscaling` | Upscaling | Image upscaling |
| `style_transfer` | Style Transfer | Artistic style transfer |

### Level 4: Specific (Particular Implementation)

The most specific level identifies particular implementations or variants.

#### Example: data_access.database.query.sql
- **Full ID**: `data_access.database.query.sql`
- **Name**: SQL Query
- **Description**: Execute SQL database queries

#### Example: ai_ml.image_generation.text_to_image.dalle
- **Full ID**: `ai_ml.image_generation.text_to_image.dalle`
- **Name**: DALL-E Image Generation
- **Description**: Generate images using DALL-E model

---

## Category Metadata Schema

Each category can have associated metadata:

```json
{
  "id": "data_access.database.query",
  "name": "Database Query",
  "description": "Execute database queries",
  "parent": "data_access.database",
  "level": 3,
  "icon": "database",
  "color": "#3B82F6",
  "tags": ["sql", "database", "query"],
  "examples": [
    "SELECT * FROM users WHERE id = ?",
    "INSERT INTO orders (product_id, quantity) VALUES (?, ?)"
  ],
  "permissions": {
    "network": true,
    "file_read": false,
    "file_write": false
  },
  "security_level": "medium"
}
```

### Metadata Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `id` | string | Yes | Unique category identifier |
| `name` | string | Yes | Human-readable name |
| `description` | string | Yes | Detailed description |
| `parent` | string | Yes | Parent category ID |
| `level` | integer | Yes | Hierarchy level (1-4) |
| `icon` | string | No | Icon identifier for UI |
| `color` | string | No | Color code for UI (hex) |
| `tags` | array | No | Related tags |
| `examples` | array | No | Example use cases |
| `permissions` | object | No | Default permissions |
| `security_level` | string | No | Security classification |

---

## JSON Schema Enum Definitions

### Level 1: Domain Enum

```json
{
  "type": "string",
  "enum": [
    "data_access",
    "data_manipulation",
    "computation",
    "communication",
    "file_operations",
    "system",
    "ai_ml",
    "security",
    "monitoring",
    "testing",
    "integration",
    "ui_ux",
    "workflow",
    "content"
  ]
}
```

### Level 2: Category Enum (by Domain)

```json
{
  "type": "object",
  "properties": {
    "data_access": {
      "type": "string",
      "enum": ["database", "api", "storage", "cache", "search", "stream"]
    },
    "data_manipulation": {
      "type": "string",
      "enum": ["transformation", "aggregation", "validation", "formatting", "parsing", "filtering"]
    },
    "computation": {
      "type": "string",
      "enum": ["math", "statistics", "logic", "optimization", "simulation"]
    },
    "communication": {
      "type": "string",
      "enum": ["email", "sms", "chat", "notification", "webhook", "voice"]
    },
    "file_operations": {
      "type": "string",
      "enum": ["read", "write", "delete", "copy", "move", "archive", "convert"]
    },
    "system": {
      "type": "string",
      "enum": ["process", "network", "environment", "logging", "scheduling", "configuration"]
    },
    "ai_ml": {
      "type": "string",
      "enum": ["llm", "image_generation", "text_analysis", "classification", "recommendation", "embedding"]
    },
    "security": {
      "type": "string",
      "enum": ["authentication", "authorization", "encryption", "audit", "compliance"]
    },
    "monitoring": {
      "type": "string",
      "enum": ["metrics", "logging", "tracing", "alerting", "dashboard"]
    },
    "testing": {
      "type": "string",
      "enum": ["unit", "integration", "e2e", "performance", "validation"]
    },
    "integration": {
      "type": "string",
      "enum": ["crm", "erp", "payment", "social", "analytics"]
    },
    "ui_ux": {
      "type": "string",
      "enum": ["rendering", "interaction", "accessibility", "localization"]
    },
    "workflow": {
      "type": "string",
      "enum": ["orchestration", "automation", "scheduling", "approval"]
    },
    "content": {
      "type": "string",
      "enum": ["generation", "editing", "translation", "summarization"]
    }
  }
}
```

### Full Category ID Pattern

```json
{
  "type": "string",
  "pattern": "^[a-z_]+(?:\\.[a-z_]+){1,3}$",
  "description": "Hierarchical category ID (e.g., 'data_access.database.query')"
}
```

---

## Usage Examples

### Example 1: Database Query Tool

```json
{
  "name": "query_database",
  "description": "Execute SQL queries on PostgreSQL database",
  "category": "data_access.database.query",
  "subcategory": "sql",
  "parameters": [
    {
      "name": "query",
      "type": "string",
      "description": "SQL query to execute",
      "required": true
    },
    {
      "name": "database",
      "type": "string",
      "description": "Database name",
      "required": true
    }
  ]
}
```

### Example 2: Image Generation Tool

```json
{
  "name": "generate_image",
  "description": "Generate images from text prompts using DALL-E",
  "category": "ai_ml.image_generation.text_to_image",
  "subcategory": "dalle",
  "parameters": [
    {
      "name": "prompt",
      "type": "string",
      "description": "Text prompt for image generation",
      "required": true
    },
    {
      "name": "size",
      "type": "string",
      "enum": ["256x256", "512x512", "1024x1024"],
      "description": "Image size",
      "required": false,
      "default": "512x512"
    }
  ]
}
```

### Example 3: Email Notification Tool

```json
{
  "name": "send_email",
  "description": "Send email notifications",
  "category": "communication.email",
  "parameters": [
    {
      "name": "to",
      "type": "string",
      "format": "email",
      "description": "Recipient email address",
      "required": true
    },
    {
      "name": "subject",
      "type": "string",
      "description": "Email subject",
      "required": true
    },
    {
      "name": "body",
      "type": "string",
      "description": "Email body",
      "required": true
    }
  ]
}
```

---

## Migration Guide

### From Free-Form Categories (v1.0)

**Before (v1.0):**
```json
{
  "name": "generate_image",
  "category": "Image Generation"
}
```

**After (v1.5):**
```json
{
  "name": "generate_image",
  "category": "ai_ml.image_generation.text_to_image",
  "subcategory": "dalle"
}
```

### Migration Steps

1. **Audit Existing Tools**
   - List all tools with categories
   - Map free-form categories to taxonomy

2. **Map to Taxonomy**
   - Use closest matching category
   - Add subcategory for specificity
   - Document any custom categories

3. **Update Tool Definitions**
   - Replace free-form category with taxonomy ID
   - Add subcategory if needed
   - Test validation

4. **Handle Custom Categories**
   - For unmapped categories, use `custom` domain
   - Example: `custom.my_category`
   - Submit RFC for new category addition

### Migration Checklist

- [ ] Audit all existing tool categories
- [ ] Map free-form categories to taxonomy
- [ ] Update tool definitions with new category IDs
- [ ] Add subcategories where appropriate
- [ ] Test validation with updated schema
- [ ] Document any custom categories
- [ ] Submit RFCs for new category additions

---

## Best Practices

### 1. Use Appropriate Granularity

- ✅ Use `data_access.database.query` for database queries
- ✅ Use `ai_ml.image_generation.text_to_image` for image generation
- ❌ Avoid overly specific categories like `data_access.database.query.select_users_by_id`

### 2. Follow Naming Conventions

- Use lowercase with underscores
- Use descriptive, clear names
- Avoid abbreviations
- Use singular nouns

### 3. Document Custom Categories

If you need a category not in the taxonomy:
1. Use `custom` domain temporarily
2. Document the use case
3. Submit RFC for official category addition

### 4. Use Subcategories for Specificity

When multiple tools share a category but differ in implementation:
- Use `subcategory` field for specific implementation
- Example: `ai_ml.image_generation.text_to_image` with `subcategory: "dalle"`

### 5. Consider Security Implications

Some categories have default security requirements:
- `security.*`: High security level
- `system.*`: Medium security level
- `data_access.*`: Medium security level

---

## Category Registry

The complete category registry is maintained in the ADL repository at:
- `/docs/tool-category-registry.json` (machine-readable)
- `/docs/tool-category-taxonomy.md` (this document)

### Adding New Categories

To add a new category:

1. **Submit RFC**: Create GitHub issue with `[RFC]` prefix
2. **Define Category**: Provide ID, name, description, parent
3. **Justify Need**: Explain why existing categories don't suffice
4. **Get Approval**: Wait for steering committee approval
5. **Update Registry**: Add to category registry
6. **Update Schema**: Update JSON Schema enums

### Category Deprecation

Categories can be deprecated but not removed:
1. Mark as deprecated in registry
2. Provide migration path
3. Maintain for backward compatibility
4. Remove after 2 major versions

---

## Validation Rules

### Category ID Validation

```json
{
  "type": "string",
  "pattern": "^[a-z_]+(?:\\.[a-z_]+){1,3}$",
  "description": "Valid category ID"
}
```

### Subcategory Validation

```json
{
  "type": "string",
  "pattern": "^[a-z0-9_-]+$",
  "description": "Valid subcategory identifier"
}
```

### Combined Validation

A tool must have either:
- A valid `category` ID (required)
- An optional `subcategory` (if needed for specificity)

---

## Appendix A: Complete Category Tree

```
data_access
├── database
│   ├── query
│   ├── insert
│   ├── update
│   ├── delete
│   ├── schema
│   └── migration
├── api
│   ├── rest
│   ├── graphql
│   ├── soap
│   └── websocket
├── storage
│   ├── s3
│   ├── azure_blob
│   ├── gcs
│   └── local
├── cache
│   ├── redis
│   ├── memcached
│   └── in_memory
├── search
│   ├── elasticsearch
│   ├── solr
│   └── vector
└── stream
    ├── kafka
    ├── rabbitmq
    └── sqs

data_manipulation
├── transformation
├── aggregation
├── validation
├── formatting
├── parsing
└── filtering

computation
├── math
├── statistics
├── logic
├── optimization
└── simulation

communication
├── email
├── sms
├── chat
├── notification
├── webhook
└── voice

file_operations
├── read
├── write
├── delete
├── copy
├── move
├── archive
└── convert

system
├── process
├── network
├── environment
├── logging
├── scheduling
└── configuration

ai_ml
├── llm
│   ├── text_generation
│   ├── code_generation
│   └── summarization
├── image_generation
│   ├── text_to_image
│   ├── image_to_image
│   ├── inpainting
│   ├── upscaling
│   └── style_transfer
├── text_analysis
│   ├── sentiment
│   ├── entity_extraction
│   └── classification
├── classification
├── recommendation
└── embedding

security
├── authentication
├── authorization
├── encryption
├── audit
└── compliance

monitoring
├── metrics
├── logging
├── tracing
├── alerting
└── dashboard

testing
├── unit
├── integration
├── e2e
├── performance
└── validation

integration
├── crm
├── erp
├── payment
├── social
└── analytics

ui_ux
├── rendering
├── interaction
├── accessibility
└── localization

workflow
├── orchestration
├── automation
├── scheduling
└── approval

content
├── generation
├── editing
├── translation
└── summarization
```

---

## Appendix B: Category Quick Reference

| Use Case | Category ID |
|----------|-------------|
| SQL Database Query | `data_access.database.query` |
| REST API Call | `data_access.api.rest` |
| Generate Image | `ai_ml.image_generation.text_to_image` |
| Send Email | `communication.email` |
| Read File | `file_operations.read` |
| Execute LLM | `ai_ml.llm.text_generation` |
| Validate Data | `data_manipulation.validation` |
| Calculate Statistics | `computation.statistics` |
| Monitor Metrics | `monitoring.metrics` |
| Authenticate User | `security.authentication` |

---

## Version History

- **v1.5.0** (Current): Hierarchical taxonomy with 14 domains, 50+ categories
- **v1.0.0**: Free-form string category field

---

*This specification is part of the ADL (Agent Definition Language) project. For more information, visit https://github.com/nextmoca/adl*
