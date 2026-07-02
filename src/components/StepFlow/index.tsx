import React, { useState, useEffect } from 'react';
import styles from './styles.module.css';

interface Step {
  title: string;
  desc: string;
  diagram?: string; // Optional simple diagram content or text
}

interface StepFlowProps {
  steps: Step[];
}

export default function StepFlow({ steps }: StepFlowProps): JSX.Element {
  const [activeStep, setActiveStep] = useState(0);
  const [isPlaying, setIsPlaying] = useState(false);

  useEffect(() => {
    let timer: any = null;
    if (isPlaying) {
      timer = setInterval(() => {
        setActiveStep((prev) => (prev + 1 < steps.length ? prev + 1 : 0));
      }, 3000);
    }
    return () => {
      if (timer) clearInterval(timer);
    };
  }, [isPlaying, steps.length]);

  const togglePlay = () => {
    setIsPlaying(!isPlaying);
  };

  const nextStep = () => {
    setActiveStep((prev) => (prev + 1 < steps.length ? prev + 1 : prev));
  };

  const prevStep = () => {
    setActiveStep((prev) => (prev > 0 ? prev - 1 : prev));
  };

  // Calculate timeline line active width percentage
  const progressPercent = steps.length > 1 ? (activeStep / (steps.length - 1)) * 100 : 0;

  const currentStep = steps[activeStep];

  return (
    <div className={styles.card}>
      <div className={styles.timeline}>
        <div className={styles.timelineLine} />
        <div className={styles.timelineLineActive} style={{ width: `${progressPercent}%` }} />
        {steps.map((_, idx) => {
          let dotClass = styles.dot;
          if (idx === activeStep) dotClass += ` ${styles.dotActive}`;
          else if (idx < activeStep) dotClass += ` ${styles.dotPassed}`;
          return (
            <div key={idx} className={dotClass} onClick={() => { setActiveStep(idx); setIsPlaying(false); }}>
              {idx + 1}
            </div>
          );
        })}
      </div>

      {currentStep && (
        <div className={styles.stepContent}>
          <h5 className={styles.stepTitle}>
            Step {activeStep + 1}: {currentStep.title}
          </h5>
          <p className={styles.stepDesc}>{currentStep.desc}</p>
          {currentStep.diagram && (
            <div style={{ marginTop: '0.5rem', background: 'var(--comp-bg)', padding: '0.5rem', borderRadius: '6px', fontSize: '0.8rem', fontFamily: 'monospace', border: '1px solid var(--comp-border)' }}>
              {currentStep.diagram}
            </div>
          )}
        </div>
      )}

      <div className={styles.controlRow}>
        <div style={{ display: 'flex', gap: '0.5rem' }}>
          <button className={styles.btn} onClick={prevStep} disabled={activeStep === 0}>
            上一步
          </button>
          <button className={styles.btn} onClick={nextStep} disabled={activeStep === steps.length - 1}>
            下一步
          </button>
        </div>
        <button
          className={`${styles.btn} ${isPlaying ? styles.btnActive : ''}`}
          onClick={togglePlay}
        >
          {isPlaying ? '⏸ 暂停播放' : '▶ 自动演示'}
        </button>
      </div>
    </div>
  );
}
