# ADL Return Type System Specification

**Version:** 1.5.0  
**Status:** Draft  
**Last Updated:** 2026-02-15

---

## 1. Executive Summary

The ADL Return Type System provides a standardized, extensible framework for defining tool output schemas in Agent Definition Language. This specification enables:

- **Tool Output Validation**: Validate that tool outputs conform to defined schemas
- **Documentation**: Self-documenting tool contracts with clear return type definitions
- **Interoperability**: Consistent return type patterns across different agents and tools
- **Type Safety**: Strong typing with support for complex data structures
- **Error Handling**: Standardized error response patterns

### Key Design Principles

1. **OpenAPI Compatibility**: Aligns with OpenAPI 3.0+ response object patterns
2. **JSON Schema Foundation**: Built on JSON Schema Draft 2020-12
3. **Progressive Complexity**: Support simple primitives to complex nested objects
4. **Backward Compatibility**: Maintain compatibility with existing ADL v1.0 definitions
5. **Extensibility**: Allow custom return types while providing standard patterns

---

## 2. Return Type Structure

### 2.1 Core Return Type Object

The `returns` field in a ToolDefinition is replaced with a structured Return Type Object:

```json
{
  "returns": {
    "type": "object",
    "schema": {
      "$ref": "#/$defs/StandardReturnTypes/ObjectResult"
    },
    "description": "Returns the created user object with generated ID",
    "examples": [
      {
        "success": true,
        "data": {
          "id": "usr_12345",
          "name": "John Doe",
          "email": "john@example.com"
        },
        "metadata": {
          "timestamp": "2026-02-15T10:30:00Z",
          "request_id": "req_abc123"
        }
      }
    ],
    "content_type": "application/json"
  }
}
```

### 2.2 Return Type Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `type` | string | Yes | High-level return type category (see Section 3) |
| `schema` | object | Yes | JSON Schema defining the return structure |
| `description` | string | No | Human-readable explanation of the return value |
| `examples` | array | No | Array of example return values |
| `content_type` | string | No | MIME type of the return value (default: application/json) |

---

## 3. Return Type Categories

### 3.1 Category Overview

Return types are organized into six primary categories:

| Category | Description | Use Cases |
|----------|-------------|-----------|
| **Structured** | Complex objects with nested properties | API responses, database records, configuration objects |
| **Primitive** | Simple scalar values | Status codes, identifiers, counts, flags |
| **Array** | Collections of items | Lists, search results, batches |
| **Binary** | Non-JSON data | Files, images, audio, video |
| **Stream** | Continuous data flows | Real-time updates, event streams |
| **Void** | No return value | Side-effect operations, fire-and-forget |

### 3.2 Category Selection Guide

```
Does the tool return data?
├── No → Void
├── Yes → Is it a continuous flow?
│   ├── Yes → Stream
│   └── No → Is it binary/non-JSON?
│       ├── Yes → Binary
│       └── No → Is it a collection?
│           ├── Yes → Array
│           └── No → Is it a simple value?
│               ├── Yes → Primitive
│               └── No → Structured
```

---

## 4. Standard Return Type Definitions

### 4.1 Structured Return Types

#### 4.1.1 ObjectResult

**Purpose**: Generic object return with success/error wrapper

**Schema**:
```json
{
  "$id": "https://adl.io/schemas/returns/ObjectResult",
  "type": "object",
  "properties": {
    "success": {
      "type": "boolean",
      "description": "Indicates if the operation succeeded"
    },
    "data": {
      "type": "object",
      "description": "The actual return data",
      "additionalProperties": true
    },
    "error": {
      "type": "object",
      "description": "Error details if success is false",
      "properties": {
        "code": { "type": "string" },
        "message": { "type": "string" },
        "details": { "type": "object" }
      }
    },
    "metadata": {
      "type": "object",
      "description": "Response metadata",
      "properties": {
        "timestamp": { "type": "string", "format": "date-time" },
        "request_id": { "type": "string" },
        "duration_ms": { "type": "integer" }
      }
    }
  },
  "required": ["success"],
  "oneOf": [
    { "required": ["data"] },
    { "required": ["error"] }
  ]
}
```

