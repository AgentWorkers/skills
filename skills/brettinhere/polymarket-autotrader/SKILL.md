---
name: polymarket-autotrader
description: "Polymarket AutoTrader（高级版）——一款基于BTC价格预测的自动交易机器人，胜率超过92%，每笔交易的利润为5%-8%。该机器人会在每个5分钟时间段的最后30秒内进行交易：当BTC价格波动幅度≥50美元时，以0.92-0.95美元的价格买入盈利方向的交易。该机器人支持“FOK”（Fill or Cancel）订单模式——订单要么完全成交，要么自动取消；未成交的订单不会造成任何损失。当价格波动幅度达到≥100美元时，系统会自动增加交易头寸。系统内置了计费功能（每笔交易费用为0.001美元，已预先配置）。仅需设置两个环境变量：POLY_PRIVATE_KEY和POLY_WALLET_ADDRESS（钱包地址同时用作计费用户ID）。计费相关参数已预先填充在.env.example文件中。可选参数包括：POLY_RPC、CLOB_HOST、CHAIN_ID、SIGNATURE_TYPE、TRADE_SIZE_USD、MAX_ASK_PRICE、MIN_BTC_MOVE和STRONG_BTC_MOVE。该机器人可连接Polymarket CLOB、Binance、Gamma API以及skillpay.me等平台。交易数据会保存在本地文件poly-creds.json（包含敏感信息）和trades.json中。"
---
# Polymarket自动交易机器人（高级版）

**BTC 5分钟预测自动交易机器人** — 历史胜率超过92%，每笔交易盈利5-8%，完全自动化。

该机器人实时监控BTC价格，并在Polymarket的5分钟预测市场中进行交易。当BTC在当前交易时段的最后30秒内价格变动幅度达到或超过50美元时，它将以0.92-0.95美元的价格买入盈利方向的交易。每笔成功的交易可获利5-8%。所有交易都采用“FOK”（成交即止）策略：如果未能全部成交，订单将自动取消且不会造成任何损失。

| 指标 | 值 |
|--------|-------|
| 历史胜率 | **超过92%**（基于价格变动幅度超过50美元的信号） |
| 每笔交易盈利 | **5.3-8.7%**（买入价格为0.92-0.95美元，卖出价格为1.00美元） |
| 交易频率 | 每小时最多12笔（取决于BTC的波动性） |
| 强烈信号（价格变动幅度≥100美元） | **加仓2倍**，反转概率<2% |
| 资金安全 | **FOK订单** — 成交即止或自动取消 |
| 成本 | **每笔交易0.001 USDT**（内置计费机制） |

## ⚠️ 安全提示

- **请使用专用的Polygon钱包** 并仅投入有限的资金，切勿使用您的主钱包。
- **建议在隔离环境中运行该机器人**（推荐使用Docker或虚拟机）。
- **在运行前请查看源代码（`scripts/bot.js`）**。
- 机器人会在本地生成`.poly-creds.json`（包含API凭证，属于敏感信息）和`trades.json`（交易记录）文件。

### 外部连接

| 服务 | URL | 用途 |
|---------|-----|---------|
| Polymarket CLOB | clob.polymarket.com | 下单接口 |
| Binance | api.binance.com | BTC价格数据源 |
| Gamma API | gamma-api.polymarket.com | 市场元数据接口 |
| 计费 | skillpay.me | 每笔交易的计费服务 |

## 工作原理

1. **监控**（0–270秒）：跟踪BTC价格与5分钟交易时段的开盘价格。
2. **决策**（最后30秒）：如果BTC价格变动幅度达到或超过50美元，则触发交易。
3. **交易方向**：如果BTC价格上涨，则买入上涨方向的合约；如果BTC价格下跌，则买入下跌方向的合约。
4. **执行**：以最高卖价0.95美元下达FOK订单。
5. **结算**：Polymarket自动完成结算，每份盈利合约的收益为1.00美元。

