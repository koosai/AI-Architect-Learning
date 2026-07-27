// src/data/course.ts — 课程结构（真实标题，来自仓库 docs/ 与 sidebars.ts）
export interface Lesson { id: string; code: string; zh: string; en: string; slug: string; week: number; min: string; }
export interface Month { n: number; zh: string; en: string; topics: string; dir: string; lessons: number; hours: string; phase: 0 | 1 | 2; }

export const MONTHS: Month[] = [
  { n: 0, zh: '开启学习之旅', en: 'Getting Started', topics: '学习方法 · 路线 · 环境', dir: '00-start', lessons: 5, hours: '6h', phase: 0 },
  { n: 1, zh: '编程系统基石', en: 'Foundations', topics: '边界 · 幂等 · 并发 · 请求链路 · p99', dir: '01-foundations', lessons: 16, hours: '28h', phase: 0 },
  { n: 2, zh: '系统设计之桥', en: 'System Design', topics: '接口契约 · C4 · 演进式架构', dir: '02-system-design-bridge', lessons: 13, hours: '26h', phase: 0 },
  { n: 3, zh: '数据、缓存与队列', en: 'Data · Cache · Queue', topics: '读写分离 · 缓存失效 · MQ 削峰', dir: '03-data-cache-queue', lessons: 13, hours: '27h', phase: 1 },
  { n: 4, zh: '设计模式与 LLD', en: 'Patterns & LLD', topics: 'DDD · 设计模式 · 业务重构', dir: '04-design-patterns-lld', lessons: 13, hours: '25h', phase: 1 },
  { n: 5, zh: '核心组件', en: 'Core Components', topics: '负载均衡 · 网关 · 限流 · 熔断 · 复制 · 分片 · 共识', dir: '05-core-components', lessons: 12, hours: '30h', phase: 1 },
  { n: 6, zh: '云原生与企业级架构', en: 'Cloud Native', topics: 'Service Mesh · 微服务 · 容器编排', dir: '06-cloud-enterprise-industrial', lessons: 12, hours: '28h', phase: 1 },
  { n: 7, zh: 'LLM 系统', en: 'LLM Systems', topics: 'Tokenizer · KV Cache · 显存 · 量化', dir: '07-llm-systems', lessons: 12, hours: '30h', phase: 2 },
  { n: 8, zh: 'RAG 检索增强', en: 'RAG', topics: '向量库 · Hybrid Search · GraphRAG', dir: '08-rag', lessons: 12, hours: '26h', phase: 2 },
  { n: 9, zh: 'Agent 智能体架构', en: 'Agents', topics: 'ReAct · Function Calling · 记忆规划', dir: '09-agent-architectures', lessons: 12, hours: '27h', phase: 2 },
  { n: 10, zh: 'Multi-Agent 协议', en: 'Multi-Agent', topics: '多智能体协同 · Supervisor 编排', dir: '10-multi-agent-protocols', lessons: 11, hours: '24h', phase: 2 },
  { n: 11, zh: '生产级 AI 平台', en: 'Production AI', topics: 'Guardrails · 评估系统 · 成本工程', dir: '11-production-ai-platform', lessons: 12, hours: '29h', phase: 2 },
  { n: 12, zh: '毕业设计 Capstone', en: 'Capstone', topics: '端到端生产级 AI 架构 + ADR', dir: '12-capstone', lessons: 6, hours: '40h', phase: 2 },
];

export const PHASES = ['工程地基 Engineering Foundations', '分布式核心 Distributed Core', 'AI 架构 AI Architecture'];

// Month 1 · 16 节（来自 docs/01-foundations/overview.mdx 的地图）
export const MONTH1_LESSONS: Lesson[] = [
  { id: 'm1l1', code: 'L1', zh: '编程如何变成系统', en: 'Programming → System', slug: '/foundations/programming-systems-primer', week: 1, min: '4-6h' },
  { id: 'm1l2', code: 'L2', zh: '模块、契约与信息隐藏', en: 'Modules & Contracts', slug: '/foundations/modules-and-contracts', week: 1, min: '2h' },
  { id: 'm1l3', code: 'L3', zh: '输入校验与防御性编程', en: 'Input Validation', slug: '/foundations/input-validation', week: 1, min: '2h' },
  { id: 'm1l4', code: 'L4', zh: '错误处理与异常设计', en: 'Error Handling', slug: '/foundations/error-handling', week: 1, min: '2h' },
  { id: 'm1l5', code: 'L5', zh: '状态放在哪里', en: 'State & Storage', slug: '/foundations/state-and-storage', week: 2, min: '2h' },
  { id: 'm1l6', code: 'L6', zh: '幂等性深入', en: 'Idempotency', slug: '/foundations/idempotency', week: 2, min: '2.5h' },
  { id: 'm1l7', code: 'L7', zh: '数据建模入门', en: 'Data Modeling', slug: '/foundations/data-modeling', week: 2, min: '2h' },
  { id: 'm1l8', code: 'L8', zh: '并发与竞态条件', en: 'Concurrency', slug: '/foundations/concurrency-basics', week: 2, min: '2.5h' },
  { id: 'm1l9', code: 'L9', zh: 'API 与 HTTP', en: 'API & HTTP', slug: '/foundations/api-and-http', week: 3, min: '2h' },
  { id: 'm1l10', code: 'L10', zh: '一次请求的完整链路', en: 'Request Path', slug: '/foundations/request-path', week: 3, min: '2.5h' },
  { id: 'm1l11', code: 'L11', zh: '同步/异步、超时与背压', en: 'Sync/Async/Timeout', slug: '/foundations/sync-async-timeout', week: 3, min: '2.5h' },
  { id: 'm1l12', code: 'L12', zh: '可观察性深入', en: 'Observability', slug: '/foundations/observability', week: 3, min: '2h' },
  { id: 'm1l13', code: 'L13', zh: '测试与 TDD', en: 'Testing & TDD', slug: '/foundations/testing-and-tdd', week: 4, min: '2h' },
  { id: 'm1l14', code: 'L14', zh: '配置、环境与部署', en: 'Config & Deploy', slug: '/foundations/config-and-deploy', week: 4, min: '2h' },
  { id: 'm1l15', code: 'L15', zh: '性能与延迟', en: 'Performance & Latency', slug: '/foundations/performance-and-latency', week: 4, min: '2h' },
  { id: 'm1l16', code: 'L16', zh: '月末 Capstone', en: 'Month-1 Capstone', slug: '/foundations/month1-capstone', week: 4, min: '4h' },
];

export const WEEK_THEMES: Record<number, string> = {
  1: '程序的构件与边界', 2: '状态、数据与一致性入门', 3: '把代码变成服务', 4: '工程化与综合实战',
};