**Example**:
```json
{
  "success": true,
  "data": {
    "user_id": "usr_12345",
    "username": "johndoe",
    "created_at": "2026-02-15T10:30:00Z"
  },
  "metadata": {
    "timestamp": "2026-02-15T10:30:00Z",
    "request_id": "req_abc123",
    "duration_ms": 45
  }
}
```

**Use Cases**:
- CRUD operations
- API responses
- Service calls

---

#### 4.1.2 EntityResult

**Purpose**: Single entity with type discriminator

**Schema**:
```json
{
  "$id": "https://adl.io/schemas/returns/EntityResult",
  "type": "object",
  "properties": {
    "id": { "type": "string" },
    "type": { "type": "string" },
    "attributes": {
      "type": "object",
      "additionalProperties": true
    },
    "relationships": {
      "type": "object",
      "additionalProperties": {
        "type": "object",
        "properties": {
          "data": {
            "oneOf": [
              { "type": "object" },
              { "type": "array" }
            ]
          }
        }
      }
    },
    "meta": { "type": "object" }
  },
  "required": ["id", "type"]
}
```

**Example**:
```json
{
  "id": "prod_98765",
  "type": "product",
  "attributes": {
    "name": "Wireless Headphones",
    "price": 99.99,
    "category": "electronics",
    "in_stock": true
  },
  "relationships": {
    "manufacturer": {
      "data": { "id": "mfg_123", "type": "manufacturer" }
    },
    "reviews": {
      "data": [
        { "id": "rev_001", "type": "review" },
        { "id": "rev_002", "type": "review" }
      ]
    }
  },
  "meta": {
    "created_at": "2026-01-15T08:00:00Z",
    "updated_at": "2026-02-10T14:30:00Z"
  }
}
```

**Use Cases**:
- Database entity retrieval
- Resource representation
- Typed object returns

---

#### 4.1.3 OperationStatus

**Purpose**: Async operation status tracking

**Schema**:
```json
{
  "$id": "https://adl.io/schemas/returns/OperationStatus",
  "type": "object",
  "properties": {
    "operation_id": { "type": "string" },
    "status": {
      "type": "string",
      "enum": ["pending", "running", "completed", "failed", "cancelled"]
    },
    "progress": {
      "type": "object",
      "properties": {
        "percent": { "type": "integer", "minimum": 0, "maximum": 100 },
        "current_step": { "type": "integer" },
        "total_steps": { "type": "integer" },
        "message": { "type": "string" }
      }
    },
    "result": {
      "type": "object",
      "description": "Present when status is 'completed'"
    },
    "error": {
      "type": "object",
      "description": "Present when status is 'failed'",
      "properties": {
        "code": { "type": "string" },
        "message": { "type": "string" }
      }
    },
    "created_at": { "type": "string", "format": "date-time" },
    "updated_at": { "type": "string", "format": "date-time" },
    "completed_at": { "type": "string", "format": "date-time" }
  },
  "required": ["operation_id", "status", "created_at"]
}
```

**Example**:
```json
{
  "operation_id": "op_abc123xyz",
  "status": "running",
  "progress": {
    "percent": 65,
    "current_step": 13,
    "total_steps": 20,
    "message": "Processing batch 13 of 20"
  },
  "created_at": "2026-02-15T10:00:00Z",
  "updated_at": "2026-02-15T10:05:30Z"
}
```

**Use Cases**:
- Long-running operations
- Batch processing
- Async job tracking

---

### 4.2 Primitive Return Types

#### 4.2.1 StringValue

**Purpose**: Simple string return

**Schema**:
```json
{
  "$id": "https://adl.io/schemas/returns/StringValue",
  "oneOf": [
    { "type": "string" },
    {
      "type": "object",
      "properties": {
        "success": { "type": "boolean" },
        "value": { "type": "string" },
        "error": {
          "type": "object",
          "properties": {
            "code": { "type": "string" },
            "message": { "type": "string" }
          }
        }
      },
      "required": ["success"]
    }
  ]
}
```

**Examples**:
```json
"Hello, World!"
```

