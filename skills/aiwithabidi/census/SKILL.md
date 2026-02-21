---
name: census
description: "美国人口普查局——提供人口统计信息、人口统计数据、ACS（American Community Survey）数据、经济指标以及地理数据。"
homepage: https://www.agxntsix.ai
license: MIT
compatibility: Python 3.10+ (stdlib only — no dependencies)
metadata: {"openclaw": {"emoji": "📊", "requires": {"env": ["CENSUS_API_KEY"]}, "primaryEnv": "CENSUS_API_KEY", "homepage": "https://www.agxntsix.ai"}}
---
# 📊 人口普查 API

美国人口普查局（US Census Bureau）提供人口统计、人口特征数据（ACS data）、经济指标以及地理信息。

## 使用要求

| 变量 | 是否必需 | 说明 |
|----------|----------|-------------|
| `CENSUS_API_KEY` | ✅ | 人口普查 API 密钥（可选） |

## 快速入门

```bash
# ACS 5-Year estimates
python3 {{baseDir}}/scripts/census.py acs-5yr --get "NAME,B01003_001E" --for "state:*"

# ACS 1-Year estimates
python3 {{baseDir}}/scripts/census.py acs-1yr --get "NAME,B01003_001E" --for "state:*"

# 2020 Decennial Census
python3 {{baseDir}}/scripts/census.py decennial --get "NAME,P1_001N" --for "state:*"

# Population estimates
python3 {{baseDir}}/scripts/census.py population --get "NAME,POP_2022" --for "state:*"

# County Business Patterns
python3 {{baseDir}}/scripts/census.py cbp --get "NAME,ESTAB,EMP" --for "state:*" --naics "72"

# Poverty data
python3 {{baseDir}}/scripts/census.py poverty --get "NAME,B17001_001E,B17001_002E" --for "state:*"

# Median household income
python3 {{baseDir}}/scripts/census.py income --get "NAME,B19013_001E" --for "state:*"

# Housing data
python3 {{baseDir}}/scripts/census.py housing --get "NAME,B25001_001E,B25002_002E,B25002_003E" --for "state:*"

# List available datasets
python3 {{baseDir}}/scripts/census.py list-datasets --year "2022"

# List ACS variables
python3 {{baseDir}}/scripts/census.py list-variables

# List available geographies
python3 {{baseDir}}/scripts/census.py list-geographies
```

## 输出格式

所有命令默认以 JSON 格式输出结果。

## 脚本参考

| 脚本 | 说明 |
|--------|-------------|
| `{baseDir}/scripts/census.py` | 主要命令行工具（CLI），包含所有相关命令 |

## 致谢

本工具由 [M. Abidi](https://www.linkedin.com/in/mohammad-ali-abidi) 和 [agxntsix.ai](https://www.agxntsix.ai) 开发；相关视频教程可在 [YouTube](https://youtube.com/@aiwithabidi) 观看，代码实现托管在 [GitHub](https://github.com/aiwithabidi) 上。  
该工具是 **AgxntSix Skill Suite** 的一部分，专为 OpenClaw 代理程序设计。

📅 **需要帮助为您的企业配置 OpenClaw 吗？** [预约免费咨询](https://cal.com/agxntsix/abidi-openclaw)