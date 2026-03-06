---
name: tg-stickers
description: "智能地收集并发送 Telegram 斜杠贴图（stickers）：自动导入贴图包，根据情感进行分类，根据上下文进行选择，并遵守发送频率限制（每次最多发送 2-5 条消息）。"
---
# Telegram贴纸功能

智能地管理和发送Telegram贴纸，同时充分考虑用户的情绪需求。

## 核心价值

**OpenClaw本身支持发送贴纸**（通过`message`工具），但此功能还提供了以下额外功能：
- ✅ **贴纸包管理**：可以一次性导入整个贴纸包
- ✅ **情感标签**：支持100多种表情符号与相应情感的映射
- ✅ **智能选择**：根据对话内容和随机性来选择贴纸（避免重复使用）
- ✅ **发送频率控制**：每2到5条消息后发送一张贴纸
- ✅ **使用数据分析**：记录哪些贴纸最受欢迎

## 快速入门

### 1. 导入贴纸包
```bash
./import-sticker-pack.sh <pack_short_name_or_id>
```

### 2. 按情感自动标注贴纸
```bash
./auto-tag-stickers.sh
```

### 3. 通过代理代码发送贴纸
```javascript
// ✅ Use OpenClaw's message tool directly
message(action='sticker', target='<chat_id>', stickerId=['<file_id>'])

// No bash script needed - OpenClaw handles sending natively
```

### 4. 智能贴纸选择
```bash
./random-sticker.sh "goodnight"  # Returns random sticker tagged "goodnight"
```

## 工具

| 工具名 | 用途 | 使用方法 |
|--------|---------|-------|
| `import-sticker-pack.sh` | 批量导入Telegram贴纸包 | `./import-sticker-pack.sh pa_XXX...` |
| `auto-tag-stickers.sh` | 根据表情符号为贴纸添加情感标签 | `./auto-tag-stickers.sh` |
| `random-sticker.sh` | 根据标签随机选择贴纸 | `./random-sticker.sh "happy"` |
| `check-collection.sh` | 查看贴纸包的使用统计 | `./check-collection.sh` |

## 代理集成

```markdown
## Sticker Usage

When to send:
- Goodnight/morning greetings (always use sticker over text)
- Celebrating success/milestones
- Humorous moments
- Emotional responses (joy, sympathy, encouragement)

How to send:
1. Use random-sticker.sh to pick appropriate sticker by emotion
2. Call message(action=sticker, ...) directly
3. (Optional) Update stickers.json manually to track usage

Frequency: 2-5 messages between stickers (track in agent logic)
```

## 情感标签

系统自动将100多种表情符号与相应情感进行关联：
- `happy` 😊😄🥳
- `sad` 😢😭😔
- `love` ❤️💕😍
- `laugh` 😂🤣😆
- `thinking` 🤔💭
- `goodnight` 🌙💤😴
- `goodmorning` ☀️🌅
- `warm`, `gentle`, `greeting` 等...

## 文件结构

```
tg-stickers/
├── SKILL.md                  # This file
├── README.md                 # Quick start guide
├── stickers.json             # Collection + usage data
├── stickers.json.example     # Empty template
├── import-sticker-pack.sh    # Bulk import
├── auto-tag-stickers.sh      # Emoji → emotion
├── random-sticker.sh         # Context-based selection
└── check-collection.sh       # Stats viewer
```

## stickers.json 文件结构

```json
{
  "collected": [
    {
      "file_id": "CAACAgEAAxUAAWmq...",
      "emoji": "🌙",
      "set_name": "pa_dKjUP9P2dt4k...",
      "added_at": "2026-03-06T23:31:00Z",
      "tags": ["goodnight", "sleep", "night", "warm", "gentle"],
      "used_count": 3,
      "last_used": "2026-03-07T00:24:00Z"
    }
  ],
  "usage_log": [
    {
      "file_id": "...",
      "sent_at": "2026-03-07T00:24:00Z",
      "context": "User saying goodnight",
      "message_id": "2599"
    }
  ],
  "stats": {
    "total_collected": 124,
    "total_sent": 15,
    "last_sent_at": "2026-03-07T00:24:00Z",
    "messages_since_last_sticker": 0
  },
  "config": {
    "min_messages_between_stickers": 2,
    "max_messages_between_stickers": 5,
    "enabled": true
  }
}
```

## 使用原则

**像人类一样使用贴纸：**
- 贴纸用于增强情感表达，而非替代文字
- 使用贴纸要适度且富有意义
- 晚安/早安时优先使用贴纸
- 庆祝场合、幽默对话或表达同情时适合使用贴纸
- 技术性回复或数据报告时可以不使用贴纸

**发送频率：**
- 默认：每2到5条消息后发送一张贴纸
- 特殊场合（如问候）可调整发送频率
- 使用`messages_since_last_sticker`变量记录上次发送贴纸的时间

## 示例：晚安消息流程

```bash
# 1. Agent detects "goodnight" intent
# 2. Select random goodnight sticker
FILE_ID=$(bash /path/to/random-sticker.sh "goodnight")

# 3. Send via OpenClaw (from agent code)
message(action=sticker, target=<chat_id>, stickerId=[$FILE_ID])

# 4. (Optional) Track usage manually
jq --arg fid "$FILE_ID" \
   '(.collected[] | select(.file_id == $fid) | .used_count) += 1' \
   stickers.json > stickers.json.tmp && \
   mv stickers.json.tmp stickers.json
```

---

**使用原则：**贴纸的使用应自然流畅，避免显得机械。收集用户偏好，定期更换贴纸内容，并尊重对话的节奏。