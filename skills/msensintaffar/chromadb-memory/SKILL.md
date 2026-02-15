---
name: chromadb-memory
description: 通过 ChromaDB 实现长期记忆功能，同时利用本地的 Ollama 嵌入模型。自动回忆功能会在每轮游戏中注入相关的上下文信息。无需使用任何云服务 API，完全实现本地化部署（即完全自托管）。
version: 1.2.0
author: matts
homepage: https://github.com/openclaw/openclaw
metadata:
  openclaw:
    emoji: "🧠"
    requires:
      bins: ["curl"]
    category: "memory"
tags:
  - memory
  - chromadb
  - ollama
  - vector-search
  - local
  - self-hosted
  - auto-recall
---
# ChromaDB内存管理

ChromaDB和本地的Ollama嵌入模型共同支持长期语义记忆功能，完全无需依赖任何云服务。

## 功能概述

- **自动回忆**：在每个代理轮次开始前，系统会使用用户输入的消息查询ChromaDB，并自动插入相关的上下文信息。
- **`chromadb_search`工具**：用于对ChromaDB中的数据进行手动语义搜索。
- **100%本地化**：嵌入模型使用Ollama（nomic-embed-text），向量存储则依赖于ChromaDB。

## 先决条件

1. **ChromaDB**必须已运行（建议使用Docker部署）：
   ```bash
   docker run -d --name chromadb -p 8100:8000 chromadb/chroma:latest
   ```

2. **Ollama**需配备相应的嵌入模型：
   ```bash
   ollama pull nomic-embed-text
   ```

3. **ChromaDB中需有索引化的文档**：可以使用任何与ChromaDB兼容的索引工具来构建文档集合。

## 安装步骤

```bash
# 1. Copy the plugin extension
mkdir -p ~/.openclaw/extensions/chromadb-memory
cp {baseDir}/scripts/index.ts ~/.openclaw/extensions/chromadb-memory/
cp {baseDir}/scripts/openclaw.plugin.json ~/.openclaw/extensions/chromadb-memory/

# 2. Add to your OpenClaw config (~/.openclaw/openclaw.json):
```

```json
{
  "plugins": {
    "entries": {
      "chromadb-memory": {
        "enabled": true,
        "config": {
          "chromaUrl": "http://localhost:8100",
          "collectionName": "longterm_memory",
          "ollamaUrl": "http://localhost:11434",
          "embeddingModel": "nomic-embed-text",
          "autoRecall": true,
          "autoRecallResults": 3,
          "minScore": 0.5
        }
      }
    }
  }
}
```

```bash
# 4. Restart the gateway
openclaw gateway restart
```

## 配置选项

| 选项          | 默认值        | 说明                          |
|----------------|--------------|---------------------------------------------|
| `chromaUrl`      | `http://localhost:8100`   | ChromaDB服务器地址                      |
| `collectionName` | `longterm_memory`  | 集合名称（会自动生成UUID，重启索引后仍可保留）       |
| `collectionId`    | —            | 集合UUID（可选，用于替代默认值）                 |
| `ollamaUrl`      | `http://localhost:11434`   | Ollama API地址                        |
| `embeddingModel`   | `nomic-embed-text`   | Ollama使用的嵌入模型                     |
| `autoRecall`     | `true`         | 启用自动回忆功能                         |
| `autoRecallResults` | `3`          | 每轮次自动显示的最大回忆结果数量                |
| `minScore`      | `0.5`         | 最小相似度阈值（0-1范围内）                   |

## 工作原理

1. 用户发送消息后，插件会通过Ollama（nomic-embed-text模型，768维嵌入）将消息转换为向量格式。
2. 系统在ChromaDB中查询与用户消息最相似的文档。
3. 符合`minScore`条件的结果会被添加到代理的上下文中（标记为`<chromadb-memories>`）。
4. 代理随后会使用这些相关信息进行响应。

## 成本分析

在最坏情况下，每次自动回忆操作会消耗约275个令牌（3个结果 × 每个结果约300个字符 + 处理开销）。考虑到上下文窗口通常包含数万个条目，这一成本可以忽略不计。

## 调优建议

- 如果回忆结果过于杂乱或干扰过多，可将`minScore`提高至0.6或0.7。
- 如果缺少所需上下文，可将`minScore`降低至0.4，并将`autoRecallResults`增加到5。
- 若仅需要手动搜索功能，可将`autoRecall`设置为`false`，并使用`chromadb_search`工具。

## 架构特点

- 该系统不依赖OpenAI或任何云服务，所有数据都存储在本地硬件上。

```
User Message → Ollama (embed) → ChromaDB (query) → Context Injection
                                                  ↓
                                          Agent Response
```

（注：由于代码块内容为空，此处保留了原有的结构框架。实际代码应填充到相应的位置。）