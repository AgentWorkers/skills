---
name: OpenCortex
homepage: https://github.com/JD2005L/opencortex
description: OpenClaw代理的自我优化内存架构：采用结构化内存文件、每晚的数据处理、每周的整合以及严格遵循的设计原则，确保代理能够不断积累知识而非遗忘。系统支持可选的指标跟踪功能，包括增长图表和综合评分，以评估其长期效果。所有敏感功能（如语音分析、基础设施自动收集、Git推送等）默认处于关闭状态，需要通过环境变量或标志明确启用。安装过程安全可靠：无需网络调用，所有脚本均采用可审计的Bash编写，并且Cron任务仅在工作区内执行。适用场景包括：（1）设置新的OpenClaw实例；（2）用户希望优化或整理内存管理；（3）用户希望代理减少遗忘现象；（4）使用最佳实践重新配置代理。**不适用于**运行时的内存搜索查询（请使用内置的内存管理工具）。相关触发命令包括：`set up memory`、`organize yourself`、`stop forgetting`、`memory architecture`、`self-improving`、`cortex`、`bootstrap memory`、`memory optimization`。
metadata: {"openclaw":{"requires":{"bins":["grep","sed","find"],"optionalBins":["git","gpg","openssl","openclaw","secret-tool","keyctl","file"]},"env":{"CLAWD_WORKSPACE":{"description":"Workspace directory (defaults to cwd)","required":false},"CLAWD_TZ":{"description":"Timezone for cron scheduling (defaults to UTC)","required":false},"OPENCORTEX_VAULT_PASS":{"description":"Vault passphrase via env var. Prefer system keyring.","required":false,"sensitive":true},"OPENCORTEX_VOICE_PROFILE":{"description":"Set to 1 to enable voice profiling in the nightly distillation cron. Off by default.","required":false,"sensitive":false},"OPENCORTEX_INFRA_COLLECT":{"description":"Set to 1 to enable infrastructure auto-collection in the nightly distillation cron. Off by default.","required":false,"sensitive":false},"OPENCORTEX_SCRUB_ALL":{"description":"Set to 1 to scrub all tracked files (not just known text types) during git backup. Off by default.","required":false,"sensitive":false},"OPENCORTEX_ALLOW_FILE_PASSPHRASE":{"description":"Set to 1 to allow vault passphrase stored in a file (.vault/.passphrase). Off by default; prefer system keyring.","required":false,"sensitive":false}},"sensitiveFiles":[".secrets-map",".vault/.passphrase"],"networkAccess":"Optional git push only (off by default, requires --push flag)"}}
---
# OpenCortex — 自我提升的记忆管理架构

将默认的 OpenClaw 代理转变为一个能够持续积累知识的系统。

