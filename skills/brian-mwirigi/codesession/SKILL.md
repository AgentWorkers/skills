---
name: codesession
description: **codesession (codesession-cli, code session, code-session)**：用于跟踪 AI 代理的会话成本、令牌使用情况、文件变更以及 Git 提交记录。支持与 Claude Code、OpenClaw、Codex、GPT、Cursor、Windsurf、Cline 等所有 AI 代理集成。具备预算管理、自动定价功能，支持 MCP 服务器、Web 仪表板以及警报/洞察报告。版本：v2.5.1。
metadata: {"openclaw": {"homepage": "https://github.com/brian-mwirigi/codesession-cli", "requires": {"bins": ["cs"]}, "install": [{"id": "npm", "kind": "node", "package": "codesession-cli", "bins": ["cs"], "label": "Install codesession-cli (npm)"}]}}
---
# 会话成本跟踪（codesession-cli）

该工具用于跟踪代理会话成本、文件变更以及 Git 提交记录，同时支持预算限制，并提供详细的会话分析功能，可通过完整的 Web 仪表板进行查看。

**最新版本：v2.5.1**  
- `cs run <命令>` 可将所有操作（会话启动、代理启动、命令执行及成本统计）整合到一步完成。  
- `cs today` 适用于多项目环境。  
- 仪表板新增了帮助页面、Codex定价信息以及安全修复。