```json
{
  "success": true,
  "value": "Hello, World!"
}
```

**Use Cases**:
- Text generation
- Name/slug generation
- Simple message returns

---

#### 4.2.2 NumberValue

**Purpose**: Numeric return (integer or float)

**Schema**:
```json
{
  "$id": "https://adl.io/schemas/returns/NumberValue",
  "oneOf": [
    { "type": "number" },
    {
      "type": "object",
      "properties": {
        "success": { "type": "boolean" },
        "value": { "type": "number" },
        "unit": { "type": "string" },
        "error": {
          "type": "object",
          "properties": {
            "code": { "type": "string" },
            "message": { "type": "string" }
          }
        }
      },
      "required": ["success"]
    }
  ]
}
```

**Examples**:
```json
42
```

```json
{
  "success": true,
  "value": 98.6,
  "unit": "fahrenheit"
}
```

**Use Cases**:
- Counts and tallies
- Measurements
- Calculations

---

#### 4.2.3 BooleanValue

**Purpose**: True/false return

**Schema**:
```json
{
  "$id": "https://adl.io/schemas/returns/BooleanValue",
  "oneOf": [
    { "type": "boolean" },
    {
      "type": "object",
      "properties": {
        "success": { "type": "boolean" },
        "value": { "type": "boolean" },
        "error": {
          "type": "object",
          "properties": {
            "code": { "type": "string" },
            "message": { "type": "string" }
          }
        }
      },
      "required": ["success"]
    }
  ]
}
```

**Examples**:
```json
true
```

```json
{
  "success": true,
  "value": false
}
```

**Use Cases**:
- Validation results
- Feature flags
- Existence checks

---

#### 4.2.4 IdentifierValue

**Purpose**: Unique identifier return

**Schema**:
```json
{
  "$id": "https://adl.io/schemas/returns/IdentifierValue",
  "type": "object",
  "properties": {
    "success": { "type": "boolean" },
    "id": { "type": "string" },
    "type": { "type": "string" },
    "error": {
      "type": "object",
      "properties": {
        "code": { "type": "string" },
        "message": { "type": "string" }
      }
    }
  },
  "required": ["success"]
}
```

**Example**:
```json
{
  "success": true,
  "id": "usr_12345abcde",
  "type": "user"
}
```

**Use Cases**:
- ID generation
- Reference returns
- Lookup results

---

### 4.3 Array Return Types

#### 4.3.1 ListResult

**Purpose**: Generic list with pagination

**Schema**:
```json
{
  "$id": "https://adl.io/schemas/returns/ListResult",
  "type": "object",
  "properties": {
    "success": { "type": "boolean" },
    "data": {
      "type": "array",
      "items": { "type": "object" }
    },
    "pagination": {
      "type": "object",
      "properties": {
        "page": { "type": "integer", "minimum": 1 },
        "per_page": { "type": "integer", "minimum": 1 },
        "total": { "type": "integer", "minimum": 0 },
        "total_pages": { "type": "integer", "minimum": 0 },
        "has_next": { "type": "boolean" },
        "has_prev": { "type": "boolean" }
      }
    },
    "error": {
      "type": "object",
      "properties": {
        "code": { "type": "string" },
        "message": { "type": "string" }
      }
    }
  },
  "required": ["success", "data"]
}
```

**Example**:
```json
{
  "success": true,
  "data": [
    { "id": "1", "name": "Item 1" },
    { "id": "2", "name": "Item 2" },
    { "id": "3", "name": "Item 3" }
  ],
  "pagination": {
    "page": 1,
    "per_page": 10,
    "total": 45,
    "total_pages": 5,
    "has_next": true,
    "has_prev": false
  }
}
```

**Use Cases**:
- Search results
- List endpoints
- Paginated data

---

#### 4.3.2 BatchResult

**Purpose**: Batch operation results with individual item status

