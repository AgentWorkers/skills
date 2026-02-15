---
name: cloudflare-dns
version: 1.0.0
description: 通过 API 管理 Cloudflare 的 DNS 记录。当用户需要列出、创建、更新或删除 DNS 记录、设置 DDNS、管理 Cloudflare 上的域名或检查 DNS 传播情况时，可以使用此功能。支持 A、AAAA、CNAME、TXT、MX 等类型的 DNS 记录。
---

# Cloudflare DNS

您可以使用随附的 `cf-dns.sh` 脚本，通过 Cloudflare API 来管理 DNS 记录。

## 设置

将凭据存储在环境变量中，或通过命令行参数传递：

```bash
export CF_API_TOKEN="your-api-token"
export CF_ZONE_ID="your-zone-id"       # optional, can auto-detect from domain
```

获取 API 令牌：登录 Cloudflare 控制面板 → 我的资料 → API 令牌 → 创建令牌 → 选择 “编辑区域 DNS” 模板。

获取区域 ID：登录 Cloudflare 控制面板 → 选择域名 → 概览 → 右侧边栏中的 “区域 ID”。

## 使用方法

脚本位于 `scripts/cf-dns.sh` 文件中。所有可用命令如下：

```bash
# List zones (find zone ID)
cf-dns.sh zones

# List all records for a zone
cf-dns.sh list <zone_id>
cf-dns.sh list --domain example.com

# Get specific record
cf-dns.sh get <zone_id> <record_id>

# Create record
cf-dns.sh create <zone_id> --type A --name www --content 1.2.3.4 [--ttl 300] [--proxied]
cf-dns.sh create <zone_id> --type CNAME --name blog --content example.com
cf-dns.sh create <zone_id> --type TXT --name @ --content "v=spf1 ..."
cf-dns.sh create <zone_id> --type MX --name @ --content mail.example.com --priority 10

# Update record
cf-dns.sh update <zone_id> <record_id> --content 5.6.7.8 [--ttl 600] [--proxied]

# Delete record
cf-dns.sh delete <zone_id> <record_id>

# DDNS: update A record to current public IP
cf-dns.sh ddns <zone_id> --name home
cf-dns.sh ddns --domain example.com --name home
```

## 常见操作模式

**添加指向 IP 地址的子域名：**
```bash
cf-dns.sh create <zone_id> --type A --name subdomain --content 203.0.113.50 --proxied
```

**设置电子邮件（MX + SPF）：**
```bash
cf-dns.sh create <zone_id> --type MX --name @ --content mail.example.com --priority 10
cf-dns.sh create <zone_id> --type TXT --name @ --content "v=spf1 include:_spf.google.com ~all"
```

**为家庭服务器配置动态 DNS：**
```bash
# Run periodically via cron
cf-dns.sh ddns --domain example.com --name home
```

## 注意事项：

- `--proxied` 选项会启用 Cloudflare 代理（显示为橙色云图标）——隐藏原始 IP 地址，并启用内容分发网络（CDN）。
- TTL 的单位为秒；在启用代理的情况下，使用 `1` 表示 “自动设置”。
- `@` 表示根域名。
- 脚本会输出 JSON 格式的数据；您可以将输出结果通过 `jq` 工具进行解析。