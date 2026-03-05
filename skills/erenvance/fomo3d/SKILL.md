---
name: fomo3d
description: 在 BNB Chain（BSC）上可以玩 Fomo3D 和老虎机游戏。Fomo3D 是一款基于区块链的游戏，玩家需要使用代币来购买游戏股份；在倒计时结束前最后一个购买股份的人将赢得大奖。该游戏还包含一个由 VRF（Verifiable Random Function）技术驱动的老虎机小游戏，可以实现随机抽奖功能。此技能提供了一个命令行界面（CLI），用于查询游戏状态、购买股份、领取股息、进行老虎机抽奖等操作。
version: 1.2.0
metadata:
  openclaw:
    emoji: "🎰"
    homepage: "https://fomo3d.app"
    primaryEnv: FOMO3D_PRIVATE_KEY
    requires:
      env:
        - FOMO3D_PRIVATE_KEY
      bins:
        - node
---
# Fomo3D — BNB Chain区块链游戏

Fomo3D是一款基于BNB Chain（BSC）的去中心化游戏，提供两种游戏模式：

1. **Fomo3D主游戏**：玩家使用代币购买游戏股份。每次购买会重置倒计时。当倒计时归零时，最后的购买者将赢得全部奖金池。所有股东都会从每次购买中获得分红。

2. **老虎机**：玩家使用代币进行随机抽奖，抽奖结果由VRF（Verifiable Random Function）生成。匹配的符号可以带来高达100倍的奖励。玩家每次抽奖都会获得分红股份。

## 安装与配置（必选）

确保在仓库根目录下安装了所有依赖项（使用`npm install`命令）。

游戏需要一个私钥。如果用户尚未配置私钥，请从仓库根目录运行`fomo3d setup`命令。该命令会提示用户输入：
- BSC私钥（用于签署交易）
- 网络（测试网或主网）
- 可选的自定义RPC地址

或者，也可以通过设置环境变量来配置（无需运行`setup`命令）：
- `FOMO3D_PRIVATE_KEY`：BSC钱包私钥（十六进制格式，可带0x前缀）
- `FOMO3D_NETWORK`：`testnet`或`mainnet`（默认为测试网）
- `FOMO3D_RPC_URL`：自定义RPC端点

**重要提示：**钱包必须是一个外部拥有的账户（EOA），而不是智能合约钱包。游戏合约要求`msg.sender == tx.origin`。

## 运行方式（命令行界面）

请从仓库根目录运行程序（`package.json`文件所在的位置）。若需要机器可读的输出，请在命令后添加`--json`参数。命令行会在`--json`模式下将输出结果以JSON格式打印到标准输出。

### 错误处理

如果发生错误，命令行会向标准输出打印`{"success":false,"error":"message"}`并退出（退出代码为1）。如果操作成功，命令行会打印`{"success":true,"data":{...}`。

## 重要概念

### 代币单位

命令行参数和JSON输出中的所有代币数量均以**wei**为单位（18位小数）。例如：
- 1个代币 = `1000000000000000000`（1e18）
- 0.5个代币 = `500000000000000000`（5e17）

向用户显示数量时，需除以1e18以获得更易读的数值。

### 股份数量

`purchase --shares`命令中的股份数量为**整数**（而非wei）。1份等于1份股份。

### 自动批准

命令行会在执行`purchase`、`buy`、`sell`、`slot spin`和`slot deposit`操作前自动检查用户的ERC20代币权限，并在需要时自动批准。无需手动批准。

### FOMO代币交易

FOMO代币在FLAP平台上交易（使用BNB Chain的债券曲线）。交易通过FlapSkill合约（地址：`0x03a9aeeb4f6e64d425126164f7262c2a754b3ff9`）进行自动路由：
- **内盘（Portal）**：当代币仍在债券曲线上时
- **外盘（PancakeSwap V2/V3）**：当代币转移到DEX后

所有交易均使用**USDT**作为报价代币。`buy/sell`命令仅在**主网**上可用。

### VRF（可验证随机函数）

老虎机抽奖使用Binance Oracle的VRF机制来保证随机性的公平性。每次抽奖需要支付少量BNB费用（约0.00015 BNB，通过`msg.value`字段传递）。抽奖结果由VRF回调决定（1-3个区块后返回）。可以使用`fomo3d slot status`或`fomo3d player`命令查看结果。

## 命令参考

### 设置

**配置钱包信息：**
`fomo3d setup`  
- 交互式配置：提示用户输入私钥、网络和可选的RPC地址。配置信息将保存到`config.json`文件中。

### 检查钱包余额：**
`fomo3d wallet --json`  
- 返回指定钱包的BNB余额和FOMO代币余额。

**输出字段：** `address`, `bnbBalance`（wei），`tokenBalance`（wei），`tokenSymbol`，`tokenDecimals`

