---
name: cortex
description: 本地优先的代理内存管理机制，采用艾宾浩斯遗忘模型（Ebbinghaus decay）进行数据衰减处理；结合混合搜索（hybrid search）技术和MCP（Memory Compression Protocol）工具进行数据存储与检索。支持导入文件、提取关键信息，利用BM25算法及语义分析技术进行高效搜索，并能实时追踪数据检索的准确性（confidence level）。该方案完全无外部依赖，仅依赖一个Go语言编写的二进制文件和SQLite数据库进行数据存储。适用于以下场景：当需要超出OpenClaw内置内存限制的持久化存储时（尤其是多代理系统、大型知识库场景，或数据压缩导致重要信息丢失的情况）。**不适用于以下场景**：对话历史记录的存储（请使用memory_search），精确字符串匹配（请使用ripgrep），或网络数据查询。
  Local-first agent memory with Ebbinghaus decay, hybrid search, and MCP tools.
  Import files, extract facts, search with BM25 + semantic, track confidence over time.
  Zero dependencies, single Go binary, SQLite storage. Use when you need persistent
  memory beyond OpenClaw's built-in MEMORY.md — especially for multi-agent setups,
  large knowledge bases, or when compaction keeps losing your important context.
  Don't use for: conversation history (use memory_search), exact string matching
  (use ripgrep), or web lookups.
homepage: https://github.com/hurttlocker/cortex
metadata:
  clawdbot:
    emoji: "🧠"
    requires:
      files: ["scripts/*"]
---
# Cortex — 以本地数据为主导的代理内存系统

**OpenClaw 应该内置的内存层**

Cortex 是一个开源的、基于导入数据的内存管理系统，专为 AI 代理设计。它采用单一的 Go 二进制文件进行存储，并使用 SQLite 作为数据库，完全不依赖云服务。该系统解决了 OpenClaw 最主要的问题：代理在数据被压缩后会丢失所有信息。

