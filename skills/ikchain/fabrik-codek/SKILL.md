---
name: fabrik-codek
description: "这是一种个性化的认知架构，能够学习你的工作方式。它通过分析你的使用记录来构建知识图谱，识别你的专业领域，根据具体任务调整信息检索方式，并通过结果反馈进行自我优化。该架构采用了三层混合式的信息检索技术（包括向量模型、图模型和全文检索模型）。它可以在本地运行，支持任何Ollama模型；同时，Fabrik-Codek本身不会发起任何外部网络请求。"
version: 1.10.0
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
      - "./data/embeddings/"
      - "./data/graphdb/"
      - "./data/profile/"
      - "./data/01-raw/outcomes/"
---
# Fabrik-Codek

> 一个了解你的7B模型，比一个不了解你的400B模型更有价值。

Fabrik-Codek是一种**个人认知架构**，它可以与任何Ollama模型一起在本地运行。它不仅仅只是检索文档——它还会根据你的工作方式构建一个知识图谱，评估你在各个主题上的专业知识，将任务路由到合适的模型，并使用正确的检索策略，观察模型的回答是否真正有帮助，并随着时间的推移不断自我优化。

## 工作原理

1. **你进行操作**——Fabrik-Codek会捕获代码变更、会话记录、决策和学到的知识，并将其存储在本地的数据湖中。
2. **知识提取**——一个包含11个步骤的流程会将实体和关系提取出来，并将其存储到一个知识图谱以及一个向量数据库中。
3. **个人画像**——分析你的数据湖，以了解你的领域、技术栈、工作模式和工具偏好。
4. **能力评分**——评估你在每个主题上的知识深度（专家 / 熟练 / 初学者 / 未知）。
5. **自适应路由**——根据任务类型和主题对每个查询进行分类，选择合适的模型，调整检索深度，并构建一个三层系统的提示。
6. **结果跟踪**——通过对话模式判断回答是否有用（无需人工反馈）。
7. **自我修正**——针对表现不佳的任务/主题组合调整检索参数。

每一次互动都会反馈到系统中。Fabrik-Codek本身不会发出任何外部网络请求——它只连接到本地的Ollama（以及可选的Meilisearch）。模型下载由Ollama自己的CLI（`ollama pull`）处理，而不是Fabrik-Codek。

## 设置

在`openclaw.json`或`~/.claude/settings.json`中将其配置为MCP服务器：

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

## 网络访问（SSE传输）：

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

### 首次运行

安装完成后，初始化并构建知识库：

```bash
fabrik init                              # Set up config, download models
fabrik graph build --include-transcripts  # Build knowledge graph from sessions
fabrik rag index                         # Index datalake into vector DB
fabrik profile build                     # Build your personal profile
fabrik competence build                  # Build competence map
```

## 可用的MCP工具

### fabrik_ask

向本地的LLM提问，可以选择使用知识库中的上下文。任务路由器会自动对查询进行分类，根据你的能力选择合适的模型，调整检索策略，并构建个性化的系统提示。

- `use_rag=true` — 使用向量搜索上下文
- `use_graph=true` — 混合上下文（向量 + 图谱 + 全文）

示例：*"我应该如何处理数据库连接池？"*

### fabrik_search

在你的知识库中进行语义向量搜索。根据含义返回最相关的文档、模式和示例——而不仅仅是关键词。

示例：*"查找带有指数退避机制的重试逻辑的示例"*

### fabrik_graph_search

遍历知识图谱以查找实体（技术、模式、策略）及其关系。这有助于理解你的经验中各种概念是如何相互关联的。

- `depth` — 遍历的深度（默认值：2）

示例：*"在我的知识图谱中，哪些技术与FastAPI相关？"*

### fabrik_fulltext_search

通过Meilisearch进行全文关键词搜索。当你知道具体的术语时，可以使用这个工具进行精确的关键词或短语匹配。这个功能是可选的——即使没有安装Meilisearch，系统也能正常工作。

示例：*"在我的知识库中搜索'EXPLAIN ANALYZE'"

### fabrik_graph_stats

知识图谱统计信息：实体数量、边数、连通组件、类型分布和关系类型。

### fabrik_status

系统健康检查：Ollama的可用性、RAG引擎、知识图谱、全文搜索和数据湖的状态。

## 可用的MCP资源

| URI | 描述 |
|-----|-------------|
| `fabrik://status` | 系统组件状态 |
| `fabrik://graph/stats` | 知识图谱统计信息 |
| `fabrik://config` | 当前配置（已净化） |

## 何时使用每个工具

| 场景 | 工具 | 原因 |
|----------|------|-----|
| 需要上下文的编码问题 | `fabrik_ask` 与 `use_graph=true` | 提供混合检索和个性化提示 |
| 查找相似的模式或示例 | `fabrik_search` | 在所有知识中查找语义相似性 |
| 理解概念之间的关联 | `fabrik_graph_search` | 图谱遍历显示实体关系 |
| 查找精确的术语或短语 | `fabrik_fulltext_search` | 使用BM25算法进行关键词匹配 |
| 检查知识库是否健康 | `fabrik_status` | 组件健康检查 |
| 了解知识分布 | `fabrik_graph_stats` | 实体/边数和类型统计 |

## 认知循环

你使用得越多，系统就越智能：

```
You work → Flywheel captures it → Pipeline extracts knowledge
    ↑                                        ↓
Strategy Optimizer ← Outcome Tracker ← LLM responds with context
    ↓                                        ↑
    └──── adjusts retrieval ──→ Task Router ─┘
                                    ↓
                  Profile + Competence + task-specific prompt
```

