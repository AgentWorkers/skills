---
name: greenhouse
description: "Greenhouse ATS（ applicant tracking system）——通过 Harvest API 管理候选人、职位、申请、录用通知以及面试流程。"
homepage: https://www.agxntsix.ai
license: MIT
compatibility: Python 3.10+ (stdlib only — no dependencies)
metadata: {"openclaw": {"emoji": "🌱", "requires": {"env": ["GREENHOUSE_API_KEY"]}, "primaryEnv": "GREENHOUSE_API_KEY", "homepage": "https://www.agxntsix.ai"}}
---
# 🌱 Greenhouse

Greenhouse ATS（ applicant tracking system）——通过 Harvest API 管理候选人、职位、申请、录用通知和面试流程。

## 必需条件

| 变量 | 是否必需 | 说明 |
|----------|----------|-------------|
| `GREENHOUSE_API_KEY` | ✅ | Harvest API 密钥 |

## 快速入门

```bash
# List candidates
python3 {{baseDir}}/scripts/greenhouse.py candidates --per_page <value> --job_id <value>

# Get candidate
python3 {{baseDir}}/scripts/greenhouse.py candidate-get id <value>

# Create candidate
python3 {{baseDir}}/scripts/greenhouse.py candidate-create --first_name <value> --last_name <value> --email_addresses <value>

# List applications
python3 {{baseDir}}/scripts/greenhouse.py applications --status <value> --job_id <value>

# Get application
python3 {{baseDir}}/scripts/greenhouse.py application-get id <value>

# Advance application
python3 {{baseDir}}/scripts/greenhouse.py application-advance id <value>

# Reject application
python3 {{baseDir}}/scripts/greenhouse.py application-reject id <value> --rejection_reason_id <value>

# List jobs
python3 {{baseDir}}/scripts/greenhouse.py jobs --status <value>
```

## 所有命令

| 命令 | 说明 |
|---------|-------------|
| `candidates` | 列出候选人信息 |
| `candidate-get` | 获取候选人详情 |
| `candidate-create` | 创建候选人信息 |
| `applications` | 列出申请信息 |
| `application-get` | 获取申请详情 |
| `application-advance` | 提升申请状态 |
| `application-reject` | 拒绝申请 |
| `jobs` | 列出职位信息 |
| `job-get` | 获取职位详情 |
| `job-stages` | 列出职位的各个阶段 |
| `offers` | 列出录用通知信息 |
| `interviews` | 列出面试信息 |
| `scorecards` | 列出面试评分记录 |
| `departments` | 列出部门信息 |
| `offices` | 列出办公室信息 |
| `users` | 列出用户信息 |
| `sources` | 列出信息来源 |

## 输出格式

所有命令默认以 JSON 格式输出。添加 `--human` 选项可获取易读的格式化输出。

```bash
python3 {{baseDir}}/scripts/greenhouse.py <command> --human
```

## 脚本参考

| 脚本 | 说明 |
|--------|-------------|
| `{{baseDir}}/scripts/greenhouse.py` | 主要命令行工具（包含所有命令） |

## 致谢

由 [M. Abidi](https://www.linkedin.com/in/mohammad-ali-abidi) 和 [agxntsix.ai](https://www.agxntsix.ai) 开发 |
[YouTube](https://youtube.com/@aiwithabidi) | [GitHub](https://github.com/aiwithabidi) 提供支持 |
本工具是 **AgxntSix Skill Suite** 的一部分，专为 OpenClaw 代理设计。

📅 **需要帮助为您的业务设置 OpenClaw 吗？** [预约免费咨询](https://cal.com/agxntsix/abidi-openclaw)