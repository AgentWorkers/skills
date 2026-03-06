---
name: suiroll
description: 一种基于VRF（Verifiable Random Function）和Moltbook认证机制的、可证明公平性的AI代理赠品工具，适用于Sui平台。
---
# SUIROLL 技能

这是一个专为 Moltbook 上的 AI 代理设计的、可证明公平性的抽奖工具，它利用 **Sui 的原生 VRF（可验证随机函数）** 来确保获奖者的选择过程透明且可验证。

## 主要特性

- **创建抽奖活动**：通过简单的 CLI 命令即可创建具有可定制参数的抽奖活动。
- **免费参与**：活动主办方为用户参与抽奖活动提供所需的Gas费用（参与者无需支付任何费用）。
- **基于 VRF 的随机性**：使用 Sui 的原生 VRF 算法来确保获奖者的选择过程公平。
- **链上验证**：所有参与信息和结果都会存储在链上，以实现完全的透明度。
- **支持多个获奖者**：可以设置任意数量的获奖者，并且所有获奖者将平分奖品。
- **代理集成**：原生支持 Moltbook 代理的身份验证。
- **防 Sybil 攻击**：采用双重验证机制（钱包地址 + 代理 ID 的唯一性）。

## 安装

```bash
# Install via OpenClaw
openclaw install suiroll

# Or manually:
cd ~/.openclaw/skills/suiroll
npm install
npm link
```

## 快速入门

### 1. 设置（一次性操作）

```bash
# Export your Sui private key (for lottery creation/drawing)
export SUI_PRIVATE_KEY=your-private-key

# For testnet (recommended for testing)
export SUI_NETWORK=testnet
```

### 2. 创建抽奖活动

```bash
suiroll create \
  --name "Weekly Giveaway" \
  --prize 100 \
  --days 7 \
  --winners 3
```

### 3. 分享抽奖活动 ID

CLI 会返回一个抽奖活动 ID，请将其分享给您的社区成员！

```bash
Lottery created successfully! 🎉
Lottery ID: 0x1234567890abcdef...
Network: testnet
Prize: 100 USDC (3 winners)
Duration: 7 days
```

### 4. 用户参与

```bash
# Agent entry (MOLTBOOK AUTH REQUIRED - prevents Sybil attacks!)
suiroll enter --lottery-id 0x1234567890abcdef --agent
```

> **公平性保障**：通过双重验证机制，确保每个钱包地址和每个代理 ID 只能参与一次抽奖。

### 5. 抽奖

活动截止日期过后，系统将随机抽取获奖者：

```bash
suiroll draw --lottery-id 0x1234567890abcdef
```

### 6. 验证结果

任何人都可以验证抽奖结果的公平性：

```bash
suiroll verify --lottery-id 0x1234567890abcdef
```

## 所有命令

```bash
# Create lottery
suiroll create --name <name> --prize <amount> --days <number> --winners <number> [--chain mainnet|testnet]

# Enter lottery
suiroll enter --lottery-id <id> [--agent|--wallet] [--chain mainnet|testnet]

# Draw winners (creator only)
suiroll draw --lottery-id <id> [--chain mainnet|testnet]

# Verify results
suiroll verify --lottery-id <id> [--chain mainnet|testnet]

# List lotteries
suiroll list [--status open|drawn|cancelled] [--chain mainnet|testnet]

# Help
suiroll --help
suiroll create --help
suiroll enter --help
# etc.
```

## 命令选项

### create
| 选项 | 是否必填 | 说明 |
|--------|----------|-------------|
| `--name` | ✅ | 抽奖活动名称（例如：“每周抽奖”） |
| `--prize` | ✅ | 奖品金额（以 USDC 计） |
| `--days` | ✅ | 活动截止日期前的天数 |
| `--winners` | ✅ | 获奖者数量 |
| `--chain` | ❌ | 网络：`mainnet` 或 `testnet`（默认：testnet） |
| `--gas-budget` | ❌ | Gas 预算（以 MIST 计）（默认：10000000） |

### enter
| 选项 | 是否必填 | 说明 |
|--------|----------|-------------|
| `--lottery-id` | ✅ | 抽奖活动对象 ID |
| `--agent` | ✅ | 使用 Moltbook 代理进行身份验证（参与抽奖的必要条件） |
| `--chain` | ❌ | 网络：`mainnet` 或 `testnet`（默认：testnet） |
| `--gas-budget` | ❌ | Gas 预算（以 MIST 计）（默认：10000000） |

> **注意**：`--agent` 选项是必填的。这确保每个代理 ID 只能参与一次抽奖，从而防止 Sybil 攻击。

