---
name: prediction-trade-journal
displayName: Prediction Trade Journal
description: 自动记录交易详情（包括相关背景信息），跟踪交易结果，并生成校准报告，以优化交易策略。
metadata: {"clawdbot":{"emoji":"📓","requires":{"env":["SIMMER_API_KEY"]},"cron":null,"autostart":false}}
authors:
  - Simmer (@simmer_markets)
version: "1.1.5"
published: true
---
# 预测交易日志

记录每一笔交易，从结果中学习，提升你的交易策略。

## 何时使用此技能

当用户希望执行以下操作时，请使用此技能：
- 查看交易历史记录
- 跟踪胜率和盈亏情况
- 生成交易报告
- 分析哪些交易策略最有效

## 快速命令

```bash
# Sync trades from API
python tradejournal.py --sync

# Show recent trades
python tradejournal.py --history 10

# Generate weekly report
python tradejournal.py --report weekly

# Export to CSV
python tradejournal.py --export trades.csv
```

**API 参考：**
- 基本 URL：`https://api.simmer.markets`
- 认证：`Authorization: Bearer $SIMMER_API_KEY`
- 获取交易记录：`GET /api/sdk/trades`

## 工作原理

1. **同步**：向 `/api/sdk/trades` 发送请求以获取交易历史记录。
2. **存储**：将交易记录及其结果保存到本地文件中。
3. **跟踪**：在市场行情确定后更新交易结果。
4. **生成报告**：计算胜率、盈亏情况并进行策略校准分析。

## 命令行接口（CLI）参考

| 命令 | 描述 |
|---------|-------------|
| `--sync` | 从 API 获取最新交易记录 |
| `--history N` | 显示最近 N 笔交易（默认值：10） |
| `--sync-outcomes` | 更新已确定的交易结果 |
| `--report daily/weekly/monthly` | 生成汇总报告 |
| `--config` | 显示配置信息 |
| `--export FILE.csv` | 将数据导出为 CSV 文件 |
| `--dry-run` | 预览功能（不进行任何实际操作） |

## 配置

| 配置项 | 环境变量 | 默认值 |
|---------|---------------------|---------|
| API 密钥 | `SIMMER_API_KEY` | （必需） |

## 数据存储

交易记录存储在本地文件 `data/trades.json` 中：

```json
{
  "trades": [{
    "id": "uuid",
    "market_question": "Will X happen?",
    "side": "yes",
    "shares": 10.5,
    "cost": 6.83,
    "outcome": {
      "resolved": false,
      "winning_side": null,
      "pnl_usd": null
    }
  }],
  "metadata": {
    "last_sync": "2025-01-29T...",
    "total_trades": 50
  }
}
```

## 技能集成

其他技能可以为交易记录添加更多背景信息（如交易理由、交易者的信心水平以及交易来源），从而帮助进行更深入的分析：

```python
from tradejournal import log_trade

# After executing a trade
log_trade(
    trade_id=result['trade_id'],
    source="copytrading",
    thesis="Mirroring whale 0x123...",
    confidence=0.70
)
```

这些信息有助于提升交易分析的准确性。

## 报告示例

```
📓 Weekly Report
========================================
Period: Last 7 days
Trades: 15
Total cost: $125.50
Resolved: 8 / 15
Win rate: 62.5%
P&L: +$18.30

By side: 10 YES, 5 NO
```

## 故障排除

**“SIMMER_API_KEY 环境变量未设置”**
- 设置 API 密钥：`export SIMMER_API_KEY=sk_live_...`

**“尚未记录任何交易”**
- 运行 `python tradejournal.py --sync` 从 API 获取交易记录。

**交易结果未显示**
- 运行 `python tradejournal.py --sync-outcomes` 更新已确定的交易结果。