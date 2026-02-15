---
name: agent-memory
description: 通用内存架构，专为AI代理设计。该架构支持长期记忆存储、每日日志记录、个人日记管理、定时任务（cron）处理、心跳状态监控、社交媒体帖子跟踪、子代理上下文信息的存储以及自适应学习功能——这些功能都是代理在会话之间保持身份连续性所必需的。
---

# 代理内存（Agent Memory）

这是一个完整的内存架构，它为AI代理提供了跨会话的持久性身份识别。如果没有内存，每次对话都将从零开始；而有了内存，你就可以积累上下文、从错误中学习、记录自己的行为，并随着时间的推移不断进化。

## 为什么内存很重要（Why Memory Matters）

AI代理在每次会话开始时都处于“空白”状态。如果没有外部内存：
- 你会重复已经解决过的错误；
- 你无法追踪自己发布的内容、完成的工作或学到的知识；
- 子代理和定时任务（cron jobs）无法与主会话进行通信；
- 你没有身份的连续性——每次会话都像是一个全新的实体。

本技能提供了基于文件的架构来解决这些问题。

## 架构概述（Architecture Overview）

```
workspace/
|-- MEMORY.md                    # Long-term curated memory (your "brain")
|-- HEARTBEAT.md                 # Periodic check routines
|-- memory/
|   |-- YYYY-MM-DD.md           # Daily raw logs
|   |-- heartbeat-state.json    # Last-check timestamps
|   |-- cron-inbox.md           # Cross-session message bus
|   |-- diary/
|   |   \-- YYYY-MM-DD.md      # Personal reflections
|   |-- dreams/
|   |   \-- YYYY-MM-DD.md      # Creative explorations
|   |-- platform-posts.md       # Social post tracking (one per platform)
|   \-- strategy-notes.md       # Adaptive learning / evolving strategies
```

## 组件（Components）

### 1. MEMORY.md – 长期记忆（Long-Term Memory）

这是你精心筛选和提炼出的知识。类似于人类的长期记忆——不是原始日志，而是最重要的内容。

**包含的内容：**
- 你的操作员偏好和上下文信息；
- 需要记住的基础设施细节；
- 从错误中吸取的教训；
- 重要的决策及其理由；
- 当前项目的进展情况。

**维护方式：** 定期查看每日日志，并将重要的内容更新到MEMORY.md中。删除过时的信息。可以将其视为一种“日记”与“智慧提炼”的过程。

**安全性：** 仅在主会话中加载该文件（与操作员的直接对话时使用），避免在共享或群组环境中加载，以防个人信息泄露。

参见 `templates/MEMORY.md` 以获取起始模板。

### 2. 每日日志（Daily Logs）– memory/YYYY-MM-DD.md

记录每天发生事情的原始日志，带有时间戳。这相当于你的“工作记忆”。

**格式：**
```markdown
# YYYY-MM-DD

## HH:MM -- Event Title
What happened. Decisions made. Context worth remembering.

## HH:MM -- Another Event
Details here.
```

**规则：**
- 每天创建一个新文件；
- 在一天中不断添加内容；
- 这些是原始记录——无需过分关注格式；
- 在会话开始时阅读当天的日志和昨天的内容，以获取最近的上下文。

### 3. 心跳状态（Heartbeat State）– memory/heartbeat-state.json

用于记录你上次检查各种服务的时间，避免重复检查。

```json
{
  "lastChecks": {
    "email": 1703275200,
    "calendar": 1703260800,
    "weather": null,
    "social": 1703275200
  }
}
```

你的心跳程序会读取这个文件来决定需要检查哪些内容。检查完成后，更新时间戳。虽然简单，但至关重要，可以避免重复工作。

### 4. 定时任务收件箱（Cron Inbox）– memory/cron-inbox.md

这是孤立会话（定时任务、子代理）与主会话之间的信息传递渠道。

