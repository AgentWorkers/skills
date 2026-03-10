---
name: bitcoin-price-feed
description: 实时流式比特币价格推送服务，专为交易者设计。通过该功能，您可以订阅基于WebSocket的实时比特币价格数据流：包括OHLC价格走势、交易量以及衍生指标（如移动平均线、百分比变化值），这些数据均实时从Bitquery的GraphQL API获取。每当用户请求比特币价格信息、实时比特币价格、实时加密货币价格或流式市场数据时，务必使用此功能。触发条件包括：“bitcoin price feed”、“stream Bitcoin price”、“live Bitcoin price”、“real-time BTC”、“streaming crypto prices”或任何与实时/流式加密货币价格相关的请求。无需等待用户明确要求使用Bitquery——只要他们需要实时比特币价格数据，即可立即使用该服务。
---
# 比特币价格流 — 实时数据传输

此技能可为您提供通过 WebSocket 实时传输的比特币价格数据：包括实时的 OHLC 价格数据（开盘价、最高价、最低价、收盘价）和成交量，以及一些派生指标（如移动平均线（SMA、EMA、WMA）和每笔交易的百分比变化）。数据直接从 Bitquery API 实时传输，无需进行轮询。

**使用场景**：
- 实时获取比特币价格数据
- 获取派生指标（如移动平均线和每笔交易的百分比变化）
- 用于交易或仪表盘展示的实时 OHLC 价格和成交量数据

---

## 先决条件**

- **环境设置**：`BITQUERY_API_KEY` — 您的 Bitquery API 密钥（必需）。该密钥必须通过 WebSocket URL 以 `?token=...` 的形式传递（例如：`wss://streaming.bitquery.iographql?token=YOUR_KEY`）。Bitquery 不支持通过请求头进行身份验证。由于密钥会显示在 URL 中，因此请将其视为敏感信息，避免在日志或浏览器/IDE 的历史记录中显示完整 URL。
- **运行环境**：Python 3 和 `pip`。需要安装以下依赖库：`pip install 'gql[websockets']`。

---

## 第一步 — 验证 API 密钥

```python
import os
api_key = os.getenv("BITQUERY_API_KEY")
if not api_key:
    print("ERROR: BITQUERY_API_KEY environment variable is not set.")
    print("Run: export BITQUERY_API_KEY=your_token")
    exit(1)
```

如果密钥缺失，请告知用户并停止操作。请确保密钥已正确设置后再继续。

## 第二步 — 启动数据流

**安装 WebSocket 相关依赖库**：

```bash
pip install 'gql[websockets]'
```

**运行实时数据流脚本**（订阅比特币价格数据）：

```bash
python ~/.openclaw/skills/bitcoin-price-feed/scripts/stream_bitquery.py
```

**可选**：在 N 秒后自动停止数据流：

```bash
python ~/.openclaw/skills/bitcoin-price-feed/scripts/stream_bitquery.py --timeout 60
```

**或者使用 Python 直接订阅实时数据流**：

```python
import asyncio
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
                    Tokens(where: {Currency: {Id: {is: "bid:bitcoin"}}, Interval: {Time: {Duration: {eq: 1}}}}) {
                        Token { Name Symbol Network }
                        Block { Time }
                        Price { Ohlc { Open High Low Close } Average { Mean SimpleMoving ExponentialMoving } }
                        Volume { Usd }
                    }
                }
            }
        """)
        async for result in session.subscribe(sub):
            print(result)  # each tick streamed in real time

asyncio.run(main())
```

---

## 数据流内容**

每笔交易数据包含以下信息：
- 每 1 秒间隔的 OHLC 价格（开盘价、最高价、最低价、收盘价）和成交量（单位：美元）
- 从 Bitquery 获取的派生指标：简单移动平均线（SMA）、指数移动平均线（EMA）、加权简单移动平均线（WMA）
- **基于会话的计算结果**：与上一笔交易的百分比变化

数据流会持续运行，直到您手动停止（使用 Ctrl+C）或通过命令行参数 `--timeout` 设置超时时间。

## 第三步 — 清晰地展示数据

在向用户展示数据时，请使用易于理解的格式。

---

## 订阅间隔**

默认订阅间隔为 1 秒（即每秒更新一次数据）。如果 API 支持其他时间间隔，您可以使用类似的订阅方式（例如 `Trading.Tokens`，并指定间隔为 5、60、1440，分别对应 5 分钟、1 小时、1 天的时间段）。

## 错误处理**
- **缺少 BITQUERY_API_KEY**：请用户提供正确的密钥并停止操作。
- **WebSocket 连接失败或收到 401 错误**：可能是密钥无效或已过期（请确保密钥仅通过 URL 的 `?token=` 参数传递）。
- **数据流中的错误**：记录错误信息并优雅地终止程序（关闭所有通信连接）。
- **未收到任何数据**：检查密钥和网络连接；Bitquery 可能需要一段时间才能发送第一笔交易数据。

## 参考资料**

完整的字段参考信息请参见 `referencesgraphql-fields.md`。您可以根据需要使用该文件添加过滤条件或请求额外的数据字段（例如时间范围）。