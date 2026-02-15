---
name: mission-control
description: 专为AI助手设计的看板式任务管理仪表板。可通过命令行界面（CLI）或仪表板用户界面（UI）来管理任务。适用于用户需要提及任务、使用看板功能、管理任务板、执行任务控制，或希望跟踪带有状态列（待办、进行中、审核中、已完成）的工作项的情况。
homepage: https://github.com/rdsthomas/mission-control
metadata: {"clawdbot": {"emoji": "🎛️"}}
---

# 任务管理工具 — 专为AI助手设计

这是一个采用Kanban风格的任务管理面板，由您（AI助手）负责维护。人类用户通过Web仪表板创建和优先级排序任务，当任务状态变为“进行中”时，AI助手会自动执行这些任务。

## 🚀 快速入门

只需说出：“为我的工作空间设置Mission Control”。

系统将执行以下操作：
1. 检查必备依赖（Tailscale、gh CLI）
2. 将仪表板文件复制到您的工作空间
3. 创建配置文件（`~/.clawdbot/mission-control.json`）
4. 安装Webhook转换脚本
5. 设置GitHub Webhook
6. 将配置推送到GitHub并启用GitHub Pages

就这样，所有设置都完成了。后续的所有操作都由AI助手负责处理。

---

## 必备条件

在开始设置之前，请确保满足以下要求：

