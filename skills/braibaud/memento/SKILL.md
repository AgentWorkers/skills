---
name: memento
description: OpenClaw代理的本地持久内存功能：该功能用于捕获对话内容，通过大型语言模型（LLM）提取结构化信息，并在每个决策回合之前自动检索相关知识。在保障用户隐私的前提下，所有存储的数据都保留在本地的SQLite数据库中。
metadata:
  version: "0.6.0"
  author: braibaud
  license: MIT
  repository: https://github.com/braibaud/Memento
  openclaw:
    emoji: "🧠"
    kind: plugin
    requires:
      node: ">=18.0.0"
      optionalEnv:
        - name: ANTHROPIC_API_KEY
          when: "Using anthropic/* models for extraction"
        - name: OPENAI_API_KEY
          when: "Using openai/* models for extraction"
        - name: MISTRAL_API_KEY
          when: "Using mistral/* models for extraction"
        - name: MEMENTO_API_KEY
          when: "Generic fallback for any provider"
        - name: CLAUDE_CODE_OAUTH_TOKEN
          when: "OpenClaw OAuth token for model routing (auto-used when running inside OpenClaw)"
        - name: MEMENTO_WORKSPACE_MAIN
          when: "Migration only: path to agent workspace for bootstrapping"
        - name: MEMENTO_AGENT_PATHS
          when: "Deep consolidation CLI: explicit agent:path mappings"
      dataFiles:
        - path: "~/.engram/conversations.sqlite"
          purpose: "Main database — conversations, facts, embeddings (local only, never uploaded)"
        - path: "~/.engram/segments/*.jsonl"
          purpose: "Human-readable conversation backups (local only)"
        - path: "~/.engram/migration-config.json"
          purpose: "Optional: agent workspace paths for one-time migration bootstrap"
    install:
      - id: npm
        kind: node
        package: "@openclaw/memento"
        label: "Install Memento plugin (npm)"
    extensions:
      - "./src/index.ts"
  keywords:
    - memory
    - knowledge-base
    - recall
    - conversation
    - extraction
    - embeddings
    - sqlite
    - privacy
    - local
    - cross-agent
---
# Memento — OpenClaw代理的本地持久化内存

Memento为你的代理提供了长期存储功能。它能够捕获对话内容，利用大型语言模型（LLM）提取结构化信息，并在每次AI轮次开始前自动注入相关知识。

**所有存储的数据都保留在你的机器上——无需云同步或订阅。** 数据提取使用你配置的LLM提供商；如果希望完全在本地进行操作，可以使用Ollama模型。

> ⚠️ **隐私声明：** 当`autoExtract`功能启用时，对话片段会被发送到你配置的LLM提供商进行信息提取。如果你使用的是云服务提供商（如Anthropic、OpenAI、Mistral），这些文本会离开你的机器。为了实现完全本地化的操作，请将`extractionModel`设置为`ollama/<model>`，并确保Ollama在本地运行。

## 功能概述

1. **捕获** 每次对话的片段，并按会话进行缓冲。
2. **提取** 通过可配置的LLM提取结构化信息（如偏好设置、决策内容、相关人员、待办事项等）（此功能为可选，详见隐私设置部分）。
3. **在每次AI轮次开始前**，利用FTS5关键字搜索及可选的语义嵌入（BGE-M3）来检索相关信息。
4. **保护隐私**：根据内容将信息分类为“共享”、“私有”或“机密”，并对敏感类别（如医疗、财务、凭证信息）进行严格保护。
5. **代理间知识共享**：共享的信息会附带来源标签；私有/机密信息永远不会在代理之间传递。

## 快速入门

安装插件后重启代理网关，Memento将自动开始数据捕获。提取功能默认是关闭的——请在准备好后再手动启用。

### 可选功能：语义搜索

为了提高检索效果，你可以下载一个本地嵌入模型：

```bash
mkdir -p ~/.node-llama-cpp/models
curl -L -o ~/.node-llama-cpp/models/bge-m3-Q8_0.gguf \
  "https://huggingface.co/gpustack/bge-m3-GGUF/resolve/main/bge-m3-Q8_0.gguf"
```

## 环境变量

所有环境变量都是可选的——你只需要根据所使用的LLM提供商来设置相应的变量：

| 变量          | 使用场景           |
|------------------|-------------------|
| `ANTHROPIC_API_KEY`    | 使用anthropic系列模型进行提取       |
| `OPENAI_API_KEY`    | 使用openai系列模型进行提取       |
| `MISTRAL_API_KEY`    | 使用mistral系列模型进行提取       |
| `MEMENTO_API_KEY`    | 通用备用键，适用于任何提供商       |
| `MEMENTO_WORKSPACE_MAIN` | 仅用于初始化时，指定代理工作空间的路径 |

对于`ollama`系列模型，无需API密钥（因为它们在本地进行推理）。

## 配置方法

在`openclaw.json`文件的`plugins.entries.memento.config`部分进行配置：

