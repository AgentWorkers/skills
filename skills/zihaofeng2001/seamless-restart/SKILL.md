---
name: seamless-restart
description: 无缝的网关重启功能，支持自动恢复上下文信息并在重启后发送通知。适用于需要重启 OpenClaw 网关的所有场景（配置更改、更新或手动重启）。该功能可确保上下文数据不会丢失，并在网关重新上线时及时通知用户。同时，当用户执行“重启”、“重新启动网关”或任何可能导致网关重启的操作时，该功能也会被自动触发。这一功能有效解决了网关重启后代理程序可能突然停止响应的常见问题。
  Seamless gateway restart with automatic context recovery and post-restart notification.
  Use whenever the agent needs to restart the OpenClaw gateway (config changes, updates,
  manual restarts). Ensures no context is lost and the user is always notified when the
  agent comes back online. Also use when the user mentions "restart", "reboot gateway",
  "apply config", or any action that triggers a gateway restart. This skill prevents the
  common problem of agents going silent after restarts.
metadata:
  openclaw:
    emoji: 🔄
---
# 无缝重启

该协议实现了零停机时间的网关重启功能，并具备自动上下文恢复机制，有效解决了网关重启后代理程序丢失上下文、从而无法正常工作的常见问题。

## 协议存在的必要性

网关重启（配置更改、更新或手动重启）会导致上下文丢失，因为新的 API 会话会从零开始，没有之前的对话记录。如果没有这个机制，代理程序在重启后将无法记住之前的操作内容，也无法主动通知用户。

## 协议流程

每次网关重启都必须遵循以下三个步骤：

### 第一步：将状态保存到 `NOW.md` 文件中

在重启之前，更新工作区根目录下的 `NOW.md` 文件：

```markdown
# NOW.md - Current State Snapshot

## Last Updated
- **Time**: [current timestamp]
- **Session**: [which channel/chat the user is in]
- **Status**: [what was happening]

## Active Tasks
- [list any in-progress tasks]

## Recent Context
- [key context points the next session needs to know]

## Post-Restart Action
- [specific actions to take after restart, e.g. notify user, continue task]
```

请保持文件内容简洁，因为该文件会在每次会话开始时被读取，避免文件过大。

### 第二步：发送通知并安排恢复任务

向用户发送重启前的通知，然后安排一个一次性 cron 作业，在重启后约 1 分钟内执行恢复操作：

**发送通知：**
```
message(action=send, channel=<current_channel>, target=<current_channel_id>,
  message="⚡ Restarting gateway — back in ~1 minute...")
```

**安排恢复任务：**
```
cron(action=add, job={
  "name": "restart-recovery",
  "schedule": {"kind": "at", "at": "<1 minute from now in ISO-8601 UTC>"},
  "payload": {
    "kind": "systemEvent",
    "text": "RESTART RECOVERY: You just restarted. Read NOW.md immediately.
      Then notify the user you are back and summarize what you were doing.
      Send the notification to the same channel the user was in before restart."
  },
  "sessionTarget": "main",
  "enabled": true
})
```

该 cron 作业执行完成后会自动删除。

### 第三步：执行重启操作

现在可以重启网关了：
```
gateway(action=restart, note="<human-readable reason>")
```

如果是配置更改导致的重启：
```
gateway(action=config.patch, raw=<config>, note="<reason>")
```

这两种情况都会触发 SIGUSR1 信号来重启网关。

### 重启后的自动处理

当恢复任务执行完成后：

1. **读取 `NOW.md` 文件以恢复上下文**。
2. **向用户发送通知，确认重启已完成**。
3. **恢复 `NOW.md` 中列出的所有正在进行的任务**。
4. **清除 `NOW.md` 文件中的“重启后操作”部分（将其设置为“none”）。

## 基于不同渠道的个性化通知

根据用户当前的聊天渠道，调整通知方式：

| 渠道 | 通知方法 |
|---------|-------------------|
| Discord | `message(action=send, channel=discord, target=<channelId>, guildId=<guildId>)` |
| Telegram | `message(action=send, channel=telegram, target=<chatId>)` |
| 其他渠道 | 使用重启前的渠道和目标信息 |

请确保在 `NOW.md` 文件中始终包含渠道信息，以便恢复任务知道应该发送通知到哪里。

## 特殊情况处理

- **连续多次重启**：如果在恢复任务执行之前需要再次重启网关，请取消之前的 cron 作业并重新创建一个新的。任何时候只能有一个恢复任务在运行。
- **在子代理任务进行中重启**：请注意 `NOW.md` 文件中列出的所有正在运行的子代理任务。重启后，这些子代理任务将会被终止，并需要通知用户哪些任务被中断。
- **意外重启（系统崩溃）**：本协议仅适用于计划内的重启。对于系统崩溃导致的重启，应依赖心跳机制进行恢复；如果代理程序无法发送心跳信号，它应在下次启动时检查 `NOW.md` 文件以获取恢复信息。

## 与 `AGENTS.md` 的集成

将此协议内容添加到您的用户规则或操作配置中：

```markdown
- **Gateway restart protocol**: Always use the seamless-restart skill for any
  gateway restart. Three steps: (1) update NOW.md, (2) notify + set recovery cron,
  (3) restart. Never restart without steps 1 and 2.
```

## 完整重启流程示例

```
1. Agent needs to restart for a config change

2. Agent updates NOW.md:
   "Status: Applying new Gemini API key. Session: Discord #misc.
    Post-Restart: Notify Zihao in Discord #misc that config is applied."

3. Agent sends: "⚡ Applying config change — restarting, back in ~1 min..."

4. Agent creates one-shot cron for T+60s:
   systemEvent → "RESTART RECOVERY: Read NOW.md, notify user, resume."

5. Agent calls: gateway(action=config.patch, raw={...}, note="New API key")

6. Gateway restarts. ~60s later, cron fires.

7. Agent reads NOW.md, sends: "✅ Back online. Config change applied successfully."

8. Agent clears Post-Restart Action in NOW.md.
```