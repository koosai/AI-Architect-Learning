// src/components/llm/types.ts
// BYO-LLM 类型定义（LLM-agnostic：任意 OpenAI 兼容服务）
export type ProviderId =
  | 'openai' | 'anthropic' | 'gemini' | 'deepseek'
  | 'qwen' | 'openrouter' | 'azure' | 'local' | 'custom';

export interface LlmConfig {
  id: string;              // uuid
  label: string;           // 用户起的名字，如“我的 GPT-5.5”
  provider: ProviderId;
  baseUrl: string;         // OpenAI 兼容 endpoint，例如 https://api.openai.com/v1
  apiKey: string;          // 仅存本地
  model: string;           // 模型名
  temperature: number;     // 0–2
  maxTokens: number;
  createdAt: number;
}

export interface LlmState {
  configs: LlmConfig[];
  activeId: string | null;
}

export interface ChatMessage {
  role: 'system' | 'user' | 'assistant';
  content: string;
}

export interface ProviderPreset {
  id: ProviderId;
  name: string;
  mono: string;
  color: string;
  hint: string;
  baseUrl: string;
  model: string;
}

export const PROVIDER_PRESETS: ProviderPreset[] = [
  { id: 'openai', name: 'OpenAI', mono: 'AI', color: '#10a37f', hint: 'GPT-5.5 · 4o', baseUrl: 'https://api.openai.com/v1', model: 'gpt-4o' },
  { id: 'anthropic', name: 'Claude', mono: 'CL', color: '#d97757', hint: 'Opus · Sonnet', baseUrl: 'https://api.anthropic.com/v1', model: 'claude-sonnet-4-5' },
  { id: 'gemini', name: 'Gemini', mono: 'GG', color: '#4285f4', hint: '2.5 Pro', baseUrl: 'https://generativelanguage.googleapis.com/v1beta/openai', model: 'gemini-2.5-pro' },
  { id: 'deepseek', name: 'DeepSeek', mono: 'DS', color: '#4d6bfe', hint: 'V3 · R1', baseUrl: 'https://api.deepseek.com/v1', model: 'deepseek-chat' },
  { id: 'qwen', name: 'Qwen', mono: 'Q', color: '#615ced', hint: 'Qwen3', baseUrl: 'https://dashscope.aliyuncs.com/compatible-mode/v1', model: 'qwen-max' },
  { id: 'openrouter', name: 'OpenRouter', mono: 'OR', color: '#8b5cf6', hint: '多模型聚合', baseUrl: 'https://openrouter.ai/api/v1', model: 'openai/gpt-4o' },
  { id: 'azure', name: 'Azure', mono: 'AZ', color: '#0078d4', hint: '企业部署', baseUrl: 'https://YOUR.openai.azure.com/openai/deployments/YOUR', model: 'gpt-4o' },
  { id: 'local', name: '本地/自托管', mono: '▤', color: '#22c55e', hint: 'vLLM·Ollama', baseUrl: 'http://localhost:11434/v1', model: 'llama3.1' },
];
