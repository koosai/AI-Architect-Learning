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

for (const name of ['moba-sync', 'gitlab-ci', 'bazel', 'cdn', 'elasticsearch']) {
  const item = errs.find(e => e.file.includes(name));
  if (!item) continue;
  console.log(`\n=== ${name} ===`);
  try {
    await mermaid.parse(item.code);
    console.log('PASSED!');
  } catch (e) {
    console.log('ERROR:', e.message);
    console.log(item.code);
  }
}