| 必备条件 | 检查内容 | 安装方法 |
|-------------|-------|---------|
| **Tailscale** | `tailscale status` | `brew install tailscale` 或 [访问官网下载](https://tailscale.com/download) |
| **Tailscale Funnel** | `tailscale funnel status` | `tailscale funnel 18789`（一次性操作） |
| **GitHub CLI** | `gh auth status` | `brew install gh && gh auth login` |

如果缺少任何依赖，请告知AI助手，它会指导您完成安装。

---

## 工作原理

1. **仪表板**：基于GitHub Pages提供的Web用户界面，用于人类用户管理任务。
2. **Webhook**：当任务状态发生变化时，GitHub会向Clawdbot发送推送事件。
3. **转换脚本**：比较旧版本与新版本的`tasks.json`文件，检测任务状态的变化。
4. **自动处理**：当任务状态变为“进行中”时，AI助手会立即开始执行相关任务。

### 动作流程

```
Human moves task → GitHub push → Webhook → Transform → Agent receives work order
      ↓                                                         ↓
   Dashboard                                              Executes task
      ↓                                                         ↓
Agent updates status ← Commits changes ← Marks subtasks done ←─┘
```

---

## 任务结构

任务数据存储在`<workspace>/data/tasks.json`文件中：

```json
{
  "id": "task_001",
  "title": "Implement feature X",
  "description": "Detailed context for the agent",
  "status": "backlog",
  "subtasks": [
    { "id": "sub_001", "title": "Research approach", "done": false },
    { "id": "sub_002", "title": "Write code", "done": false }
  ],
  "priority": "high",
  "dod": "Definition of Done - what success looks like",
  "comments": []
}
```

## 任务状态说明

| 状态 | 含义 |
|--------|---------|
| `permanent` | 循环任务（例如每日检查） |
| `backlog` | 等待处理的任务 |
| `in_progress` | **AI助手正在处理中** |
| `review` | 已完成，等待人类审核 |
| `done` | 已完成并获批准 |

---

## 命令行工具

使用`<skill>/scripts/mc-update.sh`命令来更新任务信息：

```bash
# Status changes
mc-update.sh status <task_id> review
mc-update.sh status <task_id> done

# Comments
mc-update.sh comment <task_id> "Progress update..."

# Subtasks
mc-update.sh subtask <task_id> sub_1 done

# Complete (moves to review + adds summary)
mc-update.sh complete <task_id> "Summary of what was done"

# Push to GitHub
mc-update.sh push "Commit message"
```

---

## AI助手的工作流程

当收到状态为“进行中”的任务时，AI助手会执行以下步骤：
1. **读取任务信息**：查看任务标题、描述以及子任务详情。
2. **标记任务开始**：执行`mc-update.sh start <task_id>`命令。
3. **执行任务**：处理所有子任务，并将每个子任务的完成状态更新为“已完成”。
4. **记录进度**：添加进度说明。
5. **完成任务**：执行`mc-update.sh complete <task_id> "Summary"`命令。

### 处理任务重新分配的情况

如果已完成的任务被重新标记为“进行中”并附有新的说明，AI助手会：
1. 阅读新的说明内容。
2. 解决相关问题。
3. 添加评论说明所做的修改。
4. 将任务状态重新设置为“审查中”。

---

## EPIC任务（大型项目）

EPIC任务是包含多个子任务的父任务。收到EPIC任务时：
1. 子任务会以`MC-XXX-001: 标题`的格式列出。
2. 按顺序处理每个子任务（例如：1 → 2 → 3...）。
3. 处理完每个子任务后，将其状态设置为“审查中”，并将对应的子任务标记为“已完成”。
4. 所有子任务处理完成后，将EPIC任务的状态设置为“审查中”。

---

## 心跳检测集成

请将相关配置添加到`HEARTBEAT.md`文件中：

```markdown
## Task Check

1. Check `data/tasks.json` for tasks in "in_progress"
2. Flag tasks with `processingStartedAt` but no recent activity
3. Check "review" tasks for new feedback comments
```

## 配置文件

配置信息保存在`~/.clawdbot/mission-control.json`文件中。详细配置选项请参考`assets/examples/CONFIG-REFERENCE.md`。

以下是AI助手在设置过程中默认使用的最小化配置：

```json
{
  "gateway": { "hookToken": "your-token" },
  "workspace": { "path": "/path/to/workspace" },
  "slack": { "botToken": "xoxb-...", "channel": "C0123456789" }
}
```

## 故障排除

如遇到问题，请参考`docs/TROUBLESHOOTING.md`：
- 仪表板显示空白数据？请确保已正确连接GitHub令牌。
- Webhook未触发？请检查Tailscale Funnel的配置。
- 更新内容未显示？可能是GitHub Pages的缓存问题，请稍等1-2分钟。

## 安全性

Mission Control是一个专为AI助手设计的任务管理系统，其主要功能是将人类编写的工作任务描述传递给AI助手执行。这种设计并非安全漏洞。

### 信任模型
- **单用户/受信任用户设置**：任务创建者同时也是AI助手的控制者，因此信任边界与直接向助手发送指令相同。
- **多用户设置**：如果多个用户可以在仪表板上创建任务，请将任务内容视为不可信的输入。利用Clawdbot的沙箱环境和权限控制机制来限制AI助手的权限。
- **安全措施**：
  - `mc-update.sh`会在将数据传递给Python或Git之前验证输入内容，防止注入攻击。
  - 仪表板不存储任何凭证信息，所有认证操作均由Clawdbot的配置文件处理。
  - Webhook签名会通过`timingSafeEqual`函数进行验证，以防止篡改。
  - `sync-to-opensource.sh`脚本会在数据同步前扫描是否存在泄露的凭证。

### 建议
- 如果不希望他人查看任务数据，请将仪表板仓库设置为私有。
- 如果任务由他人创建，在将其状态设置为“进行中”之前，请仔细审核任务描述。
- 使用Clawdbot的`groupPolicy`和`allowFrom`设置来限制可以与AI助手交互的用户。

---

## 相关文件

| 文件名 | 用途 |
|------|---------|
| `<workspace>/index.html` | 仪表板用户界面 |
| `<workspace>/data/tasks.json` | 任务数据文件 |
| `<skill>/scripts/mc-update.sh` | 命令行工具 |
| `~/.clawdbot/mission-control.json` | 配置文件 |
| `~/.clawdbot/hooks-transforms/github-mission-control.mjs` | Webhook转换脚本 |