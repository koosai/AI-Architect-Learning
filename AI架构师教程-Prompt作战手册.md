# AI 架构师教程 · 交互式学习站 —— Prompt 作战手册

> 目标：把 目录 里的 172 篇 MDX 教材，变成一个**本地部署、重交互、重图解、含可运行实验、带 100 个架构案例**的完整学习站。
> 本手册回答一个问题：**该用什么 prompt、按什么顺序、在什么工具里，才能把这件大事做成。**

---

## 0. 先说结论：不是"一个 prompt"，而是"一套 prompt 流水线"

这个项目的体量决定了单条 prompt 必然失败，原因有三：

1. **上下文物理极限**。172 篇现有内容 + 100 个案例（每个 300~800 行）+ 一整套 React 组件库，总产出量在几百万 token 量级，任何模型的单次会话都装不下。
2. **质量衰减**。让 AI 在一次会话里连续生成 20 个案例，第 15 个的质量一定断崖式下跌——图变少、来源开始编造、结构开始偷懒。
3. **真实系统架构容易被"自信地编造"**。WhatsApp、Spanner、vLLM 这些系统的架构细节必须来自工程博客和论文。没有约束的 prompt 会让 AI 把"合理想象"写成"事实"，这在一个教学项目里是致命的。

所以正确的打法是：**一份"项目宪法"（写进仓库常驻）+ 四个阶段的可复用 prompt 模板 + 一份 100 案例清单（manifest）**，像工厂流水线一样一个模块一个模块、一个案例一个案例地跑，每跑完一步就 `git commit` 存档。

**工具选择**：这是一个仓库级工程项目（建站 + 写组件 + 批量生成内容 + 反复构建验证），主力工具应该是 **Gemini**（命令行/桌面版），而不是聊天窗口。Gemini 能直接读写整个仓库、运行 `npm run build` 自我验证、按清单逐项执行。聊天窗口适合做单个案例的初稿或润色。

---

## 1. 现状盘点：目录 里有什么、缺什么

### 已有（这是很大的资产）

| 资产 | 说明 |
|---|---|
| 172 篇 MDX 教材 | 13 个模块（Month 0~12），从编程基础 → 系统设计 → 数据/缓存/队列 → 设计模式 → 分布式组件 → 云原生 → LLM → RAG → Agent → Multi-Agent → 生产级 AI 平台 → Capstone，内容是原创中文讲解，质量高、结构统一 |
| 章节模板 | `templates/chapter-template.mdx` 定义了统一结构：学习目标 → 零基础解释 → 术语 → 图解 → 代码/交互 → 误解 → 练习 → Speaking Drill |
| 2 个 Atlas 案例 | ChatGPT（317 行）、WhatsApp（274 行），结构非常好，可直接作为 100 案例的"黄金样板" |
| 组件使用约定 | MDX 里已经按约定引用了 13 个 React 组件（见下），props 写法统一 |

### 缺失（也就是要让 AI 去干的活）

| 缺口 | 现状 |
|---|---|
| **整个站点工程** | 目录 里 0 个 `package.json` / `docusaurus.config` / 源码文件——只有内容，没有壳 |
| **13 个组件的实现** | `ChapterMeta`、`GlossaryTerm`、`ResearchNote`、`GuidedExercise`、`TradeoffExplorer`、`PyRunner`（被引用 143 次！）、`CaseStudyHeader`、`DesignIntent`、`ArchitectureEvolution`、`PercentileLab`、`LatencyNumbers`、`FailureLab`、`CapacityEstimator` 全部只有 import，没有代码 |
| **图太少** | 172 篇里只有 18 个 mermaid 图。按"重图解"目标，每章至少 3~5 张，缺口约 600+ 张 |
| **交互与动画组件** | 需要新增：分步动画流程、可点击分层架构图、模拟器（一致性哈希环、缓存命中、令牌桶…）、新旧架构对比等 |
| **Atlas 案例** | 2 / 100，缺 98 个 |
| **页内可运行实验** | `PyRunner` 约定已存在 → 需要用 Pyodide 实现（浏览器内跑 Python，纯本地无需服务器） |

---

## 2. 技术底座决策（所有 prompt 的共同前提）

内容已经是 Docusaurus 风格的 MDX（`@site/src/components/`、`:::info` 提示块、frontmatter），所以**不要让 AI 另起炉灶换框架**——那会毁掉 172 篇现成内容。锁定：

