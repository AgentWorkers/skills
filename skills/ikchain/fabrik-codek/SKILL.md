---
name: fabrik-codek
description: "面向开发者的认知架构：超个性化引擎（个人画像、能力模型、自适应任务分配、结果跟踪），采用三层混合检索技术（向量数据 + 知识图谱 + 全文检索）。一个拥有70亿参数的模型，其价值远超过一个拥有4000亿参数的模型；该模型完全基于本地计算，无需依赖任何云服务。"
version: 1.5.0
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
    configPaths:
      - "~/.claude/projects/*"
      - "./data/embeddings/"
      - "./data/graphdb/"
    install:
      - kind: pip
        package: fabrik-codek
        bins: [fabrik]
---
# Fabrik-Codek – 专为开发者设计的本地认知架构

Fabrik-Codek 是一种 **认知架构**，它整合了感知、记忆、推理、学习与行动等功能，其运作方式类似于人类开发者通过不断实践积累专业知识的过程。与仅能检索文本的普通 RAG（Retrieval As Code）工具不同，Fabrik-Codek 结合了三种检索方式：向量搜索（语义搜索）、知识图谱遍历（关系型搜索）以及全文搜索（基于关键词或 BM25 的搜索），并通过“互惠排名融合”（Reciprocal Rank Fusion, RRF）技术将这些方式有机地结合在一起。该系统通过持续收集用户的使用数据，并将这些数据反馈到后续的查询中，从而实现自我优化。

**工作原理**：当你运行 `fabrik learn process` 命令时，Fabrik-Codek 会读取你本地的 Claude Code 会话记录文件（位于 `~/.claude/projects/` 目录下，这些文件为 JSON 格式），并从中提取结构化的知识信息（如模式、决策内容、调试策略等）。这些信息会被存储在本地向量数据库（LanceDB，位于 `./data/embeddings/`）和本地知识图谱（NetworkX，位于 `./data/graphdb/`）中。当你通过 MCP 工具进行查询时，Fabrik-Codek 会采用混合检索机制，为你的 AI 代理提供丰富的项目背景信息——不仅仅是简单的关键词匹配，还包括对你代码库中各种概念之间关系的深入理解。在整个过程中，没有任何数据会被传出你的机器。

## 设置

Fabrik-Codek 作为 MCP 服务器运行。你可以在 `openclaw.json` 配置文件中对其进行配置：

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

若需要通过网络进行访问（使用 SSE 传输协议），请参考以下配置：

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
用于在知识库中进行语义向量搜索。当你需要查找与项目知识相关联的文档、模式或示例时，可以使用该工具。  
**示例**：在知识库中搜索“仓库模式实现”的相关内容。

### `fabrik_graph_search`  
用于在知识图谱中搜索实体（如技术、模式、策略）及其之间的关系。该工具有助于你理解代码库中各个概念之间的联系。  
**示例**：在知识图谱中查找与 FastAPI 相关的实体。

### `fabrik_fulltext_search`  
通过 Meilisearch 实现的全文关键词搜索。当你知道要查找的具体关键词或短语时，可以使用该工具进行精确匹配。该工具需要 Meilisearch 在本地运行（可选，系统也可在没有 Meilisearch 的情况下正常工作）。  
**示例**：在知识库中搜索“retry exponential backoff”这个术语。

### `fabrik_ask`  
你可以向本地大型语言模型（LLM）提出编程问题，并根据需要选择是否使用知识库中的背景信息作为查询的上下文。  
- 设置 `use_rag=true` 可以利用向量搜索的上下文；  
- 设置 `use_graph=true` 可以结合向量搜索和知识图谱的信息来获取更丰富的查询结果。  
**示例**：询问 Fabrik 如何利用知识库中的信息来实现依赖注入。

### `fabrik_graph_stats`  
用于获取知识图谱的统计信息，包括实体数量、关系类型以及图谱的复杂度等。

### `fabrik_status`  
用于检查系统的运行状态，包括 Ollama 的可用性、RAG 引擎、知识图谱、全文搜索功能以及数据湖的状态。

### `fabrik_profile`  
用于创建或查看你的个人资料。该功能会分析你的使用数据，并生成相应的系统提示，以便 LLM 能根据你的实际开发环境和偏好来提供更准确的回答。  
**示例**：创建我的个人资料 或 查看我的个人资料。

## 使用场景

- **需要项目背景信息？** 使用 `fabrik_search` 进行语义相似性搜索，或使用 `fabrik_fulltext_search` 进行精确关键词匹配。  
- **探索概念之间的关系？** 使用 `fabrik_graph_search` 遍历知识图谱。  
- **有编程问题？** 使用 `fabrik_ask` 并根据需要设置 `use_rag` 或 `use_graph` 来获取更详细的答案。  
- **检查系统配置？** 使用 `fabrik_status` 确认所有组件均正常运行。

## 所需条件

- 已安装 [Fabrik-Codek](https://github.com/ikchain/Fabrik-Codek)（通过 `pip install fabrik-codek` 安装）。  
- 需要在本地运行 [Ollama](https://ollama.ai/)，并下载相应的模型（例如 `ollama pull qwen2.5-coder:7b`）。

## 安全性与隐私保护

- **100% 本地化**：所有数据都存储在你的机器上，不涉及任何外部 API 调用或云服务。  
- **无需输入密码**：Fabrik-Codek 仅连接到本地的 Ollama 实例（地址为 `localhost:11434`）。  
- **无外部接口**：该工具不与任何外部服务交互。  
- **数据存储路径**：会话记录文件存储在 `~/.claude/projects/` 目录下（这些文件已经是 JSON 格式）；索引后的数据会被保存在 `./data/embeddings/`（向量数据库）和 `./data/graphdb/`（知识图谱）中。  
- **会话数据管理**：`fabrik learn` 命令是可选的，由用户手动触发，不会自动进行后台监控。在索引会话记录之前，请确保其中不包含敏感信息。  
- **网络安全性**：默认传输方式为 `stdio`（不涉及网络传输）；若使用 SSE 传输（`--transport sse`），默认绑定到 `127.0.0.1` 地址。请确保防火墙/访问控制规则设置得当，以防止索引数据被泄露到网络中。  
- **开源信息**：源代码完全公开，可在 [github.com/ikchain/Fabrik-Codek](https://github.com/ikchain/Fabrik-Codek) 查看（采用 MIT 许可协议）。安装前请确认 pip 包的源代码与 GitHub 仓库中的代码一致。