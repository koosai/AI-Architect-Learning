import React from 'react';
import styles from './styles.module.css';

interface ResearchNoteProps {
  title: string;
  source: string;
  href?: string;
  insight: string;
  application: string;
}

export default function ResearchNote({ title, source, href, insight, application }: ResearchNoteProps): JSX.Element {
  return (
    <div className={styles.noteCard}>
      <div className={styles.header}>
        <div className={styles.titleGroup}>
          <span className={styles.badge}>Research Note</span>
          <h4 className={styles.title}>{title}</h4>
          <div className={styles.source}>来源：{source}</div>
        </div>
        {href && (
          <a href={href} target="_blank" rel="noopener noreferrer" className={styles.paperLink}>
            <span>阅读原文</span>
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
              <path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"></path>
              <polyline points="15 3 21 3 21 9"></polyline>
              <line x1="10" y1="14" x2="21" y2="3"></line>
            </svg>
          </a>
        )}
      </div>
      <div className={styles.content}>
        <div className={styles.section}>
          <span className={styles.sectionTitle}>
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
              <path d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z"></path>
              <path d="M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z"></path>
            </svg>
            关键洞察 (Insight)
          </span>
          <div className={styles.sectionBody}>{insight}</div>
        </div>
        <div className={styles.section}>
          <span className={styles.sectionTitle}>
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
              <polygon points="12 2 2 7 12 12 22 7 12 2"></polygon>
              <polyline points="2 17 12 22 22 17"></polyline>
              <polyline points="2 12 12 17 22 12"></polyline>
            </svg>
            架构启示 (Application)
          </span>
          <div className={styles.sectionBody}>{application}</div>
        </div>
      </div>
    </div>
  );
}
