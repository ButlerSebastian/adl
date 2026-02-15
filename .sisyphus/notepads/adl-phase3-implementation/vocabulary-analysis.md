# Schema Modularization - Technical Analysis

## The Vocabulary Problem

JSON Schema 2020-12 uses a vocabulary system that defines which keywords are valid. When we tried to use external `$ref`, the validation tools couldn't resolve the meta-schema because:

1. **Vocabulary References**: The schema references `https://json-schema.org/draft/2020-12/vocab/*` URIs
2. **Network Dependency**: These require network access or local caching
3. **Tool Limitations**: Current validation tools (ajv, jsonschema) have poor support for external $ref with custom vocabularies
4. **Memory Issues**: Node.js ran out of memory trying to compile the modular schema

## Why DSL Approach Makes Sense

Instead of fighting JSON Schema's limitations, we could use a **Domain-Specific Language (DSL)** approach:

### Benefits of DSL for ADL

1. **Custom Validation**: Build a validator that understands ADL's specific structure
2. **Simpler Syntax**: Define ADL in a more readable format
3. **Better Error Messages**: Provide domain-specific error messages
4. **No External Dependencies**: Self-contained validation
5. **Easier Extension**: Add ADL-specific features without JSON Schema constraints

### DSL Options

1. **Custom JSON Format**: Keep JSON but with ADL-specific validation
2. **YAML Format**: More readable than JSON
3. **Custom Syntax**: Create a new syntax specifically for ADL
4. **TypeScript/JavaScript**: Use TypeScript as the definition language

## Current Decision

For Phase 3, we're taking a **hybrid approach**:

1. **Keep JSON Schema**: Maintain compatibility with existing tools
2. **Document Components**: Component files serve as documentation
3. **TypeScript Definitions**: Provide type safety via `types/agent-definition.d.ts`
4. **Custom Validation Scripts**: Build ADL-specific validation tools

## Future Considerations

For ADL v3 or beyond, consider:

1. **Full DSL Migration**: Move to a custom DSL
2. **Code Generation**: Generate validators from TypeScript definitions
3. **Schema-less Validation**: Use runtime validation instead of schema validation
4. **Custom Meta-Schema**: Create ADL-specific meta-schema

## Evidence of Vocabulary Issues

```bash
# Error when trying to validate modular schema
Error: no schema with key or ref "https://json-schema.org/draft/2020-12/schema"

# Memory error when compiling
FATAL ERROR: Ineffective mark-compacts near heap limit
Allocation failed - JavaScript heap out of memory
```

## Conclusion

The vocabulary system in JSON Schema 2020-12 is the root cause of modularization issues. A DSL approach would be more appropriate for ADL's needs, but for now, we're maintaining compatibility while documenting the modular structure.
