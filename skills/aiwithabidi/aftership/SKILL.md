---
name: aftership
description: "AfterShip — 提供包裹追踪、配送通知、预计送达日期以及快递公司信息查询服务。"
homepage: https://www.agxntsix.ai
license: MIT
compatibility: Python 3.10+ (stdlib only — no dependencies)
metadata: {"openclaw": {"emoji": "📬", "requires": {"env": ["AFTERSHIP_API_KEY"]}, "primaryEnv": "AFTERSHIP_API_KEY", "homepage": "https://www.agxntsix.ai"}}
---
# 📬 AfterShip

AfterShip 是一个用于包裹追踪、交付通知、预估送达日期以及快递公司信息查询的工具。

## 必需条件

| 变量 | 是否必需 | 说明 |
|----------|----------|-------------|
| `AFTERSHIP_API_KEY` | ✅ | AfterShip 的 API 密钥 |


## 快速入门

```bash
# List all trackings
python3 {{baseDir}}/scripts/aftership.py list-trackings --page "1" --limit "50" --keyword <value>

# Get tracking details
python3 {{baseDir}}/scripts/aftership.py get-tracking --slug <value> --tracking-number <value>

# Create tracking
python3 {{baseDir}}/scripts/aftership.py create-tracking --tracking-number <value> --slug <value> --title <value> --emails <value> --phones <value>

# Delete tracking
python3 {{baseDir}}/scripts/aftership.py delete-tracking --slug <value> --tracking-number <value>

# Retrack expired tracking
python3 {{baseDir}}/scripts/aftership.py retrack --slug <value> --tracking-number <value>

# Detect courier for tracking number
python3 {{baseDir}}/scripts/aftership.py detect-courier --tracking-number <value>

# List all supported couriers
python3 {{baseDir}}/scripts/aftership.py list-couriers

# Get last checkpoint
python3 {{baseDir}}/scripts/aftership.py get-last-checkpoint --slug <value> --tracking-number <value>

# Get notification settings
python3 {{baseDir}}/scripts/aftership.py list-notifications --slug <value> --tracking-number <value>
```

## 输出格式

所有命令默认以 JSON 格式输出结果。

## 脚本参考

| 脚本 | 说明 |
|--------|-------------|
| `{baseDir}/scripts/aftership.py` | 主要的命令行工具（包含所有相关命令） |

## 致谢

由 [M. Abidi](https://www.linkedin.com/in/mohammad-ali-abidi) 和 [agxntsix.ai](https://www.agxntsix.ai) 开发 |
[YouTube](https://youtube.com/@aiwithabidi) | [GitHub](https://github.com/aiwithabidi) |
该工具是 **AgxntSix Skill Suite** 的一部分，专为 OpenClaw 代理设计。

📅 **需要帮助为您的业务设置 OpenClaw 吗？** [预约免费咨询](https://cal.com/agxntsix/abidi-openclaw)