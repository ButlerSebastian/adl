# ADL Enhanced Type System Specification

## Overview

The ADL Enhanced Type System extends the basic parameter typing in Agent Definition Language (ADL) to support precise, expressive, and validated tool contracts. This specification defines a comprehensive type system leveraging JSON Schema 2020-12 advanced features to enable:

- **Precise Validation**: Constraints ensure parameters meet exact requirements
- **Type Safety**: Rich type definitions prevent runtime errors
- **Self-Documentation**: Types convey semantic meaning and valid ranges
- **Interoperability**: Standard JSON Schema ensures compatibility across tools
- **Backward Compatibility**: Existing simple type definitions remain valid

## Type Categories

The enhanced type system organizes types into five categories:

### 1. Primitive Types
Basic scalar values with optional constraints.

- `string` - Text values with length and pattern constraints
- `number` - Floating-point numbers with range constraints
- `integer` - Whole numbers with range and multiple constraints
- `boolean` - True/false values
- `null` - Explicit null value

### 2. Complex Types
Structured data with nested schemas.

- `object` - Key-value structures with defined properties
- `array` - Ordered collections with item type constraints
- `tuple` - Fixed-length arrays with typed positions

### 3. Special Types
Domain-specific types with format validation.

- `datetime` - ISO 8601 date-time strings
- `date` - ISO 8601 date strings
- `time` - ISO 8601 time strings
- `duration` - ISO 8601 duration strings
- `uri` - URI/URL strings
- `email` - Email address strings
- `uuid` - UUID v4 strings
- `ipv4` - IPv4 address strings
- `ipv6` - IPv6 address strings
- `hostname` - Valid hostname strings
- `regex` - Valid regular expression strings
- `json-pointer` - JSON Pointer (RFC 6901) strings
- `base64` - Base64-encoded strings
- `binary` - Binary data (base64-encoded)

### 4. Semantic Types
Pre-defined constrained types for common use cases.

- `email` - Validated email address
- `url` - Validated URL
- `uuid` - UUID format
- `semver` - Semantic version string
- `slug` - URL-friendly identifier
- `color_hex` - Hex color code
- `language_code` - ISO 639-1 language code
- `country_code` - ISO 3166-1 country code
- `currency_code` - ISO 4217 currency code
- `timezone` - IANA timezone identifier

### 5. Composite Types
Type compositions for advanced scenarios.

- `union` (anyOf) - Value matches any of multiple types
- `intersection` (allOf) - Value matches all of multiple types
- `exclusive` (oneOf) - Value matches exactly one of multiple types
- `conditional` (if/then/else) - Type depends on another field

---

## Type Constraint System

### String Constraints

| Constraint | Type | Description | Example |
|------------|------|-------------|---------|
| `minLength` | integer | Minimum string length | `"minLength": 1` |
| `maxLength` | integer | Maximum string length | `"maxLength": 255` |
| `pattern` | string | Regex pattern (ECMA-262) | `"pattern": "^[a-z]+$"` |
| `format` | string | Predefined format | `"format": "email"` |
| `enum` | array | Allowed values | `"enum": ["a", "b"]` |

**Built-in Formats:**
- `date` - RFC 3339 date (e.g., "2024-01-15")
- `date-time` - RFC 3339 date-time (e.g., "2024-01-15T10:30:00Z")
- `time` - RFC 3339 time (e.g., "10:30:00Z")
- `duration` - ISO 8601 duration (e.g., "P1Y2M3DT4H5M6S")
- `email` - Email address per RFC 5322
- `hostname` - Internet hostname per RFC 1123
- `ipv4` - IPv4 address
- `ipv6` - IPv6 address
- `uri` - Absolute URI per RFC 3986
- `uri-reference` - URI or relative reference
- `uuid` - UUID per RFC 4122
- `regex` - Regular expression
- `json-pointer` - JSON Pointer per RFC 6901

### Numeric Constraints

| Constraint | Type | Description | Example |
|------------|------|-------------|---------|
| `minimum` | number | Minimum value (inclusive) | `"minimum": 0` |
| `maximum` | number | Maximum value (inclusive) | `"maximum": 100` |
| `exclusiveMinimum` | number | Minimum value (exclusive) | `"exclusiveMinimum": 0` |
| `exclusiveMaximum` | number | Maximum value (exclusive) | `"exclusiveMaximum": 100` |
| `multipleOf` | number | Value must be multiple of | `"multipleOf": 0.01` |

