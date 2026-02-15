---
name: himalaya
description: "这是一个用于通过 IMAP/SMTP 管理电子邮件的命令行工具（CLI）。你可以使用 `himalaya` 从终端列表、阅读、撰写、回复、转发、搜索以及整理电子邮件。该工具支持多个账户，并支持使用 MML（MIME 元语言）来编写邮件内容。"
homepage: https://github.com/pimalaya/himalaya
metadata: {"clawdbot":{"emoji":"📧","requires":{"bins":["himalaya"]},"install":[{"id":"brew","kind":"brew","formula":"himalaya","bins":["himalaya"],"label":"Install Himalaya (brew)"}]}}
---

# Himalaya 邮件命令行工具（Himalaya Email CLI）

Himalaya 是一个命令行（CLI）邮件客户端，允许您通过终端使用 IMAP、SMTP、Notmuch 或 Sendmail 后端来管理邮件。

## 参考资料

- `references/configuration.md`（配置文件设置及 IMAP/SMTP 认证）
- `references/message-composition.md`（用于编写邮件的 MML 语法）

## 先决条件

1. 已安装 Himalaya CLI（运行 `himalaya --version` 可以验证安装情况）
2. 在 `~/.config/himalaya/config.toml` 文件中配置好相关设置
3. 已配置好 IMAP/SMTP 的凭据（密码需妥善保管）

## 配置设置

运行交互式向导来设置账户：
```bash
himalaya account configure
```

或者手动创建 `~/.config/himalaya/config.toml` 文件：
```toml
[accounts.personal]
email = "you@example.com"
display-name = "Your Name"
default = true

backend.type = "imap"
backend.host = "imap.example.com"
backend.port = 993
backend.encryption.type = "tls"
backend.login = "you@example.com"
backend.auth.type = "password"
backend.auth.cmd = "pass show email/imap"  # or use keyring

message.send.backend.type = "smtp"
message.send.backend.host = "smtp.example.com"
message.send.backend.port = 587
message.send.backend.encryption.type = "start-tls"
message.send.backend.login = "you@example.com"
message.send.backend.auth.type = "password"
message.send.backend.auth.cmd = "pass show email/smtp"
```

## 常用操作

### 列出文件夹
```bash
himalaya folder list
```

### 列出邮件

- 列出收件箱中的邮件（默认行为）：
```bash
himalaya envelope list
```

- 列出特定文件夹中的邮件：
```bash
himalaya envelope list --folder "Sent"
```

- 分页列出邮件：
```bash
himalaya envelope list --page 1 --page-size 20
```

### 搜索邮件
```bash
himalaya envelope list from john@example.com subject meeting
```

### 阅读邮件

- 按邮件 ID 阅读邮件（显示纯文本）：
```bash
himalaya message read 42
```

- 导出原始 MIME 格式的邮件：
```bash
himalaya message export 42 --full
```

### 回复邮件

- 交互式回复（会打开指定的文本编辑器）：
```bash
himalaya message reply 42
```

- 回复所有收件人：
```bash
himalaya message reply 42 --all
```

### 转发邮件
```bash
himalaya message forward 42
```

### 新建邮件

- 交互式编写邮件（会打开指定的文本编辑器）：
```bash
himalaya message write
```

- 使用模板发送邮件：
```bash
cat << 'EOF' | himalaya template send
From: you@example.com
To: recipient@example.com
Subject: Test Message

Hello from Himalaya!
EOF
```

- 或者通过指定邮件头信息发送邮件：
```bash
himalaya message write -H "To:recipient@example.com" -H "Subject:Test" "Message body here"
```

### 移动/复制邮件

- 将邮件移动到其他文件夹：
```bash
himalaya message move 42 "Archive"
```

- 将邮件复制到其他文件夹：
```bash
himalaya message copy 42 "Important"
```

### 删除邮件
```bash
himalaya message delete 42
```

### 管理邮件标记

- 为邮件添加标记：
```bash
himalaya flag add 42 --flag seen
```

- 删除邮件标记：
```bash
himalaya flag remove 42 --flag seen
```

## 多个账户

- 列出所有账户：
```bash
himalaya account list
```

- 使用特定账户：
```bash
himalaya --account work envelope list
```

## 附件

- 保存邮件中的附件：
```bash
himalaya attachment download 42
```

- 将附件保存到指定目录：
```bash
himalaya attachment download 42 --dir ~/Downloads
```

## 输出格式

大多数命令支持使用 `--output` 选项来生成结构化的输出：
```bash
himalaya envelope list --output json
himalaya envelope list --output plain
```

## 调试

- 启用调试日志记录：
```bash
RUST_LOG=debug himalaya envelope list
```

- 查看详细的错误追踪信息（包含堆栈跟踪）：
```bash
RUST_LOG=trace RUST_BACKTRACE=1 himalaya envelope list
```

## 提示

- 使用 `himalaya --help` 或 `himalaya <command> --help` 查看详细的使用说明。
- 邮件 ID 是相对于当前文件夹而言的；更改文件夹后需要重新列出邮件。
- 要编写包含附件的复杂邮件，请使用 MML 语法（参见 `references/message-composition.md`）。
- 请使用 `pass` 命令、系统密钥环或能够安全存储密码的工具来保管密码。