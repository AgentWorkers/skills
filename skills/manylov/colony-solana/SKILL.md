---
name: colony-solana
description: 在 Solana 上玩 Colony 游戏：购买土地、进行升级、领取 $OLO 收益，并通过 Jupiter 进行代币交换。完全自主的游戏体验，同时支持策略优化。
---
# 种植园游戏技巧

你是一个自主代理，负责管理在Solana主网上的种植园游戏账户。种植园是一款休闲游戏，你需要购买土地来开采$OLO代币。你的目标是通过战略性的土地购买、升级以及及时的收益领取来最大化收益。

## 环境设置

### 环境变量

| 变量 | 是否必需 | 描述 |
|----------|----------|-------------|
| `SOLANA_PRIVATE_KEY` | 是 | Solana密钥对的Base58编码私钥（首次运行时自动生成） |
| `SOLANA_RPC_URL` | 否 | Solana RPC端点（默认：`https://api.mainnet-beta.solana.com`） |
| `JUPITER_API_KEY` | 用于交换/查询价格 | 来自https://portal.jup.ag的免费API密钥（执行`swap`、`swap-quote`、`price`命令时需要） |

### 首次设置

首次设置时，请严格按照以下步骤操作：

#### 第1步：安装依赖项

```bash
cd <skill-directory>
npm install
```

#### 第2步：生成钱包

如果`SOLANA_PRIVATE_KEY`尚未设置，请生成一个新的钱包：

```bash
node colony-cli.mjs generate-wallet
```

这将输出包含`publicKey`和`privateKey`的JSON文件。**立即**：
1. 将`privateKey`保存为`SOLANA_PRIVATE_KEY`环境变量。**切勿共享**。
2. 记下`publicKey`——这就是你的钱包地址。

#### 第3步：让所有者为钱包充值

向所有者发送消息，内容包括：
- **钱包地址**：步骤2中获得的`publicKey`
- **充值金额**：至少需要0.05 SOL以支付交易费用。为了全面开始游戏（购买第一块土地），建议充值0.5-1 SOL，以便将SOL兑换成$OLO代币。
- **用途**：“这是我的种植园游戏钱包。我需要SOL来支付交易费用并兑换$OLO代币以购买土地。”

#### 第4步：等待充值并验证

所有者确认充值后，检查：

```bash
node colony-cli.mjs status
```

确认`solBalance`是否大于0。如果仍然为0，请等待30秒后再检查。

#### 第5步：将SOL兑换成$OLO代币

你需要$OLO代币来购买土地（每块土地需要10,000 $OLO）。首先获取报价：

```bash
node colony-cli.mjs swap-quote --sol-amount 0.3
```

如果报价合理，执行兑换操作：

```bash
node colony-cli.mjs swap --sol-amount 0.3
```

#### 第6步：购买第一块土地

找到一块可用的土地并购买它：

```bash
node colony-cli.mjs find-land --count 1
node colony-cli.mjs buy-land --land-id <id-from-above>
```

#### 第7步：验证并启动自动循环

```bash
node colony-cli.mjs status
```

此时你应该能看到一块正在开采$OLO代币的土地。接下来，请按照策略指南中的**自动循环**进行操作。

## 游戏机制

### 种植园的运作方式

- 玩家以每块10,000 $OLO的价格购买**土地（ID从1到21000）（购买后代币会被销毁）
- 每块土地会根据其等级持续开采$OLO代币
- 玩家可以**领取**累积的收益以获得实际的$OLO代币
- 土地可以**升级**（等级从1到10）以提高开采速度
- 每个钱包最多可以拥有**10块土地**
- $OLO是Solana主网上的Token-2022 SPL代币

### 收益速度（每天收益/等级）

| 等级 | 每天收益 | 累计升级成本 |
|-------|-------------|------------------------|
| 1 | 1,000 | 10,000（购买成本） |
| 2 | 2,000 | 11,000 |
| 3 | 3,000 | 13,000 |
| 4 | 5,000 | 17,000 |
| 5 | 8,000 | 25,000 |
| 6 | 13,000 | 41,000 |
| 7 | 21,000 | 73,000 |
| 8 | 34,000 | 137,000 |
| 9 | 45,000 | 265,000 |
| 10 | 79,000 | 417,000 |

### 升级成本

| 升级等级 | 成本（$OLO） | 每天额外收益 | 回报期（天） |
|---------|-----------|-------------------|------------|
| L1 -> L2 | 1,000 | +1,000 | 1.0 |
| L2 -> L3 | 2,000 | +1,000 | 2.0 |
| L3 -> L4 | 4,000 | +2,000 | 2.0 |
| L4 -> L5 | 8,000 | +3,000 | 2.7 |
| L5 -> L6 | 16,000 | +5,000 | 3.2 |
| L6 -> L7 | 32,000 | +8,000 | 4.0 |
| L7 -> L8 | 64,000 | +13,000 | 4.9 |
| L8 -> L9 | 128,000 | +11,000 | 11.6 |
| L9 -> L10 | 152,000 | +34,000 | 4.5 |
| 新L1土地 | 10,000 | +1,000 | 10.0 |

## CLI命令参考

所有命令都会输出JSON格式的结果。所有写入命令都需要`SOLANA_PRIVATE_KEY`。

### 设置命令

#### `generate-wallet` — 生成一个新的Solana密钥对

```bash
node colony-cli.mjs generate-wallet
```

返回：`publicKey`（用于充值的地址）和`privateKey`（保存为`SOLANA_PRIVATE_KEY`）。无需环境变量。

### 读取命令（执行`game-state`、`land-info`、`price`命令时不需要私钥）

#### `game-state` — 全局游戏状态

```bash
node colony-cli.mjs game-state
```

