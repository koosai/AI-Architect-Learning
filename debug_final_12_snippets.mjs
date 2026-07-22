import fs from 'fs';
import path from 'path';
import { JSDOM } from 'jsdom';

const dom = new JSDOM('<!DOCTYPE html><html><body><div id="graphDiv"></div></body></html>', { url: 'http://localhost/' });
globalThis.window = dom.window;
globalThis.document = dom.window.document;
globalThis.location = dom.window.location;
globalThis.Option = dom.window.Option;
globalThis.Image = dom.window.Image;

const mermaidModule = await import('mermaid');
const mermaid = mermaidModule.default;
mermaid.initialize({ startOnLoad: false, securityLevel: 'loose' });

const names = [
  'scaling-strategies',
  'replication',
  'autoscaling-rollout',
  'enterprise-erp-integration',
  'advanced-rag',
  'cdn',
  'elasticsearch',
  'gitlab-ci',
  'kafka',
  'npm',
  'postgresql',
  'sqlite'
];

const errs = JSON.parse(fs.readFileSync('mermaid_errors.json', 'utf-8'));

for (const name of names) {
  const item = errs.find(e => e.file.includes(name));
  if (!item) continue;

  const filePath = item.file;
  if (!fs.existsSync(filePath)) continue;

  const fileLines = fs.readFileSync(filePath, 'utf-8').split('\n');
  let blockStart = -1;
  let codeLines = [];

  for (let i = Math.max(0, item.startLine - 5); i < Math.min(fileLines.length, item.startLine + 5); i++) {
    if (fileLines[i].trim().startsWith('```mermaid')) {
      blockStart = i;
      for (let j = i + 1; j < fileLines.length; j++) {
        if (fileLines[j].trim().startsWith('```')) break;
        codeLines.push(fileLines[j]);
      }
      break;
    }
  }

  if (blockStart === -1) continue;

  const code = codeLines.join('\n');
  console.log(`\n=== ${name} (Line ${item.startLine}) ===`);
  try {
    await mermaid.parse(code);
    console.log('PASSED!');
  } catch (e) {
    console.log('Error:', e.message.split('\n')[0]);
    console.log(code);
  }
}