### Array Constraints

| Constraint | Type | Description | Example |
|------------|------|-------------|---------|
| `minItems` | integer | Minimum number of items | `"minItems": 1` |
| `maxItems` | integer | Maximum number of items | `"maxItems": 100` |
| `uniqueItems` | boolean | All items must be unique | `"uniqueItems": true` |
| `items` | schema | Schema for all items | `"items": {"type": "string"}` |
| `contains` | schema | At least one item must match | `"contains": {"type": "integer"}` |

### Object Constraints

| Constraint | Type | Description | Example |
|------------|------|-------------|---------|
| `properties` | object | Defined property schemas | See examples below |
| `required` | array | Required property names | `"required": ["id", "name"]` |
| `additionalProperties` | boolean/schema | Allow extra properties | `"additionalProperties": false` |
| `patternProperties` | object | Regex-based property schemas | See examples below |
| `propertyNames` | schema | Schema for property names | `"propertyNames": {"pattern": "^[a-z]+$"}` |
| `minProperties` | integer | Minimum property count | `"minProperties": 1` |
| `maxProperties` | integer | Maximum property count | `"maxProperties": 10` |

---

## Type Constraint Library

The following pre-defined types are available for common use cases. Each type is defined as a JSON Schema fragment that can be referenced or embedded.

### 1. email

Validates email addresses per RFC 5322.

```json
{
  "type": "string",
  "format": "email",
  "description": "Valid email address"
}
```

**Valid:** `"user@example.com"`, `"name+tag@domain.co.uk"`
**Invalid:** `"not-an-email"`, `"@example.com"`, `"user@"`

### 2. url

Validates absolute URLs.

```json
{
  "type": "string",
  "format": "uri",
  "description": "Valid URL"
}
```

**Valid:** `"https://example.com"`, `"ftp://files.example.org"`
**Invalid:** `"not-a-url"`, `"/relative/path"`

### 3. uuid

Validates UUID v4 format.

```json
{
  "type": "string",
  "format": "uuid",
  "description": "UUID v4 identifier"
}
```

**Valid:** `"550e8400-e29b-41d4-a716-446655440000"`
**Invalid:** `"not-a-uuid"`, `"550e8400"`

### 4. datetime

Validates ISO 8601 date-time strings.

```json
{
  "type": "string",
  "format": "date-time",
  "description": "ISO 8601 date-time"
}
```

**Valid:** `"2024-01-15T10:30:00Z"`, `"2024-01-15T10:30:00+05:30"`
**Invalid:** `"2024-01-15"`, `"10:30:00"`

### 5. semver

Validates semantic version strings (MAJOR.MINOR.PATCH).

```json
{
  "type": "string",
  "pattern": "^(0|[1-9]\\d*)\\.(0|[1-9]\\d*)\\.(0|[1-9]\\d*)(?:-((?:0|[1-9]\\d*|\\d*[a-zA-Z-][0-9a-zA-Z-]*)(?:\\.(?:0|[1-9]\\d*|\\d*[a-zA-Z-][0-9a-zA-Z-]*))*))?(?:\\+([0-9a-zA-Z-]+(?:\\.[0-9a-zA-Z-]+)*))?$",
  "description": "Semantic version (e.g., 1.2.3, 2.0.0-alpha.1)"
}
```

**Valid:** `"1.2.3"`, `"2.0.0-alpha.1"`, `"1.0.0+build.123"`
**Invalid:** `"v1.2.3"`, `"1.2"`, `"1.2.3.4"`

### 6. positive_number

Positive floating-point number (greater than 0).

```json
{
  "type": "number",
  "exclusiveMinimum": 0,
  "description": "Positive number (> 0)"
}
```

**Valid:** `0.01`, `1`, `100.5`
**Invalid:** `0`, `-1`, `-0.5`

### 7. percentage

Number between 0 and 100 (inclusive).

```json
{
  "type": "number",
  "minimum": 0,
  "maximum": 100,
  "description": "Percentage value (0-100)"
}
```

**Valid:** `0`, `50`, `100`, `99.9`
**Invalid:** `-1`, `101`, `150`

### 8. non_empty_string

String with at least one character.

```json
{
  "type": "string",
  "minLength": 1,
  "description": "Non-empty string"
}
```

