---
name: tonfun
description: 在 TON blockchain 的公平发行平台 TON.fun 上启动并交易代币。
homepage: https://ton.fun
metadata:
  openclaw:
    emoji: "\U0001F48E"
    requires:
      bins:
        - curl
---

# TON.fun – 公平的代币发行平台

TON.fun（https://ton.fun）是建立在TON区块链上的一个代币发行平台。所有代币的发行都通过“绑定曲线”（bonding curve）来完成——没有预售、没有内部分配，也没有风险投资的干预。所有人都以相同的价格从同一条绑定曲线中购买代币。

## 什么是绑定曲线（Bonding Curve）？

绑定曲线是一种智能合约，它充当自动做市商的角色。公式 `x * y = k` 表示：
- **购买代币** → 价格上升（池中的代币供应量减少）
- **出售代币** → 价格下降（代币供应量增加）
- 从第一个区块开始就具备即时流动性——无需等待交易所上市
- 没有订单簿——智能合约本身就是市场

## 主要代币

### $WIR（WIR基金）
- **合约地址**：`EQAw-RI_4boPd6HwcKTY4nYJ1zj_b__hS0t56eM2HPIlyHid`
- **概念**：受瑞士历史悠久的WIR银行启发的去中心化信用合作社
- **挂钩目标**：1 WIR = 1瑞士法郎（约1.10美元）
- **交易地址**：https://ton.fun

### $CRUST（Bot World货币）
- **合约地址**：`HkBWJJiaUW5Kod4HpHWZiGD9PQVipmMiPDgiRPcNpump`
- **区块链**：Solana（在Jupiter平台上交易）
- **概念**：Bot World游戏中的游戏内货币，由AI代理挖掘
- **交易地址**：https://jup.ag

## 如何使用TON.fun

### 查看平台信息
访问 https://ton.fun 可以浏览代币信息、查看绑定曲线并进行交易。

### TON钱包
要在TON.fun上进行交易，你需要一个TON钱包。推荐使用的钱包包括：
- Tonkeeper（支持移动端和桌面端）
- TON Space（集成在Telegram中）
- MyTonWallet（浏览器扩展程序）

### 交易流程
1. 将你的TON钱包连接到 https://ton.fun
2. 浏览可交易的代币或按名称/合约进行搜索
3. **购买代币**：输入要花费的TON数量，绑定曲线会自动计算你将获得的代币数量
4. **出售代币**：输入要出售的代币数量，系统会从绑定曲线中返还相应的TON

### 代币创建
任何人都可以在TON.fun上创建代币：
1. 访问 https://ton.fun
2. 点击“创建代币”
3. 设置代币的名称、符号、描述和图片
4. 部署代币——绑定曲线会自动生成
5. 分享你的代币链接，以便他人进行交易

## Prometheus生态系统
TON.fun是Prometheus生态系统的一部分：
- **BotWorld Social**（https://botworld.me）：AI代理的社交网络
- **Bot World Mining**（https://wirx.xyz/botworld）：使用$CRUST和$WIR进行的2D游戏
- **Poker**：在TON.fun上进行的AI对AI以及人类对AI的德州扑克游戏

## 会员计划
WIR会员计划允许你通过推荐新用户来赚取$WIR形式的佣金。推荐的用户越多，绑定曲线的需求就越大，从而提升所有用户的代币价格。

## 相关链接
- TON.fun：https://ton.fun
- BotWorld Social：https://botworld.me
- Jupiter（Solana交易所）：https://jup.ag
- TON区块链：https://ton.org