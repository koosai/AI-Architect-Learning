import React, { useState } from 'react';
import styles from './styles.module.css';

export function CacheSimulator(): JSX.Element {
  const [dbVal, setDbVal] = useState('Alice');
  const [cacheVal, setCacheVal] = useState<string | null>(null);
  const [logs, setLogs] = useState<string[]>([]);
  const [activeNode, setActiveNode] = useState<'none' | 'cache' | 'db'>('none');
  const [newValue, setNewValue] = useState('Bob');

  const addLog = (msg: string) => {
    const time = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', second: '2-digit' });
    setLogs((prev) => [`[${time}] ${msg}`, ...prev].slice(0, 5));
  };

  const handleRead = () => {
    setActiveNode('cache');
    addLog('🔍 客户端发起读请求: 检查 Redis 缓存...');
    
    setTimeout(() => {
      if (cacheVal !== null) {
        addLog(`🎯 缓存命中 (Cache HIT): 直接从缓存返回数据 "${cacheVal}"`);
        setActiveNode('none');
      } else {
        addLog('💨 缓存未命中 (Cache MISS): 缓存中无数据，转向数据库查询...');
        setActiveNode('db');
        
        setTimeout(() => {
          addLog(`🗄️ 数据库查询成功: 得到数据 "${dbVal}"`);
          addLog(`🔄 写入缓存 (Write-Back): 将数据 "${dbVal}" 写入 Redis 缓存`);
          setCacheVal(dbVal);
          setActiveNode('none');
        }, 1000);
      }
    }, 1000);
  };

  const handleWrite = () => {
    setActiveNode('db');
    addLog(`✍️ 客户端写入更新: 数据库写入新值 "${newValue}"`);
    setDbVal(newValue);
    
    setTimeout(() => {
      addLog('🗑️ 缓存失效操作 (Invalidate): 从 Redis 缓存中删除旧 Key');
      setCacheVal(null);
      setActiveNode('none');
      
      // Update new value suggestion for next writes
      setNewValue((prev) => (prev === 'Bob' ? 'Charlie' : 'Bob'));
    }, 1000);
  };

  return (
    <div className={styles.card}>
      <h4 className={styles.title}>Cache-Aside (旁路缓存) 读写路径模拟器</h4>
      
      <div className={styles.layout}>
        <div className={styles.controls}>
          <div style={{ display: 'flex', gap: '0.5rem' }}>
            <button className={styles.btn} onClick={handleRead}>
              📖 读取数据 (Read Request)
            </button>
          </div>

          <div className={styles.inputGroup}>
            <label className={styles.inputLabel}>更新数据库新值 (New Value):</label>
            <div style={{ display: 'flex', gap: '0.5rem' }}>
              <input
                type="text"
                value={newValue}
                onChange={(e) => setNewValue(e.target.value)}
                className={styles.inputText}
                style={{ flex: 1 }}
              />
              <button className={`${styles.btn} ${styles.btnSec}`} onClick={handleWrite}>
                ✍️ 更新数据 (Write Request)
              </button>
            </div>
          </div>

          <div className={styles.logBox}>
            {logs.length === 0 ? (
              <div style={{ color: 'var(--comp-text-muted)' }}>点击操作按钮模拟读写流向...</div>
            ) : (
              logs.map((log, idx) => <div key={idx}>{log}</div>)
            )}
          </div>
        </div>

        <div className={styles.visuals}>
          <div className={`${styles.node} ${activeNode === 'cache' ? styles.nodeActive : ''}`}>
            🏎️ Redis 缓存
            <div className={styles.nodeState}>
              状态: {cacheVal !== null ? `"${cacheVal}"` : '空 (Empty/Evicted)'}
            </div>
          </div>

          <div className={styles.arrow}>⇅</div>

          <div className={`${styles.node} ${activeNode === 'db' ? styles.nodeActive : ''}`}>
            🗄️ 数据库 (DB)
            <div className={styles.nodeState}>
              真实数据: "{dbVal}"
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