**Schema**:
```json
{
  "$id": "https://adl.io/schemas/returns/BatchResult",
  "type": "object",
  "properties": {
    "success": { "type": "boolean" },
    "batch_id": { "type": "string" },
    "total": { "type": "integer", "minimum": 0 },
    "successful": { "type": "integer", "minimum": 0 },
    "failed": { "type": "integer", "minimum": 0 },
    "items": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "id": { "type": "string" },
          "success": { "type": "boolean" },
          "data": { "type": "object" },
          "error": {
            "type": "object",
            "properties": {
              "code": { "type": "string" },
              "message": { "type": "string" }
            }
          }
        },
        "required": ["id", "success"]
      }
    },
    "errors": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "code": { "type": "string" },
          "message": { "type": "string" },
          "count": { "type": "integer" }
        }
      }
    }
  },
  "required": ["success", "batch_id", "total"]
}
```

**Example**:
```json
{
  "success": true,
  "batch_id": "batch_abc123",
  "total": 100,
  "successful": 98,
  "failed": 2,
  "items": [
    {
      "id": "item_001",
      "success": true,
      "data": { "processed_at": "2026-02-15T10:00:00Z" }
    },
    {
      "id": "item_099",
      "success": false,
      "error": {
        "code": "VALIDATION_ERROR",
        "message": "Invalid email format"
      }
    }
  ],
  "errors": [
    {
      "code": "VALIDATION_ERROR",
      "message": "Invalid email format",
      "count": 2
    }
  ]
}
```

**Use Cases**:
- Bulk operations
- Import/export
- Batch processing

---

### 4.4 Binary Return Types

#### 4.4.1 FileResult

**Purpose**: File download with metadata

**Schema**:
```json
{
  "$id": "https://adl.io/schemas/returns/FileResult",
  "type": "object",
  "properties": {
    "success": { "type": "boolean" },
    "file": {
      "type": "object",
      "properties": {
        "name": { "type": "string" },
        "size": { "type": "integer" },
        "content_type": { "type": "string" },
        "url": { "type": "string", "format": "uri" },
        "data": { "type": "string", "description": "Base64 encoded content" },
        "checksum": {
          "type": "object",
          "properties": {
            "algorithm": { "type": "string" },
            "value": { "type": "string" }
          }
        }
      }
    },
    "error": {
      "type": "object",
      "properties": {
        "code": { "type": "string" },
        "message": { "type": "string" }
      }
    }
  },
  "required": ["success"]
}
```

**Example**:
```json
{
  "success": true,
  "file": {
    "name": "report_2026.pdf",
    "size": 1048576,
    "content_type": "application/pdf",
    "url": "https://storage.example.com/files/report_2026.pdf",
    "checksum": {
      "algorithm": "sha256",
      "value": "a1b2c3d4e5f6..."
    }
  }
}
```

**Use Cases**:
- Document generation
- Export functionality
- File downloads

---

#### 4.4.2 MediaResult

**Purpose**: Media file (image, audio, video) with metadata

**Schema**:
```json
{
  "$id": "https://adl.io/schemas/returns/MediaResult",
  "type": "object",
  "properties": {
    "success": { "type": "boolean" },
    "media": {
      "type": "object",
      "properties": {
        "type": {
          "type": "string",
          "enum": ["image", "audio", "video"]
        },
        "url": { "type": "string", "format": "uri" },
        "data": { "type": "string", "description": "Base64 encoded content" },
        "format": { "type": "string" },
        "dimensions": {
          "type": "object",
          "properties": {
            "width": { "type": "integer" },
            "height": { "type": "integer" }
          }
        },
        "duration": { "type": "number", "description": "Duration in seconds" },
        "size": { "type": "integer" },
        "alt_text": { "type": "string" }
      },
      "required": ["type"]
    },
    "error": {
      "type": "object",
      "properties": {
        "code": { "type": "string" },
        "message": { "type": "string" }
      }
    }
  },
  "required": ["success"]
}
```

**Example**:
```json
{
  "success": true,
  "media": {
    "type": "image",
    "url": "https://cdn.example.com/images/generated_123.png",
    "format": "png",
    "dimensions": {
      "width": 1024,
      "height": 1024
    },
    "size": 524288,
    "alt_text": "Generated marketing image for summer campaign"
  }
}
```

**Use Cases**:
- Image generation
- Audio processing
- Video manipulation

