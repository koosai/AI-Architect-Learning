import fs from 'fs';
import path from 'path';

const errs = JSON.parse(fs.readFileSync('mermaid_errors.json', 'utf-8'));

for (let i = 0; i < errs.length; i++) {
  const item = errs[i];
  console.log(`\n=== [${i}] ${path.basename(item.file)} (Line ${item.startLine}) ===`);
  console.log('Error:', item.error.split('\n')[0]);
  console.log(item.code);
}
