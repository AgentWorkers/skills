---
name: memento
description: OpenClaw代理的本地持久化内存：用于记录对话内容，通过大型语言模型（LLM）提取结构化信息，并在每个回合之前自动检索相关知识。遵循隐私优先原则，所有存储的数据都保存在本地SQLite数据库中。
metadata:
  version: "0.3.2"
  author: braibaud
  license: MIT
  repository: https://github.com/braibaud/Memento
  openclaw:
    emoji: "🧠"
    kind: plugin
    requires:
      node: ">=18.0.0"
      env:
        - ANTHROPIC_API_KEY
        - OPENAI_API_KEY
        - MISTRAL_API_KEY
        - MEMENTO_API_KEY
        - MEMENTO_WORKSPACE_MAIN
      config:
        - "~/.engram/conversations.sqlite"
        - "~/.engram/migration-config.json"
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

Memento为你的代理提供了长期存储功能。它能够捕获对话内容，利用大型语言模型（LLM）提取结构化信息，并在每次AI轮次之前自动注入相关知识。

**所有存储的数据都保留在你的机器上——无需云同步或订阅服务。** 数据提取使用你配置的LLM提供商；如果希望实现完全本地化的操作，可以使用本地模型（如Ollama）。

> ⚠️ **隐私说明：** 当`autoExtract`功能启用时，对话片段会被发送到你配置的LLM提供商进行信息提取。如果你使用的是云服务提供商（如Anthropic、OpenAI、Mistral），这些数据将会离开你的机器。为了实现完全本地化的操作，请将`extractionModel`设置为`ollama/<model>`，并确保Ollama在本地运行。

## 功能概述

1. **捕获** 每次对话内容，并按会话进行缓冲。
2. **提取** 通过可配置的LLM提取结构化信息（如偏好设置、决策结果、涉及的人员、待办事项等）（此功能为可选，详见隐私设置部分）。
3. **在每次AI轮次之前**，利用FTS5关键词搜索及可选的语义嵌入（BGE-M3）功能检索相关信息。
4. **保护隐私**：根据内容将信息分类为“共享”、“私有”或“机密”；对于敏感类别（如医疗、财务、凭证信息），会进行严格的权限控制。
5. **代理间知识共享**：共享的信息会附带来源标签；私有/机密信息不会在代理之间传递。

## 快速入门

安装插件后重启代理网关，Memento将自动开始工作。默认情况下，数据提取功能是关闭的——请根据需要手动启用。

### 可选功能：语义搜索

为了提升信息检索效果，你可以下载一个本地嵌入模型：

```bash
mkdir -p ~/.node-llama-cpp/models
curl -L -o ~/.node-llama-cpp/models/bge-m3-Q8_0.gguf \
  "https://huggingface.co/gpustack/bge-m3-GGUF/resolve/main/bge-m3-Q8_0.gguf"
```

## 环境变量

所有环境变量都是可选的——你只需要根据所使用的LLM提供商来设置相应的变量：

| 变量            | 需要设置的情况            |
|------------------|----------------------|
| `ANTHROPIC_API_KEY`    | 使用Anthropic系列模型进行数据提取时            |
| `OPENAI_API_KEY`    | 使用OpenAI系列模型进行数据提取时            |
| `MISTRAL_API_KEY`    | 使用Mistral系列模型进行数据提取时            |
| `MEMENTO_API_KEY`    | 适用于所有提供商的通用备用键            |
| `MEMENTO_WORKSPACE_MAIN` | 仅用于迁移：代理工作空间的路径            |

对于`ollama/*`模型，无需API密钥（因为它们在本地进行推理）。

## 配置方法

将以下配置添加到`openclaw.json`文件中的`plugins.entries.memento.config`部分：

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

> `autoExtract: true`表示明确启用该功能（默认值为`false`）。启用后，对话片段会被发送到配置的`extractionModel`进行基于LLM的信息提取。如果你希望保持数据完全本地化，可以省略此配置或将其设置为`false`。

## 数据存储方式

Memento将所有数据存储在本地：

| 路径            | 存储内容                |
|------------------|----------------------|
| `~/.engram/conversations.sqlite` | 主数据库：存储对话记录、事实信息和嵌入数据           |
| `~/.engram/segments/*.jsonl` | 人类可读的对话备份文件             |
| `~/.engram/migration-config.json` | 可选：用于数据迁移的工作空间路径           |

`~/.engram`目录的名称是项目早期（称为Engram时）遗留下来的。为避免破坏现有安装，该名称不会更改。

## 隐私与数据流

| 功能                | 数据是否会离开机器？            | 详细说明                |
|------------------|----------------------|----------------------|
| `autoCapture`（默认值：`true`） | ❌ 不会；数据仅保存在本地SQLite和JSONL文件中     |
| `autoExtract`（默认值：`false`） | ⚠️ 会；如果使用云LLM服务，数据会发送到提供商     |
| `autoRecall`（默认值：`true`） | ❌ 不会；数据仅从本地SQLite读取           |
| 机密信息            | ❌ 从不；这些信息会被从提取过程中过滤掉         |
| 数据迁移            | ❌ 不会；数据仅从本地工作空间文件读取并保存在本地SQLite中 |

## 从现有内存文件迁移数据

要从现有的代理内存文件中恢复Memento的数据，请按照以下步骤操作：

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

2. **务必先进行测试运行**，以确认哪些文件需要被迁移：

```bash
npx tsx src/extraction/migrate.ts --all --dry-run
```

3. 执行实际的数据迁移操作：

```bash
npx tsx src/extraction/migrate.ts --all
```

⚠️ 数据迁移会从你指定的工作空间路径中读取文件。请在迁移前仔细检查配置文件。

## 架构说明

- **捕获层**：监听`message:received`和`message:sent`事件，对多轮对话内容进行缓冲处理。
- **提取层**：异步调用LLM进行信息提取，同时处理数据去重、事件追踪和时间模式检测。
- **存储层**：使用SQLite（推荐使用`better-sqlite3`版本）进行数据存储，并支持FTS5全文搜索及可选的向量嵌入功能。
- **检索层**：通过`before_prompt_build`钩子，结合多种因素（如信息的新近性、出现频率和类别权重）来决定检索结果。

## 系统要求

- OpenClaw版本需达到2026.2.20或更高。
- 系统需安装Node.js 18或更高版本。
- 需要为你选择的LLM提供商获取API密钥（仅在使用数据提取功能时需要；如果使用Ollama，则无需API密钥）。
- 可选：建议使用GPU以加速嵌入信息的搜索过程；如果GPU不可用，系统会自动切换到CPU进行搜索。

## 安装方法

```bash
# From ClawHub
clawhub install memento

# Or for local development
git clone https://github.com/braibaud/Memento
cd Memento
npm install
```

注意：`better-sqlite3`模块在安装过程中会自动编译相应的原生绑定代码。这是SQLite访问的正常操作流程。