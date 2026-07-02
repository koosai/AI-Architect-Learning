# AI 架构师交互式学习站

这是一个本地部署、重交互、重图解、含浏览器可运行 Python 实验、带 100 个真实系统架构案例的完整 AI 架构师交互式学习站。

## 🚀 快速上手指南

本站面向完全不懂前端的使用者，提供极简的单命令管理。

### 1. 本地启动开发服务器 (实时预览)
在项目根目录下执行以下命令，启动开发环境：
```bash
npm start
```
启动成功后，浏览器会自动打开 `http://localhost:3000`。在编辑任意文档 (MDX) 时，页面会自动热更新预览。

### 2. 静态打包构建
当全部章节和组件更新完毕，需要生成最终的静态包以供离线部署时，执行：
```bash
npm run build
```
这会在根目录生成一个 `build/` 文件夹，其中包含纯静态的 HTML/JS/CSS 文件。

### 3. 本地离线预览与部署
要在完全断网的情况下本地运行或启动静态服务：
```bash
npx serve build
```
这会基于 `build/` 目录运行一个极其轻量级的本地 Web 服务器，支持全站离线运行（包括离线搜索与离线 `PyRunner` Python 代码执行）。

---

## 📂 目录结构说明

* `docs/` - 课程主目录（13 个月课程模块 + atlas 案例库 + projects 实战项目）
* `src/components/` - 所有高保真交互与模拟器组件（TypeScript + CSS Modules）
* `static/pyodide/` - 本地 vendor 的 Pyodide 运行环境（确保离线 Python 可执行）
* `docusaurus.config.ts` - 站点配置文件（已集成 Mermaid 图表支持与本地离线搜索插件）
* `sidebars.ts` - 侧边栏文件目录层次排序定义
* `TODO.md` - 整个项目后续阶段的执行清单
* `Gemini.md` - 仓库常驻规范：项目宪法
