# Atlas 100 案例清单（✅=已完成）

## A. AI 助手与 LLM 产品（7）
| # | 案例 | Tier | 核心看点 |
|---|---|---|---|
| A1 | ChatGPT ✅ | ★★★ | 模型架构 vs 服务架构双层、KV cache、连续批处理 |
| A2 | Claude / Gemini | ★★★ | 长上下文工程、Artifacts、agentic 编码环境的沙箱与工具协议 ✅ |
| A3 | Gemini | ★★ | 原生多模态、与 Google 生态（Search/Workspace）的集成架构 ✅ |
| A4 | GitHub Copilot ✅ | ★★★ | 编辑器内毫秒级补全：上下文收集、FIM、请求取消与缓存 |
| A5 | Perplexity | ★★ | 检索增强问答产品化：搜索编排 + 引用生成 ✅ |
| A6 | Cursor ✅ | ★★ | 代码库索引（嵌入+AST）、影子工作区、apply 模型 ✅ |
| A7 | Midjourney | ★ | 扩散模型推理服务与 Discord 作为前端的取舍 ✅ |

## B. 搜索与推荐（6）
| # | 案例 | Tier | 核心看点 |
|---|---|---|---|
| B1 | Google Search ✅ | ★★★ | 爬取-索引-服务三平面、倒排索引、排序信号演进（PageRank→学习排序→RankBrain/BERT） |
| B2 | Bing + Copilot | ★★ | 传统搜索接入 LLM 的编排层（Prometheus 架构） ✅ |
| B3 | Elasticsearch ✅ | ★★★ | Lucene 段结构、倒排+列存、分片与副本、近实时刷新 |
| B4 | Pinterest ✅ | ★★ | 视觉发现引擎：PinSage 图神经推荐、home feed 混排 ✅ |
| B5 | TikTok/抖音推荐 ✅ | ★★★ | Monolith 实时训练、特征哈希、兴趣探索 vs 利用 |
| B6 | YouTube 推荐 | ★★ | 两阶段召回+排序、观看时长目标演进 ✅ |

## C. 通讯与社交（8）
| # | 案例 | Tier | 核心看点 |
|---|---|---|---|
| C1 | WhatsApp ✅ | ★★★ | Erlang 百万连接、端到端加密、极简后端哲学 |
| C2 | X.com (Twitter) ✅ | ★★★ | 时间线 fanout 读写权衡、从 Ruby 单体到 JVM 微服务再到精简架构 |
| C3 | 微信 WeChat ✅ | ★★★ | 万亿消息、小程序容器架构、红包高并发 |
| C4 | Discord | ★★ | Elixir 网关、按 guild 分片、消息存储从 Mongo→Cassandra→ScyllaDB ✅ |
| C5 | Slack ✅ | ★★ | 工作区分片、实时消息总线、企业级权限模型 ✅ |
| C6 | Telegram | ★ | MTProto、多数据中心用户就近 |
| C7 | Instagram | ★★ | Django 单体的极限、feed 排序、Stories 的读扩散 |
| C8 | Zoom | ★★ | SFU 媒体路由、级联集群、弱网对抗 |

## D. 办公与协作（7）
| # | 案例 | Tier | 核心看点 |
|---|---|---|---|
| D1 | Microsoft 365 + Office Copilot ✅ | ★★★ | 文档格式演进（二进制→OOXML）、Graph 数据层、Copilot 的编排与权限继承 |
| D2 | Excel 计算引擎 ✅ | ★★★ | 依赖图重算、稀疏表存储、多线程重算演进 ✅ |
| D3 | Google Docs ✅ | ★★★ | OT 协同算法、为何不用 CRDT、离线合并 |
| D4 | Notion ✅ | ★★ | 万物阶 block 的数据模型、权限树、离线同步 ✅ |
| D5 | Figma ✅ | ★★★ | 浏览器里的 C++（WASM 渲染引擎）、多人协同 CRDT、multiplayer 服务器 |
| D6 | 飞书 Feishu ✅ | ★★ | IM+文档+审批一体化平台的组织架构数据模型 ✅ |
| D7 | Jira + Confluence ✅ | ★★ | 工作流状态机引擎、插件架构（如何让第三方安全扩展） ✅ |

