---
name: pumpfun-token-feed
description: 在Solana上提供PumpFun代币的实时流式数据服务，包括每个代币的实时美元价格。您可以使用此功能通过WebSocket订阅PumpFun代币的实时数据流：美元价格（开盘价、最高价、最低价、收盘价）、美元成交量、美元移动平均线（SMA、EMA、WMA）以及逐笔交易的美元价格变化率——所有数据均实时从Bitquery GraphQL API获取。当用户请求PumpFun代币的美元价格、PumpFun代币数据流、Solana上的热门加密货币数据、PumpFun代币的实时价格信息、PumpFun代币市场数据或任何与交易相关的PumpFun代币信息时，请务必使用此功能。触发条件包括：“pumpfun usd price”、“stream pumpfun tokens”、“live pumpfun prices”、“pumpfun token feed”、“real-time Solana meme coins”、“streaming pumpfun data”、“Bitquery pumpfun”、“pump.fun scalping”、“pump.fun momentum”、“pumpfun entry exit”等。无需等待用户明确要求使用Bitquery——如果他们需要PumpFun代币的实时数据流服务，应立即使用此功能。
---
# PumpFun代币流——实时数据流，价格以美元显示

此技能通过WebSocket提供PumpFun代币的实时数据流。每个数据点都包含以下信息：每种代币的美元价格（OHLC价格）、美元成交量、以美元计价的移动平均线（简单移动平均线SMA、指数移动平均线EMA、加权移动平均线WMA），以及每笔交易的美元价格百分比变化——所有这些数据都直接从Bitquery API获取，无需进行轮询。

该数据流仅包含地址中包含“pump”字样的Solana网络上的PumpFun代币。`Price.IsQuotedInUsd`字段始终为`true`，因此下游代码可以确认价格已以美元显示。

---

## 安装前需要注意的事项

此技能依赖于Bitquery的WebSocket接口，并使用一个外部依赖项和相应的凭证。在安装之前，请注意以下事项：

1. **注册表元数据**：尽管此技能及其脚本需要`BITQUERY_API_KEY`，但注册表中可能并未列出该密钥。请联系发布者或更新注册表元数据，确保安装者能够获取到这个密钥。
2. **API密钥在URL中**：API密钥必须作为查询参数传递给WebSocket URL，否则可能会泄露到日志或历史记录中。避免打印完整的URL，应将密钥存储在安全的环境变量中，并在密钥可能被泄露时及时更换。
3. **先在沙箱环境中测试**：在沙箱环境（如virtualenv）中运行包含的脚本，以确认其正常工作并限制潜在的影响范围。
4. **来源和发布者**：如果技能的官方网站或来源信息不明确，请核实发布者的身份或选择来自可靠来源的替代方案。如果注册表元数据中列出了`BITQUERY_API_KEY`且来源/发布者经过验证，那么该技能应该是可靠且无害的。

---

## 先决条件

- **环境要求**：
  - `BITQUERY_API_KEY`：您的Bitquery API密钥（必需）。该密钥必须通过WebSocket URL以`?token=...`的形式传递（例如：`wss://streaming.bitquery.iographql?token=YOUR_KEY`）。Bitquery不支持通过HTTP头部进行身份验证。由于密钥会出现在URL中，因此请将其视为敏感信息，避免在日志或浏览器/IDE的历史记录中显示完整的URL。
- **运行时环境**：Python 3及`pip`。需要安装依赖库：`pip install 'gql[websockets']`。

---

## 交易者的使用场景

交易者使用此数据流的主要原因如下：

**1. 买卖信号检测**
  监控每1秒的美元收盘价。当`Close (USD)`超过某个阈值或EMA与SMA出现偏离时，触发买入或卖出警报。EMA对价格变动的反应比SMA更迅速，交易者会关注流中的EMA/SMA交叉点。

**2. 动量与价格波动检测**
  跟踪每种代币的每笔交易的美元价格百分比变化。如果价格在短时间内突然上涨（例如：`+15%`），这可能是价格波动的早期信号。结合`Volume.Usd`（成交量）数据，可以判断价格波动是否真实。

**3. 做市交易（超短期交易）**
  1秒的数据间隔非常适合做市交易者。通过`Ohlc.High − Ohlc.Low`（美元价格）来衡量每秒内的价格波动。对于价格较低但成交量较大的代币，这种波动可能意味着有做市机会。

**4. 止损/止盈监控**
  监控每种代币的`Close (USD)`价格，并与交易者的买入价格进行比较。当`Close < stop_loss_usd`或`Close > take_profit_usd`时触发警报。由于价格已以美元显示（`IsQuotedInUsd: true`），因此无需进行价格转换。

**5. 成交量激增警报**
  `Volume.Usd`显示每秒的交易金额。如果某个低市值的PumpFun代币在短时间内出现大量交易，这可能是价格变动的前兆。可以通过`Volume.Usd > threshold`来筛选出这些交易。

**6. 多种代币价格仪表盘**
  订阅服务会同时返回所有活跃的PumpFun代币的信息。可以构建一个实时排行榜，根据美元价格变化幅度、成交量或价格波动范围对代币进行排序，便于全面了解PumpFun市场的情况。

**7. 均值回归策略**
  当`Close (USD)`与`Average.Mean (USD)`出现显著偏离时，采用均值回归策略的交易者会预期价格会回归。通过`(Close − Mean) / Mean > X%`来判断价格是否过度偏离。

**8. 新代币发布监控**
  新发布的PumpFun代币会在流中立即显示。交易者可以通过`tick_count == 1`来识别新发布的代币。

---

## 步骤1——检查API密钥