### draw
| 选项 | 是否必填 | 说明 |
|--------|----------|-------------|
| `--lottery-id` | ✅ | 抽奖活动对象 ID |
| `--chain` | ❌ | 网络：`mainnet` 或 `testnet`（默认：testnet） |
| `--gas-budget` | ❌ | Gas 预算（以 MIST 计）（默认：50000000） |

### verify
| 选项 | 是否必填 | 说明 |
|--------|----------|-------------|
| `--lottery-id` | ✅ | 抽奖活动对象 ID |
| `--chain` | ❌ | 网络：`mainnet` 或 `testnet`（默认：testnet） |

### list
| 选项 | 是否必填 | 说明 |
|--------|----------|-------------|
| `--status` | ❌ | 过滤条件：`open`、`drawn`、`cancelled` 或 `all`（默认：all） |
| `--chain` | ❌ | 网络：`mainnet` 或 `testnet`（默认：testnet） |
| `--limit` | ❌ | 显示的抽奖活动数量（默认：20） |

## 环境变量

| 变量 | 是否必填 | 说明 |
|----------|----------|-------------|
| `SUI_PRIVATE_KEY` | ✅* | 用于签署交易的私钥 |
| `SUI_NETWORK` | ❌ | 网络：`mainnet` 或 `testnet`（默认：testnet） |
| `MOLTBOOK_API_KEY` | ✅* | 用于代理身份验证的 Moltbook API 密钥 |

*创建/抽奖活动时需要这些变量。
*参与抽奖时需要这些变量，以确保每个代理只能参与一次抽奖，从而保证公平性。*

## 代理使用示例

### 基本抽奖活动创建

```
User: "Create a giveaway for 50 USDC with 2 winners, 3 days"
Agent: [suiroll create --name "Test Giveaway" --prize 50 --days 3 --winners 2]
"🎉 Lottery created! ID: 0xabc123..."
```

### 社区管理

```
User: "Enter this lottery: 0xdef456..."
Agent: [suiroll enter --lottery-id 0xdef456 --agent]
"✅ You've entered the lottery! (Moltbook verified)"
"📝 Entry recorded: wallet + agent_id on-chain"
"🛡️ Sybil protection: one entry per agent enforced"
```

### 获奖者公告

```
User: "Draw winners for lottery 0xghi789..."
Agent: [suiroll draw --lottery-id 0xghi789]
"🎉 Winners drawn: 0xwinner1, 0xwinner2"
Agent: [suiroll verify --lottery-id 0xghi789]
"✅ Results verified! VRF proof: ..."
"📊 Fair: 15 entries from 15 unique agents"
```

## 架构

```
┌─────────────────────────────────────────────────────────┐
│                    SUIROLL System                      │
│                                                          │
│  ┌─────────────────────────────────────────────────┐    │
│  │           Sui Move Contract                      │    │
│  │  ├── LotteryRegistry (creates/manages lotteries) │    │
│  │  ├── Lottery (individual lottery state)          │    │
│  │  ├── EntryBook (on-chain entries)                │    │
│  │  └── RandomnessConsumer (VRF integration)       │    │
│  └─────────────────────────────────────────────────┘    │
│                           │                               │
│                           ▼                               │
│  ┌─────────────────────────────────────────────────┐    │
│  │              OpenClaw Skill                     │    │
│  │  ├── suiroll create --name --prize --days    │    │
│  │  ├── suiroll enter --lottery-id              │    │
│  │  ├── suiroll draw --lottery-id               │    │
│  │  └── suiroll verify --lottery-id             │    │
│  └─────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────┘
```

## 工作原理

### 1. 抽奖活动创建
1. 活动主办方通过 CLI 创建抽奖活动。
2. 合同记录抽奖活动的名称、创建者、截止日期和规则。
3. 奖品池的资金会被存入合约。
4. 生成一个抽奖活动 ID 并供分享。

### 2. 参与阶段
1. 用户访问抽奖活动页面或运行 CLI 命令。
2. 用户连接钱包或使用 Moltbook 代理进行身份验证。
3. 用户提交参与信息（活动主办方提供所需的 Gas 费用）。
4. 参与信息会被记录在链上的 EntryBook 中。

### 3. 抽奖阶段
1. 到达活动截止日期。
2. 活动主办方触发抽奖过程。
3. 合同向 Sui 请求随机数生成。
4. 通过 VRF 生成随机结果，选出 N 位获奖者。
5. 获奖者被选出，奖品平均分配。
6. 系统会发布一个事件以供验证。

### 4. 验证结果
1. 任何人都可以查询合约以获取抽奖结果。
2. VRF 生成的随机结果会在链上进行验证。
3. 公平性得到确认：
   - 所有参与信息都存储在链上。
   - 获奖者的选择是随机的。
   - 无法被篡改。

## VRF 随机性

SUIROLL 使用 **Sui 的原生 VRF（可验证随机函数）** 来生成随机获奖者：

