#!/usr/bin/env node
// @ts-check
/**
 * 内容质量门禁 (Content Quality Gate)
 * =====================================
 * 一个可在任意机器 / CI 上运行的质量门禁。相较旧的 audit_quality_gates.py：
 *   1. 无任何硬编码绝对路径（路径全部相对仓库根目录解析）。
 *   2. 不止校验"形式"（图/交互/测验的数量），更校验"实质"：
 *        - LAB-REF      : 教材里引用的 labs/ 实验路径必须真实存在（否则学员一上手就 404）。
 *        - EXPECT-DUP   : PyRunner 的 expect 校验串在多个不相干文件间被复制粘贴（招牌校验形同虚设）。
 *        - EXPECT-SOUND : PyRunner 的 expect 串必须出现在其 code 输出里，否则绿灯永远点不亮 / 语义错乱。
 *        - CITE-HOLLOW  : "来源"里只指向域名首页的占位式引用（违背"真实来源纪律"）。
 *   3. 明确的分级 (P0/P1/P2) 与退出码，可直接卡住 CI。
 *
 * 用法：
 *   node scripts/quality-gate.mjs                # 跑全部门禁，有 P0/P1 违规则退出码=1
 *   node scripts/quality-gate.mjs --report-only  # 只报告，不影响退出码（增量治理期用）
 *   node scripts/quality-gate.mjs --json         # 额外输出机器可读 JSON 到 stdout 末尾
 */

import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const REPO_ROOT = path.resolve(__dirname, '..');
const DOCS_DIR = path.join(REPO_ROOT, 'docs');

// ---- 可调阈值 ---------------------------------------------------------------
const THRESHOLDS = {
  minMermaid: 3, // 每个正式章节至少 3 张图
  minInteractive: 1, // 至少 1 个交互组件
  minQuizQuestions: 3, // 至少 3 道测验题
  expectDupFiles: 3, // 同一 expect 串出现在 >= 3 个文件即判定为复制粘贴占位
};

const INTERACTIVE_COMPONENTS = [
  'TradeoffExplorer', 'SystemSimulator', 'StepFlow', 'PercentileLab',
  'LatencyNumbers', 'FailureLab', 'CapacityEstimator', 'CompareSlider',
  'ArchLayers', 'MindMap', 'ArchitectureEvolution', 'EvolutionTimeline',
  'CacheSimulator',
];

// 元信息页 / 目录页不参与"结构"硬门禁
const META_PAGE_MARKERS = [
  'overview.md', 'overview.mdx', 'index.md', 'index.mdx', 'glossary.mdx',
  'component-gallery', '00-start', 'projects', 'capstone-brief',
];

// ---- 小工具 -----------------------------------------------------------------
const args = new Set(process.argv.slice(2));
const REPORT_ONLY = args.has('--report-only');
const EMIT_JSON = args.has('--json');
const rel = (p) => path.relative(REPO_ROOT, p).split(path.sep).join('/');

/** 递归收集 docs 下的 .md / .mdx */
function collectDocs(dir) {
  /** @type {string[]} */
  const out = [];
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    if (entry.name === 'node_modules' || entry.name === 'build') continue;
    const full = path.join(dir, entry.name);
    if (entry.isDirectory()) out.push(...collectDocs(full));
    else if (/\.mdx?$/.test(entry.name)) out.push(full);
  }
  return out;
}

const isMeta = (relPath) => META_PAGE_MARKERS.some((m) => relPath.includes(m));

/** 定位子串首次出现的行号（1-based），找不到返回 0 */
function lineOf(content, needle) {
  const idx = content.indexOf(needle);
  if (idx < 0) return 0;
  return content.slice(0, idx).split('\n').length;
}

