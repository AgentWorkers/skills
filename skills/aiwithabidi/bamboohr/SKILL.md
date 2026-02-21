---
name: bamboohr
description: "**BambooHR** — 通过 REST API 管理员工信息、休假申请、报告以及公司资料"
homepage: https://www.agxntsix.ai
license: MIT
compatibility: Python 3.10+ (stdlib only — no dependencies)
metadata: {"openclaw": {"emoji": "🎋", "requires": {"env": ["BAMBOOHR_API_KEY", "BAMBOOHR_SUBDOMAIN"]}, "primaryEnv": "BAMBOOHR_API_KEY", "homepage": "https://www.agxntsix.ai"}}
---
# 🎋 BambooHR

BambooHR — 通过 REST API 管理员工信息、休假申请、报告以及公司相关数据

## 必需参数

| 参数 | 是否必填 | 说明 |
|----------|----------|-------------|
| `BAMBOOHR_API_KEY` | ✅ | API 密钥 |
| `BAMBOOHR_SUBDOMAIN` | ✅ | 公司子域名 |

## 快速入门

```bash
# List employees
python3 {{baseDir}}/scripts/bamboohr.py employees

# Get employee
python3 {{baseDir}}/scripts/bamboohr.py employee-get id <value> --fields <value>

# Create employee
python3 {{baseDir}}/scripts/bamboohr.py employee-create --firstName <value> --lastName <value> --workEmail <value>

# Update employee
python3 {{baseDir}}/scripts/bamboohr.py employee-update id <value> --fields <value>

# List employee files
python3 {{baseDir}}/scripts/bamboohr.py employee-files id <value>

# List time-off requests
python3 {{baseDir}}/scripts/bamboohr.py time-off-requests --start <value> --end <value> --status <value>

# List time-off types
python3 {{baseDir}}/scripts/bamboohr.py time-off-types

# Who is out
python3 {{baseDir}}/scripts/bamboohr.py whois-out --start <value> --end <value>
```

## 所有命令

| 命令 | 说明 |
|---------|-------------|
| `employees` | 列出所有员工 |
| `employee-get` | 获取员工信息 |
| `employee-create` | 创建新员工 |
| `employee-update` | 更新员工信息 |
| `employee-files` | 列出员工的文件 |
| `time-off-requests` | 列出休假申请 |
| `time-off-types` | 列出可用的休假类型 |
| `whois-out` | 查看当前不在岗的员工 |
| `reports` | 运行报告 |
| `fields` | 列出所有可用的字段 |
| `tables` | 列出所有数据库表 |
| `table-get` | 获取表格数据 |
| `changed` | 获取发生变更的员工信息 |

## 输出格式

所有命令默认以 JSON 格式输出。若需以易读的格式输出，请添加 `--human` 参数。

```bash
python3 {{baseDir}}/scripts/bamboohr.py <command> --human
```

## 脚本参考

| 脚本 | 说明 |
|--------|-------------|
| `{{baseDir}}/scripts/bamboohr.py` | 主 CLI 工具，包含所有命令 |

## 致谢

由 [M. Abidi](https://www.linkedin.com/in/mohammad-ali-abidi) 和 [agxntsix.ai](https://www.agxntsix.ai) 开发  
[YouTube](https://youtube.com/@aiwithabidi) | [GitHub](https://github.com/aiwithabidi)  
本工具是 **AgxntSix Skill Suite** 的一部分，专为 OpenClaw 代理设计。

📅 **需要帮助为您的企业配置 OpenClaw 吗？** [预约免费咨询](https://cal.com/agxntsix/abidi-openclaw)