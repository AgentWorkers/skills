---
name: lark-all-in-one
description: OpenClaw的全面Feishu/Lark集成功能：支持消息传递、群组管理、Bitable（多维表格）功能、文档编辑、日历管理、视频会议（vc.v1）、会议记录（minutes.v1）、任务管理、审批流程、联系人管理、云盘同步以及Wiki/知识库功能。该功能需要配置并运行官方的Lark MCP服务器。
version: "3.1.0"
author: lucascheung
tags: [feishu, lark, messaging, bitable, calendar, vc, minutes, docs, tasks, approvals]
homepage: "https://github.com/lucascheung/lark_skill"
source: "https://github.com/lucascheung/lark_skill"
requires:
  env:
    - name: LARK_APP_ID
      description: "Your Feishu/Lark App ID from the Open Platform developer console (open.feishu.cn/app or open.larksuite.com/app)"
      sensitive: false
    - name: LARK_APP_SECRET
      description: "Your Feishu/Lark App Secret from the Open Platform developer console"
      sensitive: true
  mcp_servers:
    - name: lark-mcp
      package: "@larksuiteoapi/lark-mcp"
      source: "https://github.com/larksuite/lark-openapi-mcp"
      description: "Official Feishu/Lark OpenAPI MCP server"
      command: "npx"
      args: ["-y", "@larksuiteoapi/lark-mcp", "mcp", "-a", "$LARK_APP_ID", "-s", "$LARK_APP_SECRET"]
---
# Feishu / Lark 综合技能

## 前提条件
在使用此技能之前，必须确保官方的 Lark MCP 服务器正在运行。
**设置方式**：`npx -y @larksuiteoapi/lark-mcp mcp -a <APP_ID> -s <APP_SECRET>`
**对于用户身份 API（useUAT）**：首先运行 `npx -y @larksuiteoapi/lark-mcp login -a <APP_ID> -s <APP_SECRET>`
**要启用视频会议和会议记录 API，请添加以下参数**：`-t presetcalendar.default,vc.v1.reserve.apply,vc.v1.meeting.get,vc.v1.meetingRecording.get,minutes.v1.minute.get,minutes.v1.minuteTranscript.get,minutes.v1.minuteStatistic.get`
**完整文档**：https://open.larkoffice.com/document/home/index

---

## 核心概念

### 工具命名
所有 MCP 工具都使用前缀 `mcp__lark-mcp__`。示例：
```
mcp__lark-mcp__im.v1.message.create
```

### 身份类型
| 参数 | 值 | 含义 |
|-----------|-------|---------|
| `useUAT` | `true` | 以登录用户的身份操作 — 资源归用户所有，可直接访问 |
| `useUAT` | `false`（默认） | 以应用程序/机器人的身份操作 — 资源归应用程序所有 |

对于大多数交互式操作，请使用 `useUAT: true`。对于后台自动化操作，请使用 `useUAT: false`。

### 标准参数结构
```yaml
path:      # URL path parameters (IDs, tokens)
params:    # Query string parameters (pagination, filters, id_type)
data:      # Request body payload
useUAT:    # true = user identity, false = app identity
```

### 常见 ID 类型
| ID | 格式 | 表示的内容 |
|----|--------|-----------|
| `app_token` | `appXXX` | Bitable 应用程序 |
| `table_id` | `tblXXX` | Bitable 表格 |
| `record_id` | `recXXX` | Bitable 记录 |
| `open_id` | `ou_XXX` | 用户（OpenID） |
| `union_id` | `on_XXX` | 用户（UnionID，跨应用程序） |
| `chat_id` | `oc_XXX` | 组/私信聊天 |
| `message_id` | `om_XXX` | 单个消息 |
| `document_id` | `doxcXXX` | 文档 |
| `file_token` | 变动 | Drive 文件 |
| `node_token` | 变动 | Wiki 节点 |
| `event_uid` | 变动 | 日历事件 |
| `task_guid` | 变动 | 任务 |
| `approval_code` | 变动 | 审批定义 |

---

## 1. 消息传递（IM）

### 发送消息
**工具**：`mcp__lark-mcp__im.v1.message.create`
```yaml
params:
  receive_id_type: "chat_id"   # or: open_id, union_id, email, user_id
data:
  receive_id: "oc_xxx"
  msg_type: "text"             # text | post | image | interactive | file | audio | media | sticker | share_chat | share_user
  content: '{"text":"Hello!"}'
useUAT: true
```

**消息类型和内容格式**：
- `text`：`{"text": "Hello @user"}`
- `post`（富文本）：`{"zh_cn": {"title": "标题", "content": [[{"tag":"text","text":"正文"}]]}}`
- `interactive`（卡片）：JSON 卡片定义 — 请使用 https://open.larkoffice.com/cardkit 创建卡片 |
- `image`：`{"image_key": "img_xxx"`（首先通过 Drive 上传图片）
- `share_chat`：`{"chat_id": "oc_xxx"}`

### 回复消息
**工具**：`mcp__lark-mcp__im.v1.message.reply`
```yaml
path:
  message_id: "om_xxx"
data:
  content: '{"text":"Got it!"}'
  msg_type: "text"
  reply_in_thread: false   # true = create/continue a thread
useUAT: true
```

### 列出聊天中的消息
**工具**：`mcp__lark-mcp__im.v1.message.list`
```yaml
params:
  container_id_type: "chat"
  container_id: "oc_xxx"
  page_size: 20
  sort_type: "ByCreateTimeDesc"
  start_time: "1700000000"   # optional Unix timestamp
  end_time: "1700100000"     # optional Unix timestamp
```