---

### 4.5 Stream Return Types

#### 4.5.1 EventStream

**Purpose**: Server-sent events or WebSocket message format

**Schema**:
```json
{
  "$id": "https://adl.io/schemas/returns/EventStream",
  "type": "object",
  "properties": {
    "event": { "type": "string" },
    "id": { "type": "string" },
    "data": {},
    "retry": { "type": "integer" }
  },
  "required": ["event"]
}
```

**Example**:
```json
{
  "event": "message",
  "id": "msg_001",
  "data": {
    "role": "assistant",
    "content": "Processing your request..."
  }
}
```

**Use Cases**:
- Real-time updates
- Chat streaming
- Progress notifications

---

#### 4.5.2 ChunkedData

**Purpose**: Chunked data transfer for large payloads

**Schema**:
```json
{
  "$id": "https://adl.io/schemas/returns/ChunkedData",
  "type": "object",
  "properties": {
    "chunk_id": { "type": "string" },
    "sequence": { "type": "integer", "minimum": 0 },
    "total_chunks": { "type": "integer", "minimum": 1 },
    "data": { "type": "string", "description": "Base64 encoded chunk" },
    "is_last": { "type": "boolean" },
    "checksum": { "type": "string" }
  },
  "required": ["chunk_id", "sequence", "total_chunks", "data"]
}
```

**Example**:
```json
{
  "chunk_id": "chunk_abc123",
  "sequence": 5,
  "total_chunks": 20,
  "data": "SGVsbG8gV29ybGQg...",
  "is_last": false,
  "checksum": "a1b2c3"
}
```

**Use Cases**:
- Large file transfers
- Streaming data processing
- Incremental updates

---

### 4.6 Void Return Type

#### 4.6.1 VoidResult

**Purpose**: No return value, only status

**Schema**:
```json
{
  "$id": "https://adl.io/schemas/returns/VoidResult",
  "type": "object",
  "properties": {
    "success": { "type": "boolean" },
    "message": { "type": "string" },
    "error": {
      "type": "object",
      "properties": {
        "code": { "type": "string" },
        "message": { "type": "string" }
      }
    }
  },
  "required": ["success"]
}
```

**Example**:
```json
{
  "success": true,
  "message": "Operation completed successfully"
}
```

**Use Cases**:
- Delete operations
- Fire-and-forget
- Side-effect only operations

---

## 5. Error Handling Patterns

### 5.1 Standard Error Structure

All return types support a consistent error structure:

```json
{
  "success": false,
  "error": {
    "code": "ERROR_CODE",
    "message": "Human-readable error message",
    "details": {
      "field": "additional context"
    },
    "stack_trace": "Optional stack trace for debugging"
  }
}
```

### 5.2 Error Code Categories

| Category | Prefix | Example Codes |
|----------|--------|---------------|
| Validation | `VALIDATION_` | `VALIDATION_REQUIRED`, `VALIDATION_FORMAT` |
| Authentication | `AUTH_` | `AUTH_UNAUTHORIZED`, `AUTH_EXPIRED` |
| Authorization | `FORBIDDEN_` | `FORBIDDEN_ACCESS`, `FORBIDDEN_SCOPE` |
| Not Found | `NOT_FOUND_` | `NOT_FOUND_RESOURCE`, `NOT_FOUND_ENDPOINT` |
| Conflict | `CONFLICT_` | `CONFLICT_DUPLICATE`, `CONFLICT_STATE` |
| Rate Limit | `RATE_LIMIT_` | `RATE_LIMIT_EXCEEDED` |
| Internal | `INTERNAL_` | `INTERNAL_ERROR`, `INTERNAL_TIMEOUT` |
| External | `EXTERNAL_` | `EXTERNAL_API_ERROR`, `EXTERNAL_TIMEOUT` |

### 5.3 Error Response Examples

**Validation Error**:
```json
{
  "success": false,
  "error": {
    "code": "VALIDATION_REQUIRED",
    "message": "Required field 'email' is missing",
    "details": {
      "field": "email",
      "constraint": "required"
    }
  }
}
```

