---
name: coinversaa-pulse
description: "**AI代理的加密情报工具**：7个免费工具 + 23个高级工具，专为Hyperliquid平台提供交易分析、用户行为研究、实时市场数据、交易所市场（包括商品、股票、指数）、清算情况可视化以及超过71万个钱包、18亿笔交易和369个市场的“鲸鱼用户”（大额交易者）追踪功能。"
version: 0.4.1
author: Coinversaa <chat@coinversaa.ai>
homepage: https://coinversaa.ai
repository: https://github.com/coinversaa/mcp-server
license: MIT
tags:
  - crypto
  - trading
  - hyperliquid
  - market-data
  - defi
  - analytics
  - blockchain
  - whale-tracking
  - builder-dex
  - commodities
  - stocks
  - mcp
env:
  COINVERSAA_API_KEY:
    description: "Your Coinversaa API key (starts with cvsa_). Get one at https://coinversaa.ai/developers. Optional — 7 tools available without a key."
    required: false
  COINVERSAA_API_URL:
    description: "API base URL (defaults to https://staging.api.coinversaa.ai)"
    required: false
---
# Coinversaa Pulse

这是一个专为AI代理设计的加密货币情报平台，支持查询71万个Hyperliquid钱包、18亿笔交易数据、用户行为分类以及实时市场信息，所有这些功能均可通过任何兼容MCP的客户端访问。

该平台并非基于公共区块链API构建的封装工具，而是直接索引Hyperliquid的清算数据，并提供其他平台所没有的分析功能。

**新增功能：Builder Dex支持**——现已支持8个DEX平台上的369个市场，涵盖商品、股票、指数等多种资产类型。

## 设置

### 免费 tier（无需API密钥）

立即试用，无需注册。提供7个工具，但每工具都有使用频率限制：

| 工具        | 使用频率限制 |
|------------|------------|
| `pulse_global_stats` | 每分钟10次 |
| `pulse_market_overview` | 每分钟5次 |
| `list_markets` | 每分钟5次 |
| `market_price` | 每分钟30次 |
| `market_orderbook` | 每分钟10次 |
| `pulse_most_traded_coins` | 每分钟5次 |
| `live_long_short_ratio` | 每分钟5次 |

每日每IP的请求上限为500次。

```json
{
  "mcpServers": {
    "coinversaa": {
      "command": "npx",
      "args": ["-y", "@coinversaa/mcp-server"]
    }
  }
}
```

### 全功能访问（需要API密钥）

