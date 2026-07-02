import React from 'react';
import styles from './styles.module.css';

interface Stat {
  label: string;
  value: string;
}

interface CaseStudyHeaderProps {
  oneLiner: string;
  stats: Stat[];
}

export default function CaseStudyHeader({ oneLiner, stats }: CaseStudyHeaderProps): JSX.Element {
  return (
    <div className={styles.headerContainer}>
      <div className={styles.oneLinerBox}>
        {oneLiner}
      </div>
      <div className={styles.statsGrid}>
        {stats.map((stat, idx) => (
          <div key={idx} className={styles.statCard}>
            <span className={styles.statLabel}>{stat.label}</span>
            <span className={styles.statValue}>{stat.value}</span>
          </div>
        ))}
      </div>
    </div>
  );
}
