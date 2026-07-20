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
- [x] **F8. Cloudflare Workers/Edge**：基于 V8 Isolate 的高密度、 Anycast 路由无区域 Serverless 架构 ✅
- [x] **F9. Snowflake**：云原生存算分离、多集群共享数据与零拷贝克隆数仓架构 ✅
- [x] **F10. Vercel**：构建产物不可变一键回滚与增量静态再生成 (ISR) 前端云架构 ✅
- [x] **G4. ClickHouse**：列存物理布局、CPU SIMD 向量化执行与 MergeTree 稀疏索引分析数仓架构 ✅
- [x] **G5. Cassandra**：无主对等拓扑、Gossip 成员协议、可调一致性与 Merkle 树反熵对齐数仓架构 ✅
- [x] **G6. MongoDB**：BSON 文档模型、WiredTiger MVCC 引擎与分片集群自动平衡架构 ✅
- [x] **G7. SQLite**：嵌入式单文件、VDBE 字节码虚拟机、WAL 预写日志与 VFS 抽象架构 ✅
- [x] **G8. RocksDB**：高吞吐 LSM-Tree 存储引擎、Memtable 跳表、SSTable 分级压实与 Bloom Filter 读优化架构 ✅
- [x] **G9. Flink**：有状态流计算、Watermark 乱序处理、ABS 屏障检查点与端到端 Exactly-Once 2PC 架构 ✅
- [x] **G10. Apache Iceberg**：表格式元数据树、隐式分区、ACID 事务快照隔离与时间旅行湖仓一体架构 ✅
- [x] **H2. GitHub**：Modular Monolith 架构、Spokes 三副本 Git 存储与 Actions 弹性编排架构 ✅
- [x] **H3. GitLab CI**：Runner Go 代理长轮询、`needs` DAG 拓扑调度与 S3 产物缓存架构 ✅
- [x] **H6. Bazel**：Starlark 声明式依赖图、Hermetic Linux 沙箱隔离、CAS 远程缓存与 RBE 分布式构建架构 ✅
- [x] **H7. npm registry**：Fastly CDN 离岸缓存、CouchDB `_changes` 镜像复制与 pnpm CAS 硬链接依赖树架构 ✅
- [x] **H8. Sentry**：Rust Relay 边缘代理脱敏、堆栈帧 Fingerprint 指纹归平与 Snuba/ClickHouse 列存检索架构 ✅
- [x] **I3. YouTube**：GGC 运营商 PoP 边缘节点、微切片并行转码、DASH 自适应码率与双阶段 DNN 推荐架构 ✅
- [x] **I2. Spotify**：Ogg 16KB 预加载音频分发、Discover Weekly 三合一推荐 (ALS+NLP+CNN) 与 Squad 组织架构 ✅
- [x] **I4. Twitch**：RTMP 推流入库、2s GOP GPU 实时切片转码、LL-HLS 低延迟与 TMI 百万房间 Ring Buffer 扇出架构 ✅
- [x] **I5. TikTok**：ByteVC1 竖屏转码、流量池层级递进推荐、完播率加权与客户端 Smart Preloader 0ms 秒开架构 ✅
- [x] **J2. Shopify**：Pod 物理隔离 SaaS 架构、Sorting Hat 路由、Live Migration 与 Redis Lua 脚本秒杀防超卖架构 ✅
- [x] **J4. 支付宝双 11**：LDC 单元化异地多活 (RZone/GZone/CZone)、OceanBase Paxos 强一致与多级限流降级架构 ✅
- [x] **J6. Airbnb**：Service Blocks 模块化架构收敛、Geohash 召回 + Listing Embedding 搜推与日历防重锁架构 ✅
- [x] **J7. 美团 / DoorDash**：实时派单撮合 (KM 算法)、三阶段 ETA 深度学习引擎、H3 顺路拼单与骑手 TSP 路线规划架构 ✅
- [x] **J8. 12306**：余票查询与出票物理读写分离 (GemFire/Redis 内存网格)、沿途站区间乘法 BitMatrix 扣减与异步排队削峰架构 ✅
- [x] **K4. Megatron-LM**：3D 混合并行架构 (TP/PP/DP)、列/行矩阵切片、1F1B 流水线调度与 NVLink 通信拓扑架构 ✅
- [x] **K4. Triton Inference Server**：多后端 C-API 统一推理引擎 (TensorRT/ONNX/PyTorch)、5ms Dynamic Batching 动态组包与 CUDA IPC 零拷贝显存架构 ✅
- [x] **K5. Milvus**：云原生存算分离架构 (Query Node + S3/MinIO + Pulsar WAL)、Knowhere C++ 引擎、HNSW/IVF-PQ 动态索引选型与 BitSet 混合检索架构 ✅
- [x] **K8. GPU 集群调度**：Slurm HPC 批处理 vs K8s Volcano 云原生调度、Gang Scheduling (All-or-Nothing) 0 死锁锁、NVLink/NUMA 树状拓扑感知与 GPU 碎片装箱重组架构 ✅
- [x] **L1. MOBA 同步 (王者荣耀)**：确定性帧同步 (Deterministic Lockstep)、15 FPS 66ms 逻辑帧打包、定点数 (Fixed-Point Math) 跨平台一致性、KCP/FEC 弱网可靠传输与断线追帧 (Frame Chase) 架构 ✅
- [x] **L2. Minecraft 服务器**：20 TPS (50ms) 逻辑 Tick 循环、Anvil Region File (.mca) 格式、PaperMC 异步区块 (Chunk) I/O 与 Folia 区域多线程 (Regional Multithreading) 架构 ✅
- [x] **L3. Roblox**：Luau 渐进类型化脚本沙箱隔离、Memory/Instruction 限制、Network Ownership 动态物理计算权卸载与 DataModel DOM 树差量复制架构 ✅
- [x] **L4. 游戏引擎 (Unreal Engine 5)**：Mass Entity (ECS) SOA 内存连续布局 vs AActor 层次结构、Nanite 虚拟几何体 Cluster 剔除、Lumen 实时光照与 World Partition 动态资产流送 (Asset Streaming) 架构 ✅
- [x] **M1. Auth0 / Okta**：OAuth 2.0 & OIDC 标准、Authorization Code Flow with PKCE 防截获、JWKS (JSON Web Key Set) RS256 0 查库验签、多租户物理隔离与 Auth0 Actions 管道钩子架构 ✅
- [x] **M3. Let's Encrypt**：ACME 协议 (RFC 8555) 自动化轮转、HTTP-01 / DNS-01 域名所有权校验挑战、Boulder C++ 架构与 90 天短生命周期 (Short-Lived Certs) 安全机制 ✅
