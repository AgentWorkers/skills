---
name: stripe-manager
description: "错误：需要使用 `--action` 参数。当您需要使用 Stripe 管理器功能时，请使用该参数。该参数会在以下情况下被触发：`stripe manager`、`key`、`customer-id`、`amount`、`currency`、`desc`。"
---
# Stripe Manager

这是一个功能齐全的Stripe支付管理工具包，支持通过命令行使用Stripe REST API来管理客户信息、账单、订阅服务、生成支付链接、查询账户余额、管理产品和价格、处理退款以及获取支付分析数据。

## 产品描述

Stripe Manager允许您完全访问您的Stripe账户，执行各种支付相关操作：列出并搜索客户信息、查看账单历史记录、管理订阅服务、创建和配置产品和价格、生成支付链接、处理退款、查询账户余额以及获取财务摘要。该工具同时支持实时模式（`sk_live_`）和测试模式（`sk_test_`）的API密钥。非常适合用于支付操作、财务报告、订阅服务管理和电子商务自动化场景。

## 使用要求

- `get-balance`：查询账户余额
- `list-customers`：列出所有客户
- `create-customer`：创建新客户
- `get-customer`：获取客户详细信息
- `list-charges`：列出所有账单
- `list-subscriptions`：列出所有订阅服务
- `list-products`：列出所有产品
- `list-invoices`：列出所有发票
- `list-events`：列出所有交易事件

请从 [configured-endpoint] 获取您的API密钥。

## 命令说明

请参考上述命令列表。

## 环境变量

| 变量          | 是否必需 | 说明                          |
|-----------------|---------|---------------------------------------------|
| `STRIPE_API_KEY`    | 是       | Stripe的秘密访问密钥（实时模式或测试模式）            |
| `STRIPE_OUTPUT_FORMAT` | 否       | 输出格式：`table`、`json` 或 `markdown`               |

## 使用示例

```bash
# List customers
STRIPE_API_KEY=sk_test_xxx stripe-manager customers 20

# Create a customer
STRIPE_API_KEY=sk_test_xxx stripe-manager customer create "alice@example.com" "Alice Smith"

# Check balance
STRIPE_API_KEY=sk_test_xxx stripe-manager balance

# List charges
STRIPE_API_KEY=sk_test_xxx stripe-manager charges 10

# Refund a charge
STRIPE_API_KEY=sk_test_xxx stripe-manager refund ch_1234 5000

# Create a product and price
STRIPE_API_KEY=sk_test_xxx stripe-manager product create "Pro Plan" "Professional subscription"
STRIPE_API_KEY=sk_test_xxx stripe-manager price create prod_xxx 2999 usd month

# Create a payment link
STRIPE_API_KEY=sk_test_xxx stripe-manager paylink price_xxx 1

# Revenue summary
STRIPE_API_KEY=sk_test_xxx stripe-manager summary 30
```
---
💬 意见反馈与功能请求：https://bytesagain.com/feedback
由BytesAgain提供支持 | bytesagain.com