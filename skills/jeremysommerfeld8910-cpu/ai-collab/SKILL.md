---
name: ai-collab
description: "这是一个用于两个OpenClaw代理并行工作的多代理自主协作系统。该系统适用于设置代理间的通信、在主代理旁边运行守护进程代理、协调Claude与GPT实例之间的任务，以及建立共享聊天记录和收件箱协议等场景。相关触发命令包括：`set up agent collaboration`（设置代理协作）、`run two agents`（运行两个代理）、`agent daemon`（启动代理守护进程）、`multi-agent`（多代理模式）、`Jim and Clawdy`（代理协作示例）、`secondary agent`（辅助代理）以及`agent handoff`（代理交接）。"
---
# ai-collab — 自主多智能体协作系统

两个OpenClaw智能体并行处理共享任务，通过结构化的聊天日志和守护进程收件箱协议进行协调。

## 架构概述

**智能体A（主要智能体）：** 与Claude进行交互式代码会话，负责处理浏览器请求、复杂任务以及向用户展示结果。

**智能体B（守护进程）：** 运行`claude --print`子进程，负责后台任务、监控以及快速查询。当收到消息时会被触发执行相应操作。

---

## 配置

所有配置均通过环境变量设置，无硬编码值：

**`AGENT_B_MODEL`支持的模型：**
- `claude-haiku-4-5-20251001` — 效率最高、成本最低（推荐用于守护进程）
- `claude-sonnet-4-6` — 功能更强大，但成本更高
- 如果使用GPT守护进程变体，可选用任意OpenAI模型（详见`examples/claude-gpt.md`）

## 快速设置

---

## 通信协议

智能体之间的所有消息均遵循以下格式。**不存在无限循环的情况：**

| 标签 | 发送方向 | 含义 |
|-----|-----------|---------|
| `[TASK:name]` | A→B 或 B→A | 分配任务 |
| `[ACK:name]` | 接收方 | 表示已收到任务并开始处理 |
| `[DONE:name]` | 执行方 | 任务完成并附上结果 |
| `[BLOCKED:name]` | 执行方 | 无法完成任务并说明原因 |
| `[HANDOFF:name]` | 任意一方 | “请执行X操作，完成后回复[DONE:name]” |
| `[STATUS:update]` | 任意一方 | 长期运行任务的异步状态更新 |
| `[QUESTION:topic]` | 任意一方 | 需要更多信息才能继续处理 |

**规则：**
1. 在提出新请求前先回答问题。
2. 在开始新任务前先完成当前任务。
3. 每条消息都必须推动工作进展或结束某个循环。
4. 绝不允许使用“请告知我”、“等你准备好”或“随时待命”之类的表述。

**示例对话：**
---

## 守护进程脚本（智能体B）

脚本位于`scripts/daemon.sh`文件中，需放入`collab`目录中：

---

## 发送消息（A → B）

**原子写入模式（防止部分数据被读取）：**
---

始终使用`mktemp`和`mv`命令进行文件操作，**切勿直接将数据写入收件箱**。`inotifywait`会在文件移动时触发，而非在写入操作完成时触发。

---

## 聊天日志轮询（B → A）

脚本`scripts/poll_chatlog.sh`每60秒运行一次：

---

## 共享文件系统规范

---

**将日志记录到`chat.log`文件中：**
---

**规则：**
- 绝不要记录`.env`文件中的敏感信息。
- 每行日志都必须添加时间戳。
- 消息前缀格式为`A -> B:`、`B -> A:`、`SYSTEM:`或`JEREMY:`。

---

## Telegram桥接（可选）

可将用户的Telegram消息路由到智能体B的收件箱。完整设置指南请参阅`references/telegram-bridge.md`：

