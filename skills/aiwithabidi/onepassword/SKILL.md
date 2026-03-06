---
name: onepassword
description: "1Password Connect：用于服务器端应用程序的密钥库、项目及敏感信息管理工具。"
homepage: https://www.agxntsix.ai
license: MIT
compatibility: Python 3.10+ (stdlib only — no dependencies)
metadata: {"openclaw": {"emoji": "🔐", "requires": {"env": ["OP_CONNECT_TOKEN", "OP_CONNECT_HOST"]}, "primaryEnv": "OP_CONNECT_TOKEN", "homepage": "https://www.agxntsix.ai"}}
---
# 🔐 1Password

1Password Connect — 用于服务器端应用程序的密钥库、项目及秘密管理工具。

## 必需条件

| 变量 | 是否必需 | 说明 |
|----------|----------|-------------|
| `OP_CONNECT_TOKEN` | ✅ | 1Password Connect 令牌 |
| `OP_CONNECT_HOST` | ✅ | 1Password Connect 服务器地址 |

## 快速入门

```bash
# List all vaults
python3 {{baseDir}}/scripts/onepassword.py list-vaults

# Get vault details
python3 {{baseDir}}/scripts/onepassword.py get-vault <id>

# List items in vault
python3 {{baseDir}}/scripts/onepassword.py list-items --vault-id <value>

# Get item with fields
python3 {{baseDir}}/scripts/onepassword.py get-item --vault-id <value> <id>

# Create item
python3 {{baseDir}}/scripts/onepassword.py create-item --vault-id <value> --category "LOGIN" --title <value> --fields "JSON"

# Update item
python3 {{baseDir}}/scripts/onepassword.py update-item --vault-id <value> <id> --fields "JSON"

# Delete item
python3 {{baseDir}}/scripts/onepassword.py delete-item --vault-id <value> <id>

# Check Connect server health
python3 {{baseDir}}/scripts/onepassword.py get-health

# Simple heartbeat check
python3 {{baseDir}}/scripts/onepassword.py get-heartbeat
```

## 输出格式

所有命令默认以 JSON 格式输出。

## 脚本参考

| 脚本 | 说明 |
|--------|-------------|
| `{baseDir}/scripts/onepassword.py` | 主要命令行工具（所有命令集成在一个脚本中） |

## 致谢

由 [M. Abidi](https://www.linkedin.com/in/mohammad-ali-abidi) | [agxntsix.ai](https://www.agxntsix.ai) 开发 |
[YouTube](https://youtube.com/@aiwithabidi) | [GitHub](https://github.com/aiwithabidi) 提供支持 |
该工具是 **AgxntSix Skill Suite** 的一部分，专为 OpenClaw 代理设计。

📅 **需要帮助为您的业务设置 OpenClaw 吗？** [预约免费咨询](https://cal.com/agxntsix/abidi-openclaw)