- **Docusaurus 3 + React 18 + TypeScript**：MDX 原生支持、侧边栏/搜索/暗色模式开箱即用
- **@docusaurus/theme-mermaid**：所有流程图/时序图/状态图/思维导图用 Mermaid 写在 MDX 里（可维护、可 diff，远胜贴图片）
- **Pyodide**（本地 vendor 到 `static/pyodide/`）：实现 `PyRunner`，浏览器内直接运行 Python 实验，**完全离线可用**
- **交互动画**：用 React + SVG/CSS 手写（不引重型动画库），复杂模拟器用 `<SystemSimulator>` 系列组件
- **本地部署**：`npm run build` → 纯静态文件 → 任何静态服务器（`npx serve build`、Nginx、甚至 Windows 上双击的本地服务器）都能跑，不依赖外网
- **离线搜索**：`@easyops-cn/docusaurus-search-local`

这段决策会原样写进"项目宪法"，让每一次会话都不偏航。

---

## 3. 项目宪法：`Gemini.md`（放在仓库根目录，常驻生效）

> 用法：在仓库根目录创建 `Gemini.md`，把下面内容整个贴进去。Gemini 每次启动都会自动读取它，等于每个会话都自带项目规范，不用重复解释。

````markdown
# 项目宪法：AI 架构师交互式学习站

## 使命
把 `docs/` 下 172 篇中文 MDX 教材，建成本地部署的 Docusaurus 3 学习站：
重交互、重图解、每章有可运行实验或分步指引，并配套 100 个真实系统架构深度案例（atlas/）。

## 不可违反的铁律
1. **保护原文**：已有 MDX 的正文讲解一律"只增强、不重写、不删除"。你可以插入图、
   组件、实验、测验，但不许改写作者的原创文字，除非明确要求。
2. **来源纪律**：所有关于真实系统（WhatsApp、Spanner、vLLM…）的架构断言，必须
   基于公开资料（工程博客/论文/官方文档/会议演讲），并在文末 ResearchNote 或
   延伸阅读中给出来源。查不到来源的内容必须明确标注「推断：」前缀，禁止把猜测
   写成事实。
3. **最新架构优先**：案例正文以当前公开可知的最新架构为主线；历史架构只出现在
   「架构演进」章节里，并解释每次变迁的动因（规模？成本？故障教训？）。
4. **构建即验收**：每完成一个任务单元必须 `npm run build` 通过（0 error），
   Mermaid 语法错误、断链、MDX 编译错误都算未完成。
5. **一次一个任务**：严格按 `TODO.md` 清单逐项执行，完成一项 → 输出完成报告 →
   git commit → 停下等指令。禁止一次会话贪多。
6. **中文主讲、英文术语保留**：与现有教材一致；首次出现的关键术语用 GlossaryTerm 包裹。

## 技术栈（锁定，不得更换）
Docusaurus 3 + React 18 + TypeScript；@docusaurus/theme-mermaid；
Pyodide（vendor 到 static/pyodide，离线可用）；本地搜索插件；
`npm run build` 产出纯静态站点，目标是完全离线运行。

## 目录结构
- docs/            ← 13 个课程模块（00-start … 12-capstone）
- docs/atlas/      ← 100 个架构案例
- src/components/  ← 全部交互组件（TypeScript + CSS Modules）
- static/pyodide/  ← 离线 Python 运行时
- TODO.md          ← 任务清单（唯一进度事实源）
- PROMPTS/         ← 各阶段 prompt 模板存档

## 组件规范（props 必须与 docs/ 中已有用法完全兼容）
已被 MDX 引用、必须实现的 13 个：
ChapterMeta(time, prereqs[{label,href}], outcome, howToUse)
GlossaryTerm(term, definition, children) —— 悬停/点击弹出释义
ResearchNote(title, source, href, insight, application) —— 论文/资料卡片
GuidedExercise(title, goal, hints[], steps[], checks[]) —— 可勾选的分步练习
TradeoffExplorer(title, dimensions[], options[{name,scores[],note,whenToUse}])
  —— 交互式雷达/条形对比，点击选项高亮
PyRunner(code, rows, expect) —— Pyodide 页内运行 Python，带输出区和"运行"按钮
CaseStudyHeader(oneLiner, stats[{label,value}])
DesignIntent(problem, users, devices, goals[], constraints[], firstStep)
ArchitectureEvolution(stages[{era,title,description,drivers}]) —— 可点击时间线
PercentileLab / LatencyNumbers / FailureLab / CapacityEstimator —— 交互实验器

