---
name: telnyx-rag
description: 使用 Telnyx Storage 和 AI 嵌入技术，对工作区文件进行语义搜索和问答功能。通过这种方式，您可以索引自己的记忆、知识和技能，实现自然语言检索，并获得由 AI 提供的答案。
metadata: {"openclaw":{"emoji":"🧠","requires":{"bins":["python3"],"env":["TELNYX_API_KEY"]},"primaryEnv":"TELNYX_API_KEY"}}
---

# Telnyx RAG内存管理功能

通过Telnix的内置嵌入、相似性搜索和推理API，在您的OpenClaw工作空间中实现基于RAG（Retrieval-Augmented Question Answering）的问答功能。

## 必备条件

- **您自己的Telnix API密钥** — 每个用户/代理都需要使用自己的密钥
- **Python 3.8及以上版本** — 仅使用标准库，无需外部依赖
- 请在[portal.telnyx.com](https://portal.telnyx.com/#/app/api-keys)获取您的API密钥

## 存储桶命名规范

请使用统一的命名规则，以便所有人都能轻松使用：

```
openclaw-{agent-id}
```

| 代理 | 存储桶名称 |
|-------|--------|
| Chief（主代理）| `openclaw-main` |
| Bob the Builder | `openclaw-builder` |
| 语音代理 | `openclaw-voice` |
| 您的代理 | `openclaw-{your-id}` |

**为什么这样命名？**
- **易于查找**：任何人都可以找到相应代理的存储桶
- **避免冲突**：存储桶名称与个人或团队名称无关
- **便于识别**：`openclaw-*`前缀能够将所有代理的存储桶统一显示在Telnix的存储管理界面中

## 快速入门

```bash
cd ~/skills/telnyx-rag

# Set YOUR Telnyx API key (each user/agent uses their own)
echo 'TELNYX_API_KEY=KEY...' > .env

# Run setup with validation
./setup.sh --check    # Validate requirements first
./setup.sh           # Full setup (uses bucket from config.json)

# Search your memory
./search.py "What are my preferences?"

# Ask questions (full RAG pipeline)
./ask.py "What is the porting process?"
```

## 功能介绍

- **索引**：工作空间中的文件（如MEMORY.md、memory/*.md、knowledge/、skills/等）
- **智能分块**：自动将大文件按类型（Markdown文件按标题分块，JSON/Slack文件按消息线程分块）
- **自动嵌入**：利用Telnix的AI技术对文件内容进行嵌入处理
- **自然语言搜索**：支持基于自然语言的查询，并具有重试机制
- **问答处理**：通过完整的RAG流程（检索 → 重新排序 → 生成答案）
- **优先显示来自内存中的内容**：优先显示与当前上下文相关的内容
- **增量同步**：仅上传已更改的文件
- **清理孤儿文件**：删除存储桶中已删除的文件

## 设置选项

### 选项1：环境变量
```bash
export TELNYX_API_KEY="KEY..."
./setup.sh
```

### 选项2：.env文件
```bash
echo 'TELNYX_API_KEY=KEY...' > .env
./setup.sh
```

### 验证模式
```bash
./setup.sh --check    # Validate requirements without making changes
```

### 自定义存储桶名称
```bash
./setup.sh my-custom-bucket
```

## 使用方法

### 提问（RAG流程）
```bash
# Basic question answering
./ask.py "What is Telnyx's porting process?"

# Show retrieved context alongside answer
./ask.py "How do I deploy?" --context

# Use a different model
./ask.py "Explain voice setup" --model meta-llama/Meta-Llama-3.1-8B-Instruct

# More/fewer context chunks
./ask.py "meeting decisions" --num 12

# JSON output for scripting
./ask.py "API usage limits" --json

# Search a different bucket
./ask.py "project timeline" --bucket work-memory
```

### 搜索内存内容
```bash
# Basic search with improved error handling
./search.py "What are David's communication preferences?"

# Search specific bucket
./search.py "meeting notes" --bucket my-other-bucket

# More results with timeout control
./search.py "procedures" --num 10 --timeout 45

# JSON output (for scripts)
./search.py "procedures" --json
```

### 同步文件（分块处理）
```bash
# Incremental sync with auto-chunking
./sync.py

# Override chunk size (tokens)
./sync.py --chunk-size 600

# Quiet mode for cron jobs
./sync.py --quiet

# Remove orphaned files (including stale chunks)
./sync.py --prune

# Sync + trigger embedding
./sync.py --embed

# Check status
./sync.py --status

# List indexed files (shows chunks too)
./sync.py --list
```

### 监控模式
```bash
# Watch for changes and auto-sync with chunking
./sync.py --watch
```

### 触发嵌入功能
```bash
# Trigger embedding for current bucket
./embed.sh
# OR
./sync.py --embed

# Check embedding status
./sync.py --embed-status <task_id>
```

**为什么需要这些设置？** 将文件上传到Telnix存储后，系统不会自动生成嵌入数据。只有通过这些设置，`search.py`和`ask.py`才能正常工作并返回搜索结果。

## 配置文件（config.json）

编辑`config.json`以自定义各项配置：

```json
{
  "bucket": "openclaw-memory",
  "region": "us-central-1",
  "workspace": ".",
  "patterns": [
    "MEMORY.md",
    "memory/*.md",
    "knowledge/*.json",
    "skills/*/SKILL.md"
  ],
  "priority_prefixes": ["memory/", "MEMORY.md"],
  "default_num_docs": 5,
  "chunk_size": 800,
  "ask_model": "meta-llama/Meta-Llama-3.1-70B-Instruct",
  "ask_num_docs": 8,
  "retrieve_num_docs": 20
}
```

### 配置字段

| 字段 | 默认值 | 说明 |
|-------|---------|-------------|
| `bucket` | `openclaw-{agent-id}` | Telnix存储桶名称（参见命名规范） |
| `region` | `us-central-1` | 存储区域 |
| `workspace` | `.` | 文件扫描的根目录 |
| `patterns` | （参见上文） | 需要索引的文件模式 |
| `priority_prefixes` | `["memory/", "MEMORY.md"]` | 在搜索结果中优先显示的文件类型 |
| `exclude` | `["*.tmp", ...]` | 需要排除的文件模式 |
| `chunk_size` | `800` | 每个分块的最大字符数（约4个字符/标记） |
| `ask_model` | `Meta-Llama-3.1-70B-Instruct` | 用于问答处理的LLM模型 |
| `ask_num_docs` | `8` | 用于生成答案的上下文数据量 |
| `retrieve_num_docs` | `20` | 初始检索的文档数量（重排序前的数量） |

## 工作原理

### 智能分块机制

在上传文件之前，系统会自动将大文件拆分为语义相关的块：

- **Markdown文件**：首先根据`##`和`###`标题进行分割；
- 如果某个部分仍然过大，会进一步根据段落边界进行分割；
- 每个分块都会包含元数据，包括来源文件、分块索引和标题。

