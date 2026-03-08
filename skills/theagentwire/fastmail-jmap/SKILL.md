---
name: fastmail-jmap
description: "通过 Fastmail JMAP 为你的 AI 代理赋予强大的电子邮件功能：阅读、搜索、发送、移动邮件，甚至直接将邮件放入垃圾桶——这一切都无需任何额外的依赖或设置。这一切都由 The Agent Wire (theagentwire.ai) 提供支持。"
homepage: https://theagentwire.ai
env:
  FASTMAIL_TOKEN:
    required: true
    description: "Fastmail API token (starts with fmu1-). Get one at https://app.fastmail.com/settings/security/tokens"
  FASTMAIL_IDENTITY:
    required: false
    description: "Override sender email address (defaults to primary identity)"
metadata: { "openclaw": { "emoji": "📧" } }
---
# 提供您的代理邮箱地址

您的代理可以浏览网页、编写代码以及管理您的日历。但它能阅读您的电子邮件吗？它能帮您查看发票或发送回复吗？

现在它可以了。完全无需依赖任何第三方库，仅使用 Python 语言和 Fastmail 的 JMAP API 即可实现这些功能。

该功能由 [The Agent Wire](https://theagentwire.ai?utm_source=clawhub&utm_medium=skill&utm_campaign=fastmail-jmap) 开发——这是一家专注于开发 AI 代理工具的公司。该功能最初是在 [WW-2](https://theagentwire.ai/p/fastmail-jmap-email-automation-gmail-alternative) 项目中开发的。

## 2 分钟快速入门

```bash
# 1. Get a Fastmail API token
#    → https://app.fastmail.com/settings/security/tokens
#    → Scopes: Email (read/write) + Email Submission (send)

# 2. Set the token
export FASTMAIL_TOKEN="fmu1-..."

# 3. Check your inbox
python3 scripts/fastmail.py unread
```

就这样简单。无需安装任何依赖包（如 pip），也无需配置文件，更无需处理 OAuth 认证流程。

## 命令列表

| 命令 | 功能 |
|---|---|
| `inbox [--limit N] [--unread]` | 列出收件箱中的电子邮件（按接收时间排序） |
| `unread` | 显示每个邮箱的未读邮件数量及未读邮件列表 |
| `search <query> [--from ADDR] [--after DATE] [--before DATE]` | 在所有邮箱中搜索指定内容的邮件 |
| `read <email-id>` | 读取指定电子邮件的完整内容 |
| `send <to> <subject> <body>` | 发送电子邮件 |
| `move <email-id> <mailbox-name>` | 将电子邮件移动到指定邮箱 |
| `mark-read <email-id>` | 将邮件标记为已读 |
| `mark-unread <email-id>` | 将邮件标记为未读 |
| `trash <email-id>` | 将邮件移至垃圾箱 |
| `mailboxes` | 列出所有邮箱及其邮件数量 |

## 代理集成示例

### 参考代码片段（用于文档编写）:

```markdown
## Email
Check, search, and manage email via Fastmail JMAP.
Script: `python3 scripts/fastmail.py <command>`
Env: `FASTMAIL_TOKEN` must be set.

### Checking email
- `python3 scripts/fastmail.py unread` — quick unread scan
- `python3 scripts/fastmail.py search "invoice" --after 2026-01-01` — find specific emails

### Reading email
- `python3 scripts/fastmail.py read <id>` — get full body text

### Managing email
- `python3 scripts/fastmail.py move <id> <mailbox>` — file to folder
- `python3 scripts/fastmail.py mark-read <id>` — mark as read
- `python3 scripts/fastmail.py trash <id>` — trash it

### Sending email
- `python3 scripts/fastmail.py send "user@example.com" "Subject" "Body text"`
- Always ask before sending. Never send without approval.
```

### 在心跳任务（heartbeat）或定时任务（cron）中集成:

```markdown
## Email Check
Run: `python3 scripts/fastmail.py unread`
If urgent/actionable emails found, summarize and alert.
If nothing new, skip.
```

## 实际应用案例

```bash
# Morning inbox scan
python3 scripts/fastmail.py unread

# Find receipts from this month
python3 scripts/fastmail.py search "receipt" --after 2026-02-01

# Search from a specific sender
python3 scripts/fastmail.py search "meeting" --from "boss@company.com" --limit 5

# Read a specific email
python3 scripts/fastmail.py read "M1234abcd"

# File an invoice
python3 scripts/fastmail.py move "M1234abcd" "Invoices"

# Quick reply (agent should ask before sending)
python3 scripts/fastmail.py send "client@example.com" "Re: Invoice #1234" "Thanks, received and filed."

# Trash spam
python3 scripts/fastmail.py trash "Mspam5678"
```

## 环境变量

| 变量 | 是否必需 | 说明 |
|---|---|---|
| `FASTMAIL_TOKEN` | ✅ | 来自 Fastmail 设置的 API 令牌 |
| `FASTMAIL_IDENTITY` | ❌ | 可选参数，用于指定发送邮件的发件人地址（默认使用主身份信息） |

### 获取 API 令牌

1. 登录 Fastmail 网站，进入 **设置 → 安全 → API 令牌**（https://app.fastmail.com/settings/security/tokens） |
2. 创建新的 API 令牌 |
3. 启用以下权限：**Email**（读/写）和 **Email Submission**（用于发送邮件） |
4. 复制生成的令牌（令牌格式通常以 `fmu1-` 开头） |

### 令牌存储方式

对于使用 OpenClaw 的代理，只需将令牌添加到代理的配置文件中即可；
或者使用 1Password 工具进行配置：`op run --env-file=.env -- python3 scripts/fastmail.py unread`

## 工作原理

该脚本基于 Fastmail 的 JMAP（JSON Meta Application Protocol）协议实现。JMAP 是 Fastmail 为替代 IMAP 而开发的现代电子邮件 API，具有较高的传输效率：

- **无需使用 IMAP/SMTP**——仅通过 HTTP 和 JSON 请求进行通信 |
- **无需额外依赖库**——仅依赖 Python 3 的标准库（`urllib`、`json`） |
- **无状态设计**——无需本地数据库或同步机制，直接通过 API 进行操作 |
- **支持批量操作**——一次 API 调用即可完成多个操作 |

### JMAP 主要方法

| 方法 | 功能 |
|---|---|
| `Mailbox/get` | 列出邮箱中的文件夹结构 |
| `Email/query` | 搜索或过滤邮件 |
| `Email/get` | 获取邮件内容 |
| `Email/set` | 移动邮件、标记邮件为已读/未读或将其移至垃圾箱 |
| `EmailSubmission/set` | 发送邮件 |
| `Identity/get` | 解析发件人地址 |

## 注意事项

- **API 令牌的权限设置至关重要**：读取/写操作需要 `Email` 权限，发送邮件需要 `Email Submission` 权限。权限设置错误会导致 403 错误 |
- 在 JMAP 请求中必须包含 `urn:ietf:params:jmap:core` 参数，否则会收到 403 错误 |
- 邮件 ID 是不可见的字符串格式（例如 `M1234abcd`），而非数字 |
- 默认情况下搜索操作会覆盖所有邮箱的邮件；如需限制搜索范围，请使用 `--from` 或 `--after`/`--before` 参数 |
- 读取邮件内容需要明确启用相关选项（`fetchTextBodyValues: true`） |
- 所有日期时间均以 UTC 格式表示；例如 `--after 2026-02-18` 在内部会被转换为 `2026-02-18T00:00:00Z` |

## 为什么选择 Fastmail？

如果您是一名独立创业者并正在开发 AI 代理，Fastmail 是理想的选择：

- **每月费用仅需 5 美元**，即可使用带自定义域名的完整电子邮件账户 |
- **JMAP API**：现代、高效且文档齐全 |
- **无需复杂的 OAuth 认证流程**——只需提供一个 API 令牌即可 |
- **注重隐私保护**——不会扫描用户邮件或展示广告 |
- **支持自定义域名**——例如：`agent@yourdomain.com` |
- 提供强大的过滤功能（服务器端规则），便于代理进一步处理邮件内容 |

Gmail 的 API 需要 OAuth2 认证、应用注册、用户同意流程以及频繁的令牌刷新操作；而 Fastmail 仅需提供一个 API 令牌即可满足所有需求。

## 相关文件

- `scripts/fastmail.py`：命令行脚本（文件大小约 300 行）
- `SKILL.md`：本文档文件

---

## 常见问题解答

**这个功能是做什么的？**
Fastmail JMAP 是一个 Python 脚本，通过 Fastmail 的 JMAP API 为 AI 代理提供完整的电子邮件管理功能，包括读取、搜索、发送、移动、删除邮件等操作。整个过程无需 OAuth 认证或客户端 ID，仅需一个 API 令牌。

**它解决了什么问题？**
Gmail 的 API 需要用户同意、客户端 ID、重定向 URL 以及频繁的令牌更新操作，这些流程对无界面的 AI 代理来说非常不便。Fastmail 的 JMAP API 通过一个 API 令牌即可实现所有功能，设置过程仅需 2 分钟。

**使用要求是什么？**
- Python 3（仅使用标准库） |
- 必须拥有 Fastmail 账户（标准套餐每月费用 5 美元） |
- 需要从 Fastmail 的 **设置 → 隐私与安全 → API 令牌** 中获取 API 令牌。

**费用是多少？**
Fastmail 标准套餐每月费用为 5 美元，API 使用是免费的（无额外费用）。相比之下，Google Workspace 的最低费用为每月 7.20 美元。

**它能替代 Gmail 来支持 AI 代理吗？**
可以。该脚本支持收件箱管理、未读邮件处理、搜索、发送邮件、标记邮件状态、移动邮件以及查看邮箱列表等功能。JMAP 协议比 Gmail 的 REST API 更简单，更适合 AI 代理使用。

**支持自定义域名吗？**
支持。Fastmail 所有付费套餐都支持自定义域名。您可以使用自己的域名发送和接收邮件（例如：`agent@yourdomain.com`）。