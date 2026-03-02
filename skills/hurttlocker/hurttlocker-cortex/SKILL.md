---
name: cortex
description: 本地优先的代理内存管理机制，采用艾宾浩斯遗忘模型（Ebbinghaus decay）进行数据衰减处理；结合混合搜索（hybrid search）和MCP工具进行数据检索。支持导入文件、提取关键信息，并使用BM25算法结合语义分析进行高效搜索；同时能够实时追踪信息的可信度变化。该方案完全不依赖任何外部库或服务，仅通过一个Go语言编写的二进制文件实现所有功能，数据存储采用SQLite数据库。适用于以下场景：当需要超出OpenClaw内置内存限制的持久化存储时（尤其是多代理系统、大型知识库的场景），或者当数据压缩导致重要信息丢失时。**不适用的场景**包括：对话历史记录的存储（请使用memory_search）、精确字符串匹配（请使用ripgrep）或网络查询功能。
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
# Cortex — 以本地数据为主导的AI代理内存系统

**OpenClaw应内置的内存解决方案**

Cortex是一个开源的、基于文件导入的AI代理内存管理系统。它采用单一的Go语言编写，使用SQLite作为存储引擎，完全不依赖云服务。该系统解决了OpenClaw最常见的问题：代理在数据压缩后会丢失所有信息。

