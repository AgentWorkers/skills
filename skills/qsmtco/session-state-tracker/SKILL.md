---
name: session-state-tracker
description: 通过生命周期钩子，在数据压缩和系统重启过程中实现会话状态的持久化管理
version: 2.0.0
author: qsmtco
license: MIT
homepage: https://github.com/qsmtco/qrusher/tree/main/skills/session-state-tracker
metadata:
  openclaw:
    requires:
      bins:
        - node
      env: []
    emoji: "🔄"
---
## 外部端点

此技能不调用任何外部端点。所有操作都在工作区内完成。

## 安全性与隐私

- **完全本地化操作**：无需网络访问；所有状态都存储在工作区内的 `SESSION_STATE.md` 文件中。
- **文件范围**：该技能仅读取和写入工作区根目录下的 `SESSION_STATE.md` 文件，不会访问其他文件。
- **会话发现**：`session_state_discover` 工具使用 `memory_search` 功能来查询索引化的会话记录。该功能受 OpenClaw 的 `memorySearch` 配置（本地向量数据库）控制；技能本身不会发起任何外部 API 调用。
- **无数据泄露**：除非您单独配置了外部存储后端，否则数据不会离开您的机器。

## 模型调用说明

该技能注册了三个生命周期钩子：
- `pre-compaction`：在压缩操作之前自动运行，用于持久化状态。
- `post-compaction`：在压缩操作之后自动运行，用于插入状态提示信息。
- `session-start`：在会话开始时自动运行，用于加载最新状态。

这些钩子由 OpenClaw 的核心系统触发，无需人工干预。`session_state_read`、`session_state_write`、`session_state_discover` 等工具可在需要时手动使用。

## 信任声明

使用此技能后，所有状态管理都保持本地化且透明。代码为开源，仅依赖于您的 `SESSION_STATE.md` 文件。只有在您信任作者并理解这些钩子的工作原理的情况下，才建议安装该技能。

---

## 概述

“会话状态跟踪器”通过生命周期钩子，在 OpenClaw 会话压缩和重启过程中自动持久化并恢复工作状态，从而避免上下文丢失。

### 主要特性

- **自动状态持久化**：通过 OpenClaw 的钩子实现（压缩过程中无需手动操作）。
- **结构规范化的状态文件**（`SESSION_STATE.md`），包含 YAML 标头信息。
- **原子性写入**：确保数据不会损坏。
- **发现工具**：在需要时可以从会话记录中重建状态。
- **命令行界面（CLI）**：用于手动检查和更新状态。
- **无外部依赖**：仅依赖 Node.js 和 `js-yaml`。

---

## 文件格式

`SESSION_STATE.md`（位于工作区根目录）：

```markdown
---
project: "my-project"
task: "Describe current task"
status: "active"          # active | blocked | done | in-progress
last_action: "Latest update"
next_steps:
  - "Step 1"
  - "Step 2"
updated: "2026-02-14T23:20:00.000Z"
---

## Context
Optional freeform notes, constraints, links, etc.
```

除 `body`（上下文部分）外，所有标头字段都是必需的。时间戳必须符合 ISO 8601 格式。

---

## 安装方法

```bash
clawhub install qsmtco/session-state-tracker
```

或者将技能文件夹复制到 `skills/session-state-tracker/` 目录中，并在 `openclaw.json` 文件中启用该技能：

```json
"skills": { "entries": { "session-state-tracker": { "enabled": true } } }
```

然后重启 OpenClaw 服务器。

---

## 配置说明

该技能默认启用钩子功能。为了使 `session_state_discover` 能够正常工作，请确保会话记录的索引功能处于启用状态：

```json
"agents": {
  "defaults": {
    "memorySearch": {
      "sources": ["memory", "sessions"],
      "experimental": { "sessionMemory": true }
    }
  }
}
```

无需其他额外配置。

---

## 相关工具

- `session_state_read`：读取当前状态（包括标头信息和主体内容）。
- `session_state_write`：更新状态信息（自动添加时间戳并验证数据结构）。
- `session_state_discover`：从最近的会话记录中合成状态并写入文件。

---

## 命令行界面（CLI）

```bash
# Show state
session-state show

# Update a field
session-state set task "New task"
session-state set next_steps '["A","B"]'

# Refresh from session transcripts (requires memory_search)
session-state refresh

# Clear state
session-state clear
```

---

## 工作原理

1. **会话开始**：`session-start` 钩子会读取 `SESSION_STATE.md` 文件；如果文件存在且内容更新（距离上次读取时间不超过 24 小时），则会将状态摘要插入到系统上下文中。
2. **工作过程中**：您可以调用 `session_state_write` 来记录进度。该文件是所有状态信息的唯一来源。
3. **压缩前**：`pre-compaction` 钩子会自动保存当前状态（必要时会通过 `memory_search` 功能进行索引）。
4. **压缩后**：`post-compaction` 钩子会插入一个状态提示信息，以便代理能够立即识别当前状态。
5. **重启**：整个流程会重复执行，状态会在重启后得以保留。

---

## 从 v1.x 升级到 v2.0.0

v2.0.0 版本引入了生命周期钩子机制。`SESSION_STATE.md` 的格式保持不变。升级步骤如下：
- 安装 v2.0.0 或更高版本。
- 确保该技能已被启用。
- 新的钩子机制取代了旧的 `memoryFlush.prompt` 机制；您可以从配置中移除任何自定义提示信息。
- 现有的 `SESSION_STATE.md` 文件可以继续正常使用，无需修改。

---

## 故障排除

- 钩子未触发？请检查该技能是否已启用以及 `openclaw.plugin.json` 文件是否存在。安装完成后重启 OpenClaw 服务器。
- `session_state_discover` 返回空结果？请启用会话记录的索引功能（`memorySearchexperimental.sessionMemory = true`），并确认最近的有用会话记录存在。
- 状态文件未更新？请检查文件权限；该技能会以原子方式将数据写入工作区根目录下的 `SESSION_STATE.md` 文件。

---

**简单、可靠且自动化。**