返回：游戏活动状态、已售出的土地总数、资金库余额以及地址信息。

#### `status` — 全部钱包信息及游戏概览

```bash
node colony-cli.mjs status
```

返回：钱包中的SOL/OLO余额、拥有的土地及其等级以及待领取的收益。

#### `land-info` — 详细土地信息及ROI分析

```bash
node colony-cli.mjs land-info --land-id 42
```

返回：土地等级、收益率、待领取的收益、升级成本及ROI。

#### `find-land` — 查找可用的（未拥有的）土地ID

```bash
node colony-cli.mjs find-land --count 3
```

返回：可用土地ID的列表（默认显示5块）。

#### `price` — 当前的$OLO代币价格

```bash
node colony-cli.mjs price
```

返回：来自Jupiter的$OLO代币价格。

#### `recommend` — 人工智能推荐策略

```bash
node colony-cli.mjs recommend
```

返回：按ROI优先级排序的推荐行动列表。

### 写入命令（需要`SOLANA_PRIVATE_KEY`）

#### `buy-land` — 购买一块土地

```bash
node colony-cli.mjs buy-land --land-id 42
```

消耗10,000 $OLO。返回：交易签名。

#### `upgrade-land` — 将土地升级到下一个等级

```bash
node colony-cli.mjs upgrade-land --land-id 42
```

根据当前等级消耗代币。返回：新的等级、升级成本及签名。

#### `claim` — 领取一块土地的收益

```bash
node colony-cli.mjs claim --land-id 42
```

将资金库中的$OLO代币转移到钱包。返回：领取的金额及签名。

#### `claim-all` — 领取所有拥有的土地的收益

```bash
node colony-cli.mjs claim-all
```

每次交易最多处理10次领取操作。返回：总领取金额及签名。

#### `swap-quote` — 获取Jupiter的交换报价（SOL -> $OLO）

```bash
node colony-cli.mjs swap-quote --sol-amount 0.1
```

返回：预期的$OLO输出、价格影响及交换路径。

#### `swap` — 执行Jupiter的交换操作（SOL -> $OLO）

```bash
node colony-cli.mjs swap --sol-amount 0.1
```

通过Jupiter聚合器将SOL兑换成$OLO。返回：兑换金额及签名。

## 策略指南

### 决策算法

当调用`recommend`命令时，它会按照以下优先级评估行动：
1. **立即领取收益** — 如果待领取的收益超过1,000 $OLO，则立即领取。
2. **按ROI优先级升级** — 按照ROI（回收期）对所有可承受的升级操作进行排序，并优先执行回收期最短的升级。
3. **购买新土地** — 如果拥有的土地少于10块且有能力支付10,000 $OLO。
4. **兑换SOL** — 如果$OLO代币不足但仍有SOL储备。

### ROI优先级顺序

优先考虑的升级选项（ROI最低 = 回收期最快）：
1. L1 -> L2（1.0天）
2. L2 -> L3（2.0天）
3. L3 -> L4（2.0天）
4. L4 -> L5（2.7天）
5. L5 -> L6（3.2天）
6. L6 -> L7（4.0天）
7. L9 -> L10（4.5天）
8. L7 -> L8（4.9天）
9. 新L1土地（10.0天）
10. L8 -> L9（11.6天）—— **ROI最低，除非其他选项都已达到上限**

### 自动循环

每4-6小时运行一次这个循环：

```
1. node colony-cli.mjs status          # Check current state
2. node colony-cli.mjs claim-all       # Claim if earnings > 1000
3. node colony-cli.mjs recommend       # Get next best action
4. Execute recommended action          # Buy/upgrade/swap
5. Repeat step 3-4 until no actions
```

### 安全规则

- **SOL储备**：始终保持至少0.01 SOL以支付交易费用。
- **谨慎进行交换**：在执行交换前先获取报价（使用`swap-quote`）。
- **大额交换**：在兑换超过1 SOL之前请先与用户确认。
- **价格检查**：在交换前使用`price`命令验证代币价格。
- **错误处理**：如果交易失败，请等待30秒后重试。

## 错误处理

### 常见错误及解决方法

| 错误 | 原因 | 解决方法 |
|-------|-------|---------|
| `OLO代币不足` | 代币数量不足 | 运行`recommend`命令检查是否需要交换 |
| 游戏暂停 | 系统暂停了游戏 | 等待一段时间后再尝试 |
| 土地已被拥有 | 土地已被他人购买 | 使用`find-land`命令查找可用的土地ID |
| 达到土地上限 | 土地数量达到上限 | 优先考虑升级 |
| 达到最高等级 | 土地已升级到L10 | 该土地无法再升级 |
| 未拥有该土地 | 土地ID错误 | 使用`status`命令查看拥有的土地 |
| 交易确认超时 | 网络拥堵 | 等待60秒后再次检查`status`（交易可能已成功） |
| Jupiter报价/交换失败 | DEX出现问题 | 30秒后重试；尝试较小的交易金额 |

### 检查交易状态

如果交易超时，请查看`status`以确认交易是否成功（余额或土地状态的变化应反映交易结果）。

## 关键地址

| 项目 | 地址 |
|------|---------|
| 程序ID | `BCVGJ5YoKMftBrt5fgDYhtvY7HVBccFofFiGqJtoRjqE` |
| 游戏代币（$OLO） | `2pXjxbdHnYWtH2gtDN495Ve1jm8bs1zoUL6XsUi3pump` |
| 游戏状态PDA | `6JFTxovd2WcSh9RTXKrjTsKAKBTDfsUM3FsLMXEe3eNZ` |
| 代币资金库PDA | `EgduLawRwk77jSdUhAmtcEyzrxvZXsyL8y8Ubj4dVnLA` |