---
name: fastmail-suite
description: >
  **Fastmail 的安全集成方案（默认为安全模式）**  
  通过 JMAP 和 CalDAV 协议，您可以安全地访问 Fastmail 的邮箱、联系人及日历功能。该方案支持以下操作：  
  - 阅读/搜索邮件  
  - 阅读/搜索联系人  
  - 查看即将发生的事件  
  - （仅在明确启用时）发送邮件  
  - 创建/重新安排/取消日历事件  
  **设计特点：**  
  - 专为使用最小权限的账户设计  
  - 默认情况下，所有输出内容都会被屏蔽（即不显示敏感信息）  
  - 提供明确的写入权限控制选项  
  **适用场景：**  
  当您需要以最小权限访问 Fastmail 的功能时，该方案是理想的选择。
---
# Fastmail Suite

请使用随附的脚本（仅包含 `stdlib` 模块）来安全地与 Fastmail 进行交互。

## 快速入门（安全模式 / 只读模式）

### 邮件（JMAP）

```bash
export FASTMAIL_TOKEN='…'              # read token
python3 skills/fastmail-suite/scripts/fastmail.py mail inbox --limit 20
python3 skills/fastmail-suite/scripts/fastmail.py mail search "invoice" --limit 10
python3 skills/fastmail-suite/scripts/fastmail.py mail read <email-id>
```

### 联系人（JMAP）

```bash
export FASTMAIL_TOKEN='…'
python3 skills/fastmail-suite/scripts/fastmail.py contacts search "alice"
```

### 日历（CalDAV）

```bash
export FASTMAIL_CALDAV_USER='you@yourdomain'
export FASTMAIL_CALDAV_PASS='app-password'
python3 skills/fastmail-suite/scripts/fastmail.py calendar calendars
python3 skills/fastmail-suite/scripts/fastmail.py calendar upcoming --days 7
```

## 安全模型（非常重要）

### 1) 默认情况下，输出内容会被屏蔽
- 除非您使用 `--raw` 选项，否则输出内容会被屏蔽。
- 可以通过 `FASTMAIL_REDACT` 参数全局控制这一行为（默认值为 `1`）。

### 2) 默认情况下，写入操作是被禁止的
任何写入操作都需要：

```bash
export FASTMAIL_ENABLE_WRITES=1
```

### 3) 建议使用不同的令牌/密码
- **读取邮件：** `FASTMAIL_TOKEN`
- **发送邮件：** `FASTMAIL_TOKEN_SEND`（可选，但建议使用）
- **日历操作：** `FASTMAIL-CalDAV_USER` + `FASTMAIL-CalDAV_PASS`（Fastmail 应用程序密码）

## 常用任务

### 邮件
- 列出收件箱邮件：`mail.py inbox [--limit N] [--unread]`
- 查看未读邮件：`mail.py unread [--limit N]`
- 搜索邮件：`mail.py search <query> [--from addr] [--after YYYY-MM-DD] [--before YYYY-MM-DD] [--limit N]`
- 读取邮件内容：`mail.py read <id> [--full] [--raw]`
- 发送邮件（支持写入操作）：

```bash
export FASTMAIL_ENABLE_WRITES=1
export FASTMAIL_TOKEN_SEND='…'         # token with submission scope
# optional identity selection:
export FASTMAIL_IDENTITY_EMAIL='you@yourdomain'
python3 skills/fastmail-suite/scripts/fastmail.py mail send \
  --to recipient@example.com --subject "Hello" --body "Hi there"
```

### 日历
- 查看即将发生的事件：`calendar_caldav.py upcoming --days 7 [--debug]`
- 创建日历事件：`calendar_caldav.py create --calendar-name NAME --summary TEXT --start ISO --end ISO --tz TZID`
- 重新安排/更新日历事件：`calendar_caldav.py update --href HREF --etag ETAG --summary ... --start ... --end ... --tz ...`
- 删除日历事件：`calendar_caldav.py delete --href HREF --etag ETAG`

提示：使用 `upcoming --debug` 命令可以获取用于更新/删除事件的 `href` 和 `etag` 值。

## 发布时的注意事项
- 请不要将令牌或应用程序密码直接写入脚本中，应通过环境变量进行管理。
- 脚本默认会屏蔽输出内容并禁止写入操作（这些设置已在脚本中实现）。