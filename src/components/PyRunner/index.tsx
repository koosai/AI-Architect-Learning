import React, { useState, useEffect, useRef } from 'react';
import styles from './styles.module.css';

interface PyRunnerProps {
  code: string;
  rows?: number;
  expect?: string;
}

declare global {
  interface Window {
    loadPyodide?: any;
    pyodideInstance?: any;
  }
}

export default function PyRunner({ code: initialCode, rows = 12, expect }: PyRunnerProps): JSX.Element {
  const cleanCode = initialCode.replace(/^\r?\n/, '').trimEnd();
  const [code, setCode] = useState(cleanCode);
  const [output, setOutput] = useState('');
  const [status, setStatus] = useState<'idle' | 'loading' | 'running' | 'completed' | 'error'>('idle');
  const [progress, setProgress] = useState(0);
  const [verifyPassed, setVerifyPassed] = useState(false);
  const outputRef = useRef<string>('');

  const lineCount = code.split('\n').length;
  const areaRows = Math.max(rows, lineCount);
  const lineNumbers = Array.from({ length: areaRows }, (_, i) => i + 1);

  const resetCode = () => {
    setCode(cleanCode);
    setOutput('');
    setStatus('idle');
    setVerifyPassed(false);
  };

  const runCode = async () => {
    setStatus('loading');
    setProgress(10);
    outputRef.current = '';
    setOutput('正在初始化 Python 运行时...');

    try {
      // 1. Load pyodide script if not present
      if (!window.loadPyodide) {
        setProgress(30);
        await new Promise<void>((resolve, reject) => {
          const script = document.createElement('script');
          script.src = '/pyodide/pyodide.js';
          script.onload = () => resolve();
          script.onerror = () => reject(new Error('无法加载 Pyodide，请确认已放入 static/pyodide/ 目录并且处于离线部署环境'));
          document.head.appendChild(script);
        });
      }

      setProgress(60);
      // 2. Initialize pyodide instance if not present
      if (!window.pyodideInstance) {
        window.pyodideInstance = await window.loadPyodide({
          indexURL: '/pyodide/',
        });
      }

      setProgress(90);
      const py = window.pyodideInstance;

      // 3. Setup redirect for print statements and stderr
      py.setStdout({
        batched: (text: string) => {
          outputRef.current += text + '\n';
          setOutput(outputRef.current);
        },
      });
      py.setStderr({
        batched: (text: string) => {
          outputRef.current += text + '\n';
          setOutput(outputRef.current);
        },
      });

      setStatus('running');
      // 4. Run Python code
      const result = await py.runPythonAsync(code);
      
      let finalOut = outputRef.current;
      if (result !== undefined && result !== null && typeof result.toString === 'function') {
        const resStr = result.toString();
        if (resStr !== 'None' && resStr !== '') {
          finalOut += `\n[返回值] ${resStr}`;
        }
      }

      if (!finalOut) {
        finalOut = '代码运行成功，无输出。';
      }

      setOutput(finalOut);
      setStatus('completed');

      // 5. Verify expectations if any
      if (expect) {
        // Look for expectation in stdout or result string
        const lowerOut = finalOut.toLowerCase();
        const lowerExpect = expect.toLowerCase();
        if (lowerOut.includes(lowerExpect)) {
          setVerifyPassed(true);
        } else {
          setVerifyPassed(false);
        }
      }
    } catch (err: any) {
      const errMsg = err.message || String(err);
      setOutput(`错误:\n${errMsg}`);
      setStatus('error');
      setVerifyPassed(false);
      // Reset corrupted pyodide instance if Pyodide process exited
      if (errMsg.includes('terminated with exit')) {
        window.pyodideInstance = null;
      }
    }
  };

  return (
    <div className={styles.runnerContainer}>
      <div className={styles.editorHeader}>
        <div className={styles.editorTitle}>
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
            <polygon points="5 3 19 12 5 21 5 3"></polygon>
          </svg>
          交互式 Python 实验环境
        </div>
        <div className={styles.buttonGroup}>
          {status === 'loading' && (
            <div className={styles.loadingSpinner}>
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="3" strokeLinecap="round" className="animate-spin" style={{ animation: 'spin 1s linear infinite' }}>
                <circle cx="12" cy="12" r="10" strokeDasharray="30" strokeDashoffset="10"></circle>
              </svg>
              正在加载 ({progress}%)
            </div>
          )}
          <button
            className={`${styles.actionBtn} ${styles.runBtn}`}
            onClick={runCode}
            disabled={status === 'loading' || status === 'running'}
          >
            运行代码
          </button>
          <button className={`${styles.actionBtn} ${styles.resetBtn}`} onClick={resetCode}>
            重置
          </button>
        </div>
      </div>

      <div className={styles.editorArea}>
        <div className={styles.lineNumberCol}>
          {lineNumbers.map((n) => (
            <div key={n}>{n}</div>
          ))}
        </div>
        <textarea
          className={styles.textarea}
          value={code}
          onChange={(e) => setCode(e.target.value)}
          rows={areaRows}
          spellCheck={false}
        />
      </div>

      <div className={styles.console}>
        <div className={styles.consoleHeader}>
          <span>运行输出 Console</span>
          {status === 'completed' && <span style={{ color: 'var(--brand-green)' }}>● Success</span>}
          {status === 'error' && <span style={{ color: 'var(--brand-red)' }}>● Error</span>}
        </div>
        <div className={styles.consoleOutput}>{output || '点击“运行代码”查看输出结果...'}</div>

        {verifyPassed && expect && (
          <div className={styles.successBanner}>
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="3" strokeLinecap="round" strokeLinejoin="round">
              <polyline points="20 6 9 17 4 12"></polyline>
            </svg>
            <span>符合预期目标: <strong>{expect}</strong></span>
          </div>
        )}
      </div>
    </div>
  );
}
