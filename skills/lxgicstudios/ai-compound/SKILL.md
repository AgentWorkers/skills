---
name: compound-engineering
description: 让你的AI代理能够自动学习和提升。它会回顾之前的会话内容，提取学习成果，更新内存文件，并随着时间的推移不断积累知识。通过设置每晚的自动复习机制，让你的代理变得越来越智能。
version: 1.0.0
author: lxgicstudios
keywords: compound, learning, memory, automation, agents, clawdbot, improvement, knowledge
---

# 复合工程（Compound Engineering）

让你的AI代理自动学习。从每次会话中提取学习成果，更新内存文件，并随着时间的推移不断积累知识。

**核心理念**：代理会回顾自己的工作，提取出其中的模式和经验教训，并据此更新自身的行为逻辑。明天的代理会比今天的更聪明。

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

### 被提取的内容

- **成功的方法**：那些屡试不爽的解决方案
- **问题点**：导致失败或出现问题的因素
- **用户偏好**：用户在使用过程中表现出的偏好
- **关键决策**：代理所做的决策及其背后的理由
- **待办事项**：需要记住的未完成任务

---

## Clawdbot集成

### 自动每小时更新内存数据

在你的 `HEARTBEAT.md` 文件中添加以下内容：

```markdown
# Hourly Memory Snapshot
Every hour, append a brief summary to memory/YYYY-MM-DD.md:
- What was accomplished
- Key decisions made
- Anything to remember
```

或者使用 `crontab` 来定时执行更新：

```bash
# Add to clawdbot config or crontab
0 * * * * clawdbot cron run compound-hourly
```

### 每晚自动审查任务

将以下 `crontab` 任务添加到 Clawdbot 中：

```json
{
  "id": "compound-nightly",
  "schedule": "30 22 * * *",
  "text": "Review all sessions from the last 24 hours. For each session, extract: 1) Key learnings and patterns, 2) Mistakes or gotchas to avoid, 3) User preferences discovered, 4) Unfinished items. Update MEMORY.md with a summary. Update memory/YYYY-MM-DD.md with details. Commit changes to git."
}
```

---

## 手动审查命令

当你需要手动触发审查时，可以使用以下命令：

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

### MEMORY.md（长期存储文件）

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

### memory/YYYY-MM-DD.md（每日存储文件）

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

为了更细致地记录学习过程，可以每小时生成一次快照：

```bash
# Creates memory/YYYY-MM-DD-HH.md every hour
*/60 * * * * echo "## $(date +%H):00 Snapshot" >> ~/clawd/memory/$(date +%Y-%m-%d).md
```

或者让代理通过检查时间来自动将数据追加到每日文件中。

---

## 复合学习的效果

**第1周**：代理掌握基本技能
**第2周**：代理记住你的使用习惯
**第4周**：代理能够预判你的需求
**第2个月**：代理成为你工作流程的专家

知识会不断积累，每一次会话都会让未来的学习更加高效。

---

## 设置脚本

### 每晚自动审查（macOS 使用 launchd）

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

### 每小时更新内存数据（使用 crontab）

```bash
# Add with: crontab -e
0 * * * * /opt/homebrew/bin/clawdbot cron run compound-hourly 2>&1 >> ~/clawd/logs/compound.log
```

---

## 最佳实践

1. **睡前进行审查**：在一天工作结束后运行夜间审查任务
2. **精选重要信息**：只提取有价值的学习内容，避免冗余信息
3. **定期清理**：每月从 `MEMORY.md` 文件中删除过时的内容
4. **使用 Git 进行版本控制**：确保内存文件始终处于受控状态
5. **相信复合学习的力量**：初期效果可能不明显，但长期来看效果显著

---

由 **LXGIC Studios** 开发 - [@lxgicstudios](https://x.com/lxgicstudios)

---

**开发团队信息**：
- GitHub: [github.com/lxgicstudios/ai-compound](https://github.com/lxgicstudios/ai-compound)
- Twitter: [@lxgicstudios](https://x.com/lxgicstudios)