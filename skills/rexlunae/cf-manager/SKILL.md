---
name: cloudflare
description: 通过 API 管理 Cloudflare —— 包括 DNS 区域和记录、页面规则、SSL/TLS 设置、缓存、防火墙规则、Workers 以及分析功能。免费 tier 提供 DNS、CDN、DDoS 防护和 SSL 服务。
---

# Cloudflare API 技能

用于管理 Cloudflare 的基础设施：DNS、CDN、安全设置、Workers 等。

## 认证

需要 API 令牌。请从以下链接获取：https://dash.cloudflare.com/profile/api-tokens

**推荐的权限：**
- Zone:Read（读取区域信息）
- Zone:Edit（编辑区域信息）
- Zone:DNS:Read（读取 DNS 记录）
- Zone:DNS:Edit（编辑 DNS 记录）

将令牌保存在 `~/.config/cloudflare/token` 文件中：
```bash
mkdir -p ~/.config/cloudflare
echo -n "YOUR_API_TOKEN" > ~/.config/cloudflare/token
chmod 600 ~/.config/cloudflare/token
```

## 快速参考

### 区域（域名）

```bash
# List all zones
python3 scripts/cloudflare.py zones list

# Get zone details
python3 scripts/cloudflare.py zones get <domain>

# Add new zone
python3 scripts/cloudflare.py zones add <domain>

# Delete zone
python3 scripts/cloudflare.py zones delete <domain>

# Check zone status (pending/active)
python3 scripts/cloudflare.py zones status <domain>

# Purge cache
python3 scripts/cloudflare.py zones purge <domain>
python3 scripts/cloudflare.py zones purge <domain> --urls https://example.com/page
```

### DNS 记录

```bash
# List records for a zone
python3 scripts/cloudflare.py dns list <domain>

# Add record
python3 scripts/cloudflare.py dns add <domain> --type A --name @ --content 1.2.3.4
python3 scripts/cloudflare.py dns add <domain> --type CNAME --name www --content example.com
python3 scripts/cloudflare.py dns add <domain> --type MX --name @ --content mail.example.com --priority 10
python3 scripts/cloudflare.py dns add <domain> --type TXT --name @ --content "v=spf1 include:_spf.google.com ~all"

# Update record
python3 scripts/cloudflare.py dns update <domain> <record_id> --content 5.6.7.8

# Delete record
python3 scripts/cloudflare.py dns delete <domain> <record_id>

# Proxy toggle (orange cloud on/off)
python3 scripts/cloudflare.py dns proxy <domain> <record_id> --on
python3 scripts/cloudflare.py dns proxy <domain> <record_id> --off
```

### SSL/TLS

```bash
# Get SSL mode
python3 scripts/cloudflare.py ssl get <domain>

# Set SSL mode (off, flexible, full, strict)
python3 scripts/cloudflare.py ssl set <domain> --mode full

# Always use HTTPS
python3 scripts/cloudflare.py ssl https <domain> --on
```

### 页面规则

```bash
# List page rules
python3 scripts/cloudflare.py rules list <domain>

# Add redirect rule
python3 scripts/cloudflare.py rules add <domain> --match "example.com/*" --redirect "https://new.com/$1"

# Delete rule
python3 scripts/cloudflare.py rules delete <domain> <rule_id>
```

### 防火墙

```bash
# List firewall rules
python3 scripts/cloudflare.py firewall list <domain>

# Block IP
python3 scripts/cloudflare.py firewall block <domain> --ip 1.2.3.4 --note "Spammer"

# Block country
python3 scripts/cloudflare.py firewall block <domain> --country CN --note "Block China"

# Whitelist IP
python3 scripts/cloudflare.py firewall allow <domain> --ip 1.2.3.4

# Challenge (captcha) for IP range
python3 scripts/cloudflare.py firewall challenge <domain> --ip 1.2.3.0/24
```

### 分析统计

```bash
# Get traffic stats (last 24h)
python3 scripts/cloudflare.py analytics <domain>

# Get stats for date range
python3 scripts/cloudflare.py analytics <domain> --since 2024-01-01 --until 2024-01-31
```

### Workers（无服务器架构）

```bash
# List workers
python3 scripts/cloudflare.py workers list

# Deploy worker
python3 scripts/cloudflare.py workers deploy <name> --script worker.js

# Delete worker
python3 scripts/cloudflare.py workers delete <name>
```

## DNS 记录类型

