---
name: compound-engineering
description: 让你的AI代理能够自动学习并不断改进。它会回顾之前的会话内容，提取学习成果，更新内存文件，并随着时间的推移积累知识。设置夜间自动复习机制，让代理的智能水平每天都在提升。
version: 1.0.0
author: lxgicstudios
keywords: compound, learning, memory, automation, agents, clawdbot, improvement, knowledge
---

# 复合学习机制（Compound Learning Mechanism）

让你的AI代理实现自主学习。从每次交互中提取学习成果，更新内存文件，并逐步积累知识。

**核心理念**：代理会自我回顾其行为，从中提取模式和经验教训，从而优化自身的行为策略。明天的代理会比今天的更智能。

---

## 快速入门

```bash
# Review last 24 hours and update memory
npx compound-engineering review

# Create hourly memory snapshot
npx compound-engineering snapshot

# Set up automated nightly review (cron)
npx compound-engineering setup-cron
```

---

## 工作原理

### 复合学习循环（Compound Learning Loop）

```
┌─────────────────────────────────────────┐
│           DAILY WORK                    │
│  Sessions, chats, tasks, decisions      │
└────────────────┬────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────┐
│        NIGHTLY REVIEW (10:30 PM)        │
│  • Scan all sessions from last 24h      │
│  • Extract learnings and patterns       │
│  • Update MEMORY.md and AGENTS.md       │
│  • Commit and push changes              │
└────────────────┬────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────┐
│        NEXT DAY                         │
│  Agent reads updated instructions       │
│  Benefits from yesterday's learnings    │
└─────────────────────────────────────────┘
```

### 被提取的信息包括：

- **有效策略**：屡试不爽的方法
- **问题点**：导致失败或问题的因素
- **用户偏好**：用户的使用习惯和偏好
- **关键决策**：代理做出的重要决策及其背后的思考过程
- **待办事项**：需要后续处理的任务

---

## Clawdbot集成

### 自动每小时更新内存数据

在`HEARTBEAT.md`文件中添加以下代码：

```markdown
# Hourly Memory Snapshot
Every hour, append a brief summary to memory/YYYY-MM-DD.md:
- What was accomplished
- Key decisions made
- Anything to remember
```

或者使用Cron任务来定时更新：

```bash
# Add to clawdbot config or crontab
0 * * * * clawdbot cron run compound-hourly
```

### 每晚自动审查

将以下Cron任务添加到Clawdbot中：

```json
{
  "id": "compound-nightly",
  "schedule": "30 22 * * *",
  "text": "Review all sessions from the last 24 hours. For each session, extract: 1) Key learnings and patterns, 2) Mistakes or gotchas to avoid, 3) User preferences discovered, 4) Unfinished items. Update MEMORY.md with a summary. Update memory/YYYY-MM-DD.md with details. Commit changes to git."
}
```

---

## 手动审查命令

如果你想手动触发审查过程，可以使用以下命令：

```
Review the last 24 hours of work. Extract:

1. **Patterns that worked** - approaches to repeat
2. **Gotchas encountered** - things to avoid
3. **Preferences learned** - user likes/dislikes
4. **Key decisions** - and their reasoning
5. **Open items** - unfinished work

Update:
- MEMORY.md with significant long-term learnings
- memory/YYYY-MM-DD.md with today's details
- AGENTS.md if workflow changes needed

Commit changes with message "compound: daily review YYYY-MM-DD"
```

---

## 内存文件结构

- **MEMORY.md**（长期存储文件）
```markdown
# Long-Term Memory

## Patterns That Work
- When doing X, always Y first
- User prefers Z approach for...

## Gotchas to Avoid  
- Don't do X without checking Y
- API Z has rate limit of...

## User Preferences
- Prefers concise responses
- Timezone: PST
- ...

## Project Context
- Main repo at /path/to/project
- Deploy process is...
```

- **memory/YYYY-MM-DD.md**（每日存储文件）
```markdown
# 2026-01-28 (Tuesday)

## Sessions
- 09:00 - Built security audit tool
- 14:00 - Published 40 skills to MoltHub

## Decisions
- Chose to batch publish in parallel (5 sub-agents)
- Security tool covers 6 check categories

## Learnings
- ClawdHub publish can timeout, retry with new version
- npm publish hangs sometimes, may need to retry

## Open Items
- [ ] Finish remaining MoltHub uploads
- [ ] Set up analytics tracker
```

---

## 每小时生成快照

为了更细致地记录学习过程，可以每小时生成一次内存快照：

```bash
# Creates memory/YYYY-MM-DD-HH.md every hour
*/60 * * * * echo "## $(date +%H):00 Snapshot" >> ~/clawd/memory/$(date +%Y-%m-%d).md
```

或者让代理通过检测时间来自动将数据追加到每日文件中。

---

## 复合学习的效果

- **第1周**：代理掌握基本功能
- **第2周**：代理记住你的使用习惯
- **第4周**：代理能够预判你的需求
- **第2个月**：代理成为你工作流程的专家

知识会不断积累，每次交互都会让后续的学习更加高效。

---

## 设置脚本

### 每晚自动审查（macOS使用launchd）

```xml
<!-- ~/Library/LaunchAgents/com.clawdbot.compound-review.plist -->
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "...">
<plist version="1.0">
<dict>
  <key>Label</key>
  <string>com.clawdbot.compound-review</string>
  <key>ProgramArguments</key>
  <array>
    <string>/opt/homebrew/bin/clawdbot</string>
    <string>cron</string>
    <string>run</string>
    <string>compound-nightly</string>
  </array>
  <key>StartCalendarInterval</key>
  <dict>
    <key>Hour</key>
    <integer>22</integer>
    <key>Minute</key>
    <integer>30</integer>
  </dict>
</dict>
</plist>
```

### 每小时更新内存数据（使用crontab）

```bash
# Add with: crontab -e
0 * * * * /opt/homebrew/bin/clawdbot cron run compound-hourly 2>&1 >> ~/clawd/logs/compound.log
```

---

## 最佳实践：

1. **睡前进行审查**：在一天工作结束后运行夜间审查任务
2. **精选重要信息**：只提取有价值的学习内容，避免无关信息
3. **定期清理**：每月删除`MEMORY.md`文件中的过时数据
4. **使用Git进行版本控制**：确保内存文件的安全性和可追溯性
5. **耐心等待效果**：虽然初期效果可能不明显，但随着时间推移效果会显著提升

---

由 **LXGIC Studios** 开发 - [@lxgicstudios](https://x.com/lxgicstudios)