**Valid:** `"a"`, `"hello"`, `" "`
**Invalid:** `""` (empty string)

### 9. slug

URL-friendly identifier (lowercase, alphanumeric, hyphens).

```json
{
  "type": "string",
  "pattern": "^[a-z0-9]+(?:-[a-z0-9]+)*$",
  "minLength": 1,
  "maxLength": 100,
  "description": "URL-friendly slug (e.g., 'my-page-title')"
}
```

**Valid:** `"hello-world"`, `"page123"`, `"a"`
**Invalid:** `"Hello World"`, `"slug_with_underscores"`, `"-starts-with-hyphen"`

### 10. json_string

String containing valid JSON.

```json
{
  "type": "string",
  "contentMediaType": "application/json",
  "description": "JSON-encoded string"
}
```

**Valid:** `'{"key": "value"}'`, `'[1, 2, 3]'`, `'"string"'`
**Invalid:** `'not json'`, `'{'`, `'{key: value}'`

### 11. color_hex

Hexadecimal color code.

```json
{
  "type": "string",
  "pattern": "^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$",
  "description": "Hex color code (e.g., #FF5733, #f0f)"
}
```

**Valid:** `"#FF5733"`, `"#f0f"`, `"#aabbcc"`
**Invalid:** `"FF5733"`, `"#GGGGGG"`, `"#ff"`

### 12. language_code

ISO 639-1 language code.

```json
{
  "type": "string",
  "pattern": "^[a-z]{2}$",
  "description": "ISO 639-1 language code (e.g., 'en', 'fr', 'de')"
}
```

**Valid:** `"en"`, `"fr"`, `"de"`, `"ja"`
**Invalid:** `"eng"`, `"EN"`, `"e"`

### 13. country_code

ISO 3166-1 alpha-2 country code.

```json
{
  "type": "string",
  "pattern": "^[A-Z]{2}$",
  "description": "ISO 3166-1 country code (e.g., 'US', 'GB', 'JP')"
}
```

**Valid:** `"US"`, `"GB"`, `"JP"`, `"DE"`
**Invalid:** `"usa"`, `"us"`, `"U"`

### 14. currency_code

ISO 4217 currency code.

```json
{
  "type": "string",
  "pattern": "^[A-Z]{3}$",
  "description": "ISO 4217 currency code (e.g., 'USD', 'EUR', 'JPY')"
}
```

**Valid:** `"USD"`, `"EUR"`, `"JPY"`, `"GBP"`
**Invalid:** `"$"`, `"dollar"`, `"us"`

### 15. timezone

IANA timezone identifier.

```json
{
  "type": "string",
  "pattern": "^[A-Za-z_]+/[A-Za-z_]+$",
  "description": "IANA timezone (e.g., 'America/New_York', 'UTC')"
}
```

**Valid:** `"America/New_York"`, `"UTC"`, `"Europe/London"`
**Invalid:** `"EST"`, `"New York"`, `"America-New-York"`

### 16. port_number

Valid TCP/UDP port number.

```json
{
  "type": "integer",
  "minimum": 1,
  "maximum": 65535,
  "description": "Port number (1-65535)"
}
```

**Valid:** `1`, `80`, `443`, `8080`, `65535`
**Invalid:** `0`, `65536`, `-1`, `3.14`

### 17. file_path

Valid file path string.

```json
{
  "type": "string",
  "minLength": 1,
  "pattern": "^[^\\0]+$",
  "description": "File path (no null bytes)"
}
```

**Valid:** `"/home/user/file.txt"`, `"C:\\Windows\\file.txt"`, `"relative/path"`
**Invalid:** `"path\\x00with\\x00null"`

### 18. file_extension

File extension (with dot).

```json
{
  "type": "string",
  "pattern": "^\\.[a-zA-Z0-9]+$",
  "description": "File extension (e.g., '.txt', '.json')"
}
```

**Valid:** `".txt"`, `".json"`, `".py"`, `".HTML"`
**Invalid:** `"txt"`, `"."`, `".file.name"`

### 19. ipv4

IPv4 address.

```json
{
  "type": "string",
  "format": "ipv4",
  "description": "IPv4 address"
}
```

**Valid:** `"192.168.1.1"`, `"10.0.0.1"`, `"255.255.255.255"`
**Invalid:** `"256.1.1.1"`, `"192.168.1"`, `"not-an-ip"`

### 20. ipv6

IPv6 address.

