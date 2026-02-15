---
name: the-flip
description: "**规则说明：**  
1. 玩家需要投入 1 美元（USDC）才能参与游戏。  
2. 游戏包含 14 次随机硬币翻转（coin flips）。  
3. 如果玩家能连续 14 次都猜中硬币的翻转结果，就能赢得全部奖金（jackpot）。  
4. 该游戏在 Solana 的开发者网络（devnet）上实时进行，玩家可以随时加入。  

**游戏详情：**  
- **游戏费用：** 1 美元（USDC）  
- **游戏次数：** 14 次  
- **获胜条件：** 连续 14 次猜中硬币翻转结果  
- **游戏平台：** Solana 开发者网络（devnet）  
- **游戏特点：** 实时游戏，玩家可随时参与"
metadata:
  openclaw:
    emoji: "🎰"
    homepage: "https://github.com/maurodelazeri/the-flip-publish"
    requires:
      bins: ["node"]
---

# 🎰 THE FLIP

**费用：1 美元（USDC）。进行 14 次硬币翻转。如果全部预测正确，即可赢得全部奖金。**

游戏没有轮次限制，也没有报名窗口；游戏会持续进行。你可以随时参与，你的“门票”将跟随接下来的 14 次全球性硬币翻转。获胜者将获得全部奖金。

---

## 命令

### 1. 查看游戏状态
```bash
node app/demo.mjs status
```
返回：奖金总额、全球翻转次数、总参与人数以及最近的翻转结果。

### 2. 参与游戏
```bash
node app/demo.mjs enter HHTHHTTHHTHHTH
# Or with a specific wallet:
node app/demo.mjs enter HHTHHTTHHTHHTH ~/.config/solana/id.json
```
- 预测结果：需要输入 14 个字符，每个字符只能是 “H”（正面）或 “T”（反面）
- 费用：1 美元（USDC）
- 你的“门票”将从当前的全球翻转次数开始生效。

### 3. 查看你的“门票”结果
```bash
node app/demo.mjs ticket YOUR_WALLET_ADDRESS
# Or with a specific start flip:
node app/demo.mjs ticket YOUR_WALLET_ADDRESS 42
```
返回：你的预测结果、目前的翻转情况以及你的游戏状态（存活/已被淘汰/获胜）。

### 4. 索赔奖金（如果全部预测正确）
```bash
node app/demo.mjs claim YOUR_WALLET_ADDRESS START_FLIP
```
仅在你全部预测与实际翻转结果完全匹配时生效。

### 5. 继续进行游戏（任何人都可以操作）
```bash
node app/demo.mjs flip
```
执行下一次硬币翻转。无需权限——任何人都可以调用该命令。

---

## API（供代理使用）

基础 URL：`https://the-flip.vercel.app`

### GET /api/game
```json
{
  "phase": "active",
  "jackpot": 5.25,
  "globalFlip": 42,
  "totalEntries": 100,
  "totalWins": 2,
  "recentFlips": ["H", "T", "H", "H", "T", ...]
}
```

### GET /api/ticket?wallet=ADDRESS&startFlip=42
```json
{
  "found": true,
  "status": "ALIVE",
  "score": 5,
  "predictions": ["H", "T", "H", ...],
  "flips": [
    {"index": 0, "predicted": "H", "actual": "H", "match": true, "revealed": true},
    ...
  ]
}
```

---

## 设置（仅首次使用）

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
| **参与费用** | 1 美元（USDC，仅限开发网络 devnet） |
| **预测要求** | 需要输入 14 个字符，每个字符为 “H” 或 “T” |
| **翻转过程** | 持续进行——无需权限，任何人都可以触发翻转 |
| **奖金分配** | 所有参与者的奖金的 99% 归获胜者；获胜后奖金池将重置 |
| **中奖几率** | 每次参与的中奖几率为 1/16,384 |
| **项目地址** | `7rSMKhD3ve2NcR4qdYK5xcbMHfGtEjTgoKCS5Mgx9ECX` |
| **USDC 钱包地址** | `4zMMC9srt5Ri5X14GAgXhaHii3GnPAEERYPJgZJDncDU` |
| **运行网络** | Solana 开发网络（devnet） |
**资金存储方式** | 使用 PDA（Personal Digital Assistant）存储资金——无需私钥 |
| **游戏界面** | [the-flip.vercel.app](https://the-flip.vercel.app) |

---

## 来源代码

https://github.com/maurodelazeri/the-flip-publish

所有游戏逻辑都存储在链上；资金通过 PDA（Personal Digital Assistant）进行存储，无需私钥管理。奖金的领取过程是原子的（验证和支付在同一笔交易中完成）。