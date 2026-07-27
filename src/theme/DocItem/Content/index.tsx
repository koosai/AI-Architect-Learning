// src/theme/DocItem/Content/index.tsx
// Wrapper swizzle：在原课程正文上方注入 AI 助手工具条。不改动 Docusaurus 原渲染。
import React from 'react';
import Content from '@theme-original/DocItem/Content';
import type ContentType from '@theme/DocItem/Content';
import type { WrapperProps } from '@docusaurus/types';
import LessonToolbar from '@site/src/components/llm/LessonToolbar';

type Props = WrapperProps<typeof ContentType>;

export default function ContentWrapper(props: Props): JSX.Element {
  return (
    <>
      <LessonToolbar />
      <Content {...props} />
    </>
  );
}
