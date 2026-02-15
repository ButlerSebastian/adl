# ADL v1.0 to v1.5 Migration Guide

## Overview

Welcome to the ADL v1.5 migration guide! This document provides a comprehensive overview of the new features introduced in ADL v1.5 and guides you through the process of migrating your existing ADL v1.0 agent definitions to take advantage of these new capabilities.

### What's New in v1.5

ADL v1.5 introduces three major new features:

1. **Tool Category Taxonomy**: A standardized hierarchical system for organizing and discovering AI agent tools
2. **Enhanced Type System**: Comprehensive parameter constraints and validation using JSON Schema 2020-12
3. **Return Type System**: Structured return type definitions with 15 standard patterns

### Migration Timeline

- **Current Version**: v1.5.0 (February 15, 2026)
- **Backward Compatibility**: All v1.0 definitions remain valid in v1.5
- **Migration Status**: Optional but recommended for new features
- **Breaking Changes**: None - all new fields are optional

## Breaking Changes

### No Breaking Changes in v1.5

ADL v1.5 maintains full backward compatibility with v1.0. All existing agent definitions will continue to work without modification.

### Key Compatibility Points

- All new fields are **optional**
- Existing simple type definitions remain valid
- No changes to core ADL structure
- Tools without new fields continue to function

### Backward Compatibility Guarantee

```json
{
  "name": "existing_agent",
  "tools": [{
    "name": "existing_tool",
    "parameters": [{
      "name": "param1",
      "type": "string",
      "description": "Simple parameter"
    }]
  }]
}
```

The above v1.0 definition is fully compatible with v1.5.

## New Features Overview

### 1. Tool Category Taxonomy

A hierarchical categorization system for tools following the pattern:
```
domain.category.subcategory.specific
```

**Benefits**:

- Improved tool discovery and organization
- Standardized categorization across platforms
- Governance and policy application
- Enhanced documentation

### 2. Enhanced Type System

Comprehensive parameter constraints and validation:

**String Constraints**: `minLength`, `maxLength`, `pattern`, `format`, `enum`

**Numeric Constraints**: `minimum`, `maximum`, `multipleOf`, `exclusiveMinimum/Maximum`

**Array Constraints**: `minItems`, `maxItems`, `uniqueItems`, `items`

**Object Constraints**: `properties`, `required`, `additionalProperties`

### 3. Return Type System

Structured return type definitions with 15 standard patterns:

**Structured**: `ObjectResult`, `EntityResult`, `OperationStatus`

**Primitive**: `StringValue`, `NumberValue`, `BooleanValue`, `IdentifierValue`

**Array**: `ListResult`, `BatchResult`

**Binary**: `FileResult`, `MediaResult`

**Stream**: `EventStream`, `ChunkedData`

**Void**: `VoidResult`

## Feature 1: Tool Category Taxonomy

### What is Tool Category Taxonomy?

The Tool Category Taxonomy provides a standardized, hierarchical system for organizing and discovering AI agent tools. It follows a Kubernetes-style pattern:

```
domain.category.subcategory.specific
```

### How to Add Category and Subcategory

**Before (v1.0)**:
```json
{
  "name": "generate_image",
  "category": "Image Generation"
}
```

**After (v1.5)**:
```json
{
  "name": "generate_image",
  "category": "ai_ml.image_generation.text_to_image",
  "subcategory": "dalle"
}
```

### Pattern Validation Rules

**Category ID Pattern**:
```json
{
  "type": "string",
  "pattern": "^[a-z_]+(?:\\.[a-z_]+){1,3}$",
  "description": "Valid category ID"
}
```

**Subcategory Pattern**:
```json
{
  "type": "string",
  "pattern": "^[a-z0-9_-]+$",
  "description": "Valid subcategory identifier"
}
```

### Available Domains and Categories

**Level 1: Domains** (14 available):

- `data_access`, `data_manipulation`, `computation`, `communication`, `file_operations`, `system`, `ai_ml`, `security`, `monitoring`, `testing`, `integration`, `ui_ux`, `workflow`, `content`

**Level 2: Categories** (examples):

- `data_access`: `database`, `api`, `storage`, `cache`, `search`, `stream`
- `ai_ml`: `llm`, `image_generation`, `text_analysis`, `classification`, `recommendation`, `embedding`
- `communication`: `email`, `sms`, `chat`, `notification`, `webhook`, `voice`

**Level 3: Subcategories** (examples):

- `data_access.database`: `query`, `insert`, `update`, `delete`, `schema`, `migration`
- `ai_ml.image_generation`: `text_to_image`, `image_to_image`, `inpainting`, `upscaling`, `style_transfer`