- **JSON/Slack文件**：按消息中的标记数量进行分组；
- 元数据中会包含频道名称、时间范围和作者信息；
- 分块的文件名具有确定性，便于识别。

### 分块命名规则
```
knowledge/meetings.md  →  knowledge/meetings__chunk-001.md
                          knowledge/meetings__chunk-002.md
                          knowledge/meetings__chunk-003.md
```

### 分块元数据

每个分块都包含一个YAML格式的元数据头：
```
---
source: knowledge/meetings.md
chunk: 2/5
title: Q4 Planning Discussion
---

(chunk content here)
```

### Slack文件导出时的额外信息
```
---
source: slack/general.json
chunk: 3/12
title: general
channel: general
date_range: 2024-01-15 to 2024-01-16
authors: alice, bob, charlie
---
```

### 分块生命周期

- 当源文件发生变化时，系统会删除旧的分块并上传新的分块；
- 分块之间的对应关系会记录在`.sync-state.json`文件中；
- 使用`--prune`参数可以清除因文件删除而产生的“孤儿分块”。

### 重新排序机制（ask.py）

RAG流程采用多信号重排序策略：

1. **语义相似性**：基于Telnix的嵌入距离（表示内容相似度）；
2. **关键词匹配**：使用TF-IDF算法计算关键词与查询内容的匹配程度；
3. **优先级调整**：来自指定来源的分块会获得更高的排序权重；
4. **去重**：如果两个相邻分块的内容高度相似（重叠度超过80%），则合并为一个分块。

初次检索时会获取`retrieve_num_docs`个分块（默认为20个），之后会重新排序并选择最佳的`ask_num_docs`个分块作为答案的生成依据。

## 新功能（v2）

