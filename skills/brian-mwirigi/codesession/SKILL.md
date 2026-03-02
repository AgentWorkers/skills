---
name: codesession
description: **codesession (codesession-cli, code session, code-session)** — 用于追踪 AI 代理的会话成本、令牌使用情况、文件变更以及 Git 提交记录。支持与 Claude Code、OpenClaw、Codex、GPT、Cursor、Windsurf、Cline 等所有 AI 代理集成。具备预算管理、自动定价功能，支持 MCP 服务器、Web 控制面板以及警报与数据洞察功能。版本：v2.4.0。
metadata: {"openclaw": {"homepage": "https://github.com/brian-mwirigi/codesession-cli", "requires": {"bins": ["cs"]}, "install": [{"id": "npm", "kind": "node", "package": "codesession-cli", "bins": ["cs"], "label": "Install codesession-cli (npm)"}]}}
---
# 会话成本跟踪（codesession-cli）

该工具用于追踪代理会话成本、文件变更及 Git 提交记录，同时支持预算限制，并通过完整的 Web 仪表板提供详细的会话分析。

**最新版本：v2.4.0** - 支持 Codex 定价模式（`codex-mini-latest`、`gpt-5.1-codex-max`、`gpt-5.1-codex-mini`、`gpt-5.3-codex`），修复了安全漏洞并提升了稳定性。

