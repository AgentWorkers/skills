---
name: interclaw
description: 一种安全、有序且经过PGP加密的电子邮件通信机制，用于代理之间的协作，支持通过普通电子邮件进行通信。
homepage: https://github.com/zachlagden/interclaw
user-invocable: true
metadata: {"openclaw":{"emoji":"🦞🔒","requires":{"bins":["gpg"],"anyBins":["himalaya"],"env":["INTERCLAW_EMAIL","INTERCLAW_SMTP_HOST","INTERCLAW_SMTP_PORT","INTERCLAW_SMTP_USER","INTERCLAW_SMTP_PASS","INTERCLAW_IMAP_HOST","INTERCLAW_IMAP_PORT","INTERCLAW_IMAP_USER","INTERCLAW_IMAP_PASS","PGP_PRIVATE_KEY_ID"],"optionalEnv":["INTERCLAW_HOME","INTERCLAW_MAX_MESSAGE_AGE","INTERCLAW_AGENT_ID","INTERCLAW_TRUSTED_FINGERPRINTS","INTERCLAW_SHARED_SECRET","INTERCLAW_POLL_INTERVAL","INTERCLAW_AUTO_ACK","INTERCLAW_LOG_LEVEL","PGP_PASSPHRASE","HIMALAYA_CONFIG"]},"install":[{"id":"gpg-apt","kind":"apt","package":"gnupg","label":"Install GnuPG (apt)","bins":["gpg"],"os":["linux"]},{"id":"gpg-brew","kind":"brew","formula":"gnupg","label":"Install GnuPG (brew)","bins":["gpg"],"os":["darwin"]},{"id":"himalaya-brew","kind":"brew","formula":"himalaya","label":"Install Himalaya (brew)","bins":["himalaya"],"os":["darwin"]},{"id":"himalaya-download","kind":"download","url":"https://github.com/pimalaya/himalaya/releases/tag/v1.1.0","label":"Install Himalaya v1.1.0 (download binary)","bins":["himalaya"],"os":["linux","darwin"]}]}}
---
# InterClaw — 安全的代理间电子邮件通信系统

您当前正在使用 **InterClaw v3**。该功能为每个 OpenClaw 实例提供了通过电子邮件和 PGP 协议实现的安全、加密且有序的通信通道，可以与其他任何 OpenClaw 实例进行通信。

**当您需要与其他代理通信时：**
1. 选择合适的通信方式（例如：`[COORD]`、`[ENCRYPTED]`、`[MULTI]` 等）；
2. 使用辅助脚本进行通信，而不是直接发送原始电子邮件。

## 必须遵守的核心规则：
- **严禁** 向其他代理发送原始电子邮件；
- **始终使用 `interclaw-send` 命令发送消息**；
- **务必使用 `interclaw-receive` 命令验证接收到的消息**；
- **仅信任配置文件中列出的代理指纹（PGP 密钥指纹）**。

## 如何发送消息
```bash
interclaw-send --to recipient@example.com --tag COORD --topic protocol --body "We should update to v3"
```

**多接收者场景：**
```bash
interclaw-send --to "benjamin@...,harvey@..." --tag MULTI --topic opsec --body "..."
```

脚本会自动完成以下操作：
- 为消息分配唯一的 `GlobalSeq` 和 `ConvID/ConvSeq`；
- 添加所有必要的邮件头信息；
- 对消息进行 PGP 签名（如果选择了 `[ENCRYPTED]` 选项，则会进行加密）；
- 通过 `himalaya` 服务器发送消息。

## 如何接收和处理消息

InterClaw 实际上是一个通信协议与安全层的组合，并非传统的邮件客户端。邮件传输方式是可配置的——您可以根据自己的需求选择合适的接收机制：

### 模式 1：内置的邮件轮询器（最简单的方式）
```bash
interclaw-receive --poll
interclaw-receive --poll --account work
interclaw-receive --once    # single poll for cron
```
使用 `himalaya` 服务器来获取未读邮件。适合初次使用。需要配置 IMAP 信息。

### 模式 2：通过自定义管道接收邮件（推荐用于生产环境）
```bash
interclaw-receive --stdin < /path/to/message.eml
```
您现有的 cron 或 gateway 任务可以直接将新邮件发送到 `interclaw-receive --stdin`。这是最灵活的接收方式，支持 fetchmail、getmail、procmail 等邮件客户端，或任何 MDA（Mail Delivery Agent）工具。无需配置 IMAP。

### 模式 3：直接处理文件
```bash
interclaw-receive --file /var/mail/incoming/msg-001.eml
```
可以直接处理 `.eml` 格式的邮件文件或纯文本邮件文件。同样无需配置 IMAP。

**这三种模式** 都会执行相同的处理流程：仅使用 InterClaw 的过滤规则、PGP 签名验证、邮件头信息检查、消息顺序检测、基于标签的路由以及自动确认机制。

> **强烈建议不要使用 Gmail**。Gmail 的 SMTP 服务会修改 MIME 格式和邮件编码，导致 PGP 签名失效。请改用 Fastmail、Proton Mail Bridge、Migadu 或其他标准的 IMAP 服务提供商。

## 完整的协议文档
请参阅 `docs/protocol-v3.md`（包含在本技能文档中）。

## 安全模型：
- **仅允许通过白名单中的代理进行通信**；
- **每条消息都必须包含有效的 PGP 签名**；
- **禁止使用 HTML 标签、链接以及任何可能执行代码的内容**；
- **系统不会自动信任其他代理的密钥**——所有密钥指纹都需要通过外部方式验证；
- **具体的加密设置由您的配置文件决定**。

## 首次设置：
### 一键启动
```bash
# 1. Bootstrap (installs gpg, himalaya, symlinks scripts to PATH)
./scripts/interclaw-bootstrap

# 2. Initialize (generates PGP key, writes config + himalaya TOML)
interclaw-config init \
  --email donna@example.com \
  --smtp-host smtp.fastmail.com \
  --smtp-pass "app-password" \
  --imap-host imap.fastmail.com \
  --imap-pass "app-password"

# 3. Verify
interclaw-config check
```

IMAP 服务器地址、用户名和密码会自动从 SMTP 配置中获取。代理的标识符会从发送者的电子邮件地址中生成。除非指定了 `--pgp-key-id` 或 `--no-pgp-gen` 参数，否则系统会自动生成 PGP 密钥。

### 与代理建立连接
```bash
interclaw-handshake --peer friend@example.com --fingerprint <expected-fp>
```

连接成功后，可以使用 `--fingerprint` 参数进行额外的身份验证。

## 多代理部署：
如果要在同一台机器上运行多个代理，请为每个代理设置一个唯一的 `INTERCLAW_HOME` 目录。每个代理都将拥有自己的电子邮件地址、PGP 密钥以及独立的状态。

**所有 `interclaw-*` 命令** 在执行前都会检查 `INTERCLAW_HOME` 的设置，以确保使用正确的代理配置。

## 可用的命令：
| 命令          | 功能描述                          |
|----------------|-------------------------------------------|
| `interclaw-bootstrap` | 安装依赖项并将相关脚本链接到系统路径中            |
| `interclaw-send`    | 发送已签名（可选加密）的消息                    |
| `interclaw-receive`   | 处理接收到的邮件（支持轮询、文件或标准输入）            |
| `interclaw-handshake` | 与新的代理建立安全连接（支持重试机制）            |
| `interclaw-status`   | 查看通信记录、确认状态及消息传输间隔              |
| `interclaw-config`    | 管理配置信息和可信代理列表                    |
| `interclaw-setup-polling` | 可选：配置 cron 或 systemd 任务以实现自动轮询            |