```json
{
  "type": "string",
  "format": "ipv6",
  "description": "IPv6 address"
}
```

**Valid:** `"2001:0db8:85a3:0000:0000:8a2e:0370:7334"`, `"::1"`, `"fe80::1"`
**Invalid:** `"not-an-ip"`, `":::"`

---

## Complex Type Examples

### Object with Properties

```json
{
  "name": "user_profile",
  "type": "object",
  "description": "User profile information",
  "properties": {
    "id": {
      "type": "string",
      "format": "uuid"
    },
    "name": {
      "type": "string",
      "minLength": 1,
      "maxLength": 100
    },
    "email": {
      "type": "string",
      "format": "email"
    },
    "age": {
      "type": "integer",
      "minimum": 0,
      "maximum": 150
    }
  },
  "required": ["id", "name", "email"]
}
```

### Array with Typed Items

```json
{
  "name": "tags",
  "type": "array",
  "description": "List of tags",
  "items": {
    "type": "string",
    "minLength": 1,
    "maxLength": 50,
    "pattern": "^[a-z0-9-]+$"
  },
  "minItems": 0,
  "maxItems": 20,
  "uniqueItems": true
}
```

### Tuple (Fixed Array)

```json
{
  "name": "coordinates",
  "type": "array",
  "description": "Latitude and longitude",
  "items": [
    { "type": "number", "minimum": -90, "maximum": 90 },
    { "type": "number", "minimum": -180, "maximum": 180 }
  ],
  "minItems": 2,
  "maxItems": 2
}
```

### Union Type (anyOf)

```json
{
  "name": "identifier",
  "description": "User identifier (ID or email)",
  "anyOf": [
    {
      "type": "string",
      "format": "uuid",
      "description": "User UUID"
    },
    {
      "type": "string",
      "format": "email",
      "description": "User email"
    }
  ]
}
```

### Intersection Type (allOf)

```json
{
  "name": "validated_email",
  "description": "Email with additional validation",
  "allOf": [
    {
      "type": "string",
      "format": "email"
    },
    {
      "type": "string",
      "minLength": 5,
      "maxLength": 254
    }
  ]
}
```

### Exclusive Type (oneOf)

```json
{
  "name": "port_config",
  "description": "Port configuration (number or range)",
  "oneOf": [
    {
      "type": "integer",
      "minimum": 1,
      "maximum": 65535,
      "description": "Single port"
    },
    {
      "type": "string",
      "pattern": "^\\d+-\\d+$",
      "description": "Port range (e.g., '8080-8090')"
    }
  ]
}
```

### Enum Type

```json
{
  "name": "status",
  "type": "string",
  "description": "Task status",
  "enum": ["pending", "running", "completed", "failed", "cancelled"]
}
```

### Pattern Properties

```json
{
  "name": "metadata",
  "type": "object",
  "description": "Custom metadata with prefixed keys",
  "patternProperties": {
    "^x-": {
      "type": "string",
      "description": "Custom extension field"
    }
  },
  "additionalProperties": false
}
```

---

## Validation Rules

### Type Validation

1. **Primitive Type Checking**: Values must match the declared type
2. **Null Handling**: Explicit `null` type required for nullable values
3. **Type Coercion**: No automatic type conversion (strict mode)

### Constraint Validation

1. **String Constraints**:
   - `minLength` and `maxLength` are inclusive
   - `pattern` uses ECMA-262 regular expressions
   - `format` validation depends on implementation support

2. **Numeric Constraints**:
   - `minimum`/`maximum` are inclusive bounds
   - `exclusiveMinimum`/`exclusiveMaximum` are exclusive bounds
   - `multipleOf` supports decimal values (e.g., 0.01 for currency)

3. **Array Constraints**:
   - `minItems` and `maxItems` apply after validation
   - `uniqueItems` uses deep equality for objects
   - `items` schema validates every array element

4. **Object Constraints**:
   - `required` properties must be present (can be null if type allows)
   - `additionalProperties: false` rejects undefined properties
   - `patternProperties` keys are evaluated in order

### Composition Validation

1. **anyOf (Union)**: Value must validate against at least one schema
2. **oneOf (Exclusive)**: Value must validate against exactly one schema
3. **allOf (Intersection)**: Value must validate against all schemas
4. **not**: Value must not validate against the schema

### Error Reporting

