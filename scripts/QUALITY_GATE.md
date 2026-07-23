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
| **P1** | `EXPECT-SOUND` | `<PyRunner>` 的 `expect` 串必须出现在其 `code` 输出里，否则校验绿灯永远点不亮。 |
| **P1** | `CITE-HOLLOW`（全占位） | 某文件"来源"全是域名首页、无一条具体文章链接 = 伪造引用。 |
| **P2** | `CITE-HOLLOW`（含占位） | 文件含个别域名首页占位引用（白名单放行 DDIA/raft 等权威单页站）。 |
| **P2** | `STRUCT` | 正式章节图 ≥3 / 交互 ≥1 / 测验 ≥3（元信息页豁免）。 |

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

## 当前基线（2026-07-23）

```
P0 = 1   （labs/ 目录整体缺失，298 条引用悬空，波及 155 个章节 / 12 个模块）
P1 = 37  （52 处 expect 复制粘贴聚合为 1 条 EXPECT-DUP + 多条 EXPECT-SOUND + 多条全占位来源）
P2 = 56  （含占位引用 / 结构提示）
```

这份基线就是"补硬伤"工作的验收标尺：每修复一批，重跑门禁看计数下降，归零即可切严格模式。
