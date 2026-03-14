---
name: kalshi-weather-trader
description: 使用 Solana 上的 Simmer SDK 和 DFlow，通过 NOAA 预报数据来交易 Kalshi 的天气市场。这是 popular polymarket-weather-trader 的一个扩展功能。适用于用户希望在 Kalshi 交易温度相关的数据、自动化进行天气相关的投资决策，或查看 NOAA 的天气预报的情况。
metadata:
  author: Simmer (@simmer_markets)
  version: "1.0.0"
  displayName: Kalshi Weather Trader
  difficulty: intermediate
  attribution: Strategy inspired by gopfan2, powered by DFlow
---# Kalshi 天气交易工具

使用 NOAA 的天气预报数据，在 Kalshi 平台上通过 DFlow 进行温度市场的交易。

> **这是一个模板。** 默认的交易信号基于 NOAA 的温度预报数据——您可以根据需要将其与其他天气 API、不同的预报模型或额外的市场类型（如降水量、风速等）结合使用。该工具负责处理所有交易相关的工作（包括市场发现、数据解析、交易执行以及风险控制）。您需要提供自己的交易策略（即“alpha”参数）。

> **由 DFlow 提供支持。** Kalshi 的交易通过 DFlow 基于 Solana 的预测市场基础设施来执行。进行买入操作时，需要进行 KYC 验证。

## 适用场景

当用户希望执行以下操作时，可以使用此工具：
- 在 Kalshi 平台上进行天气市场交易（而非 Polymarket 平台）
- 自动化设置温度交易策略
- 查看自己在 Kalshi 平台上的天气交易持仓
- 配置交易阈值或交易地点

## 设置流程

当用户请求安装或配置此工具时，请按照以下步骤操作：

1. **获取 Simmer API 密钥**
   - 可以从 `simmer.markets/dashboard` 的 SDK 标签页获取该密钥
   - 将其存储在环境变量 `SIMMER_API_KEY` 中

2. **提供 Solana 私钥**（用于实时交易）
   - 这是您的 Solana 钱包的 Base58 编码的秘密密钥
   - 将其存储在环境变量 `SOLANA_PRIVATE_KEY` 中
   - SDK 会使用此密钥在客户端自动签名交易

