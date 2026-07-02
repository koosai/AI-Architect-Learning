import React from 'react';
import styles from './styles.module.css';

interface TimelineEvent {
  year: string;
  title: string;
  why?: string;
  change?: string;
  drivers?: string; // Support either why or drivers
}

interface EvolutionTimelineProps {
  events: TimelineEvent[];
}

export default function EvolutionTimeline({ events }: EvolutionTimelineProps): JSX.Element {
  return (
    <div className={styles.timeline}>
      {events.map((event, idx) => {
        const drivers = event.why || event.drivers;
        return (
          <div key={idx} className={styles.event}>
            <div className={styles.dot} />
            <div className={styles.contentCard}>
              <div className={styles.header}>
                <span className={styles.year}>{event.year}</span>
                <h4 className={styles.title}>{event.title}</h4>
              </div>
              <div className={styles.details}>
                {drivers && (
                  <div className={styles.section}>
                    <span className={styles.sectionLabel}>升级动因 / 瓶颈</span>
                    <p className={styles.sectionText}>{drivers}</p>
                  </div>
                )}
                {event.change && (
                  <div className={styles.section}>
                    <span className={styles.sectionLabel}>变动细节</span>
                    <p className={styles.sectionText}>{event.change}</p>
                  </div>
                )}
              </div>
            </div>
          </div>
        );
      })}
    </div>
  );
}
