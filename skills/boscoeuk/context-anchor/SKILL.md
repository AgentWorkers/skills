---
name: context-anchor
version: 1.0.0
description: 通过扫描内存文件来恢复从上下文压缩中丢失的信息，并从你上次停止的地方继续执行。适用于在系统重新启动后、压缩操作完成后，或者当你不清楚自己之前在做什么的时候使用。
---

# **上下文恢复技能（Context Recovery Skill）**

该技能通过扫描内存文件并生成一份“当前工作状态”简报，帮助代理在系统压缩后快速恢复工作上下文。

## **技能存在的必要性**

虽然系统压缩可以节省内存空间，但文件本身仍然保留。然而，在系统恢复后，代理需要：
1. 了解自己之前正在处理的任务；
2. 查看之前所做的决策；
3. 找出尚未完成或存在问题的任务；
4. 快速熟悉当前的工作环境。

该技能能够自动化完成这些恢复工作。

---

## **快速入门**

```bash
# Full briefing (default)
./scripts/anchor.sh

# Just show current task
./scripts/anchor.sh --task

# Just show active context files
./scripts/anchor.sh --active

# Just show recent decisions
./scripts/anchor.sh --decisions

# Show open loops / questions
./scripts/anchor.sh --loops

# Scan specific number of days back
./scripts/anchor.sh --days 3
```

---

## **扫描范围**

| 扫描路径        | 扫描内容                          |
|---------------|-----------------------------------|
| `memory/current-task.md` | 当前任务的状态、阻碍因素及后续步骤         |
| `memory/YYYY-MM-DD.md` | 最近的每日日志（默认为过去2天的日志）         |
| `context/active/*.md` | 正在进行的任务文件                     |
| 日志文件        | 包含决策内容的日志行（如 "Decision:", "Decided:", "✅"）       |
| 日志文件        | 存在问题的日志行（如 "?", "TODO:", "Blocker:", "Need to"）       |

---

## **输出格式**

脚本会生成一份结构化的简报，内容如下：

```
═══════════════════════════════════════════════════════════
                    CONTEXT ANCHOR
              Where You Left Off
═══════════════════════════════════════════════════════════

📋 CURRENT TASK
───────────────────────────────────────────────────────────
[Contents of memory/current-task.md or "No current task set"]

📂 ACTIVE CONTEXT FILES
───────────────────────────────────────────────────────────
• context/active/project-name.md (updated 2h ago)
  └─ First line preview...

🎯 RECENT DECISIONS (last 2 days)
───────────────────────────────────────────────────────────
[2026-01-30] Decision: Use Cloudflare Pages for hosting
[2026-01-30] ✅ Completed email capture setup

❓ OPEN LOOPS
───────────────────────────────────────────────────────────
[2026-01-30] Need to enable SFTP on NAS
[2026-01-30] TODO: Create Product Hunt account

═══════════════════════════════════════════════════════════
```

---

## **与 AGENTS.md 的集成**

您可以将该技能添加到您的“每次会话”（Every Session）自动化流程中：
```markdown
## Every Session

Before doing anything else:
1. Run `./skills/context-anchor/scripts/anchor.sh` for orientation
2. Read `SOUL.md` — this is who you are
3. Read `USER.md` — this is who you're helping
...
```

或者，在您对工作内容感到困惑时手动使用该技能。

---

## **自定义设置**

### 更改工作区根目录

```bash
WORKSPACE=/path/to/workspace ./scripts/anchor.sh
```

### 更改扫描日志的日期范围

```bash
./scripts/anchor.sh --days 5  # Scan 5 days back
```

---

## **无依赖项**

该技能完全基于 Bash 脚本实现，仅依赖以下工具：
- `find`, `grep`, `head`, `tail`, `date`, `stat`
- 适用于 macOS 和 Linux 系统
- 不需要任何外部工具

---

## **使用场景**

- **会话开始时**：快速了解当前的工作进度；
- **系统压缩后**：恢复丢失的工作上下文；
- **感到困惑时**：帮助您回忆之前在做什么；
- **任务交接时**：向其他代理展示工作进展；
- **日常回顾**：查看之前所做的决策。