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

const tests = [
  `mindmap\n  root("(12306 架构"))`,
  `mindmap\n  root((12306 架构))`,
  `mindmap\n  root("12306 架构")`,
  `mindmap\n  root[12306 架构]`,
  `mindmap\n  root((12306 架构))`,
  `mindmap\n  root(12306 架构)`
];

for (let i = 0; i < tests.length; i++) {
  try {
    await mermaid.parse(tests[i]);
    console.log(`Test ${i}: PASSED! -> ${tests[i].split('\n')[1]}`);
  } catch (e) {
    console.log(`Test ${i}: FAILED -> ${tests[i].split('\n')[1]} (${e.message.split('\n')[0]})`);
  }
}
