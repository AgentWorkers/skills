---
name: jules-api
description: "通过 `curl` 使用 Jules REST API（v1alpha）来执行以下操作：列出源代码信息、创建会话、监控活动、批准计划、发送消息以及检索输出结果（例如 PR 的 URL）。当用户希望以编程方式将编码任务委托给 Jules 时，可以使用此 API。使用此功能需要设置 `JULES_API_KEY` 环境变量（可从 https://jules.google.com/settings#api 获取）。"
env:
  JULES_API_KEY:
    required: true
    description: "API key for the Jules service. Obtain from https://jules.google.com/settings#api"
dependencies:
  - name: curl
    required: true
    description: "Used for all API requests to jules.googleapis.com"
  - name: python3
    required: true
    description: "Used by jules_api.sh for safe JSON string escaping"
  - name: node
    required: false
    description: "Required only for scripts/jules.js CLI wrapper"
  - name: jules
    required: false
    description: "Jules CLI binary, required only for scripts/jules.js CLI wrapper"
---
# Jules REST API 技能

## 快速入门

```bash
# 0. Set your API key (required — get one at https://jules.google.com/settings#api)
export JULES_API_KEY="your-api-key-here"

# 1. Verify available sources (pre-flight check)
./scripts/jules_api.sh sources

# 2. Create a session with plan approval and auto PR creation
./scripts/jules_api.sh new-session \
  --source "sources/github/OWNER/REPO" \
  --title "Add unit tests" \
  --prompt "Add comprehensive unit tests for the authentication module" \
  --branch main \
  --require-plan-approval \
  --auto-pr

# 3. Monitor session progress and approve the plan
./scripts/jules_api.sh activities --session SESSION_ID
./scripts/jules_api.sh approve-plan --session SESSION_ID
```

**注意：** 使用你的 GitHub 用户名/组织名，而不是本地系统用户名（例如，`sources/github/octocat/Hello-World`，而不是 `sources/github/$USER/Hello-World`）。

## 概述

此技能允许你通过编程方式与 **Jules REST API (v1alpha)** 进行交互，从而将编码任务委托给 Jules（Google 的自主 AI 编码代理）。它支持以下功能：

- **任务分配**：创建带有具体提示的新编码会话
- **会话监控**：实时跟踪会话状态和活动
- **计划管理**：批准或审查生成的计划
- **消息传递**：向活跃的会话发送跟进消息
- **结果整合**：从已完成的会话中获取 PR URL 和代码更改

## 开始使用前

### 1. 获取 API 密钥

在 Jules 网页应用中创建一个 API 密钥：
- 访问：https://jules.google.com/settings#api
- 你最多可以同时拥有 **3 个 API 密钥**

将密钥导出到运行代理的机器上：

```bash
export JULES_API_KEY="your-api-key-here"
```

### 2. 连接你的 GitHub 仓库

在 API 能够操作 GitHub 仓库之前，你必须：
1. 通过 Jules 网页界面安装 **Jules GitHub 应用**
2. 授予 Jules 访问你希望其操作的特定仓库的权限

### 3. 验证仓库访问权限

```bash
# List available sources to verify access and see correct format
./scripts/jules_api.sh sources
```

你会看到如下信息：
```json
{
  "sources": [
    {
      "name": "sources/github/octocat/Hello-World",
      "githubRepo": {
        "owner": "octocat",
        "repo": "Hello-World",
        "defaultBranch": { "displayName": "main" },
        "branches": [
          { "displayName": "main" },
          { "displayName": "develop" }
        ]
      }
    }
  ]
}
```

## 基础 URL 与身份验证

| 属性 | 值 |
|----------|-------|
| 基础 URL | `https://jules.googleapis.com/v1alpha` |
| 身份验证头 | `x-goog-api-key: $JULES_API_KEY` |

所有请求都使用以下方式进行身份验证：
```bash
-H "x-goog-api-key: $JULES_API_KEY"
```

