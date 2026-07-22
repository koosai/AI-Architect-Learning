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

// 1. Fix replication.mdx
const repPath = path.join(docsDir, '05-core-components', 'replication.mdx');
let repContent = fs.readFileSync(repPath, 'utf-8');

repContent = repContent.replace('WriteSet_S["写集合 (W=2) <br/>(A, B) -.-> NodeA_S & NodeB_S', 'WriteSet_S["写集合 (W=2) <br/>(A, B)"] -.-> NodeA_S & NodeB_S');
repContent = repContent.replace('ReadSet_S["读集合 (R=2) <br/>(B, C) -.-> NodeB_S & NodeC_S', 'ReadSet_S["读集合 (R=2) <br/>(B, C)"] -.-> NodeB_S & NodeC_S');
repContent = repContent.replace('WriteSet_W["写集合 (W=1) <br/>(A) -.-> NodeA_W', 'WriteSet_W["写集合 (W=1) <br/>(A)"] -.-> NodeA_W');
repContent = repContent.replace('ReadSet_W["读集合 (R=2) <br/>(B, C) -.-> NodeB_W & NodeC_W', 'ReadSet_W["读集合 (R=2) <br/>(B, C)"] -.-> NodeB_W & NodeC_W');

fs.writeFileSync(repPath, repContent);
console.log('Fixed replication.mdx unclosed node quote!');

// 2. Fix enterprise-erp-integration.mdx
const erpPath = path.join(docsDir, '06-cloud-enterprise-industrial', 'enterprise-erp-integration.mdx');
let erpContent = fs.readFileSync(erpPath, 'utf-8');

erpContent = erpContent.replace('Broker["["消息队列 / Event Broker"]]"', 'Broker["消息队列 / Event Broker"]');
erpContent = erpContent.replace('Broker["["消息队列 / Event Broker"]"]', 'Broker["消息队列 / Event Broker"]');

fs.writeFileSync(erpPath, erpContent);
console.log('Fixed enterprise-erp-integration.mdx double bracket!');