📦 [npm](https://www.npmjs.com/package/codesession-cli) • ⭐ [GitHub](https://github.com/brian-mwirigi/codesession-cli) • 📝 [更新日志](https://github.com/brian-mwirigi/codesession-cli/blob/main/CHANGELOG.md)

## 安装

```bash
# 1. 通过 npm 全局安装 CLI
npm install -g codesession-cli

# 2. 安装 OpenClaw 插件
clawhub install codesession
```

安装完成后，`cs` 命令将在全局范围内可用。OpenClaw 代理会自动使用该工具进行会话跟踪。

> **系统要求：** Node.js 18 及以上版本，以及 C/C++ 编译工具（用于编译嵌入式 SQLite 模块）。

> | 操作系统 | 安装编译工具 |
> |---|---|
> | **Ubuntu/Debian** | `sudo apt-get install -y build-essential python3`
> | **macOS** | `xcode-select --install`
> | **Windows** | `npm install -g windows-build-tools` 或安装 Visual Studio Build Tools`
> | **Alpine** | `apk add build-base python3`

数据会存储在本地文件 `~/.codesession/sessions.db` 中。

## 使用场景

- 在多步骤任务开始时，**必须** 启动会话跟踪。
- 每次调用 API 后，**必须** 记录 AI 使用情况。
- 任务完成后，**必须** 结束会话。
- 在执行高成本操作前，请检查预算。
- 使用 `cs dashboard` 在浏览器中查看会话数据。

## 命令

### 启动会话跟踪

```bash
# 代理模式（使用 `--json` 以获得结构化输出）：
cs start "任务描述" --json --close-stale

# 如果会话中途中断（例如程序崩溃），可以恢复：
cs start "任务描述" --json --resume

# 交互模式（持续运行并实时监控文件变化）：
cs start "任务描述"
```

> **代理模式与交互模式的区别：** 使用 `--json` 时，会话会创建在数据库中，输出为 JSON 格式，程序立即退出；此时会话保持“活动”状态，当运行 `cs end` 时仍会跟踪 Git 变更。不使用 `--json` 时，程序会持续运行并实时监控文件变化及 Git 提交。

### 记录 AI 使用情况（每次 API 调用后）

```bash
# 使用预设的计费规则自动计算成本：
cs log-ai -p anthropic -m claude-sonnet-4 --prompt-tokens 8000 --completion-tokens 2000 --json

# 可指定代理名称（v1.9.1 新功能）：
cs log-ai -p anthropic -m claude-sonnet-4 --prompt-tokens 8000 --completion-tokens 2000 --agent "代码审查机器人" --json

# 手动指定成本：
cs log-ai -p anthropic -m claude-opus-4-6 -t 15000 -c 0.30 --json

# 显示所有字段：
cs log-ai -p openai -m gpt-4o --prompt-tokens 5000 --completion-tokens 1500 -c 0.04 --agent "研究机器人" --json
```
可用模型：`anthropic`、`openai`、`google`、`mistral`、`deepseek`。

成本根据可配置的定价表自动计算（包含 Codex 在内的 21 种内置模型）。使用 `cs pricing list --json` 查看可用模型列表。如果模型未在列表中，请手动指定成本（格式：`-c <成本>`）。

**代理名称（可选）：** 使用 `--agent "代理名称"` 标记执行任务的代理，适用于多代理系统、A/B 测试及成本分配。代理名称会显示在仪表板上，可用于按代理过滤/分析成本。

### 查看当前状态

```bash
cs status --json
```
返回包含当前会话成本、使用的令牌数量、文件变更情况及持续时间的 JSON 数据。所有 JSON 响应中都包含 `schemaVersion` 和 `codesessionVersion` 字段。

### 结束会话并获取摘要

```bash
cs end -n "完成说明" --json
```
结束会话后，`codesession` 会自动扫描自会话开始以来的所有文件变更和 Git 提交记录（即使使用了 `--json` 模式，也无需实时监控工具）。

### Web 仪表板

```bash
cs dashboard
# 打开 http://localhost:3737 查看完整分析界面

cs dashboard --port 4000       # 自定义端口
cs dashboard --no-open         # 不自动打开浏览器
```

仪表板内容包括：
- **概览**：关键绩效指标（KPI）、每日成本/令牌使用趋势、支出预测
- **会话**：可搜索/排序的会话列表，包含时间线、文件、提交记录、AI 调用信息及备注
- **模型**：各模型及提供商的成本明细、令牌使用情况
- **洞察**：文件热点区域、活动热图、项目成本分布
- **警报**：设置每日/总成本/会话成本阈值，并支持警报功能（声音提示+浏览器通知）
- **重新开始**：通过侧边栏重置所有会话数据

### 查看会话详情

```bash
cs show --json --files --commits
```

### 查看历史数据

```bash
cs stats --json
```

### 导出会话数据

```bash
cs export --format json --limit 10
cs export --format csv
```

### 添加备注/注释

```bash
cs note "开始重构阶段"
cs note "测试通过，进入清理阶段"
```
添加的备注会以时间戳形式显示在 `cs show --json` 的 `annotations` 部分。

### 恢复过期会话

```bash
cs recover --max-age 12
```
自动结束超过 12 小时的活动会话。

## 代理工作流程

代理在执行每个命令时**必须** 使用 `--json` 以获得结构化输出：

1. 任务开始：`cs start "修复认证漏洞" --json --close-stale`
2. 添加上下文注释：`cs note "分析认证流程" --json`
3. 每次调用 AI 后：`cs log-ai -p anthropic -m claude-sonnet-4 --prompt-tokens 8000 --completion-tokens 2000 --agent "漏洞修复器" --json`
4. 检查成本：`cs status --json`（查看 `aiCost` 字段）
5. 任务结束：`cs end -n "修复了认证漏洞，添加了测试用例" --json`
6. 查看历史会话：`cs dashboard`

**提示：** 使用 `--agent` 标志可明确记录具体代理的工作内容，尤其适用于多代理系统（如“代码审查机器人”、“测试编写器”、“文档生成器”等）。

## 定价

定价设置可自定义。运行 `cs pricing list` 查看所有模型价格。可以覆盖或新增模型：

```bash
# 简单模型名称：
cs pricing set my-model 5.00 15.00

# 带提供商名称的模型名称（避免名称冲突）：
cs pricing set gpt-4o 2.50 10.00 --provider openai
```
如果模型未在定价表中，使用 `--c <成本>` 手动指定成本。

## 预算监控

如果用户设置了预算或检测到高成本支出：
- 在执行高成本操作前，检查 `cs status --json`
- 如果单次会话的 `aiCost` 超过 5.00 美元，提醒用户
- 如果成本持续上升，建议更换成本较低的模型

## 重要提示

- 使用 `--close-stale` 选项可避免因程序崩溃导致的会话状态错误。
- 如果未安装 `codesession-cli`，请勿强制进行会话跟踪，以免影响用户任务。
- **所有命令都必须** 使用 `--json` 以获得结构化输出。
- 使用 `--json` 时，`cs start` 会立即创建会话并退出（无需长时间运行的进程）。
- 会话范围基于 Git 根目录：即使从子目录运行，也会关联到整个仓库的会话记录。
- 在 `--json` 模式下发生错误时，退出代码始终为 1，响应格式为 `{ "error": { "code": "...", "message": "..." }`。
- 通过检查 JSON 响应中的 `schemaVersion` 字段来检测潜在的代码变更。

## 更新检查

定期检查 CLI 是否为最新版本（例如在会话开始时或每天一次）：

```bash
# 比较已安装版本与 npm 上的最新版本：
cs --version          # 已安装版本
npm view codesession-cli version  # npm 上的最新版本
```
如果发现已安装版本过时，通知用户：
> “codesession-cli 有新版本可用：v1.9.4 -> v2.0.0。请运行 `npm install -g codesession-cli` 进行更新。”

更新过程中不要中断工作流程，只需通知用户即可。

## JSON 输出

所有命令都支持 `--json` 选项，以生成机器可读的 JSON 输出格式，便于程序化处理会话数据。