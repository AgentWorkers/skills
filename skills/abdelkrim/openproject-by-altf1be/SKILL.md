---
name: openproject-by-altf1be
description: "**OpenProject CRUD技能**  
通过OpenProject API v3（支持API令牌认证）来管理工作包、项目、时间记录、评论、附件、状态等信息。该技能适用于云部署和自托管的环境。"
homepage: https://github.com/ALT-F1-OpenClaw/openclaw-skill-openproject
metadata:
  {"openclaw": {"emoji": "📊", "requires": {"env": ["OP_HOST", "OP_API_TOKEN"]}, "primaryEnv": "OP_HOST"}}
---
# OpenProject 由 @altf1be 开发

通过 API v3 管理 OpenProject 的工作包、项目、时间记录、评论、附件以及工作流程的转换。支持云托管和自托管实例。

## 设置

1. 登录到您的 OpenProject 实例。
2. 转到 **我的账户 → 访问令牌 → + 添加**。
3. 创建一个 API 令牌并复制它。
4. 设置环境变量（或在 `{baseDir}` 目录下创建一个 `.env` 文件）：

```
OP_HOST=https://projects.xflowdata.com
OP_API_TOKEN=your-api-token
OP_DEFAULT_PROJECT=my-project
```

5. 安装依赖项：`cd {baseDir} && npm install`

## 命令

### 工作包

```bash
# List work packages (with optional filters)
node {baseDir}/scripts/openproject.mjs wp-list --project my-project --status open --assignee me

# Create a work package
node {baseDir}/scripts/openproject.mjs wp-create --project my-project --type Task --subject "Fix login bug" --description "Users can't log in"

# Read work package details
node {baseDir}/scripts/openproject.mjs wp-read --id 42

# Update a work package
node {baseDir}/scripts/openproject.mjs wp-update --id 42 --subject "New title" --priority High

# Delete a work package (requires --confirm)
node {baseDir}/scripts/openproject.mjs wp-delete --id 42 --confirm
```

### 项目

```bash
# List all projects
node {baseDir}/scripts/openproject.mjs project-list

# Read project details
node {baseDir}/scripts/openproject.mjs project-read --id my-project

# Create a project
node {baseDir}/scripts/openproject.mjs project-create --name "My Project" --identifier my-project
```

### 评论（活动）

```bash
# List comments on a work package
node {baseDir}/scripts/openproject.mjs comment-list --wp-id 42

# Add a comment
node {baseDir}/scripts/openproject.mjs comment-add --wp-id 42 --body "Ready for review"
```

### 附件

```bash
# List attachments on a work package
node {baseDir}/scripts/openproject.mjs attachment-list --wp-id 42

# Upload an attachment
node {baseDir}/scripts/openproject.mjs attachment-add --wp-id 42 --file ./screenshot.png

# Delete an attachment (requires --confirm)
node {baseDir}/scripts/openproject.mjs attachment-delete --id 10 --confirm
```

### 时间记录

```bash
# List time entries
node {baseDir}/scripts/openproject.mjs time-list --project my-project

# Log time
node {baseDir}/scripts/openproject.mjs time-create --wp-id 42 --hours 2.5 --comment "Code review" --activity-id 1

# Update time entry
node {baseDir}/scripts/openproject.mjs time-update --id 5 --hours 3 --comment "Updated"

# Delete time entry (requires --confirm)
node {baseDir}/scripts/openproject.mjs time-delete --id 5 --confirm
```

### 状态与转换

```bash
# List all statuses
node {baseDir}/scripts/openproject.mjs status-list

# Update work package status
node {baseDir}/scripts/openproject.mjs wp-update --id 42 --status "In progress"
```

### 参考数据

```bash
# List work package types
node {baseDir}/scripts/openproject.mjs type-list

# List priorities
node {baseDir}/scripts/openproject.mjs priority-list

# List project members
node {baseDir}/scripts/openproject.mjs member-list --project my-project

# List versions/milestones
node {baseDir}/scripts/openproject.mjs version-list --project my-project

# List categories
node {baseDir}/scripts/openproject.mjs category-list --project my-project
```

## 安全性

- 使用 API 令牌进行身份验证（基本认证，`apikey` 作为用户名）。
- 不会将任何敏感信息或令牌输出到标准输出（stdout）。
- 所有删除操作都需要明确使用 `--confirm` 标志。
- 防止文件上传时的路径遍历攻击。
- 内置的速率限制机制，采用指数级退避重试策略。
- 配置验证仅在命令执行时进行。

## 依赖项

- `commander` — 命令行框架
- `dotenv` — 用于加载环境变量
- Node.js 内置的 `fetch` 模块（需要 Node.js 版本 >= 18）

## 作者

Abdelkrim BOUJRAF — [ALT-F1 SRL](https://www.alt-f1.be)，布鲁塞尔 🇧🇪 🇲🇦
X: [@altf1be](https://x.com/altf1be)