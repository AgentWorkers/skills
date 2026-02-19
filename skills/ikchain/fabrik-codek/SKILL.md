---
name: fabrik-codek
description: "面向开发者的认知架构：采用三层混合检索机制（向量检索 + 知识图谱 + 全文搜索），能够从用户的编码过程中学习，并随着时间的推移变得越来越智能。该架构可将任何 Ollama 模型与用户积累的项目知识相结合。完全本地化运行，无需依赖任何云服务。"
version: 1.3.0
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
# Fabrik-Codek – 开发者的本地认知架构

Fabrik-Codek 是一种 **认知架构**，它将感知、记忆、推理、学习与行动紧密结合在一起，类似于人类开发者随着时间的推移积累专业知识的方式。与仅能检索文本的普通 RAG（Retrieval As Code）工具不同，Fabrik-Codek 结合了三种检索方式：向量搜索（语义搜索）、知识图谱遍历（关系搜索）和全文搜索（基于关键词或 BM25 算法的搜索），并通过 **互惠排名融合（Reciprocal Rank Fusion, RRF）** 技术将这三种方式融合在一起。该系统通过一个数据循环机制不断优化自身性能，该机制会记录用户的使用行为，并将这些信息反馈到后续的查询中。

**工作原理**：当你运行 `fabrik learn process` 命令时，Fabrik-Codek 会读取你本地的 Claude Code 会话记录文件（位于 `~/.claude/projects/*` 目录下，这些文件已经是 JSON 格式，存储在本地磁盘上），并从中提取结构化的知识信息（如模式、决策和调试策略）。这些信息会被存储在本地向量数据库（LanceDB，位于 `./data/embeddings/`）和本地知识图谱（使用 NetworkX 构建，位于 `./data/graphdb/`）中。当你通过 MCP 工具进行查询时，Fabrik-Codek 会采用混合检索方式，为你的 AI 代理提供丰富的项目上下文——不仅仅是简单的关键词匹配，还包括对代码库中各个概念之间关联关系的理解。在整个过程中，没有任何数据会被输出到外部。

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

如果你需要通过网络进行访问（使用 SSE 传输协议），请参考以下配置：

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
用于在知识库中进行语义向量搜索。当你需要从项目积累的知识中查找相关文档、模式或示例时，可以使用此工具。

**示例**：**“在我的知识库中搜索仓库模式的实现方式”。**

### `fabrik_graph_search`
用于在知识图谱中搜索实体（技术、模式、策略）及其之间的关系。这有助于你理解各个概念之间的联系。

**示例**：**“在知识图谱中查找与 FastAPI 相关的实体”。**

### `fabrik_fulltext_search`
通过 Meilisearch 进行全文关键词搜索。当你知道要查找的具体关键词或短语时，可以使用此工具进行精确匹配。需要注意的是，Meilisearch 需要在本机运行（可选；系统也可以在没有 Meilisearch 的情况下正常工作）。

**示例**：**“在知识库中搜索 ‘retry exponential backoff’”。**

### `fabrik_ask`
可以向本地的 LLM（Large Language Model）提出编程问题，并可以选择性地结合知识库中的相关信息。设置 `use_rag=true` 可以使用向量搜索上下文；设置 `use_graph=true` 可以使用混合搜索方式（结合向量搜索、知识图谱和全文搜索）。

**示例**：**“利用知识库中的信息，询问如何实现依赖注入”。**

### `fabrik_graph_stats`
用于获取知识图谱的统计信息，包括实体数量、关系类型以及图谱的复杂度等。

### `fabrik_status`
用于检查系统运行状态：包括 Ollama 的可用性、RAG 引擎、知识图谱、全文搜索功能以及数据湖的状态。

## 使用场景

- **需要项目上下文？** 使用 `fabrik_search` 进行语义相似性查询，或使用 `fabrik_fulltext_search` 进行精确关键词匹配。
- **探索概念之间的关系？** 使用 `fabrik_graph_search` 遍历知识图谱。
- **有编程问题？** 使用 `fabrik_ask` 并设置相应的选项（`use_rag` 或 `use_graph`）以获取包含上下文的答案。
- **检查系统配置？** 使用 `fabrik_status` 确认所有组件都在正常运行。

## 必备条件

- 已安装 [Fabrik-Codek](https://github.com/ikchain/Fabrik-Codek)（通过 `pip install fabrik-codek` 安装）。
- 本地已运行 [Ollama](https://ollama.ai/)，并下载了相应的模型（例如 `ollama pull qwen2.5-coder:7b`）。

## 安全性与隐私

- **100% 本地化**：所有数据都存储在本地机器上，不涉及任何外部 API 调用、遥测数据传输或云服务依赖。
- **无需密码**：Fabrik-Codek 仅连接到本地的 Ollama 实例（地址为 `localhost:11434`）。
- **无外部接口**：该工具不会访问任何外部服务。
- **数据存储路径**：会话记录文件从 `~/.claude/projects/*` 读取（这些文件已经是 JSON 格式，存储在本地磁盘上）；索引后的数据会被写入 `./data/embeddings/`（向量数据库）和 `./data/graphdb/`（知识图谱）。这些路径已在技能的元数据中明确指定。
- **会话数据管理**：`fabrik learn` 命令是手动触发的，用户可以选择是否执行；索引前会先对会话记录进行审查，以确保不包含敏感信息。
- **网络访问**：默认使用 `stdio` 协议（无需网络连接）；如果使用 SSE 传输协议（`--transport sse`），默认绑定到 `127.0.0.1` 地址。请确保防火墙/访问控制规则设置正确，以防止索引数据被泄露到网络中。
- **开源信息**：源代码完全开源，可在 [github.com/ikchain/Fabrik-Codek](https://github.com/ikchain/Fabrik-Codek) 查看（采用 MIT 许可证）。安装前请确认 pip 包的源代码与 GitHub 仓库中的代码一致。