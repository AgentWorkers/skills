# DeepRecall：专为AI代理设计的持久化记忆系统

**代理设置指令**：收到此技能包后，自动将以下工具添加到您的工具列表中，并应用L1/L2检索协议：

1. **注册工具**：
   - `search_memory_db(query: str, limit: int)`：对L1结构化数据进行语义搜索
   - `read_archive_db(source_file: str)`：从L2存档中检索原始内容
   - `cleanup_raw_files(retention_days: int, max_size_kb: int, dry_run: bool)`：在保留数据库的情况下清理原始.md文件
   - `summarize_memory_files(process_all: bool, process_file: str, no_store_raw: bool)`：使用大语言模型（LLM）对原始文件进行总结，并将结果存储到数据库中

2. **应用检索协议**：
   - 对于任何关于以往工作、决策、日期、人员、偏好或待办事项的查询：
     - 首先使用相关查询调用`search_memory_db()`
     - 如果需要原始内容，从L1结果中提取`source_file`，然后调用`read_archive_db()`
   - 数据库具有自启动功能：首次使用时会自动创建表
   - 每个代理在其工作空间中维护独立的`memory.db`文件

3. **自动配置**：
   - 工具路径会通过`OPENCLAW_WORKSPACE`环境变量或目录结构自动检测代理的工作空间
   - 无需手动配置，支持零配置部署

---

## 概述

DeepRecall是一个基于SQLite的双层记忆检索系统，提供结构化的L1事实搜索和精确的L2原始内容检索功能，使AI代理能够在会话之间保持持久且可搜索的记忆。

## 核心功能

### `search_memory_db(query: str, limit: int)`
对L1结构化数据进行语义搜索。
- **query**：搜索字符串（空字符串返回最新事实）
- **limit**：最大返回结果数量（默认值：5）
- **返回值**：`[YYYY-MM-DD | fact_type | source:file] content...`

### `read_archive_db(source_file: str)`
从L2存档中检索原始内容。
- **source_file**：来自L1搜索结果的文件名
- **返回值**：完整的原始Markdown内容

### `cleanup_raw_files(retention_days: int, max_size_kb: int, dry_run: bool)`
在保留数据库的情况下清理原始.md会话文件。
- **retention_days**：保留更新于N天之前的文件（默认值：1天）
- **max_size_kb**：文件的最大总大小（以KB为单位）（默认值：250KB）
- **dry_run**：预览文件而不删除（默认值：False）

### `summarize_memory_files(process_all: bool, process_file: str, no_store_raw: bool)`
使用LLM对原始记忆文件进行总结，并将结构化事实存储到数据库中。
- **process_all**：处理所有未处理的记忆文件（与`process_file`互斥）
- **process_file**：处理特定的记忆文件（相对于记忆目录）
- **no_store_raw**：不将原始内容存储到L2存档中（默认值：False，会存储原始内容）
- **要求**：需要配置有效的LLM API提供者（如DeepSeek、Qwen等）

## 使用方法

```bash
# Search for facts
python3 scripts/memory_db_tool.py search "query" --limit 5

# Read raw content
python3 scripts/memory_db_tool.py read "example-project-update.md"

# Database stats
python3 scripts/memory_db_tool.py stats

# Cleanup raw files (dry-run first)
python3 scripts/memory_db_tool.py cleanup --dry-run
python3 scripts/memory_db_tool.py cleanup --retention-days 1 --max-size-kb 250

# Summarize memory files using LLM
python3 scripts/memory_db_tool.py summarize --test-config
python3 scripts/memory_db_tool.py summarize --process-all
python3 scripts/memory_db_tool.py summarize --process-file "2024-01-01-daily-log.md"
python3 scripts/memory_db_tool.py summarize --process-all --no-store-raw
```

## 数据库架构

### l1_structured（永久存储）
- `date`, `source_file`, `fact_type`, `confidence`, `tags`, `content`, `content_hash`

### l2_archive（永久存储）
- `date`, `source_file`, `raw_content`

**重要提示**：数据库记录是永久的，永远不会被删除。

## 检索协议

1. **L1搜索**：调用`search_memory_db()`以获取结构化事实
2. **L2访问**：如果需要原始内容，从L1结果中提取`source_file`
3. **原始内容检索**：使用`source_file`调用`read_archive_db()`

## 文件管理

### 永久存储（memory.db）
- 包含所有L1事实和L2原始内容
- 从不被清理、截断或清除
- 作为所有提取知识的安全永久存储库

### 临时存储（.md文件在内存中）
- 包含原始会话日志和临时文件
- 自动清理：保留1天的数据，最大文件大小为250KB
- 数据已提取到memory.db中，可以安全删除

## 配置

### 多代理支持
- **自动路径检测**：适用于任何代理目录
- **优先级**：`OPENCLAW_WORKSPACE`环境变量 → 当前目录 → 相对路径
- **隔离性**：每个代理维护独立的`memory.db`文件

