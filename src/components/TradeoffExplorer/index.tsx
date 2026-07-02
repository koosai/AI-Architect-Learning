import React, { useState } from 'react';
import styles from './styles.module.css';

interface Option {
  name: string;
  scores: number[];
  note: string;
  whenToUse: string;
}

interface TradeoffExplorerProps {
  title: string;
  dimensions: string[];
  options: Option[];
}

export default function TradeoffExplorer({ title, dimensions, options }: TradeoffExplorerProps): JSX.Element {
  const [activeIdx, setActiveIdx] = useState(0);
  const activeOption = options[activeIdx] || options[0];

  const getBarColor = (score: number) => {
    if (score >= 4) return 'var(--brand-green)';
    if (score >= 3) return 'var(--ifm-color-primary)';
    if (score >= 2) return 'var(--brand-yellow)';
    return 'var(--brand-red)';
  };

  return (
    <div className={styles.explorerCard}>
      <h4 className={styles.title}>
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
          <line x1="18" y1="20" x2="18" y2="10"></line>
          <line x1="12" y1="20" x2="12" y2="4"></line>
          <line x1="6" y1="20" x2="6" y2="14"></line>
        </svg>
        {title}
      </h4>

      <div className={styles.layout}>
        <div className={styles.optionsPane}>
          {options.map((option, idx) => (
            <button
              key={idx}
              className={`${styles.optionBtn} ${idx === activeIdx ? styles.optionBtnActive : ''}`}
              onClick={() => setActiveIdx(idx)}
            >
              <span>{option.name}</span>
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
                <polyline points="9 18 15 12 9 6"></polyline>
              </svg>
            </button>
          ))}
        </div>

        {activeOption && (
          <div className={styles.detailsPane}>
            <div>
              <p className={styles.noteText}>{activeOption.note}</p>
            </div>

            <div className={styles.whenToUseBox}>
              <div className={styles.whenToUseTitle}>适用场景</div>
              <p className={styles.whenToUseText}>{activeOption.whenToUse}</p>
            </div>

            <div className={styles.scoresList}>
              {dimensions.map((dim, idx) => {
                const score = activeOption.scores[idx] || 0;
                const percentage = Math.min(100, Math.max(0, (score / 5) * 100));
                return (
                  <div key={idx} className={styles.scoreRow}>
                    <div className={styles.scoreLabelRow}>
                      <span>{dim}</span>
                      <span>{score} / 5</span>
                    </div>
                    <div className={styles.barTrack}>
                      <div
                        className={styles.barFill}
                        style={{
                          width: `${percentage}%`,
                          backgroundColor: getBarColor(score),
                        }}
                      />
                    </div>
                  </div>
                );
              })}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
