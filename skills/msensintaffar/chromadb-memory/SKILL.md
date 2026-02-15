---
name: chromadb-memory
description: 通过ChromaDB实现长期记忆功能，同时利用本地Ollama模型生成的嵌入数据。系统会在每一步操作中自动插入相关的上下文信息。完全无需使用任何云服务API，实现完全自托管的运行模式。
version: 1.0.0
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

# ChromaDB内存

ChromaDB和本地Ollama嵌入技术共同支持长期语义记忆功能，完全无需依赖云端服务。

## 功能概述

- **自动回忆**：在每个代理轮次开始前，系统会使用用户输入的消息查询ChromaDB，并自动插入相关上下文信息。
- **`chromadb_search`工具**：用于对ChromaDB中的数据集进行手动语义搜索。
- **100%本地化**：嵌入数据由Ollama（nomic-embed-text模型生成，存储在ChromaDB中）。

## 先决条件

1. **已安装并运行ChromaDB**（建议使用Docker部署）：
   ```bash
   docker run -d --name chromadb -p 8100:8000 chromadb/chroma:latest
   ```

2. **已安装并配置Ollama**（包含相应的嵌入模型）：
   ```bash
   ollama pull nomic-embed-text
   ```

3. **数据已索引**：使用与ChromaDB兼容的索引器将数据添加到集合中。

## 安装步骤

```bash
# 1. Copy the plugin extension
mkdir -p ~/.openclaw/extensions/chromadb-memory
cp {baseDir}/scripts/index.ts ~/.openclaw/extensions/chromadb-memory/
cp {baseDir}/scripts/openclaw.plugin.json ~/.openclaw/extensions/chromadb-memory/

# 2. Get your collection ID
curl -s http://localhost:8100/api/v2/tenants/default_tenant/databases/default_database/collections | python3 -c "import json,sys; [print(f'{c[\"id\"]}  {c[\"name\"]}') for c in json.load(sys.stdin)]"

# 3. Add to your OpenClaw config (~/.openclaw/openclaw.json):
```

```json
{
  "plugins": {
    "entries": {
      "chromadb-memory": {
        "enabled": true,
        "config": {
          "chromaUrl": "http://localhost:8100",
          "collectionId": "YOUR_COLLECTION_ID",
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

| 选项          | 默认值       | 说明                          |
|---------------|------------|---------------------------------------------|
| `chromaUrl`      | `http://localhost:8100` | ChromaDB服务器地址                     |
| `collectionId`    | *必填*      | ChromaDB集合的唯一标识符（UUID）                |
| `ollamaUrl`      | `http://localhost:11434` | Ollama API地址                        |
| `embeddingModel`   | `nomic-embed-text` | Ollama使用的嵌入模型                     |
| `autoRecall`     | `true`       | 启用自动回忆功能                         |
| `autoRecallResults` | `3`        | 每轮次自动回忆的最大结果数量                   |
| `minScore`      | `0.5`       | 最小相似度阈值（0-1范围内）                   |

## 工作原理

1. 用户发送消息。
2. 插件通过Ollama（nomic-embed-text模型，768维嵌入）将消息转换为嵌入数据。
3. 系统在ChromaDB中查询与消息最相似的记录。
4. 符合`minScore`条件的结果会被插入到代理的上下文中（标记为`<chromadb-memories>`）。
5. 代理根据这些信息生成相应的响应。

## 代币消耗

在最坏情况下，每次自动回忆操作会消耗约275个代币（3个结果 × 每个结果约300个字符 + 处理开销）。在20万条上下文数据范围内，这一消耗可以忽略不计。

## 调优建议

- **回忆效果不佳？** 将`minScore`提高至0.6或0.7。
- **缺少相关上下文？** 降低`minScore`至0.4，并将`autoRecallResults`增加到5。
- **仅需要手动搜索？** 将`autoRecall`设置为`false`，并使用`chromadb_search`工具进行搜索。

## 架构特点

- **完全本地化**：所有数据处理和存储都在本地完成，无需依赖OpenAI或云端服务。
- **数据安全**：用户的记忆信息仅存储在用户的硬件设备上。