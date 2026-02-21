---
name: fabrik-codek
description: "面向开发者的认知架构：采用三层混合检索技术（向量检索 + 知识图谱 + 全文搜索），并结合个人编程栈、技术架构及工具使用偏好进行个性化定制。该架构能够将任何 Ollama 模型与开发者积累的项目知识无缝整合。完全基于本地运行，无需依赖任何云服务。"
version: 1.4.0
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

Fabrik-Codek 是一种**认知架构**，它将感知、记忆、推理、学习与行动紧密结合在一起，类似于人类开发者通过不断实践积累专业知识的过程。与仅能检索文本的普通 RAG（Retrieval As Code）工具不同，Fabrik-Codek 结合了三种检索方式：向量搜索（语义搜索）、知识图谱遍历（关系搜索）和全文搜索（基于关键词或 BM25 的搜索），并通过“互惠排名融合”（Reciprocal Rank Fusion, RRF）技术将这些方法进行整合。该系统通过持续收集用户的使用数据，并将这些数据反馈到后续的查询中，从而不断提升自身的性能。

**工作原理**：当你运行 `fabrik learn process` 命令时，Fabrik-Codek 会读取你本地的 Claude Code 会话转录文件（位于 `~/.claude/projects/` 目录下，这些文件已经是 JSON 格式的文件），并从中提取结构化的知识信息（如模式、决策内容、调试策略等）。这些信息会被存储在本地向量数据库（LanceDB，位于 `./data/embeddings/`）和本地知识图谱（NetworkX，位于 `./data/graphdb/`）中。当你通过 MCP（Model-Based Computing Platform）工具进行查询时，Fabrik-Codek 会采用混合检索方式，为你的 AI 代理提供深入的项目上下文理解——不仅仅是简单的关键词匹配，还包括对你代码库中各种概念之间关系的理解。在整个过程中，没有任何数据会被传输到外部。

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

**如需网络访问（使用 SSE 传输协议）：**

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
用于在知识图谱中搜索实体（技术、模式、策略）及其之间的关系。你可以用它来理解各种概念之间的关联。  
**示例**：**“在知识图谱中查找与 FastAPI 相关的实体”。**

### `fabrik_fulltext_search`  
通过 Meilisearch 进行全文关键词搜索。当你知道要查找的具体关键词或短语时，可以使用此工具。需要先在本地运行 Meilisearch（可选，系统也可以在没有 Meilisearch 的情况下正常工作）。  
**示例**：**“在知识库中搜索‘retry exponential backoff’”。**

### `fabrik_ask`  
你可以向本地的大型语言模型（LLM）提出编程问题，并可以选择是否结合知识库中的相关信息。设置 `use_rag=true` 可以使用向量搜索的上下文，设置 `use_graph=true` 可以使用混合（向量 + 知识图谱 + 全文）的上下文。  
**示例**：**“利用知识库中的信息，询问如何实现依赖注入”。**

### `fabrik_graph_stats`  
用于获取知识图谱的统计信息，包括实体数量、关系类型以及图谱的复杂度等。**

### `fabrik_status`  
用于检查系统的运行状态，包括 Ollama 的可用性、RAG 引擎、知识图谱、全文搜索功能以及数据湖的状态。

### `fabrik_profile`  
用于创建或查看你的个人资料。该功能会分析你的使用数据，并生成相应的系统提示，以便 LLM 能够根据你的实际开发环境和偏好来提供更准确的回答。  
**示例**：**“创建我的个人资料”或“查看我的个人资料”。**

## 使用场景

- **需要项目上下文？** 使用 `fabrik_search` 进行语义相似性搜索，或使用 `fabrik_fulltext_search` 进行精确的关键词匹配。  
- **探索概念之间的关系？** 使用 `fabrik_graph_search` 遍历知识图谱。  
- **有编程问题？** 使用 `fabrik_ask` 并设置相应的参数（`use_rag` 或 `use_graph`）以获取更丰富的答案。  
- **检查系统配置？** 使用 `fabrik_status` 确认所有组件是否正常运行。  

## 所需条件

- 已安装 [Fabrik-Codek](https://github.com/ikchain/Fabrik-Codek)（通过 `pip install fabrik-codek` 安装）。  
- 需要在本地运行 [Ollama](https://ollama.ai/)，并下载相应的模型（例如 `ollama pull qwen2.5-coder:7b`）。  

## 安全性与隐私

- **100% 本地处理**：所有数据都存储在你的机器上，不涉及任何外部 API 调用或云服务。  
- **无需输入密码**：Fabrik-Codek 仅连接到本地的 Ollama 实例（地址为 `localhost:11434`）。  
- **无外部接口**：该工具不会访问任何外部服务。  
- **数据路径**：转录文件从 `~/.claude/projects/` 目录读取（文件已保存为 JSON 格式），索引后的数据分别存储在 `./data/embeddings/`（向量数据库）和 `./data/graphdb/`（知识图谱）中。这些路径已在技能的元数据中明确说明。  
- **会话数据管理**：`fabrik learn` 命令是可选的，由用户手动触发，不会自动进行后台监控。转录文件可能包含敏感的会话信息，在索引前请仔细审查。  
- **网络访问**：默认使用 `stdio` 协议（不涉及网络传输）；如果使用 SSE 传输（`--transport sse`），默认绑定到 `127.0.0.1` 地址。请确保防火墙/访问控制规则设置得当，以防止索引数据被泄露到网络中。  
- **开源信息**：源代码完全开源，可在 [github.com/ikchain/Fabrik-Codek](https://github.com/ikchain/Fabrik-Codek) 查看（采用 MIT 许可证）。安装前请确认 pip 包的源代码与 GitHub 仓库中的内容一致。