📦 [完整源代码请访问 GitHub](https://github.com/JD2005L/opencortex) — 可以查看代码、提交问题或参与开发。

## 功能概述

1. **将记忆数据** 分类存储到不同用途的文件中，而非采用单一的扁平化存储结构。
2. **夜间执行维护任务**，将每日的工作成果转化为永久性知识。
3. **每周进行数据整合**，识别出跨日重复出现的模式或问题。
4. **建立一系列记忆管理原则**，并通过夜间审计来确保这些原则得到执行（包括工具文档的验证、决策的记录、子代理的工作总结、故障分析等），确保没有任何信息被遗漏。
5. **根据日常对话生成用户的“语音档案”**，用于辅助自动写作（需启用 `OPENCORTEX_VOICE_PROFILE=1`）。
6. **使用 AES-256 加密技术** 对敏感数据进行加密存储，文档中仅保留密钥的引用；支持密钥轮换（`vault.sh rotate`）并验证密钥名称（`vault.sh set`）。
7. **提供安全的 Git 备份功能**，并对敏感数据进行清洗处理（敏感数据仅在隔离的副本中进行修改）。
8. **跟踪系统的发展情况**（可选）—— 提供每日指标快照、综合评分以及 ASCII 格式的增长图表。

## 安装流程

**安装前提**（如果尚未安装，请分别安装以下软件）：
- [OpenClaw](https://github.com/openclaw/openclaw) 2026.2.x+  
- [ClawHub CLI](https://clawhub.com)

```bash
# 1. Download the skill from your OpenClaw workspace directory
cd ~/clawd    # or wherever your workspace is
clawhub install opencortex

# 2. Run the installer FROM YOUR WORKSPACE DIRECTORY (not from inside the skill folder)
bash skills/opencortex/scripts/install.sh

# Optional: preview what would be created without changing anything
bash skills/opencortex/scripts/install.sh --dry-run
```

安装程序会询问是否需要启用某些可选功能（如加密存储、语音档案生成、系统数据收集、Git 备份等）。可以多次运行安装程序，系统会自动跳过已存在的功能。安装过程不涉及网络请求，仅会在本地创建文件并设置 cron 任务。

```bash
# 3. Verify everything is working (read-only — checks files and cron jobs, changes nothing)
bash skills/opencortex/scripts/verify.sh
```

你还可以通过命令询问 OpenClaw 代理：“OpenCortex 是否正在运行？” 该代理能够执行相应的验证并返回结果。

安装完成后，请查看并自定义以下文件：
- `SOUL.md`：用于设置个人风格和身份信息。
- `USER.md`：包含关于你的个人信息。
- `MEMORY.md`：用于定义记忆管理原则（根据需要添加或删除内容）。
- `.secrets-map`：用于存储需要加密的敏感数据。

## 更新流程

```bash
# 1. Download the latest version (run from workspace root)
clawhub install opencortex --force

# 2. Re-run the installer — it detects your existing install and offers to update
bash skills/opencortex/scripts/install.sh
```

安装程序会检测你的当前系统版本，并提供三种选择：更新（推荐）、完全重新安装或取消安装。更新过程不会破坏现有数据，只会添加缺失的内容、更新 cron 任务，并提供新的可选功能，而不会覆盖你自定义的设置。

## 系统架构

```
SOUL.md          ← Identity, personality, boundaries
AGENTS.md        ← Operating protocol, delegation rules
MEMORY.md        ← Principles + memory index (< 3KB, loaded every session)
TOOLS.md         ← Tool shed: APIs, scripts, and access methods with abilities descriptions
INFRA.md         ← Infrastructure atlas: hosts, IPs, services, network
USER.md          ← Human's preferences, projects, communication style
BOOTSTRAP.md     ← First-run checklist for new sessions

memory/
  projects/      ← One file per project (distilled, not raw)
  contacts/      ← One file per person/org (role, context, preferences)
  workflows/     ← One file per workflow/pipeline (services, steps, issues)
  runbooks/      ← Step-by-step procedures (delegatable to sub-agents)
  preferences.md ← Cross-cutting user preferences by category
  archive/       ← Archived daily logs + weekly summaries
  YYYY-MM-DD.md  ← Today's working log (distilled nightly)
```

## 默认安装的原则

| 编号 | 名称 | 功能 |
|---|------|---------|
| P1 | 首先委派任务 | 评估哪些任务适合委托给子代理处理；确保任务始终有明确的负责人。 |
| P2 | 将内容记录下来 | 将重要信息写入文件，而非仅保存在脑海中。 |
| P3 | 在执行外部操作前先确认 | 在发送邮件、公开发布内容或执行可能造成影响的操作前先进行确认。 |
| P4 | 文档化工具和工作流程 | 记录使用的工具和工作流程，并通过夜间审计来确保这些信息得到维护。 |
| P5 | 记录决策和偏好设置 | 记录用户的决策和偏好设置，并通过夜间和每周的审计来监督执行情况。 |
| P6 | 子代理工作反馈 | 将子代理的工作结果反馈到日志中；对于未完成的任务，系统会自动进行整理。 |
| P7 | 记录故障信息 | 对故障和修正措施进行标记，并通过夜间审计来分析根本原因。 |
| P8 | 先查看文档再行动 | 在将任务委托给用户之前，先查阅 `TOOLS.md`、`INFRA.md` 和 `MEMORY.md` 中的相关信息；确保决策的合理性。 |

## 自动执行的 cron 任务

| 时间 | 名称 | 功能 |
|------|------|-------------|
| 每天凌晨 3 点（本地时间） | 数据整合 | 读取每日日志，将其整理到项目/工具/基础设施相关的文件中，然后进行审计、优化并归档。 |
| 每周周日凌晨 5 点 | 数据整合与分析 | 分析一周内的模式、重复出现的问题以及未完成的任务，并自动生成操作手册。 |

这两个任务会共享一个锁文件 `/tmp/opencortex-distill.lock`，以防止在每日和每周的运行过程中发生冲突。你可以通过 `openclaw cron list` 查看并编辑 cron 任务的配置，使用 `openclaw cron edit <id> --cron "..."` 命令进行修改。

## Git 备份（可选）

如果安装时启用了此功能，系统会：
- 创建 `scripts/git-backup.sh` 脚本：每 6 小时自动执行一次备份，将敏感数据清洗后存储在隔离的临时副本中（工作区的文件不会被修改）。
- 在 `.secrets-map` 文件中存储敏感数据的映射关系（使用 `git ignored` 权限进行保护）。

在每次推送代码之前，`git-backup.sh` 会检查备份副本中是否还包含原始的敏感数据。如果发现未清洗的敏感数据，备份过程会中止，以防止数据泄露。

## 自定义功能

- **添加新项目**：创建 `memory/projects/my-project.md` 文件，并将其添加到 `MEMORY.md` 的索引中。
- **添加联系人**：创建 `memory/contacts/name.md` 文件。系统会根据对话内容自动生成联系人信息。
- **添加工作流程**：创建 `memory/workflows/my-pipeline.md` 文件。系统会根据描述自动创建相应的工作流程。
- **添加偏好设置**：将设置添加到 `memory/preferences.md` 的相应分类中。系统会从对话中自动捕获这些设置。
- **添加记忆管理原则**：将原则内容添加到 `MEMORY.md` 的 `🔴 PRINCIPLES` 部分。请保持内容简短。
- **添加操作手册**：创建 `memory/runbooks/my-procedure.md` 文件。子代理可以直接参考这些手册来执行任务。
- **添加新工具**：在 `TOOLS.md` 中记录工具的详细信息（包括用途、访问方式以及目标导向的能力描述），以便将来能够快速查找相关内容。

## 系统的自我提升机制

```
Daily work → daily log
  → nightly distill → routes to project/tools/infra/principles files
                     → optimization pass (dedup, prune stale, condense)
  → weekly synthesis → patterns, recurring problems, unfinished threads → auto-creates runbooks from repeated procedures → `memory/runbooks/`
Sub-agent work → debrief (P6) → daily log → same pipeline
Decisions → captured with reasoning (P5) → never re-asked
New tools → documented with abilities (P4) → findable by intent
```

每天，OpenCortex 代理都会变得更加“聪明”且组织更加有序。