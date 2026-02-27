---
name: fabrik-codek
description: "这是一种个人认知架构，能够学习你的工作方式。它通过分析你的使用记录构建知识图谱，分析你的专业技能，并根据具体任务调整信息检索方式；同时，它还能通过反馈结果来自我优化。该架构采用了三层混合式的信息检索技术（包括向量模型、图模型和全文检索模型）。该架构完全基于本地计算，且可以与任何Ollama模型配合使用。"
version: 1.7.1
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
      - "./data/profile/"
    install:
      - kind: pip
        package: fabrik-codek
        bins: [fabrik]
---
# Fabrik-Codek

> 一个了解你的7B模型，比一个不了解你的400B模型更有价值。

Fabrik-Codek是一个**个人认知架构**，它可以与任何Ollama模型一起在本地运行。它不仅仅能够检索文档——它还会根据你的工作方式构建一个知识图谱，评估你在各个主题上的专业知识，将任务路由到合适的模型，并使用正确的检索策略，观察模型的响应是否真正有帮助，并且会随着时间的推移不断自我优化。

## 工作原理

1. **你进行操作**——Fabrik-Codek会捕获代码变更、会话记录、决策以及学习成果，并将这些信息存储在本地的数据湖中。
2. **知识提取**——一个包含11个步骤的流程会将实体和关系提取出来，并将其存储到一个知识图谱中，同时还会生成一个向量数据库。
3. **个人画像**——分析你的数据湖，以了解你的领域、技术栈、工作模式以及工具偏好。
4. **能力评分**——评估你在每个主题上的知识深度（专家 / 熟练 / 初学者 / 未知）。
5. **自适应路由**——根据任务类型和主题对查询进行分类，选择合适的模型，调整检索深度，并生成个性化的系统提示。
6. **结果跟踪**——通过对话模式来判断响应是否有用（无需人工反馈）。
7. **自我修正**——对于表现不佳的任务/主题组合，会调整检索参数。

每一次交互都会反馈到系统中。没有任何数据会离开你的机器。

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

### 网络访问（SSE传输）：

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

向本地的大语言模型（LLM）提问，并可以选择从知识库中获取上下文信息。任务路由器会自动对查询进行分类，根据你的能力选择合适的模型，调整检索策略，并生成个性化的系统提示。
- `use_rag=true` — 使用向量搜索上下文
- `use_graph=true` — 混合上下文（向量 + 知识图谱 + 全文）

示例：*"我应该如何处理数据库连接池？"*

### fabrik_search

在你的知识库中进行语义向量搜索。根据含义返回最相关的文档、模式和示例——而不仅仅是关键词。

示例：*"查找带有指数退避机制的重试逻辑的示例"*

### fabrik_graph_search

遍历知识图谱以查找实体（技术、模式、策略）及其之间的关系。这有助于理解概念在你的经验中的关联方式。
- `depth` — 遍历的深度（默认值：2）

示例：*"在我的知识图谱中，哪些技术与FastAPI相关？"*

### fabrik_fulltext_search

通过Meilisearch进行全文关键词搜索。当你知道具体的术语时，可以使用这个工具进行精确的关键词或短语匹配。这个工具是可选的——即使没有安装Meilisearch，系统也能正常工作。

示例：*"在我的知识库中搜索‘EXPLAIN ANALYZE’"*

### fabrik_graph_stats

知识图谱统计信息：实体数量、边数、连通组件、类型分布以及关系类型。

### fabrik_status

系统健康检查：Ollama的可用性、RAG引擎、知识图谱、全文搜索以及数据湖的状态。

## 可用的MCP资源

| URI | 描述 |
|-----|-------------|
| `fabrik://status` | 系统组件状态 |
| `fabrik://graph/stats` | 知识图谱统计信息 |
| `fabrik://config` | 当前配置（已清理） |

## 何时使用每个工具

| 场景 | 工具 | 原因 |
|----------|------|-----|
| 需要上下文的编码问题 | `fabrik_ask` with `use_graph=true` | 提供混合检索和个性化提示 |
| 查找相似的模式或示例 | `fabrik_search` | 在所有知识中查找语义相似性 |
| 理解概念之间的关联 | `fabrik_graph_search` | 通过图谱遍历显示实体之间的关系 |
| 查找确切的术语或短语 | `fabrik_fulltext_search` | 使用BM25算法进行关键词匹配 |
| 检查知识库是否健康 | `fabrik_status` | 组件健康检查 |
| 了解知识分布 | `fabrik_graph_stats` | 实体/边的数量和类型 |

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

