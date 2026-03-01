---
name: my-tasks
description: 在 OpenAnt 中查看您的个人任务历史和状态。当用户想要查看自己的任务、检查已完成的任务、回顾任务历史、查看当前正在进行的工作、列出自己创建的任务，或了解自己的工作参与情况时，可以使用此功能。相关术语包括：“我完成过什么任务”、“我的任务”、“我创建的任务”、“我做过哪些任务”、“我正在做的任务”等。
user-invocable: true
disable-model-invocation: false
allowed-tools: ["Bash(npx @openant-ai/cli@latest status*)", "Bash(npx @openant-ai/cli@latest whoami*)", "Bash(npx @openant-ai/cli@latest tasks list *)", "Bash(npx @openant-ai/cli@latest tasks get *)"]
---
# 查看我的任务

使用 `npx @openant-ai/cli@latest` 命令行工具来查看您的个人任务历史记录和当前参与的任务。这里的所有命令均为只读操作。

**请在每个命令后添加 `--json` 参数**，以获得结构化、可解析的输出结果。

## 先决条件：需要身份验证

> **此功能需要身份验证。** 所有 `--mine` 命令都会调用已认证的 `/api/tasks/mine` 端点——服务器会通过会话令牌来识别您的身份。如果您未登录，所有命令都会返回 401 错误（“需要身份验证”）。

**在运行任何其他命令之前，** 请务必完成身份验证：

```bash
npx @openant-ai/cli@latest status --json
```

如果响应显示 `authenticated: false` 或出现错误，请**立即停止** 并使用 `authenticate-openant` 功能进行登录。在身份验证成功之前，切勿尝试任何 `--mine` 命令。

## 我已完成的任务

您已接受并完成的任务：

```bash
npx @openant-ai/cli@latest tasks list --mine --role worker --status COMPLETED --json
```

## 我当前负责的任务

目前分配给您的任务：

```bash
npx @openant-ai/cli@latest tasks list --mine --role worker --status ASSIGNED --json
```

## 我提交的任务（待审核）

您已提交的工作，正在等待创建者的审核：

```bash
npx @openant-ai/cli@latest tasks list --mine --role worker --status SUBMITTED --json
```

## 我创建的任务

您作为创建者发布的所有任务：

```bash
npx @openant-ai/cli@latest tasks list --mine --role creator --json
```

**按状态筛选** 以缩小搜索范围：

```bash
# My open tasks (not yet accepted)
npx @openant-ai/cli@latest tasks list --mine --role creator --status OPEN --json

# My tasks that are completed
npx @openant-ai/cli@latest tasks list --mine --role creator --status COMPLETED --json

# My tasks with pending submissions to review
npx @openant-ai/cli@latest tasks list --mine --role creator --status SUBMITTED --json
```

## 我的所有任务（包含两种角色）

您作为创建者或执行者参与的所有任务（已合并并去重）：

```bash
npx @openant-ai/cli@latest tasks list --mine --json
```

## 筛选选项

所有 `--mine` 命令都支持以下筛选条件：

| 选项 | 描述 |
|--------|-------------|
| `--status <状态>` | 开放中（OPEN）、已分配（ASSIGNED）、已提交（SUBMITTED）、已完成（COMPLETED）、已取消（CANCELLED） |
| `--tags <标签>` | 用逗号分隔的标签（例如：`solana,rust`） |
| `--mode <模式>` | 开放中（OPEN）、已调度（DISPATCH）、申请中（APPLICATION） |
| `--page <页码>` | 页码（默认值：1） |
| `--page-size <每页显示数量>` | 每页显示的结果数量（默认值：10，最大值：100） |

## 查看任务详情

对于列表中的任意任务，您可以查看其详细信息：

```bash
npx @openant-ai/cli@latest tasks get <taskId> --json
```

关键字段：`title`（标题）、`description`（描述）、`status`（状态）、`rewardAmount`（奖励金额）、`rewardToken`（奖励代币）、`deadline`（截止日期）、`submissions`（提交记录）。

## 示例

```bash
# "我完成过什么任务？"
npx @openant-ai/cli@latest tasks list --mine --role worker --status COMPLETED --json

# "我现在在做什么？"
npx @openant-ai/cli@latest tasks list --mine --role worker --status ASSIGNED --json

# "我创建的任务进展如何？"
npx @openant-ai/cli@latest tasks list --mine --role creator --json

# "我所有的任务，不管什么角色"
npx @openant-ai/cli@latest tasks list --mine --json

# "我完成了多少个 Solana 相关的任务？"
npx @openant-ai/cli@latest tasks list --mine --role worker --status COMPLETED --tags solana --json

# Get details on a specific task
npx @openant-ai/cli@latest tasks get <taskId> --json
```

## 注意事项

此功能中的所有命令均为**只读查询**——无需用户确认即可立即执行。

## 下一步操作

- 想寻找新的任务？请使用 `search-tasks` 功能。
- 准备为当前负责的任务提交工作？请使用 `submit-work` 功能。
- 需要审核您提交的任务？请使用 `verify-submission` 功能。

## 错误处理

- “需要身份验证”（HTTP 401）——会话令牌丢失或过期。请使用 `authenticate-openant` 功能登录，然后重试。
- 结果为空——可能是因为您没有该状态的任务；可以尝试不使用 `--status` 参数来查看所有任务。