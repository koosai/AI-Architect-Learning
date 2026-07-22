import fs from 'fs';
import path from 'path';
import { JSDOM } from 'jsdom';

// Setup JSDOM DOM environment for Mermaid parser
const dom = new JSDOM('<!DOCTYPE html><html><body><div id="graphDiv"></div></body></html>', {
  url: 'http://localhost/',
});

globalThis.window = dom.window;
globalThis.document = dom.window.document;
globalThis.location = dom.window.location;

try {
  Object.defineProperty(globalThis, 'navigator', {
    value: dom.window.navigator,
    configurable: true,
    writable: true,
  });
} catch (e) {}

const mermaidModule = await import('mermaid');
const mermaid = mermaidModule.default;

mermaid.initialize({
  startOnLoad: false,
  securityLevel: 'loose',
});

function repairMermaidCode(code) {
  const lines = code.split('\n');
  let firstLine = '';
  for (const l of lines) {
    const st = l.trim().replace('\r', '');
    if (st && !st.startsWith('%%')) {
      firstLine = st;
      break;
    }
  }

  let diagType = 'flowchart';
  if (firstLine.includes('sequenceDiagram')) diagType = 'sequenceDiagram';
  else if (firstLine.includes('packet-beta')) diagType = 'packet-beta';
  else if (firstLine.includes('mindmap')) diagType = 'mindmap';
  else if (firstLine.includes('classDiagram')) diagType = 'classDiagram';

  const newLines = [];

  for (let l of lines) {
    let line = l.replace('\r', '');
    const st = line.trim();

    if (!st || st === firstLine) {
      newLines.push(line);
      continue;
    }

    // 1. Mindmap fixes
    if (diagType === 'mindmap') {
      // Fix root("(Text")) -> root((Text))
      line = line.replace(/root\s*\("\(([^)]+)\)"?\)/g, 'root(($1))');
      line = line.replace(/root\s*\("\(([^)]+)\)"\)/g, 'root(($1))');
      newLines.push(line);
      continue;
    }

    // 2. Packet-beta fixes
    if (diagType === 'packet-beta') {
      line = line.replace(/"([^"]*)\("([^"]*)"\)"/g, '"$1 ($2)"');
      line = line.replace(/"([^"]*)"([^"]*)"([^"]*)"/g, '"$1 \'$2\' $3"');
      newLines.push(line);
      continue;
    }

    // 3. Sequence diagram fixes
    if (diagType === 'sequenceDiagram') {
      if (st.startsWith('subgraph')) {
        const title = st.replace('subgraph', '').trim().replace(/[\[\]"']/g, '');
        const indent = line.match(/^\s*/)[0];
        line = `${indent}box "${title}"`;
      }
      newLines.push(line);
      continue;
    }

    // 4. Flowchart / Graph fixes
    if (diagType === 'flowchart') {
      // Convert Note over -> node
      const mNote = line.match(/^(\s*)Note\s+over\s+([A-Za-z0-9_,\-\.]+)\s*:\s*(.*)$/i);
      if (mNote) {
        const indent = mNote[1];
        const refs = mNote[2].split(',').map(r => r.trim());
        const txt = mNote[3].trim().replace(/"/g, "'");
        const firstRef = refs[0].replace(/\./g, '_');
        const noteId = `Note_${firstRef}`;
        newLines.push(`${indent}${noteId}["${txt}"]`);
        for (const ref of refs) {
          newLines.push(`${indent}${ref} -.-> ${noteId}`);
        }
        continue;
      }

      // Fix invalid arrows
      line = line.replace(/-\.-\s*x\|/g, '-.->|');
      line = line.replace(/-->\s*x\|/g, '-->|');
      line = line.replace(/-\.-\s*x\s/g, '-.-> ');

      // Fix node IDs starting with digits e.g. 12306 -> N_12306
      line = line.replace(/\b([0-9][A-Za-z0-9_\-\.]*)\s*(\[|\()/g, 'N_$1$2');

      // Fix subgraph sub_id starting with digit e.g. subgraph 12306 -> subgraph S_12306
      line = line.replace(/^(\s*)subgraph\s+([0-9][A-Za-z0-9_\-\.]*)\b/g, '$1subgraph S_$2');

      // Fix subgraph titles with parens/colons/chinese: subgraph SubID Title (Text)
      const mSub = line.match(/^(\s*)subgraph\s+([A-Za-z0-9_\-\.\u4e00-\u9fa5]+)\s*(.*)$/);
      if (mSub) {
        const indent = mSub[1];
        const subId = mSub[2];
        const rest = mSub[3].trim();

        let cleanSubId = subId.replace(/[^\w]/g, '_');
        if (/^[0-9]/.test(cleanSubId)) cleanSubId = `S_${cleanSubId}`;

        if (rest) {
          const cleanTitle = rest.replace(/^\["?|"?\]$/g, '').replace(/"/g, "'");
          line = `${indent}subgraph ${cleanSubId} ["${cleanTitle}"]`;
        } else {
          if (cleanSubId !== subId) line = `${indent}subgraph ${cleanSubId} ["${subId}"]`;
          else line = `${indent}subgraph ${cleanSubId}`;
        }
        newLines.push(line);
        continue;
      }

      // Quote unquoted node text containing parens/colons/slashes
      line = line.replace(/\b([A-Za-z0-9_\-\.]+)\s*\[([^"\n\[\]]+)\](:::\w+)?/g, (m, nid, text, style = '') => {
        if (/^[0-9]/.test(nid)) nid = `N_${nid}`;
        const cleanText = text.replace(/"/g, "'");
        return `${nid}["${cleanText}"]${style}`;
      });

      // Fix edge labels -->|Text| -> -->|"Text"|
      line = line.replace(/(-->\||->>\||-\.->\||==>\|)([^|\n]+)\|/g, (m, arrow, lbl) => {
        const inner = lbl.trim().replace(/^["']|["']$/g, '').replace(/"/g, "'");
        return `${arrow}"${inner}"|`;
      });
    }

    newLines.push(line);
  }

  return newLines.join('\n');
}

async function runSmartRepair() {
  const errJsonPath = 'c:/Users/K.K/OneDrive/Desktop/AI架构师教程/mermaid_errors.json';
  if (!fs.existsSync(errJsonPath)) {
    console.log('No mermaid_errors.json found.');
    return;
  }

  const errors = JSON.parse(fs.readFileSync(errJsonPath, 'utf-8'));
  console.log(`Processing ${errors.length} failing diagrams from mermaid_errors.json...`);

  const fileGroups = {};
  for (const errItem of errors) {
    if (!fileGroups[errItem.file]) fileGroups[errItem.file] = [];
    fileGroups[errItem.file].push(errItem);
  }

  let totalFixed = 0;
  let totalStillFailing = 0;

  for (const filePath of Object.keys(fileGroups)) {
    if (!fs.existsSync(filePath)) continue;
    const content = fs.readFileSync(filePath, 'utf-8');
    const lines = content.split('\n');

    let inMermaid = false;
    let mermaidLines = [];
    let newDocLines = [];
    let fileModified = false;

    for (let i = 0; i < lines.length; i++) {
      const line = lines[i];
      if (line.trim().startsWith('```mermaid')) {
        inMermaid = true;
        mermaidLines = [];
        newDocLines.push(line);
        continue;
      }

      if (inMermaid && line.trim().startsWith('```')) {
        inMermaid = false;
        const code = mermaidLines.join('\n');
        
        // Attempt repair
        const repairedCode = repairMermaidCode(code);
        try {
          // Validate repaired code with real Mermaid parser
          await mermaid.parse(repairedCode);
          if (repairedCode !== code) {
            fileModified = true;
            totalFixed++;
          }
          newDocLines.push(...repairedCode.split('\n'));
        } catch (parseErr) {
          totalStillFailing++;
          newDocLines.push(...code.split('\n'));
        }
        newDocLines.push(line);
        continue;
      }

      if (inMermaid) {
        mermaidLines.push(line);
      } else {
        newDocLines.push(line);
      }
    }

    if (fileModified) {
      fs.writeFileSync(filePath, newDocLines.join('\n'));
    }
  }

  console.log(`\nResults: ${totalFixed} diagrams successfully repaired & validated. ${totalStillFailing} remaining for inspection.`);
}

runSmartRepair().catch(console.error);
