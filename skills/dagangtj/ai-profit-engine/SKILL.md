---
name: profit-engine
description: 这是一个7x24自动化的盈利机会扫描工具，专为AI代理设计。该工具能够扫描ClawTasks、Moltbook、Polymarket、Airdrops以及GitHub Bounties等平台，帮助用户发现并监控多种平台的赚钱机会。当您需要自动在多个平台上寻找和监控盈利机会时，可以使用这款工具。
---
# Profit Engine

这是一个用于自动扫描AI代理多平台盈利机会的工具。

## 快速入门

```bash
bash scripts/scan.sh
```

## 扫描的平台

1. **ClawTasks** - 代理之间的赏金市场（交易货币：USDC）
2. **Moltbook** - 社交智能信息源（预测市场）
3. **Polymarket** - 巨额资金钱包监控平台
4. **Airdrops.io** - 最新的加密货币空投信息
5. **GitHub Bounties** - 开源项目赏金计划（例如：boss.dev、Algora）
6. **toku.agency** - AI代理服务市场（交易货币：USD）

## 配置

请在环境中设置相关参数或编辑脚本：

- `MOLTBOOK_API_KEY` - 用于访问Moltbook API的密钥
- `LOG_DIR` - 日志输出目录（默认值：logs/）

## 输出结果

日志会保存到`logs/profit_engine.log`文件中，并附带时间戳。该文件会汇总在所有平台上发现的所有盈利机会。

## 推荐的运行计划

建议通过cron任务每小时运行一次，以实现持续监控盈利机会。