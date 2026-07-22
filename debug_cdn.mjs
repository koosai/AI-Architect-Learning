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

const cdnFile = 'c:/Users/K.K/OneDrive/Desktop/AI架构师教程/docs/atlas/cdn.mdx';
const fileLines = fs.readFileSync(cdnFile, 'utf-8').split('\n');

let blockStart = -1;
let blockEnd = -1;

for (let i = 0; i < fileLines.length; i++) {
  if (fileLines[i].trim().startsWith('```mermaid')) {
    blockStart = i;
    const codeLines = [];
    for (let j = i + 1; j < fileLines.length; j++) {
      if (fileLines[j].trim().startsWith('```')) {
        blockEnd = j;
        break;
      }
      codeLines.push(fileLines[j]);
    }

    if (i === 82 || i === 83 || i === 84) {
      const fixedCode = `flowchart TB
  subgraph User_Tier["用户终端与 Local DNS"]
    Client["User Browser / App"]
    LDNS["Local DNS (ISP 递归解析器)"]
  end

  subgraph GSLB_Tier["GSLB 全局负载均衡 (DNS 调度中心)"]
    GSLB["Akamai GSLB DNS Cluster"]
    NetworkMap["Global Network Map Engine"]
  end

  subgraph Edge_PoP["全球边缘机房 (Edge PoP Cluster)"]
    Edge1["Edge Node 1 (Closest to User)"]
    Edge2["Edge Node 2 (Consistent Hash Peer)"]
  end

  subgraph Origin_Tier["客户源站 (Origin Infrastructure)"]
    OriginShield["Origin Shield (回源防护屏障)"]
    OriginDB["Customer Origin Server (App/DB)"]
  end

  Client -->|"1. DNS Query: cdn.example.com"| LDNS
  LDNS -->|"2. 带 EDNS0 Client IP 查询"| GSLB
  GSLB -->|"3. 结合 NetworkMap 计算最快 PoP"| LDNS
  LDNS -->|"4. 返回 Edge IP (1.2.3.4)"| Client

  Client -->|"5. HTTP/3 Request"| Edge1
  Edge1 -->|"6. 200 OK (来自边缘 SSD/RAM 10ms)"| Client
  Edge1 -->|"7. 一致性哈希查找文件归属"| Edge2
  Edge2 -->|"8. Collapse Forwarding 合并回源"| OriginShield
  OriginShield -->|"9. 唯一回源请求"| OriginDB
  OriginDB -->|"10. 返回源数据并缓存"| Edge1`;

      try {
        await mermaid.parse(fixedCode);
        console.log('CDN FIXED CODE PASSED 100%!');
        const newLines = [
          ...fileLines.slice(0, blockStart + 1),
          ...fixedCode.split('\n'),
          ...fileLines.slice(blockEnd)
        ];
        fs.writeFileSync(cdnFile, newLines.join('\n'));
        console.log('Successfully saved to cdn.mdx!');
      } catch (e) {
        console.log('CDN Fix Failed:', e.message);
      }
    }
  }
}