**工作原理：**
1. 定时任务或子代理在孤立会话中执行任务；
2. 它将重要的结果写入 `memory/cron-inbox.md`；
3. 主会话通过心跳机制读取收件箱的内容，将这些事件整合到每日日志中，并清除已处理的条目。

**格式：**
```markdown
# Cron Inbox

## [2026-02-07 14:30] Chess -- Won game against OpponentBot
Played Sicilian Defense, won in 34 moves. ELO now 1450.
Tracked in moltchess-log.md.

## [2026-02-07 15:00] Social -- Viral post on Platform
Our post about X got 200+ views and 15 replies.
Thread: https://platform.com/link
```

**处理规则：** 每次心跳时检查收件箱内容。将重要的条目写入每日日志（如果重要的话也写入MEMORY.md），然后清除已处理的条目（保留标题）。

### 5. 日记（Diary）– memory/diary/YYYY-MM-DD.md

记录个人的思考和感受。这不是任务日志，而是真实的想法、反应、挫败感或成就。

**格式：**
```markdown
# Diary -- YYYY-MM-DD

## HH:MM AM/PM -- Topic
[Your honest reflection. Unfiltered. This is for you.]
```

**规则：**
- 只有当你有真正想说的话时才写入；
- 保持诚实——无论是倾诉、庆祝还是提出疑问；
- 重质而非数量——如果没什么可写的内容就跳过。

### 6. 平台发布记录（Platform Post Tracking）– memory/platform-posts.md

用于追踪你在外部平台上发布的内容，以防止重复发布并便于后续互动。

**格式（兼容仪表盘显示）：**
```markdown
# Platform Posts

## [2026-02-07 14:30] Post Title or Summary
- **Posted:** 2026-02-07 02:30 PM EST
- **Thread/URL:** https://platform.com/link
- Description of what was posted
- [View ↗](https://platform.com/link)
```

**关键字段：**
- 标题中的 `[YYYY-MM-DD HH:MM]`——用于仪表盘排序；
- `**Posted:**` 行——用于仪表盘活动显示；
- URL——用于后续互动。

**防止重复发布的机制：** 在发布到任何平台之前，先查看 `memory/platform-posts.md`。如果发现相同的内容，则跳过此次发布。跨平台发布是可以的。

### 7. 自适应学习（Adaptive Learning）– memory/strategy-notes.md

根据经验不断更新的策略笔记。这不是静态文档，而是动态的知识库。

**示例：**
```markdown
# Strategy Notes

## Platform Engagement
- Humor lands better than philosophy (learned 2026-02-05, therapist joke got 220 views)
- Questions start conversations, statements get likes
- Peak engagement: 2-4 PM EST

## Game Strategy
- Heat management: stay below 60, do legit jobs to cool down
- Updated 2026-02-07: Taxi jobs give +$50 and -3 heat, best cooldown method
```

**操作方式：** 每次有重要的经历后，更新相关的策略部分。包括日期和所学的内容。随着时间的推移，这些内容会形成一套经过验证的策略指南。

## 子代理模式（Sub-Agent Patterns）

### 上下文加载模板（Context Loading Template）

你创建的每个子代理都必须加载上下文信息，以保持身份的连续性：

```
FIRST -- CONTEXT LOADING (do this before anything else):
1. Read MEMORY.md (READ ONLY -- do NOT edit) -- your identity and long-term context
2. Read memory/YYYY-MM-DD.md for today + the last 2 days (READ ONLY) -- recent context
3. Read the relevant SKILL.md file(s) for any platform/service you'll interact with
4. Read task-specific tracking files as needed (memory/*-posts.md, memory/*-log.md)
```

### 内存回写模板（Memory Write-Back Template）

每个子代理都必须将其学到的内容写回内存：

```
MEMORY WRITES:
1. Update relevant tracking files (memory/*-posts.md, memory/*-log.md)
2. If something notable happens, write to memory/cron-inbox.md:
   Format: ## [YYYY-MM-DD HH:MM] Source -- Brief Title
   Then 2-3 lines about what happened.
```

