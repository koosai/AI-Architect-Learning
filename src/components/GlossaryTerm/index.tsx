import React from 'react';
import styles from './styles.module.css';

interface GlossaryTermProps {
  term: string;
  definition: string;
  children: React.ReactNode;
}

export default function GlossaryTerm({ term, definition, children }: GlossaryTermProps): JSX.Element {
  return (
    <span className={styles.termWrapper}>
      {children}
      <span className={styles.tooltip}>
        <div className={styles.tooltipHeader}>{term}</div>
        <div>{definition}</div>
        <div className={styles.tooltipArrow}>
          <div className={styles.tooltipArrowInner} />
        </div>
      </span>
    </span>
  );
}
