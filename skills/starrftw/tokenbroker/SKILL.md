---
name: tokenbroker
description: AI代理技能：用于GitHub项目分析及nad.fun代币的发布。该技能可分析代码仓库，生成代币的相关信息（如标识符、宣传材料），并最终在nad.fun平台上发布这些代币。
version: 1.01
metadata:
  tags: monad, nadfun, token, launch, github, memecoin, autonomous
---

# SKILL.md – TokenBroker 技能集

## 安全性与数据隐私

### 仅限本地存储
- 所有凭据（GitHub 令牌、私钥、API 密钥）均存储在 `.env` 文件中（仅限本地）
- 任何凭据都不会被传输到外部服务器（除非是前往预定的端点，如 GitHub API、nad.fun API 或 Monad RPC）
- 该技能完全在您的本地环境中运行

### `.env` 文件的生成
- 安装向导会在您的本地机器上生成一个 `.env` 文件
- 该文件**永远不会被提交到版本控制系统中**（被 Git 忽略）
- 您可以随时查看和编辑该文件

### 凭据的使用范围
- `GITHUB_TOKEN`：仅用于通过 GitHub API 获取公共仓库数据
- `PRIVATE_KEY`：仅用于 EVM 交易签名（绝不会以明文形式暴露）
- `BUILDER_ID`：用于 A2A 协议的本地标识符
- `NAD_FUN_API_KEY`：仅用于 nad.fun 的令牌创建 API

### 测试网模式
- 为确保安全，默认情况下该技能运行在**测试网**上
- 主网模式需要手动配置
- 签署交易前请务必仔细检查交易内容

---

**这款 AI 代理技能专为 memecoin 设计，可在 nad.fun 上运行。** 它能够分析 GitHub 项目，生成令牌元数据，并直接在 nad.fun 的绑定曲线上进行令牌发行。

## 什么是 TokenBroker？

TokenBroker 是一款专为 AI 代理设计的**完整的 memecoin 发行解决方案**：
1. **分析** GitHub 项目，筛选出适合制作模因的项目
2. **生成** 令牌名称、代码标识符、描述以及营销内容
3. **在 nad.fun 上发行** 令牌（包括图像、元数据等）
4. **利用 X、Telegram 和 Discord 等平台进行推广**

## 何时使用该技能

### TokenBroker 的功能包括：
- 分析 GitHub 仓库并进行评分
- 生成令牌的名称、代码标识符和描述
- 生成适合模因风格的图像
- 集成 nad.fun API（用于上传文件、生成令牌盐值）
- 创建营销内容（通过 X、Telegram 和 Discord 等平台发布）

### 不包含的功能
- 钱包私钥管理（由宿主负责）
- 超出 nad.fun 绑定曲线的链上交易

## 架构（tokenbroker/src/generators/）

```
generators/
├── identity.ts     # Token name, ticker, description generation
├── reasoning.ts    # Investment thesis, narrative creation
├── promo.ts        # X threads, Telegram, Discord content
├── nadfun.ts       # Nad.fun API: upload image/metadata, mine salt
└── index.ts        # Pipeline orchestrator (generateAll)
```

## 代理的快速入门指南

```typescript
import { generateAll, prepareLaunch } from './generators/index.js';

// 1. Analyze repo and generate all launch assets
const assets = await generateAll({
  repoAnalysis: await analyzeGitHubRepo('https://github.com/user/project')
});

console.log('Token name:', assets.identity.name);
console.log('Ticker:', assets.identity.ticker);
console.log('X Thread:', assets.promo.xThread.tweets);

// 2. Prepare launch on nad.fun (API calls only)
const prepared = await prepareLaunch(assets.identity, 'mainnet');
// -> Returns: { imageUri, metadataUri, salt, saltAddress }

// 3. Deploy on-chain (requires ethers + private key)
// Use deploy.ts module with wallet for on-chain execution
```

## 生成器函数

### generateIdentity(input)
分析仓库信息并生成令牌的标识信息：
```typescript
{
  name: "SWAPPRO",
  ticker: "SWAP", 
  tagline: "The next generation DeFi protocol",
  description: "Full token description...",
  nameReasoning: "How the name was derived"
}
```

### generateReasoning(input)
创建投资分析报告和叙述内容：
```typescript
{
  investmentThesis: "Why this token should exist...",
  problemStatement: "The problem being solved",
  solution: "The proposed solution",
  marketOpportunity: "Market size and opportunity",
  competitiveAdvantage: "Why this wins",
  tokenUtilityRationale: "Token value proposition",
  vision: "Long-term vision"
}
```

### generatePromo(input)
生成营销内容：
```typescript
{
  xThread: { title, tweets: [...], hashtags, mentions },
  telegramPost: { title, content, hasButton, buttonText, buttonUrl },
  discordAnnouncement: { title, content, hasEmbed, embedColor, embedFields },
  tagline: "Marketing tagline",
  elevatorPitch: "One-liner pitch"
}
```

### prepareLaunch(identity, network)
为在 nad.fun 上发行令牌做准备（包括 API 调用）：
```typescript
{
  imageUri: "ipfs://...",
  metadataUri: "ipfs://...", 
  salt: "0x...",
  saltAddress: "0x..."
}
```

## 与 nad.fun 的集成

TokenBroker 直接与 nad.fun API 集成：

| 步骤 | API 端点 | 功能 |
|------|-------------|----------|
| 1 | POST /agent/token/image | 上传令牌图像 |
| 2 | POST /agent/token/metadata | 上传令牌元数据 |
| 3 | POST /agent/salt | 生成令牌盐值 |
| 4 | BondingCurveRouter.create() | 在链上部署令牌 |

### 网络配置
| 网络 | API | RPC |
|---------|-----|-----|
| 测试网 | https://dev-api.nad.fun | https://testnet-rpc.monad.xyz |
| 主网 | https://api.nadapp.net | https://rpc.monad.xyz |

## 安装

```bash
npm install
```

## 配置

```bash
# Network (testnet | mainnet)
NETWORK=mainnet

# GitHub (optional - for repo analysis)
GITHUB_TOKEN=ghp_...
```

## 链上部署

TokenBroker 会准备所有发行所需的数据。若需进行实际的链上部署，请按照以下步骤操作：

```bash
npm install ethers
```

**专为智能代理的未来而设计。** 🦞