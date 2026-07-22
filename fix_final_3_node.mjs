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
  rep = rep.replace(/\["\("节点 A <br\/>\(新数据 X=v2\)"\]"\)/g, '[("节点 A <br/>(新数据 X=v2)")]');
  rep = rep.replace(/\["\("节点 B <br\/>\(新数据 X=v2\)"\]"\)/g, '[("节点 B <br/>(新数据 X=v2)")]');
  rep = rep.replace(/\["\("节点 C <br\/>\(旧数据 X=v1\)"\]"\)/g, '[("节点 C <br/>(旧数据 X=v1)")]');
  rep = rep.replace(/\["\("节点 A <br\/>\(新数据 Y=v2\)"\]"\)/g, '[("节点 A <br/>(新数据 Y=v2)")]');
  rep = rep.replace(/\["\("节点 B <br\/>\(旧数据 Y=v1\)"\]"\)/g, '[("节点 B <br/>(旧数据 Y=v1)")]');
  rep = rep.replace(/\["\("节点 C <br\/>\(旧数据 Y=v1\)"\]"\)/g, '[("节点 C <br/>(旧数据 Y=v1)")]');
  fs.writeFileSync(repFile, rep);
  console.log('Fixed replication.mdx');
}

// 2. enterprise-erp-integration.mdx
const erpFile = path.join(docsDir, '06-cloud-enterprise-industrial', 'enterprise-erp-integration.mdx');
if (fs.existsSync(erpFile)) {
  let erp = fs.readFileSync(erpFile, 'utf-8');
  erp = erp.replace('Broker["["消息队列 / Event Broker"]"]', 'Broker["消息队列 / Event Broker"]');
  fs.writeFileSync(erpFile, erp);
  console.log('Fixed enterprise-erp-integration.mdx');
}

// 3. cdn.mdx
const cdnFile = path.join(docsDir, '04-atlas-case-studies', 'tier1', 'cdn.mdx');
if (fs.existsSync(cdnFile)) {
  let cdn = fs.readFileSync(cdnFile, 'utf-8');
  cdn = cdn.replace('LDNS -->>Client: 4. 返回 Edge IP (1.2.3.4)', 'LDNS -->|4. 返回 Edge IP| Client');
  cdn = cdn.replace('Edge1 -->>Client: 6. 200 OK (来自边缘 SSD/RAM 10ms)', 'Edge1 -->|6. 边缘缓存命中 200 OK| Client');
  cdn = cdn.replace('OriginDB -->>Edge1: 10. 返回源数据并缓存', 'OriginDB -->|10. 返回源数据并缓存| Edge1');
  // Remove stray end at end of block
  cdn = cdn.replace(/OriginDB -->\|10. 返回源数据并缓存\| Edge1\s*end/g, 'OriginDB -->|10. 返回源数据并缓存| Edge1');
  fs.writeFileSync(cdnFile, cdn);
  console.log('Fixed cdn.mdx');
}
