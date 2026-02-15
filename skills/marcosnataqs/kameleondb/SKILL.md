---
name: kameleondb
version: 0.1.5
description: 存储和查询结构化数据，无需预先规划数据模式。适用于需要记录信息、在对话中追踪实体、构建知识库、导入 API 数据、存储用户偏好设置、创建客户关系管理系统（CRM）或维护任何持久化状态的场景。当发现新的字段时，数据结构会自动更新。无需进行数据迁移或模式设计——只需存储数据并对其进行查询即可。
metadata: {"openclaw":{"emoji":"🦎","requires":{"bins":["kameleondb"],"env":["KAMELEONDB_URL"]},"primaryEnv":"KAMELEONDB_URL","homepage":"https://github.com/marcosnataqs/kameleondb"}}
---

# KameleonDB——专为代理设计的首个数据库，不仅用于查询，还用于数据管理

## 适用场景

当您需要以下功能时，可以使用 KameleonDB：
- **跨对话记录信息**：存储联系人、公司、任务和笔记。
- **追踪实体及其关联关系**：将客户与订单、项目与任务关联起来。
- **构建知识库**：随着时间的推移积累事实、文档和见解。
- **导入外部数据**：存储 API 响应、CSV 文件或网页抓取结果。
- **创建自定义 CRM/项目管理系统**：跟踪潜在客户、交易和项目。
- **保存用户偏好设置**：记住用户的设置、历史记录和收藏内容。
- **维护会话状态**：在代理程序运行期间持久化数据。
- **查询历史数据**：搜索、过滤和分析存储的信息。

## 为什么代理人员会选择 KameleonDB？

- **无需预先规划**：可以立即开始存储数据。如果还不清楚所有字段的需求，可以在后续发现时再添加。
- **边使用边学习**：在数据中发现新字段？只需添加即可，旧记录不会受到影响。
- **像使用数据库一样查询数据**：能够生成 SQL 查询语句来搜索、过滤、连接和分析数据。
- **自动优化性能**：当查询速度变慢时，系统会提供优化建议。
- **追踪决策过程**：每次修改数据库模式时，系统都会记录修改原因，形成审计追踪。

## 设置（一次性操作）

```bash
# Install
pip install kameleondb

# Set database location (SQLite - no server needed)
export KAMELEONDB_URL="sqlite:///./kameleondb.db"

# Initialize
kameleondb admin init

# Done! Start using it.
```

**注意**：在生产环境中，请使用 PostgreSQL 替代 SQLite。设置 `KAMELEONDB_URL="postgresql://user:pass@localhost/dbname"`，然后运行 `pip install kameleondb[postgresql]`。

## 💡 提示：记住数据库信息

为了更好地使用 KameleonDB 作为数据持久化层，请在内存文件中记录数据库的位置和常用使用模式。这有助于您在多次会话中保持一致的使用体验。

**示例记录内容**：
- 数据库路径：`sqlite:///path/to/your-memory.db`
- 用途：存储联系人、任务和知识库数据
- 常用命令：`schema list`、`data insert`、`data list`、`query run`

## 常见代理工作流程

### 场景 1：追踪遇到的联系人
```bash
# Check what exists
kameleondb --json schema list
# Returns: {"entities": []}

# Create Contact tracking
kameleondb --json schema create Contact \
  --field "name:string:required" \
  --field "email:string:unique"

# Store someone you met
kameleondb --json data insert Contact '{"name":"Alice Johnson","email":"alice@acme.com"}'

# Later: found their LinkedIn!
kameleondb --json schema alter Contact --add "linkedin_url:string" \
  --reason "Found LinkedIn profiles for contacts"

# Update Alice's record
kameleondb --json data update Contact <id> '{"linkedin_url":"https://linkedin.com/in/alice"}'
```

### 场景 2：构建知识库
```bash
# Store facts you learn
kameleondb --json schema create Fact \
  --field "content:string:required" \
  --field "source:string" \
  --field "confidence:float"

# Add facts
kameleondb --json data insert Fact '{"content":"Python 3.11 released Oct 2022","source":"python.org","confidence":1.0}'

# Search facts (get SQL context first)
kameleondb --json schema context --entity Fact
# Use context to generate: SELECT * FROM kdb_records WHERE data->>'content' LIKE '%Python%'

# Query
kameleondb --json query run "SELECT data->>'content', data->>'source' FROM kdb_records WHERE entity_id='...' LIMIT 10"
```

