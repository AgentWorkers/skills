---
name: minimal-memory
description: Maintain clean, efficient memory files with GOOD/BAD/NEUTRAL categorization and semantic search. Use when managing agent memory, deciding what to store, searching past memories, or organizing knowledge. Triggers on: memory cleanup requests, "remember this", "search memory", memory organization discussions, or when MEMORY.md grows too large.
---

# 最小化内存管理

通过结构化的分类和双层存储方式，保持代理程序内存的精简、易搜索性和可操作性。

## 核心原则

- **MEMORY.md**：长期重要的内容（仅记录好的或坏的学习经验）
- **memory/YYYY-MM-DD.md**：每日操作记录（标记为“好”、“坏”或“中立”）

## 信息分类

为每条内存记录添加相应的标签：

| 标签 | 含义 | 是否应保存在 MEMORY.md 中？ | 示例 |
|-----|---------|-------------------|---------|
| `[GOOD]` | 效果良好，可重复使用 | ✅ 是 | `[GOOD] CSV 批处理格式可防止重复记录` |
| `[BAD]` | 失败，应避免 | ✅ 是 | `[BAD] Bird CLI 被某些反自动化工具阻止` |
| `[NEUTRAL]` | 事实性信息、背景信息、状态 | ❌ 否 | `[NEUTRAL] 30天媒体计划中的第5天` |

### 编写规则
1. **新记录必须添加标签**。
2. **具体说明**：哪些方法有效/无效，以及原因。
3. **每个记录只使用一个标签**——选择最合适的分类。
4. **中立记录**：30天后自动归档，除非被提升为“好”或“坏”。

## 各类记录的存放位置

### MEMORY.md（分类后的学习经验）
记录内容不超过150行，仅包含“好”和“坏”的记录：

```markdown
## GOOD - What Works
- `[GOOD]` Cron jobs with CSV batching = zero duplicates
- `[GOOD]` Browser tool > CLI for X.com automation
- `[GOOD]` Moltbook "crypto" submolt for token posts

## BAD - What to Avoid  
- `[BAD]` Never use bird CLI for X (anti-bot blocks it)
- `[BAD]` Don't post identical content across platforms
```

### memory/YYYY-MM-DD.md（每日日志）
包含所有三类记录及其完整背景信息：

```markdown
# 2026-02-15

## [GOOD]
- Fixed duplicate posting with 4-batch CSV structure
- Created 10 cron jobs for complete automation

## [BAD]  
- Old CSV format caused content duplication (now deprecated)

## [NEUTRAL]
- Day 5 of 30-day media plan
- Posted $ZEN token shill at 07:00 batch
```

## 快速命令

### 搜索内存记录
```bash
# Search all memory files
~/.openclaw/skills/minimal-memory/scripts/search.sh "duplicate posting"

# Search only GOOD learnings
~/.openclaw/skills/minimal-memory/scripts/search.sh --good "CSV"

# Search only BAD learnings  
~/.openclaw/skills/minimal-memory/scripts/search.sh --bad "CLI"

# Recent entries only (last 7 days)
~/.openclaw/skills/minimal-memory/scripts/search.sh --recent "cron job"
```

### 每日内存记录
```bash
# Create today's memory file with template
~/.openclaw/skills/minimal-memory/scripts/daily.sh

# Add entry with auto-tagging
~/.openclaw/skills/minimal-memory/scripts/add.sh GOOD "Browser tool works better than CLI"
```

### 清理操作
```bash
# Review and migrate GOOD/BAD to MEMORY.md
~/.openclaw/skills/minimal-memory/scripts/cleanup.sh

# Archive old NEUTRAL entries (>30 days)
~/.openclaw/skills/minimal-memory/scripts/archive.sh
```

## 工作流程

### 编写内存记录时
1. **给记录添加标签**：判断其属于“好”、“坏”还是“中立”。
2. **将记录写入每日文件**，并在文件前加上标签前缀。
3. **每周审核**：将“好”或“坏”的记录提升到 MEMORY.md 中。
4. **30天后归档“中立”记录**。

### 搜索记录时
1. **使用搜索脚本**快速查找所有文件中的内容。
2. **先查看 MEMORY.md**以获取常见模式。
3. **如需具体背景信息，再查看每日文件**。
4. **优先查看最近的记录**（除非需要查找历史数据）。

### 每周清理
1. 阅读过去7天的每日记录。
2. 提取“好”和“坏”的记录。
3. 将它们添加到 MEMORY.md 的“好”和“坏”部分。
4. 删除重复项，合并相似的内容。
5. 确保 MEMORY.md 的内容不超过150行。

## 避免的错误做法
- **不要**跳过给记录添加标签——每个记录都需要分类。
- **不要**将“中立”记录保存在 MEMORY.md 中。
- **不要**让 MEMORY.md 的内容超过200行。
- **不要**永久保存“中立”记录（最长保存30天）。
- **不要**创建单独的主题文件——使用每日记录和搜索功能即可。

### 建议的做法
- **在询问用户“我们尝试过这个方法吗？”之前，先使用搜索功能**。
- **每周将“好”或“坏”的记录迁移至 MEMORY.md**。
- **详细描述失败或成功的细节**。
- **信任搜索脚本来获取相关背景信息**。

## 从旧系统迁移数据
如果 MEMORY.md 中有未标记的记录：
1. 读取整个 MEMORY.md 文件。
2. 为每条记录分类（“好”、“坏”或“中立”）。
3. 将“中立”记录移至相应的每日文件中。
4. 将“好”和“坏”的记录保留到带有标签的 MEMORY.md 中。
5. 未来的记录：务必先在每日文件中添加标签。