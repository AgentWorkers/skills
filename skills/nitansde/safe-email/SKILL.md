---
name: safe-email
description: >
  **以隐私保护为核心的工作流程：通过 IMAP 处理明确转发的电子邮件，并创建日历/提醒事项**  
  该流程仅适用于用户明确要求在专用邮箱中处理最新转发的电子邮件的情况。使用此流程需要用户的 IMAP 认证信息以及已配置的日历/提醒集成功能。任何具有删除功能的操作均为可选（需用户明确确认）。
metadata:
  credentialsRequired:
    - imap_username
    - imap_app_password_or_oauth
    - calendar_integration_credentials
    - reminder_integration_credentials
  envRequired:
    - SAFE_EMAIL_IMAP_USERNAME
    - SAFE_EMAIL_IMAP_APP_PASSWORD
  secretSourcesAccepted:
    - env
    - os_keychain
    - secure_config_ref
    - oauth_token_store
  openclaw:
    requires:
      bins: ["himalaya"]
      credentials:
        - imap_username
        - imap_app_password_or_oauth
        - calendar_integration_credentials
        - reminder_integration_credentials
      env:
        - SAFE_EMAIL_IMAP_USERNAME
        - SAFE_EMAIL_IMAP_APP_PASSWORD
      secretSources:
        - env
        - os_keychain
        - secure_config_ref
        - oauth_token_store
      recommendedSecretSource: os_keychain_or_secure_config_ref
    capabilities:
      - imap_read_latest_only
      - calendar_write
      - reminder_write
      - email_delete_optional
    compliance:
      explicitTriggerRequired: true
      autoPollingForbidden: true
      destructiveActionsNeedConsent: true
      forwardToDedicatedInboxRequired: true
---
# 安全邮件处理（隐私优先）

使用此功能可安全地处理转发的邮件，并将可操作的邮件内容转换为以下形式：
- 日历事件，和/或
- 提醒/任务

此功能的设计较为保守，且**仅允许用户主动触发**（即用户必须明确表示同意才能使用该功能）。

## 所需的访问权限和凭证（必须向用户说明）

此工作流程需要以下权限：
1. **IMAP邮箱访问权限**，以访问专用的收件箱（用户名 + 应用程序密码/OAuth）
2. **日历写入权限**（用户选择的任何日历系统）
3. **提醒/任务写入权限**（用户选择的任何提醒系统）
4. **可选的邮件删除权限**（仅当用户启用后续删除操作时）

如果缺少上述任何一项权限，请以只读/解析模式运行，并询问用户下一步该怎么做。

## 所需的凭证及可接受的凭证存储方式

首次运行前需要提供的凭证：
- IMAP用户名（专用收件箱地址）
- IMAP应用程序密码或OAuth令牌
- 日历集成凭证/配置（具体取决于服务提供商）
- 提醒集成凭证/配置（具体取决于服务提供商）

可接受的凭证存储方式：
- 环境变量（例如：`SAFE_EMAIL_IMAP_USERNAME`、`SAFE_EMAIL_IMAP_APP_PASSWORD`）
- 操作系统钥匙链/凭证存储库
- 安全配置文件
- OAuth令牌存储库

**政策说明**：
- 必须提供凭证；凭证的来源可以灵活选择。
- 建议使用操作系统钥匙链或安全配置文件来存储凭证，而非明文形式。
- 绝不要在技能包内部存储明文凭证。

## 用户需要事先了解的信息：

1. **使用专用的电子邮件收件箱**（推荐使用全新的Gmail账户）进行AI处理。
   - 请勿将此收件箱与个人主要收件箱关联。
   - 请确保该收件箱仅用于自动化处理转发的邮件。

2. **在请求助手处理邮件之前，请先将邮件转发到该专用收件箱**。
   - 如果用户未转发邮件，则可能没有内容可供处理。
   - 请在用户使用说明中明确这一点。

3. **IMAP访问需要Gmail应用程序密码**（适用于已启用两步验证的Gmail账户）。

## 安全规则（不可协商）

1. **未经用户明确指示，切勿自动检查邮件内容**。
   - 不允许后台自动轮询邮件。
   - 除非用户自行设置，否则不进行定期的收件箱扫描。

2. **仅处理必要的内容**。
   - 仅读取与用户请求相关的最新邮件内容。
   **优先选择与请求操作相关的最新邮件**。

3. **是否删除邮件由用户决定**。
   - 默认情况下不删除邮件。
   - 仅在用户明确表示同意后，才会删除邮件（可以全局删除或每次运行后删除）。

