const fs = require('fs');
const path = require('path');

const schemaDir = path.join(__dirname, 'schema');
const componentsDir = path.join(schemaDir, 'components');

// Function to extract $refs from a JSON schema
function extractRefs(schema, filePath) {
  const refs = [];
  
  function traverse(obj) {
    if (obj && typeof obj === 'object') {
      if (obj.$ref) {
        refs.push(obj.$ref);
      }
      for (const key in obj) {
        traverse(obj[key]);
      }
    }
  }
  
  traverse(schema);
  return refs;
}

// Function to resolve $ref paths relative to a file
function resolveRef(ref, baseFile) {
  if (ref.startsWith('#/')) {
    // Internal reference, not a file reference
    return null;
  }
  
  const baseDir = path.dirname(baseFile);
  const resolvedPath = path.resolve(baseDir, ref);
  
  // Check if the resolved path exists
  if (fs.existsSync(resolvedPath)) {
    return resolvedPath;
  }
  
  return null;
}

// Build dependency graph
const graph = {};

function addToGraph(filePath) {
  const content = fs.readFileSync(filePath, 'utf8');
  const schema = JSON.parse(content);
  const refs = extractRefs(schema, filePath);
  
  graph[filePath] = [];
  
  for (const ref of refs) {
    const resolved = resolveRef(ref, filePath);
    if (resolved) {
      graph[filePath].push(resolved);
    }
  }
}

// Find all component files
const componentFiles = [];
function findComponentFiles(dir) {
  const files = fs.readdirSync(dir);
  for (const file of files) {
    const filePath = path.join(dir, file);
    const stat = fs.statSync(filePath);
    if (stat.isDirectory()) {
      findComponentFiles(filePath);
    } else if (file.endsWith('.json')) {
      componentFiles.push(filePath);
    }
  }
}

findComponentFiles(componentsDir);

// Add main schema to graph
const mainSchemaPath = path.join(schemaDir, 'agent-definition.schema.json');
componentFiles.push(mainSchemaPath);

// Build graph
for (const file of componentFiles) {
  addToGraph(file);
}

// Check for circular dependencies
function hasCycle(graph) {
  const visited = {};
  const recStack = {};
  
  function dfs(node) {
    if (!visited[node]) {
      visited[node] = true;
      recStack[node] = true;
      
      for (const neighbor of graph[node] || []) {
        if (!visited[neighbor] && dfs(neighbor)) {
          return true;
        } else if (recStack[neighbor]) {
          return true;
        }
      }
    }
    
    recStack[node] = false;
    return false;
  }
  
  for (const node in graph) {
    if (dfs(node)) {
      return true;
    }
  }
  
  return false;
}

console.log("Checking for circular dependencies...");
console.log("Component files:", componentFiles.map(f => path.relative(__dirname, f)));

if (hasCycle(graph)) {
  console.log("❌ Circular dependencies found!");
  process.exit(1);
} else {
  console.log("✅ No circular dependencies found.");
  process.exit(0);
}