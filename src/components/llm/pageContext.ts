// src/components/llm/pageContext.ts
// 抓取当前课程页面的可读上下文，喂给助手（截断以控 token）。
export function getPageContext(maxChars = 4000): string {
  if (typeof document === 'undefined') return '';
  const title = document.title || '';
  // Docusaurus 正文容器
  const article =
    document.querySelector('article .markdown') ||
    document.querySelector('.theme-doc-markdown') ||
    document.querySelector('main article') ||
    document.querySelector('main');
  let body = '';
  if (article) {
    body = (article as HTMLElement).innerText || '';
    body = body.replace(/\n{3,}/g, '\n\n').trim();
  }
  const url = typeof location !== 'undefined' ? location.pathname : '';
  const head = `页面标题：${title}\n路径：${url}\n\n正文（截断）：\n`;
  const budget = Math.max(0, maxChars - head.length);
  return head + body.slice(0, budget);
}

export function getPageTitle(): string {
  if (typeof document === 'undefined') return '';
  const h1 = document.querySelector('article h1, main h1');
  return (h1 as HTMLElement)?.innerText?.trim() || document.title || '';
}
