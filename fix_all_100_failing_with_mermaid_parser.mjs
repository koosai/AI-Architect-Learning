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
globalThis.Option = dom.window.Option;
globalThis.Image = dom.window.Image;
if (dom.window.SVGElement) {
  globalThis.SVGElement = dom.window.SVGElement;
}

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

  // Candidate 1: Targeted line transformations with sequence note & message sanitization
  const lines1 = [];
  for (let l of lines) {
    let line = l.replace('\r', '');

    // Separate inline 'end Note' into separate lines
    if (line.includes('end') && line.includes('Note over')) {
      const parts = line.split(/(\bend\b)/);
      for (const p of parts) {
        if (p.trim()) lines1.push(p);
      }
      continue;
    }

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
        let title = line.replace(/^\s*(?:subgraph|box)\s*(?:[A-Za-z0-9_\-\.]+\s*)?/g, '').trim();
        title = title.replace(/^[\['"]+|[\['"]+$/g, '');
        title = title.replace(/->/g, '→').replace(/"/g, "'");
        line = `${indent}box "${title}"`;
      } else if (st.startsWith('Note')) {
        line = line.replace(/->/g, '→').replace(/"/g, "'");
      } else if (line.includes(':')) {
        const parts = line.split(':');
        const prefix = parts[0];
        let msg = parts.slice(1).join(':').trim();
        msg = msg.replace(/"/g, "'").replace(/\[/g, '(').replace(/\]/g, ')');
        line = `${prefix}: ${msg}`;
      }
      lines1.push(line);
      continue;
    }

    if (diagType === 'flowchart' || firstLine.includes('graph')) {
      // Fix invalid arrows
      line = line.replace(/-\.-\s*x\|/g, '-.->|');
      line = line.replace(/-->\s*x\|/g, '-->|');
      line = line.replace(/-\.-\s*x\s/g, '-.-> ');
      line = line.replace(/<-->/g, '<--->');

      // Convert Note over in flowchart -> node
      const mNote = line.match(/^(\s*)Note\s+over\s+([A-Za-z0-9_,\-\.]+)\s*:\s*(.*)$/i);
      if (mNote) {
        const indent = mNote[1];
        const refs = mNote[2].split(',').map(r => r.trim());
        let txt = mNote[3].trim().replace(/"/g, "'");
        txt = txt.replace(/\[/g, '(').replace(/\]/g, ')');
        const firstRef = refs[0].replace(/\./g, '_');
        const noteId = `Note_${firstRef}`;
        lines1.push(`${indent}${noteId}["${txt}"]`);
        for (const ref of refs) {
          lines1.push(`${indent}${ref} -.-> ${noteId}`);
        }
        continue;
      }

      // Restore Stadium Shape: Start("[Text")]) or Start("[Text]") -> Start(["Text"])
      line = line.replace(/(\b[A-Za-z0-9_\-\.]+\s*)\["\(?([^"\n]+)"?\)?\]\)/g, '$1(["$2"])');
      line = line.replace(/(\b[A-Za-z0-9_\-\.]+\s*)\["([^"\n]+)"\]\)/g, '$1(["$2"])');

      // Restore Database Shape: NodeID["("Text")"] / NodeID["("Text"]")] -> NodeID[("Text")]
      line = line.replace(/(\b[A-Za-z0-9_\-\.]+\s*)\["\("([^"\n]+)"\)"\]/g, '$1[("$2")]');
      line = line.replace(/(\b[A-Za-z0-9_\-\.]+\s*)\["\("([^"\n]+)"\]"\)\]/g, '$1[("$2")]');
      line = line.replace(/(\b[A-Za-z0-9_\-\.]+\s*)\("\["\("([^"\n]+)"\)"\]"\)/g, '$1[("$2")]');
      line = line.replace(/(\b[A-Za-z0-9_\-\.]+\s*)\("\("([^"\n]+)"\)"\)/g, '$1[("$2")]');
      line = line.replace(/(\b[A-Za-z0-9_\-\.]+\s*)\("\("([^"\n]+)"\]"\)/g, '$1[("$2")]');

      // Restore Circle Shape: Ring("("Text")")) -> Ring(("Text"))
      line = line.replace(/(\b[A-Za-z0-9_\-\.]+\s*)\("\("([^"\n]+)"\)\)+/g, '$1(("$2"))');
      line = line.replace(/(\b[A-Za-z0-9_\-\.]+\s*)\("\("([^"\n]+)\)"?\)/g, '$1(("$2"))');
      line = line.replace(/(\b[A-Za-z0-9_\-\.]+\s*)\("\("([^"\n]+)"\)\)/g, '$1(("$2"))');

      // Quote & Sanitize Decision Nodes NodeID{Text} -> NodeID{"Clean Text"} (strip :::style from decision nodes)
      line = line.replace(/(\b[A-Za-z0-9_\-\.]+\s*)\{([^"\n\}]+)\}(?:::\w+)?/g, (m, nid, inner) => {
        let clean = inner.trim();
        clean = clean.replace(/""$/, '"').replace(/^""/, '"');
        if (clean.startsWith('"') && clean.endsWith('"') && !clean.slice(1, -1).includes('"')) {
          return `${nid}{${clean}}`;
        }
        clean = clean.replace(/\|([^|\n]+)\|/g, 'abs($1)').replace(/"/g, "'");
        return `${nid}{"${clean}"}`;
      });

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

      // Fix unquoted node text NodeID[Text] -> NodeID["Text"]
      line = line.replace(/\b([A-Za-z0-9_\-\.]+)\s*\[([^"\n\[\]]+)\](:::\w+)?/g, (m, nid, text, style = '') => {
        if (/^[0-9]/.test(nid)) nid = `N_${nid}`;
        let clean = text.trim().replace(/"/g, "'");
        return `${nid}["${clean}"]${style}`;
      });

      // Fix inner quotes & parens in node labels anywhere on line: NodeID["Text"]
      line = line.replace(/(\b[A-Za-z0-9_\-\.]+\s*\[")([^"\n]+)("\])(:::\w+)?/g, (m, p1, inner, p3, style = '') => {
        let clean = inner.replace(/"/g, "'").replace(/\[/g, '(').replace(/\]/g, ')');
        return `${p1}${clean}${p3}${style}`;
      });

      // Fix stray trailing quotes/parens
      line = line.replace(/(\b[A-Za-z0-9_\-\.]+\s*\["[^"\n]+)"\)\)$/g, '$1"]');
      line = line.replace(/(\b[A-Za-z0-9_\-\.]+\s*\["[^"\n]+)"\]"\]$/g, '$1"]');
      line = line.replace(/(\b[A-Za-z0-9_\-\.]+\s*\["[^"\n]+)"\)$/g, '$1"]');

      // Edge labels
      line = line.replace(/(-->\||->>\||-\.->\||==>\|)([^|\n]+)\|/g, (m, arrow, lbl) => {
        let inner = lbl.trim();
        while ((inner.startsWith('"') && inner.endsWith('"')) || (inner.startsWith("'") && inner.endsWith("'"))) {
          inner = inner.slice(1, -1).trim();
        }
        inner = inner.replace(/"/g, "'").replace(/\[/g, '(').replace(/\]/g, ')');
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
