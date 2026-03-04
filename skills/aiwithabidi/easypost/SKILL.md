---
name: easypost
description: "EasyPost 提供了多种功能，包括生成运输标签、比较运费、追踪包裹状态、验证收货地址以及购买保险服务。"
homepage: https://www.agxntsix.ai
license: MIT
compatibility: Python 3.10+ (stdlib only — no dependencies)
metadata: {"openclaw": {"emoji": "🚚", "requires": {"env": ["EASYPOST_API_KEY"]}, "primaryEnv": "EASYPOST_API_KEY", "homepage": "https://www.agxntsix.ai"}}
---
# 🚚 EasyPost

EasyPost 提供了邮寄标签生成、运费比较、包裹追踪、地址验证以及保险服务。

## 必需条件

| 变量 | 是否必需 | 说明 |
|----------|----------|-------------|
| `EASYPOST_API_KEY` | ✅ | EasyPost 的 API 密钥 |


## 快速开始

```bash
# Create shipment & get rates
python3 {{baseDir}}/scripts/easypost.py create-shipment --from "JSON address" --to "JSON address" --parcel "JSON"

# Get shipment details
python3 {{baseDir}}/scripts/easypost.py get-shipment <id>

# List shipments
python3 {{baseDir}}/scripts/easypost.py list-shipments --page-size "20"

# Buy label for shipment
python3 {{baseDir}}/scripts/easypost.py buy-shipment <id> --rate-id <value>

# Create a tracker
python3 {{baseDir}}/scripts/easypost.py create-tracker --tracking-code <value> --carrier <value>

# Get tracker details
python3 {{baseDir}}/scripts/easypost.py get-tracker <id>

# List trackers
python3 {{baseDir}}/scripts/easypost.py list-trackers --page-size "20"

# Verify/create address
python3 {{baseDir}}/scripts/easypost.py verify-address --street1 <value> --city <value> --state <value> --zip <value> --country "US"

# Insure a shipment
python3 {{baseDir}}/scripts/easypost.py create-insurance --shipment-id <value> --amount <value>

# Refund a label
python3 {{baseDir}}/scripts/easypost.py create-refund --carrier <value> --tracking-codes "comma-separated"

# List rates for shipment
python3 {{baseDir}}/scripts/easypost.py list-rates <id>

# Create return shipment
python3 {{baseDir}}/scripts/easypost.py create-return --from "JSON" --to "JSON" --parcel "JSON" --is-return "true"
```

## 输出格式

所有命令默认以 JSON 格式输出结果。

## 脚本参考

| 脚本 | 说明 |
|--------|-------------|
| `{baseDir}/scripts/easypost.py` | 主要的命令行工具（包含所有 EasyPost 命令） |

## 致谢

由 [M. Abidi](https://www.linkedin.com/in/mohammad-ali-abidi) 和 [agxntsix.ai](https://www.agxntsix.ai) 开发 |
[YouTube](https://youtube.com/@aiwithabidi) | [GitHub](https://github.com/aiwithabidi) |
该工具是 **AgxntSix Skill Suite** 的一部分，专为 OpenClaw 代理设计。

📅 **需要帮助为您的业务设置 OpenClaw 吗？** [预约免费咨询](https://cal.com/agxntsix/abidi-openclaw)