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

function generateFixCandidates(code) {
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

  const candidates = [];

  // Candidate 1: Targeted syntax restoration
  const lines1 = [];
  for (let l of lines) {
    let line = l.replace('\r', '');
    const st = line.trim();

    if (!st || st === firstLine) {
      lines1.push(line);
      continue;
    }

    if (diagType === 'mindmap') {
      line = line.replace(/root\s*\("\(([^)]+)\)"?\)/g, 'root(($1))');
      line = line.replace(/root\s*\("\(([^)]+)\)"\)/g, 'root(($1))');
      line = line.replace(/root\s*\("([^"]+)"\)/g, 'root(($1))');
      lines1.push(line);
      continue;
    }

    if (diagType === 'sequenceDiagram') {
      if (st.startsWith('subgraph') || st.startsWith('box')) {
        const indent = line.match(/^\s*/)[0];
        let title = line.replace(/^\s*(subgraph|box)\s*(?:[A-Za-z0-9_\-\.]+\s*)?/g, '').trim();
        title = title.replace(/^[\['"]+|[\['"]+$/g, '');
        title = title.replace(/->/g, '→').replace(/"/g, "'");
        line = `${indent}box "${title}"`;
      } else if (st.startsWith('Note')) {
        line = line.replace(/->/g, '→');
      }
      lines1.push(line);
      continue;
    }

    if (diagType === 'flowchart' || firstLine.includes('graph')) {
      // Fix invalid arrows
      line = line.replace(/-\.-\s*x\|/g, '-.->|');
      line = line.replace(/-->\s*x\|/g, '-->|');
      line = line.replace(/-\.-\s*x\s/g, '-.-> ');

      // Restore Circle Shape: NodeID("(Text")) -> NodeID(("Text"))
      line = line.replace(/(\b[A-Za-z0-9_\-\.]+\s*)\("\("?([^"\n]+)"?\)\)+/g, '$1(("$2"))');
      line = line.replace(/(\b[A-Za-z0-9_\-\.]+\s*)\("\("([^"\n]+)"\)\)/g, '$1(("$2"))');

      // Restore Stadium Shape: NodeID["["Text"]] -> NodeID["Text"]
      line = line.replace(/(\b[A-Za-z0-9_\-\.]+\s*)\["\["([^"\n]+)"\]"\]/g, '$1["$2"]');
      line = line.replace(/(\b[A-Za-z0-9_\-\.]+\s*)\["\(?([^"\n]+)"\)?\]\)/g, '$1(["$2"])');

      // Restore Database Shape: NodeID["("Text")"] -> NodeID[("Text")]
      line = line.replace(/(\b[A-Za-z0-9_\-\.]+\s*)\["\("([^"\n]+)"\)"\]/g, '$1[("$2")]');
      line = line.replace(/(\b[A-Za-z0-9_\-\.]+\s*)\("\["\("([^"\n]+)"\)"\]"\)/g, '$1[("$2")]');
      line = line.replace(/(\b[A-Za-z0-9_\-\.]+\s*)\("\("([^"\n]+)"\)"\)/g, '$1[("$2")]');

      // Subgraph title quotes & safe sub_id
      const mSub = line.match(/^(\s*)subgraph\s+([A-Za-z0-9_\-\.\u4e00-\u9fa5]+)\s*(.*)$/);
      if (mSub) {
        const indent = mSub[1];
        const subId = mSub[2];
        const rest = mSub[3].trim();
        let cleanSubId = subId.replace(/[^\w]/g, '_');
        if (/^[0-9]/.test(cleanSubId)) cleanSubId = `S_${cleanSubId}`;

        if (rest) {
          let cleanTitle = rest.replace(/^[\['"]+|[\['"]+$/g, '').trim();
          cleanTitle = cleanTitle.replace(/"/g, "'");
          line = `${indent}subgraph ${cleanSubId} ["${cleanTitle}"]`;
        } else {
          if (cleanSubId !== subId) line = `${indent}subgraph ${cleanSubId} ["${subId}"]`;
          else line = `${indent}subgraph ${cleanSubId}`;
        }
        lines1.push(line);
        continue;
      }

      // Fix inner quotes & parens in node labels: NodeID["Text"]
      line = line.replace(/\b([A-Za-z0-9_\-\.]+)\s*\["([^"\n]+)"\](:::\w+)?/g, (m, nid, text, style = '') => {
        let clean = text.replace(/"/g, "'").replace(/\[/g, '(').replace(/\]/g, ')');
        return `${nid}["${clean}"]${style}`;
      });

      // Edge labels
      line = line.replace(/(-->\||->>\||-\.->\||==>\|)([^|\n]+)\|/g, (m, arrow, lbl) => {
        let inner = lbl.trim();
        while ((inner.startsWith('"') && inner.endsWith('"')) || (inner.startsWith("'") && inner.endsWith("'"))) {
          inner = inner.slice(1, -1).trim();
        }
        inner = inner.replace(/"/g, "'");
        return `${arrow}"${inner}"|`;
      });
    }

    lines1.push(line);
  }
  candidates.push(lines1.join('\n'));

  return candidates;
}

async function runAtomicRepairOnlyFailing() {
  const allFiles = getAllFiles(docsDir);
  console.log(`Scanning and atomic-repairing ${allFiles.length} files...`);

  let iteration = 0;
  let totalFixed = 999;

  while (iteration < 3 && totalFixed > 0) {
    iteration++;
    console.log(`\n--- Iteration ${iteration} ---`);

    totalFixed = 0;
    let totalDiagrams = 0;
    let totalPassing = 0;
    let totalFailing = 0;
    const failingItems = [];

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
            // 1. Check if original code passes as-is
            await mermaid.parse(code);
            totalPassing++;
            newDocLines.push(...mermaidLines);
          } catch (err) {
            // 2. Original code failed, test candidate fixes
            const candidates = generateFixCandidates(code);
            let fixed = false;

            for (const cand of candidates) {
              try {
                await mermaid.parse(cand);
                // Candidate PASSED 100%!
                fixed = true;
                fileModified = true;
                totalFixed++;
                newDocLines.push(...cand.split('\n'));
                break;
              } catch (errCand) {
                // Candidate failed, try next
              }
            }

            if (!fixed) {
              totalFailing++;
              failingItems.push({
                file: filePath,
                startLine,
                error: err.message || String(err),
                code,
              });
              newDocLines.push(...mermaidLines);
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
      }
    }

    console.log(`Iteration ${iteration} Results: Passing=${totalPassing}, Fixed=${totalFixed}, Remaining Failing=${totalFailing}`);
    if (totalFailing > 0) {
      fs.writeFileSync('c:/Users/K.K/OneDrive/Desktop/AI架构师教程/mermaid_errors.json', JSON.stringify(failingItems, null, 2));
    } else {
      fs.writeFileSync('c:/Users/K.K/OneDrive/Desktop/AI架构师教程/mermaid_errors.json', '[]');
    }
  }
}

runAtomicRepairOnlyFailing().catch(console.error);
