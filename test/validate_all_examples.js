const fs = require('fs');
const path = require('path');
const Ajv = require('ajv');
const addFormats = require('ajv-formats');

const ajv = new Ajv({ 
  allErrors: true,
  loadSchema: async (uri) => {
    const filePath = path.resolve(__dirname, uri.replace('https://example.com/schemas/', 'schema/'));
    try {
      const content = fs.readFileSync(filePath, 'utf8');
      return JSON.parse(content);
    } catch (error) {
      console.error(`Error loading schema ${uri}: ${error.message}`);
      throw error;
    }
  }
});
addFormats(ajv);

async function validateAllExamples() {
  const schemaPath = path.join(__dirname, 'schema', 'agent-definition.schema.json');
  const examplesDir = path.join(__dirname, 'examples');
  
  console.log('Loading schema...');
  const schema = JSON.parse(fs.readFileSync(schemaPath, 'utf8'));
  
  console.log('Compiling schema...');
  const validate = await ajv.compileAsync(schema);
  
  const exampleFiles = fs.readdirSync(examplesDir).filter(file => file.endsWith('.json'));
  
  console.log(`\nValidating ${exampleFiles.length} examples...\n`);
  
  let allValid = true;
  for (const file of exampleFiles) {
    const examplePath = path.join(examplesDir, file);
    const example = JSON.parse(fs.readFileSync(examplePath, 'utf8'));
    
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
}

validateAllExamples().catch(error => {
  console.error('Validation error:', error);
  process.exit(1);
});