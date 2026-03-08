---
name: evm-bnb-band-trader
description: Execute BNB Chain EVM swing trades after importing a private key: buy when trigger price exceeds market condition, then place 5% take-profit and 3% stop-loss management. Use when user asks to automate BNB band/swing trading with strict TP/SL and wallet-key based execution.
---

# EVM BNB Band Trader

实现具有严格风险控制的BNB链波段交易策略。

## 1) 配置秘钥和参数

在运行脚本之前，请设置以下环境变量：

- `EVM_PRIVATE_KEY`（钱包私钥，切勿硬编码）
- `BNB_RPC_URL`（BSC RPC端点）
- `TOKEN_IN`（输入代币，默认为WBNB）
- `TOKEN_OUT`（输出代币）
- `BUY_TRIGGER PRICE`（买入触发价格）
- `BUY_SIZE_BNB`（买入数量，单位为BNB）
- `TAKE_PROFIT_PCT`（盈利止盈百分比，默认为0.05）
- `STOP_LOSS_PCT`（止损百分比，默认为0.03）
- `POLL_SECONDS`（轮询间隔，默认为10秒）

## 2) 运行机器人

使用以下脚本：

```bash
python scripts/bnb_band_bot.py --mode run
```

**先进行模拟运行：**

```bash
python scripts/bnb_band_bot.py --mode dry-run
```

## 3) 策略规则（固定不变）

- **入场规则**：当最新价格大于等于`BUY_TRIGGER PRICE`时执行买入操作。
- **止盈规则**：当价格大于等于入场价格乘以1.05时卖出。
- **止损规则**：当价格小于等于入场价格乘以0.97时卖出。
- **单笔交易模式**：不允许进行加仓操作（即不采用金字塔式交易策略）。

## 4) 安全控制措施

- 如果缺少环境变量，则拒绝运行脚本。
- 如果私钥格式无效，则拒绝运行脚本。
- 如果Gas费用或账户余额不足，则拒绝运行脚本。
- 所有交易决策都会记录下来，并附带时间戳。

## 5) 注意事项

- 该脚本使用DEX的报价和交换功能；在实际投入资金之前，请先通过模拟运行验证滑点（slippage）和Gas费用的相关参数。
- 请务必先进行模拟运行，以确保策略的稳定性和安全性。