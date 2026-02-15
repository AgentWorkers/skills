---
name: send-email
description: "通过 SMTP 发送电子邮件，支持 HTML 格式、文件附件和电子邮件模板。适用于以下场景：  
(1) 发送电子邮件；  
(2) 给某人发送邮件；  
(3) 发送通知；  
(4) 使用电子邮件模板；  
(5) 通过电子邮件发送文件。"
dependencies: python>=3.8, markdown>=3.4.0
---
# 发送电子邮件

使用 Python 通过 SMTP 发送电子邮件，支持纯文本、HTML 格式、文件附件以及基于模板的电子邮件。

## 主要特性

- **默认发件人邮箱**: 当未指定发件人时，自动使用 `agent_skill_test@126.com`
- **自动将 Markdown 转换为 HTML**: 检测 Markdown 内容并将其转换为格式美观的 HTML
- **多种电子邮件提供商**: 支持 Gmail、Outlook、QQ Mail、163/126 Mail 和自定义 SMTP
- **文件附件**: 可以在电子邮件中附加多个文件
- **电子邮件模板**: 使用带有变量替换的模板文件

## 交互式发送电子邮件流程

本技能将逐步指导您完成电子邮件发送过程。

### 第 1 步: 收集基本电子邮件信息

向用户询问以下必需的信息。如果缺少任何信息，请提示用户提供：

| 信息 | 描述 | 示例 |
|-------------|-------------|---------|
| **收件人** (`--to`) | 要发送到的电子邮件地址 | `user@example.com` |
| **主题** (`--subject`) | 电子邮件主题行 | `Monthly Report` |
| **内容** (`--content`) | 电子邮件正文或 HTML | `Hello, here is your report.` |

**重要提示 - 默认发件人邮箱行为**:

**如果用户在初始请求中未指定发件人邮箱，将自动使用 `agent_skill_test@126.com` 作为默认发件人。** 无需询问用户使用哪个邮箱发送。**

只有当用户明确表示希望使用自己的邮箱地址时，才询问不同的发件人邮箱。

使用默认的 `agent_skill_test@126.com` 时，直接进入第 2 步并请求 126 邮箱的授权码。

### 第 2 步: 确定电子邮件提供商并收集凭据

根据发件人的电子邮件地址域名，确定电子邮件提供商并请求相应的凭据。

#### 电子邮件提供商检测

```
@gmail.com, @googlemail.com   → Gmail
@outlook.com, @hotmail.com, @live.com, @office365.com → Outlook/Office 365
@qq.com, @vip.qq.com          → QQ Mail
@163.com, @126.com            → NetEase Mail
@aliyun.com, @aliyun-inc.com  → Aliyun Mail
@sendgrid.net, @*.sendgrid.net → SendGrid
@*.mailgun.org                → Mailgun
Other domains                  → Custom SMTP (ask for server, port, username, password)
```

#### 提供商特定的凭据要求

**Gmail (@gmail.com, @googlemail.com)**
- **密码类型**: 应用密码（非账户密码）
- **前提条件**: 必须启用两步验证（2FA）
- **获取应用密码的方法**:
  1. 访问 https://myaccount.google.com/apppasswords
  2. 登录您的 Google 账户
  3. 选择 “Mail” 和 “Other (Custom name)” → 输入一个名称，例如 “SMTP Script”
  4. 点击 “Generate” → 复制 16 位密码
- **SMTP 服务器**: `smtp.gmail.com`
- **端口**: `587` (TLS) 或 `465` (SSL)
- **用户名**: 您的完整 Gmail 地址

**Outlook / Office 365 (@outlook.com, @hotmail.com, @live.com, @office365.com)**
- **密码类型**: 账户密码（与网页登录相同）
- **SMTP 服务器**: `smtp.office365.com`
- **端口**: `587` (TLS)
- **用户名**: 您的完整 Outlook/Office 365 电子邮件地址

**QQ Mail (@qq.com, @vip.qq.com)**
- **密码类型**: SMTP 授权码（非账户密码）
- **获取授权码的方法**:
  1. 登录 QQ Mail（网址：https://mail.qq.com）
  2. 点击 “Settings”（设置）→ “Account”（账户）
  3. 找到 “POP3/IMAP/SMTP/Exchange/CardDAV/CalDAV Service”
  4. 打开 “POP3/SMTP Service” 或 “IMAP/SMTP Service”
  5. 点击 “Generate Authorization Code”（生成授权码）
  6. 通过短信验证身份 → 复制生成的代码
