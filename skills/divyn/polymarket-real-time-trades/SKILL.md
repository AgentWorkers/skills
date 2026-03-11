---
name: polymarket-prediction-trades
description: 实时流式 Polymarket 预测交易服务，支持在 Polygon（matic）平台上进行交易，并提供实时的 USD 价格信息。通过此功能，您可以使用 WebSocket 订阅 Polymarket 预测市场的实时交易数据：包括交易结果（买方、卖方、交易金额、抵押品金额、价格、订单 ID）、市场元数据（问题标题、数据来源、结果标签）以及交易详情。这些数据直接从 Bitquery GraphQL API 中实时获取。该服务涵盖所有 Polymarket 市场，例如体育赛事赔率、比特币涨跌市场以及其他类型的预测市场。每当用户请求 Polymarket 交易数据、实时预测市场信息、Polymarket 交易流、实时 Polymarket 数据、Polymarket 订单流、Polymarket 体育赛事赔率或任何与 Polymarket 相关的数据时，请务必使用此功能。无需用户明确要求使用 Bitquery——只要用户需要实时或流式 Polymarket 数据（包括体育赛事或加密货币市场的数据），即可立即使用此功能。
---
# Polymarket 预测交易 — 在 Polygon 上的实时流式数据

该技能通过 WebSocket 在 Polygon（matic）上提供 Polymarket 预测交易的实时流式数据。每个事件都包含以下信息：成功的预测交易结果、对应的代币数量、以美元计的抵押品金额、价格（以美元计）、买家/卖家地址、市场问题、结果标签（例如“上涨”/“下跌”）以及交易哈希。

所有显示的交易都满足 `TransactionStatus.Success: true` 的条件。该数据流使用了 Bitquery 的 `EVM.PredictionTrades` 订阅服务，以便下游代码可以构建仪表板、跟踪订单流程或监控特定市场。

