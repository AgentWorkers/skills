---
name: polymarket
description: "与 Polymarket US 的预测市场进行交互。用户可以使用该功能来：浏览/搜索预测市场、查看市场价格和赔率、查看投资组合的持仓和余额、下达或取消交易、查询订单状态、查找相关事件或体育赛事信息，以及获取市场结算信息。此功能需要 `polymarket-us` Python 包，交易时还可以选择使用 API 密钥。"
---
# Polymarket US

通过 Polymarket US API 使用 Python SDK 进行交易和浏览预测市场。

## 设置

确保已安装 SDK：
```bash
pip install polymarket-us
```

API 密钥仅用于交易/投资组合相关接口。请在 [https://polymarket.us/developer](https://polymarket.us/developer) 生成 API 密钥。

将凭据存储为环境变量：
- `POLYMARKET_KEY_ID` — API 密钥的 UUID
- `POLYMARKET_SECRET_KEY` — Ed25519 私钥（base64 编码）

## 使用方法

使用 `polymarket_us` SDK 编写并执行 Python 脚本。有关完整的 API 详情，请参阅 [references/api_reference.md](references/api_reference.md)。

### 公开数据（无需认证）

```python
from polymarket_us import PolymarketUS
client = PolymarketUS()

# Search markets
results = client.search.query({"query": "bitcoin", "limit": 5})

# Browse trending markets
markets = client.markets.list({"limit": 10, "orderBy": ["volumeNum"], "orderDirection": "desc"})

# Check price
bbo = client.markets.bbo("market-slug")

client.close()
```

### 交易（需要认证）

```python
import os
from polymarket_us import PolymarketUS

client = PolymarketUS(
    key_id=os.environ["POLYMARKET_KEY_ID"],
    secret_key=os.environ["POLYMARKET_SECRET_KEY"],
)

# Check balance
balances = client.account.balances()

# View positions
positions = client.portfolio.positions()

# Preview then place order
preview = client.orders.preview({"request": {
    "marketSlug": "some-market",
    "intent": "ORDER_INTENT_BUY_LONG",
    "type": "ORDER_TYPE_LIMIT",
    "price": {"value": "0.55", "currency": "USD"},
    "quantity": 100,
}})

# Place order (ALWAYS confirm with user before executing)
order = client.orders.create({
    "marketSlug": "some-market",
    "intent": "ORDER_INTENT_BUY_LONG",
    "type": "ORDER_TYPE_LIMIT",
    "price": {"value": "0.55", "currency": "USD"},
    "quantity": 100,
    "tif": "TIME_IN_FORCE_GOOD_TILL_CANCEL",
})

client.close()
```

## 规则说明

1. **下单前务必预览订单内容** — 向用户展示他们即将进行的交易内容。
2. **下单前必须获得用户确认** — 禁止自动交易。
3. **价格始终代表“YES”方的概率** — 例如，要购买“NO”选项，应将价格设置为 $0.60（即 1.00 - 0.40）。
4. **在市场中，第一支队伍代表“YES”，第二支队伍代表“NO”。
5. **有效价格范围**：0.001 至 0.999。
6. **优雅地处理错误** — 捕获 `AuthenticationError`、`BadRequestError`、`RateLimitError` 等异常。

## 结果展示格式

在向用户展示市场数据时：
- 清晰地显示市场标题或问题内容。
- 以百分比形式显示“YES”/“NO”选项的价格（例如，55¢ 表示 55% 的概率）。
- 对于持仓情况，显示盈亏（P&L）和当前价值。
- 保持语言简洁易懂 — 这是预测市场，让体验更加有趣。