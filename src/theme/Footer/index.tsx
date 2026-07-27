// src/theme/Footer/index.tsx
// Wrapper swizzle：保留原 Footer，加一行品牌带。
import React from 'react';
import Footer from '@theme-original/Footer';
import type FooterType from '@theme/Footer';
import type { WrapperProps } from '@docusaurus/types';

type Props = WrapperProps<typeof FooterType>;

export default function FooterWrapper(props: Props): JSX.Element {
  return (
    <>
      <div style={{
        borderTop: '1px solid var(--comp-border)',
        background: 'var(--ifm-footer-background-color)',
        padding: '14px 24px',
        display: 'flex', alignItems: 'center', gap: 10,
        fontSize: 12, color: 'var(--comp-text-muted)',
        justifyContent: 'center', flexWrap: 'wrap',
      }}>
        <span style={{
          width: 20, height: 20, borderRadius: 6, display: 'grid', placeItems: 'center',
          background: 'var(--comp-gradient)', color: '#fff', fontWeight: 700, fontSize: 11,
        }} aria-hidden>A</span>
        从零到 AI Architect · 13 个月 · 130+ 节 · 102 个 Atlas 案例 · LLM-agnostic
      </div>
      <Footer {...props} />
    </>
  );
}
