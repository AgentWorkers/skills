# 技能：快速统一内存（Fast Unified Memory）

这是一个高性能的统一内存系统，它将 OpenClaw 内存与基于 Ollama 的 nomic-embed-text 模型的语义记忆存储相结合，以实现超快的嵌入处理速度。

## 概述

该技能提供了一个统一的记忆层，融合了以下两种存储方式：
- **OpenClaw 内存**：标准的基于文件的记忆存储系统
- **语义记忆**：使用 Ollama 嵌入技术的向量记忆系统

## 特点

- ⚡ **超快速度**：整体搜索时间约为 130 毫秒（嵌入处理约 40 毫秒 + 搜索处理约 90 毫秒）
- 🔒 **隐私保护**：所有处理操作均在本地通过 Ollama 完成
- 💰 **免费**：无需支付 API 费用，使用本地的 Ollama 实例
- 🧠 **智能匹配**：利用 nomic-embed-text 模型实现智能的相似性匹配功能

## 使用要求

- 确保 [Ollama](https://ollama.ai) 已安装并正常运行
- 需要拉取 `nomic-embed-text` 模型：`ollama pull nomic-embed-text`

## 安装

```bash
# Install Ollama first
curl -fsSL https://ollama.ai/install.sh | sh

# Pull the embedding model
ollama pull nomic-embed-text

# Start Ollama
ollama serve
```

## 使用方法

### 命令

```bash
# Search both memory systems
node fast-unified-memory.js search "your query"

# Add a memory
node fast-unified-memory.js add "User prefers concise responses"

# List all memories
node fast-unified-memory.js list

# Show system stats
node fast-unified-memory.js stats
```

## 架构

```
┌─────────────────────────────────────────────┐
│           FAST UNIFIED MEMORY                │
│                                             │
│  ┌─────────────┐    ┌─────────────┐        │
│  │   OpenClaw  │    │   Semantic  │        │
│  │   Memory    │    │   Memory    │        │
│  │ (files)     │    │  (vectors) │        │
│  └─────────────┘    └─────────────┘        │
│           ↓                  ↓              │
│    [Keyword Match]   [Cosine Similarity]   │
│                                             │
│        Unified Results (ranked)             │
└─────────────────────────────────────────────┘
```

## 性能指标

| 指标        | 值         |
|------------|------------|
| 嵌入生成时间    | 约 40 毫秒     |
| 向量搜索时间    | 约 50 毫秒     |
| 文件搜索时间    | 约 40 毫秒     |
| **总搜索时间** | 约 130 毫秒     |

## 配置设置

该技能使用以下默认配置：
- Ollama 的 URL：`http://localhost:11434`
- 嵌入模型：`nomic-embed-text`
- 内存存储路径：`~/.mem0/fast-store.json`
- OpenClaw 内存路径：`~/.openclaw/workspace/memory/`

## 相关文件

- `fast-unified-memory.js`：主要的命令行工具
- `SKILL.md`：本文档文件

## 故障排除

- **Ollama 未运行**：
```bash
ollama serve
```

- **模型未找到**：
```bash
ollama pull nomic-embed-text
```

- **端口冲突**：
该技能默认使用 Ollama 的 11434 端口。如果使用其他端口，请更新 `OLLAMA_URL` 变量。

## 许可证

MIT 许可证