/** 提取每个 <PyRunner ...> 块（含 expect 与 code） */
function extractPyRunners(content) {
  /** @type {{expect: string|null, code: string, line: number}[]} */
  const blocks = [];
  const parts = content.split('<PyRunner');
  for (let i = 1; i < parts.length; i++) {
    const chunk = parts[i];
    const expectM = chunk.match(/expect="([^"]*)"/);
    const codeM = chunk.match(/code=\{`([\s\S]*?)`\}/);
    blocks.push({
      expect: expectM ? expectM[1] : null,
      code: codeM ? codeM[1] : '',
      line: lineOf(content, '<PyRunner' + chunk.slice(0, 20)),
    });
  }
  return blocks;
}

/** 从"来源/参考/References"小节里抽取 URL；若无该小节则退回全文 */
function extractSourceUrls(content) {
  const headingRe = /^#{1,4}\s*(来源|参考|参考文献|参考资料|References|Sources|来源清单)\b/im;
  const m = content.match(headingRe);
  const scope = m ? content.slice(content.indexOf(m[0])) : content;
  const urls = (scope.match(/https?:\/\/[^\s)\]"'>]+/g) || []).map((u) => u.replace(/[.,);]+$/, ''));
  return urls;
}

// 合法的"权威单页/单主题"引用：其主页本身即是该引用（书、协议规范、单一理念站），不算占位。
const CANONICAL_HOMEPAGES = new Set([
  'dataintensive.net', 'raft.github.io', 'jepsen.io', '12factor.net', 'dora.dev',
  'principlesofchaos.org', 'use-the-index-luke.com', 'hyrumslaw.com', 'highscalability.com',
  'rocksdb.org', 'flink.apache.org', 'volcano.sh', 'slurm.schedmd.com',
  // 权威规范/单主题官方站——主页本身即是该引用
  'c4model.com', 'modelcontextprotocol.io', 'finops.org', 'www.finops.org',
  'adr.github.io', 'opencontainers.org', 'gdpr.eu', 'artificialintelligenceact.eu',
  'enterpriseintegrationpatterns.com', 'www.enterpriseintegrationpatterns.com',
  'continuousdelivery.com', 'luau-lang.org',
]);
// 明显的占位/示例域名：永远算占位，无论是否只有域名
const JUNK_HOSTS = new Set(['example.com', 'www.example.com', 'google.com', 'www.google.com']);

function isHollowUrl(u) {
  const m = u.match(/^https?:\/\/([^/]+)(\/?.*)$/);
  if (!m) return false;
  const host = m[1].toLowerCase();
  const pathPart = m[2].replace(/\/$/, '');
  if (JUNK_HOSTS.has(host)) return true; // 示例域名，含路径也算占位
  if (pathPart !== '') return false; // 有具体路径 → 视为具体链接
  return !CANONICAL_HOMEPAGES.has(host); // 纯域名首页：白名单放行，其余判占位
}

// ---- 执行门禁 ---------------------------------------------------------------
const files = collectDocs(DOCS_DIR).sort();

/** @type {{p0: string[], p1: string[], p2: string[]}} */
const findings = { p0: [], p1: [], p2: [] };

// expect 串 -> 使用它的文件集合（用于 EXPECT-DUP）
/** @type {Map<string, Set<string>>} */
const expectUsage = new Map();
// labs 引用路径 -> 引用它的文件集合（用于 LAB-REF）
/** @type {Map<string, Set<string>>} */
const labRefs = new Map();

const perFile = [];

for (const file of files) {
  const relPath = rel(file);
  const content = fs.readFileSync(file, 'utf8');
  const meta = isMeta(relPath);

  // ---- 结构统计 (P2) ----
  const mermaid = (content.match(/```mermaid/gi) || []).length;
  let interactive = 0;
  for (const c of INTERACTIVE_COMPONENTS) {
    interactive += (content.match(new RegExp(`<${c}\\b`, 'g')) || []).length;
  }
  const quizQuestions = (content.match(/\bq\s*:\s*['"`]/g) || []).length;

  if (!meta) {
    const defs = [];
    if (mermaid < THRESHOLDS.minMermaid) defs.push(`Mermaid ${mermaid}/${THRESHOLDS.minMermaid}`);
    if (interactive < THRESHOLDS.minInteractive) defs.push(`交互 ${interactive}/${THRESHOLDS.minInteractive}`);
    if (quizQuestions < THRESHOLDS.minQuizQuestions) defs.push(`测验 ${quizQuestions}/${THRESHOLDS.minQuizQuestions}`);
    if (defs.length) findings.p2.push(`[STRUCT] ${relPath} — 结构不达标: ${defs.join(', ')}`);
  }

  // ---- labs 引用收集 (P0) ----
  for (const m of content.matchAll(/labs\/[A-Za-z0-9_./-]+/g)) {
    const p = m[0].replace(/[.,)]+$/, '');
    if (!labRefs.has(p)) labRefs.set(p, new Set());
    labRefs.get(p).add(relPath);
  }

  // ---- PyRunner 校验 (P1) ----
  const runners = extractPyRunners(content);
  for (const r of runners) {
    if (!r.expect) continue;
    if (!expectUsage.has(r.expect)) expectUsage.set(r.expect, new Set());
    expectUsage.get(r.expect).add(relPath);
    // EXPECT-SOUND: expect 串未作为字面量出现在 code 源码里。
    // 注意：这是静态检查，看不到运行时输出——若 expect 由 f-string/print 多参数在运行时拼出
    // （如 print("卖出:", sold) 运行时输出 "卖出: 2"），会误报。故列为 P2 供人工/执行核对，
    // 不作硬门禁。真正可靠的复制粘贴信号由 EXPECT-DUP(P1) 兜底。
    if (r.code && !r.code.toLowerCase().includes(r.expect.toLowerCase())) {
      findings.p2.push(`[EXPECT-SOUND] ${relPath}:${r.line} — expect="${r.expect}" 非 code 字面量（运行时拼接则忽略，否则绿灯点不亮）`);
    }
  }

  // ---- 占位引用 (P1) ----
  const urls = extractSourceUrls(content);
  const hollow = urls.filter(isHollowUrl);
  const specific = urls.filter((u) => !isHollowUrl(u));
  if (hollow.length && specific.length === 0 && urls.length > 0) {
    findings.p1.push(`[CITE-HOLLOW] ${relPath} — 来源全部为域名首页占位(${hollow.length} 条)，无任何具体文章/论文链接`);
  } else if (hollow.length) {
    findings.p2.push(`[CITE-HOLLOW] ${relPath} — 含 ${hollow.length} 条域名首页占位引用: ${hollow.slice(0, 3).join(', ')}${hollow.length > 3 ? ' …' : ''}`);
  }

  perFile.push({ relPath, meta, mermaid, interactive, quizQuestions, hollow: hollow.length });
}

