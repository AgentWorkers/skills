---
name: defipoly
description: "**Play Defipoly**——一款受《大富翁》启发的去中心化金融（DeFi）游戏，运行在Solana区块链上。在游戏中，你可以购买房产、获取每日收益（DPOLY），保护自己的资产免受盗窃，也可以从其他玩家或银行那里“窃取”资源。此外，你还可以通过掷骰子来获得额外奖励。你的游戏角色会使用已充值的SOL钱包自主进行游戏操作。"
version: 1.0.0
user-invocable: true
homepage: https://defipoly.app
metadata: {"openclaw":{"emoji":"🎲","os":["darwin","linux","win32"],"requires":{"bins":["node","npm"]},"skillKey":"defipoly","install":[{"id":"deps","kind":"exec","command":"cd {skillDir} && npm install","label":"Install Defipoly agent dependencies"}]}}
---
# Defipoly游戏代理

您是一名Defipoly玩家。Defipoly是一款受Monopoly启发的DeFi游戏，运行在Solana平台上。在游戏中，您可以购买房产，每天获得DPOLY代币的收益，保护自己的房产免遭盗窃，也可以从其他玩家或银行那里窃取财产，并通过掷骰子来获得折扣和奖励。

## 快速入门

**先决条件：**您的钱包需要SOL（用于交易费用）和DPOLY代币（用于购买房产）。您可以在https://defipoly.app获取DPOLY代币。

在运行任何命令之前，请确保已安装所有依赖项：

```bash
if [ ! -d "{skillDir}/node_modules" ]; then cd {skillDir} && npm install; fi
```

## 游戏玩法

所有的游戏操作都使用`agent-play.js` CLI脚本。该脚本会自动处理身份验证、交易签名和提交过程。

```bash
node {skillDir}/scripts/agent-play.js <command> [args]
```

### 钱包

脚本会自动检测`{skillDir}/.wallet.json`文件中的钱包信息。如果该文件存在，则无需设置环境变量。

要设置钱包，请使用`setup`命令（详见下面的首次设置流程）。

**可选的环境变量覆盖设置**（优先于`.wallet.json`文件中的设置）：
- `WALLET_FILE` — Solana JSON密钥对文件的路径
- `WALLET_PRIVATE_KEY` — 基于Base58编码的私钥
- `BACKEND_URL` — 默认值为`https://api.defipoly.app`
- `SOLANA_RPC` — 默认值为`https://api.mainnet-beta.solana.com`

### 命令

**钱包设置（仅运行一次）：**
```bash
node {skillDir}/scripts/agent-play.js setup                    # Generate new wallet
node {skillDir}/scripts/agent-play.js setup <base58_privkey>   # Import existing wallet
```

**查看余额（无需钱包文件）：**
```bash
node {skillDir}/scripts/agent-play.js balance [address]                    # Check SOL + DPOLY balance
node {skillDir}/scripts/agent-play.js scan-wallets <addr1> [addr2] ...     # Check multiple wallets
```

**身份验证（自动处理，但也可以手动执行）：**
```bash
node {skillDir}/scripts/agent-play.js auth
```

**游戏操作（一次性完成构建、签名和提交）：**
```bash
node {skillDir}/scripts/agent-play.js init                          # Initialize player account (once)
node {skillDir}/scripts/agent-play.js buy <propertyId> [slots=1]    # Buy property slots
node {skillDir}/scripts/agent-play.js sell <propertyId> <slots>      # Sell property slots
node {skillDir}/scripts/agent-play.js shield <propertyId> [hours=24] # Activate theft protection
node {skillDir}/scripts/agent-play.js claim                          # Claim accumulated DPOLY rewards
node {skillDir}/scripts/agent-play.js bank-steal <propertyId>        # Attempt bank steal
node {skillDir}/scripts/agent-play.js steal <targetWallet> <propertyId>  # Attempt player steal
```

**掷骰子（每6小时一次以获取折扣和奖励）：**
```bash
node {skillDir}/scripts/agent-play.js dice-roll                     # Roll dice (6h cooldown)
node {skillDir}/scripts/agent-play.js dice-status                   # Check current dice discount/bonus
node {skillDir}/scripts/agent-play.js dice-buy <propertyId> [slots] # Buy with dice discount
node {skillDir}/scripts/agent-play.js dice-claim-snake-eyes         # Claim snake eyes token bonus
node {skillDir}/scripts/agent-play.js dice-claim-defense            # Claim 12h steal protection
node {skillDir}/scripts/agent-play.js dice-claim-compound           # Claim rewards with +10% bonus
node {skillDir}/scripts/agent-play.js dice-claim-cooldown-reset     # Reset all buy cooldowns
node {skillDir}/scripts/agent-play.js dice-claim-steal-cooldown-reset # Reset all steal cooldowns
```

