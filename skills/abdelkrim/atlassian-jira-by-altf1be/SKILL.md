---
name: atlassian-jira-by-altf1be
description: "Atlassian Jira Cloud CRUD技能：通过Jira REST API v3（支持电子邮件和API令牌认证）来管理问题、评论、附件、工作流转换以及使用JQL进行搜索。"
homepage: https://github.com/ALT-F1-OpenClaw/openclaw-skill-atlassian-jira
metadata:
  {"openclaw": {"emoji": "🎫", "requires": {"env": ["JIRA_HOST", "JIRA_EMAIL", "JIRA_API_TOKEN"]}, "primaryEnv": "JIRA_HOST"}}
---
# Jira Cloud 由 @altf1be 开发

通过 REST API 管理 Atlassian Jira Cloud 的问题、评论、附件以及工作流转换。

## 设置

1. 从 https://id.atlassian.com/manage-profile/security/api-tokens 获取 API 令牌。
2. 设置环境变量（或在 `{baseDir}` 目录下创建 `.env` 文件）：

```
JIRA_HOST=yourcompany.atlassian.net
JIRA_EMAIL=you@example.com
JIRA_API_TOKEN=your-api-token
JIRA_DEFAULT_PROJECT=PROJ
```

3. 安装依赖项：`cd {baseDir} && npm install`

## 命令

### 问题（Issues）

```bash
# List issues (optionally filter by project, status, assignee)
node {baseDir}/scripts/jira.mjs list --project PROJ --status "In Progress" --assignee "currentUser()"

# Create an issue
node {baseDir}/scripts/jira.mjs create --project PROJ --type Task --summary "Fix login bug" --description "Users can't log in" --priority High

# Read issue details
node {baseDir}/scripts/jira.mjs read --key PROJ-123

# Update issue fields
node {baseDir}/scripts/jira.mjs update --key PROJ-123 --summary "New title" --priority Low

# Delete issue (requires --confirm)
node {baseDir}/scripts/jira.mjs delete --key PROJ-123 --confirm

# Search with JQL
node {baseDir}/scripts/jira.mjs search --jql "project = PROJ AND status = Open ORDER BY created DESC"
```

### 评论（Comments）

```bash
# List comments on an issue
node {baseDir}/scripts/jira.mjs comment-list --key PROJ-123

# Add a comment
node {baseDir}/scripts/jira.mjs comment-add --key PROJ-123 --body "This is ready for review"

# Update a comment
node {baseDir}/scripts/jira.mjs comment-update --key PROJ-123 --comment-id 10001 --body "Updated comment"

# Delete a comment (requires --confirm)
node {baseDir}/scripts/jira.mjs comment-delete --key PROJ-123 --comment-id 10001 --confirm
```

### 附件（Attachments）

```bash
# List attachments on an issue
node {baseDir}/scripts/jira.mjs attachment-list --key PROJ-123

# Upload an attachment
node {baseDir}/scripts/jira.mjs attachment-add --key PROJ-123 --file ./screenshot.png

# Delete an attachment (requires --confirm)
node {baseDir}/scripts/jira.mjs attachment-delete --attachment-id 10001 --confirm
```

### 工作流转换（Workflow Transitions）

```bash
# List available transitions for an issue
node {baseDir}/scripts/jira.mjs transitions --key PROJ-123

# Move issue to a new status (by transition ID or name)
node {baseDir}/scripts/jira.mjs transition --key PROJ-123 --transition-id 31
node {baseDir}/scripts/jira.mjs transition --key PROJ-123 --transition-name "Done"
```

## 依赖项（Dependencies）

- `commander` — 命令行框架
- `dotenv` — 用于加载环境变量
- Node.js 内置的 `fetch` 函数（需要 Node.js 版本 >= 18）

## 安全性（Security）

- 采用电子邮件 + API 令牌进行身份验证（基于 Base64 编码的基本认证）
- 任何敏感信息或令牌都不会被输出到标准输出（stdout）。
- 所有删除操作都需要使用 `--confirm` 标志。
- 防止文件上传时的路径遍历攻击。
- 内置了基于指数退避策略的速率限制机制。
- 配置验证仅在命令执行时进行。

## 作者（Author）

Abdelkrim BOUJRAF — [ALT-F1 SRL](https://www.alt-f1.be)，布鲁塞尔 🇧🇪
X: [@altf1be](https://x.com/altf1be)