import React, { useState } from 'react';
import styles from './styles.module.css';

type NodeState = 'idle' | 'active' | 'passed' | 'failed';

export default function FailureLab(): JSX.Element {
  const [emptyInput, setEmptyInput] = useState(false);
  const [invalidEmail, setInvalidEmail] = useState(false);
  const [duplicateEmail, setDuplicateEmail] = useState(false);
  const [dbDown, setDbDown] = useState(false);

  const [activeStep, setActiveStep] = useState<number>(-1); // -1 = idle, 0 = Client, 1 = Boundary, 2 = State, 3 = Storage, 4 = Logs
  const [nodeStates, setNodeStates] = useState<NodeState[]>(['idle', 'idle', 'idle', 'idle']);
  const [isSimulating, setIsSimulating] = useState(false);

  const [blockedLayer, setBlockedLayer] = useState('无');
  const [userMsg, setUserMsg] = useState('等待发送请求...');
  const [logText, setLogText] = useState('日志留空...');

  const runSimulation = () => {
    if (isSimulating) return;
    setIsSimulating(true);
    setActiveStep(0);
    setNodeStates(['active', 'idle', 'idle', 'idle']);
    setBlockedLayer('无');
    setUserMsg('正在发送请求...');
    setLogText('[INFO] Request initialized from client...');

    // Flow simulation timeline
    // Step 0: Client sending request
    setTimeout(() => {
      // Step 1: Boundary check
      setActiveStep(1);
      if (emptyInput || invalidEmail) {
        setNodeStates(['passed', 'failed', 'idle', 'idle']);
        setBlockedLayer('Boundary (边界校验)');
        if (emptyInput) {
          setUserMsg('注册失败：姓名不能为空');
          setLogText('[WARNING] Signup rejected at boundary: empty name. IP=127.0.0.1 status=400');
        } else {
          setUserMsg('注册失败：邮箱格式不正确');
          setLogText('[WARNING] Signup rejected at boundary: invalid email format user@bad. IP=127.0.0.1 status=400');
        }
        setIsSimulating(false);
        return;
      }
      setNodeStates(['passed', 'passed', 'idle', 'idle']);
      setLogText((prev) => prev + '\n[INFO] Boundary check passed. Initiating state check...');

      // Step 2: State deduplication check
      setTimeout(() => {
        setActiveStep(2);
        if (duplicateEmail) {
          setNodeStates(['passed', 'passed', 'failed', 'idle']);
          setBlockedLayer('State (重复提交校验)');
          setUserMsg('您已提交过报名，请勿重复操作');
          setLogText((prev) => prev + '\n[INFO] Deduplication hit: email already exists. Returning cached record. status=200 (idempotent)');
          setIsSimulating(false);
          return;
        }
        setNodeStates(['passed', 'passed', 'passed', 'idle']);
        setLogText((prev) => prev + '\n[INFO] Deduplication check passed. Writing record to database...');

        // Step 3: Storage save check
        setTimeout(() => {
          setActiveStep(3);
          if (dbDown) {
            setNodeStates(['passed', 'passed', 'passed', 'failed']);
            setBlockedLayer('Storage (数据库存储)');
            setUserMsg('系统繁忙，请稍后再试');
            setLogText((prev) => prev + '\n[ERROR] Connection timeout with PostgreSQL cluster. StorageError raised. status=500');
            setIsSimulating(false);
            return;
          }
          setNodeStates(['passed', 'passed', 'passed', 'passed']);
          setBlockedLayer('无 (成功)');
          setUserMsg('注册成功！');
          setLogText((prev) => prev + '\n[INFO] Storage success. Record saved. id=user_827f\n[INFO] Signup success. status=201');
          setIsSimulating(false);
        }, 1000);
      }, 1000);
    }, 1000);
  };

  const getArrowStyle = (stepIndex: number) => {
    if (activeStep >= stepIndex) return `${styles.flowArrow} ${styles.flowArrowActive}`;
    return styles.flowArrow;
  };

  const getNodeStyle = (index: number, state: NodeState) => {
    let base = styles.flowNode;
    if (state === 'active') base += ` ${styles.flowNodeActive}`;
    if (state === 'passed') base += ` ${styles.flowNodePassed}`;
    if (state === 'failed') base += ` ${styles.flowNodeFailed}`;
    return base;
  };

  return (
    <div className={styles.card}>
      <div className={styles.togglesGrid}>
        <label className={styles.toggleLabel}>
          <span className={styles.switch}>
            <input type="checkbox" checked={emptyInput} onChange={(e) => setEmptyInput(e.target.checked)} disabled={isSimulating} />
            <span className={styles.slider}></span>
          </span>
          <span>空输入</span>
        </label>

        <label className={styles.toggleLabel}>
          <span className={styles.switch}>
            <input type="checkbox" checked={invalidEmail} onChange={(e) => setInvalidEmail(e.target.checked)} disabled={isSimulating} />
            <span className={styles.slider}></span>
          </span>
          <span>非法邮箱</span>
        </label>

        <label className={styles.toggleLabel}>
          <span className={styles.switch}>
            <input type="checkbox" checked={duplicateEmail} onChange={(e) => setDuplicateEmail(e.target.checked)} disabled={isSimulating} />
            <span className={styles.slider}></span>
          </span>
          <span>重复邮箱</span>
        </label>

        <label className={styles.toggleLabel}>
          <span className={styles.switch}>
            <input type="checkbox" checked={dbDown} onChange={(e) => setDbDown(e.target.checked)} disabled={isSimulating} />
            <span className={styles.slider}></span>
          </span>
          <span>数据库宕机</span>
        </label>
      </div>

      <div className={styles.btnRow}>
        <button onClick={runSimulation} className={styles.sendBtn} disabled={isSimulating}>
          {isSimulating ? '模拟运行中...' : '发送注册请求'}
        </button>
      </div>

      <div className={styles.flowDiagram}>
        <div className={getNodeStyle(0, nodeStates[0])}>
          📱 客户端 Client
        </div>
        <div className={getArrowStyle(1)}>➔</div>
        <div className={getNodeStyle(1, nodeStates[1])}>
          🛡️ 边界校验 Boundary
        </div>
        <div className={getArrowStyle(2)}>➔</div>
        <div className={getNodeStyle(2, nodeStates[2])}>
          ⚙️ 状态校验 State
        </div>
        <div className={getArrowStyle(3)}>➔</div>
        <div className={getNodeStyle(3, nodeStates[3])}>
          💾 数据库存储 Storage
        </div>
      </div>

      <div className={styles.resultsGrid}>
        <div className={styles.resultBox} style={{ borderLeft: '3px solid var(--brand-purple)' }}>
          <div className={styles.resultTitle}>🔒 被阻断层</div>
          <p className={styles.resultText} style={{ fontWeight: 'bold' }}>{blockedLayer}</p>
        </div>

        <div className={styles.resultBox} style={{ borderLeft: '3px solid var(--brand-blue)' }}>
          <div className={styles.resultTitle}>💬 用户看到</div>
          <p className={styles.resultText}>{userMsg}</p>
        </div>

        <div className={styles.resultBox} style={{ borderLeft: '3px solid var(--brand-yellow)', gridColumn: 'span 2' }}>
          <div className={styles.resultTitle}>📝 系统日志 (Observability)</div>
          <pre className={styles.resultText} style={{ fontFamily: 'monospace', whiteSpace: 'pre-wrap', fontSize: '0.82rem' }}>{logText}</pre>
        </div>
      </div>
    </div>
  );
}
