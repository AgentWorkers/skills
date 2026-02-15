---
name: claude-code-wingman
description: 您的 Claude Code 助手——能够跨多个项目协调多个 Claude Code 会话，并通过 WhatsApp 对所有会话进行实时监控。
metadata: {"clawdbot":{"emoji":"🦅","requires":{"anyBins":["claude","tmux"]}}}
---

# Claude Code Wingman

这是一个多会话管理工具，允许您通过 WhatsApp 同时管理多个正在不同项目上运行的 Claude Code 实例。

**GitHub:** https://github.com/yossiovadia/claude-code-orchestrator

## ⚡ 重要提示：** 先处理审批命令

**当用户发送符合以下模式的消息时，立即运行相应的命令：**

| 用户消息模式 | 要运行的命令 |
|---------------------|----------------|
| `approve <session>` | `~/code/claude-code-orchestrator/lib/handle-approval.sh approve <session>` |
| `always <session>` | `~/code/claude-code-orchestrator/lib/handle-approval.sh always <session>` |
| `deny <session>` | `~/code/claude-code-orchestrator/lib/handle-approval.sh deny <session>` |

**示例：**
- 用户：`approve vsr-bugfix` → 运行：`~/code/claude-code-orchestrator/lib/handle-approval.sh approve vsr-bugfix`
- 用户：`always heartbeat-test` → 运行：`~/code/claude-code-orchestrator/lib/handle-approval.sh always heartbeat-test`
- 用户：`deny proxy-refactor` → 运行：`~/code/claude-code-orchestrator/lib/handle-approval.sh deny proxy-refactor`

**运行后，回复命令的输出结果**（例如：“✓ 会话 'vsr-bugfix' 已获批准（一次）”。

**为什么这很重要：** 当 Claude Code 会话需要审批时，主监控守护进程会通过 WhatsApp 发送通知。用户需要通过手机发送这些命令来进行审批。快速响应可以确保会话不会被阻塞。

### 快速状态查询命令

| 用户消息 | 要运行的命令 |
|--------------|----------------|
| `sessions` 或 `status` | `~/code/claude-code-orchestrator/lib/session-status.sh --all --json` |
| `status <session>` | `~/code/claude-code-orchestrator/lib/session-status.sh <session> --json` |

解析 JSON 数据并返回易于理解的摘要。

---

## 功能简介

该工具可以并行管理多个 Claude Code 会话，每个会话都在不同的目录中执行不同的任务。您可以通过 WhatsApp 或聊天界面远程监控和控制所有会话。

**核心理念：**
- **多个 tmux 会话同时运行**  
- **每个会话对应一个 Claude Code 实例**，每个实例都在自己的目录中工作  
- **不同任务并行进行**（例如：VSR 问题修复、Clawdbot 功能开发、代理重构）  
- **您可以通过 Clawdbot（辅助工具）通过 WhatsApp 来管理所有会话**  
- **实时仪表板** 显示所有活跃会话及其状态

## 🎯 实际应用示例：多会话管理

**早上 - 您通过 WhatsApp 发送指令：** “开始处理 VSR 问题 #1131、启动 Clawdbot 的身份验证功能，并重构代理代码”

**Clawdbot 会创建 3 个会话：**  
```
✅ Session: vsr-issue-1131     (~/code/semantic-router)
✅ Session: clawdbot-auth      (~/code/clawdbot)
✅ Session: proxy-refactor     (~/code/claude-code-proxy)
```

**午餐时间 - 您询问：** “显示仪表板”

**Clawdbot 回答：**  
```
┌─────────────────────────────────────────────────────────┐
│ Active Claude Code Sessions                             │
├─────────────────┬──────────────────────┬────────────────┤
│ vsr-issue-1131  │ semantic-router      │ ✅ Working     │
│ clawdbot-auth   │ clawdbot             │ ✅ Working     │
│ proxy-refactor  │ claude-code-proxy    │ ⏳ Waiting approval │
└─────────────────┴──────────────────────┴────────────────┘
```

**您继续询问：** “VSR 问题的进展如何？”

**Clawdbot 显示会话输出：**  
“几乎完成 - 修复了模式验证错误，现在正在运行测试。8 个测试中有 10 个通过了。”

**您再次指令：** “告诉代理重构模块接下来运行测试”

**Clawdbot 向相应的会话发送命令。**

**结果：** 3 个任务同时进行，您可以通过手机实现完全的远程控制。🎯

