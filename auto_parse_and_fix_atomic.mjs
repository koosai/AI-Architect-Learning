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

function generateFixVariants(code) {
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

  const variants = [];

  // Candidate A: Targeted line-level transformations
  const linesA = [];
  for (let l of lines) {
    let line = l.replace('\r', '');
    const st = line.trim();

    if (!st || st === firstLine) {
      linesA.push(line);
      continue;
    }

    if (diagType === 'mindmap') {
      line = line.replace(/root\s*\("\(([^)]+)\)"?\)/g, 'root(($1))');
      line = line.replace(/root\s*\("\(([^)]+)\)"\)/g, 'root(($1))');
      line = line.replace(/root\s*\("([^"]+)"\)/g, 'root(($1))');
      linesA.push(line);
      continue;
    }

    if (diagType === 'sequenceDiagram') {
      if (st.startsWith('subgraph') || st.startsWith('box')) {
        const title = line.replace(/subgraph|box/g, '').trim().replace(/[\[\]"']/g, '');
        const indent = line.match(/^\s*/)[0];
        line = `${indent}box "${title}"`;
      }
      linesA.push(line);
      continue;
    }

    if (diagType === 'flowchart') {
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
        linesA.push(`${indent}${noteId}["${txt}"]`);
        for (const ref of refs) {
          linesA.push(`${indent}${ref} -.-> ${noteId}`);
        }
        continue;
      }

      // Fix Circle shape: Name("("Text")")) -> Name(("Text"))
      line = line.replace(/(\b[A-Za-z0-9_\-\.]+\s*)\("\("([^"\n]+)"\)\)+/g, '$1(("$2"))');
      line = line.replace(/(\b[A-Za-z0-9_\-\.]+\s*)\("\("([^"\n]+)\)"?\)/g, '$1(("$2"))');

      // Fix Database shape: NodeID[("Text")]
      line = line.replace(/\["\("([^"\n]+)"\)"\]/g, '[("$1")]');
      line = line.replace(/\("\["\("([^"\n]+)"\)"\]"\)/g, '[("$1")]');

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
        linesA.push(line);
        continue;
      }

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

    linesA.push(line);
  }
  variants.push(linesA.join('\n'));

  // Candidate B: Strip inner double quotes & replace unescaped inner brackets in NodeID["..."]
  const linesB = [];
  for (let l of linesA) {
    let line = l;
    if (diagType === 'flowchart') {
      line = line.replace(/(\b[A-Za-z0-9_\-\.]+\s*\[")([^"\n]+)("\])/g, (m, p1, p2, p3) => {
        let clean = p2.replace(/"/g, "'").replace(/\[/g, '(').replace(/\]/g, ')');
        return `${p1}${clean}${p3}`;
      });
      line = line.replace(/(\b[A-Za-z0-9_\-\.]+\s*\[)([^"\n\[\]]+)(\])/g, (m, p1, p2, p3) => {
        let clean = p2.replace(/"/g, "'").replace(/\[/g, '(').replace(/\]/g, ')');
        return `${p1}"${clean}"${p3}`;
      });
    }
    linesB.push(line);
  }
  variants.push(linesB.join('\n'));

  // Candidate C: Extreme quote cleanup for complex code snippets in node labels
  const linesC = [];
  for (let l of linesB) {
    let line = l;
    if (diagType === 'flowchart') {
      // Replace stray "] or "] inside string
      line = line.replace(/"]"/g, ')');
      line = line.replace(/"]]/g, ')]');
    }
    linesC.push(line);
  }
  variants.push(linesC.join('\n'));

  return variants;
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
          // Code failed, test repair variants
          const variants = generateFixVariants(code);
          let fixed = false;

          for (const cand of variants) {
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
