import React, { useState } from 'react';
import styles from './styles.module.css';

interface GuidedExerciseProps {
  title: string;
  goal: string;
  hints?: string[];
  steps: string[];
  checks?: string[];
}

export default function GuidedExercise({ title, goal, hints, steps, checks }: GuidedExerciseProps): JSX.Element {
  const [showHints, setShowHints] = useState(false);
  const [stepStates, setStepStates] = useState<boolean[]>(new Array(steps.length).fill(false));
  const [checkStates, setCheckStates] = useState<boolean[]>(new Array(checks?.length || 0).fill(false));

  const totalItems = steps.length + (checks?.length || 0);
  const checkedItems = stepStates.filter(Boolean).length + checkStates.filter(Boolean).length;
  const progressPercent = totalItems > 0 ? Math.round((checkedItems / totalItems) * 100) : 0;

  const toggleStep = (index: number) => {
    const nextStates = [...stepStates];
    nextStates[index] = !nextStates[index];
    setStepStates(nextStates);
  };

  const toggleCheck = (index: number) => {
    const nextStates = [...checkStates];
    nextStates[index] = !nextStates[index];
    setCheckStates(nextStates);
  };

  return (
    <div className={styles.card}>
      <div className={styles.header}>
        <span className={styles.badge}>Guided Exercise</span>
        <h4 className={styles.title}>{title}</h4>
      </div>

      <div className={styles.goalSection}>
        <div className={styles.goalLabel}>实验目标</div>
        <p className={styles.goalText}>{goal}</p>
      </div>

      {hints && hints.length > 0 && (
        <div>
          <button className={styles.hintToggleBtn} onClick={() => setShowHints(!showHints)}>
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round" style={{ transform: showHints ? 'rotate(90deg)' : 'none', transition: 'transform 0.2s' }}>
              <polyline points="9 18 15 12 9 6"></polyline>
            </svg>
            <span>{showHints ? '隐藏提示' : '显示提示'}</span>
          </button>
          {showHints && (
            <div className={styles.hintsBox}>
              {hints.map((hint, idx) => (
                <div key={idx} className={styles.hintItem}>
                  💡 {hint}
                </div>
              ))}
            </div>
          )}
        </div>
      )}

      <div className={styles.progressBarContainer}>
        <div className={styles.progressBar}>
          <div className={styles.progressFill} style={{ width: `${progressPercent}%` }} />
        </div>
        <span className={styles.progressText}>{progressPercent}% 已完成</span>
      </div>

      <div className={styles.sectionTitle}>操作步骤</div>
      <div className={styles.checklist}>
        {steps.map((step, idx) => (
          <label key={idx} className={styles.checkItem}>
            <input type="checkbox" checked={stepStates[idx]} onChange={() => toggleStep(idx)} className={styles.checkboxInput} />
            <div className={styles.checkboxRepl}>
              <svg width="10" height="10" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="4" strokeLinecap="round" strokeLinejoin="round">
                <polyline points="20 6 9 17 4 12"></polyline>
              </svg>
            </div>
            <span className={styles.itemLabel}>
              <strong>第 {idx + 1} 步：</strong>
              {step}
            </span>
          </label>
        ))}
      </div>

      {checks && checks.length > 0 && (
        <>
          <div className={styles.sectionTitle}>自检清单</div>
          <div className={styles.checklist}>
            {checks.map((check, idx) => (
              <label key={idx} className={styles.checkItem}>
                <input type="checkbox" checked={checkStates[idx]} onChange={() => toggleCheck(idx)} className={styles.checkboxInput} />
                <div className={styles.checkboxRepl}>
                  <svg width="10" height="10" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="4" strokeLinecap="round" strokeLinejoin="round">
                    <polyline points="20 6 9 17 4 12"></polyline>
                  </svg>
                </div>
                <span className={styles.itemLabel}>🔍 {check}</span>
              </label>
            ))}
          </div>
        </>
      )}
    </div>
  );
}