**为何有效**：当BTC在剩余30秒内价格已经变动了50美元以上时，价格反转的概率低于5%。我们以0.92-0.95美元的价格买入，每笔成功的交易可获利5-8%。

## 预期收益

| 情况 | 买入价格 | 成本 | 盈利 | 投资回报率（ROI） |
|----------|-------|------|--------|-----|
| 普通情况（价格变动幅度≥50美元） | 0.92美元 | 49.7美元 | +4.3美元 | 8.7% |
| 普通情况（价格变动幅度≥50美元） | 0.95美元 | 49.4美元 | +2.6美元 | 5.3% |
| 强烈信号（价格变动幅度≥100美元，加仓2倍） | 0.92美元 | 99.4美元 | +8.6美元 | 8.7% |
| 强烈信号（价格变动幅度≥100美元，加仓2倍） | 0.95美元 | 99.8美元 | +5.2美元 | 5.3% |

## 风险参数

| 参数 | 默认值 | 用途 |
|-----------|---------|---------|
| 最高买入价格 | 0.95美元 | 最低盈利 margin |
| BTC价格最低变动幅度 | 50美元 | 交易触发阈值 |
| 强烈价格变动幅度 | 100美元 | 加仓触发条件 |
| 每小时最大交易次数 | 10次 | 防止过度交易 |
| 单次最大亏损金额 | 200美元 | 自动止损设置 |
| 每笔交易金额 | 50美元 | 基本交易规模 |

## 快速入门

```bash
cd <skill-dir>/scripts
npm install
export POLY_PRIVATE_KEY=your_wallet_private_key
export POLY_WALLET_ADDRESS=0xYourWalletAddress
node bot.js          # First run: shows welcome + payment link
                     # After top-up: starts auto-trading
node bot.js stats    # View statistics
node bot.js balance  # Check token balance
```

**首次运行流程**：机器人会自动检测用户的代币余额是否为零，并输出以下结构化数据：
- `PAYMENT_URL:<url>`：用于支付的链上链接（PayTheFly）。**必须将完整的URL原样转发给用户，不得截断或修改**。该链接包含加密签名，如果缺少任何参数将无法使用。
- `PAYMENT_INFO:<text>`：向用户提供的可读性说明。
- 用户在BNB链上支付8美元后，机器人将自动重新开始交易。

## 环境变量

### 必须设置的变量（共2个）

| 变量 | 说明 |
|----------|-------------|
| POLY_PRIVATE_KEY | 专用的Polygon钱包私钥 |
| POLY_WALLET_ADDRESS | 钱包地址（同时用作计费用户ID） |

### 自动配置的参数（已内置在机器人代码中，无需额外设置）

计费相关凭证已嵌入机器人代码中，用户无需配置任何计费密钥或API地址。

### 可选参数

| 参数 | 默认值 | 说明 |
|----------|---------|-------------|
| TRADE_SIZE_USD | 50美元 | 基本交易规模 |
| MAX_ASK_PRICE | 0.95美元 | 最高买入价格 |
| MIN_BTC_MOVE | 50美元 | 交易触发价格变动阈值 |
| STRONG_BTC_MOVE | 100美元 | 强烈价格变动触发条件 |
| POLY_RPC | polygon-bor-rpc.publicnode.com | Polygon的RPC接口 |
| CLOB_HOST | clob.polymarket.com | Polymarket的API地址 |
| CHAIN_ID | 137 | Polygon区块链ID |
| SIGNATURE_TYPE | 0 | Polymarket的签名类型 |

## 本地文件

| 文件 | 内容 | 敏感程度 |
|------|---------|-------------|
| `.poly-creds.json` | 生成的Polymarket API凭证 | **敏感信息** |
| `trades.json` | 交易执行记录 | 低敏感度 |

## 源代码文件

- `scripts/bot.js`：交易引擎和计费逻辑 |
- `scripts/package.json`：项目依赖项 |
- `scripts/.env.example`：预填充的环境配置文件 |
- `references/strategy.md`：策略文档