**GitHub 链接：** https://github.com/hurttlocker/cortex  
**安装方式：** 使用 `brew install hurttlocker/cortex/cortex`，或从 [Releases](https://github.com/hurttlocker/cortex/releases) 下载最新版本。

## 为什么选择 Cortex？

OpenClaw 的默认内存存储方式是 Markdown 文件。当存储空间满时，系统会通过压缩来节省空间，但这种压缩方式会导致数据丢失。Cortex 解决了这个问题：

| 问题 | Cortex 的解决方案 |
|---|---|
| 压缩导致数据丢失 | 持久化的 SQLite 数据库可以保存所有数据 |
| 无法搜索 — 只能手动导出文件 | 结合 BM25 索引和语义搜索功能（关键词搜索约 16 毫秒，语义搜索约 52 毫秒） |
| 所有数据的重要性相同 | 采用艾宾浩斯遗忘曲线算法：重要信息得以保留，无关信息会自然淡出 |
| 无法导入现有文件 | 支持导入多种类型的文件（Markdown、文本文件等）；支持 8 种数据源（GitHub、Gmail、Calendar、Drive、Slack、Notion、Discord、Telegram） |
| 多个代理之间的数据冲突 | 每个代理的数据都有独立的管理范围 |
| 高昂的云存储费用 | 使用本地 SQLite，每月费用为零 |

## 快速入门

### 1. 安装 Cortex

```bash
# macOS/Linux (Homebrew)
brew install hurttlocker/cortex/cortex

# Or download binary directly
# https://github.com/hurttlocker/cortex/releases/latest
```

### 2. 导入数据

```bash
# Import OpenClaw's memory files
cortex import ~/clawd/memory/ --extract

# Import specific files
cortex import ~/clawd/MEMORY.md --extract
cortex import ~/clawd/USER.md --extract
```

### 3. 进行搜索

```bash
# Fast keyword search
cortex search "wedding venue" --limit 5

# Semantic search (requires ollama with nomic-embed-text)
cortex search "what decisions did I make about the project" --mode semantic

# Hybrid (recommended)
cortex search "trading strategy" --mode hybrid
```

### 4. 作为 MCP 服务器使用（推荐）

```bash
# Add to your MCP config — Cortex exposes 17 tools + 4 resources
cortex mcp              # stdio mode
cortex mcp --port 8080  # HTTP+SSE mode
```

## 主要特性

### 艾宾浩斯遗忘曲线算法
不同类型的数据会以不同的速度被遗忘：
- 身份信息（名称、角色）可保留约 2 年；
- 时间相关信息（事件、日期）约 1 周后逐渐淡出；
- 状态信息（状态、情绪）约 2 周后逐渐淡出。
这意味着搜索结果会自动优先显示重要信息，无需人工筛选。

### 混合搜索机制
- **BM25**：通过 SQLite 的 FTS5 索引实现即时关键词匹配（约 16 毫秒）；
- **语义搜索**：基于本地嵌入模型进行语义分析（约 52 毫秒）；
- **混合搜索**：结合两种方法，通过互惠排名算法优化搜索结果。

### 数据提取
所有导入的文件都会被自动提取相关信息：
- 基于规则的提取（无需额外成本，即时完成）；
- 可选地使用 LLM（如 Grok、Gemini 等）进行信息增强；
- 自动将数据分类为 9 种类型：身份、关系、偏好、决策、时间、位置、状态、配置、键值对。

### 数据源连接（测试版）
可以从外部源导入数据：
```bash
cortex connect sync --provider github --extract
cortex connect sync --provider gmail --extract
cortex connect sync --all --extract
```

### 知识图谱
可以可视化地查看存储的数据：
```bash
cortex graph --serve --port 8090
# Opens interactive 2D graph explorer in browser
```

### 自动清理机制
系统具有自动清理过期数据的功能：
```bash
cortex cleanup --purge-noise  # Remove garbage + duplicates
cortex stale 30               # Find facts not accessed in 30 days
cortex conflicts               # Detect contradictions
cortex conflicts --resolve llm # Auto-resolve with LLM
```

## 与 OpenClaw 的集成

**推荐的搜索流程**
首先使用 OpenClaw 的内置 `memory_search` 功能查询对话记录，然后使用 Cortex 进行深入的知识检索。

### 自动化脚本
随附的 `scripts/cortex.sh` 脚本提供了便捷的命令行接口：
```bash
scripts/cortex.sh search "query" 5       # Hybrid search
scripts/cortex.sh stats                    # Memory health
scripts/cortex.sh stale 30                # Stale fact detection
scripts/cortex.sh conflicts               # Contradiction detection
scripts/cortex.sh sync                    # Incremental import
scripts/cortex.sh reimport                # Full wipe + re-import
scripts/cortex.sh compaction              # Pre-compaction state brief
```

### 自动同步机制
支持通过 `launchd` 或 `systemd` 自动启动服务：
```bash
# Auto-import sessions + sync connectors every 30 min
cortex connect schedule --every 30m --install
```

## 架构特点

- **语言**：Go（62,300 行代码，包含 1,081 个测试用例）；
- **存储方式**：SQLite + FTS5 + WAL 模式；
- **二进制文件大小**：19MB，纯 Go 语言编写，无 CGO 依赖，运行时无额外依赖；
- **支持平台**：macOS（arm64/amd64）、Linux（arm64/amd64）、Windows（amd64）；
- **MCP（Memory Management System）**：包含 17 个工具和 4 种数据源连接方式（stdio 或 HTTP+SSE）；
- **嵌入模型**：支持使用 Ollama（nomic-embed-text）或 OpenAI/DeepSeek 自定义的嵌入模型；
- **可扩展性**：可处理超过 100,000 个数据源；每天处理约 20-50 条数据，未来 5 年内不会达到性能瓶颈；
- **许可证**：MIT 许可证。

## 与其他内存管理工具的对比

| 功能 | Cortex | Mem0 | Zep | LangMem |
|---|---|---|---|---|
| 部署方式** | 单一二进制文件 | 需依赖云服务或 K8s | 需依赖云服务 | 需依赖 Python 库 |
| 成本** | 免费 | 每月 19-249 美元 | 每月 25 美元以上 | 需额外支付基础设施费用 |
| 隐私保护** | 100% 本地存储 | 默认依赖云服务 | 需依赖云服务 | 隐私保护程度取决于具体实现 |
| 数据衰减机制** | 采用艾宾浩斯遗忘曲线算法 | 仅基于时间戳删除数据 | 仅基于时间戳删除数据 | 无明确的数据衰减机制 |
| 数据导入方式** | 支持导入多种文件及多种数据源 | 仅支持从聊天记录中提取数据 | 仅支持从聊天记录或文档中提取数据 |
| 搜索方式** | 结合 BM25 索引和语义搜索 | 使用向量模型和知识图谱 | 仅基于时间戳的简单搜索 | 基于 JSON 文档的搜索 |
| MCP 功能** | 内置 17 个数据管理工具 | 无 | 无 | 无 |
| 依赖项** | 无额外依赖 | 需依赖 Python 和云服务 | 需依赖云服务和额外服务 | 需依赖 Python 和语言相关的服务 |

## 安装要求

- **Cortex 二进制文件**：可通过 Homebrew 安装，或从 GitHub 的 Releases 下载；
- **可选组件**：使用 Ollama 和 `nomic-embed-text` 进行语义搜索；
- **可选功能**：需要 LLM API 密钥（如 Grok、Gemini 等）进行数据增强；
- 无需安装 Python、Node.js 或 Docker；只需安装 Cortex 二进制文件即可。