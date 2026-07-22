import fs from 'fs';
import path from 'path';
import { JSDOM } from 'jsdom';

// Initialize JSDOM environment safely
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
} catch (e) {
  // ignore if getter exists
}

async function testDiagrams() {
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

  const allFiles = getAllFiles(docsDir);
  console.log(`Scanning ${allFiles.length} files for Mermaid diagrams...`);

  let totalDiagrams = 0;
  let failedDiagrams = [];

  for (const filePath of allFiles) {
    const content = fs.readFileSync(filePath, 'utf-8');
    const lines = content.split('\n');
    
    let inMermaid = false;
    let mermaidLines = [];
    let startLine = 0;

    for (let i = 0; i < lines.length; i++) {
      const line = lines[i];
      if (line.trim().startsWith('```mermaid')) {
        inMermaid = true;
        mermaidLines = [];
        startLine = i + 1;
        continue;
      }

      if (inMermaid && line.trim().startsWith('```')) {
        inMermaid = false;
        totalDiagrams++;
        const code = mermaidLines.join('\n');
        
        try {
          // Test with real mermaid parse
          await mermaid.parse(code);
        } catch (err) {
          failedDiagrams.push({
            file: filePath,
            startLine,
            error: err.message || String(err),
            code,
          });
        }
        continue;
      }

      if (inMermaid) {
        mermaidLines.push(line);
      }
    }
  }

  console.log(`\n================ SUMMARY ================`);
  console.log(`Total diagrams tested: ${totalDiagrams}`);
  console.log(`Total failed diagrams: ${failedDiagrams.length}`);
  console.log(`=========================================\n`);

  if (failedDiagrams.length > 0) {
    fs.writeFileSync(
      'c:/Users/K.K/OneDrive/Desktop/AI架构师教程/mermaid_errors.json',
      JSON.stringify(failedDiagrams, null, 2)
    );
    for (const f of failedDiagrams) {
      console.log(`\n[FAIL] File: ${f.file}:${f.startLine}`);
      console.log(`Error: ${f.error.split('\n')[0]}`);
    }
  }
}

testDiagrams().catch(console.error);
