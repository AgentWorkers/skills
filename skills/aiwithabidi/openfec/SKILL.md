---
name: openfec
description: "OpenFEC — 提供竞选财务数据、候选人信息、委员会资料以及捐款查询功能。"
homepage: https://www.agxntsix.ai
license: MIT
compatibility: Python 3.10+ (stdlib only — no dependencies)
metadata: {"openclaw": {"emoji": "🗳️", "requires": {"env": ["FEC_API_KEY"]}, "primaryEnv": "FEC_API_KEY", "homepage": "https://www.agxntsix.ai"}}
---
# 🗳️ OpenFEC

OpenFEC 是一个用于查询竞选财务数据、候选人信息、委员会成员以及捐款记录的工具。

## 使用要求

| 变量 | 是否必需 | 说明 |
|----------|----------|-------------|
| `FEC_API_KEY` | ✅ | FEC API 密钥（或 DEMO_KEY） |


## 快速入门

```bash
# Search candidates
python3 {{baseDir}}/scripts/openfec.py search-candidates --q <value> --office <value> --state <value> --party <value> --cycle <value> --per-page "20"

# Get candidate details
python3 {{baseDir}}/scripts/openfec.py get-candidate <id>

# Get candidate financial totals
python3 {{baseDir}}/scripts/openfec.py candidate-totals <id> --cycle <value>

# Search committees
python3 {{baseDir}}/scripts/openfec.py search-committees --q <value> --committee-type <value> --per-page "20"

# Get committee details
python3 {{baseDir}}/scripts/openfec.py get-committee <id>

# List filings
python3 {{baseDir}}/scripts/openfec.py list-filings --candidate-id <value> --committee-id <value> --per-page "20"

# Search individual contributions
python3 {{baseDir}}/scripts/openfec.py search-contributions --contributor-name <value> --contributor-state <value> --min-amount <value> --max-amount <value> --per-page "20"

# Search disbursements
python3 {{baseDir}}/scripts/openfec.py search-disbursements --committee-id <value> --recipient-name <value> --per-page "20"

# Get election results
python3 {{baseDir}}/scripts/openfec.py election-results --office "president" --cycle <value>

# Totals by entity type
python3 {{baseDir}}/scripts/openfec.py get-totals --cycle <value>
```


## 输出格式

所有命令默认以 JSON 格式输出结果。


## 脚本参考

| 脚本 | 说明 |
|--------|-------------|
| `{baseDir}/scripts/openfec.py` | 主要命令行工具（包含所有可用命令） |


## 致谢

OpenFEC 由 [M. Abidi](https://www.linkedin.com/in/mohammad-ali-abidi) 和 [agxntsix.ai](https://www.agxntsix.ai) 开发。  
相关视频教程可在 [YouTube](https://youtube.com/@aiwithabidi) 观看，代码源代码可在 [GitHub](https://github.com/aiwithabidi) 获取。  
该工具属于 **AgxntSix Skill Suite** 的一部分，专为 OpenClaw 代理设计。

📅 **需要帮助为您的企业配置 OpenClaw 吗？** [预约免费咨询](https://cal.com/agxntsix/abidi-openclaw)