---
name: bandwidth
description: "带宽：用于支持消息传递、语音通话、电话号码以及紧急服务（如911）的通信资源。"
homepage: https://www.agxntsix.ai
license: MIT
compatibility: Python 3.10+ (stdlib only — no dependencies)
metadata: {"openclaw": {"emoji": "📡", "requires": {"env": ["BANDWIDTH_API_TOKEN", "BANDWIDTH_ACCOUNT_ID"]}, "primaryEnv": "BANDWIDTH_API_TOKEN", "homepage": "https://www.agxntsix.ai"}}
---
# 📡 带宽服务

带宽服务支持消息传递、语音通话、电话号码以及紧急呼叫（911）功能。

## 所需参数

| 参数名 | 是否必填 | 说明 |
|---------|---------|-------------|
| `BANDWIDTH_API_TOKEN` | ✅ | 带宽服务API令牌 |
| `BANDWIDTH_ACCOUNT_ID` | ✅ | 账户ID |

## 快速入门

```bash
# Send SMS/MMS
python3 {{baseDir}}/scripts/bandwidth.py send-message --from <value> --to <value> --text <value> --application-id <value>

# List messages
python3 {{baseDir}}/scripts/bandwidth.py list-messages --from <value> --to <value>

# Create outbound call
python3 {{baseDir}}/scripts/bandwidth.py create-call --from <value> --to <value> --answer-url <value> --application-id <value>

# Get call details
python3 {{baseDir}}/scripts/bandwidth.py get-call <id>

# List phone numbers
python3 {{baseDir}}/scripts/bandwidth.py list-numbers

# Search available numbers
python3 {{baseDir}}/scripts/bandwidth.py search-numbers --area-code <value> --quantity "10"

# Order phone number
python3 {{baseDir}}/scripts/bandwidth.py order-number --numbers "comma-separated"

# List applications
python3 {{baseDir}}/scripts/bandwidth.py list-applications
```

## 输出格式

所有命令默认以JSON格式输出结果。

## 脚本参考

| 脚本名 | 说明 |
|---------|-------------|
| `{baseDir}/scripts/bandwidth.py` | 主要命令行工具（包含所有相关命令） |

## 致谢

该工具由 [M. Abidi](https://www.linkedin.com/in/mohammad-ali-abidi) 和 [agxntsix.ai](https://www.agxntsix.ai) 开发。  
相关视频教程可在 [YouTube](https://youtube.com/@aiwithabidi) 观看，代码源代码可在 [GitHub](https://github.com/aiwithabidi) 获取。  
该工具属于 **AgxntSix Skill Suite** 的一部分，专为 OpenClaw 代理设计。

📅 **需要帮助为您的企业配置 OpenClaw 吗？** [预约免费咨询](https://cal.com/agxntsix/abidi-openclaw)