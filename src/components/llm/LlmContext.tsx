// src/components/llm/LlmContext.tsx
// 全局 LLM 状态：配置的增删改、当前激活配置、模态与助手面板的开关。
// SSR 安全：初始为空，挂载后从 localStorage 水合。
import React, {
  createContext, useContext, useState, useEffect, useCallback, useMemo,
} from 'react';
import type { LlmState, LlmConfig } from './types';
import {
  loadState, saveState, upsertConfig, removeConfig, activeConfig,
} from './store';

interface LlmContextValue {
  ready: boolean;                    // 是否已水合
  state: LlmState;
  active: LlmConfig | null;
  isConfigured: boolean;
  // 配置管理
  save: (cfg: LlmConfig) => void;
  remove: (id: string) => void;
  setActive: (id: string) => void;
  // UI 开关
  tutorOpen: boolean;
  openTutor: () => void;
  closeTutor: () => void;
  configOpen: boolean;
  editingId: string | null;
  openConfig: (id?: string) => void;
  closeConfig: () => void;
}

const Ctx = createContext<LlmContextValue | null>(null);

export function LlmProvider({ children }: { children: React.ReactNode }) {
  const [state, setState] = useState<LlmState>({ configs: [], activeId: null });
  const [ready, setReady] = useState(false);
  const [tutorOpen, setTutorOpen] = useState(false);
  const [configOpen, setConfigOpen] = useState(false);
  const [editingId, setEditingId] = useState<string | null>(null);

  useEffect(() => {
    setState(loadState());
    setReady(true);
  }, []);

  const persist = useCallback((next: LlmState) => {
    setState(next);
    saveState(next);
  }, []);

  const save = useCallback((cfg: LlmConfig) => {
    persist(upsertConfig(loadState(), cfg));
  }, [persist]);

  const remove = useCallback((id: string) => {
    persist(removeConfig(loadState(), id));
  }, [persist]);

  const setActive = useCallback((id: string) => {
    persist({ ...loadState(), activeId: id });
  }, [persist]);

  const openConfig = useCallback((id?: string) => {
    setEditingId(id ?? null);
    setConfigOpen(true);
  }, []);

  const value = useMemo<LlmContextValue>(() => {
    const active = activeConfig(state);
    return {
      ready, state, active,
      isConfigured: !!active,
      save, remove, setActive,
      tutorOpen,
      openTutor: () => setTutorOpen(true),
      closeTutor: () => setTutorOpen(false),
      configOpen, editingId,
      openConfig,
      closeConfig: () => setConfigOpen(false),
    };
  }, [ready, state, tutorOpen, configOpen, editingId, save, remove, setActive, openConfig]);

  return <Ctx.Provider value={value}>{children}</Ctx.Provider>;
}

export function useLlm(): LlmContextValue {
  const v = useContext(Ctx);
  if (!v) throw new Error('useLlm 必须在 <LlmProvider> 内使用');
  return v;
}