### 获取单条消息
**工具**：`mcp__lark-mcp__im.v1.message.get`
```yaml
path:
  message_id: "om_xxx"
```

### 删除消息
**工具**：`mcp__lark-mcp__im.v1.message.delete`
```yaml
path:
  message_id: "om_xxx"
useUAT: true
```

### 更新/编辑消息（卡片或文本）
**工具**：`mcp__lark-mcp__im.v1.message.update`
```yaml
path:
  message_id: "om_xxx"
data:
  msg_type: "interactive"
  content: '{"config":{},"elements":[...]}'
useUAT: true
```

### 添加消息反应（表情符号）
**工具**：`mcp__lark-mcp__im.v1.messageReaction.create`
```yaml
path:
  message_id: "om_xxx"
data:
  reaction_type:
    emoji_type: "THUMBSUP"   # THUMBSUP, OK, HEART, etc.
useUAT: true
```

### 列出消息反应
**工具**：`mcp__lark-mcp__im.v1.messageReaction.list`
```yaml
path:
  message_id: "om_xxx"
params:
  reaction_type: "THUMBSUP"   # optional filter
```

### 固定/取消固定消息
**工具**：`mcp__lark-mcp__im.v1.pin.create` / `mcp__lark-mcp__im.v1.pin.delete`
```yaml
data:
  message_id: "om_xxx"
  chat_id: "oc_xxx"
useUAT: true
```

### 查看消息阅读记录（谁已阅读）
**工具**：`mcp__lark-mcp__im.v1.message.readUsers`
```yaml
path:
  message_id: "om_xxx"
params:
  user_id_type: "open_id"
  page_size: 50
```

---

## 2. 组/聊天管理

### 列出机器人所在的所有聊天
**工具**：`mcp__lark-mcp__im.v1.chat.list`
```yaml
params:
  user_id_type: "open_id"
  page_size: 20
```

### 列出用户所在的聊天
**工具**：`mcp__lark-mcp__im.v1.chat.list`
```yaml
params:
  user_id_type: "open_id"
  page_size: 20
useUAT: true
```

### 获取聊天信息
**工具**：`mcp__lark-mcp__im.v1.chat.get`
```yaml
path:
  chat_id: "oc_xxx"
params:
  user_id_type: "open_id"
```

### 创建群组聊天
**工具**：`mcp__lark-mcp__im.v1.chat.create`
```yaml
data:
  name: "Project Alpha"
  description: "Discuss Project Alpha here"
  owner_id: "ou_xxx"           # optional, defaults to app/user
  user_id_list: ["ou_xxx", "ou_yyy"]
  bot_id_list: []
  chat_mode: "group"
  chat_type: "private"         # private | public
  external: false
useUAT: true
```

### 更新群组信息
**工具**：`mcp__lark-mcp__im.v1.chat.update`
```yaml
path:
  chat_id: "oc_xxx"
data:
  name: "New Name"
  description: "Updated description"
  owner_id: "ou_xxx"           # transfer ownership
  add_member_permission: "all_members"
  at_all_permission: "all_members"
  edit_permission: "all_members"
useUAT: true
```

### 解散群组
**工具**：`mcp__lark-mcp__im.v1.chat.delete`
```yaml
path:
  chat_id: "oc_xxx"
useUAT: true
```

### 列出聊天成员
**工具**：`mcp__lark-mcp__im.v1.chatMembers.get`
```yaml
path:
  chat_id: "oc_xxx"
params:
  member_id_type: "open_id"
  page_size: 50
```

### 向聊天中添加成员
**工具**：`mcp__lark-mcp__im.v1.chatMembers.create`
```yaml
path:
  chat_id: "oc_xxx"
params:
  member_id_type: "open_id"
data:
  id_list: ["ou_xxx", "ou_yyy"]
useUAT: true
```

### 从聊天中移除成员
**工具**：`mcp__lark-mcp__im.v1.chatMembers.delete`
```yaml
path:
  chat_id: "oc_xxx"
params:
  member_id_type: "open_id"
data:
  id_list: ["ou_xxx"]
useUAT: true
```

### 搜索公共聊天
**工具**：`mcp__lark-mcp__im.v1.chat.search`
```yaml
params:
  query: "design team"
  page_size: 20
useUAT: true
```

### 列出聊天标签
**工具**：`mcp__lark-mcp__im.v1.chatTab.listTabs`
```yaml
path:
  chat_id: "oc_xxx"
```

### 获取聊天公告
**工具**：`mcp__lark-mcp__im.v1.chatAnnouncement.get`
```yaml
path:
  chat_id: "oc_xxx"
params:
  user_id_type: "open_id"
```

### 更新聊天公告
**工具**：`mcp__lark-mcp__im.v1.chatAnnouncement.patch`
```yaml
path:
  chat_id: "oc_xxx"
data:
  revision_id: 1
  requests: ['{"requestType":"InsertBlocksAtDocumentTail","insertBlocksAtDocumentTailRequest":{"payload":{"blocks":[{"blockType":2,"text":{"elements":[{"textRun":{"content":"New announcement"}}],"style":{}}}]}}}']
useUAT: true
```

---

## 3. Bitable（多维表格/基础）

### 创建 Bitable 应用程序
**工具**：`mcp__lark-mcp__bitable.v1.app.create`
```yaml
data:
  name: "Project Tracker"
  folder_token: ""   # optional: Drive folder to place it in
useUAT: true
```

### 获取 Bitable 应用程序信息
**工具**：`mcp__lark-mcp__bitable.v1.app.get`
```yaml
path:
  app_token: "appXXX"
```

