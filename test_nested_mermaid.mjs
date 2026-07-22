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

const allFiles = getAllFiles(docsDir);
console.log(`Checking ${allFiles.length} files...`);

for (const fp of allFiles) {
  const content = fs.readFileSync(fp, 'utf-8');
  const lines = content.split('\n');

  let inMermaid = false;
  let mermaidLines = [];
  let startLine = 0;

  for (let i = 0; i < lines.length; i++) {
    const line = lines[i];
    if (line.trim().startsWith('```mermaid')) {
      if (inMermaid) {
        console.log(`[NESTED MERMAID] ${path.basename(fp)} Line ${i+1}`);
      }
      inMermaid = true;
      mermaidLines = [];
      startLine = i + 1;
      continue;
    }

    if (inMermaid && line.trim().startsWith('```')) {
      inMermaid = false;
      const code = mermaidLines.join('\n');
      try {
        await mermaid.parse(code);
      } catch (err) {
        console.log(`[FAILING DIAGRAM] ${path.basename(fp)} Line ${startLine}: ${err.message.split('\n')[0]}`);
      }
      continue;
    }

    if (inMermaid) {
      mermaidLines.push(line);
    }
  }
}
