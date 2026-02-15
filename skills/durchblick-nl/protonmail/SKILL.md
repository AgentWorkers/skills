---
name: protonmail
description: 通过 IMAP 桥接（Proton Bridge 或 Hydroxide）读取、搜索和扫描 ProtonMail 中的邮件。同时提供重要邮件的每日汇总。
metadata: {"clawdbot":{"emoji":"📧","requires":{"bins":["python3"]}}}
---

# ProtonMail 使用技巧

您可以通过 IMAP 访问 ProtonMail，具体方法如下：
- **Proton Bridge**（官方推荐方案）
- **hydroxide**（第三方工具，无界面版本）

## 设置

### 方案 1：Proton Bridge（使用 Docker）

```bash
# Pull and run
docker run -d --name=protonmail-bridge \
  -v protonmail:/root \
  -p 143:143 -p 1025:25 \
  --restart=unless-stopped \
  shenxn/protonmail-bridge

# Initial login (interactive)
docker run --rm -it -v protonmail:/root shenxn/protonmail-bridge init
# Then: login → enter credentials → info (shows bridge password) → exit
```

### 方案 2：hydroxide（无界面版本）

```bash
# Install
git clone https://github.com/emersion/hydroxide.git
cd hydroxide && go build ./cmd/hydroxide

# Login
./hydroxide auth your@email.com

# Run as service
./hydroxide serve
```

## 配置

在 `~/.config/protonmail-bridge/config.env` 文件中创建配置文件：

```bash
PROTONMAIL_HOST=127.0.0.1
PROTONMAIL_PORT=143
PROTONMAIL_USER=your@email.com
PROTONMAIL_PASS=your-bridge-password
```

或者直接设置环境变量。

## 使用方法

```bash
# List mailboxes
protonmail.py mailboxes

# Show recent inbox
protonmail.py inbox --limit 10

# Show unread emails
protonmail.py unread

# Search emails
protonmail.py search "keyword"

# Read specific email
protonmail.py read 123
```

## 日常扫描

`daily-scan.py` 脚本会根据以下条件识别重要邮件：
- 来信人信息（银行、政府机构、学校）
- 紧急关键词（DE/EN/NL）

您可以在脚本中配置相应的规则，或者通过环境变量来设置这些条件。

## ProtonMail 的 Sieve 过滤器

推荐使用的 Sieve 过滤器用于自动分类邮件：

```sieve
require ["fileinto", "imap4flags"];

# Important emails - flag them
if anyof (
    address :contains "From" ["@bank", "@government"],
    header :contains "Subject" ["Urgent", "Dringend", "Belangrijk"]
) {
    addflag "\\Flagged";
}

# Newsletters - auto-read and move
if anyof (
    address :contains "From" "newsletter@",
    address :contains "From" "noreply@"
) {
    addflag "\\Seen";
    fileinto "Newsletter";
    stop;
}
```