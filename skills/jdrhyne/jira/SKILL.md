---
name: jira
description: **使用场景：**  
当用户提及 Jira 问题（例如：“PROJ-123”）、询问工单详情、希望创建/查看/更新问题、检查冲刺进度或管理 Jira 工作流程时，该功能会被触发。它会响应包含以下关键词的输入：“jira”、“issue”、“ticket”、“sprint”、“backlog” 或问题键（issue key）的指令。
metadata:
  {
    "openclaw":
      {
        "emoji": "🎫",
        "requires":
          {
            "anyBins": ["jira"],
            "env": ["JIRA_API_TOKEN"],
          },
      },
  }
---

# Jira

支持与 Jira 的自然语言交互，兼容多种后端。

## 后端检测

**请先运行此检查** 以确定应使用哪种后端：

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
| **CLI** | 提供 `jira` 命令 | `references/commands.md` |
| **MCP** | 提供 Atlassian MCP 工具 | `references/mcp.md` |
| **无** | 两者均不可用 | 安装 CLI 的指南 |

---

## 快速参考（CLI）

> 如果使用 MCP 后端，请跳过本节。

| 操作 | 命令 |
|--------|---------|
| 查看问题 | `jira issue view ISSUE-KEY` |
| 列出我的问题 | `jira issue list -a$(jira me)` |
| 查看我的进行中的问题 | `jira issue list -a$(jira me) -s"In Progress"` |
| 创建问题 | `jira issue create -tType -s"Summary" -b"Description"` |
| 移动/转换问题状态 | `jira issue move ISSUE-KEY "State"` |
| 分配给我 | `jira issue assign ISSUE-KEY $(jira me)` |
| 取消分配 | `jira issue assign ISSUE-KEY x` |
| 添加评论 | `jira issue comment add ISSUE-KEY -b"Comment text"` |
| 在浏览器中打开问题 | `jira open ISSUE-KEY` |
| 查看当前冲刺中的问题 | `jira sprint list --state active` |
| 查看我的信息 | `jira me` |

---

## 快速参考（MCP）

> 如果使用 CLI 后端，请跳过本节。

| 操作 | MCP 工具 |
|--------|----------|
| 搜索问题 | `mcp__atlassian__searchJiraIssuesUsingJql` |
| 查看问题 | `mcp__atlassian__getJiraIssue` |
| 创建问题 | `mcp__atlassian__createJiraIssue` |
| 更新问题 | `mcp__atlassian__editJiraIssue` |
| 查看问题状态转换记录 | `mcp__atlassian__getTransitionsForJiraIssue` |
| 转换问题状态 | `mcp__atlassian__transitionJiraIssue` |
| 向问题添加评论 | `mcp__atlassian__addCommentToJiraIssue` |
| 查找用户 ID | `mcp__atlassian__lookupJiraAccountId` |
| 列出项目 | `mcp__atlassian__getVisibleJiraProjects` |

更多 MCP 命令模式请参阅 `references/mcp.md`。

---

## 常用命令

- `create a jira ticket` （创建 Jira 问题）
- `show me PROJ-123` （显示项目 PROJ-123 的信息）
- `list my tickets` （列出我的问题）
- `move ticket to done` （将问题状态改为“已完成”）
- `what's in the current sprint` （查看当前冲刺中的问题）

---

## 问题键的格式

问题键的格式为：`[A-Z]+-[0-9]+`（例如：PROJ-123、ABC-1）。

当用户在对话中提到问题键时：
- **CLI**：使用 `jira issue view KEY` 或 `jira open KEY`
- **MCP**：使用 `mcp__atlassian__jira_get_issue` 并传入问题键

---

## 工作流程

**创建问题时：**
1. 如果用户提到了代码、问题或 Pull Request（PR），请先了解相关背景信息。
2. 起草问题内容。
3. 与用户一起审核问题内容。
4. 使用相应后端创建问题。

**更新问题时：**
1. 首先获取问题详情。
2. 检查问题状态（特别注意进行中的问题）。
3. 显示更改内容与原始内容。
4. 在更新前获取批准。
5. 添加注释说明更改内容。

---

## 在执行任何操作前，请问自己：

1. **问题的当前状态是什么？** —— 必须先获取问题的最新状态。不要假设问题的状态、分配者或字段与用户所想的一致。
2. **还有谁会受到影响？** —— 查看问题的关注者、关联的问题以及父级任务。一个简单的编辑操作可能会通知到多人。
3. **这个操作可以撤销吗？** —— 有些工作流程不允许撤销操作。某些状态转换可能是单向的。描述内容的修改无法撤销。
4. **我使用的标识符正确吗？** —— 确保使用正确的问题键、状态转换 ID 和用户 ID。在 MCP 环境中，显示名称无法用于分配问题。

---

**绝对禁止的操作：**

- **在没有获取当前状态的情况下进行状态转换** —— 有些工作流程要求问题必须处于特定状态才能转换。例如，如果问题必须先处于“进行中”状态才能转换为“已完成”，否则操作会失败。
- **在 MCP 环境中不能使用显示名称进行问题分配** —— 只能使用用户 ID 进行分配。必须先调用 `lookupJiraAccountId`，否则分配操作会失败。
- **在未显示原始内容的情况下修改问题描述** —— Jira 不支持撤销操作。用户必须清楚自己修改的内容。
- **在使用 CLI 时，如果没有提供所有必需的字段，绝对不要使用 `--no-input` 选项** —— 这会导致错误且无法察觉。请先检查项目所需的字段。
- **不要假设状态转换的名称是通用的** —— 不同项目对“已完成”、“关闭”或“完成”的定义可能不同。请先确认可用的状态转换选项。
- **在没有明确批准的情况下不要批量修改问题** —— 每次修改问题都会通知所有关注者。批量修改会导致大量通知。

---

## 安全注意事项：

- 在执行任何操作前，务必显示相应的命令或工具调用信息。
- 在修改问题之前，务必获得批准。
- 修改问题时请保留原始信息。
- 更新问题后，请验证结果的正确性。
- 如遇到认证问题，请及时向用户反馈，以便他们能够解决问题。

---

**如果无法使用任何后端**

如果既无法使用 CLI 也无法使用 MCP，请为用户提供相应的指导：

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

## 深入使用建议

**在以下情况下请加载参考文档：**
- 创建包含复杂字段或多行内容的问题。
- 构建复杂的 JQL 查询。
- 解决错误或认证问题。
- 处理状态转换、问题链接或冲刺相关操作。

**以下情况无需加载参考文档：**
- 简单的查看/列出问题操作（快速参考已足够使用）。
- 基本的状态查询（例如：`jira issue view KEY`）。
- 在浏览器中打开问题。

| 操作 | 是否需要加载参考文档？ |
|------|-----------------|
| 查看单个问题 | 不需要 |
| 列出我的问题 | 不需要 |
- 带有描述的问题创建操作 | **需要** —— CLI 需要 `/tmp` 模式。
- 转换问题状态 | **需要** —— 需要使用状态转换 ID。
- 使用 JQL 进行搜索 | **需要** —— 对于复杂的查询。
- 链接问题 | **需要** —— MCP 有相关限制，可能需要脚本辅助。

参考文档：
- CLI 命令模式：`references/commands.md`
- MCP 命令模式：`references/mcp.md`