## 安装方法

### 推荐使用 Clawdbot 安装

```bash
clawdbot skill install claude-code-wingman
```

或者访问：https://clawdhub.com/skills/claude-code-wingman

### 手动安装

```bash
cd ~/code
git clone https://github.com/yossiovadia/claude-code-orchestrator.git
cd claude-code-orchestrator
chmod +x *.sh lib/*.sh
```

### 系统要求**

- `claude` CLI（Claude Code 的命令行工具）  
- `tmux`（终端多路复用器）  
- `jq`（JSON 处理工具）

## 核心原则：** 始终使用 wingman 脚本**

**重要提示：** 与 Claude Code 会话交互时，务必使用 `claude-wingman.sh` 脚本，切勿直接运行 tmux 命令。

**原因：**
- ✅ 确保正确处理 Enter 键（例如使用 C-m 键）  
- ✅ 保持会话管理的一致性  
- 为未来的仪表板/跟踪功能做好准备  
- 避免因手动操作 tmux 命令而产生的错误  

**错误操作（请勿这样做：**  
```bash
tmux send-keys -t my-session "Run tests"
# ^ Might forget C-m, won't be tracked in dashboard
```

**正确操作（务必这样做：**  
```bash
~/code/claude-code-orchestrator/claude-wingman.sh \
  --session my-session \
  --workdir ~/code/myproject \
  --prompt "Run tests"
```

---

## 如何通过 Clawdbot 使用该工具

### 启动新会话

当用户请求进行编码工作时，使用以下命令启动 Claude Code 会话：

```bash
~/code/claude-code-orchestrator/claude-wingman.sh \
  --session <session-name> \
  --workdir <project-directory> \
  --prompt "<task description>"
```

### 向现有会话发送命令

要向正在运行的会话发送新任务，使用以下命令：

```bash
~/code/claude-code-orchestrator/claude-wingman.sh \
  --session <existing-session-name> \
  --workdir <same-directory> \
  --prompt "<new task>"
```

**注意：** 脚本会检测会话是否存在，如果存在则直接发送命令，而不会创建重复的会话。

### 检查会话状态

解析输出信息，判断 Claude Code 的状态：
- **正在工作**（显示工具调用和进度）
- **空闲**（显示提示符）
- **出错**（显示错误信息）
- **等待审批**（显示“是否允许此工具调用？”的提示）

---

## 示例交互流程

**用户：** “修复 api.py 中的错误”

**Clawdbot：**  
```
Spawning Claude Code session for this...

[Runs wingman script]

✅ Session started: vsr-bug-fix
📂 Directory: ~/code/semantic-router
🎯 Task: Fix bug in api.py
```

**用户：** “状态如何？”

**Clawdbot：**  
```bash
tmux capture-pane -t vsr-bug-fix -p -S -50
```

**Clawdbot 回答：** “Claude Code 正在运行测试，8 个测试中有 10 个通过了。”

**用户：** “告诉它提交更改。”

**Clawdbot：**  
```bash
~/code/claude-code-orchestrator/claude-wingman.sh \
  --session vsr-bug-fix \
  --workdir ~/code/semantic-router \
  --prompt "Commit the changes with a descriptive message"
```

## 命令参考

### 启动新会话  
```bash
~/code/claude-code-orchestrator/claude-wingman.sh \
  --session <name> \
  --workdir <dir> \
  --prompt "<task>"
```

### 向现有会话发送命令  
```bash
~/code/claude-code-orchestrator/claude-wingman.sh \
  --session <existing-session> \
  --workdir <same-dir> \
  --prompt "<new command>"
```

### 监控会话进度  
```bash
tmux capture-pane -t <session-name> -p -S -100
```

### 列出所有活跃会话  
```bash
tmux ls
```

**筛选 Claude Code 会话：**  
```bash
tmux ls | grep -E "(vsr|clawdbot|proxy|claude)"
```

**查看自动审批日志（如需）**  
```bash
cat /tmp/auto-approver-<session-name>.log
```

### 会话完成后结束会话  
```bash
tmux kill-session -t <session-name>
```

### 手动附加会话（供用户操作）  
```bash
tmux attach -t <session-name>
# Detach: Ctrl+B, then D
```

---

## 开发计划：多会话仪表板（即将推出）

**计划中的功能：**

