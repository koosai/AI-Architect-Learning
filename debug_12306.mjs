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

const errs = JSON.parse(fs.readFileSync('mermaid_errors.json', 'utf-8'));
const item = errs.find(e => e.file.includes('12306'));

let lines = item.code.split('\n');
const fixedLines = [];

for (let l of lines) {
  let line = l.replace('\r', '');
  const st = line.trim();
  if (st && !st.startsWith('mindmap') && !st.startsWith('root')) {
    const indent = line.match(/^\s*/)[0];
    let txt = st.replace(/^["'\[]+|["'\]]+$/g, '').replace(/"/g, "'");
    if (txt.includes('(') || txt.includes(')') || txt.includes('/') || txt.includes(':')) {
      txt = `["${txt}"]`;
    }
    line = `${indent}${txt}`;
  }
  fixedLines.push(line);
}

const fixedCode = fixedLines.join('\n');

console.log('=== TEST FIXED CODE ===');
console.log(fixedCode);

try {
  await mermaid.parse(fixedCode);
  console.log('\nPASSED 100%!');
} catch (e) {
  console.log('\nERROR MESSAGE:', e.message);
}
