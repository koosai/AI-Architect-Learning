import React, { useState } from 'react';
import styles from './styles.module.css';

interface LayerItem {
  name: string;
  components: string[];
  detail: string;
}

interface ArchLayersProps {
  title?: string;
  layers: LayerItem[];
}

export default function ArchLayers({ title = '分层架构设计图', layers }: ArchLayersProps): JSX.Element {
  const [activeIdx, setActiveIdx] = useState<number | null>(0); // First layer open by default

  const handleToggle = (idx: number) => {
    setActiveIdx((prev) => (prev === idx ? null : idx));
  };

  return (
    <div className={styles.card}>
      <h4 className={styles.title}>
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round" style={{ marginRight: '0.4rem', verticalAlign: 'middle' }}>
          <polygon points="12 2 2 7 12 12 22 7 12 2"></polygon>
          <polyline points="2 17 12 22 22 17"></polyline>
          <polyline points="2 12 12 17 22 12"></polyline>
        </svg>
        {title}
      </h4>

      <div className={styles.layersStack}>
        {layers.map((layer, idx) => {
          const isOpen = activeIdx === idx;
          return (
            <div
              key={idx}
              className={`${styles.layerWrapper} ${isOpen ? styles.layerWrapperActive : ''}`}
            >
              <div
                className={`${styles.layerHeader} ${isOpen ? styles.layerHeaderActive : ''}`}
                onClick={() => handleToggle(idx)}
              >
                <span className={styles.layerTitle}>{layer.name}</span>
                <svg
                  width="16"
                  height="16"
                  viewBox="0 0 24 24"
                  fill="none"
                  stroke="currentColor"
                  strokeWidth="2.5"
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  style={{ transform: isOpen ? 'rotate(90deg)' : 'none', transition: 'transform 0.2s' }}
                >
                  <polyline points="9 18 15 12 9 6"></polyline>
                </svg>
              </div>

              {isOpen && (
                <div className={styles.layerBody}>
                  {layer.components && layer.components.length > 0 && (
                    <div className={styles.compsGrid}>
                      {layer.components.map((comp, compIdx) => (
                        <div key={compIdx} className={styles.compCard}>
                          {comp}
                        </div>
                      ))}
                    </div>
                  )}
                  <p className={styles.detailText}>{layer.detail}</p>
                </div>
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
}
