---
name: jira
description: >
  **使用场景：**  
  当用户提到 Jira 问题（例如：“PROJ-123”）、询问工单信息、希望创建/查看/更新问题、检查冲刺进度或管理 Jira 工作流程时，该功能会被触发。它会响应包含以下关键词的输入：`jira`、`issue`、`ticket`、`sprint`、`backlog` 或问题键（issue key）等。
homepage: https://github.com/ankitpokhrel/jira-cli
repository: https://github.com/PSPDFKit-labs/agent-skills
metadata:
  {
    "openclaw":
      {
        "emoji": "🎫",
      },
    "envVars":
      [
        {
          "name": "JIRA_API_TOKEN",
          "required": false,
          "description": "Needed for REST/curl fallback; not required for jira CLI or MCP backends",
        },
        {
          "name": "JIRA_USER",
          "required": false,
          "description": "Needed for REST/curl fallback; not required for jira CLI or MCP backends",
        },
        {
          "name": "JIRA_BASE_URL",
          "required": false,
          "description": "Needed for REST/curl fallback; not required for jira CLI or MCP backends",
        },
      ],
  }
---
# Jira

支持与Jira的自然语言交互，兼容多种后端。

## 后端检测

**请先运行此检查**，以确定应使用哪种后端：

```
1. Check if jira CLI is available:
   → Run: which jira
   → If found: USE CLI BACKEND

2. If no CLI, check for Atlassian MCP:
   → Look for mcp__atlassian__* tools
   → If available: USE MCP BACKEND

3. If neither available:
   → GUIDE USER TO SETUP
```

| 后端 | 使用场景 | 参考文档 |
|---------|-------------|-----------|
| **CLI** | 提供`jira`命令 | `references/commands.md` |
| **MCP** | 提供Atlassian MCP工具 | `references/mcp.md` |
| **无** | 两者均不可用 | 安装CLI的指南 |

---

## 快速参考（CLI）

> 如果使用MCP后端，请跳过本节。

| 操作 | 命令 |
|--------|---------|
| 查看问题 | `jira issue view ISSUE-KEY` |
| 列出我的问题 | `jira issue list -a$(jira me)` |
| 查看我正在进行中的问题 | `jira issue list -a$(jira me) -s"In Progress"` |
| 创建问题 | `jira issue create -tType -s"描述" -b"标题"` |
| 移动/转换问题状态 | `jira issue move ISSUE-KEY "状态"` |
| 分配给我 | `jira issue assign ISSUE-KEY $(jira me)` |
| 取消分配 | `jira issue assign ISSUE-KEY x` |
| 添加评论 | `jira issue comment add ISSUE-KEY -b"评论内容"` |
| 在浏览器中打开问题 | `jira open ISSUE-KEY` |
| 查看当前冲刺中的问题 | `jira sprint list --state active` |
| 查看我的信息 | `jira me` |

---

## 快速参考（MCP）

> 如果使用CLI后端，请跳过本节。

| 操作 | MCP工具 |  
|--------|----------|  
| 搜索问题 | `mcp__atlassian__searchJiraIssuesUsingJql` |
| 查看问题 | `mcp__atlassian__getJiraIssue` |
| 创建问题 | `mcp__atlassian__createJiraIssue` |
| 更新问题 | `mcp__atlassian__editJiraIssue` |
| 查看问题转换历史 | `mcp__atlassian__getTransitionsForJiraIssue` |
| 转换问题状态 | `mcp__atlassian__transitionJiraIssue` |
| 添加评论 | `mcp__atlassian__addCommentToJiraIssue` |
| 查找用户ID | `mcp__atlassian__lookupJiraAccountId` |
| 列出项目 | `mcp__atlassian__getVisibleJiraProjects` |

更多MCP操作方式请参阅`references/mcp.md`。

---

## 常用命令

- `create a jira ticket`（创建Jira工单）
- `show me PROJ-123`（显示PROJ-123项目中的所有工单）
- `list my tickets`（列出我的所有工单）
- `move ticket to done`（将工单状态改为“已完成”）
- `what's in the current sprint`（查看当前冲刺中的问题）

---

## 问题键的格式

