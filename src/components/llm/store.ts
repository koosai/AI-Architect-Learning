// src/components/llm/store.ts
// 本地持久化：API Key 等只存浏览器 localStorage，绝不上传。
import type { LlmState, LlmConfig } from './types';

const KEY = 'aia.llm.v1';
const empty: LlmState = { configs: [], activeId: null };

function canUse(): boolean {
  return typeof window !== 'undefined' && !!window.localStorage;
}

export function loadState(): LlmState {
  if (!canUse()) return empty;
  try {
    const raw = window.localStorage.getItem(KEY);
    if (!raw) return empty;
    const parsed = JSON.parse(raw) as LlmState;
    if (!parsed || !Array.isArray(parsed.configs)) return empty;
    return parsed;
  } catch {
    return empty;
  }
}

export function saveState(state: LlmState): void {
  if (!canUse()) return;
  try {
    window.localStorage.setItem(KEY, JSON.stringify(state));
  } catch {
    /* quota / private mode — silently ignore */
  }
}

export function upsertConfig(state: LlmState, cfg: LlmConfig): LlmState {
  const i = state.configs.findIndex((c) => c.id === cfg.id);
  const configs = i >= 0
    ? state.configs.map((c) => (c.id === cfg.id ? cfg : c))
    : [...state.configs, cfg];
  return { configs, activeId: state.activeId ?? cfg.id };
}

export function removeConfig(state: LlmState, id: string): LlmState {
  const configs = state.configs.filter((c) => c.id !== id);
  const activeId = state.activeId === id ? (configs[0]?.id ?? null) : state.activeId;
  return { configs, activeId };
}

export function activeConfig(state: LlmState): LlmConfig | null {
  return state.configs.find((c) => c.id === state.activeId) ?? null;
}

export function uuid(): string {
  if (typeof crypto !== 'undefined' && 'randomUUID' in crypto) return crypto.randomUUID();
  return 'cfg-' + Math.random().toString(36).slice(2) + Date.now().toString(36);
}