- **智能分块**：Markdown文件按标题分块，Slack JSON文件按消息线程分块；
- 元数据头中包含文件来源、分块索引和标题；
- 分块大小可以通过`--chunk-size`参数或`config.json`文件进行配置；
- 分块文件名具有确定性，便于重复使用。

### RAG问答流程（ask.py）

- **端到端流程**：用户发起查询 → 系统检索 → 重新排序 → 生成答案；
- 使用Telnix的LLM API生成最终答案；
- 每个答案都会包含对应的源文件引用；
- 提供`--context`参数来查看检索到的分块内容；
- 支持`--json`参数以结构化格式输出答案。

### 优化点

- **多信号评分机制**：综合考虑嵌入相似度、关键词匹配度和内容优先级；
- **去重处理**：删除内容高度重复的分块；
- **增量同步**：仅上传已修改的文件；
- **进度跟踪**：支持显示大文件同步的进度条；
- **智能清理**：自动删除本地已删除的文件，并清理不再使用的分块；
- **状态记录**：维护同步历史和分块映射关系；
- **错误处理**：改进了错误处理机制，能够更准确地解析Telnix API的错误响应；
- **配置选项**：支持设置请求超时时间，支持静默运行（`--quiet`参数）。

### 与OpenClaw的集成方法

请将相关配置添加到`TOOLS.md`文件中：
```markdown
## Semantic Memory & Q&A

Ask questions about your workspace:
\`\`\`bash
cd ~/skills/telnyx-rag && ./ask.py "your question"
\`\`\`

Search memory semantically:
\`\`\`bash
cd ~/skills/telnyx-rag && ./search.py "your query"
\`\`\`
```

### 自动同步机制

您可以在系统的心跳脚本或定时任务中调用相关命令进行自动同步：
```bash
# Quiet sync with orphan cleanup
cd ~/skills/telnyx-rag && ./sync.py --quiet --prune

# Sync with embedding
cd ~/skills/telnyx-rag && ./sync.py --quiet --embed
```

## 常见问题及解决方法

### 设置问题

- **“Python版本过低”**：需要Python 3.8及以上版本；
  - 检查版本：`python3 --version`
- **“API密钥验证失败”**：确认密钥是否有效；
  - 请在[portal.telnyx.com](https://portal.telnyx.com/#/app/api-keys)获取新的API密钥。

### 同步问题

- **“找不到存储桶”**：请检查存储桶名称是否正确；
- **“未找到结果”**：同步完成后请等待1-2分钟（嵌入处理需要时间）；
  - 检查上传的文件是否完整：`./sync.py --list`
- **触发嵌入功能**：`./sync.py --embed`

### 问答相关问题

- **“LLM生成失败”**：确认API密钥具有足够的权限；
  - 可以尝试使用其他LLM模型：`./ask.py "query" --model meta-llama/Meta-Llama-3.1-8B-Instruct`
- **“未找到相关文档”**：确保文件已成功同步并嵌入；
  - 可以尝试使用更宽泛的查询关键词。

### API参考

- **Python接口**：[详细说明](```python
from ask import ask
from search import search_memory

# Ask a question (full RAG pipeline)
answer = ask("What is the deployment process?")
print(answer)

# With options
answer = ask(
    "project timeline",
    num_final=5,
    model="meta-llama/Meta-Llama-3.1-8B-Instruct",
    show_context=True,
    output_json=True,
)
print(answer)

# Basic search
results = search_memory("What do I know about X?", num_docs=5)
print(results)
```)
- **Bash接口**：[详细说明](```bash
# Ask and capture answer
answer=$(./ask.py "What are the API limits?" --json)

# Search and capture JSON
results=$(./search.py "query" --json)
```

## 性能优化建议

- **调整分块大小**：较小的分块（400-600个字符）适用于精确检索，较大的分块（800-1200个字符）适用于获取更多上下文信息；
- **使用`--quiet`参数**：减少定时任务的输出信息；
- **定期使用`--prune`参数清理不再使用的文件；
- **监控模式**：开发时可以使用`./sync.py --watch`进行实时监控；
- **批量处理**：先同步文件，再执行嵌入操作：`./sync.py && ./sync.py --embed`

## 致谢

本功能是基于[OpenClaw](https://github.com/openclaw/openclaw)开发的，使用了[Telnix Storage](https://telnyx.com/products/cloud-storage)和AI相关API来实现。