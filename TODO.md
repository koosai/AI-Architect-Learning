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
- [x] **H1. Git** (内容寻址对象库、DAG 结构与零成本分支) ✅
- [x] **H4. VS Code** (Electron 多进程、扩展宿主隔离与 LSP 协议) ✅
- [x] **H5. Docker** (Namespaces, Cgroups, UnionFS, 镜像分层) ✅
- [x] **I1. Netflix** (微服务 Zuul/Eureka 体系与自建 CDN) ✅
- [x] **J1. Amazon 电商** (SOA 架构与购物车 Dynamo 高可用起源) ✅
- [x] **J3. Stripe** (支付状态机、幂等键设计、API 版本控制) ✅
- [x] **J5. Uber** (H3 地理索引、派单撮合与 Docstore) ✅
- [x] **K1. vLLM** (PagedAttention 显存管理、连续批处理) ✅
- [x] **K6. MCP 协议** (模型-工具解耦的 Host-Server USB 生态) ✅
- [x] **M1. Signal 协议** (双棘轮、前向安全保密通讯协议) ✅

*注：详细 100 案例清单及进度，请至 `PROMPTS/atlas-manifest.md` 查看。*

---

## 阶段四：全站 QA 与离线验收

- [x] **构建无警告**：实现全站零 Warn 编译。 ✅
- [x] **断链审计**：检查并修复所有 Markdown 内链与 Atlas 回链。 ✅
- [x] **质量门槛自检**：统计每篇 Mermaid (≥3) / 交互 (≥1) / 测验 (≥3) 达标度。 ✅
- [x] **术语一致性**：整合 GlossaryTerm 生成汇总术语页 `docs/glossary.mdx`。 ✅
- [x] **完全离线测试**：断网环境下运行 `npx serve build` 验证所有交互和 Python 运行功能。 ✅

## 阶段五：Atlas 案例增量扩建 (A2)

- [x] **A2. Claude / Gemini**：长上下文工程与 AI Artifacts 容器化沙箱架构 ✅
- [x] **K7. LangGraph / Agent 框架**：基于状态图的多智能体编排与容错架构 ✅
- [x] **A3. Gemini**：原生多模态与 Google 搜索/Workspace 生态集成架构 ✅
- [x] **A5. Perplexity**：RAG 搜索问答产品化与多源并发检索编排架构 ✅
- [x] **C4. Discord**：Elixir 网关、按 Guild 分片与 ScyllaDB 存储架构 ✅
- [x] **F3. AWS Lambda**：基于 Firecracker microVM 的 Serverless 架构与冷启动优化 ✅
- [x] **K3. Ray**：分布式 Actor 调度与大模型训练/RLHF 基座架构 ✅
- [x] **A7. Midjourney**：扩散模型推理服务与 Discord 作为前端的取舍 ✅
- [x] **B2. Bing + Copilot**：传统搜索与 LLM 绑定的 Prometheus 编排架构 ✅
- [x] **B6. YouTube 推荐**：两阶段召回+排序、观看时长目标演进 ✅
- [x] **A6. Cursor**：代码库索引（嵌入+AST）、影子工作区、apply 模型 ✅
- [x] **B4. Pinterest**：PinSage 图神经网络推荐与 home feed 混排 ✅
- [x] **C5. Slack**：工作区分片、实时消息总线、企业级权限模型 ✅
- [x] **D2. Excel**：依赖图重算、稀疏表存储、多线程重算演进 ✅
- [x] **D4. Notion**：万物皆 block 的数据模型、权限树、离线同步 ✅
- [x] **D6. 飞书 Feishu**：IM+文档+审批一体化平台的组织架构数据模型 ✅
- [x] **D7. Jira + Confluence**：工作流状态机引擎、插件架构（如何让第三方安全扩展） ✅
- [x] **E2. Windows NT**：混合内核、HAL、Win32 子系统与 WSL ✅
- [x] **E3. macOS / Darwin**：XNU=Mach+BSD 混合、沙箱与签名链 ✅
- [x] **E5. iOS**：安全启动链、沙箱模型、Metal 图形栈 ✅
- [x] **E6. FreeRTOS**：抢占式微型调度器、内存受限设计（几 KB RAM） ✅
- [x] **E7. QNX**：微内核消息传递、确定性延迟、故障隔离 ✅
- [x] **E8. VxWorks**：硬实时、火星车上的优先级反转事故（经典案例） ✅
- [x] **E9. ROS 2**：DDS 发布订阅、实时性改造、Nav2 行为树 ✅
- [x] **E10. Fuchsia / Zircon**：能力安全微内核、组件化用户态——OS 的下一代实验 ✅
- [x] **F4. EC2 Nitro**：基于专属 ASIC 控制卡的虚拟化硬件卸载与 Enclaves 架构 ✅
- [x] **F5. Azure Cosmos DB**：全球一致性光谱、多主复制与冲突合并架构 ✅