**Level 4: Specific** (examples):

- `data_access.database.query.sql`
- `ai_ml.image_generation.text_to_image.dalle`

### Migration Steps

1. **Audit Existing Tools**: List all tools with categories
2. **Map to Taxonomy**: Use closest matching category
3. **Update Definitions**: Replace free-form category with taxonomy ID
4. **Add Subcategories**: Add subcategory for specificity
5. **Test Validation**: Validate with updated schema

### Best Practices

1. **Use Appropriate Granularity**:
   - ✅ Use `data_access.database.query` for database queries
   - ✅ Use `ai_ml.image_generation.text_to_image` for image generation
   - ❌ Avoid overly specific categories

2. **Follow Naming Conventions**:
   - Use lowercase with underscores
   - Use descriptive, clear names
   - Avoid abbreviations
   - Use singular nouns

3. **Use Subcategories for Specificity**:
   ```json
   {
     "category": "ai_ml.image_generation.text_to_image",
     "subcategory": "dalle"
   }
   ```

4. **Document Custom Categories**:
   - Use `custom` domain temporarily
   - Document the use case
   - Submit RFC for official category addition

### Example Migration

**Customer Support Agent Example**:
```json
{
  "name": "lookup_order",
  "category": "data_access.database.query",
  "subcategory": "sql"
}
```

### Link to Full Taxonomy Specification

For complete details, see: [Tool Category Taxonomy Specification](./tool-category-taxonomy.md)

## Feature 2: Enhanced Type System

### What is the Enhanced Type System?

The Enhanced Type System extends basic parameter typing to support precise, expressive, and validated tool contracts using JSON Schema 2020-12 features.

### List of New Constraint Fields

**String Constraints**:

- `minLength`: Minimum string length
- `maxLength`: Maximum string length
- `pattern`: Regex pattern (ECMA-262)
- `format`: Predefined format (email, uri, uuid, etc.)
- `enum`: Allowed values

**Numeric Constraints**:

- `minimum`: Minimum value (inclusive)
- `maximum`: Maximum value (inclusive)
- `exclusiveMinimum`: Minimum value (exclusive)
- `exclusiveMaximum`: Maximum value (exclusive)
- `multipleOf`: Value must be multiple of

**Array Constraints**:

- `minItems`: Minimum number of items
- `maxItems`: Maximum number of items
- `uniqueItems`: All items must be unique
- `items`: Schema for all items
- `contains`: At least one item must match

**Object Constraints**:

- `properties`: Defined property schemas
- `required`: Required property names
- `additionalProperties`: Allow extra properties
- `patternProperties`: Regex-based property schemas
- `propertyNames`: Schema for property names
- `minProperties`: Minimum property count
- `maxProperties`: Maximum property count

### Before/After Examples

#### String Constraints

**Before (v1.0)**:
```json
{
  "name": "email",
  "type": "string",
  "description": "User email address"
}
```

**After (v1.5)**:
```json
{
  "name": "email",
  "type": "string",
  "format": "email",
  "description": "User email address"
}
```

#### Numeric Constraints

**Before**:
```json
{
  "name": "limit",
  "type": "number",
  "description": "Maximum results"
}
```

**After**:
```json
{
  "name": "limit",
  "type": "integer",
  "minimum": 1,
  "maximum": 1000,
  "description": "Maximum results"
}
```

#### Array Constraints

**Before**:
```json
{
  "name": "tags",
  "type": "array",
  "description": "List of tags"
}
```

**After**:
```json
{
  "name": "tags",
  "type": "array",
  "items": {
    "type": "string",
    "minLength": 1,
    "maxLength": 50
  },
  "maxItems": 20,
  "uniqueItems": true,
  "description": "List of tags"
}
```

#### Object Constraints

**Before**:
```json
{
  "name": "user",
  "type": "object",
  "description": "User information"
}
```

**After**:
```json
{
  "name": "user",
  "type": "object",
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
    }
  },
  "required": ["id", "name", "email"],
  "description": "User information"
}
```

### Migration Steps

1. **Review String Parameters**: Add `format`, `minLength`, `maxLength`, `pattern`
2. **Review Numeric Parameters**: Add `minimum`, `maximum`, `multipleOf`
3. **Review Array Parameters**: Add `items`, `minItems`, `maxItems`, `uniqueItems`
4. **Review Object Parameters**: Add `properties`, `required`, `additionalProperties`
5. **Add Enums**: For parameters with fixed value sets
6. **Test Validation**: Use JSON Schema validators