### 更新 Bitable 应用程序
**工具**：`mcp__lark-mcp__bitable.v1.app.update`
```yaml
path:
  app_token: "appXXX"
data:
  name: "New Name"
  is_advanced: true   # enable advanced features
useUAT: true
```

### 列出 Bitable 应用程序中的表格
**工具**：`mcp__lark-mcp__bitable.v1.appTable.list`
```yaml
path:
  app_token: "appXXX"
params:
  page_size: 20
```

### 创建表格
**工具**：`mcp__lark-mcp__bitable.v1.appTable.create`
```yaml
path:
  app_token: "appXXX"
data:
  table:
    name: "Tasks"
    default_view_name: "Grid View"
    fields:
      - field_name: "Task Name"
        type: 1   # 1=text, 2=number, 3=single-select, 4=multi-select, 5=date, 7=checkbox, 11=person, 15=url, 99001=phone
      - field_name: "Status"
        type: 3
        property:
          options:
            - name: "To Do"
              color: 0
            - name: "In Progress"
              color: 1
            - name: "Done"
              color: 2
      - field_name: "Assignee"
        type: 11
      - field_name: "Due Date"
        type: 5
useUAT: true
```

### 删除表格
**工具**：`mcp__lark-mcp__bitable.v1.appTable.delete`
```yaml
path:
  app_token: "appXXX"
  table_id: "tblXXX"
useUAT: true
```

### 列出表格中的字段
**工具**：`mcp__lark-mcp__bitable.v1.appTableField.list`
```yaml
path:
  app_token: "appXXX"
  table_id: "tblXXX"
params:
  page_size: 50
  view_id: ""   # optional: filter by view
```

### 创建字段
**工具**：`mcp__lark-mcp__bitable.v1.appTableField.create`
```yaml
path:
  app_token: "appXXX"
  table_id: "tblXXX"
data:
  field_name: "Priority"
  type: 3   # single-select
  property:
    options:
      - name: "High"
        color: 0
      - name: "Medium"
        color: 1
      - name: "Low"
        color: 2
useUAT: true
```

### 更新字段
**工具**：`mcp__lark-mcp__bitable.v1.appTableField.update`
```yaml
path:
  app_token: "appXXX"
  table_id: "tblXXX"
  field_id: "fldXXX"
data:
  field_name: "Renamed Field"
  property:
    options:
      - name: "Critical"
        color: 0
useUAT: true
```

### 删除字段
**工具**：`mcp__lark-mcp__bitable.v1.appTableField.delete`
```yaml
path:
  app_token: "appXXX"
  table_id: "tblXXX"
  field_id: "fldXXX"
useUAT: true
```

### 搜索/列出记录
**工具**：`mcp__lark-mcp__bitable.v1.appTableRecord.search`
```yaml
path:
  app_token: "appXXX"
  table_id: "tblXXX"
params:
  user_id_type: "open_id"
  page_size: 100
  page_token: ""   # for pagination
data:
  view_id: ""   # optional
  field_names: ["Task Name", "Status", "Assignee"]   # optional: only return these fields
  sort:
    - field_name: "Due Date"
      desc: false
  filter:
    conjunction: "and"   # and | or
    conditions:
      - field_name: "Status"
        operator: "is"   # is | isNot | contains | doesNotContain | isEmpty | isNotEmpty | isGreater | isLess
        value: ["In Progress"]
  automatic_fields: false
useUAT: true
```

### 获取单条记录
**工具**：`mcp__lark-mcp__bitable.v1.appTableRecord.get`
```yaml
path:
  app_token: "appXXX"
  table_id: "tblXXX"
  record_id: "recXXX"
params:
  user_id_type: "open_id"
```

### 创建记录
**工具**：`mcp__lark-mcp__bitable.v1.appTableRecord.create`
```yaml
path:
  app_token: "appXXX"
  table_id: "tblXXX"
params:
  user_id_type: "open_id"
data:
  fields:
    "Task Name": "Fix login bug"
    "Status": "To Do"
    "Assignee": [{"id": "ou_xxx"}]
    "Due Date": 1700000000000   # milliseconds timestamp
useUAT: true
```

### 批量创建记录
**工具**：`mcp__lark-mcp__bitable.v1.appTableRecord.batchCreate`
```yaml
path:
  app_token: "appXXX"
  table_id: "tblXXX"
params:
  user_id_type: "open_id"
data:
  records:
    - fields:
        "Task Name": "Task 1"
        "Status": "To Do"
    - fields:
        "Task Name": "Task 2"
        "Status": "In Progress"
useUAT: true
```

### 更新记录
**工具**：`mcp__lark-mcp__bitable.v1.appTableRecord.update`
```yaml
path:
  app_token: "appXXX"
  table_id: "tblXXX"
  record_id: "recXXX"
params:
  user_id_type: "open_id"
data:
  fields:
    "Status": "Done"
useUAT: true
```

### 批量更新记录
**工具**：`mcp__lark-mcp__bitable.v1.appTableRecord.batchUpdate`
```yaml
path:
  app_token: "appXXX"
  table_id: "tblXXX"
params:
  user_id_type: "open_id"
data:
  records:
    - record_id: "recXXX"
      fields:
        "Status": "Done"
    - record_id: "recYYY"
      fields:
        "Status": "In Progress"
useUAT: true
```

### 删除记录
**工具**：`mcp__lark-mcp__bitable.v1.appTableRecord.delete`
```yaml
path:
  app_token: "appXXX"
  table_id: "tblXXX"
  record_id: "recXXX"
useUAT: true
```

