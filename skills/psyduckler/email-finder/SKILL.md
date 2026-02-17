---
name: email-finder
description: 通过结合网站抓取、搜索技巧、模式猜测、DNS分析以及SMTP验证来获取某个域名的电子邮件地址。这些方法可用于潜在客户的开发（prospecting leads）、寻找用于外联的联系方式，或从公司域名中构建联系人列表。如果需要，还可以提供某个人的名字来生成并验证常见的电子邮件地址模式。
---
# 电子邮件查找器

使用多种方法来发现与特定域名关联的电子邮件地址。

## 工作原理

1. **网站抓取** — 获取域名的主页、联系页面、关于页面和团队页面，并通过正则表达式提取电子邮件地址。
2. **目录搜索** — 在目录和搜索引擎中搜索已公开的电子邮件地址。
3. **模式猜测** — 如果提供了姓名，会生成常见的电子邮件格式（如 first@、first.last@、first@last.com 等）。
4. **DNS 指示** — 检查 MX/SPF/DMARC 记录以确定电子邮件服务提供商。
5. **SMTP 验证** — 使用 RCPT TO 命令验证所有找到的或猜测到的电子邮件地址。

## 依赖项

```bash
pip3 install dnspython
```

## 使用方法

### 基本域名搜索
```bash
python3 scripts/find_emails.py example.com
```

### 提供姓名以进行模式猜测
```bash
python3 scripts/find_emails.py example.com --name "John Smith"
```

### 跳过 SMTP 验证
```bash
python3 scripts/find_emails.py example.com --no-verify
```

### 参数选项
- `--name "First Last"` — 为特定人员启用模式猜测功能。
- `--no-verify` — 跳过 SMTP 验证步骤。
- `--timeout SECONDS` — 连接超时时间（默认值：10 秒）。

## 输出结果

输出结果以 JSON 格式显示到标准输出：

```json
{
  "domain": "example.com",
  "provider": "Google Workspace",
  "mx": ["aspmx.l.google.com"],
  "spf": "v=spf1 include:_spf.google.com ~all",
  "dmarc": "v=DMARC1; p=reject; rua=mailto:dmarc@example.com",
  "emails_found": 2,
  "emails": [
    {
      "email": "info@example.com",
      "source": "scraped",
      "deliverable": "yes",
      "smtp_detail": "2.1.5 OK"
    },
    {
      "email": "john.smith@example.com",
      "source": "guessed",
      "deliverable": "catch-all",
      "smtp_detail": "2.1.5 OK"
    }
  ]
}
```

### 数据字段说明

| 字段 | 含义 |
|-------|---------|
| `scraped` | 从域名网站上获取的电子邮件地址 |
| `searched` | 通过搜索或目录查询找到的电子邮件地址 |
| `guessed` | 根据姓名生成的电子邮件地址 |
| `dns` | 从 DNS 记录中获取的电子邮件地址（如 DMARC 报告等） |

### 结果状态

| 字段 | 含义 |
|-------|---------|
| `yes` | 服务器接受了该电子邮件地址 |
| `no` | 服务器拒绝了该电子邮件地址（无效） |
| `catch-all` | 服务器接受了所有地址 |
| `unknown` | 无法确定该地址的状态 |
| `not_checked` | 验证步骤被跳过 |

## 速率限制

该脚本在每个阶段都内置了速率限制机制，以保护您的 IP 地址：

```bash
# Defaults: 0.5s between page fetches, 2s between SMTP checks, max 15 SMTP checks
python3 scripts/find_emails.py example.com --name "John Smith"

# Conservative settings for sensitive environments
python3 scripts/find_emails.py example.com --scrape-delay 1.0 --smtp-delay 4 --max-smtp-checks 8

# Just scrape, no SMTP (zero risk)
python3 scripts/find_emails.py example.com --no-verify
```

### 参数选项
- `--scrape-delay SECONDS` — 在获取网站页面之间添加延迟（默认值：0.5 秒）。
- `--smtp-delay SECONDS` — 在进行 SMTP 验证之间添加延迟（默认值：2.0 秒）。
- `--max-smtp-checks N` — 每次运行时允许的最大 SMTP 验证次数（默认值：15 次）。超出次数的地址将被标记为 `not_checked` 状态。

## 速率限制的重要性

该工具会同时访问网站服务器和邮件服务器。如果没有速率限制：
- **网站抓取** — 过度的爬取行为可能导致您的 IP 被 WAF（如 Cloudflare）阻止，从而被视为机器人程序。适当的延迟可以避免这种情况。
- **SMTP 验证** — 邮件服务器会标记频繁发送 RCPT TO 请求的 IP 地址，可能导致您的 IP 被列入黑名单，影响您发送邮件的能力。
- **家庭/办公 IP 的特殊性** — 与数据中心 IP 不同，您的家庭/办公 IP 会用于所有互联网活动。一旦被列入黑名单，将影响您的所有网络活动。

### 使用建议

| 情况 | 推荐方法 |
|----------|---------------------|
| 单个域名查询 | 使用默认设置即可。 |
| 域名 + 姓名模式猜测 | 使用默认设置（15 次 SMTP 验证足以覆盖所有可能的电子邮件格式）。 |
| 连续查询多个域名 | 在查询不同域名之间添加 5-10 秒的延迟。每天不要查询超过 20 个域名。 |
| 仅需要电子邮件服务提供商的信息 | 使用 `--no-verify` 选项，仅通过 DNS 检查，无风险。 |
| 大量域名查询（50 个以上） | 使用付费服务（如 Hunter.io、Apollo）或分几天进行查询。 |

**关键原则**：该脚本适用于针对性查询，不适合批量抓取数据。如果需要处理大量域名，请使用具有适当 IP 声誉管理的专业服务。

## 限制因素

- 网站抓取依赖于电子邮件地址在页面源代码中可见；无法获取被混淆或通过 JavaScript 动态生成的电子邮件地址。
- 搜索引擎可能会阻止自动化查询。
- SMTP 验证需要使用出站端口 25。
- “catch-all” 邮箱地址会接收所有邮件，因此无法确认收件人的真实邮箱地址。
- 请尊重网站规则：脚本会在请求之间添加延迟，但请避免连续频繁地执行查询。