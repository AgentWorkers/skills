# 会话状态跟踪器技能

**版本：** 1.0.0  
**作者：** qsmtco  
**许可证：** MIT

---

## 概述

会话状态跟踪器解决了在 OpenClaw 会话压缩和重启过程中上下文丢失的问题。它提供了一个持久的 `SESSION_STATE.md` 文件，可以随时查看您当前的项目、任务、状态以及下一步操作。

### 主要特性

- **手动或自动状态维护** – 代理可以在取得显著进展后更新 `SESSION_STATE.md`  
- **可选集成**：支持预压缩前的数据清除和会话记录索引，以实现无缝操作  
- **命令行工具**：用于手动检查和更新状态  
- **无需外部网络访问** – 完全在工作区内运行

---

## 问题描述

OpenClaw 会自动压缩长时间运行的会话，以保持在模型上下文窗口内。压缩过程会汇总旧消息并将其从活动上下文中移除，从而导致对话连贯性的丢失：

- 代理会忘记当前的任务和下一步操作  
- 用户需要反复解释他们正在做什么  
- 长时间运行的项目会变得碎片化  

现有的机制（如 `MEMORY.md`、每日日志）用于长期存储数据，而非用于存储*当前的工作上下文*。我们需要一个轻量级的、始终存在的“锚点”，以便在压缩后仍能访问相关信息。

---

## 解决方案架构

该解决方案围绕一个简单的文件（`SESSION_STATE.md`）和可选的 OpenClaw 功能构建：

1. **`SESSION_STATE.md`** – 一个包含 YAML 前言的小型 Markdown 文件，用于存储当前状态  
2. **可选：预压缩前的数据清除自定义** – 指示代理在压缩前验证/更新状态文件  
3. **可选：会话记录索引** (`memorySearchexperimental.sessionMemory = true`) – 使 `memory_search` 能够从压缩后的消息中检索原始内容  

该技能本身提供了用于读取、写入和查询状态的工具。这些工具的使用方式（自动或手动）由代理的配置文件（如 `AGENTS.md`）和用户的设置决定。

---

## 文件格式

`SESSION_STATE.md` 位于工作区根目录下：

```markdown
---
project: "session-state-tracker"
task: "Implement skill with read/write/discover tools"
status: "active"          # active | blocked | done
last_action: "Designed revised architecture"
next_steps:
  - "Create skill skeleton"
  - "Implement state.js"
  - "Write CLI"
updated: "2026-02-14T23:20:00Z"
---

## Context
- Brief freeform notes, constraints, links, etc.
```

所有前言字段都是字符串、数组、布尔值或数字。`Context` 部分用于人类阅读的注释，但不会被程序使用。

---

## 实现步骤

本部分介绍了如何在您的 OpenClaw 安装中设置会话状态跟踪器系统。**该技能本身是自包含的；以下步骤是可选的配置选项，用于增强自动化功能。**

### 1. 安装该技能

将 `skills/session-state-tracker/` 目录复制到您的工作区，或通过 ClawHub 安装：

```bash
clawhub install qsmtco/session-state-tracker
```

该技能提供了三个工具：  
- `session_state_read` – 读取状态文件  
- `session_state_write` – 更新字段（自动添加时间戳）  
- `session_state_discover` – 使用 `memory_search` 从会话记录中重建状态  

此外还有一个命令行工具 `session-state`（命令：`show`、`set`、`refresh`、`clear`）。  

**该技能本身不需要重启网关**（如果 `commands_nativeSkills = "auto"`，则会自动加载；否则需要重启网关）。

---

### 2. 可选：启用会话记录索引

**隐私影响：** 此设置会将您的对话记录索引到内存向量存储中，使得过去的信息可以通过 `memory_search` 进行搜索。这会增加内存系统的搜索范围。只有在您理解并接受这一影响的情况下才启用此功能。**

**为什么有用：** `session_state_discover` 工具依赖于 `memory_search` 来查找最近的任务提及。如果没有会话索引，该工具将返回空结果。**

**如何启用：**

修改您的 OpenClaw 配置文件（`~/.openclaw/openclaw.json` 或您个人资料中的 `openclaw.json`）：

```json5
{
  "agents": {
    "defaults": {
      "memorySearch": {
        "sources": ["memory", "sessions"],
        "experimental": { "sessionMemory": true },
        "sync": { "sessions": { "deltaBytes": 100000, "deltaMessages": 50 } }
      }
    }
  }
}
```

然后重启网关：

```bash
openclaw gateway restart
```

---

### 3. 可选：自定义预压缩前的提示信息

