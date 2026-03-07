---
name: terraform-cloud
description: "Terraform Cloud — 通过 REST API 管理工作区、运行任务、计划、状态以及变量"
homepage: https://www.agxntsix.ai
license: MIT
compatibility: Python 3.10+ (stdlib only — no dependencies)
metadata: {"openclaw": {"emoji": "🏗️", "requires": {"env": ["TFC_TOKEN", "TFC_ORG"]}, "primaryEnv": "TFC_TOKEN", "homepage": "https://www.agxntsix.ai"}}
---
# 🏗️ Terraform Cloud

Terraform Cloud：通过 REST API 管理工作区、运行任务、计划、状态和变量。

## 必需条件

| 变量 | 是否必需 | 说明 |
|----------|----------|-------------|
| `TFC_TOKEN` | ✅ | 来自 app.terraform.io 的 API 令牌 |
| `TFC_ORG` | ✅ | 组织名称 |

## 快速入门

```bash
# List organizations
python3 {{baseDir}}/scripts/terraform-cloud.py orgs

# List workspaces
python3 {{baseDir}}/scripts/terraform-cloud.py workspaces --search[name] <value>

# Get workspace
python3 {{baseDir}}/scripts/terraform-cloud.py workspace-get id <value>

# Create workspace
python3 {{baseDir}}/scripts/terraform-cloud.py workspace-create --name <value> --auto-apply <value> --terraform-version <value>

# Delete workspace
python3 {{baseDir}}/scripts/terraform-cloud.py workspace-delete id <value>

# Lock workspace
python3 {{baseDir}}/scripts/terraform-cloud.py workspace-lock id <value> --reason <value>

# Unlock workspace
python3 {{baseDir}}/scripts/terraform-cloud.py workspace-unlock id <value>

# List runs
python3 {{baseDir}}/scripts/terraform-cloud.py runs id <value>
```

## 所有命令

| 命令 | 说明 |
|---------|-------------|
| `orgs` | 列出所有组织 |
| `workspaces` | 列出所有工作区 |
| `workspace-get` | 获取工作区信息 |
| `workspace-create` | 创建工作区 |
| `workspace-delete` | 删除工作区 |
| `workspace-lock` | 锁定工作区 |
| `workspace-unlock` | 解锁工作区 |
| `runs` | 列出所有运行任务 |
| `run-get` | 获取运行任务信息 |
| `run-create` | 创建运行任务 |
| `run-apply` | 应用运行任务 |
| `run-discard` | 放弃运行任务 |
| `run-cancel` | 取消运行任务 |
| `plan-get` | 获取计划信息 |
| `state-version` | 获取当前状态 |
| `variables` | 列出所有变量 |
| `variable-create` | 创建变量 |
| `variable-delete` | 删除变量 |
| `teams` | 列出所有团队 |

## 输出格式

所有命令默认以 JSON 格式输出。若需可读的格式化输出，请添加 `--human` 参数。

```bash
python3 {{baseDir}}/scripts/terraform-cloud.py <command> --human
```

## 脚本参考

| 脚本 | 说明 |
|--------|-------------|
| `{{baseDir}}/scripts/terraform-cloud.py` | 主要的 CLI 工具，包含所有命令 |

## 致谢

由 [M. Abidi](https://www.linkedin.com/in/mohammad-ali-abidi) 和 [agxntsix.ai](https://www.agxntsix.ai) 开发 |
[YouTube](https://youtube.com/@aiwithabidi) | [GitHub](https://github.com/aiwithabidi) 提供支持 |
该工具是 **AgxntSix Skill Suite** 的一部分，专为 OpenClaw 代理设计。

📅 **需要帮助为您的企业设置 OpenClaw 吗？** [预约免费咨询](https://cal.com/agxntsix/abidi-openclaw)