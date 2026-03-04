---
name: copper
description: "**Copper CRM集成**：通过Copper的REST API来管理人员、公司、商机、项目、任务和活动。Copper是一款基于Google Workspace的本地CRM系统，具备强大的关系管理功能。该系统专为AI代理设计，仅使用Python标准库开发，无需任何第三方依赖。可用于CRM管理、交易跟踪、关系梳理、项目管理以及销售流程自动化。"
homepage: https://www.agxntsix.ai
license: MIT
compatibility: Python 3.10+ (stdlib only — no dependencies)
metadata: {"openclaw": {"emoji": "🟤", "requires": {"env": ["COPPER_API_KEY", "COPPER_EMAIL"]}, "primaryEnv": "COPPER_API_KEY", "homepage": "https://www.agxntsix.ai"}}
---
# 🟤 Copper CRM

Copper CRM集成——通过Copper的REST API来管理人员、公司、机会、项目和活动。

## 功能

- **人员管理**——支持对联系人进行完整的CRUD操作（创建、读取、更新、删除）以及搜索功能。
- **公司跟踪**——可以查看公司的详细信息及其相互关系。
- **机会管理**——跟踪销售机会的进展阶段、价值以及转化率。
- **项目管理**——能够跟踪项目的各个阶段及分配的任务。
- **任务管理**——创建、分配并完成任务。
- **活动记录**——记录与任何实体相关的通话、会议等信息。
- **关系映射**——显示不同实体之间的关联关系。
- **跨所有实体类型搜索**——支持全面搜索。
- **自定义字段**——可以读写自定义字段的值。
- **管道报告**——提供关于销售机会转化率、进展速度等指标的报告。

## 需求

| 变量 | 是否必填 | 说明 |
|----------|----------|-------------|
| `COPPER_API_KEY` | ✅ | Copper CRM的API密钥/令牌 |
| `COPPER_EMAIL` | ✅ | 你的Copper账户邮箱 |

## 快速入门

```bash
# List people/contacts
python3 {baseDir}/scripts/copper.py people --limit 20
```

```bash
# Get person details
python3 {baseDir}/scripts/copper.py person-get 12345
```

```bash
# Create a person
python3 {baseDir}/scripts/copper.py person-create '{"name":"Jane Doe","emails":[{"email":"jane@example.com"}]}'
```

```bash
# Update a person
python3 {baseDir}/scripts/copper.py person-update 12345 '{"title":"VP Sales"}'
```



## 命令

### `people`  
列出人员/联系人信息。  
```bash
python3 {baseDir}/scripts/copper.py people --limit 20
```

### `person-get`  
获取人员详细信息。  
```bash
python3 {baseDir}/scripts/copper.py person-get 12345
```

### `person-create`  
创建新人员。  
```bash
python3 {baseDir}/scripts/copper.py person-create '{"name":"Jane Doe","emails":[{"email":"jane@example.com"}]}'
```

### `person-update`  
更新人员信息。  
```bash
python3 {baseDir}/scripts/copper.py person-update 12345 '{"title":"VP Sales"}'
```

### `companies`  
列出所有公司信息。  
```bash
python3 {baseDir}/scripts/copper.py companies --limit 20
```

### `company-create`  
创建新公司。  
```bash
python3 {baseDir}/scripts/copper.py company-create '{"name":"Acme Corp"}'
```

### `opportunities`  
列出所有销售机会。  
```bash
python3 {baseDir}/scripts/copper.py opportunities --limit 20
```

### `opportunity-create`  
创建新的销售机会。  
```bash
python3 {baseDir}/scripts/copper.py opportunity-create '{"name":"Acme Deal","monetary_value":50000}'
```

### `projects`  
列出所有项目信息。  
```bash
python3 {baseDir}/scripts/copper.py projects --limit 20
```

### `tasks`  
列出所有任务信息。  
```bash
python3 {baseDir}/scripts/copper.py tasks --limit 20 --status open
```

### `task-create`  
创建新任务。  
```bash
python3 {baseDir}/scripts/copper.py task-create '{"name":"Follow up","due_date":"2026-03-01"}'
```

### `activities`  
列出与特定实体相关的活动记录。  
```bash
python3 {baseDir}/scripts/copper.py activities --person 12345
```

### `search`  
在所有实体类型中进行搜索。  
```bash
python3 {baseDir}/scripts/copper.py search "Acme"
```

### `pipelines`  
列出所有的销售机会管道（销售流程）。  
```bash
python3 {baseDir}/scripts/copper.py pipelines
```

### `pipeline-report`  
生成销售机会管道的汇总报告。  
```bash
python3 {baseDir}/scripts/copper.py pipeline-report
```


## 输出格式

所有命令默认以JSON格式输出。若需可读性更强的输出格式，可添加`--human`参数。  
```bash
# JSON (default, for programmatic use)
python3 {baseDir}/scripts/copper.py people --limit 5

# Human-readable
python3 {baseDir}/scripts/copper.py people --limit 5 --human
```

## 脚本参考

| 脚本 | 说明 |
|--------|-------------|
| `{baseDir}/scripts/copper.py` | 主要的命令行工具，用于执行所有Copper CRM相关操作 |

## 数据政策

本技能**从不将数据存储在本地**。所有请求都会直接发送到Copper CRM API，结果会直接输出到标准输出（stdout）。你的数据将保存在Copper CRM的服务器上。

## 致谢  
---

由[M. Abidi](https://www.linkedin.com/in/mohammad-ali-abidi) | [agxntsix.ai](https://www.agxntsix.ai)开发  
[YouTube](https://youtube.com/@aiwithabidi) | [GitHub](https://github.com/aiwithabidi)提供支持  
本技能是**AgxntSix Skill Suite**的一部分，专为OpenClaw代理设计。  

📅 **需要帮助为您的企业设置OpenClaw吗？** [预约免费咨询](https://cal.com/agxntsix/abidi-openclaw)