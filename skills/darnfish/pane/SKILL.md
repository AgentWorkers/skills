---
name: pane-mcp
description: 通过 mcporter，可以使用 Pane 托管的 MCP 服务器访问个人财务数据（银行账户、交易记录、余额、支出情况、投资信息以及加密货币相关数据）。需要具备 Pane 账户和 API 密钥。
homepage: https://pane.money
metadata: {"clawdbot":{"emoji":"💳","install":[{"id":"mcporter","kind":"skill","skill":"steipete/mcporter","label":"Install mcporter skill"}]},"openclaw":{"primaryEnv":"PANE_API_KEY","requires":{"env":["PANE_API_KEY"],"bins":["mcporter"],"skills":["mcporter"]}}}
---
# MCP面板

您可以通过[Pane](https://pane.money)访问用户关联的金融账户。Pane是一个由Plaid提供支持的MCP（Money Control Panel）服务器，支持查询银行账户、交易记录、余额、消费汇总、定期付款、投资情况、负债以及加密货币持有量等功能。您还可以在对话中添加持久性注释以记录相关信息。

## 设置

用户必须拥有一个已关联金融账户的Pane账户，并从[pane.money/dashboard/connect](https://pane.money/dashboard/connect)获取API密钥。

请设置`PANE_API_KEY`环境变量（切勿直接将密钥粘贴到shell命令中）：

```bash
# Add to your shell profile (.zshrc, .bashrc, etc.)
export PANE_API_KEY="pane_sk_live_..."
```

接下来配置mcporter：

```bash
# Add Pane as an MCP server using the env var
mcporter config add pane --url https://mcp.pane.money --header "Authorization: Bearer $PANE_API_KEY"

# Verify connection
mcporter list pane --schema
```

## 工具

### 金融数据（仅读）

**get_accounts** — 列出所有关联的账户及其余额

```bash
mcporter call pane.get_accounts type=all
mcporter call pane.get_accounts type=checking
```

**get_transactions** — 搜索和过滤交易记录

**参数**：`account_id`（UUID）、`start_date`/`end_date`（YYYY-MM-DD格式）、`category`（Plaid分类）、`search`（最多200个字符）、`min_amount`/`max_amount`、`limit`（1-500，默认为50）、`offset`。

**get_balances** — 获取当前余额及净资产汇总（会触发Plaid实时更新）

**返回内容**：每个账户的余额及汇总信息：`total_cash`、`total_credit_debt`、`total_investments`、`total_loans`、`total_crypto`、`net_worth`。

**get_spending_summary** — 按类别、商家、周或月对消费进行分组统计

**时间范围缩写**：`last_7d`、`last_30d`、`this_week`、`last_week`、`this_month`、`last_month`、`this_year`。请使用`period`或`start_date`+`end_date`中的一个，但不能同时使用两者。

**get_recurring** — 获取订阅服务、账单及收入流的信息

**返回内容**：包含订阅服务/账单/收入的数组及月度总计。时间频率转换规则：每周 x 4.33、每两周 x 2.17、每月 x 1、每年 x 12。

**get_investments** — 获取投资持仓及投资组合价值

**数据缓存时间**：15分钟。返回的持仓信息包括符号、数量、当前价值（currentValue）和成本基准（costBasis）。

**get_liabilities** — 获取信用卡债务、学生贷款和抵押贷款的详细信息

**数据缓存时间**：1小时。返回年利率（APR）、还款金额及到期日期。

**get_crypto** — 获取跨交易所账户和链上钱包的加密货币持有量

**注意**：需要启用加密货币相关功能，该操作会触发钱包数据的实时更新。

### 注释（读写）

注释是附加在交易记录、商家、账户或用户个人资料上的持久性备注。这些注释会自动显示在后续的工具结果中。

**write_annotation** — 保存注释

**使用范围**：`profile`（无target_id）、`merchant`（不区分大小写的商家名称）、`account`（UUID）。每条注释最多2,000个字符，每个目标对象最多可保存50条注释。

**list_annotations** — 列出所有保存的注释

**delete_annotation** — 根据ID删除注释

**注意**：删除操作仅针对已保存的注释。

## 资源

**快速入门**：首先访问`pane://profile`以获取概览，然后使用相应工具进行详细查询。

## 隐私设置

每个账户的隐私设置由用户自行设定，服务器会自动执行相应的隐私保护规则：

| 设置范围 | 可查看内容 | 可查看的交易记录 | 可查看的商家信息 |
|-------|-------------|-----------------|-------------------------|
| `full`    | 所有余额和交易记录    | 所有商家信息        | 所有商家信息                |
| `balances_and_redacted` | 所有余额        | 部分交易记录      | 部分商家信息                |
| `balances_only` | 仅余额        | 隐藏交易记录      | 隐藏商家信息                |
| `hidden`    | 无余额和交易记录    | 无商家信息        | 无商家信息                |

如果某个账户的交易记录为空，可能是因为其隐私设置限制了数据的显示——这并不意味着数据丢失。

## 请求限制

每位用户每分钟最多30次请求，每天最多1,000次请求。建议优先使用`get_spending_summary`而非反复调用`get_transactions`。在使用工具前，请先读取相关资源以优化请求效率。

## 常用操作模式

- **净资产**：使用`get_balances type=all`查询。
- **月度消费**：先使用`get_spending_summary period=this_month group_by=category`，再使用`group_by=merchant`获取详细信息。
- **订阅服务审计**：使用`get_recurring type=subscriptions`查询。
- **交易搜索**：使用`get_transactions search="merchant name"`或`category=FOOD_AND_DRINK min_amount:50`进行搜索。
- **Plaid分类**：`FOOD_AND_DRINK`、`TRANSPORTATION`、`ENTERTAINMENT`、`RENT_AND_UTILITIES`、`GENERAL_MERCHANDISE`、`PERSONAL_CARE`、`TRAVEL`、`MEDICAL`、`EDUCATION`、`INCOME`、`TRANSFER_IN`、`TRANSFER_OUT`、`LOAN_PAYMENTS`、`BANK_FEES`。

## 注意事项：

- 数额：正数为支出（debit），负数为收入（credit）。
- 日期格式：`YYYY-MM-DD`（UTC时间）。
- 分页：在`get_transactions`和`list_annotations`中使用`limit`和`offset`参数进行分页。
- 错误返回`isError: true`，常见原因包括请求限制（请稍后重试）、订阅服务未激活（402错误）或未启用加密货币功能。
- 注释为持久性数据，服务器端会处理；请勿在注释中存储密码、完整账户号码或敏感信息。
- 建议使用`--output json`格式输出结果，以便机器可读。