### 批量删除记录
**工具**：`mcp__lark-mcp__bitable.v1.appTableRecord.batchDelete`
```yaml
path:
  app_token: "appXXX"
  table_id: "tblXXX"
data:
  records: ["recXXX", "recYYY"]
useUAT: true
```

### 列出视图
**工具**：`mcp__lark-mcp__bitable.v1.appTableView.list`
```yaml
path:
  app_token: "appXXX"
  table_id: "tblXXX"
params:
  page_size: 20
```

### 创建视图
**工具**：`mcp__lark-mcp__bitable.v1.appTableView.create`
```yaml
path:
  app_token: "appXXX"
  table_id: "tblXXX"
data:
  view_name: "Kanban"
  view_type: "kanban"   # grid | kanban | gallery | gantt | form
useUAT: true
```

### 管理 Bitable 合作者
**工具**：`mcp__lark-mcp__bitable.v1.appRoleMember.create`
```yaml
path:
  app_token: "appXXX"
  role_id: "roleXXX"
data:
  member_id: "ou_xxx"
  member_id_type: "open_id"
useUAT: true
```

---

## 4. 文档（Docs）

### 搜索文档
**工具**：`mcp__lark-mcp__drive.v1.file.search`（或 `docx.builtin.search`)
```yaml
params:
  query: "Q4 report"
  page_size: 20
useUAT: true
```

### 获取文档内容（纯文本）
**工具**：`mcp__lark-mcp__docx.v1.document.rawContent`
```yaml
path:
  document_id: "doxcXXX"
params:
  lang: 0   # 0=default
useUAT: true
```

### 获取文档元数据
**工具**：`mcp__lark-mcp__docx.v1.document.get`
```yaml
path:
  document_id: "doxcXXX"
useUAT: true
```

### 创建新文档
**工具**：`mcp__lark-mcp__docx.v1.document.create`
```yaml
data:
  folder_token: ""   # optional: Drive folder
  title: "Meeting Notes - 2026-03-06"
useUAT: true
```

### 列出文档块
**工具**：`mcp__lark-mcp__docx.v1.documentBlock.list`
```yaml
path:
  document_id: "doxcXXX"
params:
  page_size: 50
  document_revision_id: -1   # -1 = latest
useUAT: true
```

### 更新文档块（插入内容）
**工具**：`mcp__lark-mcp__docx.v1.documentBlockChildren.batchUpdate`
```yaml
path:
  document_id: "doxcXXX"
  block_id: "doxcXXX"   # parent block (document root = document_id)
data:
  requests:
    - insertBlocksAfterBlockRequest:
        targetBlockId: "blockXXX"
        payload:
          blocks:
            - blockType: 2   # 2=text, 3=heading1, 4=heading2, 12=bullet, 22=code
              text:
                elements:
                  - textRun:
                      content: "New paragraph content"
  revision_id: -1   # -1 = latest
useUAT: true
```

---

## 5. 云盘（Drive）

### 列出根目录或文件夹中的文件
**工具**：`mcp__lark-mcp__drive.v1.file.list`
```yaml
params:
  folder_token: ""   # empty = root ("My Drive")
  page_size: 20
  order_by: "EditedTime"   # EditedTime | CreatedTime | Name
  direction: "DESC"
useUAT: true
```

### 创建文件夹
**工具**：`mcp__lark-mcp__drive.v1.file.createFolder`
```yaml
data:
  name: "Q1 Reports"
  folder_token: ""   # parent folder, empty = root
useUAT: true
```

### 移动文件
**工具**：`mcp__lark-mcp__drive.v1.file.move`
```yaml
path:
  file_token: "xxx"
data:
  type: "doc"   # doc | sheet | bitable | mindnote | file | wiki | docx
  folder_token: "targetFolderToken"
useUAT: true
```

### 复制文件
**工具**：`mcp__lark-mcp__drive.v1.file.copy`
```yaml
path:
  file_token: "xxx"
data:
  name: "Copy of Report"
  type: "docx"
  folder_token: "targetFolderToken"
useUAT: true
```

### 删除文件
**工具**：`mcp__lark-mcp__drive.v1.file.delete`
```yaml
path:
  file_token: "xxx"
params:
  type: "docx"
useUAT: true
```

### 获取文件统计信息
**工具**：`mcp__lark-mcp__drive.v1.fileStatistics.get`
```yaml
path:
  file_token: "xxx"
  file_type: "docx"   # docx | sheet | bitable | file
```

### 管理文件权限（添加协作者）
**工具**：`mcp__lark-mcp__drive.v1.permissionMember.create`
```yaml
path:
  token: "xxx"
  type: "docx"
data:
  member_type: "openid"   # openid | unionid | email | opendepartmentid | groupid
  member_id: "ou_xxx"
  perm: "view"   # view | edit | full_access
useUAT: true
```

### 列出文件协作者
**工具**：`mcp__lark-mcp__drive.v1.permissionMember.list`
```yaml
path:
  token: "xxx"
  type: "docx"
useUAT: true
```

### 获取文件评论
**工具**：`mcp__lark-mcp__drive.v1.fileComment.list`
```yaml
path:
  file_token: "xxx"
  file_type: "docx"
params:
  is_solved: false
  page_size: 20
useUAT: true
```

### 添加文件评论
**工具**：`mcp__lark-mcp__drive.v1.fileComment.create`
```yaml
path:
  file_token: "xxx"
  file_type: "docx"
data:
  reply_list:
    replies:
      - content:
          elements:
            - type: "text_run"
              text_run:
                text: "Great work on this section!"
useUAT: true
```