**Not Found Error**:
```json
{
  "success": false,
  "error": {
    "code": "NOT_FOUND_RESOURCE",
    "message": "User with ID 'usr_123' not found",
    "details": {
      "resource_type": "user",
      "resource_id": "usr_123"
    }
  }
}
```

---

## 6. Return Type Schema Reference

### 6.1 JSON Schema Definition

The complete return type system is defined in the ADL schema:

```json
{
  "$defs": {
    "ReturnType": {
      "type": "object",
      "description": "Return type definition for a tool",
      "additionalProperties": false,
      "properties": {
        "type": {
          "type": "string",
          "description": "Return type category",
          "enum": [
            "ObjectResult",
            "EntityResult",
            "OperationStatus",
            "StringValue",
            "NumberValue",
            "BooleanValue",
            "IdentifierValue",
            "ListResult",
            "BatchResult",
            "FileResult",
            "MediaResult",
            "EventStream",
            "ChunkedData",
            "VoidResult",
            "Custom"
          ]
        },
        "schema": {
          "oneOf": [
            { "type": "object" },
            { "type": "string", "format": "uri" }
          ],
          "description": "JSON Schema or reference to schema definition"
        },
        "description": {
          "type": "string",
          "description": "Human-readable description of the return value"
        },
        "examples": {
          "type": "array",
          "description": "Example return values",
          "items": {}
        },
        "content_type": {
          "type": "string",
          "description": "MIME type of the return value",
          "default": "application/json"
        }
      },
      "required": ["type", "schema"]
    },
    "StandardReturnTypes": {
      "description": "Standard return type schemas",
      "type": "object",
      "properties": {
        "ObjectResult": { "$ref": "#/$defs/ObjectResultSchema" },
        "EntityResult": { "$ref": "#/$defs/EntityResultSchema" },
        "OperationStatus": { "$ref": "#/$defs/OperationStatusSchema" },
        "StringValue": { "$ref": "#/$defs/StringValueSchema" },
        "NumberValue": { "$ref": "#/$defs/NumberValueSchema" },
        "BooleanValue": { "$ref": "#/$defs/BooleanValueSchema" },
        "IdentifierValue": { "$ref": "#/$defs/IdentifierValueSchema" },
        "ListResult": { "$ref": "#/$defs/ListResultSchema" },
        "BatchResult": { "$ref": "#/$defs/BatchResultSchema" },
        "FileResult": { "$ref": "#/$defs/FileResultSchema" },
        "MediaResult": { "$ref": "#/$defs/MediaResultSchema" },
        "EventStream": { "$ref": "#/$defs/EventStreamSchema" },
        "ChunkedData": { "$ref": "#/$defs/ChunkedDataSchema" },
        "VoidResult": { "$ref": "#/$defs/VoidResultSchema" }
      }
    }
  }
}
```

### 6.2 Return Type Selection Matrix

| Use Case | Recommended Type | Alternative |
|----------|-----------------|-------------|
| Create/Update/Delete | `ObjectResult` | `EntityResult` |
| Get Single Item | `EntityResult` | `ObjectResult` |
| Search/List | `ListResult` | `BatchResult` |
| Bulk Operations | `BatchResult` | `OperationStatus` |
| Long-running Task | `OperationStatus` | `EventStream` |
| Generate Text | `StringValue` | `ObjectResult` |
| Calculate/Count | `NumberValue` | `ObjectResult` |
| Check/Validate | `BooleanValue` | `ObjectResult` |
| Generate ID | `IdentifierValue` | `StringValue` |
| Generate File | `FileResult` | `MediaResult` |
| Generate Image/Audio/Video | `MediaResult` | `FileResult` |
| Real-time Updates | `EventStream` | `ChunkedData` |
| Large Data Transfer | `ChunkedData` | `FileResult` |
| Delete/Archive | `VoidResult` | `ObjectResult` |

---

## 7. Migration Guide

### 7.1 From ADL v1.0 to v1.5

**Before (v1.0)**:
```json
{
  "tools": [{
    "name": "get_user",
    "returns": {
      "type": "object",
      "description": "Returns user data"
    }
  }]
}
```