Validation errors should include:
- Path to the invalid field
- Constraint that failed
- Actual value received
- Expected value or constraint

Example error:
```json
{
  "path": "/tools/0/parameters/0/value",
  "constraint": "format",
  "expected": "email",
  "actual": "not-an-email",
  "message": "Value does not match format 'email'"
}
```

---

## Migration Guide

### From Basic Types (v1.0)

**Before (v1.0):**
```json
{
  "name": "email",
  "type": "string",
  "description": "User email address",
  "required": true
}
```

**After (v1.5):**
```json
{
  "name": "email",
  "type": "string",
  "format": "email",
  "description": "User email address",
  "required": true
}
```

### Adding Constraints to Existing Parameters

**Before:**
```json
{
  "name": "limit",
  "type": "number",
  "description": "Maximum results",
  "required": false,
  "default": 10
}
```

**After:**
```json
{
  "name": "limit",
  "type": "integer",
  "minimum": 1,
  "maximum": 1000,
  "description": "Maximum results",
  "required": false,
  "default": 10
}
```

### Converting to Semantic Types

**Before:**
```json
{
  "name": "user_id",
  "type": "string",
  "description": "User UUID",
  "required": true
}
```

**After:**
```json
{
  "name": "user_id",
  "type": "string",
  "format": "uuid",
  "description": "User UUID",
  "required": true
}
```

### Migration Checklist

- [ ] Review all `string` parameters for format opportunities
- [ ] Add `minLength`/`maxLength` to string parameters
- [ ] Review all `number` parameters for range constraints
- [ ] Use `integer` type for whole numbers
- [ ] Add `enum` for parameters with fixed value sets
- [ ] Convert arrays to use `items` schema
- [ ] Add `minItems`/`maxItems` to arrays
- [ ] Define object `properties` for complex parameters
- [ ] Add `required` arrays to object parameters
- [ ] Test all parameters with validation tool

---

## JSON Schema Examples

### Complete Tool Parameter Examples

#### 1. Search with Pagination

```json
{
  "name": "search_documents",
  "description": "Search documents with pagination",
  "parameters": [
    {
      "name": "query",
      "type": "string",
      "minLength": 1,
      "maxLength": 500,
      "description": "Search query string",
      "required": true
    },
    {
      "name": "index_id",
      "type": "string",
      "format": "uuid",
      "description": "Index to search",
      "required": true
    },
    {
      "name": "limit",
      "type": "integer",
      "minimum": 1,
      "maximum": 100,
      "default": 10,
      "description": "Maximum results to return",
      "required": false
    },
    {
      "name": "offset",
      "type": "integer",
      "minimum": 0,
      "default": 0,
      "description": "Number of results to skip",
      "required": false
    }
  ]
}
```

#### 2. User Registration

```json
{
  "name": "register_user",
  "description": "Register a new user",
  "parameters": [
    {
      "name": "email",
      "type": "string",
      "format": "email",
      "description": "User email address",
      "required": true
    },
    {
      "name": "username",
      "type": "string",
      "pattern": "^[a-zA-Z0-9_]{3,20}$",
      "description": "Username (3-20 alphanumeric chars)",
      "required": true
    },
    {
      "name": "age",
      "type": "integer",
      "minimum": 13,
      "maximum": 120,
      "description": "User age",
      "required": false
    },
    {
      "name": "preferences",
      "type": "object",
      "description": "User preferences",
      "properties": {
        "language": {
          "type": "string",
          "pattern": "^[a-z]{2}$",
          "default": "en"
        },
        "notifications": {
          "type": "boolean",
          "default": true
        }
      },
      "required": false
    }
  ]
}
```

#### 3. File Upload

```json
{
  "name": "upload_file",
  "description": "Upload a file",
  "parameters": [
    {
      "name": "filename",
      "type": "string",
      "pattern": "^[^\\\\/:*?\"<>|]+$",
      "maxLength": 255,
      "description": "Name of the file",
      "required": true
    },
    {
      "name": "content_type",
      "type": "string",
      "pattern": "^[a-z]+/[a-z0-9.+-]+$",
      "description": "MIME type",
      "required": true
    },
    {
      "name": "size",
      "type": "integer",
      "minimum": 1,
      "maximum": 104857600,
      "description": "File size in bytes (max 100MB)",
      "required": true
    },
    {
      "name": "tags",
      "type": "array",
      "items": {
        "type": "string",
        "minLength": 1,
        "maxLength": 50
      },
      "maxItems": 10,
      "uniqueItems": true,
      "description": "File tags",
      "required": false
    }
  ]
}
```

