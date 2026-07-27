// src/components/llm/LlmConfigModal.tsx
import React, { useEffect, useMemo, useState } from 'react';
import { useLlm } from './LlmContext';
import { PROVIDER_PRESETS, type LlmConfig, type ProviderId } from './types';
import { uuid } from './store';
import { testConnection, type TestResult } from './client';
import styles from './llm.module.css';

const blank = (): LlmConfig => {
  const p = PROVIDER_PRESETS[0];
  return {
    id: uuid(), label: '我的 ' + p.name, provider: p.id,
    baseUrl: p.baseUrl, apiKey: '', model: p.model,
    temperature: 0.6, maxTokens: 4096, createdAt: Date.now(),
  };
};

export default function LlmConfigModal() {
  const { configOpen, editingId, state, closeConfig, save, setActive } = useLlm();
  const [form, setForm] = useState<LlmConfig>(blank);
  const [showKey, setShowKey] = useState(false);
  const [testing, setTesting] = useState(false);
  const [result, setResult] = useState<TestResult | null>(null);

  useEffect(() => {
    if (!configOpen) return;
    const existing = state.configs.find((c) => c.id === editingId);
    setForm(existing ? { ...existing } : blank());
    setResult(null); setShowKey(false);
  }, [configOpen, editingId]);

  const pickProvider = (id: ProviderId) => {
    const p = PROVIDER_PRESETS.find((x) => x.id === id)!;
    setForm((f) => ({ ...f, provider: id, baseUrl: p.baseUrl, model: p.model, label: '我的 ' + p.name }));
    setResult(null);
  };

  const runTest = async () => {
    setTesting(true); setResult(null);
    const r = await testConnection(form);
    setResult(r); setTesting(false);
  };

  const onSave = () => {
    save(form);
    setActive(form.id);
    closeConfig();
  };

  const preset = useMemo(
    () => PROVIDER_PRESETS.find((p) => p.id === form.provider) ?? PROVIDER_PRESETS[0],
    [form.provider],
  );

  if (!configOpen) return null;

  return (
    <div className={styles.overlay} onClick={closeConfig}>
      <div className={styles.modal} onClick={(e) => e.stopPropagation()}>
        <div className={styles.modalHead}>
          <div className={styles.brandIcon} aria-hidden>🔌</div>
          <div style={{ flex: 1 }}>
            <h3 className={styles.h3}>连接 AI 服务</h3>
            <p className={styles.sub}>自带任意 OpenAI 兼容服务 · 密钥仅存本地浏览器</p>
          </div>
          <button className={styles.iconBtn} onClick={closeConfig} aria-label="关闭">✕</button>
        </div>

        <div className={styles.modalBody}>
          <div className={styles.stepLabel}>1 · 选择服务商</div>
          <div className={styles.providerGrid}>
            {PROVIDER_PRESETS.map((p) => (
              <button
                key={p.id}
                className={`${styles.providerCard} ${form.provider === p.id ? styles.providerActive : ''}`}
                onClick={() => pickProvider(p.id)}
              >
                <span className={styles.providerMono} style={{ background: p.color }}>{p.mono}</span>
                <span className={styles.providerName}>{p.name}</span>
                <span className={styles.providerHint}>{p.hint}</span>
              </button>
            ))}
          </div>

          <div className={styles.stepLabel}>2 · 凭据与参数</div>
          <div className={styles.formGrid2}>
            <label className={styles.field}>
              <span>配置名称</span>
              <input value={form.label} onChange={(e) => { setForm((f) => ({ ...f, label: e.target.value })); }} placeholder="我的 GPT-5.5" />
            </label>
            <label className={styles.field}>
              <span>模型名称</span>
              <input value={form.model} onChange={(e) => { setForm((f) => ({ ...f, model: e.target.value })); setResult(null); }} placeholder={preset.model} />
            </label>
          </div>

          <label className={styles.field}>
            <span>API Key</span>
            <div className={styles.keyRow}>
              <input
                type={showKey ? 'text' : 'password'}
                value={form.apiKey}
                onChange={(e) => { setForm((f) => ({ ...f, apiKey: e.target.value })); setResult(null); }}
                placeholder="sk-••••••••••••••••"
                spellCheck={false}
              />
              <button type="button" className={styles.keyToggle} onClick={() => setShowKey((s) => !s)}>
                {showKey ? '隐藏' : '显示'}
              </button>
            </div>
          </label>

          <label className={styles.field}>
            <span>Base URL / Endpoint</span>
            <input value={form.baseUrl} onChange={(e) => { setForm((f) => ({ ...f, baseUrl: e.target.value })); setResult(null); }} placeholder={preset.baseUrl} spellCheck={false} />
          </label>

          <div className={styles.formGrid2}>
            <label className={styles.field}>
              <span>温度 Temperature <b>{form.temperature.toFixed(1)}</b></span>
              <input type="range" min={0} max={2} step={0.1} value={form.temperature}
                onChange={(e) => setForm((f) => ({ ...f, temperature: parseFloat(e.target.value) }))} />
            </label>
            <label className={styles.field}>
              <span>最大 Tokens</span>
              <input type="number" value={form.maxTokens}
                onChange={(e) => setForm((f) => ({ ...f, maxTokens: parseInt(e.target.value || '0', 10) }))} placeholder="4096" />
            </label>
          </div>

          <div className={styles.note}>
            🔒 API Key 通过浏览器 <b>localStorage</b> 保存在本机，不会发送到任何第三方服务器（仅直连你填写的 Endpoint）。
          </div>

          <div className={styles.actions}>
            <button className={`${styles.testBtn} ${result?.ok ? styles.testOk : ''}`} onClick={runTest} disabled={testing}>
              {testing ? '测试中…' : result?.ok ? '连接正常' : '测试连接'}
            </button>
            {result && !testing && (
              <span className={result.ok ? styles.testMsgOk : styles.testMsgErr}>
                {result.ok ? `连接成功 · 延迟 ${result.ms}ms` : `失败：${result.error}`}
              </span>
            )}
            <div style={{ flex: 1 }} />
            <button className={styles.primaryBtn} onClick={onSave} disabled={!form.model || !form.baseUrl}>
              保存并启用
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