## 核心概念

### 资源

| 资源 | 描述 |
|----------|-------------|
| **来源** | 与 Jules 连接的 GitHub 仓库。格式：`sources/github/{owner}/{repo}` |
| **会话** | Jules 执行编码任务的工作单元。包含状态、活动和输出 |
| **活动** | 会话中的单个事件（例如，生成计划、发送消息、进度更新等） |

### 会话状态

| 状态 | 描述 |
|-------|-------------|
| `QUEUED` | 会话正在等待开始 |
| `PLANNING` | 生成执行计划 |
| `AWAITING_PLAN_APPROVAL` | 等待用户批准计划 |
| `AWAITING_USER_FEEDBACK` | 需要用户输入才能继续 |
| `IN_PROGRESS` | 正在积极执行任务 |
| `PAUSED` | 暂时停止 |
| `COMPLETED` | 成功完成 |
| `FAILED` | 遇到错误 |

### 活动类型

| 类型 | 描述 |
|------|-------------|
| Plan Generated | 为任务生成了计划 |
| Plan Approved | 计划已获批准（手动或自动） |
| User Message | 用户向会话发送了消息 |
| Agent Message | Jules 发送了消息 |
| Progress Update | 当前工作的状态更新 |
| Session Completed | 会话成功完成 |
| Session Failed | 会话遇到错误 |

## 工作流程

### 选项 1：需要计划批准并自动创建 PR 的会话（推荐）

创建一个在执行前需要计划批准的会话，并在完成后自动创建 PR：

```bash
./scripts/jules_api.sh new-session \
  --source "sources/github/octocat/Hello-World" \
  --title "Fix login bug" \
  --prompt "Fix the null pointer exception in the login handler when email is empty" \
  --branch main \
  --require-plan-approval \
  --auto-pr
```

**推荐原因：**
- 你在 Jules 执行更改之前先审查并批准计划
- 完成后自动创建 PR
- 在自动化和人工监督之间取得平衡

### 选项 2：完全自动化的会话（无需计划批准）

对于低风险或常规任务（位于非敏感仓库中），你可以跳过计划批准：

```bash
# Create session without plan approval (use only for low-risk tasks)
./scripts/jules_api.sh new-session \
  --source "sources/github/octocat/Hello-World" \
  --title "Fix typo in README" \
  --prompt "Fix the typo in README.md line 5" \
  --branch main \
  --auto-pr
```

**警告：** 如果不使用 `--require-plan-approval`，Jules 会自动批准其计划并执行更改。仅适用于非关键仓库中的低风险任务。

### 选项 3：交互式会话

在活跃的会话期间发送跟进消息：

```bash
# Create session
./scripts/jules_api.sh new-session \
  --source "sources/github/octocat/Hello-World" \
  --title "Add API endpoints" \
  --prompt "Add REST API endpoints for user management" \
  --branch main

# Send additional instructions
./scripts/jules_api.sh send-message \
  --session SESSION_ID \
  --prompt "Also add input validation for all endpoints"
```

## API 参考

### 来源

#### 列出来源
列出所有连接的 GitHub 仓库。

```bash
curl -sS \
  -H "x-goog-api-key: $JULES_API_KEY" \
  "https://jules.googleapis.com/v1alpha/sources"
```

**查询参数：**
| 参数 | 类型 | 默认值 | 描述 |
|-----------|------|---------|-------------|
| `pageSize` | 整数 | 30 | 返回的来源数量（1-100） |
| `pageToken` | 字符串 | - | 上一次响应的分页令牌 |
| `filter` | 字符串 | - | AIP-160 过滤器（例如，`name=sources/source1`）

**响应：**
```json
{
  "sources": [
    {
      "name": "sources/github/octocat/Hello-World",
      "githubRepo": {
        "owner": "octocat",
        "repo": "Hello-World",
        "isPrivate": false,
        "defaultBranch": { "displayName": "main" },
        "branches": [
          { "displayName": "main" },
          { "displayName": "develop" }
        ]
      }
    }
  ],
  "nextPageToken": "..."
}
```