新增组件（增强交互/动画用）：
StepFlow(steps[{title,desc,diagram?}]) —— 上一步/下一步/自动播放的流程动画
ArchLayers(layers[{name,components[],detail}]) —— 可逐层点开的分层架构图
CompareSlider(before, after, labels) —— 新旧架构左右滑动对比
SystemSimulator(type, params) —— 内置模拟器：consistent-hash | token-bucket |
  cache-lru | raft-election | kv-cache | fanout | cap-partition
QuizCard(questions[{q,options[],answer,explain}]) —— 章末自测
MindMap(root, children tree) —— 可折叠交互思维导图（基于 Mermaid mindmap 或自绘 SVG）
EvolutionTimeline(events[{year,title,why,change}]) —— 架构变迁时间轴

## 每章质量门槛（增强后必须全部满足）
- Mermaid 图 ≥ 3（至少 1 张结构图 + 1 张流程/时序图）
- 交互组件 ≥ 1（TradeoffExplorer / SystemSimulator / StepFlow 任一）
- 可运行实验：能用 PyRunner 的必须页内可跑；不能的用 GuidedExercise
  把步骤拆到"复制粘贴即可执行"的粒度
- GlossaryTerm ≥ 5；ResearchNote ≥ 1；QuizCard ≥ 3 题；「常见误解」小节保留并充实

## Atlas 案例结构（100 个案例统一遵守，样板见 docs/atlas/chatgpt.mdx）
1. CaseStudyHeader（一句话本质 + 关键数字）
2. DesignIntent（问题/用户/设备/目标/约束/第一步）
3. 全景思维导图（Mermaid mindmap：整个系统一张图）
4. 最新架构总览（C4 风格：Context 图 + Container 图，Mermaid）
5. 核心机制拆解 2~4 个（每个配时序图或数据流图 + 讲清"为什么这样设计"）
6. 关键数据结构与算法（为什么选它：B+树/LSM/CRDT/一致性哈希/倒排…）
7. 架构演进史（EvolutionTimeline + CompareSlider：每次变迁的动因与代价）
8. 设计模式与课程映射（本案例用到了课程哪些概念，链接回对应章节）
9. TradeoffExplorer（本系统最核心的一组取舍）
10. 如果是你来设计（GuidedExercise：让学习者复现关键决策）
11. QuizCard + 来源清单（每条架构断言可追溯）
图表配额：Tier1 案例 ≥ 8 张图，Tier2 ≥ 6 张，Tier3 ≥ 4 张。

## 完成报告格式（每个任务结束时输出）
- 本次完成：文件列表 + 每个文件新增了什么
- 质量门槛自检表（逐项 ✅/❌）
- 来源清单（案例任务必填)
- 构建结果：npm run build 输出摘要
- 建议的下一个任务
````

---

## 4. 阶段一 Prompt：站点脚手架 + 组件库（1~2 个会话）

> 用法：新开 Gemini 会话，仓库里已放好 `Gemini.md` 和 `docs/`（把 目录 内容拷进去），贴以下 prompt。

````text
阅读 Gemini.md 后执行阶段一：搭建站点骨架并实现全部组件。

任务清单（按顺序，每完成一项 commit 一次）：

1. 初始化 Docusaurus 3 + TypeScript 项目（classic preset），把现有 13 个模块目录
   接入 docs/，用 sidebars.ts 生成分组侧边栏：侧边栏顺序 = 00-start → 12-capstone
   → atlas → projects。中文站点标题「从零到 AI Architect」。
2. 接入 @docusaurus/theme-mermaid，确认 docs 里已有的 18 个 mermaid 块全部渲染。
3. 实现 Gemini.md「组件规范」中列出的全部组件（13 个已引用 + 7 个新增），
   要求：
   - TypeScript + CSS Modules，浅色/深色主题都好看；
   - props 必须兼容 docs/ 中已有的真实用法（先 grep 现有 MDX 里的调用再写接口）；
   - PyRunner 用 Pyodide：首次点击"运行"时懒加载 /static/pyodide/，
     显示加载进度；支持 print 输出、异常展示、代码可编辑、"重置"按钮；
   - 每个组件写一个最小 demo 页 /docs/99-component-gallery/ 方便人工验收；
   - SystemSimulator 先实现 token-bucket、consistent-hash、cache-lru 三种，
     其余类型留接口注册机制，后续增量添加。