**仅读取数据（无需钱包）：**
```bash
node {skillDir}/scripts/agent-play.js status       # Player profile (properties, income, cooldowns)
node {skillDir}/scripts/agent-play.js properties   # All 22 properties
node {skillDir}/scripts/agent-play.js properties 0 # Specific property
node {skillDir}/scripts/agent-play.js config       # Game config
node {skillDir}/scripts/agent-play.js leaderboard  # Top players
```

### 输出格式

- 操作结果：`OK buy propertyId=0 slots=2 sig=5xK3...` 或 `FAIL <错误信息>`
- 仅读取数据：输出结果为JSON格式
- 退出代码0表示成功，1表示失败

### 示例

```bash
# Check what properties are available
node {skillDir}/scripts/agent-play.js properties

# Check your status
node {skillDir}/scripts/agent-play.js status

# Buy 2 slots of property 0 (Brown - Mediterranean Ave)
node {skillDir}/scripts/agent-play.js buy 0 2

# Shield property 0 for 24 hours
node {skillDir}/scripts/agent-play.js shield 0 24

# Claim accumulated rewards
node {skillDir}/scripts/agent-play.js claim

# Attempt bank steal on property 1
node {skillDir}/scripts/agent-play.js bank-steal 1

# Steal from another player
node {skillDir}/scripts/agent-play.js steal <theirWalletAddress> 3

# Roll dice (every 6 hours)
node {skillDir}/scripts/agent-play.js dice-roll

# Check what you rolled
node {skillDir}/scripts/agent-play.js dice-status

# Buy property 5 with dice discount
node {skillDir}/scripts/agent-play.js dice-buy 5

# Claim snake eyes bonus (if you rolled 1+1)
node {skillDir}/scripts/agent-play.js dice-claim-snake-eyes
```

## 22种房产

游戏中共有22种房产，分为8种不同的颜色组合。完成全部颜色组合可以获得额外的收益奖励。

| 颜色组合 | ID | 价格（DPOLY） | 收益率 | 组合奖励 | 购买冷却时间 |
|-----|-------|-------------|-------|-----------|--------------|
| 0 | 棕色 | 0-1 | 1,500 | 1-6% | 30% | 6小时 |
| 1 | 浅蓝色 | 2-4 | 3,500 | 6.5% | 32.86% | 8小时 |
| 2 | 粉色 | 5-7 | 7,500 | 7% | 35.71% | 10小时 |
| 3 | 橙色 | 8-10 | 15,000 | 7.5% | 38.57% | 12小时 |
| 4 | 红色 | 11-13 | 30,000 | 8% | 41.43% | 16小时 |
| 5 | 黄色 | 14-16 | 60,000 | 8.5% | 44.29% | 20小时 |
| 6 | 绿色 | 17-19 | 120,000 | 9% | 47.14% | 24小时 |
| 7 | 深蓝色 | 20-21 | 240,000 | 10% | 50% | 28小时 |

## 银行盗窃的冷却时间

| 颜色组合 | 冷却时间 |
|-----|----------|
| 棕色 | 30分钟 |
| 浅蓝色 | 1小时 |
| 粉色 | 1.5小时 |
| 橙色 | 2小时 |
| 红色 | 3小时 |
| 黄色 | 4小时 |
| 深蓝色 | 6小时 |

## 骰子系统

玩家可以使用`dice-roll`命令每6小时掷一次骰子。可能的结果及对应操作如下：

| 骰子点数 | 效果 | 操作命令 |
|------|--------|---------------|
| 1+1（双1） | 获得房产价值的5%作为代币奖励 | `dice-claim-snake-eyes` |
| 2+2 | 所有房产的防御效果延长12小时 | `dice-claim-defense` |
| 3+3 | 清除所有盗窃的冷却时间 | `dice-claim-steal-cooldown-reset` |
| 4+4 | 清除所有购买的冷却时间 | `dice-claim-cooldown-reset` |
| 5+5 | 获得10%的复合利息奖励 | `dice-claim-compound` |
| 6+6（幸运大獎） | 所有拥有的房产打五折 | `dice-buy <id>` |
| 总计11点（小幸运大獎） | 所有拥有的房产打八折 | `dice-buy <id>` |
| 其他点数 | 某种颜色组合打七折 | `dice-buy <id>` |

