---
name: skulk-email
description: >
  **通过 DreamHost 发送/接收电子邮件**  
  - **功能**：可以阅读收件箱、发送电子邮件以及搜索邮件内容。  
  - **使用方式**：无论您使用的是哪种 VPS（包括 DigitalOcean），都可以通过 DreamHost 的 Roundcube Webmail（基于 HTTPS 协议）来发送/接收邮件，从而绕过 SMTP 端口的限制。  
  - **额外功能**：还可以通过 IMAP 协议访问共享的 Gmail 收件箱。  
  - **适用场景**：适用于发送电子邮件、查看收件箱、阅读邮件内容，或为代理设置电子邮件账户。  
  - **依赖软件**：需要安装 `python3`、`curl` 和 `jq`（这些工具必须预先安装在您的服务器上）。  
  - **认证信息**：DreamHost 的邮箱地址和密码存储在 `~/.config/skulk-email/credentials.json` 文件中（使用前请手动创建该文件，详见“设置”部分）。  
  - **注意事项**：无需使用任何第三方服务或 API 密钥。
---
# Skulk 邮件工具

通过 DreamHost 读取和发送电子邮件。可选地，也可以读取共享的 Gmail 收件箱。

**主要功能：**  
- 即使在禁止 SMTP 的 VPS 提供商（如 DigitalOcean）上，也能通过 DreamHost 的 Roundcube Webmail（基于 HTTPS）正常发送邮件。无需使用第三方服务或中继服务。

## 必备条件：  
- **python3**：用于 IMAP 操作  
- **curl**：用于通过 Roundcube Webmail 发送邮件  
- **jq**：用于解析配置文件中的凭据信息  
- **DreamHost 邮箱账号**：包含电子邮件地址和密码  
- **凭据文件**：存储在本地文件 `~/.config/skulk-email/credentials.json` 中（不会被传输到 DreamHost 服务器之外）

## 安全性：  
- 凭据信息仅从本地的 JSON 文件中读取，且具有严格的访问权限（目录权限 700，文件权限 600）  
- 密码仅通过 TLS（IMAP SSL，端口 993）和 HTTPS（端口 443）传输  
- 任何凭据信息都不会被记录、缓存或发送给第三方  
- Roundcube 会话使用的 Cookie 文件是进程级别的，并在程序退出时会被清除

## 设置步骤：  
### 1. 准备 DreamHost 邮箱账号  
您需要一个由 DreamHost 提供的电子邮件地址及其密码。  

### 2. 存储凭据  
```bash
mkdir -p ~/.config/skulk-email && chmod 700 ~/.config/skulk-email
```  
创建文件 `~/.config/skulk-email/credentials.json`：  
```json
{
  "skulk_email": "you@yourdomain.com",
  "skulk_password": "your-dreamhost-mailbox-password",
  "gmail_email": "",
  "gmail_app_password": ""
}
```  
Gmail 相关字段是可选的——如果不需要共享 Gmail 功能，可以留空。  
```bash
chmod 600 ~/.config/skulk-email/credentials.json
```  

### 3. 测试  
```bash
bash scripts/skulk-email.sh test
```  

## 命令使用方法  
```bash
# Test connection
bash scripts/skulk-email.sh test

# Read inbox
bash scripts/skulk-email.sh inbox [limit]

# Check unread count
bash scripts/skulk-email.sh count

# List unread messages
bash scripts/skulk-email.sh unread [limit]

# Read a specific message by ID
bash scripts/skulk-email.sh read <message-id>

# Send email
bash scripts/skulk-email.sh send <to> <subject> <body>

# Search messages
bash scripts/skulk-email.sh search <query> [limit]

# Read shared Gmail inbox (if configured)
bash scripts/skulk-email.sh gmail-inbox [limit]
bash scripts/skulk-email.sh gmail-unread [limit]
bash scripts/skulk-email.sh gmail-count
bash scripts/skulk-email.sh gmail-read <message-id>
```  

## 工作原理：  
- **读取邮件**：直接通过 `imap.dreamhost.com:993`（SSL）或 `imap.gmail.com:993` 进行 IMAP 操作  
- **发送邮件**：通过 HTTPS 进行身份验证，然后通过 Web 界面编写并发送邮件  
- **依赖库**：`python3`、`curl`、`jq`（大多数系统都预装了这些工具）  
- **无需使用 SMTP 端口**：该工具可以在任何允许 HTTPS 的防火墙后正常使用。  

## 为什么不用 SMTP？  
许多 VPS 提供商（如 DigitalOcean，某些 AWS 配置）会永久禁止 outbound SMTP 端口 25、465 和 587 以防止垃圾邮件。而 DreamHost 的 Roundcube Webmail 使用的是 HTTPS（端口 443），因此不会被阻止。该工具实现了 Webmail 的自动登录和发送功能——就像在浏览器中编写邮件一样，只是通过脚本实现而已。  

## 注意事项：  
- 使用新邮箱地址发送的第一封邮件可能会被归类为垃圾邮件。请让收件人标记为“非垃圾邮件”。  
- 请合理控制发送量——这只是一个 Webmail 自动化工具，并非批量发送工具。  
- 凭据信息仅存储在本地文件 `~/.config/skulk-email/` 中，绝不会被泄露。  
- 脚本路径是相对于当前脚本目录的。  

## 致谢：  
该工具由 Skulk 🦊 开发 — [The Human Pattern Lab](https://thehumanpatternlab.com)