4. 下载并 vendor Pyodide 到 static/pyodide/（锁定版本），断网状态下 PyRunner
   必须可用。
5. 接入离线本地搜索插件。
6. 写 README.md：一条命令本地开发（npm start）、一条命令构建（npm run build）、
   一条命令离线部署（npx serve build），面向完全不懂前端的使用者。
7. npm run build 全绿后，生成 TODO.md：
   - 阶段二：13 个模块的章节富化任务（每模块一项）
   - 阶段三：100 个案例任务（从 PROMPTS/atlas-manifest.md 读取清单）
   - 阶段四：QA 任务
逐项执行，遵守宪法第 5 条：做完第 1 项先停下来给我看。
````

**验收要点（人工花 10 分钟检查）**：`npm start` 打开后随便点 3 个章节——组件是否渲染、PyRunner 断网能不能跑、暗色模式是否正常。不过关就把截图/报错贴回去让它修，别急着进阶段二。

---

## 5. 阶段二 Prompt 模板：章节富化（13 个模块 × 各 1 个会话）

> 用法：每个模块新开一个会话，替换 `{{...}}` 占位符。**一个会话只做一个模块**，这是质量的生命线。

````text
阅读 Gemini.md。执行阶段二富化任务：模块 {{03-data-cache-queue}}。

流程（对模块内每一个 .mdx 依次执行，一次一篇）：

1. 通读该篇，列出它包含的知识点清单（输出给我，作为增强依据）。
2. 按「每章质量门槛」做增量增强，铁律：不改写、不删除原有正文，只插入：
   a. 图：每个核心概念至少 1 张 Mermaid 图。选型规则——
      结构/组成 → flowchart TB；调用/交互 → sequenceDiagram；
      状态变化 → stateDiagram-v2；数据流 → flowchart LR 带标注箭头；
      知识全景 → mindmap。图必须画"这一章的具体内容"，禁止通用装饰图。
   b. 交互：为最核心的机制配 1 个交互组件。有对应 SystemSimulator 类型就用它
      （如限流章 → token-bucket）；没有就用 StepFlow 把机制拆成 4~7 步动画；
      涉及方案选型的用 TradeoffExplorer。
   c. 实验：已有 PyRunner 的检查代码可运行、expect 描述准确；
      没有实验的章节，若知识点可以用 ≤60 行纯 Python（无第三方依赖，
      Pyodide 限制）演示，就新增 PyRunner 实验；
      不可页内运行的（如 Docker/K8s 实操），改用 GuidedExercise：
      每一步 = 一条可直接复制的命令 + 预期输出 + 出错时最常见的 2 个原因。
   d. 章末新增 QuizCard ≥ 3 题（至少 1 题考"为什么"而不是"是什么"）。
3. 每完成一篇：跑 npm run build，贴质量门槛自检表，commit（消息格式：
   enrich(m3): cache-patterns +4 diagrams +simulator +quiz）。
4. 整个模块完成后输出模块级报告：新增图/组件/实验/测验总数，
   以及你认为本模块仍然薄弱、值得我后续人工补强的 2 个点。

从 overview.mdx 开始。
````

---

## 6. 阶段三：Atlas 案例工厂（核心重头戏）

### 6.1 先把 100 案例清单放进仓库：`PROMPTS/atlas-manifest.md`

> ★★★ = Tier1 深度旗舰（≥600 行、≥8 图）；★★ = Tier2 标准（≥350 行、≥6 图）；★ = Tier3 精讲（≥200 行、≥4 图）。清单可按兴趣增删，但每类保底 1~2 个。

````markdown
# Atlas 100 案例清单（✅=已完成）

## A. AI 助手与 LLM 产品（7）
| # | 案例 | Tier | 核心看点 |
|---|---|---|---|
| A1 | ChatGPT ✅ | ★★★ | 模型架构 vs 服务架构双层、KV cache、连续批处理 |
| A2 | Claude / Gemini | ★★★ | 长上下文工程、Artifacts、agentic 编码环境的沙箱与工具协议 |
| A3 | Gemini | ★★ | 原生多模态、与 Google 生态（Search/Workspace）的集成架构 |
| A4 | GitHub Copilot | ★★★ | 编辑器内毫秒级补全：上下文收集、FIM、请求取消与缓存 |
| A5 | Perplexity | ★★ | 检索增强问答产品化：搜索编排 + 引用生成 |
| A6 | Cursor | ★★ | 代码库索引（嵌入+AST）、影子工作区、apply 模型 |
| A7 | Midjourney | ★ | 扩散模型推理服务与 Discord 作为前端的取舍 |

