---
name: memento
description: OpenClaw代理的本地持久化内存：用于捕获对话内容，通过大型语言模型（LLM）提取结构化信息，并在每个回合开始前自动调用相关知识。以隐私保护为核心原则，所有存储的数据都保存在本地SQLite数据库中。
metadata:
  version: "0.5.2"
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
# Memento — 为 OpenClaw 代理提供的本地持久化存储功能

Memento 为代理提供了长期存储能力。它能够捕获对话内容，利用大型语言模型（LLM）提取结构化信息，并在每次 AI 行动之前自动注入相关知识。

**所有存储的数据都保留在您的机器上——无需云同步或订阅服务。** 数据提取使用您配置的 LLM 提供商；若希望实现完全离线的操作，可以使用本地的 Ollama 模型。

> ⚠️ **隐私说明：** 当启用 `autoExtract` 时，对话片段会被发送到您配置的 LLM 提供商进行事实提取。如果您使用的是云服务（如 Anthropic、OpenAI、Mistral），这些文本会离开您的机器。若希望实现完全本地化的操作，请将 `extractionModel` 设置为 `ollama/<model>` 并确保 Ollama 在本地运行。

## 功能概述

1. **捕获** 每次对话内容，并按会话进行缓冲。
2. **提取** 通过可配置的 LLM 提取结构化信息（如偏好设置、决策、人物信息、待办事项）（需手动启用——详见隐私设置部分）。
3. **在每次 AI 行动之前**，利用 FTS5 关键词搜索和可选的语义嵌入（BGE-M3）来检索相关事实。
4. **保护隐私**：根据内容将事实分为“共享”、“私有”或“机密”三类；对于敏感类别（医疗、财务、凭证等），会进行严格限制。
5. **代理间知识共享**：共享的事实会附带来源标签；私有/机密事实不会在代理之间传递。

## 快速入门

安装插件后，重启代理网关，Memento 会自动开始捕获数据。默认情况下，数据提取功能是关闭的——请根据需要手动启用。

### 可选功能：语义搜索

为了提高检索效果，您可以下载一个本地的嵌入模型：

```bash
mkdir -p ~/.node-llama-cpp/models
curl -L -o ~/.node-llama-cpp/models/bge-m3-Q8_0.gguf \
  "https://huggingface.co/gpustack/bge-m3-GGUF/resolve/main/bge-m3-Q8_0.gguf"
```

## 环境变量

所有环境变量都是可选的——您只需要根据所使用的 LLM 提供商来设置相应的变量：

| 变量          | 需要时使用       |
|-----------------|--------------|
| `ANTHROPIC_API_KEY`   | 使用 `anthropic/*` 模型时   |
| `OPENAI_API_KEY`    | 使用 `openai/*` 模型时   |
| `MISTRAL_API_KEY`    | 使用 `mistral/*` 模型时   |
| `MEMENTO_API_KEY`    | 通用备用键       |
| `MEMENTO_WORKSPACE_MAIN` | 仅用于迁移时设置    |

对于 `ollama/*` 模型，无需 API 密钥（因为它们在本地进行推理）。

## 配置方法

在 `openclaw.json` 文件的 `plugins.entries.memento.config` 部分进行配置：

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

> `autoExtract: true` 是一个可选的配置项（默认值为 `false`）。启用后，对话片段会被发送到配置的 `extractionModel` 进行提取。若希望保持数据完全在本地，可以将其设置为 `false`。
> `autoQueryPlanning: true` 也是一个可选的配置项（默认值为 `false`）。启用后，每次检索前会执行一次快速的 LLM 调用，以扩展查询范围并识别相关类别——这会增加每次操作的 LLM 调用次数，但能提高检索精度。

## 数据存储

Memento 将所有数据存储在本地：

| 路径            | 存储内容                |
|-----------------|----------------------|
| `~/.engram/conversations.sqlite` | 主数据库：对话记录、事实信息、嵌入模型 |
| `~/.engram/segments/*.jsonl` | 人类可读的对话备份文件       |
| `~/.engram/migration-config.json` | 可选：迁移工作空间路径（仅用于初始化） |

`~/.engram` 目录的名称是项目早期名为 Engram 时的遗留名称，为避免破坏现有安装，该名称不会更改。

## 隐私与数据流

| 功能            | 数据是否离开机器？            | 详细说明                |
|-----------------|-------------------|----------------------|
| `autoCapture`       | ❌ 不会；数据仅保存在本地 SQLite 和 JSONL 文件中 |                          |
| `autoExtract`       | ⚠️ 会；如果使用云 LLM，则会将对话文本发送到配置的提供商 | 使用 `ollama/*` 可实现本地处理            |
| `autoRecall`       | ❌ 不会；数据仅从本地 SQLite 中读取       |                          |
| 机密信息          | ❌ 绝不会；从提取过程中过滤掉，不会发送到任何 LLM           |                          |
| 数据迁移         | ❌ 不会；仅读取本地工作空间文件并写入本地 SQLite     |                          |

## 数据迁移（从现有记忆文件中初始化）

数据迁移是一个**可选的、一次性**的过程，用于将数据从现有的代理记忆或 Markdown 文件中导入到 Memento 中。该过程由用户手动触发，不会自动执行。

### 数据迁移过程

迁移过程仅读取您在配置中明确指定的文件，不会扫描文件系统、读取任意文件或访问配置路径之外的内容。

### 设置步骤

1. 创建 `~/.engram/migration-config.json` 文件，或设置 `MEMENTO_WORKSPACE_MAIN` 变量：

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

干运行会显示所有将被读取的文件路径——请在继续之前仔细检查这些路径。

3. 执行实际的数据迁移操作：

```bash
npx tsx src/extraction/migrate.ts --all
```

### 安全注意事项

- 迁移过程仅读取您配置的文件路径范围内的文件。
- 提取出的事实会继承其原有的可见性分类（共享/私有/机密）。
- 机密级别的事实**绝不会** 被发送到云 LLM 提供商。
- 迁移配置文件是可选的；如果未配置，则迁移过程不会执行。
- 迁移脚本仅使用配置的 LLM 进行网络通信。

## 架构说明

- **捕获层**：拦截 `message:received` 和 `message:sent` 事件，对多轮对话内容进行缓冲。
- **提取层**：异步调用 LLM 进行数据提取，同时处理数据去重、记录事件发生次数、跟踪状态变化（`previous_value`），并维护知识图谱关系（包括带有 `causal_weight` 的因果边）。
- **存储层**：使用 SQLite 7 版本（推荐使用 `better-sqlite3`），支持 FTS5 全文搜索和可选的向量嵌入；知识图谱包含 `fact_relations` 及其对应的 `causal_weight`，支持多层聚类和状态变化跟踪（`previous_value`）。
- **检索层**：支持可选的 LLM 查询规划（`autoQueryPlanning`），采用多因素评分机制（最近性 × 频率 × 类别权重），通过 `before_prompt_build` 钩子注入查询结果。

## 系统要求

- OpenClaw 2026.2.20 或更高版本。
- Node.js 18 或更高版本。
- 需要您选择的 LLM 提供商的 API 密钥（用于数据提取；如果禁用了数据提取功能或使用 Ollama，则不需要 API 密钥）。
- 可选：使用 GPU 加速嵌入模型的搜索（若未启用 GPU，系统会自动切换到 CPU）。

## 安装方法

```bash
# From ClawHub
clawhub install memento

# Or for local development
git clone https://github.com/braibaud/Memento
cd Memento
npm install
```

注意：`better-sqlite3` 包含了在安装 `npm` 时编译的本地绑定库。这是 SQLite 访问的正常行为。