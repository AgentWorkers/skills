---
name: meetgeek
description: 通过命令行界面（CLI）查询 MeetGeek 的会议信息：可以列出所有会议、获取 AI 生成的会议摘要、会议记录以及待办事项，并使用自然语言搜索您所有的通话记录。
---

# MeetGeek Skill

从 MeetGeek 中检索会议信息，包括会议摘要、录音文本、待办事项，并支持对会议内容进行搜索。

**npm:** https://www.npmjs.com/package/meetgeek-cli  
**GitHub:** https://github.com/nexty5870/meetgeek-cli

## 安装

```bash
npm install -g meetgeek-cli
```

## 设置

```bash
meetgeek auth   # Interactive API key setup
```

请从 MeetGeek 的“集成”（Integrations）→“公共 API 集成”（Public API Integration）处获取您的 API 密钥。

## 命令

### 列出最近的会议
```bash
meetgeek list
meetgeek list --limit 20
```

### 获取会议详情
```bash
meetgeek show <meeting-id>
```

### 获取 AI 生成的会议摘要（含待办事项）
```bash
meetgeek summary <meeting-id>
```

### 获取完整的会议录音文本
```bash
meetgeek transcript <meeting-id>
meetgeek transcript <meeting-id> -o /tmp/call.txt  # save to file
```

### 获取会议亮点
```bash
meetgeek highlights <meeting-id>
```

### 搜索会议
```bash
# Search in a specific meeting
meetgeek ask "topic" -m <meeting-id>

# Search across all recent meetings
meetgeek ask "what did we discuss about the budget"
```

### 用户认证管理
```bash
meetgeek auth --show   # check API key status
meetgeek auth          # interactive setup
meetgeek auth --clear  # remove saved key
```

## 使用示例

### 查找特定的会议
```bash
# List meetings to find the one you want
meetgeek list --limit 10

# Then use the meeting ID (first 8 chars shown, use full ID)
meetgeek summary 81a6ab96-19e7-44f5-bd2b-594a91d2e44b
```

### 获取会议的待办事项
```bash
meetgeek summary <meeting-id>
# Look for the "✅ Action Items" section
```

### 查找关于某个主题的讨论内容
```bash
# Search across all meetings
meetgeek ask "pricing discussion"

# Or in a specific meeting
meetgeek ask "timeline" -m <meeting-id>
```

### 导出会议录音文本以供参考
```bash
meetgeek transcript <meeting-id> -o ~/call-transcript.txt
```

## 注意事项

- 会议 ID 是 UUID 格式，列表中显示的是前 8 个字符。
- 录音文本中包含发言者的姓名和时间戳。
- 会议摘要由 AI 生成，包含关键点和待办事项。
- 搜索功能基于录音文本中的关键词进行。

## 配置

API 密钥存储在：`~/.config/meetgeek/config.json`