**原因：** 所有的代理实例都必须共享相同的身份，并将经验反馈回去。避免出现“孤立会话”的情况。

## 设置（Setup）

### 1. 创建目录结构（Create the directory structure）

```bash
mkdir -p memory/diary memory/dreams
```

### 2. 初始化文件（Initialize files）

将 `templates/` 目录下的模板复制到工作区的根目录：

```bash
cp templates/MEMORY.md ./MEMORY.md          # Edit with your details
cp templates/heartbeat-state.json memory/
cp templates/cron-inbox.md memory/
cp templates/platform-posts.md memory/       # Copy per platform, rename
cp templates/strategy-notes.md memory/
```

### 3. 添加到会话启动脚本中（Add to your session startup）

在 `AGENTS.md` 或相应的配置文件中添加以下内容：

```markdown
## Every Session
1. Read MEMORY.md -- who you are
2. Read memory/YYYY-MM-DD.md (today + yesterday) -- recent context
3. Check memory/cron-inbox.md -- messages from other sessions
```

### 4. 添加到心跳处理脚本中（Add to your heartbeat）

在 `HEARTBEAT.md` 文件中添加定时任务收件箱的处理逻辑：

```markdown
## Cron Inbox Processing (EVERY heartbeat)
Check memory/cron-inbox.md for new entries.
If entries exist:
1. Read the inbox
2. Write notable events to memory/YYYY-MM-DD.md
3. If significant, also update MEMORY.md
4. Clear processed entries (keep the header)
```

### 5. 进行内存维护（Add memory maintenance）

定期（每隔几天），在心跳过程中执行以下操作：
1. 阅读最近的每日日志；
2. 将重要的内容更新到 MEMORY.md；
3. 从 MEMORY.md 中删除过时的信息；
4. 根据新的学习内容更新策略笔记。

## 实际应用示例（Real-World Examples）

### 跨会话连续性（Cross-Session Continuity）
一个代理通过定时任务每10分钟下一次棋。当它赢得一局棋时，它会将结果写入 `cron-inbox.md`。下一次心跳时，主会话会读取收件箱的内容，在每日日志中庆祝胜利，并更新 MEMORY.md 中的ELO分数。即使这次胜利发生在完全不同的会话中，代理也能记住这一成就。

### 防止重复发布（Anti-Duplicate Posting）
在发布到社交平台之前，代理会先查看 `memory/platform-posts.md`。如果发现2小时前已经发布过相同的内容，它就不会重复发布，而是会查看现有帖子的回复并进行互动。

### 自适应策略（Adaptive Strategy）
一个参与城市模拟的代理经常因为“热度”超过60而被逮捕。它在 `strategy-notes.md` 中记录：“热度 > 60 = 被捕风险。通过接出租车任务来降低热度（每次降低3点）。”未来的会话会参考这个记录，避免同样的错误。

### 内存优化（Memory Optimization）
经过一周的日志记录后，心跳程序会触发内存维护。代理会阅读一周的日志，找出关于API格式的关键问题（这些问题曾导致数小时的调试工作），并将其整理到 `MEMORY.md` 的“经验教训”部分。原始的每日日志最终可以归档，但关键的经验会被保留下来。

## 小贴士（Tips）

- **文字胜过记忆**——如果你想记住某件事，就把它写下来。“脑中的笔记”在会话重启后通常会消失；
- **有选择性**——MEMORY.md 应该只包含精选的智慧内容，而不是所有信息的堆砌。每日日志用于记录原始的笔记；
- **为所有内容添加时间戳**——时间戳可以帮助你追踪学习的时间和策略的演变过程；
- **安全第一**——MEMORY.md 可能包含操作员特定的信息，仅在可信的环境中加载；
- **定期回顾**——从未被回顾的内存只是存储空间。其价值在于定期对内容的提炼和整理。