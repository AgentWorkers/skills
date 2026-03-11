---
name: Payments & Banking
description: 资金钱包功能包括：转账、汇款以及货币兑换。支持多种支付方式进行充值，并提供国际货币转账服务。
version: 1.0.0
---
# 支付与银行服务

当用户需要为钱包充值、汇款或进行货币兑换时，请使用此技能。

## 可用工具

- `get_balance` — 获取当前账户余额 | `GET /api/v1/bank/balance` | 需要认证
- `get_masterpay_balance` — 获取 MasterPay 主钱包余额 | `GET /api/v1/masterpay/balance` | 需要认证
- `list_card_wallets` — 列出所有 MasterPay 卡钱包及其余额 | `GET /api/v1/masterpay/wallets` | 需要认证
- `get_topup_methods` — 获取可用的充值方式 | `GET /api/v1/bank/topup/payment_methods` | 需要认证
- `get_topup_quote` — 获取充值金额的报价 | `POST /api/v1/bank/topup/quote` | 需要认证
- `initiate_topup` — 开始充值交易 | `POST /api/v1/bank/topup` | 需要认证
- `get_topup_status` — 查看充值状态 | `GET /api/v1/bank/topup/:id` | 需要认证
- `confirm_topup` — 确认待处理的充值请求 | `POST /api/v1/bank/topup/:id/confirm` | 需要认证
- `get_transfer_quote` — 获取转账报价 | `POST /api/v1/bank/transfer/quote` | 需要认证
- `initiate_transfer` — 开始转账交易 | `POST /api/v1/bank/transfer` | 需要认证
- `get_transfer_status` | 查看转账状态 | `GET /api/v1/bank/transfer/:id` | 需要认证
- `confirm_transfer` | 确认待处理的转账请求 | `POST /api/v1/bank/transfer/:id/confirm` | 需要交易 PIN
- `get_remittance_countries` | 获取支持的汇款目的地国家 | `GET /api/v1/bank/transfer/remittance/countries` | 需要认证
- `get_exchange_rate` | 获取货币对的当前汇率 | `GET /api/v1/bank/transfer/remittance/rate` | 需要认证
- `get_remittance_reference_data` | 获取汇款表单的参考信息（银行、分行等） | `GET /api/v1/bank/transfer/remittance/reference-data` | 需要认证
- `get_remittance_quote` | 获取国际汇款的报价 | `POST /api/v1/bank/transfer/remittance/quote` | 需要认证
- `initiate/remittance` | 开始国际汇款 | `POST /api/v1/bank/transfer/remittance` | 需要认证
- `get_remittance_status` | 查看汇款状态 | `GET /api/v1/bank/transfer/remittance/:id` | 需要认证
- `get_remittance_history` | 查看汇款交易历史 | `GET /api/v1/bank/transfer/remittance/history` | 需要认证
- `confirm/remittance` | 确认待处理的汇款请求 | `POST /api/v1/bank/transfer/remittance/:id/confirm` | 需要交易 PIN
- `cancel/remittance` | 取消待处理的汇款请求 | `POST /api/v1/bank/transfer/remittance/:id/cancel` | 需要认证
- `list_recipients` | 列出保存的收款人信息 | `GET /api/v1/bank/transfer/remittance/recipients` | 需要认证
- `create_recipient` | 创建新的收款人信息 | `POST /api/v1/bank/transfer/remittance/recipients` | 需要认证
- `get_recipient` | 获取保存的收款人详情 | `GET /api/v1/bank/transfer/remittance/recipients/:recipient_id` | 需要认证
- `update_recipient` | 更新保存的收款人信息 | `PUT /api/v1/bank/transfer/remittance/recipients/:recipient_id` | 需要认证
- `delete_recipient` | 删除保存的收款人信息 | `DELETE /api/v1/bank/transfer/remittance/recipients/:recipient_id` | 需要认证
- `get_conversion_pairs` | 获取可用的货币兑换对 | `GET /api/v1/bank/convert/pairs` | 需要认证
- `get_conversion_rate` | 获取两种货币之间的兑换率 | `GET /api/v1/bank/convert/rate` | 需要认证
- `initiate_conversion` | 开始货币兑换 | `POST /api/v1/bank/convert` | 需要认证
- `confirm_conversion` | 确认待处理的兑换请求 | `POST /api/v1/bank/convert/:id/confirm` | 需要交易 PIN
- `list_transactions` | 分页查看交易历史 | `GET /api/v1/transactions` | 需要认证
- `get_transaction` | 获取特定交易的详情 | `GET /api/v1/transactions/:id` | 需要认证
- `downloadreceipt` | 以 PDF 格式下载交易收据 | `GET /api/v1/transactions/:id/receipt/pdf` | 需要认证

## 推荐操作流程

### 为钱包充值

1. 获取可用的充值方式：`GET /api/v1/bank/topup/payment_methods`
2. 获取充值报价：`POST /api/v1/bank/topup/quote`（提供 `amount`、`currency`、`payment_method` 参数）
3. 开始充值：`POST /api/v1/bank/topup`（使用报价信息）
4. 确认充值：`POST /api/v1/bank/topup/:id/confirm`

### 发送国际汇款

1. 查看可汇款的国家：`GET /api/v1/bank/transfer/remittance/countries`
2. 获取汇率：`GET /api/v1/bank/transfer/remittance/rate?from=USD&to=PHP`
3. 创建或选择收款人：`POST/GET /api/v1/bank/transfer/remittance/recipients`
4. 获取汇款报价：`POST /api/v1/bank/transfer/remittance/quote`
5. 开始汇款：`POST /api/v1/bank/transfer/remittance`
6. 确认汇款：`POST /api/v1/bank/transfer/remittance/:id/confirm`（需要交易 PIN）

## 规则

- 所有金融操作均需要认证。
- 充值和转账操作必须先获取报价，然后确认；请勿跳过报价步骤。
- 转账、汇款和货币兑换的确认操作需要输入交易 PIN；充值操作不需要。
- 汇款操作需要保存收款人信息；如未保存，请使用 `create_recipient` 创建收款人。
- 报价中的汇率仅供参考，实际汇率可能在确认时发生变化。
- 交易历史记录采用分页显示；请使用 `page` 和 `page_size` 参数进行分页查询。

## 代理操作指南

执行此技能时，请遵循以下说明：

- 严格按照文档中规定的操作流程进行，切勿跳过任何步骤。
- 如果某个工具需要认证，请确保会话中包含有效的令牌（bearer token）。
- 如果某个工具需要交易 PIN，请每次操作时都向用户索取新的 PIN；切勿缓存或记录 PIN。
- 严禁泄露、记录或保存任何敏感信息（密码、令牌、完整卡号、CVV 码等）。
- 如果用户请求超出此技能范围的操作，请拒绝请求并推荐相应的技能。
- 如果某一步骤失败，请查看错误信息，并按照提供的恢复指南进行操作后再重试。
- 所有金融操作都必须先获取报价，切勿直接开始操作。
- 转账、汇款和货币兑换的确认操作需要输入交易 PIN；充值操作不需要。
- 汇款操作需要保存收款人信息；如未保存，请使用 `create_recipient` 创建收款人。
- 报价中的汇率仅供参考；最终汇率在确认时确定。
- 交易历史记录采用分页显示；请使用 `page` 和 `page_size` 参数进行分页查询。