---

## 6. 日历

### 列出所有日历
**工具**：`mcp__lark-mcp__calendar.v4calendar.list`
```yaml
params:
  page_size: 20
useUAT: true
```

### 获取主日历
**工具**：`mcp__lark-mcp__calendar.v4calendar.primary`
```yaml
params:
  user_id_type: "open_id"
useUAT: true
```

### 创建日历
**工具**：`mcp__lark-mcp__calendar.v4calendar.create`
```yaml
data:
  summary: "Team Calendar"
  description: "Shared team schedule"
  permissions: "public"   # private | show_only_free_busy | public
  color: -1
  summary_alias: ""
useUAT: true
```

### 列出事件
**工具**：`mcp__lark-mcp__calendar.v4calendarEvent.list`
```yaml
path:
  calendar_id: "primary"   # or specific calendar ID
params:
  start_time: "1700000000"
  end_time: "1702600000"
  page_size: 50
useUAT: true
```

### 获取日历事件
**工具**：`mcp__lark-mcp__calendar.v4calendarEvent.get`
```yaml
path:
  calendar_id: "primary"
  event_id: "xxx"
params:
  user_id_type: "open_id"
useUAT: true
```

### 创建日历事件
**工具**：`mcp__lark-mcp__calendar.v4calendarEvent.create`
```yaml
path:
  calendar_id: "primary"
data:
  summary: "Team Standup"
  description: "Daily sync"
  start_time:
    timestamp: "1700000000"
    timezone: "Asia/Shanghai"
  end_time:
    timestamp: "1700003600"
    timezone: "Asia/Shanghai"
  attendees:
    - type: "user"
      user_id: "ou_xxx"
  need_notification: true
  visibility: "default"   # default | public | private
  free_busy_status: "busy"   # busy | free
  color: -1
  reminders:
    - minutes: 10
  recurrence_rule: ""   # e.g. "FREQ=DAILY;COUNT=5" for recurring events
useUAT: true
```

### 更新日历事件
**工具**：`mcp__lark-mcp__calendar.v4calendarEvent.patch`
```yaml
path:
  calendar_id: "primary"
  event_id: "xxx"
data:
  summary: "Updated Meeting Title"
  description: "Updated description"
useUAT: true
```

### 删除日历事件
**工具**：`mcp__lark-mcp__calendar.v4calendarEvent.delete`
```yaml
path:
  calendar_id: "primary"
  event_id: "xxx"
params:
  need_notification: true
useUAT: true
```

### 列出事件参与者
**工具**：`mcp__lark-mcp__calendar.v4calendarEventAttendee.list`
```yaml
path:
  calendar_id: "primary"
  event_id: "xxx"
params:
  user_id_type: "open_id"
  page_size: 50
useUAT: true
```

### 向事件添加参与者
**工具**：`mcp__lark-mcp__calendar.v4calendarEventAttendee.create`
```yaml
path:
  calendar_id: "primary"
  event_id: "xxx"
data:
  attendees:
    - type: "user"
      user_id: "ou_xxx"
  need_notification: true
useUAT: true
```

### 获取用户的空闲/忙碌状态
**工具**：`mcp__lark-mcp__calendar.v4.freebusy.list`
```yaml
data:
  time_min: "2026-03-06T09:00:00+08:00"
  time_max: "2026-03-06T18:00:00+08:00"
  user_id_list: ["ou_xxx", "ou_yyy"]
useUAT: true
```

---

## 7. 任务

### 列出任务
**工具**：`mcp__lark-mcp__task.v2.task.list`
```yaml
params:
  completed: false
  type: "my"   # my | created | assigned
  page_size: 50
useUAT: true
```

### 获取任务
**工具**：`mcp__lark-mcp__task.v2.task.get`
```yaml
path:
  task_guid: "xxx"
params:
  user_id_type: "open_id"
useUAT: true
```

### 创建任务
**工具**：`mcp__lark-mcp__task.v2.task.create`
```yaml
params:
  user_id_type: "open_id"
data:
  summary: "Write Q4 report"
  description: "Compile all metrics and write the Q4 summary report"
  due:
    timestamp: "1700000000000"   # milliseconds
    is_all_day: false
  origin:
    platform_i18n_name: '{"zh_cn":"来自OpenClaw","en_us":"From OpenClaw"}'
  members:
    - id: "ou_xxx"
      type: "user"
      role: "assignee"   # assignee | follower
  task_list_configs:
    - tasklist_guid: "tsklistXXX"   # optional: add to a task list
  repeat_rule: ""   # e.g. "FREQ=WEEKLY;BYDAY=MO" for recurring
useUAT: true
```

### 更新任务
**工具**：`mcp__lark-mcp__task.v2.task.patch`
```yaml
path:
  task_guid: "xxx"
params:
  user_id_type: "open_id"
data:
  task:
    summary: "Updated task name"
    due:
      timestamp: "1700100000000"
  update_fields: ["summary", "due"]   # specify which fields to update
useUAT: true
```

### 完成任务
**工具**：`mcp__lark-mcp__task.v2.task.complete`
```yaml
path:
  task_guid: "xxx"
useUAT: true
```

### 取消任务
**工具**：`mcp__lark-mcp__task.v2.task.uncomplete`
```yaml
path:
  task_guid: "xxx"
useUAT: true
```

### 删除任务
**工具**：`mcp__lark-mcp__task.v2.task.delete`
```yaml
path:
  task_guid: "xxx"
useUAT: true
```

