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

// 1. replication.mdx
const repFile = path.join(docsDir, '05-core-components', 'replication.mdx');
if (fs.existsSync(repFile)) {
  let rep = fs.readFileSync(repFile, 'utf-8');
  rep = rep.replace(/\[A, B"\]"\]/g, '(A, B)');
  rep = rep.replace(/\[B, C"\]"\]/g, '(B, C)');
  rep = rep.replace(/\[A"\]"\]/g, '(A)');
  rep = rep.replace(/\[B, C"\]/g, '(B, C)');
  fs.writeFileSync(repFile, rep);
  console.log('Fixed replication.mdx final lines!');
}

// 2. enterprise-erp-integration.mdx
const erpFile = path.join(docsDir, '06-cloud-enterprise-industrial', 'enterprise-erp-integration.mdx');
if (fs.existsSync(erpFile)) {
  let erp = fs.readFileSync(erpFile, 'utf-8');
  erp = erp.replace('Broker["["消息队列 / Event Broker"]"]', 'Broker["消息队列 / Event Broker"]');
  erp = erp.replace('A3("(Sys A"))', 'A3(("Sys A"))');
  erp = erp.replace('B3("(Sys B"))', 'B3(("Sys B"))');
  erp = erp.replace('C3("(Sys C"))', 'C3(("Sys C"))');
  erp = erp.replace('D3("(Sys D"))', 'D3(("Sys D"))');
  fs.writeFileSync(erpFile, erp);
  console.log('Fixed enterprise-erp-integration.mdx final lines!');
}
