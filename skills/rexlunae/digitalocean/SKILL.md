---
name: digitalocean
description: 通过 API 管理 DigitalOcean 资源：  
- Droplets（创建/销毁/调整大小/重启）  
- DNS 区域及记录  
- Spaces（对象存储服务）  
- 数据库  
- 防火墙  
- 负载均衡器  
- Kubernetes 集群  
- 以及账户和计费信息。
---

# DigitalOcean API 技能

通过编程方式控制 DigitalOcean 的基础设施：包括虚拟机（Droplets）、DNS、数据库、存储和网络设置。

## 认证

需要使用 API 令牌。请从以下链接获取令牌：  
https://cloud.digitalocean.com/account/api/tokens  
将令牌保存在 `~/.config/digitalocean/token` 文件中（仅保存令牌内容，不要添加换行符）：  
```bash
mkdir -p ~/.config/digitalocean
echo -n "YOUR_API_TOKEN" > ~/.config/digitalocean/token
chmod 600 ~/.config/digitalocean/token
```

## 快速参考

### 虚拟机（Droplets）

```bash
# List all droplets
python3 scripts/digitalocean.py droplets list

# Get droplet details
python3 scripts/digitalocean.py droplets get <droplet_id>

# Create droplet
python3 scripts/digitalocean.py droplets create <name> --region nyc1 --size s-1vcpu-1gb --image ubuntu-24-04-x64

# Power actions
python3 scripts/digitalocean.py droplets power-on <droplet_id>
python3 scripts/digitalocean.py droplets power-off <droplet_id>
python3 scripts/digitalocean.py droplets reboot <droplet_id>

# Resize droplet
python3 scripts/digitalocean.py droplets resize <droplet_id> --size s-2vcpu-4gb

# Snapshot
python3 scripts/digitalocean.py droplets snapshot <droplet_id> --name "backup-2024"

# Destroy droplet
python3 scripts/digitalocean.py droplets destroy <droplet_id>
```

### DNS 管理

```bash
# List domains
python3 scripts/digitalocean.py dns list

# Get domain records
python3 scripts/digitalocean.py dns records <domain>

# Add record
python3 scripts/digitalocean.py dns add <domain> --type A --name www --data 1.2.3.4 --ttl 300

# Update record
python3 scripts/digitalocean.py dns update <domain> <record_id> --data 5.6.7.8

# Delete record
python3 scripts/digitalocean.py dns delete <domain> <record_id>

# Add domain
python3 scripts/digitalocean.py dns create <domain>
```

### 防火墙

```bash
# List firewalls
python3 scripts/digitalocean.py firewalls list

# Create firewall
python3 scripts/digitalocean.py firewalls create <name> --inbound tcp:22:0.0.0.0/0 --inbound tcp:80:0.0.0.0/0 --inbound tcp:443:0.0.0.0/0

# Add droplet to firewall
python3 scripts/digitalocean.py firewalls add-droplet <firewall_id> <droplet_id>
```

### 对象存储（Spaces）

```bash
# List spaces (requires spaces key)
python3 scripts/digitalocean.py spaces list

# Create space
python3 scripts/digitalocean.py spaces create <name> --region nyc3
```

### 数据库

```bash
# List database clusters
python3 scripts/digitalocean.py databases list

# Get database details
python3 scripts/digitalocean.py databases get <db_id>
```

### 账户与计费

```bash
# Account info
python3 scripts/digitalocean.py account

# Balance
python3 scripts/digitalocean.py billing balance

# Billing history
python3 scripts/digitalocean.py billing history
```

### SSH 密钥

```bash
# List SSH keys
python3 scripts/digitalocean.py ssh-keys list

# Add SSH key
python3 scripts/digitalocean.py ssh-keys add <name> --key "ssh-ed25519 AAAA..."
```

### 镜像与快照

```bash
# List available images
python3 scripts/digitalocean.py images list

# List your snapshots
python3 scripts/digitalocean.py images snapshots

# Delete snapshot
python3 scripts/digitalocean.py images delete <image_id>
```

### 地区与实例规格

```bash
# List regions
python3 scripts/digitalocean.py regions

# List droplet sizes
python3 scripts/digitalocean.py sizes
```

## DNS 记录类型

支持的 DNS 记录类型：  
- `A` — IPv4 地址  
- `AAAA` — IPv6 地址  
- `CNAME` — 典型名称（别名）  
- `MX` — 邮件交换记录（需要指定优先级）  
- `TXT` — 文本记录  
- `NS` — 名称服务器  
- `SRV` — 服务记录  
- `CAA` — 证书颁发机构授权记录  

## 常见工作流程

### 部署新服务器

```bash
# 1. Create droplet
python3 scripts/digitalocean.py droplets create myserver --region nyc1 --size s-1vcpu-2gb --image ubuntu-24-04-x64 --ssh-keys <key_id>

# 2. Get IP address
python3 scripts/digitalocean.py droplets get <droplet_id>

# 3. Add DNS record
python3 scripts/digitalocean.py dns add mydomain.com --type A --name @ --data <ip>

# 4. Set up firewall
python3 scripts/digitalocean.py firewalls create web-server --inbound tcp:22:0.0.0.0/0 --inbound tcp:80:0.0.0.0/0 --inbound tcp:443:0.0.0.0/0
python3 scripts/digitalocean.py firewalls add-droplet <fw_id> <droplet_id>
```

### 将 DNS 服务迁移到 DigitalOcean

```bash
# 1. Add domain
python3 scripts/digitalocean.py dns create example.com

# 2. Add records
python3 scripts/digitalocean.py dns add example.com --type A --name @ --data 1.2.3.4
python3 scripts/digitalocean.py dns add example.com --type CNAME --name www --data example.com.

# 3. Update nameservers at registrar to:
#    ns1.digitalocean.com
#    ns2.digitalocean.com
#    ns3.digitalocean.com
```

## 直接使用 API 进行操作

对于脚本未涵盖的操作，可以直接通过 API 进行操作：  
```bash
TOKEN=$(cat ~/.config/digitalocean/token)
curl -H "Authorization: Bearer $TOKEN" \
     -H "Content-Type: application/json" \
     https://api.digitalocean.com/v2/droplets
```

## API 文档

- 完整的 API 参考文档：https://docs.digitalocean.com/reference/api/  
- API v2 的基础 URL：https://api.digitalocean.com/v2/  

## 常见虚拟机规格

| 规格名称 | CPU 核心数 | 内存（RAM） | 磁盘空间（Disk） | 每月价格（Price/mo） |
|------------|-------------|----------------|------------------|----------------------|
| s-1vcpu-512mb-10gb | 1          | 512MB           | 10GB             | $4                   |
| s-1vcpu-1gb      | 1          | 1GB             | 25GB             | $6                   |
| s-1vcpu-2gb      | 1          | 2GB             | 50GB             | $12                   |
| s-2vcpu-2gb      | 2          | 2GB             | 60GB             | $18                   |
| s-2vcpu-4gb      | 2          | 4GB             | 80GB             | $24                   |
| s-4vcpu-8gb      | 4          | 8GB             | 160GB             | $48                   |

## 常见地区

| 地区名称       | 所在位置       |
|--------------|-------------|
| nyc1, nyc3      | 纽约          |
| sfo3         | 旧金山        |
| ams3         | 阿姆斯特丹        |
| sgp1         | 新加坡        |
| lon1         | 伦敦          |
| fra1         | 法兰克福        |
| tor1         | 多伦多         |
| blr1         | 班加罗尔        |
| syd1         | 悉尼          |