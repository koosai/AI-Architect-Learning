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
const item = errs.find(e => e.file.includes('scaling-strategies'));

let code = item.code;
code = code.replace(/Ring\("\("哈希空间环 \(0 ~ 2\^32 - 1"\)"\)\)/g, 'Ring(("哈希空间环 (0 ~ 2^32 - 1)"))');

console.log('=== TEST CODE ===');
console.log(code);

try {
  await mermaid.parse(code);
  console.log('PASSED 100%!');
} catch (e) {
  console.log('ERROR:', e.message);
}
