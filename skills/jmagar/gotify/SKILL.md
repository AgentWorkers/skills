---
name: gotify
description: 当长时间运行的任务完成或发生重要事件时，通过 Gotify 发送推送通知。适用于用户要求“发送 Gotify 通知”、“在此任务完成后通知我”、“通过 Gotify 提醒我”或希望收到任务完成通知的情况。
version: 1.0.1
metadata:
  clawdbot:
    emoji: "🔔"
    requires:
      bins: ["curl", "jq"]
---

# Gotify通知技能

当长时间运行的任务完成或发生重要事件时，向您的Gotify服务器发送推送通知。

## 目的

此技能使Clawdbot能够通过Gotify发送推送通知，适用于以下场景：
- 在长时间运行的任务完成后发出警报
- 发送后台操作的状态更新
- 通知重要事件或错误
- 与任务完成钩子集成

## 设置

创建凭据文件：`~/.clawdbot/credentials/gotify/config.json`

```json
{
  "url": "https://gotify.example.com",
  "token": "YOUR_APP_TOKEN"
}
```

- `url`：您的Gotify服务器URL（末尾不要加斜杠）
- `token`：来自Gotify的应用程序令牌（在“设置”→“应用程序”→“创建应用程序”中获取）

## 使用方法

### 基本通知

```bash
bash scripts/send.sh "Task completed successfully"
```

### 带标题的通知

```bash
bash scripts/send.sh --title "Build Complete" --message "skill-sync tests passed"
```

### 带优先级（0-10）

```bash
bash scripts/send.sh -t "Critical Alert" -m "Service down" -p 10
```

### 支持Markdown格式

```bash
bash scripts/send.sh --title "Deploy Summary" --markdown --message "
## Deployment Complete

- **Status**: ✅ Success
- **Duration**: 2m 34s
- **Commits**: 5 new
"
```

## 与任务完成集成

### 选项1：任务完成后直接调用

```bash
# Run long task
./deploy.sh && bash ~/clawd/skills/gotify/scripts/send.sh "Deploy finished"
```

### 选项2：钩子集成（未来版本）

当Clawdbot支持任务完成钩子时，此技能可以自动触发：

```bash
# Example hook configuration (conceptual)
{
  "on": "task_complete",
  "run": "bash ~/clawd/skills/gotify/scripts/send.sh 'Task: {{task_name}} completed in {{duration}}'"
}
```

## 参数

- `-m, --message <文本>`：通知消息（必填）
- `-t, --title <文本>`：通知标题（可选）
- `-p, --priority <0-10>`：优先级（默认值：5）
  - 0-3：低优先级
  - 4-7：普通优先级
  - 8-10：高优先级（可能会触发声音/振动）
- `--markdown`：在消息中启用Markdown格式

## 示例

### 当子代理完成任务时通知用户

```bash
# After spawning subagent
sessions_spawn --task "Research topic" --label my-research
# ... wait for completion ...
bash scripts/send.sh -t "Research Complete" -m "Check session: my-research"
```

### 高优先级错误通知

```bash
if ! ./critical-task.sh; then
  bash scripts/send.sh -t "⚠️ Critical Failure" -m "Task failed, check logs" -p 10
fi
```

### 支持Markdown格式的丰富通知

```bash
bash scripts/send.sh --markdown -t "Daily Summary" -m "
# System Status

## ✅ Healthy
- UniFi: 34 clients
- Sonarr: 1,175 shows
- Radarr: 2,551 movies

## 📊 Stats
- Uptime: 621h
- Network: All OK
"
```

## 工作流程

当用户发出以下指令时：
- **“任务完成后通知我”** → 在他们的命令中添加 `&& bash scripts/send.sh "Task complete"`
- **“发送Gotify警报”** → 运行 `bash scripts/send.sh` 并附上消息
- **“发送任务完成的推送通知”** → 将其集成到工作流程中，并设置适当的标题/优先级

请务必确认通知已成功发送（通过检查包含消息ID的JSON响应来验证）。

## 注意事项

- 需要访问您的Gotify服务器的网络权限
- 应用程序令牌必须具有“创建消息”的权限
- 优先级会影响客户端设备上的通知显示方式
- Markdown格式的支持取决于Gotify客户端的版本（大多数现代客户端都支持）

## 参考资料

- Gotify API文档：https://gotify.net/docs/
- Gotify的Android/iOS应用程序（用于接收通知）