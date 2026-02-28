---
name: memento
description: OpenClaw代理的本地持久内存功能：该功能用于捕获对话内容，通过大型语言模型（LLM）提取结构化信息，并在每个决策回合之前自动调用相关知识。在数据隐私方面，所有存储的数据都严格保留在本地的SQLite数据库中。
metadata:
  version: "0.5.0"
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
# Memento — OpenClaw代理的本地持久化存储系统

Memento为OpenClaw代理提供了长期存储功能。它能够记录对话内容，利用大型语言模型（LLM）提取结构化信息，并在每次AI轮次开始前自动注入相关知识。

**所有存储的数据都保留在您的机器上——无需云同步或订阅服务。** 数据提取使用您配置的LLM提供商；如果您希望实现完全离线的操作，可以使用本地模型（如Ollama）。

> ⚠️ **隐私说明：** 当`autoExtract`功能启用时，对话片段会被发送到您配置的LLM提供商进行事实提取。如果您使用的是云服务提供商（如Anthropic、OpenAI、Mistral），相关文本会离开您的机器。为了实现完全本地化的操作，请将`extractionModel`设置为`ollama/<model>`，并确保Ollama在本地运行。

## 主要功能

1. **记录**每次对话内容，并按会话进行缓冲。
2. **提取**结构化信息（如偏好设置、决策结果、涉及的人物、待办事项），这些信息通过可配置的LLM进行提取（需用户选择是否启用此功能——详见隐私设置部分）。
3. **在每次AI轮次开始前**，通过FTS5关键词搜索及可选的语义嵌入（BGE-M3）功能检索相关事实。
4. **保护隐私**：根据内容将事实分为“共享”、“私有”或“机密”三类；对于敏感类别（如医疗、财务、凭证信息），会进行特殊处理。
5. **代理间知识共享**：共享的事实会附带来源标签；私有/机密事实不会在代理之间传递。

## 快速入门

安装插件后重启代理网关，Memento将自动开始数据捕获。默认情况下，数据提取功能是关闭的——请根据需要手动启用。

### 可选功能：语义搜索

为了提高检索效率，您可以下载一个本地嵌入模型：

```bash
mkdir -p ~/.node-llama-cpp/models
curl -L -o ~/.node-llama-cpp/models/bge-m3-Q8_0.gguf \
  "https://huggingface.co/gpustack/bge-m3-GGUF/resolve/main/bge-m3-Q8_0.gguf"
```

## 环境变量

所有环境变量都是可选的——您只需要根据所使用的LLM提供商来设置相应的变量：

| 变量            | 使用场景           |
|------------------|-------------------|
| `ANTHROPIC_API_KEY`     | 使用Anthropic系列模型进行提取       |
| `OPENAI_API_KEY`     | 使用OpenAI系列模型进行提取       |
| `MISTRAL_API_KEY`     | 使用Mistral系列模型进行提取       |
| `MEMENTO_API_KEY`     | 适用于所有提供商的通用备用键       |
| `MEMENTO_WORKSPACE_MAIN` | 仅用于迁移：代理工作空间的路径       |

对于`ollama/*`系列模型，无需API密钥（因为它们在本地进行推理）。

## 配置方法

在`openclaw.json`文件中的`plugins.entries.memento.config`部分进行配置：

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
      "crossAgentRecall": true
    }
  }
}
```

> `autoExtract: true`表示明确启用该功能（默认值为`false`）。启用后，对话片段会被发送到配置的`extractionModel`进行LLM驱动的事实提取。如需保持数据完全本地化，可将其设置为`false`。

## 数据存储方式

Memento将所有数据存储在本地：

| 路径                | 存储内容                |
|------------------|----------------------|
| `~/.engram/conversations.sqlite` | 主数据库：存储对话记录、事实信息和嵌入数据   |
| `~/.engram/segments/*.jsonl` | 人类可读的对话备份文件         |
| `~/.engram/migration-config.json` | 可选：用于数据迁移的工作空间路径       |

`~/.engram`目录的名称是项目早期（名为Engram时）遗留下来的；为避免破坏现有安装，该名称不会更改。

## 隐私与数据流处理

| 功能                | 数据是否离开机器？            | 详细说明                |
|------------------|------------------|----------------------|
| `autoCapture`（默认值：`true`）    | ❌ 不会；数据仅保存在本地SQLite和JSONL文件中   |
| `autoExtract`（默认值：`false`）    | ⚠️ 会；如果使用云LLM，则会将对话文本发送给配置的提供商 | 使用`ollama/*`模型时，数据保持本地化   |
| `autoRecall`（默认值：`true`）    | ❌ 不会；数据仅从本地SQLite读取         |
| 机密信息            | ❌ 绝不会；这些信息在提取过程中会被过滤掉       |
| 数据迁移            | ❌ 不会；数据仅从本地工作空间文件读取并写入本地SQLite |

## 数据迁移（从现有内存文件中恢复数据）

数据迁移是一个**可选的、一次性**的过程，用于从现有的代理内存或Markdown文件中恢复Memento数据。此过程由用户手动触发，不会自动执行。

### 数据迁移过程

迁移过程仅会读取您在配置文件中明确指定的文件，不会扫描您的文件系统、读取任意文件或访问配置路径之外的内容。

### 设置步骤

1. 创建`~/.engram/migration-config.json`文件，或设置`MEMENTO_WORKSPACE_MAIN`变量：

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

2. **务必先进行一次测试运行**，以确认哪些文件会被读取：

```bash
npx tsx src/extraction/migrate.ts --all --dry-run
```

测试运行会显示所有将被读取的文件路径——请在正式迁移前仔细检查这些文件。

3. 执行实际的数据迁移操作：

```bash
npx tsx src/extraction/migrate.ts --all
```

### 安全注意事项

- 迁移过程仅读取您配置的文件路径范围内的文件。
- 提取出的信息会继承原有的可见性分类（共享/私有/机密）。
- 机密级别的信息**绝不会**被发送到云端的LLM提供商。
- 数据迁移配置文件是可选的；如果未配置，则迁移过程不会执行。
- 迁移脚本仅限于访问配置的LLM服务，不会进行任何网络操作。

## 架构概述

- **数据捕获层**：拦截`message:received`和`message:sent`事件，将多轮对话内容进行缓冲。
- **数据提取层**：使用异步LLM进行提取，同时处理数据去重、事件追踪和时间模式检测。
- **数据存储层**：使用SQLite（推荐使用`better-sqlite3`版本）进行存储，并支持FTS5全文搜索及可选的向量嵌入功能。
- **数据检索层**：通过`before_prompt_build`钩子实现多因素评分（基于数据的新近性、出现频率和类别权重）。

## 系统要求

- OpenClaw版本需达到2026.2.20或更高。
- 需要Node.js 18或更高版本的运行环境。
- 需要为您选择的LLM提供商配置API密钥（用于数据提取；如果禁用了数据提取功能或使用Ollama，则无需此密钥）。
- **可选**：建议使用GPU以加速嵌入搜索；若未启用GPU，系统会自动切换到CPU进行搜索。

## 安装说明

```bash
# From ClawHub
clawhub install memento

# Or for local development
git clone https://github.com/braibaud/Memento
cd Memento
npm install
```

注意：`better-sqlite3`库在安装过程中会自动编译相应的本地绑定代码。这是SQLite访问的正常行为。