**原因：** 如果您希望在压缩前自动更新状态文件，可以自定义 `memoryFlush.prompt` 以提醒代理检查 `SESSION_STATE.md`。**

**如何设置：**

```json5
{
  "agents": {
    "defaults": {
      "compaction": {
        "memoryFlush": {
          "prompt": "Check SESSION_STATE.md. If your current task has changed, update the file. Then write any lasting notes to memory/YYYY-MM-DD.md. Reply with NO_REPLY if nothing to store."
        }
      }
    }
  }
}
```

应用设置后重启网关。

---

### 4. 使用 `AGENTS.md` 更新维护规则

在您的工作区 `AGENTS.md` 中添加以下内容。这**不属于** 该技能本身，而是代理行为的配置。

```markdown
## Session State Maintenance

`SESSION_STATE.md` is your working memory across compaction and restarts.

**Format:**
```markdown
---
project: ""
task: ""
status: "active|blocked|done"
last_action: ""
next_steps: []
updated: "ISO 时间戳"
---
## 上下文
- 笔记、约束条件、链接
```

**Rules:**

1. **At session start** (after reading `SOUL.md`, `USER.md`, `memory/`):
   - If `SESSION_STATE.md` exists and `updated` is within the last 24 hours, read it and keep its contents in mind.
   - If missing or older than 24 hours, use `memory_search(sources=["sessions"], query="project|task|working on")` to discover current focus, then write a fresh state file.

2. **After significant progress or a change in focus**:
   - Call `session_state_write` (or write manually) to update `SESSION_STATE.md`.
   - Always update the `updated` timestamp.

3. **When you see a `compaction` entry in the conversation**:
   - Read `SESSION_STATE.md` to refresh your memory of the current task before responding.
   - If the file feels out of date, run discovery (`session_state_discover`) and update it.

4. **During the pre-compaction flush** (if you customized the prompt):
   - Verify `SESSION_STATE.md` matches the current focus; update if needed.
   - Then write any lasting notes to `memory/YYYY-MM-DD.md`.
   - Respond with `NO_REPLY`.

5. **Never delete** `SESSION_STATE.md`. If obsolete, set `status: "done"` and create a new file for new work.
```

---

### 5. 创建初始状态

如果 `SESSION_STATE.md` 不存在，请使用您当前的项目创建它：

```bash
session-state set project "my-project"
session-state set task "Describe current task"
session-state set status "active"
session-state set last_action "Initialized state"
session-state set next_steps '["Step 1", "Step 2"]'
```

或者手动编辑该文件。

---

## 工作原理

### 正常操作（含可选配置）

1. 您开始一个会话。代理会首先读取 `SESSION_STATE.md`（如果文件存在）；否则会从会话记录中获取信息。  
2. 您开始执行任务。代理会在执行重要操作后更新状态文件（通过 `session_state_write` 或手动编辑）。  
3. 当接近压缩阈值时，如果启用了提示信息，代理会收到提示来检查/更新状态。  
4. 代理根据需要更新状态，并记录每日笔记，回复 `NO_REPLY`。  
5. 执行压缩：旧消息会被汇总并从上下文中移除。  
6. 当用户发送新消息时，对话中会包含一个表示“压缩完成”的标记。  
7. 根据 `AGENTS.md` 中的规则，代理会再次读取 `SESSION_STATE.md` 以重新确定当前状态。  
8. 对话会以状态文件作为基准继续进行。

### 无可选配置（手动模式）

如果您未启用会话索引或自定义数据清除功能，仍可以手动运行 `session-state refresh`（当怀疑状态过时时）或直接编辑 `SESSION_STATE.md`。代理仍会按照 `AGENTS.md` 中的规则在会话开始时和压缩后读取该文件（无论配置如何，代理都需要养成读取该文件的习惯）。

---

## 工具定义

### `session_state_read`

读取 `SESSION_STATE.md` 并返回**所有前言字段以及 `body`（即 `Context` 部分）**。

**输入：** 无  
**输出：**
```json
{
  "project": "session-state-tracker",
  "task": "Implement skill",
  "status": "active",
  "last_action": "Designed architecture",
  "next_steps": ["Create skeleton", "Implement state.js"],
  "updated": "2026-02-14T23:20:00Z",
  "body": "Notes about constraints, links, etc."
}
```

### `session_state_write`

更新 `SESSION_STATE.md` 中的一个或多个字段。除非特别指定，否则会自动将 `updated` 字段设置为当前 ISO 时间戳。  

**输入：** 部分对象，例如：`{"task": "New task", "status": "active"}`  
**输出：** `{"success": true, "fields": ["task", "status"], "updated": "2026-02-14T23:25:00Z"}`  

