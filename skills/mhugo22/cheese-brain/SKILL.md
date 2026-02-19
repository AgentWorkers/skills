---
name: cheese-brain
description: 这是一个基于 DuckDB 的知识管理系统，支持快速检索 22 种以上的实体类型（项目、联系人、工具、工作流程、决策等）。当您需要回顾过去项目的背景信息、查找配置细节、获取工具文档、检索联系人信息、搜索工作流程/程序，或查询任何被记录的知识时，都可以使用该系统。该系统支持亚毫秒级的关键词搜索以及带有相关性排序的 BM25 全文搜索功能。
---
# Cheese Brain

这是一个为AI代理和人类设计的快速、持久的知识库。它能够存储和检索各种实体（项目、联系人、工具、工作流程、决策等），并提供亚毫秒级的搜索速度。

## 安装

Cheese Brain是一个Python包，使用前需要先进行安装：

```bash
# Clone the repository
git clone https://github.com/mhugo22/cheese-brain.git
cd cheese-brain

# Create virtual environment and install
python3 -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -e .
```

**验证安装：**

```bash
cheese-brain stats
```

如果显示了相关统计信息（实体数量、数据库大小），则表示安装成功。

## 适用场景

在以下情况下可以使用Cheese Brain：

- **回顾项目信息**：例如“email-monitor项目是哪个？”——可立即获取项目的详细信息，包括仓库地址、路径和计划安排。
- **查找工具**：例如“备份脚本在哪里？”——可获取工具的位置、使用方法及相关工作流程。
- **查找联系人信息**：例如“Scout日历的URL是什么？”——可获取联系人的日历URL、位置和时区信息。
- **搜索工作流程**：例如“如何恢复配置？”——可获取详细的步骤及所需工具。
- **检索决策记录**：例如“我们为什么选择DuckDB？”——可查看过去的决策及其理由和日期。
- **查询基础设施信息**：例如“Telegram频道的ID是多少？”——可获取频道的集成详情及相关配置信息。

**主要优势：**数据在会话之间保持持久化。你无需手动“记住”信息，只需查询Cheese Brain即可立即获取所需内容。

## 常见使用模式

### 快速搜索（最常用）

```bash
# Keyword search (fast, loose matching)
cheese-brain search "email monitor"
cheese-brain search "backup config"
cheese-brain search "calendar feed"

# Full-text search (BM25 relevance ranking)
cheese-brain fts "email monitoring"
cheese-brain fts "backup config" --category tool
```

**输出结果：**包含标题、类别、标签以及匹配实体的全部详细信息的表格。

### 获取特定实体

当搜索结果有多个时，可以通过ID获取具体实体：

```bash
cheese-brain get <entity-id>
```

**输出结果：**包含实体全部详细信息的JSON对象（如路径、URL、计划安排等）。

### 添加新实体

当你发现需要长期保存的新内容时，可以执行以下操作：

```bash
cheese-brain add \
  --title "New Project Name" \
  --category project \
  --tags "tag1,tag2,tag3" \
  --data '{"repo": "https://github.com/...", "status": "active"}'
```

**实体类别：**项目、工具、工作流程、联系人、决策、书签、基础设施、想法等。
**数据字段：**用于存储实体特定详细信息的JSON字段（如路径、URL、计划安排、凭据等）。

### 更新实体

```bash
cheese-brain update <entity-id> --title "New Title" --tags "new,tags"
cheese-brain update <entity-id> --data '{"status": "shipped", "deployed": "2026-02-17"}'
```

### 列出和浏览实体

```bash
cheese-brain list                     # All entities (most recent first)
cheese-brain list --category project  # Filter by category
cheese-brain list --tag shipped       # Filter by tag
cheese-brain list --limit 10          # Limit results
```

### 统计和标签信息

```bash
cheese-brain stats                    # Database statistics
cheese-brain tags                     # Tag usage analysis
```

## 按使用场景查询示例

- **“email-monitor项目是哪个？”**
- **“如何备份配置？”**
- **“日历的URL是什么？”**
- **“有哪些项目已经发布？”**
- **“查找与监控相关的信息”**

## 高级功能

### 全文搜索（FTS）

当知识库中的实体数量较多时，可以使用全文搜索功能获得按相关性排序的结果：

```bash
# First-time setup (one-time only)
cheese-brain create-fts-index

# Search with relevance ranking
cheese-brain fts "backup automation"
cheese-brain fts "email calendar" --category tool
cheese-brain fts "security logging" --limit 10
```

