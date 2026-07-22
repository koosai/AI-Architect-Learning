import fs from 'fs';
import path from 'path';
import { JSDOM } from 'jsdom';

const dom = new JSDOM('<!DOCTYPE html><html><body><div id="graphDiv"></div></body></html>', {
  url: 'http://localhost/',
});

globalThis.window = dom.window;
globalThis.document = dom.window.document;
globalThis.location = dom.window.location;
globalThis.Option = dom.window.Option;
globalThis.Image = dom.window.Image;

const mermaidModule = await import('mermaid');
const mermaid = mermaidModule.default;
mermaid.initialize({ startOnLoad: false, securityLevel: 'loose' });

function generateFixes(code) {
  const cands = [];
  const lines = code.split('\n');
  const firstLine = lines[0] ? lines[0].trim() : '';
  const isSeq = firstLine.includes('sequenceDiagram');
  const isMind = firstLine.includes('mindmap');

  // Fix 1: Master shape restorers & arrow fixes
  const lines1 = [];
  for (let l of lines) {
    let line = l.replace('\r', '');
    const st = line.trim();

    if (!st || st === firstLine) {
      lines1.push(line);
      continue;
    }

    if (isMind) {
      line = line.replace(/root\s*\("\(([^)]+)\)"?\)/g, 'root(($1))');
      line = line.replace(/root\s*\("\(([^)]+)\)"\)/g, 'root(($1))');
      line = line.replace(/root\s*\("([^"]+)"\)/g, 'root(($1))');
      line = line.replace(/root\s*\(([^)]+)\)/g, 'root(($1))');
      lines1.push(line);
      continue;
    }

    if (!isSeq) {
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

      line = line.replace(/<-->/g, '<--->');
      line = line.replace(/<==>/g, '<===>');

      // Specific corruptions
      line = line.replace(/Ring\("\("哈希空间环 \(0 ~ 2\^32 - 1"\)"\)\)/g, 'Ring(("哈希空间环 (0 ~ 2^32 - 1)"))');
      line = line.replace(/(\b[A-Za-z0-9_\-\.]+\s*)\("\("([^"\n]+)"\)\)+/g, '$1(("$2"))');
      line = line.replace(/(\b[A-Za-z0-9_\-\.]+\s*)\("\("([^"\n]+)\)"?\)/g, '$1(("$2"))');
      line = line.replace(/(\b[A-Za-z0-9_\-\.]+\s*)\("\("([^"\n]+)"\)\)/g, '$1(("$2"))');
      line = line.replace(/(\b[A-Za-z0-9_\-\.]+\s*)\("\(([^"\n]+)\)"\)+/g, '$1(("$2"))');
      line = line.replace(/(\b[A-Za-z0-9_\-\.]+\s*)\("\(([^"\n]+)\)"\)/g, '$1(("$2"))');

      line = line.replace(/\['public'"\]\)/g, "'public')");
      line = line.replace(/\)""\}/g, ')"}');
    }

    lines1.push(line);
  }
  cands.push(lines1.join('\n'));

  // Fix 2: Deep inner quote replacement inside NodeID["..."]
  const lines2 = [];
  for (let l of lines1) {
    if (!isSeq && !isMind) {
      l = l.replace(/(\b[A-Za-z0-9_\-\.]+\s*\[")([\s\S]*?)("\])(:::\w+)?(?=\s*(?:-->|---|==>|<==>|<--->|;\s*$|$))/g, (m, p1, inner, p3, style = '') => {
        let clean = inner.replace(/"/g, "'").replace(/\[/g, '(').replace(/\]/g, ')');
        return `${p1}${clean}${p3}${style}`;
      });
    }
    lines2.push(l);
  }
  cands.push(lines2.join('\n'));

  return cands;
}

async function fixRemaining50() {
  const errs = JSON.parse(fs.readFileSync('mermaid_errors.json', 'utf-8'));
  console.log(`Testing fixes for ${errs.length} failing diagrams...`);

  let fixedCount = 0;

  for (const item of errs) {
    const filePath = item.file;
    if (!fs.existsSync(filePath)) continue;

    const fileLines = fs.readFileSync(filePath, 'utf-8').split('\n');

    // Find the mermaid block starting around item.startLine
    let blockStart = -1;
    let blockEnd = -1;
    let codeLines = [];

    for (let i = Math.max(0, item.startLine - 5); i < Math.min(fileLines.length, item.startLine + 5); i++) {
      if (fileLines[i].trim().startsWith('```mermaid')) {
        blockStart = i;
        for (let j = i + 1; j < fileLines.length; j++) {
          if (fileLines[j].trim().startsWith('```')) {
            blockEnd = j;
            break;
          }
          codeLines.push(fileLines[j]);
        }
        break;
      }
    }

    if (blockStart === -1 || blockEnd === -1) {
      console.log(`[MERMAID BLOCK NOT FOUND] ${path.basename(filePath)} Line ${item.startLine}`);
      continue;
    }

    const currentCode = codeLines.join('\n');
    const cands = generateFixes(currentCode);

    let fixedCode = null;
    for (const cand of cands) {
      try {
        await mermaid.parse(cand);
        fixedCode = cand;
        break;
      } catch (e) {
        // Continue trying
      }
    }

    if (fixedCode) {
      // Replace original lines in fileLines
      const newLines = [
        ...fileLines.slice(0, blockStart + 1),
        ...fixedCode.split('\n'),
        ...fileLines.slice(blockEnd)
      ];
      fs.writeFileSync(filePath, newLines.join('\n'));
      fixedCount++;
      console.log(`[FIXED] ${path.basename(filePath)} Line ${item.startLine}`);
    } else {
      console.log(`[STILL FAILING] ${path.basename(filePath)} Line ${item.startLine}`);
    }
  }

  console.log(`Successfully repaired ${fixedCount} / ${errs.length} remaining failing diagrams.`);
}

fixRemaining50().catch(console.error);
