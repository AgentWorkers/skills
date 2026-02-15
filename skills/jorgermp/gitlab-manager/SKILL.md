---
name: gitlab-manager
description: 通过 API 管理 GitLab 仓库、合并请求（Merge Requests）和问题（Issues）。可用于创建仓库、审阅合并请求中的代码或跟踪问题等任务。
---

# GitLab Manager

此技能允许通过API与GitLab.com进行交互。

## 前提条件

- **GITLAB_TOKEN**：必须在环境中设置一个具有`api`权限范围的个人访问令牌（Personal Access Token）。

## 使用方法

使用提供的Node.js脚本来与GitLab进行交互。

### 脚本位置
`scripts/gitlab_api.js`

### 命令

#### 1. 创建仓库
在GitLab中创建一个新的项目。
```bash
./scripts/gitlab_api.js create_repo "<name>" "<description>" "<visibility>"
# Visibility: private (default), public, internal
```

#### 2. 列出合并请求（Merge Requests）
列出特定项目的合并请求（MRs）。
```bash
./scripts/gitlab_api.js list_mrs "<project_path>" "[state]"
# Project path: e.g., "jorgermp/my-repo" (will be URL encoded automatically)
# State: opened (default), closed, merged, all
```

#### 3. 评论合并请求
为特定的合并请求添加评论。这有助于代码审查。
```bash
./scripts/gitlab_api.js comment_mr "<project_path>" <mr_iid> "<comment_body>"
```

#### 4. 创建问题（Issue）
创建一个新的问题。
```bash
./scripts/gitlab_api.js create_issue "<project_path>" "<title>" "<description>"
```

## 示例

**创建一个私有仓库：**
```bash
GITLAB_TOKEN=... ./scripts/gitlab_api.js create_repo "new-tool" "A cool new tool" "private"
```

**审查合并请求：**
```bash
# First list to find ID
GITLAB_TOKEN=... ./scripts/gitlab_api.js list_mrs "jorgermp/my-tool" "opened"
# Then comment
GITLAB_TOKEN=... ./scripts/gitlab_api.js comment_mr "jorgermp/my-tool" 1 "Great work, but check indentation."
```