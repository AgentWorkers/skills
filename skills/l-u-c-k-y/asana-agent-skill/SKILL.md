---
name: asana
description: "通过个人访问令牌（Personal Access Token, PAT），您可以管理 Asana 中的任务、项目、简报、状态更新、自定义字段、依赖关系、附件、事件以及时间线。"
homepage: https://developers.asana.com/docs/personal-access-token
user-invocable: true
metadata: {"openclaw":{"requires":{"env":["ASANA_PAT"]},"primaryEnv":"ASANA_PAT","homepage":"https://developers.asana.com/docs/personal-access-token"}}
---

# Asana

该技能提供了一个不依赖任何外部库的 Node.js 命令行工具（CLI），它使用 **个人访问令牌（Personal Access Token, PAT）** 来调用 Asana 的 REST API（v1）。

- 脚本文件：`{baseDir}/scripts/asana.mjs`
- 认证方式：`ASANA_PAT`（推荐）或 `ASANA_TOKEN`
- 输出格式：**仅限 JSON**（标准输出），适用于代理程序和自动化任务

## 设置

1. 在您的 Asana 账户中创建一个个人访问令牌（使用开发者控制台（Developer Console）并非必需）。
2. 将该令牌设置为 OpenClaw/Clawdbot 的环境变量 `ASANA_PAT`。

### 常见的令牌注入方式

- **Shell 环境变量（本地测试）**：
  `export ASANA_PAT="..."`

- **OpenClaw 配置**（推荐）：将令牌设置为 `skills.entries.asana.apiKey`（或 `env.ASANA_PAT`），这样该密钥仅在代理程序运行时被使用。

### 通过 OpenClaw CLI 进行配置（推荐）

这是设置令牌的最安全方式，因为它可以将敏感信息隐藏起来，避免显示在命令行提示或历史记录中。

**推荐配置方式（将 `apiKey` 更改为 `ASANA_PAT`）：**

```json
{
  "skills": {
    "entries": {
      "asana": {
        "apiKey": "ASANA_PAT"
      }
    }
  }
}
```

`skills.entries.asana.apiKey` 是一个便利字段：对于那些声明了 `metadata.openclaw.primaryEnv` 的技能，OpenClaw 会将该 API 密钥注入到代理程序运行的环境变量中（本技能的主要环境变量是 `ASANA_PAT`）。

**另一种方式（通过环境变量设置）：**

```json
{
  "skills": {
    "entries": {
      "asana": {
        "env": {
          "apiKey": "ASANA_PAT"
        }
      }
    }
  }
}
```

**如何查看已存储的令牌：**

```json
{
  "skills": {
    "entries": {
      "asana": {
        "env": {
          "apiKey": "ASANA_PAT"
        }
      }
    }
  }
}
```

**如何删除已存储的令牌：**

```json
{
  "skills": {
    "entries": {
      "asana": {
        "env": {
          "apiKey": ""
        }
      }
    }
  }
}
```

#### 注意：沙箱环境

当任务在沙箱环境中运行时，技能进程会在 Docker 中执行，因此不会继承主机环境。在这种情况下，`skills.entries.*.env/apiKey` 仅适用于主机环境下的运行。

可以通过以下方式设置 Docker 环境变量：
- `agents.defaults.sandbox.docker.env`（或针对每个代理程序设置 `agents.list[].sandbox.docker.env`）
- 或将环境变量直接嵌入到沙箱镜像中

## 初始操作（用于测试和了解功能）

- 查看用户信息：
  `node {baseDir}/scripts/asana.mjs me`

- 列出工作空间：
  `node {baseDir}/scripts/asana.mjs workspaces`

- （推荐）设置默认工作空间：
  `node {baseDir}/scripts/asana.mjs set-default-workspace --workspace <workspace_gid>`

## ID 解析

当用户提供名称（项目/任务/用户）时，可以使用以下方法将其解析为对应的 GID：
- `typeahead --workspace <gid> --resource_type project|task|user --query "..."`（快速且推荐）
- `projects --workspace <gid> --all`（列出所有项目）
- `users --workspace <gid> --all`（列出所有用户）

如果存在多个匹配项，请避免猜测正确的 GID。

## 核心功能：任务管理

### 列出分配给用户的任务（提升个人工作效率）

```bash
node {baseDir}/scripts/asana.mjs tasks-assigned --assignee me --workspace <workspace_gid> --all
```

### 列出项目中的任务

```bash
node {baseDir}/scripts/asana.mjs tasks-in-project --project <project_gid> --all
```

### 任务搜索（高级搜索 API）

推荐使用 `search-tasks` 这个原生 API，因为它支持多种过滤条件，比使用自定义的辅助搜索命令更高效。

示例：在项目中搜索任务：
```bash
node {baseDir}/scripts/asana.mjs search-tasks --workspace <gid> --project <project_gid> --text "..."
```

常用过滤条件：
- `--assignee me|<gid|email>`（对应 `assignee.any`）
- `--completed true|false`
- `--created_at.after <iso>` / `--modified_at.after <iso>`
- `--due_on.before YYYY-MM-DD` / `--due_at.before <iso>`
- `--is Blocked true|false` / `--isblocking true|false`

### 创建/更新/完成任务

- **创建任务**：
  `node {baseDir}/scripts/asana.mjs create-task --workspace <gid> --name "..." --projects <project_gid> --assignee me`
- **更新任务**：
  `node {baseDir}/scripts/asana.mjs update-task <task_gid> --name "..." --due_on 2026-02-01`
- **完成任务**：
  `node {baseDir}/scripts/asana.mjs complete-task <task_gid>`

## 项目经理的工作流程

该技能支持项目经理在 Asana 中常用的工作流程：

