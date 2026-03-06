---
name: yield-shark
description: 🦈 YieldShark——一款DeFi稳定币收益监测工具，可实时追踪50多个平台的年化收益率（APY）。
version: 1.0.3
author: gztanht
license: MIT
tags: [defi, yield, crypto, finance, stablecoin, usdt, usdc, apy, aave, compound]
pricing:
  free_tier: 5 queries/day
  sponsorship: 0.5 USDT or 0.5 USDC for unlimited
  note: "Feel free to sponsor more if you find it useful!"
wallet:
  usdt_erc20: "0x33f943e71c7b7c4e88802a68e62cca91dab65ad9"
  usdc_erc20: "0xcb5173e3f5c2e32265fbbcaec8d26d49bf290e44"
metadata:
  clawdbot:
    emoji: 🦈
    requires:
      bins: [npm, node]
---
# 🦈 YieldShark - DeFi收益收割工具

**嗅探财富**——在DeFi领域寻找最高的年化收益率（APY）！

## 概述

YieldShark实时监控50多个DeFi平台（包括Aave、Compound、Curve、Uniswap、Yearn、Beefy等）上的稳定币收益，为您的加密货币投资提供数据驱动的洞察。

## 特点

- **实时数据**：直接集成DeFiLlama API（免费、公开）
- **支持多种代币**：USDT、USDC、DAI
- **支持多种区块链**：Ethereum、Arbitrum、Optimism、Base、Polygon、BSC
- **智能过滤**：排除流动性池（LP pools），过滤年化收益率异常低（<30%）或总价值（TVL）低于10万美元的资产
- **风险评级**：基于审计和保险机制的A-E等级安全评分
- **费用估算**：计算扣除交易费用后的净年化收益率
- **平台对比**：可横向比较各大DeFi平台的收益情况

## 安装

```bash
clawhub install yield-shark
```

## 使用方法

### 快速入门

```bash
# Query USDT yields
node scripts/monitor.mjs USDT

# Query USDC with custom limit
node scripts/monitor.mjs USDC --limit 10

# Query DAI on specific chain
node scripts/monitor.mjs DAI --chain ethereum
```

### 所有脚本

```bash
# Monitor yields
node scripts/monitor.mjs USDT

# Compare platforms
node scripts/compare.mjs --token USDT

# Calculate net APY
node scripts/calculate.mjs --amount 5000 --platform compound

# Set yield alerts
node scripts/alert.mjs --apy 5

# Generate report
node scripts/report.mjs --format markdown
```

### NPM命令

```bash
npm run monitor    # Run monitor script
npm run compare    # Compare platforms
npm run test:usdt  # Test USDT query
npm run test:usdc  # Test USDC query
npm run test:dai   # Test DAI query
```

## 输出示例

```
💰 USDT 最优收益排行 (DeFiLlama 实时数据)

排名  平台 (链)            APY      风险    Gas     TVL
──────────────────────────────────────────────────────────────────────
🥇 Compound V3  (Optimism)   3.5%     🟢 A+    $0.3   $1M
🥈 Beefy        (Optimism)   3.4%     🟡 B+    $0.3   $1M
🥉 Compound V3  (Polygon)    2.9%     🟢 A+    $0.5   $0M

💡 智能推荐:
   ✅ Compound V3 (Optimism) 综合最优 - 3.47% APY
```

## 支持的平台

### 借贷协议
- **Aave V3**（评级A，支持多种区块链） - https://app.aave.com
- **Compound V3**（评级A+，交易费用最低） - https://app.compound.finance
- **Spark**（评级A，收益率较高） - https://app.spark.fi
- **Morpho**（评级B+，利率优化） - https://app.morpho.org
- **Euler**（评级B，功能创新） - https://app.euler.finance

### DEX流动性池
- **Curve**（评级A，专注于稳定币交易） - https://curve.fi
- **Uniswap V3**（评级A，交易量最大） - https://app.uniswap.org
- **Balancer**（评级A，支持多种代币交易） - https://app.balancer.fi
- **Convex**（评级B+，提供CRV奖励机制） - https://www.convexfinance.com

### 收益聚合器
- **Yearn V2**（评级B+，自动复利功能） - https://yearn.finance
- **Beefy**（评级B+，支持多种区块链） - https://app.beefy.com
- **Automata**（评级B，注重隐私保护） - https://www.ata.network

### 稳定币平台
- **Ethena**（评级B+，基于合成美元的稳定币） - https://www.ethena.fi
- **Ondo**（评级A，由RWA支持） - https://www.ondo.finance
- **MakerDAO**（评级A+，DAI发行方） - https://makerdao.com

## 数据来源

- **主要数据源**：DeFiLlama API（https://yields.llama.fi/pools）
- **更新频率**：实时更新（数据缓存周期为5分钟）
- **覆盖范围**：50多个平台、7种区块链、3种稳定币

## 价格

| 价格等级 | 费用 | 每日查询次数限制 |
|------|-------|-------------------|
| 免费 | $0 | 3次 |
| 按次付费 | 0.01 USDT | 无限制 |
| 月度订阅 | 10 USDT | 无查询次数限制 + 优先支持 |

## 赞助商

支持项目开发：

- **USDT（ERC20）**：`0x33f943e71c7b7c4e88802a68e62cca91dab65ad9`
- **USDC（ERC20）**：`0xcb5173e3f5c2e32265fbbcaec8d26d49bf290e44`

## 安全与风险声明

⚠️ **重要提示**：DeFi协议存在智能合约风险。请务必：
1. 查看协议的审计报告（我们提供风险评级）
2. 从小额投资开始
3. 在不同平台分散投资
4. 切勿投资超出您能承受的损失范围

**本工具仅提供信息，不提供财务建议。请自行判断风险！**

## 开发计划

- [ ] 支持更多代币的比较功能（如USDT、USDC）
- [ ] 历史收益趋势分析
- [ ] 提供Telegram/Email通知功能
- [ ] 添加平台官网链接
- [ ] 支持更多区块链（如Monad、Sonic等）

## 技术支持

- GitHub：https://github.com/gztanht/yield-shark
- ClawHub：https://clawhub.com/skills/yield-shark

---

**由@gztanht开发**

*嗅探财富*