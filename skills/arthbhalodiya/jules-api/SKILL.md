---
name: jules
description: 通过 Jules REST API 创建和管理 Google Jules AI 编码会话。可以启动任务、监控进度、批准计划、发送消息、列出源代码仓库以及检索会话活动/生成的结果文件。
metadata: {"openclaw":{"requires":{"env":["JULES_API_KEY"],"bins":["curl"]},"primaryEnv":"JULES_API_KEY","emoji":"🤖","homepage":"https://jules.google/docs/api/reference/"}}
---
# Jules API 技能

通过其 REST API 与 [Google Jules](https://jules.google) 人工智能编程代理进行交互。Jules 可以在您的 GitHub 仓库中自主执行编码任务——编写代码、修复错误、添加测试以及创建拉取请求（pull requests）。

**基础 URL：** `https://jules.googleapis.com/v1alpha`
**认证：** 通过 `x-goog-api-key` 请求头传递您的 API 密钥。您可以在 [jules.google.com/settings](https://jules.google.com/settings) 获取 API 密钥。

---

## 列出来源（连接的仓库）

查看哪些 GitHub 仓库已连接到您的 Jules 账户：

```bash
curl -s -H "x-goog-api-key: $JULES_API_KEY" \
  "https://jules.googleapis.com/v1alpha/sources?pageSize=30"
```

（支持分页查询：）

```bash
curl -s -H "x-goog-api-key: $JULES_API_KEY" \
  "https://jules.googleapis.com/v1alpha/sources?pageSize=10&pageToken=PAGE_TOKEN"
```

**过滤特定来源：**

```bash
curl -s -H "x-goog-api-key: $JULES_API_KEY" \
  "https://jules.googleapis.com/v1alpha/sources?filter=name%3Dsources%2Fgithub-owner-repo"
```

## 获取来源信息

获取特定仓库的详细信息和分支信息：

```bash
curl -s -H "x-goog-api-key: $JULES_API_KEY" \
  "https://jules.googleapis.com/v1alpha/sources/SOURCE_ID"
```

**示例：** `sources/github-myorg-myrepo` —— 请替换为您在“列出来源”步骤中获取的实际来源 ID。

---

## 创建会话（开始编码任务）

创建一个新的 Jules 会话以在某个仓库上执行编码任务：

```bash
curl -s -X POST \
  -H "x-goog-api-key: $JULES_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "TASK_DESCRIPTION",
    "title": "OPTIONAL_TITLE",
    "sourceContext": {
      "source": "sources/github-OWNER-REPO",
      "githubRepoContext": {
        "startingBranch": "main"
      }
    },
    "requirePlanApproval": true
  }' \
  "https://jules.googleapis.com/v1alpha/sessions"
```

### 参数

| 参数 | 是否必填 | 描述 |
|---|---|---|
| `prompt` | 是 | 用于指示 Jules 执行的任务描述 |
| `title` | 否 | 可选标题（如果省略，则会自动生成） |
| `sourceContext.source` | 是 | 来源资源名称（例如 `sources/github-owner-repo`） |
| `sourceContext.githubRepoContext.startingBranch` | 是 | 要从哪个分支开始执行（例如 `main`、`develop`） |
| `requirePlanApproval` | 否 | 如果设置为 `true`，则在执行前需要明确批准计划 |
| `automationMode` | 否 | 设置为 `AUTO_CREATE_PR` 会在任务完成后自动创建拉取请求（PR） |

### 自动批准 + 自动创建拉取请求的示例

```bash
curl -s -X POST \
  -H "x-goog-api-key: $JULES_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Add comprehensive unit tests for the auth module",
    "sourceContext": {
      "source": "sources/github-myorg-myrepo",
      "githubRepoContext": { "startingBranch": "main" }
    },
    "automationMode": "AUTO_CREATE_PR"
  }' \
  "https://jules.googleapis.com/v1alpha/sessions"
```

---

## 列出所有会话

查看所有的 Jules 会话：

```bash
curl -s -H "x-goog-api-key: $JULES_API_KEY" \
  "https://jules.googleapis.com/v1alpha/sessions?pageSize=10"
```

（支持使用 `pageToken` 进行分页查询：）

```bash
curl -s -H "x-goog-api-key: $JULES_API_KEY" \
  "https://jules.googleapis.com/v1alpha/sessions?pageSize=10&pageToken=NEXT_PAGE_TOKEN"
```

## 获取会话信息

通过会话 ID 获取会话详情（如果任务已完成，会包含拉取请求的 URL）：

```bash
curl -s -H "x-goog-api-key: $JULES_API_KEY" \
  "https://jules.googleapis.com/v1alpha/sessions/SESSION_ID"
```

### 会话状态

| 状态 | 含义 |
|---|---|
| `QUEUED` | 等待处理 |
| `PLANNING` | Jules 正在分析并制定计划 |
| `AWAITING_PLAN_APPROVAL` | 计划已准备好，等待用户批准 |
| `AWAITING_USER_FEEDBACK` | Jules 需要用户的额外输入 |
| `IN_PROGRESS` | Jules 正在积极执行任务 |
| `PAUSED` | 会话已暂停 |
| `COMPLETED` | 任务成功完成 |
| `FAILED` | 任务未能完成 |

---

## 批准计划

当会话处于 `AWAITING_PLAN_APPROVAL` 状态时，批准该计划：

```bash
curl -s -X POST \
  -H "x-goog-api-key: $JULES_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{}' \
  "https://jules.googleapis.com/v1alpha/sessions/SESSION_ID:approvePlan"
```

## 发送消息

向正在执行的会话发送反馈、回答问题或提供额外指示：

```bash
curl -s -X POST \
  -H "x-goog-api-key: $JULES_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "YOUR_MESSAGE_HERE"
  }' \
  "https://jules.googleapis.com/v1alpha/sessions/SESSION_ID:sendMessage"
```

当会话状态为 `AWAITING_USER_FEEDBACK` 时使用此功能；或在任务执行过程中（`IN_PROGRESS` 状态）提供额外指导。

---

## 列出活动（监控进度）

获取会话的所有事件和进度信息：

```bash
curl -s -H "x-goog-api-key: $JULES_API_KEY" \
  "https://jules.googleapis.com/v1alpha/sessions/SESSION_ID/activities?pageSize=50"
```

**按特定时间戳获取活动记录（用于轮询）：**

```bash
curl -s -H "x-goog-api-key: $JULES_API_KEY" \
  "https://jules.googleapis.com/v1alpha/sessions/SESSION_ID/activities?createTime=2026-01-17T00:03:53Z"
```

### 活动类型

活动记录中会包含以下事件类型之一：

| 事件 | 描述 |
|---|---|
| `planGenerated` | Jules 创建了计划（包含 `plan_steps[]`） |
| `planApproved` | 计划已获得批准 |
| `userMessaged` | 用户发送了消息 |
| `agentMessaged` | Jules 发送了消息 |
| `progressUpdated` | 执行过程中的状态更新 |
| `sessionCompleted` | 会话成功完成 |
| `sessionFailed` | 会话遇到错误（包含错误原因） |

### 文档输出

活动记录可能包含以下文档类型：

- **ChangeSet**：代码变更信息（包含 `gitPatch`、基础提交信息及建议的提交信息） |
- **BashOutput**：命令执行结果（包含 `command`、`output`、`exitCode`） |
- **Media**：二进制输出文件（包含 `mimeType` 和 Base64 编码的 `data`）

## 获取单个活动记录

```bash
curl -s -H "x-goog-api-key: $JULES_API_KEY" \
  "https://jules.googleapis.com/v1alpha/sessions/SESSION_ID/activities/ACTIVITY_ID"
```

---

## 删除会话

```bash
curl -s -X DELETE \
  -H "x-goog-api-key: $JULES_API_KEY" \
  "https://jules.googleapis.com/v1alpha/sessions/SESSION_ID"
```

---

## 典型工作流程

1. **列出来源** 以获取仓库资源名称 |
2. **创建会话** 并指定任务描述 |
3. **轮询会话** 以跟踪状态变化 |
4. **列出活动记录** 以监控进度并查看 Jules 的消息 |
5. 如果设置了 `requirePlanApproval`，则在会话状态为 `AWAITING_PLAN_APPROVAL` 时批准计划 |
6. 如果会话状态为 `AWAITING_USER_FEEDBACK`，发送反馈信息 |
7. 当任务完成（`COMPLETED`）时，获取会话信息以获取拉取请求的 URL。

## 错误处理

| 状态码 | 含义 |
|---|---|
| 200 | 成功 |
| 400 | 请求无效（参数错误） |
| 401 | 未经授权（API 密钥无效或缺失） |
| 403 | 欠乏权限 |
| 404 | 未找到相关资源 |
| 429 | 请求频率超出限制 |
| 500 | 服务器错误 |

错误响应的详细信息如下：

```json
{
  "error": {
    "code": 400,
    "message": "Invalid session ID format",
    "status": "INVALID_ARGUMENT"
  }
}
```

## 注意事项：

- 请从 [jules.google.com/settings](https://jules.google.com/settings) 获取您的 API 密钥，并将其设置为 `JULES_API_KEY` 环境变量 |
- 来源（仓库）可以通过 Jules 的 Web 界面进行管理（地址：[jules.google](https://jules.google)）；API 对于来源资源仅支持读取操作 |
- 会话资源的命名格式为 `sessions/{sessionId}` |
- 活动记录的命名格式为 `sessions/{sessionId}/activities/{activityId}` |
- 所有列表接口都支持 `pageSize`（1-100）和 `pageToken` 进行分页查询