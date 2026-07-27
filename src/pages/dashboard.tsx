// src/pages/dashboard.tsx — 学习仪表盘（新页面，仓库原本没有）
import React, { useEffect, useState } from 'react';
import Layout from '@theme/Layout';
import Link from '@docusaurus/Link';
import BrowserOnly from '@docusaurus/BrowserOnly';
import { MONTHS, MONTH1_LESSONS } from '@site/src/data/course';
import { load, completedCount, type Progress } from '@site/src/components/progress/progressStore';
import { useLlm } from '@site/src/components/llm/LlmContext';
import s from './learning.module.css';

function Inner() {
  const [p, setP] = useState<Progress | null>(null);
  const { openTutor, isConfigured, openConfig } = useLlm();
  useEffect(() => { setP(load()); }, []);
  if (!p) return null;

  const done = completedCount(p);
  const nextLesson = MONTH1_LESSONS.find((l) => !p.completed[l.id]) ?? MONTH1_LESSONS[0];
  const cur = MONTHS[1]; // 当前示例课程月 = Month 1（可按实际进度推导）
  const monthDone = MONTH1_LESSONS.filter((l) => p.completed[l.id]).length;
  const stats = [
    { label: '连续学习', value: String(p.streak || 0), unit: '天', c: 'var(--brand-yellow)' },
    { label: '已完成课程', value: String(done), unit: '节', c: 'var(--brand-cyan)' },
    { label: '累计 XP', value: String(p.xp || 0), unit: '', c: 'var(--ifm-color-primary)' },
    { label: '最佳连续', value: String(p.bestStreak || 0), unit: '天', c: 'var(--brand-green)' },
  ];

  return (
    <div className={s.wrap}>
      <div className={s.headRow}>
        <div>
          <div className={s.kicker}>{new Date().toLocaleDateString('zh-CN', { year: 'numeric', month: 'long', day: 'numeric', weekday: 'long' })}</div>
          <h1 className={s.h1}>欢迎回来 👋</h1>
          <p className={s.lead}>继续你的架构师之路。下一节：<b>{nextLesson.code} · {nextLesson.zh}</b></p>
        </div>
        <Link className={s.primaryBtn} to={nextLesson.slug}>继续学习 →</Link>
      </div>

      {/* Continue hero */}
      <Link to={nextLesson.slug} className={s.hero}>
        <div className={s.heroIcon} aria-hidden>▶</div>
        <div style={{ flex: 1 }}>
          <div className={s.badgeRow}><span className={s.badgeAccent}>继续学习</span><span className={s.muted}>Month {cur.n} · {cur.zh}</span></div>
          <div className={s.heroTitle}>{nextLesson.code} · {nextLesson.zh}</div>
          <div className={s.progressLine}>
            <span className={s.bar}><span style={{ width: `${Math.round((monthDone / cur.lessons) * 100)}%` }} /></span>
            <span className={s.muted}>{monthDone}/{cur.lessons} 完成</span>
          </div>
        </div>
      </Link>

      {/* Stats */}
      <div className={s.statGrid}>
        {stats.map((st) => (
          <div key={st.label} className={s.statCard}>
            <div className={s.muted}>{st.label}</div>
            <div className={s.statVal} style={{ color: st.c }}>{st.value}<span className={s.statUnit}>{st.unit}</span></div>
          </div>
        ))}
      </div>

      <div className={s.cols}>
        <div>
          {/* Month 1 lessons */}
          <div className={s.card}>
            <div className={s.cardHead}><b>本月课程 · Month 1 编程系统基石</b><Link to="/foundations/overview" className={s.link}>全部 →</Link></div>
            <div className={s.lessonList}>
              {MONTH1_LESSONS.slice(0, 6).map((l) => (
                <Link key={l.id} to={l.slug} className={s.lessonRow}>
                  <span className={`${s.dot} ${p.completed[l.id] ? s.dotDone : ''}`} />
                  <span className={s.code}>{l.code}</span>
                  <span className={s.lessonName}>{l.zh}<span className={s.muted}> · {l.en}</span></span>
                  <span className={s.muted}>{l.min}</span>
                </Link>
              ))}
            </div>
          </div>
        </div>

        <div className={s.rail}>
          <div className={s.aiCard}>
            <div className={s.badgeRow}><span className={s.aiIcon} aria-hidden>✦</span><b>AI 学习助手</b></div>
            <p className={s.muted} style={{ margin: '8px 0 11px', lineHeight: 1.55 }}>
              {isConfigured ? '已连接。随堂讲解、出题、总结随时可用。' : '连接你自己的 AI 服务（OpenAI/Claude/Gemini/本地…），密钥仅存本地。'}
            </p>
            <button className={s.primaryBtn} style={{ width: '100%' }} onClick={isConfigured ? openTutor : () => openConfig()}>
              {isConfigured ? '打开助手' : '启用助手'}
            </button>
          </div>
          <div className={s.card}>
            <div className={s.cardHead}><b>快速入口</b></div>
            <div className={s.railLinks}>
              <Link to="/roadmap" className={s.railLink}>🗺 学习路线</Link>
              <Link to="/progress" className={s.railLink}>📈 学习进度</Link>
              <Link to="/achievements" className={s.railLink}>🏆 成就 · 证书</Link>
              <Link to="/foundations/overview" className={s.railLink}>📖 课程内容</Link>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default function DashboardPage() {
  return (
    <Layout title="学习仪表盘" description="AI Architect 学习仪表盘">
      <BrowserOnly>{() => <Inner />}</BrowserOnly>
    </Layout>
  );
}
