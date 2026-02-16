const fs = require('fs');
const path = require('path');
const Ajv = require('ajv');
const addFormats = require('ajv-formats');

const ajv = new Ajv({ allErrors: true });
addFormats(ajv);

const schemaPath = path.join(__dirname, 'schema', 'agent-definition.schema.json');
const schema = JSON.parse(fs.readFileSync(schemaPath, 'utf8'));

const examplesDir = path.join(__dirname, 'examples');
const exampleFiles = fs.readdirSync(examplesDir).filter(file => file.endsWith('.json'));

console.log('Testing validation of all examples...\n');

let allValid = true;
for (const file of exampleFiles) {
  const examplePath = path.join(examplesDir, file);
  const example = JSON.parse(fs.readFileSync(examplePath, 'utf8'));
  
  const validate = ajv.compile(schema);
  const valid = validate(example);
  
  if (valid) {
    console.log(`✅ ${file} is valid`);
  } else {
    console.log(`❌ ${file} is NOT valid:`);
    console.log(validate.errors);
    allValid = false;
  }
}

console.log('\n' + (allValid ? '✅ All examples are valid!' : '❌ Some examples are invalid.'));

if (!allValid) {
  process.exit(1);
}