可在[coinversaa.ai/developers](https://coinversaa.ai/developers)获取API密钥，解锁全部30个工具，并提升使用频率限制（每分钟100次，无每日请求上限）。

**Claude Desktop**：请编辑`~/Library/Application Support/Claude/claude_desktop_config.json`文件以配置API访问权限。

**Cursor**：需将API密钥添加到`.cursor/mcp.json`文件中。

**Claude代码**：请参考相关文档或GitHub仓库进行配置。

**OpenClaw**：请参考相关文档或GitHub仓库进行配置。

## Builder Dex市场

Hyperliquid支持多个DEX平台，每个平台都有自己独特的市场、抵押品代币和交易符号格式：

| DEX平台 | 交易类型        | 抵押品代币      | 示例交易符号       |
|---------|----------------|--------------|-------------------|
| *(原生)*    | 核心衍生品（加密货币） | USDC          | BTC, ETH, SOL, HYPE     |
| `xyz`     | 商品、股票、指数     | USDC          | xyz:GOLD, xyz:SILVER, xyz:TSLA |
| `flx`     | 衍生品        | USDH          | flx:BTC, flx:ETH     |
| `vntl`     | 衍生品        | USDH          | vntl:ANTHROPIC, vntl:BTC   |
| `hyna`     | 衍生品        | USDE          | hyna:SOL, hyna:BTC     |
| `km`     | 能源与商品     | USDH          | km:OIL, km:NATGAS    |
| `abcd`     | 其他资产     | USDC          | abcd:BITCOIN       |
| `cash`     | 股票与证券     | USDT0          | cash:TSLA, cash:AAPL     |

**交易符号格式：**
- Hyperliquid原生平台：`BTC`, `ETH`, `SOL`
- Builder Dex平台：`prefix:COIN`（例如：`xyz:GOLD`, `cash:TSLA`, `hyna:SOL`）

使用`list_markets`工具可查询所有可用市场及其所属的DEX平台。

## 工具（共30个，其中7个免费，23个需要API密钥）

### Pulse——交易者情报工具

当用户询问顶级交易者、市场活动或交易趋势时，可使用这些工具：

- **`pulse_global_stats`**：Hyperliquid平台的整体统计数据（交易者数量、交易量、盈亏总额、数据覆盖周期）。适用于了解市场规模。
- **`pulse_market_overview`**：市场概览（24小时交易量、未平仓合约数量、标价、融资费率、24小时价格波动）。可选参数`dex`可按DEX平台过滤（hl, xyz, flx, vntl, hyna, km, abcd, cash）。
- **`list_markets`**：查询所有DEX平台上的市场信息（包括市场名称、标价、24小时交易量、融资费率、未平仓合约数量、24小时价格波动）。适用于了解市场种类。
- **`pulse_leaderboard`：交易者排行榜（按盈亏总额、胜率、交易量、综合评分或风险调整后评分排序）。可选参数`sort`、`period`（天/周/月/全部时间）、`limit`（1-100）、`minTrades`。
- **`pulse_hidden_gems`**：发现被忽视的高绩效交易者（按最低胜率、盈亏总额、交易数量筛选）。
- **`pulse_most_traded_coins`：按交易量和交易次数排序的热门交易币种。
- **`pulse_biggest_trades`：Hyperliquid平台上最大额度的盈利或亏损交易。
- **`pulse_recent_trades`：过去N分钟/小时内最大的交易记录（按绝对盈亏总额排序）。
- **`pulse_token_leaderboard`：特定币种的顶级交易者排行榜。
- **`market_historical_oi`：历史每小时未平仓合约数据（以USD计价）。支持按币种筛选或查看全局汇总数据。

### Pulse——交易者画像工具

这些工具可用于深入分析特定钱包的交易情况。所有需要`address`参数的工具都要求提供完整的以太坊地址（格式为`0x + 40个十六进制字符）：

- **`pulse_trader_profile`：交易者全面信息（总盈亏总额、交易次数、胜率、交易量、最大盈利/亏损金额、首次/最后一次交易日期、盈亏等级、资金规模等级）。
- **`pulse_trader_performance`：过去30天与历史数据的对比（趋势：上升/下降/稳定）。
- **`pulse_trader_trades`：查询特定钱包的近期交易记录（包括每次买卖的金额、价格等）。
- **`pulse_trader_daily_stats`：交易者的每日盈亏总额、交易次数、胜率。
- **`pulse_trader_token_stats`：按币种划分的盈亏明细。
- **`pulse_trader_closed_positions`：交易者的完整持仓历史（包括入场/出场价格、持有时长、盈亏总额）。
- **`pulse_trader_closed_position_stats`：汇总持仓统计数据（平均持有时长、持仓胜率、总盈亏）。

### Pulse——用户行为分类工具

Coinversaa将71万个钱包分为不同的行为等级，这些数据是独一无二的：

**盈亏等级**（按盈利能力划分）：`money_printer`, `smart_money`, `grinder`, `humble_earner`, `exit_liquidity`, `semi_rekt`, `full_rekt`, `giga_rekt`

**资金规模等级**（按交易量划分）：`leviathan`, `tidal_whale`, `whale`, `small_whale`, `apex_predator`, `dolphin`, `fish`, `shrimp`

- **`pulse_cohort_summary`：所有钱包的行为分类统计（包括钱包数量、平均盈亏总额、平均胜率、总交易量）。
- **`pulse_cohort_positions`：特定等级钱包当前的持仓情况。
- **`pulse_cohort_trades`：指定等级钱包在指定时间窗口内的所有交易记录。
- **`pulse_cohort_history`：特定等级钱包的历史表现数据（按天数划分）。
- **`pulse_cohort_bias_history`：所有交易者的历史偏爱趋势数据（按币种筛选）。
- **`pulse_cohort_performance_daily`：所有等级钱包的历史每日表现数据。

### Market——实时市场数据

直接从Hyperliquid获取的实时市场数据：

- **`market_price`：任意符号（原生或Builder Dex平台）的当前标价。
- **`market_positions`：任意钱包的所有未平仓合约信息（包括合约数量、未实现盈亏、杠杆率）。
- **`market_orderbook`：任意交易对的买卖深度信息。

### 实时分析工具

提供实时计算的分析结果：

- **`live_liquidation_heatmap`：任意币种的清算行为分布图（按价格区间划分）。
- **`live_long_short_ratio`：全球或特定币种的多头/空头比例（可选查看历史数据）。
- **`live_cohort_bias`：特定币种各等级的交易者净持仓倾向。
- **`pulse_recent_closed_positions`：所有交易者的最近成交记录（可按币种、规模、持有时长筛选）。

## 使用示例

连接后，您可以尝试向AI提问：

- “Hyperliquid平台上盈亏总额最高的5位交易者是谁？”
- “当前处于`money_printer`等级的钱包持有哪些资产？”
- “过去10分钟内最大的交易记录是什么？”
- “查找胜率超过70%的被低估的交易者？”
- “深入分析钱包0x7fda...7d1的交易情况——他们的表现如何？”
- “BTC的清算行为集中在哪些价格区间？”
- “当前`smart_money`等级的交易者是多头还是空头？”
- “哪些币种目前交易最活跃？”
- “展示过去24小时内最大的亏损交易记录。”
- “这位交易者是短线投资者还是长线投资者？他们的平均持有时间是多少？”
- “这位交易者主要投资哪些币种？”
- “鲸鱼级交易者过去一小时交易了哪些币种？”
- “将这位交易者过去30天的表现与历史表现进行对比。”
- “xyz Dex平台上有哪些市场可用？”
- “展示所有商品市场（如黄金、白银、石油）的行情。”

## 产品优势：

- **丰富的市场类型**：8个DEX平台上的369个市场（涵盖商品、股票、指数等资产）。
- **精细的用户行为分类**：71万个钱包被划分为不同的盈利等级和资金规模等级。
- **实时持仓数据**：实时查看顶级交易者的持仓情况。
- **实时交易数据**：可按时间窗口查询任意钱包或交易群体的所有交易记录。
- **精准的清算分析**：对任意币种的清算行为进行详细分析。
- **深度挖掘工具**：发现排名系统未发现的优秀交易者。
- **海量数据支持**：Hyperliquid最全面的数据集通过API提供。

## 使用频率限制

**免费 tier**：每条请求的使用频率限制为5-30次/分钟，每日每IP请求上限为500次。具体限制详见“设置”部分。

**付费 tier（需要API密钥）**：每分钟100次请求，无每日请求上限。

每个响应中都会包含使用频率限制的相关信息：
- `X-RateLimit-Limit`：您配置的频率限制
- `X-RateLimit-Remaining`：当前时间窗口内剩余的请求次数
- `X-RateLimit-Reset`：距离时间窗口重置的剩余时间（以秒计）
- `X-RateLimit-Tier`：`free`或`paid`（表示是否为付费 tier）
- `X-RateLimit-Daily-Remaining`：（仅限免费 tier）当天剩余的请求次数

## 链接：

- 官网：[coinversaa.ai](https://coinversaa.ai)
- API文档：[coinversaa.ai/developers](https://coinversaa.ai/developers)
- GitHub仓库：[github.com/coinversaa/mcp-server](https://github.com/coinversaa/mcp-server)
- npm包：[@coinversaa/mcp-server](https://www.npmjs.com/package/@coinversaa/mcp-server)
- 技术支持：[chat@coinversaa.ai](mailto:chat@coinversaa.ai)

---

由[Coinversaa](https://coinversaa.ai)开发——专为AI代理提供的加密货币情报平台。