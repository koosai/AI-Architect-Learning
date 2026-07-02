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
