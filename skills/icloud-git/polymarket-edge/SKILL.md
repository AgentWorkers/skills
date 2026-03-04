---
name: polymarket-edge
description: "使用5分钟周期的BTC EMA交叉策略，在Polymarket预测市场中进行交易与分析。您可以浏览市场、查看订单簿、执行交易信号、管理自动交易系统，并查看投资组合的持仓情况。所有服务均通过SkillPay.me按每次调用收费（0.001 USDT/次调用，使用BNB Chain的USDT支付）。"
metadata:
  openclaw:
    requires:
      env:
        - SKILL_BILLING_API_KEY
        - SKILL_ID
      bins:
        - python3
        - pip
    primaryEnv: SKILL_BILLING_API_KEY
---
# Polymarket Edge

这是一个在本地运行的FastAPI技能（skill），它封装了Polymarket的Gamma API和CLOB API，并内置了EMA(5/20)交叉策略以及SkillPay.me计费功能。

## 设置

```bash
# Install dependencies
pip install -r requirements.txt

# Set required environment variables
export SKILL_BILLING_API_KEY=sk_your_skillpay_api_key_here
export SKILL_ID=polymarket-edge

# Start the skill server (port 8080)
python main.py
```

交互式文档可在 `http://localhost:8080/docs` 查看。

## 环境变量

| 变量 | 是否必需 | 描述 |
|---|---|---|
| `SKILL_BILLING_API_KEY` | ✅ | 来自您的skillpay.me控制面板 |
| `SKILL_ID` | ✅ | 您的技能名称，例如 `polymarket-edge` |
| `POLYMARKET_PRIVATE_KEY` | 可选 | 用于执行实时交易的EVM私钥 |

## 计费

每个被计费的API请求都需要在查询字符串中添加 `?user_id=<id>`。  
如果用户没有足够的代币，API会返回 **HTTP 402** 错误，并提供充值链接（`top_up_url`）。

```
GET  /balance?user_id=alice          → current token balance
GET  /topup?user_id=alice&amount=10  → BNB Chain USDT payment link
```

1 USDT = 1000个代币；1次调用 = 1个代币；最低充值金额为8 USDT；SkillPay的费用为5%。

## 主要API端点（所有端点都需要 `?user_id=`）

### 市场数据
```
GET /markets/search?q=bitcoin    Search all Polymarket markets
GET /markets/btc                 List active BTC/Bitcoin markets
GET /market/{id}                 Single market details
GET /market/{token_id}/book      Full order book (bids + asks)
GET /market/{token_id}/price     Mid-price, spread, implied probability
GET /market/{token_id}/history   5-min OHLCV candles
```

### 策略信号
```
POST /signal                     Run EMA crossover on top BTC markets
                                 Returns BUY_YES / BUY_NO / HOLD / SKIP per market
```

### 自动交易器
```
GET  /autotrader/status          Is the auto-trader running?
POST /autotrader/start           Start 5-min BTC cycle (background task)
POST /autotrader/stop            Stop auto-trader
GET  /autotrader/log             Last 50 trade log entries
```

### 投资组合
```
GET /portfolio?wallet=0x...      Open positions + USD value for a wallet
```

## 策略逻辑

- **价格数据**：从Polymarket CLOB获取5分钟内的YES代币价格历史数据。
- **交易信号**：当EMA(5)向上穿越EMA(20)时，执行 `BUY_YES`；向下穿越时，执行 `BUY_NO`。
- **过滤条件**：如果价差大于0.05，或者YES代币的价格不在[0.15, 0.85]区间内，则忽略该信号。
- **实时交易**：在 `/autotrader/start` 请求中设置 `?auto_trade=true`（需要 `POLYMARKET_PRIVATE_KEY` 和 `py-clob-client`）。

## 实时交易（可选）

```bash
pip install py-clob-client
export POLYMARKET_PRIVATE_KEY=0x<your_burner_wallet>
# Then uncomment the py-clob-client block in polymarket_client.py
curl -X POST "http://localhost:8080/autotrader/start?user_id=alice&auto_trade=true"
```

⚠️ 请使用临时钱包（burner wallet）进行交易。切勿泄露您的私钥。