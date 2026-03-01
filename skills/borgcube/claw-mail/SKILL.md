---
name: claw-mail
description: >
  **多账户电子邮件管理功能（适用于 IMAP/SMTP）**  
  该工具支持在多个账户之间执行以下操作：  
  - 获取、阅读、搜索、编写、发送、回复、转发电子邮件  
  - 支持 IMAP 收件箱功能，确保邮件可靠送达  
  - 通过 1Password 和 macOS Keychain 实现安全凭证存储  
  - 支持 TLS 1.2 及更高版本的加密协议  
  - 提供 OAuth2 认证机制  
  - 具备 IMAP IDLE 推送监控功能  
  - 支持连接池技术，提高效率  
  - 支持 S/MIME 签名功能  
  - 支持日历邀请功能  
  - 支持邮件合并功能  
  - 支持会话线程管理  
  - 具备 Webhook 规则触发功能  
  - 支持自定义日期文件夹归档规则  
  **主要特点：**  
  - **多账户管理**：用户可轻松管理多个电子邮件账户。  
  - **安全保障**：通过 1Password 和 macOS Keychain 保护用户凭证安全。  
  - **高级加密**：采用 TLS 1.2 及更高版本的加密协议，确保数据传输安全。  
  - **便捷认证**：支持 OAuth2 认证，简化用户登录流程。  
  - **实时推送**：通过 IMAP IDLE 推送功能实时接收新邮件。  
  - **高效管理**：支持连接池技术，减少资源消耗。  
  - **丰富功能**：包括邮件合并、日历邀请、Webhook 规则等实用功能。  
  - **灵活配置**：用户可自定义文件夹归档规则，便于长期存储邮件。
license: MIT
metadata:
  author: openclaw
  version: "0.7.0"
compatibility: >
  Requires Python 3.11+ and PyYAML. Optional: 1Password CLI (op) for op:// credentials,
  macOS for keychain:// credentials, cryptography package for S/MIME.
allowed-tools: Bash(python3 *) Read Write
---
# clawMail 技能

clawMail 是一个电子邮件管理工具，支持多账户的 IMAP/SMTP 功能。您可以执行以下操作：
- 从多个电子邮件账户中获取、阅读、搜索、处理、撰写、发送、回复、转发、移动和管理电子邮件、草稿以及文件夹。

## 多账户模型

- **账户配置**：每个账户都有自己的 IMAP/SMTP 凭据、邮箱、获取邮件数量限制、归档设置和处理规则。
- **默认账户**：系统会指定一个默认账户。如果没有使用 `--account` 参数，所有脚本都会自动使用默认账户。
- **SMTP 备用方案**：如果某个账户的 SMTP 服务器出现故障，系统会自动通过配置的备用中继服务器重新尝试发送。
- **IMAP 发件箱**：邮件在发送前会被暂存到临时发件箱文件夹中。如果 SMTP 发送失败，邮件会留在发件箱中，等待系统重新尝试发送。
- **账户级规则与全局规则**：每个账户都有自己的规则，同时还有适用于所有账户的全局规则。
- **OAuth2**：账户可以使用 OAuth2（XOAUTH2）进行身份验证，而无需使用密码。
- **按日期归档邮件**：`archive_mail.py` 脚本会根据 `archive_root` 和 `archive_frequency` 的设置将邮件归档到相应的文件夹中（例如 `Archive-202603`、`Archive-W09` 或 `Archive-20260315`）。

## 安全性

- **TLS 1.2+**：所有 IMAP 和 SMTP 连接都强制使用 TLS 1.2 或更高版本的加密协议。
- **强加密算法**：仅允许使用 ECDHE+AESGCM、ECDHE+CHACHA20、DHE+AESGCM 和 DHE+CHACHA20 等加密算法；禁止使用 MD5、RC4、3DES 和 DSS 等弱加密算法。
- **证书验证**：始终启用主机名检查和证书验证。
- **RFC 5322 标准**：所有发出的邮件都会自动包含 Date、Message-ID 和 MIME-Version 标头。
- **安全凭证存储**：配置文件中的密码支持多种存储方式，包括 1Password CLI（`op://vault/item/field`）、macOS Keychain（`keychain://service/account`）和环境变量（`env://VAR_NAME`）。

## 可用脚本

所有脚本都位于 `scripts/` 目录中。可以通过 `python3 scripts/<name>.py` 命令来运行这些脚本。每个脚本都支持 `--account <name>` 参数，以便针对特定账户执行操作。

