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

  // Precision fix strategy
  const lines1 = [];
  for (let l of lines) {
    let line = l.replace('\r', '');

    // 1. Fix flowchart -->>
    line = line.replace(/-->>\s*([A-Za-z0-9_\-\.]+)\s*:\s*(.*)$/, '-->|"$2"| $1');
    line = line.replace(/-->>/g, '-->');

    // 2. Fix flowchart <--|label|
    line = line.replace(/([A-Za-z0-9_\-\.]+)\s*<--\|([^|]+)\|\s*([A-Za-z0-9_\-\.]+)/, '$3 -->|"$2"| $1');

    // 3. Fix flowchart <--> and <==>
    line = line.replace(/<-->/g, '<--->');
    line = line.replace(/<==>/g, '<===>');

    // 4. Fix subgraph inner quotes
    if (line.trim().startsWith('subgraph')) {
      line = line.replace(/("W \+ R = 4 > 3")/g, "'W + R = 4 > 3'");
      line = line.replace(/("W \+ R = 3 <= 3")/g, "'W + R = 3 <= 3'");
    }

    // 5. Fix circle shape (Sys A") -> (Sys A)
    line = line.replace(/\("(Sys [A-D])"\)\)/g, '(($1))');
    line = line.replace(/\("\(?"?([^"\n\)\(]+)"?\)\)+/g, '(("$1"))');

    // 6. Fix unclosed brackets/quotes in node strings
    line = line.replace(/\[105"\]\)/g, '(105)');
    line = line.replace(/\["\]\)/g, ')');
    line = line.replace(/\(用户 ACL: \['public'"\]\)/g, "(用户 ACL: 'public')");
    line = line.replace(/Doc#2\[Del"\]\)/g, 'Doc#2 (Del)');
    line = line.replace(/Doc#4\[Del"\]\)/g, 'Doc#4 (Del)');
    line = line.replace(/Mem\["\]\)/g, 'Mem)');

    // 7. Fix stray quotes in decision nodes
    line = line.replace(/\)""\}/g, ')"}');

    // 8. Fix stadium shape Start("[...
    line = line.replace(/Start\("\["([^"]+)"\]"\)/g, 'Start(["$1"])');
    line = line.replace(/Start\("\["([^"]+)"\)\)/g, 'Start(["$1"])');
    line = line.replace(/Start\("\[([^"]+)"\)\)/g, 'Start(["$1"])');
    line = line.replace(/Start\("\[([^"]+)"\]\)/g, 'Start(["$1"])');

    // 9. Fix cdn alt/else
    if (line.trim().startsWith('alt ') || line.trim().startsWith('else ') || line.trim() === 'end') {
      line = `%% ${line.trim()}`;
    }

    lines1.push(line);
  }
  cands.push(lines1.join('\n'));

  // Candidate 2: sanitize node inner text completely
  const lines2 = [];
  for (let l of lines1) {
    let line = l.replace(/(\b[A-Za-z0-9_\-\.]+\s*\[")([\s\S]*?)("\])(:::\w+)?(?=\s*(?:-->|---|==>|<==>|<--->|;\s*$|$))/g, (m, p1, inner, p3, style = '') => {
      let clean = inner.replace(/"/g, "'").replace(/\[/g, '(').replace(/\]/g, ')');
      return `${p1}${clean}${p3}${style}`;
    });
    lines2.push(line);
  }
  cands.push(lines2.join('\n'));

  return cands;
}

async function fixFinal16() {
  const errs = JSON.parse(fs.readFileSync('mermaid_errors.json', 'utf-8'));
  console.log(`Testing fixes for remaining ${errs.length} failing diagrams...`);

  let fixedCount = 0;

  for (const item of errs) {
    const filePath = item.file;
    if (!fs.existsSync(filePath)) continue;

    const fileLines = fs.readFileSync(filePath, 'utf-8').split('\n');

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

    if (blockStart === -1 || blockEnd === -1) continue;

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
      const newLines = [
        ...fileLines.slice(0, blockStart + 1),
        ...fixedCode.split('\n'),
        ...fileLines.slice(blockEnd)
      ];
      fs.writeFileSync(filePath, newLines.join('\n'));
      fixedCount++;
      console.log(`[FIXED!] ${path.basename(filePath)} Line ${item.startLine}`);
    } else {
      console.log(`[STILL FAILING] ${path.basename(filePath)} Line ${item.startLine}`);
    }
  }

  console.log(`Fixed ${fixedCount} / ${errs.length} remaining diagrams!`);
}

fixFinal16().catch(console.error);
