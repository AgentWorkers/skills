---
name: pocket-transcripts
description: 用于读取来自 Pocket AI (heypocket.com) 录音设备的文字记录和摘要。当用户需要检索、搜索或分析他们的 Pocket 录音内容、文字记录、摘要或待办事项时，可以使用该功能。该功能会在涉及 Pocket 设备数据、对话记录、会议录音或音频笔记检索的请求时被触发。
---

# Pocket Transcripts

通过逆向工程的API，可以读取来自Pocket AI设备的转录文本和摘要。

## 快速参考

| 功能 | 描述 |
|----------|-------------|
| `get_recordings(days, limit)` | 列出最近的录音记录 |
| `get_recording_full(id)` | 获取转录文本、摘要以及待办事项 |
| `get_transcript(id)` | 获取原始的转录文本 |
| `get_summarization(id)` | 获取Markdown格式的摘要 |
| `search_recordings(query)` | 按文本内容进行搜索 |

## 设置（只需一次）

### 1. 使用用户配置文件启动Chrome浏览器

```bash
~/.factory/skills/browser/start.js --profile
# or
~/.claude/skills/browser/start.js --profile
```

### 2. 登录Pocket应用

导航至Pocket应用并登录：
```bash
~/.factory/skills/browser/nav.js https://app.heypocket.com
```

### 3. 提取Token

```bash
python3 scripts/reader.py extract
```

Token会被保存在`~/.pocket_token.json`文件中，有效期为1小时。

## 使用方法

### 列出录音记录

```python
from pathlib import Path
import sys
sys.path.insert(0, str(Path.home() / '.claude/skills/pocket-transcripts/scripts'))
from reader import get_recordings, get_recording_full

recordings = get_recordings(days=30, limit=20)
for r in recordings:
    print(f"{r.recorded_at:%Y-%m-%d} | {r.duration_str} | {r.title}")
```

### 获取完整的转录文本和摘要

```python
full = get_recording_full(recording_id)

print(f"Transcript ({len(full['transcript'])} chars):")
print(full['transcript'][:500])

print(f"\nSummary (markdown):")
print(full['summary'])

print(f"\nAction Items: {len(full['action_items'])}")
for item in full['action_items']:
    print(f"  - {item}")
```

### 搜索录音记录

```python
results = search_recordings("meeting", days=90)
for r in results:
    print(f"{r.title} - {r.description[:100]}")
```

## API详细信息

**基础URL**: `https://production.heypocketetai.com/api/v1`

**认证方式**: 使用浏览器中的Firebase Bearer Token（从IndexedDB中获取）

**主要API端点**:
- `GET /recordings` - 带分页和过滤功能的录音记录列表
- `GET /recordings/{id}?include=all` - 包含转录文本和摘要的完整数据

**数据结构**:
- 转录文本: `data.transcription.transcription.text`
- 摘要: `data.summarizations[id].v2.summary.markdown`
- 待办事项: `data.summarizations[id].v2.actionItems.items`

## Token刷新

Firebase Token的有效期为1小时。过期后，请按照以下步骤操作：
1. 确保Chrome浏览器以`--profile`模式运行。
2. 确认已登录到app.heypocket.com。
3. 重新运行命令：`python3 scripts/reader.py extract`

## 数据模型

### PocketRecording
- `id`, `title`, `description`
- `duration`（秒），`duration_str`（人类可读的时长格式）
- `recorded_at`, `created_at`
- `has_transcription`, `has_summarization`
- `num_speakers`
- `latitude`, `longitude`（如果启用了位置信息）
- `tags`（字符串列表）

### PocketSummarization
- `summary`（Markdown格式的摘要）
- `action_items`（待办事项列表）
- `transcript`（原始转录文本）