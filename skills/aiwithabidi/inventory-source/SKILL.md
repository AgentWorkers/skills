---
name: inventory-source
description: "**库存来源**：支持代发货自动化、供应商管理、产品数据同步以及订单路由功能。"
homepage: https://www.agxntsix.ai
license: MIT
compatibility: Python 3.10+ (stdlib only — no dependencies)
metadata: {"openclaw": {"emoji": "📋", "requires": {"env": ["INVENTORYSOURCE_API_KEY"]}, "primaryEnv": "INVENTORYSOURCE_API_KEY", "homepage": "https://www.agxntsix.ai"}}
---
# 📋 库存管理工具

库存管理工具（Inventory Management Tool）支持自动发货、供应商管理、产品数据同步以及订单路由等功能。

## 必需条件

| 变量          | 是否必需 | 说明                          |
|---------------|---------|-------------------------------------------|
| `INVENTORYSOURCE_API_KEY` | ✅       | 库存管理工具的API密钥                    |

## 快速入门

```bash
# List connected suppliers
python3 {{baseDir}}/scripts/inventory-source.py list-suppliers

# Get supplier details
python3 {{baseDir}}/scripts/inventory-source.py get-supplier <id>

# List products
python3 {{baseDir}}/scripts/inventory-source.py list-products --page "1" --per-page "50"

# Get product details
python3 {{baseDir}}/scripts/inventory-source.py get-product <id>

# Trigger inventory sync
python3 {{baseDir}}/scripts/inventory-source.py sync-inventory

# List orders
python3 {{baseDir}}/scripts/inventory-source.py list-orders --page "1" --status <value>

# Get order details
python3 {{baseDir}}/scripts/inventory-source.py get-order <id>

# Route order to supplier
python3 {{baseDir}}/scripts/inventory-source.py route-order <id>

# List connected stores
python3 {{baseDir}}/scripts/inventory-source.py list-integrations

# Get product feed
python3 {{baseDir}}/scripts/inventory-source.py get-feed <id>
```

## 输出格式

所有命令默认以JSON格式输出结果。

## 脚本参考

| 脚本            | 说明                          |
|-----------------|-------------------------------------------|
| `{baseDir}/scripts/inventory-source.py` | 主要命令行工具（所有功能集成在一个脚本中） |

## 致谢

该工具由[M. Abidi](https://www.linkedin.com/in/mohammad-ali-abidi)和[agxntsix.ai](https://www.agxntsix.ai)共同开发。  
更多信息请访问[YouTube频道](https://youtube.com/@aiwithabidi)或[GitHub仓库](https://github.com/aiwithabidi)。  
本工具属于**AgxntSix Skill Suite**的一部分，专为OpenClaw代理设计。

📅 **需要帮助为您的业务配置OpenClaw吗？** [预约免费咨询](https://cal.com/agxntsix/abidi-openclaw)