---
name: circleci
description: "CircleCI（持续集成/持续交付）——通过 REST API 管理管道、工作流、作业以及相关数据洞察。"
homepage: https://www.agxntsix.ai
license: MIT
compatibility: Python 3.10+ (stdlib only — no dependencies)
metadata: {"openclaw": {"emoji": "🔄", "requires": {"env": ["CIRCLECI_TOKEN"]}, "primaryEnv": "CIRCLECI_TOKEN", "homepage": "https://www.agxntsix.ai"}}
---
# 🔄 CircleCI

CircleCI 是一款用于持续集成和持续部署（CI/CD）的工具，它通过 REST API 管理各种管道（pipelines）、工作流（workflows）、作业（jobs）以及相关的数据洞察（insights）。

## 必需条件

| 变量 | 是否必需 | 说明 |
|----------|----------|-------------|
| `CIRCLECI_TOKEN` | ✅ | 来自 circleci.com 的个人 API 令牌 |

## 快速入门

```bash
# Get current user
python3 {{baseDir}}/scripts/circleci.py me

# List pipelines
python3 {{baseDir}}/scripts/circleci.py pipelines slug <value> --branch <value>

# Get pipeline
python3 {{baseDir}}/scripts/circleci.py pipeline-get id <value>

# Trigger pipeline
python3 {{baseDir}}/scripts/circleci.py pipeline-trigger slug <value> --branch <value> --parameters <value>

# Get pipeline config
python3 {{baseDir}}/scripts/circleci.py pipeline-config id <value>

# List workflows
python3 {{baseDir}}/scripts/circleci.py workflows id <value>

# Get workflow
python3 {{baseDir}}/scripts/circleci.py workflow-get id <value>

# Cancel workflow
python3 {{baseDir}}/scripts/circleci.py workflow-cancel id <value>
```

## 所有命令

| 命令 | 说明 |
|---------|-------------|
| `me` | 获取当前用户信息 |
| `pipelines` | 列出所有管道 |
| `pipeline-get` | 获取特定管道的信息 |
| `pipeline-trigger` | 触发某个管道 |
| `pipeline-config` | 获取管道的配置信息 |
| `workflows` | 列出所有工作流 |
| `workflow-get` | 获取特定工作流的信息 |
| `workflow-cancel` | 取消工作流 |
| `workflow-rerun` | 重新运行工作流 |
| `jobs` | 列出工作流中的所有作业 |
| `job-get` | 获取作业的详细信息 |
| `job-cancel` | 取消作业 |
| `job-artifacts` | 列出作业生成的工件 |
| `insights-workflows` | 查看工作流的运行数据 |
| `contexts` | 列出所有工作流的环境变量 |
| `envvars` | 列出项目中的环境变量 |
| `envvar-set` | 设置环境变量 |

## 输出格式

所有命令默认以 JSON 格式输出。若需要可读性更强的输出格式，可以使用 `--human` 选项。

```bash
python3 {{baseDir}}/scripts/circleci.py <command> --human
```

## 脚本参考

| 脚本 | 说明 |
|--------|-------------|
| `{{baseDir}}/scripts/circleci.py` | 主要的命令行工具（CLI），包含所有可用的命令 |

## 致谢

本工具由 [M. Abidi](https://www.linkedin.com/in/mohammad-ali-abidi) 和 [agxntsix.ai](https://www.agxntsix.ai) 开发。  
更多信息请访问 [YouTube](https://youtube.com/@aiwithabidi) 和 [GitHub](https://github.com/aiwithabidi)。  
本工具是 **AgxntSix Skill Suite** 的一部分，专为 OpenClaw 代理设计。  

📅 **需要帮助为您的企业设置 OpenClaw 吗？** [预约免费咨询](https://cal.com/agxntsix/abidi-openclaw)