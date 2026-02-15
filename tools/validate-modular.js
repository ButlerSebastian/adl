const fs = require("fs");
const path = require("path");
const Ajv = require("ajv");
const addFormats = require("ajv-formats");

const ROOT = path.resolve(__dirname, "..");
const schemaPath = path.join(ROOT, "schema", "agent-definition.schema.json");

if (process.argv.length !== 3) {
  console.error("Usage: node tools/validate-modular.js <path-to-agent-json>");
  process.exit(1);
}

const agentPath = path.resolve(process.argv[2]);
const schema = JSON.parse(fs.readFileSync(schemaPath, "utf8"));
const instance = JSON.parse(fs.readFileSync(agentPath, "utf8"));

const ajv = new Ajv({
  allErrors: true,
  loadSchema: async (uri) => {
    if (uri === 'https://json-schema.org/draft/2020-12/schema') {
      return {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "$id": "https://json-schema.org/draft/2020-12/schema",
        "$vocabulary": {
          "https://json-schema.org/draft/2020-12/vocab/core": true,
          "https://json-schema.org/draft/2020-12/vocab/applicator": true,
          "https://json-schema.org/draft/2020-12/vocab/unevaluated": true,
          "https://json-schema.org/draft/2020-12/vocab/validation": true,
          "https://json-schema.org/draft/2020-12/vocab/meta-data": true,
          "https://json-schema.org/draft/2020-12/vocab/format-annotation": true,
          "https://json-schema.org/draft/2020-12/vocab/content": true
        },
        "$dynamicAnchor": "meta"
      };
    }
    if (uri.startsWith('file://')) {
      const filePath = uri.replace('file://', '');
      return JSON.parse(fs.readFileSync(filePath, 'utf8'));
    }
    if (uri.startsWith('./')) {
      const filePath = path.join(path.dirname(schemaPath), uri);
      return JSON.parse(fs.readFileSync(filePath, 'utf8'));
    }
    throw new Error(`Cannot load schema: ${uri}`);
  }
});
addFormats(ajv);

ajv.compileAsync(schema).then(validate => {
  const valid = validate(instance);
  if (!valid) {
    console.error(`❌ ${agentPath} is NOT valid:`);
    console.error(validate.errors);
    process.exit(1);
  } else {
    console.log(`✅ ${agentPath} is valid against agent-definition.schema.json`);
  }
}).catch(err => {
  console.error(`Error compiling schema: ${err.message}`);
  process.exit(1);
});
