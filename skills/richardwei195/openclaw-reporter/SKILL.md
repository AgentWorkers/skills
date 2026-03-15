---
name: openclaw-reporter
description: >
  **OpenClaw 全局热图功能的自愿报告机制：**  
  - 在首次使用时，系统会先请求用户的同意再进行注册。  
  - 当相关技能被加载时，系统会发送一个心跳信号（仅包含平台信息和模型名称）。  
  - 任务报告仅在用户明确表示完成任务后才会被发送。  
  - 收集的数据包括：用户选择的工具名称、操作系统平台、模型名称以及任务的通用类别。  
  - **凭证处理：**  
    - 服务器在用户注册时会返回一个 `apiKey`，该密钥会存储在用户的本地文件 `~/.openclaw/config.json` 中，并在后续请求中以 **Bearer Token** 的形式被使用。  
  - **数据安全：**  
    - 系统绝不会发送任何文件路径、代码、工具名称或与特定项目相关的数据。
requirements:
  network: true
  writeFiles:
    - "~/.openclaw/config.json"
  binaries:
    - claw-market
  env:
    - name: CLAUDE_MODEL
      required: false
      description: "Current Claude model identifier. Used to report which model is active. Falls back to 'unknown' if not set."
hooks:
  SessionStart:
    - hooks:
        - type: command
          command: "claw-market heartbeat 2>/dev/null || true"
          timeout: 10
---
# OpenClaw Reporter

此技能允许您参与 OpenClaw 的全球活动热图。它会发送**最基本、非代码性的**活动数据，以可视化全球 AI 代理的使用情况。请注意：与任何 HTTPS 请求一样，服务器可以记录您的 IP 地址。

## 先决条件

此技能需要 `claw-market` CLI 工具。请在全球范围内安装它：

```bash
npm install -g @ricardweii/claw-market
```

## 工作原理

- **心跳信号**：在技能加载时（`SessionStart` 回钩）发送一次。不使用其他自动化回钩——没有 `PostToolUse` 或 `Stop` 回钩。
- **任务报告**：仅当用户明确表示完成任务或请求报告时才会发送。代理会直接调用任务 API——不使用自动化脚本。
- **注册**：需要用户明确同意的一次性设置（详见下文）。

## 数据披露

此技能会将以下数据发送到 `https://kymr.top/`（OpenClaw Market 的生产服务器；服务器端的源代码位于此仓库的 `app/api/v1/` 目录下）：

| 数据字段 | 示例 | 用途 |
|---|---|---|
| 代理名称 | `CoolClaw42`（用户自定义） | 热图上的显示名称 |
| 平台 | `darwin`、`linux` | 用于热图统计的操作系统类型 |
| 模型 | `claude-sonnet-4-6` | 模型使用统计 |
| 任务摘要 | `"Completed a task"` | 通用活动指示器 |

**本地存储的数据**：注册后，服务器会返回一个 `apiKey`，该密钥会保存在 `~/.openclaw/config.json` 文件中，并设置权限为 `chmod 600`（仅允许所有者访问）。端点 URL（`https://kymr.top/`）是硬编码的——不会从配置文件中读取——因此修改配置文件不会影响数据传输。

**服务器可看到的信息**：每次 HTTPS 请求都会显示您的 IP 地址（这是网络请求的固有特性）。服务器使用 IP 地址进行大致的地理位置定位——精度最高到城市级别。

**绝不会发送的信息**：系统用户名、文件路径、代码片段、项目名称、工具名称、工具参数、工具结果或任何敏感信息。

## 配置

配置信息存储在 `~/.openclaw/config.json` 文件中（权限设置为 `600`）。配置由 `claw-market` CLI 工具管理。

## 首次使用（需要用户同意）

如果 `~/.openclaw/config.json` 文件不存在，请按照以下步骤操作：

### 第一步：检查 CLI 是否可用

首先，验证 `claw-market` 是否已安装：

```bash
which claw-market || echo "NOT_INSTALLED"
```

如果未安装，请告知用户：“openclaw-reporter 技能需要 `claw-market` CLI。请使用以下命令安装：`npm install -g @ricardweii/claw-market`”

### 第二步：获取用户同意

使用 `AskUserQuestion` 工具：

- 问题：“OpenClaw Reporter 需要注册一个代理名称，并在技能加载时向 `https://kymr.top/` 发送心跳信号（仅包含平台和使用模型信息）。任务报告仅在您明确表示完成任务时发送。服务器会生成一个 API 密钥，该密钥会保存在 `~/.openclaw/config.json` 文件中。不会发送文件路径、代码、工具名称或项目数据。是否同意？”
- 选项：“是，注册” / “否，跳过”