## B. 搜索与推荐（6）
| B1 | Google Search | ★★★ | 爬取-索引-服务三平面、倒排索引、排序信号演进（PageRank→学习排序→RankBrain/BERT） |
| B2 | Bing + Copilot | ★★ | 传统搜索接入 LLM 的编排层（Prometheus 架构） |
| B3 | Elasticsearch | ★★★ | Lucene 段结构、倒排+列存、分片与副本、近实时刷新 |
| B4 | Pinterest | ★★ | 视觉发现引擎：PinSage 图神经推荐、home feed 混排 |
| B5 | TikTok/抖音推荐 | ★★★ | Monolith 实时训练、特征哈希、兴趣探索 vs 利用 |
| B6 | YouTube 推荐 | ★★ | 两阶段召回+排序、观看时长目标演进 |

## C. 通讯与社交（8）
| C1 | WhatsApp ✅ | ★★★ | Erlang 百万连接、端到端加密、极简后端哲学 |
| C2 | X.com (Twitter) | ★★★ | 时间线 fanout 读写权衡、从 Ruby 单体到 JVM 微服务再到精简架构 |
| C3 | 微信 WeChat | ★★★ | 万亿消息、小程序容器架构、红包高并发 |
| C4 | Discord | ★★ | Elixir 网关、按 guild 分片、消息存储从 Mongo→Cassandra→ScyllaDB |
| C5 | Slack | ★★ | 工作区分片、实时消息总线、企业级权限模型 |
| C6 | Telegram | ★ | MTProto、多数据中心用户就近 |
| C7 | Instagram | ★★ | Django 单体的极限、feed 排序、Stories 的读扩散 |
| C8 | Zoom | ★★ | SFU 媒体路由、级联集群、弱网对抗 |

## D. 办公与协作（7）
| D1 | Microsoft 365 + Office Copilot | ★★★ | 文档格式演进（二进制→OOXML）、Graph 数据层、Copilot 的编排与权限继承 |
| D2 | Excel 计算引擎 | ★★★ | 依赖图重算、稀疏表存储、多线程重算演进 |
| D3 | Google Docs | ★★★ | OT 协同算法、为何不用 CRDT、离线合并 |
| D4 | Notion | ★★ | 万物皆 block 的数据模型、权限树、离线同步 |
| D5 | Figma | ★★★ | 浏览器里的 C++（WASM 渲染引擎）、多人协同 CRDT、multiplayer 服务器 |
| D6 | 飞书 Feishu | ★★ | IM+文档+审批一体化平台的组织架构数据模型 |
| D7 | Jira + Confluence | ★★ | 工作流状态机引擎、插件架构（如何让第三方安全扩展） |

## E. 操作系统谱系（10）
| E1 | Linux 内核（服务器） | ★★★ | 宏内核、调度器演进（O(1)→CFS→EEVDF）、VFS、epoll |
| E2 | Windows NT（桌面） | ★★ | 混合内核、HAL、Win32 子系统与 WSL |
| E3 | macOS / Darwin | ★★ | XNU=Mach+BSD 混合、沙箱与签名链 |
| E4 | Android | ★★★ | ART 运行时、Binder IPC、进程生命周期与 LMK |
| E5 | iOS | ★★ | 安全启动链、沙箱模型、Metal 图形栈 |
| E6 | FreeRTOS（嵌入式 MCU） | ★★ | 抢占式微型调度器、内存受限设计（几 KB RAM） |
| E7 | QNX（车载实时） | ★★ | 微内核消息传递、确定性延迟、故障隔离 |
| E8 | VxWorks（航天/特殊） | ★ | 硬实时、火星车上的优先级反转事故（经典案例） |
| E9 | ROS 2（机器人） | ★★★ | DDS 发布订阅、实时性改造、Nav2 行为树 |
| E10 | Fuchsia / Zircon | ★ | 能力安全微内核、组件化用户态——OS 的下一代实验 |

