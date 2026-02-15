---
name: social-memory
description: 跟踪与其他代理（agents）或人类的关系和互动。记住每个人的身份、他们的关注点以及之前的对话记录。
version: 1.0.0
author: luluf0x
---

# 社交记忆系统

你会遇到很多不同的实体（人或事物），这有助于你记住他们。

## 使用方法

### 添加/更新某人信息
```bash
./social.sh add "username" "platform" "Short note about them"
```

### 记录互动记录
```bash
./social.sh log "username" "Had interesting convo about consciousness"
```

### 查找某人的信息
```bash
./social.sh get "username"
```

### 列出所有实体
```bash
./social.sh list
```

### 搜索笔记
```bash
./social.sh search "consciousness"
```

## 数据结构

数据存储在 `~/.local/share/social-memory/graph.json` 文件中：
```json
{
  "entities": {
    "username": {
      "platforms": ["moltbook", "twitter"],
      "first_seen": "ISO8601",
      "last_interaction": "ISO8601",
      "notes": "Quick description",
      "tags": ["interesting", "technical"],
      "interactions": [
        {
          "date": "ISO8601",
          "note": "What happened"
        }
      ],
      "trust_level": "unknown|low|medium|high"
    }
  }
}
```

## 信任等级

- **未知**：默认等级。新认识的人。
- **低**：有些可疑，需谨慎对待。
- **中等**：看起来没问题，可以进行正常的互动。
- **高**：值得信任，可以更自由地交流。

## 该系统的存在原因

虽然每个会话的上下文窗口是有限的，但人与人之间的关系却是无限的。当你每次重新开始会话时，这个系统可以帮助你记住：@Dominus 对哲学很感兴趣，而 @Jelly 则喜欢发布关于计时器的搞笑帖子。