- **个人画像** 从你的数据湖中学习你的领域、技术栈和偏好。
- **能力模型** 根据4个指标（条目数量、图谱密度、更新频率、结果成功率）来评估你的专业知识。
- **任务路由器** 将查询分为7种类型，检测主题，选择模型，并调整检索策略。
- **结果跟踪** 通过对话模式判断响应的质量（主题变化 = 被接受，重新表述 = 被拒绝）。
- **策略优化器** 为表现不佳的任务/主题组合调整检索参数。
- **图谱时效性衰减** 使过时的知识逐渐消失，强化最近的活动。
- **语义漂移检测** 在知识图谱构建过程中，当实体的上下文发生变化时发出警报。

## 需求

- 从[GitHub仓库](https://github.com/ikchain/Fabrik-Codek)下载[Fabrik-Codek](https://github.com/ikchain/Fabrik-Codek)的源代码，并使用`git clone`和`pip install -e ".[dev]"进行安装。
- 确保[Ollama](https://ollama.ai/)已在本地运行（例如，使用`ollama pull qwen2.5-coder:7b`）。
- 可选：安装[Meilisearch](https://meilisearch.com/)以支持全文搜索（即使不安装Meilisearch，系统也能正常工作）。

**安装说明**：Fabrik-Codek是从[GitHub仓库](https://github.com/ikchain/Fabrik-Codek)直接安装的，而不是通过PyPI。这样你可以在安装前审核源代码。`pip install`中的元数据用于依赖项解析，但实际安装是从克隆的仓库中进行的。

## 安全性与隐私

### 无外部网络请求

Fabrik-Codek**不进行任何出站网络请求**。它仅连接到你本地运行的服务：
- **Ollama** 在`localhost:11434`——你的本地LLM服务器
- **Meilisearch** 在`localhost:7700`（可选）——你的本地搜索引擎

没有遥测数据，没有分析功能，也不会发送任何信息到外部。你可以在源代码中验证这一点：`grep -r "requests\.\|httpx\.\|urllib" src/`，会发现没有出站请求。

### `fabrik init`的作用

`fabrik init`执行以下仅在本地进行的操作：
1. 检查Python版本（>= 3.11）
2. 检查Ollama是否在`localhost:11434`上运行
3. 在当前目录创建一个`.env`配置文件
4. 创建本地数据目录（`./data/embeddings/`、`./data/graphdb/`、`./data/profile/`）
5. 通过`ollama pull`下载Ollama模型——模型是由Ollama自己从[ollama.ai/library](https://ollama.ai/library)下载的，而不是由Fabrik-Codek下载的。

Fabrik-Codek不会从任何服务器下载文件。模型的下载完全由Ollama的CLI处理。

### 数据访问范围

**读取**（全部在本地进行，均为可选）：

| 路径 | 内容 | 时机 |
|------|------|------|
| `~/.claude/projects/*/` | 会话记录JSONL文件（已经存储在Claude Code的磁盘上） | 仅在运行`fabrik learn process`或`fabrik graph build --include-transcripts`时 |
| `./data/` 或 `FABRIK_DATALAKE_PATH` | 你的数据湖（训练数据对、捕获的数据、元数据） | 在执行`graph build`、`rag index`、`profile build`、`competence build`时 |

**写入**（全部在本地进行）：

| 路径 | 内容 |
|------|------|
| `./data/embeddings/` | LanceDB向量索引 |
| `./data/graphdb/` | NetworkX知识图谱（JSON格式） |
| `./data/profile/` | 个人画像、能力映射、策略覆盖信息（JSON格式） |
| `./data/01-raw/outcomes/` | 结果跟踪记录（JSONL格式） |

所有路径都在技能的元数据`configPaths`中进行了声明。该技能永远不会将这些数据写入其他目录。

### 网络传输

- **默认：`stdio`** — 不启动网络监听器，不开放端口，不暴露任何信息
- **可选：`sse`** — 默认情况下会启动一个绑定到`127.0.0.1:8421`的HTTP服务器（仅限本地访问，其他机器无法访问）
- 如果将SSE绑定地址更改为`0.0.0.0`，你的索引数据将可以通过网络访问。**请勿在没有适当防火墙/ACL规则的情况下这样做**

### 会话记录的隐私

`fabrik learn`命令会读取Claude Code的会话记录，其中可能包含敏感数据（代码、凭证、对话历史）。这个命令是**可选的**——你必须手动运行它。除非你明确配置了`fabrik learn watch`，否则它不会在后台运行或按计划执行。在索引之前，请查看`~/.claude/projects/`中的内容。

### 源代码验证

Fabrik-Codek是完全开源的，代码托管在[github.com/ikchain/Fabrik-Codek](https://github.com/ikchain/Fabrik-Codek)（MIT许可证）。在安装前，请克隆仓库并进行审核。