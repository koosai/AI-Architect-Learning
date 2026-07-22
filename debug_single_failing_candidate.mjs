import fs from 'fs';
import path from 'path';
import { JSDOM } from 'jsdom';

const dom = new JSDOM('<!DOCTYPE html><html><body><div id="graphDiv"></div></body></html>', {
  url: 'http://localhost/',
});

globalThis.window = dom.window;
globalThis.document = dom.window.document;
globalThis.location = dom.window.location;
globalThis.Option = dom.window.Option;
globalThis.Image = dom.window.Image;

const mermaidModule = await import('mermaid');
const mermaid = mermaidModule.default;
mermaid.initialize({ startOnLoad: false, securityLevel: 'loose' });

const errs = JSON.parse(fs.readFileSync('mermaid_errors.json', 'utf-8'));
const item = errs.find(e => e.file.includes('lld-classes'));

console.log('=== ORIGINAL CODE ===');
console.log(item.code);

const lines = item.code.split('\n');
const lines1 = [];
for (let l of lines) {
  let line = l.replace('\r', '');
  const st = line.trim();
  if (!st || st.startsWith('%%') || st.startsWith('flowchart') || st.startsWith('graph')) {
    lines1.push(line);
    continue;
  }
  // Decision nodes NodeID{Text}
  line = line.replace(/(\b[A-Za-z0-9_\-\.]+\s*)\{([^"\n\}]+)\}(?:::\w+)?/g, (m, nid, inner) => {
    let clean = inner.trim();
    clean = clean.replace(/""$/, '"').replace(/^""/, '"');
    clean = clean.replace(/\|([^|\n]+)\|/g, 'abs($1)').replace(/"/g, "'");
    return `${nid}{"${clean}"}`;
  });

  // NodeID["Text"] with inner quotes regex fix
  line = line.replace(/(\b[A-Za-z0-9_\-\.]+\s*\[")([\s\S]*?)("\])(:::\w+)?(?=\s*(?:-->|---|==>|;\s*$|$))/g, (m, p1, inner, p3, style = '') => {
    let clean = inner.replace(/"/g, "'").replace(/\[/g, '(').replace(/\]/g, ')');
    return `${p1}${clean}${p3}${style}`;
  });
  lines1.push(line);
}

const cand1 = lines1.join('\n');
console.log('\n=== CANDIDATE 1 ===');
console.log(cand1);

try {
  await mermaid.parse(cand1);
  console.log('\nSUCCESS! CANDIDATE 1 PASSES!');
} catch (e) {
  console.log('\nCANDIDATE 1 FAILED:', e.message);
}
