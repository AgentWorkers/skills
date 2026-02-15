---
name: binance-dca-tool
description: Binance的“成本平均法（DCA）”工具支持自动化和手动重复购买加密货币的功能。用户可以使用该工具来制定DCA策略、在Binance平台上执行重复购买操作、查看DCA投资计划、查看交易历史记录，或管理任意交易对（如BTC/USDT、ETH/USDT等）的系统性购买计划。该工具会在用户请求进行DCA投资、重复购买、成本平均、资产积累操作或Binance现货交易时自动触发相应的功能。
---

# Binance DCA

在 Binance 上执行和规划定投（Dollar-Cost Averaging）策略。

## 设置

需要两个环境变量（切勿将它们硬编码）：

```bash
export BINANCE_API_KEY="your-key"
export BINANCE_SECRET_KEY="your-secret"
```

可选：`BINANCE_BASE_URL`（默认值为 `https://api.binance.com`）。使用 `https://testnet.binance.vision` 进行模拟交易。

## 快速入门

```bash
# Check current BTC price
bash scripts/dca.sh price BTCUSDT

# Project a DCA plan: $50 every 7 days, 12 buys
bash scripts/dca.sh plan 50 7 12 BTCUSDT

# Execute a $50 market buy
bash scripts/dca.sh buy BTCUSDT 50

# Check recent trades
bash scripts/dca.sh history BTCUSDT 10

# Check USDT balance
bash scripts/dca.sh balance USDT
```

## 操作

### price [SYMBOL]
获取当前现货价格。默认为 BTCUSDT。

### balance [ASSET]
检查某种资产的可用余额和锁定余额。默认为 USDT。

### buy SYMBOL AMOUNT [TYPE] [PRICE]
下达买入订单。`AMOUNT` 以报价货币（USDT）表示。
- `MARKET`（默认）：以市场价格立即执行
- `LIMIT`：需要指定价格参数 — 例如：`buy BTCUSDT 50 LIMIT 95000`

### history [SYMBOL] [LIMIT]
显示带有时间戳、方向、数量、价格和费用的最近交易记录。

### plan [AMOUNT] [FREQ_days] [NUM_BUYS] [SYMBOL]
制定定投计划，并展示在不同价格水平下的盈亏情况（-30% 至 +100%）。默认参数：$50，每 7 天买入一次，资产为 BTCUSDT。

## DCA 策略指导

在帮助用户规划定投时，请注意以下几点：
1. **询问预算**：每次买入的金额是多少？购买的频率是多少？
2. **设定预期**：定投可以平滑价格波动，但不能保证盈利。
3. **进行预测**：在正式执行前，使用 `plan` 功能展示不同的投资情景。
4. **建议先在测试网（testnet）进行测试**：将 `BINANCE_BASE_URL` 设置为 `https://testnet.binance.vision`。
5. **仓位大小**：建议每次买入占投资组合的 1-2%，以采取保守的投资策略。
6. **切勿存储凭据**：始终使用环境变量来保存敏感信息。

## 定投计划的调度

对于自动化的定期买入操作，建议设置 cron 作业或使用 OpenClaw 的 cron 功能进行调度：

```
# Example: buy $50 BTC every Monday at 9am UTC
0 9 * * 1 BINANCE_API_KEY=... BINANCE_SECRET_KEY=... /path/to/dca.sh buy BTCUSDT 50
```

或者通过 OpenClaw 的 cron 功能进行代理管理的调度，并设置提醒和确认机制。

## 错误处理

- 缺少 API 密钥 → 显示包含设置说明的错误信息。
- 金额无效 → 在调用 API 之前进行验证。
- API 请求失败 → 显示包含错误详情和端点信息的错误信息。
- 在向用户确认之前，务必验证订单的响应状态。