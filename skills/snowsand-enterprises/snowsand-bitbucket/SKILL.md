---
name: snowsand-bitbucket
version: 1.0.0
description: 通过 REST API 与 Bitbucket Cloud 进行交互。该 API 可用于仓库管理（如列出、查看、创建仓库、添加评论、批准合并请求等）、分支管理、提交历史记录查询、管道状态查询以及工作区/团队相关信息的查询。它会在 Bitbucket 的各种操作（如合并请求审核、分支管理、管道检查）或任何 Atlassian Bitbucket Cloud 任务触发时自动执行。
---
# Bitbucket Cloud 集成

本文档介绍了如何使用 Bitbucket Cloud 的 REST API v2 进行仓库管理、拉取请求（Pull Requests）、分支（Branches）、提交（Commits）以及流水线（Pipelines）的操作。

## 认证

Bitbucket Cloud 支持使用应用密码（App Password）进行认证。所需的环境变量包括：

- `BITBUCKET_WORKSPACE`：默认的工作区名称（例如：`myteam`）
- `BITBUCKET_USERNAME`：Bitbucket 用户名（而非电子邮件地址）
- `BITBUCKET_APP_PASSWORD`：从 [https://bitbucket.org/account/settings/app-passwords/](https://bitbucket.org/account/settings/app-passwords/) 获取的应用密码

请创建一个具有以下权限的应用密码：
- **仓库（Repositories）**：读写权限（用于仓库操作）
- **拉取请求（Pull Requests）**：读写权限（用于处理拉取请求）
- **流水线（Pipelines）**：读取权限（用于查看流水线状态）
- **账户（Account）**：读取权限（用于获取用户信息）

测试连接：
```bash
curl -s -u "$BITBUCKET_USERNAME:$BITBUCKET_APP_PASSWORD" \
  "https://api.bitbucket.org/2.0/user" | jq .
```

## 快速参考

所有操作均通过 `scripts/bitbucket.py` 脚本完成：

| 操作            | 命令                                      |
|-----------------|-----------------------------------------|
| **仓库（Repositories）**    |                                           |
| 列出仓库         | `bitbucket.py repos`                        |
| 查看仓库         | `bitbucket.py repo my-repo`                        |
| 创建仓库         | `bitbucket.py create-repo my-new-repo --private`                |
| **拉取请求（Pull Requests）** |                                           |
| 列出拉取请求       | `bitbucket.py prs my-repo`                        |
| 查看拉取请求       | `bitbucket.py pr my-repo 42`                        |
| 创建拉取请求       | `bitbucket.py create-pr my-repo --title "Feature" --source feature-branch`     |
| 评论拉取请求       | `bitbucket.py pr-comment my-repo 42 "LGTM!"`                |
| 审核拉取请求       | `bitbucket.py approve my-repo 42`                        |
| 合并拉取请求       | `bitbucket.py merge my-repo 42`                        |
| 拒绝拉取请求       | `bitbucket.py decline my-repo 42`                        |
| **分支（Branches）**    |                                           |
| 列出分支         | `bitbucket.py branches my-repo`                        |
| 查看分支         | `bitbucket.py branch my-repo main`                        |
| 创建分支         | `bitbucket.py create-branch my-repo feature-x --from main`                |
| 删除分支         | `bitbucket.py delete-branch my-repo old-feature`                |
| **提交（Commits）**    |                                           |
| 列出提交记录       | `bitbucket.py commits my-repo`                        |
| 查看提交记录       | `bitbucket.py commit my-repo abc123`                        |
| **流水线（Pipelines）**    |                                           |
| 列出流水线         | `bitbucket.py pipelines my-repo`                        |
| 查看流水线         | `bitbucket.py pipeline my-repo {uuid}`                        |
| 流水线步骤         | `bitbucket.py pipeline-steps my-repo {uuid}`                        |
| **工作区（Workspaces）** |                                           |
| 列出工作区         | `bitbucket.py workspaces`                        |
| 查看工作区成员       | `bitbucket.py members`                        |
| 查看当前用户       | `bitbucket.py me`                          |

## 常见工作流程

### 仓库管理
```bash
# List all repositories in workspace
bitbucket.py repos

# List with pagination
bitbucket.py repos --page 2 --pagelen 25

# View specific repository details
bitbucket.py repo my-repo

# Create a new private repository
bitbucket.py create-repo my-new-repo --private --description "Project description"

# Create public repository with specific project
bitbucket.py create-repo my-public-repo --project PROJ
```

### 拉取请求工作流程
```bash
# List open pull requests
bitbucket.py prs my-repo

# List all PRs (including merged/declined)
bitbucket.py prs my-repo --state all

# View PR details
bitbucket.py pr my-repo 42

# Create a pull request
bitbucket.py create-pr my-repo \
  --title "Add new feature" \
  --source feature-branch \
  --destination main \
  --description "This PR adds..."

# Add a comment
bitbucket.py pr-comment my-repo 42 "Looks good, just one question..."

# Approve the PR
bitbucket.py approve my-repo 42

# Unapprove (remove approval)
bitbucket.py unapprove my-repo 42

# Request changes
bitbucket.py request-changes my-repo 42

# Merge with default strategy
bitbucket.py merge my-repo 42

# Merge with specific strategy
bitbucket.py merge my-repo 42 --strategy squash

# Decline a PR
bitbucket.py decline my-repo 42
```

### 分支操作
```bash
# List all branches
bitbucket.py branches my-repo

# View branch details
bitbucket.py branch my-repo feature-x

# Create branch from main
bitbucket.py create-branch my-repo feature-y --from main

# Create branch from specific commit
bitbucket.py create-branch my-repo hotfix-1 --from abc123def

# Delete a branch (cannot delete main branch)
bitbucket.py delete-branch my-repo old-feature
```

### 提交历史记录
```bash
# List recent commits (default branch)
bitbucket.py commits my-repo

# Commits on specific branch
bitbucket.py commits my-repo --branch feature-x

# Limit results
bitbucket.py commits my-repo --pagelen 10

# View specific commit
bitbucket.py commit my-repo abc123def456
```

### 流水线状态
```bash
# List recent pipelines
bitbucket.py pipelines my-repo

# Filter by status
bitbucket.py pipelines my-repo --status SUCCESSFUL
bitbucket.py pipelines my-repo --status FAILED

# View pipeline details
bitbucket.py pipeline my-repo '{pipeline-uuid}'

# View pipeline steps
bitbucket.py pipeline-steps my-repo '{pipeline-uuid}'

# Trigger a pipeline
bitbucket.py run-pipeline my-repo --branch main
```

### 工作区和用户信息
```bash
# List accessible workspaces
bitbucket.py workspaces

# List workspace members
bitbucket.py members

# Get current user info
bitbucket.py me
```

## 合并策略

在合并拉取请求时，可使用的策略包括：

| 策略            | 描述                                      |
|-----------------|-----------------------------------------|
| `merge_commit`      | 创建合并提交（默认策略）                        |
| `squash`         | 将所有提交合并为一个提交                         |
| `fast_forward`      | 如果可能，直接合并（快速合并）                        |

## 流水线状态

| 状态            | 描述                                      |
|-----------------|-----------------------------------------|
| `PENDING`        | 等待启动                                  |
| `IN_PROGRESS`      | 正在运行                                  |
| `SUCCESSFUL`      | 合并成功                                |
| `FAILED`        | 合并失败                                  |
| `STOPPED`        | 被手动停止                                |

## 错误处理

常见错误：
- **401 Unauthorized**：请检查 `BITBUCKET_USERNAME` 和 `BITBUCKET_APP_PASSWORD` 是否正确。
- **403 Forbidden**：应用密码没有所需的权限。
- **404 Not Found**：仓库、拉取请求或分支不存在。
- **400 Bad Request**：参数或分支名称无效。

## 原生 API 访问

对于脚本未涵盖的操作，可以直接使用 Bitbucket Cloud 的原生 REST API 进行操作：
```bash
# GET request
curl -s -u "$BITBUCKET_USERNAME:$BITBUCKET_APP_PASSWORD" \
  "https://api.bitbucket.org/2.0/repositories/$BITBUCKET_WORKSPACE/my-repo" | jq .

# POST request
curl -s -X POST -u "$BITBUCKET_USERNAME:$BITBUCKET_APP_PASSWORD" \
  -H "Content-Type: application/json" \
  -d '{"content": {"raw": "Comment text"}}' \
  "https://api.bitbucket.org/2.0/repositories/$BITBUCKET_WORKSPACE/my-repo/pullrequests/42/comments" | jq .
```

API 文档：[https://developer.atlassian.com/cloud/bitbucket/rest/](https://developer.atlassian.com/cloud/bitbucket/rest/)