## F. 云平台与基础设施（10）
| F1 | AWS S3 | ★★★ | 11 个 9 的对象存储：分区、纠删码、强一致性改造（2020） |
| F2 | DynamoDB | ★★★ | 从 Dynamo 论文到全托管：一致性哈希→分区自动管理、自适应容量 |
| F3 | AWS Lambda | ★★ | Firecracker microVM、冷启动优化、事件驱动计费 |
| F4 | EC2 Nitro | ★★ | 虚拟化卸载到专用硬件的架构革命 |
| F5 | Azure Cosmos DB | ★★ | 五种一致性级别、多主全球分布 |
| F6 | Google Spanner | ★★★ | TrueTime、外部一致性、全球分布式 SQL |
| F7 | Borg → Kubernetes | ★★★ | 声明式调和循环、控制器模式、etcd/Raft |
| F8 | Cloudflare Workers/Edge | ★★ | V8 isolate 多租户、全球任播、无区域架构 |
| F9 | Snowflake | ★★ | 存算分离、虚拟仓库、多集群共享数据 |
| F10 | Vercel | ★ | 前端云：构建产物不可变、边缘函数与 ISR |

## G. 数据与流处理（10）
| G1 | PostgreSQL | ★★★ | MVCC、WAL、B+树与 vacuum、扩展生态（pgvector） |
| G2 | Redis | ★★★ | 单线程事件循环为何快、数据结构编码、持久化与集群演进 |
| G3 | Kafka | ★★★ | 顺序写日志、零拷贝、ISR 复制、KRaft 去 ZooKeeper |
| G4 | ClickHouse | ★★ | 列存+向量化执行、MergeTree、为什么分析快 1000 倍 |
| G5 | Cassandra | ★★ | 无主复制、LSM、可调一致性 |
| G6 | MongoDB | ★ | 文档模型、从 MMAPv1 到 WiredTiger、分片演进 |
| G7 | SQLite | ★★ | 嵌入式单文件、世界部署量最大数据库的极简架构 |
| G8 | RocksDB | ★★ | LSM 树深度：memtable/SST/compaction 策略 |
| G9 | Flink | ★★ | 有状态流计算、checkpoint 对齐、exactly-once |
| G10 | Iceberg 数据湖 | ★★ | 表格式元数据层、快照隔离、湖仓一体 |

## H. 开发者工具链（8）
| H1 | Git | ★★★ | 内容寻址对象库、DAG、为什么分支几乎零成本 |
| H2 | GitHub | ★★ | 单体 Rails 的规模化、Spokes 三副本存储、Actions 调度 |
| H3 | GitLab CI | ★ | Runner 架构、流水线 DAG 调度 |
| H4 | VS Code | ★★★ | Electron 多进程、扩展宿主隔离、LSP 协议改变行业 |
| H5 | Docker | ★★★ | namespace+cgroup+联合文件系统、镜像分层与 OCI |
| H6 | Bazel | ★ | 远程缓存+沙箱的可复现构建、Google 单仓库工程学 |
| H7 | npm registry | ★ | 全球最大包仓库：CDN 化、依赖解析的演进 |
| H8 | Sentry | ★ | 错误聚合指纹、事件洪峰削峰 |

## I. 流媒体与内容（5）
| I1 | Netflix | ★★★ | 微服务先驱：Zuul/Eureka/Hystrix 谱系、Open Connect 自建 CDN、混沌工程 |
| I2 | Spotify | ★★ | 音频分发、Discover Weekly 推荐管线、squad 组织与架构关系 |
| I3 | YouTube 视频管线 | ★★ | 上传→转码→多码率分发、Vitess 分库 MySQL |
| I4 | Twitch | ★★ | 直播摄取、转码集群、聊天系统百万房间 |
| I5 | TikTok 视频管线 | ★ | 短视频冷启动分发、边缘缓存策略 |

## J. 电商、支付与出行（8）
| J1 | Amazon 电商 | ★★★ | 从单体到 SOA 的祖师爷、购物车高可用（Dynamo 起源） |
| J2 | Shopify | ★★ | 模块化单体的胜利、Pod 租户隔离、闪购洪峰 |
| J3 | Stripe | ★★★ | 支付状态机、幂等键设计、API 版本化哲学 |
| J4 | 支付宝双 11 | ★★ | 单元化 LDC 架构、OceanBase、洪峰限流 |
| J5 | Uber | ★★★ | H3 地理索引、派单撮合、从 Postgres 到 Schemaless 再到 Docstore |
| J6 | Airbnb | ★ | 搜索排序、服务化迁移的教训 |
| J7 | 美团/DoorDash | ★★ | 履约调度：预估送达时间、骑手路径规划 |
| J8 | 12306 | ★★ | 春运抢票：余票查询与出票分离、排队削峰 |

