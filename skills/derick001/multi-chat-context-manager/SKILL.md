---
name: multi-chat-context-manager
description: 这是一个用于存储和检索每个频道/用户对话上下文的命令行工具（CLI）。
version: 1.0.2
author: skill-factory
metadata:
  openclaw:
    requires:
      bins:
        - python3
---
# 多聊天上下文管理器

## 功能介绍

这是一个简单的命令行（CLI）工具，用于存储、检索和清除聊天记录的上下文信息。上下文数据以 JSON 格式保存，键值为频道/用户/线程 ID。它只是一个实用工具库，而非自动集成插件。

## 使用场景

- 当你需要手动为每个频道或用户存储聊天历史记录时
- 当你需要为脚本提供一个简单的键值存储机制来保存上下文信息时
- 当你在构建自定义集成系统并需要持久化聊天上下文时

## 使用方法

存储聊天记录：
```bash
python3 scripts/context_manager.py store --channel "telegram-123" --user "user-456" --message "Hello" --response "Hi there"
```

检索上下文：
```bash
python3 scripts/context_manager.py retrieve --channel "telegram-123" --user "user-456"
```

清除上下文：
```bash
python3 scripts/context_manager.py clear --channel "telegram-123"
```

列出所有上下文：
```bash
python3 scripts/context_manager.py list
```

## 示例

### 示例 1：存储和检索聊天记录

存储：
```bash
python3 scripts/context_manager.py store --channel "discord-general" --user "john" --message "What is AI?" --response "AI is artificial intelligence."
```

检索：
```bash
python3 scripts/context_manager.py retrieve --channel "discord-general" --user "john"
```

输出：
```json
{
  "channel_id": "discord-general",
  "user_id": "john",
  "history": [{"message": "What is AI?", "response": "AI is artificial intelligence."}
}
```

## 系统要求

- Python 3.x
- 无需依赖任何外部库

## 限制

- 这只是一个 CLI 工具，不具备自动集成功能
- 不会自动拦截来自平台的消息
- 数据以明文 JSON 格式存储（未加密）
- 不支持并发访问时的文件锁定机制
- 必须在脚本或工作流程中手动调用该工具