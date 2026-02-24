---
name: OpenCortex
homepage: https://github.com/JD2005L/opencortex
description: OpenClaw代理的自我优化内存架构：将默认的扁平化内存结构转变为一个结构化、能够自我维护的知识系统，该系统会随着时间的推移变得越来越智能。适用场景包括：(1) 设置新的OpenClaw实例；(2) 用户希望优化或整理内存管理；(3) 用户希望代理减少遗忘信息的情况；(4) 使用最佳实践重新启动代理。**不适用于**运行时的内存搜索查询（请使用内置的内存管理工具）。相关触发指令包括：`set up memory`、`organize yourself`、`stop forgetting`、`memory architecture`、`self-improving`、`cortex`、`bootstrap memory`、`memory optimization`。
metadata: {"openclaw":{"requires":{"bins":["grep","sed","find"],"optionalBins":["git","gpg","openssl","openclaw","secret-tool","keyctl"]},"env":{"CLAWD_WORKSPACE":{"description":"Workspace directory (defaults to cwd)","required":false},"CLAWD_TZ":{"description":"Timezone for cron scheduling (defaults to UTC)","required":false},"OPENCORTEX_VAULT_PASS":{"description":"Vault passphrase via env var. Prefer system keyring.","required":false,"sensitive":true}},"sensitiveFiles":[".secrets-map",".vault/.passphrase"],"networkAccess":"Optional git push only (off by default, user must enable during install)"}}
---
# OpenCortex — 自我提升的记忆架构

将一个普通的 OpenClaw 代理转变为一个能够每天积累知识的系统。

📦 [完整源代码在 GitHub 上](https://github.com/JD2005L/opencortex) — 可以查看代码、提交问题或参与贡献。

## 功能概述

1. **将记忆结构化**：将信息存储在特定用途的文件中，而不是以扁平化的形式保存。
2. **执行夜间维护**：将每日的工作成果转化为永久性的知识。
3. **进行每周汇总**：分析跨日的模式和趋势。
4. **建立行为准则**：通过夜间审计来确保良好的记忆管理习惯得到执行，包括工具文档的验证、决策的记录、子代理的汇报以及避免不必要的延迟。没有任何细节会被遗漏。
5. **生成用户的语音档案**：通过日常对话来构建用户的语音特征，用于自动代写内容。
6. **加密敏感数据**：使用 AES-256 加密算法进行存储，并在文档中仅保留密钥的引用；支持密钥轮换（`vault.sh rotate`），并在 `vault.sh set` 中验证密钥名称。
7. **提供安全的 Git 备份**：自动清理敏感信息。

## 安装步骤

**先决条件**（如果尚未安装，请分别安装以下软件）：
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

安装程序会询问是否需要启用某些功能（加密存储、语音分析、Git 备份等）。可以多次运行安装程序，程序会自动跳过已存在的功能。安装过程不涉及网络请求，仅会在本地创建文件并设置 cron 任务。

安装程序会完成以下操作：
- 创建文件结构（不会覆盖现有文件）。
- 设置 cron 任务（每日数据整理、每周汇总）。
- （可选）设置带有敏感信息清理功能的 Git 备份。

安装程序还会生成 `memory/VOICE.md` 文件，该文件记录了用户日常交流的特征。夜间整理过程会分析用户的对话内容，从而生成词汇库、语调模式和决策风格。这些信息可用于代表用户自动撰写内容（如社区帖子、电子邮件、社交媒体帖子），但不适用于日常对话。

安装完成后，请查看并自定义以下文件：
- `SOUL.md`：定义用户的个性和身份特征。
- `USER.md`：包含用户的个人信息。
- `MEMORY.md`：记录行为准则（根据需要添加或删除内容）。
- `.secrets-map`：用于存储用户的敏感信息，以便后续进行 Git 备份时的清理操作。

## 架构说明

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
  runbooks/      ← Step-by-step procedures (delegatable to sub-agents)
  archive/       ← Archived daily logs + weekly summaries
  YYYY-MM-DD.md  ← Today's working log (distilled nightly)
```

## 默认安装的行为准则

| 编号 | 名称 | 目的 |
| --- | --- |
| P1 | 首先委托任务 | 评估哪些任务可以委托给子代理，并确保自己随时待命处理。 |
| P2 | 一切记录在案 | 将决策和信息写入文件，而不是仅保存在脑海中。 |
| P3 | 外部操作前先确认 | 在发送电子邮件、发布公开内容或执行可能产生影响的操作前先确认。 |
| P4 | 积极创建工具 | 主动记录和使用工具；夜间审计会监督这一过程。 |
| P5 | 记录决策过程 | 详细记录决策及其背后的理由；夜间和每周审计会对此进行验证。 |
| P6 | 子代理汇报结果 | 委托的任务会反馈到每日日志中；未完成的任务会通过汇总机制进行处理。 |
| P7 | 记录失败情况 | 对失败和错误进行标记，并进行根本原因分析；夜间审计会确保这一点得到执行。 |
| P8 | 先查看工具文档 | 在将任务委托给用户之前，先查阅相关文档。 |


## 已安装的 cron 任务

| 时间 | 任务名称 | 功能描述 |
| --- | --- | --- |
| 每天凌晨 3 点（本地时间） | 数据整理 | 读取每日日志，将其整理到项目/工具/基础设施相关文件中，并进行审计。 |
| 每周周日凌晨 5 点 | 数据汇总 | 分析一周内的模式、重复出现的问题和未完成的任务；根据重复的操作自动生成操作手册。 |

这两个任务会使用一个共享的锁文件（`/tmp/opencortex-distill.lock`）来避免同时运行时发生冲突。

可以通过编辑 `openclaw cron list`，然后使用 `openclaw cron edit <id> --cron "..."` 来自定义任务时间。

如需手动更新 OpenCortex，可以使用 `clawhub update opencortex` 命令。

## Git 备份（可选）

如果启用了此功能，系统会执行以下操作：
- 创建 `scripts/git-backup.sh` 脚本：每 6 小时自动提交一次数据。
- 创建 `scripts/git-scrub-secrets.sh` 脚本：在提交前将敏感信息替换为占位符。
- 创建 `scripts/git-restore-secrets.sh` 脚本：推送后恢复敏感信息。
- 创建 `.secrets-map` 文件：将敏感信息映射到占位符（文件权限设置为 600，防止未经授权的访问）。

要将敏感信息添加到 `.secrets-map` 中，请使用以下格式：`actual_secret|{{PLACEHOLDER_NAME}}`。

每次推送之前，`git-backup.sh` 会检查文件中是否还包含原始的敏感信息。如果发现敏感信息，推送操作会被中止，并恢复原始数据，确保敏感信息不会被上传到远程仓库。

## 自定义功能

**添加新项目**：创建 `memory/projects/my-project.md` 文件，并将其添加到 `MEMORY.md` 的索引中。夜间整理过程会将相关的日志条目保存到该文件中。
**添加新行为准则**：将其添加到 `MEMORY.md` 的 `🔴 PRINCIPLES` 部分。内容应简短明了，最好是一句话的声明。
**添加操作手册**：创建 `memory/runbooks/my-procedure.md` 文件，其中包含详细的操作步骤。子代理可以直接参考这些手册。
**添加新工具**：在 `TOOLS.md` 中记录工具的详细信息，包括工具的用途、访问方式以及其功能描述，以便将来能够根据需求快速查找。

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

每天，这个代理都会变得更加知识丰富、组织更加有序。