#### 4. API Configuration

```json
{
  "name": "configure_api",
  "description": "Configure API endpoint",
  "parameters": [
    {
      "name": "endpoint",
      "type": "string",
      "format": "uri",
      "description": "API endpoint URL",
      "required": true
    },
    {
      "name": "method",
      "type": "string",
      "enum": ["GET", "POST", "PUT", "DELETE", "PATCH"],
      "description": "HTTP method",
      "required": true
    },
    {
      "name": "timeout",
      "type": "integer",
      "minimum": 1,
      "maximum": 300,
      "default": 30,
      "description": "Timeout in seconds",
      "required": false
    },
    {
      "name": "retry_policy",
      "type": "object",
      "description": "Retry configuration",
      "properties": {
        "max_retries": {
          "type": "integer",
          "minimum": 0,
          "maximum": 10,
          "default": 3
        },
        "backoff": {
          "type": "string",
          "enum": ["fixed", "linear", "exponential"],
          "default": "exponential"
        }
      },
      "required": false
    }
  ]
}
```

#### 5. Complex Search Filter

```json
{
  "name": "advanced_search",
  "description": "Advanced search with filters",
  "parameters": [
    {
      "name": "filters",
      "type": "array",
      "description": "Search filters",
      "items": {
        "type": "object",
        "properties": {
          "field": {
            "type": "string",
            "minLength": 1
          },
          "operator": {
            "type": "string",
            "enum": ["eq", "ne", "gt", "gte", "lt", "lte", "contains", "startsWith", "endsWith"]
          },
          "value": {
            "anyOf": [
              { "type": "string" },
              { "type": "number" },
              { "type": "boolean" },
              {
                "type": "array",
                "items": { "type": "string" }
              }
            ]
          }
        },
        "required": ["field", "operator", "value"]
      },
      "required": false
    },
    {
      "name": "sort",
      "type": "array",
      "description": "Sort specifications",
      "items": {
        "type": "object",
        "properties": {
          "field": { "type": "string" },
          "direction": {
            "type": "string",
            "enum": ["asc", "desc"],
            "default": "asc"
          }
        },
        "required": ["field"]
      },
      "maxItems": 3,
      "required": false
    }
  ]
}
```

---

## Schema Reference

### ToolParameter Schema (Enhanced)

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://adl.dev/schemas/tool-parameter.json",
  "title": "Tool Parameter",
  "type": "object",
  "description": "Enhanced parameter definition with type constraints",
  "properties": {
    "name": {
      "type": "string",
      "minLength": 1,
      "pattern": "^[a-zA-Z_][a-zA-Z0-9_]*$",
      "description": "Parameter name (valid identifier)"
    },
    "type": {
      "type": "string",
      "enum": ["string", "number", "integer", "boolean", "object", "array", "null"],
      "description": "JSON Schema type"
    },
    "description": {
      "type": "string",
      "minLength": 1,
      "description": "Human-readable description"
    },
    "required": {
      "type": "boolean",
      "default": false,
      "description": "Whether parameter is required"
    },
    "default": {
      "description": "Default value if parameter is omitted"
    },
    "format": {
      "type": "string",
      "description": "String format (email, uri, uuid, date-time, etc.)"
    },
    "pattern": {
      "type": "string",
      "description": "Regex pattern for string validation"
    },
    "minLength": {
      "type": "integer",
      "minimum": 0,
      "description": "Minimum string length"
    },
    "maxLength": {
      "type": "integer",
      "minimum": 0,
      "description": "Maximum string length"
    },
    "minimum": {
      "type": "number",
      "description": "Minimum numeric value (inclusive)"
    },
    "maximum": {
      "type": "number",
      "description": "Maximum numeric value (inclusive)"
    },
    "exclusiveMinimum": {
      "type": "number",
      "description": "Minimum numeric value (exclusive)"
    },
    "exclusiveMaximum": {
      "type": "number",
      "description": "Maximum numeric value (exclusive)"
    },
    "multipleOf": {
      "type": "number",
      "exclusiveMinimum": 0,
      "description": "Value must be multiple of this"
    },
    "enum": {
      "type": "array",
      "description": "Allowed values"
    },
    "items": {
      "description": "Schema for array items"
    },
    "minItems": {
      "type": "integer",
      "minimum": 0,
      "description": "Minimum array length"
    },
    "maxItems": {
      "type": "integer",
      "minimum": 0,
      "description": "Maximum array length"
    },
    "uniqueItems": {
      "type": "boolean",
      "default": false,
      "description": "Array items must be unique"
    },
    "properties": {
      "type": "object",
      "description": "Object property schemas"
    },
    "required": {
      "type": "array",
      "items": { "type": "string" },
      "description": "Required object properties"
    },
    "additionalProperties": {
      "description": "Allow additional object properties"
    },
    "anyOf": {
      "type": "array",
      "description": "Union type schemas"
    },
    "oneOf": {
      "type": "array",
      "description": "Exclusive type schemas"
    },
    "allOf": {
      "type": "array",
      "description": "Intersection type schemas"
    }
  },
  "required": ["name", "type", "description"]
}
```

---

## Best Practices

### 1. Use Semantic Types

Prefer semantic types over generic strings:
- ✅ Use `"format": "email"` for email addresses
- ✅ Use `"format": "uuid"` for identifiers
- ❌ Avoid plain `"type": "string"` without format

### 2. Set Reasonable Constraints

Always define boundaries:
- Set `minLength`/`maxLength` for strings
- Set `minimum`/`maximum` for numbers
- Set `minItems`/`maxItems` for arrays

### 3. Use Enums for Fixed Values

When values are from a fixed set:
```json
{
  "type": "string",
  "enum": ["pending", "active", "completed"]
}
```

### 4. Document with Examples

Include example values in descriptions:
```json
{
  "description": "Port number (e.g., 80, 443, 8080)"
}
```

### 5. Validate Early

Use JSON Schema validators during development:
```bash
# Python
jsonschema -i params.json schema.json

