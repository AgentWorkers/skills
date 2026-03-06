---
name: eidolon-search
description: 使用 SQLite 的 FTS5 功能进行 AI 代理的内存搜索：与直接读取完整文件相比，可以减少 90% 以上的存储空间占用（同时搜索速度提升 10 倍以上）。适用于代理需要高效地搜索 Markdown 格式的记忆文件、日常笔记或任何文本语料库的场景。该功能在内存搜索、文件搜索、知识检索过程中触发，尤其是在上下文窗口有限且读取完整文件成本过高的情况下非常实用。
---
# Eidolon 搜索工具

这是一个基于 FTS5（Full-Text Search 5）技术的 AI 代理内存搜索工具。它会对 Markdown 文件进行一次索引构建，之后进行搜索时能够节省 90% 以上的搜索资源（即减少所需的查询次数或数据量）。

## 快速入门

### 1. 构建索引（仅一次）

```bash
python3 scripts/build-index.py <memory_dir> <db_path>
```

示例：
```bash
python3 scripts/build-index.py ./memory ./memory.db
```

该命令会在当前目录及其子目录中，对所有 `.md` 格式的文件创建一个包含 FTS5 全文索引的 SQLite 数据库（支持递归搜索）。

### 2. 进行搜索

```bash
python3 scripts/search.py <query> [limit] [db_path]
```

示例：
```bash
python3 scripts/search.py "Physical AI roadmap" 5
python3 scripts/search.py "project timeline" 10 ./memory.db
```

- 默认搜索限制：10 条结果
- 默认数据库路径：`./memory.db`
- 搜索结果会包含文件路径和相关性评分

### 3. 文件更新时重新构建索引

只需再次运行 `build-index.py` 即可。该命令会从头开始重新构建索引（速度很快，通常在 1 秒内完成）。

## 适用场景

- **内存文件搜索**：在大量日常笔记或记忆记录中查找特定信息
- **资源受限的环境**：当读取所有文件会超出系统资源限制时
- **重复搜索**：只需构建一次索引，之后可多次使用
- **大型工作空间**：包含 10 个以上 Markdown 文件，文件总大小超过 50KB 的场景

## 不适用场景

- 单个文件（小于 5KB）：直接读取文件内容即可
- 需要基于语义/意义的搜索：FTS5 仅支持基于关键词的搜索
- 有关已知限制，请参阅 [references/QUALITY.md](references/QUALITY.md)

## 代理搜索技巧

FTS5 是基于关键词的搜索引擎。以下方法可提升搜索效果：
- 使用具体术语：例如使用 “Jetson Orin” 而不是 “hardware plans”
- 使用 “OR” 连接同义词：例如 “car OR vehicle OR automobile”
- 使用引号标注短语：例如 “Physical AI”
- 如果初次搜索无结果，可尝试多次查询
- 根据搜索结果中的文件路径查看完整内容以获取更多背景信息

## 性能测试

- 搜索资源节省：90% 以上（实际测试结果为 93%–98.9%）
- 搜索速度：提升 15 倍（实际测试结果为 10–20 倍）
- 详细性能数据请参阅 [references/PERFORMANCE.md](references/PERFORMANCE.md)

你可以自行运行性能测试：
```bash
python3 scripts/benchmark-recall.py    # Recall@5, Recall@10
python3 scripts/benchmark-cache.py     # Warm vs cold cache
```

## 数据库架构

```sql
CREATE VIRTUAL TABLE memory_fts USING fts5(path, content);
```

- 直接通过 SQL 进行数据查询：
```bash
sqlite3 memory.db "SELECT path, snippet(memory_fts, 1, '<b>', '</b>', '...', 32) FROM memory_fts WHERE memory_fts MATCH 'query' ORDER BY rank LIMIT 5;"
```