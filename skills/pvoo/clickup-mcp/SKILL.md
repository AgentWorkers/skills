---
name: clickup-mcp
description: 通过官方的MCP工具来管理ClickUp任务、文档、时间跟踪记录、评论、聊天记录以及进行搜索。使用前需要完成OAuth身份验证。
homepage: https://clickup.com
metadata: {"clawdbot":{"emoji":"✅","requires":{"bins":["mcporter"],"env":["CLICKUP_TOKEN"]}}}
---

# ClickUp MCP（官方）

通过官方的MCP服务器访问ClickUp。支持完整的工作空间搜索、任务管理、时间跟踪、评论、聊天和文档功能。

## 设置

### 选项1：直接使用OAuth（仅限支持的应用程序）

ClickUp MCP仅允许来自**允许列表中的应用程序**的OAuth登录：
- Claude Desktop、Claude Code、Cursor、VS Code、Windsurf、ChatGPT

```bash
# Claude Code
claude mcp add clickup --transport http https://mcp.clickup.com/mcp
# Then /mcp in session to authorize
```

### 选项2：使用Claude Code通过mcporter进行登录（推荐）

1. **步骤1：通过Claude Code进行授权**
```bash
claude mcp add clickup --transport http https://mcp.clickup.com/mcp
claude
# In Claude Code, run: /mcp
# Complete OAuth in browser
```

2. **步骤2：提取token**
```bash
jq -r '.mcpOAuth | to_entries | .[] | select(.key | startswith("clickup")) | .value.accessToken' ~/.claude/.credentials.json
```

3. **步骤3：将token添加到环境变量中**
```bash
# Add to ~/.clawdbot/.env
CLICKUP_TOKEN=eyJhbGciOiJkaXIi...
```

4. **步骤4：配置mcporter**
   在`config/mcporter.json`文件中进行配置：
```json
{
  "mcpServers": {
    "clickup": {
      "baseUrl": "https://mcp.clickup.com/mcp",
      "description": "Official ClickUp MCP",
      "headers": {
        "Authorization": "Bearer ${CLICKUP_TOKEN}"
      }
    }
  }
}
```

5. **步骤5：测试**
```bash
mcporter list clickup
mcporter call 'clickup.clickup_search(keywords: "test", count: 3)'
```

### Token刷新

Token的有效期较长（约10年）。如果token过期：
1. 在Claude Code中重新运行`/mcp`命令。
2. 从`~/.claude/.credentials.json`文件中重新提取token。
3. 更新`.env`文件中的`CLICKUP_TOKEN`变量。

## 可用的工具（32个）

### 搜索

| 工具 | 描述 |
|------|-------------|
| `clickup_search` | 在任务、文档、仪表板、聊天和文件中进行全局搜索 |

### 任务

| 工具 | 描述 |
|------|-------------|
| `clickup_create_task` | 创建任务，设置名称、描述、状态、分配者、截止日期和优先级 |
| `clickup_get_task` | 获取任务详情（包括子任务） |
| `clickup_update_task` | 更新任务的任何字段 |
| `clickup.attach_task_file` | 为任务附加文件（URL或Base64编码的形式） |
| `clickup_add_tag_to_task` | 为任务添加标签 |
| `clickup_remove_tag_from_task` | 从任务中删除标签 |

### 评论

| 工具 | 描述 |
|------|-------------|
| `clickup_get_task_comments` | 获取任务的所有评论 |
| `clickup_create_task_comment` | 添加评论（支持@提及功能） |

### 时间跟踪

| 工具 | 描述 |
|------|-------------|
| `clickup_start_time_tracking` | 为任务启动计时器 |
| `clickup_stop_time_tracking` | 停止计时器 |
| `clickup_add_time_entry` | 手动记录时间 |
| `clickup_get_task_time_entries` | 获取任务的时间记录 |
| `clickup_get_current_time_entry` | 查看当前任务的计时状态 |

