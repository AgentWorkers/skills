---
name: midos-memory-cascade
description: 一种自动扩展的多层内存搜索机制：该机制从内存缓存开始，逐步扩展到 SQLite 数据库、grep 工具以及 LanceDB 向量搜索引擎，以最小的延迟找到最佳答案。
metadata:
  {}
---
# MidOS 内存级联系统

这是一个具备自调优和自动扩展功能的搜索引擎，它会按照从快到慢的顺序依次尝试不同的内存存储层，一旦找到高置信度的答案，就会立即停止搜索。

## 功能概述

与传统的代理机制不同，该系统会自动尝试所有存储层来处理查询请求：

| 存储层 | 存储方式 | 响应时间 | 查找策略 |
|------|---------|---------|----------|
| T0 | 内存会话缓存 | <1ms | 通过精确匹配或模糊匹配关键字进行查找 |
| T1 | JSON 格式的数据文件 | <5ms | 通过文件名和关键字进行匹配 |
| T2 | SQLite 数据库（pipeline_synergy.db） | <5ms | 使用结构化 SQL 的 LIKE 语句进行查询 |
| T3 | SQLite 的 FTS5 支持 | <1ms | 在 22,000 行数据中查找全文本关键字 |
| T4 | 对 46,000 个数据块进行 grep 操作 | 约 3 秒 | 作为最后的手段，采用暴力搜索（brute-force grep） |
| T5 | LanceDB 关键字搜索（基于 BM25 算法） | 响应时间较长 | 需要处理 670,000 条向量数据，不支持嵌入式查询 |
| T5b | LanceDB 语义搜索 | 3–30 秒 | 使用嵌入式相似度算法进行查询，为最后的解决方案 |

**问题路由规则：** 以 “how/what/why” 等开头的查询会直接跳过关键字搜索层，转而使用语义搜索功能。

**自学习机制：** 该系统会记录每次查询所使用的存储层。随着查询历史的积累，`evolve()` 函数会学习到最优的查询路径（直接跳转到能够快速找到答案的存储层），并将那些始终无法提供有效结果的存储层标记为可跳过的选项。

## 使用方式

### Python API

```python
from tools.memory.memory_cascade import recall, store

# Search across all tiers
result = recall("adaptive alpha reranking")
# → {"answer": {...}, "tier": "T5:lancedb", "latency_ms": 340, "confidence": 0.87}

# Write to the right storage automatically
store("pattern", content="...", tags=["ml", "reranking"])
```

### 命令行界面（CLI）

```bash
# Search
python memory_cascade.py recall "query here"

# View tier resolution stats
python memory_cascade.py stats

# Run self-evolution (learn shortcuts + tier skips)
python memory_cascade.py evolve
```

### `recall()` 函数的选项

```python
recall(
    query: str,
    min_confidence: float = 0.5,  # stop escalating at this threshold
    max_tier: int = 6             # 0=T0 only, 6=all tiers
)
```

**返回值：**

```json
{
  "answer": { "source": "...", "text": "..." },
  "confidence": 0.87,
  "latency_ms": 340.2,
  "tiers_tried": 3,
  "resolved_at": "T5:lancedb",
  "shortcut": null,
  "question_routed": false,
  "escalation": [...]
}
```

## 系统要求

- Python 3.10 及以上版本（核心搜索逻辑仅依赖标准库）
- 可选：`hive_commons` 模块（用于支持 LanceDB 存储层 T5/T5b）
- 可选：`tools.memory.memory_router` 模块（用于实现数据存储的路由功能）

**容错机制：** 如果 LanceDB 无法使用，系统会自动降级为使用 grep（T4）进行查询。所有基于标准库的存储层（T0–T4）均无需额外依赖即可正常运行。

## 架构特点

- **线程安全：** 会话缓存使用 `threading.Lock` 来确保并发安全性；统计数据的写入操作使用独立的锁机制。
- **跨进程安全：** JSONL 数据的写入操作会利用操作系统提供的文件锁定机制（Windows 上使用 `msvcrt`，Unix 上使用 `fcntl`）。
- **置信度评分机制：** 根据术语的重叠程度、匹配结果的准确性以及内容的丰富程度来计算置信度得分（分数范围为 0–1）。
- **统计数据持久化：** 数据统计结果会保存在 `knowledge/SYSTEM/cascade_stats.json` 文件中。

该系统由 MidOS 构建，是 MidOS 提供的 200 多项技能之一。更多相关信息请访问 [midos.dev/pro](http://midos.dev/pro)。

---

（注：由于代码块内容较长且包含具体的技术细节，翻译时仅保留了核心功能和架构描述。对于代码示例、命令行命令以及具体的实现细节，建议直接参考原始的 SKILL.md 文件。）