3. **完成 KYC 验证**
   - 仅用于买入操作
   - 请访问 [dflow.net/proof](https://dflow.net/proof) 完成验证
   - 检查验证状态：`curl "https://api.simmer.markets/api/proof/status?wallet=YOUR_SOLANA_ADDRESS"`

4. **为钱包充值**
   - 在 Solana 主网上充值 SOL（交易费用约为 0.01 SOL）
   - 在 Solana 主网上充值 USDC 作为交易资金

5. **询问配置详情**（或确认默认设置）
   - **买入阈值**：价格低于此阈值时买入（默认为 0.15 SOL）
   **卖出阈值**：价格高于此阈值时卖出（默认为 0.45 SOL）
   **单次交易最大持仓金额**：每次交易的最大金额（默认为 2.00 美元）
   **交易地点**：指定交易的城市（默认为纽约市 NYC）

6. **将配置信息保存到环境变量中**

7. **设置定时任务**（默认未启用——用户需要手动启用）

## 配置参数

| 参数 | 环境变量 | 默认值 | 说明 |
|---------|---------------------|---------|-------------|
| 买入阈值 | `SIMMER_WEATHER_ENTRY_THRESHOLD` | 0.15 | 价格低于此阈值时买入 |
| 卖出阈值 | `SIMMER_WEATHER_EXIT_THRESHOLD` | 0.45 | 价格高于此阈值时卖出 |
| 单次交易最大金额 | `SIMMER_WEATHER_MAX_POSITION_USD` | 2.00 | 每次交易的最大金额（美元） |
| 每次扫描周期的最大交易次数 | `SIMMER_WEATHER_MAX_TRADES_PER_RUN` | 5 | 每次扫描周期内的最大交易次数 |
| 交易地点 | `SIMMER_WEATHER_LOCATIONS` | NYC | 用逗号分隔的城市列表（例如：NYC, Chicago, Seattle, Atlanta, Dallas, Miami） |
| 仅交易二进制选项 | `SIMMER_WEATHER_binary_ONLY` | false | 如果设置为 true，则仅交易二进制类型的天气市场（即只有“是/否”选项的市场） |
| 智能资金分配比例 | `SIMMER_WEATHER_SIZING_PCT` | 0.05 | 每次交易的资金分配比例（百分比） |
| 最大滑点限制 | `SIMMER_WEATHER_SLIPPAGE_MAX` | 0.15 | 如果滑点超过此值，则跳过该交易（0.15 表示 15%） |
| 最低流动性要求 | `SIMMER_WEATHER_MIN_LIQUIDITY` | 0 | 如果市场流动性低于此值，则跳过该市场（0 表示禁用交易） |

**支持的地点：** NYC, Chicago, Seattle, Atlanta, Dallas, Miami

## 快速命令

```bash
# Check account balance and positions
python scripts/status.py

# Detailed position list
python scripts/status.py --positions
```

**API 参考：**
- 基础 URL：`https://api.simmer.markets`
- 认证方式：`Authorization: Bearer $SIMMER_API_KEY`
- 财产组合信息：`GET /api/sdk/portfolio`
- 持仓信息：`GET /api/sdk/positions`

## 运行工具

```bash
# Dry run (default — shows opportunities, no trades)
python weather_trader.py

# Execute real trades
python weather_trader.py --live

# With smart position sizing (uses portfolio balance)
python weather_trader.py --live --smart-sizing

# Check positions only
python weather_trader.py --positions

# View config
python weather_trader.py --config

# Quiet mode — only output on trades/errors (ideal for high-frequency runs)
python weather_trader.py --live --smart-sizing --quiet
```

## 工作原理

脚本的工作流程如下：
1. 从 Simmer API 获取当前活跃的天气市场信息
2. 按事件类型对市场进行分组（每个温度数据对应一个事件）
3. 解析事件信息以获取具体地点和日期
4. 获取该地点/日期的 NOAA 天气预报数据
5. 找到与预报数据匹配的温度区间
6. **风险控制**：检查是否存在价格剧烈波动的警告、滑点过大等问题
7. **趋势分析**：判断近期价格是否下跌（作为买入信号）
8. **买入操作**：如果区间价格低于买入阈值且满足所有风险控制条件，则执行买入
9. **卖出操作**：检查当前持仓情况，如果价格高于卖出阈值，则卖出
10. **标记交易**：所有交易都会被标记为 `sdk:kalshi-weather` 以便后续追踪

## 风险控制机制

在交易前，该工具会执行以下检查：
- **价格剧烈波动**：如果价格波动过于频繁，则跳过当前交易
- **滑点过大**：如果预计滑点超过 15%，则跳过交易
- **市场状态**：如果市场在 2 小时内已结束交易，则跳过当前交易
- **Kalshi 维护窗口**：Kalshi 的清算所每周四凌晨 3:00-5:00 有维护窗口，此期间提交的订单将失败

可以通过 `--no-safeguards` 参数关闭风险控制机制（但不建议这样做）。

## 常见问题及解决方法：

- **“风险控制机制被触发”**：表示市场价格波动过于剧烈，建议等待一段时间后再进行交易
- **滑点过高**：市场流动性较低，建议减少持仓规模或跳过交易
- **未找到天气市场**：可能是由于天气市场处于非活跃状态（可能是季节性原因），请确保已导入相关数据：`POST /api/sdk/markets/import/kalshi`
- **需要完成 KYC 验证**：请在 [dflow.net/proof](https://dflow.net/proof) 完成验证（仅适用于买入操作）
- **未设置 SOLANA 私钥**：确保环境变量 `SOLANA_PRIVATE_KEY` 已设置，SDK 会使用该密钥自动签名交易
- **交易费用不足**：请确保 Solana 钱包中有至少 0.05 SOL 的余额用于支付交易费用
- **API 密钥无效**：请从 `simmer.markets/dashboard` 的 SDK 标签页重新获取 API 密钥