| 类型 | 用途 | 示例 |
|------|---------|---------|
| A     | IPv4 地址   | 192.0.2.1   |
| AAAA   | IPv6 地址   | 2001:db8::1   |
| CNAME  | 别名     | www → example.com |
| MX     | 邮件服务器 | mail.example.com（优先级 10） |
| TXT    | 文本/验证信息 | v=spf1 ... |
| NS     | 名称服务器 | ns1.example.com |
| SRV    | 服务类型   | _sip._tcp.example.com |
| CAA    | 证书颁发机构 | letsencrypt.org |

## 代理状态（Orange Cloud）

- **Proxied (on)**：流量通过 Cloudflare CDN 处理——实现缓存、DDoS 防护并隐藏源 IP 地址
- **DNS only (off)**：直接连接到源服务器——适用于邮件服务器或非 HTTP 服务

```bash
# Enable proxy
python3 scripts/cloudflare.py dns add example.com --type A --name @ --content 1.2.3.4 --proxied

# Disable proxy (DNS only)
python3 scripts/cloudflare.py dns add example.com --type A --name mail --content 1.2.3.4 --no-proxy
```

## SSL 模式

| 模式 | 描述         |
|------|-------------|
| off    | 不使用 SSL（不推荐）   |
| flexible | HTTPS 到 Cloudflare，HTTP 到源服务器 |
| full    | HTTPS 端到端，源服务器需使用有效证书 |
| strict | HTTPS 端到端，源服务器需使用有效证书 |

## 常见操作流程

### 添加新域名

```bash
# 1. Add zone to Cloudflare
python3 scripts/cloudflare.py zones add example.com

# 2. Note the nameservers (e.g., adam.ns.cloudflare.com, bella.ns.cloudflare.com)

# 3. Update nameservers at your registrar

# 4. Add DNS records
python3 scripts/cloudflare.py dns add example.com --type A --name @ --content 1.2.3.4 --proxied
python3 scripts/cloudflare.py dns add example.com --type CNAME --name www --content example.com --proxied

# 5. Set SSL to strict
python3 scripts/cloudflare.py ssl set example.com --mode strict
```

### 从其他提供商迁移 DNS

```bash
# 1. Add zone (Cloudflare will scan existing records)
python3 scripts/cloudflare.py zones add example.com

# 2. Verify records imported correctly
python3 scripts/cloudflare.py dns list example.com

# 3. Add any missing records
python3 scripts/cloudflare.py dns add example.com --type MX --name @ --content mail.example.com --priority 10

# 4. Update nameservers at registrar

# 5. Wait for propagation, check status
python3 scripts/cloudflare.py zones status example.com
```

### 设置邮件记录

```bash
# MX records
python3 scripts/cloudflare.py dns add example.com --type MX --name @ --content mx1.provider.com --priority 10
python3 scripts/cloudflare.py dns add example.com --type MX --name @ --content mx2.provider.com --priority 20

# SPF
python3 scripts/cloudflare.py dns add example.com --type TXT --name @ --content "v=spf1 include:_spf.provider.com ~all"

# DKIM
python3 scripts/cloudflare.py dns add example.com --type TXT --name selector._domainkey --content "v=DKIM1; k=rsa; p=..."

# DMARC
python3 scripts/cloudflare.py dns add example.com --type TXT --name _dmarc --content "v=DMARC1; p=quarantine; rua=mailto:dmarc@example.com"
```

## 直接 API 访问

```bash
TOKEN=$(cat ~/.config/cloudflare/token)
curl -H "Authorization: Bearer $TOKEN" \
     -H "Content-Type: application/json" \
     https://api.cloudflare.com/client/v4/zones
```

## API 文档

- 完整的 API 参考文档：https://developers.cloudflare.com/api/
- API v4 的基础 URL：https://api.cloudflare.com/client/v4/

## 免费计划包含的内容

- DNS 托管（无限查询次数）
- CDN（在 300 多个边缘节点进行缓存）
- DDoS 防护（无限量使用）
- SSL/TLS 证书（自动续订）
- 3 条页面规则
- 基本防火墙规则
- 分析统计功能

## 名称服务器

当您添加一个域名时，Cloudflare 会自动分配两个名称服务器：
- `adam.ns.cloudflare.com`
- `bella.ns.cloudflare.com`

请在您的域名注册商处更新这些名称服务器信息。区域状态会显示为“pending”，直到名称服务器的更改生效。