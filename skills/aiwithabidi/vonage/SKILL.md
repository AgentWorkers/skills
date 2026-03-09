---
name: vonage
description: "Vonage 提供短信服务、语音通话功能，同时支持 API 验证、号码管理以及应用程序管理。"
homepage: https://www.agxntsix.ai
license: MIT
compatibility: Python 3.10+ (stdlib only — no dependencies)
metadata: {"openclaw": {"emoji": "📞", "requires": {"env": ["VONAGE_API_KEY", "VONAGE_API_SECRET"]}, "primaryEnv": "VONAGE_API_KEY", "homepage": "https://www.agxntsix.ai"}}
---
# 📞 Vonage

Vonage 提供短信服务、语音通话功能，以及用于验证 API、管理电话号码和应用的管理工具。

## 必需参数

| 参数 | 是否必填 | 说明 |
|--------|--------|---------|
| `VONAGE_API_KEY` | ✅ | Vonage API 密钥 |
| `VONAGE_API_SECRET` | ✅ | Vonage API 秘钥 |

## 快速入门

```bash
# Send SMS
python3 {{baseDir}}/scripts/vonage.py send-sms --from <value> --to <value> --text <value>

# Search messages
python3 {{baseDir}}/scripts/vonage.py list-messages --date <value> --to <value>

# Create voice call
python3 {{baseDir}}/scripts/vonage.py create-call --to <value> --from <value> --ncco "JSON"

# List calls
python3 {{baseDir}}/scripts/vonage.py list-calls

# Get call details
python3 {{baseDir}}/scripts/vonage.py get-call <id>

# Send verification code
python3 {{baseDir}}/scripts/vonage.py send-verify --number <value> --brand <value>

# Check verification code
python3 {{baseDir}}/scripts/vonage.py check-verify --request-id <value> --code <value>

# List your numbers
python3 {{baseDir}}/scripts/vonage.py list-numbers

# Search available numbers
python3 {{baseDir}}/scripts/vonage.py search-numbers --country "US" --type "mobile-lvn"

# Buy a number
python3 {{baseDir}}/scripts/vonage.py buy-number --country <value> --msisdn <value>

# List applications
python3 {{baseDir}}/scripts/vonage.py list-applications

# Create application
python3 {{baseDir}}/scripts/vonage.py create-application --name <value>

# Get account balance
python3 {{baseDir}}/scripts/vonage.py get-balance
```

## 输出格式

所有命令默认以 JSON 格式输出结果。

## 脚本参考

| 脚本 | 说明 |
|--------|---------|
| `{baseDir}/scripts/vonage.py` | 主要的命令行工具（包含所有相关命令） |

## 致谢

该项目由 [M. Abidi](https://www.linkedin.com/in/mohammad-ali-abidi) 和 [agxntsix.ai](https://www.agxntsix.ai) 共同开发。  
相关视频教程可在 [YouTube](https://youtube.com/@aiwithabidi) 查看，代码源码托管在 [GitHub](https://github.com/aiwithabidi) 上。  
该工具是 **AgxntSix Skill Suite** 的一部分，专为 OpenClaw 代理设计。

📅 **需要帮助为您的业务设置 OpenClaw 吗？** [预约免费咨询](https://cal.com/agxntsix/abidi-openclaw)