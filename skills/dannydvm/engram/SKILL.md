---
name: engram
description: **用于AI代理的持久性语义记忆层**  
该系统采用“本地优先”的存储策略（SQLite + LanceDB），并结合Ollama模型进行数据存储与检索。能够存储和调用事实、决策、偏好、事件以及跨会话的相关信息。系统支持记忆内容的衰减处理、数据去重功能，支持多种类型的数据存储（共5种类型），以及多种类型的数据关系（共7种图关系）。同时具备代理/用户级别的数据访问控制、语义搜索功能，并能根据上下文自动从文本中提取相关信息（支持规则驱动、大型语言模型或混合方法）。支持数据的导入/导出操作，提供REST API接口以及MCP协议。该系统有效解决了“上下文窗口”相关的问题以及数据存储的压缩/恢复问题。  

**服务器地址及界面**：  
服务器运行在本地（localhost:3400），管理界面位于 `/dashboard`。  

**安装方式**：  
可通过npm包 `engram-memory` 进行安装。安装时需要确保已安装Ollama模型以及 `nomic-embed-text` 插件。
requires:
  bins:
    - engram
install:
  npm: engram-memory
  setup: |
    # Install Ollama and embedding model
    brew install ollama  # macOS
    ollama pull nomic-embed-text
    
    # Start server (run as daemon or manually)
    engram serve
---

# Engram：为AI代理提供持久性记忆系统

Engram能够为您的AI代理提供持久且语义明确的内存存储，这种记忆能够在会话结束、数据压缩或系统崩溃后依然保留。所有数据都存储在本地，无需依赖云服务，也不会产生任何token费用。

## 启动序列（必填）

**在每次会话开始时**，请运行以下命令：
```bash
engram search "<current task context>" --limit 10
```

示例：`engram search "client onboarding status churn risk" --limit 10`
该命令会从之前的会话中检索与“客户入职状态及流失风险”相关的信息，以便您在开始新工作之前能够快速获取所需信息。

## 存储记忆

Engram支持五种类型的内存：
- `fact`（事实）
- `decision`（决策）
- `preference`（偏好）
- `event`（事件）
- `relationship`（关系）

```bash
# Facts — objective information
engram add "API rate limit is 100 req/min" --type fact --tags api,limits

# Decisions — choices made
engram add "We chose PostgreSQL over MongoDB for better ACID" --type decision --tags database

# Preferences — user/client likes/dislikes
engram add "Dr. Steph prefers text over calls" --type preference --tags dr-steph,communication

# Events — milestones, dates
engram add "Launched v2.0 on January 15, 2026" --type event --tags launch,milestone

# Relationships — people, roles, connections  
engram add "Mia is client manager, reports to Danny" --type relationship --tags team,roles
```

**何时存储记忆？**
- 客户状态发生变化时（例如流失风险、潜在的追加销售机会、客户投诉等）
- 关于项目或客户的重要决策
- 工作过程中获取的事实信息（如凭证、客户偏好、日期等）
- 完成的里程碑（如入职流程、产品发布等）

## 搜索

Engram支持**语义搜索**，能够理解记忆内容的实际含义而不仅仅是关键词。

```bash
# Basic search
engram search "database choice" --limit 5

# Filter by type
engram search "user preferences" --type preference --limit 10

# Filter by agent (see only your memories + global)
engram search "project status" --agent theo --limit 10
```

## 基于上下文的记忆检索

Engram会根据以下因素对记忆进行排序：
- 语义相似度
- 最近访问时间
- 重要性
- 访问频率

```bash
engram recall "Setting up new client deployment" --limit 10
```

当您需要根据特定上下文找到最相关的记忆时，这种检索方式会更加高效。

## 记忆之间的关系

Engram支持七种类型的关系：
- `related_to`（与...相关）
- `supports`（支持...）
- `contradicts`（与...矛盾）
- `caused_by`（由...引起）
- `supersedes`（被...取代）
- `part_of`（是...的一部分）
- `references`（引用...）

这些关系有助于提高记忆的检索效率——关系紧密的记忆会在检索结果中占据更靠前的位置。

## 从文本中自动提取记忆

Engram能够从原始文本中自动提取记忆信息（默认基于规则进行提取，也可选择使用大型语言模型LLM进行提取）：
```bash
# From stdin
echo "Mia confirmed client is happy. We decided to upsell SEO." | engram ingest

# From command
engram extract "Sarah joined as CTO last Tuesday. Prefers async communication."
```