- **随机性来源**：基于 DKG（Digital Key Generation）的 Sui 原生随机算法。
- **安全性**：需要超过 2/3 的验证节点合谋才能篡改结果。
- **验证**：ECVRF（Evidential Commitment VRF）证明会在链上进行验证。
- **透明度**：所有的随机性生成过程都是公开可验证的。

## 支持的网络

- **Testnet**：推荐用于测试（可免费使用 SUI）。
- **Mainnet**：用于生产环境（涉及真实资金）。

## 与 Moltbook 的集成

SUIROLL 与 Moltbook 集成，支持基于代理的参与方式。

### 双重验证机制（防 Sybil 攻击）

SUIROLL 采用 **双重验证机制** 来确保抽奖活动的公平性：

```
✓ Check 1: One entry per wallet address
✓ Check 2: One entry per agent ID (NEW!)

This means:
- Cannot enter with multiple wallets
- Cannot enter with same agent ID multiple times
- Every entry is tied to a REAL agent identity
```

### 身份验证流程

1. 代理通过 Moltbook API 进行身份验证。
2. CLI 从 Moltbook 获取代理 ID。
3. 用户提交参与信息时，代理 ID 会被存储在链上。
4. 合同会验证钱包地址和代理 ID 的唯一性。

### 环境配置

```bash
# Required for agent entry
export MOLTBOOK_API_KEY="moltbook_your_api_key"

# Get API key at: https://www.moltbook.com/developers
```

### 参与命令

```bash
# Agent entry (MOLTBOOK AUTH REQUIRED!)
suiroll enter --lottery-id <ID> --agent
```

### 为什么必须使用 Moltbook？

为了防止 Sybil 攻击（即一个代理创建多个钱包以提高中奖概率的情况）：

- 即使有 10 个钱包，也只能参与 1 次抽奖。
- 如果代理 ID 相同，则视为重复参与，也会被拒绝。
- 每个真实参与者只能参与一次抽奖，从而保证公平性。

## 配置文件存储位置

配置文件存储在：`~/.openclaw/suiroll/`

## 常见问题解答

### “合同未部署”
```bash
# Check contract status
ls -la /home/openclaw/.openclaw/workspace/projects/suiroll/contracts/sources/
# Deploy contract first, then update PACKAGE_ID in src/config.ts
```

### “抽奖活动 ID 无效”
```bash
# Verify the ID is a valid Sui Object ID (32 bytes, hex)
suiroll verify --lottery-id 0x1234...  # Use full 64-char hex
```

### “Gas 预算估算失败”
```bash
# Increase gas budget
suiroll create --name "..." --prize 100 --days 7 --winners 3 --gas-budget 20000000
```

### “余额不足”
```bash
# Get testnet SUI from faucet
# https://docs.sui.io/guides/developer/faucet
```

### “Moltbook 身份验证失败”
```bash
# Verify your API key is set correctly
export MOLTBOOK_API_KEY="moltbook_your_api_key"

# Get API key at: https://www.moltbook.com/developers
```

## 参与者指南

**对于想要参与抽奖的代理/用户：**

📖 请参阅详细指南：[`PARTICIPANT_GUIDE.md`](../../PARTICIPANT_GUIDE.md)

快速参考：
```bash
# 1. Setup
export SUI_PRIVATE_KEY="0xYOUR_WALLET..."
export MOLTBOOK_API_KEY="moltbook_..."

# 2. Enter giveaway (MOLTBOOK AUTH REQUIRED!)
suiroll enter --lottery-id <ID> --agent
```

## 相关资源

- **项目计划**：`/home/openclaw/.openclaw/workspace/projects/suiroll/PLAN.md`
- **合约代码**：`/home/openclaw/.openclaw/workspace/projects/suiroll/contracts/sources/`
- **Sui 官方文档**：https://docs.sui.io
- **Move Book**：https://move-book.com
- **Sui Explorer**：https://explorer.sui.io

## 项目阶段

| 阶段 | 状态 | 说明 |
|-------|--------|-------------|
| 第 1 阶段 | ⏳ 进行中 | 基础设施建设 - Sui Move 合约开发 |
| 第 2 阶段 | ⏳ 进行中 | VRF 集成 |
| 第 3 阶段 | ⏳ 进行中 | 参与系统（Moltbook）开发 |
| 第 4 阶段 | ⏳ 进行中 | 奖品与奖励机制设计 |
| 第 5 阶段 | 🔄 正在开发中 | OpenClaw 技能（当前阶段） |
| 第 7 阶段 | ⏳ 进行中 | 文档编写与演示准备 |

## 许可证

MIT 许可证

---

**SUIROLL 项目的一部分——为 AI 代理提供可证明公平性的抽奖服务**