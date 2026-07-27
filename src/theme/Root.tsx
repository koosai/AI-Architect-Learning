// src/theme/Root.tsx
// Docusaurus 自动用 src/theme/Root 包裹整个应用（无需 swizzle eject）。
// 这里挂载全局 LLM 上下文 + 浮动 AI 助手 + 配置模态。
// 助手 UI 仅在浏览器渲染（BrowserOnly），SSG 构建安全。
import React from 'react';
import BrowserOnly from '@docusaurus/BrowserOnly';
import { LlmProvider } from '@site/src/components/llm/LlmContext';

export default function Root({ children }: { children: React.ReactNode }) {
  return (
    <LlmProvider>
      {children}
      <BrowserOnly>
        {() => {
          const AiTutor = require('@site/src/components/llm/AiTutor').default;
          const LlmConfigModal = require('@site/src/components/llm/LlmConfigModal').default;
          return (
            <>
              <AiTutor />
              <LlmConfigModal />
            </>
          );
        }}
      </BrowserOnly>
    </LlmProvider>
  );
}
