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
  const candidates = [];
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

  // Candidate 1: Targeted line replacements
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
    } else if (diagType === 'sequenceDiagram') {
      if (st.startsWith('subgraph')) {
        const title = st.replace('subgraph', '').trim().replace(/[\[\]"']/g, '');
        const indent = line.match(/^\s*/)[0];
        line = `${indent}box "${title}"`;
      }
    } else if (diagType === 'flowchart') {
      // Fix invalid arrows
      line = line.replace(/-\.-\s*x\|/g, '-.->|');
      line = line.replace(/-->\s*x\|/g, '-->|');
      line = line.replace(/-\.-\s*x\s/g, '-.-> ');

      // Convert Note over -> node
      const mNote = line.match(/^(\s*)Note\s+over\s+([A-Za-z0-9_,\-\.]+)\s*:\s*(.*)$/i);
      if (mNote) {
        const indent = mNote[1];
        const refs = mNote[2].split(',').map(r => r.trim());
        const txt = mNote[3].trim().replace(/"/g, "'");
        const firstRef = refs[0].replace(/\./g, '_');
        const noteId = `Note_${firstRef}`;
        lines1.push(`${indent}${noteId}["${txt}"]`);
        for (const ref of refs) {
          lines1.push(`${indent}${ref} -.-> ${noteId}`);
        }
        continue;
      }

      // Restore Shapes
      line = line.replace(/\["\("([^"\n]+)"\)"\]/g, '[("$1")]');
      line = line.replace(/\("\["\("([^"\n]+)"\)"\]"\)/g, '[("$1")]');
      line = line.replace(/\("\("([^"\n]+)"\)\)/g, '(("$1"))');
      line = line.replace(/\("\[([^"\n]+)\]"\)/g, '(["$1"])');
      line = line.replace(/\["\("([^"\n]+)"\]/g, '(["$1"])');

      // Subgraph title quotes
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

      // Unquoted node labels with parens/colons
      line = line.replace(/\b([A-Za-z0-9_\-\.]+)\s*\[([^"\n\[\]]+)\](:::\w+)?/g, (m, nid, text, style = '') => {
        if (/^[0-9]/.test(nid)) nid = `N_${nid}`;
        let clean = text.trim().replace(/"/g, "'");
        clean = clean.replace(/\[/g, '(').replace(/\]/g, ')');
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

  // Candidate 2: Simplify inner quotes & parens aggressively
  const lines2 = [];
  for (let l of lines) {
    let line = l.replace('\r', '');
    const st = line.trim();
    if (!st || st === firstLine) {
      lines2.push(line);
      continue;
    }
    if (diagType === 'flowchart') {
      line = line.replace(/-\.-\s*x/g, '-.->');
      line = line.replace(/\["([^"\n]+)"\]/g, (m, inner) => {
        const clean = inner.replace(/"/g, "'").replace(/\[/g, '(').replace(/\]/g, ')');
        return `["${clean}"]`;
      });
    }
    lines2.push(line);
  }
  candidates.push(lines2.join('\n'));

  return candidates;
}

async function runAtomicRepair() {
  const allFiles = getAllFiles(docsDir);
  console.log(`Scanning and repairing ${allFiles.length} files...`);

  let totalDiagrams = 0;
  let totalFixed = 0;
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
          // Check if code passes as-is
          await mermaid.parse(code);
          totalPassing++;
          newDocLines.push(...mermaidLines);
        } catch (err) {
          // Code failed, test candidates
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
              // Try next candidate
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

  console.log(`\n==========================================`);
  console.log(`Total Diagrams Scanned: ${totalDiagrams}`);
  console.log(`Passed As-Is: ${totalPassing}`);
  console.log(`Repaired & Verified (0 errors): ${totalFixed}`);
  console.log(`Total Validated Passing Diagrams: ${totalPassing + totalFixed} / ${totalDiagrams} (${((totalPassing + totalFixed) / totalDiagrams * 100).toFixed(1)}%)`);
  console.log(`Remaining Failing: ${totalFailing}`);
  console.log(`==========================================`);

  if (totalFailing > 0) {
    fs.writeFileSync('c:/Users/K.K/OneDrive/Desktop/AI架构师教程/mermaid_errors.json', JSON.stringify(failingItems, null, 2));
  } else {
    fs.writeFileSync('c:/Users/K.K/OneDrive/Desktop/AI架构师教程/mermaid_errors.json', '[]');
  }
}

runAtomicRepair().catch(console.error);
