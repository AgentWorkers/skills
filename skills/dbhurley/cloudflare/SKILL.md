---
name: cloudflare
description: Cloudflare CLI（命令行界面）：用于管理DNS记录、清除缓存以及控制Workers路由的配置。
version: 1.0.0
author: dbhurley
homepage: https://cloudflare.com
metadata:
  clawdis:
    emoji: "🔶"
    requires:
      bins: ["python3", "uv"]
      env:
        - CLOUDFLARE_API_TOKEN
    primaryEnv: CLOUDFLARE_API_TOKEN
---

# Cloudflare CLI

通过API管理Cloudflare的DNS、缓存和Workers服务。

## 🔑 所需的密钥

| 变量 | 说明 | 获取方式 |
|----------|-------------|------------|
| `CLOUDFLARE_API_TOKEN` | 限定的API令牌 | 登录Cloudflare → 我的个人资料 → API令牌 |

**推荐的令牌权限：**
- DNS:Read（读取DNS记录）
- DNS:Edit（编辑DNS记录）
- Cache Purge（清除缓存）
- Workers Routes:Edit（编辑Workers路由）

## ⚙️ 设置

在`~/.clawdis/clawdis.json`文件中进行配置：
```json
{
  "skills": {
    "cloudflare": {
      "env": {
        "CLOUDFLARE_API_TOKEN": "your-token"
      }
    }
  }
}
```

## 📋 命令

### 验证令牌

```bash
# Test that your token works
uv run {baseDir}/scripts/cloudflare.py verify
```

### 区域（域名）

```bash
# List all zones
uv run {baseDir}/scripts/cloudflare.py zones

# Get zone details
uv run {baseDir}/scripts/cloudflare.py zone <zone_id_or_domain>
```

### DNS记录

```bash
# List DNS records for a zone
uv run {baseDir}/scripts/cloudflare.py dns list <domain>

# Add DNS record
uv run {baseDir}/scripts/cloudflare.py dns add <domain> --type A --name www --content 1.2.3.4
uv run {baseDir}/scripts/cloudflare.py dns add <domain> --type CNAME --name blog --content example.com

# Update DNS record
uv run {baseDir}/scripts/cloudflare.py dns update <domain> <record_id> --content 5.6.7.8

# Delete DNS record (asks for confirmation)
uv run {baseDir}/scripts/cloudflare.py dns delete <domain> <record_id>

# Delete without confirmation
uv run {baseDir}/scripts/cloudflare.py dns delete <domain> <record_id> --yes
```

### 缓存

```bash
# Purge everything
uv run {baseDir}/scripts/cloudflare.py cache purge <domain> --all

# Purge specific URLs
uv run {baseDir}/scripts/cloudflare.py cache purge <domain> --urls "https://example.com/page1,https://example.com/page2"

# Purge by prefix
uv run {baseDir}/scripts/cloudflare.py cache purge <domain> --prefix "/blog/"
```

### Workers路由

```bash
# List routes
uv run {baseDir}/scripts/cloudflare.py routes list <domain>

# Add route
uv run {baseDir}/scripts/cloudflare.py routes add <domain> --pattern "*.example.com/*" --worker my-worker
```

## 📤 输出格式

所有命令都支持`--json`选项，以生成机器可读的输出格式：
```bash
uv run {baseDir}/scripts/cloudflare.py dns list example.com --json
```

## 🔗 常见工作流程

### 将域名指向Vercel服务器
```bash
# Add CNAME for apex
cloudflare dns add example.com --type CNAME --name @ --content cname.vercel-dns.com --proxied false

# Add CNAME for www
cloudflare dns add example.com --type CNAME --name www --content cname.vercel-dns.com --proxied false
```

### 部署后清除缓存
```bash
cloudflare cache purge example.com --all
```

## 📦 安装

```bash
clawdhub install cloudflare
```