### 添加任务评论
**工具**：`mcp__lark-mcp__task.v2.taskComment.create`
```yaml
path:
  task_guid: "xxx"
data:
  content: "Progress update: 80% complete"
  reply_to_comment_id: ""   # optional
useUAT: true
```

### 列出任务评论
**工具**：`mcp__lark-mcp__task.v2.taskComment.list`
```yaml
path:
  task_guid: "xxx"
params:
  page_size: 20
useUAT: true
```

### 列出任务列表
**工具**：`mcp__lark-mcp__task.v2.tasklist.list`
```yaml
params:
  user_id_type: "open_id"
  page_size: 20
useUAT: true
```

### 将任务添加到任务列表
**工具**：`mcp__lark-mcp__task.v2.task.addTasklist`
```yaml
path:
  task_guid: "xxx"
data:
  tasklist_guid: "tsklistXXX"
  section_guid: ""   # optional: specific section
useUAT: true
```

---

## 8. 联系人（用户和部门）

### 通过 Open ID 获取用户
**工具**：`mcp__lark-mcp__contact.v3.user.get`
```yaml
path:
  user_id: "ou_xxx"
params:
  user_id_type: "open_id"
useUAT: true
```

### 通过电子邮件或电话批量获取用户
**工具**：`mcp__lark-mcp__contact.v3.user.batchGetId`
```yaml
params:
  user_id_type: "open_id"
data:
  emails: ["user@company.com"]
  mobiles: ["+8613800000000"]
useUAT: true
```

### 搜索用户
**工具**：`mcp__lark-mcp__contact.v3.user.findByDepartment`
```yaml
params:
  user_id_type: "open_id"
  department_id_type: "open_department_id"
  department_id: "od_xxx"
  page_size: 50
useUAT: true
```

### 获取当前用户信息
**工具**：`mcp__lark-mcp__authen.v1.userInfo.get`
```yaml
useUAT: true
```

### 列出部门
**工具**：`mcp__lark-mcp__contact.v3.department.children`
```yaml
params:
  department_id_type: "open_department_id"
  parent_department_id: "0"   # "0" = root
  page_size: 50
  fetch_child: false
useUAT: true
```

### 获取部门信息
**工具**：`mcp__lark-mcp__contact.v3.department.get`
```yaml
path:
  department_id: "od_xxx"
params:
  department_id_type: "open_department_id"
  user_id_type: "open_id"
useUAT: true
```

---

## 9. Wiki / 知识库

### 列出 Wiki 空间
**工具**：`mcp__lark-mcp__wiki.v2.space.list`
```yaml
params:
  page_size: 20
useUAT: true
```

### 获取 Wiki 空间信息
**工具**：`mcp__lark-mcp__wiki.v2.space.get`
```yaml
path:
  space_id: "xxx"
useUAT: true
```

### 列出 Wiki 节点
**工具**：`mcp__lark-mcp__wiki.v2.spaceNode.list`
```yaml
path:
  space_id: "xxx"
params:
  parent_node_token: ""   # empty = root level
  page_size: 50
useUAT: true
```

### 搜索 Wiki
**工具**：`mcp__lark-mcp__wiki.v2.spaceNode.search`
```yaml
path:
  space_id: "xxx"
params:
  keyword: "onboarding guide"
  page_size: 20
useUAT: true
```

### 获取 Wiki 节点信息
**工具**：`mcp__lark-mcp__wiki.v2.spaceNode.get`
```yaml
params:
  token: "wikcXXX"
useUAT: true
```

### 创建 Wiki 节点（新建页面）
**工具**：`mcp__lark-mcp__wiki.v2.spaceNode.create`
```yaml
path:
  space_id: "xxx"
data:
  node_type: "origin"   # origin = new doc; copy = copy existing
  parent_node_token: "wikcXXX"   # parent page token
  title: "New Page Title"
useUAT: true
```

### 移动 Wiki 节点
**工具**：`mcp__lark-mcp__wiki.v2.spaceNode.move`
```yaml
path:
  space_id: "xxx"
  node_token: "wikcXXX"
data:
  target_parent_token: "wikcYYY"
  target_space_id: ""   # empty = same space
useUAT: true
```

---

## 10. 审批工作流

### 获取审批定义
**工具**：`mcp__lark-mcp__approval.v4.approval.get`
```yaml
path:
  approval_code: "xxx"
params:
  locale: "zh-CN"   # zh-CN | en-US | ja-JP
```

### 创建审批实例（提交审批）
**工具**：`mcp__lark-mcp__approval.v4.instance.create`
```yaml
data:
  approval_code: "xxx"
  open_id: "ou_xxx"   # submitter
  form: '[{"id":"widget1","type":"input","value":"Expense claim for $500"}]'
  node_approver_open_id_list: []   # optional: specify approvers per node
useUAT: true
```

### 获取审批实例
**工具**：`mcp__lark-mcp__approval.v4.instance.get`
```yaml
path:
  instance_id: "xxx"
params:
  locale: "zh-CN"
  user_id: "ou_xxx"
  user_id_type: "open_id"
useUAT: true
```

### 列出审批实例
**工具**：`mcp__lark-mcp__approval.v4.instance.list`
```yaml
params:
  approval_code: "xxx"
  start_time: "1700000000000"
  end_time: "1702600000000"
  page_size: 100
```

### 批准审批实例
**工具**：`mcp__lark-mcp__approval.v4.instance.approve`
```yaml
data:
  approval_code: "xxx"
  instance_code: "xxx"
  user_id: "ou_xxx"
  task_id: "xxx"
  comment: "Looks good, approved!"
useUAT: true
```