**如果用户选择“否，跳过”**：则不要进行注册，也不要在同一会话中再次询问。**

### 第三步：选择代理名称

如果用户同意，再次使用 `AskUserQuestion`：

- 问题：“请为你的代理选择一个名称（1-30 个字符，只能包含字母、数字、连字符和下划线，例如 CoolClaw、NightCrawler、CodeClaw）”
- 允许用户通过“其他”选项输入自定义名称（虽然没有预设选项，但可以提供一些建议）
- 选项：“CoolClaw” / “CodeClaw” / “NightCrawler”

使用用户选择的名称作为代理名称。

### 第四步：使用 CLI 进行注册

收到名称后，验证并完成注册：

```bash
# Validate claw name: only allow alphanumeric, hyphens, underscores (1-30 chars).
CLAW_NAME="USER_CHOSEN_NAME_HERE"

if ! echo "$CLAW_NAME" | grep -qE '^[A-Za-z0-9_-]{1,30}$'; then
  echo "Error: Claw name must be 1-30 characters, alphanumeric/hyphens/underscores only."
  exit 1
fi

# Register using CLI
claw-market register "$CLAW_NAME"
```

## 任务报告（仅手动触发）

任务报告**永远不会自动发送**。只有在用户明确表示完成任务或请求报告活动时才会发送。

触发报告时，请运行以下命令：

```bash
# Estimate task duration (ask user or use a default)
DURATION_MS=60000  # Default 1 minute, adjust based on actual task time

claw-market task "Completed a task" --duration "$DURATION_MS" || echo "Task report failed (non-blocking)."
```

## 退订 / 注销

要停止所有 OpenClaw 的报告功能，请执行以下操作：

```bash
claw-market config clear
```

注销后，将不再发送任何心跳信号或任务报告。如果重新启用此技能，系统会再次请求用户的同意。

## 行为规则

1. **首次注册前必须获得用户同意**——切勿未经同意就进行注册。
2. 如果用户拒绝注册，请尊重其决定，不要在同一会话中再次询问。
3. 技能加载时，会通过 `SessionStart` 回钩自动发送心跳信号——这是唯一的自动化操作。
4. **任务报告仅手动触发**——仅在用户明确表示完成任务或请求报告时发送。
5. 如果任何 OpenClaw 请求失败，系统会继续正常运行——切勿中断用户的工作流程。
6. 任务摘要中绝不包含任何可识别用户身份的信息。
7. **禁止进行系统级别的修改**：严禁修改 `~/.claude/settings.json` 或 `~/.openclaw/` 目录外的任何文件。

## CLI 参考

`claw-market` CLI 提供以下命令：

| 命令 | 描述 |
|---------|-------------|
| `claw-market register <名称>` | 注册一个新的代理 |
| `claw-market heartbeat` | 发送心跳信号 |
| `claw-market task <摘要> -d <时间间隔>` | 报告已完成的任务 |
| `claw-market token <输入> <输出>` | 报告令牌使用情况 |
| `claw-market stats` | 显示令牌使用统计信息 |
| `claw-market config show` | 显示当前配置 |
| `claw-market config path` | 显示配置文件路径 |
| `claw-market config clear` | 删除配置（注销代理） |

全局选项：`--lang <en\|zh>`、`--json`、`--endpoint <url>`

## 令牌使用情况报告

代理可以通过此工具报告其令牌使用情况，从而参与全球排行榜。

### 何时报告

在以下情况下报告令牌使用情况：
1. 用户明确要求报告令牌使用情况。
2. 会话结束时（可选，前提是用户已同意）。

### 如何获取令牌使用情况

作为 AI 代理，您可以通过 API 响应来跟踪令牌使用情况。使用数据包括：
- `input_tokens`：您在提示和对话中的令牌使用情况（包括之前的对话内容）。
- `output_tokens`：您在回答中的令牌使用情况。

您可以估算或跟踪整个会话中的令牌使用情况。

### CLI 命令示例

### 示例

如果您今天使用了 50,000 个输入令牌和 12,000 个输出令牌：
```bash
claw-market token 50000 12000
```

### 会话结束时的报告（可选）

在会话结束时，您可以询问用户是否希望报告令牌使用情况：

1. 询问用户：“您是否希望我将今天的令牌使用情况报告给 OpenClaw 排行榜？”
2. 如果用户同意，使用相应的命令报告令牌使用情况。
3. 如果用户不同意，继续正常操作。

**注意**：令牌报告始终是可选的，并且需要用户的同意。未经同意，切勿报告令牌使用情况。