## E. 操作系统谱系（10）
| # | 案例 | Tier | 核心看点 |
|---|---|---|---|
| E1 | Linux 内核（服务器） ✅ | ★★★ | 宏内核、调度器演进（O(1)→CFS→EEVDF）、VFS、epoll |
| E2 | Windows NT（桌面） ✅ | ★★ | 混合内核、HAL、Win32 子系统与 WSL ✅ |
| E3 | macOS / Darwin ✅ | ★★ | XNU=Mach+BSD 混合、沙箱与签名链 ✅ |
| E4 | Android ✅ | ★★★ | ART 运行时、Binder IPC、进程生命周期与 LMK |
| E5 | iOS ✅ | ★★ | 安全启动链、沙箱模型、Metal 图形栈 ✅ |
| E6 | FreeRTOS（嵌入式 MCU） ✅ | ★★ | 抢占式微型调度器、内存受限设计（几 KB RAM） ✅ |
| E7 | QNX（车载实时） ✅ | ★★ | 微内核消息传递、确定性延迟、故障隔离 ✅ |
| E8 | VxWorks（航天/特殊） ✅ | ★ | 硬实时、火星车上的优先级反转事故（经典案例） ✅ |
| E9 | ROS 2（机器人） ✅ | ★★★ | DDS 发布订阅、实时性改造、Nav2 行为树 ✅ |
| E10 | Fuchsia / Zircon ✅ | ★ | 能力安全微内核、组件化用户态——OS 的下一代实验 ✅ |

## F. 云平台与基础设施（10）
| # | 案例 | Tier | 核心看点 |
|---|---|---|---|
| F1 | AWS S3 ✅ | ★★★ | 11 个 9 的对象存储：分区、纠删码、强一致性改造（2020） |
| F2 | DynamoDB ✅ | ★★★ | 从 Dynamo 论文到全托管：一致性哈希→分区自动管理、自适应容量 |
| F3 | AWS Lambda ✅ | ★★ | Firecracker microVM、冷启动优化、事件驱动计费 ✅ |
| F4 | EC2 Nitro ✅ | ★★ | 虚拟化卸载到专用硬件的架构革命 ✅ |
| F5 | Azure Cosmos DB ✅ | ★★ | 五种一致性级别、多主全球分布 ✅ |
| F6 | Google Spanner ✅ | ★★★ | TrueTime、外部一致性、全球分布式 SQL |
| F7 | Borg → Kubernetes ✅ | ★XX | 声明式调和循环、控制器模式、etcd/Raft |
| F8 | Cloudflare Workers/Edge ✅ | ★★ | V8 isolate 多租户、全球任播、无区域架构 ✅ |
| F9 | Snowflake ✅ | ★★ | 存算分离、虚拟仓库、多集群共享数据 ✅ |
| F10 | Vercel ✅ | ★ | 前端云：构建产物不可变、边缘函数与 ISR ✅ |

## G. 数据与流处理（10）
| # | 案例 | Tier | 核心看点 |
|---|---|---|---|
| G1 | PostgreSQL ✅ | ★★★ | MVCC、WAL、B+树与 vacuum、扩展生态（pgvector） |
| G2 | Redis ✅ | ★★★ | 单线程事件循环为何快、数据结构编码、持久化与集群演进 |
| G3 | Kafka ✅ | ★★★ | 顺序写日志、零拷贝、ISR 复制、KRaft 去 ZooKeeper |
| G4 | ClickHouse ✅ | ★★ | 列存+向量化执行、MergeTree、为什么分析快 1000 倍 ✅ |
| G5 | Cassandra ✅ | ★★ | 无主复制、LSM、可调一致性 ✅ |
| G6 | MongoDB ✅ | ★ | 文档模型、从 MMAPv1 到 WiredTiger、分片演进 ✅ |
| G7 | SQLite ✅ | ★★ | 嵌入式单文件、世界部署量最大数据库的极简架构 ✅ |
| G8 | RocksDB ✅ | ★★ | LSM 树深度：memtable/SST/compaction 策略 ✅ |
| G9 | Flink ✅ | ★★ | 有状态流计算、checkpoint 对齐、exactly-once ✅ |
| G10 | Iceberg 数据湖 ✅ | ★★ | 表格式元数据层、快照隔离、湖仓一体 ✅ |

## H. 开发者工具链（8）
| # | 案例 | Tier | 核心看点 |
|---|---|---|---|
| H1 | Git ✅ | ★★★ | 内容寻址对象库、DAG、为什么分支几乎零成本 |
| H2 | GitHub ✅ | ★★ | 单体 Rails 的规模化、Spokes 三副本存储、Actions 调度 ✅ |
| H3 | GitLab CI ✅ | ★ | Runner 架构、流水线 DAG 调度 ✅ |
| H4 | VS Code ✅ | ★★★ | Electron 多进程、扩展宿主隔离、LSP 协议改变行业 |
| H5 | Docker ✅ | ★★★ | namespace+cgroup+联合文件系统、镜像分层与 OCI |
| H6 | Bazel ✅ | ★ | 远程缓存+沙箱的可复现构建、Google 单仓库工程学 ✅ |
| H7 | npm registry ✅ | ★ | 全球最大包仓库：CDN 化、依赖解析的演进 ✅ |
| H8 | Sentry ✅ | ★ | 错误聚合指纹、事件洪峰削峰 ✅ |

