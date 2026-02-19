---
name: polymarket-user-analyzer
description: 分析 Polymarket 用户的交易策略和模式。从用户名中提取钱包地址，获取交易历史数据，并生成包含胜率、市场偏好、头寸规模、入场价格分析以及盈利能力指标在内的综合策略报告。在需要分析 Polymarket 用户的交易策略、交易模式或表现时使用该功能。
---
# Polymarket 用户分析器

通过用户名或钱包地址分析 Polymarket 用户的交易策略。

## 该工具的功能

1. 从 Polymarket 用户名中提取钱包地址。
2. 通过 Polymarket 数据 API 获取完整的交易历史记录。
3. 分析交易模式和策略特征。
4. 生成全面的绩效报告。

## 快速入门

```bash
# Analyze by username
node scripts/analyze_user.js @vague-sourdough

# Analyze by wallet address
node scripts/analyze_user.js 0x8c74b4eef9a894433B8126aA11d1345efb2B0488

# Save detailed report
node scripts/analyze_user.js @username --output report.json
```

## 分析指标

该分析器提供以下指标：

### 基本统计信息
- 执行的交易总数
- 投入的总资本
- 平均持仓规模
- 交易频率

### 市场偏好
- 市场类型分布（政治、体育、加密货币等）
- 关注的特定资产（BTC、ETH、SOL 等）
- 市场时间偏好（5 分钟、每小时、每天、长期）

### 交易模式
- 交易方向偏好（看涨/看跌）
- 入场价格分布（逆向交易 vs 跟随市场趋势）
- 持仓规模策略（固定 vs 动态）
- 交易时间模式

### 绩效指标
- 总利润/亏损
- 投资回报率（ROI）
- 胜率（如果可以从赎回操作中计算得出）
- 经风险调整后的回报

### 策略分类

该分析器可以识别常见的策略类型：
- **价值投资者**：购买被低估的资产（低入场价格）
- **趋势追随者**：跟随市场趋势（高入场价格）
- **套利者**：利用价格差异获利
- **高频交易者**：进行高频小额交易
- **坚定型交易者**：进行大额交易，交易频率较低

## API 参考

### Polymarket 数据 API

**从用户名获取钱包地址：**
```javascript
// Fetch user profile page and extract address
const response = await fetch(`https://polymarket.com/@${username}`);
const html = await response.text();
const address = html.match(/0x[a-fA-F0-9]{40}/)[0];
```

**获取交易历史记录：**
```
GET https://data-api.polymarket.com/activity?user={address}&limit={limit}
```

**响应格式：**
```json
{
  "proxyWallet": "0x...",
  "timestamp": 1234567890,
  "type": "TRADE" | "REDEEM",
  "side": "BUY" | "SELL",
  "price": 0.45,
  "size": 10.5,
  "usdcSize": 5.0,
  "outcome": "Yes" | "No",
  "title": "Market title",
  "slug": "market-slug"
}
```

## 输出格式

该分析器会生成一份结构化的报告：

```markdown
# Strategy Analysis: @username

## Overview
- Total Trades: X
- Capital Deployed: $X
- ROI: X%
- Strategy Type: [Classification]

## Market Focus
- Primary Markets: [List]
- Asset Distribution: [Breakdown]

## Trading Characteristics
- Average Entry Price: X
- Position Sizing: [Fixed/Dynamic]
- Direction Bias: [Neutral/Bullish/Bearish]

## Performance
- Total P&L: $X
- Win Rate: X%
- Best Trade: [Details]
- Worst Trade: [Details]

## Strategy Insights
[Key observations and patterns]
```

## 隐私与伦理

**重要提示：** 该工具仅分析 Polymarket 上链数据。所有 Polymarket 交易都是公开透明的。该工具不会：
- 访问用户的私人信息
- 需要用户认证
- 将数据存储或传输到外部服务器
- 违反任何服务条款

用户应了解自己的 Polymarket 活动是公开的，任何人都可以对其进行分析。

## 限制

- 仅分析已完成的交易（上链数据）
- 无法查看未成交的订单或用户的私人交易策略
- “赎回”操作并不总是代表盈利（市场价格可能归零）
- 历史数据受 API 限制（通常仅显示最近 100 至 1000 笔交易）
- 不考虑交易手续费或滑点

## 使用场景

- **学习**：研究成功交易者的策略
- **研究**：分析市场参与者的行为
- **尽职调查**：验证交易绩效
- **策略开发**：识别盈利模式
- **市场分析**：了解交易者的情绪和持仓情况