问题键的格式为：`[A-Z]+-[0-9]+`（例如：PROJ-123、ABC-1）。

当用户在对话中提到问题键时：
- **CLI**：使用`jira issue view KEY`或`jira open KEY`命令
- **MCP**：使用`mcp__atlassian__jira_getIssue`命令并传入问题键

---

## 工作流程

**创建工单的步骤：**
1. 如果用户提到了代码、工单或拉取请求（PR），请先了解相关背景信息。
2. 起草工单内容。
3. 与用户共同审阅内容。
4. 使用相应的后端创建工单。

**更新工单的步骤：**
1. 首先获取工单详情。
2. 检查工单状态（特别注意正在进行中的工单）。
3. 显示当前状态与修改后的状态。
4. 在更新前获取批准。
5. 添加注释说明修改内容。

---

## 在执行任何操作之前，请问自己：

1. **当前工单的状态是什么？** —— 必须先获取工单的详细信息。不要假设工单的状态、分配者或字段与用户的认知一致。
2. **还有谁会受到影响？** —— 查看工单的关注者、关联问题以及父级任务。一个简单的修改可能会通知到多人。
3. **这个操作可以撤销吗？** —— 有些工作流程可能有单向的状态转换。描述内容的修改通常是不可撤销的。
4. **我使用的标识符正确吗？** —— 确保使用正确的问题键、转换ID和用户ID。在MCP系统中，显示名称无法用于分配工单。

---

**绝对禁止的行为：**

- **绝对禁止在未获取当前状态的情况下进行状态转换** —— 某些工作流程可能需要经过中间状态。例如，如果需要先将工单状态改为“进行中”，否则直接改为“已完成”可能会导致问题。
- **绝对禁止使用显示名称进行工单分配** —— 在MCP系统中，只能使用用户ID进行分配。必须先调用`lookupJiraAccountId`函数。
- **绝对禁止在未显示原始内容的情况下修改工单描述** —— Jira不支持撤销操作。用户必须清楚自己修改的内容。
- **绝对禁止在未填写所有必要字段的情况下使用`--no-input`选项（CLI）** —— 这会导致错误且无法正常执行操作。请先检查项目所需的字段。
- **绝对禁止在没有明确批准的情况下批量修改工单** —— 每次修改都会通知所有关注者。批量修改可能会导致大量通知。

---

## 安全注意事项：

- 在执行任何操作之前，务必显示相应的命令或工具调用方式。
- 在修改工单之前，务必获得批准。
- 修改工单时，请保留原始信息。
- 修改后，请验证更新内容是否正确。
- 如遇到认证问题，请及时向用户说明，以便他们能够解决问题。

---

**如果既没有CLI也没有MCP可用，请指导用户：**

```
To use Jira, you need one of:

1. **jira CLI** (recommended):
   https://github.com/ankitpokhrel/jira-cli

   Install: brew install ankitpokhrel/jira-cli/jira-cli
   Setup:   jira init

2. **Atlassian MCP**:
   Configure in your MCP settings with Atlassian credentials.
```

---

## 深入了解

**在以下情况下需要加载参考文档：**
- 创建包含复杂字段或多行内容的工单时。
- 构建复杂的JQL查询时。
- 解决错误或认证问题时。
- 处理工单状态转换、关联问题或冲刺管理相关操作时。

**以下情况下无需加载参考文档：**
- 简单的查看/列出工单的操作（请参考上面的快速参考）。
- 基本的状态查询（例如：`jira issue view KEY`）。
- 在浏览器中直接打开工单。

| 操作 | 是否需要加载参考文档？ |
|------|-----------------|
| 查看单个工单 | 不需要 |
| 列出我的工单 | 不需要 |
- 创建包含描述内容的工单 | **需要** —— CLI需要使用`/tmp`模式。
- 转换工单状态 | **需要** —— 需要知道转换ID。
- 使用JQL进行搜索 | **需要** —— 对于复杂的查询。
- 关联工单 | **需要** —— MCP系统有相关限制，可能需要脚本辅助。

**参考文档：**
- CLI操作方式：`references/commands.md`
- MCP操作方式：`references/mcp.md`