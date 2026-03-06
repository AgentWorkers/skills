---
name: realtor
description: "Realtor.com — 通过 API 搜索房源信息、房产代理以及房产详情"
homepage: https://www.agxntsix.ai
license: MIT
compatibility: Python 3.10+ (stdlib only — no dependencies)
metadata: {"openclaw": {"emoji": "🏡", "requires": {"env": ["REALTOR_API_KEY"]}, "primaryEnv": "REALTOR_API_KEY", "homepage": "https://www.agxntsix.ai"}}
---
# 🏡 Realtor.com

Realtor.com — 通过API搜索房源、房产代理及房产详情

## 前提条件

| 变量 | 是否必需 | 说明 |
|----------|----------|-------------|
| `REALTOR_API_KEY` | ✅ | 用于Realtor API的RapidAPI密钥 |

## 快速入门

```bash
# Search for-sale listings
python3 {{baseDir}}/scripts/realtor.py search-sale --city <value> --state_code <value> --postal_code <value> --price_min <value> --price_max <value>

# Search rentals
python3 {{baseDir}}/scripts/realtor.py search-rent --city <value> --state_code <value> --postal_code <value>

# Search recently sold
python3 {{baseDir}}/scripts/realtor.py search-sold --city <value> --state_code <value>

# Get property details
python3 {{baseDir}}/scripts/realtor.py property --property_id <value>

# Search agents
python3 {{baseDir}}/scripts/realtor.py agents --city <value> --state_code <value> --name <value>

# Get agent details
python3 {{baseDir}}/scripts/realtor.py agent-get --nrds_id <value>

# Location auto-complete
python3 {{baseDir}}/scripts/realtor.py auto-complete --input <value>
```

## 所有命令

| 命令 | 说明 |
|---------|-------------|
| `search-sale` | 搜索待售房源 |
| `search-rent` | 搜索出租房源 |
| `search-sold` | 搜索已售房源 |
| `property` | 获取房产详情 |
| `agents` | 搜索房产代理 |
| `agent-get` | 获取代理详情 |
| `auto-complete` | 地址自动补全 |

## 输出格式

所有命令默认以JSON格式输出。若需可读的格式化输出，请添加 `--human` 参数。

```bash
python3 {{baseDir}}/scripts/realtor.py <command> --human
```

## 脚本参考

| 脚本 | 说明 |
|--------|-------------|
| `{{baseDir}}/scripts/realtor.py` | 主要命令行工具（包含所有命令） |

## 致谢
由 [M. Abidi](https://www.linkedin.com/in/mohammad-ali-abidi) | [agxntsix.ai](https://www.agxntsix.ai) 开发 |
[YouTube](https://youtube.com/@aiwithabidi) | [GitHub](https://github.com/aiwithabidi) 提供支持 |
本工具属于 **AgxntSix Skill Suite** 的一部分，专为OpenClaw代理设计。

📅 **需要帮助为您的企业设置OpenClaw吗？** [预约免费咨询](https://cal.com/agxntsix/abidi-openclaw)