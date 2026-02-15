---
name: ynab
description: 通过命令行界面（CLI）管理YNAB的预算、账户、类别和交易。
metadata: {"clawdbot":{"emoji":"💰","requires":{"bins":["ynab"],"env":["YNAB_API_KEY"]},"primaryEnv":"YNAB_API_KEY","install":[{"id":"node","kind":"node","package":"@stephendolan/ynab-cli","bins":["ynab"],"label":"Install ynab-cli (npm)"}]}}
---

# YNAB CLI

## 安装
```bash
npm i -g @stephendolan/ynab-cli
```

## 认证
```bash
# Get API key from https://app.ynab.com/settings/developer
# Then set YNAB_API_KEY env var, or:
ynab auth login
ynab auth status
```

## 预算管理
```bash
ynab budgets list
ynab budgets view [id]
ynab budgets set-default <id>
```

## 账户管理
```bash
ynab accounts list
ynab accounts view <id>
ynab accounts transactions <id>
```

## 分类管理
```bash
ynab categories list
ynab categories view <id>
ynab categories transactions <id>
ynab categories budget <id> --month <YYYY-MM> --amount <amount>
```

## 交易记录
```bash
ynab transactions list
ynab transactions list --account <id> --since <YYYY-MM-DD>
ynab transactions list --approved=false --min-amount 100
ynab transactions search --memo "coffee"
ynab transactions search --payee-name "Amazon"
ynab transactions view <id>
ynab transactions create --account <id> --amount <amount> --date <YYYY-MM-DD>
ynab transactions update <id> --amount <amount>
ynab transactions delete <id>
ynab transactions split <id> --splits '[{"amount": -50.00, "category_id": "xxx"}]'
```

## 支付方管理
```bash
ynab payees list
ynab payees view <id>
ynab payees update <id> --name <name>
ynab payees transactions <id>
```

## 月份管理
```bash
ynab months list
ynab months view <YYYY-MM>
```

## 计划任务管理
```bash
ynab scheduled list
ynab scheduled view <id>
ynab scheduled delete <id>
```

## 原始 API 接口
```bash
ynab api GET /budgets
ynab api POST /budgets/{budget_id}/transactions --data '{"transaction": {...}}'
```

## 注意事项：
- 所有金额均以您的预算货币为单位，而非毫单位（milliunits）。
- 使用 `--compact` 选项可生成压缩后的 JSON 数据。
- API 的请求速率限制为每小时 200 次。
- 无法通过 API 创建分类、分组或支付方。