```json
{
  "memento": {
    "autoCapture": true,
    "extractionModel": "anthropic/claude-sonnet-4-6",
    "extraction": {
      "autoExtract": true,
      "minTurnsForExtraction": 3
    },
    "recall": {
      "autoRecall": true,
      "maxFacts": 20,
      "crossAgentRecall": true,
      "autoQueryPlanning": false
    }
  }
}
```

> `autoExtract: true` 是一个可选功能（默认值为`false`）。启用该功能后，对话片段会被发送到配置的`extractionModel`进行提取。如果希望所有数据都保留在本地，可以将其设置为`false`。
> `autoQueryPlanning: true` 是一个可选功能（默认值为`false`）。启用该功能后，在每次检索前会快速调用LLM，通过同义词扩展查询范围并确定相关类别——这会略微增加每次轮次的计算成本。

## 数据存储

Memento将所有数据存储在本地：

| 路径            | 存储内容                |
|------------------|----------------------|
| `~/.engram/conversations.sqlite` | 主数据库：存储对话记录、事实信息和嵌入数据   |
| `~/.engram/segments/*.jsonl` | 人类可读的对话备份文件         |
| `~/.engram/migration-config.json` | 可选：用于初始化时的工作空间路径     |

## 隐私与数据流

| 功能            | 数据是否会离开机器？            | 详细说明                |
|------------------|----------------------|-------------------------|
| `autoCapture`       | ❌ 不会；数据仅保存在本地SQLite和JSONL文件中 |                          |
| `autoExtract`       | ⚠️ 会；如果使用云LLM，则会将对话文本发送到配置的提供商 | 使用`ollama`模型时数据保留在本地             |
| `autoRecall`       | ❌ 不会；数据仅从本地SQLite读取         |                          |
| 机密信息         | ❌ 绝不会；这些信息会被从提取过程中过滤掉       |                          |
| 数据迁移         | ❌ 不会；数据仅从本地工作空间文件读取并保存在本地SQLite中 |                          |

## 数据迁移（从现有内存文件初始化）

数据迁移是一个**可选的、一次性**的过程，用于将数据从现有的代理内存或Markdown文件中导入到Memento中。该过程由用户手动触发，不会自动执行。

### 数据迁移过程

迁移过程**仅**读取你在配置中明确指定的文件，不会扫描文件系统、读取任意文件或访问配置路径之外的内容。

### 设置步骤

1. 创建`~/.engram/migration-config.json`文件，或设置`MEMENTO_WORKSPACE_MAIN`路径：

```json
{
  "agents": [
    {
      "agentId": "main",
      "workspace": "/path/to/your-workspace",
      "paths": ["MEMORY.md", "memory/*.md"]
    }
  ]
}
```

2. **务必先进行** 干运行（dry-run），以确认哪些文件会被读取：

```bash
npx tsx src/extraction/migrate.ts --all --dry-run
```

干运行会显示所有会被读取的文件路径——在正式迁移之前请仔细检查这些文件。

3. 执行实际的数据迁移操作：

```bash
npx tsx src/extraction/migrate.ts --all
```

### 安全注意事项

- 迁移过程仅读取你配置的文件路径范围内的文件。
- 提取出的信息会保留其原有的可见性分类（共享/私有/机密）。
- 机密级别的信息**绝对不会**被发送到云LLM提供商。
- 迁移配置文件是可选的；如果没有配置文件，迁移过程将不会执行。
- 迁移脚本仅使用配置的LLM进行数据提取，不会访问网络资源。

## 架构说明

- **捕获层**：监听`message:received`和`message:sent`事件，对多轮对话片段进行缓冲处理。
- **提取层**：异步调用LLM进行信息提取，同时处理数据去重、记录数据出现次数、维护时间状态变化（`previous_value`），并建立知识图谱关系（包括带有`causal_weight`的因果关系）。
- **存储层**：使用SQLite 7版本（better-sqlite3）进行数据存储，支持FTS5全文搜索和可选的向量嵌入；知识图谱包含`fact_relations`（带有`causal_weight`），支持多层聚类和时间状态跟踪（`previous_value`）。
- **检索层**：支持可选的LLM查询规划（`autoQueryPlanning`），采用多因素评分机制（基于信息的新颖性、频率和类别权重），通过`before_prompt_build`钩子注入查询结果。

## 系统要求

- OpenClaw版本需达到2026.2.20或更高。
- 需要Node.js 18或更高版本。
- 需要为你选择的LLM提供商配置API密钥（用于数据提取；如果禁用了数据提取功能或使用Ollama，则无需API密钥）。
- 可选：为了加速嵌入搜索，建议使用GPU；如果无法使用GPU，系统会自动切换到CPU处理。

## 安装方法

```bash
# From ClawHub
clawhub install memento

# Or for local development
git clone https://github.com/braibaud/Memento
cd Memento
npm install
```

注意：`better-sqlite3`在安装过程中会自动编译相应的本地绑定库。这是SQLite访问的正常行为。