## K. AI 训练与推理基建（8）
| K1 | vLLM | ★★★ | PagedAttention（OS 虚拟内存思想进推理）、连续批处理 |
| K2 | Megatron-LM | ★★ | 3D 并行（数据/张量/流水线）、万卡训练的通信拓扑 |
| K3 | Ray | ★★ | 分布式 actor/task、对象存储 plasma、RLHF 基座 |
| K4 | Triton Inference Server | ★ | 多框架统一推理、动态批处理、模型集成 |
| K5 | Milvus 向量数据库 | ★★ | 存算分离的向量检索、HNSW/IVF 索引选型 |
| K6 | MCP 协议生态 | ★★★ | 模型-工具解耦的 USB 时刻：host/client/server、能力协商 |
| K7 | LangGraph / Agent 框架 | ★★ | 图状态机编排、checkpoint、human-in-the-loop |
| K8 | GPU 集群调度 | ★★ | Slurm vs K8s、gang scheduling、拓扑感知与碎片治理 |

## L. 游戏与实时系统（4）
| L1 | MOBA 同步（王者荣耀） | ★★ | 帧同步 vs 状态同步、确定性锁步、断线重连 |
| L2 | Minecraft 服务器 | ★ | 区块加载、tick 循环、单线程瓶颈与社区优化 |
| L3 | Roblox | ★★ | UGC 平台：脚本沙箱、物理分布式模拟 |
| L4 | 游戏引擎（Unreal） | ★ | ECS vs Actor、渲染管线、资产流送 |

## M. 安全与身份（4）
| M1 | Signal 协议 | ★★★ | 双棘轮、前向保密——被 WhatsApp/Messenger 采纳的加密架构 |
| M2 | OAuth2 / OIDC 生态 | ★★ | 授权码流程、token 设计、为什么密码永不出域 |
| M3 | Let's Encrypt | ★ | ACME 自动化 PKI，把 HTTPS 变成默认值的架构 |
| M4 | 1Password | ★ | 零知识架构：两把钥匙派生、同步而不泄密 |

## N. 网络与去中心化（5）
| N1 | DNS 全球体系 | ★★ | 层级委托、任播根服务器、缓存 TTL 的博弈 |
| N2 | CDN（Akamai 原理） | ★★ | 边缘缓存、回源策略、动态加速 |
| N3 | BitTorrent | ★★ | 分块交换、tit-for-tat 激励、DHT 去中心化索引 |
| N4 | Bitcoin | ★★ | UTXO、工作量证明、最长链共识的取舍 |
| N5 | NTP 时间同步 | ★ | 层级时钟源、时钟偏移估计——分布式系统的隐形地基 |
````

### 6.2 案例工厂 Prompt 模板（每次 1~2 个案例，可无限复用）

````text
阅读 Gemini.md 与 PROMPTS/atlas-manifest.md。执行阶段三案例任务：{{C2 X.com}}。

第 0 步（先做，单独输出，等我确认后再写正文）：
- 用 web 搜索收集本案例的一手资料：官方工程博客、架构演讲、论文、
  权威技术分析。列出 6~12 条来源清单（标题+链接+它能支撑正文哪一节）。
- 明确声明哪些部分公开资料充分、哪些只能合理推断。推断内容在正文中
  一律加「推断：」标注。

第 1 步：按 Gemini.md「Atlas 案例结构」11 节完整撰写
docs/atlas/{{x-com}}.mdx，硬性要求：
- 以【最新公开架构】为主线；历史架构全部放进「架构演进」节，
  每次变迁必须回答三问：当时遇到什么瓶颈？为什么这样改？付出了什么代价？
- 数据结构小节必须讲到"为什么是它"：给出 1~2 个被否决的替代方案及否决理由。
- 图表配额（Tier {{★★★ → ≥8 张}}）且类型覆盖：
  mindmap 全景 ×1、C4 Context ×1、C4 Container ×1、核心机制时序图 ≥2、
  数据流图 ×1、演进对比（CompareSlider 或双图）×1、状态图或部署图 ×1。
  每张图下面必须有 2~4 句"读图指引"。
- 交互配额：TradeoffExplorer ×1、EvolutionTimeline ×1、
  GuidedExercise（"如果是你来设计"）×1、QuizCard ≥4 题。
- 与课程联动：至少回链 4 个课程章节（如 fanout → 03 模块 feed-fanout）。
- 风格对齐 docs/atlas/chatgpt.mdx：先建立直觉再上术语，多用类比。

