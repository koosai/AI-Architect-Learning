// src/components/llm/client.ts
// OpenAI 兼容对话客户端：任意实现了 /chat/completions 的服务都可用。
// 仅从浏览器直连用户自己填写的 endpoint，密钥不经过任何第三方。
import type { LlmConfig, ChatMessage } from './types';

function authHeaders(cfg: LlmConfig): Record<string, string> {
  const h: Record<string, string> = { 'Content-Type': 'application/json' };
  if (cfg.apiKey) h['Authorization'] = `Bearer ${cfg.apiKey}`;
  if (cfg.provider === 'openrouter') {
    h['HTTP-Referer'] = typeof location !== 'undefined' ? location.origin : '';
    h['X-Title'] = 'AI Architect';
  }
  return h;
}

function endpoint(cfg: LlmConfig): string {
  return cfg.baseUrl.replace(/\/$/, '') + '/chat/completions';
}

export interface TestResult {
  ok: boolean;
  ms: number;
  error?: string;
}

// 轻量“测试连接”：发一条最小请求，测通与延迟。
export async function testConnection(cfg: LlmConfig, signal?: AbortSignal): Promise<TestResult> {
  const t0 = Date.now();
  try {
    const res = await fetch(endpoint(cfg), {
      method: 'POST',
      headers: authHeaders(cfg),
      signal,
      body: JSON.stringify({
        model: cfg.model,
        messages: [{ role: 'user', content: 'ping' }],
        max_tokens: 1,
        temperature: 0,
        stream: false,
      }),
    });
    const ms = Date.now() - t0;
    if (!res.ok) {
      let msg = `HTTP ${res.status}`;
      try {
        const j = await res.json();
        msg = j?.error?.message || j?.message || msg;
      } catch { /* ignore body parse */ }
      return { ok: false, ms, error: msg };
    }
    return { ok: true, ms };
  } catch (e: any) {
    return { ok: false, ms: Date.now() - t0, error: e?.message || '网络错误 / CORS 被拒' };
  }
}

// 流式对话：逐块回调 onDelta；返回完整文本。解析 SSE data: 行。
export async function streamChat(
  cfg: LlmConfig,
  messages: ChatMessage[],
  onDelta: (text: string) => void,
  signal?: AbortSignal,
): Promise<string> {
  const res = await fetch(endpoint(cfg), {
    method: 'POST',
    headers: authHeaders(cfg),
    signal,
    body: JSON.stringify({
      model: cfg.model,
      messages,
      temperature: cfg.temperature,
      max_tokens: cfg.maxTokens,
      stream: true,
    }),
  });

  if (!res.ok) {
    let msg = `HTTP ${res.status}`;
    try { const j = await res.json(); msg = j?.error?.message || msg; } catch {}
    throw new Error(msg);
  }

  // 不支持流式的服务：回退到一次性 JSON。
  if (!res.body) {
    const j = await res.json();
    const text = j?.choices?.[0]?.message?.content ?? '';
    onDelta(text);
    return text;
  }

  const reader = res.body.getReader();
  const decoder = new TextDecoder();
  let buffer = '';
  let full = '';

  while (true) {
    const { value, done } = await reader.read();
    if (done) break;
    buffer += decoder.decode(value, { stream: true });
    const lines = buffer.split('\n');
    buffer = lines.pop() ?? '';
    for (const line of lines) {
      const trimmed = line.trim();
      if (!trimmed || !trimmed.startsWith('data:')) continue;
      const payload = trimmed.slice(5).trim();
      if (payload === '[DONE]') return full;
      try {
        const j = JSON.parse(payload);
        const delta = j?.choices?.[0]?.delta?.content ?? '';
        if (delta) { full += delta; onDelta(delta); }
      } catch { /* 跨服务偶发非标准行，忽略 */ }
    }
  }
  return full;
}

// 学习助手的系统提示：注入当前课程上下文，约束“讲思路、不直接给 lab 答案”。
export function buildSystemPrompt(pageContext: string): ChatMessage {
  return {
    role: 'system',
    content:
      '你是「AI Architect」学习平台的随堂助手，面向正在学习分布式系统与 AI 架构的中文学习者。' +
      '用中文讲解、保留必要英文术语（如 Load Balancing、TrueTime）。' +
      '解释概念时先给直觉与类比，再给精确定义；对比方案时点明取舍。' +
      '涉及动手 Lab 时给思路和下一步提示，不直接给出完整答案。' +
      (pageContext ? `\n\n【当前页面上下文】\n${pageContext}` : ''),
  };
}