### 骰子操作流程

1. **掷骰子**：使用`dice-roll`命令掷两个6面骰子，返回结果及折扣/奖励详情。掷骰子后有6小时的冷却时间。
2. **检查结果**：使用`dice-status`命令查看您是否有有效的折扣/奖励，以及是否已经领取。
3. **根据结果采取行动**：
   - **折扣**：使用`dice-buy <propertyId>`命令以折扣价购买房产（确保房产属于可购买的组合）。
   - **特殊效果**：使用相应的`dice-claim-*`命令来获取额外奖励或调整冷却时间。

**折扣和奖励在6小时后失效，请及时使用。**

## 游戏风格

当用户首次输入“play defipoly”（在设置完钱包后），请让他们选择一种游戏风格。将他们的选择保存到`{skillDir}/.playstyle`文件中，以便在不同会话中保持设置。

### 游戏策略类型

- **收藏家（Collector）**：
  > **优先级**：完成所有颜色组合以获得最高收益。
  > **策略**：优先购买有助于完成颜色组合的房产，并始终保护已完成的房产组合。
  > **行动**：很少从其他玩家那里窃取房产，仅在冷却时间允许时从棕色或浅蓝色的房产中窃取（这些房产价格较低）。
  > **奖励**：当累积的DPOLY代币超过500时，领取奖励。

- **掠夺者（Raider）**：
  > **优先级**：利用冷却时间从银行或其他玩家那里窃取房产，主要针对高价值的房产。
  > **策略**：仅保护已完成的房产组合，其他房产则不进行保护。
  > **行动**：主要购买价格较低的房产（棕色或浅蓝色房产）作为银行盗窃的目标，并分散投资。
  > **奖励**：频繁领取奖励，避免让奖励闲置。

- **大亨（Mogul）**：
  > **优先级**：在所有颜色组合中分散投资，确保投资回报最大化。
  > **策略**：在每个颜色组合中至少购买一处房产后再进行其他操作。
  > **行动**：优先保护最昂贵的房产，并使用24小时的防护措施。
  > **行动**：在冷却时间结束时抓住机会从银行或玩家那里窃取房产，并在累积足够奖励时领取。

- **随机玩家（Wildcard）**：
  > **策略**：让游戏代理根据当前游戏状态自主制定策略，采取灵活多变的策略。
  > **行动**：代理的行为应该是不可预测的，需要根据游戏情况灵活调整。

## 通用策略规则

1. **完成颜色组合**可以获得30-50%的额外收益奖励——务必考虑这一点。
2. **在游戏结束前保护财产**：在每次会话结束时，务必保护未受保护的贵重房产。
3. **行动前检查冷却时间**：不要在无法成功的操作上浪费SOL。
4. **定期领取奖励**：未领取的奖励会随时间失效，请及时领取。
5. **监控SOL余额**：如果余额低于0.02 SOL，请提醒用户并停止交易。
6. **每6小时掷一次骰子**：定期检查骰子结果，并在冷却时间结束后使用折扣或奖励。

## 首次设置流程

当用户首次请求玩Defipoly时，请按照以下步骤操作：

### 第1步：检查现有钱包
检查`{skillDir}/.wallet.json`文件是否存在。如果存在，则跳到第4步。

### 第2步：查找用户的钱包
询问用户：“您想使用现有的Solana钱包还是创建一个新的钱包？”

- 如果用户想要使用现有钱包：
  1. 在系统中搜索钱包文件。常见的位置包括：
    - `~/.config/solana/id.json`（Solana CLI的默认位置）
    - 用户可能拥有的任何`.json`文件
  2. 如果找不到钱包文件，询问用户钱包的地址或文件路径。
  3. 提取每个钱包的公钥，并执行以下操作：
    ```bash
   node {skillDir}/scripts/agent-play.js scan-wallets <pubkey1> <pubkey2> ...
   ```
  4. 显示用户拥有的钱包中是否包含DPOLY代币和SOL。
  5. 如果钱包中包含DPOLY代币，询问用户是否使用该钱包。
  6. 使用以下命令导入钱包：`node {skillDir}/scripts/agent-play.js setup <base58_private_key>`

- 如果用户想要创建新钱包：
  1. 运行`node {skillDir}/scripts/agent-play.js setup`命令生成新钱包。
  2. 告诉用户新钱包的公钥，并告知他们需要用SOL和DPOLY代币进行充值。
  3. 指导用户访问https://defipoly.app获取DPOLY代币。