### 核心脚本

| 脚本 | 功能 |
|--------|---------|
| `scripts/fetch_mail.py` | 从 IMAP 文件夹中获取邮件 |
| `scripts/read_mail.py` | 根据 Message-ID 读取并显示邮件内容；将附件保存到磁盘 |
| `scripts/search_mail.py` | 按主题、发件人、邮件内容或日期搜索邮件 |
| `scripts/send_mail.py` | 通过 SMTP 发送富文本格式的电子邮件（支持备用方案）；可附加文件 |
| `scripts/compose_mail.py` | 根据模板编写富文本格式的电子邮件；可附加文件 |
| `scripts/reply_mail.py` | 回复邮件时保留原始邮件内容 |
| `scripts/forward_mail.py` | 内联引用或附加附件地转发邮件 |
| `scripts/draft_mail.py` | 保存、列出、恢复或通过 IMAP 草稿文件夹发送草稿 |
| `scripts/process_mail.py | 根据规则处理邮件 |
| `scripts/manage_folders.py` | 列出、创建、删除和重命名 IMAP 文件夹 |
| `scripts/move_mail.py | 在 IMAP 文件夹之间移动邮件（支持批量操作） |
| `scripts/heartbeat.py` | 运行完整的邮件处理周期（清空发件箱、获取新邮件并处理邮件） |
| `scripts/idle_monitor.py` | 通过 IMAP IDLE 协议监控邮箱状态（提供推送通知） |
| `scripts/retry_send.py | 重试发送失败在发件箱中的邮件 |
| `scripts/calenderInvite.py` | 编写并发送 iCalendar 会议邀请 |
| `scripts/mail_merge.py` | 根据模板和 CSV/JSON 数据批量发送个性化邮件 |
| `scripts/thread_mail.py` | 将邮件分组到相应的讨论线程中 |
| `scripts/archive_mail.py` | 自动将旧邮件归档到按日期命名的文件夹中（每日/每周/每月/每年） |

### 库模块

| 模块 | 功能 |
|--------|---------|
| `scripts/lib/imap_client.py` | 提供 IMAP 客户端功能，支持 IDLE 协议、搜索、文件夹管理和 TLS 1.2+ 协议 |
| `scripts/lib/smtp_client.py` | 提供 SMTP 客户端功能，支持 TLS 1.2+ 协议、RFC 5322 标准、OAuth2 和 MIME 格式处理 |
| `scripts/lib/composer.py` | 用于编写富文本格式电子邮件的工具，支持模板和附件功能 |
| `scripts/lib/processor.py | 基于规则的邮件处理流程，支持 Webhook 动作 |
| `scripts/lib/account_manager.py | 多账户管理模块，包含 SMTP 备用方案和发件箱功能 |
| `scripts/lib/outbox.py` | 用于临时存储邮件的 IMAP 发件箱 |
| `scripts/lib/credential_store.py | 安全的凭证存储机制（支持 1Password、Keychain 和环境变量） |
| `scripts/lib/pool.py | 用于管理 IMAP/SMTP 连接的连接池 |
| `scripts/lib/send_queue.py | 用于发送邮件的旧式队列机制（现已被发件箱功能替代） |
| `scripts/lib/smime.py` | 处理 S/MIME 格式的邮件签名和加密 |
| `scripts/lib/oauth2.py` | 提供 OAuth2（XOAUTH2）令牌管理功能 |
| `scripts/lib/models.py | 定义相关数据模型（如 EmailMessage、EmailAddress 等） |

### 参考文档

- `references/REFERENCE.md`：API 概述、所有脚本参数及输出格式说明 |
- `references/TEMPLATES.md`：提供的电子邮件模板及模板变量 |
- `references/RULES.md`：如何配置邮件处理规则 |
- `ROADMAP.md`：功能路线图和进度跟踪信息 |

## 快速入门

### 获取邮件

```bash
python3 scripts/fetch_mail.py --config config.yaml

python3 scripts/fetch_mail.py --account personal --unread-only --format cli --config config.yaml
```

### 发送富文本邮件

邮件会先被暂存到 IMAP 的临时发件箱文件夹中，然后通过 SMTP 发送（支持备用方案），发送成功后邮件会从发件箱中删除。

```bash
python3 scripts/send_mail.py \
  --to "recipient@example.com" \
  --subject "Weekly Report" \
  --body "<p>Here are this week's results.</p>" \
  --template default \
  --attach report.pdf \
  --config config.yaml
