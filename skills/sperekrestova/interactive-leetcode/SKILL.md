---
name: interactive-leetcode-mcp
description: **使用说明：**  
当用户希望练习 LeetCode 的题目、提交解决方案或设置 LeetCode 的集成功能时，请参考本文档。本文档涵盖了 MCP 服务器的安装方法、学习引导式的练习流程、解决方案的提交方式以及身份验证的相关内容。
homepage: https://github.com/SPerekrestova/interactive-leetcode-mcp
disable-model-invocation: true
metadata:
  clawdbot:
    requires:
      bins: [npx]
      config: [~/.leetcode-mcp/credentials.json]
    credentials:
      stores: ~/.leetcode-mcp/credentials.json
      contents: csrftoken, LEETCODE_SESSION, createdAt timestamp
      permissions: "0600"
---

# 交互式 LeetCode MCP

这是一个用于 LeetCode 练习的 MCP（Master Control Panel）工具，它提供学习引导提示、解决方案提交以及基于 AI 的身份验证功能。

## 先决条件：确保 MCP 服务器已连接

在开始之前，请检查 `get_started` 工具是否可用。如果可用，则说明服务器已连接——可以直接进入下一节。

**如果 `get_started` 不可用**，则需要安装 MCP 服务器。**在继续之前请用户确认**——并告知用户这将下载并运行一个 npm 包。

