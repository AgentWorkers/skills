---
name: epragma-redmine-issue
description: 您可以通过 REST API 从任何 Redmine 服务器中读取问题信息，该 API 支持配置 URL 和凭据。当您需要获取单个问题、列出/筛选问题或检查问题字段以进行变更规划时，可以使用此功能；同时，该工具还支持通过环境变量将配置信息部署到不同的 Redmine 实例中。
user-invocable: true
---
# ePragma Redmine Issue

通过 REST API 查看 Redmine 问题。

## 配置

使用此技能需要配置 `REDMINE_URL` 和 `REDMINE_API_KEY`。

### 使用 OpenClaw CLI 进行配置

运行以下命令来配置此技能：

```bash
# Set your Redmine URL
openclaw skills config epragma-redmine-issue set REDMINE_URL https://your-redmine-server.com

# Set your API key (generate from Redmine My Account page)
openclaw skills config epragma-redmine-issue set REDMINE_API_KEY your-api-key-here
```

### 获取 API 密钥

1. 登录到您的 Redmine 服务器。
2. 转到“我的账户”。
3. 点击“API 访问密钥”旁边的“显示”。
4. 复制密钥。

## 获取一个问题

```bash
node {baseDir}/scripts/issues.mjs get --id 123
```

## 列出问题

```bash
node {baseDir}/scripts/issues.mjs list
node {baseDir}/scripts/issues.mjs list --project-id my-project --status-id open --limit 20 --offset 0
node {baseDir}/scripts/issues.mjs list --assigned-to-id me --sort "updated_on:desc"
node {baseDir}/scripts/issues.mjs list --project my-project
```

## 列出项目

```bash
node {baseDir}/scripts/issues.mjs projects
```

## 列出问题状态

```bash
node {baseDir}/scripts/issues.mjs statuses
```

## 更新一个问题

```bash
node {baseDir}/scripts/issues.mjs update --id 123 --status-id 2 --notes "this is ok"
node {baseDir}/scripts/issues.mjs update --id 123 --assigned-to-id 6 --priority-id 3
node {baseDir}/scripts/issues.mjs update --id 123 --done-ratio 50 --notes "done 50%"
```

## 为问题添加评论

```bash
node {baseDir}/scripts/issues.mjs comment --id 123 --notes "This is a comment"
```

## 创建新问题

```bash
# Required: --project-id (or project name), --subject
# Optional: --description, --tracker-id, --priority-id, --assigned-to-id, --status-id, --start-date, --due-date, --done-ratio, --estimated-hours

node {baseDir}/scripts/issues.mjs create --project-id 1 --subject "New issue title"
node {baseDir}/scripts/issues.mjs create --project-id epragma --subject "Bug report" --description "Details here" --priority-id 4
```

## 记录时间

```bash
# List time entries (filters: --issue-id, --project-id, --user-id, --from, --to, --spent-on)
node {baseDir}/scripts/issues.mjs time-list
node {baseDir}/scripts/issues.mjs time-list --issue-id 232
node {baseDir}/scripts/issues.mjs time-list --project-id 1 --from 2026-01-01 --to 2026-01-31

# Add time entry (required: --issue-id OR --project-id, --hours; optional: --activity-id, --spent-on, --comments)
node {baseDir}/scripts/issues.mjs time-add --issue-id 232 --hours 2 --activity-id 9 --comments "Work done"
node {baseDir}/scripts/issues.mjs time-add --project-id 1 --hours 1.5 --activity-id 8

# List available activities
node {baseDir}/scripts/issues.mjs time-activities
```

## 注意：

- URL 和认证信息是专为跨环境部署设计的变量。
- API 响应以 JSON 格式返回。
- 对于自动化操作，建议使用 `REDMINE_API_KEY` 而不是用户名/密码。