## I. 流媒体与内容（5）
| # | 案例 | Tier | 核心看点 |
|---|---|---|---|
| I1 | Netflix ✅ | ★★★ | 微服务先驱：Zuul/Eureka/Hystrix 谱系、Open Connect 自建 CDN、混沌工程 |
| I2 | Spotify ✅ | ★★ | 音频分发、Discover Weekly 推荐管线、squad 组织与架构关系 ✅ |
| I3 | YouTube 视频管线 ✅ | ★★ | 上传→转码→多码率分发、Vitess 分库 MySQL ✅ |
| I4 | Twitch ✅ | ★★ | 直播吞吐、转码集群、聊天系统百万房间 ✅ |
| I5 | TikTok 视频管线 ✅ | ★ | 短视频冷启动分发、边缘缓存策略 ✅ |

## J. 电商、支付与出行（8）
| # | 案例 | Tier | 核心看点 |
|---|---|---|---|
| J1 | Amazon 电商 ✅ | ★★★ | 从单体到 SOA 的祖师爷、购物车高可用（Dynamo 起源） |
| J2 | Shopify ✅ | ★★ | 多租户架构演进、Pod 物理隔离、闪购秒杀防护 ✅ |
| J3 | Stripe ✅ | ★★★ | 支付状态机、幂等键设计、API 版本化哲学 |
| J4 | 支付宝双 11 ✅ | ★★ | 单元化 LDC 架构、OceanBase、洪峰限流 ✅ |
| J5 | Uber ✅ | ★★★ | H3 地理索引、派单撮合、从 Postgres 到 Schemaless 再到 Docstore |
| J6 | Airbnb ✅ | ★ | 搜索排序、服务化迁移的教训 ✅ |
| J7 | 美团/DoorDash ✅ | ★★ | 履约调度：预估送达时间、骑手路径规划 ✅ |
| J8 | 12306 ✅ | ★★ | 春运抢票：余票查询与出票分离、排队削峰 ✅ |

## K. AI 训练与推理基建（8）
| # | 案例 | Tier | 核心看点 |
|---|---|---|---|
| K1 | vLLM ✅ | ★★★ | PagedAttention（OS 虚拟内存思想进推理）、连续批处理 |
| K2 | Megatron-LM ✅ | ★★ | 3D 并行（数据/张量/流水线）、万卡训练的通信拓扑 ✅ |
| K3 | Ray | ★★ | 分布式 actor/task、对象存储 plasma、RLHF 基座 ✅ |
| K4 | Triton Inference Server ✅ | ★ | 多框架统一推理、动态批处理、模型集成 ✅ |
| K5 | Milvus 向量数据库 | ★★ | 存算分离的向量检索、HNSW/IVF 索引选型 |
| K6 | MCP 协议生态 ✅ | ★★★ | 模型-工具解耦的 USB 时刻：host/client/server、能力协商 |
| K7 | LangGraph / Agent 框架 | ★★ | 图状态机编排、checkpoint、human-in-the-loop ✅ |
| K8 | GPU 集群调度 | ★★ | Slurm vs K8s、gang scheduling、拓扑感知与碎片治理 |

## L. 游戏与实时系统（4）
| # | 案例 | Tier | 核心看点 |
|---|---|---|---|
| L1 | MOBA 同步（王者荣耀） | ★★ | 帧同步 vs 状态同步、确定性锁步、断线重连 |
| L2 | Minecraft 服务器 | ★ | 区块加载、tick 循环、单线程瓶颈与社区优化 |
| L3 | Roblox | ★★ | UGC 平台：脚本沙箱、物理分布式模拟 |
| L4 | 游戏引擎（Unreal） | ★ | ECS vs Actor、渲染管线、资产流送 |

## M. 安全与身份（4）
| # | 案例 | Tier | 核心看点 |
|---|---|---|---|
| M1 | Signal 协议 ✅ | ★★★ | 双棘轮、前向保密——被 WhatsApp/Messenger 采纳的加密架构 |
| M2 | OAuth2 / OIDC 生态 | ★★ | 授权码流程、token 设计、为什么密码永不出域 |
| M3 | Let's Encrypt | ★ | ACME 自动化 PKI，把 HTTPS 变成默认值的架构 |
| M4 | 1Password | ★ | 零知识架构：两把钥匙派生、同步而不泄密 |

## N. 网络与去中心化（5）
| # | 案例 | Tier | 核心看点 |
|---|---|---|---|
| N1 | DNS 全球体系 | ★★ | 层级委托、任播根服务器、缓存 TTL 的博弈 |
| N2 | CDN（Akamai 原理） | ★★ | 边缘缓存、回源策略、动态加速 |
| N3 | BitTorrent | ★★ | 分块交换、tit-for-tat 激励、DHT 去中心化索引 |
| N4 | Bitcoin | ★★ | UTXO、工作量证明、最长链共识的取舍 |
| N5 | NTP 时间同步 | ★ | 层级时钟源、时钟偏移估计——分布式系统的隐形地基 |
