---
name: codesession
description: **codesession** (codesession-cli, code session, code-session) — 用于追踪 AI 代理的会话成本、令牌使用情况、文件变更以及 Git 提交记录。支持与 Claude Code、OpenClaw、Codex、GPT、Cursor、Windsurf、Cline 等所有 AI 代理集成。具备预算管理、自动定价功能，支持 MCP 服务器、Web 仪表板以及警报系统，可提供数据分析与洞察。版本：v2.3.0。
metadata: {"openclaw": {"homepage": "https://github.com/brian-mwirigi/codesession-cli", "requires": {"bins": ["cs"]}, "install": [{"id": "npm", "kind": "node", "package": "codesession-cli", "bins": ["cs"], "label": "Install codesession-cli (npm)"}]}}
---
# 会话成本跟踪（codesession-cli）

该工具用于追踪代理会话成本、文件变更及Git提交记录，同时支持预算限制设置，并通过完整的Web仪表板提供详细的会话分析功能。

**最新版本：v2.2.0** - 新增Claude Code MCP插件、警报功能、会话数据重置选项以及洞察页面。

📦 [npm](https://www.npmjs.com/package/codesession-cli) • ⭐ [GitHub](https://github.com/brian-mwirigi/codesession-cli) • 📝 [更新日志](https://github.com/brian-mwirigi/codesession-cli/blob/main/CHANGELOG.md)

## 安装

```bash
# 1. 通过npm全局安装CLI
npm install -g codesession-cli

# 2. 安装OpenClaw插件
clawhub install codesession
```

安装完成后，`cs`命令将在全局环境中可用。OpenClaw代理会自动使用该工具进行会话跟踪。

> **系统要求：** Node.js 18及以上版本，以及C/C++编译工具（用于编译内置的SQLite模块）。

> | 操作系统 | 编译工具安装方式 |
|---|---|
| **Ubuntu/Debian** | `sudo apt-get install -y build-essential python3`
| **macOS** | `xcode-select --install`
| **Windows** | `npm install -g windows-build-tools` 或安装Visual Studio Build Tools`
| **Alpine** | `apk add build-base python3`

> 数据存储在本地路径`~/.codesession/sessions.db`中。

## 使用场景

- 在执行多步骤任务时，**始终**在任务开始时启动会话跟踪。
- 每次调用API后，**务必**记录AI使用情况。
- 任务完成后，**务必**结束会话。
- 在执行高成本操作前，请检查预算。
- 使用`cs dashboard`在浏览器中查看会话数据。

## 命令说明

### 启动会话跟踪

```bash
# 代理模式（使用`--json`可获取结构化输出）：
cs start "任务描述" --json --close-stale

# 如果会话中途中断（如系统崩溃），可恢复会话：
cs start "任务描述" --json --resume

# 交互模式（持续运行并实时监控文件变化）：
cs start "任务描述"
```

> **代理模式与交互模式的区别：** 使用`--json`时，会话会创建在数据库中，输出为JSON格式，程序立即退出；此时会话保持“活跃”状态，后续可以通过`cs end`命令继续跟踪Git变更。不使用`--json`时，程序会持续运行并实时监控文件变化及Git提交。

### 记录AI使用情况（每次API调用后）

```bash
# 使用预设的提示令牌（成本自动计算）：
cs log-ai -p anthropic -m claude-sonnet-4 --prompt-tokens 8000 --completion-tokens 2000 --json

# 可指定代理名称（v1.9.1新增功能）：
cs log-ai -p anthropic -m claude-sonnet-4 --prompt-tokens 8000 --completion-tokens 2000 --agent "代码审核机器人" --json

# 手动指定成本：
cs log-ai -p anthropic -m claude-opus-4-6 -t 15000 -c 0.30 --json

# 显示所有详细信息：
cs log-ai -p openai -m gpt-4o --prompt-tokens 5000 --completion-tokens 1500 -c 0.04 --agent "研究机器人" --json
```
可用提供商：`anthropic`, `openai`, `google`, `mistral`, `deepseek`。
成本根据可配置的定价表自动计算（支持17种以上内置模型）。使用`cs pricing list --json`查看可用模型。如果模型未在列表中，请手动指定成本（格式：`-c <成本>`）。

**代理名称（可选）：** 使用`--agent "代理名称"`来记录执行任务的代理。适用于多代理系统、A/B测试及成本分配。代理名称会显示在仪表板上，可用于按代理筛选/分析成本。

### 查看当前状态

```bash
cs status --json
```
返回包含当前会话成本、使用令牌数量、文件变更情况及持续时间的JSON数据。所有JSON响应均包含`schemaVersion`和`codesessionVersion`字段。

### 结束会话并获取摘要

```bash
cs end -n "完成说明" --json
```
结束会话后，`codesession`会自动扫描自会话开始以来的所有文件变更和Git提交记录（即使使用了`--json`模式，也无需额外监控工具）。

### Web仪表板

```bash
cs dashboard
# 打开http://localhost:3737，查看完整分析界面
```

或使用自定义端口：
```bash
cs dashboard --port 4000
cs dashboard --no-open  # 不自动打开浏览器
```

仪表板功能包括：
- **概览**：关键性能指标、每日成本/令牌使用趋势、费用预测
- **会话**：可搜索/排序的会话列表，包含时间线、文件信息、提交记录及AI调用详情
- **模型**：按模型和提供商划分的成本明细、令牌使用情况
- **洞察**：文件热点、活动热度图、项目成本分布
- **警报**：设置每日/总成本/会话成本阈值，并支持警报功能（声音提示+浏览器通知）
- **重置会话数据**：通过侧边栏重置所有会话信息

### 查看会话详情

```bash
cs show --json --files --commits
```

### 查看历史统计信息

```bash
cs stats --json
```

### 导出会话数据

```bash
cs export --format json --limit 10
cs export --format csv
```

### 添加注释

```bash
cs note "开始重构阶段"
cs note "测试通过，进入清理阶段"
```
添加的注释会以时间戳形式显示在`cs show --json`的`annotations`字段中。

### 恢复过期会话

```bash
cs recover --max-age 12
```
自动结束超过12小时的活跃会话。

## 代理工作流程

建议代理在所有命令中**始终**使用`--json`选项，以确保输出数据具有结构化且可解析。

1. 任务开始时：`cs start "修复认证漏洞" --json --close-stale`
2. 添加上下文注释：`cs note "分析认证流程" --json`
3. 每次调用AI后：`cs log-ai -p anthropic -m claude-sonnet-4 --prompt-tokens 8000 --completion-tokens 2000 --agent "漏洞修复器" --json`
4. 检查费用：`cs status --json`（查看`aiCost`字段）
5. 任务结束时：`cs end -n "修复了认证漏洞，添加了测试用例" --json`
6. 查看历史会话：`cs dashboard`

**提示：** 使用`--agent`参数可明确记录具体代理的工作内容，尤其在多代理系统中非常有用（例如“代码审核机器人”、“测试编写器”、“文档生成机器人”等）。

## 定价

定价设置可自定义。运行`cs pricing list`查看所有可用模型及其价格。如需修改模型价格：

```bash
# 使用模型名称：
cs pricing set my-model 5.00 15.00

# 使用提供商名称（避免名称冲突）：
cs pricing set gpt-4o 2.50 10.00 --provider openai
```

如果模型未在定价表中，需手动指定成本（格式：`-c <成本>`）。

## 预算监控

- 如果用户设置了预算或检测到高费用支出：
  - 在执行高成本操作前，使用`cs status --json`检查预算。
  - 如果单次会话的费用超过5美元，及时提醒用户。
  - 如果费用持续上升，建议更换成本较低的模型。

## 重要提示

- 使用`--close-stale`选项可避免因系统崩溃导致的会话状态异常。
- 如果未安装`codesession-cli`，请勿强制进行会话跟踪，以免影响用户任务。
- **所有命令均需使用`--json`选项**，以确保输出数据具有结构化格式。
- 使用`--json`时，`cs start`会立即创建会话并结束程序。
- 会话范围基于`git root`目录，即使从子目录运行，也会关联到整个仓库的会话记录。
- 在`--json`模式下发生错误时，退出代码为1，响应内容为`{"error": {"code": "...", "message": "..."}`。
- 通过检查JSON响应中的`schemaVersion`字段可检测数据结构变更。

## 更新检查

定期检查CLI是否为最新版本（例如在会话开始时或每天一次）：

```bash
# 检查安装版本与npm上的最新版本：
cs --version          # 安装版本
npm view codesession-cli version  # npm上的最新版本
```

如果发现版本过低，通知用户：
> “codesession-cli已更新至v2.0.0，请运行`npm install -g codesession-cli`进行升级。”

更新过程中请勿中断用户的工作流程，只需及时通知用户即可。

## JSON输出格式

所有命令均支持`--json`选项，以生成机器可读的JSON格式输出。这有助于程序化处理会话数据。