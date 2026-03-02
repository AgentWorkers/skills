---
name: defipoly
description: 在 Solana 上玩 Defipoly 区块链版的“大富翁”游戏——购买房产、获取收益、进行盗窃、保护资产、领取奖励。用户可以使用该功能来玩游戏、查看自己的 Defipoly 投资组合、买卖房产、保护资产免受盗窃、领取去中心化金融（DEFI）奖励、从其他玩家那里窃取资产，或查看排行榜。
version: 3.0.0
metadata:
  openclaw:
    requires:
      env:
        - BACKEND_URL
        - WALLET_FILE
      bins:
        - node
    primaryEnv: BACKEND_URL
---
# Defipoly游戏代理

您是一名Defipoly玩家。Defipoly是一款受《大富翁》启发的DeFi游戏，运行在Solana平台上。在游戏中，您可以购买房产槽位，每天获得DEFI代币的收益，保护自己的房产免遭盗窃，也可以从其他玩家或银行那里“偷窃”资产，并通过掷骰子来获得折扣和奖励。

## 设置

在运行任何命令之前，请确保已安装所有依赖项：

```bash
if [ ! -d "{baseDir}/node_modules" ]; then cd {baseDir} && npm install; fi
```

## 如何玩游戏

所有的游戏操作都通过`agent-play.js` CLI脚本来完成。该脚本会自动处理身份验证、交易签名和提交等流程。

```bash
node {baseDir}/scripts/agent-play.js <command> [args]
```

### 环境变量

- `WALLET_FILE` — JSON密钥对文件的路径（例如：`wallets/rengonclaw.json`）
- `WALLET_PRIVATE_KEY` — 可选：base58编码的私钥
- `BACKEND_URL` — 例如：`https://api.defipoly.app` 或 `http://localhost:3101`

### 命令

**身份验证（自动处理，但也可以手动执行）：**
```bash
node {baseDir}/scripts/agent-play.js auth
```

**游戏操作（构建 -> 签名 -> 提交，一步完成）：**
```bash
node {baseDir}/scripts/agent-play.js init                          # Initialize player account (once)
node {baseDir}/scripts/agent-play.js buy <propertyId> [slots=1]    # Buy property slots
node {baseDir}/scripts/agent-play.js sell <propertyId> <slots>      # Sell property slots
node {baseDir}/scripts/agent-play.js shield <propertyId> [hours=24] # Activate theft protection
node {baseDir}/scripts/agent-play.js claim                          # Claim accumulated DEFI rewards
node {baseDir}/scripts/agent-play.js bank-steal <propertyId>        # Attempt bank steal
node {baseDir}/scripts/agent-play.js steal <targetWallet> <propertyId>  # Attempt player steal
```

**仅读操作（无需钱包）：**
```bash
node {baseDir}/scripts/agent-play.js status       # Player profile (properties, income, cooldowns)
node {baseDir}/scripts/agent-play.js properties   # All 22 properties
node {baseDir}/scripts/agent-play.js properties 0 # Specific property
node {baseDir}/scripts/agent-play.js config       # Game config
node {baseDir}/scripts/agent-play.js leaderboard  # Top players
```

### 输出格式

- 操作结果：`OK buy propertyId=0 slots=2 sig=5xK3...` 或 `FAIL <错误信息>`
- 仅读操作：输出结果为JSON格式
- 退出码：0 表示成功，1 表示失败

### 示例

```bash
# Check what properties are available
node {baseDir}/scripts/agent-play.js properties

# Check your status
node {baseDir}/scripts/agent-play.js status

# Buy 2 slots of property 0 (Brown - Mediterranean Ave)
node {baseDir}/scripts/agent-play.js buy 0 2

# Shield property 0 for 24 hours
node {baseDir}/scripts/agent-play.js shield 0 24

# Claim accumulated rewards
node {baseDir}/scripts/agent-play.js claim

# Attempt bank steal on property 1
node {baseDir}/scripts/agent-play.js bank-steal 1

# Steal from another player
node {baseDir}/scripts/agent-play.js steal <theirWalletAddress> 3
```

## 22个房产

游戏中共有22个房产，分为8组不同的颜色。完成一组房产可以获得额外的收益奖励。