// ---- LAB-REF: 检查引用的 labs 路径是否存在 (P0) ----
let missingLabRefs = 0;
/** @type {string[]} */
const missingLabDetail = [];
const missingByMonth = new Map(); // month 目录 -> 缺失路径数
const chaptersTouched = new Set();
for (const [p, refFiles] of [...labRefs].sort()) {
  const abs = path.join(REPO_ROOT, p);
  if (!fs.existsSync(abs)) {
    missingLabRefs++;
    missingLabDetail.push(`[LAB-REF] 缺失 ${p} — 被 ${refFiles.size} 个章节引用`);
    const monthM = p.match(/labs\/(month\d+|[^/]+)/);
    const month = monthM ? monthM[1] : '(其它)';
    missingByMonth.set(month, (missingByMonth.get(month) || 0) + 1);
    for (const rf of refFiles) chaptersTouched.add(rf);
  }
}
const labsRootMissing = !fs.existsSync(path.join(REPO_ROOT, 'labs'));
if (missingLabRefs > 0) {
  if (labsRootMissing) {
    findings.p0.push(
      `[LAB-REF] labs/ 目录整体缺失：${missingLabRefs} 条实验路径全部悬空，波及 ${chaptersTouched.size} 个章节，`
      + `跨 ${missingByMonth.size} 个模块（${[...missingByMonth].sort().map(([m, n]) => `${m}:${n}`).join(', ')}）。`
      + `每章"动手 Lab（必做）"学员一上手即 No such file or directory。`
    );
  } else {
    findings.p0.push(...missingLabDetail);
  }
}