#### 获取来源
按名称获取单个来源。

```bash
curl -sS \
  -H "x-goog-api-key: $JULES_API_KEY" \
  "https://jules.googleapis.com/v1alpha/sources/github/octocat/Hello-World"
```

使用此功能在创建会话之前查看可用的分支。

---

### 会话

#### 创建会话
创建一个新的编码会话。

```bash
curl -sS "https://jules.googleapis.com/v1alpha/sessions" \
  -X POST \
  -H "Content-Type: application/json" \
  -H "x-goog-api-key: $JULES_API_KEY" \
  -d '{
    "prompt": "Add unit tests for the login module",
    "title": "Add Login Tests",
    "sourceContext": {
      "source": "sources/github/octocat/Hello-World",
      "githubRepoContext": {
        "startingBranch": "main"
      }
    },
    "requirePlanApproval": true,
    "automationMode": "AUTO_CREATE_PR"
  }'
```

**请求体字段：**
| 字段 | 类型 | 是否必需 | 描述 |
|-------|------|----------|-------------|
| `prompt` | 字符串 | 是 | 用于 Jules 的任务描述 |
| `title` | 字符串 | 否 | 会话的简短标题 |
| `sourceContext.source` | 字符串 | 是 | 来源名称（例如，`sources/github/owner/repo`） |
| `sourceContext.githubRepoContext.startingBranch` | 字符串 | 是 | 要从哪个分支开始 |
| `requirePlanApproval` | 布尔值 | 否 | 如果为 true，则暂停以等待计划批准。建议在生产仓库中使用 true |
| `automationMode` | 字符串 | 否 | 设置为 `AUTO_CREATE_PR` 以自动创建 PR |

**响应：**
```json
{
  "name": "sessions/31415926535897932384",
  "id": "31415926535897932384",
  "prompt": "Add unit tests for the login module",
  "title": "Add Login Tests",
  "state": "QUEUED",
  "url": "https://jules.google/session/31415926535897932384",
  "createTime": "2026-01-15T10:30:00Z",
  "updateTime": "2026-01-15T10:30:00Z"
}
```

#### 列出会话
列出你的会话。

```bash
curl -sS \
  -H "x-goog-api-key: $JULES_API_KEY" \
  "https://jules.googleapis.com/v1alpha/sessions?pageSize=20"
```

**查询参数：**
| 参数 | 类型 | 默认值 | 描述 |
|-----------|------|---------|-------------|
| `pageSize` | 整数 | 返回的会话数量（1-100） |
| `pageToken` | 字符串 | - | 上一次响应的分页令牌 |

#### 获取会话
按 ID 获取单个会话。

```bash
curl -sS \
  -H "x-goog-api-key: $JULES_API_KEY" \
  "https://jules.googleapis.com/v1alpha/sessions/SESSION_ID"
```

**响应包含完成后的输出：**
```json
{
  "name": "sessions/31415926535897932384",
  "id": "31415926535897932384",
  "state": "COMPLETED",
  "outputs": [
    {
      "pullRequest": {
        "url": "https://github.com/octocat/Hello-World/pull/42",
        "title": "Add Login Tests",
        "description": "This PR adds comprehensive unit tests..."
      }
    }
  ]
}
```

#### 发送消息
向活跃的会话发送消息。

```bash
curl -sS \
  -X POST \
  -H "Content-Type: application/json" \
  -H "x-goog-api-key: $JULES_API_KEY" \
  "https://jules.googleapis.com/v1alpha/sessions/SESSION_ID:sendMessage" \
  -d '{"prompt": "Also add integration tests"}'
```

使用此功能提供反馈、回答问题或给出额外指令。

#### 批准计划
批准待定的计划（仅在 `requirePlanApproval` 为 true 时需要）。

