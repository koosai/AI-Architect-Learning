import React, { useState } from 'react';
import styles from './styles.module.css';

interface LatencyItem {
  name: string;
  ns: number;
  label: string;
  humanLabel: string;
  icon: string;
}

export default function LatencyNumbers(): JSX.Element {
  const [scale, setScale] = useState<'system' | 'human'>('system');

  const items: LatencyItem[] = [
    { name: 'L1 缓存引用', ns: 0.5, label: '0.5 ns', humanLabel: '1.6 秒 (眨眼间)', icon: '⚡' },
    { name: 'L2 缓存引用', ns: 7, label: '7 ns', humanLabel: '23 秒 (倒杯水)', icon: '🏃' },
    { name: '主内存访问', ns: 100, label: '100 ns', humanLabel: '5.5 分钟 (冲杯咖啡)', icon: '🧠' },
    { name: 'SSD 随机读取', ns: 16000, label: '16,000 ns (16 μs)', humanLabel: '15 小时 (睡一觉)', icon: '💾' },
    { name: '同机房网络往返 (RTT)', ns: 500000, label: '500,000 ns (0.5 ms)', humanLabel: '19 天 (深度旅游)', icon: '🏢' },
    { name: '机械硬盘寻道', ns: 10000000, label: '10,000,000 ns (10 ms)', humanLabel: '1 年 (等庄稼收割)', icon: '💿' },
    { name: '跨大西洋网络往返', ns: 150000000, label: '150,000,000 ns (150 ms)', humanLabel: '15 年 (等孩子长大)', icon: '🌎' },
  ];

  // We will use log base 10 scale for width display to avoid massive skew while showing scale variations
  // min ns is 0.5 (log10 is -0.3), max ns is 150,000,000 (log10 is 8.17)
  const getBarWidth = (ns: number) => {
    const minLog = Math.log10(0.5);
    const maxLog = Math.log10(150000000);
    const valLog = Math.log10(ns);
    const percent = ((valLog - minLog) / (maxLog - minLog)) * 100;
    return `${Math.max(5, percent)}%`;
  };

  return (
    <div className={styles.card}>
      <div className={styles.header}>
        <h4 className={styles.title}>
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
            <circle cx="12" cy="12" r="10"></circle>
            <polyline points="12 6 12 12 16 14"></polyline>
          </svg>
          延迟数量级对照表 (Jeff Dean 经典指标)
        </h4>
        <div className={styles.toggleContainer}>
          <button
            className={`${styles.toggleBtn} ${scale === 'system' ? styles.toggleBtnActive : ''}`}
            onClick={() => setScale('system')}
          >
            系统尺度
          </button>
          <button
            className={`${styles.toggleBtn} ${scale === 'human' ? styles.toggleBtnActive : ''}`}
            onClick={() => setScale('human')}
          >
            人类尺度
          </button>
        </div>
      </div>

      <table className={styles.table}>
        <tbody>
          {items.map((item, idx) => (
            <tr key={idx} className={styles.row}>
              <td className={styles.cell + ' ' + styles.cellName}>
                <span>{item.icon} </span>
                {item.name}
              </td>
              <td className={styles.cell + ' ' + styles.cellScale}>
                {scale === 'system' ? item.label : item.humanLabel}
              </td>
              <td className={styles.cell + ' ' + styles.cellBar}>
                <div className={styles.barTrack}>
                  <div
                    className={styles.barFill}
                    style={{ width: getBarWidth(item.ns) }}
                  />
                </div>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
      <div style={{ marginTop: '0.8rem', fontSize: '0.8rem', color: 'var(--comp-text-muted)', fontStyle: 'italic' }}>
        * 💡 人类尺度换算公式：将 1 个 CPU 时钟周期 (约 0.3 ns) 放大为 1 秒。
      </div>
    </div>
  );
}