该 npm 包的名称是 [`@sperekrestova/interactive-leetcode-mcp`](https://www.npmjs.com/package/@sperekrestova/interactive-leetcode-mcp)（来源：[GitHub](https://github.com/SPerekrestova/interactive-leetcode-mcp))。该工具通过 stdio 传输方式进行运行，要求使用 Node.js >= 20。

用户确认后，需要将该包添加到客户端的 MCP 配置文件中（具体文件因客户端而异）：

```json
{
  "mcpServers": {
    "leetcode": {
      "command": "npx",
      "args": ["-y", "@sperekrestova/interactive-leetcode-mcp@3.1.1"]
    }
  }
}
```

对于 Claude Code 来说，还可以运行以下命令：

```bash
claude mcp add --transport stdio leetcode -- npx -y @sperekrestova/interactive-leetcode-mcp@3.1.1
```

**建议固定使用特定版本**（如上所示），而不是使用 `@latest`，以避免执行未经测试的代码。用户可以在 [npm 页面](https://www.npmjs.com/package/@sperekrestova/interactive-leetcode-mcp) 或 [GitHub 仓库的发布记录](https://github.com/SPerekrestova/interactive-leetcode-mcp/releases) 中查看最新版本，并在查看更新日志后更新所使用的版本。

添加服务器配置后，告知用户重新启动会话，以便 MCP 工具能够正常使用。在 `get_started` 可用之前，不要继续进行会话流程。

## 首要操作：始终调用 `get_started`

在每次 LeetCode 会话开始时，必须调用 `get_started` 工具。该工具会返回完整的使用指南，包括提示使用规则、会话流程、学习模式规则、身份验证流程以及语言设置。

**切勿跳过此步骤**——这只是一个简单的调用，并不会与工具描述重复。MCP 的提示需要用户手动触发，它们不会自动启用。`get_started` 的返回结果会明确告知您何时以及如何进行这些操作。

## 会话流程（非常重要）

```
1. Call get_started              <-- FIRST, every session
2. Invoke leetcode_learning_mode <-- BEFORE any problem discussion
3. User picks a problem
4. Invoke leetcode_problem_workflow(problemSlug, difficulty)
5. Invoke leetcode_workspace_setup(language, problemSlug, codeTemplate)
6. Guide user with progressive hints (4 levels)
7. submit_solution when ready
```

步骤 2、4 和 5 需要通过 `Skill` 工具或相应的提示机制来触发。这三个步骤必须在用户开始编写代码之前完成。

**步骤 2 是必须执行的**。如果您跳过了 `leetcode_learning_mode`，将会绕过渐进式提示系统，可能导致过早显示解决方案。请在搜索或讨论问题之前先调用该步骤。

## 提示使用规则

| 提示            | 触发条件          | 参数                        |
|------------------|------------------|---------------------------|
| `leetcode_learning_mode` | 会话开始时          |                           |
| `leetcode_problem_workflow` | 用户选择问题后        | problemSlug, difficulty            |
| `leetcode_workspace_setup` | 用户开始编写代码前      | language, problemSlug, codeTemplate       |
| `leetcode_authentication_guide` | 需要身份验证时、出现 401 错误或凭证过期时 |                           |

## 学习模式规则

- 未经提示级别 1 → 2 → 3 的引导，切勿直接显示完整解决方案
- 级别 1：引导性问题（“你看到了什么模式？”）
- 级别 2：通用解题方法（“可以考虑使用哈希表...”）
- 级别 3：具体提示（“遍历一次，并记录已使用的值...”）
- 只有在用户明确请求后，才显示完整解决方案
- `get_problem_solution` 仅会在级别 4 或用户明确请求时返回社区提供的完整解决方案

## 工具快速参考

| 工具            | 功能                | 是否需要身份验证            |
|------------------|------------------|----------------------|
| `get_daily_challenge` | 当天的挑战题          | 不需要                     |
| `get_problem`      | 根据问题 slug 获取问题           | 不需要                     |
| `search_problems`     | 根据标签/难度/关键词查找问题       | 不需要                     |
| `list_problem_solutions` | 问题解决方案的元数据          | 不需要                     |
| `get_problem_solution` | 完整解决方案（仅限级别 4）        | 不需要                     |
| `submit_solution`     | 提交代码                | 不需要                     |
| `get_user_profile`     | 用户的统计信息            | 不需要                     |
| `get_recent_submissions` | 最近的提交记录           | 不需要                     |
| `get_recent_ac_submissions` | 被接受的提交记录           | 不需要                     |
| `get_user_contest_ranking` | 用户的竞赛排名            | 不需要                     |
| `start_leetcode_auth`    | 开始身份验证流程            | 不需要                     |
| `save_leetcode_credentials` | 验证并保存凭证            | 不需要                     |
| `check_auth_status`    | 检查凭证状态              | 不需要                     |
| `get_user_status`     | 当前用户信息              | 需要                     |
| `get_problemsubmission_report` | 提交详情              | 需要                     |
| `get_problem_progress` | 查看提交进度            | 需要                     |
| `get_all_submissions` | 查看所有提交记录           | 需要                     |

*`submit_solution` 需要用户已保存的凭证才能成功提交。*

## 身份验证流程

1. 在执行任何需要身份验证的操作之前，先调用 `check_auth_status`。
2. 如果用户未认证或凭证已过期，**询问用户是否希望进行认证**。请告知用户，认证信息将存储在本地文件 `~/.leetcode-mcp/credentials.json` 中（仅允许所有者读写）。未经用户同意，不要继续操作。
3. 用户同意后，调用 `leetcode_authentication_guide` 提示。
4. 调用 `start_leetcode_auth`，该提示会指导用户完成凭证的输入。
5. 如果操作成功，继续执行原始操作。
6. 如果任何工具返回 401 错误，重新从步骤 1 开始。

**始终将身份验证的引导任务交给 `leetcode_authentication_guide` 提示来完成**。不要自行编写身份验证指令——该提示会处理浏览器特定的引导流程、错误恢复和故障排除。

**凭证存储方式：**MCP 服务器将凭证存储在本地文件 `~/.leetcode-mcp/credentials.json` 中，文件权限设置为 `0o600`（仅允许所有者读写）。存储的凭证包括 `csrftoken`、`LEETCODE_SESSION` 和 `createdAt` 时间戳。凭证永远不会传输给第三方，仅用于直接调用 LeetCode 的 API。凭证的有效期为 7-14 天。

## 提交代码的语言设置

| 用户输入的语言 | 传递给 `submit_solution` 的语言参数 |
|------------------|------------------------|
| Python / Python 3    | `python3`                     |
| Python 2    | `python`                     |
| Java           | `java`                     |
| C++          | `cpp`                     |
| JavaScript     | `javascript`                     |
| TypeScript     | `typescript`                     |

默认语言设置为 “Python”（如果没有指定版本）——此时使用 `python3`。

## 资源（仅用于读取）

| 资源 URI            | 提供的内容                |
|------------------|------------------------|
| `categories://problems/all` | 所有问题类别                |
| `tags://problems/all` | 所有问题的标签                |
| `langs://problems/all` | 所支持的所有编程语言            |
| `problem://{titleSlug}` | 问题详情                |
| `solution://{topicId}` | 解决方案详情（遵循相同的学习模式规则） |

## 常见错误

- 在调用 `leetcode_learning_mode` 之前直接跳转到问题搜索
- 未经过提示级别 1 → 2 → 3 的引导就直接显示完整解决方案
- 未调用 `leetcode_workspace_setup`——代码应保存在文件中，而不仅仅是聊天框内
- 手动进行身份验证引导，而不是使用 `leetcode_authentication_guide`
- 在 `submit_solution` 中传递 “Python” 而不是 “python3”
- 在执行需要身份验证的操作之前未调用 `check_auth_status`
- 跳过 `get_started`，认为工具描述已经足够