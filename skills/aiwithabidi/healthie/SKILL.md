---
name: healthie
description: "**Healthie** — 通过 GraphQL API 管理患者信息、预约记录、健康目标以及相关文档。"
homepage: https://www.agxntsix.ai
license: MIT
compatibility: Python 3.10+ (stdlib only — no dependencies)
metadata: {"openclaw": {"emoji": "🏥", "requires": {"env": ["HEALTHIE_API_KEY"]}, "primaryEnv": "HEALTHIE_API_KEY", "homepage": "https://www.agxntsix.ai"}}
---
# 🏥 Healthie

Healthie 是一个通过 GraphQL API 管理患者信息、预约记录、健康目标以及相关文档的工具。

## 必需条件

| 变量 | 是否必需 | 说明 |
|----------|----------|-------------|
| `HEALTHIE_API_KEY` | ✅ | 来自 Healthie 开发者设置的 API 密钥 |

## 快速入门

```bash
# List patients
python3 {{baseDir}}/scripts/healthie.py patients --offset <value> --keywords <value>

# Get patient
python3 {{baseDir}}/scripts/healthie.py patient-get id <value>

# Create patient
python3 {{baseDir}}/scripts/healthie.py patient-create --first_name <value> --last_name <value> --email <value>

# List appointments
python3 {{baseDir}}/scripts/healthie.py appointments --provider_id <value>

# Get appointment
python3 {{baseDir}}/scripts/healthie.py appointment-get id <value>

# Create appointment
python3 {{baseDir}}/scripts/healthie.py appointment-create --patient_id <value> --provider_id <value> --datetime <value>

# Delete appointment
python3 {{baseDir}}/scripts/healthie.py appointment-delete id <value>

# List appointment types
python3 {{baseDir}}/scripts/healthie.py appointment-types
```

## 所有命令

| 命令 | 说明 |
|---------|-------------|
| `patients` | 列出所有患者信息 |
| `patient-get` | 获取指定患者的详细信息 |
| `patient-create` | 创建新患者 |
| `appointments` | 列出所有预约记录 |
| `appointment-get` | 获取指定预约的详细信息 |
| `appointment-create` | 创建新的预约 |
| `appointment-delete` | 删除指定的预约 |
| `appointment-types` | 列出所有预约类型 |
| `providers` | 列出所有医疗服务提供者 |
| `goals` | 列出所有患者的健康目标 |
| `goal-create` | 创建新的健康目标 |
| `documents` | 列出所有与患者相关的文档 |
| `forms` | 列出所有可使用的表格或表单 |
| `tags` | 列出所有用于标记文档的标签 |

## 输出格式

所有命令默认以 JSON 格式输出。若需以更易阅读的格式输出，请添加 `--human` 参数。

```bash
python3 {{baseDir}}/scripts/healthie.py <command> --human
```

## 脚本参考

| 脚本 | 说明 |
|--------|-------------|
| `{{baseDir}}/scripts/healthie.py` | 主要的命令行工具（CLI）——包含所有可用的命令 |

## 致谢

Healthie 由 [M. Abidi](https://www.linkedin.com/in/mohammad-ali-abidi) 和 [agxntsix.ai](https://www.agxntsix.ai) 共同开发。  
更多相关信息请访问 [YouTube](https://youtube.com/@aiwithabidi) 和 [GitHub](https://github.com/aiwithabidi)。  
该工具是 **AgxntSix Skill Suite** 的一部分，专为 OpenClaw 代理设计。

📅 **需要帮助为您的业务设置 OpenClaw 吗？** [预约免费咨询](https://cal.com/agxntsix/abidi-openclaw)