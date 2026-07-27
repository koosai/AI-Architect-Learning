// src/pages/achievements.tsx — 成就与证书
import React, { useEffect, useState } from 'react';
import Layout from '@theme/Layout';
import BrowserOnly from '@docusaurus/BrowserOnly';
import { load, completedCount, type Progress } from '@site/src/components/progress/progressStore';
import s from './learning.module.css';

interface Badge { icon: string; name: string; desc: string; unlocked: (p: Progress) => boolean; progress?: (p: Progress) => number; }

const BADGES: Badge[] = [
  { icon: '🧭', name: '启程', desc: '完成第一节课', unlocked: (p) => completedCount(p) >= 1 },
  { icon: '🧪', name: '第一次绿灯', desc: '通过第一个测验', unlocked: (p) => Object.keys(p.quiz).length >= 1 },
  { icon: '🔥', name: '7 天连续', desc: '连续学习 7 天', unlocked: (p) => p.bestStreak >= 7, progress: (p) => Math.min(1, p.bestStreak / 7) },
  { icon: '🏛', name: '地基奠定者', desc: '完成 Month 1 全部 16 节', unlocked: (p) => completedCount(p) >= 16, progress: (p) => Math.min(1, completedCount(p) / 16) },
  { icon: '⚡', name: '满分快枪手', desc: '一次测验满分', unlocked: (p) => Object.values(p.quiz).some((q) => q.score === q.total) },
  { icon: '📚', name: '博览', desc: '累计 500 XP', unlocked: (p) => p.xp >= 500, progress: (p) => Math.min(1, p.xp / 500) },
  { icon: '🌙', name: '夜猫子', desc: '深夜完成学习会话', unlocked: () => false },
  { icon: '👑', name: '共识大师', desc: '完成共识与协调（M5L11）', unlocked: (p) => !!p.completed['m5l11'] },
];

function Inner() {
  const [p, setP] = useState<Progress | null>(null);
  useEffect(() => { setP(load()); }, []);
  if (!p) return null;
  const unlocked = BADGES.filter((b) => b.unlocked(p)).length;
  const stats = [
    { v: String(unlocked), l: '已解锁徽章' },
    { v: String(p.xp), l: '累计 XP' },
    { v: `${p.bestStreak}`, l: '最佳连续天数' },
    { v: String(completedCount(p)), l: '完成课程' },
  ];

  return (
    <div className={s.wrap}>
      <h1 className={s.h1}>成就与证书</h1>
      <p className={s.lead}>坚持看得见。徽章、连续天数与结业证书，记录你成为架构师的每一步。</p>
      <div className={s.statGrid} style={{ marginTop: 18 }}>
        {stats.map((st) => (
          <div key={st.l} className={s.statCard} style={{ textAlign: 'center' }}>
            <div className={s.statVal} style={{ margin: 0 }}>{st.v}</div>
            <div className={s.muted} style={{ marginTop: 3 }}>{st.l}</div>
          </div>
        ))}
      </div>
      <h3 style={{ margin: '8px 0 13px', fontSize: 14 }}>徽章</h3>
      <div className={s.badgeGrid}>
        {BADGES.map((b) => {
          const on = b.unlocked(p);
          const prog = b.progress ? Math.round(b.progress(p) * 100) : (on ? 100 : 0);
          return (
            <div key={b.name} className={`${s.badge} ${on ? '' : s.badgeLocked}`}>
              {on && <span style={{ position: 'absolute', top: 11, right: 11 }} aria-hidden>✅</span>}
              <div className={s.badgeIcon}>{b.icon}</div>
              <div style={{ fontSize: 13, fontWeight: 620 }}>{b.name}</div>
              <p className={s.muted} style={{ margin: '3px 0 10px', lineHeight: 1.45 }}>{b.desc}</p>
              {!on && b.progress && (
                <div className={s.bar} style={{ maxWidth: '100%' }}><span style={{ width: `${prog}%` }} /></div>
              )}
              <div className={s.muted} style={{ marginTop: 6 }}>{on ? '已解锁' : b.progress ? `${prog}%` : '未解锁'}</div>
            </div>
          );
        })}
      </div>
    </div>
  );
}

export default function AchievementsPage() {
  return (<Layout title="成就与证书"><BrowserOnly>{() => <Inner />}</BrowserOnly></Layout>);
}
