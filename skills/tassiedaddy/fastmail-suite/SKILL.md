---
name: fastmail-suite
description: **安全的、默认即安全的 Fastmail 集成（电子邮件、联系人、日历）**：通过 JMAP 和 CalDAV 协议实现。适用于需要验证 Fastmail 的配置、筛选/搜索电子邮件、查看邮件线程、读取/搜索联系人、查看即将发生的事件，或（仅在明确启用时）发送电子邮件以及创建/重新安排/取消日历事件的场景。该集成设计为支持最小权限访问模型，输出内容默认会被屏蔽敏感信息，并提供了明确的写入权限控制选项。
env:
  FASTMAIL_TOKEN:
    required: true
    description: "Fastmail JMAP API token (Mail + Contacts scopes). Read-only is recommended by default."
  FASTMAIL_TOKEN_SEND:
    required: false
    description: "Optional Fastmail JMAP token with Email Submission scope for sending mail. Only needed when writes are explicitly enabled."
  FASTMAIL_CALDAV_USER:
    required: false
    description: "Username/email for Fastmail CalDAV (calendar app password). Required for calendar features."
  FASTMAIL_CALDAV_PASS:
    required: false
    description: "Fastmail CalDAV app password used for calendar access."
  FASTMAIL_REDACT:
    required: false
    description: "Controls redaction of output (default 1 = redacted)."
  FASTMAIL_ENABLE_WRITES:
    required: false
    description: "When set to 1, enables write operations (send/move/update). Omit or 0 to keep read-only."
metadata: { "openclaw": { "emoji": "📧" } }
---
# Fastmail Suite

请使用随附的脚本（仅包含 `stdlib` 模块）来安全地与 Fastmail 进行交互。

## 快速入门

设置凭据/令牌：

```bash
# JMAP token (Mail + Contacts scopes)
export FASTMAIL_TOKEN='…'

# CalDAV app password (calendar)
export FASTMAIL_CALDAV_USER='you@yourdomain'
export FASTMAIL_CALDAV_PASS='app-password'

# Optional: redact output (default is 1)
export FASTMAIL_REDACT=1
```

验证设置：

```bash
python3 skills/fastmail-suite/scripts/suite.py status
```

## Suite CLI (v0.2)

### 状态/入职检查

```bash
python3 skills/fastmail-suite/scripts/suite.py status
```

预期的输出格式：
- `Mail (JMAP): OK` / `MISSING TOKEN` / `AUTH FAILED`
- `Calendar (CalDAV): OK` / `MISSING APP PASSWORD` / `AUTH FAILED`
- `Contacts (JMAP): OK` / `MISSING TOKEN` / `AUTH FAILED`

### 收件箱分类

```bash
python3 skills/fastmail-suite/scripts/suite.py triage today
python3 skills/fastmail-suite/scripts/suite.py triage last-7d
```

分类结果包括：
- 最常发送邮件的发件人；
- 需要处理的邮件主题类型（如 `invoice`、`bill`、`payment`、`due`、`confirm`、`action required`、`reminder` 等）；
- 来自 `friends.tas.edu.au` 的邮件以及与账单/支付相关的邮件会被特别标记。

### 搜索

```bash
python3 skills/fastmail-suite/scripts/suite.py search "from:billing@ subject:invoice last:7d"
python3 skills/fastmail-suite/scripts/suite.py search "has:attachment before:2026-02-01 tax"
python3 skills/fastmail-suite/scripts/suite.py search "after:2026-02-01 reminder"
```

支持的查询参数：
- `from:foo`  
- `subject:bar`  
- `has:attachment`  
- `last:7d`（以及其他类似的日期范围）  
- `before:YYYY-MM-DD`  
- `after:YYYY-MM-DD`  
- 简单的文本搜索（针对邮件主题或正文内容）

### 主题讨论记录摘要

```bash
python3 skills/fastmail-suite/scripts/suite.py thread <email-id>
python3 skills/fastmail-suite/scripts/suite.py thread <thread-id>
python3 skills/fastmail-suite/scripts/suite.py thread "school invoice"
```

