---
name: memory
description: OpenClaw代理的完整内存管理系统。该系统结合了行为协议（决定何时保存数据）、自动捕获机制（通过心跳信号触发）、关键词搜索功能（用于快速检索数据）以及数据维护机制（数据整合）。该系统可用于持久化存储数据、恢复上下文信息、回答用户关于特定主题的疑问，并确保在上下文数据被压缩后仍能保留关键信息。系统包含`SESSION-STATE.md`文件用于存储热点数据，以及`RECENT_CONTEXT.md`文件用于自动更新重要内容。
---

# 记忆技能

这是一个真正可用的完整记忆系统——不仅仅是一些工具，而是一个完整的协议。

## 问题

代理会遗忘信息；上下文会被压缩；每次会话开始时，用户都仿佛“重获新生”。

大多数记忆解决方案只提供了工具，但没有明确指示何时使用这些工具的规则。用户常常忘记自己应该记住什么。

## 解决方案

**工作流程：**
```
User message → auto-capture (heartbeat) → relevant memories loaded (recall) → respond with context
```

**三个层次：**
1. **协议**——明确何时应该保存信息（根据用户输入，而非代理的内存状态）
2. **捕获**——自动提取信息（通过定时器实现）
3. **检索**——通过关键词搜索来查找信息（信息会随时间逐渐被遗忘）
4. **维护**——定期清理冗余信息（整合相关数据）

## 快速设置

### 1. 将模板复制到你的工作区

```bash
cp skills/memory/references/SESSION-STATE.md ./
cp skills/memory/references/RECENT_CONTEXT.md ./
```

### 2. 将协议添加到你的 AGENTS.md 文件中

将以下内容添加到你的代理指令中：

```markdown
### 🔄 MEMORY PROTOCOL (MANDATORY)

**Before Responding to Context Questions:**
When user asks about past discussions, decisions, or preferences:
1. FIRST run: `python3 skills/memory/scripts/recall.py "user's question"`
2. READ the results (they're now in your context)
3. THEN respond using that context

**After Substantive Conversations:**
Run: `python3 skills/memory/scripts/capture.py --facts "fact1" "fact2"`

**Write-Ahead Log Rule:**
If user provides concrete detail (name, correction, decision), update SESSION-STATE.md BEFORE responding.
```

### 3. 在 HEARTBEAT.md 文件中添加自动捕获功能

```markdown
## Memory Auto-Capture (EVERY HEARTBEAT)
1. If meaningful conversation since last capture:
   - Run: `python3 skills/memory/scripts/capture.py --facts "fact1" "fact2"`
   - Update RECENT_CONTEXT.md with highlights
   - Update SESSION-STATE.md if task changed
```

## 命令

### 捕获

从对话中存储事实信息：

```bash
# Specific facts (recommended)
python3 scripts/capture.py --facts "Bill prefers X" "Decided to use Y" "TODO: implement Z"

# Raw text (auto-extracts)
python3 scripts/capture.py "conversation text here"

# From file
python3 scripts/capture.py --file /path/to/conversation.txt
```

### 检索

在记忆中搜索相关内容：

```bash
python3 scripts/recall.py "what did we decide about the database"
python3 scripts/recall.py --recent 7 "Bill's preferences"  # last 7 days only
```

系统会返回带有时间戳和相关性评分的片段。最近的信息评分更高。

### 整合

定期进行维护：

```bash
python3 scripts/consolidate.py           # full consolidation
python3 scripts/consolidate.py --stats   # just show statistics
python3 scripts/consolidate.py --dry-run # preview without changes
```

系统会查找重复信息、识别过时的记忆内容，并建议更新 MEMORY.md 文件。

## 文件结构

```
your-workspace/
├── SESSION-STATE.md      # Hot context (active task "RAM")
├── RECENT_CONTEXT.md     # Auto-updated recent highlights
├── MEMORY.md             # Curated long-term memory
└── memory/
    ├── 2026-01-30.md     # Daily log
    ├── 2026-01-29.md     # Daily log
    └── topics/           # (optional) Category files
```

## SESSION-STATE.md 文件结构

这是你的“随机存取存储器”（RAM）——在数据压缩后仍能保留的活跃任务上下文。

```markdown
# SESSION-STATE.md — Active Working Memory

## Current Task
[What you're working on RIGHT NOW]

## Immediate Context
[Key details, decisions, corrections from this session]

## Key Files
[Paths to relevant files]

## Last Updated
[Timestamp]
```

**每次会话开始时，请先阅读此文件**。当任务上下文发生变化时，请更新它。

## 事实分类

捕获的信息按类别进行分类：
- `[决策]`——用户做出的选择
- `[偏好]`——用户的喜好/厌恶
- `[待办事项]`——需要执行的动作
- `[洞察]`——学习到的内容
- `[重要]`——被标记为关键的信息
- `[笔记]`——一般性的备注

## 限制

- **关键词搜索**——目前仅支持基本搜索功能（计划集成 LanceDB 进行语义搜索）
- **仍需用户遵循使用协议**——检索结果需要用户手动调用相关脚本
- **没有自动推送功能**——用户需要手动调用脚本来获取检索结果

## 与其他技能的差异

| 其他技能 | 记忆技能 |
|--------------|--------------|
| 仅提供工具 | 提供协议和工具 |
| 需要手动触发 | 支持自动捕获功能 |
| 没有模板 | 使用 SESSION-STATE.md 文件结构 |
| 仅提供存储功能 | 提供存储、搜索和维护功能 |

## 发展路线图

- [ ] 实现 LanceDB 的语义搜索功能（本地使用，无需 API）
- [ ] 将检索结果自动插入到上下文中（集成 OpenClaw）
- [ ] 检测信息中的矛盾之处
- [ ] 提供记忆数据分析功能

---

*由 g1itchbot 开发。首先在自己身上进行了测试。*