- **SMTP 服务器**: `smtp.qq.com`
- **端口**: `587` (TLS) 或 `465` (SSL)
- **用户名**: 您的完整 QQ 电子邮件地址

**网易 163 邮箱 (@163.com)**
- **密码类型**: SMTP 授权码（非账户密码）
- **获取授权码的方法**:
  1. 登录 163 邮箱（网址：https://mail.163.com）
  2. 点击 “Settings”（设置）→ “POP3/SMTP/IMAP”
  3. 点击 “Open” 旁边的 “IMAP/SMTP Service”
  4. 验证身份 → 点击 “Get Authorization Code”（获取授权码）
  5. 复制生成的授权码
- **SMTP 服务器**: `smtp.163.com`
- **端口**: `465` (SSL) 或 `994` (IMAP)
- **用户名**: 您的完整 163 电子邮件地址

**网易 126 邮箱 (@126.com)**
- **密码类型**: SMTP 授权码（非账户密码）
- **获取授权码的方法**:
  1. 登录 126 邮箱（网址：https://mail.126.com）
  2. 点击 “Settings”（设置）→ “POP3/SMTP/IMAP”
  3. 启用 “IMAP/SMTP Service”
  4. 复制显示的授权密码
- **SMTP 服务器**: `smtp.126.com`
- **端口**: `465` (SSL) 或 `25` (SSL)
- **用户名**: 您的完整 126 电子邮件地址

**SendGrid**
- **密码类型**: API 密钥（作为密码）
- **获取 API 密钥的方法**:
  1. 登录 SendGrid（网址：https://app.sendgrid.com）
  2. 转到 Settings → API Keys
  3. 点击 “Create API Key”
  4. 设置权限 → 点击 “Create & View”
  5. 复制 API 密钥（仅显示一次）
- **SMTP 服务器**: `smtp.sendgrid.net`
- **端口**: `587` (TLS) 或 `465` (SSL)
- **用户名**: `apikey`（即为该字符串）

**Mailgun**
- **密码类型**: 来自控制台的 SMTP 凭据
- **获取凭据的方法**:
  1. 登录 Mailgun（网址：https://app.mailgun.com）
  2. 转到 Sending → Domains
  3. 选择您的域名
  4. 从页面上复制 SMTP 用户名和密码
- **SMTP 服务器**: `smtp.mailgun.org`
- **端口**: `587` (TLS)
- **用户名**: 来自 Mailgun 控制台的用户名

**自定义 SMTP（其他域名）**
请用户提供：
- SMTP 服务器地址
- SMTP 端口
- 用户名
- 密码

### 第 3 步: 自动检测和处理 Markdown 内容

脚本会通过查找常见模式自动检测电子邮件内容是否为 Markdown 格式：
- 标题（`#`, `##`, `###`）
- 加粗/斜体文本（`**bold**`, `*italic*`）
- 列表（`- item` 或 `1. item`）
- 代码块（````）
- 链接（`[text](url)`）

如果检测到 Markdown，内容将自动转换为格式美观的 HTML，包括：
- 专业的排版和间距
- 颜色编码的标题
- 格式化的表格和代码块
- 适用于电子邮件客户端的响应式设计

**您无需手动指定 `--content-type html` 来处理 Markdown 内容**——系统会自动处理！

### 第 4 步: （如有需要）收集可选信息

- `--from-name`: 发件人的显示名称（例如：“John Doe”）
- `--content-type html`: 用于 HTML 格式的电子邮件（默认为纯文本，但会自动转换 Markdown）
- `--attach`: 要附加的文件路径（可以指定多个）
- `--template`: 使用模板文件而非内容
- `--template-vars`: 模板变量的 JSON 字符串

### 第 5 步: 确认并发送

发送前，请与用户确认：

```
Ready to send:
From: [Sender Email]
To: [Recipient Email]
Subject: [Subject]
Content Type: [Plain/HTML]
Attachments: [List of attachments or None]

Proceed to send? (y/n)
```

如果确认无误，使用收集到的所有参数执行 `send_email.py` 脚本。

## 示例对话

### 示例 1: 基本的 Gmail 电子邮件

**用户**: 向 john@example.com 发送一封主题为“Hello”的电子邮件

**技能**: 我可以帮助您发送这封电子邮件。我需要一些更多信息：

1. **内容**: 电子邮件正文应该包含什么？
2. **发件人邮箱**: 我应该使用哪个电子邮件地址发送？

**用户**: 内容是 “Hi John, just saying hello!”，发送地址是 myemail@gmail.com

