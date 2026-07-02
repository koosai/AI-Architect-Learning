import React from 'react';
import styles from './styles.module.css';

interface Prereq {
  label: string;
  href: string;
}

interface ChapterMetaProps {
  time?: string;
  prereqs?: Prereq[];
  outcome?: string;
  howToUse?: string;
}

export default function ChapterMeta({ time, prereqs, outcome, howToUse }: ChapterMetaProps): JSX.Element {
  return (
    <div className={styles.metaCard}>
      <div className={styles.metaGrid}>
        {time && (
          <div className={styles.metaSection}>
            <span className={styles.metaTitle}>
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
                <circle cx="12" cy="12" r="10"></circle>
                <polyline points="12 6 12 12 16 14"></polyline>
              </svg>
              建议学时
            </span>
            <span className={styles.metaContent}>{time}</span>
          </div>
        )}

        {prereqs && prereqs.length > 0 && (
          <div className={styles.metaSection}>
            <span className={styles.metaTitle}>
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
                <path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"></path>
                <path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"></path>
              </svg>
              前置知识
            </span>
            <div className={styles.metaContent}>
              {prereqs.map((prereq, index) => (
                <a key={index} href={prereq.href} className={styles.prereqLink}>
                  {prereq.label}
                </a>
              ))}
            </div>
          </div>
        )}

        {outcome && (
          <div className={styles.metaSection}>
            <span className={styles.metaTitle}>
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
                <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path>
                <polyline points="22 4 12 14.01 9 11.01"></polyline>
              </svg>
              学习目标
            </span>
            <span className={styles.metaContent}>{outcome}</span>
          </div>
        )}

        {howToUse && (
          <div className={styles.metaSection}>
            <span className={styles.metaTitle}>
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
                <circle cx="12" cy="12" r="10"></circle>
                <line x1="12" y1="16" x2="12" y2="12"></line>
                <line x1="12" y1="8" x2="12.01" y2="8"></line>
              </svg>
              避坑指南与学法
            </span>
            <span className={styles.metaContent}>{howToUse}</span>
          </div>
        )}
      </div>
    </div>
  );
}
