---
name: fastmail-jmap
description: "通过 Fastmail JMAP 为你的 AI 代理赋予强大的电子邮件功能：阅读邮件、搜索邮件、发送邮件、移动邮件、将邮件放入垃圾箱——完全无需依赖任何外部服务。这一切都通过 The Agent Wire (theagentwire.ai) 实现。"
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

您的代理可以浏览网页、编写代码以及管理您的日历，但它能读取您的电子邮件吗？它能帮您查看发票或发送回复吗？现在它可以了。这个工具完全依赖Python语言实现，且仅使用Fastmail的JMAP API。

该工具由[The Agent Wire](https://theagentwire.ai)开发——这是一个专注于开发AI代理工具的团队。

## 2分钟快速入门

```bash
# 1. Get a Fastmail API token
#    → https://app.fastmail.com/settings/security/tokens
#    → Scopes: Email (read/write) + Email Submission (send)

# 2. Set the token
export FASTMAIL_TOKEN="fmu1-..."

# 3. Check your inbox
python3 scripts/fastmail.py unread
```

就这么简单。无需安装任何依赖包，也无需配置文件，更无需处理OAuth认证。

## 命令列表

| 命令 | 功能 |
|---|---|
| `inbox [--limit N] [--unread]` | 列出收件箱中的电子邮件（按接收时间排序） |
| `unread` | 显示每个邮箱的未读邮件数量及未读邮件列表 |
| `search <查询内容> [--fromADDR] [--after DATE] [--before DATE]` | 在所有邮箱中搜索指定内容 |
| `read <邮件ID>` | 读取邮件的完整内容 |
| `send <收件人> <主题> <邮件内容>` | 发送电子邮件 |
| `move <邮件ID> <邮箱名称>` | 将邮件移动到指定邮箱 |
| `mark-read <邮件ID>` | 将邮件标记为已读 |
| `mark-unread <邮件ID>` | 将邮件标记为未读 |
| `trash <邮件ID>` | 将邮件移至垃圾箱 |
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

### 在心跳脚本或定时任务中集成:

```markdown
## Email Check
Run: `python3 scripts/fastmail.py unread`
If urgent/actionable emails found, summarize and alert.
If nothing new, skip.
```

## 实际应用示例

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

| 变量 | 是否必填 | 说明 |
|---|---|---|
| `FASTMAIL_TOKEN` | ✅ | 来自Fastmail设置的API令牌 |
| `FASTMAIL_IDENTITY` | ❌ | 可选：覆盖发送者的邮箱地址（默认使用主邮箱地址） |

### 获取API令牌

1. 访问[Fastmail设置 → 安全 → API令牌](https://app.fastmail.com/settings/security/tokens) |
2. 创建新的API令牌 |
3. 启用以下权限：**Email**（读写）和**Email Submission**（用于发送邮件） |
4. 复制令牌（令牌格式以`fmu1-`开头） |

### 令牌存储方式

对于使用OpenClaw的代理，只需将令牌添加到代理的配置文件中：
```json
{
  "env": {
    "vars": {
      "FASTMAIL_TOKEN": "fmu1-..."
    }
  }
}
```

或者使用1Password工具进行配置：`op run --env-file=.env -- python3 scripts/fastmail.py unread`

## 工作原理

该工具基于[JMAP](https://jmap.io/)协议（一种基于JSON的现代电子邮件协议）与Fastmail进行通信。JMAP替代了传统的IMAP/SMTP协议，具有更高的效率和更简洁的接口：

- **无需IMAP/SMTP**：仅使用HTTP和JSON请求 |
- **无需额外依赖库**：仅依赖Python 3的标准库（`urllib`、`json`） |
- **无状态设计**：无需本地数据库或同步操作，只需发送请求即可 |
- **支持批量操作**：多个操作可以通过一次API调用完成 |

### 主要使用的JMAP方法

| 方法 | 功能 |
|---|---|
| `Mailbox/get` | 列出邮箱内的文件夹 |
| `Email/query` | 搜索或过滤邮件 |
| `Email/get` | 获取邮件内容 |
| `Email/set` | 移动邮件、标记为已读/未读或移至垃圾箱 |
| `EmailSubmission/set` | 发送邮件 |
| `Identity/get` | 解析发件人地址 |

## 注意事项

- **API令牌的权限设置非常重要**：读取/写入邮件需要`Email`权限，发送邮件需要`Email Submission`权限。权限设置不正确会导致403错误 |
- **JMAP请求中必须包含`urn:ietf:params:jmap:core`字段**，否则会导致403错误 |
- **邮件ID为不透明的字符串格式**（例如`M1234abcd`），而非数字 |
- **搜索操作为全局范围**，如需限制搜索范围，请使用`--from`或`--after`/`--before`参数 |
- **获取邮件内容需要明确指定`fetchTextBodyValues`参数**（脚本会自动处理该参数） |
- **日期格式为UTC**：例如`--after 2026-02-18`在内部会被转换为`2026-02-18T00:00:00Z` |

## 为什么选择Fastmail？

如果您是独立创业者并正在开发AI代理，Fastmail是理想的选择：

- **每月5美元即可拥有包含自定义域名的完整邮箱账户** |
- **使用JMAP API**：现代、高效且文档齐全 |
- **无需复杂的OAuth认证流程**：只需提供API令牌即可 |
- **注重隐私保护**：不会扫描用户邮件或展示广告 |
- **支持自定义域名**：例如`you@yourdomain.com` |
- **提供强大的过滤功能**：代理可以通过服务器端的规则进一步优化邮件处理流程 |

Gmail的API需要OAuth2认证、应用注册、用户同意流程以及频繁的令牌更新。而Fastmail只需提供一个API令牌即可满足所有需求。

## 相关文件

- `scripts/fastmail.py`：命令行脚本（单个文件，约300行代码）
- `SKILL.md`：本文档文件

---

## 常见问题解答

**这个工具是什么？**
Fastmail JMAP是一个Python脚本，通过Fastmail的JMAP API为AI代理提供完整的电子邮件管理功能（包括读取、搜索、发送、移动、删除邮件等操作）。无需使用OAuth认证或客户端ID，只需一个API令牌即可。

**它解决了什么问题？**
Gmail的API需要用户同意、客户端ID、重定向URL以及频繁的令牌更新流程，这些对于无界面的AI代理来说非常不便。Fastmail的JMAP API通过一个API令牌即可实现所有功能，设置过程仅需2分钟。

**使用要求是什么？**
- Python 3（仅使用标准库） |
- 必须拥有Fastmail账户（标准套餐每月5美元） |
- 需要从Fastmail的“隐私与安全”设置中获取API令牌。

**费用是多少？**
Fastmail的标准套餐每月费用为5美元，API使用是包含在内的，无需额外付费。相比之下，Google Workspace的最低费用为每月7.20美元。

**它能替代Gmail用于AI代理吗？**
完全可以。该工具支持收件箱管理、未读邮件查看、搜索、发送邮件、移动邮件、标记邮件状态以及邮箱列表等功能。JMAP协议比Gmail的REST API更简洁、更易于代理使用。

**支持自定义域名吗？**
支持。Fastmail的所有付费套餐都支持自定义域名，您可以使用自己的域名发送和接收邮件（例如`agent@yourdomain.com`）。