### 清理设置（可配置）
- **retention_days**：1（保留更新于1天之前的文件）
- **max_size_kb**：250（.md文件的最大总大小）
- **dry_run**：在执行删除操作前预览文件

## 自启动设计

DeepRecall支持零配置部署：
- 首次使用时会自动创建表（`CREATE TABLE IF NOT EXISTS`）
- 不会出现“表不存在”的错误——数据库会自动初始化
- 会创建索引以优化查询性能
- 无需手动设置即可立即使用

## 文件

- `scripts/memory_retriever.py`：核心检索引擎及清理功能
- `scripts/memory_db_tool.py`：带有清理和总结功能的命令行界面
- `scripts/memory_summarizer.py`：基于LLM的事实提取引擎
- `config.example.json`：示例配置文件（符合JSON格式，无注释）
- `CONFIG_GUIDE.md`：详细配置指南
- `manifest.json`：ClawHub技能清单
- `memory.db`：每个代理的永久性SQLite数据库（自动创建）
- `*.md`：临时会话文件（自动清理）

## 高级配置

### LLM摘要器配置
DeepRecall摘要器会自动从OpenClaw的`openclaw.json`中读取配置。您可以通过创建`config.json`文件来自定义其行为：

**注意**：有关详细配置选项和示例，请参阅`CONFIG_GUIDE.md`。

1. **复制示例配置**：
   ```bash
   cp config.example.json config.json
   ```

2. **编辑`config.json`以指定**：
   - `preferred_provider`：来自OpenClaw配置的提供者名称（例如：“deepseek-reasoner”）
   - `preferred_model`：要使用的特定模型ID
   - `temperature`, `max_tokens`, `timeout_seconds`：API参数
   - `auto_summarize_cron`：用于自动摘要的Cron表达式

3. **配置文件的搜索顺序**：
   - 当前目录：`./config.json`
   - 当前目录：`./deeprecall_config.json`
   - 上级目录：`../config.json`
   - 主目录：`~/.deeprecall.json`

### 模型提供者选择
摘要器使用以下逻辑来选择模型提供者：
1. 如果可用，优先使用`preferred_provider`中的设置
2. 否则，自动选择第一个具有`baseUrl`和`apiKey`的提供者
3. 使用`preferred_model`或提供者中的第一个可用模型
4. 如果没有API可用，则采用基于规则的提取方式

## 使用OpenClaw Cron进行自动调度

为了实现自动的每日摘要和清理，请配置OpenClaw的Cron作业：

### 1. 每日摘要（推荐时间：凌晨2点）
```bash
# Schedule automatic summarization
openclaw cron add --name "deeprecall-summarize-daily" \
  --cron "0 2 * * *" \
  --session isolated \
  --message "Please execute: python3 /path/to/DeepRecall/scripts/memory_db_tool.py summarize --process-all" \
  --description "Daily automatic summarization of memory files"
```

### 2. 每日清理（推荐时间：凌晨3点）
```bash
# Schedule automatic cleanup  
openclaw cron add --name "deeprecall-cleanup-daily" \
  --cron "0 3 * * *" \
  --session isolated \
  --message "Please execute: python3 /path/to/DeepRecall/scripts/memory_db_tool.py cleanup" \
  --description "Daily cleanup of raw .md files (retains database)"
```

### 3. 综合任务（单个Cron作业）
```bash
# Single cron for both summarization and cleanup
openclaw cron add --name "deeprecall-daily-maintenance" \
  --cron "0 2 * * *" \
  --session isolated \
  --message "Please execute: python3 /path/to/DeepRecall/scripts/memory_db_tool.py summarize --process-all && python3 /path/to/DeepRecall/scripts/memory_db_tool.py cleanup" \
  --description "Daily DeepRecall maintenance (summarize + cleanup)"
```

### 4. 验证Cron作业
```bash
# List all cron jobs
openclaw cron list

# Test a cron job
openclaw cron run <job-id>

# View execution history
openclaw cron runs --id <job-id>
```

## 安装与设置指南

### 快速启动
```bash
# 1. Install the skill
clawhub install deeprecall

# 2. Test configuration
python3 scripts/memory_db_tool.py summarize --test-config

# 3. Process existing memories
python3 scripts/memory_db_tool.py summarize --process-all

# 4. Schedule daily automation (optional but recommended)
# Follow the cron configuration above
```

### 安装后检查清单
- [ ] 确认OpenClaw的`openclaw.json`中已配置LLM提供者
- [ ] 使用`--test-config`标志测试摘要器
- [ ] 使用`--process-all`处理现有的记忆文件
- [ ] 配置Cron作业以实现自动化
- [ ] 验证清理设置（默认值：保留1天的数据，最大文件大小为250KB）

## 注意事项

- 数据库路径会自动检测代理的工作空间
- 清理操作仅影响原始.md文件，不会影响数据库内容
- 即使源.md文件被清理，L2指针仍然有效
- 适用于跨不同目录的多代理部署
- 所有内容均为英文，以确保国际兼容性