---
name: openclaw-memory-brain
description: "OpenClaw插件用于个人记忆管理：具备自动捕获功能（并带有安全防护机制），支持基于语义的本地搜索，以及安全的文本编辑/删除操作。"
---
# openclaw-memory-brain

这是一个**OpenClaw Gateway插件**，它的工作方式类似于一个轻量级的“个人大脑”：
- 它会监听传入的消息；
- 当某些触发条件或主题出现时，会捕获可能具有价值的笔记；
- 允许通过搜索工具进行语义化的检索。

所有数据都存储在本地（使用JSONL格式），并且可以选择是否对敏感信息进行加密处理。

## 功能介绍

- **事件监听**：`message_received` → 可选地捕获消息；
- **检索工具**：`brain_memory_search({ query, limit })`；
- **保存功能**：`/remember-brain <text>`（用于显式保存笔记）。

## 捕获规则（默认设置）

默认情况下，该插件仅**显式捕获**满足以下条件的消息：
- 消息长度达到最低要求（`minChars`，默认为80个字符）；
- 消息中包含特定的触发词（推荐格式：“Merke dir:”）。

如果您希望更积极地捕获消息，请在配置文件中设置`requireExplicit: false`（但不建议在涉及安全性的环境中使用此设置）。

## 安装方法

### 在ClawHub中安装
```bash
clawhub install openclaw-memory-brain
```

### 开发者使用方法
```bash
openclaw plugins install -l ~/.openclaw/workspace/openclaw-memory-brain
openclaw gateway restart
```

## 搜索功能

示例调用方式：
```json
{ "query": "Anthropic reset schedule", "limit": 5 }
```

## 配置设置
```json
{
  "plugins": {
    "entries": {
      "openclaw-memory-brain": {
        "enabled": true,
        "config": {
          "storePath": "~/.openclaw/workspace/memory/brain-memory.jsonl",
          "dims": 256,
          "redactSecrets": true,
          "capture": {
            "minChars": 80,
            "requireExplicit": false,
            "explicitTriggers": ["merke dir", "remember this", "notiere", "keep this"],
            "autoTopics": ["entscheidung", "decision"]
          },
          "defaultTags": ["brain"]
        }
      }
    }
  }
}
```

## 安全性

- 该插件在存储数据前会自动对敏感信息（如令牌、密钥等）进行加密处理；
- 如果您需要严格的隐私保护且仅允许显式捕获消息，请使用`openclaw-memory-docs`插件。