```bash
curl -sS \
  -X POST \
  -H "Content-Type: application/json" \
  -H "x-goog-api-key: $JULES_API_KEY" \
  "https://jules.googleapis.com/v1alpha/sessions/SESSION_ID:approvePlan"
```

#### 删除会话
删除会话。

```bash
curl -sS \
  -X DELETE \
  -H "x-goog-api-key: $JULES_API_KEY" \
  "https://jules.googleapis.com/v1alpha/sessions/SESSION_ID"
```

---

### 活动

#### 列出活动
列出会话中的活动。

```bash
curl -sS \
  -H "x-goog-api-key: $JULES_API_KEY" \
  "https://jules.googleapis.com/v1alpha/sessions/SESSION_ID/activities?pageSize=30"
```

**查询参数：**
| 参数 | 类型 | 默认值 | 描述 |
|-----------|------|---------|-------------|
| `pageSize` | 整数 | 返回的活动数量（1-100） |
| `pageToken` | 字符串 | - | 上一次响应的分页令牌 |

**响应：**
```json
{
  "activities": [
    {
      "name": "sessions/123/activities/456",
      "createTime": "2026-01-15T10:31:00Z",
      "planGenerated": {
        "plan": "1. Analyze existing code\n2. Create test files\n3. Write tests..."
      }
    },
    {
      "name": "sessions/123/activities/457",
      "createTime": "2026-01-15T10:32:00Z",
      "progressUpdate": {
        "title": "Writing tests",
        "details": "Creating test file for auth module..."
      }
    }
  ],
  "nextPageToken": "..."
}
```

活动可能包含代码更改的工件：
```json
{
  "artifacts": [
    {
      "changeSet": {
        "gitPatch": {
          "unidiffPatch": "diff --git a/...",
          "baseCommitId": "abc123",
          "suggestedCommitMessage": "Add unit tests for login"
        }
      }
    }
  ]
}
```

#### 获取活动
按 ID 获取单个活动。

```bash
curl -sS \
  -H "x-goog-api-key: $JULES_API_KEY" \
  "https://jules.googleapis.com/v1alpha/sessions/SESSION_ID/activities/ACTIVITY_ID"
```

## 脚本参考

### jules_api.sh

`scripts/jules_api.sh` 脚本为常见的 API 操作提供了便捷的封装。

**用法：**
```bash
# List sources
./scripts/jules_api.sh sources

# List sessions
./scripts/jules_api.sh sessions [--page-size N]

# List activities for a session
./scripts/jules_api.sh activities --session <id> [--page-size N]

# Send message to session
./scripts/jules_api.sh send-message --session <id> --prompt "..."

# Approve plan
./scripts/jules_api.sh approve-plan --session <id>

# Create new session
./scripts/jules_api.sh new-session \
  --source "sources/github/owner/repo" \
  --title "..." \
  --prompt "..." \
  [--branch main] \
  [--auto-pr] \
  [--no-plan-approval]
```

**标志：**
| 标志 | 描述 |
|------|-------------|
| `--source` | 来源名称（格式：`sources/github/owner/repo`） |
| `--title` | 会话标题 |
| `--prompt` | 任务描述或消息内容 |
| `--session` | 会话 ID |
| `--branch` | 起始分支（默认：`main` |
| `--auto-pr` | 启用自动创建 PR |
| `--require-plan-approval` | 要求明确的计划批准（默认） |
| `--no-plan-approval` | 跳过计划批准（仅用于低风险任务） |
| `--page-size` | 返回的结果数量 |

### jules.js

`scripts/jules.js` 脚本为编程使用封装了 Jules CLI。

**用法：**
```bash
node scripts/jules.js version
node scripts/jules.js list-repos
node scripts/jules.js list-sessions
node scripts/jules.js new --repo owner/repo --task "Your task"
node scripts/jules.js pull --session SESSION_ID
```

## 常见错误

### “Source not found” 或 “Repository not found”