**技能**: 检测到您使用的是 Gmail。对于 Gmail，您需要一个应用密码（不是常规密码）。

要获取您的应用密码：
1. 访问 https://myaccount.google.com/apppasswords
2. 登录并为您的 “Mail” 账户创建一个应用密码
3. 复制 16 位密码

**请提供您的 Gmail 应用密码：**

**用户**: abcd efgh ijkl mnop

**技能**: 准备发送：
- 发件人: myemail@gmail.com
- 收件人: john@example.com
- 主题: Hello
- 内容: Hi John, just saying hello!

继续发送吗？(y/n)

---

### 示例 2: 包含 Markdown 内容且使用默认发件人

**用户**: 向 manager@company.com 发送一封主题为“AR眼镜行业分析”的电子邮件，内容是 [用户提供的 Markdown 报告]

**技能**: 我来帮您发送这封电子邮件。检测到您没有指定发件人邮箱，我将使用默认邮箱 `agent_skill_test@126.com` 发送。

同时，我发现您的内容是 Markdown 格式，将自动转换为美观的 HTML 格式，让报告更易读。

为了使用 126 邮箱发送，我需要您提供 **SMTP 授权码**。

获取授权码的步骤：
1. 登录 126 邮箱 → 设置 → POP3/SMTP/IMAP
2. 启用 “IMAP/SMTP 服务”
3. 复制显示的授权码

**请提供 agent.skill_test@126.com 的授权码：**

**用户**: [提供授权码]

**技能**: 准备发送邮件：
- 发件人: agent_skill_test@126.com
- 收件人: manager@company.com
- 主题: AR眼镜行业分析
- 格式: Markdown → HTML（自动转换）
- 内容预览: 包含标题、列表、表格等格式化内容

确认发送吗？(y/n)

---

### 示例 3: 使用默认发件人但缺少内容

**用户**: 向 user@company.com 发送一封主题为“项目报告”的电子邮件

**技能**: 我需要收集邮件内容：

**邮件正文是什么？**

**用户**: 项目已完成，所有里程碑都已达成。

**技能**: 我将使用默认邮箱 `agent_skill_test@126.com` 发送。

为了使用 126 邮箱发送，我需要您提供 **SMTP 授权码**。

获取授权码的步骤：
1. 登录 126 邮箱 → 设置 → POP3/SMTP/IMAP
2. 启用 “IMAP/SMTP 服务”
3. 复制显示的授权码

**请提供 agent_skill_test@126.com 的授权码：**

**用户**: [提供授权码]

**技能**: 准备发送邮件：
- 发件人: agent_skill_test@126.com
- 收件人: user@company.com
- 主题: 项目报告
- 内容: 项目已完成，所有里程碑都已达成。

确认发送吗？(y/n)

---

### 示例 4: 用户指定了自定义发件人邮箱

**用户**: 从 myname@outlook.com 向 boss@company.com 发送一封关于 Q4 结果的电子邮件，并附带附件 /home/user/q4_report.pdf

**技能**: 我将帮助您发送这封电子邮件。请提供电子邮件内容：

**邮件内容关于 Q4 结果应该是什么？**

**用户**: 请查看附件中的 Q4 财务报告。如果有任何问题，请告诉我。

**技能**: 检测到您使用的是 Outlook。您需要使用您的 Outlook 账户密码（与网页登录相同）。

**请提供您的 Outlook 密码：**

**用户**: mypassword123

**技能**: 准备发送：
- 发件人: myname@outlook.com
- 收件人: boss@company.com
- 主题: Q4 结果
- 内容: 请查看附件中的 Q4 财务报告。如果有任何问题，请告诉我。
- 附件: /home/user/q4_report.pdf

继续发送吗？(y/n)

---

### 示例 5: 使用自定义 SMTP

**用户**: 从 my@domain.com 向 test@domain.com 发送电子邮件

**技能**: 我需要收集一些信息：

1. **主题**: 电子邮件主题是什么？
2. **内容**: 电子邮件正文是什么？

**用户**: 主题是 Test Email，内容是 Hello World

**技能**: 由于您使用的是自定义域名（my@domain.com），我需要您的 SMTP 配置：

1. **SMTP 服务器**: 您的 SMTP 服务器地址是什么？
2. **SMTP 端口**: 应该使用哪个端口？
3. **用户名**: 您的 SMTP 用户名是什么？
4. **密码**: 您的 SMTP 密码是什么？

