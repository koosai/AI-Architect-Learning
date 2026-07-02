import React, { useState } from 'react';
import styles from './styles.module.css';

interface Comp {
  label: string;
  isNew?: boolean;
}

interface Layer {
  name: string;
  comps: Comp[];
}

interface Era {
  year: string;
  title: string;
  intent: string;
  change: string;
  why: string;
  layers: Layer[];
}

interface ArchitectureEvolutionProps {
  eras: Era[];
}

export default function ArchitectureEvolution({ eras }: ArchitectureEvolutionProps): JSX.Element {
  const [activeIdx, setActiveIdx] = useState(0);
  const activeEra = eras[activeIdx] || eras[0];

  return (
    <div className={styles.card}>
      <div className={styles.timelineNav}>
        {eras.map((era, idx) => (
          <button
            key={idx}
            className={`${styles.navItem} ${idx === activeIdx ? styles.navItemActive : ''}`}
            onClick={() => setActiveIdx(idx)}
          >
            {era.year}
          </button>
        ))}
      </div>

      {activeEra && (
        <div className={styles.layout}>
          <div className={styles.detailsPane}>
            <div className={styles.eraHeader}>
              <span className={styles.eraYear}>{activeEra.year} ERA</span>
              <h4 className={styles.eraTitle}>{activeEra.title}</h4>
            </div>

            <div className={styles.section}>
              <span className={styles.sectionLabel}>
                <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
                  <polygon points="12 2 2 7 12 12 22 7 12 2"></polygon>
                  <polyline points="2 17 12 22 22 17"></polyline>
                  <polyline points="2 12 12 17 22 12"></polyline>
                </svg>
                演进诉求 (Intent/Bottleneck)
              </span>
              <p className={styles.sectionText}>{activeEra.intent}</p>
            </div>

            <div className={styles.section}>
              <span className={styles.sectionLabel}>
                <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
                  <circle cx="12" cy="12" r="10"></circle>
                  <polyline points="12 6 12 12 14 14"></polyline>
                </svg>
                主要变动 (Change)
              </span>
              <p className={styles.sectionText}>{activeEra.change}</p>
            </div>

            <div className={styles.section}>
              <span className={styles.sectionLabel}>
                <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
                  <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path>
                  <polyline points="22 4 12 14.01 9 11.01"></polyline>
                </svg>
                决策动因 (Why)
              </span>
              <p className={styles.sectionText}>{activeEra.why}</p>
            </div>
          </div>

          <div className={styles.visualPane}>
            <div className={styles.visualTitle}>系统架构分层演进</div>
            <div className={styles.layersStack}>
              {activeEra.layers.map((layer, idx) => (
                <div key={idx} className={styles.layerRow}>
                  <div className={styles.layerHeader}>{layer.name}</div>
                  <div className={styles.layerComps}>
                    {layer.comps.map((comp, compIdx) => (
                      <span
                        key={compIdx}
                        className={`${styles.compBadge} ${comp.isNew ? styles.compBadgeNew : ''}`}
                      >
                        {comp.label}
                        {comp.isNew && (
                          <span style={{ fontSize: '0.7rem', marginLeft: '0.2rem', fontWeight: 'bold' }}>
                            [New]
                          </span>
                        )}
                      </span>
                    ))}
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