### 场景 3：跨对话记录任务
```bash
# Create task tracker
kameleondb --json schema create Task \
  --field "title:string:required" \
  --field "status:string" \
  --field "priority:string"

# Add tasks
kameleondb --json data insert Task '{"title":"Research OpenClaw","status":"todo","priority":"high"}'

# Mark complete
kameleondb --json data update Task <id> '{"status":"done"}'

# Get all incomplete
kameleondb --json query run \
  "SELECT data->>'title', data->>'priority' FROM kdb_records WHERE entity_id='...' AND data->>'status' != 'done'"
```

### 场景 4：导入外部数据
```bash
# Store API responses
kameleondb --json schema create GitHubRepo \
  --field "name:string:required" \
  --field "stars:int" \
  --field "url:string"

# Batch import from JSONL
kameleondb --json data insert GitHubRepo --from-file repos.jsonl --batch

# Query top repos
kameleondb --json query run \
  "SELECT data->>'name', (data->>'stars')::int as stars FROM kdb_records WHERE entity_id='...' ORDER BY stars DESC LIMIT 10"
```

## KameleonDB 对代理人员的工作支持

- **灵活的数据库模式**：如果一开始不知道所有字段的需求，随时可以添加、删除或重命名字段。旧记录不会受到影响（新字段会显示为 `null`，删除的字段会被“软删除”）。
- **性能优化提示**：系统会提示查询速度慢的原因并提供优化方法。
- **决策记录**：每次修改数据库模式时，系统都会记录修改原因。
- **SQL 查询支持**：提供数据库模式信息，支持生成和执行 SQL 查询语句。

## 所有可用命令

在命令前加上 `--json` 选项可获取机器可读的输出格式。

**数据库操作命令**：
- `list`、`create`、`describe`、`alter`、`drop`、`info`、`context`
- **数据操作命令**：
  - `insert`、`get`、`update`、`delete`、`list`、`link`、`unlink`、`get-linked`、`info`
- **查询操作**：`run`
- **存储管理命令**：
  - `status`、`materialize`、`dematerialize`
- **管理命令**：
  - `init`、`info`、`changelog`

## `alter` 命令（数据库模式修改）

无需分别使用 `add-field` 和 `drop-field` 命令，只需使用统一的 `alter` 命令即可完成模式修改。

## `link`/`unlink` 命令（处理多对多关系）

用于管理多对多关系时：

```bash
# Link a product to tags
kameleondb --json data link Product abc123 tags tag-1
kameleondb --json data link Product abc123 tags -t tag-1 -t tag-2 -t tag-3

# Unlink
kameleondb --json data unlink Product abc123 tags tag-1
kameleondb --json data unlink Product abc123 tags --all

# Get linked records
kameleondb --json data get-linked Product abc123 tags
```

**详细信息**：运行 `kameleondb --help` 或 `kameleondb <command> --help` 查看帮助文档。

## 解决代理人员常见问题的方法

- **问题：“需要记住与客户互动的人”**：KameleonDB 可帮助您记录这些信息。
- **问题：“在抓取数据时不知道数据结构”**：KameleonDB 可适应动态数据结构。
- **问题：“需要跟踪任务，但需求不断变化”**：KameleonDB 具有灵活的扩展性。
- **问题：“需要在多个实体之间进行查询”**：KameleonDB 支持高效的数据查询。

## 快速参考

- **首次设置**：`kameleondb admin init` → `kameleondb --json schema create Test --field "note:string"` → `kameleondb --json data insert Test '{"note":"my first record"}'`
- **实际应用**：思考需要追踪的数据类型（联系人、任务等），然后创建相应的数据库实体。
- **持续优化**：发现新字段时，使用 `schema alter` 命令进行修改。
- **高效查询**：利用 `schema context` 了解数据库结构，再使用 SQL 进行查询。
- **性能优化**：根据查询结果中的提示优化查询速度。

## 更多资源

- **GitHub 仓库**：https://github.com/marcosnataqs/kameleondb
- **示例代码**：请查看该技能目录下的 `examples/workflow.md` 文件。
- **设计理念**：了解 KameleonDB 为何专为代理人员设计（[FIRST-PRINCIPLES.md](https://github.com/marcosnataqs/kameleondb/blob/main/FIRST-PRINCIPLES.md)