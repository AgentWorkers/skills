---
name: usaspending
description: "USAspending.gov：提供联邦政府支出数据、合同信息、拨款详情、获奖项目信息以及相关机构的查询服务。无需使用API密钥即可访问该平台。"
homepage: https://www.agxntsix.ai
license: MIT
compatibility: Python 3.10+ (stdlib only — no dependencies)
metadata: {"openclaw": {"emoji": "🏛️", "requires": {}, "primaryEnv": "", "homepage": "https://www.agxntsix.ai"}}
---
# 🏛️ USAspending

USAspending.gov 提供联邦政府支出数据、合同信息、拨款详情、获奖项目以及相关机构和接收方的查询服务。使用该服务无需 API 密钥。

## 使用要求

基本功能无需 API 密钥即可使用。

## 快速入门

```bash
# Search federal awards
python3 {{baseDir}}/scripts/usaspending.py search-awards --keywords <value> --award-type "contracts" --limit "25" --page "1"

# Get award details
python3 {{baseDir}}/scripts/usaspending.py get-award <id>

# Search recipients
python3 {{baseDir}}/scripts/usaspending.py search-recipients --keyword <value> --limit "25"

# Get recipient details
python3 {{baseDir}}/scripts/usaspending.py get-recipient <id>

# List top-tier agencies
python3 {{baseDir}}/scripts/usaspending.py list-agencies

# Get agency details
python3 {{baseDir}}/scripts/usaspending.py get-agency --code <value>

# Spending by category
python3 {{baseDir}}/scripts/usaspending.py spending-by-category --category "awarding_agency" --filters "JSON"

# Spending over time
python3 {{baseDir}}/scripts/usaspending.py spending-over-time --group "fiscal_year" --filters "JSON"

# List CFDA programs
python3 {{baseDir}}/scripts/usaspending.py list-cfda

# Autocomplete search
python3 {{baseDir}}/scripts/usaspending.py autocomplete --search-text <value>
```

## 输出格式

所有命令默认以 JSON 格式输出结果。

## 脚本参考

| 脚本 | 描述 |
|--------|-------------|
| `{baseDir}/scripts/usaspending.py` | 主要命令行工具（包含所有相关命令） |

## 开发者信息

由 [M. Abidi](https://www.linkedin.com/in/mohammad-ali-abidi) 和 [agxntsix.ai](https://www.agxntsix.ai) 开发  
[YouTube 频道](https://youtube.com/@aiwithabidi) | [GitHub 仓库](https://github.com/aiwithabidi)  
该工具是 **AgxntSix Skill Suite** 的一部分，专为 OpenClaw 代理程序设计。

📅 **需要帮助为您的企业配置 OpenClaw 吗？** [预约免费咨询](https://cal.com/agxntsix/abidi-openclaw)