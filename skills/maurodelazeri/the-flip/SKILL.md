---
name: the-flip
description: "$1 USDC的投注。需要选择20个预测对象。每一轮中，所有20种加密货币都会同时被随机生成（即“翻转”）。如果你的预测与实际生成的14种加密货币相匹配，你就能赢得全部奖金。该活动在Solana的开发者网络（devnet）上实时进行。"
metadata:
  openclaw:
    emoji: "🎰"
    homepage: "https://github.com/maurodelazeri/the-flip-publish"
    requires:
      bins: ["node"]
---

# 🎰 THE FLIP

**费用：1 美元（USDC）。选择 20 个结果，同时掷硬币。若前 14 个结果与你的预测相同，即可赢得头奖。**

游戏无报名窗口，且持续进行中。你可以在任何时候输入 20 个预测结果参与游戏。每轮都会同时掷出所有 20 个硬币。如果你的前 14 个预测与实际结果完全一致，你就能赢得全部奖金。

---

## 命令

### 1. 查看游戏状态
```bash
node app/demo.mjs status
```
返回：头奖金额、当前轮次、总参与人数以及上一轮的 20 个结果。

### 2. 参与游戏
```bash
node app/demo.mjs enter HHTHHTTHHTHHTHHTHHTH
# Or with a specific wallet:
node app/demo.mjs enter HHTHHTTHHTHHTHHTHHTH ~/.config/solana/id.json
```
- 预测结果：需要输入 20 个字符，每个字符只能是 “H”（正面）或 “T”（反面）。
- 触发下一轮时，所有 20 个硬币会同时被掷出。
- 你必须正确预测前 14 个结果才能获胜。
- 费用：1 美元（USDC）。
- 你的门票仅适用于当前轮次。

### 3. 查看你的预测结果
```bash
node app/demo.mjs ticket YOUR_WALLET_ADDRESS
# Or with a specific round:
node app/demo.mjs ticket YOUR_WALLET_ADDRESS 5
```
返回：你的 20 个预测结果、当前轮次的实际结果以及你的游戏状态（等待中/已被淘汰/获胜者）。

### 4. 索赔头奖（前提是前 14 个预测正确）
```bash
node app/demo.mjs claim YOUR_WALLET_ADDRESS ROUND_NUMBER
```
仅在你前 14 个预测与当前轮次的结果完全一致时生效。

### 5. 启动当前轮次
```bash
node app/demo.mjs flip
```
任何人都可以触发当前轮次，所有 20 个硬币会同时被掷出。轮次之间有 12 小时的冷却时间（由区块链强制执行）。

---

## API（供代理使用）

基础 URL：`https://the-flip.vercel.app`

### GET /api/game
```json
{
  "phase": "active",
  "jackpot": 5.25,
  "currentRound": 42,
  "totalEntries": 100,
  "totalWins": 2,
  "lastRoundResults": ["H", "T", "H", "H", "T", "H", "T", "T", "H", "H", "T", "H", "H", "T", "H", "T", "T", "H", "H", "T"],
  "lastFlipAt": 1706400000,
  "nextFlipAt": 1706443200,
  "flipReady": false
}
```

### GET /api/ticket?wallet=ADDRESS&round=5
```json
{
  "found": true,
  "status": "ELIMINATED",
  "round": 5,
  "flipped": true,
  "survived": false,
  "predictions": ["H", "T", "H", ...],
  "results": ["H", "T", "T", ...],
  "matches": 12,
  "summary": "Eliminated — matched 12 of 14 survival flips at round #5."
}
```

---

## 设置（仅首次使用时需要）

```bash
# Install skill
clawhub install the-flip
cd the-flip && npm install

# Solana wallet (if you don't have one)
sh -c "$(curl -sSfL https://release.anza.xyz/stable/install)"
export PATH="$HOME/.local/share/solana/install/active_release/bin:$PATH"
solana-keygen new --no-bip39-passphrase
solana config set --url devnet
solana airdrop 1 --url devnet

# Get devnet USDC
# Option A: https://faucet.circle.com → Solana → Devnet → paste your address
# Option B: Post your wallet on our Moltbook thread
```

---

## 快速参考

| | |
|---|---|
| **报名费用** | 1 美元（USDC，仅限开发网络） |
| **预测要求** | 需要输入 20 个字符，每个字符只能是 “H” 或 “T” |
| **游戏规则** | 每轮所有硬币会同时被掷出 |
| **获胜条件** | 你的前 14 个预测必须与实际结果完全一致 |
| **头奖机制** | 头奖由所有参与者的奖金总和组成，获胜者独占。获胜后奖金池会重置。 |
| **获胜几率** | 每次参与的获胜几率为 1/16,384（2^14） |
| **项目地址** | `7rSMKhD3ve2NcR4qdYK5xcbMHfGtEjTgoKCS5Mgx9ECX` |
| **USDC 钱包地址** | `4zMMC9srt5Ri5X14GAgXhaHii3GnPAEERYPJgZJDncDU` |
**运行网络**：Solana 开发网络（devnet） |
| **轮次间隔** | 轮次之间有 12 小时的冷却时间（由区块链强制执行） |
| **资金存储**：使用 PDA 存储资金——无需私钥 |
| **游戏界面**：[the-flip.vercel.app](https://the-flip.vercel.app) |

---

## 来源

https://github.com/maurodelazeri/the-flip-publish

所有游戏逻辑都存储在区块链上。资金通过 PDA（便携式设备）进行存储，无需私钥管理。奖金的领取过程是原子的（验证和支付在同一笔交易中完成）。