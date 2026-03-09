---
name: powerskills-outlook
description: 通过 COM（Component Object Model）实现 Outlook 邮件和日历的自动化操作。可以读取收件箱、未读邮件、已发送邮件；搜索邮件；发送、回复邮件；创建邮件草稿；列出日历事件和邮件文件夹。适用于需要查看工作邮件、发送/接收 Outlook 消息、搜索邮件或查看日历的场景。要求在 Windows 系统上安装 Outlook 桌面应用程序。
license: MIT
metadata:
  author: aloth
  cli: powerskills
  parent: powerskills
---
# PowerSkills — Outlook

用于处理电子邮件和日历的 Outlook COM 自动化功能。

## 要求

- 安装了 Microsoft Outlook（桌面版，支持 COM 接口）
- 使用非管理员权限的 PowerShell 会话（管理员权限无法访问用户的 Outlook 配置文件）

## 可用操作

```powershell
.\powerskills.ps1 outlook <action> [--params]
```

| 操作          | 参数          | 描述                                      |
|------------------|--------------|-----------------------------------------|
| `inbox`         | `--limit N`      | 列出收件箱中的邮件（默认值：15 条）                   |
| `unread`        | `--limit N`      | 列出未读邮件（默认值：20 条）                   |
| `sent`         | `--limit N`      | 列出已发送的邮件（默认值：15 条）                   |
| `read`         | `--index N`      | 根据索引读取邮件内容（例如：`inbox\|sent\|drafts`）         |
| `search`        | `--query "text"`    | 按主题或正文内容搜索邮件（默认值：7 天内的邮件）         |
| `calendar`       | `--days N`      | 列出即将发生的事件（默认值：7 天内的事件）             |
| `send`         | `--to addr`      | 发送邮件（可选参数：`--subject text`、`--body text`、`--cc addr`）   |
| `reply`         | `--index N`      | 回复收件箱中的邮件（可选参数：`--body text`、`--reply-all`）     |
| `folders`       |             | 列出所有邮件文件夹及其包含的邮件数量                 |

## 使用示例

```powershell
# Check unread mail
.\powerskills.ps1 outlook unread --limit 5

# Read a specific email
.\powerskills.ps1 outlook read --index 0 --folder inbox

# Read from sent folder
.\powerskills.ps1 outlook read --index 3 --folder sent

# Search for emails
.\powerskills.ps1 outlook search --query "project update" --limit 10

# Save a reply as draft
.\powerskills.ps1 outlook reply --index 0 --body "Thanks, will review." --draft

# Check calendar for next 3 days
.\powerskills.ps1 outlook calendar --days 3
```

## 输出字段

### 列出操作的结果（收件箱、未读邮件、已发送邮件）
- `index`：邮件在收件箱中的索引位置
- `subject`：邮件主题
- `sender`：邮件发送者
- `sender_email`：邮件发送者的电子邮件地址
- `received`：邮件接收时间
- `unread`：邮件是否未读
- `importance`：邮件的重要性等级
- `hasattachments`：邮件是否包含附件

### 读取邮件的结果
- `subject`：邮件主题
- `sender`：邮件发送者
- `sender_email`：邮件发送者的电子邮件地址
- `to`：邮件收件人
- `cc`：邮件抄送收件人
- `received`：邮件接收时间
- `body`：邮件正文
- `unread`：邮件是否未读
- `importance`：邮件的重要性等级
- `attachments`：邮件是否包含附件

### 日历操作的结果
- `subject`：事件主题
- `start`：事件开始时间
- `end`：事件结束时间
- `location`：事件地点
- `organizer`：事件组织者
- `is_recurring`：事件是否重复
- `all_day`：事件是否全天有效
- `busy_status`：事件是否显示为“忙碌”状态