// src/pages/roadmap.tsx — 13 个月学习路线时间轴
import React, { useEffect, useState } from 'react';
import Layout from '@theme/Layout';
import Link from '@docusaurus/Link';
import BrowserOnly from '@docusaurus/BrowserOnly';
import { MONTHS, PHASES } from '@site/src/data/course';
import { load } from '@site/src/components/progress/progressStore';
import s from './learning.module.css';

function Inner() {
  const [done, setDone] = useState(0);
  useEffect(() => { setDone(Object.keys(load().completed).length); }, []);
  const CUR = 1; // 当前月（示例）
  let lastPhase = -1;

  return (
    <div className={s.wrap}>
      <h1 className={s.h1}>学习路线</h1>
      <p className={s.lead}>13 个月，从工程地基到生产级 AI 架构。你正在 <b>Month {CUR} · {MONTHS[CUR].zh}</b>。</p>
      <div className={s.timeline} style={{ marginTop: 22 }}>
        <div className={s.tlSpine} />
        {MONTHS.map((m) => {
          const state = m.n < CUR ? 'done' : m.n === CUR ? 'cur' : 'locked';
          const showPhase = m.phase !== lastPhase; lastPhase = m.phase;
          return (
            <div key={m.n}>
              {showPhase && <div className={s.phaseHead}><span>{PHASES[m.phase]}</span><span /></div>}
              <div className={s.tlRow}>
                <div className={`${s.tlNode} ${state === 'cur' ? s.tlNodeCur : ''} ${state === 'done' ? s.tlNodeDone : ''}`}>
                  {state === 'done' ? '✓' : state === 'locked' ? '🔒' : ('0' + m.n).slice(-2)}
                </div>
                <Link className={s.tlCard} to={m.n <= CUR ? (m.n === 1 ? '/foundations/overview' : '/') : '/roadmap'}>
                  <div className={s.badgeRow}>
                    <span className={s.muted} style={{ fontFamily: 'var(--ifm-font-family-monospace)' }}>MONTH {('0' + m.n).slice(-2)}</span>
                    <span className={s.badgeAccent}>{state === 'done' ? '已完成' : state === 'cur' ? '进行中' : '未解锁'}</span>
                  </div>
                  <div style={{ fontSize: 15, fontWeight: 620, letterSpacing: '-0.02em', margin: '3px 0 2px', color: 'var(--comp-text)' }}>
                    {m.zh} <span className={s.muted}>· {m.en}</span>
                  </div>
                  <div className={s.muted}>{m.topics}</div>
                  <div className={s.muted} style={{ marginTop: 8 }}>{m.lessons} 节课 · 约 {m.hours}</div>
                </Link>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}

export default function RoadmapPage() {
  return (<Layout title="学习路线" description="13 个月学习路线"><BrowserOnly>{() => <Inner />}</BrowserOnly></Layout>);
}