### 拒绝审批实例
**工具**：`mcp__lark-mcp__approval.v4.instance.reject`
```yaml
data:
  approval_code: "xxx"
  instance_code: "xxx"
  user_id: "ou_xxx"
  task_id: "xxx"
  comment: "Please revise the budget figures"
useUAT: true
```

### 取消审批实例
**工具**：`mcp__lark-mcp__approval.v4.instance.cancel`
```yaml
data:
  approval_code: "xxx"
  instance_code: "xxx"
  user_id: "ou_xxx"
useUAT: true
```

### 向审批实例添加评论
**工具**：`mcp__lark-mcp__approval.v4.instanceComment.create`
```yaml
path:
  instance_id: "xxx"
data:
  content: "Please check the attached receipts"
  at_info_list:
    - user_id: "ou_xxx"
      name: "John"
      offset: "14"
useUAT: true
```

---

## 11. 常见工作流

### 工作流：查找用户并发送私信
```
1. mcp__lark-mcp__contact.v3.user.batchGetId
   → emails: ["user@company.com"] → get open_id

2. mcp__lark-mcp__im.v1.message.create
   → receive_id_type: "open_id"
   → receive_id: <open_id from step 1>
   → send the message
```

### 工作流：创建 Bitable 表格并从数据中填充内容
```
1. mcp__lark-mcp__bitable.v1.app.create → get app_token
2. mcp__lark-mcp__bitable.v1.appTable.create → define schema → get table_id
3. mcp__lark-mcp__bitable.v1.appTableRecord.batchCreate → insert records (up to 500 per call)
```

### 工作流：向群组发送每周报告
```
1. mcp__lark-mcp__bitable.v1.appTableRecord.search
   → filter: Status = "Done", Due Date in last 7 days
   → collect completed items

2. Format into rich-text post or interactive card

3. mcp__lark-mcp__im.v1.message.create
   → msg_type: "post" or "interactive"
   → send to project group chat_id
```

### 工作流：安排会议并检查空闲/忙碌状态
```
1. mcp__lark-mcp__calendar.v4.freebusy.list
   → check availability of all attendees in target window

2. Pick a free slot

3. mcp__lark-mcp__calendar.v4.calendarEvent.create
   → add all attendees, set reminders

4. mcp__lark-mcp__im.v1.message.create
   → notify attendees with meeting details
```

### 工作流：提交并跟踪审批
```
1. mcp__lark-mcp__approval.v4.approval.get → inspect form fields

2. mcp__lark-mcp__approval.v4.instance.create
   → fill form data, submit

3. mcp__lark-mcp__approval.v4.instance.get
   → poll for status: PENDING | APPROVED | REJECTED | CANCELED
```

### 工作流：创建任务并分配
```
1. mcp__lark-mcp__contact.v3.user.batchGetId → resolve assignee email → open_id

2. mcp__lark-mcp__task.v2.task.create
   → summary, description, due date, members with role "assignee"

3. Optionally: mcp__lark-mcp__im.v1.message.create
   → notify assignee via DM
```

---

## 12. 错误参考

| 错误代码 | 含义 | 解决方案 |
|------------|---------|-----|
| `99991663` | 令牌过期 | 重新登录或刷新令牌 |
| `99991664` | 无效令牌 | 检查应用程序凭据 |
| `99991400` | 权限被拒绝 | 在开发者控制台中授予所需的权限范围 |
| `230001` | 机器人未在聊天中 | 先将机器人添加到群组 |
| `1254502` | 记录未找到 | 验证 record_id 是否正确 |
| `1254520` | 字段未找到 | 确保 field_name 的拼写准确 |
| `1300006` | 事件未找到 | 验证 event_id 和 calendar_id |
| `1100003` | 会议未找到 | 会议可能已经结束或 reserve_id 不正确 |
| `1100007` | 会议不活跃 | 先使用 `reserve.get` 检查状态 |
| `11000032` | 非会议主持人 | 只有主持人可以执行此操作 |
| `1700001` | 会议记录未找到 | 检查 minute_token 的格式（`obcn...`） |
| `1700002` | 会议记录未准备好 | 转录仍在处理中，稍后重试 |

### 常见问题
- **“工具未找到”**：MCP 服务器未运行。请使用 `npx -y @larksuiteoapi/lark-mcp mcp -a <APP_ID> -s <APP_SECRET>` 启动它 |
- **资源无法访问**：使用 `useUAT: true` — 由机器人创建的资源可能对用户不可见 |
- **权限错误**：在 Feishu Open Platform 控制台中启用所需的权限范围（例如 `bitable:app`, `im:message`, `calendar:calendar`, `task:task:write`） |
- **message_id 未找到**：消息可能已过期，或者需要 `im:message:send_as_bot` 权限范围 |
- **user_access_token 过期**：运行 `npx -y @larksuiteoapi/lark-mcp login` 以刷新令牌（有效期 2 小时，可以使用 offline_access 权限范围刷新）

---

## 13. 视频会议（vc.v1）

> **注意**：视频会议 API 需要 `vc:meeting` 权限范围，并且通常需要 `useUAT: true`（用户身份）。可以通过在 lark-mcp 中添加 `-t vc.v1.*` 来启用这些功能。

