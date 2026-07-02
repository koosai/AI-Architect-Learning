import React, { useState } from 'react';
import styles from './styles.module.css';

export default function PercentileLab(): JSX.Element {
  const defaultLatencies = [5, 6, 4, 7, 5, 8, 4, 6, 5, 6];
  const [latencies, setLatencies] = useState<number[]>(defaultLatencies);

  const addFast = () => {
    if (latencies.length >= 24) return;
    const ms = Math.floor(Math.random() * 5) + 4; // 4 - 8 ms
    setLatencies([...latencies, ms]);
  };

  const addSlow = () => {
    if (latencies.length >= 24) return;
    const ms = Math.floor(Math.random() * 200) + 400; // 400 - 600 ms
    setLatencies([...latencies, ms]);
  };

  const reset = () => {
    setLatencies(defaultLatencies);
  };

  // Math Helpers
  const sorted = [...latencies].sort((a, b) => a - b);
  const avg = Math.round((latencies.reduce((acc, v) => acc + v, 0) / latencies.length) * 10) / 10;
  
  const getPercentile = (p: number) => {
    if (sorted.length === 0) return 0;
    const idx = Math.ceil((p / 100) * sorted.length) - 1;
    return sorted[Math.max(0, idx)];
  };

  const p50 = getPercentile(50);
  const p90 = getPercentile(90);
  const p99 = getPercentile(99);

  const maxVal = Math.max(...latencies, 10);

  return (
    <div className={styles.card}>
      <h4 className={styles.title}>
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
          <line x1="18" y1="20" x2="18" y2="10"></line>
          <line x1="12" y1="20" x2="12" y2="4"></line>
          <line x1="6" y1="20" x2="6" y2="14"></line>
        </svg>
        分位数 (Percentiles) vs 平均数 (Average) 实验器
      </h4>

      <div className={styles.controls}>
        <div className={styles.controlGroup}>
          <button className={styles.btn} onClick={addFast} disabled={latencies.length >= 24}>
            ➕ 添加正常请求 (4-8ms)
          </button>
          <button className={styles.btn} style={{ backgroundColor: 'var(--brand-red)' }} onClick={addSlow} disabled={latencies.length >= 24}>
            ⚠️ 添加长尾请求 (400-600ms)
          </button>
        </div>
        <button className={`${styles.btn} ${styles.btnReset}`} onClick={reset}>
          重置
        </button>
      </div>

      <div className={styles.metricsGrid}>
        <div className={styles.metricBox} style={{ borderTop: '3px solid var(--comp-text-muted)' }}>
          <div className={styles.metricTitle}>总请求数</div>
          <div className={styles.metricVal}>{latencies.length}</div>
        </div>
        <div className={styles.metricBox} style={{ borderTop: '3px solid var(--brand-blue)' }}>
          <div className={styles.metricTitle}>平均延迟 (Average)</div>
          <div className={styles.metricVal} style={{ color: 'var(--brand-blue)' }}>{avg} ms</div>
        </div>
        <div className={styles.metricBox} style={{ borderTop: '3px solid var(--brand-cyan)' }}>
          <div className={styles.metricTitle}>中位数 (p50)</div>
          <div className={styles.metricVal} style={{ color: 'var(--brand-cyan)' }}>{p50} ms</div>
        </div>
        <div className={styles.metricBox} style={{ borderTop: '3px solid var(--brand-yellow)' }}>
          <div className={styles.metricTitle}>p90 分位数</div>
          <div className={styles.metricVal} style={{ color: 'var(--brand-yellow)' }}>{p90} ms</div>
        </div>
        <div className={styles.metricBox} style={{ borderTop: '3px solid var(--brand-red)' }}>
          <div className={styles.metricTitle}>p99 分位数</div>
          <div className={styles.metricVal} style={{ color: 'var(--brand-red)' }}>{p99} ms</div>
        </div>
      </div>

      <div className={styles.chartArea}>
        {latencies.map((val, idx) => {
          const heightPercent = (val / maxVal) * 100;
          const isSlow = val > 10;
          return (
            <div key={idx} className={styles.chartBarContainer}>
              <div
                className={`${styles.chartBar} ${isSlow ? styles.chartBarSlow : ''}`}
                style={{ height: `${Math.max(4, heightPercent)}%` }}
              >
                <div className={styles.tooltip}>{val} ms</div>
              </div>
              <span className={styles.barLabel}>R{idx + 1}</span>
            </div>
          );
        })}
      </div>
      <div style={{ fontSize: '0.82rem', color: 'var(--comp-text-muted)', lineHeight: 1.4 }}>
        💡 <strong>架构心智</strong>：试着加入 1-2 个“长尾请求”。你会发现**平均值和 p50 (中位数) 几乎没有变化**，但 **p90 和 p99 会立即飙升**。在实际的高并发架构中，如果 1% 的请求极慢，虽然“平均延迟”好看，但对于访问几十个服务的用户来说，最终体验就是 100% 变慢。所以架构设计必须“看分位数，而非平均值”。
      </div>
    </div>
  );
}
