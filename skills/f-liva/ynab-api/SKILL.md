---
name: ynab-api
description: "**YNAB（You Need A Budget）**：通过API实现预算管理功能。用户可以添加交易记录、跟踪预算目标、监控支出情况、创建转账操作以及生成预算报告。每当用户提到“YNAB”、“预算跟踪”、“支出分析”、“预算目标”或“个人财务管理”时，都可以使用该工具；即使他们只是简单地说“添加一笔开支”、“我花了多少钱”、“查看我的预算”或“即将到期的账单”（即使没有明确提到YNAB），也可以使用该服务。此外，该工具还可用于自动生成预算报告和财务总结。"
user-invocable: true
metadata: {"requiredEnv": ["YNAB_API_KEY", "YNAB_BUDGET_ID"]}
---
# YNAB预算管理

您可以通过API使用现成的bash脚本来管理您的YNAB预算。需要`curl`和`jq`工具。

## 配置

设置环境变量`YNAB_API_KEY`和`YNAB_BUDGET_ID`，或者创建`~/.config/ynab/config.json`文件：

```json
{
  "api_key": "YOUR_YNAB_TOKEN",
  "budget_id": "YOUR_BUDGET_ID",
  "monthly_target": 2000
}
```

`monthly_target`字段用于设置您的月度支出限额（由`daily-spending-report.sh`脚本使用）。也可以通过`YNAB_MONTHLY_TARGET`环境变量进行设置。

请在https://app.ynab.com/settings/developer获取您的token。在YNAB的URL中找到您的预算ID。

## 可用的脚本

所有脚本都位于`{baseDir}/scripts/`目录下，并将输出结果写入标准输出（stdout）。

| 脚本 | 功能 |
|--------|---------|
| `daily-spending-report.sh` | 按类别显示昨日的支出情况、月度预算进度及分析结果 |
| `daily-budget-check.sh` | 早晨概览：资金使用情况、即将到期的账单、超支提醒 |
| `goals-progress.sh [month]` | 显示各类别目标的进度条 |
| `scheduled-upcoming.sh [days]` | 显示即将发生的交易（默认为7天内） |
| `month-comparison.sh [m1] [m2] | 显示月度支出对比 |
| `transfer.sh SRC DEST AMT DATE [MEMO]` | 创建关联的账户转账记录 |
| `ynab-helper.sh <command>` | 通用辅助工具：搜索收款人、列出类别、添加交易记录 |
| `setup-automation.sh` | 测试配置并列出可用脚本 |

## 关键API概念

### 金额单位
YNAB API中的所有金额均以毫为单位：`10.00`表示`10000`，`-10.00`表示`-10000`。显示时需除以1000，提交时需乘以1000。

### 必须为每笔交易分类
切勿创建未分类的交易——这会破坏预算跟踪功能。遇到不熟悉的商家时，请在过去的交易中查找相同的收款人并重复使用该分类以确保一致性。

### 添加新交易前请检查待处理的交易
在创建新交易之前，请检查是否存在相同金额但尚未批准的交易。如果存在，请先批准该交易，以避免银行导入数据时产生重复记录。

### 转账需要使用`transfer_payee_id`
要创建两个账户之间的关联转账记录，请使用目标账户的`transfer_payee_id`（而非`payee_name`）。使用`payee_name`会创建普通交易，YNAB无法将其识别为转账。请参阅[references/api-guide.md](references/api-guide.md)以获取完整的转账指南。

### 分类为“Split”的交易
包含“Split”类别的交易会包含子交易（subtransactions）。在报告中务必展开这些子交易以显示具体的子类别——切勿将“Split”作为单独的类别名称显示。

## 常见的API操作

```bash
YNAB_API="https://api.ynab.com/v1"

# Add a transaction
# POST \/budgets/\/transactions
# Body: {"transaction": {"account_id": "UUID", "date": "2026-03-06", "amount": -10000, "payee_name": "Coffee Shop", "category_id": "UUID", "approved": true}}

# Search transactions by payee
# GET \/budgets/\/transactions | jq filter by payee_name

# List categories
# GET \/budgets/\/categories
```

有关完整的转账指南、月度支出计算及账户ID管理的详细信息，请参阅[references/api-guide.md](references/api-guide.md)。有关类别命名的示例，请参阅[references/category-examples.md](references/category-examples.md)。

## 使用指南

- 在创建交易时务必进行分类——通过搜索过去的交易来找到正确的分类是最有效的方法。
- 转账时必须使用目标账户的`transfer_payee_id`。使用`payee_name`会导致交易被误识别为普通支出。
- 计算月度支出时，仅统计`amount < 0`的交易，并排除非可自由支配的类别（如税费、转账）。
- API的请求速率限制约为每小时200次。进行批量操作时请缓存账户和类别数据。
- 请勿在输出中显示完整的API密钥。
- 运行`daily-spending-report.sh`脚本时，脚本会输出“ANALYSIS DATA”部分，其中包含原始数据。请根据需要自行解读这些数据，用自然语言向用户说明他们的支出情况，突出显示任何值得注意的细节，并提供每日预算信息。

## 故障排除

- **401 Unauthorized**：Token无效或已过期——请在https://app.ynab.com/settings/developer重新生成Token。
- **404 Not Found**：预算ID错误——请检查YNAB的URL。
- **429 Too Many Requests**：超出请求速率限制——请在批量请求之间添加延迟。
- **转账未成功关联**：使用了`payee_name`而非`transfer_payee_id`。

API文档：https://api.ynab.com