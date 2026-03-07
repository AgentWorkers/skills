---
name: telnyx
description: "Telnyx 是一款集语音通信、短信/MMS消息发送、SIP中继、号码管理以及传真功能于一体的综合性通信平台。"
homepage: https://www.agxntsix.ai
license: MIT
compatibility: Python 3.10+ (stdlib only — no dependencies)
metadata: {"openclaw": {"emoji": "☎️", "requires": {"env": ["TELNYX_API_KEY"]}, "primaryEnv": "TELNYX_API_KEY", "homepage": "https://www.agxntsix.ai"}}
---
# ☎️ Telnyx

Telnyx 是一款提供语音通话、短信/MMS消息服务、SIP中继、号码管理以及传真功能的工具。

## 必需条件

| 变量 | 是否必需 | 说明 |
|----------|----------|-------------|
| `TELNYX_API_KEY` | ✅ | Telnyx API 密钥（v2） |


## 快速入门

```bash
# Send SMS/MMS
python3 {{baseDir}}/scripts/telnyx.py send-message --from <value> --to <value> --text <value>

# List messages
python3 {{baseDir}}/scripts/telnyx.py list-messages --page-size "25"

# Create outbound call
python3 {{baseDir}}/scripts/telnyx.py create-call --from <value> --to <value> --connection-id <value>

# List active calls
python3 {{baseDir}}/scripts/telnyx.py list-calls

# Get call details
python3 {{baseDir}}/scripts/telnyx.py get-call <id>

# Hang up call
python3 {{baseDir}}/scripts/telnyx.py hangup-call <id>

# List phone numbers
python3 {{baseDir}}/scripts/telnyx.py list-numbers --page-size "25"

# Search available numbers
python3 {{baseDir}}/scripts/telnyx.py search-numbers --country-code "US" --limit "10"

# Order phone number
python3 {{baseDir}}/scripts/telnyx.py order-number --phone-numbers "JSON array"

# List SIP connections
python3 {{baseDir}}/scripts/telnyx.py list-connections

# Create SIP connection
python3 {{baseDir}}/scripts/telnyx.py create-connection --name <value> --connection-type "ip"

# Send a fax
python3 {{baseDir}}/scripts/telnyx.py send-fax --from <value> --to <value> --media-url <value>

# List faxes
python3 {{baseDir}}/scripts/telnyx.py list-faxes

# Get account balance
python3 {{baseDir}}/scripts/telnyx.py get-balance
```


## 输出格式

所有命令默认以 JSON 格式输出结果。


## 脚本参考

| 脚本 | 说明 |
|--------|-------------|
| `{baseDir}/scripts/telnyx.py` | 主要的 CLI 工具，包含所有命令 |


## 致谢

该工具由 [M. Abidi](https://www.linkedin.com/in/mohammad-ali-abidi) 和 [agxntsix.ai](https://www.agxntsix.ai) 开发。  
相关视频教程可在 [YouTube](https://youtube.com/@aiwithabidi) 查看，代码源码托管在 [GitHub](https://github.com/aiwithabidi) 上。  
Telnyx 是 **AgxntSix Skill Suite** 的一部分，专为 OpenClaw 代理设计。  

📅 **需要帮助为您的业务设置 OpenClaw 吗？** [预约免费咨询](https://cal.com/agxntsix/abidi-openclaw)