### `session_state_discover`

使用 `memory_search`（源设置为 `["sessions"]`）从最近的对话片段中合成新的状态，并自动将结果写入 `SESSION_STATE.md`。  

**输入：** 可选参数 `{ query, limit, minScore }`  
**输出：** 类似于 `session_state_read` 的状态对象，但包含 `_meta` 字段，用于显示片段数量和主要来源。  

**注意：** 需要 `memory_search` 工具可用，并且必须启用会话记录索引才能获得有效结果。

---

## 命令行工具

该技能会安装一个名为 `session-state` 的二进制文件：

```bash
# Show current state (including Context)
session-state show

# Update a single field (string; for arrays use JSON format)
session-state set task "Refine discovery algorithm"
session-state set next_steps '["Step A","Step B"]'

# Refresh state from session transcripts (calls discover)
session-state refresh

# Clear state (sets all fields empty)
session-state clear
```

**注意：** 使用 `session-state refresh` 时，需要确保 `memory_search` 工具在运行环境中可用（通过 OpenClaw 的 `exec` 命令执行时，该工具会被自动加载；如果在 shell 中手动执行，则可能需要手动配置环境。）

---

## 依赖项与要求

- OpenClaw >= 2026.2.0（以确保工具的稳定性和 `memory_search` 的可用性）  
- Node.js 18+  
- **可选：** 启用会话记录索引（`memorySearchexperimental.sessionMemory = true`）以支持状态查询  
- **可选：** 自定义 `memoryFlush.prompt` 以实现自动预压缩前的数据清除  

技能运行时的依赖项：  
- `js-yaml`（用于解析 YAML 文件）

---

## 安全性与隐私考虑

- **文件范围：** 该技能仅读取和写入工作区根目录下的 `SESSION_STATE.md`，不会访问工作区外的文件。  
- **网络：** 该技能本身不会进行网络调用。`session_state_discover` 使用 `memory_search` 工具，该工具可能会根据您的 OpenClaw 配置使用远程嵌入 API。具体取决于您的内存提供者设置。  
- **权限：** 该技能以代理的标准文件 I/O 权限运行，不会请求提升的权限（如 `exec`、`node` 或沙箱逃逸）。  
- **持久性：** 状态信息保存在一个普通的 Markdown 文件中，您可以通过 Git 或其他方式备份。  
- **配置更改：** 推荐的配置选项（会话索引、数据清除提示）是**可选的**，并且会影响**网关上的所有代理**。在应用这些配置之前，请仔细考虑隐私影响：  
  - 会话索引会增加存储在内存向量数据库中的数据量（包括完整的对话片段）。  
  - 数据清除提示功能虽然无害，但会触发一次预压缩操作。  
- **用户控制：** 您可以选择在纯手动模式下使用该技能，无需进行任何配置更改。只需直接编辑 `SESSION_STATE.md`，并根据需要使用命令行工具即可。

---

## 故障排除

| 症状 | 可能原因 | 解决方法 |
|---------|--------------|-----|
| `session-state refresh` 失败，提示“memory_search 不可用” | 未启用会话索引或在 OpenClaw 的执行环境中之外运行 | 在配置中启用 `memorySearchexperimental.sessionMemory`，或通过 `openclaw exec` 运行该技能 |
| 压缩后状态文件未被读取 | `AGENTS.md` 中的规则缺失或过时 | 确保包含“会话状态维护”部分，并包含规则 #3 |
| YAML 解析错误 | 前言格式错误（例如缺少冒号、缩进不正确） | 使用 YAML 验证工具；保持值简单（标量、JSON 数组） |
| `readState` 返回空值 | 文件缺失或为空 | 创建至少包含前言字段的初始 `SESSION_STATE.md` 文件 |

---

## 设计理念

- **使用普通文件而非数据库**：便于人类阅读，支持 Git 操作，无需额外基础设施。  
- **依赖项最少**：仅依赖 `js-yaml` 进行可靠的 YAML 解析。  
- **通过 `AGENTS.md` 规则控制代理行为**：尊重 OpenClaw 的架构，由代理决定何时读取/写入文件。  
- **与现有功能兼容**：无需更改网关的默认设置；即使没有会话索引也能正常使用。  

---

## 未来改进计划

- 在写入时验证状态格式（确保包含所有必需字段）  
- 添加 `session_state validate` 命令  
- 支持每个项目多个状态文件（子目录）  
- 集成心跳检测机制以标记过时的状态  

---

**这就是完整的技能说明。** 所有配置步骤都明确标注为可选，并附有隐私提示。该技能的权限要求较低，仅操作状态文件。