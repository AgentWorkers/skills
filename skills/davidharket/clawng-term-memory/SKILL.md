---
name: clawng-term-memory
description: 让你的 OpenClaw 代理具备可移植性和持久性。使用 Git 对 `SOUL.md`、`MEMORY.md` 以及所有核心知识文件进行版本控制，并自动将更改推送到 GitHub——这样你的代理的身份信息、内存设置以及运行规则都会被备份，你可以在任何机器上通过克隆仓库来恢复这些数据。每当核心知识文件被修改时，务必执行提交（commit）并推送更改。此外，在需要查看文件的历史记录、比较文件差异（diff）或回滚更改时，也请使用 Git 功能。通过 Git 的历史记录，你可以观察到你的辅助工具（assistant）是如何逐步发展的。
---
# clawng-term-memory

让您的 OpenClaw 代理具备 **可移植性和持久性**。对代理的配置、内存内容以及运行规则的任何修改都会被提交到 Git 中，并推送到一个私有的 GitHub 仓库中——这样您就可以通过克隆该仓库，在任何机器上恢复代理的精确配置。

通过 Git 的历史记录，您可以观察到代理的演变过程：了解它何时学会了新技能、哪些决策发生了变化，以及它一周前的状态。这就像是对代理“思维”的版本控制。

## 设置

1. 在您的工作区中初始化一个 Git 仓库（如果尚未完成的话）：
```bash
cd ~/.openclaw/workspace
git init
git config user.name "YourAgent"
git config user.email "agent@example.com"
```

2. 创建一个私有的 GitHub 仓库，然后使用 SSH（推荐）或 HTTPS 将其添加为远程仓库：
**SSH（推荐——无需暴露令牌）：**
```bash
git remote add origin git@github.com:<user>/<repo>.git
```

**使用凭证存储的 HTTPS（URL 中不包含令牌）：**
```bash
git remote add origin https://github.com/<user>/<repo>.git
git config credential.helper store
# Git will prompt for credentials on first push and store them securely
```

3. 提交初始更改：
```bash
git branch -M main && git push -u origin main
```

4. 如果工作区路径非标准配置，请进行相应设置（可选）：
```bash
export CLAWNG_WORKSPACE=/your/custom/workspace/path
```
如果未设置，默认工作区路径为 `$HOME/.openclaw/workspace`。

## 多代理/多机器支持

每台机器都有自己的分支（格式为 `agent/<hostname>`），并且每个分支都对应一个 `MEMORY.md` 文件。每天，一个 AI 合成任务会读取所有代理的内存数据，并自动将结果写入到 `main` 分支下的 `SHARED_MEMORY.md` 文件中——整个过程完全自动化，无需人工干预。

```
agent/vps-1 → MEMORY.md ──┐
agent/vps-2 → MEMORY.md ──┤ Claude synthesizes → SHARED_MEMORY.md → main
agent/vps-3 → MEMORY.md ──┘
```

- `commit.sh` 脚本会自动将更改推送到 `agent/<hostname>` 分支（该分支会在首次提交时创建）。
- `merge.sh` 脚本会收集所有代理的 `MEMORY.md` 文件，供 AI 合成任务使用。
- AI 合成代理会在每晚将数据去重并合并到 `main` 分支下的 `SHARED_MEMORY.md` 文件中。
- 所有代理都会从 `main` 分支读取 `SHARED_MEMORY.md` 文件，以确保数据的一致性。

该系统可以扩展到 10 台以上的机器，且不会出现冲突。

## 被跟踪的文件
- `SOUL.md`、`MEMORY.md`、`USER.md`、`TOOLS.md`、`IDENTITY.md`、`AGENTS.md`、`HEARTBEAT.md`
- `memory/*.md`（每日笔记）
- `skills/`（已安装的技能）

## 提交并推送更改

在修改任何核心文件后，请运行以下命令：
```bash
bash /path/to/workspace/skills/clawng-term-memory/scripts/commit.sh "short description of what changed"
```

示例：
- `"MEMORY.md: 添加了新的客户端上下文信息"`
- `"SOUL.md: 更新了运行规则"`
- `"memory/2026-02-21.md: 日志记录"`
- `"HEARTBEAT.md: 调整了检查频率"`

## 每日 AI 合成（每天运行一次）

`merge.sh` 脚本会收集所有代理的 `MEMORY.md` 文件，然后由 AI 代理将这些文件合并到 `main` 分支下的 `SHARED_MEMORY.md` 文件中。该过程会自动去重并解决文件冲突，同时保留所有唯一的信息。

您可以将此任务设置为 OpenClaw 的 Cron 作业（默认在本地时间 02:00 运行）。

## 查看历史记录

```bash
cd /path/to/workspace && git log --oneline --graph memory/ MEMORY.md SOUL.md
```

## 比较文件差异

```bash
cd /path/to/workspace && git diff HEAD~1 MEMORY.md
```

## 将文件恢复到之前的版本

```bash
cd /path/to/workspace && git checkout HEAD~1 -- MEMORY.md
bash skills/clawng-term-memory/scripts/commit.sh "revert MEMORY.md to previous version"
```

## 自动提交规则

**在修改任何核心配置文件后，务必运行提交脚本。** 即：编写代码 → 提交更改 → 推送到仓库。每次修改都必须遵循这一流程，没有任何例外。