### 工作空间与层级结构

| 工具 | 描述 |
|------|-------------|
| `clickup_get_workspace_hierarchy` | 获取工作空间的完整结构（包括空间、文件夹和列表） |
| `clickup_create_list` | 在空间中创建列表 |
| `clickup_create_list_in_folder` | 在文件夹中创建列表 |
| `clickup_get_list` | 获取列表详情 |
| `clickup_update_list` | 更新列表设置 |
| `clickup_create_folder` | 在空间中创建文件夹 |
| `clickup_get_folder` | 获取文件夹详情 |
| `clickup_update_folder` | 更新文件夹设置 |

### 成员

| 工具 | 描述 |
|------|-------------|
| `clickup_get_workspace_members` | 列出所有工作空间成员 |
| `clickup_find_member_by_name` | 通过名称或电子邮件查找成员 |
| `clickup.resolve_assignees` | 根据名称获取用户ID |

### 聊天

| 工具 | 描述 |
|------|-------------|
| `clickup_get_chat_channels` | 列出所有聊天频道 |
| `clickup_send_chat_message` | 向聊天频道发送消息 |

### 文档

| 工具 | 描述 |
|------|-------------|
| `clickup_create_document` | 创建新文档 |
| `clickup_list_document_pages` | 获取文档的页面结构 |
| `clickup_get_document_pages` | 获取文档页面的内容 |
| `clickup_create_document_page` | 为文档添加页面 |
| `clickup_update_document_page` | 编辑文档页面的内容 |

## 使用示例

### 搜索工作空间

```bash
mcporter call 'clickup.clickup_search(
  keywords: "Q4 marketing",
  count: 10
)'
```

### 创建任务

```bash
mcporter call 'clickup.clickup_create_task(
  name: "Review PR #42",
  list_id: "901506994423",
  description: "Check the new feature",
  status: "to do"
)'
```

### 更新任务

```bash
mcporter call 'clickup.clickup_update_task(
  task_id: "abc123",
  status: "in progress"
)'
```

### 添加评论

```bash
mcporter call 'clickup.clickup_create_task_comment(
  task_id: "abc123",
  comment_text: "@Mark can you review this?"
)'
```

### 时间跟踪

```bash
# Start timer
mcporter call 'clickup.clickup_start_time_tracking(
  task_id: "abc123",
  description: "Working on feature"
)'

# Stop timer
mcporter call 'clickup.clickup_stop_time_tracking()'

# Log time manually (duration in ms, e.g., 2h = 7200000)
mcporter call 'clickup.clickup_add_time_entry(
  task_id: "abc123",
  start: "2026-01-06 10:00",
  duration: "2h",
  description: "Code review"
)'
```

### 获取工作空间结构

```bash
mcporter call 'clickup.clickup_get_workspace_hierarchy(limit: 10)'
```

### 聊天

```bash
# List channels
mcporter call 'clickup.clickup_get_chat_channels()'

# Send message
mcporter call 'clickup.clickup_send_chat_message(
  channel_id: "channel-123",
  content: "Team standup in 5 minutes!"
)'
```

## 限制

- **无法执行删除操作** — 为安全考虑，建议使用ClickUp的UI界面。
- **没有自定义字段** — 官方MCP不支持自定义字段。
- **无法管理文档视图** — 目前不提供相关功能。
- **需要使用OAuth登录** — 必须使用允许列表中的应用程序（可以使用Claude Code作为替代方案）。
- **有请求速率限制** — 与ClickUp API的请求速率限制相同（约100次/分钟）。

## 资源

- [ClickUp MCP文档](https://developer.clickup.com/docs/connect-an-ai-assistant-to-clickups-mcp-server)
- [支持的工具](https://developer.clickup.com/docs/mcp-tools)
- [ClickUp API参考](https://clickup.com/api)
- [反馈/申请加入允许列表](https://feedback.clickup.com)