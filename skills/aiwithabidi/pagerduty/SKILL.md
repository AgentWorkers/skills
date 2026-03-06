---
name: pagerduty
description: "PagerDuty 事件管理功能：通过 REST API 管理事件、服务、调度计划、升级策略以及值班安排。"
homepage: https://www.agxntsix.ai
license: MIT
compatibility: Python 3.10+ (stdlib only — no dependencies)
metadata: {"openclaw": {"emoji": "🚨", "requires": {"env": ["PAGERDUTY_API_KEY"]}, "primaryEnv": "PAGERDUTY_API_KEY", "homepage": "https://www.agxntsix.ai"}}
---
# 🚨 PagerDuty

PagerDuty 提供事件管理功能，支持通过 REST API 管理事件、服务、调度计划、升级策略以及值班安排。

## 必需条件

| 变量 | 是否必需 | 说明 |
|----------|----------|-------------|
| `PAGERDUTY_API_KEY` | ✅ | 来自 pagerduty.com 的 API 令牌 |

## 快速入门

```bash
# List incidents
python3 {{baseDir}}/scripts/pagerduty.py incidents --statuses[] <value> --since <value> --until <value>

# Get incident
python3 {{baseDir}}/scripts/pagerduty.py incident-get id <value>

# Create incident
python3 {{baseDir}}/scripts/pagerduty.py incident-create --title <value> --service_id <value> --urgency <value>

# Update incident
python3 {{baseDir}}/scripts/pagerduty.py incident-update id <value> --status <value>

# List incident notes
python3 {{baseDir}}/scripts/pagerduty.py incident-notes id <value>

# Add note
python3 {{baseDir}}/scripts/pagerduty.py incident-note-add id <value> --content <value>

# List services
python3 {{baseDir}}/scripts/pagerduty.py services --query <value>

# Get service
python3 {{baseDir}}/scripts/pagerduty.py service-get id <value>
```

## 所有命令

| 命令 | 说明 |
|---------|-------------|
| `incidents` | 列出所有事件 |
| `incident-get` | 获取单个事件详情 |
| `incident-create` | 创建新事件 |
| `incident-update` | 更新事件信息 |
| `incident-notes` | 查看事件备注 |
| `incident-note-add` | 为事件添加备注 |
| `services` | 列出所有服务 |
| `service-get` | 获取单个服务详情 |
| `service-create` | 创建新服务 |
| `oncalls` | 列出值班安排 |
| `schedules` | 列出所有调度计划 |
| `schedule-get` | 获取特定调度计划的详细信息 |
| `escalation-policies` | 查看升级策略 |
| `users` | 列出所有用户 |
| `user-get` | 获取用户详情 |
| `teams` | 列出所有团队 |
| `vendors` | 列出所有供应商 |
| `notifications` | 查看通知设置 |
| `abilities` | 查看用户权限（能力设置） |

## 输出格式

所有命令默认以 JSON 格式输出。若需以易读的格式输出结果，可添加 `--human` 参数。

```bash
python3 {{baseDir}}/scripts/pagerduty.py <command> --human
```

## 脚本参考

| 脚本 | 说明 |
|--------|-------------|
| `{{baseDir}}/scripts/pagerduty.py` | 主要命令行工具（包含所有命令） |

## 致谢

该工具由 [M. Abidi](https://www.linkedin.com/in/mohammad-ali-abidi) 和 [agxntsix.ai](https://www.agxntsix.ai) 开发。  
更多信息请访问 [YouTube](https://youtube.com/@aiwithabidi) 和 [GitHub](https://github.com/aiwithabidi)。  
该工具是 OpenClaw 代理套件（**AgxntSix Skill Suite**）的一部分。

📅 **需要帮助为您的企业配置 OpenClaw 吗？** [预约免费咨询](https://cal.com/agxntsix/abidi-openclaw)