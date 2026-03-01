---
name: polymarket-manual-trade
displayName: Manual Trade Placement
description: 在 Polymarket 上进行手动交易，只需告诉您的代理应该投注什么。该功能支持 FAK（即时成交）和 GTC（挂单等待成交）两种订单类型。您可以传递一个 Simmer 市场 ID 或完整的 Polymarket URL——该技能会自动导入相关数据并处理价格发现过程。FAK 和 GTC 订单类型均已经过全面测试，可以正常使用。
metadata:
  clawdbot:
    emoji: "🎯"
    requires:
      pip: ["simmer-sdk"]
      env: ["SIMMER_API_KEY", "WALLET_PRIVATE_KEY"]
    cron: null
    automaton:
      managed: false
      entrypoint: "manual_trade.py"
version: "1.0.4"
published: true
---
# 手动交易下单

在 Polymarket 上进行交易，只需告诉您的 AI 代理应该投注什么。支持即时成交（FAK）和 GTC 限价单。可以与 Simmer 市场 ID 或完整的 Polymarket 事件 URL 一起使用。

## 使用方法

告诉您的代理：
> “在 [Polymarket URL 或市场 ID] 上购买 10 美元”
> “在 [市场] 上以 0.35 的价格下达一个 GTC 限价单，金额为 20 美元”

或者直接运行：

```bash
# FAK — instant fill at best ask price (default)
python3 manual_trade.py --market <market_id_or_url> --side YES --amount 10

# GTC — limit order, sits on book until filled
python3 manual_trade.py --market <market_id_or_url> --side NO --amount 20 --order GTC --price 0.35

# Full Polymarket URL — auto-imports and trades
python3 manual_trade.py \
  --market https://polymarket.com/event/spacex-starship-flight-test-12/will-the-chopsticks-catch-spacex-starship-flight-test-12-superheavy-booster \
  --side YES --amount 10

# Dry run (preview without placing)
python3 manual_trade.py --market <id> --side YES --amount 10 --dry-run
```

## 订单类型

| 类型 | 行为 | 适用场景 |
|------|----------|-------------|
| **FAK**（默认） | 立即以最佳卖价 + 0.01 的价格成交；剩余部分会被取消。| 您希望立即以市场价格买入 |
| **GTC** | 限价单会存放在 CLOB 订单簿中；资金在下单时被锁定，当市场价格达到您的价格时成交。| 您希望以特定价格成交 |

## 参数

| 参数 | 说明 |
|------|-------------|
| `--market` / `-m` | Simmer 市场 ID 或完整的 Polymarket URL |
| `--side` / `-s` | `YES` 或 `NO` |
| `--amount` / `-a` | 金额（默认为 10 美元） |
| `--order` / `-o` | `FAK`、`GTC` 或 `FOK`（默认为 FAK） |
| `--price` / `-p` | 限价（可选；如果省略，则自动获取最佳卖价 + 0.01） |
| `--venue` / `-v` | `polymarket` 或 `sim`（默认为 polymarket） |
| `--dry-run` | 不进行实际交易，仅预览 |

## 工作原理

1. **市场解析**：如果您提供了 Polymarket URL，系统会通过 Simmer 的导入 API 自动解析到正确的市场。
2. **价格获取**：获取实时的 CLOB 订单簿，使用 `asks[-1]`（最佳卖价）+ 0.01 作为 FAK 单的价格，以确保成交。
3. **订单提交**：使用 simmer-sdk 和您的钱包密钥完成订单的签署和提交。
4. **确认**：系统会报告已成交的股份数量、成本和交易 ID。

## 所需条件

- `SIMMER_API_KEY`：您的 Simmer API 密钥
- `WALLET_PRIVATE_KEY`：您的 Polymarket 钱包私钥（用于链上签名）
- `simmer-sdk` 版本需大于或等于 0.8.32

---

本功能专为 [Simmer](https://www.simmer.markets/) 开发——这是一个专为 Polymarket 和 Kalshi 设计的 AI 交易代理平台。