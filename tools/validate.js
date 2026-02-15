#!/usr/bin/env node
const fs = require("fs");
const path = require("path");
const Ajv = require("ajv");
const addFormats = require("ajv-formats");

const ROOT = path.resolve(__dirname, "..");
const schemaPath = path.join(ROOT, "schema", "agent-definition.schema.json");

if (process.argv.length !== 3) {
  console.error("Usage: node tools/validate.js <path-to-agent-json>");
  process.exit(1);
}

const agentPath = path.resolve(process.argv[2]);
const schema = JSON.parse(fs.readFileSync(schemaPath, "utf8"));
const instance = JSON.parse(fs.readFileSync(agentPath, "utf8"));

const ajv = new Ajv({ allErrors: true, strict: false });
addFormats(ajv);
const validate = ajv.compile(schema);
const valid = validate(instance);

if (!valid) {
  console.error(`❌ ${agentPath} is NOT valid:`);
  console.error(validate.errors);
  process.exit(1);
} else {
  console.log(`✅ ${agentPath} is valid against agent-definition.schema.json`);
}