### Best Practices

1. **Use Semantic Types**:
   - ✅ Use `"format": "email"` for email addresses
   - ✅ Use `"format": "uuid"` for identifiers
   - ❌ Avoid plain `"type": "string"` without format

2. **Set Reasonable Constraints**:
   - Set `minLength`/`maxLength` for strings
   - Set `minimum`/`maximum` for numbers
   - Set `minItems`/`maxItems` for arrays

3. **Use Enums for Fixed Values**:
   ```json
   {
     "type": "string",
     "enum": ["pending", "active", "completed"]
   }
   ```

4. **Document with Examples**:
   ```json
   {
     "description": "Port number (e.g., 80, 443, 8080)"
   }
   ```

### Link to Full Type System Specification

For complete details, see: [Enhanced Type System Specification](./enhanced-type-system.md)

## Feature 3: Return Type System

### What is the Return Type System?

The Return Type System provides a standardized, extensible framework for defining tool output schemas in ADL. It enables tool output validation, self-documenting contracts, and interoperability.

### List of 15 Return Type Categories

**Structured**:

1. `ObjectResult`: Generic object with success/error wrapper
2. `EntityResult`: Single entity with type discriminator
3. `OperationStatus`: Async operation status tracking

**Primitive**:

4. `StringValue`: Simple string return
5. `NumberValue`: Numeric return
6. `BooleanValue`: True/false return
7. `IdentifierValue`: Unique identifier return

**Array**:

8. `ListResult`: Generic list with pagination
9. `BatchResult`: Batch operation results with individual item status

**Binary**:

10. `FileResult`: File download with metadata
11. `MediaResult`: Media file (image, audio, video) with metadata

**Stream**:

12. `EventStream`: Server-sent events or WebSocket message format
13. `ChunkedData`: Chunked data transfer for large payloads

**Void**:

14. `VoidResult`: No return value, only status

### Before/After Example

**Before (v1.0)**:
```json
{
  "name": "get_user",
  "returns": {
    "type": "object",
    "description": "Returns user data"
  }
}
```

**After (v1.5)**:
```json
{
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
}
```

### How to Add Schema, Examples, and Content Type

**Complete Return Type Definition**:
```json
{
  "returns": {
    "type": "MediaResult",
    "schema": {
      "$ref": "#/$defs/StandardReturnTypes/MediaResult"
    },
    "description": "Returns generated image with metadata",
    "examples": [{
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
    }],
    "content_type": "application/json"
  }
}
```

### Migration Steps

1. **Identify Current Return Types**: Review all tools with `returns` field
2. **Map to New Types**: Use the selection matrix to choose appropriate types
3. **Add Schema References**: Replace simple type strings with schema references
4. **Add Examples**: Include at least one example for each return type
5. **Validate**: Use ADL validator to check new definitions

### Best Practices

1. **Always Include Success Flag**: Use `success` boolean for clear status indication
2. **Provide Examples**: Include realistic examples for documentation
3. **Use Standard Types**: Prefer standard types over custom schemas
4. **Handle Errors Consistently**: Use standard error structure
5. **Document Content Types**: Specify when returning non-JSON data

### Link to Full Return Type Specification

For complete details, see: [Return Type System Specification](./return-type-system.md)

## Migration Steps

### Step-by-Step Guide for Migrating Existing Agents

1. **Backup Your Definitions**: Always create backups before migration
2. **Review Documentation**: Read this guide and linked specifications
3. **Audit Existing Agents**: Identify all agents that could benefit from new features
4. **Prioritize Migration**: Start with most frequently used agents
5. **Update Tool Categories**: Add taxonomy categories and subcategories
6. **Enhance Parameter Types**: Add constraints and validation
7. **Define Return Types**: Add structured return type definitions
8. **Add Examples**: Include examples for parameters and returns
9. **Validate**: Use ADL validation tools to check your changes
10. **Test**: Test migrated agents in development environment
11. **Deploy**: Roll out changes to production

### Optional vs Recommended Changes

**Optional Changes**:

- Adding categories and subcategories
- Adding parameter constraints
- Adding return type definitions
- Adding examples

**Recommended Changes**:

- Add categories for better tool discovery
- Add parameter constraints for validation
- Add return types for documentation
- Add examples for clarity

### Validation Steps

1. **Use ADL Validator**:

   ```bash
   python tools/validate.py your_agent.json
   ```

2. **Check for Errors**: Address any validation errors
3. **Test in Development**: Verify agent behavior
4. **Review Examples**: Ensure examples are realistic

## Best Practices

### When to Use Each New Feature

