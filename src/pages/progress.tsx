// src/pages/progress.tsx — 学习进度（热力图 + 掌握度 + 薄弱点）
import React, { useEffect, useState } from 'react';
import Layout from '@theme/Layout';
import BrowserOnly from '@docusaurus/BrowserOnly';
import { load, completedCount, type Progress } from '@site/src/components/progress/progressStore';
import { MONTHS } from '@site/src/data/course';
import { useLlm } from '@site/src/components/llm/LlmContext';
import s from './learning.module.css';

function heatColor(v: number) {
  return ['var(--comp-hover)', 'rgba(113,103,255,.28)', 'rgba(113,103,255,.5)', 'rgba(113,103,255,.72)', 'var(--ifm-color-primary)'][v];
}

function Inner() {
  const [p, setP] = useState<Progress | null>(null);
  const { openTutor } = useLlm();
  useEffect(() => { setP(load()); }, []);
  if (!p) return null;
  const totalLessons = MONTHS.reduce((a, m) => a + m.lessons, 0);
  const done = completedCount(p);
  const quizzes = Object.values(p.quiz);
  const acc = quizzes.length ? Math.round(quizzes.reduce((a, q) => a + q.score / q.total, 0) / quizzes.length * 100) : 0;

  // 由已完成课程时间戳生成近 12 周热力（无数据则空）
  const weeks = Array.from({ length: 12 }, (_, w) =>
    Array.from({ length: 7 }, (_, d) => {
      const seed = (w * 7 + d);
      const has = Object.values(p.completed).some((t) => Math.floor((Date.now() - t) / 86400000) === (83 - seed));
      return has ? 3 : 0;
    }));

  const stats = [
    { label: '总进度', value: `${Math.round(done / totalLessons * 100)}%`, sub: `${done} / ${totalLessons} 节` },
    { label: '累计 XP', value: String(p.xp), sub: '完成课程 + 测验' },
    { label: '连续学习', value: `${p.streak}天`, sub: `个人最佳 ${p.bestStreak} 天` },
    { label: '测验正确率', value: `${acc}%`, sub: `${quizzes.length} 次测验` },
  ];

  return (
    <div className={s.wrap}>
      <h1 className={s.h1}>学习进度</h1>
      <p className={s.lead}>你的节奏、掌握度与坚持——一眼看清走到哪了。</p>
      <div className={s.statGrid} style={{ marginTop: 18 }}>
        {stats.map((st) => (
          <div key={st.label} className={s.statCard}>
            <div className={s.muted}>{st.label}</div>
            <div className={s.statVal}>{st.value}</div>
            <div className={s.muted} style={{ marginTop: 3 }}>{st.sub}</div>
          </div>
        ))}
      </div>

      <div className={s.card}>
        <div className={s.cardHead}><b>学习热力图 · 近 12 周</b><span className={s.muted}>完成课程当天点亮</span></div>
        <div style={{ display: 'flex', gap: 4, overflowX: 'auto', padding: 16 }}>
          {weeks.map((wk, i) => (
            <div key={i} style={{ display: 'flex', flexDirection: 'column', gap: 4 }}>
              {wk.map((v, j) => <span key={j} style={{ width: 14, height: 14, borderRadius: 3, background: heatColor(v) }} />)}
            </div>
          ))}
        </div>
      </div>

      <div className={s.card}>
        <div className={s.cardHead}><b>薄弱点 · AI 建议复习</b></div>
        <div style={{ padding: 16 }}>
          {quizzes.length === 0
            ? <p className={s.muted} style={{ margin: 0 }}>完成一些测验后，这里会根据错题给出针对性复习建议。</p>
            : <p className={s.muted} style={{ margin: '0 0 12px' }}>基于你的测验记录，AI 可生成针对性复习题。</p>}
          <button className={s.primaryBtn} onClick={openTutor}>让 AI 生成复习题</button>
        </div>
      </div>
    </div>
  );
}

export default function ProgressPage() {
  return (<Layout title="学习进度"><BrowserOnly>{() => <Inner />}</BrowserOnly></Layout>);
}
