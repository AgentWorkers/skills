---
name: openclaw-github-sync
description: 将 OpenClaw 代理的非敏感数据（选定的内存内容、MD 文件、笔记以及自定义技能）保存在一个单独的 Git 仓库中，并对其进行版本控制，以便远程审查或进行微调。在设置或使用基于 Git 的工作流程时，可以利用这个仓库来导出工作区的上下文、提交更改（可能需要分多次提交），并按照预定时间表（例如每晚）将更改推送到远程仓库，从而避免泄露任何敏感信息。
homepage: https://github.com/bradvin/openclaw-github-sync
metadata: {"openclaw":{"emoji":"🔄","homepage":"https://github.com/bradvin/openclaw-github-sync","requires":{"bins":["git","rsync","python3"],"env":["SYNC_REMOTE"]}}}
---
# OpenClaw Git 同步

我们维护一个独立的 Git 仓库，其中存放了 OpenClaw 工作空间中经过筛选、不包含敏感信息的文件（如记忆记录、技能信息、配置文件等），以便相关人员可以远程审查和修改这些内容。

这一设置较为保守：系统默认只允许导出那些被明确允许导出的文件。

## 信任边界

同步仓库是一个重要的信任边界。所有从远程仓库拉取的文件都可能包含潜在的安全风险，因此必须谨慎对待：

- 拉取操作必须由人工执行，且仅应在明确请求的情况下进行。
- 拉取操作可能会覆盖工作空间中的文件，包括技能信息、Markdown 文档以及用户配置文件。
- 恶意或不安全的更改可能会影响代理程序的行为、提示信息以及工具的使用方式。
- 请使用由您控制的私有仓库，并确保只有具备最低权限的用户才能访问该仓库；在每次拉取之前，必须经过人工审核。
- 每次请求拉取操作时，都必须及时通知相关人员；切勿通过定时任务（如 cron 作业）自动执行拉取操作。

## 关键规则：

- **默认情况下，绝不要同步任何敏感信息。** 只同步那些被导出清单中明确允许导出的文件。
- 如果可能的话，建议使用 `memory/public/` 目录下的“净化后的”记忆记录文件（需用户主动选择），而不是原始的 `memory/*.md` 文件。
- 确保同步仓库与主工作空间仓库分开管理。
- 使用由您控制的私有仓库，并确保只有具备最低权限的用户才能访问该仓库；在每次拉取之前，必须经过人工审核。
- 拉取操作必须由人工执行，切勿自动化 `pull.sh` 脚本；只有在明确请求的情况下才执行拉取操作。

## 文件与目录结构：

- 工作空间目录：`$HOME/.openclaw/workspace`
- 同步仓库（导出目标）：选择一个目录，例如 `$HOME/.openclaw/workspace/openclaw-sync-repo`
- 导出清单文件：`references/export-manifest.txt`

## 先决条件：

- 必需工具：`git`、`rsync`、`python3`
- 需要配置的环境变量：`SYNC_REMOTE`（设置在 `references/.env` 中）
- 必需的访问权限：对私有同步仓库具有 SSH/身份验证访问权限
- 可选工具：`gh`（仅用于 `scripts/create_private_repo.sh` 脚本）、`jq`（有助于更好地处理批量提交操作）

## 设置步骤：

1. 复制示例环境配置文件：
   `cp references/.env.example references/.env`
2. 根据您的环境实际情况编辑 `references/.env` 文件。
3. 至少将 `SYNC_REMOTE` 设置为您控制的私有仓库的 SSH 地址。

```bash
SYNC_REMOTE="git@github.com:YOUR_ORG/YOUR_REPO.git"
```

## 工作流程：

### 1) 创建/连接私有同步仓库（GitHub）

使用 `scripts/create_private_repo.sh`（或等效的 `gh repo create` 命令）在机器人账户下创建一个私有仓库。

### 2) 执行一次性同步

运行 `scripts/sync.sh` 脚本，传入以下参数：
- `SYNC_REMOTE`（远程仓库的 SSH 地址，例如 `git@github.com:YOUR_ORG/YOUR_REPO.git`）
- `SYNC_REPO_DIR`（本地同步仓库的路径）

该脚本会执行以下操作：
- 从远程仓库拉取最新版本的数据（如果存在的话）
- 将被允许导出的文件导入同步仓库
- 如果有多个文件组发生了变化，会为每个文件组创建单独的提交记录
- 将更改推送到远程仓库

### 3) 每晚自动同步

配置一个夜间运行的 OpenClaw 定时任务（`agentTurn`），仅执行同步操作（`scripts/sync.sh`），并报告同步结果（成功或失败）。
切勿自动执行 `pull.sh` 或 `context.sh pull` 脚本；拉取操作必须由人工发起。

## 相关资源：

- `scripts/sync.sh`：负责文件的导出、分组提交以及推送操作
- `scripts/create_private_repo.sh`：用于通过 `gh` 命令创建私有 GitHub 仓库
- `references/export-manifest.txt`：列出了可导出的文件路径
- `references/groups.json`：定义了文件分组的规则