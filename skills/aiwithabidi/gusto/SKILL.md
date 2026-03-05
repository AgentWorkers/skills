---
name: gusto
description: "**Gusto Payroll & HR** — 通过 REST API 管理员工信息、薪资发放、福利待遇以及税务表格。"
homepage: https://www.agxntsix.ai
license: MIT
compatibility: Python 3.10+ (stdlib only — no dependencies)
metadata: {"openclaw": {"emoji": "💰", "requires": {"env": ["GUSTO_ACCESS_TOKEN", "GUSTO_COMPANY_ID"]}, "primaryEnv": "GUSTO_ACCESS_TOKEN", "homepage": "https://www.agxntsix.ai"}}
---
# 💰 Gusto

Gusto 是一款用于薪资管理和人力资源管理的工具，支持通过 REST API 来处理员工信息、薪资发放、福利发放以及税务表格的生成。

## 必需参数

| 参数名 | 是否必需 | 说明 |
|---------|---------|-------------|
| `GUSTO_ACCESS_TOKEN` | ✅ | OAuth 访问令牌 |
| `GUSTO_company_ID` | ✅ | 公司的唯一标识符（UUID） |

## 快速入门

```bash
# Get company info
python3 {{baseDir}}/scripts/gusto.py company

# List locations
python3 {{baseDir}}/scripts/gusto.py locations

# List employees
python3 {{baseDir}}/scripts/gusto.py employees

# Get employee
python3 {{baseDir}}/scripts/gusto.py employee-get id <value>

# Create employee
python3 {{baseDir}}/scripts/gusto.py employee-create --first_name <value> --last_name <value> --email <value>

# List payrolls
python3 {{baseDir}}/scripts/gusto.py payrolls --start_date <value> --end_date <value>

# Get payroll
python3 {{baseDir}}/scripts/gusto.py payroll-get id <value>

# List pay schedules
python3 {{baseDir}}/scripts/gusto.py pay-schedules
```

## 所有命令

| 命令 | 说明 |
|---------|-------------|
| `company` | 获取公司信息 |
| `locations` | 列出公司所在的位置 |
| `employees` | 列出所有员工 |
| `employee-get` | 获取指定员工的详细信息 |
| `employee-create` | 创建新员工 |
| `payrolls` | 列出所有员工的薪资记录 |
| `payroll-get` | 获取指定员工的薪资记录 |
| `pay-schedules` | 列出员工的薪资发放计划 |
| `compensations` | 列出员工的薪酬信息 |
| `benefits` | 列出员工享有的福利 |
| `employee-benefits` | 获取指定员工的福利详情 |
| `contractors` | 列出所有承包商的信息 |
| `contractor-payments` | 列出承包商的付款记录 |
| `tax-forms` | 列出所有需要提交的税务表格 |
| `garnishments` | 列出所有已执行的工资扣押记录 |

## 输出格式

所有命令默认以 JSON 格式输出。若需要以更易读的格式输出，可以使用 `--human` 选项。

```bash
python3 {{baseDir}}/scripts/gusto.py <command> --human
```

## 脚本参考

| 脚本名 | 说明 |
|--------|-------------|
| `{{baseDir}}/scripts/gusto.py` | 主要的命令行工具（包含所有命令） |

## 开发者信息

由 [M. Abidi](https://www.linkedin.com/in/mohammad-ali-abidi) 和 [agxntsix.ai](https://www.agxntsix.ai) 开发  
[YouTube](https://youtube.com/@aiwithabidi) | [GitHub](https://github.com/aiwithabidi)  
该工具是 **AgxntSix Skill Suite** 的一部分，专为 OpenClaw 代理设计。

📅 **需要帮助为您的企业配置 OpenClaw 吗？** [预约免费咨询](https://cal.com/agxntsix/abidi-openclaw)