显示主题讨论记录的简要信息：
- 参与者  
- 大致的时间线  
- 最新的 1–2 条消息及其简短的文本摘要

## 其他现有脚本

### 电子邮件（JMAP）

```bash
python3 skills/fastmail-suite/scripts/fastmail.py mail inbox --limit 20
python3 skills/fastmail-suite/scripts/fastmail.py mail search "invoice" --limit 10
python3 skills/fastmail-suite/scripts/fastmail.py mail read <email-id>
```

### 联系人（JMAP）

```bash
python3 skills/fastmail-suite/scripts/fastmail.py contacts list --limit 20
python3 skills/fastmail-suite/scripts/fastmail.py contacts search "alice" --limit 5
python3 skills/fastmail-suite/scripts/fastmail.py contacts get <contact-id>
```

### 日历（CalDAV）

```bash
python3 skills/fastmail-suite/scripts/fastmail.py calendar calendars
python3 skills/fastmail-suite/scripts/fastmail.py calendar upcoming --days 7
```

## 安全性与凭据（重要提示）

Fastmail Suite 使用真实的 Fastmail 凭据进行操作，因此设计上采取了保守的原则。

### 必需的凭据：
- `FASTMAIL_TOKEN` — Fastmail JMAP API 令牌（适用于邮件和联系人功能）。最佳实践是在常规使用中仅使用 **只读** 令牌。

### 可选但受支持的凭据：
- `FASTMAIL_TOKEN_SEND` — 用于发送邮件的独立 JMAP 令牌（仅在使用写入功能时需要）。
- `FASTMAIL_CALDAV_USER` / `FASTMAIL_CALDAV_PASS` — Fastmail 应用程序密码（用于日历功能）。
- `FASTMAIL_REDACT` — 控制输出内容的显示方式（默认值为 `1`，表示隐藏部分内容）。
- `FASTMAIL_ENABLE_WRITES` — 当设置为 `1` 时，允许执行写入操作（发送、移动、更新邮件）。如果不需要写入功能，请将其设置为 `0` 以保持只读模式。

### 安全机制：
- **默认情况下，输出内容会被隐藏**  
  除非您明确使用 `--raw` 参数。默认设置 `FASTMAIL_REDACT=1`。
- **默认情况下，不允许执行写入操作**  
  除非 `FASTMAIL_ENABLE_WRITES=1` 且您提供了相应的令牌（例如 `FASTMAIL_TOKEN_SEND` 用于发送邮件），否则该工具不会执行任何写入操作。
- **角色分离**  
  您可以严格区分不同的操作权限：
  - **仅读取邮件**：使用 `FASTMAIL_TOKEN`  
  - **发送邮件**：使用 `FASTMAIL_TOKEN_SEND`（仅在启用写入功能时需要）  
  - **访问日历**：使用 `FASTMAIL_CALDAV_USER` + `FASTMAIL_CALDAV_PASS`（Fastmail 应用程序密码）
- **完全支持只读模式**  
  即使不启用写入功能，您也可以使用 **只读 JMAP 令牌和日历应用程序密码** 来运行整个工具集（查看状态、分类邮件、搜索、查看主题讨论记录、管理联系人信息、查看日历）。

## 更新日志

### v0.1.1
- 对联系人相关的命令（`list`、`search`、`get`）进行了实际 Fastmail 账户的测试。
- `suite.py` 现在会通过 JMAP 检查联系人账户的状态，并报告相应的结果。

### v0.2
- 新增了 `scripts/suite.py` 文件，其中包含 JMAP 和 CalDAV 功能的入职检查。
- 新增了邮件处理流程：
  - `triage today`（处理今天的邮件）
  - `triage last-7d`（处理过去 7 天的邮件）
  - `search <query>`（支持使用 `from:`, `subject:`, `has:attachment`, `last:`, `before:`, `after:` 等参数进行搜索）
- 在 `scripts/fastmail.py` 中添加了用于调用其他功能的包装器代码。
- 提供了状态检查、邮件分类、搜索和主题讨论记录查看的快速入门和使用示例。