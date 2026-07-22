import fs from 'fs';
import path from 'path';

const docsDir = 'c:/Users/K.K/OneDrive/Desktop/AI架构师教程/docs';
const erpPath = path.join(docsDir, '06-cloud-enterprise-industrial', 'enterprise-erp-integration.mdx');

const fileLines = fs.readFileSync(erpPath, 'utf-8').split('\n');

for (let i = 0; i < fileLines.length; i++) {
  if (fileLines[i].trim().startsWith('```mermaid')) {
    console.log(`\n=== Mermaid Block at Line ${i+1} ===`);
    for (let j = i + 1; j < fileLines.length; j++) {
      if (fileLines[j].trim().startsWith('```')) break;
      console.log(`${j+1}: ${fileLines[j]}`);
    }
  }
}