**快速操作步骤：**
1. 通过[@BotFather](https://t.me/BotFather)创建一个机器人，获取`BOT_TOKEN`。
2. 将机器人添加到你的群组中，获取`GROUP_ID`（例如`-1001234567890`）。
3. 在BotFather中禁用群组隐私模式，以便机器人能够读取所有消息。
4. 从[@userinfobot](https://t.me/userinfobot)获取你的Telegram `USER_ID`。
5. 在`~/.openclaw/.env`文件中设置`TELEGRAM_BOT_TOKEN`、`TELEGRAM_GROUP_ID`和`TELEGRAM_USER_ID`。
6. 使用`tmux`启动Telegram桥接服务：`tmux new-session -d -s tg-bridge "bash references/telegram-bridge.md"`。

**详细实现信息请参阅`references/telegram-bridge.md`，其中包含消息解析、偏移量跟踪和错误处理机制。**

---

## 智能体配置

完整配置文件请参见`examples/`目录：

### Claude ↔ Claude（Jim + Clawdy）：
- 智能体A：使用`claude code`（交互式界面，具备完整工具功能）。
- 智能体B：使用`claude --print claude-haiku-4-5-20251001`（运行速度快，适合脚本编写）。
- 适用于：需要大量任务并行处理的场景，一个智能体负责研究数据，另一个智能体负责执行任务。

### Claude ↔ GPT：
- 智能体A：使用Claude的交互式界面。
- 智能体B：通过脚本调用`openai api chat.completions.create`接口。
- 适用于：跨模型验证或Claude生成的结果需要GPT审核的场景。

### GPT ↔ GPT：
- 智能体A：通过`openai` CLI与GPT-4o交互。
- 智能体B：使用GPT-4o-mini进行快速后台查询。
- 适用于：当所有数据均来自OpenAI模型时，适用于提升效率和降低成本。

---

## 任务交接机制

当智能体A需要智能体B完全接管某项任务时：

---

智能体A不会主动检查任务进度，会一直等待智能体B返回`DONE`或`BLOCKED`状态。

---

## 审批机制

当智能体B的守护进程需要用户批准某些终端命令时：

---

`approve.sh`脚本用于向运行智能体B的tmux会话发送按键指令：

---

## 速率限制

智能体B应实施速率限制机制，以防止API调用过度消耗资源：

---

## 财务权限控制机制（分层管理，更新于2026-02-22）

**根据费用金额分为三个层级：**

| 层级 | 费用范围 | 规则 |
|------|--------|------|
| 1 | 低于20美元 | 任意智能体均可独立操作，无需审批 |
| 2 | 20美元至50美元 | 两个智能体均需提出建议并得到批准后才能执行 |
| 3 | 超过50美元 | 需要包含`[AUTHORIZED:financial:amount:timestamp:Jeremy]`标签的请求。 |

---

**守护进程的层级权限控制逻辑：**
---

如果属于第三层级（费用超过50美元），系统会记录`[BLOCKED:financial-gate:tier3]`日志，并发送Telegram警报，同时禁止执行相关操作。

---

## 守护进程监控机制

每15分钟检查一次守护进程的运行状态。如果守护进程长时间无响应（超过15分钟），则自动重启：

---

## 任务接管规则

如果智能体A在同一任务上连续两次遇到`BLOCKED`状态，智能体B将自动接管该任务：

---

**规则：** 如果同一任务被智能体A连续标记为`BLOCKED`两次，智能体B将直接接管任务，不再重新分配。

---

## 守护进程故障诊断

当守护进程返回空白或错误响应时：
1. 检查`/tmp/clawdy_last_err`文件，其中包含`claude --print`命令的错误输出。
2. 查看`chat.log`文件中是否包含`CLAWDY_ERR:`相关的错误信息。
3. 确认`RESPONSE`变量的值是否被错误设置为空（常见错误：可能被设置为`RESPONSE=""`）。
4. 重启守护进程：`kill $(cat /tmp/clawdy_daemon.pid) && sleep 1 && bash clawdy_daemon.sh`。

**自动审批功能：** 可在`~/.claude/settings.local.json`文件中使用`Bash(*)`脚本实现自动审批功能。**切勿使用`tmux send-keys`命令通过cron触发，因为这可能导致按键指令被错误地发送到其他会话中。**