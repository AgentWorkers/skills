---
name: shippo
description: "Shippo：提供物流标签生成、运费比较、包裹追踪、地址验证以及退货处理等服务。"
homepage: https://www.agxntsix.ai
license: MIT
compatibility: Python 3.10+ (stdlib only — no dependencies)
metadata: {"openclaw": {"emoji": "📦", "requires": {"env": ["SHIPPO_API_TOKEN"]}, "primaryEnv": "SHIPPO_API_TOKEN", "homepage": "https://www.agxntsix.ai"}}
---
# 📦 Shippo

Shippo 提供了 shipping labels（运输标签）、运费比较、包裹追踪、地址验证以及退货处理等功能。

## 必需条件

| 变量 | 是否必需 | 说明 |
|----------|----------|-------------|
| `SHIPPO_API_TOKEN` | ✅ | Shippo 的 API 令牌 |


## 快速入门

```bash
# Create shipment & get rates
python3 {{baseDir}}/scripts/shippo.py create-shipment --from "JSON address" --to "JSON address" --parcel "JSON"

# List shipments
python3 {{baseDir}}/scripts/shippo.py list-shipments --results "25" --page "1"

# Get shipment details
python3 {{baseDir}}/scripts/shippo.py get-shipment <id>

# Get rates for shipment
python3 {{baseDir}}/scripts/shippo.py get-rates <id>

# Purchase shipping label
python3 {{baseDir}}/scripts/shippo.py purchase-label --rate <value>

# List label transactions
python3 {{baseDir}}/scripts/shippo.py list-transactions --results "25"

# Get label/transaction details
python3 {{baseDir}}/scripts/shippo.py get-transaction <id>

# Track a package
python3 {{baseDir}}/scripts/shippo.py track-package --carrier <value> --tracking-number <value>

# Validate an address
python3 {{baseDir}}/scripts/shippo.py validate-address --name <value> --street1 <value> --city <value> --state <value> --zip <value> --country "US"

# List saved parcels
python3 {{baseDir}}/scripts/shippo.py list-parcels

# Create a parcel template
python3 {{baseDir}}/scripts/shippo.py create-parcel --length <value> --width <value> --height <value> --weight <value>

# Create return shipment
python3 {{baseDir}}/scripts/shippo.py create-return --from "JSON" --to "JSON" --parcel "JSON" --is-return "true"

# List carrier accounts
python3 {{baseDir}}/scripts/shippo.py list-carriers
```


## 输出格式

所有命令默认以 JSON 格式输出结果。


## 脚本参考

| 脚本 | 说明 |
|--------|-------------|
| `{baseDir}/scripts/shippo.py` | 主要的 CLI 工具——集成了所有相关命令 |


## 致谢

该工具由 [M. Abidi](https://www.linkedin.com/in/mohammad-ali-abidi) 和 [agxntsix.ai](https://www.agxntsix.ai) 开发。  
相关视频教程可在 [YouTube](https://youtube.com/@aiwithabidi) 查看，代码源码托管在 [GitHub](https://github.com/aiwithabidi) 上。  
该工具是 **AgxntSix Skill Suite** 的一部分，专为 OpenClaw 代理设计。

📅 **需要帮助为您的业务配置 OpenClaw 吗？** [预约免费咨询](https://cal.com/agxntsix/abidi-openclaw)