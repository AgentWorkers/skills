---
name: basecamp-cli
description: Basecamp 4 的 CLI（命令行接口）和 MCP（管理控制台）服务器：当您需要与 Basecamp 项目、待办事项、消息、日程安排、看板卡片或团队讨论记录进行交互时，可以使用这些工具。该系统提供了 76 种基于人工智能的项目管理工具，以支持自动化的工作流程。
mcp: true
metadata: {"openclaw":{"emoji":"🏕️","homepage":"https://github.com/drkraft/basecamp-cli","primaryEnv":"BASECAMP_CLIENT_SECRET","requires":{"bins":["basecamp-mcp"],"env":["BASECAMP_CLIENT_ID","BASECAMP_CLIENT_SECRET"]},"install":[{"id":"npm","kind":"node","package":"@drkraft/basecamp-cli","bins":["basecamp","basecamp-mcp"],"label":"Install @drkraft/basecamp-cli (npm)","global":true}]}}
---

# Basecamp CLI

这是一个功能齐全的命令行工具（CLI）和MCP（Management Console）服务器，用于与Basecamp 4的API进行交互。

## 主要特性

- **21个CLI命令组**：覆盖了Basecamp 4的所有核心功能领域。
- **76个MCP工具**：支持与AI助手的集成。
- 支持自动分页和重试机制（采用指数级退避策略）。
- 使用PKCE（Proof Key Exchange）进行OAuth 2.0身份验证。

## 安装

```bash
npm install -g @drkraft/basecamp-cli
```

## 系统要求

- 必须安装Node.js版本20或更高。

## 身份验证设置

1. 在[https://launchpad.37signals.com/integrations](https://launchpad.37signals.com/integrations)创建一个OAuth应用程序。
   - 将重定向URI设置为`http://localhost:9292/callback`。
2. 配置应用程序的认证信息：
```bash
basecamp auth configure --client-id <your-client-id>
export BASECAMP_CLIENT_SECRET="<your-client-secret>"
export BASECAMP_CLIENT_ID="<your-client-id>"
```
3. 登录到Basecamp：
```bash
basecamp auth login
```

## MCP服务器配置

将以下配置添加到您的MCP配置文件中（例如：`~/.config/claude/claude_desktop_config.json`）：

```json
{
  "mcpServers": {
    "basecamp": {
      "command": "basecamp-mcp",
      "env": {
        "BASECAMP_CLIENT_ID": "<your-client-id>",
        "BASECAMP_CLIENT_SECRET": "<your-client-secret>"
      }
    }
  }
}
```

## 可用的MCP工具（共76个）

| 功能类别 | 工具名称          |
|---------|-----------------|
| 项目        | `basecamp_list_projects`, `basecamp_get_project`, `basecamp_create_project`, `basecamp_archive_project` |
| 待办事项列表 | `basecamp_list_todolists`, `basecamp_get_todolist`, `basecamp_create_todolist`, `basecamp_delete_todolist` |
| 待办事项组    | `basecamp_list_todolist_groups`, `basecamp_create_todolist_group` |
| 待办事项      | `basecamp_list_todos`, `basecamp_get_todo`, `basecamp_create_todo`, `basecamp_update_todo`, `basecamp_complete_todo`, `basecamp_uncomplete_todo`, `basecamp_delete_todo`, `basecamp_move_todo` |
| 消息        | `basecamp_list_messages`, `basecamp_get_message`, `basecamp_create_message` |
| 人员        | `basecamp_list_people`, `basecamp_get_person`, `basecamp_get_me` |
| 评论        | `basecamp_list_comments`, `basecamp_get_comment`, `basecamp_create_comment`, `basecamp_update_comment`, `basecamp_delete_comment` |
| 保险箱       | `basecamp_list_vaults`, `basecamp_get_vault`, `basecamp_create_vault`, `basecamp_update_vault` |
| 文档        | `basecamp_list_documents`, `basecamp_get_document`, `basecamp_create_document`, `basecamp_update_document` |
| 上传        | `basecamp_list_uploads`, `basecamp_get_upload`, `basecamp_create_upload`, `basecamp_update_upload` |
| 日程        | `basecamp_get_schedule`, `basecamp_list_schedule_entries`, `basecamp_get_schedule_entry`, `basecamp_create_schedule_entry`, `basecamp_update_schedule_entry`, `basecamp_delete_schedule_entry` |
| 卡片表       | `basecamp_get_card_table`, `basecamp_get_column`, `basecamp_create_column`, `basecamp_update_column`, `basecamp_delete_column`, `basecamp_list_cards`, `basecamp_get_card`, `basecamp_create_card`, `basecamp_update_card`, `basecamp_move_card`, `basecamp_delete_card` |
| 搜索        | `basecamp_search`         |
| 录音        | `basecamp_list_recordings`, `basecamp_archive_recording`, `basecamp_restore_recording`, `basecamp_trash_recording` |
| 订阅        | `basecamp_list_subscriptions`, `basecamp_subscribe`, `basecamp_unsubscribe` |
| Webhook     | `basecamp_list_webhooks`, `basecamp_get_webhook`, `basecamp_create_webhook`, `basecamp_update_webhook`, `basecamp_delete_webhook`, `basecamp_test_webhook` |
| 活动        | `basecamp_list_events`        |
| 火炬活动     | `basecamp_list_campfires`, `basecamp_get_campfire_lines`, `basecamp_send_campfire_line` |

## CLI快速参考

```bash
# Projects
basecamp projects list
basecamp projects get <id>

# Todos
basecamp todolists list --project <id>
basecamp todos list --project <id> --list <list-id>
basecamp todos create --project <id> --list <list-id> --content "Task"
basecamp todos complete <id> --project <id>
basecamp todos delete <id> --project <id>
basecamp todos move <id> --project <id> --list <target-list-id>

# Messages
basecamp messages list --project <id>
basecamp messages create --project <id> --subject "Title" --content "<p>Body</p>"

# Kanban
basecamp cardtables get --project <id>
basecamp cardtables cards --project <id> --column <col-id>
basecamp cardtables create-card --project <id> --column <col-id> --title "Card"

# Search
basecamp search "keyword"
basecamp search "keyword" --type Todo --project <id>
```

所有CLI命令都支持`--format json`选项，用于输出JSON格式的结果。

## 链接

- [完整文档](https://github.com/drkraft/basecamp-cli)
- [npm包](https://www.npmjs.com/package/@drkraft/basecamp-cli)
- [Basecamp API参考文档](https://github.com/basecamp/bc3-api)