```python
import os
api_key = os.getenv("BITQUERY_API_KEY")
if not api_key:
    print("ERROR: BITQUERY_API_KEY environment variable is not set.")
    print("Run: export BITQUERY_API_KEY=your_token")
    exit(1)
```

如果API密钥缺失，请告知用户并停止安装流程。切勿在没有密钥的情况下继续操作。

---

## 步骤2——启动数据流

安装一次WebSocket相关的依赖库：

```bash
pip install 'gql[websockets]'
```

然后使用流处理脚本：

```bash
python ~/.openclaw/skills/pumpfun-token-feed/scripts/stream_pumpfun.py
```

**可选**：运行N秒后停止数据流：

```bash
python ~/.openclaw/skills/pumpfun-token-feed/scripts/stream_pumpfun.py --timeout 60
```

或者使用Python直接订阅数据流：

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
            subscription {
                Trading {
                    Tokens(
                        where: {
                            Interval: {Time: {Duration: {eq: 1}}},
                            Token: {
                                NetworkBid: {},
                                Network: {is: "Solana"},
                                Address: {includesCaseInsensitive: "pump"}
                            }
                        }
                    ) {
                        Token { Address Name Symbol Network }
                        Block { Time }
                        Price {
                            IsQuotedInUsd
                            Ohlc { Open High Low Close }
                            Average { Mean SimpleMoving ExponentialMoving WeightedSimpleMoving }
                        }
                        Volume { Usd }
                    }
                }
            }
        """)
        async for result in session.subscribe(sub):
            tokens = result["Trading"]["Tokens"]
            for t in tokens:
                ohlc = t["Price"]["Ohlc"]
                vol  = t["Volume"]["Usd"]
                print(
                    f"{t['Token']['Symbol']} | "
                    f"USD Close: ${float(ohlc['Close']):.8f} | "
                    f"Vol USD: ${float(vol):,.2f}"
                )

asyncio.run(main())
```

---

## 每个数据点的美元价格信息

流中的所有价格均已以美元显示（PumpFun/Solana代币的`Price.IsQuotedInUsd`字段为`true`），无需进行价格转换。

| 字段 | 对交易者的意义 |
|---|---|
| `Price.Ohlc.Open` (USD) | 该1秒数据点的开盘美元价格 |
| `Price.Ohlc.High` (USD) | 该1秒数据点的最高美元价格 |
| `Price.Ohlc.Low` (USD) | 该1秒数据点的最低美元价格 |
| `Price.Ohlc.Close` (USD) | 最终美元价格——用于买卖/止损逻辑 |
| `Price.Average.Mean` (USD) | 该时间段的美元平均价格 |
| `Price.Average.SimpleMoving` (USD) | SMA——平滑后的美元价格趋势线 |
| `Price.Average.ExponentialMoving` (USD) | EMA——对美元价格变动反应更迅速 |
| `Price.Average.WeightedSimpleMoving` (USD) | WMA——加权美元平均价格 |
| `Volume.Usd` | 该1秒数据点的总交易金额——用于判断市场活跃度或价格波动 |
| Tick Δ % | 根据连续的收盘价计算得出的价格百分比变化 |

> **关于美元价格单位**：PumpFun代币的交易价格通常在`$0.00000001`至`$0.001`之间。请始终显示8位小数，以避免显示`$0.00`这样的零值。

---

## 为交易者格式化输出数据

在向交易者展示数据时，使用以下格式：

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
PumpFun: BONK  (bonkABcD...pumpXyZw)  [Solana]
Time: 2025-03-06T14:00:01Z
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
USD Price  │  Open:  $0.00001234   High: $0.00001350
           │  Low:   $0.00001200   Close: $0.00001310  ← entry/exit ref
USD Averages
  Mean:    $0.00001270
  SMA:     $0.00001260
  EMA:     $0.00001275   (EMA > SMA → bullish momentum)
  WMA:     $0.00001268
Tick Δ:   +0.61% USD vs previous tick

USD Volume:  $45,678.00   ← whale check
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## 订阅间隔

默认订阅使用1秒的数据间隔（`duration 1`）。`Trading.Tokens`订阅支持其他时间间隔，具体取决于交易者的需求：

| 时间间隔 | 使用场景 |
|---|---|
| `1` | 做市交易、价格波动检测（1秒数据） |
| `5` | 短期价格趋势分析（5秒数据） |
| `60` | 日内价格波动分析（1分钟蜡烛图） |
| `1440` | 长期跟踪（1天数据） |

---

## 过滤逻辑

订阅服务会根据以下三个条件同时过滤代币：
- `Network: {is: "Solana"}`——仅限Solana区块链上的代币 |
- `Address: {includesCaseInsensitive: "pump"}`——地址中必须包含“pump”（表示PumpFun代币） |
- `NetworkBid: {}`——Bitquery网络出价过滤器（必需） |
- `Interval.Time.Duration: {eq: 1}`——1秒间隔的数据点 |

---

## 错误处理

- **缺少BITQUERY_API_KEY**：提示用户导出该密钥并停止操作。
- **WebSocket连接失败/401错误**：可能是API密钥无效或已过期（认证信息仅通过URL的`?token=`参数传递，切勿在HTTP头部传递密钥）。
- **订阅数据中的错误**：记录错误并优雅地停止服务（发送完整日志并关闭连接）。
- **未收到数据点**：Bitquery可能需要一段时间才能发送第一个数据点；PumpFun代币的交易活动可能是间歇性的。
- **所有价格显示为$0.00**：由于PumpFun代币的价格通常低于$0.0001，因此需要显示8位小数。

---

## 参考资料

完整的字段说明请参阅`referencesgraphql-fields.md`。您可以根据需要使用该文件添加过滤条件或请求额外的数据字段（例如特定代币地址、时间范围等）。