**官方文档：** [Polymarket API — 获取价格、交易和市场数据](https://docs.bitquery.io/docs/examples/polymarket-api/)（Bitquery）。

---

## 安装前的注意事项

该技能的代码实现了上述的 Polymarket 数据流，并且仅与 Bitquery 进行交互。在安装之前，请注意以下事项：

1. **注册表元数据**：确认注册表元数据中声明了 `BITQUERY_API_KEY` 作为必需的凭据。如果没有这个凭据，技能在运行时将会失败。如果注册表中没有列出这个环境变量，那么这就是主要的不一致之处——请联系发布者更新注册表，以便安装者能够看到这一要求。
2. **将 API 密钥视为机密**：仅将其设置在一个环境变量中。**不要** 打印或记录完整的 WebSocket URL；该密钥会以 `?token=...` 的形式传递，并可能出现在日志或 shell 历史记录中。如果您怀疑密钥在测试或使用过程中被泄露，请及时更换密钥。
3. **先在沙箱环境中测试**：在沙箱环境（如 virtualenv 或容器）中运行捆绑的脚本，以观察其行为，然后再在生产环境中使用。
4. **验证发布者/来源**：如果该技能的官网或来源未知，请验证发布者的身份或选择来自可信来源的替代方案。如果注册表中声明了 `BITQUERY_API_KEY` 且来源经过验证，那么该技能与其描述的功能是一致的。
5. **如果密钥被泄露，请及时更换**：如果密钥可能已经被泄露（例如 URL 被打印或记录下来），请在 Bitquery 仪表板中更换密钥，并更新您的环境设置。

---

## 凭据

- **运行时所需的唯一密钥**：`BITQUERY_API_KEY`（Bitquery API 密钥）。
- **注册表**：注册表元数据应将该密钥声明为必需的凭据。如果未声明，安装者在阅读此文档或运行脚本之前可能不会意识到该技能需要 API 密钥——这是需要在注册表层面解决的主要问题。
- **使用方式**：密钥必须作为查询参数（`?token=...`）传递在 WebSocket URL 中；Bitquery 不支持基于头部的身份验证方式。由于密钥会出现在 URL 中，如果 URL 被打印或捕获，密钥泄露的风险会更高。**最佳实践**：将 `BITQUERY_API_KEY` 设置在环境变量中，切勿记录或打印完整的 WebSocket URL，并在怀疑密钥被泄露时及时更换。

---

## 先决条件

- **环境**：`BITQUERY_API_KEY`——您的 Bitquery API 密钥（必需）。请将其设置在环境变量中；脚本和示例代码会从该环境变量中读取密钥。密钥仅以 `?token=...` 的形式传递在 WebSocket URL 中；切勿打印或记录完整的 URL。
- **运行时环境**：Python 3 和 `pip`。需要安装以下依赖库：`pip install 'gql[websockets']`。

---

## 交易者的使用场景

交易者使用这些数据流的主要原因如下：

**1. 订单流程/市场活动**：监控所有已成交的订单：买家、卖家、以美元计的抵押品金额、价格（以美元计）以及交易结果（“是/否”或“上涨/下跌”）。识别最活跃的市场以及哪种交易方向（买入/卖出）占主导地位。
**2. 大额交易检测**：通过 `CollateralAmountInUSD` 或 `Amount` 过滤条件来发现大额的预测市场交易。这有助于追踪资金流向特定交易结果。
**3. 市场特定监控**：使用 `Question.MarketId`、`Question.Title` 或 `Question.Id` 来过滤数据流，仅关注某个市场（例如“以太坊价格走势 - 3 月 10 日”），并实时跟踪该市场的所有交易。
**4. 结果不平衡分析**：根据 `Outcome.Label`（例如“上涨” vs “下跌”）和 `IsOutcomeBuy` 对交易进行汇总，以了解每种结果下的净买入压力——有助于分析市场情绪或趋势。
**5. 解决方案来源/数据市场**：使用 `Question.ResolutionSource` 和 `Question.Title` 来关注由数据源或预言机驱动的市场（例如 Chainlink 数据流），并监控与解决方案相关的交易活动。
**6. 入场/出场时机判断**：通过 `PriceInUSD` 和 `CollateralAmountInUSD` 来分析每笔交易的交易规模和价格，从而帮助判断在预测市场中的入场和出场时机。
**7. 协议/市场验证**：`Marketplace.ProtocolName` 和 `ProtocolFamily`（例如“polymarket”、“Gnosis_CTF”）可以确认交易是否来自 Polygon 平台；这有助于避免与其他协议混淆。
**8. 审计追踪**：每个事件都包含 `Transaction.Hash`、`Block.Time`、`Call.Signature.Name`（例如“matchOrders”）和 `Log.Signature.Name`（例如“OrderFilled”），以便进行完整的链上审计。

---

## 第一步 — 检查 API 密钥

```python
import os
api_key = os.getenv("BITQUERY_API_KEY")
if not api_key:
    print("ERROR: BITQUERY_API_KEY environment variable is not set.")
    print("Run: export BITQUERY_API_KEY=your_token")
    exit(1)
```

如果 API 密钥缺失，请告知用户并停止操作。在没有密钥的情况下请勿继续。

---

## 第二步 — 运行数据流

安装一次 WebSocket 相关的依赖库：

```bash
pip install 'gql[websockets]'
```

然后使用流式数据获取脚本：

```bash
python ~/.openclaw/skills/polymarket-prediction-trades/scripts/stream_polymarket.py
```

**可选**：运行 N 秒后停止数据流：

```bash
python ~/.openclaw/skills/polymarket-prediction-trades/scripts/stream_polymarket.py --timeout 60
```

或者使用 Python 直接订阅数据流：

```python
import asyncio, os
from gql import Client, gql
from gql.transport.websockets import WebsocketsTransport

async def main():
    token = os.environ["BITQUERY_API_KEY"]
    url = f"wss://streaming.bitquery.io/graphql?token={token}"
    transport = WebsocketsTransport(
        url=url,
        headers={"Sec-WebSocket-Protocol": "graphql-ws"},
    )
    async with Client(transport=transport) as session:
        sub = gql("""
            subscription MyQuery {
              EVM(network: matic) {
                PredictionTrades(where: { TransactionStatus: { Success: true } }) {
                  Block { Time }
                  Call { Signature { Name } }
                  Log { Signature { Name } SmartContract }
                  Trade {
                    OutcomeTrade {
                      Buyer
                      Seller
                      Amount
                      CollateralAmount
                      CollateralAmountInUSD
                      OrderId
                      Price
                      PriceInUSD
                      IsOutcomeBuy
                    }
                    Prediction {
                      CollateralToken { Name Symbol SmartContract AssetId }
                      ConditionId
                      OutcomeToken { Name Symbol SmartContract AssetId }
                      Marketplace { SmartContract ProtocolVersion ProtocolName ProtocolFamily }
                      Question { Title ResolutionSource Image MarketId Id CreatedAt }
                      Outcome { Id Index Label }
                    }
                  }
                  Transaction { From Hash }
                }
              }
            }
        """)
        async for result in session.subscribe(sub):
            for trade in (result.get("EVM") or {}).get("PredictionTrades") or []:
                q = (trade.get("Trade") or {}).get("Prediction") or {}
                q = q.get("Question") or {}
                ot = (trade.get("Trade") or {}).get("OutcomeTrade") or {}
                pred = (trade.get("Trade") or {}).get("Prediction") or {}
                outcome = pred.get("Outcome") or {}
                print(
                    f"{q.get('Title', '?')} | "
                    f"Outcome: {outcome.get('Label', '?')} | "
                    f"${float(ot.get('CollateralAmountInUSD') or 0):.2f}"
                )

asyncio.run(main())
```

---

## 每笔交易的字段说明

| 字段          | 对交易者的意义                                      |
|---------------|-------------------------------------------|
| `Trade.OutcomeTrade.Buyer` | 买方的地址                                      |
| `Trade.OutcomeTrade.Seller` | 卖方的地址                                      |
| `Trade.OutcomeTrade.Amount` | 预测结果对应的代币数量（原始值）                        |
| `Trade.OutcomeTrade.CollateralAmount` | 抵押品代币的数量                                  |
| `Trade.OutcomeTrade.CollateralAmountInUSD` | 以美元计的抵押品金额（用于筛选大额交易）                    |
| `Trade.OutcomeTrade.OrderId` | 订单标识符                                      |
| `Trade.OutcomeTrade.Price` | 抵押品的价格（通常为 0 或 1，用于二元预测）                   |
| `Trade.OutcomeTrade.PriceInUSD` | 以美元计的价格（用于入场/出场参考）                        |
| `Trade.OutcomeTrade.IsOutcomeBuy` | `True` 表示买方购买了预测结果（“是”/“上涨”）            |
| `Trade.Prediction.Question.Title` | 市场问题（例如“以太坊价格走势 - ...”）                        |
| `Trade.Prediction.Question.MarketId` | 用于过滤的市场 ID                                  |
| `Trade.Prediction.Question.ResolutionSource` | 解决方案的来源（例如 Chainlink 的 URL）                   |
| `Trade.Prediction.Outcome.Label` | 预测结果标签（例如“上涨”、“下跌”）                        |
| `Trade.Prediction.Marketplace.ProtocolName` | 交易发生的平台名称（例如“polymarket”）                    |
| `Block.Time` | 交易的时间戳（ISO 格式）                              |
| `Transaction.Hash` | 用于审计的链上交易哈希                              |
| `Call.Signature.Name` | 用于处理交易的合约签名名称（例如“matchOrders”）                   |
| `Log.Signature.Name` | 用于记录交易状态的合约签名名称（例如“OrderFilled”）                   |

---

## 第四步 — 为交易者格式化输出数据

在向交易者展示预测交易数据时，使用以下格式：

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Polymarket  [matic]  Protocol: polymarket (Gnosis_CTF)
Time: 2026-03-10T13:21:11Z  Tx: 0x9566...f2da
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Question: Ethereum Up or Down - March 10, 9:15AM-9:30AM ET
MarketId: 1537455  |  Outcome: Down  (Index 1)
Resolution: https://data.chain.link/streams/eth-usd
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
OutcomeTrade
  Side:       BUY outcome (IsOutcomeBuy: true)
  Buyer:      0x22dc...91bb  →  Seller: 0x86a2...73a8
  Collateral: 0.316471 USDC  (USD: $0.32)
  Price:      0.632942  (USD: $0.633)
  Amount:     500000 (outcome tokens)
  OrderId:    44433632...
Call: matchOrders  |  Log: OrderFilled @ 0x4bfb...982e
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## 错误处理

- **缺少 BITQUERY_API_KEY**：告知用户导出该密钥并停止操作。
- **WebSocket 连接失败/401 错误**：API 密钥无效或已过期（认证仅通过 URL 的 `?token=` 参数进行）——请勿在请求头中传递密钥。
- **数据流中的订阅错误**：记录错误并优雅地停止操作（发送完整的数据并关闭连接）。
- **未收到任何事件**：Polymarket 的预测数据流可能不连续；请等待几秒钟或检查 Polygon 在 matic 上是否有最新的交易活动。
- **`PredictionTrades` 为空**：确保筛选条件满足 `TransactionStatus: { Success: true }`，并且网络连接处于 matic 状态。

---

## 参考资料

- **Bitquery Polymarket API 文档**：[Polymarket API — 获取价格、交易和市场数据](https://docs.bitquery.io/docs/examples/polymarket-api/)
- 完整的字段参考信息请参见 `referencesgraphql-fields.md`。您可以使用这些信息来添加筛选条件或在订阅请求中请求额外的字段（例如按 `MarketId`、`ConditionId` 或日期进行筛选）。