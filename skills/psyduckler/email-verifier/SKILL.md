---
name: email-verifier
description: 通过 SMTP 验证电子邮件地址的送达能力，无需实际发送邮件。该工具会检查 MX 记录，执行 RCPT TO 验证，并识别“收件箱代理”（catch-all）域名。适用于验证电子邮件列表、在发送邮件前确认地址是否存在、清理潜在客户列表或验证联系信息等场景。支持单条邮件验证、批量验证以及 CSV 文件输入。
---
# 电子邮件验证器

该工具通过连接到收件人的邮件服务器来验证电子邮件地址是否可送达，而无需实际发送任何邮件。

## 工作原理

1. **MX 查询** — 查找域名对应的邮件交换服务器（Mail Exchange Server）。
2. **SMTP 握手** — 连接到 MX 服务器的 25 号端口。
3. **RCPT TO 检查** — 询问服务器是否接受该地址的邮件。
4. **“收件箱转发”域名检测** — 通过测试一个随机地址来检测是否存在“收件箱转发”（catch-all）域名。

## 依赖项
```bash
pip3 install dnspython
```

## 使用方法

### 验证单个或多个电子邮件
```bash
python3 scripts/verify_email.py user@example.com another@domain.com
```

### 从标准输入（stdin）验证
```bash
echo "user@example.com" | python3 scripts/verify_email.py --stdin
```

### 从 CSV 文件（例如潜在客户列表）验证
```bash
python3 scripts/verify_email.py --csv leads.csv --email-column "Contact Email"
```

### 命令行参数
- `--helo DOMAIN` — SMTP 问候语中使用的域名（默认：verify.local）
- `--timeout SECONDS` — 连接超时时间（默认：10 秒）

## 输出结果

输出结果将以 JSON 数组的形式显示到标准输出（stdout）。每个结果包含以下信息：
```json
{
  "email": "user@example.com",
  "domain": "example.com",
  "mx_host": "aspmx.l.google.com",
  "smtp_code": 250,
  "smtp_response": "2.1.5 OK",
  "deliverable": "yes"
}
```

### 可送达性判断标准

| 判断结果 | 含义 |
|---------|--------|
| `yes`   | 服务器接受了该地址 |
| `no`    | 服务器拒绝了该地址（地址无效） |
| `catch-all` | 服务器接受所有地址，无法确认收件箱是否存在 |
| `unknown` | 无法确定（可能由于超时、服务器阻止或被列入灰名单） |

## 速率限制

为保护您的 IP 地址的信誉，该脚本内置了速率限制机制：
```bash
# Defaults: 1s between checks, max 20 per domain before 30s pause
python3 scripts/verify_email.py --csv leads.csv --email-column "Contact Email"

# Conservative: slower checks, lower burst limit
python3 scripts/verify_email.py --delay 3 --max-per-domain 10 --burst-pause 60 email@example.com

# Aggressive (not recommended from residential IPs)
python3 scripts/verify_email.py --delay 0.5 --max-per-domain 50 email@example.com
```

### 命令行参数
- `--delay SECONDS` — 每次验证之间的延迟时间（默认：1.0 秒）
- `--max-per-domain N` — 每个域名允许的最大验证次数（默认：20 次）
- `--burst-pause SECONDS` | 达到每个域名最大验证次数后的暂停时间（默认：30 秒）

### 速率限制的重要性

SMTP 验证会直接连接到邮件服务器。如果不使用速率限制，可能会产生以下问题：
- **IP 被列入黑名单** — 邮件服务器（尤其是 Gmail 和 Microsoft）会标记频繁发送 RCPT TO 请求的 IP 地址。一旦被标记，您的 IP 可能会被封锁数小时甚至永久。
- **25 号端口被封锁** — 互联网服务提供商（ISP）会监控 25 号端口的出站流量。异常的请求量可能导致端口被自动封锁。
- **增加被列入灰名单的风险** — 频繁的验证请求会导致服务器返回临时失败结果，从而降低验证的准确性。
- **被视为垃圾邮件行为** — 因为垃圾邮件发送者也会使用类似的方法。合法使用该工具时必须控制请求频率。

### 对代理程序的建议设置

| 使用场景 | 推荐设置 |
|---------|-------------------|
| 快速抽查（1-5 封电子邮件） | 使用默认设置 |
| 小型潜在客户列表（10-50 封电子邮件） | `--delay 2 --max-per-domain 15` |
| 大批量邮件（50-200 封电子邮件） | `--delay 3 --max-per-domain 10 --burst-pause 60` |
| 大规模验证（200 封以上） | 建议使用专用服务（如 ZeroBounce 或 NeverBounce） |

**经验法则**：
- 从住宅 IP 地址发起的验证请求，每天对不同域名的验证次数应控制在 50 次以内。
- 对同一域名进行重复验证时，每次会话中的请求次数应控制在 15 次以内。

## 注意事项

- **“收件箱转发”域名** 会接受所有地址；因此“yes”结果并不能保证收件箱确实存在邮件。
- **部分服务器会阻止 SMTP 验证请求**（可能直接断开连接或超时），导致结果显示为“unknown”。
- **被列入灰名单的服务器** 会暂时拒绝所有验证请求。
- **为避免被封锁，请不要使用同一 IP 地址批量发送验证请求；对于大量邮件列表，建议使用专用服务（如 ZeroBounce 或 NeverBounce）。
- **部分网络环境会封锁 25 号端口**，在这种情况下该工具可能无法正常使用。
- 如果频繁使用该工具，住宅 IP 地址也可能被标记为可疑来源；建议使用专门用于批量验证的服务。