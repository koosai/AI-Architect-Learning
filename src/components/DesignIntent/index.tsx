import React from 'react';
import styles from './styles.module.css';

interface DesignIntentProps {
  problem: string;
  users: string;
  devices: string;
  goals: string[];
  constraints: string[];
  firstStep: string;
}

export default function DesignIntent({
  problem,
  users,
  devices,
  goals,
  constraints,
  firstStep,
}: DesignIntentProps): JSX.Element {
  return (
    <div className={styles.card}>
      <h4 className={styles.title}>
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
          <circle cx="12" cy="12" r="10"></circle>
          <line x1="12" y1="16" x2="12" y2="12"></line>
          <line x1="12" y1="8" x2="12.01" y2="8"></line>
        </svg>
        系统设计初衷 & 意图
      </h4>

      <div className={styles.introGrid}>
        <div className={styles.box}>
          <span className={styles.label}>
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
              <path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"></path>
              <line x1="12" y1="9" x2="12" y2="13"></line>
              <line x1="12" y1="17" x2="12.01" y2="17"></line>
            </svg>
            核心痛点/问题
          </span>
          <p className={styles.text}>{problem}</p>
        </div>

        <div className={styles.box}>
          <span className={styles.label}>
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
              <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path>
              <circle cx="9" cy="7" r="4"></circle>
              <path d="M23 21v-2a4 4 0 0 0-3-3.87"></path>
              <path d="M16 3.13a4 4 0 0 1 0 7.75"></path>
            </svg>
            目标用户
          </span>
          <p className={styles.text}>{users}</p>
        </div>

        <div className={styles.box}>
          <span className={styles.label}>
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
              <rect x="2" y="3" width="20" height="14" rx="2" ry="2"></rect>
              <line x1="8" y1="21" x2="16" y2="21"></line>
              <line x1="12" y1="17" x2="12" y2="21"></line>
            </svg>
            终端设备/运行环境
          </span>
          <p className={styles.text}>{devices}</p>
        </div>
      </div>

      <div className={styles.goalsConstraints}>
        <div className={styles.listSection}>
          <span className={`${styles.listSectionTitle} text-emerald-500`}>
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round" style={{ color: 'var(--brand-green)' }}>
              <polyline points="22 11.08 12 14.01 9 11.01"></polyline>
              <circle cx="12" cy="12" r="10"></circle>
            </svg>
            核心设计目标
          </span>
          <ul className={styles.list}>
            {goals.map((goal, idx) => (
              <li key={idx} className={styles.listItem}>
                <span className={styles.bullet} style={{ color: 'var(--brand-green)' }}>✓</span>
                <span>{goal}</span>
              </li>
            ))}
          </ul>
        </div>

        <div className={styles.listSection}>
          <span className={`${styles.listSectionTitle} text-rose-500`}>
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round" style={{ color: 'var(--brand-red)' }}>
              <circle cx="12" cy="12" r="10"></circle>
              <line x1="15" y1="9" x2="9" y2="15"></line>
              <line x1="9" y1="9" x2="15" y2="15"></line>
            </svg>
            技术约束/边界
          </span>
          <ul className={styles.list}>
            {constraints.map((constraint, idx) => (
              <li key={idx} className={styles.listItem}>
                <span className={styles.bullet} style={{ color: 'var(--brand-red)' }}>⚠</span>
                <span>{constraint}</span>
              </li>
            ))}
          </ul>
        </div>
      </div>

      <div className={styles.firstStepSection}>
        <span className={styles.label}>
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
            <polyline points="22 2 15 22 11 13 2 9 22 2"></polyline>
          </svg>
          突破口 (Strategic First Step)
        </span>
        <p className={styles.text} style={{ fontWeight: 550 }}>{firstStep}</p>
      </div>
    </div>
  );
}
