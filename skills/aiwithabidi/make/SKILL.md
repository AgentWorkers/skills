---
name: make
description: "Make（前身为Integromat）自动化平台：通过Make API管理自动化场景、触发执行、监控执行过程、管理连接以及处理数据存储。支持构建和管理可视化自动化流程，监控执行日志，管理团队资源，并触发工作流程。该平台专为AI代理设计，仅使用Python标准库，无任何外部依赖。适用于可视化工作流程自动化、场景管理、执行监控以及无需编码的自动化任务。"
homepage: https://www.agxntsix.ai
license: MIT
compatibility: Python 3.10+ (stdlib only — no dependencies)
metadata: {"openclaw": {"emoji": "🔧", "requires": {"env": ["MAKE_API_KEY", "MAKE_ZONE"]}, "primaryEnv": "MAKE_API_KEY", "homepage": "https://www.agxntsix.ai"}}
---
# 🔧 Make (Integromat)

Make（前身为Integromat）是一个自动化平台，通过Make API来管理自动化场景、触发执行、监控执行过程、管理连接以及处理数据存储。

## 主要功能

- **场景管理**：列出、激活或停用自动化场景。
- **触发执行**：按需执行自动化场景。
- **执行日志**：监控执行历史和状态。
- **连接管理**：查看和管理应用程序连接。
- **数据存储操作**：对数据存储进行创建、读取、更新和删除（CRUD）操作。
- **Webhook管理**：创建和管理Webhook。
- **组织管理**：管理团队和用户。
- **模板浏览**：查找可用的自动化场景模板。
- **蓝图导出**：导出自动化场景的定义。
- **使用情况监控**：查看操作记录和数据传输统计信息。

## 必需参数

| 参数 | 是否必填 | 说明 |
|--------|---------|-----------------------------|
| `MAKE_API_KEY` | ✅ | Make (Integromat)的API密钥/令牌 |
| `MAKE_ZONE` | ❌ | API区域（默认：us1.make.com） |

## 快速入门

```bash
# List scenarios
python3 {baseDir}/scripts/make.py scenarios --limit 20
```

```bash
# Get scenario details
python3 {baseDir}/scripts/make.py scenario-get 12345
```

```bash
# Trigger a scenario run
python3 {baseDir}/scripts/make.py scenario-run 12345
```

```bash
# Activate a scenario
python3 {baseDir}/scripts/make.py scenario-activate 12345
```

## 命令

### `scenarios`  
列出所有自动化场景。  
```bash
python3 {baseDir}/scripts/make.py scenarios --limit 20
```

### `scenario-get`  
获取特定场景的详细信息。  
```bash
python3 {baseDir}/scripts/make.py scenario-get 12345
```

### `scenario-run`  
触发某个自动化场景的执行。  
```bash
python3 {baseDir}/scripts/make.py scenario-run 12345
```

### `scenario-activate`  
激活某个自动化场景。  
```bash
python3 {baseDir}/scripts/make.py scenario-activate 12345
```

### `scenario-deactivate`  
停用某个自动化场景。  
```bash
python3 {baseDir}/scripts/make.py scenario-deactivate 12345
```

### `executions`  
列出所有执行记录。  
```bash
python3 {baseDir}/scripts/make.py executions --scenario 12345 --limit 20
```

### `execution-get`  
获取单次执行的详细信息。  
```bash
python3 {baseDir}/scripts/make.py execution-get exec_abc
```

### `connections`  
列出所有已建立的连接。  
```bash
python3 {baseDir}/scripts/make.py connections --limit 20
```

### `data-stores`  
列出所有可用的数据存储。  
```bash
python3 {baseDir}/scripts/make.py data-stores
```

### `data-store-records`  
列出数据存储中的记录。  
```bash
python3 {baseDir}/scripts/make.py data-store-records 789 --limit 50
```

### `webhooks`  
列出所有已创建的Webhook。  
```bash
python3 {baseDir}/scripts/make.py webhooks
```

### `webhook-create`  
创建一个新的Webhook。  
```bash
python3 {baseDir}/scripts/make.py webhook-create '{"name":"My Hook"}'
```

### `organizations`  
列出所有组织信息。  
```bash
python3 {baseDir}/scripts/make.py organizations
```

### `users`  
列出所有团队成员的信息。  
```bash
python3 {baseDir}/scripts/make.py users
```

### `usage`  
获取使用情况统计信息。  
```bash
python3 {baseDir}/scripts/make.py usage
```

## 输出格式

所有命令默认以JSON格式输出。若需以更易读的格式输出，可使用`--human`选项。  
```bash
# JSON (default, for programmatic use)
python3 {baseDir}/scripts/make.py scenarios --limit 5

# Human-readable
python3 {baseDir}/scripts/make.py scenarios --limit 5 --human
```

## 脚本参考

| 脚本 | 说明 |
|--------|-----------------------------|
| `{baseDir}/scripts/make.py` | 主要的命令行工具（CLI），用于执行所有Make (Integromat)相关操作 |

## 数据处理政策

该工具 **从不将数据存储在本地**。所有请求都会直接发送到Make (Integromat)的API，结果会返回到标准输出（stdout）。您的数据将保存在Make (Integromat)的服务器上。

## 致谢  
---
由[M. Abidi](https://www.linkedin.com/in/mohammad-ali-abidi) | [agxntsix.ai](https://www.agxntsix.ai)开发  
[YouTube频道](https://youtube.com/@aiwithabidi) | [GitHub仓库](https://github.com/aiwithabidi)  
属于OpenClaw代理的**AgxntSix技能套件**的一部分。  

📅 **需要帮助为您的企业设置OpenClaw吗？** [预约免费咨询](https://cal.com/agxntsix/abidi-openclaw)