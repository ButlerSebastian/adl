#!/usr/bin/env node

const fs = require('fs');
const path = require('path');
const Ajv = require('ajv');
const addFormats = require('ajv-formats');

const ajv = new Ajv({ strict: false });
addFormats(ajv);
const schemaPath = path.join(__dirname, 'schema', 'agent-definition.schema.json');
const schema = JSON.parse(fs.readFileSync(schemaPath, 'utf8'));
const validate = ajv.compile(schema);

const examplesDir = path.join(__dirname, 'examples');
const exampleFiles = fs.readdirSync(examplesDir).filter(f => f.endsWith('.json'));

let allValid = true;

console.log("Validating examples against schema...\n");

for (const file of exampleFiles) {
  const examplePath = path.join(examplesDir, file);
  const example = JSON.parse(fs.readFileSync(examplePath, 'utf8'));
  
  const isValid = validate(example);
  
  if (isValid) {
    console.log(`✅ ${file} is valid`);
  } else {
    console.log(`❌ ${file} is invalid:`);
    console.log(validate.errors);
    allValid = false;
  }
}

console.log("\n" + (allValid ? "✅ All examples are valid!" : "❌ Some examples are invalid."));
process.exit(allValid ? 0 : 1);