---
name: memory-reflect
description: "睡眠时间内存反思功能：回顾近期对话和日常笔记，提取有价值的见解，并将其巩固为长期记忆。该功能会在 cron 任务、心跳信号或明确请求的触发下启动，用于反思近期发生的活动。它以后台处理的形式运行，旨在逐步提升内存的使用效率和质量。"
---
# 记忆整理（Memory Reflect）

回顾近期活动，并将有价值的见解巩固到长期记忆中。

这一做法的灵感来源于“睡眠时计算”（sleep-time computing）的概念——即记忆的形成在活动间隙进行得最为有效，而非在活动进行期间。

## 运行时机

- **定时任务（Cron/Heartbeat）**：作为周期性后台任务来执行（建议频率：每天1-2次）
- **按需**：当用户需要整理、巩固或回顾近期记忆时
- **压缩后**：在上下文窗口压缩事件之后

## 处理流程

### 1. 收集近期资料

找出近期发生的变化，然后阅读相关文件：

```python
# Find recently modified notes — use json format for the complete list
# (text format truncates to ~5 items in the summary)
recent_activity(timeframe="2d", output_format="json")

# Read specific daily notes
read_note(identifier="memory/2026-02-27")
read_note(identifier="memory/2026-02-26")

# Check active tasks
search_notes(note_types=["task"], status="active")
```

### 2. 评估信息的重要性

对于每一条信息，需要判断：
- 这是否是一个会影响未来工作的**决策**？ → 保留
- 这是否是一个值得学习的**经验**或需要避免的**错误**？ → 保留
- 这是否是一个**工作偏好**或**工作风格的见解**？ → 保留
- 这是否是一个**人际关系**的细节（例如谁负责什么、联系方式）？ → 保留
- 这是否是**临时性的内容**（例如天气信息、心跳检测结果、常规任务）？ → 跳过
- 这是否已经记录在 `MEMORY.md` 或其他长期存储文件中？ → 跳过

### 3. 更新长期记忆

将整理后的见解按照 `MEMORY.md` 的现有结构写入其中：
- 添加新的章节或更新现有章节
- 使用简洁、客观的语言
- 包含日期以提供时间背景
- 删除或更新被新信息取代的过时条目

### 4. 记录整理过程

在今天的日常笔记中添加一条简短的记录：

```markdown
## Reflection (HH:MM)
- Reviewed: [list of files reviewed]
- Added to MEMORY.md: [brief summary of what was consolidated]
- Removed/updated: [anything cleaned up]
```

## 指导原则

- **有选择性**：目标是提炼精华，而非重复记录。`MEMORY.md` 应该是经过筛选的智慧结晶，而不是日常笔记的简单复制。
- **保持风格一致性**：如果该代理有个人特色或风格文件，整理后的内容应与其风格相符。
- **不要删除日常笔记**：它们是原始记录，整理内容只是从中提取有价值的部分，而非完全替代它们。
- **合并内容，而非重复添加**：如果 `MEMORY.md` 已经有关于某个主题的章节，应直接更新该章节，而不是添加重复条目。
- **标注不确定性**：如果某条信息看似重要但不确定，可以标注为“（需要确认）”而非直接跳过。
- **逐步重构**：如果 `MEMORY.md` 是按时间顺序排列的，可以在整理过程中将其重构为按主题分类的章节。经过筛选的知识比原始日志更有价值。
- **检查文件系统问题**：在收集资料时注意是否存在递归嵌套（如 `memory/memory/...`）、孤立文件或文件冗余等问题。