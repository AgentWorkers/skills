---
name: trench
description: "专为AI代理设计的快速表情包币种交易系统。能够即时捕捉新发行的代币，并在Solana的DEX平台（如Jupiter、Raydium、Pump.fun）上快速执行买入/卖出操作。该系统具备MEV（最大有效价值）保护机制、自动滑点控制功能、欺诈行为检测能力以及仓位管理功能。适用于代理需要交易表情包币种、抢占新出现的交易机会、监控代币发行情况，或在Solana上管理高波动性资产的情况。"
---
# Trench 🪖

这是一项专为Solana平台上的AI代理设计的快速模因币交易执行技能。

> ⚠️ 此技能正处于积极开发阶段，核心模块即将推出。

## 功能（计划中）

### 执行
- 通过Jupiter聚合器与Raydium直接进行快速买卖
- 监控Pump.fun代币的买入/卖出行为并追踪其价格变动
- 使用Jito工具包提交交易以保护用户利益（MEV保护）
- 优化交易费用
- 对失败的交易进行自动重试

### 智能分析
- 新交易池的检测（Raydium、Pump.fun）
- 识别欺诈行为/陷阱（通过检查流动性锁定情况、代币铸造权限及主要持有者信息）
- 通过Rugcheck API对代币的安全性进行评分
- 通过DexScreener/Birdeye获取实时价格数据

### 仓位管理
- 自动设置获利/止损点
- 使用追踪止损策略
- 支持多钱包管理
- 按仓位记录盈亏情况

## 架构

```
trench/
├── SKILL.md
├── scripts/
│   ├── buy.py           # Fast buy execution
│   ├── sell.py           # Fast sell execution
│   ├── snipe.py          # New pool sniper
│   ├── monitor.py        # Token monitor & alerts
│   ├── safety.py         # Rug detection & token analysis
│   └── portfolio.py      # Position & PnL tracking
└── references/
    ├── jupiter-api.md    # Jupiter V6 swap API reference
    ├── raydium.md        # Raydium pool interaction
    ├── jito-bundles.md   # Jito bundle submission
    └── pump-fun.md       # Pump.fun API & graduation mechanics
```

## 使用示例

```
"Buy 0.5 SOL worth of POPCAT with 1% slippage"
"Snipe the next pump.fun graduation with 0.1 SOL"
"Set a 3x take-profit on my WIF position"
"Check if this token CA is safe: <address>"
"Show my open positions and PnL"
```