# PersistentMind

**为AI代理提供持久化、可搜索且具有上下文感知功能的内存系统。存储重要信息，再也不会丢失上下文。**

免费且开源（MIT许可证） • 无依赖项 • 本地运行 • 无需API密钥

---

## 为什么需要这个工具？

AI代理在会话之间会忘记所有信息。每次开始新的对话时，都需要重新输入相同的上下文：用户的偏好设置、项目配置、之前犯过的错误以及记录的修正步骤。这个工具可以永久解决这个问题。

### 它解决的问题：
- 代理在会话之间会忘记用户的偏好设置
- 因为修正内容没有被持久化，同样的错误会反复出现
- 每次都需要重新解释项目背景信息
- 无法随着时间的推移建立团队知识库

---

## 核心概念

### 内存类型

| 类型 | 用途 | 示例 |
|------|---------|---------|
| `fact` | 事实性信息 | “数据库使用的是PostgreSQL 16” |
| `preference` | 用户偏好 | “用户更喜欢简洁的回复” |
| `procedure` | 操作步骤 | “使用`poetry run alembic upgrade head`来执行迁移” |
| `correction` | 错误及修正方法 | “切勿使用通配符导入——否则持续集成（CI）会失败” |
| `context` | 背景信息 | “这是一个面向人力资源团队的B2B SaaS产品” |
| `relationship` | 事物之间的关联 | “AuthService依赖于UserRepository” |
| `reminder` | 以后需要处理的提醒 | “在修改数据库架构之前先与团队确认” |

### 内存范围

| 范围 | 持久化方式 | 用途 |
|-------|----------|---------|
| `global` | 永久保存 | 跨项目通用设置、通用规则 |
| `project` | 仅在项目中保存 | 项目特定的事实、操作步骤、修正内容 |
| `session` | 仅保存在当前会话中 | 临时工作笔记 |

---

## 功能

### 1. 存储信息

```python
from persistentmind import PersistentMind, MemoryType, MemoryScope

mm = PersistentMind(project="my-app")

# Critical correction — will always surface first in context
mm.remember(
    "Never use wildcard imports — the linter will fail CI",
    memory_type=MemoryType.CORRECTION,
    scope=MemoryScope.PROJECT,
    importance=10.0,
    tags=["linting", "ci", "imports"]
)

# Global preference — applies everywhere
mm.remember(
    "User prefers code examples over long explanations",
    memory_type=MemoryType.PREFERENCE,
    scope=MemoryScope.GLOBAL,
    importance=8.0
)

# Auto-tags extracted from content automatically if you don't specify
mm.remember(
    "The Stripe API key is in .env as STRIPE_SECRET_KEY",
    memory_type=MemoryType.FACT,
    scope=MemoryScope.PROJECT,
    importance=9.0
)
```

### 2. 搜索信息

```python
# Full-text search with relevance scoring
results = mm.recall("database migrations")
for r in results:
    print(f"[{r.relevance_score:.2f}] [{r.memory.memory_type}] {r.memory.content}")

# Search with filters
results = mm.recall("imports", type_filter="correction", min_importance=7.0)

# Get by type
corrections = mm.recall_by_type(MemoryType.CORRECTION)

# Get by tag
db_memories = mm.recall_by_tag("database")
```

### 3. 将上下文信息插入提示中

```python
# Get a formatted context block to prepend to any prompt
context = mm.get_context(project="my-app", max_tokens_estimate=1500)

prompt = f"""
{context}

---

User request: {user_input}
"""
```

**提示内容：**  
修正内容会始终优先显示，重要性评分决定了显示的顺序。

### 4. 内存管理

```python
# Update an existing memory
mm.update_memory(memory_id="mem_abc123", importance=9.0, tags=["critical"])

# Archive a memory (soft delete)
mm.forget("mem_abc123")

# Permanently delete
mm.forget("mem_abc123", permanent=True)

# Expire automatically after N days
mm.remember("Temp token: abc...", expires_in_days=7)
```

### 5. 去重

```python
# Find near-duplicate memories (dry run — just report)
groups = mm.consolidate(dry_run=True)
for g in groups:
    print(f"Found {g['count']} similar memories:")
    for m in g['memories']:
        print(f"  - {m['content']}")

# Actually merge them
mm.consolidate(dry_run=False)
```

### 6. 团队共享

```python
# Export your memory set
mm.export_memories("team_memories.json")

# Import a colleague's memories
mm.import_memories("team_memories.json")
```

### 7. 统计与摘要

```python
print(mm.format_summary())
```

```
🧠 Total Active Memories: 24  |  Archived: 3
   Avg Importance: 7.4/10

📊 BY TYPE
  • correction             4
  • fact                   8
  • preference             5
  • procedure              4
  • context                3
```

---

## 重要性评分指南

| 评分 | 使用场景 |
|-------|----------|
| 10 | 非常重要——绝不能违反（例如安全规则、持续集成要求） |
| 8-9 | 重要——具有较高优先级或关键事实 |
| 5-7 | 有用但非关键 |
| 1-4 | 可知但优先级较低 |

---

## API参考

### `PersistentMind(storage_path, project, session_id, auto_cleanup_days)`
初始化。数据默认存储在`.persistentmind/`目录下。

### `remember(content, memory_type, scope, tags, importance, project, expires_in_days, source)`
存储新的信息。返回一个`Memory`对象。

### `recall(query, scope_filter, type_filter, project_filter, limit, min_importance)`
搜索信息。返回按相关性排序的`List[MemorySearchResult]`。

### `recall_by_type(memory_type, limit)`
获取所有特定类型的信息，并按重要性排序。

### `recall_by_tag(tag, limit)`
获取所有带有特定标签的信息。

### `get_context(project, max_tokens_estimate)`
获取用于插入提示的格式化上下文内容。修正内容会优先显示。

### `update_memory(memory_id, content, importance, tags)`
更新现有信息的字段。

### `forget(memory_id, permanent)`
将信息归档（默认）或永久删除。

### `consolidate(dry_run)`
查找重复的信息。将`dry_run`设置为`False`以合并这些信息。

### `get_stats()`
返回内存统计信息字典。

### `format_summary()`
生成便于阅读的内存摘要。

### `export_memories(output_file, include_archived)`
将信息导出为JSON格式，用于备份或团队共享。

### `import_memories(input_file, overwrite_duplicates)`
从JSON导出文件中导入信息。

---

## 隐私与安全

- ✅ **零数据传输** — 无数据被发送到任何外部
- ✅ **仅本地存储** — 所有数据都存储在您机器上的`.persistentmind/`目录中
- ✅ **无需API密钥** — 完全不需要任何凭证
- ✅ **无需身份验证** — 无需账户或登录
- ✅ **完全透明** — 使用MIT许可证，源代码公开

---

## 更新日志

### [1.0.0] - 2026-02-16

- ✨ 首次发布 — PersistentMind
- ✨ 支持7种内存类型：事实、偏好、操作步骤、上下文、修正内容、关联关系、提醒
- ✨ 3种存储范围：全局、项目、会话
- ✨ 全文搜索功能，包含相关性评分、重要性排序、时效性衰减机制
- ✨ 可通过`get_context()`将上下文信息插入提示中
- ✨ 从内容中自动提取标签
- ✨ 通过合并重复信息来优化存储空间
- ✨ 支持导出/导入功能，便于团队共享
- ✨ 自动清理过期的会话数据
- ✅ 无依赖项，仅本地存储，采用MIT许可证

---

**最后更新时间**：2026年2月16日
**当前版本**：1.0.0
**状态**：活跃且由社区维护

© 2026 UnisAI社区