import fs from 'fs';
import path from 'path';
import { JSDOM } from 'jsdom';

// Initialize JSDOM environment for Mermaid in Node.js
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

const docsDir = 'c:/Users/K.K/OneDrive/Desktop/AI架构师教程/docs';

function getAllFiles(dir, fileList = []) {
  const files = fs.readdirSync(dir);
  for (const file of files) {
    const filePath = path.join(dir, file);
    if (fs.statSync(filePath).isDirectory()) {
      getAllFiles(filePath, fileList);
    } else if (filePath.endsWith('.mdx') || filePath.endsWith('.md')) {
      fileList.push(filePath);
    }
  }
  return fileList;
}

function fixDiagramCode(code) {
  const lines = code.split('\n');
  let diagType = 'flowchart';
  
  let firstLine = '';
  for (const l of lines) {
    const st = l.trim().replace('\r', '');
    if (st && !st.startsWith('%%')) {
      firstLine = st;
      break;
    }
  }

  if (firstLine.includes('sequenceDiagram')) diagType = 'sequenceDiagram';
  else if (firstLine.includes('packet-beta')) diagType = 'packet-beta';
  else if (firstLine.includes('mindmap')) diagType = 'mindmap';
  else if (firstLine.includes('classDiagram')) diagType = 'classDiagram';
  else if (firstLine.includes('C4Context') || firstLine.includes('C4Container')) diagType = 'C4';

  const newLines = [];

  for (let l of lines) {
    let line = l.replace('\r', '');
    const st = line.trim();

    if (!st || st === firstLine) {
      newLines.push(line);
      continue;
    }

    // Packet-beta
    if (diagType === 'packet-beta') {
      line = line.replace(/"([^"]*)\("([^"]*)"\)"/g, '"$1 ($2)"');
      line = line.replace(/"([^"]*)"([^"]*)"([^"]*)"/g, '"$1 \'$2\' $3"');
      newLines.push(line);
      continue;
    }

    // Sequence diagram
    if (diagType === 'sequenceDiagram') {
      if (st.startsWith('subgraph')) {
        const title = st.replace('subgraph', '').trim().replace(/[\[\]"']/g, '');
        const indent = line.match(/^\s*/)[0];
        line = `${indent}box "${title}"`;
      }
      newLines.push(line);
      continue;
    }

    // Flowchart
    if (diagType === 'flowchart') {
      // Fix Note over -> node
      const mNote = line.match(/^(\s*)Note\s+over\s+([A-Za-z0-9_\-\.]+)\s*:\s*(.*)$/i);
      if (mNote) {
        const indent = mNote[1];
        const ref = mNote[2];
        const txt = mNote[3].trim().replace(/"/g, "'");
        const noteId = `Note_${ref.replace(/\./g, '_')}`;
        newLines.push(`${indent}${noteId}["${txt}"]`);
        newLines.push(`${indent}${ref} -.-> ${noteId}`);
        continue;
      }

      // Fix invalid arrows
      line = line.replace(/-\.-\s*x\|/g, '-.->|');
      line = line.replace(/-->\s*x\|/g, '-->|');
      line = line.replace(/-\.-\s*x\s/g, '-.-> ');

      // Fix node ID starting with digit e.g. 12306 -> N_12306
      line = line.replace(/\b([0-9][A-Za-z0-9_\-\.]*)\s*(\[|\()/g, 'N_$1$2');

      // Fix subgraph sub_id starting with digit e.g. subgraph 12306 -> subgraph S_12306
      line = line.replace(/^(\s*)subgraph\s+([0-9][A-Za-z0-9_\-\.]*)\b/g, '$1subgraph S_$2');

      // Clean inner quotes & brackets in node labels
      line = line.replace(/(\b[A-Za-z0-9_\-\.]+\s*\[")([^"\n]+)("\])/g, (m, p1, p2, p3) => {
        const clean = p2.replace(/"/g, "'").replace(/\[/g, '(').replace(/\]/g, ')');
        return `${p1}${clean}${p3}`;
      });

      // Edge labels
      line = line.replace(/(-->\||->>\||-\.->\||==>\|)([^|\n]+)\|/g, (m, arrow, lbl) => {
        const inner = lbl.trim().replace(/^["']|["']$/g, '').replace(/"/g, "'");
        return `${arrow}"${inner}"|`;
      });
    }

    newLines.push(line);
  }

  return newLines.join('\n');
}

async function autoFixAndVerify() {
  const allFiles = getAllFiles(docsDir);
  console.log(`Starting automated Mermaid repair on ${allFiles.length} files...`);

  let iteration = 0;
  let totalErrors = 999;

  while (iteration < 10 && totalErrors > 0) {
    iteration++;
    console.log(`\n--- Iteration ${iteration} ---`);

    let currentErrors = [];
    let totalDiagrams = 0;
    let modifiedFilesCount = 0;

    for (const filePath of allFiles) {
      const content = fs.readFileSync(filePath, 'utf-8');
      const lines = content.split('\n');

      let inMermaid = false;
      let mermaidLines = [];
      let startLine = 0;
      let fileModified = false;
      let newDocLines = [];

      for (let i = 0; i < lines.length; i++) {
        const line = lines[i];
        if (line.trim().startsWith('```mermaid')) {
          inMermaid = true;
          mermaidLines = [];
          startLine = i + 1;
          newDocLines.push(line);
          continue;
        }

        if (inMermaid && line.trim().startsWith('```')) {
          inMermaid = false;
          totalDiagrams++;
          const code = mermaidLines.join('\n');

          try {
            await mermaid.parse(code);
            newDocLines.push(...mermaidLines);
          } catch (err) {
            // Attempt fix
            const fixedCode = fixDiagramCode(code);
            try {
              await mermaid.parse(fixedCode);
              fileModified = true;
              newDocLines.push(...fixedCode.split('\n'));
            } catch (err2) {
              currentErrors.push({
                file: filePath,
                startLine,
                error: err2.message || String(err2),
                code: fixedCode,
              });
              newDocLines.push(...fixedCode.split('\n'));
            }
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
        modifiedFilesCount++;
      }
    }

    totalErrors = currentErrors.length;
    console.log(`Modified files: ${modifiedFilesCount}, Total diagrams: ${totalDiagrams}, Failing: ${totalErrors}`);

    if (totalErrors > 0) {
      fs.writeFileSync(
        'c:/Users/K.K/OneDrive/Desktop/AI架构师教程/mermaid_errors.json',
        JSON.stringify(currentErrors, null, 2)
      );
    }
  }
}

autoFixAndVerify().catch(console.error);