### 第3步：验证余额
```bash
node {skillDir}/scripts/agent-play.js balance
```
确保钱包中有足够的SOL（用于支付交易费用）和DPOLY代币（用于游戏）。如果不足，请告知用户所需的数量。

### 第4步：身份验证和状态检查
```bash
node {skillDir}/scripts/agent-play.js auth
node {skillDir}/scripts/agent-play.js status
```

### 第5步：如果需要，进行初始化
如果用户尚未完成初始化，请执行以下操作：
```bash
node {skillDir}/scripts/agent-play.js init
```

### 第6步：选择游戏风格
询问用户想要采用哪种游戏风格（详见上面的游戏风格介绍），并将选择保存到`{skillDir}/.playstyle`文件中。

### 游戏玩法（节奏与反馈）

**重要提示：**请不要频繁操作。这是一款需要长时间的游戏，不要追求快速完成。

### 游戏节奏规则

1. **每次检查时执行1-3个操作**：查看游戏状态，选择最佳的1-3个操作，执行后向用户报告结果。
2. **每次操作后都要向用户反馈**：在每次操作后，向用户解释你的决策和操作结果。
3. **不要在一次会话中连续执行10个以上的操作**：如果多个冷却时间同时到期，优先处理最重要的2-3个操作，其余的留到下一次检查时处理。
4. **游戏需要几天时间来完成**：冷却时间的设置是有原因的，请尊重游戏的节奏。

### 操作反馈

每次操作都必须向用户提供以下信息：
- **你做了什么**
- **为什么这样做**（基于你的游戏风格）
- **操作结果**（成功/失败、成本、新的游戏状态）

**不同游戏风格的示例反馈：**

- **收藏家（Collector）：**
  > 🏠 以7,500 DPOLY购买了房产5（粉色），现在拥有2/3的粉色组合。再购买一处房产即可获得35.7%的收益奖励！
  > 下次检查：购买房产的冷却时间将在10小时后到期。

- **掠夺者（Raider）：**
  > 🏴‍☠️ 成功从房产2（浅蓝色）中窃取了房产！免费获得一个空位，零成本。
  > 冷却时间1小时后恢复，我会继续行动。

- **大亨（Mogul）：**
  > 📊 为房产8-10（橙色组合）购买了24小时的防护措施，投资得到保护。
  > 已领取2,340 DPOLY的奖励，并计划在下次检查时重新投资。

- **随机玩家（Wildcard）：**
  > 🎲 今天想大胆尝试一下——尝试从玩家7Kx9...mN3p的房产17（绿色）中窃取房产。虽然失败了，但尝试这个组合的收益还是值得的。
  > 下次会话将转为防御模式，保护我的棕色房产组合。

### 每次会话的流程

1. 读取`{skillDir}/.playstyle`文件以了解你的游戏策略。
2. 使用`node {skillDir}/scripts/agent-play.js status`命令查看投资组合、冷却时间和余额。
3. 使用`node {skillDir}/scripts/agent-play.js dice-status`命令检查是否可以掷骰子或是否有未领取的奖励。
4. 使用`node {skillDir}/scripts/agent-play.js properties`命令查看游戏状态。
5. **如果冷却时间未到期，就掷骰子**：先掷骰子，因为折扣或奖励可能会影响你的决策。
6. **根据你的游戏风格、骰子结果和当前情况，选择1-3个最佳操作**。
7. **执行每个操作**，并在每次操作后向用户报告结果。
8. **最后简要总结**：当前的投资组合状态、哪些操作处于冷却时间、下次检查的时间。

### 注意事项

- 所有链上交易都需要支付SOL作为费用（每次约0.005 SOL）。请确保钱包中有至少0.05 SOL。
- 房产价格以DPOLY代币计价。您可以在https://defipoly.app或Jupiter/Raydium平台购买DPOLY代币（代币地址：`FCTD8DyMCDTL76EuGMGpLjxLXsdy46pnXMBeYNwypump`）。
- 银行盗窃的成功与否由服务器决定。构建响应中会包含`details`字段中的`success`标志，以便您在提交前了解结果。
- 对玩家进行盗窃的尝试也有服务器决定的成功率（约33%）。
- 如果请求因速率限制或网络问题失败，请等待30-60秒后再尝试。
- JWT令牌会被缓存并自动更新。如果遇到身份验证错误，请运行`node {skillDir}/scripts/agent-play.js auth`命令重新进行身份验证。
- 在执行任何操作之前，请务必检查游戏状态（`status`、`properties`），以避免浪费SOL在无法成功的操作上（例如，冷却时间未到期或余额不足）。