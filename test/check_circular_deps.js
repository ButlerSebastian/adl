const fs = require('fs');
const path = require('path');

function findRefs(filePath, visited = new Set(), pathStack = []) {
  if (visited.has(filePath)) {
    console.log(`❌ Circular dependency detected:`);
    console.log(`   ${pathStack.join(' -> ')} -> ${filePath}`);
    return true;
  }

  visited.add(filePath);
  pathStack.push(filePath);

  try {
    const content = fs.readFileSync(filePath, 'utf8');
    const data = JSON.parse(content);

    function traverse(obj) {
      if (!obj || typeof obj !== 'object') return false;

      if (obj.$ref && typeof obj.$ref === 'string') {
        const refPath = path.resolve(path.dirname(filePath), obj.$ref);
        if (findRefs(refPath, new Set(visited), [...pathStack])) {
          return true;
        }
      }

      for (const key in obj) {
        if (obj.hasOwnProperty(key)) {
          if (traverse(obj[key])) return true;
        }
      }
      return false;
    }

    if (traverse(data)) return true;

  } catch (error) {
    console.log(`⚠️ Error reading ${filePath}: ${error.message}`);
  }

  visited.delete(filePath);
  pathStack.pop();
  return false;
}

const mainSchemaPath = path.join(__dirname, 'schema', 'agent-definition.schema.json');
console.log('Checking for circular dependencies...\n');

const hasCircularDeps = findRefs(mainSchemaPath);

if (!hasCircularDeps) {
  console.log('✅ No circular dependencies detected.');
} else {
  console.log('\n❌ Circular dependencies found.');
  process.exit(1);
}