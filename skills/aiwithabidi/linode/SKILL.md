---
name: linode
description: "Linode（Akamai）——提供计算实例、存储卷、网络服务、NodeBalancers、域名管理以及Kubernetes平台。"
homepage: https://www.agxntsix.ai
license: MIT
compatibility: Python 3.10+ (stdlib only — no dependencies)
metadata: {"openclaw": {"emoji": "☁️", "requires": {"env": ["LINODE_TOKEN"]}, "primaryEnv": "LINODE_TOKEN", "homepage": "https://www.agxntsix.ai"}}
---
# ☁️ Linode/Akamai

Linode (Akamai) 提供计算实例、存储空间、网络服务、NodeBalancers、域名管理以及 Kubernetes 相关功能。

## 必需条件

| 变量 | 是否必需 | 说明 |
|----------|----------|-------------|
| `LINODE_TOKEN` | ✅ | Linode/Akamai 的 API 令牌 |


## 快速入门

```bash
# List Linode instances
python3 {{baseDir}}/scripts/linode.py list-instances --page "1"

# Get instance details
python3 {{baseDir}}/scripts/linode.py get-instance <id>

# Create instance
python3 {{baseDir}}/scripts/linode.py create-instance --type "g6-nanode-1" --region "us-east" --image "linode/ubuntu24.04" --label <value> --root-pass <value>

# Delete instance
python3 {{baseDir}}/scripts/linode.py delete-instance <id>

# Boot instance
python3 {{baseDir}}/scripts/linode.py boot-instance <id>

# Reboot instance
python3 {{baseDir}}/scripts/linode.py reboot-instance <id>

# Shut down instance
python3 {{baseDir}}/scripts/linode.py shutdown-instance <id>

# List volumes
python3 {{baseDir}}/scripts/linode.py list-volumes

# Create volume
python3 {{baseDir}}/scripts/linode.py create-volume --label <value> --size "20" --region "us-east"

# List NodeBalancers
python3 {{baseDir}}/scripts/linode.py list-nodebalancers

# List domains
python3 {{baseDir}}/scripts/linode.py list-domains

# List domain records
python3 {{baseDir}}/scripts/linode.py list-domain-records <id>

# List firewalls
python3 {{baseDir}}/scripts/linode.py list-firewalls

# List LKE clusters
python3 {{baseDir}}/scripts/linode.py list-kubernetes

# List instance types/plans
python3 {{baseDir}}/scripts/linode.py list-types

# List regions
python3 {{baseDir}}/scripts/linode.py list-regions

# List images
python3 {{baseDir}}/scripts/linode.py list-images

# Get account info
python3 {{baseDir}}/scripts/linode.py get-account
```


## 输出格式

所有命令默认以 JSON 格式输出结果。

## 脚本参考

| 脚本 | 说明 |
|--------|-------------|
| `{baseDir}/scripts/linode.py` | 主要的 CLI 工具，集成了所有相关命令 |


## 致谢

本工具由 [M. Abidi](https://www.linkedin.com/in/mohammad-ali-abidi) 和 [agxntsix.ai](https://www.agxntsix.ai) 开发。
[YouTube](https://youtube.com/@aiwithabidi) | [GitHub](https://github.com/aiwithabidi)
该工具是 **AgxntSix Skill Suite** 的一部分，专为 OpenClaw 代理设计。

📅 **需要帮助为您的企业配置 OpenClaw 吗？** [预约免费咨询](https://cal.com/agxntsix/abidi-openclaw)