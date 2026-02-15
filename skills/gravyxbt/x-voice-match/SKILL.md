---
name: x-voice-match
description: 分析某个 Twitter/X 账号的发布风格，并生成与该账号风格相符的原创帖子。适用于用户希望发布具有自己特色的 X 账号内容、分析其发布模式，或确保所有帖子保持一致的风格时。该功能支持与 Bird CLI 的集成。
---

# X 语音匹配

该工具分析 Twitter/X 账号的发帖模式，生成与账号所有者独特语音相匹配的原创内容。

## 快速入门

**步骤 1：分析账号**
```bash
cd /data/workspace/skills/x-voice-match
python3 scripts/analyze_voice.py @username [--tweets 50] [--output profile.json]
```

**步骤 2：生成帖子**
```bash
python3 scripts/generate_post.py --profile profile.json --topic "your topic" [--count 3]
```

或者使用一站式解决方案：
```bash
python3 scripts/generate_post.py --account @username --topic "AI agents taking over" --count 5
```

## 分析内容

该工具会分析以下方面：

- **内容长度**：推文的字符数量、多条推文的使用情况（单行 vs 多行）
- **语气特征**：幽默风格、讽刺、自嘲、尖锐程度
- **主题范围**：加密货币、人工智能、科技、表情包、个人生活、时事
- **互动模式**：引用他人观点 vs 发表原创内容、引发他人反应的推文、对话开场白
- **语言风格**：特定短语、俚语使用、表情符号的运用、标点符号的格式
- **内容类型**：观察性评论、观点性言论、表情包、多条推文的系列、问题、个人故事

## 输出格式

### 语音档案（JSON）
```json
{
  "account": "@gravyxbt_",
  "analyzed_tweets": 50,
  "patterns": {
    "avg_length": 85,
    "length_distribution": {"short": 0.6, "medium": 0.3, "long": 0.1},
    "uses_threads": false,
    "humor_style": "self-deprecating, ironic",
    "topics": ["crypto", "AI agents", "memes", "current events"],
    "engagement_type": "reactive QT heavy",
    "signature_phrases": ["lmao", "fr", "based"],
    "emoji_usage": "minimal, strategic",
    "punctuation": "lowercase, casual"
  }
}
```

### 生成的帖子
返回 1- 条帖子，并附带置信度评分及生成理由。

## 与现有工具的集成

支持与 Bird CLI（`/data/workspace/bird.sh`）配合使用：
```bash
# Fetch fresh tweets for analysis
./bird.sh user-tweets @gravyxbt_ -n 50 > recent_tweets.txt
python3 scripts/analyze_voice.py --input recent_tweets.txt
```

## 帖子类型模板

请参阅 [references/post-types.md](references/post-types.md) 以了解常见的 X 账号帖子类型：
- 观察性评论
- 观点性言论
- 自嘲式幽默
- 加密货币相关评论
- 引发他人反应的推文
- 问题类帖子

## 高级用法

### 更新语音档案
定期重新分析以捕捉语言风格的演变：
```bash
python3 scripts/analyze_voice.py @username --update profile.json
```

### 按类型生成帖子
```bash
python3 scripts/generate_post.py --profile profile.json --type "hot-take" --topic "crypto"
```

### 批量生成
```bash
python3 scripts/generate_post.py --profile profile.json --batch topics.txt --output posts.json
```

## 工作流程

1. **首次使用**：对 30-50 条推文进行完整分析
2. **生成帖子**：提供主题，获取 3-5 个符合该风格的选项
3. **用户选择**：选择最佳选项或根据反馈进行迭代
4. **定期更新**：每月分析一次，或在语音风格发生重大变化时重新分析

## 提示

- **最低推文数量**：基本分析需要 30 条推文，更高精度分析需要 50 条以上
- **时效性很重要**：最近的推文更能反映当前的语言风格
- **主题相关性**：生成的帖子在账号常涉及的主题上效果最佳
- **置信度评分**：低于 70% 的帖子可能不够真实，需重新生成