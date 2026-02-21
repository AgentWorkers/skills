# FearHarvester 技能

这是一个用于极端恐惧市场（即市场情绪极度悲观的环境）的自动定期投资（DCA）代理。

## 策略
- 持续监控恐惧指数（Fear Index）和贪婪指数（Greed Index）
- 当恐惧指数和贪婪指数均低于 10 时（极度恐惧市场），进行比特币（BTC）或以太坊（ETH）的定期投资
- 当恐惧指数和贪婪指数均高于 50 时（市场情绪趋于中性或贪婪情绪开始回升），将投资重新分配到高收益资产中
- 该策略完全排除人类情绪对投资决策的影响（即避免在恐惧情绪高涨时盲目买入）

## 使用方法
```bash
uv run python scripts/backtest.py --start 2018-01-01 --capital 10000
uv run python scripts/signals.py --live
uv run python scripts/executor.py --dry-run
```

## 历史表现（2018-2024 年）
在恐惧指数和贪婪指数均低于 10 的情况下进行投资，持有 90 天后，平均收益为 40%-80%