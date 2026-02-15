---
name: godaddy
description: GoDaddy API 用于管理 DNS 记录。可用于列出、添加、更新或删除由 GoDaddy 管理的域名上的 DNS 记录。
---

# GoDaddy DNS

用于管理托管在 GoDaddy 上的域名的 DNS 记录。

## 设置

从 GoDaddy 获取 API 凭据：
1. 访问 https://developer.godaddy.com/keys
2. 创建一个新的 API 密钥（生产环境）
3. 记下 API 密钥（Key）和 API 密码（Secret）

将凭据保存到 `~/.clawdbot/clawdbot.json` 文件中：
```json
{
  "skills": {
    "entries": {
      "godaddy": {
        "apiKey": "YOUR_API_KEY",
        "apiSecret": "YOUR_API_SECRET"
      }
    }
  }
}
```

或者通过环境变量设置：`GODADDY_API_KEY=xxx` 和 `GODADDY_API_SECRET=xxx`

## 快速参考

### 列出域名
```bash
{baseDir}/scripts/godaddy.sh domains list
```

### DNS 记录
```bash
# List all DNS records for a domain
{baseDir}/scripts/godaddy.sh dns list <domain>

# List records by type
{baseDir}/scripts/godaddy.sh dns list <domain> --type A
{baseDir}/scripts/godaddy.sh dns list <domain> --type CNAME
{baseDir}/scripts/godaddy.sh dns list <domain> --type TXT
{baseDir}/scripts/godaddy.sh dns list <domain> --type MX

# Get specific record
{baseDir}/scripts/godaddy.sh dns get <domain> <type> <name>

# Add a record
{baseDir}/scripts/godaddy.sh dns add <domain> --type A --name www --data 1.2.3.4 --ttl 3600
{baseDir}/scripts/godaddy.sh dns add <domain> --type CNAME --name blog --data example.com --ttl 3600
{baseDir}/scripts/godaddy.sh dns add <domain> --type TXT --name _dmarc --data "v=DMARC1; p=none" --ttl 3600

# Update a record (replaces existing records with same type+name)
{baseDir}/scripts/godaddy.sh dns update <domain> --type A --name www --data 5.6.7.8 --ttl 3600

# Delete records by type and name
{baseDir}/scripts/godaddy.sh dns delete <domain> --type A --name www
```

## 常见 DNS 记录类型

| 类型 | 用途 |
|------|-------|
| A     | IPv4 地址 |
| AAAA   | IPv6 地址 |
| CNAME  | 别名（指向另一个域名） |
| MX     | 邮件服务器 |
| TXT    | 文本记录（用于 SPF、DKIM 验证等） |
| NS     | 名称服务器 |
| SRV    | 服务记录 |

## 示例

### 添加指向 IP 的子域名
```bash
godaddy.sh dns add example.com --type A --name app --data 192.168.1.1 --ttl 600
```

### 为 www 添加 CNAME 别名
```bash
godaddy.sh dns add example.com --type CNAME --name www --data example.com --ttl 3600
```

### 为域名添加 TXT 记录以进行验证
```bash
godaddy.sh dns add example.com --type TXT --name @ --data "google-site-verification=xxx" --ttl 3600
```

### 添加 MX 记录
```bash
godaddy.sh dns add example.com --type MX --name @ --data "mail.example.com" --ttl 3600 --priority 10
```

## 注意事项

- API 基础地址：`https://api.godaddy.com`
- 认证方式：`Authorization: sso-key {key}:{secret}`
- 符号 `@` 代表根域名
- TTL（生存时间）以秒为单位（大多数记录类型的最低值为 600 秒）
- 请遵守 API 使用限制，避免频繁调用 API