# 内容质量门禁 (Content Quality Gate)

`scripts/quality-gate.mjs` —— 一个**可在任意机器 / CI 上运行**的内容质量门禁，纯 Node.js 标准库实现，无需 `npm install`。

它取代旧的 `scripts/audit_quality_gates.py`（后者硬编码了 `c:\Users\K.K\...` 绝对路径、输出到本地 IDE 私有目录，无法在 CI 或他人机器运行，且只校验"形式"）。

## 为什么要它

旧门禁只数结构（图 ≥3 / 交互 ≥1 / 测验 ≥3），于是**它度量的东西都做得很好，它不度量的东西全部塌方**：
labs 不存在、`expect` 校验被复制粘贴、来源用域名首页占位——这些都不影响 `npm run build` 通过，却直接毁掉学习体验与可信度。
新门禁在保留结构检查之外，**校验"实质"**。

## 检查项与分级

| 级别 | 规则 | 含义 |
|---|---|---|
| **P0** | `LAB-REF` | 教材中引用的 `labs/...` 实验路径必须真实存在。缺失 = 学员一上手即 `No such file or directory`。 |
| **P1** | `EXPECT-DUP` | 同一 `expect` 校验串被 ≥3 个不相干文件复制粘贴 = 招牌"运行即验证"形同虚设。 |
| **P1** | `QUIZ` | QuizCard 数字 `answer` 须落在选项区间、选项 ≥2（防"字母答案判错"类静默 bug）。 |
| **P1** | `TRADEOFF` | TradeoffExplorer `scores` 长度须 == `dimensions` 长度、分值统一 0–5 刻度。 |
| **P1** | `GLOSSARY` | `<GlossaryTerm>` 须有 `definition`。 |
| **P1** | `CITE-HOLLOW`（Atlas） | Atlas 案例来源含域名首页占位/编造引用即失败（可信度硬门禁）。 |
| **P1** | `CITE-THIN`（Atlas） | Atlas 案例须有 ≥2 条具体一手来源。 |
| **P2** | `EXPECT-SOUND` | `expect` 串非 code 字面量（运行时 f-string 拼接会误报，故仅提示）。 |
| **P2** | `CITE-HOLLOW`（非 Atlas） | 非 Atlas 文档含个别域名首页占位引用（白名单放行权威官方站/规范）。 |
| **P2** | `RESEARCHNOTE` / `STRUCT` | ResearchNote 须有 href；正式章节图 ≥3 / 交互 ≥1 / 测验 ≥3。 |

> 引用检查只对"含正式『来源』小节的文档"（即 Atlas 案例）生效——课程章节用内联上下文链接、正文里的示例 URL（example.com 等）不会被误判为引用。

阈值与白名单集中在脚本顶部 `THRESHOLDS` / `CANONICAL_HOMEPAGES` / `JUNK_HOSTS`，可按需调整。

## 用法

```bash
npm run quality-gate          # 严格模式：有 P0/P1 违规 → 退出码 1（卡住 CI）
npm run quality-gate:report   # 只报告，不影响退出码（存量治理期用）
node scripts/quality-gate.mjs --json          # 追加机器可读 JSON（始终为最后输出）
```

## CI 接入

`.github/workflows/quality-gate.yml` 在改动 `docs/**`、`labs/**` 或门禁自身时触发。

**治理期策略**：当前内容仍有存量 P0/P1 违规（labs 整体缺失、52 处 expect、占位引用），
CI 暂用 `--report-only` 保证"可见但不红"，并把报告作为 artifact 上传。

**存量清零后**：把 workflow 里那一步改为 `npm run quality-gate`（去掉 `--report-only`），
门禁即转为硬卡——任何新引入的上述缺陷都会让 PR 变红。

## 基线与治理进度

| 时点 | P0 | P1 | P2 | 说明 |
|---|---|---|---|---|
| 初始 (建门禁时) | 1 | 37 | 56 | labs 全缺；52 处 expect 复制粘贴；多处全占位来源 |
| 补硬伤第一批 | 1 | **0** | 56 | 52 处 expect 全部修到与真实输出一致（EXPECT-DUP 清零）；9 处"全占位来源"P1 清零 |
| labs 全量补齐 | **0** | **0** | 56 | 12 个月 + Atlas 引用共 298 条路径全部落地，154 个 test 均 `python3` 跑通 |

**当前 P0 = P1 = 0。** 剩余仅 P2=56 提示级（EXPECT-SOUND 运行时拼接的静态误报 + 边缘首页引用）。
P2=56 主要为 `EXPECT-SOUND` 静态提示（expect 由运行时 f-string 拼接，非硬伤）与边缘首页引用，属"人工/执行核对"级。

> 门禁说明：`EXPECT-SOUND` 是静态检查，看不到运行时输出，对 f-string/多参数 print 会误报，故列 P2 不作硬门禁；可靠的复制粘贴信号由 `EXPECT-DUP`(P1) 兜底。