📦 [npm](https://www.npmjs.com/package/codesession-cli) • ⭐ [GitHub](https://github.com/brian-mwirigi/codesession-cli) • 📝 [变更日志](https://github.com/brian-mwirigi/codesession-cli/blob/main/CHANGELOG.md)

## 安装

```bash
# 1. 通过 npm 全局安装 CLI  
npm install -g codesession-cli  

# 2. 安装 OpenClaw 插件  
clawhub install codesession  
```

安装完成后，`cs` 命令将在全局环境中可用。OpenClaw 代理会自动使用该工具进行会话跟踪。

> **系统要求：** Node.js 18+ 及 C/C++ 编译工具（用于编译内置的 SQLite 模块）  

> | 操作系统 | 编译工具安装方法 |
|---|---|
| **Ubuntu/Debian** | `sudo apt-get install -y build-essential python3` |
| **macOS** | `xcode-select --install` |
| **Windows** | `npm install -g windows-build-tools` 或安装 Visual Studio Build Tools |
| **Alpine** | `apk add build-base python3` |

数据会存储在本地路径 `~/.codesession/sessions.db` 中。

## 使用场景

- **务必** 在多步骤任务开始时启动会话跟踪。  
- **每次调用 API 后** 都需记录 AI 使用情况。  
- 任务完成后 **务必** 结束会话。  
- 在执行高成本操作前请检查预算。  
- 使用 `cs dashboard` 在浏览器中查看会话数据。

## 命令说明

### 启动会话跟踪

```bash
# 代理模式（建议使用 --json 以获得结构化输出）  
cs start "任务描述" --json --close-stale  

# 如果会话中途中断（如系统崩溃），可恢复会话：  
cs start "任务描述" --json --resume  

# 交互模式（持续运行并实时监控文件变化）  
cs start "任务描述"  
```

> **代理模式与交互模式的区别：**  
- 使用 `--json` 时，会话会创建在数据库中，输出为 JSON 格式，程序立即退出；后续通过 `cs end` 可继续跟踪 Git 变更。  
- 不使用 `--json` 时，程序会持续运行并实时监控文件变化及 Git 提交。

### 记录 AI 使用情况（每次 API 调用后）

```bash
# 使用预设的提示令牌（费用自动计算）：  
cs log-ai -p anthropic -m claude-sonnet-4 --prompt-tokens 8000 --completion-tokens 2000 --json  

# 可指定代理名称（v1.9.1 新功能）：  
cs log-ai -p anthropic -m claude-sonnet-4 --prompt-tokens 8000 --completion-tokens 2000 --agent "代码审核机器人" --json  

# 手动指定费用：  
cs log-ai -p anthropic -m claude-opus-4-6 -t 15000 -c 0.30 --json  

# 显示所有相关字段：  
cs log-ai -p openai -m gpt-4o --prompt-tokens 5000 --completion-tokens 1500 -c 0.04 --agent "研究机器人" --json  
```
可用模型：`anthropic`, `openai`, `google`, `mistral`, `deepseek`  
费用根据可配置的定价表自动计算（包含 Codex 在内的 21 种模型）。使用 `cs pricing list --json` 查看可用模型；若模型未列出，请手动指定费用：`-c <费用>`。

**代理名称（可选）：** 通过 `--agent "代理名称"` 标记执行任务的代理，适用于多代理系统、A/B 测试及成本分配。代理名称会显示在仪表板上，便于按代理筛选/分析费用。

### 查看当前状态

```bash
cs status --json  
```
返回包含当前会话成本、使用令牌数量、文件变更情况及持续时间的 JSON 数据。所有 JSON 响应中均包含 `schemaVersion` 和 `codesessionVersion` 字段。

### 结束会话并获取统计信息

```bash
cs end -n "完成说明" --json  
```
会话结束后，codesession 会自动扫描自会话开始以来的所有文件变更和 Git 提交记录（即使使用了 `--json` 模式，也无需额外监控工具）。

### Web 仪表板

```bash
cs dashboard  
# 打开 http://localhost:3737 查看完整分析界面  
cs dashboard --port 4000       # 自定义端口  
cs dashboard --no-open         # 不自动打开浏览器  
```

仪表板功能包括：  
- **概览**：KPI、每日成本/令牌使用趋势、费用预测  
- **会话**：可搜索/排序的会话详情（包含时间线、文件、提交记录、AI 调用记录及备注）  
- **模型**：按模型和提供者划分的费用明细  
- **洞察**：文件热点、活动热图、项目费用分布  
- **警报**：设置每日/总费用/会话费用阈值（支持声音提示和浏览器通知）  
- **重置会话**：通过侧边栏重置所有会话数据  

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
注释会以时间戳形式显示在 `cs show --json` 的 `annotations` 部分。

### 恢复过期会话

```bash
cs recover --max-age 12  
```
自动结束超过 12 小时的活动会话。

## 代理工作流程

建议代理在所有命令中都使用 `--json` 以获得结构化输出：

1. 任务开始：`cs start "修复认证漏洞" --json --close-stale`  
2. 添加上下文注释：`cs note "分析认证流程" --json`  
3. 每次调用 AI 后：`cs log-ai -p anthropic -m claude-sonnet-4 ...`  
4. 检查费用：`cs status --json`（查看 `aiCost` 字段）  
5. 任务完成：`cs end -n "修复认证漏洞，添加测试" --json`  
6. 查看历史会话：`cs dashboard`  

**提示：** 使用 `--agent` 标志可明确记录具体代理的工作内容，尤其适用于多代理系统（如“代码审核机器人”、“测试编写器”等）。

## 定价

定价设置可自定义。运行 `cs pricing list` 查看所有模型价格。例如：

```bash
# 使用模型名称：  
cs pricing set my-model 5.00 15.00  

# 使用提供者名称：  
cs pricing set gpt-4o 2.50 10.00 --provider openai  
```

如果模型未在定价表中，需手动指定费用：`-c <费用>`。

## 代理模式与 `cs run`（v2.5.0）

**快速启动会话的方法：**

```bash
cs run python my_agent.py  
# 或：cs run --name "fix auth" node agent.js  
```

该命令会启动会话、启动代理、执行命令，然后结束会话并输出费用统计。无需额外终端或环境变量。

如需手动控制，可在一个终端中启动代理并设置环境变量：

```bash
cs proxy --session "我的任务"   # 也会自动启动会话  
# 然后在代理 shell 中设置环境变量：  
export ANTHROPIC_BASE_URL=http://127.0.0.1:3739  
export OPENAI_BASE_URL=http://127.0.0.1:3739/v1  
```

代理仅绑定到 `127.0.0.1` 地址，不会存储提示文本或 API 密钥，仅记录令牌使用情况。

## 预算监控

如果用户设置了预算或检测到高费用支出：  
- 在执行高成本操作前查看 `cs status --json`。  
- 若单次会话费用超过 5 美元，立即提醒用户。  
- 若费用持续上升，建议更换成本较低的模型。

## 重要提示：

- 使用 `--close-stale` 可避免因系统崩溃导致的会话异常。  
- 若未安装 codesession-cli，请勿阻止用户正常操作。  
- **所有命令都必须使用 `--json` 以获得结构化输出。**  
- 使用 `--json` 时，`cs start` 会立即创建会话并结束（无需长时间运行的进程）。  
- 会话范围基于 Git 根目录；即使在子目录中运行，也会关联到整个仓库的会话记录。  
- 在 `--json` 模式下出现错误时，退出代码为 1，响应中包含错误信息。  
- 通过检查 JSON 响应中的 `schemaVersion` 识别版本更新。

## 更新检查

定期检查 CLI 是否为最新版本（例如在会话开始时或每天一次）：

```bash
# 检查安装版本与 npm 上的最新版本：  
cs --version          # 安装版本  
npm view codesession-cli version  # npm 上的最新版本  
```

若发现版本过旧，通知用户：  
> “codesession-cli 有新版本可用：v1.9.4 → v2.0.0。请运行 `npm install -g codesession-cli` 进行更新。”  

更新过程中请勿中断工作流程，只需通知用户即可。

## JSON 输出格式

所有命令都支持 `--json` 选项，以生成机器可读的 JSON 格式输出，便于程序化处理会话数据。