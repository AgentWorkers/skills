---
name: fabrik-codek
description: "面向开发者的认知架构：一种混合式的RAG（向量 + 知识图谱）系统，能够从您的编码过程中学习，并随着时间的推移变得越来越智能。该系统可将任何Ollama模型与您积累的项目知识相结合。完全基于本地运行，无需依赖任何云服务。"
version: 1.0.0
homepage: https://github.com/ikchain/Fabrik-Codek
user-invocable: true
metadata:
  clawdbot:
    requires:
      bins: [fabrik]
      anyBins: [python3, python]
    homepage: https://github.com/ikchain/Fabrik-Codek
    os: [macos, linux]
    emoji: "🧠"
    install:
      - kind: pip
        package: fabrik-codek
        bins: [fabrik]
---
# Fabrik-Codek – 专为开发者设计的本地认知架构

Fabrik-Codek 是一种 **认知架构**，它整合了感知、记忆、推理、学习与行动等功能，其运作方式类似于人类开发者通过不断实践积累经验的过程。与仅能检索文本的普通 RAG（Retrieval-Augmented Grammar）工具不同，Fabrik-Codek 能够构建一个包含实体及其关系的持久性知识图谱（涵盖技术、模式、决策等信息），并结合向量搜索技术进行高效查询。同时，该系统通过持续收集用户的使用数据来优化自身性能，并将这些数据反馈到未来的查询中。

**工作原理**：您正常编写代码，Fabrik-Codek 会监控您的开发过程，提取相关知识（如代码模式、决策、调试策略等），并将其存储在向量数据库（LanceDB）和知识图谱（NetworkX）中。通过混合检索机制，它能为 AI 代理提供深入的项目上下文理解——不仅仅是简单的关键词匹配，还包括对代码库中各种概念之间联系的全面理解。

## 设置

Fabrik-Codek 作为 MCP（Master Control Point）服务器运行。您可以在 `openclaw.json` 文件中配置相关设置：

```json
{
  "mcpServers": {
    "fabrik-codek": {
      "command": "fabrik",
      "args": ["mcp"]
    }
  }
}
```

若需要支持网络访问（使用 SSE 协议），请参考以下配置：

```json
{
  "mcpServers": {
    "fabrik-codek": {
      "command": "fabrik",
      "args": ["mcp", "--transport", "sse", "--port", "8421"]
    }
  }
}
```

## 可用工具

### `fabrik_search`
用于在知识库中进行语义向量搜索。当您需要查找相关文档、模式或项目经验中的示例时，可使用此工具。
**示例**：在知识库中搜索“仓库模式实现”的相关内容。

### `fabrik_graph_search`
用于在知识图谱中搜索实体（技术、模式、策略）及其之间的关系。该工具有助于您理解各种概念之间的关联。
**示例**：在知识图谱中查找与 FastAPI 相关的实体。

### `fabrik_ask`
向本地大语言模型（LLM）提出编程问题，并可结合知识库中的相关信息。设置 `use_rag=true` 以使用向量搜索机制，或设置 `use_graph=true` 以使用混合检索（向量 + 图谱）方式。
**示例**：利用知识库中的信息询问如何实现依赖注入。

### `fabrik_graph_stats`
用于获取知识图谱的统计信息，包括实体数量、关系类型及图谱的复杂度等。

### `fabrik_status`
用于检查系统运行状态：包括 Ollama 服务是否可用、RAG 引擎的运行情况、知识图谱的状态以及数据湖的运行状况。

## 使用场景

- **需要项目背景信息？** 使用 `fabrik_search` 查找相关知识。
- **探索概念之间的关联？** 使用 `fabrik_graph_search` 遍历知识图谱。
- **有编程问题？** 使用 `fabrik_ask` 并设置 `use_rag` 或 `use_graph` 以获取更详细的答案。
- **检查系统配置？** 使用 `fabrik_status` 确认所有组件均正常运行。

## 系统要求

- 已安装 [Fabrik-Codek](https://github.com/ikchain/Fabrik-Codek)（通过 `pip install fabrik-codek` 安装）。
- 需要在本地运行 [Ollama](https://ollama.ai/)，并下载相应的模型（例如 `ollama pull qwen2.5-coder:7b`）。

## 安全性与隐私保护

- **100% 本地化**：所有数据均存储在您的机器上，无外部 API 调用，无数据传输，也不依赖任何云服务。
- **无需密码**：Fabrik-Codek 仅连接到本地的 Ollama 服务器（地址：`localhost:11434`）。
- **无外部接口**：该工具不会访问任何外部服务。