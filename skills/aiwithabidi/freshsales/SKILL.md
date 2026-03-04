---
name: freshsales
description: "Freshsales CRM集成：通过Freshsales API管理联系人、潜在客户、交易、账户、任务以及销售流程。可追踪交易进展，自动分配潜在客户，记录活动日志，并生成销售报告。专为AI代理设计——仅使用Python标准库，无任何依赖项。适用于销售CRM、联系人管理、交易跟踪、销售流程报告及销售自动化场景。"
homepage: https://www.agxntsix.ai
license: MIT
compatibility: Python 3.10+ (stdlib only — no dependencies)
metadata: {"openclaw": {"emoji": "🟢", "requires": {"env": ["FRESHSALES_API_KEY", "FRESHSALES_DOMAIN"]}, "primaryEnv": "FRESHSALES_API_KEY", "homepage": "https://www.agxntsix.ai"}}
---
# 🟢 Freshsales

Freshsales 是一款 CRM（客户关系管理）工具，您可以通过其 API 来管理联系人、潜在客户、交易、账户、任务以及销售流程。

## 主要功能

- **联系人管理**：创建、更新、搜索和分类联系人。
- **潜在客户跟踪**：捕获潜在客户信息，评估其转化潜力，分配处理人员，并推动转化。
- **交易管理**：跟踪交易进度，预测交易金额，以及判断交易是否成功。
- **账户管理**：查看公司信息及账户层级结构。
- **任务管理**：创建和分配销售任务，并跟踪任务执行情况。
- **活动记录**：记录电话通话、电子邮件、会议和备注等销售相关活动。
- **销售流程管理**：查看和管理销售活动。
- **搜索功能**：可跨联系人、潜在客户和交易进行搜索。
- **报告生成**：提供交易价值、转化率等关键指标的报告。
- **自定义筛选**：支持根据字段内容进行自定义筛选。

## 所需配置

| 变量          | 必需      | 说明                          |
|---------------|---------|--------------------------------------------|
| `FRESHSALES_API_KEY` | ✅       | Freshsales 的 API 密钥/令牌                |
| `FRESHSALES_DOMAIN` | ✅       | 您的 Freshsales 域名（例如：yourorg.freshsales.io）         |

## 快速入门

```bash
# List contacts
python3 {baseDir}/scripts/freshsales.py contacts --limit 20
```

```bash
# Get contact details
python3 {baseDir}/scripts/freshsales.py contact-get 12345
```

```bash
# Create a contact
python3 {baseDir}/scripts/freshsales.py contact-create '{"first_name":"Jane","last_name":"Doe","email":"jane@example.com"}'
```

```bash
# Update a contact
python3 {baseDir}/scripts/freshsales.py contact-update 12345 '{"lead_score":85}'
```

## 命令说明

### `contacts`  
列出所有联系人信息。

```bash
python3 {baseDir}/scripts/freshsales.py contacts --limit 20
```

### `contact-get`  
获取特定联系人的详细信息。

```bash
python3 {baseDir}/scripts/freshsales.py contact-get 12345
```

### `contact-create`  
创建一个新的联系人。

```bash
python3 {baseDir}/scripts/freshsales.py contact-create '{"first_name":"Jane","last_name":"Doe","email":"jane@example.com"}'
```

### `contact-update`  
更新现有联系人的信息。

```bash
python3 {baseDir}/scripts/freshsales.py contact-update 12345 '{"lead_score":85}'
```

### `leads`  
列出所有潜在客户信息。

```bash
python3 {baseDir}/scripts/freshsales.py leads --limit 20 --sort updated_at
```

### `lead-create`  
创建一个新的潜在客户。

```bash
python3 {baseDir}/scripts/freshsales.py lead-create '{"first_name":"John","company":"Acme"}'
```

### `deals`  
列出所有交易信息。

```bash
python3 {baseDir}/scripts/freshsales.py deals --limit 20
```

### `deal-create`  
创建一个新的交易记录。

```bash
python3 {baseDir}/scripts/freshsales.py deal-create '{"name":"Acme Upgrade","amount":50000}'
```

### `deal-update`  
更新交易的当前阶段或金额。

```bash
python3 {baseDir}/scripts/freshsales.py deal-update 789 '{"deal_stage_id":3}'
```

### `accounts`  
列出所有账户信息。

```bash
python3 {baseDir}/scripts/freshsales.py accounts --limit 20
```

### `tasks`  
列出所有待办任务。

```bash
python3 {baseDir}/scripts/freshsales.py tasks --limit 10 --status open
```

### `task-create`  
创建一个新的销售任务。

```bash
python3 {baseDir}/scripts/freshsales.py task-create '{"title":"Follow up with Acme","due_date":"2026-03-01"}'
```

### `search`  
在所有数据源中搜索相关信息。

```bash
python3 {baseDir}/scripts/freshsales.py search "Acme"
```

### `activities`  
查看最近发生的销售活动。

```bash
python3 {baseDir}/scripts/freshsales.py activities --limit 20
```

### `pipeline`  
获取交易流程的汇总信息。

```bash
python3 {baseDir}/scripts/freshsales.py pipeline
```

## 输出格式

所有命令默认以 JSON 格式输出。若需以易读的格式输出结果，可使用 `--human` 选项。

```bash
# JSON (default, for programmatic use)
python3 {baseDir}/scripts/freshsales.py contacts --limit 5

# Human-readable
python3 {baseDir}/scripts/freshsales.py contacts --limit 5 --human
```

## 脚本参考

| 脚本          | 说明                          |
|---------------|--------------------------------------------|
| `{baseDir}/scripts/freshsales.py` | 主要的命令行工具，用于执行所有 Freshsales 相关操作 |

## 数据处理政策

本技能 **从不将数据存储在本地**。所有请求都会直接发送到 Freshsales API，结果会直接返回到标准输出（stdout）。您的数据将保存在 Freshsales 服务器上。

## 致谢

本技能由 [M. Abidi](https://www.linkedin.com/in/mohammad-ali-abidi) 和 [agxntsix.ai](https://www.agxntsix.ai) 开发。相关视频教程可在 [YouTube](https://youtube.com/@aiwithabidi) 查看，代码实现托管在 [GitHub](https://github.com/aiwithabidi) 上。本技能属于 **AgxntSix Skill Suite** 的一部分，专为 OpenClaw 代理设计。

📅 **需要帮助为您的企业配置 OpenClaw 吗？** [预约免费咨询](https://cal.com/agxntsix/abidi-openclaw)