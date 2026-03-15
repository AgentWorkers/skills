---
name: Polymarket Screener
description: "按类别、概率和流动性筛选 Polymarket 的预测市场，并跟踪概率变化，以发现高价值的投资机会。适用于需要使用 Polymarket 筛选工具的场景。触发条件：Polymarket 筛选器被激活。"
---
# Polymarket 筛选器 🎯

使用 Polymarket 的公共 API 对预测市场进行筛选和分析。找出被低估的投注机会，追踪概率变化，发现高潜力的市场。

## Polymarket 筛选器与手动浏览的比较

| 功能 | 手动浏览 | Polymarket 筛选器 |
|---------|----------------|-------------------|
| 按概率范围筛选 | ❌ 有限 | ✅ 可以精确设置范围（例如：20%-40%） |
| 按流动性筛选 | ❌ 不支持 | ✅ 支持最小/最大流动性筛选 |
| 跟踪概率变化 | ❌ 需手动检查 | ✅ 自动追踪概率变化（使用 delta 算法） |
| 多类别扫描 | ❌ 一次只能扫描一个类别 | ✅ 可同时扫描所有类别 |
| 概率变化警报 | ❌ 无 | ✅ 可配置警报阈值 |
| 历史概率数据 | ❌ 图表显示有限 | ✅ 可导出时间序列数据 |
| 批量机会评分 | ❌ 无 | ✅ 自动评分 |
| 自定义观察列表 | ❌ 无 | ✅ 支持 JSON 格式的观察列表并附带跟踪功能 |
| 导出为 HTML 报告 | ❌ 无 | ✅ 提供专业格式的报告输出 |
| 按预期价值排序 | ❌ 无 | ✅ 内置预期价值计算器 |

## 开始使用

无需 API 密钥——Polymarket 的公共 API 是免费的。

```bash
# List active markets
bash scripts/polymarket-screener.sh list --limit 20

# Filter by category
bash scripts/polymarket-screener.sh list --category politics --limit 50

# Find high-opportunity markets (low probability, high liquidity)
bash scripts/polymarket-screener.sh opportunities --min-liquidity 50000 --prob-range "5-30"

# Track probability changes
bash scripts/polymarket-screener.sh track --market-id MARKET_SLUG --hours 48

# Generate full screening report
bash scripts/polymarket-screener.sh report --output polymarket-report.html
```

## 市场类别

- **政治** — 选举、立法、政府行动
- **加密货币** — 价格预测、ETF 批准、协议事件
- **体育** — 比赛结果、锦标赛、运动员表现
- **娱乐** — 奖项、新作品发布、名人活动
- **科学** — 太空探索、气候变化、研究里程碑
- **商业** — 财报、IPO、并购、市场指数
- **世界** — 地缘政治、国际事件

## 机会评分

市场评分依据以下标准：

```
Score = (Liquidity Factor × 0.3) + (Probability Edge × 0.3) + (Time Value × 0.2) + (Movement × 0.2)

Liquidity Factor:  Higher liquidity = higher score (easier to enter/exit)
Probability Edge:  Markets with probabilities far from 50% but trending = opportunity
Time Value:        Markets resolving soon with high uncertainty = valuable
Movement:          Recent probability shifts indicate new information
```

### 什么是好的投资机会？

1. **概率在 15%-35% 或 65%-85% 之间** — 有足够的优势，同时概率不会过于极端
2. **流动性大于 50,000 美元** — 可以进行有效的投资
3. **近期价格变动超过 5%** — 市场正在积极重新定价
4. **事件在 30 天内发生** — 时间价值明确
5. **你拥有独特的知识优势** — 你知道市场不知道的信息

## 输出格式

| 命令 | 描述 |
|---------|-------------|
| `markets` | 显示所有市场 |
| `odds` | 显示赔率 |
| `value-bets` | 显示价值投注信息 |
| `watchlist` | 显示观察列表 |

## API 使用限制

Polymarket 的公共 API 有使用限制。本筛选器会自动遵守这些限制：
- 列表端点：每分钟 60 次请求
- 市场详情端点：每分钟 120 次请求
- 支持指数级退避的重试机制

## 免责声明

⚠️ 预测市场涉及真实资金和财务风险。本工具仅提供分析功能，不负责投注或管理投资。请自行进行充分研究。

---
💬 意见反馈与功能请求：https://bytesagain.com/feedback
由 BytesAgain 提供支持 | bytesagain.com

## 命令说明

运行 `polymarket-screener help` 可查看所有可用命令。