```

### 回复和转发邮件

```bash
python3 scripts/reply_mail.py --message-id "<id@example.com>" --body "Thanks!" --config config.yaml

python3 scripts/forward_mail.py --message-id "<id@example.com>" --to "colleague@x.com" --config config.yaml
```

### 搜索邮件

```bash
python3 scripts/search_mail.py --subject "invoice" --unseen --config config.yaml

python3 scripts/search_mail.py --criteria '(FROM "alice@x.com" SINCE 01-Jan-2026)' --config config.yaml
```

### 管理草稿

```bash
python3 scripts/draft_mail.py --action save --to "user@x.com" --subject "WIP" --body "..." --config config.yaml
python3 scripts/draft_mail.py --action list --format cli --config config.yaml
python3 scripts/draft_mail.py --action send --message-id "<draft@x.com>" --config config.yaml
```

### 发件箱与重试机制

```bash
python3 scripts/retry_send.py --config config.yaml
python3 scripts/retry_send.py --config config.yaml --list
```

### 邮件处理周期

系统会清空每个账户的发件箱，然后获取新邮件并进行处理：

```bash
python3 scripts/heartbeat.py --config config.yaml
python3 scripts/heartbeat.py --config config.yaml --account work
```

### 归档旧邮件

```bash
python3 scripts/archive_mail.py --config config.yaml --days 90 --frequency monthly
python3 scripts/archive_mail.py --config config.yaml --days 30 --frequency daily --archive-root "Old Mail" --dry-run --format cli
```

邮件归档时会根据 `archive_root` 和 `archive_frequency` 的设置进行分类（默认设置为“每月归档”）。系统会自动将邮件移动到相应的归档文件夹中（例如 `Archive-202603`、`Archive-W09` 或 `Archive-20260315`）。

### 创建配置文件

您可以使用 `assets/config.example.yaml` 作为模板来创建 `config.yaml` 文件：

```yaml
default_account: work

accounts:
  work:
    label: "Work"
    sender_address: "alice@company.com"
    sender_name: "Alice Smith"
    imap:
      host: imap.company.com
      port: 993
      username: "alice@company.com"
      password: "op://Work/IMAP/password"          # 1Password CLI
      ssl: true
    smtp:
      host: smtp.company.com
      port: 587
      username: "alice@company.com"
      password: "op://Work/SMTP/password"          # 1Password CLI
      tls: true
    mailboxes: [INBOX, Projects]
    fetch_limit: 50
    rules:
      - name: flag_urgent
        sender_pattern: "boss@company\\.com"
        actions: [flag, tag]
        tag: urgent

  personal:
    label: "Personal"
    sender_address: "alice@gmail.com"
    imap:
      host: imap.gmail.com
      password: "keychain://imap.gmail.com/alice@gmail.com"  # macOS Keychain
    smtp:
      host: smtp.gmail.com
      password: "keychain://smtp.gmail.com/alice@gmail.com"  # macOS Keychain
```

您还可以全局或针对每个账户设置 `archive_root`（例如 `Archive`）和 `archive_frequency`（每日/每周/每月/每年）。这些设置会影响 `archive_mail.py` 脚本以及系统对归档规则的处理，确保归档邮件始终被保存在正确的文件夹中。

### 安全凭证存储

配置文件中的密码支持以下四种存储方式：

| 存储方式 | 后端 | 示例 |
|--------|---------|---------|
| `op://` | 1Password CLI | `"op://Work/IMAP/password"` |
| `keychain://` | macOS Keychain | `"keychain://imap.gmail.com/alice"` |
| `env://` | 环境变量 | `"env://GMAIL_APP_PASSWORD"` |
| **明文** | 直接输入的密码 | `"my-password"`（此方式会记录警告信息） |

### OAuth2 身份验证（Gmail、Outlook 365）

对于需要 OAuth2 认证的账户，请在 IMAP/SMTP 配置中设置 `auth: oauth2`：

```yaml
imap:
  host: imap.gmail.com
  username: "user@gmail.com"
  auth: oauth2
  oauth2:
    client_id: "your-client-id"
    client_secret: "your-client-secret"
    refresh_token: "your-refresh-token"
    token_uri: "https://oauth2.googleapis.com/token"
```

### 单账户配置

如果配置文件中的 `imap:` 和 `smtp:` 设置为扁平格式，系统会自动将其视为名为“default”的单个账户。