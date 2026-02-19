# SurrealDB知识图谱内存系统 v2.1

这是一个全面的知识图谱内存系统，具备语义搜索、情景记忆、工作记忆以及自动上下文注入功能。

## 用途

该技能可用于：
- **语义记忆**：通过带有置信度加权的向量搜索来存储和检索事实信息。
- **情景记忆**：记录任务历史并从中学习。
- **工作记忆**：跟踪活跃任务的状态，并在系统崩溃时恢复数据。
- **自动上下文注入**：将相关上下文自动插入到代理的提示中。
- **结果校准**：根据任务结果调整事实的置信度。

## 触发语句：
- “记住这个”
- “存储事实”
- “你知道……吗？”
- “搜索知识”
- “查找类似的任务”
- “从历史中学习”

## 新版本（v2）的功能

| 功能 | 说明 |
|---------|-------------|
| **语义事实** | 带有置信度评分的向量索引事实 |
| **情景记忆** | 包含决策、问题、解决方案和学习内容的任务历史记录 |
| **工作记忆** | 可在系统崩溃后恢复的基于YAML的任务状态 |
| **结果校准** | 在成功完成任务的事实中增加置信度 |
| **自动注入** | 自动将相关事实/情景插入到提示中 |
| **实体提取** | 自动进行实体链接和关系发现 |
| **置信度衰减** | 过时的事实会随时间自然衰减 |

## 仪表盘界面

控制面板中的“Memory”标签页采用两列布局：

### 左侧栏：
- **📊 统计数据**：事实、实体、关系和存档项目的实时数量
- **置信度条形图**：置信度得分的可视化显示
- **来源分类**：按源文件分组的事实
- **🏥 系统健康状况**：SurrealDB的状态、数据库模式及Python依赖项
- **🔗 DB Studio**：快速链接到SurrealDB的Web界面

### 右侧栏：
- **📥 知识提取**
  - *提取变更*：从修改过的文件中逐步提取事实
  - *发现关系*：发现现有事实之间的语义关系
  *完整同步*：完成提取及关系发现
  - 进度条，显示实时状态更新

- **🔧 维护**
  - *应用衰减**：降低过时事实的置信度
  *清理过时数据**：将置信度低于阈值的事实存档
  *全面清理**：执行完整的维护周期

- **💡 提示**：操作的快速参考

当系统需要设置时，会显示一个**安装**部分，其中包含手动设置步骤。

## 先决条件

1. **已安装并运行SurrealDB**：
   ```bash
   # Install (one-time)
   ./scripts/install.sh
   
   # Start server
   surreal start --bind 127.0.0.1:8000 --user root --pass root file:~/.openclaw/memory/knowledge.db
   ```

2. **Python依赖项**（使用该技能的虚拟环境）：
   ```bash
   cd /path/to/surrealdb-memory
   python3 -m venv .venv
   source .venv/bin/activate
   pip install surrealdb openai pyyaml
   ```

3. **OpenAI API密钥**（用于嵌入操作，需在OpenClaw配置或环境中设置）

4. **mcporter**已配置并连接到该技能的MCP服务器

## MCP服务器设置

在`config/mcporter.json`文件中进行以下配置：
```json
{
  "servers": {
    "surrealdb-memory": {
      "command": ["python3", "/path/to/surrealdb-memory/scripts/mcp-server-v2.py"],
      "env": {
        "OPENAI_API_KEY": "${OPENAI_API_KEY}",
        "SURREAL_URL": "http://localhost:8000",
        "SURREAL_USER": "root",
        "SURREAL_PASS": "root"
      }
    }
  }
}
```

## MCP工具（共11个）

### 核心工具
| 工具 | 说明 |
|------|-------------|
| `knowledge_search` | 对事实进行语义搜索 |
| `knowledge_recall` | 获取包含完整上下文（关系、实体）的事实 |
| `knowledge_store` | 存储新事实 |
| `knowledge_stats` | 获取数据库统计信息 |

### v2版本的工具
| 工具 | 说明 |
|------|-------------|
| `knowledge_store_sync` | 带有重要性优先级的存储（重要性高则立即写入） |
| `episode_search` | 查找类似的过去任务 |
| `episode_learnings` | 从历史记录中获取可操作的教训 |
| `episode_store` | 记录已完成的任务 |
| `working_memory_status` | 获取当前任务状态 |
| `context_aware_search` | 带有任务上下文增强的搜索 |
| `memory_inject` | **用于提示的智能上下文注入** |

### `memory_inject`工具

`memory_inject`工具返回格式化后的上下文，可直接用于提示生成：
```bash
mcporter call surrealdb-memory.memory_inject \
    query="user message" \
    max_facts:7 \
    max_episodes:3 \
    confidence_threshold:0.9 \
    include_relations:true
```

## 自动注入（增强循环集成）

启用此功能后，内存内容会自动在每次代理操作时被注入：

1. **在模式界面中启用**：
   - 打开控制面板 → “Mode”标签页
   - 滚动到“🧠 Memory & Knowledge Graph”部分
   - 切换“Auto-Inject Context”选项
   - 配置限制（最大事实数量、最大情景数量、置信度阈值）

2. **工作原理**：
   - 每当用户发送消息时，会自动调用`memory_inject`函数
   - 根据用户的查询内容搜索相关事实
   - 如果事实的置信度低于阈值，会包含情景记忆
   - 格式化后的上下文会被插入到代理的提示中

