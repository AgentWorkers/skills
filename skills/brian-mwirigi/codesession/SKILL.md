---
name: codesession
description: 使用 `codesession-cli` 跟踪代理会话成本、文件变更以及 Git 提交记录。该工具可执行预算限制管理，并通过 Web 仪表板提供详细的会话分析功能。版本：2.0.0 – 新增了警报功能、重置会话状态的功能以及数据洞察页面。
metadata: {"openclaw": {"homepage": "https://github.com/brian-mwirigi/codesession-cli", "requires": {"bins": ["cs"]}, "install": [{"id": "npm", "kind": "node", "package": "codesession-cli", "bins": ["cs"], "label": "Install codesession-cli (npm)"}]}}
---
# 会话成本跟踪（codesession-cli）

该工具用于跟踪代理会话的成本、文件变更以及 Git 提交记录，同时支持预算限制，并提供详细的会话分析，可通过完整的 Web 仪表板进行查看。

**最新版本：v2.0.0** - 新增了仪表板警报功能、会话数据重置选项以及智能分析页面。

📦 [npm](https://www.npmjs.com/package/codesession-cli) • ⭐ [GitHub](https://github.com/brian-mwirigi/codesession-cli) • 📝 [更新日志](https://github.com/brian-mwirigi/codesession-cli/blob/main/CHANGELOG.md)

## 安装

```bash
# 1. Install the CLI globally from npm
npm install -g codesession-cli

# 2. Install the OpenClaw skill
clawhub install codesession
```

安装完成后，`cs` 命令将在全局范围内可用。OpenClaw 代理会自动使用该工具来跟踪会话信息。

> **系统要求：** Node.js 18 及以上版本，以及 C/C++ 编译工具（用于编译内置的 SQLite 模块）。

> | 操作系统 | 安装编译工具 |
> |---|---|
> | **Ubuntu/Debian** | `sudo apt-get install -y build-essential python3` |
| **macOS** | `xcode-select --install` |
| **Windows** | `npm install -g windows-build-tools` 或安装 Visual Studio Build Tools |
| **Alpine** | `apk add build-base python3` |

> 数据会存储在本地文件 `~/.codesession/sessions.db` 中。

## 使用场景

- 在执行多步骤任务时，**必须** 在任务开始时启动会话跟踪。
- 每次调用 API 后，**必须** 记录 AI 的使用情况。
- 任务完成后，**必须** 结束会话跟踪。
- 在执行高成本操作前，检查预算。
- 使用浏览器中的 `cs dashboard` 查看会话数据。

## 命令说明

### 启动会话跟踪
```bash
# Agent mode (always use --json for structured output):
cs start "task description" --json --close-stale

# Resume if a session was left open (e.g. after a crash):
cs start "task description" --json --resume

# Human/interactive mode (stays running with live file watcher):
cs start "task description"
```

- **代理模式 vs 交互模式：** 使用 `--json` 选项时，会话信息会被写入数据库并生成 JSON 格式的输出，然后程序立即退出；此时会话仍处于“活动”状态，并会在您再次运行 `cs end` 时继续跟踪 Git 变更。
- 不使用 `--json` 选项时，程序会持续运行，实时监控文件变化并监听 Git 提交事件，直到您按下 Ctrl+C 或在另一个终端中运行 `cs end`。

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
支持的 AI 提供商包括：`anthropic`、`openai`、`google`、`mistral`、`deepseek`。
成本会根据可配置的定价表自动计算（内置了 17 种以上模型）。使用 `cs pricing list --json` 查看可用模型；如果模型未在列表中，请手动指定 `-c <cost>` 参数。

**代理名称（可选）：** 使用 `--agent "代理名称"` 来标识执行任务的代理。适用于多代理系统、A/B 测试和成本分配。代理名称会显示在仪表板上，可用于按代理过滤和分析成本。

### 查看当前会话状态
```bash
cs status --json
```
返回包含当前会话成本、使用的令牌数量、文件变更情况及会话持续时间的 JSON 数据。所有 JSON 响应中都包含 `schemaVersion` 和 `codesessionVersion` 字段。

### 结束会话并获取摘要
```bash
cs end -n "completion notes" --json
```
结束会话后，codesession 会自动扫描自会话开始以来的所有文件变更和 Git 提交记录（即使使用了 `--json` 选项，也不需要实时监控工具）。

### Web 仪表板
```bash
cs dashboard
# Opens http://localhost:3737 with full analytics UI

cs dashboard --port 4000       # custom port
cs dashboard --no-open         # don't auto-open browser
```

仪表板功能包括：
- **概览**：关键绩效指标（KPI）、每日成本/令牌使用趋势、成本预测。
- **会话记录**：可搜索/排序的表格，显示每个会话的详细信息（包括时间线、文件列表、提交记录和 AI 调用记录）。
- **模型统计**：按模型和提供商划分的成本明细、令牌使用比例及使用图表。
- **智能分析**：文件热点分析、活动热图、项目成本分布、定价信息。
- **警报**：可设置每日/总成本/会话成本的阈值，并支持警报功能（声音提示和浏览器通知）。
- **重置会话数据**：通过侧边栏可重置所有会话记录。

### 查看会话详情
```bash
cs show --json --files --commits
```

### 查看历史记录
```bash
cs stats --json
```

### 导出会话数据
```bash
cs export --format json --limit 10
cs export --format csv
```

### 添加注释/备注
```bash
cs note "Starting refactor phase"
cs note "Tests passing, moving to cleanup"
```
添加的注释会以时间戳的形式显示在 `cs show --json` 的 `annotations` 部分。

### 恢复过期会话
```bash
cs recover --max-age 12
```
系统会自动结束所有超过 12 小时的活跃会话。

## 代理工作流程

代理在执行命令时**必须** 使用 `--json` 选项，以确保输出格式统一且易于解析：

1. 任务开始时：`cs start "修复认证漏洞" --json --close-stale`
2. 添加上下文注释：`cs note "分析认证流程" --json`
3. 每次调用 AI 服务后：`cs log-ai -p anthropic -m claude-sonnet-4 --prompt-tokens 8000 --completion-tokens 2000 --agent "Bug Fixer" --json`
4. 检查成本：`cs status --json`（查看 `aiCost` 字段）
5. 任务结束时：`cs end -n "修复了认证漏洞，并添加了测试用例" --json`
6. 查看历史会话记录：`cs dashboard`

**提示：** 使用 `--agent` 标志来指定执行任务的代理，这在多代理系统中非常有用（例如区分“代码审核机器人”、“测试编写器”和“文档生成代理”等角色）。

## 定价

定价设置是可配置的。运行 `cs pricing list` 可查看所有模型的价格。如需修改或添加新模型，请执行以下操作：

```bash
# Plain model key
cs pricing set my-model 5.00 15.00

# Provider-namespaced key (avoids collisions)
cs pricing set gpt-4o 2.50 10.00 --provider openai
```

如果模型未在定价表中，调用 API 时必须手动指定 `-c <成本>` 参数。

## 预算监控

如果用户设置了预算或系统检测到高成本支出：
- 在执行高成本操作前，检查 `cs status --json`。
- 如果单次会话的成本超过 5 美元，及时提醒用户。
- 如果成本持续上升，建议使用成本更低的模型。

## 重要提示：

- 在使用 `cs start` 时务必加上 `--close-stale` 选项，以避免因系统崩溃导致的会话状态异常。
- 如果未安装 codesession-cli，请勿阻止用户继续任务。
- 所有命令都必须使用 `--json` 选项，以确保输出格式一致。
- 使用 `--json` 选项时，`cs start` 会立即创建会话并结束程序（无需长时间运行的进程）。
- 会话记录的范围基于 Git 的根目录；即使从子目录执行命令，也会记录在仓库级别的会话中。
- 在使用 `--json` 模式时，程序的退出代码始终为 1，响应中会包含 `{ "error": { "code": "...", "message": "..." } `。
- 通过检查 JSON 响应中的 `schemaVersion` 字段来检测潜在的格式问题。

## 更新检查

定期检查 CLI 是否为最新版本（例如在会话开始时或每天一次）：

```bash
# Compare installed version to latest on npm:
cs --version          # installed version
npm view codesession-cli version  # latest on npm
```

如果发现已安装版本过旧，及时通知用户：
> “codesession-cli 有新版本可用：v1.9.4 -> v2.0.0。请运行 `npm install -g codesession-cli` 进行更新。”

更新过程中不要中断用户的工作流程，只需通知用户后继续操作即可。

## JSON 输出格式

所有命令都支持 `--json` 选项，以生成机器可读的 JSON 输出格式。这有助于程序化地处理会话数据。