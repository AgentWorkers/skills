---
name: ez-google
description: **使用场景：**  
当需要发送电子邮件、查看收件箱、阅读邮件、查看日历、安排会议、创建事件、搜索 Google Drive 内容、创建 Google 文档、读取或编辑电子表格、查找联系人，或执行任何与 Gmail、Google 日历、Drive、Docs、Sheets、Slides 或 Contacts 相关的任务时均可使用。该工具支持托管式 OAuth 认证，无需手动配置 API 密钥，对代理（agent）非常友好。
metadata: {"openclaw":{"emoji":"📧"}}
---

# ez-google

专为代理（Agent）设计的 Google Workspace 工具。使用托管的 OAuth 进行简单操作——用户只需点击链接并复制返回的令牌即可。无需 API 密钥或凭据。

**运行所有命令的格式：** `uv run scripts/<script>.py <command> [args]`

## 认证（请先执行此步骤）

```bash
auth.py status        # Check: AUTHENTICATED or NOT_AUTHENTICATED
auth.py login         # Get URL → send to user
auth.py save '<TOKEN>'  # Save token from hosted OAuth
```

**认证流程：** `status` → 如果未认证 → `login` → 用户点击链接并复制令牌 → `save '<TOKEN>'`

---

## Gmail

```bash
gmail.py list [-n 10] [-q "query"]   # List emails
gmail.py search "query"              # Search emails
gmail.py get MESSAGE_ID              # Read email
gmail.py send "to" "subject" "body"  # Send email
gmail.py draft "to" "subject" "body" # Create draft
gmail.py labels                      # List labels

# Bulk operations (up to 1000 messages per API call)
gmail.py bulk-label "query" --add LABEL --remove LABEL  # Add/remove labels
gmail.py bulk-trash "query" [-y]     # Move to trash (use -y to skip confirmation)
```

**批量操作示例：**
```bash
gmail.py bulk-label "from:newsletter@example.com" --add ARCHIVE --remove INBOX
gmail.py bulk-trash "subject:alert older_than:30d" -y
gmail.py bulk-label "category:promotions" --add Label_3  # Use label IDs from `labels`
```

## 日历（Calendar）

```bash
gcal.py list [DATE]                  # List events (DATE: YYYY-MM-DD or "today")
gcal.py create "title" "START" "END" # Create event (START/END: YYYY-MM-DDTHH:MM)
gcal.py get EVENT_ID                 # Event details
gcal.py delete EVENT_ID              # Delete event
gcal.py calendars                    # List calendars
```

## 驱动器（Drive）

```bash
drive.py list [-n 20]                # List files
drive.py search "query"              # Search by name
drive.py get FILE_ID                 # File metadata
drive.py download FILE_ID            # File content
drive.py create-folder "name"        # Create folder
```

## 文档（Docs）

```bash
docs.py create "title"               # Create doc
docs.py get DOC_ID                   # Read content
docs.py find "query"                 # Find by title
docs.py append DOC_ID "text"         # Append text
docs.py insert DOC_ID "text"         # Insert at start
docs.py replace DOC_ID "old" "new"   # Replace text
```

## 表格（Sheets）

```bash
sheets.py create "title"             # Create spreadsheet
sheets.py get ID "Sheet!A1:D10"      # Read data
sheets.py info ID                    # Sheet metadata
sheets.py find "query"               # Find by name
sheets.py write ID "Sheet!A1" "a,b;c,d"   # Write (rows separated by ;)
sheets.py append ID "Sheet!A:B" "a,b;c,d" # Append rows
```

## 幻灯片（Slides）

```bash
slides.py find "query"               # Find presentations
slides.py get PRESENTATION_ID        # Get slides info
slides.py text PRESENTATION_ID       # Extract all text
slides.py create "title"             # Create presentation
```

## 人员/联系人（People/Contacts）

```bash
people.py me                         # Current user profile
people.py contacts [-n 100]          # List contacts
people.py search "name"              # Search contacts
people.py get CONTACT_ID             # Contact details
```

## 聊天（仅限 Workspace）

```bash
chat.py spaces                       # List spaces
chat.py messages SPACE_ID [-n 20]    # List messages
chat.py send SPACE_ID "text"         # Send message
chat.py get SPACE_ID                 # Space details
```

---

注意：添加新服务后，请先运行 `auth.py logout`，然后再运行 `login` 以授予新的权限。