**After (v1.5)**:
```json
{
  "tools": [{
    "name": "get_user",
    "returns": {
      "type": "EntityResult",
      "schema": {
        "$ref": "#/$defs/StandardReturnTypes/EntityResult"
      },
      "description": "Returns user entity with relationships",
      "examples": [{
        "id": "usr_123",
        "type": "user",
        "attributes": {
          "name": "John Doe",
          "email": "john@example.com"
        }
      }]
    }
  }]
}
```

### 7.2 Migration Steps

1. **Identify Current Return Types**: Review all tools with `returns` field
2. **Map to New Types**: Use the selection matrix to choose appropriate types
3. **Add Schema References**: Replace simple type strings with schema references
4. **Add Examples**: Include at least one example for each return type
5. **Validate**: Use ADL validator to check new definitions

### 7.3 Backward Compatibility

- Old `returns` objects with `type` and `description` remain valid
- Tools without `returns` field continue to work
- Migration is optional but recommended for new features

---

## 8. Best Practices

### 8.1 Return Type Design

1. **Always Include Success Flag**: Use `success` boolean for clear status indication
2. **Provide Examples**: Include realistic examples for documentation
3. **Use Standard Types**: Prefer standard types over custom schemas
4. **Handle Errors Consistently**: Use standard error structure
5. **Document Content Types**: Specify when returning non-JSON data

### 8.2 Common Patterns

**Pattern 1: Simple Success Response**:
```json
{
  "success": true,
  "data": { "id": "123" }
}
```

**Pattern 2: Error with Details**:
```json
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid input",
    "details": { "field": "email", "issue": "format" }
  }
}
```

**Pattern 3: Paginated List**:
```json
{
  "success": true,
  "data": [...],
  "pagination": {
    "page": 1,
    "per_page": 10,
    "total": 100
  }
}
```

---

## 9. Appendix

### 9.1 Complete Type Reference

| Type | Category | Schema ID | Description |
|------|----------|-----------|-------------|
| ObjectResult | Structured | `https://adl.io/schemas/returns/ObjectResult` | Generic object with success/error wrapper |
| EntityResult | Structured | `https://adl.io/schemas/returns/EntityResult` | Typed entity with relationships |
| OperationStatus | Structured | `https://adl.io/schemas/returns/OperationStatus` | Async operation tracking |
| StringValue | Primitive | `https://adl.io/schemas/returns/StringValue` | Simple string return |
| NumberValue | Primitive | `https://adl.io/schemas/returns/NumberValue` | Numeric return |
| BooleanValue | Primitive | `https://adl.io/schemas/returns/BooleanValue` | True/false return |
| IdentifierValue | Primitive | `https://adl.io/schemas/returns/IdentifierValue` | ID generation/return |
| ListResult | Array | `https://adl.io/schemas/returns/ListResult` | Paginated list |
| BatchResult | Array | `https://adl.io/schemas/returns/BatchResult` | Batch operation results |
| FileResult | Binary | `https://adl.io/schemas/returns/FileResult` | File download |
| MediaResult | Binary | `https://adl.io/schemas/returns/MediaResult` | Media file (image/audio/video) |
| EventStream | Stream | `https://adl.io/schemas/returns/EventStream` | Real-time events |
| ChunkedData | Stream | `https://adl.io/schemas/returns/ChunkedData` | Chunked transfer |
| VoidResult | Void | `https://adl.io/schemas/returns/VoidResult` | No return value |

### 9.2 JSON Schema References

All return type schemas are compatible with:
- JSON Schema Draft 2020-12
- OpenAPI 3.0+ Specification
- JSON Schema Validation Draft 2020-12

### 9.3 Related Documentation

- [ADL Schema Reference](./schema-reference.md)
- [Parameter Type System](./parameter-type-system.md)
- [Tool Definition Guide](./tool-definition-guide.md)
- [Migration Guide v1.5](./migration-v1.5.md)

---

## 10. Changelog

### v1.5.0 (2026-02-15)
- Initial release of Return Type System
- 15 standard return type definitions
- Error handling patterns
- Migration guide from v1.0

---

*End of Specification*
