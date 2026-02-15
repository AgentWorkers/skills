---
name: codecast
description: 通过 Webhook 将 Stream 编码代理会话（如 Claude Code、Codex、Gemini CLI 等）实时传输到 Discord 频道。适用于在调用编码代理时，需要实现透明且可观察的开发会话场景——避免出现“黑箱”现象。该工具能够将 Claude Code 生成的 stream-json 数据解析为格式规范的 Discord 消息，这些消息会显示工具调用、文件操作、bash 命令及其执行结果，且不会消耗任何 AI 令牌。适用于需要“将会话流式传输到 Discord”、“中继代理输出”或“使开发会话可见”的场景。
---

# Codecast

将实时编码会话直播到 Discord 平台。所有工具调用、文件写入操作以及 Bash 命令都会被实时显示，没有任何隐藏的部分，也不会消耗任何 AI 令牌。

## 工作原理

```
┌──────────┐  stream-json  ┌──────────────┐  platform  ┌──────────┐
│ Claude   │ ────────────→ │ parse-stream │ ────────→ │ Discord  │
│ Code -p  │               │ .py          │           │ #channel │
└──────────┘               └──────────────┘           └──────────┘
```

- Claude Code 以 `-p`（打印）模式运行，并使用 `--output-format stream-json --verbose` 选项进行输出。
- `parse-stream.py` 读取 JSON 格式的输入数据，并通过平台适配器发送格式化后的消息。
- 平台适配器（目前为 Discord）负责处理消息的发送和线程管理。
- `unbuffer`（来自 `expect` 库）用于防止标准输出（stdout）被缓冲。
- 非 Claude 类型的代理会使用未经格式化的原始输出数据进行传输。
- 通过设置每 60 秒最多发送 25 条消息的速率限制，可以有效避免 Webhook 被过度使用。

## 首次设置

安装该插件后，请按照以下步骤操作：

### 1. 使脚本可执行

```bash
chmod +x <skill-dir>/scripts/dev-relay.sh <skill-dir>/scripts/parse-stream.py
```

### 2. 创建 Discord Webhook

在目标 Discord 频道中，通过 Discord API 或服务器设置 → 集成 → Webhook 功能来创建一个 Webhook。

如果机器人具有 `MANAGE_WEBHOOKS` 权限，可以通过 API 创建 Webhook：
```bash
curl -s -X POST "https://discord.com/api/v10/channels/<CHANNEL_ID>/webhooks" \
  -H "Authorization: Bot <BOT_TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{"name":"Codecast"}'
```

保存 Webhook 的 URL：
```bash
echo "https://discord.com/api/webhooks/<ID>/<TOKEN>" > <skill-dir>/scripts/.webhook-url
chmod 600 <skill-dir>/scripts/.webhook-url
```

### 3. （仅适用于 Claude Code）跳过权限确认步骤

如果 `~/.claude/settings.json` 文件不存在，请创建该文件：
```json
{
  "permissions": {
    "defaultMode": "bypassPermissions",
    "allow": ["*"]
  }
}
```

### 4. 安装 `unbuffer` 库

```bash
brew install expect    # macOS
apt install expect     # Linux
```

## 使用方法

安装完成后，需要对相关脚本执行 `chmod +x` 命令使其可执行：
```bash
chmod +x <skill-dir>/scripts/dev-relay.sh <skill-dir>/scripts/parse-stream.py
```

### 使用 OpenClaw 的方法（推荐）

```bash
exec background:true command:"<skill-dir>/scripts/dev-relay.sh -w ~/projects/myapp -- claude -p --dangerously-skip-permissions --output-format stream-json --verbose 'Build a REST API for todos'"
```

### 直接使用方法

```bash
bash <skill-dir>/scripts/dev-relay.sh -w ~/projects/myapp -- claude -p --dangerously-skip-permissions --output-format stream-json --verbose 'Build auth module'
```

### 参数说明

| 参数 | 说明 | 默认值 |
|------|------------|---------|
| `-w <dir>` | 工作目录 | 当前目录 |
| `-t <sec>` | 超时时间 | 1800 秒（30 分钟） |
| `-h <sec>` | 挂起阈值 | 120 秒 |
| `-i <sec>` | 发送间隔 | 10 秒 |
| `-n <name>` | 代理显示名称 | 自动检测 |
| `-P <platform>` | 聊天平台 | discord |
| `--thread` | 将消息发送到特定 Discord 线程 | 关闭 |
| `--skip-reads` | 隐藏读取工具相关的事件 | 关闭 |
| `--resume <dir>` | 从指定目录重新播放会话记录 | 不适用 |

### 线程模式

将所有消息发送到同一个 Discord 线程中，以保持频道记录的整洁：
```bash
bash <skill-dir>/scripts/dev-relay.sh --thread -w ~/projects/myapp -- claude -p --dangerously-skip-permissions --output-format stream-json --verbose 'Refactor auth'
```

### 会话重播

可以重新播放之前的会话内容（例如，转移到另一个频道或在新 Webhook 设置生效后）：
```bash
bash <skill-dir>/scripts/dev-relay.sh --resume /tmp/dev-relay.XXXXXX
```

会话开始时，会显示代理的传输目录路径（例如：`📂 Relay: /tmp/dev-relay.XXXXXX`）。

## Discord 上显示的内容

对于 Claude Code（使用 stream-json 格式输出）：
- ⚙️ 模型信息及权限状态
- 📝 文件写入操作（包含行数和内容预览）
- ✏️ 文件编辑记录
- 🖥️ Bash 命令
- 📤 Bash 命令的输出结果（截断为 800 个字符）
- 👁️ 文件读取操作（通过 `--skip-reads` 选项可隐藏）
- 🔍 网页搜索结果
- 💬 助手发送的消息
- ✅/❌ 完成提示（包括轮次、耗时、成本和会话统计信息）

对于其他类型的代理（使用原始输出格式）：
- 输出内容以代码块的形式显示，并进行 ANSI 格式的转换
- 提供挂起检测警告
- 显示完成状态或错误信息

### 会话总结

每个会话结束时，会显示以下总结信息：
- 创建和编辑的文件列表及其数量
- 执行的 Bash 命令
- 各工具的使用情况
- 总消耗成本

## 架构概述

```
scripts/
├── dev-relay.sh          # Shell entry point, flag parsing, process management
├── parse-stream.py       # JSON stream parser, rate limiter, event loop
├── .webhook-url          # Discord webhook URL (gitignored)
└── platforms/
    ├── __init__.py       # Platform adapter loader
    └── discord.py        # Discord webhook + thread support
```

## 支持的代理类型

| 代理类型 | 输出格式 | 支持情况 |
|-------|------------|--------|
| Claude Code | stream-json（解析后的格式） | 完全支持 |
| Codex | 原始 ANSI 格式 | 基本支持 |
| Gemini CLI | 原始 ANSI 格式 | 基本支持 |
| 其他 CLI 工具 | 原始 ANSI 格式 | 基本支持 |

## 交互式输入

在会话进行中，可以通过以下方式将用户输入传递给代理：
- 使用 OpenClaw 时：`process:submitsessionId:<id> data:"your message"`
- 会话相关信息会存储在 `/tmp/dev-relay-session.json` 文件中。

## 完成通知

会话结束后，代理会立即调用 `openclaw gateway wake` 命令来通知 OpenClaw。