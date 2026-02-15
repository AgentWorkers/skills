---
name: apple-mail
description: 在 macOS 上，可以通过 `osascript` 脚本来读取和操作 Apple Mail 的内容。以下是该脚本的一些主要用途：  
1. 列出所有邮件账户；  
2. 查看某个账户下的所有邮箱/文件夹；  
3. 从指定的邮箱中获取邮件内容；  
4. 阅读邮件的具体内容。  
该脚本仅适用于 macOS 上的 Apple Mail 应用程序。
metadata: {"moltbot":{"emoji":"📧","os":["darwin"],"requires":{"bins":["osascript"]}}}
---

# Apple Mail 技能

## 概述

该技能允许通过 AppleScript (osascript) 与 macOS 上的 Apple Mail 进行交互。它提供了列出账户、浏览邮箱、检索邮件列表以及阅读完整邮件内容的功能。

## 先决条件

- 安装并配置了 macOS 系统和 Apple Mail 应用程序。
- 在 Apple Mail 中至少设置了一个邮件账户。
- 使用该技能时，Apple Mail 必须处于运行状态。

## 快速入门

### 列出可用账户

```bash
python3 {baseDir}/scripts/list_accounts.py
```

### 列出某个账户的邮箱

```bash
python3 {baseDir}/scripts/list_mailboxes.py "Account Name"
```

### 从邮箱中获取邮件

```bash
# Get 10 most recent messages (default)
python3 {baseDir}/scripts/get_messages.py "Account Name" "INBOX"

# Get specific number of messages
python3 {baseDir}/scripts/get_messages.py "Account Name" "INBOX" --limit 20
```

### 阅读完整邮件内容

```bash
python3 {baseDir}/scripts/get_message_content.py "MESSAGE_ID"
```

## 常见工作流程

### 工作流程 1：浏览邮件

1. 列出所有可用的账户。
2. 选择一个账户并查看其邮箱。
3. 从指定的邮箱中获取邮件。
4. 阅读特定邮件的完整内容。

### 工作流程 2：搜索特定邮件

1. 从目标邮箱中获取指定数量的邮件。
2. 查看邮件的主题和发件人。
3. 找到感兴趣的邮件 ID。
4. 阅读相关邮件的完整内容。

## 脚本参考

### `list_accounts.py`

列出 Apple Mail 中所有已配置的邮件账户。

**输出格式：** 账户名称的 JSON 数组
```json
{
  "accounts": ["iCloud", "Gmail", "Work"],
  "count": 3
}
```

### `list_mailboxes.py <account_name>`

列出特定账户的所有邮箱（文件夹）。

**参数：**
- `account_name`：邮件账户的名称（来自 list_accounts.py）

**输出格式：** 邮箱名称的 JSON 数组
```json
{
  "account": "iCloud",
  "mailboxes": ["INBOX", "Sent", "Drafts", "Trash", "Archive"],
  "count": 5
}
```

### `get_messages.py <account_name> <mailbox_name> [--limit N]`

从指定的邮箱中检索邮件列表。

**参数：**
- `account_name`：邮件账户的名称。
- `mailbox_name`：邮箱的名称（例如：“INBOX”、“Sent”）。
- `--limit N`：可选参数，指定要检索的邮件数量上限（默认值：10）。

**输出格式：** 包含邮件元数据的 JSON 数组
```json
{
  "account": "iCloud",
  "mailbox": "INBOX",
  "messages": [
    {
      "id": "123456",
      "subject": "Meeting Tomorrow",
      "sender": "colleague@example.com",
      "date_sent": "Monday, January 27, 2026 at 10:30:00 AM",
      "date_received": "Monday, January 27, 2026 at 10:30:05 AM",
      "read_status": false,
      "message_size": 2048
    }
  ],
  "count": 1
}
```

### `get_message_content.py <message_id>`

检索特定邮件的完整内容。

**参数：**
- `message_id`：来自 get_messages.py 的邮件 ID。

**输出格式：** 包含邮件详细信息的 JSON 对象

## 常见使用模式

### 模式 1：查找未读邮件

1. 从 INBOX 中获取邮件。
2. 筛选 `read_status` 为 `false` 的邮件。
3. 阅读未读邮件的内容。

### 模式 2：查看已发送的邮件

1. 列出所有标记为 “Sent” 的邮箱。
2. 从已发送的邮箱中获取邮件。
3. 查看最近发送的邮件。

### 模式 3：搜索多个邮箱

1. 列出该账户的所有邮箱。
2. 遍历感兴趣的邮箱。
3. 从每个邮箱中获取邮件。
4. 整合并展示结果。

## 错误处理

所有脚本都会以统一的格式输出错误信息：

```json
{
  "error": "Error description",
  "details": "Additional context if available"
}
```

常见错误：
- **Apple Mail 未运行**：请启动 Mail 应用程序。
- **账户名称无效**：请检查拼写，账户名称区分大小写。
- **邮箱名称无效**：请使用 `list_mailboxes.py` 中提供的准确名称。
- **邮件未找到**：邮件可能已被删除或移动。

## 重要说明

- **区分大小写**：账户名称和邮箱名称均区分大小写。
- **必须运行 Mail 应用程序**：所有脚本都需要 Apple Mail 处于打开状态。
- **权限**：首次使用时，系统可能会在系统偏好设置中请求自动化权限。
- **性能**：大型邮箱的查询可能需要更多时间；使用 `--limit` 参数来限制查询结果的数量。
- **邮件 ID**：邮件 ID 是永久性的，除非邮件被删除。

## 限制

- 仅适用于 macOS。
- 仅支持 Apple Mail，不支持其他邮件客户端。
- 仅支持读取操作，无法发送或删除邮件。
- 无法修改邮件属性（如标记、文件夹等）。
- 仅能访问直接隶属于账户的邮箱，嵌套文件夹可能无法访问。