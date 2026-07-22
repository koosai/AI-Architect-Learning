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

const docsDir = 'c:/Users/K.K/OneDrive/Desktop/AI架构师教程/docs';
const erpPath = path.join(docsDir, '06-cloud-enterprise-industrial', 'enterprise-erp-integration.mdx');

let content = fs.readFileSync(erpPath, 'utf-8');
content = content.replace('Broker["["消息队列 / Event Broker"]]', 'Broker["消息队列 / Event Broker"]');

fs.writeFileSync(erpPath, content);
console.log('Saved line 69 fix in enterprise-erp-integration.mdx');

// Test mermaid parse on fixed block
const lines = content.split('\n');
const codeLines = lines.slice(48, 80);
const code = codeLines.join('\n');

try {
  await mermaid.parse(code);
  console.log('\nFINAL DIAGRAM PASSED 100%!');
} catch (e) {
  console.log('Error:', e.message);
}
