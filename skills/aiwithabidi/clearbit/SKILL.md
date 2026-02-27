---
name: clearbit
description: "Clearbit：用于个人信息补充、企业信息整理、潜在客户挖掘以及网站访问者识别（身份验证）的工具。"
homepage: https://www.agxntsix.ai
license: MIT
compatibility: Python 3.10+ (stdlib only — no dependencies)
metadata: {"openclaw": {"emoji": "🔮", "requires": {"env": ["CLEARBIT_API_KEY"]}, "primaryEnv": "CLEARBIT_API_KEY", "homepage": "https://www.agxntsix.ai"}}
---
# 🔮 Clearbit

Clearbit 是一款用于丰富个人信息、企业信息、潜在客户信息以及识别网站访问者的工具。

## 必需条件

| 变量 | 是否必需 | 说明 |
|----------|----------|-------------|
| `CLEARBIT_API_KEY` | ✅ | Clearbit API 密钥（或 HubSpot Clearbit 密钥） |


## 快速入门

```bash
# Enrich person by email
python3 {{baseDir}}/scripts/clearbit.py enrich-person --email <value>

# Enrich company by domain
python3 {{baseDir}}/scripts/clearbit.py enrich-company --domain <value>

# Combined person + company lookup
python3 {{baseDir}}/scripts/clearbit.py combined-lookup --email <value>

# Prospect/search for leads
python3 {{baseDir}}/scripts/clearbit.py prospect --query "JSON filter object"

# Reveal company by IP address
python3 {{baseDir}}/scripts/clearbit.py reveal --ip <value>

# Find company domain by name
python3 {{baseDir}}/scripts/clearbit.py name-to-domain --name <value>
```

## 输出格式

所有命令默认以 JSON 格式输出结果。

## 脚本参考

| 脚本 | 说明 |
|--------|-------------|
| `{baseDir}/scripts/clearbit.py` | 主 CLI 工具，包含所有相关命令 |


## 致谢

该工具由 [M. Abidi](https://www.linkedin.com/in/mohammad-ali-abidi) 和 [agxntsix.ai](https://www.agxntsix.ai) 开发。  
更多信息请访问 [YouTube](https://youtube.com/@aiwithabidi) 和 [GitHub](https://github.com/aiwithabidi)。  
该工具是 **AgxntSix Skill Suite** 的一部分，专为 OpenClaw 代理设计。

📅 **需要帮助为您的业务设置 OpenClaw 吗？** [预约免费咨询](https://cal.com/agxntsix/abidi-openclaw)