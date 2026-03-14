---
name: vultr
description: 管理Vultr云基础设施，包括VPS实例、裸机、Kubernetes集群、数据库、DNS、防火墙、VPC（虚拟私有网络）、对象存储等。根据需求，负责部署、管理、列出或修改Vultr资源。具体职责涵盖以下方面：处理VPS实例、裸机资源、Kubernetes集群、数据库、负载均衡器、DNS配置、防火墙设置、VPC配置、快照管理、SSH密钥管理、块存储（Block Storage）和对象存储（Object Storage）的配置，以及预留IP地址（Reserved IP Addresses）的分配。同时，还需处理与计费相关的操作。
---
---
name: vultr
version: 1.0.0
description: 用于管理Vultr云基础设施，包括VPS实例、裸机、Kubernetes集群、数据库、DNS、防火墙、VPC、对象存储等。适用于部署、管理、列出或修改Vultr资源的需求。
author: Erwin Evans
tags:
  - vultr
  - cloud
  - infrastructure
  - kubernetes
  - vps
---

# Vultr云基础设施管理

通过Vultr API v2来管理Vultr云资源。

## 设置

设置`VULTR_API_KEY`环境变量，或在命令中传递`--api-key`参数。

API密钥的生成地址：https://my.vultr.com/settings/#settingsapi

## 使用方法

```bash
python3 scripts/vultr.py <resource> <action> [options]
```

## 快速参考

### 账户
```bash
vultr.py account get              # Account info, balance
vultr.py account bgp              # BGP configuration
vultr.py account bandwidth        # Bandwidth usage
```

### 实例（VPS）
```bash
vultr.py instances list                                    # List all instances
vultr.py instances get --id abc123                         # Get instance details
vultr.py instances create --region ewr --plan vc2-1c-1gb --os 174   # Create instance
vultr.py instances start --id abc123                       # Start instance
vultr.py instances stop --id abc123                        # Stop instance
vultr.py instances reboot --id abc123                      # Reboot instance
vultr.py instances delete --id abc123                      # Delete instance
```

### 裸机
```bash
vultr.py bare-metal list                                   # List bare metal
vultr.py bare-metal create --region ewr --plan vbm-4c-32gb --os 174
```

### Kubernetes（VKE）
```bash
vultr.py kubernetes list                                   # List clusters
vultr.py kubernetes create --region ewr --version v1.28 --label my-cluster
vultr.py kubernetes kubeconfig --id abc123                 # Get kubeconfig
vultr.py kubernetes versions                               # Available versions
```

### 数据库
```bash
vultr.py databases plans                                   # List plans
vultr.py databases list                                    # List databases
vultr.py databases create --region ewr --type pg --plan <plan>
```

### DNS
```bash
vultr.py dns list                                          # List domains
vultr.py dns create --domain example.com --ip 192.0.2.1   # Create domain
vultr.py dns records --domain example.com                  # List records
vultr.py dns create-record --domain example.com --record-type A --record-name www --record-data 192.0.2.1
```

### 防火墙
```bash
vultr.py firewall list                                     # List groups
vultr.py firewall create --description "Web servers"
vultr.py firewall rules --id abc123                        # List rules
vultr.py firewall create-rule --id abc123 --ip-type v4 --protocol tcp --port 22 --subnet 10.0.0.0/8
```

### VPC
```bash
vultr.py vpc list                                          # List VPCs
vultr.py vpc create --region ewr --description "Private network" --subnet 10.0.0.0/24
```

### 快照
```bash
vultr.py snapshots list                                    # List snapshots
vultr.py snapshots create --instance-id abc123 --description "Backup"
```

### SSH密钥
```bash
vultr.py ssh-keys list                                     # List keys
vultr.py ssh-keys create --name "my-key" --key "ssh-rsa AAAA..."
```

### 地区与套餐
```bash
vultr.py regions list                                      # List regions
vultr.py plans list                                        # List VPS plans
vultr.py plans bare-metal                                  # Bare metal plans
```

### 块存储
```bash
vultr.py block-storage list                                # List volumes
vultr.py block-storage create --region ewr --size 100 --label "data"
vultr.py block-storage attach --id abc123 --instance xyz789
```

### 对象存储
```bash
vultr.py object-storage clusters                           # List clusters
vultr.py object-storage create --cluster abc123 --label "my-bucket"
```

### 预留IP
```bash
vultr.py reserved-ips list                                 # List reserved IPs
vultr.py reserved-ips create --region ewr --ip-type v4 --label "frontend"
```

### 计费
```bash
vultr.py billing history                                   # Billing history
vultr.py billing invoices                                  # List invoices
vultr.py billing pending-charges                           # Current charges
```

## 常见工作流程

### 部署Web服务器
```bash
# 1. Get available regions and plans
vultr.py regions list
vultr.py plans list

# 2. Create instance with Ubuntu 24.04
vultr.py instances create \
  --region ewr \
  --plan vc2-2c-4gb \
  --os 174 \
  --label "web-server" \
  --hostname "web01" \
  --ipv6 \
  --ssh-keys ssh-key-id

# 3. Configure firewall
vultr.py firewall create --description "Web servers"
vultr.py firewall create-rule --id fw-id --ip-type v4 --protocol tcp --port 22 --subnet your-ip/32
vultr.py firewall create-rule --id fw-id --ip-type v4 --protocol tcp --port 80
vultr.py firewall create-rule --id fw-id --ip-type v4 --protocol tcp --port 443
```

### 创建Kubernetes集群
```bash
# 1. Get available versions
vultr.py kubernetes versions

# 2. Create cluster
vultr.py kubernetes create \
  --region ewr \
  --version v1.28.0 \
  --label "prod-cluster"

# 3. Get kubeconfig
vultr.py kubernetes kubeconfig --id cluster-id > kubeconfig
```

### 设置托管数据库
```bash
# 1. List plans
vultr.py databases plans

# 2. Create PostgreSQL database
vultr.py databases create \
  --region ewr \
  --type pg \
  --plan vdb-1-4-2 \
  --label "prod-db"
```

## 完整API参考

请参阅[references/api-reference.md](references/api-reference.md)以获取完整的端点文档。

## 响应格式

所有命令返回JSON格式的结果。成功响应会包含资源数据；错误响应会包含一个`error`字段，其中包含错误详情。

成功响应示例：
```json
{
  "instance": {
    "id": "abc123",
    "label": "web-server",
    "region": "ewr",
    "status": "active",
    "main_ip": "192.0.2.1"
  }
}
```

错误响应示例：
```json
{
  "error": "Invalid API key",
  "status": 401
}
```
---