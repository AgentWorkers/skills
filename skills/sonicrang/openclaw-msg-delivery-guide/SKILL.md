---
name: openclaw-msg-delivery-guide
description: 确保后续回复能够真正到达 OpenClaw 中的用户。当用户请求提醒、安排检查、跟进通知、任务完成更新、定期监控或任何需要分步骤执行且结果对用户可见的任务时，应使用此功能。对于需要定时执行或依赖通知的任务，默认使用 cron；对于后台任务的结果传递，可使用子代理（subagent）来完成；如果任务已经立即完成，则直接回复用户；除非用户明确要求进行低频、非实时的跟进，否则避免使用心跳（heartbeat）机制。
metadata:
  openclaw:
    requires:
      bins: ["openclaw"]
      files: ["~/.openclaw/cron/jobs.json"]
      note: "This skill may inspect and modify local OpenClaw cron configuration, run openclaw cron commands, manually trigger jobs for verification, and send test notifications while validating delivery behavior against the local scheduler store."
---
# OpenClaw 消息传递指南

## 核心问题

需要避免以下失败情况：

- 工作开始后，代理承诺稍后回复，但实际上并未绑定任何消息传递路径，导致用户始终无法收到结果。

**执行**与**消息传递**是两个不同的过程：开始工作并不等同于绑定一个用户可以看到的后续消息。

## 核心规则

### 规则 1：在没有明确传递路径的情况下，切勿承诺稍后回复

在说出以下话语之前（如：“5分钟后回复”、“请关注此任务并告知是否有进展”、“稍后发送”或“每小时检查一次并通知我”），必须能够回答以下三个问题：
1. 什么事件被视为完成或可报告的进展？
2. 谁将发送后续消息？
3. 使用哪种机制来实际传递消息？

如果任何问题的答案都不明确，请先确定消息传递路径：选择合适的传递机制并绑定目标，然后再承诺后续操作。

### 规则 2：根据传递需求选择合适的机制

**默认映射**如下：
- **直接回复**：立即发送结果。
- **Cron**：指定具体时间或重复调度；通知非常重要。
- **子代理**：后台任务，在完成时向请求者发送反馈。
- **心跳机制**：仅用于低频率的简单检查；除非用户明确要求，否则应避免使用。
- **`message`发送**：工具已发送了用户可见的结果。

### 规则 3：需要定时通知时，使用 Cron

对于类似“5分钟后回复”、“20分钟后提醒我”、“每小时检查一次并在有变化时通知我”或“每天9点发送报告”这样的请求，建议使用以下方式：
- 使用 `--at` 参数设置一次性 Cron 任务。
- 使用 `--cron` 参数设置重复执行的 Cron 任务。
- 如果任务需要独立运行并传递自己的结果，使用 `--session isolated` 参数。
- 从当前会话元数据中获取明确的传递目标。

除非用户明确要求使用主会话或心跳机制，否则不要默认使用主会话的 Cron 任务。

### 规则 4：后台执行并不意味着会自动通知用户

启动执行任务或长时间运行的任务仅表示工作已经开始，并不意味着用户会立即收到更新。如果用户期望收到后续消息，必须明确绑定消息传递路径。

## 关键示例

### 1. “5分钟后回复”

应使用一次性 Cron 任务，而非心跳机制。

```bash
openclaw cron add \
  --name "Reply in 5 minutes" \
  --at "5m" \
  --session isolated \
  --message "Reply to the user with the requested follow-up. If nothing meaningful changed, say that clearly." \
  --announce \
  --channel <channel> \
  --to <destination>
```

### 2. “在后台运行此任务，并在完成后通知我”

当主要需求是后台执行并需要提交完成报告时，应使用子代理。

**所需行为**：
- 启动任务。
- 告知用户任务已开始。
- 当子代理完成并返回结果时，立即将结果发送给用户。

### 3. “每小时检查一次该网站并在有变化时通知我”

应使用重复执行的 Cron 任务，并设置明确的传递路径。

```bash
openclaw cron add \
  --name "Hourly site check" \
  --cron "0 * * * *" \
  --session isolated \
  --message "Check the target site. Notify only when there is a real change; otherwise stay silent." \
  --announce \
  --channel <channel> \
  --to <destination>
```

### 4. 结果已通过 `message` 功能发送给用户

如果用户可见的结果已经通过 `message(action=send)` 发送过，则不要再次发送普通回复，只需返回 `NO_REPLY`。

## 不良做法：
- 在没有指定传递路径的情况下承诺稍后回复。
- 对于需要立即通知的情况使用心跳机制。
- 启动后台任务后，假设系统会自动通知用户。
- 当用户期望收到可见的通知时，创建没有明确传递路径的 Cron 任务。
- 仅在用户明确请求进度更新时才绑定最终的完成路径。

## 测试与验证

### Cron 任务的测试与验证

在添加或修改 Cron 任务后，需执行以下操作：
1. 确认任务存在于 `openclaw cron list` 中。
2. 验证 `~/.openclaw/cron/jobs.json` 文件中存储的字段是否正确。
3. 手动运行一次任务。
4. 确认通知已到达指定的聊天频道。

对于重复执行的任务，在手动触发之前，请先验证以下内容：
- 调度类型（`at` 或 `cron`）。
- 会话目标。
- 传递内容。
- 传递方式。
- 传递目标。

此处不需要对模型进行额外验证；除非用户特别要求，否则使用默认模型。

在修改 Cron 任务时，不要仅依赖 CLI 的输出结果，务必验证系统中存储的任务信息。

### 后台任务的后续处理

需要验证以下内容：
- 任务是否真正开始执行。
- 用户是否知道当前轮次是否已经发送了结果。
- 传递路径是否明确。

## 额外指导

### 进度更新方式

对于长时间运行的任务，在承诺后续通知之前，需先确定预期的更新方式：
- **仅发送结果**。
- **分阶段更新**。
- **固定间隔更新**。

### 无变化时保持沉默

对于重复执行的检查任务，建议仅在真正发生变化时才发送通知；否则保持沉默。

### 结果发送到当前聊天频道

当结果需要发送到同一聊天频道时，应根据当前会话元数据来确定传递目标，而不是硬编码用户特定的标识符。