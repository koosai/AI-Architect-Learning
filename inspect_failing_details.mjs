import fs from 'fs';
import path from 'path';

const errs = JSON.parse(fs.readFileSync('mermaid_errors.json', 'utf-8'));
console.log(`Total failing: ${errs.length}`);

const byReason = {};
for (const e of errs) {
  const firstErr = e.error.split('\n')[0];
  byReason[firstErr] = (byReason[firstErr] || 0) + 1;
}

console.log('\n--- Failure Reasons Breakdown ---');
for (const [reason, count] of Object.entries(byReason)) {
  console.log(`${count}x : ${reason}`);
}

console.log('\n--- First 15 Failing Diagrams ---');
errs.slice(0, 15).forEach((e, i) => {
  console.log(`\n[${i + 1}] File: ${path.basename(e.file)} (Line ${e.startLine})`);
  console.log(`Error: ${e.error.split('\n')[0]}`);
  console.log('Code snippet:');
  console.log(e.code.split('\n').slice(0, 12).join('\n'));
});
