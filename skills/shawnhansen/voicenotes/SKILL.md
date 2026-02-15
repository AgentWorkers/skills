---
name: voicenotes
description: 同步并访问 Voicenotes.com 上的语音笔记。当用户需要从 Voicenotes 中检索语音记录、文字记录以及 AI 生成的摘要时，可以使用此功能。支持获取笔记内容、将其同步到 Markdown 格式，以及搜索文字记录。
---

# Voicenotes 集成

将来自 [voicenotes.com](https://voicenotes.com) 的语音笔记同步到工作区中。

## 设置

1. 从以下链接获取访问令牌：https://voicenotes.com/app?obsidian=true#settings
2. 设置环境变量：`export VOICENOTES_TOKEN="your-token-here"`

## 快速入门

```bash
# Verify connection
./scripts/get-user.sh | jq .

# Fetch recent notes (JSON)
./scripts/fetch-notes.sh | jq '.data[:3]'

# Sync all notes to markdown files
./scripts/sync-to-markdown.sh --output-dir ./voicenotes
```

## 脚本

### fetch-notes.sh
以 JSON 格式获取语音笔记。
```bash
./scripts/fetch-notes.sh                    # All notes
./scripts/fetch-notes.sh --limit 10         # Last 10 notes
./scripts/fetch-notes.sh --since 2024-01-01 # Notes since date
```

### get-user.sh
验证令牌并获取用户信息。
```bash
./scripts/get-user.sh | jq '{name, email}'
```

### sync-to-markdown.sh
将笔记同步到带有前置内容的 Markdown 文件中。
```bash
./scripts/sync-to-markdown.sh --output-dir ./voicenotes
```

输出格式：
```markdown
---
voicenotes_id: abc123
created: 2024-01-15T10:30:00Z
tags: [idea, project]
---

# Note Title

## Transcript
The transcribed content...

## Summary
AI-generated summary...
```

## API 参考

基础 URL：`https://api.voicenotes.com/api/integrations/obsidian-sync`

所需请求头：
- `Authorization: Bearer {token}`
- `X-API-KEY: {token}`

端点：
- `GET /user/info` - 用户详细信息
- `GET /recordings` - 列出语音笔记（分页）
- `GET /recordings/{id}/signed-url` - 音频下载 URL

## 数据结构

每个语音笔记包含以下内容：
- `recording_id` - 唯一标识符
- `title` - 笔记标题
- `transcript` - 完整的文字记录
- `creations[]` - 人工智能生成的摘要、待办事项等
- `tags[]` - 用户标签
- `created_at` / `updated_at` - 创建/更新时间戳
- `duration` - 录音时长（以秒为单位）

## 提示

- 笔记是分页显示的；使用 `links.next` 查看更多页面
- 使用 `--since` 仅获取自上次同步以来的新笔记
- 人工智能生成的摘要包括摘要、待办事项和自定义提示
- 每分钟请求次数有限制（约 60 次）