- **更新项目简介**：
  `node {baseDir}/scripts/asana.mjs upsert-project-brief`
- **编写状态更新**：
  `node {baseDir}/scripts/asana.mjs create-status-update`
- **管理时间线**（开始/截止日期）并安全地调整计划
- **使用自定义字段**作为重要元数据
- **解析任务阻塞原因和依赖关系**：
  `project-blockers`, `dependencies`, `dependents`

### 项目简介

- **读取项目简介**：
  `node {baseDir}/scripts/asana.mjs project-brief <project_gid>`
- **更新项目简介**：
  `node {baseDir}/scripts/asana.mjs upsert-project-brief <project_gid> --title "项目简介" --html_text "<body>...</body>"
```

### 状态更新

- **创建状态更新**：
  `node {baseDir}/scripts/asana.mjs create-status-update --parent <project_gid> --status_type on_track --text "每周更新..."
- **列出所有状态更新**：
  `node {baseDir}/scripts/asana.mjs status-updates --parent <project_gid> --all`

### 管理项目章节和任务

- **列出项目章节**：
  `node {baseDir}/scripts/asana.mjs sections --project <project_gid> --all`
- **创建新章节**：
  `node {baseDir}/scripts/asana.mjs create-section --project <project_gid> --name "Blocked"`
```

#### 将任务添加到项目中

命令：`add-task-to-project`

该命令会发送 `POST /tasks/{task_gid}/addProject` 请求，并支持设置任务的章节信息及顺序。

示例：
```bash
node {baseDir}/scripts/asana.mjs add-task-to-project <task_gid> --project <project_gid>`
```

带有章节信息的示例：
```bash
node {baseDir}/scripts/asana.mjs add-task-to-project <task_gid> --project <project_gid> --section <section_gid> --insert_before null --insert_after null`
```

`--section`, `--insert_before`, 和 `--insert_after` 是可选参数；如果提供这些参数，它们会作为请求体的一部分被发送。

#### 从项目中删除任务

命令：`remove-task-from-project`

该命令会发送 `POST /tasks/{task_gid}/removeProject` 请求。

示例：
```bash
node {baseDir}/scripts/asana.mjs remove-task-from-project <task_gid> --project <project_gid>`
```

## 自定义字段

自定义字段对于实现可靠的自动化任务管理至关重要：

- **列出项目的自定义字段**：
  `node {baseDir}/scripts/asana.mjs project-custom-fields <project_gid> --all`
- **读取自定义字段的定义**：
  `node {baseDir}/scripts/asana.mjs custom-field <custom_field_gid>`
- **在创建/更新任务时设置自定义字段**：
  `node {baseDir}/scripts/asana.mjs update-task <task_gid> --custom_fields '{"<custom_field_gid>":"<value>"}`
  *注：对于枚举类型，值应为对应的枚举 ID；对于数字，应直接传递 JSON 格式的数值。*

## 丰富的文本、提及功能及数据可靠性

Asana 的富文本字段是包含在 `<body>` 根元素中的 XML 格式 HTML 内容。API 会拒绝无效的 XML 或不支持的标签。

**使用建议：**
- 使用 `html_notes` 用于任务描述。
- 使用 `html_text` 用于注释/状态更新。
- 避免使用不支持的标签（如 `<p>` 和 `<br>`；建议使用换行符 `\n` 或 `<hr/>` 作为分隔符。
- 对于提及功能，使用 `<a data-asana-gid="..."></a>`（或自闭合的 `<a .../>`）。

### 提及通知

创建提及链接并不能保证用户一定会收到通知（特别是当用户尚未被分配到该任务或未关注该任务时）。

为了确保通知能够成功送达，请采取以下方法之一：
- 先将用户分配到任务中，然后再发布评论；
- 或者将用户添加为关注者，等待几秒钟后再发布评论。

该技能支持以下操作模式：
```bash
node {baseDir}/scripts/asana.mjs comment <task_gid> --html_text "<body>Hi <a data-asana-gid=\"<user_gid>\"/>...</body>" --ensure_followers <user_gid> --wait_ms 2500`
```

**注意**：纯文本评论（使用 `--text` 参数）无法通过 API 创建真正的提及功能；它们仍然只是普通文本。

## 附件、上传和内联图片

- **向任务添加附件**：
  `node {baseDir}/scripts/asana.mjs upload-attachment --parent <task_gid> --file /path/to/file.png`
- **在任务或项目简介中嵌入图片**：
  `node {baseDir}/scripts/asana.mjs append-inline-image --attachment <attachment_gid> --task <task_gid>`

## 活动流/类似收件箱的功能

Asana 没有提供统一的“收件箱”API来处理所有通知。最接近这一功能的稳定 API 是 `Events` 端点，它针对特定的资源（如项目或任务）提供增量更新。

**使用方法：**
- `events --resource <gid>` 可以获取项目的最新变更信息（或用户“我的任务”列表）。
- 该命令会将同步令牌存储在本地，以便后续调用时仅获取变更内容。

## 时间线调整

- **调整单个任务的截止日期**（可选包含子任务）：
  `node {baseDir}/scripts/asana.mjs shift-task-dates <task_gid> --delta_days 7 --dry_run true`
- **调整整个项目的任务截止日期**：
  `node {baseDir}/scripts/asana.mjs shift-project-tasks --project <project_gid> --delta_days -3 --dry_run true --all`
  首先使用 `--dry_run true` 运行命令，然后再使用 `--dry_run false` 重新运行。

## 不包含的功能

- 项目组合（仅限高级会员）被有意省略。
- 该技能未包含与机器人“个性”相关的设置；具体行为需要在代理程序的提示中配置。