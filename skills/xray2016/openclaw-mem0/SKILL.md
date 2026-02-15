# OpenClaw Mem0 插件

OpenClaw 的 Mem0 集成模块为代理程序添加了智能的长期记忆功能，使它们能够自动记住用户偏好、信息以及之前的对话内容。

## 使用场景

- 当您希望代理程序在不同会话中记住用户信息（姓名、职位、偏好设置）时。
- 当您需要通过检索之前的交互记录来提供“无限上下文”时。
- 当您希望构建一个能够随时间学习的个性化助手时。
- 当您需要同时支持云托管（由第三方服务管理）和本地自托管（在本地服务器上运行）的记忆存储方案时。

## 设置

### 平台模式（推荐）

1. 在 [mem0.ai](https://mem0.ai) 获取免费的 API 密钥。
2. 将该插件添加到您的 OpenClaw 配置文件中：

```json
{
  "plugins": {
    "entries": {
      "openclaw-mem0": {
        "enabled": true,
        "config": {
          "mode": "platform",
          "apiKey": "your-mem0-api-key",
          "userId": "default-user"
        }
      }
    }
  }
}
```

### 开源模式（本地自托管）

您需要安装 `mem0ai` 包，并连接到自己的 Mem0 服务器：

```json
{
  "plugins": {
    "entries": {
      "openclaw-mem0": {
        "enabled": true,
        "config": {
          "mode": "open-source",
          "oss": {
            "vectorStore": {
              "provider": "chroma",
              "config": {
                "collectionName": "memories",
                "path": "./chroma_db"
              }
            }
          }
        }
      }
    }
  }
}
```

## 使用方法

该插件可自动运行（无需额外配置），同时也提供了手动操作工具。

### 自动功能

- **自动回忆**：在每个代理轮次开始前，它会从内存中检索相关内容并显示在系统提示中。
- **自动捕获**：在每个代理轮次结束后，它会分析对话内容并将关键信息存储到内存中。

### 手动工具

代理程序可以主动使用以下工具：

| 工具 | 描述 | 参数 |
|------|-------------|------------|
| `memory_store` | 显式保存信息 | `text`（字符串），`longTerm`（布尔值） |
| `memory_search` | 搜索内存中的内容 | `query`（字符串），`scope`（“session”或“long-term”） |
| `memory_get` | 通过 ID 获取内存中的信息 | `memoryId`（字符串） |
| `memory_list` | 列出所有内存中的信息 | `userId`（字符串） |
| `memory_forget` | 删除内存中的信息 | `memoryId`（字符串）或 `query`（字符串） |

### 示例

**用户**：“我下个月要搬到东京。”
*代理程序会自动记录这一信息。*

**两周后**
**用户**：“哪里有适合我告别晚餐的好餐厅？”
*代理程序会自动回忆起“用户即将搬到东京”的信息，并推荐当地的一家餐厅。*

## 插件结构

```
openclaw-mem0/
  package.json            # NPM package config (@xray2016/openclaw-mem0)
  index.ts                # Plugin implementation & tools
  lib/                    # Internal Mem0 client implementation
  SKILL.md                # This file
  README.md               # Detailed documentation
```

## 开发者

该插件由 @xRay2016 维护，基于原始的 Mem0 OpenClaw 集成版本进行了修改。