### 查看当前轮次信息：**
`fomo3d status --json`  
- 返回当前轮次的状态，包括倒计时、奖金池、股份价格和最后购买者的信息。

**输出字段：** `currentRound`，`roundStatus`（未开始/进行中/已结束），`paused`，`countdownRemaining`（秒），`grandPrizePool`（wei），`dividendPool`（wei），`sharePrice`（wei），`totalShares`，`lastBuyers`（地址数组），`pools`

**策略提示：**  
- 当`countdownRemaining`时间较短时，购买股份具有更高的预期价值，因为您有可能赢得奖金。每次购买都会使倒计时重置。

### 查看玩家信息：**
`fomo3d player --json`  
- 返回玩家的持股数量、收益和待提取的收益。如果没有指定地址，将使用默认配置的钱包。

**输出字段：** `address`，`shares`，`totalEarnings`（wei），`pendingEarnings`（wei），`pendingWithdrawal`（wei），`hasExited`，`currentRound`

**决策指南：**
- 如果`pendingWithdrawal`大于0：在购买更多股份之前，必须先运行`fomo3d settle`命令。
- 如果`pendingEarnings`大于0且当前轮次仍在进行中：可以选择`exit`以锁定收益，或者继续持有以获取更多分红。
- 如果`hasExited`为`true`：表示已退出当前轮次，等待轮次结束或进行收益结算。

### 购买股份：**
`fomo3d purchase --shares`  
- 在当前轮次购买股份。`--shares`参数为整数，表示购买的数量（而非wei）。代币价格 = 股份数量 × `sharePrice`（自动计算）。

**系统自动执行的检查：**
- 游戏必须处于进行中状态。
- 不能有未完成的提款操作（必须先完成`settle`操作）。
- 代币权限会自动检查并批准（如需要）。

**输出字段：** `txHash`，`blockNumber`，`status`，`sharesAmount`，`tokensCost`（wei）

### 退出游戏：**
`fomo3d exit --json`  
- 退出当前轮次并锁定您的收益。

**输出字段：** `txHash`，`blockNumber`，`status`

### 结算分红和奖金：**
`fomo3d settle --json`  
- 在轮次结束后结算分红和奖金。当`pendingEarnings`或`pendingWithdrawal`大于0时必须调用此命令。

**输出字段：** `txHash`，`blockNumber`，`status`，`pendingEarnings`（wei），`pendingWithdrawal`（wei）

### 结束轮次：**
`fomo3d end-round --json`  
- 结束倒计时归零的轮次。任何人都可以调用此命令。奖金将分配给最后的购买者。

**输出字段：** `txHash`，`blockNumber`，`status`

### 使用USDT购买FOMO代币（仅限主网）：**
`fomo3d buy --amount`  
- 通过FLAP平台使用USDT购买FOMO代币。FlapSkill合约会根据代币状态自动选择内盘（Portal）或外盘（PancakeSwap）进行交易。USDT权限会自动批准。

**示例：** 使用10 USDT购买FOMO代币：
**输出字段：** `txHash`，`blockNumber`，`status`，`usdtSpent`（wei），`token`

### 卖出FOMO代币换取USDT（仅限主网）：**
`fomo3d sell --amount`  
- 指定要出售的代币数量（以wei为单位，18位小数）。
`fomo3d sell --percent`  
- 按持有代币的比例出售（10000=100%，5000=50%，1000=10%）。

**注意：** 不能同时使用这两个参数。代币权限会自动批准。

**示例：** 出售50%的代币：
**输出字段（--amount）：** `txHash`，`blockNumber`，`status`，`tokensSold`（wei），`method`
**输出字段（--percent）：** `txHash`，`blockNumber`，`status`，`percentBps`，`method`

### 查询代币信息：**
`fomo3d token-info --json`  
- 查询FOMO代币在FLAP平台上的状态和您的持有量。

**输出字段（主网）：** `token`，`network`，`status`（未创建/可交易/在DEX/锁定中），`phase`（内盘/外盘），`quoteToken`，`currentPrice`（wei），`totalSupply`（wei），`reserveBalance`（wei），`progress`（wei），`fomoBalance`（wei），`usdtBalance`（wei），`account`

**决策指南：**
- 如果`status`为`Tradable`：代币位于内盘（债券曲线上），可通过Portal进行交易。
- 如果`status`为`DEX`：代币已转移到外盘（PancakeSwap），可通过DEX进行交易。
- `progress`表示代币距离转移到外盘的进度（数值越高，转移越接近）。

### 查看老虎机信息：**
`fomo3d slot status --json`  
- 返回老虎机的配置信息、奖金池和统计数据。

**输出字段：** `paused`，`token`，`minBet`（wei），`maxBet`（wei），`prizePool`（wei），`totalShares`，`vrfFee`（wei），`stats`（`totalSpins`，`totalBetAmount`，`totalWinAmount`，`totalDividendsDistributed`）