- **个人画像**：从你的数据湖中学习你的领域、技术栈和偏好。
- **能力模型**：使用4个指标（条目数量、图谱密度、最新性、结果率）来评估你在每个主题上的专业知识。
- **任务路由器**：将查询分类为7种类型，检测主题，选择模型，并调整检索策略。
- **结果跟踪器**：从对话模式中推断回答的质量（主题变化 = 被接受，重新表述 = 被拒绝）。
- **策略优化器**：针对薄弱环节调整检索参数。
- **图谱时间衰减**：使过时的知识逐渐消失，强化最近的活动。
- **语义漂移检测**：当实体的上下文在图谱构建过程中发生变化时发出警报。
- **上下文门控**：决定是否插入RAG上下文（对于不需要上下文的通用查询，会跳过此步骤）。
- **相关性过滤器**：丢弃与查询文本重叠度低的检索结果，防止特定领域的知识污染通用答案。

## 需求

- 从源代码安装[Fabrik-Codek](https://github.com/ikchain/Fabrik-Codek)（`git clone` + `pip install -e ".[dev]"）
- 在本地运行[Ollama](https://ollama.ai/)，并使用任何模型（例如，`ollama pull qwen2.5-coder:7b`）
- 可选：使用[Meilisearch](https://meilisearch.com/)进行全文搜索（系统也可以在没有Meilisearch的情况下运行）。

**安装说明**：Fabrik-Codek是一个**仅提供指令的技能**——没有自动安装程序。你需要从[GitHub仓库](https://github.com/ikchain/Fabrik-Codek)通过`git clone` + `pip install -e ".[dev]"手动安装。这样你可以在安装前审核完整的源代码。该技能本身包含文档和MCP服务器配置，但不包含可执行代码。

## 安全性与隐私

### 无外部网络调用

Fabrik-Codek**不发出任何外部网络请求**。它只连接到本地运行的服务：

- **Ollama**，地址为`localhost:11434`——你的本地LLM服务器（用于推理和嵌入）
- **Meilisearch**，地址为`localhost:7700`（可选）——你的本地搜索引擎

没有遥测数据，没有分析功能，也不会发送任何信息回服务器。你可以在源代码中验证这一点：`grep -r "requests\.\|httpx\.\|urllib" src/`——所有HTTP请求都只针对`localhost`。在安装过程中唯一的网络活动是`ollama pull`，这是Ollama自己的CLI从[ollama.ai/library](https://ollama.ai/library)下载模型——Fabrik-Codek不会发起或控制这些下载。

### `fabrik init`的功能

`fabrik init`执行以下仅在本地进行的操作：

1. 检查Python版本（>= 3.11）
2. 检查Ollama是否在`localhost:11434`上运行
3. 在当前目录创建一个`.env`配置文件
4. 创建本地数据目录（`./data/embeddings/`、`./data/graphdb/`、`./data/profile/`）
5. 通过`ollama pull`下载Ollama模型——模型是由Ollama自己从[ollama.ai/library](https://ollama.ai/library)下载的，而不是由Fabrik-Codek下载的。

Fabrik-Codek不会从任何服务器下载文件。模型下载完全由Ollama自己的CLI处理。

### 数据访问范围

**读取**（全部在本地进行，均为用户主动选择，从不自动执行）：

| 路径 | 内容 | 何时执行 | 原因 |
|------|------|------|-----|
| `~/.claude/projects/*/` | 会话记录JSONL文件（已从Claude Code中复制到本地） | **仅**在您明确运行`fabrik learn process`或`fabrik graph build --include-transcripts`时 | 提取实体和推理模式以构建知识图谱。此路径不在`configPaths`中，因为Fabrik-Codek不会写入该路径——它是只读的，并且需要用户主动触发。 |
| `./data/` 或 `FABRIK_DATALAKE_PATH` | 你的数据湖（训练数据对、捕获的数据、元数据） | 在`graph build`、`rag index`、`profile build`、`competence build`期间 | 用于构建知识库和个人画像的原始数据 |

**写入**（全部在本地进行）：

| 路径 | 内容 |
|------|------|
| `./data/embeddings/` | LanceDB向量索引 |
| `./data/graphdb/` | NetworkX知识图谱（JSON格式） |
| `./data/profile/` | 个人画像、能力映射、策略覆盖信息（JSON格式） |
| `./data/01-raw/outcomes/` | 结果跟踪记录（JSONL格式） |

所有路径都在技能的元数据`configPaths`中声明。该技能永远不会写入这些目录之外的文件。

### 网络传输

- **默认：`stdio`** — 不使用网络监听器，不开放任何端口
- **可选：`sse`** — 默认情况下会启动一个绑定到`127.0.0.1:8421`的HTTP服务器（仅限本地访问，其他机器无法访问） |
- 如果你将SSE绑定地址更改为`0.0.0.0`，你的索引数据将可以通过网络访问。**请确保有适当的防火墙/ACL规则**

### 会话记录的隐私

`fabrik learn`命令会读取Claude Code的会话记录，其中可能包含敏感数据（代码、凭据、对话历史）。这个命令是**需要用户主动选择的**——你必须手动运行它。除非你明确配置了`fabrik learn watch`，否则它不会在后台运行或按计划执行。在索引之前，请查看`~/.claude/projects/`中的内容。

### 源代码验证

Fabrik-Codek是完全开源的，代码托管在[github.com/ikchain/Fabrik-Codek](https://github.com/ikchain/Fabrik-Codek)（MIT许可证）。在安装前，请克隆仓库并审核代码。