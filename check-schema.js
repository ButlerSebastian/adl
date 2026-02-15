const fs = require('fs');
const path = require('path');

const schemaPath = path.join(__dirname, 'schema', 'agent-definition.schema.json');
const schema = JSON.parse(fs.readFileSync(schemaPath, 'utf8'));

console.log("Schema structure:");
console.log("$schema:", schema.$schema);
console.log("$id:", schema.$id);
console.log("title:", schema.title);
console.log("type:", schema.type);
console.log("\nProperties count:", Object.keys(schema.properties).length);
console.log("\n$defs count:", Object.keys(schema.$defs).length);

// Check if $defs have inline definitions or $refs
console.log("\n$defs entries:");
for (const [key, value] of Object.entries(schema.$defs)) {
  console.log(`  ${key}:`, value.$ref ? `$ref: ${value.$ref}` : 'inline definition');
}

// Check if component files exist
console.log("\nComponent files:");
const componentFiles = [
  './components/rag/index.json',
  './components/tool/definition.json',
  './components/tool/parameter.json',
  './components/common/key-schema.json',
  './components/memory/definition.json'
];

for (const file of componentFiles) {
  const fullPath = path.join(__dirname, 'schema', file);
  const exists = fs.existsSync(fullPath);
  console.log(`  ${file}: ${exists ? 'exists' : 'missing'}`);
}