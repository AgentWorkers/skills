---
name: crypto-funding-alert
description: 实时加密货币资金费率扫描器，具备智能提醒功能；能够识别对盈利多头头寸不利的资金费率情况。支持Binance期货市场。扫描过程无需使用API密钥。
metadata:
  {
    "openclaw":
      {
        "requires": { "bins": ["node"] },
        "tags": ["crypto", "trading", "funding-rate", "binance", "futures", "arbitrage", "defi", "scanner", "alert", "monitoring"],
      },
  }
---
# 加密货币资金费率警报

这是一个实时加密货币资金费率扫描工具，能够识别出在Binance期货市场中因资金费率为负而产生的盈利机会。

## 主要功能

- **智能扫描**：监控40多种主要加密货币的资金费率变化。
- **风险管理**：内置安全过滤机制（如交易量限制、杠杆限制和止损设置）。
- **评分系统**：综合考量资金费率、价格趋势和交易量等因素。
- **警报等级**：分为“强烈推荐”、“中等推荐”和“观察中”三种类型。
- **无需API密钥**：直接使用Binance的公开API接口。
- **历史数据记录**：将扫描结果保存为JSONL格式，便于后续分析。

## 工作原理

当资金费率为负时，多头投资者会从空头投资者那里获得收益。这为投资者提供了以下盈利机会：
1. 开立多头头寸。
2. 每8小时收取一次资金费用。
3. 从潜在的价格上涨中获利。

该工具通过以下条件筛选盈利机会：
- 最低绝对资金费率（0.05%）。
- 24小时交易量至少达到1000万美元。
- 价格趋势分析。
- 综合评分算法。

## 使用方法

### 基本扫描
```bash
node scan.js
```

### 自定义配置
```bash
node scan.js --max-leverage 2 --min-volume 20000000 --stop-loss 0.15
```

### 自动化监控（定时任务）
```bash
# Add to OpenClaw cron - scan every 4 hours
openclaw cron add "0 */4 * * *" "cd ~/.openclaw/workspace/skills/crypto-funding-alert && node scan.js"
```

## 配置说明

请修改`scan.js`文件中的`SAFE_CONFIG`对象：
```javascript
const SAFE_CONFIG = {
  maxLeverage: 3,          // Maximum leverage (1-5x recommended)
  maxPositionPct: 0.3,     // Max position size (30% of capital)
  stopLossPct: 0.10,       // Stop-loss percentage (10%)
  minVolume: 10000000,     // Minimum 24h volume ($10M)
  minAbsRate: 0.0005,      // Minimum funding rate (0.05%)
  maxCoins: 5,             // Max simultaneous positions
};
```

## 输出示例
```
🔍 Safe Funding Rate Monitor | 2026-02-26T06:21:00.000Z
══════════════════════════════════════════════════════════════════════
Safety: 3x max | 10% stop-loss | $10M min volume
══════════════════════════════════════════════════════════════════════

  Signal   Coin     Rate      24h     Vol($M)  Score  Annual(3x)
  ────────────────────────────────────────────────────────────────
  🟢 STRONG   DOGE     -0.0125%    2.34%    145.2    72.3  41%
  🟡 MODERATE SOL      -0.0089%   -1.12%     89.5    48.7  29%
  ⚪ WATCH    XRP      -0.0056%   -2.45%     67.3    35.2  18%

🏆 推荐操作:
   DOGE: 开多 3x | 止损 10% | 费率 -0.0125% | 年化 41%

══════════════════════════════════════════════════════════════════════
📁 历史记录: data/funding-monitor/scan_history.jsonl
```

## 安全规则

基于实际交易经验，我们建议遵循以下规则：
- **最大杠杆**：3倍（降低清算风险）。
- **头寸规模**：每种加密货币的头寸占比不超过30%（分散风险）。
- **止损设置**：至少设定10%的止损点（保护本金）。
- **交易量要求**：仅选择流动性较高的市场（交易量超过1000万美元）。
- **趋势判断**：偏好24小时内的正向价格走势。
- **避免恐慌性交易**：在市场极度波动时暂停操作。

## 数据存储

扫描结果会被保存到以下路径：
```
~/.openclaw/workspace/data/funding-monitor/scan_history.jsonl
```

每条数据记录包含以下信息：
```json
{
  "timestamp": "2026-02-26T06:21:00.000Z",
  "results": [...],
  "config": {...}
}
```

## 命令行选项
```bash
node scan.js [options]

Options:
  --max-leverage <n>      Maximum leverage (default: 3)
  --min-volume <n>        Minimum 24h volume in USD (default: 10000000)
  --stop-loss <n>         Stop-loss percentage (default: 0.10)
  --min-rate <n>          Minimum absolute funding rate (default: 0.0005)
  --max-coins <n>         Maximum simultaneous positions (default: 5)
  --coins <list>          Comma-separated coin list (default: built-in list)
  --output <path>         Custom output directory
```

## 集成示例

- **Telegram警报**：将扫描结果通过Telegram发送通知。
- **Discord Webhook**：将警报信息发送到Discord频道。
- **自定义脚本**：可将扫描结果集成到自定义脚本中。

## 免责声明

本工具仅用于提供信息参考。加密货币交易存在较高的风险。请务必：
- 自行进行充分研究。
- 不要投资超出自己承受能力范围的金额。
- 采取适当的风险管理措施。
- 先用小额资金测试交易策略。
- 在交易前了解资金费率的运作机制。

## 系统要求

- 系统需运行Node.js 14及以上版本。
- 需要互联网连接。
- 扫描过程中无需使用API密钥。

## 技术支持

如遇到问题或需要新增功能，请访问ClawHub仓库或联系工具开发者。

## 许可证

本工具采用MIT许可证。

## 关键词

加密货币、交易、资金费率、Binance、期货、套利、去中心化金融（DeFi）、扫描工具、警报系统、自动化监控、负资金费率、多头头寸、风险管理、自动化交易。