**GitHub链接：** https://github.com/hurttlocker/cortex  
**安装方法：** 使用`brew install hurttlocker/cortex/cortex`进行安装，或从[发布页面](https://github.com/hurttlocker/cortex/releases)下载最新版本。

## 为什么选择Cortex？

OpenClaw默认使用Markdown文件作为内存存储方式。当存储空间不足时，系统会通过压缩来节省空间，但这种压缩方式会导致数据丢失。Cortex解决了这个问题：

| 问题 | Cortex的解决方案 |
|---|---|
| 压缩导致数据丢失 | 使用持久化的SQLite数据库，数据可以跨会话保存 |
| 无法搜索数据 | 只能将文件直接导入到内存中 | 结合BM25索引和语义搜索功能（关键词搜索约16毫秒，语义搜索约52毫秒） |
| 所有数据权重相同 | 采用艾宾浩斯遗忘曲线算法，重要信息得以保留，无关信息逐渐被遗忘 |
| 无法导入现有文件 | 支持导入多种类型的文件（Markdown、文本文件等），并提供8种数据源连接方式（GitHub、Gmail、Calendar、Drive、Slack、Notion、Discord、Telegram） |
| 多个代理之间的数据冲突 | 支持为每个代理独立管理内存 |
| 高昂的云存储费用 | 免费使用本地SQLite存储 |

## 快速入门

### 1. 安装Cortex

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

### 4. 作为MCP服务器使用（推荐用于OpenClaw）

```bash
# Add to your MCP config — Cortex exposes 17 tools + 4 resources
cortex mcp              # stdio mode
cortex mcp --port 8080  # HTTP+SSE mode
```

## 主要特性

### 艾宾浩斯遗忘曲线算法
不同类型的数据遗忘速度不同：身份信息（如名称、角色）可保存约2年，时间相关的信息（如事件、日期）约1周，状态信息（如状态、情绪）约2周。这使得搜索结果能够自然地优先显示重要内容，无需人工筛选。

### 混合搜索机制
- **BM25索引**：通过SQLite的FTS5引擎实现即时关键词匹配（约16毫秒）  
- **语义搜索**：基于本地嵌入模型进行语义分析（约52毫秒）  
- **混合搜索**：结合两种算法，通过互惠排名算法优化搜索结果

### 数据提取
所有导入的文件都会被自动提取关键信息：
- 基于规则的提取（无需额外成本，即时完成）  
- 可选的外部语言模型（如Grok、Gemini）进行信息增强  
- 自动将数据分类为9种类型：身份、关系、偏好、决策、时间、位置、状态、配置、键值对

### 数据源连接（测试版）
支持从外部来源导入数据：
```bash
cortex connect sync --provider github --extract
cortex connect sync --provider gmail --extract
cortex connect sync --all --extract
```

### 知识图谱
支持可视化展示内存中的数据结构：
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

## 与OpenClaw的集成

**推荐的搜索流程：**
首先使用OpenClaw内置的`memory_search`功能查询对话记录，然后通过Cortex进行深入的知识检索。

### 自动化脚本
随附的`scripts/cortex.sh`脚本提供了便捷的命令行接口：
```bash
scripts/cortex.sh search "query" 5       # Hybrid search
scripts/cortex.sh stats                    # Memory health
scripts/cortex.sh stale 30                # Stale fact detection
scripts/cortex.sh conflicts               # Contradiction detection
scripts/cortex.sh sync                    # Incremental import
scripts/cortex.sh reimport                # Full wipe + re-import
scripts/cortex.sh compaction              # Pre-compaction state brief
```

### 自动同步机制（支持launchd/systemd）
系统支持通过`launchd`或`systemd`服务自动启动Cortex：
```bash
# Auto-import sessions + sync connectors every 30 min
cortex connect schedule --every 30m --install
```

## 架构特点

- **编程语言：** Go（62,300行代码，包含1,081个测试用例）  
- **存储方式：** SQLite + FTS5索引 + WAL（Write-Ahead Logging）  
- **二进制文件大小：** 19MB，纯Go语言实现，无CGO依赖，运行时无额外依赖  
- **支持平台：** macOS（arm64/amd64）、Linux（arm64/amd64）、Windows（amd64）  
- **MCP（Memory Management Component）：** 包含17个工具和4种数据源连接方式（stdio、HTTP、SSE）  
- **嵌入模型：** 可使用Ollama（nomic-embed-text）或OpenAI/DeepSeek等模型进行数据嵌入  
- **扩展性：** 支持管理超过10万个数据条目，日处理量约20-50条，未来5年内无需扩容  
- **许可证：** MIT许可

## 与其他内存管理工具的对比

| 功能 | Cortex | Mem0 | Zep | LangMem |
|---|---|---|---|---|
| 部署方式：** 单一二进制文件 | 需依赖云服务或Kubernetes | 需依赖云服务 | 使用Python库 |
| 成本：** 免费 | 每月19-249美元 | 每月25美元以上 | 需额外支付基础设施费用 |
| 隐私保护：** 100%本地存储 | 默认使用云服务 | 需依赖云服务 | 隐私保护程度取决于具体实现 |
| 数据衰减机制：** 采用艾宾浩斯遗忘曲线算法 | 仅基于时间戳删除数据 | 仅基于时间戳删除数据 | 无特定机制 |
| 数据导入方式：** 支持文件导入及多种数据源连接 | 仅支持聊天记录提取 | 支持聊天记录和文档导入 | 支持聊天记录提取 |
| 搜索功能：** 结合BM25索引和语义搜索 | 使用向量模型和知识图谱 | 基于时间戳的简单搜索 | 仅支持JSON格式的文档搜索 |
| MCP（Memory Management Component）：** 内置17个工具 | 无 | 无 | 无 |
| 依赖项：** 无额外依赖 | 需依赖Python和云服务 | 需依赖云服务和额外服务 | 需依赖Python和特定库 |

## 使用要求

- **Cortex二进制文件：** 可通过Homebrew安装或从GitHub下载  
- **可选组件：** 需安装Ollama及`nomic-embed-text`以实现语义搜索  
- **可选功能：** 需配置LLM API密钥（如Grok、Gemini等）进行数据增强  
- **系统要求：** 无需Python、Node.js或Docker环境，仅需Cortex二进制文件  

## v1.1/v1.2版本与OpenClaw的集成指南

### 如何选择`cortex answer`或`cortex search`？
- `cortex answer`：用于回答“我知道关于X的什么？”或“Y是谁？”等问题，提供连贯的回答并附带引用  
- `cortex search`：用于查找包含特定内容（如X）的文件，或用于调试和探索数据内容，返回排序后的结果列表  

### 配置文件（config.yaml）
在`~/.cortex/config.yaml`中配置搜索策略：
```yaml
search:
  source_boost:
    - prefix: "memory/"
      weight: 1.5
    - prefix: "file:MEMORY"
      weight: 1.6
    - prefix: "github"
      weight: 1.3
    - prefix: "session:"
      weight: 0.9
```  
配置文件中的权重值越高，数据的重要性越高。每日笔记和核心文件会优先于自动导入的数据被检索。

### 搜索意图设置
当知道数据的位置时，可以使用`--intent`参数指定搜索方向：
- `--intent memory`：搜索个人决策、偏好信息或人员相关信息  
- `--intent connector`：搜索代码、Pull请求、电子邮件或外部数据  
- `--intent import`：搜索导入的文件和文档  
- 未设置该参数时，系统会搜索所有数据（默认设置，适合数据探索）

### 系统运行计划
建议每天凌晨3:30自动运行系统：
- **首次运行时**：仅进行测试，查看日志  
- **后续运行**：按照预设的策略处理数据  

### 系统配置示例
- **新代理（数据量<500条）：** [配置示例](```yaml
policies:
  reinforce_promote:
    min_reinforcements: 3
    min_sources: 2
  decay_retire:
    inactive_days: 90
    confidence_below: 0.25
  conflict_supersede:
    min_confidence_delta: 0.20
```)  
- **成熟代理（数据量>2000条）：** [配置示例](```yaml
policies:
  reinforce_promote:
    min_reinforcements: 5
    min_sources: 3
  decay_retire:
    inactive_days: 45
    confidence_below: 0.35
  conflict_supersede:
    min_confidence_delta: 0.10
```)  

### 数据导入后的处理
在批量导入数据后，需要运行相应的清理脚本：
```bash
cortex cleanup --dedup-facts    # Remove near-duplicates
cortex conflicts --auto-resolve  # Resolve contradictions
```  

### 推荐的OpenClaw搜索流程（更新版）
[详细流程说明](```
memory_search → cortex answer (synthesis) → cortex search (pointers) → QMD → ripgrep → web
```)