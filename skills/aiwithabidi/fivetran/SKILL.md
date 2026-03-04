---
name: fivetran
description: "Fivetran — 通过 REST API 管理连接器、目标数据源、同步状态以及相关组。"
homepage: https://www.agxntsix.ai
license: MIT
compatibility: Python 3.10+ (stdlib only — no dependencies)
metadata: {"openclaw": {"emoji": "🔗", "requires": {"env": ["FIVETRAN_API_KEY", "FIVETRAN_API_SECRET"]}, "primaryEnv": "FIVETRAN_API_KEY", "homepage": "https://www.agxntsix.ai"}}
---
# 🔗 Fivetran

Fivetran — 通过 REST API 管理连接器、目标数据源、同步状态和组。

## 必需参数

| 参数 | 是否必需 | 说明 |
|----------|----------|-------------|
| `FIVETRAN_API_KEY` | ✅ | API 密钥 |
| `FIVETRAN_API_SECRET` | ✅ | API 密码 |

## 快速入门

```bash
# List connectors
python3 {{baseDir}}/scripts/fivetran.py connectors group_id <value>

# Get connector
python3 {{baseDir}}/scripts/fivetran.py connector-get id <value>

# Create connector
python3 {{baseDir}}/scripts/fivetran.py connector-create --service <value> --group_id <value> --config <value>

# Update connector
python3 {{baseDir}}/scripts/fivetran.py connector-update id <value> --paused <value>

# Delete connector
python3 {{baseDir}}/scripts/fivetran.py connector-delete id <value>

# Trigger sync
python3 {{baseDir}}/scripts/fivetran.py connector-sync id <value>

# Get schema
python3 {{baseDir}}/scripts/fivetran.py connector-schema id <value>

# List destinations
python3 {{baseDir}}/scripts/fivetran.py destinations
```

## 所有命令

| 命令 | 说明 |
|---------|-------------|
| `connectors` | 列出所有连接器 |
| `connector-get` | 获取特定连接器信息 |
| `connector-create` | 创建新的连接器 |
| `connector-update` | 更新连接器信息 |
| `connector-delete` | 删除连接器 |
| `connector-sync` | 触发连接器同步 |
| `connector-schema` | 获取连接器的数据结构（schema） |
| `destinations` | 列出所有目标数据源 |
| `destination-get` | 获取特定目标数据源信息 |
| `groups` | 列出所有组 |
| `group-get` | 获取特定组信息 |
| `group-create` | 创建新的组 |
| `users` | 列出所有用户 |
| `metadata-connectors` | 列出所有可用的连接器类型 |
| `webhooks` | 列出所有关联的 Webhook |

## 输出格式

所有命令默认以 JSON 格式输出。若需可读性更强的输出格式，可使用 `--human` 选项。

```bash
python3 {{baseDir}}/scripts/fivetran.py <command> --human
```

## 脚本参考

| 脚本 | 说明 |
|--------|-------------|
| `{{baseDir}}/scripts/fivetran.py` | 主 CLI 工具，包含所有命令 |

## 致谢

由 [M. Abidi](https://www.linkedin.com/in/mohammad-ali-abidi) 和 [agxntsix.ai](https://www.agxntsix.ai) 开发 |
[YouTube](https://youtube.com/@aiwithabidi) | [GitHub](https://github.com/aiwithabidi) 提供技术支持 |
本工具是 **AgxntSix Skill Suite** 的一部分，专为 OpenClaw 代理设计。

📅 **需要帮助为您的业务设置 OpenClaw 吗？** [预约免费咨询](https://cal.com/agxntsix/abidi-openclaw)