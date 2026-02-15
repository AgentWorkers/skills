---
name: binance-dca
description: Binance的“成本平均法（DCA）”工具支持自动和手动重复购买加密货币的功能。用户可以使用该工具来制定DCA策略，在Binance平台上执行重复购买操作，查看DCA投资计划的结果，查阅交易历史记录，或管理任何交易对（如BTC/USDT、ETH/USDT等）的系统性购买计划。该工具会在用户请求进行DCA投资、设置重复购买、执行成本平均策略或进行Binance现货交易时自动触发相应的操作。
---

# Binance DCA（定期定额投资）

在Binance平台上执行和规划定期定额投资（Dollar-Cost Averaging, DCA）策略。

## 设置

需要两个环境变量（切勿将这些变量硬编码到代码中）：

```bash
export BINANCE_API_KEY="your-key"
export BINANCE_SECRET_KEY="your-secret"
```

可选：`BINANCE_BASE_URL`（默认值为`https://api.binance.com`）。如需进行模拟交易（paper trading），请使用`https://testnet.binance.vision`。

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
获取当前现货价格。默认为BTCUSDT。

### balance [ASSET]  
查看某种资产的可用余额和锁定余额。默认为USDT。

### buy [SYMBOL] [AMOUNT] [TYPE] [PRICE]  
下达买入订单。`AMOUNT`以报价货币（USDT）为单位。  
- `MARKET`（默认）：立即以市场价格成交  
- `LIMIT`：需要指定价格参数——例如：`buy BTCUSDT 50 LIMIT 95000`  

### history [SYMBOL] [LIMIT]  
显示带有时间戳、交易方向、交易数量、价格和费用的最近交易记录。

### plan [AMOUNT] [FREQ_days] [NUM_BUYS] [SYMBOL]  
制定定期定额投资计划，并进行情景分析，展示在不同价格水平下的盈亏情况（-30%至+100%）。默认参数：每次投资50美元，每7天买入一次，资产为BTCUSDT。

## DCA策略指导

在帮助用户规划定期定额投资时，请注意以下几点：  
1. **询问预算**：每次投资多少金额，以及投资频率是多少？  
2. **明确预期**：定期定额投资可以平滑价格波动，但不能保证盈利。  
3. **进行预测**：在正式执行前，使用`plan`功能查看不同的投资情景。  
4. **建议先在测试网（testnet）进行测试**：将`BINANCE_BASE_URL`设置为`https://testnet.binance.vision`。  
5. **确定投资金额**：建议每次投资占投资组合的1-2%，以采取保守的投资策略。  
6. **切勿存储凭据**：始终使用环境变量来存储敏感信息。

## 安排定期定额投资交易  

对于自动化的重复投资，建议设置cron作业或使用OpenClaw的cron功能来安排交易，并设置提醒和确认机制。

## 错误处理  
- 缺少API密钥 → 显示包含设置说明的错误信息。  
- 金额无效 → 在调用API之前进行验证。  
- API请求失败 → 显示包含错误详情和端点信息的错误信息。  
- 在向用户确认交易结果之前，务必验证订单的响应状态。