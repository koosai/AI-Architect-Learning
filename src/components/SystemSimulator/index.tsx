import React, { useState, useEffect } from 'react';
import styles from './styles.module.css';

interface SystemSimulatorProps {
  type: 'token-bucket' | 'consistent-hash' | 'cache-lru';
  params?: Record<string, any>;
}

export default function SystemSimulator({ type, params }: SystemSimulatorProps): JSX.Element {
  // Common states
  const [logs, setLogs] = useState<string[]>([]);
  const addLog = (msg: string) => {
    const time = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', second: '2-digit' });
    setLogs((prev) => [`[${time}] ${msg}`, ...prev].slice(0, 5));
  };

  // 1. Token Bucket states
  const capacity = params?.capacity || 8;
  const refillRate = params?.refillRate || 1; // token per second
  const [tokens, setTokens] = useState(capacity);

  useEffect(() => {
    if (type !== 'token-bucket') return;
    const timer = setInterval(() => {
      setTokens((prev) => Math.min(capacity, prev + refillRate));
    }, 1000);
    return () => clearInterval(timer);
  }, [type, capacity, refillRate]);

  const sendRequestToken = () => {
    if (tokens >= 1) {
      setTokens((prev) => prev - 1);
      addLog(`🟢 请求成功: 消耗 1 个令牌，剩余 ${tokens - 1} 个令牌`);
    } else {
      addLog(`🔴 请求受限: 桶内无令牌，限流拦截！`);
    }
  };

  // 2. Consistent Hashing states
  const [hashKey, setHashKey] = useState('user_128');
  const [keyAngle, setKeyAngle] = useState<number | null>(null);
  const [targetNode, setTargetNode] = useState<string | null>(null);

  // Hash nodes on ring
  const nodes = [
    { name: '节点 A', angle: 60, color: 'var(--brand-purple)' },
    { name: '节点 B', angle: 180, color: 'var(--brand-cyan)' },
    { name: '节点 C', angle: 300, color: 'var(--brand-yellow)' },
  ];

  const handleHash = () => {
    if (!hashKey) return;
    // Compute simple deterministic hash angle between 0 and 360
    let hash = 0;
    for (let i = 0; i < hashKey.length; i++) {
      hash = hashKey.charCodeAt(i) + ((hash << 5) - hash);
    }
    const angle = Math.abs(hash) % 360;
    setKeyAngle(angle);

    // Find first node clockwise (node.angle >= angle)
    // Ring is circular, so if angle is greater than all nodes, it wraps to the first node
    const sortedNodes = [...nodes].sort((a, b) => a.angle - b.angle);
    let matched = sortedNodes.find((n) => n.angle >= angle);
    if (!matched) matched = sortedNodes[0]; // wrap around

    setTargetNode(matched.name);
    addLog(`🔑 Key '${hashKey}' 哈希位置: ${angle}° ➜ 顺时针最近节点: ${matched.name} (${matched.angle}°)`);
  };

  // 3. LRU Cache states
  const [cache, setCache] = useState<string[]>(['A', 'B', 'C']);
  const [hitKey, setHitKey] = useState<string | null>(null);
  const [evictedKey, setEvictedKey] = useState<string | null>(null);

  const requestCacheKey = (key: string) => {
    setHitKey(null);
    setEvictedKey(null);

    const exists = cache.includes(key);
    if (exists) {
      // Hit: Move to front
      const filtered = cache.filter((k) => k !== key);
      setCache([key, ...filtered]);
      setHitKey(key);
      addLog(`🎯 Cache HIT: Key '${key}' 命中！已移动到队列最前 (MRU)`);
    } else {
      // Miss
      let newCache = [...cache];
      let evicted: string | null = null;
      if (cache.length >= 4) {
        evicted = newCache.pop() || null;
        setEvictedKey(evicted);
      }
      newCache = [key, ...newCache];
      setCache(newCache);
      addLog(`💨 Cache MISS: Key '${key}' 未命中。${evicted ? `淘汰末尾 (LRU) Key '${evicted}' 并` : ''}载入最前`);
    }
  };

  return (
    <div className={styles.card}>
      <h4 className={styles.title}>
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
          <polyline points="22 12 18 12 15 21 9 3 6 12 2 12"></polyline>
        </svg>
        {type === 'token-bucket' && '令牌桶限流模拟器 (Token Bucket)'}
        {type === 'consistent-hash' && '一致性哈希环模拟器 (Consistent Hashing)'}
        {type === 'cache-lru' && 'LRU 缓存淘汰机制模拟器 (LRU Cache)'}
      </h4>

      <div className={styles.simulatorContainer}>
        {/* Token Bucket UI */}
        {type === 'token-bucket' && (
          <>
            <div className={styles.controlPane}>
              <div>
                <strong>⚙️ 配置参数:</strong>
                <ul style={{ margin: '0.4rem 0 0 0', paddingLeft: '1.2rem', fontSize: '0.88rem' }}>
                  <li>桶最大容量: {capacity} 个</li>
                  <li>令牌填充率: {refillRate} 个/秒</li>
                </ul>
              </div>
              <button className={styles.btn} onClick={sendRequestToken}>
                ⚡ 发送高并发请求 (消耗 1 令牌)
              </button>
              <div className={styles.logBox}>
                {logs.length === 0 ? '等待操作...' : logs.map((log, i) => <div key={i}>{log}</div>)}
              </div>
            </div>
            <div className={styles.visualPane}>
              <div style={{ marginBottom: '0.5rem', fontWeight: 'bold', fontSize: '0.9rem' }}>
                令牌桶状态 (当前令牌: {tokens} / {capacity})
              </div>
              <div className={styles.bucketGraphic}>
                {Array.from({ length: tokens }).map((_, i) => (
                  <div key={i} className={styles.tokenDot} />
                ))}
              </div>
            </div>
          </>
        )}

        {/* Consistent Hash UI */}
        {type === 'consistent-hash' && (
          <>
            <div className={styles.controlPane}>
              <div style={{ display: 'flex', flexDirection: 'column', gap: '0.4rem' }}>
                <label style={{ fontSize: '0.88rem', fontWeight: 'bold' }}>输入请求的 Key 值:</label>
                <div style={{ display: 'flex', gap: '0.5rem' }}>
                  <input
                    type="text"
                    value={hashKey}
                    onChange={(e) => setHashKey(e.target.value)}
                    style={{ flex: 1, padding: '0.4rem', border: '1px solid var(--comp-border)', borderRadius: '6px', background: 'var(--comp-bg)', color: 'var(--comp-text)' }}
                  />
                  <button className={styles.btn} onClick={handleHash}>
                    计算哈希
                  </button>
                </div>
              </div>
              <div className={styles.logBox}>
                {logs.length === 0 ? '输入 Key 并计算哈希...' : logs.map((log, i) => <div key={i}>{log}</div>)}
              </div>
            </div>
            <div className={styles.visualPane}>
              <svg width="200" height="200" viewBox="0 0 200 200">
                {/* Hash Ring Circle */}
                <circle cx="100" cy="100" r="80" fill="none" stroke="var(--comp-border)" strokeWidth="3" />
                {/* Node Points on Ring */}
                {nodes.map((node, i) => {
                  const rad = (node.angle * Math.PI) / 180;
                  const cx = 100 + 80 * Math.cos(rad);
                  const cy = 100 + 80 * Math.sin(rad);
                  const isTarget = targetNode === node.name;
                  return (
                    <g key={i}>
                      <circle
                        cx={cx}
                        cy={cy}
                        r={isTarget ? 10 : 7}
                        fill={node.color}
                        stroke={isTarget ? '#ffffff' : 'none'}
                        strokeWidth="2"
                      />
                      <text
                        x={cx + (cx > 100 ? 12 : -45)}
                        y={cy + (cy > 100 ? 12 : -5)}
                        fontSize="10"
                        fill="var(--comp-text)"
                        fontWeight="bold"
                      >
                        {node.name} ({node.angle}°)
                      </text>
                    </g>
                  );
                })}
                {/* Key Point on Ring */}
                {keyAngle !== null && (() => {
                  const rad = (keyAngle * Math.PI) / 180;
                  const cx = 100 + 80 * Math.cos(rad);
                  const cy = 100 + 80 * Math.sin(rad);
                  return (
                    <g>
                      <line x1="100" y1="100" x2={cx} x2-attr={cx} y2={cy} stroke="var(--brand-red)" strokeWidth="1.5" strokeDasharray="3" />
                      <circle cx={cx} cy={cy} r="6" fill="var(--brand-red)" />
                      <text x={cx + (cx > 100 ? 8 : -30)} y={cy + 15} fontSize="9" fill="var(--brand-red)" fontWeight="bold">
                        Key ({keyAngle}°)
                      </text>
                    </g>
                  );
                })()}
              </svg>
            </div>
          </>
        )}

        {/* LRU Cache UI */}
        {type === 'cache-lru' && (
          <>
            <div className={styles.controlPane}>
              <div>
                <strong>🖱️ 点击 Key 模拟读写请求:</strong>
                <div style={{ display: 'flex', gap: '0.4rem', marginTop: '0.6rem', flexWrap: 'wrap' }}>
                  {['A', 'B', 'C', 'D', 'E', 'F'].map((k) => (
                    <button
                      key={k}
                      className={`${styles.btn} ${styles.btnSec}`}
                      onClick={() => requestCacheKey(k)}
                      style={{ padding: '0.4rem 0.8rem', minWidth: '40px' }}
                    >
                      Key {k}
                    </button>
                  ))}
                </div>
              </div>
              <div className={styles.logBox}>
                {logs.length === 0 ? '点击上面按键发送请求...' : logs.map((log, i) => <div key={i}>{log}</div>)}
              </div>
            </div>
            <div className={styles.visualPane}>
              <div style={{ marginBottom: '0.8rem', fontWeight: 'bold', fontSize: '0.9rem' }}>
                LRU 缓存队列 (容量: 4)
              </div>
              <div className={styles.cacheList}>
                {cache.map((key, index) => {
                  const isHit = hitKey === key;
                  let blockClass = styles.cacheBlock;
                  if (isHit) blockClass += ` ${styles.cacheBlockHit}`;
                  return (
                    <div key={key} className={blockClass}>
                      {key}
                      <span className={styles.cacheBadge}>
                        {index === 0 ? 'MRU' : index === cache.length - 1 ? 'LRU' : `#${index}`}
                      </span>
                    </div>
                  );
                })}
                {evictedKey && (
                  <div className={`${styles.cacheBlock} ${styles.cacheBlockEvicted}`}>
                    {evictedKey}
                    <span className={styles.cacheBadge} style={{ background: 'var(--brand-red)' }}>OUT</span>
                  </div>
                )}
                {cache.length === 0 && <span style={{ color: 'var(--comp-text-muted)', fontSize: '0.88rem' }}>缓存为空</span>}
              </div>
            </div>
          </>
        )}
      </div>
    </div>
  );
}
