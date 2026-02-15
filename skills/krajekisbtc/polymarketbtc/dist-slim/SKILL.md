---
name: polymarket-btc15m
description: 使用技术分析（TA）信号，在Polymarket平台上进行15分钟周期的比特币买卖交易。支持Clawbot模式（动态调整交易规模、设定止盈/止损点、自动结算）或固定模式。适用于信号验证、交易执行，或通过私钥实现自动化操作。
---

# Polymarket BTC 15分钟交易策略

Clawbot 使用 PolymarketBTC15mAssistant 提供的交易信号来管理 Polymarket 上的 BTC 15分钟交易。

## 模式

| 模式 | 开/关 | 交易规模 | 盈利目标 | 止损点 | 预结算卖出 |
|------|--------|---------------|-------------|-----------|----------------------|
| **Clawbot** | `CLAWBOT_MODE=true` | 根据余额和风险动态调整 | 是 | 是 | 是 |
| **固定模式** | `CLAWBOT_MODE=false`（默认） | 固定规模（ORDER_SIZE） | 否 | 否 | 否 |

### Clawbot 的工作逻辑

- **高风险模式**（交易后期，利润空间小）：使用余额的 2–3% 进行交易，止损点设置得更严格；
- **强信号模式**（利润空间大）：使用余额的较高比例（最高 15%）进行交易，盈利目标设置得更宽；
- **保留资金**：始终保留余额的 20% 作为备用资金；
- **单笔交易的最大规模**：不超过余额的 30%。

## 环境变量

| 变量 | 是否必需 | 说明 |
|----------|----------|-------------|
| `POLYMARKET_PRIVATE_KEY` | 是（交易所需） | 钱包私钥 |
| `POLYMARKET_FUNDER` | 是（交易所需） | 来自 polymarket.com 设置的资助者信息 |
| `CLAWBOT_MODE` | 否 | `true` 或 `false`（默认） |
| `POLYMARKET_ORDER_SIZE` | 否 | 当 Clawbot 关闭时使用的交易数量（默认：5） |
| `POLYMARKET_SIGNATURE_TYPE` | 否 | 0/1/2（默认：2） |

## 命令

### 获取交易信号

```bash
npm run signal
```

当 `CLAWBOT_MODE=true` 时，输出会包含 `clawbotParams`（余额、交易规模、盈利目标百分比、止损点百分比、预结算卖出条件）。

### 执行交易

```bash
npm run trade:up
npm run trade:down
node src/trade-cli.js --execute=UP --yes
```

### 交易监控（仅限 Clawbot 模式）

一个交易周期的监控过程：

```bash
node src/trade-cli.js --monitor
```

后台守护进程（持续运行，直到用户按下 Ctrl+C 结束）：

```bash
npm run monitor
```

## Clawbot 的工作流程

1. **获取交易信号**：
   - 运行 `npm run signal`；
   - 获取信号详情：操作类型、交易方向、当前交易阶段、信号强度、模型预测结果、剩余时间；
   - 如果处于 Clawbot 模式，还会显示 `clawbotParams`（余额、建议交易规模、盈利目标、止损点）。

2. **执行买入交易**：
   - 运行 `npm run signal` → 确认操作方向（买入）；
   - 如果条件匹配，执行 `npm run trade:up`（或 `--execute=UP --yes`）；
   - 如果条件不匹配，中止交易并给出原因。

3. **启用/禁用 Clawbot 模式**：
   - 在 `.env` 文件中设置 `CLAWBOT_MODE` 的值（`true` 或 `false`）；
   - 注意：Clawbot 模式下交易规模和止损点会自动调整；固定模式下则需要手动设置。

4. **运行交易监控**：
   - 在 Clawbot 模式下，运行 `npm run monitor` 在后台进行监控；
   - 或者通过 `node src/trade-cli.js --monitor` 执行一次交易周期的监控。

## 安全注意事项

- 本系统无法保证盈利；Clawbot 可以提高交易机会，但无法消除风险；
- 除非明确允许自动化交易，否则建议用户手动确认交易决策；
- 严禁记录或泄露 `POLYMARKET_PRIVATE_KEY`。

## 安装说明

```bash
cp -r clawbot-skill ~/.clawbot/skills/polymarket-btc15m
# or
ln -s /path/to/PolymarketBTC15mAssistant-main ~/.clawbot/skills/polymarket-btc15m
```

请确保项目的执行环境允许从项目目录中执行 `npm` 和 `node` 命令。