// ---- EXPECT-DUP: 同一 expect 串跨多个文件复制粘贴 (P1) ----
for (const [val, fileSet] of [...expectUsage].sort((a, b) => b[1].size - a[1].size)) {
  if (fileSet.size >= THRESHOLDS.expectDupFiles) {
    findings.p1.push(`[EXPECT-DUP] expect="${val}" 被 ${fileSet.size} 个不相干文件复制粘贴，招牌"期望校验"形同虚设`);
  }
}

// ---- 输出报告 ---------------------------------------------------------------
const C = { red: '\x1b[31m', yellow: '\x1b[33m', gray: '\x1b[90m', green: '\x1b[32m', bold: '\x1b[1m', reset: '\x1b[0m' };
const c = (color, s) => (process.stdout.isTTY ? color + s + C.reset : s);

console.log(c(C.bold, '\n=== 内容质量门禁报告 (Content Quality Gate) ===\n'));
console.log(`扫描文件: ${files.length}  |  docs 根目录: ${rel(DOCS_DIR)}\n`);

function printGroup(title, list, color) {
  console.log(c(color + C.bold, `${title} (${list.length})`));
  if (!list.length) {
    console.log(c(C.gray, '  （无）'));
  } else {
    // 折叠展示：单组最多展示 20 条以免刷屏
    const cap = 20;
    const shown = list.slice(0, cap);
    for (const f of shown) console.log('  ' + c(color, '•') + ' ' + f);
    if (shown.length < list.length) console.log(c(C.gray, `  … 另有 ${list.length - shown.length} 条同类问题（--json 查看全部）`));
  }
  console.log('');
}

printGroup('P0 · 阻断级（学习闭环断裂）', findings.p0, C.red);
printGroup('P1 · 严重（招牌功能失效 / 来源失信）', findings.p1, C.yellow);
printGroup('P2 · 提示（结构与来源精细度）', findings.p2, C.gray);

const totalP0 = findings.p0.length;
const totalP1 = findings.p1.length;
const totalP2 = findings.p2.length;

console.log(c(C.bold, '---- 汇总 ----'));
console.log(`P0=${totalP0}  P1=${totalP1}  P2=${totalP2}`);
console.log(`labs 引用: ${labRefs.size} 条唯一路径，其中 ${missingLabRefs} 条缺失`);

const gateFailed = totalP0 > 0 || totalP1 > 0;
let exitCode = 0;
if (gateFailed && !REPORT_ONLY) {
  console.log(c(C.red + C.bold, `\n✗ 质量门禁未通过：存在 ${totalP0} 个 P0 + ${totalP1} 个 P1 违规。`));
  exitCode = 1;
} else if (gateFailed) {
  console.log(c(C.yellow, `\n⚠ 存在违规，但 --report-only 模式不影响退出码。`));
} else {
  console.log(c(C.green + C.bold, '\n✓ 质量门禁通过。'));
}

// JSON 始终作为最后输出，便于 CI 用 `sed -n '/marker/,$p'` 稳定截取。
if (EMIT_JSON) {
  console.log('\n<<<QUALITY_GATE_JSON>>>');
  console.log(JSON.stringify({ files: files.length, findings, missingLabRefs, missingLabDetail, thresholds: THRESHOLDS }, null, 2));
}

process.exit(exitCode);