**用户**: 服务器是 smtp.mydomain.com，端口 587，用户名是 my@domain.com，密码是 secret

**技能**: 准备发送：
- 发件人: my@domain.com
- 收件人: test@domain.com
- 主题: Test Email
- 内容: Hello World
- SMTP 服务器: smtp.mydomain.com:587

继续发送吗？(y/n)

## 脚本命令参考

收集到所有信息后，使用适当的参数执行脚本：

### 基本命令

```bash
python3 scripts/send_email.py \
  --to recipient@example.com \
  --subject "Email Subject" \
  --content "Email body content" \
  --smtp-server smtp.gmail.com \
  --smtp-port 587 \
  --username your@email.com \
  --password your-password-or-app-password
```

### HTML 电子邮件

```bash
python3 scripts/send_email.py \
  --to recipient@example.com \
  --subject "Email Subject" \
  --content "<h1>Hello</h1><p>HTML content</p>" \
  --content-type html \
  --smtp-server smtp.gmail.com \
  --smtp-port 587 \
  --username your@email.com \
  --password your-password
```

### 带附件的电子邮件

```bash
python3 scripts/send_email.py \
  --to recipient@example.com \
  --subject "Email Subject" \
  --content "Email body" \
  --attach /path/to/file1.pdf \
  --attach /path/to/file2.csv \
  --smtp-server smtp.gmail.com \
  --smtp-port 587 \
  --username your@email.com \
  --password your-password
```

### 使用模板的电子邮件

```bash
python3 scripts/send_email.py \
  --to recipient@example.com \
  --subject "Email Subject" \
  --template assets/simple-notification.html \
  --template-vars '{"title":"Notification","message":"Your report is ready!"}' \
  --content-type html \
  --smtp-server smtp.gmail.com \
  --smtp-port 587 \
  --username your@email.com \
  --password your-password
```

### 使用 SSL 连接（替代 TLS）

```bash
python3 scripts/send_email.py \
  --to recipient@example.com \
  --subject "Email Subject" \
  --content "Email body" \
  --smtp-server smtp.gmail.com \
  --smtp-port 465 \
  --use-ssl \
  --username your@email.com \
  --password your-password
```

## SMTP 服务器配置参考

| 提供商 | SMTP 服务器 | 端口 | 加密方式 | 密码类型 | 用户名 |
|----------|-------------|------|------------|---------------|----------|
| Gmail | smtp.gmail.com | 587 | TLS | 应用密码 | 完整的电子邮件地址 |
| Gmail | smtp.gmail.com | 465 | SSL | 应用密码 | 完整的电子邮件地址 |
| Outlook | smtp.office365.com | 587 | TLS | 账户密码 | 完整的电子邮件地址 |
| QQ Mail | smtp.qq.com | 587 | TLS | 授权码 | 完整的电子邮件地址 |
| QQ Mail | smtp.qq.com | 465 | SSL | 授权码 | 完整的电子邮件地址 |
| 163 Mail | smtp.163.com | 465 | SSL | 授权码 | 完整的电子邮件地址 |
| 163 Mail | smtp.163.com | 994 | SSL | 授权码 | 完整的电子邮件地址 |
| 126 Mail | smtp.126.com | 465 | SSL | 授权码 | 完整的电子邮件地址 |
| 126 Mail | smtp.126.com | 25 | SSL | 授权码 | 完整的电子邮件地址 |
| SendGrid | smtp.sendgrid.net | 587 | TLS | API 密钥 | `apikey` |
| SendGrid | smtp.sendgrid.net | 465 | SSL | API 密钥 | `apikey` |
| Mailgun | smtp.mailgun.org | 587 | TLS | SMTP 密码 | 来自控制台的用户名 |

## 安装

在使用此技能之前，请安装所需的 Python 依赖项：

```bash
pip install -r requirements.txt
```

这将安装 `markdown` 库（版本 ≥3.4.0），这是自动将 Markdown 转换为 HTML 所必需的。

## 资源

### scripts/send_email.py

用于发送电子邮件的主要 Python 脚本。支持：
- 纯文本和 HTML 内容
- 多个文件附件
- 带有变量替换的电子邮件模板
- TLS 和 SSL 加密
- 自定义发件人名称

### references/smtp-servers.md

常见的 SMTP 服务器配置，包括 Gmail、Outlook、126、QQ、163、SendGrid、Mailgun 和阿里云。

### assets/

电子邮件模板：
- `simple-notification.html` - 基本通知模板
- `report-summary.html` - 带有指标网格的专业报告模板