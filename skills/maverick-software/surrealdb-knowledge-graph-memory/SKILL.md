# SurrealDB知识图谱内存系统

这是一个基于SurrealDB构建的知识图谱内存系统，它支持向量化语义搜索、置信度评分、图谱感知的事实关系管理、MCP工具以及由大型语言模型（LLM）驱动的知识提取功能。

## 描述

该系统可用于：
- 以相互关联的事实形式存储和检索知识
- 进行带有置信度权重的语义搜索
- 管理事实之间的关系（支持、矛盾、更新）
- 从内存文件中提取知识（利用LLM）
- 通过人工智能发现事实之间的关联
- 进行内存维护（包括数据衰减、修剪和整合）

**触发命令**：
- “记住这个”（remember this）
- “存储事实”（store fact）
- “你知道什么”（what do you know about）
- “内存搜索”（memory search）
- “内存维护”（memory maintenance）
- “修剪内存”（prune memory）
- “知识图谱”（knowledge graph）
- “查找关系”（find relations）

## ⚠️ 安全与安装注意事项

此系统执行系统级操作，请在安装前仔细阅读以下内容：

| 操作          | 执行位置        | 说明                          |
|------------------|------------------|---------------------------------------------|
| **网络安装**       | `install.sh`, `memory.ts`    | 运行 `curl https://install.surrealdb.com \| sh`                |
| **源代码修补**     | `integrate-clawdbot.sh`    | 使用 `sed -i` 修补 Clawdbot 的源代码文件                |
| **服务管理**       | `memory.ts`      | 可以启动 SurrealDB 服务器并导入数据库模式            |
| **Python 包安装**     | `install.sh`, `memory.ts`    | 通过 pip 安装 surrealdb、openai 和 pyyaml                |
| **文件访问**       | `extract-knowledge.py`    | 读取 `MEMORY.md` 及 `memory/*.md` 文件以提取数据           |

**默认凭据**：
示例中使用 `root/root` —— 请在生产环境中更换凭据，并确保仅绑定到本地主机。

**API 密钥**：
- `OPENAI_API_KEY` 是必需的，用于文本嵌入（text-embedding-3-small）和知识提取（GPT-4o-mini）功能。请使用具有适当权限的 API 密钥。

