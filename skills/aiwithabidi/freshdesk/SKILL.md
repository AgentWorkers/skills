---
name: freshdesk
description: "Freshdesk 帮助台——通过 REST API 管理工单、联系人、公司和代理。"
homepage: https://www.agxntsix.ai
license: MIT
compatibility: Python 3.10+ (stdlib only — no dependencies)
metadata: {"openclaw": {"emoji": "🆘", "requires": {"env": ["FRESHDESK_API_KEY", "FRESHDESK_DOMAIN"]}, "primaryEnv": "FRESHDESK_API_KEY", "homepage": "https://www.agxntsix.ai"}}
---
# 🆘 Freshdesk

Freshdesk 是一个帮助台管理系统，支持通过 REST API 管理工单、联系人、公司和代理。

## 必需参数

| 参数 | 是否必填 | 说明 |
|----------|----------|-------------|
| `FRESHDESK_API_KEY` | ✅ | API 密钥 |
| `FRESHDESK_DOMAIN` | ✅ | 域名（例如：yourcompany.freshdesk.com） |

## 快速入门

```bash
# List tickets
python3 {{baseDir}}/scripts/freshdesk.py tickets --filter <value> --email <value>

# Get ticket
python3 {{baseDir}}/scripts/freshdesk.py ticket-get id <value>

# Create ticket
python3 {{baseDir}}/scripts/freshdesk.py ticket-create --subject <value> --description <value> --email <value> --priority <value> --status <value>

# Update ticket
python3 {{baseDir}}/scripts/freshdesk.py ticket-update id <value> --status <value> --priority <value>

# Delete ticket
python3 {{baseDir}}/scripts/freshdesk.py ticket-delete id <value>

# Reply to ticket
python3 {{baseDir}}/scripts/freshdesk.py ticket-reply id <value> --body <value>

# Add note
python3 {{baseDir}}/scripts/freshdesk.py ticket-note id <value> --body <value>

# List conversations
python3 {{baseDir}}/scripts/freshdesk.py conversations id <value>
```

## 所有命令

| 命令 | 说明 |
|---------|-------------|
| `tickets` | 列出所有工单 |
| `ticket-get` | 获取工单详情 |
| `ticket-create` | 创建新工单 |
| `ticket-update` | 更新工单状态 |
| `ticket-delete` | 删除工单 |
| `ticket-reply` | 回复工单 |
| `ticket-note` | 为工单添加备注 |
| `conversations` | 列出所有对话记录 |
| `contacts` | 列出所有联系人 |
| `contact-get` | 获取联系人详情 |
| `contact-create` | 创建新联系人 |
| `companies` | 列出所有公司 |
| `agents` | 列出所有代理 |
| `groups` | 列出所有团队/组 |
| `roles` | 列出所有角色 |
| `products` | 列出所有产品 |
| `satisfaction-ratings` | 查看客户满意度评分 |
| `time-entries` | 查看工单的记录时间 |

## 输出格式

所有命令默认以 JSON 格式输出。若需以易读的格式输出，请使用 `--human` 选项。

```bash
python3 {{baseDir}}/scripts/freshdesk.py <command> --human
```

## 脚本参考

| 脚本 | 说明 |
|--------|-------------|
| `{{baseDir}}/scripts/freshdesk.py` | 主要的命令行工具（包含所有相关命令） |

## 致谢

该工具由 [M. Abidi](https://www.linkedin.com/in/mohammad-ali-abidi) 和 [agxntsix.ai](https://www.agxntsix.ai) 开发。  
更多信息请访问 [YouTube](https://youtube.com/@aiwithabidi) 和 [GitHub](https://github.com/aiwithabidi)。  
本工具是 **AgxntSix Skill Suite** 的一部分，专为 OpenClaw 代理设计。

📅 **需要帮助为您的企业配置 OpenClaw 吗？** [预约免费咨询](https://cal.com/agxntsix/abidi-openclaw)