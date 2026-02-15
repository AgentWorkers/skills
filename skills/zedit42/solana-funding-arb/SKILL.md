---
name: solana-funding-arb
description: Solana 永续性去中心化交易所（DEX）资金费率套利工具——扫描器与自动交易系统。该工具通过比较 Drift 和 Flash Trade 平台上的资金费率，来发现并执行跨去中心化交易所的套利机会。适用于分析 Solana 的资金费率、寻找资金套利机会、构建Delta中性策略或运行自动化资金收集任务。该工具具备蒙特卡洛模拟、回测以及全自动交易功能。
---

# Solana资金利率套利（v2.0）

这是一个用于Solana永续DEXs的自动化资金利率套利机器人。

## 🔥 v2.0的新功能

- **自动交易**：完全自动化的头寸管理
- **多DEX支持**：Drift Protocol + Flash Trade
- **头寸管理器**：跟踪盈亏和收取的资金
- **风险管理**：止损、最大回撤限制、自动再平衡
- **Cron任务集成**：定时检查利率

## 支持的DEX

| DEX | 市场 | 交易方式 | 数据来源 |
|-----|---------|---------|-------------|
| Drift Protocol | 64 | ✅ 全部支持 | 直接API |
| Flash Trade | 19 | 🔶 DRY_RUN | CoinGecko |

## 策略选项

| 策略 | 杠杆倍数 | 胜率 | 年化收益率（APY） | 最大回撤率 |
|----------|----------|----------|-----|--------------|
| 超级安全策略 | 1倍 | 96% | 126% | 2% |
| 保守策略 | 1.5倍 | 89% | 203% | 4% |
| 中等策略 | 2.5倍 | 85% | 411% | 9% |

## 快速入门

```bash
cd scripts && npm install

# 1. Scan funding rates (no trading)
npm run trade:scan

# 2. Check position status
npm run trade:status

# 3. Run in DRY_RUN mode (simulated)
npm run trade:dry

# 4. Run live trading (requires wallet)
npm run trade

# Other commands
npm run scan        # Basic rate scanner
npm run dashboard   # Web dashboard (:3456)
npm run monte-carlo # Risk simulations
```

## 配置

**配置文件：** `~/.secrets/funding-arb-config.json`

```json
{
  "strategy": "ultra_safe",
  "max_position_pct": 50,
  "min_spread": 0.5,
  "max_dd_pct": 2,
  "auto_execute": true,
  "dry_run": true,
  "leverage": 1,
  "check_interval_hours": 4,
  "min_apy_threshold": 100,
  "max_position_usd": 100,
  "notification": {
    "telegram": true,
    "on_open": true,
    "on_close": true,
    "on_funding": true
  },
  "risk": {
    "max_positions": 2,
    "stop_loss_pct": 2,
    "take_profit_pct": null,
    "auto_rebalance": true,
    "rebalance_threshold": 0.3
  }
}
```

## 环境变量

在scripts目录下创建`.env`文件，或使用`~/.secrets/.env`文件：

```env
# Required for live trading
SOLANA_PRIVATE_KEY=[1,2,3,...]  # Or use wallet file
SOLANA_WALLET_PATH=/path/to/wallet.json

# Optional
SOLANA_RPC_URL=https://mainnet.helius-rpc.com/?api-key=YOUR_KEY
DEBUG=true  # Verbose logging
```

## Cron任务设置

每4小时运行一次：

```bash
# Add to crontab -e
0 */4 * * * ~/clawd/skills/solana-funding-arb/scripts/cron-runner.sh
```

## 工作原理

1. **扫描**：比较Drift Protocol和Flash Trade上的资金利率
2. **识别**：找出一个市场支付资金、另一个市场接收资金的交易对
3. **执行**：
   - 在利率为负的市场买入（接收资金）
   - 在利率为正的市场卖出（接收资金）
4. **收集资金**：确保总盈亏为零（Delta-neutral）
5. **再平衡**：当价差逆转或最大回撤率被超过时平仓

### 示例交易

```
SOL Funding Rates:
- Drift: -500% APY (longs receive)
- Flash: +800% APY (shorts receive)
- Spread: 1300% APY

Action:
→ LONG $50 SOL on Drift (receive 500% APY)
→ SHORT $50 SOL on Flash (receive 800% APY)
→ Net: Delta-neutral, collecting ~1300% APY in funding
```

## 相关文件

```
scripts/
├── src/trading/
│   ├── auto-trader.ts      # Main trading logic
│   ├── drift-client.ts     # Drift Protocol integration
│   ├── flash-client.ts     # Flash Trade integration
│   └── position-manager.ts # Position tracking
├── cron-runner.sh          # Cron wrapper script
└── ...

~/.clawd/funding-arb/
├── positions.json          # Current positions
├── history.json           # Trade history
├── trader-state.json      # Bot state
└── logs/                  # Cron logs
```

## 风险

⚠️ **智能合约风险**：DEX可能出现漏洞或被黑客攻击
⚠️ **利率逆转**：每日发生概率为15-18%
⚠️ **执行滑点**：0.2-0.4%
⚠️ **强制清算**：仅当杠杆倍数大于1倍时发生

## 收益率对比

| 平台 | 年化收益率（APY） | 与超级安全策略相比 |
|----------|-----|---------------|
| 超级安全策略（1倍杠杆） | 126% | — |
| 美国银行（FDIC） | 4.5% | 低28倍 |
| Aave V3 | 2.5% | 低50倍 |
| Marginfi | 8.5% | 低15倍 |

## 测试步骤

1. 首先使用`dry_run: true`（默认设置）启动程序
2. 运行`npm run trade:scan`来验证交易机会
3. 运行`npm run trade:dry`来测试交易流程
4. 准备就绪后，将`dry_run: false`和`max_position_usd: 10`设置为合适的值
5. 在`~/.clawd/funding-arb/logs/`目录下查看日志

## 参考资料

- [Drift Protocol文档](https://docs.drift.trade)
- [Flash Trade文档](https://flash.trade)
- [API参考](references/api.md)