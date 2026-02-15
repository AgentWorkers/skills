---
name: feishu-native-emoji
description: 提供了对 Feishu 原生表情符号集（例如 [Smile]、[Like]）的访问权限，以实现更真实的互动体验。
tags: [feishu, emoji, ui]
---

# 🎭 Feishu原生表情符号

该技能用于管理Feishu原生表情符号代码（例如 `[微笑]`、`[捂脸]`）的映射及使用方式，这些代码替代了标准的Unicode表情符号。

## 使用方式

该功能主要作为被动资源，用于让代理（Agent）在消息中添加个性化元素（即使用这些原生表情符号）。

### 资源文件
- `emoji_list.txt`：包含所有支持的表情符号代码的原始列表。

## 集成建议
在为Feishu构建消息时，建议优先使用 `emoji_list.txt` 中提供的代码。