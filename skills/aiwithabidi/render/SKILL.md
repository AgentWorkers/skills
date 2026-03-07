---
name: render
description: "**Render Cloud Platform**  
通过 **Render API** 管理服务、部署、数据库、环境组以及自定义域名。支持部署 Web 服务、静态网站和定时任务（cron jobs），并具备自动扩展功能。专为 AI 代理设计，仅使用 Python 标准库，无任何外部依赖。适用于云部署、服务管理、数据库配置、持续集成/持续交付（CI/CD）自动化以及基础设施管理。"
homepage: https://www.agxntsix.ai
license: MIT
compatibility: Python 3.10+ (stdlib only — no dependencies)
metadata: {"openclaw": {"emoji": "🚀", "requires": {"env": ["RENDER_API_KEY"]}, "primaryEnv": "RENDER_API_KEY", "homepage": "https://www.agxntsix.ai"}}
---
# 🚀 Render

Render 是一个云平台服务，通过 Render API 管理服务、部署、数据库、环境组以及自定义域名。

## 主要功能

- **服务管理**：支持 Web 服务、静态网站和 Cron 作业的管理。
- **部署跟踪**：记录部署历史、提供回滚功能以及实时显示部署状态。
- **数据库管理**：负责 PostgreSQL 数据库的配置与维护。
- **环境变量管理**：允许用户创建和管理环境变量及其组。
- **自定义域名**：支持添加和配置自定义域名。
- **自动部署**：可通过 API 触发服务的自动部署。
- **扩展管理**：支持调整实例数量并规划扩展策略。
- **日志查询**：提供服务日志的访问功能。
- **带宽监控**：实时监控带宽使用情况与费用。
- **基础设施即代码（Infrastructure as Code）**：支持基于代码的基础设施管理。

## 必需参数

| 参数          | 是否必需 | 说明                |
|--------------|---------|-------------------|
| `RENDER_API_KEY` | ✅      | Render 的 API 密钥/令牌         |
|              |            |                    |

## 快速入门

```bash
# List services
python3 {baseDir}/scripts/render.py services --limit 20
```

```bash
# Get service details
python3 {baseDir}/scripts/render.py service-get srv-abc123
```

```bash
# Create a service
python3 {baseDir}/scripts/render.py service-create '{"type":"web_service","name":"my-api","repo":"https://github.com/user/repo","branch":"main","runtime":"python"}'
```

```bash
# List deployments
python3 {baseDir}/scripts/render.py deploys --service srv-abc123 --limit 10
```

## 命令列表

### `services`  
列出所有服务。  
```bash
python3 {baseDir}/scripts/render.py services --limit 20
```

### `service-get`  
获取服务详细信息。  
```bash
python3 {baseDir}/scripts/render.py service-get srv-abc123
```

### `service-create`  
创建新的服务。  
```bash
python3 {baseDir}/scripts/render.py service-create '{"type":"web_service","name":"my-api","repo":"https://github.com/user/repo","branch":"main","runtime":"python"}'
```

### `deploys`  
列出所有部署记录。  
```bash
python3 {baseDir}/scripts/render.py deploys --service srv-abc123 --limit 10
```

### `deploy`  
触发服务的部署。  
```bash
python3 {baseDir}/scripts/render.py deploy --service srv-abc123
```

### `deploy-rollback`  
将服务回滚到之前的版本。  
```bash
python3 {baseDir}/scripts/render.py deploy-rollback --service srv-abc123 --deploy dep-xyz
```

### `databases`  
列出所有数据库。  
```bash
python3 {baseDir}/scripts/render.py databases
```

### `database-create`  
创建一个新的 PostgreSQL 数据库。  
```bash
python3 {baseDir}/scripts/render.py database-create '{"name":"my-db","plan":"starter"}'
```

### `env-vars`  
列出所有环境变量。  
```bash
python3 {baseDir}/scripts/render.py env-vars --service srv-abc123
```

### `env-set`  
设置环境变量。  
```bash
python3 {baseDir}/scripts/render.py env-set --service srv-abc123 "DATABASE_URL" "postgres://..."
```

### `env-delete`  
删除指定的环境变量。  
```bash
python3 {baseDir}/scripts/render.py env-delete --service srv-abc123 DATABASE_URL
```

### `domains`  
列出所有自定义域名。  
```bash
python3 {baseDir}/scripts/render.py domains --service srv-abc123
```

### `domain-add`  
添加新的自定义域名。  
```bash
python3 {baseDir}/scripts/render.py domain-add --service srv-abc123 api.example.com
```

### `logs`  
获取服务的日志记录。  
```bash
python3 {baseDir}/scripts/render.py logs --service srv-abc123 --limit 100
```

### `suspend`  
暂停服务的运行。  
```bash
python3 {baseDir}/scripts/render.py suspend --service srv-abc123
```

## 输出格式

所有命令默认以 JSON 格式输出。若需人类可读的格式输出，可使用 `--human` 选项。  
```bash
# JSON (default, for programmatic use)
python3 {baseDir}/scripts/render.py services --limit 5

# Human-readable
python3 {baseDir}/scripts/render.py services --limit 5 --human
```

## 脚本参考

| 脚本          | 说明                |
|--------------|-------------------|
| `{baseDir}/scripts/render.py` | 主要的命令行接口脚本        |

## 数据处理政策

该服务 **绝不将数据存储在本地**。所有请求都会直接发送到 Render API，结果会直接输出到标准输出（stdout）。用户的数据将保存在 Render 服务器上。

## 开发者信息

由 [M. Abidi](https://www.linkedin.com/in/mohammad-ali-abidi) 和 [agxntsix.ai](https://www.agxntsix.ai) 开发。  
相关内容可查看 [YouTube](https://youtube.com/@aiwithabidi) 和 [GitHub](https://github.com/aiwithabidi)。  
本功能属于 OpenClaw 代理的 **AgxntSix Skill Suite** 套件的一部分。

📅 **需要帮助为您的业务设置 OpenClaw 吗？** [预约免费咨询](https://cal.com/agxntsix/abidi-openclaw)