3. **配置（在模式设置中）**：
| 设置 | 默认值 | 说明 |
|---------|---------|-------------|
| Auto-Inject Context | 关闭 | 开启/关闭自动注入 |
| Max Facts | 7 | 最大可注入的语义事实数量 |
| Max Episodes | 3 | 最大情景数量 |
| Confidence Threshold | 90% | 当置信度低于此值时包含情景 |
| Include Relations | 开启 | 是否包含实体关系 |

## 带进度跟踪的提取功能

当通过UI执行提取操作时，您会看到：
- **进度条**：显示提取进度的百分比
- **当前步骤**：显示正在处理的操作（例如：“从MEMORY.md文件中提取事实”）
- **计数器**：显示文件处理的进度（例如：“(3/7)”）
- **详细信息**：显示子步骤的详细信息

进度会通过轮询实时更新。完成后，统计信息会自动刷新。

## 命令行接口（CLI命令）

```bash
# Activate venv
source .venv/bin/activate

# Store a fact
python scripts/memory-cli.py store "Important fact" --confidence 0.9

# Search
python scripts/memory-cli.py search "query"

# Get stats
python scripts/knowledge-tool.py stats

# Run maintenance
python scripts/memory-cli.py maintain

# Extract from files
python scripts/extract-knowledge.py extract        # Changed files only
python scripts/extract-knowledge.py extract --full # All files
python scripts/extract-knowledge.py discover-relations
```

## 数据库模式（v2）

### 表结构
- `fact`：包含嵌入信息和置信度的语义事实
- `entity`：提取的实体（人物、地点、概念）
- `relates_to`：事实之间的关系
- `mentions`：事实与实体之间的链接
- `episode`：包含任务结果的历史记录
- `working_memory`：活跃任务的快照

### 关键字段（fact）
- `content`：事实的文本内容
- `embedding`：用于语义搜索的向量
- `confidence`：基础置信度（0-1）
- `success_count` / `failure_count`：任务结果的记录
- `scope`：全局、客户端或代理级别

### 关键字段（episode）
- `goal`：尝试完成的目标
- `outcome`：成功、失败或放弃
- `decisions`：所做的关键决策
- `problems`：遇到的问题（结构化）
- `solutions`：采用的解决方案（结构化）
- `key_learnings`：从中提取的教训

## 置信度评分

置信度的计算方式如下：
- **基础置信度**（0.0–1.0）
- **来自支持事实的增强**：来自相关事实的置信度提升
- **来自知名实体的增强**：来自知名实体的置信度提升
- **基于结果的历史调整**：根据成功/失败情况调整置信度
- **来自矛盾事实的减分**：因矛盾事实导致的置信度下降
- **时间衰减**：可配置，每月约5%

## 维护

### 自动维护（Cron任务）

```bash
# Extract facts from memory files (every 6 hours)
0 */6 * * * cd ~/openclaw/skills/surrealdb-memory && source .venv/bin/activate && python scripts/extract-knowledge.py extract

# Discover relations (daily at 3 AM)
0 3 * * * cd ~/openclaw/skills/surrealdb-memory && source .venv/bin/activate && python scripts/extract-knowledge.py discover-relations
```

### 手动维护（通过UI）

使用“Memory”标签页中的“维护”功能：
- **应用衰减**：降低过时事实的置信度
- **清理过时数据**：将置信度低于0.3的事实存档
- **全面清理**：执行完整的维护周期

## 文件

### 脚本
| 文件 | 用途 |
|------|---------|
| `mcp-server-v2.py` | 包含所有11个工具的MCP服务器 |
| `mcp-server.py` | 旧版v1的MCP服务器 |
| `episodes.py`：情景记忆模块 |
| `working_memory.py`：工作记忆模块 |
| `memory-cli.py`：用于手动操作的命令行工具 |
| `extract-knowledge.py`：从文件批量提取数据 |
| `knowledge-tools.py`：高级提取工具 |
| `schema-v2.sql`：v2版本的数据库模式 |
| `migrate-v2.py`：迁移脚本 |

### 集成

| 文件 | 用途 |
|------|---------|
| `openclaw-integration/gateway/memory.ts`：网关服务器相关代码 |
| `openclaw-integration/ui/memory-view.ts`：记忆图谱仪表盘UI |
| `openclaw-integration/ui/memory-controller.ts`：UI控制器相关代码 |

## 故障排除

**“连接被拒绝”**
→ 启动SurrealDB：`surreal start --bind 127.0.0.1:8000 --user root --pass root file:~/.openclaw/memory/knowledge.db`

**“未配置MCP服务器”**
→ 确保`mcporter`从包含`config/mcporter.json`文件的目录中运行，并且其中定义了surrealdb-memory服务器

**`memory_inject`返回空结果**
→ 检查环境变量中是否设置了`OPENAI_API_KEY`
→ 确保SurrealDB正在运行且数据库模式已初始化

**搜索结果为空**
→ 通过UI或CLI执行提取操作，以从内存文件中填充事实数据

**进度条不更新**
→ 确保在UI更新后重新启动网关服务
→ 检查浏览器控制台中的轮询错误

## 从v1版本迁移

```bash
# Apply v2 schema (additive, won't delete existing data)
./scripts/migrate-v2.sh

# Or manually:
source .venv/bin/activate
python scripts/migrate-v2.py
```

## 统计信息

通过UI（仪表盘）或CLI查看知识图谱：
```bash
mcporter call surrealdb-memory.knowledge_stats
```

示例输出：
```json
{
  "facts": 379,
  "entities": 485,
  "relations": 106,
  "episodes": 3,
  "avg_confidence": 0.99
}
```