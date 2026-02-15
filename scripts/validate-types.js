#!/usr/bin/env node

/**
 * Type validation script for ADL
 * 
 * This script validates that the TypeScript type definitions
 * are consistent with the JSON Schema.
 */

const fs = require('fs');
const path = require('path');

// Read the schema
const schemaPath = path.join(__dirname, '../schema/agent-definition.schema.json');
const schema = JSON.parse(fs.readFileSync(schemaPath, 'utf8'));

// Read the TypeScript definitions
const tsPath = path.join(__dirname, '../types/agent-definition.d.ts');
const tsContent = fs.readFileSync(tsPath, 'utf8');

console.log('🔍 Validating ADL Type Definitions...\n');

// Check for required fields in schema
const requiredFields = schema.required || [];
console.log(`📋 Required fields in schema: ${requiredFields.join(', ')}`);

// Extract TypeScript interface definitions
const interfaceRegex = /export interface (\w+) \{([^}]+)\}/g;
const interfaces = {};
let match;

while ((match = interfaceRegex.exec(tsContent)) !== null) {
  const interfaceName = match[1];
  const interfaceBody = match[2];
  interfaces[interfaceName] = interfaceBody;
}

console.log(`\n📋 Found ${Object.keys(interfaces).length} TypeScript interfaces:`);
Object.keys(interfaces).forEach(name => {
  console.log(`  - ${name}`);
});

// Validate that the main AgentDefinition interface matches schema properties
console.log('\n🔬 Validating AgentDefinition interface...');
if (interfaces.AgentDefinition) {
  const agentProps = schema.properties;
  const tsProps = interfaces.AgentDefinition.split(';').map(p => p.trim()).filter(p => p);
  
  console.log(`Schema has ${Object.keys(agentProps).length} properties`);
  console.log(`TypeScript has ${tsProps.length} properties`);
  
  // Check for missing required properties
  const missingRequired = requiredFields.filter(field => {
    const propMatch = tsProps.find(p => p.startsWith(field + ':'));
    return !propMatch;
  });
  
  if (missingRequired.length > 0) {
    console.log(`❌ Missing required properties: ${missingRequired.join(', ')}`);
  } else {
    console.log('✅ All required properties are present');
  }
}

// Check TypeScript compilation
console.log('\n🔧 Checking TypeScript compilation...');
const { execSync } = require('child_process');

try {
  const result = execSync('npx tsc --noEmit types/agent-definition.d.ts', { encoding: 'utf8' });
  console.log('✅ TypeScript compilation successful');
} catch (error) {
  console.log('❌ TypeScript compilation failed:');
  console.log(error.stdout);
}

console.log('\n✅ Type validation complete!');