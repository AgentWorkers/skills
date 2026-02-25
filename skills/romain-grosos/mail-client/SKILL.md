---
name: mail-client
description: "OpenClaw代理的IMAP/SMTP邮件客户端。适用场景：  
(1) 从邮箱中读取或列出电子邮件；  
(2) 按发送者、主题、日期或文本内容搜索电子邮件；  
(3) 发送纯文本或HTML格式的电子邮件；  
(4) 移动、标记或删除邮件。  
不适用场景：  
- 批量发送邮件；  
- 发送新闻通讯；  
- 管理日历/联系人（请使用CalDAV）；  
- 需要OAuth认证的邮件服务（请使用专门的工具）。"
homepage: https://github.com/Rwx-G/openclaw-skill-mail-client
compatibility: Python 3.9+ - no external dependencies (stdlib only) - network access to IMAP/SMTP server
metadata:
  {
    "openclaw": {
      "emoji": "📧",
      "requires": { "env": ["MAIL_USER", "MAIL_APP_KEY", "MAIL_SMTP_HOST", "MAIL_IMAP_HOST"] },
      "primaryEnv": "MAIL_APP_KEY"
    }
  }
ontology:
  reads: [emails]
  writes: [emails, flags]
---
# mail-client

这是一个用于读取/搜索标准邮件服务器中的邮件以及发送邮件的工具，仅使用Python标准库，不依赖任何外部库。

---

## 常用命令短语

- “检查我的邮件”
- “我有未读邮件吗？”
- “阅读来自Alice的邮件”
- “搜索关于发票的邮件”
- “给Bob发送邮件”
- “将那封邮件移到归档文件夹”
- “将邮件标记为已读”
- “删除那条邮件”
- “列出我的邮件文件夹”

---

## 快速入门

```bash
python3 scripts/setup.py   # interactive setup: credentials + permissions
python3 scripts/init.py    # validate all configured capabilities
python3 scripts/mail.py config  # show current config (no secrets)
```

---

## 设置

### 1. 运行设置向导

```bash
python3 scripts/setup.py
```

设置向导会收集以下信息：
- SMTP服务器地址/端口、IMAP服务器地址/端口
- 邮件用户名和应用程序密钥（即应用密码）
- 需要启用的功能（默认情况下所有功能均关闭）
- 默认文件夹和最大搜索结果数量

### 2. 验证设置

```bash
python3 scripts/init.py
```

验证结果应为“所有检查均通过”或“跳过”（无错误）。

### 3. 在`config.json`中启用所需功能

编辑位于技能根目录下的`config.json`文件：

```json
{
  "allow_send": true,
  "allow_read": true,
  "allow_search": true,
  "allow_delete": false,
  "default_folder": "INBOX",
  "max_results": 20
}
```

---

## 数据存储与凭证管理

| 文件路径 | 编写者 | 用途 | 存储内容 |
|--------|---------|---------|-----------------|
| `~/.openclaw/secrets/mail_creds` | `setup.py` | SMTP/IMAP凭证及应用程序密钥 | 是 | 文件权限设置为600，不会被提交到Git仓库 |
| `skill_dir/config.json` | `setup.py` | 行为限制、文件夹设置等默认值 | 否 | 仅包含配置信息，不会被提交到Git仓库 |

### `~/.openclaw/secrets/mail_creds`

由`setup.py`生成，文件权限设置为600，不会被提交到Git仓库。其中包含：

```
MAIL_SMTP_HOST=mail.example.com
MAIL_SMTP_PORT=587
MAIL_IMAP_HOST=mail.example.com
MAIL_IMAP_PORT=993
MAIL_USER=user@example.com
MAIL_APP_KEY=app-password-here
MAIL_FROM=user@example.com
```

### `skill_dir/config.json`

由`setup.py`生成，用于控制工具的行为设置（哪些功能被启用）。该文件不包含敏感信息，因此不会被提交到Git仓库。如果需要，可以参考`config.example.json`作为初始配置文件。

---

## 模块使用方法

在Python代码中直接导入`MailClient`模块即可使用该工具：

```python
from scripts.mail import MailClient

client = MailClient()

# List 5 unread messages
msgs = client.list_messages(limit=5, unseen_only=True)
for m in msgs:
    print(m["from"], m["subject"])

# Read a message
msg = client.read_message("42")
print(msg["body"])

# Send a message
result = client.send(
    to="alice@example.com",
    subject="Hello",
    body="Hi Alice, how are you?",
)
print(result)

# Search
found = client.search_messages(from_addr="bob@example.com", unseen_only=True)
```

---

## 命令行接口（CLI）参考

```
python3 scripts/mail.py <subcommand> [options]
```

| 命令 | 需要的权限 | 功能描述 |
|------|---------|-------------|
| `list` | `allow_read` | 列出邮件（按发送时间排序） |
| `read <uid>` | `allow_read` | 根据用户ID读取邮件内容 |
| `search` | `allow_search` | 使用过滤器搜索邮件 |
| `send` | `allow_send` | 发送邮件 |
| `move <uid> <folder>` | `allow_delete` | 将邮件移动到指定文件夹 |
| `mark-read <uid>` | `allow_read` | 将邮件标记为已读 |
| `mark-unread <uid>` | `allow_read` | 将邮件标记为未读 |
| `delete <uid>` | `allow_delete` | 删除邮件 |
| `folders` | `allow_read` | 列出IMAP文件夹 |
| `quota` | 无 | 查看邮箱配额 |
| `config` | 无 | 显示当前配置信息 |

### 使用示例

```bash
# List last 10 messages
python3 scripts/mail.py list --limit 10

# List unread only
python3 scripts/mail.py list --unseen

# Read message UID 42
python3 scripts/mail.py read 42

# Search from a sender since a date
python3 scripts/mail.py search --from-addr alice@example.com --since 01-Jan-2026

# Search by subject containing "invoice"
python3 scripts/mail.py search --subject "invoice"

# Send with CC
python3 scripts/mail.py send \
  --to recipient@example.com \
  --subject "Report" \
  --body "Please find attached." \
  --cc manager@example.com

# Move UID 42 to Archive
python3 scripts/mail.py move 42 Archive

# Mark as unread
python3 scripts/mail.py mark-unread 42

# Delete UID 42
python3 scripts/mail.py delete 42

# List folders
python3 scripts/mail.py folders

# Check quota
python3 scripts/mail.py quota
```

---

## 模板示例

- **代理任务：检查并汇总未读邮件**
- **代理任务：发送通知邮件**
- **代理任务：搜索并归档旧发票**

---

## 高级功能建议

- **每日摘要**：每天早上列出未读邮件，并汇总邮件发送者和主题。
- **自动归档**：将符合特定条件的邮件移动到归档文件夹。
- **通过监控脚本发送警报**：例如在磁盘空间不足、备份失败或系统出现错误时发送通知。
- **草稿模式发送**：利用大型语言模型（LLM）生成邮件正文，再通过该工具发送。
- **与日历功能结合**：通过邮件发送会议摘要。

---

## 可与其他工具结合使用

- `nextcloud-files`：将邮件附件附加到Nextcloud服务器或保存到其中。
- `ghost-admin`：在Ghost博客发布新文章时发送通知邮件。
- 与任何监控或自动化工具结合使用，以实现警报通知功能。

---

## 故障排除

如遇到以下问题，请参考[references/troubleshooting.md]：
- 连接失败
- 认证失败
- 无法找到IMAP文件夹
- SMTP中继服务器拒绝接收邮件
- 自签名证书问题（仅适用于本地服务器）

---