4. **在处理不明确的信息时需先询问用户**。
   - 如果邮件中的时间、时区、目标系统或邮件重复等情况不明确，请先询问用户。

## 设置指南（Gmail + IMAP）

### 1) 创建一个专用的Gmail账户

专门为该功能创建一个Gmail收件箱。

### 2) 为该账户启用两步验证

Gmail应用程序密码需要启用两步验证。

### 3) 创建应用程序密码

在Google账户的安全设置中：
- 进入“应用程序密码”设置
- 为Mail/IMAP功能创建一个新的应用程序密码
- 将密码存储在安全凭证管理器或操作系统钥匙链中。

### 4) 配置IMAP/SMTP客户端（示例：Himalaya）

使用标准的Gmail服务器：
- IMAP：`imap.gmail.com:993`（TLS）
- SMTP：`smtp.gmail.com:587`（STARTTLS）

建议使用基于命令或钥匙链的方式来获取凭证，而非明文密码。

**示例（概念性说明）**：
```toml
backend.type = "imap"
backend.host = "imap.gmail.com"
backend.port = 993
backend.encryption.type = "tls"
backend.login = "your-dedicated-inbox@gmail.com"
backend.auth.type = "password"
backend.auth.cmd = "<secure-command-to-read-app-password>"

message.send.backend.type = "smtp"
message.send.backend.host = "smtp.gmail.com"
message.send.backend.port = 587
message.send.backend.encryption.type = "start-tls"
message.send.backend.login = "your-dedicated-inbox@gmail.com"
message.send.backend.auth.type = "password"
message.send.backend.auth.cmd = "<secure-command-to-read-app-password>"
```

## 执行流程

### 第0步 — 需要用户的明确指令

只有在用户发出如下指令时才继续执行：
- “我刚刚转发了一封邮件，请处理它。”
- “阅读最新的转发邮件并创建日历/提醒记录。”

如果没有收到明确指令，请停止操作。

### 第1步 — 仅读取最新的相关邮件

- 列出收件箱中的最新邮件。
- 仅打开与用户请求相关的最新邮件。
- 避免批量读取旧邮件或无关邮件。

### 第2步 — 提取结构化信息

提取以下信息（如果可用）：
- 标题/主题
- 日期/时间
- 时区（如果缺失，请询问用户或使用用户配置的时区）
- 地点
- 链接
- 备注/详细信息（例如确认编号、参与者）
- 操作类型（事件、提醒或两者兼有）

如果日期/时间信息缺失或不明确，请在创建日历/提醒记录之前先询问用户。

### 第2.5步 — 在写入数据前进行安全检查

- 检查是否存在重复的日历/提醒记录（通过标题和日期/时间进行判断）。
- 如果信息准确性较低，请向用户展示预览内容。
- 如果信息准确且用户选择了“自动创建”，则继续操作，并准确报告所写入的内容。

### 第3步 — 在用户指定的系统中创建输出结果

该功能支持多种日历/提醒系统。
用户可以使用自己常用的工具（如Apple Calendar、Google Calendar、Notion任务、Reminders等）来接收结果。

**最低要求的输出内容**：
- **日历事件**：标题、开始时间、结束时间/持续时间、时区、地点、备注
- **提醒/任务**：标题、截止日期/时间（如果已知）、备注、优先级/列表

### 第4步 — 可选：删除处理后的邮件内容

仅当用户启用了删除功能时才执行删除操作（全局删除或每次运行后单独确认）：
1. 将处理后的邮件移至“垃圾桶”。
2. 在支持的情况下永久删除邮件。
3. 向用户确认删除状态。

### 第5步 — 提供简洁的确认信息

包括以下内容：
- 创建了哪些内容（日历事件/提醒）
- 提取的关键信息（时间/地点）
- 是否已执行删除操作（是/否）
- 任何未解决的疑问

## 故障处理方式

- 如果解析邮件失败：提供已提取的部分信息并请求用户确认。
- 如果创建日历/提醒记录失败：不要删除邮件。
- 如果删除操作失败：明确告知用户“邮件已处理但尚未完全删除”，并在用户同意后重新尝试。

## 默认的隐私保护措施：

- 仅允许用户主动触发功能。
- 仅获取最低必要的访问权限。
- 无自动监控行为。
- 仅在用户明确同意的情况下删除邮件。
- 每次运行后都会提供清晰的审计记录。