- **wingman 仪表板**：显示所有活跃的 Claude Code 会话  
- `wingman status <session>`：显示特定会话的详细状态  
- **会话注册表**：  
  - 持久跟踪会话状态（即使 Clawdbot 重启也能保留数据）  
  - 用 JSON 文件存储会话元数据  
  - 自动清理不再使用的会话  

**目前：** 可以直接使用 tmux 命令，但建议始终通过 wingman 脚本来发送命令！

## 工作流程

1. **用户请求进行编码工作**（例如修复错误、添加新功能、重构代码等）  
2. **Clawdbot 通过管理脚本启动 Claude Code 会话**  
3. **自动审批模块在后台处理权限审批**  
4. **Clawdbot 监控并报告进度**  
5. **用户可以随时附加到会话中进行查看或控制**  
6. **Claude Code 自动完成工作**

## 首次使用时的提示

当 Claude Code 在新目录中运行时，会显示提示：  
> “您是否信任该目录中的文件？”

**首次使用时：** 用户需要手动附加并点击“批准”（按 Enter 键）。之后，系统将自动处理后续操作。

**处理方式：**  
```
User, Claude Code needs you to approve the folder trust (one-time). Please run:
tmux attach -t <session-name>

Press Enter to approve, then Ctrl+B followed by D to detach.
```

## 最佳实践

### 何时使用该工具

- **适用于：**  
  - 大量代码生成或重构任务  
  - 多文件修改  
  - 长时间运行的任务  
  - 重复性的编码工作  

**不适用的情况：**  
  - 快速读取文件  
  - 简单的编辑操作  
  - 需要进行讨论或规划的设计工作  

### 会话命名规则

使用描述性强的名称：  
- `vsr-issue-1131`：特定问题的处理  
- `vsr-feature-auth`：功能开发  
- `project-bugfix-X`：错误修复  

## 故障排除

### 提示符未响应
如果系统未及时响应，用户可以手动附加会话并点击 Enter 键。

### 自动审批模块无法工作
检查日志文件：`cat /tmp/auto-approver-<session-name>.log`  
日志中应显示：“检测到审批提示！正在导航到选项 2...”

### 会话已存在
使用以下命令结束会话：`tmux kill-session -t <会话名称>`

## 高级技巧

- **并行会话**：在不同的会话中同时运行多个任务  
- **统一命名规则**：使用项目前缀（如 `vsr-`、`myapp-` 等）  
- **定期检查进度**：每隔几分钟检查一次会话状态  
- **让任务完成**：不要过早结束会话，让 Claude Code 完成所有工作

---

## 🔔 审批处理（与 WhatsApp 的集成）

当会话需要审批时，主监控守护进程会通过 WhatsApp 发送通知。您可以使用以下命令进行处理：

### 通过 WhatsApp 接收审批请求

收到审批通知后，回复相应的命令：

**Clawdbot 会解析您的消息并执行相应操作：**  
```bash
# Approve once
~/code/claude-code-orchestrator/lib/handle-approval.sh approve <session-name>

# Approve all similar (always)
~/code/claude-code-orchestrator/lib/handle-approval.sh always <session-name>

# Deny
~/code/claude-code-orchestrator/lib/handle-approval.sh deny <session-name>
```

### WhatsApp 流程示例

**收到通知后：**  
```
🔒 Session 'vsr-bugfix' needs approval

Bash(rm -rf ./build && npm run build)

Reply with:
• approve vsr-bugfix - Allow once
• always vsr-bugfix - Allow all similar
• deny vsr-bugfix - Reject
```

**您回复：** “approve vsr-bugfix”

**Clawdbot：**  
```bash
~/code/claude-code-orchestrator/lib/handle-approval.sh approve vsr-bugfix
```

**系统回复：** “✓ 会话 'vsr-bugfix' 已获批准（一次）”

### 启动监控守护进程

```bash
# Start monitoring all sessions (reads config from ~/.clawdbot/clawdbot.json)
~/code/claude-code-orchestrator/master-monitor.sh &

# With custom intervals
~/code/claude-code-orchestrator/master-monitor.sh --poll-interval 5 --reminder-interval 120 &

# Check if running
cat /tmp/claude-orchestrator/master-monitor.pid

# View logs
tail -f /tmp/claude-orchestrator/master-monitor.log

# Stop the daemon
kill $(cat /tmp/claude-orchestrator/master-monitor.pid)
```

无需设置环境变量——手机信息和 Webhook 令牌会从 Clawdbot 配置文件中读取。