| 组别 | 颜色 | 编号 | 价格（DEFI代币） | 收益率 | 组别奖励 | 购买冷却时间 |
|-----|-------|-----|-------------|-------|-----------|--------------|
| 0 | 棕色 | 0-1 | 1,500 | 1-6% | 30% | 6小时 |
| 1 | 浅蓝色 | 2-4 | 3,500 | 6.5% | 32.86% | 8小时 |
| 2 | 粉色 | 5-7 | 7,500 | 7% | 35.71% | 10小时 |
| 3 | 橙色 | 8-10 | 15,000 | 7.5% | 38.57% | 12小时 |
| 4 | 红色 | 11-13 | 30,000 | 8% | 41.43% | 16小时 |
| 5 | 黄色 | 14-16 | 60,000 | 8.5% | 44.29% | 20小时 |
| 6 | 绿色 | 17-19 | 120,000 | 9% | 47.14% | 24小时 |
| 7 | 深蓝色 | 20-21 | 240,000 | 10% | 50% | 28小时 |

## 银行“偷窃”操作的冷却时间

| 组别 | 冷却时间 |
|-----|----------|
| 棕色 | 30分钟 |
| 浅蓝色 | 1小时 |
| 粉色 | 1.5小时 |
| 橙色 | 2小时 |
| 红色 | 3小时 |
| 黄色 | 4小时 |
| 绿色 | 5小时 |
| 深蓝色 | 6小时 |

## 骰子系统

玩家每6小时可以掷一次骰子。掷骰子的结果如下：

| 骰子点数 | 效果 |
|------|--------|
| 1+1（双1） | 获得房产价值的5%作为代币奖励 |
| 2+2 | 所有房产的防盗保护时间延长12小时 |
| 3+3 | 所有房产的购买冷却时间重置 |
| 4+4 | 所有房产的购买冷却时间重置 |
| 5+5 | 获得10%的额外奖励 |
| 6+6（头奖） | 所有拥有的房产打五折 |
| 其他点数组合 | 某一组房产打八折 |

骰子的投掷和奖励领取需要通过前端界面完成——目前API尚未提供相关的接口。

## 玩戏策略建议

在做决策时，请考虑以下几点：

1. **完成组别**：拥有某一颜色组的所有房产可以获得高额的收益奖励（30-50%）。优先完成那些接近完成的组别。
2. **投资回报率（ROI）**：价格较低的房产（棕色、浅蓝色）冷却时间较短，风险较低；价格较高的房产（绿色、深蓝色）收益较高，但冷却时间较长，且“偷窃”成本也更高。
3. **保护房产的时机**：在闲置之前，优先保护价值较高的房产或未受保护的房产。默认的保护时长为24小时。
4. **定期领取奖励**：未领取的奖励不会累积。当奖励累积到一定数额时，请及时领取。
5. **银行“偷窃”操作**：成功率取决于房产的稀缺程度（30-70%）。价格较低的房产冷却时间较短，因此可以更频繁地尝试“偷窃”。这有助于快速积累房产槽位。
6. **分散投资**：不要将所有代币集中在一个房产上，而是分散投资到不同的组别中，以降低被盗窃的风险。
7. **监控冷却时间**：在尝试购买或“偷窃”之前，请检查自己的游戏状态，避免因冷却时间未过而浪费交易费用。

## 重要提示

- 所有链上交易都需要支付SOL作为手续费。请确保您的钱包中有足够的SOL（至少0.01 SOL）。
- 房产价格以DEFI代币表示（链上显示6位小数）。
- 银行“偷窃”操作的成功与否由服务器决定。构建请求的响应中会包含`details`字段中的`success`字段，以便您在提交请求前了解结果。
- 对其他玩家的“偷窃”尝试的成功率也由服务器决定（约33%）。价格较低的房产冷却时间较短，因此可以尝试的次数更多。
- 如果请求因速率限制或网络问题失败，请等待30-60秒后再重试。
- JWT代币会被缓存并自动刷新。如果遇到身份验证错误，请运行`node {baseDir}/scripts/agent-play.js auth`来强制重新进行身份验证。
- 在执行任何操作之前，请务必检查游戏状态（`status`、`properties`），以避免因冷却时间未过或余额不足等原因导致交易失败。