---
name: claw-agent-creator-archit
description: >
  Create new OpenClaw agents for Arch's multi-agent system. Use this skill when asked to
  create, add, or set up a new OpenClaw agent, or when adding an agent to the system defined
  in ~/.openclaw/. Covers the full lifecycle: directory creation, workspace files (SOUL.md,
  IDENTITY.md, etc.), openclaw.json config, Telegram routing (bindings + groups + mention
  patterns), cron job creation with proper prompt engineering, and gateway restart. Includes
  hard-won lessons from building the Wire (News) agent — the first non-default agent in the
  system. Also use when modifying existing agent configs, adding cron jobs to agents, or
  debugging agent routing issues.
---

# OpenClaw 代理创建器

在 `~/.openclaw/` 目录下创建并配置 OpenClaw 多代理系统的代理。

## 系统环境

- **所有者**: Archit（Arch 用户），Linux 用户名 `archit`，时区为 America/Denver
- **网关**: 运行在端口 18789 的单个进程，负责管理所有代理
- **机器人**: 一个在所有代理之间共享的 Telegram 机器人——路由机制决定了哪个代理处理哪些聊天消息
- **现有代理**: 查看 `~/.openclaw/openclaw.json` 文件中的 `agents.list[]` 以获取当前代理列表
- **实现历史**: 有关 Wire 代理的实现细节，请参阅 `~/.openclaw/implementation-docs/` 目录

## 代理创建流程

### 1. 收集需求

在创建代理之前，与 Arch 进行沟通，明确以下内容：
- 代理的名称和 ID（使用小写字母，ID 中不能包含空格）
- 代理的角色和职责（具体明确）
- 代理使用的模型层级：基础模型（仅限 Kimi K2.5）或完整级联模型（包括 Claude Sonnet）
- 是否需要用于问答的 Telegram 群组
- 是否需要设置 cron 任务（任务内容、执行时间表）
- 是否需要启用心跳检测功能

### 2. 停止网关服务

```bash
openclaw gateway stop
```

**在编辑 `openclaw.json` 或 `cron/jobs.json` 之前必须执行此操作**。网关会在每次 cron 任务执行后更新 `jobs.json` 文件中的任务状态。在网关运行时进行编辑可能会导致数据丢失或系统故障。

### 3. 备份配置文件

```bash
cp ~/.openclaw/openclaw.json ~/.openclaw/openclaw.json.backup.$(date +%Y%m%d%H%M%S)
```

### 4. 创建目录结构

```bash
mkdir -p ~/.openclaw/workspace-<agent_id>/memory
mkdir -p ~/.openclaw/agents/<agent_id>/agent
```

**切勿** 在多个代理之间重复使用 `agentDir` 目录——这可能导致认证或会话冲突。

### 5. 编写工作空间配置文件

使用 `assets/templates/` 目录中的模板作为起点。每个代理都需要以下文件：
| 文件 | 用途 | 是否必需 |
|------|---------|----------|
| `SOUL.md` | 代理的个性、角色、职责及行为模式 | 是 |
| `IDENTITY.md` | 代理的快速参考信息（名称、角色、表情符号） | 是 |
| `USER.md` | 关于 Arch 的信息（可复制自现有代理的工作空间文件） | 是 |
| `AGENTS.md` | 代理的工作空间规则（启动顺序、内存使用、安全设置） | 是 |
| `HEARTBEAT.md` | 定期任务清单（如果禁用了心跳检测功能，则无需此文件） | 是 |

`SOUL.md` 是最重要的文件。请详细说明代理的职责，并在代理在不同场景下的行为模式（如简报模式和聊天模式）进行相应配置。

### 6. 编辑 `openclaw.json` 文件——添加代理信息

将代理信息添加到 `agents.list[]` 列表中。有关所有有效字段的详细信息，请参阅 [references/config-schema.md](references/config-schema.md)。