第 2 步：npm run build 通过后，输出完成报告（含来源清单复核表：
正文每个架构断言 → 对应来源编号），commit，
更新 atlas-manifest.md 打 ✅，然后停下。
````

**节奏建议**：每个会话跑 1 个 Tier1 或 2 个 Tier2/Tier3。100 个案例 ≈ 55~70 个会话。**这是马拉松**，合理预期是每天跑 2~4 个会话、6~10 周完成；想快就先跑完 20 个 Tier1 + 各类目 1 个代表，站点已经非常可用，剩下的细水长流。

---

## 7. 阶段四 Prompt：全站 QA 与一致性（2~3 个会话）

````text
阅读 Gemini.md。执行阶段四全站 QA，逐项输出问题清单并修复：

1. 构建与链接：npm run build 零警告；写脚本扫描全站内链，输出并修复所有断链
   （尤其 atlas 回链课程章节的相对路径）。
2. 质量门槛审计：写脚本统计每篇 MDX 的 mermaid 数 / 组件数 / QuizCard 数，
   输出不达标清单（对照 Gemini.md 门槛），逐篇补齐。
3. 术语一致性：抽取全站 GlossaryTerm，找出同一术语不同定义的冲突，统一为
   最准确版本，并生成 docs/glossary.mdx 汇总页（按字母序，回链出处）。
4. 来源审计：扫描 atlas 中没有 ResearchNote/来源支撑的绝对化断言
   （"一定""必然""就是"），要么补来源，要么改为「推断：」。
5. 离线验收：断网环境下 npx serve build，人工路径：首页 → 任一章节 →
   跑一个 PyRunner 实验 → 打开一个 Tier1 案例 → 搜索一个术语。
   把这条验收路径写进 README。
6. 生成 docs/atlas/overview.mdx 案例总目录：按 14 类分组的卡片墙 +
   一张全景 mindmap（100 案例 → 14 类 → 课程模块映射）。
````

---

## 8. 常用纠偏小 Prompt（贴着用）

| 场景 | 直接贴这句 |
|---|---|
| 图太抽象 | 「这张图是通用装饰图。重画：图里必须出现本章的具体组件名/数据名/步骤名，让读者不看正文也能复述机制。」 |
| 开始编造 | 「暂停。X 这一段没有来源。给出公开来源链接，找不到就改写为『推断：』并弱化措辞。」 |
| 擅自改写原文 | 「违反宪法第 1 条。git diff 找出被改写的原文段落，全部恢复，只保留新插入的内容。」 |
| 内容变水 | 「这一节低于 chatgpt.mdx 样板的信息密度。对照样板第 N 节的写法重写：每个断言要么有数字、要么有机制、要么有来源。」 |
| 交互组件敷衍 | 「这个组件只是静态展示。加入用户可操作的变量（滑块/按钮/输入），操作后结果要实时变化并解释变化原因。」 |
| 会话贪多质量掉 | 「停止当前批量操作。回到 TODO.md，只完成当前一项，输出完成报告后结束会话。」 |
| 想快速起量 | 「本会话只做 Tier3 案例 {{X}}、{{Y}}，严格 ≥200 行 ≥4 图，不许为省事降为清单式罗列。」 |

---

## 9. 执行路线图（现实预期）

| 阶段 | 会话数 | 日历时间（业余节奏） | 里程碑 |
|---|---|---|---|
| 一：脚手架+组件 | 1~2 | 第 1 周 | 站点能跑、20 个组件全渲染、PyRunner 离线可用 |
| 二：13 模块富化 | 13 | 第 2~4 周 | 每章 ≥3 图 ≥1 交互 ≥1 实验 ≥3 测验 |
| 三A：Tier1 × 20 案例 | ~20 | 第 4~7 周 | 旗舰案例上线，站点已可对外展示 |
| 三B：Tier2/3 × 78 案例 | ~40 | 第 7~12 周 | 100 案例满员 |
| 四：QA + 总目录 | 2~3 | 第 12~13 周 | 断网验收通过、术语表、案例全景图 |

三条最重要的经验，最后再强调一次：

1. **宪法常驻 + 清单驱动 + 小步提交**，是让 AI 在百次会话里不走样的唯一办法。
2. **来源纪律**决定这套教材是"可信的架构教科书"还是"看起来很像的幻觉合集"。
3. 先做 **20 个 Tier1 + 全类目覆盖**，你就已经拥有一个了不起的作品；剩下 80 个是复利，不是门槛。
