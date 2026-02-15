---
name: kalshi
description: 在 Kalshi 预测市场（受美国商品期货交易委员会（CFTC）监管的预测市场交易所）上进行交易。您可以查看投资组合、搜索市场、分析订单簿、下达或取消订单。该平台适用于与 Kalshi API 进行交互、交易二元合约、查看市场价格、管理持仓，以及研究政治、经济、加密货币、天气、体育和技术事件相关的预测市场。
homepage: https://kalshi.com/docs/api
metadata:
  {
    "openclaw":
      {
        "emoji": "📈",
        "requires": { "bins": ["node"], "env": ["KALSHI_API_KEY_ID", "KALSHI_PRIVATE_KEY_PATH"] },
        "primaryEnv": "KALSHI_API_KEY_ID",
      },
  }
---

# Kalshi

通过一个自包含的命令行界面（CLI）脚本在 Kalshi 预测市场上进行交易。支持市场搜索、投资组合跟踪以及完整的订单生命周期管理（下单、取消、监控）。

## 快速入门

所有命令都通过同一个脚本执行，输出结果为 JSON 格式。

## CLI

**主脚本：**

```bash
{baseDir}/scripts/kalshi-cli.mjs <command> [args...]
```

**辅助脚本：**

```bash
{baseDir}/scripts/quick-analysis.mjs <ticker>
```

该辅助脚本将市场详情和订单簿信息合并在一起，便于快速分析。

## 命令

| 命令                                      | 描述                                      |
| ----------------------------------------- | ------------------------------------------------ |
| `balance`                                 | 获取账户余额（现金 + 投资组合价值）                     |
| `portfolio`                               | 获取余额及所有未平仓头寸                         |
| `trending`                                | 按 24 小时成交量排序的热门市场                     |
| `search <query>`                          | 通过关键词搜索市场                         |
| `market <ticker>`                         | 获取单个市场的详细信息                         |
| `orderbook <ticker>`                      | 获取某个市场的买卖价差                         |
| `buy <ticker> <yes\|no> <count> <price>`  | 下单买入（价格范围：1-99 分）                     |
| `sell <ticker> <yes\|no> <count> <price>` | 下单卖出（价格范围：1-99 分）                     |
| `cancel <orderId>`                        | 取消待成交订单                         |
| `orders [resting\|canceled\|executed]`    | 列出所有订单（可按状态筛选）                     |
| `fills [ticker]`                          | 列出最近的交易记录（可按股票代码筛选）                     |

## 示例

```bash
# Check balance
{baseDir}/scripts/kalshi-cli.mjs balance

# See what's trending
{baseDir}/scripts/kalshi-cli.mjs trending

# Search for markets about bitcoin
{baseDir}/scripts/kalshi-cli.mjs search "bitcoin"

# Get details on a specific market
{baseDir}/scripts/kalshi-cli.mjs market KXBTCD-26FEB14-B55500

# Check orderbook
{baseDir}/scripts/kalshi-cli.mjs orderbook KXBTCD-26FEB14-B55500

# Buy 5 YES contracts at 65 cents
{baseDir}/scripts/kalshi-cli.mjs buy KXBTCD-26FEB14-B55500 yes 5 65

# Sell 5 YES contracts at 70 cents
{baseDir}/scripts/kalshi-cli.mjs sell KXBTCD-26FEB14-B55500 yes 5 70

# Check open orders
{baseDir}/scripts/kalshi-cli.mjs orders resting

# Check recent fills
{baseDir}/scripts/kalshi-cli.mjs fills
```

## 输出结果

所有命令的输出结果均为 JSON 格式，需解析后呈现给用户。

## 交易规则

**重要提示：** 在执行任何买卖订单之前，务必先与用户确认相关信息。

在执行交易前，需向用户展示以下信息：
- 股票代码（Ticker）
- 交易方向（YES 或 NO）
- 订单数量（合约数）
- 价格（单位：分）
- 总成本 = 订单数量 × 单价（分） = $X.XX

**价格格式：**
- 价格单位为分（1-99 分）
- 65 分 = 每份合约 $0.65
- 最低价格：1 分，最高价格：99 分

**收益规则：**
- 如果预测正确，每份合约收益为 $1.00
- 如果预测错误，每份合约损失 $0
- 预测结果为 “YES” 且价格为 65 分时：成本为 65 分，若预测正确则收益为 $1.00（每份合约利润 35 分）
- 预测结果为 “NO” 且价格为 35 分时：成本为 35 分，若预测正确则收益为 $1.00（每份合约利润 65 分）
- 预测结果为 “YES” 且价格高于 65 分或 “NO” 且价格低于 35 分时：收益约为 $1.00（价差导致微小波动）

**卖出前操作：** 首先通过投资组合确认用户是否持有该股票头寸。

## 参考文档**
- **[setup-guide.md](references/setup-guide.md)** - 获取 API 凭据、配置设置及故障排除
- **[trading-guide.md](references/trading-guide.md)** - 市场机制、交易策略建议及风险管理
- **[api-notes.md](references/api-notes.md)** - API 技术细节、数据格式及常见用法

## 环境变量
- `KALSHI_API_KEY_ID` — 你的 Kalshi API 密钥（UUID 格式）
- `KALSHI_PRIVATE_KEY_PATH` — 你的 RSA 私钥 PEM 文件的绝对路径

详细配置说明请参阅 [setup-guide.md](references/setup-guide.md)。