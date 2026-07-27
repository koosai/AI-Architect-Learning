// src/pages/profile.tsx — 个人与设置（含 AI 服务管理）
import React, { useEffect, useState } from 'react';
import Layout from '@theme/Layout';
import BrowserOnly from '@docusaurus/BrowserOnly';
import { useLlm } from '@site/src/components/llm/LlmContext';
import { load, type Progress } from '@site/src/components/progress/progressStore';
import s from './learning.module.css';

function Inner() {
  const { state, active, setActive, remove, openConfig, isConfigured } = useLlm();
  const [p, setP] = useState<Progress | null>(null);
  useEffect(() => { setP(load()); }, []);

  return (
    <div className={s.wrap} style={{ maxWidth: 820 }}>
      <div className={s.headRow}>
        <div style={{ display: 'flex', alignItems: 'center', gap: 16 }}>
          <div style={{ width: 60, height: 60, borderRadius: 16, background: 'var(--comp-gradient)', display: 'grid', placeItems: 'center', color: '#fff', fontSize: 24, fontWeight: 650 }}>K</div>
          <div><h1 className={s.h1} style={{ fontSize: 21 }}>我的账户</h1><p className={s.muted} style={{ margin: '2px 0 0' }}>本地档案 · 进度保存在此浏览器</p></div>
        </div>
      </div>

      {/* AI 服务管理 */}
      <div className={s.card}>
        <div className={s.cardHead}><b>AI 服务 · LLM 提供商</b><button className={s.primaryBtn} style={{ height: 32 }} onClick={() => openConfig()}>+ 新增配置</button></div>
        <div style={{ padding: 14 }}>
          {!isConfigured && <p className={s.muted} style={{ margin: 0 }}>还没有连接任何 AI 服务。点「新增配置」自带 API Key 接入任意 OpenAI 兼容服务，密钥仅存本地。</p>}
          {state.configs.map((c) => (
            <div key={c.id} style={{ display: 'flex', alignItems: 'center', gap: 12, padding: '11px 12px', border: '1px solid var(--comp-border)', borderRadius: 11, marginBottom: 8, background: c.id === active?.id ? 'var(--comp-accent-bg)' : 'var(--comp-bg)' }}>
              <div style={{ flex: 1 }}>
                <div style={{ fontSize: 12.5, fontWeight: 600 }}>{c.label} {c.id === active?.id && <span className={s.badgeAccent}>使用中</span>}</div>
                <div className={s.muted} style={{ fontFamily: 'var(--ifm-font-family-monospace)' }}>{c.model} · {c.baseUrl.replace(/^https?:\/\//, '')} · sk-••••{(c.apiKey || '').slice(-4)}</div>
              </div>
              {c.id !== active?.id && <button className={s.railLink} style={{ padding: '4px 10px' }} onClick={() => setActive(c.id)}>启用</button>}
              <button className={s.railLink} style={{ padding: '4px 10px' }} onClick={() => openConfig(c.id)}>编辑</button>
              <button className={s.railLink} style={{ padding: '4px 10px', color: 'var(--brand-red)' }} onClick={() => remove(c.id)}>删除</button>
            </div>
          ))}
        </div>
      </div>

      {/* 阅读偏好（示意，落地时接 colorMode / 字号） */}
      <div className={s.card}>
        <div className={s.cardHead}><b>阅读与外观</b></div>
        <div style={{ padding: 16 }} className={s.muted}>
          主题深/浅色由右上角切换或系统偏好控制；字号、专注模式、信息密度可在此扩展。学习进度键：<code>aia.progress.v1</code>，AI 配置键：<code>aia.llm.v1</code>（均在本浏览器）。
        </div>
      </div>
    </div>
  );
}

export default function ProfilePage() {
  return (<Layout title="我的账户"><BrowserOnly>{() => <Inner />}</BrowserOnly></Layout>);
}
