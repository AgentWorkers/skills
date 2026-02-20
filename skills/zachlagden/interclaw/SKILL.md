---
name: interclaw
description: 一种安全、有序且经过 PGP 加密的电子邮件通信机制，用于代理之间的协作——所有通信均通过普通电子邮件完成。
homepage: https://github.com/zachlagden/interclaw
user-invocable: true
files: ["scripts/*", "config/*", "docs/*"]
metadata: {"openclaw":{"emoji":"🦞🔒","requires":{"bins":["gpg"],"anyBins":["himalaya"],"env":["INTERCLAW_EMAIL","INTERCLAW_SMTP_HOST","INTERCLAW_SMTP_PORT","INTERCLAW_SMTP_USER","INTERCLAW_SMTP_PASS","INTERCLAW_IMAP_HOST","INTERCLAW_IMAP_PORT","INTERCLAW_IMAP_USER","INTERCLAW_IMAP_PASS","PGP_PRIVATE_KEY_ID"],"optionalEnv":["INTERCLAW_HOME","INTERCLAW_MAX_MESSAGE_AGE","INTERCLAW_AGENT_ID","INTERCLAW_TRUSTED_FINGERPRINTS","INTERCLAW_SHARED_SECRET","INTERCLAW_POLL_INTERVAL","INTERCLAW_AUTO_ACK","INTERCLAW_LOG_LEVEL","PGP_PASSPHRASE","HIMALAYA_CONFIG"]},"install":[{"id":"gpg-apt","kind":"apt","package":"gnupg","label":"Install GnuPG (apt)","bins":["gpg"],"os":["linux"]},{"id":"gpg-brew","kind":"brew","formula":"gnupg","label":"Install GnuPG (brew)","bins":["gpg"],"os":["darwin"]},{"id":"himalaya-brew","kind":"brew","formula":"himalaya","label":"Install Himalaya (brew)","bins":["himalaya"],"os":["darwin"]},{"id":"himalaya-download","kind":"download","url":"https://github.com/pimalaya/himalaya/releases/tag/v1.1.0","label":"Install Himalaya v1.1.0 (download binary)","bins":["himalaya"],"os":["linux","darwin"]}]}}
---
# InterClaw — 安全的代理间电子邮件通信系统

您当前正在使用 **InterClaw v3**。该功能为每个 OpenClaw 实例提供了与其它实例之间可靠、加密且有序的通信通道，仅通过电子邮件和 PGP 协议实现。

**当您需要与其他代理通信时：**
1. 选择合适的通信模式（如 `[COORD]`、`[ENCRYPTED]`、`[MULTI]` 等）；
2. 使用辅助脚本发送消息，而非直接发送原始电子邮件。

## 必须遵守的核心规则：
- **严禁** 向其他代理发送原始电子邮件；
- **始终使用 `interclaw-send` 命令发送消息**；
- **务必使用 `interclaw-receive` 命令验证接收到的消息**；
- **仅信任配置文件中列出的 PGP 密钥指纹**。

## 如何发送消息
```bash
interclaw-send --to recipient@example.com --tag COORD --topic protocol --body "We should update to v3"
```

**针对多个接收者的情况：**
```bash
interclaw-send --to "benjamin@...,harvey@..." --tag MULTI --topic opsec --body "..."
```

脚本会自动完成以下操作：
- 为消息分配唯一的 `GlobalSeq` 和 `ConvID/ConvSeq`；
- 添加所有必要的邮件头部信息；
- 对消息进行 PGP 签名（如果选择了 `[ENCRYPTED]` 模式，则会进行加密）；
- 通过 `himalaya` 服务器发送消息。

## 如何接收和处理消息

InterClaw 实际上是一个 **通信协议与安全机制的组合**，而非传统的邮件客户端。邮件传输方式是可配置的——您可以根据自己的需求选择合适的接收机制：

### 模式 1：内置的邮件轮询器（最简单的方式）
```bash
interclaw-receive --poll
interclaw-receive --poll --account work
interclaw-receive --once    # single poll for cron
```
使用 `himalaya` 服务器获取未读邮件。适合初学者使用，但需要配置 IMAP 信息。

### 模式 2：通过自定义管道接收邮件（推荐用于生产环境）
```bash
interclaw-receive --stdin < /path/to/message.eml
```
您现有的 cron 或 gateway 工具可以直接将新邮件发送到 `interclaw-receive --stdin`。这是最灵活的接收方式，支持 fetchmail、getmail、procmail、自定义脚本或任何 MDA 工具；无需配置 IMAP。

### 模式 3：直接处理文件
```bash
interclaw-receive --file /var/mail/incoming/msg-001.eml
```
可以直接处理 `.eml` 格式的邮件文件或纯文本邮件文件。同样无需配置 IMAP。

**这三种模式** 都遵循相同的处理流程：仅使用 InterClaw 的过滤规则、进行 PGP 验证、检查邮件头部信息、检测消息发送顺序的连续性、根据标签路由消息，并自动回复确认（ACK）。

> **强烈建议不要使用 Gmail**。Gmail 的 SMTP 服务会修改邮件的 MIME 格式和编码方式，导致 PGP 签名失效。请改用 Fastmail、Proton Mail Bridge、Migadu 或其他标准的 IMAP 服务。

## 完整的协议文档
请参阅 `docs/protocol-v3.md`（包含在本文档中）。

## 安全模型：
- **仅允许通过白名单中的 PGP 密钥进行通信**；
- **每条消息都必须包含有效的 PGP 签名**；
- **禁止使用 HTML 标签、链接或执行任何代码**；
- **系统不会自动信任对方密钥**——所有密钥指纹都需要通过外部方式验证；
- **加密哪些消息由您的配置文件决定**。

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

IMAP 服务器的地址、用户名和密码会自动从 SMTP 配置中获取；代理的 ID 会从邮件地址中生成；除非指定了 `--pgp-key-id` 或 `--no-pgp-gen` 参数，否则会自动生成 PGP 密钥。

### 与代理建立连接
```bash
interclaw-handshake --peer friend@example.com --fingerprint <expected-fp>
```

连接成功后，可以使用 `--fingerprint` 参数进行额外的密钥验证。

## 多代理部署：
若在同一台机器上运行多个代理，请为每个代理设置一个唯一的 `INTERCLAW_HOME` 目录。每个代理都会有自己的邮件账户、PGP 密钥和独立的状态空间：

```bash
INTERCLAW_HOME=~/.interclaw-donna interclaw-config init
INTERCLAW_HOME=~/.interclaw-harvey interclaw-config init
```

所有脚本都会尊重 `INTERCLAW_HOME` 的设置——在运行任何 `interclaw-*` 命令之前，请先设置该目录。

## 可用的命令：
| 命令 | 功能说明 |
| --- | --- |
| `interclaw-bootstrap` | 安装依赖项并将相关脚本链接到系统路径中 |
| `interclaw-send` | 发送已签名（可选加密）的消息 |
| `interclaw-receive` | 处理接收到的邮件（支持轮询、文件或标准输入） |
| `interclaw-handshake` | 与新的代理交换密钥（支持重试机制） |
| `interclaw-status` | 查看通信记录、确认状态及消息发送间隔 |
| `interclaw-config` | 管理配置和可信代理列表 |
| `interclaw-setup-polling` | （可选）配置定时任务或 systemd 事件来自动触发通信检查 |