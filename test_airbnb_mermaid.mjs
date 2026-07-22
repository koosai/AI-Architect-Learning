import fs from 'fs';
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

const content = fs.readFileSync('c:/Users/K.K/OneDrive/Desktop/AI架构师教程/docs/atlas/airbnb.mdx', 'utf-8');
const lines = content.split('\n');

let inMermaid = false;
let mermaidLines = [];
let blockStart = 0;

for (let i = 0; i < lines.length; i++) {
  const line = lines[i];
  if (line.trim().startsWith('```mermaid')) {
    inMermaid = true;
    mermaidLines = [];
    blockStart = i + 1;
    continue;
  }
  if (inMermaid && line.trim().startsWith('```')) {
    inMermaid = false;
    const code = mermaidLines.join('\n');
    console.log(`\n=== Testing Diagram at Line ${blockStart} ===`);
    try {
      await mermaid.parse(code);
      console.log('PASSED!');
    } catch (e) {
      console.log('FAILING! Error:', e.message);
      console.log(code);
    }
    continue;
  }
  if (inMermaid) {
    mermaidLines.push(line);
  }
}