**Tool Category Taxonomy**:

- Use when you have many tools and need better organization
- Use when you need to apply policies based on tool categories
- Use when you want to improve tool discovery

**Enhanced Type System**:

- Use when you need parameter validation
- Use when you want to prevent runtime errors
- Use when you need to document valid parameter ranges

**Return Type System**:

- Use when you need to validate tool outputs
- Use when you want self-documenting tool contracts
- Use when you need consistent return patterns

### Common Patterns

**Pattern 1: Simple Tool with Category**:
```json
{
  "name": "send_email",
  "category": "communication.email",
  "parameters": [{
    "name": "to",
    "type": "string",
    "format": "email"
  }]
}
```

**Pattern 2: Tool with Constraints**:
```json
{
  "name": "search",
  "parameters": [{
    "name": "query",
    "type": "string",
    "minLength": 1,
    "maxLength": 500
  }]
}
```

**Pattern 3: Tool with Return Type**:
```json
{
  "name": "get_user",
  "returns": {
    "type": "EntityResult",
    "schema": {
      "$ref": "#/$defs/StandardReturnTypes/EntityResult"
    }
  }
}
```

### Tips for Smooth Migration

1. **Start Small**: Migrate one agent at a time
2. **Test Thoroughly**: Validate and test each change
3. **Document Changes**: Keep track of what you've migrated
4. **Use Examples**: Include examples for clarity
5. **Follow Best Practices**: Use the patterns and conventions in this guide

## Troubleshooting

### Common Issues and Solutions

**Issue 1: Validation Error on Category Pattern**

```
Error: Category ID does not match pattern
```

**Solution**: Use lowercase with underscores and proper hierarchy:

```json
{
  "category": "ai_ml.image_generation.text_to_image"
}
```

**Issue 2: Parameter Constraint Validation Failure**

```
Error: Value does not match format 'email'
```

**Solution**: Ensure parameter values match the format:

```json
{
  "name": "email",
  "type": "string",
  "format": "email"
}
```

**Issue 3: Missing Required Field in Return Type**

```
Error: Missing required field 'success'
```

**Solution**: Include all required fields:

```json
{
  "returns": {
    "type": "ObjectResult",
    "schema": {
      "$ref": "#/$defs/StandardReturnTypes/ObjectResult"
    }
  }
}
```

### Validation Errors

**Common Validation Errors**:

- Pattern mismatch for category IDs
- Format validation failures (email, uuid, etc.)
- Missing required fields
- Type mismatches

**How to Fix**:

1. Check the error message
2. Review the specification
3. Update your definition
4. Re-validate

### Pattern Matching Issues

**Issue**: Category ID doesn't match pattern

**Solution**: Use the correct pattern:

```json
{
  "type": "string",
  "pattern": "^[a-z_]+(?:\\.[a-z_]+){1,3}$"
}
```

## Resources

### Links to All Specification Documents

- [Tool Category Taxonomy Specification](./tool-category-taxonomy.md)
- [Enhanced Type System Specification](./enhanced-type-system.md)
- [Return Type System Specification](./return-type-system.md)
- [ADL Schema Reference](../schema/adl.schema.json)

### Links to Example Files

- [Creative Producer Agent Example](../examples/creative_producer_agent.json)
- [Customer Support Agent Example](../examples/customer_support_agent.json)
- [Product Advisor Agent Example](../examples/product_advisor_agent.json)

### Links to Validation Tools

- ADL Validator: `python tools/validate.py your_agent.json`
- JSON Schema Validator: `jsonschema -i params.json schema.json`
- Node.js Validator: `ajv validate -s schema.json -d params.json`

### Additional Resources

- [ADL GitHub Repository](https://github.com/nextmoca/adl)
- [ADL Documentation](../README.md)
- [ADL Roadmap](../ROADMAP.md)
- [ADL Governance](../GOVERNANCE.md)

## Conclusion

Migrating to ADL v1.5 provides significant benefits including better tool organization, enhanced validation, and improved documentation. While migration is optional, it's highly recommended to take advantage of these new features.

### Summary of Changes

1. **Tool Category Taxonomy**: Standardized hierarchical categorization
2. **Enhanced Type System**: Comprehensive parameter constraints
3. **Return Type System**: Structured return type definitions

### Next Steps

1. Review this migration guide
2. Read the linked specification documents
3. Start migrating your agents
4. Validate and test your changes
5. Deploy to production

### Need Help?

For questions or issues, visit: [ADL GitHub Issues](https://github.com/nextmoca/adl/issues)

Happy migrating! 🚀
