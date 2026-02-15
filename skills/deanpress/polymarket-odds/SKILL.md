---
name: Polymarket
description: 通过 CLI 查询 Polymarket 预测市场的赔率和事件。可以搜索市场、获取当前价格，并按类别列出事件。支持体育博彩（NFL、NBA、足球/EPL、欧冠联赛）、政治、加密货币、选举和地缘政治等相关领域的数据。基于实际市场数据的预测比传统民意调查更准确。无需使用 API 密钥。当有人询问赔率、概率、预测结果或“某事件发生的几率是多少”时，可以使用此工具。
---

# Polymarket 预测市场

从 Polymarket（全球最大的预测市场）查询实时赔率。

## 快速入门

```bash
# Search for markets (instant via /public-search API)
polymarket search "Arsenal FC"
polymarket search "Super Bowl"
polymarket search "Bitcoin"
polymarket search "Trump"

# Browse by category
polymarket events --tag=sports
polymarket events --tag=crypto
polymarket events --tag=politics

# Get specific market details
polymarket market will-bitcoin-reach-100k
```

该技能对应的命令行工具（CLI）位于 `polymarket.mjs` 文件中。使用以下命令运行该工具：
```bash
node /path/to/skill/polymarket.mjs <command>
```

## 命令

| 命令 | 描述 |
|---------|-------------|
| `search <查询>` | 通过关键词搜索市场（推荐） |
| `events [选项]` | 列出活跃的事件 |
| `market <slug>` | 根据市场标识符获取市场详情 |
| `tags` | 列出可用的分类 |
| `price <token_id>` | 获取某个代币的当前价格 |
| `book <token_id>` | 获取订单簿的深度信息 |

## 事件选项

- `--tag=<slug>` - 按类别筛选（例如：crypto、politics、sports 等） |
- `--limit=<n>` - 最大结果数量（默认：20）

## 理解赔率

- 赔率表示概率：
  - 0.65（65%）表示“是”的概率为 65%
- 成交量：总交易金额
- 流动性：订单簿中的可用资金

## 单场比赛投注

Polymarket 提供足球、NFL、NBA 等比赛的单独赛事预测市场。

```bash
# Soccer - use "FC" suffix for team names
polymarket search "Arsenal FC"
polymarket search "Manchester United FC"
polymarket search "Liverpool FC"

# NFL/NBA - team name works
polymarket search "Patriots"
polymarket search "Chiefs"
polymarket search "Lakers"
```

**可用的市场类型：**
- **货币线（Moneyline）**：赢/平/输的百分比
- **点差（Spreads）**：例如：Arsenal -1.5
- **总进球数（Totals）**：进球数超过/低于 2.5
- **双方均进球（BTTS）**：两队都进球

## 常见分类

| 分类（Tag） | 可用的市场（Markets） |
|---------|------------------|
| `sports` | NFL、NBA、足球、网球等 |
| `politics` | 选举、立法、人事任命 |
| `crypto` | 价格目标、ETF、法规 |
| `business` | 首次公开募股（IPO）、收购、财报 |
| `tech` | 产品发布、人工智能发展 |

## API 参考

该命令行工具使用以下公共 API 端点（无需认证）：

- **搜索（Search）**：`GET /public-search?q=<查询>` - 关键词搜索 |
- **事件（Events）**：`GET /events?active=true&closed=false` - 列出事件 |
- **市场（Markets）**：`GET /markets?slug=<slug>` - 市场详情 |
- **分类（Tags）**：`GET /tags` - 可用的分类 |

基础 URL：`https://gamma-api.polymarket.com`

## 注意事项

- 使用真实资金进行交易的市场通常比民意调查或专家预测更准确 |
- 赔率会随着交易情况实时更新 |
- 当预测结果正确时，市场结算金额为 $1.00；错误时，结算金额为 $0.00