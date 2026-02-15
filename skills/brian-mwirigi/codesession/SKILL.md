---
name: codesession
description: 使用 codesession-cli 跟踪代理会话成本、文件更改以及 Git 提交记录。该工具可执行预算限制的监控，并通过 Web 仪表板提供详细的会话分析功能。版本 1.9.6 新增了代理名称跟踪、并发会话管理以及 Web 仪表板功能。
metadata: {"openclaw": {"homepage": "https://github.com/brian-mwirigi/codesession-cli", "requires": {"bins": ["cs"]}, "install": [{"id": "npm", "kind": "node", "package": "codesession-cli", "bins": ["cs"], "label": "Install codesession-cli (npm)"}]}}
---

# 会话成本跟踪（codesession-cli）

该工具用于跟踪代理会话的成本、文件变更以及 Git 提交记录，同时支持预算限制，并提供详细的会话分析，支持通过网页仪表板进行查看。

**最新版本：v1.9.6** - 支持代理名称跟踪、并发会话处理以及带有分析功能的网页仪表板。

📦 [npm](https://www.npmjs.com/package/codesession-cli) • ⭐ [GitHub](https://github.com/brian-mwirigi/codesession-cli) • 📝 [更新日志](https://github.com/brian-mwirigi/codesession-cli/blob/main/CHANGELOG.md)

## 安装

```bash
# 1. Install the CLI globally from npm
npm install -g codesession-cli

# 2. Install the OpenClaw skill
clawhub install codesession
```

安装完成后，`cs` 命令将在全局范围内可用。OpenClaw 代理会自动使用该工具来跟踪会话。

> **系统要求：** Node.js 18 及更高版本，以及 C/C++ 编译工具（用于编译嵌入式 SQLite 模块）。
>
> | 操作系统 | 安装编译工具 |
> |---|---|
> | **Ubuntu/Debian** | `sudo apt-get install -y build-essential python3` |
> | **macOS** | `xcode-select --install` |
> | **Windows** | `npm install -g windows-build-tools` 或安装 Visual Studio Build Tools |
> | **Alpine** | `apk add build-base python3` |
>
> 数据会存储在本地文件 `~/.codesession/sessions.db` 中。

## 使用场景

- 在执行多步骤任务时，**务必** 在任务开始时启动会话跟踪。
- 每次调用 API 后，**务必** 记录 AI 的使用情况。
- 任务完成后，**务必** 结束会话。
- 在执行高成本操作前，检查预算。
- 使用 `cs dashboard` 在浏览器中查看会话数据。

## 命令说明

### 开始跟踪
```bash
# Agent mode (always use --json for structured output):
cs start "task description" --json --close-stale

# Resume if a session was left open (e.g. after a crash):
cs start "task description" --json --resume

# Human/interactive mode (stays running with live file watcher):
cs start "task description"
```

- **代理模式 vs 交互模式：** 使用 `--json` 选项时，会话会创建在数据库中，会生成 JSON 格式的输出后程序立即退出；此时会话保持“活动”状态，并在运行 `cs end` 时继续跟踪 Git 变更。如果不使用 `--json`，程序会持续运行，实时监控文件变化和 Git 提交。
- **代理名称（可选）：** 使用 `--agent "代理名称"` 可以记录执行任务的代理。这适用于多代理系统、A/B 测试以及成本分配。代理名称会显示在仪表板上，可用于按代理过滤/分析成本。

### 记录 AI 使用情况（每次 API 调用后）
```bash
# With granular tokens (cost auto-calculated from built-in pricing):
cs log-ai -p anthropic -m claude-sonnet-4 --prompt-tokens 8000 --completion-tokens 2000 --json

# With agent name tracking (NEW in v1.9.1):
cs log-ai -p anthropic -m claude-sonnet-4 --prompt-tokens 8000 --completion-tokens 2000 --agent "Code Review Bot" --json

# With manual cost:
cs log-ai -p anthropic -m claude-opus-4-6 -t 15000 -c 0.30 --json

# With all fields:
cs log-ai -p openai -m gpt-4o --prompt-tokens 5000 --completion-tokens 1500 -c 0.04 --agent "Research Agent" --json
```
支持的 AI 提供商包括：`anthropic`、`openai`、`google`、`mistral`、`deepseek`。成本会根据可配置的定价表自动计算（内置了 17 种以上模型）。使用 `cs pricing list --json` 查看可用模型；如果模型未在列表中，需手动指定 `-c <成本>`。

### 检查当前状态
```bash
cs status --json
```
返回包含当前会话成本、使用的令牌数量、文件变更情况及会话持续时间的 JSON 数据。所有 JSON 响应中都包含 `schemaVersion` 和 `codesessionVersion` 字段。

### 结束会话并获取摘要
```bash
cs end -n "completion notes" --json
```
结束会话时，codesession 会自动扫描自会话开始以来所有更改的文件和提交的 Git 提交记录（即使使用了 `--json` 模式，也不需要实时监控工具）。

### 网页仪表板
```bash
cs dashboard
# Opens http://localhost:3737 with full analytics UI

cs dashboard --port 4000       # custom port
cs dashboard --no-open         # don't auto-open browser
```

仪表板提供以下功能：
- **概览**：关键绩效指标（KPI）、每日成本/令牌使用趋势、支出预测、成本变化情况。
- **会话**：可搜索/排序的表格，包含每个会话的详细信息（时间线、文件列表、提交记录、AI 调用记录、备注）。
- **模型**：按模型和提供商划分的成本明细、令牌使用比例、使用情况图表。
- **洞察**：文件热点区域、活动热图、项目成本分布、定价表。

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
cs note "Starting refactor phase"
cs note "Tests passing, moving to cleanup"
```
添加的备注会以时间戳的形式显示在 `cs show --json` 的 `annotations` 部分。

### 恢复过期会话
```bash
cs recover --max-age 12
```
系统会自动结束所有超过 12 小时的活动会话。

## 代理工作流程

代理在执行每个命令时**必须** 使用 `--json` 选项，以确保输出格式统一且易于解析：
1. 任务开始时：`cs start "修复认证漏洞" --json --close-stale`
2. 添加上下文备注：`cs note "分析认证流程" --json`
3. 每次调用 AI 服务后：`cs log-ai -p anthropic -m claude-sonnet-4 --prompt-tokens 8000 --completion-tokens 2000 --agent "Bug Fixer" --json`
4. 检查费用：`cs status --json`（查看 `aiCost` 字段）
5. 任务结束时：`cs end -n "修复了认证漏洞，并添加了测试用例" --json`
6. 查看历史会话：`cs dashboard`

**提示：** 使用 `--agent` 标志可以明确指定执行任务的代理，这在多代理系统中非常有用（例如：“代码审查机器人”、“测试编写器”、“文档生成代理”）。

## 定价

定价设置是可配置的。运行 `cs pricing list` 可查看所有可用模型的价格。如需自定义模型价格，可以使用以下命令：
```bash
# Plain model key
cs pricing set my-model 5.00 15.00

# Provider-namespaced key (avoids collisions)
cs pricing set gpt-4o 2.50 10.00 --provider openai
```

如果模型不在定价表中，调用 API 时必须手动指定 `-c <成本>`。

## 预算监控

如果用户设置了预算或系统检测到高成本支出：
- 在执行高成本操作前，检查 `cs status --json`。
- 如果单次会话的 `aiCost` 超过 5 美元，提醒用户。
- 如果成本持续上升，建议更换更经济的模型。

## 重要提示：

- 使用 `--close-stale` 选项在 `cs start` 命令中，以避免因系统崩溃导致的会话状态异常。
- 如果未安装 codesession-cli，请跳过会话跟踪功能，以免影响用户任务。
- **务必** 在每个命令中都使用 `--json` 选项，确保输出格式统一。
- 使用 `--json` 时，`cs start` 会立即创建会话并退出（无需长时间运行的进程）。
- 会话的范围基于 Git 的根目录——即使从子目录运行，也会关联到整个仓库的会话记录。
- 在 `--json` 模式下发生错误时，退出代码始终为 1，响应中会包含 `{ "error": { "code": "...", "message": "..." } `。
- 通过检查 JSON 响应中的 `schemaVersion` 字段来检测潜在的代码变更。

## 更新检查

定期检查 CLI 是否为最新版本（例如在会话开始时或每天一次）：
```bash
# Compare installed version to latest on npm:
cs --version          # installed version
npm view codesession-cli version  # latest on npm
```

如果发现已安装版本过时，通知用户：
> “codesession-cli 有新版本可用：v1.8.4 -> v1.9.0。请运行 `npm install -g codesession-cli` 进行更新。”

更新过程中不要中断工作流程，只需通知用户后继续执行任务即可。

## JSON 输出格式

所有命令都支持 `--json` 选项，以生成机器可读的 JSON 输出格式。这有助于程序化地处理会话数据。