---
name: hostinger
description: 通过 API 管理 Hostinger 账户——包括 VPS 的管理（启动/停止/重启、快照、备份、防火墙、Docker）、DNS 区域管理、域名管理、网站托管以及计费功能。当需要部署服务器、发布内容、管理服务器配置、设置 DNS 或控制任何 Hostinger 服务时，请使用此功能。
---

# Hostinger API 技能

**程序化控制 Hostinger 服务：** VPS 实例、DNS 记录、域名、网站及托管服务。

## 认证

需要 API 令牌。请从以下链接获取令牌：  
https://hpanel.hostinger.com/profile/api  
将令牌保存在 `~/.config/hostinger/token` 文件中（仅保存令牌，不要添加换行符）：  
```bash
mkdir -p ~/.config/hostinger
echo -n "YOUR_API_TOKEN" > ~/.config/hostinger/token
chmod 600 ~/.config/hostinger/token
```

## 快速参考

### VPS 操作  
```bash
# List all VPS instances
python3 scripts/hostinger.py vps list

# Get VPS details
python3 scripts/hostinger.py vps get <vm_id>

# Start/stop/restart VPS
python3 scripts/hostinger.py vps start <vm_id>
python3 scripts/hostinger.py vps stop <vm_id>
python3 scripts/hostinger.py vps restart <vm_id>

# Create/restore snapshots
python3 scripts/hostinger.py vps snapshot-create <vm_id>
python3 scripts/hostinger.py vps snapshot-restore <vm_id>

# View backups
python3 scripts/hostinger.py vps backups <vm_id>
```

### DNS 管理  
```bash
# Get DNS records for domain
python3 scripts/hostinger.py dns get <domain>

# Update DNS records (JSON file with records array)
python3 scripts/hostinger.py dns update <domain> <records.json>

# Reset DNS to defaults
python3 scripts/hostinger.py dns reset <domain>

# DNS snapshots
python3 scripts/hostinger.py dns snapshots <domain>
python3 scripts/hostinger.py dns snapshot-restore <domain> <snapshot_id>
```

### 域名管理  
```bash
# List all domains
python3 scripts/hostinger.py domains list

# Get domain details
python3 scripts/hostinger.py domains get <domain>

# Update nameservers
python3 scripts/hostinger.py domains nameservers <domain> ns1.example.com ns2.example.com

# Check availability
python3 scripts/hostinger.py domains check example.com example.org
```

### 托管服务/网站  
```bash
# List websites
python3 scripts/hostinger.py hosting websites

# List datacenters
python3 scripts/hostinger.py hosting datacenters
```

### 账单管理  
```bash
# View subscriptions
python3 scripts/hostinger.py billing subscriptions

# View payment methods
python3 scripts/hostinger.py billing payment-methods

# View catalog
python3 scripts/hostinger.py billing catalog
```

## DNS 记录格式

在更新 DNS 记录时，需要提供一个 JSON 文件：  
```json
{
  "records": [
    {"type": "A", "name": "@", "value": "1.2.3.4", "ttl": 300},
    {"type": "A", "name": "www", "value": "1.2.3.4", "ttl": 300},
    {"type": "MX", "name": "@", "value": "mail.example.com", "priority": 10, "ttl": 300},
    {"type": "TXT", "name": "@", "value": "v=spf1 include:_spf.google.com ~all", "ttl": 300}
  ]
}
```

## VPS Docker 管理

对于使用 Docker 操作系统的 VPS：  
```bash
# List Docker projects
python3 scripts/hostinger.py docker list <vm_id>

# Deploy from docker-compose.yml URL
python3 scripts/hostinger.py docker deploy <vm_id> <project_name> --url <compose_url>

# Or from local file
python3 scripts/hostinger.py docker deploy <vm_id> <project_name> --file <compose.yml>

# Start/stop/restart project
python3 scripts/hostinger.py docker start <vm_id> <project_name>
python3 scripts/hostinger.py docker stop <vm_id> <project_name>
python3 scripts/hostinger.py docker restart <vm_id> <project_name>

# View logs
python3 scripts/hostinger.py docker logs <vm_id> <project_name>

# Delete project
python3 scripts/hostinger.py docker down <vm_id> <project_name>
```

## VPS 防火墙  

```bash
# List firewalls
python3 scripts/hostinger.py firewall list

# Create firewall
python3 scripts/hostinger.py firewall create <name>

# Add rule
python3 scripts/hostinger.py firewall add-rule <firewall_id> --protocol tcp --port 443 --source 0.0.0.0/0

# Activate on VM
python3 scripts/hostinger.py firewall activate <firewall_id> <vm_id>
```

## 直接使用 API 进行操作

对于脚本未涵盖的操作，可以使用 `curl` 命令进行操作：  
```bash
TOKEN=$(cat ~/.config/hostinger/token)
curl -H "Authorization: Bearer $TOKEN" \
     -H "Content-Type: application/json" \
     https://developers.hostinger.com/api/vps/v1/virtual-machines
```

## API 文档

- 完整的 API 参考文档：https://developers.hostinger.com  
- OpenAPI 规范：https://github.com/hostinger/api/blob/main/openapi.json  
- Python SDK：https://github.com/hostinger/api-python-sdk  
- CLI 工具：https://github.com/hostinger/api-cli  

## 常见工作流程

### 部署网站

1. 获取 VPS ID：`python3 scripts/hostinger.py vps list`  
2. 更新 DNS 记录以指向 VPS：`python3 scripts/hostinger.py dns update domain.com records.json`  
3. 通过 SSH 连接到 VPS 进行部署，或使用 Docker：`python3 scripts/hostinger.py docker deploy <vm_id> mysite --file docker-compose.yml`  

### 保护 VPS 安全

1. 创建防火墙：`python3 scripts/hostinger.py firewall create "web-server"`  
2. 添加 SSH、HTTP、HTTPS 的规则  
3. 激活防火墙：`python3 scripts/hostinger.py firewall activate <fw_id> <vm_id>`  

### 更改前的备份

1. 创建快照：`python3 scripts/hostinger.py vps snapshot-create <vm_id>`  
2. 进行更改  
3. 如有需要，恢复数据：`python3 scripts/hostinger.py vps snapshot-restore <vm_id>`