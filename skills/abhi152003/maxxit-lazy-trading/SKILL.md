---
emoji: 📈
name: maxxit-lazy-trading
version: 1.2.8
author: Maxxit
description: 通过 Maxxit 的 Lazy Trading API，在 Ostium、Aster 和 Avantis 上执行永久性交易（即长期持有的交易）。该 API 提供了用于开仓/平仓、风险管理、获取市场数据、复制交易其他 OpenClaw 代理的程序化接口，以及一个无需信任的 Alpha Marketplace，用于买卖经过 ZK（Zcash-Kernel）验证的交易信号（这些信号来自 Arbitrum Sepolia）。
homepage: https://maxxit.ai
repository: https://github.com/Maxxit-ai/maxxit-latest
disableModelInvocation: true
requires:
  env:
    - MAXXIT_API_KEY
    - MAXXIT_API_URL
metadata:
  openclaw:
    requiredEnv:
      - MAXXIT_API_KEY
      - MAXXIT_API_URL
    bins:
      - curl
    primaryCredential: MAXXIT_API_KEY
---
# Maxxit 懒人交易（Lazy Trading）

通过 Maxxit 的懒人交易 API，在 Ostium、Aster DEX 和 Avantis DEX 上执行永续期货交易。此技能支持通过编程接口自动开仓/平仓和管理风险。

## 何时使用此技能

- 用户希望在 Ostium 上进行交易
- 用户希望在 Aster DEX 上进行交易
- 用户询问关于他们的懒人交易账户详情
- 用户想要查看他们的 USDC/ETH 余额
- 用户想要查看他们的未平仓头寸或投资组合
- 用户想要查看他们的平仓历史或利润/亏损（PnL）
- 用户想要查找可交易的符号
- 用户想要获取市场数据或 LunarCrush 指标用于分析
- 用户想要获取整个市场快照以用于交易
- 用户想要比较不同代币的排名（AltRank）
- 用户想要发现高情绪价值的交易机会
- 用户想要了解加密货币资产的社会媒体关注度趋势
- 用户想要开新的交易头寸（多头/空头）
- 用户想要平仓现有的头寸
- 用户想要设置或修改止盈水平
- 用户想要设置或修改止损水平
- 用户想要获取当前的代币/市场价格

## 代码示例

（由于代码示例较长，这里仅提供部分示例结构。实际代码请参考原始 SKILL.md 文件。）

---

## ⚠️ DEX 路由规则（必读）

1. **如有疑问，请先询问交易所**：“您想在 Ostium、Aster 还是 Avantis 上进行交易？”
2. **在回复中明确说明当前使用的交易所**（例如：“使用 Ostium...”）
3. **不要混合交易所建议**：
   - 如果用户在 **Ostium** 上交易，仅建议使用 Ostium 的接口/操作。
   - 如果用户在 **Aster** 上交易，仅建议使用 Aster 的接口/操作。
   - 如果用户在 **Avantis** 上交易，仅建议使用 Avantis 的接口/操作。
4. **不要询问网络类型**：
   - 在此设置中，**Ostium** 仅支持主网。
   - **Aster** 仅支持测试网。
   - **Avantis** 也仅支持主网（基础链）。
   - 因此，对于任何交易所都不要询问“主网还是测试网？”
5. 如果用户在对话过程中更改交易所，请确认更改后继续使用相应的交易所流程。