### 预订/安排会议
**工具**：`mcp__lark-mcp__vc.v1.reserve.apply`
**返回值**：`reserve_id`, `reserve_token` — 保存这些值以管理预订。
**工具**：`mcp__lark-mcp__vc.v1.reserve.update`
**工具**：`mcp__lark-mcp__vc.v1.reserve.delete`
**工具**：`mcp__lark-mcp__vc.v1.reserve.get`
**工具**：`mcp__lark-mcp__vc.v1.activeMeeting`
**工具**：`mcp__lark-mcp__vc.v1.meeting.get`
**工具**：`mcp__lark-mcp__vc.v1.meeting.listByNo`
**工具**：`mcp__lark-mcp__vc.v1.meeting.invite`
**工具**：`mcp__lark-mcp__vc.v1.meeting.kickout`
**工具**：`mcp__lark-mcp__vc.v1.meeting.setHost`
**工具**：`mcp__lark-mcp__vc.v1.meeting.end`
**工具**：`mcp__lark-mcp__vc.v1.participant.list`
**工具**：`mcp__lark-mcp__vc.v1.meetingRecording.get`
**工具**：`mcp__lark-mcp__vc.v1.meetingRecording.setPermission`
**工具**：`mcp__lark-mcp__vc.v1.export.meetingList`
**工具**：`mcp__lark-mcp__vc.v1.export.participantList`
**工具**：`mcp__lark-mcp__vc.v1.room.get`
**工具**：`mcp__lark-mcp__vc.v1.room.list`
**工具**：`mcp__lark-mcp__vc.v1.create`

---

## 14. 会议记录（minutes.v1）

> Feishu Minutes（妙记）是基于 AI 的会议转录和笔记产品。
> **注意**：会议记录 API 需要 `minutes:minute:readonly` 权限范围。目前只能通过 API 进行读取（没有写入端点）。
> 会议记录是从视频会议录像或上传的音频/视频文件自动生成的。

### 获取会议记录元数据
**工具**：`mcp__lark-mcp__minutes.v1.minute.get`
**返回值**：标题、时长、所有者、创建时间、视频状态、转录状态。

### 获取会议记录文本
**工具**：`mcp__lark-mcp__minutes.v1.minuteTranscript.get`
**返回值**：包含以下内容的转录片段数组：
- `start_time` / `end_time`（毫秒）
- `paragraph` — 说话的内容
- `speaker_id`, `speaker_name` — 说话者

### 获取会议记录的统计信息/参与者
**工具**：`mcp__lark-mcp__minutes.v1.minuteStatistic.get`
**返回值**：包含发言时间和单词计数的参与者列表。

### 获取会议记录的音频/视频文件（仅元数据）
**工具**：`mcp__lark-mcp__minutes.v1.minuteMedia.get`
**返回值**：原始录制的下载 URL。
> ⚠️ lark-mcp 直接不支持文件下载/上传。请使用该 URL 进行外部流媒体播放/访问。

### 如何获取 minute_token
会议记录的 token 可以从以下位置获取：
1. 会议录像中 — 会议结束后显示的 Minutes URL
2. 日历事件中（包含在事件详细信息中）
3. 格式：`obcn` 后跟字母数字字符（例如 `obcn6qGKMiZy0eNFSKl6e8XXXXX`

### 工作流：向群组发送会议总结
**工具**：`mcp__lark-mcp__`

---

## 15. 高级群组聊天工作流

本节涵盖了超出基本 CRUD 操作的群组聊天场景。

### 按名称查找群组
**工具**：`mcp__lark-mcp__`

### 向群组发送 @mention 消息
**工具**：`mcp__lark-mcp__`

### 向群组发送交互式卡片
**工具**：`mcp__lark-mcp__`

### 使用机器人和成员创建专用项目群组
**工具**：`mcp__lark-mcp__`

### 设置群组公告
**工具**：`mcp__lark-mcp__`

### 监控群组消息（事件驱动）
> 在 Feishu Open Platform 中注册 `im.message.receive_v1` 事件，以接收
> 机器人所在群组中发送的所有消息。OpenClaw 的 Feishu 组件会自动处理这些消息——无需轮询。
事件负载包括：`message_id`, `chat_id`, `sender.open_id`, `message.content`, `message.msg_type`

### 向多个群组批量通知
**工具**：`mcp__lark-mcp__`

### 在群组中转发特定消息
**工具**：`mcp__lark-mcp__`

### 转发消息到另一个聊天
**工具**：`mcp__lark-mcp__`

### 获取用户的未读消息
**工具**：`mcp__lark-mcp__`

### 转移群组所有权
**工具**：`mcp__lark-mcp__`

### 在视频会议后向群组发送会议笔记
**工具**：`mcp__lark-mcp__`

---

## 16. 所需的应用程序权限参考

| 功能 | 所需权限范围 |
|---------|----------------|
| 发送消息 | `im:message` |
| 阅读消息 | `im:message:readonly` |
| 群组管理 | `im:chat`, `im:chat:write` |
| 转发消息 | `im:message` |
| Bitable（阅读） | `bitable:app:readonly` |
| Bitable（写入） | `bitable:app` |
| 文档（阅读） | `docs:doc:readonly` |
| 文档（写入） | `docs:doc` |
| 云盘 | `drive:drive` |
| 日历（阅读） | `calendar:calendar:readonly` |
| 日历（写入） | `calendar:calendar` |
| 任务 | `task:task:write` |
| 联系人 | `contact:user.base:readonly` |
| Wiki | `wiki:wiki:readonly` |
| 审批 | `approval:approval:readonly`, `approval:instance` |
| **视频会议（预订/管理）** | `vc:meeting` |
| **视频会议（参与者）** | `vc:meeting:readonly` |
| **视频会议（记录）** | `vc:record` |
| **视频会议（会议室）** | `vc:room:readonly` |
| **视频会议（导出报告）** | `vc:export` |
| **会议记录（阅读）** | `minutes:minute:readonly` |