系统会自动识别记忆的类型、添加标签，并对其进行重要性评分。

## 系统管理

```bash
# Stats (memory count, types, storage size)
engram stats

# Export backup
engram export -o backup.json

# Import backup
engram import backup.json

# View specific memory
engram get <memory-id>

# Soft delete (preserves for audit)
engram forget <memory-id> --reason "outdated"

# Apply decay manually (usually runs daily automatically)
engram decay
```

## 记忆衰减

Engram的设计灵感来源于生物记忆机制：
- 每条记忆都有一个重要性评分（范围从0.0到1.0）。
- 每天记忆的重要性会以0.99的速率衰减（可配置）。
- 访问某条记忆会提升其重要性评分。
- 重要性较低的记忆会逐渐从搜索结果中消失。
- 所有记忆都不会被删除，只是被归档，需要时可以重新检索。

## 记忆的访问范围

Engram支持四种访问范围：
- `global`（全局）
- `agent`（代理）
- `user`（用户）
- `session`（会话）

默认情况下，代理可以查看自己的记忆以及全局记忆；
使用`--agent <agentId>`命令可以过滤出特定代理的记忆。
这种范围隔离机制可以防止不同代理之间的记忆相互干扰。

## REST API

Engram的服务器运行地址为`http://localhost:3400`，可以通过`engram serve`命令启动服务。
```bash
# Add memory
curl -X POST http://localhost:3400/api/memories \
  -H "Content-Type: application/json" \
  -d '{"content": "...", "type": "fact", "tags": ["x","y"]}'

# Search
curl "http://localhost:3400/api/memories/search?q=query&limit=5"

# Recall with context
curl -X POST http://localhost:3400/api/recall \
  -H "Content-Type: application/json" \
  -d '{"context": "...", "limit": 10}'

# Stats
curl http://localhost:3400/api/stats
```

**控制台**：`http://localhost:3400/dashboard`（支持可视化搜索、浏览、删除和导出记忆数据）。

## 与MCP系统的集成

Engram可以作为MCP（Memory and Context Platform）的服务器使用。您可以在MCP客户端配置中添加Engram的相关功能：
```json
{
  "mcpServers": {
    "engram": {
      "command": "engram-mcp"
    }
  }
}
```

**MCP相关工具**：
- `engram_add`：用于添加新的记忆
- `engram_search`：用于搜索记忆
- `engram_recall`：用于检索记忆
- `engram_forget`：用于删除记忆

## 配置文件

配置文件位于`~/.engram/config.yaml`：
```yaml
storage:
  path: ~/.engram

embeddings:
  provider: ollama           # or "openai"
  model: nomic-embed-text
  ollama_url: http://localhost:11434

server:
  port: 3400
  host: localhost

decay:
  enabled: true
  rate: 0.99                 # 1% decay per day
  archive_threshold: 0.1

dedup:
  enabled: true
  threshold: 0.95            # cosine similarity for dedup
```

## 使用建议：
1. **启动时进行检索**：每次会话开始时，务必执行`engram search "<context>" --limit 10`以获取相关记忆。
2. **正确分类记忆类型**：使用正确的记忆类型有助于提高检索效果。
3. **合理添加标签**：标签有助于过滤和跨记忆之间的关联。
4. **自动提取对话内容**：在重要的对话发生后，使用`engram ingest`命令将对话内容存储到记忆系统中。
5. **让记忆自然衰减**：不要存储无关紧要的信息，让重要的记忆保持较高的重要性。
6. **利用关系结构**：在添加相互关联的记忆后，使用`auto-relate`命令建立它们之间的关系。
7. **按代理划分记忆**：将不同代理的记忆分开存储，以保持清晰的上下文。

## 常见问题排查：

- **服务器未运行？**请检查服务器是否正常启动。
- **嵌入功能失败？**请检查相关的代码实现是否正确。
- **需要重置配置？**可以使用相应的命令进行重置。

---

**创建者：** Danny Veiga ([@dannyveigatx](https://x.com/dannyveigatx))  
**来源代码：** https://github.com/Dannydvm/engram-memory  
**文档：** https://github.com/Dannydvm/engram-memory/blob/main/README.md