**原因：** 仓库未连接或来源名称格式不正确。

**解决方案：**
1. 运行 `./scripts/jules_api.sh sources` 以列出可用的来源
2. 确保已为该仓库安装了 Jules GitHub 应用
3. 使用列表中的确切来源名称（例如，`sources/github/octocat/Hello-World`）

### “Missing JULES_API_KEY”

**原因：** 环境中未设置 API 密钥。

**解决方案：**
```bash
export JULES_API_KEY="your-api-key"
```

### 身份验证错误

**原因：** API 密钥无效或已过期。

**解决方案：**
1. 在 https://jules.google.com/settings#api 生成新的 API 密钥
2. 更新 `JULES_API_KEY` 环境变量
3. 注意：你最多可以同时拥有 3 个 API 密钥

### 会话卡在 AWAITING_PLAN_APPROVAL 状态

**原因：** 会话创建时设置了 `requirePlanApproval: true`。

**解决方案：**
```bash
./scripts/jules_api.sh approve-plan --session SESSION_ID
```

### 任务因模糊的提示而失败

**原因：** 模糊的提示可能导致意外结果。

**解决方案：**
- 编写清晰、具体的提示
- 将大型任务分解为更小、更具体的任务
- 避免使用需要长时间运行的命令（例如开发服务器、监控脚本）

### 大文件被跳过

**原因：** 超过 768,000 个字符的文件可能会被跳过。

**解决方案：**
- 将对大文件的操作分解为多个部分
- 考虑在处理之前分割大文件

## 最佳实践

### 编写有效的提示

1. **具体明确**：不要使用“修复错误”，而应使用“修复 `auth.js:45` 中的 `null pointer exception`（当 `email` 未定义时）”
2. **提供上下文**：提及相关的文件、函数或错误信息
3. **保持任务专注**：每个会话只处理一个逻辑任务

### 监控会话

1. 轮询会话状态以跟踪进度
2. 检查活动以获取详细的进度更新
3. 对于 `AWAITING_USER_FEEDBACK` 状态，发送澄清消息

### 安全性

1. 不要在提示中包含任何秘密或凭据
2. 合并之前审查生成的 PR
3. 使用 `requirePlanApproval: true`（建议对所有仓库使用，尤其是生产环境）
4. 仅在你打算与 Jules 一起使用的仓库上安装 Jules GitHub 应用——限制访问范围
5. 将 `JULES_API_KEY` 视为敏感信息：安全存储它，定期轮换，并且永远不要将其粘贴到不可信的地方

### 性能

1. 使用 `automationMode: AUTO_CREATE_PR` 以简化工作流程
2. 仅对非关键仓库中的常规、低风险任务跳过计划批准（`requirePlanApproval: false`）
3. 将复杂任务分解为多个会话

## 提取结果

当会话完成时，从输出中获取 PR URL：

```bash
# Get session details
curl -sS \
  -H "x-goog-api-key: $JULES_API_KEY" \
  "https://jules.googleapis.com/v1alpha/sessions/SESSION_ID" \
  | jq '.outputs[].pullRequest.url'
```

## 已知的限制

- **Alpha API**：规格可能会更改；API 密钥和定义是实验性的
- **不允许长时间运行的命令**：Jules 无法运行 `npm run dev` 或类似的监控脚本
- **上下文大小**：超过 768,000 个字符的文件可能会被跳过
- **提示的准确性**：模糊的提示可能导致意外结果

## 参考资料

- [Jules API 文档](https://jules.google/docs/api/reference/overview/)
- [会话参考](https://jules.google/docs/api/reference/sessions/)
- [活动参考](https://jules.google/docs/api/reference/activities/)
- [来源参考](https://jules.google/docs/api/reference/sources/)
- [类型参考](https://jules.google/docs/api/reference/types/)
- [Google 开发者 - Jules API](https://developers.google.com/jules/api)
- [Jules 设置（API 密钥）](https://jules.google.com/settings#api)