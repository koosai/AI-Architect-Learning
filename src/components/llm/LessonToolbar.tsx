// src/components/llm/LessonToolbar.tsx
// 注入到每个课程页顶部：一键让 AI 讲解/总结/出题当前这节。
import React from 'react';
import { useLlm } from './LlmContext';
import styles from './llm.module.css';

export default function LessonToolbar() {
  const { openTutor } = useLlm();
  return (
    <div className={styles.lessonBar}>
      <span className={styles.lessonBarHint}>学不动了？让 AI 助手结合本页帮你</span>
      <div className={styles.lessonBarActions}>
        <button className={styles.lessonBtn} onClick={openTutor}>
          <span aria-hidden>✦</span> 讲解本节
        </button>
        <button className={styles.lessonBtnGhost} onClick={openTutor}>生成测验</button>
        <button className={styles.lessonBtnGhost} onClick={openTutor}>总结本章</button>
      </div>
    </div>
  );
}