**何时使用全文搜索？**
- **全文搜索：**适用于大型知识库（超过100个实体）、多词查询或需要优先获取最相关结果的情况。
- **关键词搜索：**适用于快速查找、精确匹配或小型知识库的情况。

### 导出和备份

```bash
# JSON export (human-readable)
cheese-brain export backup.json

# Parquet export (2-9x smaller, columnar format)
cheese-brain export backup.parquet --format parquet

# Restore from backup
cheese-brain restore-backup backup.json  # Auto-detects format
```

**注意：**可能已经通过OpenClaw的cron任务配置了自动每日备份（请查看`~/.cheese-brain/backups/`目录）。

## 数据模型

每个实体包含以下字段：

- **id**（UUID）：唯一标识符
- **title**（字符串）：实体名称
- **category**（字符串）：实体类型（项目、工具、联系人等）
- **tags**（数组）：可搜索的标签
- **data**（JSON）：结构化数据（如路径、URL、计划安排等）
- **created_at** / **updated_at** / **deleted_at**（时间戳）

**实体示例：**

```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "title": "Email Monitor Project",
  "category": "project",
  "tags": ["automation", "nodejs", "gmail", "calendar", "telegram", "shipped"],
  "data": {
    "repo": "https://github.com/username/email-monitor",
    "path": "/path/to/workspace/email-monitor/",
    "schedule": "7am, 1pm, 5pm, 9pm CST",
    "run_command": "node process.js",
    "telegram_channel": "-100XXXXXXXXXX"
  },
  "created_at": "2026-02-17T06:55:00Z",
  "updated_at": "2026-02-17T08:30:00Z"
}
```

## 性能

- **搜索速度：**关键词搜索<1毫秒；全文搜索约5毫秒
- **数据库大小：**每个实体约0.3MB（具体取决于数据字段的复杂度）
- **扩展性：**支持存储超过10万个实体（全文搜索时间不变，关键词搜索为线性扫描）

## 故障排除

- **命令找不到：**确保虚拟环境已激活：`source /path/to/cheese-brain/venv/bin/activate`
- 或使用完整路径：`/path/to/cheese-brain/venv/bin/cheese-brain`

- **数据库被锁定：**关闭其他正在运行的Cheese Brain进程
- 检查`~/.cheese-brain/`目录下是否存在锁文件。

- **查询速度慢：**
  - 如果尚未创建全文搜索索引，请执行`cheese-brain create-fts-index`命令。
  - 检查数据库大小：`cheese-brain stats`
  - 考虑归档旧数据（使用`--deleted`标志进行软删除）。

## 文档资料

- **完整文档：**https://github.com/mhugo22/cheese-brain
- **备份/恢复指南：**仓库中的`BACKUP_RECOVERY.md`
- **全文搜索指南：**仓库中的`FTS.md`
- **性能分析：**仓库中的`PERFORMANCE_ANALYSIS.md`
- **安全指南：**仓库中的`SECURITY.md`

## 安全特性

- **文件权限：**数据库和备份文件自动设置为仅所有者可访问（权限设置为`0600`）。
- **敏感信息隐藏：**`api_key`、`token`、`password`等敏感信息会自动隐藏（使用`--reveal`命令可显示）。
- **加密导出：**使用`cheese-brain export --encrypt`命令可生成加密备份文件。
- **数据验证：**每个实体最大存储量为1MB，支持最多10层嵌套结构，具备SQL注入防护机制。

**最佳实践：**不要将敏感信息以明文形式存储。建议使用密码管理工具（如1Password、Bitwarden）并妥善管理这些信息：

```json
{"api_key_location": "1Password: OpenAI API", "notes": "Retrieve from vault"}
```

## 使用技巧

1. **统一使用标签**：使用小写、连字符分隔的标签格式（例如`email-monitoring`，而非`Email Monitoring`）。
2. **使用数据字段**：将结构化信息（如路径、URL、计划安排等）存储在JSON数据字段中，以便于查询。
3. **先搜索再获取**：先使用搜索功能找到目标实体，再使用`get <id>`命令获取详细信息。
4. **使用全文搜索**：在不确定搜索内容时，优先使用全文搜索功能。
5. **定期更新数据**：确保实体信息始终保持最新状态（如状态更新、URL变更等）。
6. **采用软删除机制**：避免直接删除实体，使用`--deleted`标志标记为非活跃状态（数据可恢复）。