---
name: printful
description: "Printful——提供按需打印产品服务、订单管理、运费计算、原型生成以及店铺管理功能。"
homepage: https://www.agxntsix.ai
license: MIT
compatibility: Python 3.10+ (stdlib only — no dependencies)
metadata: {"openclaw": {"emoji": "👕", "requires": {"env": ["PRINTFUL_API_KEY"]}, "primaryEnv": "PRINTFUL_API_KEY", "homepage": "https://www.agxntsix.ai"}}
---
# 👕 Printful

Printful 提供按需打印服务，包括产品打印、订单管理、运费计算、原型生成以及店铺维护等功能。

## 必需条件

| 变量 | 是否必需 | 说明 |
|----------|----------|-------------|
| `PRINTFUL_API_KEY` | ✅ | Printful 的 API 令牌 |


## 快速入门

```bash
# List sync products
python3 {{baseDir}}/scripts/printful.py list-products --limit "20" --offset "0"

# Get product details
python3 {{baseDir}}/scripts/printful.py get-product <id>

# Create an order
python3 {{baseDir}}/scripts/printful.py create-order --recipient "JSON" --items "JSON array"

# List orders
python3 {{baseDir}}/scripts/printful.py list-orders --limit "20" --offset "0" --status <value>

# Get order details
python3 {{baseDir}}/scripts/printful.py get-order <id>

# Cancel an order
python3 {{baseDir}}/scripts/printful.py cancel-order <id>

# Estimate order costs
python3 {{baseDir}}/scripts/printful.py estimate-costs --recipient "JSON" --items "JSON array"

# Calculate shipping rates
python3 {{baseDir}}/scripts/printful.py get-shipping-rates --recipient "JSON" --items "JSON array"

# Browse product catalog
python3 {{baseDir}}/scripts/printful.py list-catalog --category <value>

# Get catalog product details
python3 {{baseDir}}/scripts/printful.py get-catalog-product <id>

# List mockup templates
python3 {{baseDir}}/scripts/printful.py list-mockup-templates --product-id <value>

# Generate mockup
python3 {{baseDir}}/scripts/printful.py create-mockup --product-id <value> --files "JSON"

# List warehouses
python3 {{baseDir}}/scripts/printful.py list-warehouses

# List supported countries
python3 {{baseDir}}/scripts/printful.py list-countries

# Get store info
python3 {{baseDir}}/scripts/printful.py get-store-info
```


## 输出格式

所有命令默认以 JSON 格式输出结果。

## 脚本参考

| 脚本 | 说明 |
|--------|-------------|
| `{baseDir}/scripts/printful.py` | 主要命令行工具（包含所有 Printful 相关命令） |


## 致谢

由 [M. Abidi](https://www.linkedin.com/in/mohammad-ali-abidi) 和 [agxntsix.ai](https://www.agxntsix.ai) 开发  
[YouTube](https://youtube.com/@aiwithabidi) | [GitHub](https://github.com/aiwithabidi)  
该工具是 **AgxntSix Skill Suite** 的一部分，专为 OpenClaw 代理设计。  

📅 **需要帮助为您的业务设置 OpenClaw 吗？** [预约免费咨询](https://cal.com/agxntsix/abidi-openclaw)