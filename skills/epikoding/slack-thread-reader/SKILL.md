---
name: slack-thread
description: >
  **阅读并总结 Slack 频道历史记录及线程对话内容**  
  当您收到一个 Slack 链接（格式如：`https://...slack.com/archives/...`），或者被要求查看频道/线程的聊天记录、总结对话内容，或检查频道中的最新消息时，可以使用此功能。
---
# Slack 线程阅读器

该脚本用于获取 Slack 频道的聊天记录和线程回复。

## 脚本位置

`scripts/slack-thread.sh`（入口脚本）→ `scripts/slack-thread.py`（主要逻辑）

## 使用方法

### 读取特定线程
```bash
scripts/slack-thread.sh https://your-workspace.slack.com/archives/CHANNEL/pTIMESTAMP
scripts/slack-thread.sh <channel-id> <thread-ts>
```

### 读取频道聊天记录
```bash
scripts/slack-thread.sh https://your-workspace.slack.com/archives/CHANNEL
scripts/slack-thread.sh <channel-id>
scripts/slack-thread.sh <channel-id> --limit 30
```

### 包含线程回复的频道聊天记录（完整内容）
```bash
scripts/slack-thread.sh <channel-id> --with-threads
```

### 限制线程回复数量（可选）
```bash
scripts/slack-thread.sh <channel-id> --with-threads --thread-limit 5
```

## 工作流程

1. 当收到 Slack 链接或频道 ID 时，使用此脚本来获取聊天记录。
2. **⚠️ 如果链接类型与用户请求不符，请务必要求用户澄清。**
   - 链接格式：`/archives/CHANNEL` 表示频道；`/archives/CHANNEL/pTIMESTAMP` 表示特定线程
   - 例如：如果用户提供了线程链接但请求的是“获取频道聊天记录”，则应提示：“您提供的链接指向的是一个特定线程。您是想获取该线程的内容还是整个频道的聊天记录？”
   - 人们可能会犯错。如果链接与请求不一致，请直接询问用户，而不是自行猜测。
3. **当用户要求汇总频道聊天记录时**：询问用户“是否需要包含线程回复”，并根据用户的选择设置 `--with-threads` 参数。
4. 根据用户的选择，汇总聊天记录或直接输出获取到的原始内容。

## 参数选项

| 参数 | 描述 | 默认值 |
|--------|-------------|---------|
| `--limit N` | 频道聊天记录的最大条目数 | 50 |
| `--with-threads` | 是否包含线程回复 | 关闭（`off`） |
| `--thread-limit N` | 每个线程的最大回复数（0 表示全部） | 0（全部） |

## 输出内容格式

| 内容 | 格式 | 示例 |
|---------|--------|---------|
| 时间戳 | ISO 8601 格式（秒） | `[2026-02-11T17:45:56]` |
| 发件人 | 真实姓名 | `John Doe:` |
| 被提及者 | `@name`（已解析） | `@Jane Smith` |
| 表情符号反应 | 表情符号 + 反应名称 | `[:thumbsup: John,Jane]` |
| 附件 | 文件名（格式） | `📎 image.png (image/png)` |
| 线程回复数量 | 💬N | `💬13` |
| 线程回复（内联显示） | ├ └ （树状结构） | （使用 `--with-threads` 时显示）

## 注意事项

- 该机器人必须是目标频道的成员。如果出现 `channel_not_found` 错误，请指导用户在频道中运行 `/invite @botname` 命令来邀请机器人。
- 如果未使用 `--with-threads` 选项，频道聊天记录中将不包含线程对话内容。在汇总聊天记录时，请务必确认是否需要显示线程回复。