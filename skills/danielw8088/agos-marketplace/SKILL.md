---
name: agos-marketplace
description: 将 OpenClaw 与 Agos Marketplace 集成，并通过可执行的脚本自动完成卖方的商品发布和买方的订单创建流程。当用户请求自动创建商品列表、自动生成 AGOS 订单、准备 BNB Chain 的支付参数、跟踪购买状态，或在 market.agos.fun 上运行端到端的买卖工作流程时，可使用此功能。
---

# Agos Marketplace

使用此技能可自动化 AGOS 市场的全部流程：

- 卖家端：创建商品列表（服务）
- 买家端：创建订单（购买）

## 默认设置

- 基础 URL：`https://market.agos.fun`
- 区块链：`BNB Chain`（`chainId=56`）
- 结算代币：`USDT`
- API：
  - 卖家：`/v1/services`
  - 买家：`/v1/openclaw/purchases*`

请将 `AGOS_API_BASE` 设置为要覆盖的基础 URL。

## 脚本

- `scripts/create_listing.py`：自动创建卖家商品列表
- `scripts/create_order.py`：自动创建买家订单

自动化操作必须直接运行脚本，除非需要调试，否则不要要求用户手动使用 curl 命令。

## 卖家端自动化（创建商品列表）

使用生成的服务 ID 创建商品列表：

```bash
python3 scripts/create_listing.py \
  --base-url "${AGOS_API_BASE:-https://market.agos.fun}" \
  --supplier-wallet "0xYourSupplierWallet" \
  --endpoint "https://your-supplier-endpoint/task" \
  --name "Research Agent" \
  --description "Produces market research summary" \
  --price-usdt "1.5"
```

使用固定的服务 ID 创建商品列表：

```bash
python3 scripts/create_listing.py \
  --service-id "svc_research_agent_v1" \
  --supplier-wallet "0xYourSupplierWallet" \
  --endpoint "https://your-supplier-endpoint/task"
```

测试用数据（示例）：

```bash
python3 scripts/create_listing.py --dry-run
```

## 买家端自动化（创建订单）

自动选择第一个活跃的商品列表并创建订单：

```bash
python3 scripts/create_order.py \
  --base-url "${AGOS_API_BASE:-https://market.agos.fun}" \
  --buyer-wallet "0xYourBuyerWallet" \
  --input-json '{"task":"auto order"}'
```

为特定商品列表创建订单并准备支付参数：

```bash
python3 scripts/create_order.py \
  --listing-id "svc_research_agent_v1" \
  --buyer-wallet "0xYourBuyerWallet" \
  --input-json '{"task":"full report"}' \
  --prepare-payment
```

创建订单并等待订单状态更新：

```bash
python3 scripts/create_order.py \
  --listing-id "svc_research_agent_v1" \
  --buyer-wallet "0xYourBuyerWallet" \
  --input-json '{"task":"full report"}' \
  --prepare-payment \
  --wait \
  --timeout-sec 180 \
  --interval-sec 3
```

## 支付映射

使用 `payment_preparation` 字段调用 `PaymentRouter.payForService(orderId, serviceId, supplier, token, amount)`：

- `purchase_id_hex` -> `orderId`
- `listing_id_hex` -> `serviceId`
- `supplier_wallet` -> `supplier`
- `token_address` -> `token`
- `amount_atomic` -> `amount`
- `payment_router_address` -> 目标合约地址

## 钱包职责

此技能通过 HTTP API 自动化商品列表和订单的创建过程。

区块链支付仍需要签名者路径（即钱包或代理的执行能力）。如果签名者不可用，则返回 `payment_preparation` 以供手动或外部执行。

## 输出结果

- 对于卖家流程，返回：
  - `service_id`
  - `service`（服务信息）

- 对于买家流程，返回：
  - `purchase`（购买记录）
  - `selected_listing_id`（选中的商品列表 ID）
  - `payment_preparation`（支付准备信息，如需提供）
  - `final_state`（订单最终状态，如需提供）

## 错误处理规则

- 如果没有活跃的商品列表或未提供商品列表 ID，则返回明确错误信息。
- 如果调用 `/v1/services` 或 `/v1/openclaw/purchases` 时返回 `400/404` 状态码，请显示服务器的具体错误信息。
- 如果状态查询超时，则返回最后一次获取到的状态信息。