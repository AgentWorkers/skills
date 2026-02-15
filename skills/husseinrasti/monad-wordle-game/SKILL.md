---
name: monad-wordle
description: 在Monad区块链上使用$WORDLE代币玩一个5个字母的Wordle游戏。可以通过HTTP API开始游戏、提交猜测以及获取游戏状态。
license: MIT
metadata:
  author: Hussein Rasti
  version: "1.0"
  network:
    chain: Monad Mainnet
    game_contract:
      address: 0x143c5Fd7186470d2d0b1465C10571874c43FD297
    token:
      address: 0xAfcECBd7c43ABbDB10C394ad03C9D88ec8377777
      symbol: WORDLE
  payment:
    cost_per_game: 100 WORDLE
  tags:
    - blockchain
    - game
    - wordle
    - monad
    - erc20
    - onchain-payment
---

# Monad Wordle 技能

该技能使 AI 代理能够在 Monad 主网区块链上玩 5 个字母的 Wordle 游戏。游戏开始前需要支付 100 个 $WORDLE 代币，代理可以通过一个简洁的 HTTP API 提交猜测并获取游戏状态。

**注意：** 所有的代币购买和游戏操作都必须发生在 Monad 主网上。

------------------------------------------------------------------------

### 先决条件

在开始游戏之前，请确保：
1. 钱包已连接到 Monad 主网。
2. 钱包中持有 $MON 代币。
3. 代理需要使用 $MON 在 nad.fun 上购买 $WORDLE 代币。
4. 钱包中至少持有 100 个 $WORDLE 代币。
5. 批准 WordleGame 合同以使用这些 $WORDLE 代币。

------------------------------------------------------------------------

### 执行流程

用户 → 代理
↓
将钱包连接到 Monad 主网
↓
检查 $WORDLE 代币余额
↓
如果余额不足 → 通过 nad.fun 使用 $MON 购买 $WORDLE 代币
↓
批准 WordleGame 合同
↓
调用合约中的 playGame() 函数
↓
接收交易哈希 (txHash)
↓
将 txHash 发送到 /api/game/start
↓
游戏会话创建完成

------------------------------------------------------------------------

### 智能合约详情

**$WORDLE 代币**
- 地址：`0xAfcECBd7c43ABbDB10C394ad03C9D88ec8377777`
- 符号：WORDLE
- 小数位数：18

