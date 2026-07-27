// src/components/llm/AiTutor.tsx
// 浮动按钮 → 面板。未配置显示引导；已配置显示随堂对话（流式）。
import React, { useEffect, useRef, useState, useCallback } from 'react';
import { useLlm } from './LlmContext';
import { PROVIDER_PRESETS, type ChatMessage } from './types';
import { streamChat, buildSystemPrompt } from './client';
import { getPageContext, getPageTitle } from './pageContext';
import styles from './llm.module.css';

const QUICK_ASKS = ['解释这一节', '生成 3 道测验', '总结本章', '对比方案', '推荐下一步'];

interface UiMsg { role: 'user' | 'assistant'; content: string; }

export default function AiTutor() {
  const { isConfigured, active, tutorOpen, openTutor, closeTutor, openConfig } = useLlm();
  const [msgs, setMsgs] = useState<UiMsg[]>([]);
  const [input, setInput] = useState('');
  const [busy, setBusy] = useState(false);
  const [pageTitle, setPageTitle] = useState('');
  const scrollRef = useRef<HTMLDivElement>(null);
  const abortRef = useRef<AbortController | null>(null);

  useEffect(() => {
    if (tutorOpen) setPageTitle(getPageTitle());
  }, [tutorOpen]);

  useEffect(() => {
    const el = scrollRef.current;
    if (el) el.scrollTop = el.scrollHeight;
  }, [msgs, busy]);

  const send = useCallback(async (text: string) => {
    const q = text.trim();
    if (!q || busy || !active) return;
    setInput('');
    const history: UiMsg[] = [...msgs, { role: 'user', content: q }];
    setMsgs([...history, { role: 'assistant', content: '' }]);
    setBusy(true);

    const chat: ChatMessage[] = [
      buildSystemPrompt(getPageContext()),
      ...history.map((m) => ({ role: m.role, content: m.content } as ChatMessage)),
    ];
    const ctrl = new AbortController();
    abortRef.current = ctrl;
    try {
      await streamChat(active, chat, (delta) => {
        setMsgs((prev) => {
          const next = [...prev];
          next[next.length - 1] = { role: 'assistant', content: next[next.length - 1].content + delta };
          return next;
        });
      }, ctrl.signal);
    } catch (e: any) {
      setMsgs((prev) => {
        const next = [...prev];
        next[next.length - 1] = { role: 'assistant', content: `⚠️ 出错了：${e?.message || '请求失败'}。请到设置检查你的 API Key / Base URL / 模型名，或该服务是否允许浏览器直连（CORS）。` };
        return next;
      });
    } finally {
      setBusy(false);
      abortRef.current = null;
    }
  }, [busy, active, msgs]);

  const onKey = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); send(input); }
  };

  return (
    <>
      {!tutorOpen && (
        <button className={styles.fab} onClick={openTutor} aria-label="AI 学习助手" title="AI 学习助手">
          <svg width="25" height="25" viewBox="0 0 24 24" fill="none" stroke="#fff" strokeWidth="1.9" strokeLinecap="round" strokeLinejoin="round">
            <path d="M21 11.5a8 8 0 0 1-11.7 7.1L4 20l1.4-5A8 8 0 1 1 21 11.5z" />
            <path d="M12 7v2M9.5 12.5c.6.7 1.5 1 2.5 1s1.9-.3 2.5-1" />
          </svg>
        </button>
      )}

      {tutorOpen && (
        <div className={styles.panel}>
          <div className={styles.panelHead}>
            <span className={styles.panelIcon} aria-hidden>✦</span>
            <div style={{ flex: 1 }}>
              <div className={styles.panelTitle}>AI 学习助手</div>
              <div className={styles.panelSub}>
                {isConfigured ? `已连接 · ${active?.model}` : '未连接 · 需配置'}
              </div>
            </div>
            <button className={styles.iconBtn} onClick={closeTutor} aria-label="关闭">✕</button>
          </div>

          {!isConfigured ? (
            <div className={styles.onboard}>
              <div className={styles.onboardIcon} aria-hidden>🔌</div>
              <h4 className={styles.onboardTitle}>先连接你的 AI 服务</h4>
              <p className={styles.onboardText}>
                本平台不内置任何模型 —— 你可以自带 API Key，接入任意 OpenAI 兼容服务。
                密钥仅保存在<b>你的浏览器本地</b>，绝不上传。
              </p>
              <div className={styles.miniGrid}>
                {PROVIDER_PRESETS.map((p) => (
                  <span key={p.id} className={styles.miniCell} title={p.name}>
                    <span className={styles.providerMono} style={{ background: p.color }}>{p.mono}</span>
                  </span>
                ))}
              </div>
              <button className={styles.primaryBtn} style={{ width: '100%' }} onClick={() => openConfig()}>
                连接 AI 服务
              </button>
            </div>
          ) : (
            <>
              <div className={styles.ctxBar}>
                上下文：<b>{pageTitle || '当前页面'}</b>
              </div>
              <div className={styles.chat} ref={scrollRef}>
                {msgs.length === 0 && (
                  <div className={styles.empty}>问我这节课的任何问题，或点下面的快捷提问。</div>
                )}
                {msgs.map((m, i) => (
                  <div key={i} className={m.role === 'user' ? styles.rowUser : styles.rowAi}>
                    {m.role === 'assistant' && <span className={styles.aiAvatar} aria-hidden>✦</span>}
                    <div className={m.role === 'user' ? styles.bubbleUser : styles.bubbleAi}>
                      {m.content || (busy && i === msgs.length - 1 ? '思考中…' : '')}
                    </div>
                  </div>
                ))}
              </div>
              <div className={styles.composer}>
                <div className={styles.quickRow}>
                  {QUICK_ASKS.map((q) => (
                    <button key={q} className={styles.quickChip} onClick={() => send(q)} disabled={busy}>{q}</button>
                  ))}
                </div>
                <div className={styles.inputRow}>
                  <textarea
                    rows={1}
                    value={input}
                    onChange={(e) => setInput(e.target.value)}
                    onKeyDown={onKey}
                    placeholder="问一问这节课的任何问题…"
                  />
                  <button className={styles.sendBtn} onClick={() => send(input)} disabled={busy || !input.trim()} aria-label="发送">
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M4 12h15M13 6l6 6-6 6" /></svg>
                  </button>
                </div>
              </div>
            </>
          )}
        </div>
      )}
    </>
  );
}