# Node.js
ajv validate -s schema.json -d params.json
```

### 6. Keep Backward Compatibility

When adding constraints to existing parameters:
- Ensure new constraints don't reject previously valid values
- Use `anyOf` to support multiple formats during migration
- Document breaking changes in change log

---

## Appendix A: Common Patterns

### Nullable Types

```json
{
  "anyOf": [
    { "type": "string", "format": "email" },
    { "type": "null" }
  ]
}
```

### Optional with Default

```json
{
  "type": "string",
  "enum": ["asc", "desc"],
  "default": "asc",
  "required": false
}
```

### Conditional Required

```json
{
  "type": "object",
  "properties": {
    "type": { "enum": ["email", "sms"] },
    "email": { "type": "string", "format": "email" },
    "phone": { "type": "string", "pattern": "^\\+?[1-9]\\d{1,14}$" }
  },
  "required": ["type"],
  "if": {
    "properties": { "type": { "const": "email" } }
  },
  "then": {
    "required": ["email"]
  },
  "else": {
    "required": ["phone"]
  }
}
```

### Recursive Types

```json
{
  "$defs": {
    "tree_node": {
      "type": "object",
      "properties": {
        "value": { "type": "string" },
        "children": {
          "type": "array",
          "items": { "$ref": "#/$defs/tree_node" }
        }
      }
    }
  }
}
```

---

## Appendix B: Type Quick Reference

| Use Case | Type Definition |
|----------|----------------|
| Email | `{"type": "string", "format": "email"}` |
| URL | `{"type": "string", "format": "uri"}` |
| UUID | `{"type": "string", "format": "uuid"}` |
| DateTime | `{"type": "string", "format": "date-time"}` |
| Positive Integer | `{"type": "integer", "exclusiveMinimum": 0}` |
| Percentage | `{"type": "number", "minimum": 0, "maximum": 100}` |
| Port | `{"type": "integer", "minimum": 1, "maximum": 65535}` |
| Non-empty String | `{"type": "string", "minLength": 1}` |
| String List | `{"type": "array", "items": {"type": "string"}}` |
| Enum | `{"type": "string", "enum": ["a", "b"]}` |
| Nullable | `{"anyOf": [{"type": "string"}, {"type": "null"}]}` |

---

## Version History

- **v1.5.0** (Current): Enhanced type system with constraints, formats, and compositions
- **v1.0.0**: Basic type support (string, number, boolean, object, array, null)

---

*This specification is part of the ADL (Agent Definition Language) project. For more information, visit https://github.com/nextmoca/adl*