**WordleGame 合约**
- 地址：`0x143c5Fd7186470d2d0b1465C10571874c43FD297`
- ABI：[gameAbi](https://github.com/husseinrasti/monad-wordle/blob/main/contract/abi.json)

------------------------------------------------------------------------

### 钱包设置

```typescript
const NETWORK = "mainnet"

const CONFIG = {
  mainnet: {
    chainId: 143,
    rpcUrl: "https://monad-mainnet.drpc.org",
    apiUrl: "https://api.nadapp.net",
    DEX_ROUTER: "0x0B79d71AE99528D1dB24A4148b5f4F865cc2b137",
    BONDING_CURVE_ROUTER: "0x6F6B8F1a20703309951a5127c45B49b1CD981A22",
    LENS: "0x7e78A8DE94f21804F7a17F4E8BF9EC2c872187ea",
    CURVE: "0xA7283d07812a02AFB7C09B60f8896bCEA3F90aCE",
    WMON: "0x3bd359C1119dA7Da1D913D1C4D2B7c461115433A",
    V3_FACTORY: "0x6B5F564339DbAD6b780249827f2198a841FEB7F3",
    CREATOR_TREASURY: "0x42e75B4B96d7000E7Da1e0c729Cec8d2049B9731",
  },
}[NETWORK]
```

### 基本设置

```typescript
import { createPublicClient, createWalletClient, http } from "viem"
import { privateKeyToAccount } from "viem/accounts"

const chain = {
  id: CONFIG.chainId,
  name: "Monad",
  nativeCurrency: { name: "MON", symbol: "MON", decimals: 18 },
  rpcUrls: { default: { http: [CONFIG.rpcUrl] } },
}

const account = privateKeyToAccount(process.env.PRIVATE_KEY as `0x${string}`)

const publicClient = createPublicClient({
  chain,
  transport: http(CONFIG.rpcUrl),
})

const walletClient = createWalletClient({
  account,
  chain,
  transport: http(CONFIG.rpcUrl),
})
```

------------------------------------------------------------------------

### NadFun 集成指南
Monad 区块链的代币交易平台，支持绑定曲线（bonding curves）功能。您可以在这里交易代币、创建自己的代币或监控事件——所有操作均通过 viem 完成。

### 交易 - 购买
仅使用 viem 进行 nad.fun 的绑定曲线和 DEX 相关交易。

### 网络配置

| 网络 | LENS                                       | BONDING_CURVE_ROUTER                       | DEX_ROUTER                                 |
| ------- | ------------------------------------------ | ------------------------------------------ | ------------------------------------------ |
| 主网 | 0x7e78A8DE94f21804F7a17F4E8BF9EC2c872187ea | 0x6F6B8F1a20703309951a5127c45B49b1CD981A22 | 0x0B79d71AE99528D1dB24A4148b5f4F865cc2b137 |

智能合约 ABI 信息请参阅：https://nad.fun/abi.md

### 购买代币

使用 $MON 代币购买 $WORDLE 代币。

```typescript
// 1. Get quote
const [router, amountOut] = await publicClient.readContract({
  address: CONFIG.LENS,
  abi: lensAbi,
  functionName: "getAmountOut",
  args: [wordleToken, parseEther(monAmount), true],
})

// 2. Calculate slippage (1%)
const amountOutMin = (amountOut * 99n) / 100n
const deadline = BigInt(Math.floor(Date.now() / 1000) + 300)

// 3. Execute
const callData = encodeFunctionData({
  abi: routerAbi,
  functionName: "buy",
  args: [{ amountOutMin, token: wordleToken, to: account.address, deadline }],
})

const hash = await walletClient.sendTransaction({
  account,
  to: router,
  data: callData,
  value: parseEther(monAmount),
  chain,
})

await publicClient.waitForTransactionReceipt({ hash })
```

**购买参数**：
- `amountOutMin`：最低购买数量
- `token`：代币类型
- `to`：接收代币的地址
- `deadline`：交易截止时间

------------------------------------------------------------------------

### 支付流程

要在 Monad 主网上玩游戏，代理需要按照以下步骤操作：
1. 使用钱包连接到 Monad 主网。
2. 购买至少 100 个 $WORDLE 代币。
3. 批准并支付：调用 WordleGame 合同中的 playGame() 函数。
4. 游戏开始后：将交易哈希发送到 `/api/game/start` 端点。

------------------------------------------------------------------------

### 支付验证规则

API 必须验证以下内容：
- 交易是在 Monad 主网上执行的。
- 交易接收方（tx.to）必须是 WordleGame 合同的地址。
- 交易的代币类型必须是 ERC20 标准的 $WORDLE 代币。
- 支付金额必须达到 100 个 $WORDLE。
- 确保已触发 GamePlayed 事件。
- 交易哈希不能已被使用过。
- 交易发送方必须与提供的钱包地址一致。

### 防止重放攻击

系统必须防止任何重放攻击（replay attacks）。

------------------------------------------------------------------------

### API 端点

所有 API 端点都位于应用程序的基地址（base URL）上。

### 基地址

```
https://wordle.nadnation.xyz
```

### 1. 开始新游戏

**端点：** `POST /api/game/start`

**描述：** 在支付验证通过后，启动一个新的 Wordle 游戏。

**请求体：**
```json
{
  "address": "0x...",
  "txHash": "0x..."
}
```

**参数：**
- `address`（字符串，必填）：玩家的钱包地址
- `txHash`（字符串，必填）：证明已向 WordleGame 合同支付 100 个 $WORDLE 代币的交易哈希

**响应：**
```json
{
  "gameId": "k17abc123...",
  "message": "Game started successfully"
}
```

**示例：**
```bash
curl -X POST https://wordle.nadnation.xyz/api/game/start \
  -H "Content-Type: application/json" \
  -d '{
    "address": "0x1234567890abcdef1234567890abcdef12345678",
    "txHash": "0xabcdef1234567890abcdef1234567890abcdef1234567890abcdef1234567890"
  }'
```

### 2. 提交猜测

**端点：** `POST /api/game/guess`

**描述：** 为当前游戏提交一个 5 个字母的猜测词。

**请求体：**
```json
{
  "gameId": "k17abc123...",
  "guess": "crane"
}
```

**参数：**
- `gameId`（字符串，必填）：从开始游戏时返回的游戏 ID
- `guess`（字符串，必填）：一个 5 个字母的单词（必须存在于单词字典中）

**响应：**
```json
{
  "result": ["correct", "present", "absent", "absent", "present"],
  "status": "playing",
  "guessesRemaining": 5
}
```

**示例：**
```bash
curl -X POST https://wordle.nadnation.xyz/api/game/guess \
  -H "Content-Type: application/json" \
  -d '{
    "gameId": "k17abc123...",
    "guess": "crane"
  }'
```

### 3. 获取游戏状态

**端点：** `GET /api/game/state?gameId={gameId}`

**描述：** 获取当前游戏的状态。

**查询参数：**
- `gameId`（字符串，必填）：游戏 ID

**响应：**
```json
{
  "gameId": "k17abc123...",
  "status": "playing",
  "guesses": ["crane", "slant"],
  "results": [
    ["correct", "present", "absent", "absent", "present"],
    ["correct", "absent", "present", "absent", "correct"]
  ],
  "guessesRemaining": 4,
  "word": "APPLE" // Only revealed if status is 'won' or 'lost'
}
```

**示例：**
```bash
curl "https://wordle.nadnation.xyz/api/game/state?gameId=k17abc123..."
```

### 4. 查看排行榜

**端点：** `GET /api/game/leaderboard`

**描述：** 查看排行榜上的前几名玩家。

**响应：**
```json
[
  {
    "rank": 1,
    "address": "0x1234...5678",
    "gamesPlayed": 50,
    "gamesWon": 45,
    "winRate": 90,
    "currentStreak": 10,
    "maxStreak": 15
  }
]
```

### 游戏策略

### 推荐的玩法：
1. **从包含常见元音和辅音的单词开始**：
   - 如 “CRANE”, “SLATE”, “TRACE”, “ADIEU”, “AUDIO”。
2. **分析反馈信息**：
   - 绿色（正确）：字母位置正确。
   - 黄色（存在）：字母存在但位置错误。
   - 灰色（不存在）：字母不在单词中。

------------------------------------------------------------------------

### 错误处理

### 常见错误：
1. **交易哈希已被使用**：`{"error": "Transaction hash already used"}`
2. **未找到 GamePlayed 事件**：`{"error": "GamePlayed event not found"}`
3. **输入的单词无效**：`{"error": "Not a valid word"}`
4. **猜测长度不正确**：`{"error": "Guess must be exactly 5 letters"}`
5. **游戏已结束**：`{"error": "Game is already finished"}`