**注意：** `maxBet` = `prizePool / 100`（动态计算）。奖金池较低时，最大投注额也会相应减少。

### 进行老虎机抽奖：**
`fomo3d slot spin --bet`  
- 进行老虎机抽奖。需要足够的代币余额进行投注，并支付VRF费用（约0.00015 BNB）。

**限制：**
- `minBet` ≤ `bet` ≤ `maxBet`。
- 钱包必须有足够的BNB来支付VRF费用。
- 在之前的抽奖结果尚未返回之前，无法进行新的抽奖。

**抽奖结果：**
- 抽奖结果不在响应中显示。结果将在1-3个区块后通过VRF回调确定。可以使用`fomo3d player --json`或`fomo3d slot status --json`命令查看结果。

### 取消未完成的抽奖：**
`fomo3d slot cancel --json`  
- 取消因VRF响应延迟而未完成的抽奖。

**输出字段：** `txHash`，`blockNumber`，`status`

### 向奖金池充值：**
`fomo3d slot deposit --amount`  
- 将代币充值到老虎机奖金池。**注意：** 充值的代币将永久锁定。每次抽奖后，所有充值者将根据投注金额的比例获得分红。

**输出字段：** `txHash`，`blockNumber`，`status`，`amount`（wei）

### 提取老虎机分红：**
`fomo3d slot claim --json`  
- 提取老虎机抽奖的累积分红。

## 推荐操作流程：

### 首次使用：
1. `fomo3d setup`：配置钱包和网络。
2. `fomo3d wallet --json`：验证BNB和代币余额。
3. `fomo3d status --json`：检查游戏状态。

### 在主网上购买FOMO代币：
1. `fomo3d token-info --json`：查询代币状态和USDT余额。
2. `fomo3d buy --amount 10000000000000000000 --json`：使用10 USDT购买代币。
3. `fomo3d token-info --json`：确认FOMO代币余额。

### 在主网上出售FOMO代币：
1. `fomo3d token-info --json`：查询FOMO代币余额。
2. `fomo3d sell --amount 1000000000000000000 --json`：出售全部FOMO代币。
3. 或者：`fomo3d sell --percent 5000 --json`：出售50%的代币。

### 玩Fomo3D游戏：
1. `fomo3d status --json`：查看当前轮次状态和倒计时。
2. `fomo3d purchase --shares 1 --json`：开始购买股份。
3. `fomo3d player --json`：查看收益情况。
4. 准备提取收益时：先运行`fomo3d exit --json`，然后运行`fomo3d settle --json`。
5. 如果倒计时归零且你是最后购买者：运行`fomo3d end-round --json`，然后运行`fomo3d settle --json`。

### 玩老虎机：
1. `fomo3d slot status --json`：查看最小/最大投注额和奖金池。
2. `fomo3d slot spin --bet <amount> --json`：进行抽奖。
3. 等待5-10秒，等待VRF回调结果。
4. `fomo3d player --json`：查看是否中奖。

### 获得被动收入（老虎机分红）：
`fomo3d slot deposit --amount <amount> --json`：向老虎机充值代币（充值操作不可撤销）。
5. 定期使用`fomo3d slot claim --json`：提取分红。

## 全局参数：
| 参数 | 说明 |
|------|-------------|
| `--json` | 以JSON格式输出（用于程序化访问） |
| `--network testnet` | `mainnet` | 指定使用测试网或主网 |
| `--help` | 显示帮助信息 |
| `--version` | 显示版本信息 |

## 网络信息：
| 网络 | 链路ID | Fomo3D钻石状态 | 老虎机钻石状态 | FOMO代币状态 |
|---------|----------|----------------|--------------|------------|
| BSC Testnet | 97 | `0x22E309c31Bed932afB505308434fB774cB2B23a6` | `0x007813509FA42B830db82C773f0Dd243fBEbF678` | `0x57e3a4fd1fe7f837535ea3b86026916f8c7d5d46` |
| BSC Mainnet | 56 | `0x062AfaBEA853178E58a038b808EDEA119fF5948b` | `0x6eB59fFEc7CC639DFF4238D09B99Ea4c9150156E` | `0x13f26659398d7280737ffc9aba3d4f3cf53b7777` |

## 交易合约（仅限主网）：
| 合约 | 地址 | 功能 |
|----------|---------|---------|
| FlapSkill | `0x03a9aeeb4f6e64d425126164f7262c2a754b3ff9` | 代币买卖（自动路由内盘/外盘） |
| USDT (BSC) | `0x55d398326f99059fF775485246999027B3197955` | 支付媒介 |
| FLAP Portal | `0xe2cE6ab80874Fa9Fa2aAE65D277Dd6B8e65C9De0` | 查询代币状态 |