**最小化代理配置示例：**
```json
{
  "id": "<agent_id>",
  "name": "<Display Name>",
  "workspace": "/home/archit/.openclaw/workspace-<agent_id>",
  "agentDir": "/home/archit/.openclaw/agents/<agent_id>/agent",
  "identity": { "name": "<Display Name>" }
}
```

**常见配置项：**
- `"model"`：覆盖默认的模型层级。工作代理应使用成本较低的模型。
- `"heartbeat": { "every": "0" }`：禁用仅用于 cron 任务的代理的心跳检测功能。
- `"groupChat": { "mentionPatterns": ["@<id>", "@<Name>"] }`：允许在群组中使用 @ 提到功能。

**只能有一个代理的 `default` 属性设置为 `true`（当前为 Fossil）。默认代理会接收所有未被路由到的消息。**

### 7. 编辑 `openclaw.json` 文件——配置 Telegram 路由（如需）

**需要修改三个配置项**。缺少任何一个配置项都可能导致代理无法正常工作。有关详细说明，请参阅 [references/telegram-routing.md](references/telegram-routing.md)。

1. 在 `channelsTelegram.groups` 中配置群组路由：
   ```json
   "-100XXXXXXXXXX": { "requireMention": false }
   ```

2. 在 `bindings[]` 中配置代理与 Telegram 机器人的绑定关系：
   ```json
   { "agentId": "<id>", "match": { "channel": "telegram", "peer": { "kind": "group", "id": "-100XXXXXXXXXX" } } }
   ```

3. 在代理配置中设置提及模式（如果步骤 6 中已配置了 `groupChat`，则此步骤可以跳过）。

### 8. 创建 cron 任务（如需）

编辑 `cron/jobs.json` 文件。每个 cron 任务的提示信息必须包含以下内容：
- **动态的群组 ID 解析逻辑**（切勿硬编码 Telegram 群组 ID）：
  ```
  FIRST: Resolve your Telegram group ID by running:
  jq -r '.bindings[] | select(.agentId == "<agent_id>") | .match.peer.id' ~/.openclaw/openclaw.json
  Use the output as the target for all Telegram messages in this task.
  ```
- **日期格式**: `$(date '+%A, %B %d, %Y')`，用于生成消息的时间戳
- **其他约束条件**: 来源允许列表、消息新鲜度规则、格式模板
- **发送指令**: 使用 `target '<AGENT_GROUP_ID>'` 作为占位符（该占位符会根据群组 ID 动态生成）

这种自修复机制可确保 cron 任务在 Telegram 群组 ID 更改时仍能正常运行。有关完整提示格式的示例，请参阅 [references/prompt-patterns.md](references/prompt-patterns.md)，以及相关原理说明，请参阅 [references/telegram-routing.md](references/telegram-routing.md)。

**重要提示**：如果从其他代理的工作空间复制文件或提示信息，请使用 `grep` 命令查找硬编码的路径，并进行更新。

### 9. 重启网关服务并验证配置

```bash
openclaw gateway start
```

通过日志验证配置是否正确：
- 代理是否已成功注册：`agent registered: <id>`
- 消息是否被正确路由：`lane enqueue: lane-session:agent:<id>:...`

如果发送到 Telegram 群组的消息显示 `skip: no-mention`，则说明 `channelsTelegram.groups` 配置有误（请参阅 [references/bugs-and-pitfalls.md](references/bugs-and-pitfalls.md)）。

## 参考文件

| 文件 | 阅读时机 |
|------|-------------|
| [references/config-schema.md](references/config-schema.md) | 在编写代理配置或 cron 任务时 |
| [references/telegram-routing.md](references/telegram-routing.md) | 在配置 Telegram 群组路由时 |
| [references/prompt-patterns.md](references/prompt-patterns.md) | 在编写 cron 任务提示信息时 |
| [references/bugs-and-pitfalls.md](references/bugs-and-pitfalls.md) | 在调试问题或修改配置之前 |

## 模板文件

工作空间文件的起始模板位于 `assets/templates/` 目录中。请根据需要复制并自定义这些模板。