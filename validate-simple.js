#!/usr/bin/env node

const fs = require('fs');
const path = require('path');

// Simple validation: check if JSON is valid and has required fields
function validateAgentFile(filePath) {
  try {
    const content = fs.readFileSync(filePath, 'utf8');
    const agent = JSON.parse(content);
    
    const required = ['name', 'description', 'role', 'llm', 'llm_settings', 'tools'];
    const missing = required.filter(field => !agent[field]);
    
    if (missing.length > 0) {
      return { valid: false, errors: [`Missing required fields: ${missing.join(', ')}`] };
    }
    
    return { valid: true };
  } catch (error) {
    return { valid: false, errors: [error.message] };
  }
}

// Validate all examples
const examplesDir = path.join(__dirname, 'examples');
const exampleFiles = fs.readdirSync(examplesDir).filter(f => f.endsWith('.json'));

console.log("Validating examples...\n");

let allValid = true;

for (const file of exampleFiles) {
  const examplePath = path.join(examplesDir, file);
  const result = validateAgentFile(examplePath);
  
  if (result.valid) {
    console.log(`✅ ${file} is valid`);
  } else {
    console.log(`❌ ${file} is invalid: ${result.errors.join(', ')}`);
    allValid = false;
  }
}

console.log("\n" + (allValid ? "✅ All examples are valid!" : "❌ Some examples are invalid."));
process.exit(allValid ? 0 : 1);