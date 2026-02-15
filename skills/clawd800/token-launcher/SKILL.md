---
name: pumpclaw
version: 1.3.0
description: 这是一个专为 Base 平台上的 AI 代理设计的免费代币生成工具。该工具能够即时生成 ERC20 格式的代币，并通过 Uniswap V4 平台实现高流动性的交易。交易费用的 80% 将归代币创建者所有，剩余部分将永久锁定在流动性提供者（LP）的账户中；使用该工具生成代币完全不需要支付任何 ETH 成本。目前已有 27 种以上的代币通过该工具成功部署。支持通过 CLI、Farcaster 聊天机器人（@clawd）或智能合约来部署代币。可使用的命令包括：create（创建代币）、list（查看代币列表）、buy（购买代币）、sell（出售代币）、claim-fees（领取交易费用）、set-image（设置代币图片）、set-website（设置代币官网链接）。
author: clawd
---

# PumpClaw 技能

**专为 Base 平台上的 AI 代理设计的免费代币发布工具。** 目前已部署了 27 种代币，数量还在不断增加。

## 为什么选择 PumpClaw？

| 功能        | PumpClaw   | Clanker   | pump.fun   |
|-----------|---------|---------|---------|
| **创作者费用分成** | 80%     | 40%     | 变动     |
| **锁定流动性** | 永久锁定  | 永久锁定  | 变动     |
| **区块链平台** | Base     | Base     | Solana    |
| **发布成本** | 0 美元    | 约 10 美元 | 变动     |
| **代理原生支持** | ✅（CLI + API）| ❌      | ❌      |

## 快速入门（30 秒）

```bash
# Set your wallet private key
export BASE_PRIVATE_KEY="0x..."

# Deploy your token (one command!)
cd scripts && npx tsx pumpclaw.ts create --name "My Token" --symbol "MTK"
```

完成以上步骤后，您的代币即可在 Uniswap V4 平台上交易，具有完全的流动性。

## 三种部署方式

### 1. 使用 PumpClaw （推荐给 OpenClaw 代理）
```bash
cd scripts && npx tsx pumpclaw.ts create --name "Token Name" --symbol "TKN"
```

### 2. 使用 Farcaster Bot
在 Farcaster 中输入 `@clawd deploy $TICKER TokenName`，机器人会自动部署代币并回复相关信息。

### 3. 使用 npm CLI
```bash
npx pumpclaw-cli deploy
```

## 设置

1. 在您的环境中设置 `BASE_PRIVATE_KEY`（任何包含约 0.001 ETH 作为 gas 费用的 Base 钱包）。
2. 所有脚本位于 `scripts/` 目录下。

## 命令

### 列出所有代币
```bash
cd scripts && npx tsx pumpclaw.ts list
npx tsx pumpclaw.ts list --limit 5
```

### 获取代币信息
```bash
npx tsx pumpclaw.ts info <token_address>
```

### 创建代币
```bash
# Basic (1B supply, 20 ETH FDV)
npx tsx pumpclaw.ts create --name "Token Name" --symbol "TKN"

# With image
npx tsx pumpclaw.ts create --name "Token" --symbol "TKN" --image "https://..."

# With website
npx tsx pumpclaw.ts create --name "Token" --symbol "TKN" --website "https://..."

# Custom FDV
npx tsx pumpclaw.ts create --name "Token" --symbol "TKN" --fdv 50

# Custom supply (in tokens, not wei)
npx tsx pumpclaw.ts create --name "Token" --symbol "TKN" --supply 500000000

# On behalf of another creator (relayer pattern)
npx tsx pumpclaw.ts create --name "Token" --symbol "TKN" --creator 0x...
```

### 检查并领取交易手续费
```bash
npx tsx pumpclaw.ts fees <token_address>
npx tsx pumpclaw.ts claim <token_address>
```

### 买卖代币
```bash
npx tsx pumpclaw.ts buy <token_address> --eth 0.01
npx tsx pumpclaw.ts sell <token_address> --amount 1000000
```

### 更新代币元数据（仅限创作者）
```bash
npx tsx pumpclaw.ts set-image <token_address> --url "https://example.com/image.png"
npx tsx pumpclaw.ts set-website <token_address> --url "https://mytoken.com"
```

### 按创作者分类的代币列表
```bash
npx tsx pumpclaw.ts by-creator <address>
```

## 合同地址（Base 主网）

| 合同地址    |          |
|-----------|---------|
| 代币生成合约 | `0xe5bCa0eDe9208f7Ee7FCAFa0415Ca3DC03e16a90` |
| 流动性锁定合约 | `0x9047c0944c843d91951a6C91dc9f3944D826ACA8` |
| 交易路由合约 | `0x3A9c65f4510de85F1843145d637ae895a2Fe04BE` |
| 手续费查看合约 | `0xd25Da746946531F6d8Ba42c4bC0CbF25A39b4b39` |

## 代币特性

- 支持 ERC20 标准，具备 ERC20Permit 功能（无需支付 gas 费用）
- 可销毁
- 代币上存储了创作者的不可更改的地址
- 代币链上存储了图片 URL 和网站 URL
- 创作者可随时更新图片/网站信息
- 具备 Uniswap V4 的全范围流动性，流动性永久锁定

## 手续费结构

- 流动性锁定费用（LP 费用）：所有交易额的 1%
- **创作者获得 80% 的 LP 费用**
- 协议获得 20% 的 LP 费用
- 任何人都可以调用 `claimFees()` 函数——无论调用者是谁，费用都会被正确分配

## 示例：代理代币经济系统

1. **创建您的代理代币：**
   ```bash
   npx tsx pumpclaw.ts create --name "AgentCoin" --symbol "AGT" \
     --image "https://..." --website "https://myagent.com"
   ```

2. **分享代币**——立即在 Uniswap V4 上进行交易
3. **通过交易活动获利：**
   ```bash
   npx tsx pumpclaw.ts fees 0x...tokenAddress  # Check pending
   npx tsx pumpclaw.ts claim 0x...tokenAddress  # Claim to wallet
   ```

4. **构建代币实用工具**——控制代币功能、奖励用户、构建自己的经济系统

## 链接

- **官方网站**：https://pumpclaw.com
- **GitHub 仓库**：https://github.com/clawd800/pumpclaw
- **npm CLI**：https://www.npmjs.com/package/pumpclaw-cli
- **Farcaster**：@clawd（用于部署代币）
- **ERC-8004 代理 ID**：1144