**安全安装步骤**：
1. 从 [surrealdb.com/install](https://surrealdb.com/install) 手动安装 SurrealDB。
2. 创建一个 Python 虚拟环境（venv）：`python3 -m venv .venv && source .venv/bin/activate`。
3. 查看并运行 `pip install -r scripts/requirements.txt`。
4. 设置 `OPENAI_API_KEY`，并确保其权限最小化。
5. 可以跳过 `integrate-clawdbot.sh`，或查看它将应用的更改。

## 特点

### MCP 工具
该系统提供了一个包含 4 个工具的 MCP 服务器，用于管理知识图谱：
| 工具          | 说明                          |
|------------------|---------------------------------------------|
| `knowledge_search` | 根据查询进行语义搜索                        |
| `knowledge_recall` | 带有完整上下文（关系、实体）的事实检索                |
| `knowledge_store` | 带有置信度和标签的新事实存储                    |
| `knowledge_stats` | 获取知识图谱的统计信息                        |

### 知识提取
- 从 `MEMORY.md` 和 `memory/*.md` 文件中提取结构化事实。
- 使用 LLM（GPT-4o-mini）识别实体和关系。
- 支持基于文件变化的增量提取。
- 需要时支持完全重新提取数据。

### 置信度评分
每个事实的置信度由以下因素综合计算得出：
- **基础置信度**（0.0–1.0）
- **来自高置信度支持事实的增强**  
- **来自被广泛提及的实体的增强**  
- **来自高置信度矛盾事实的减分**  
- **时间衰减**：每月减少 5% 的置信度

### 关系发现
- 人工智能自动发现孤立事实之间的语义联系。
- 创建表示支持、矛盾、更新或详细说明关系的边。
- 可以手动执行，也可以通过每日定时任务自动执行。

## 先决条件

1. **已安装并运行 SurrealDB**：
   ```bash
   # Option A: Use the installer (runs curl | sh - review first!)
   ./scripts/install.sh
   
   # Option B: Manual install (recommended)
   # See https://surrealdb.com/install
   
   # Start server (change credentials in production!)
   surreal start --bind 127.0.0.1:8000 --user root --pass root file:~/.clawdbot/memory/knowledge.db
   ```

2. **Python 依赖项**（使用系统的虚拟环境）：
   ```bash
   cd /path/to/surrealdb-memory
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r scripts/requirements.txt
   ```

3. **OpenAI API 密钥**（**必需**）：用于嵌入和知识提取：
   ```bash
   # Used for: text-embedding-3-small (embeddings), GPT-4o-mini (extraction)
   # Recommendation: Use a scoped key with minimal permissions
   export OPENAI_API_KEY="sk-..."
   ```

## 快速入门

```bash
# Initialize the database schema
./scripts/init-db.sh

# Run initial knowledge extraction
source .venv/bin/activate
python3 scripts/extract-knowledge.py extract --full

# Check status
python3 scripts/extract-knowledge.py status
```

## MCP 服务器使用方法

### 推荐使用 mcporter：
```bash
# Stats
mcporter call surrealdb-memory.knowledge_stats

# Search for facts
mcporter call surrealdb-memory.knowledge_search query="topic" limit:10

# Recall a fact with context
mcporter call surrealdb-memory.knowledge_recall query="topic"
mcporter call surrealdb-memory.knowledge_recall fact_id="fact:abc123"

# Store a new fact
mcporter call surrealdb-memory.knowledge_store content="New fact" confidence:0.9
```

### MCP 服务器配置
请将以下配置添加到您的 MCP 客户端配置文件中：
```json
{
  "surrealdb-memory": {
    "command": "python3",
    "args": ["scripts/mcp-server.py"],
    "cwd": "/path/to/surrealdb-memory"
  }
}
```

## 命令行接口（CLI）

### knowledge-tool.py（简单 CLI）
```bash
# Search for facts
python3 scripts/knowledge-tool.py search "query" --limit 10

# Recall a fact
python3 scripts/knowledge-tool.py recall "query"
python3 scripts/knowledge-tool.py recall "fact:abc123"

# Store a fact
python3 scripts/knowledge-tool.py store "Fact content" --confidence 0.9

# Get stats
python3 scripts/knowledge-tool.py stats
```

### extract-knowledge.py

| 命令            | 说明                          |
|------------------|---------------------------------------------|
| `extract`          | 仅从已更改的文件中提取数据                |
| `extract --full`      | 提取所有文件中的数据                    |
| `status`          | 显示提取状态和统计信息                    |
| `reconcile`        | 进行深度数据整合（修剪、衰减、清理孤立数据）           |
| `discover-relations` | 通过人工智能发现事实之间的关系             |
| `dedupe`          | 查找并删除重复的事实                    |
| `rebuild-links`      | 为现有事实重建实体链接                    |
| `check`          | 检查是否需要数据提取（用于心跳检测）                |

### memory-cli.py

| 命令            | 说明                          |
|------------------|---------------------------------------------|
| `store <内容>`       | 存储新事实（可选参数：--source, --confidence, --tags）       |
| `search <查询>`       | 进行语义搜索，并返回按相似度和置信度加权的事实         |
| `get <事实ID>`       | 获取包含相关事实和实体的完整事实信息             |
| `relate <事实1> <关系> <事实2>` | 创建支持、矛盾、更新或详细说明的关系             |
| `decay`          | 对过时的事实应用时间衰减                    |
| `prune`          | 删除置信度低的事实                     |
| `consolidate`      | 合并相似的事实                         |
| `maintain`        | 运行完整维护周期（衰减、修剪、整合）                 |
| `stats`          | 显示数据库统计信息                     |

## 网关集成

该系统包含用于 Clawdbot 控制界面的网关处理程序：
| 方法            | 说明                          |
|------------------|---------------------------------------------|
| `memory.health`      | 检查 SurrealDB 的状态、模式和依赖项                |
| `memory.stats`      | 获取事实/实体/关系的数量统计                 |
| `memory.repair`     | 自动修复：安装二进制文件、启动服务器、初始化模式         |
| `memory.runExtraction`    | 运行数据提取、整合或关系发现操作             |
| `memory.extractionProgress` | 监控提取进度                         |
| `memory.activity`      | 获取最近的活动记录（查询、提取操作）                 |
| `memory.maintenance`     | 运行衰减/修剪操作                         |

### 安装网关集成

将网关处理程序复制到 Clawdbot 的源代码中：
```bash
cp clawdbot-integration/gateway/memory.ts /path/to/clawdbot/src/gateway/server-methods/

# Add to server-methods.ts:
import { memoryHandlers } from "./server-methods/memory.js";
// Add ...memoryHandlers to coreGatewayHandlers

# Rebuild Clawdbot
cd /path/to/clawdbot && npm run build
```

## 配置

创建 `~/.clawdbot/surrealdb-memory.yaml` 配置文件：
```yaml
connection: "http://localhost:8000"
namespace: clawdbot
database: memory
user: root
password: root

embedding:
  provider: openai
  model: text-embedding-3-small
  dimensions: 1536

confidence:
  decay_rate: 0.05  # per month
  support_threshold: 0.7
  contradict_drain: 0.20

maintenance:
  prune_after_days: 30
  min_confidence: 0.2
```

## 相关文件

```
surrealdb-memory/
├── SKILL.md                 # This file
├── scripts/
│   ├── mcp-server.py        # MCP server with 4 tools
│   ├── knowledge-tool.py    # Simple CLI wrapper
│   ├── extract-knowledge.py # LLM extraction from memory files
│   ├── memory-cli.py        # Full CLI for CRUD operations
│   ├── knowledge-tools.py   # Higher-level extraction tools
│   ├── schema.sql         # Database schema with graph functions
│   ├── init-db.sh           # Initialize database with schema
│   ├── install.sh           # Install SurrealDB binary
│   ├── migrate-sqlite.py    # Import from existing SQLite memory
│   ├── web-ui.py            # Optional web interface
│   └── requirements.txt     # Python dependencies
├── clawdbot-integration/
│   └── gateway/
│       └── memory.ts        # Gateway RPC handlers
└── references/
    ├── surql-examples.md    # SurrealQL query patterns
    └── conflict-patterns.md # Contradiction detection rules
```

## 维护计划

请将相关配置添加到 `HEARTBEAT.md` 文件中，或创建一个定时任务来自动执行维护操作：
```markdown
## Memory Maintenance (weekly)
- Run `surrealdb-memory` knowledge extraction check
- Run reconciliation if facts are stale
```

您也可以通过控制界面的“每日自动发现”选项来启用自动关系发现功能。

## 故障排除

- **“连接被拒绝”**：请确保 SurrealDB 正在运行。
- **“surrealdb 包未安装”**：请安装所需的 Python 依赖项。
- **“OPENAI_API_KEY 未设置”**：请导出 API 密钥。
- **搜索速度慢**：请确认向量索引已正确创建（检查 `schema.sql` 文件是否已应用）。
- **控制界面显示“正在启动...”且无响应**：尝试强制刷新浏览器（Ctrl+Shift+R）。

## 版本历史

- **v1.2.0**（2026-02-09）：添加了 MCP 服务器及 4 个工具，修复了查询相关的问题。
- **v1.1.0**（2026-02-09）：增加了网关集成和关系发现功能。
- **v1.0.0**（2026-01-31）：初始版本，支持数据提取和命令行接口。