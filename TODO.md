# 项目执行 TODO 清单

---

## 阶段二：课程章节富化任务 (13 项)

每个模块为一个独立任务会话，严格遵循《项目宪法》第 2 条“章节富化”规则：只插入不删除，包含图解 (≥3)、交互 (≥1)、实验及测验 (≥3)。

- [x] **M01: 编程系统基石** 富化任务 ✅
- [x] **M02: 系统设计之桥** 富化任务 ✅
- [x] **M03: 数据、缓存与队列** 富化任务 ✅
- [x] **M04: 设计模式与 LLD** 富化任务 ✅
- [x] **M05: 分布式核心组件** 富化任务 ✅
- [x] **M06: 云原生与企业级架构** 富化任务 ✅
- [x] **M07: 大语言模型系统** 富化任务 ✅
- [x] **M08: RAG 检索增强系统** 富化任务 ✅
- [x] **M9: Agent 智能体架构** 富化任务 ✅
- [x] **M10: Multi-Agent 多智能体协议** 富化任务 ✅
- [x] **M11: 生产级 AI 平台** 富化任务 ✅
- [x] **M12: 毕业设计 Capstone** 富化任务 ✅

---

## 阶段三：100 个架构案例库 (Atlas) 扩建任务 (100 项)

按 `PROMPTS/atlas-manifest.md` 列表，执行增量填充。以下为核心优先（Tier 1）及各分类代表案例，逐步划掉：

### 优先启动的旗舰案例 (Tier 1 深度案例)
- [x] **A1. ChatGPT** (模型架构与推理服务器架构) - 已完成 ✅
- [x] **C1. WhatsApp** (Erlang 百万长连接极简后端) - 已完成 ✅
- [x] **A4. GitHub Copilot** (毫秒级补全上下文收集与缓存) ✅
- [x] **B1. Google Search** (爬取-索引-服务三平面、倒排与 PageRank 演进) ✅
- [x] **B3. Elasticsearch** (Lucene 段结构、倒排列存、分片与近实时) ✅
- [x] **B5. TikTok/抖音推荐** (Monolith 实时训练、特征哈希与召回排序) ✅
- [x] **C2. Twitter/X.com** (时间线 Fanout 读写权衡、微服务极简演进) ✅
- [x] **C3. 微信 WeChat** (万亿消息与红包高并发单元化架构) ✅
- [x] **D1. Office 365 + Copilot** (Graph 数据层、协作编排与安全控制) ✅
- [x] **D3. Google Docs** (OT 协同算法与离线合并机制) ✅
- [x] **D5. Figma** (WASM 渲染引擎与 multiplayer 协同服务器) ✅
- [x] **E1. Linux 内核** (宏内核、调度器 CFS/EEVDF、VFS、epoll) ✅
- [x] **E4. Android 操作系统** (ART 运行时、Binder IPC 及 LMK) ✅
- [x] **F1. AWS S3** (11个9对象存储、分区纠删码与强一致性改造) ✅
- [x] **F2. DynamoDB** (一致性哈希、分区自动管理与自适应容量) ✅
- [x] **F6. Google Spanner** (TrueTime、外部一致性、全球 SQL) ✅
- [x] **F7. Kubernetes** (声明式调和循环、控制器模式、etcd 集群) ✅
- [x] **G1. PostgreSQL** (MVCC、WAL、B+ 树与扩展 pgvector) ✅
- [x] **G2. Redis** (单线程事件循环、数据结构编码与集群高可用) ✅
- [x] **G3. Kafka** (顺序写日志、零拷贝、ISR 副本与 KRaft 去 ZK) ✅
- [ ] **H1. Git** (内容寻址对象库、DAG 结构与零成本分支)
- [ ] **H4. VS Code** (Electron 多进程、扩展宿主隔离与 LSP 协议)
- [ ] **H5. Docker** (Namespaces, Cgroups, UnionFS, 镜像分层)
- [ ] **I1. Netflix** (微服务 Zuul/Eureka 体系与自建 CDN)
- [ ] **J1. Amazon 电商** (SOA 架构与购物车 Dynamo 高可用起源)
- [ ] **J3. Stripe** (支付状态机、幂等键设计、API 版本控制)
- [ ] **J5. Uber** (H3 地理索引、派单撮合与 Docstore)
- [ ] **K1. vLLM** (PagedAttention 显存管理、连续批处理)
- [ ] **K6. MCP 协议** (模型-工具解耦的 Host-Server USB 生态)
- [ ] **M1. Signal 协议** (双棘轮、前向安全保密通讯协议)

*注：详细 100 案例清单及进度，请至 `PROMPTS/atlas-manifest.md` 查看。*

---

## 阶段四：全站 QA 与离线验收

- [ ] **构建无警告**：实现全站零 Warn 编译。
- [ ] **断链审计**：检查并修复所有 Markdown 内链与 Atlas 回链。
- [ ] **质量门槛自检**：统计每篇 Mermaid (≥3) / 交互 (≥1) / 测验 (≥3) 达标度。
- [ ] **术语一致性**：整合 GlossaryTerm 生成汇总术语页 `docs/glossary.mdx`。
- [ ] **完全离线测试**：断网环境下运行 `npx serve build` 验证所有交互和 Python 运行功能。
