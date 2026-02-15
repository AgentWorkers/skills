---
name: ovh
version: 1.0.0
description: 通过 API 管理 OVHcloud 服务。当用户询问关于 OVH 域名、DNS 记录、VPS、云实例、专用服务器、电子邮件、SSL 证书或任何 OVH 服务管理的相关信息时，可以使用该功能。支持资源的列表显示、创建、更新和删除操作。
---

# OVH

您可以通过自带的 `ovh-cli.py` 脚本来管理 OVHcloud 服务。

## 设置

将凭据存储在环境变量中：

```bash
export OVH_ENDPOINT="ovh-ca"  # or ovh-eu, ovh-us, etc.
export OVH_APP_KEY="your-app-key"
export OVH_APP_SECRET="your-app-secret"
export OVH_CONSUMER_KEY="your-consumer-key"
```

**获取凭据：**
1. 访问 https://ca.api.ovh.com/createToken/（或选择 eu/us 变体）
2. 创建具有所需权限的应用程序
3. 通过提供的 URL 验证消费者密钥

**端点：** `ovh-eu`, `ovh-ca`, `ovh-us`, `soyoustart-eu`, `soyoustart-ca`, `kimsufi-eu`, `kimsufi-ca`

## 使用方法

脚本位于 `scripts/ovh-cli.py` 文件中。可使用的命令如下：

```bash
# Account info
ovh-cli.py me

# Domains
ovh-cli.py domains                      # List all domains
ovh-cli.py domain <domain>              # Get domain info
ovh-cli.py domain <domain> renew        # Check renewal info

# DNS (OVH-managed zones, not Cloudflare)
ovh-cli.py dns <domain>                 # List DNS records
ovh-cli.py dns <domain> get <id>        # Get specific record
ovh-cli.py dns <domain> create --type A --subdomain www --target 1.2.3.4 [--ttl 300]
ovh-cli.py dns <domain> update <id> --target 5.6.7.8
ovh-cli.py dns <domain> delete <id>
ovh-cli.py dns <domain> refresh         # Refresh zone (apply changes)

# VPS
ovh-cli.py vps                          # List all VPS
ovh-cli.py vps <name>                   # VPS details
ovh-cli.py vps <name> status            # Current state
ovh-cli.py vps <name> reboot            # Reboot VPS
ovh-cli.py vps <name> start             # Start VPS
ovh-cli.py vps <name> stop              # Stop VPS
ovh-cli.py vps <name> ips               # List IPs

# Cloud Projects
ovh-cli.py cloud                        # List projects
ovh-cli.py cloud <project> instances    # List instances
ovh-cli.py cloud <project> instance <id> # Instance details

# Dedicated Servers
ovh-cli.py dedicated                    # List servers
ovh-cli.py dedicated <name>             # Server details
ovh-cli.py dedicated <name> reboot      # Reboot server

# SSL Certificates
ovh-cli.py ssl                          # List certificates
ovh-cli.py ssl <id>                     # Certificate details

# Bills & Orders
ovh-cli.py bills [--limit N]            # Recent bills
ovh-cli.py orders [--limit N]           # Recent orders
```

## 常用操作模式

**检查域名有效期：**
```bash
ovh-cli.py domain pushp.ovh renew
```

**添加 DNS 记录：**
```bash
ovh-cli.py dns pushp.ovh create --type A --subdomain api --target 203.0.113.50
ovh-cli.py dns pushp.ovh refresh
```

**管理虚拟专用服务器（VPS）：**
```bash
ovh-cli.py vps myvps status
ovh-cli.py vps myvps reboot
```

## 注意事项

- DNS 更改需要执行 `refresh` 操作才能生效
- 使用 `--json` 标志可获取机器可读的输出格式
- 部分操作是异步的；请通过后续调用检查操作状态