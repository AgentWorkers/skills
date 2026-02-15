---
name: basecred-8004-registration
description: 通过聊天界面实现交互式的 ERC-8004 代理注册功能。系统引导用户填写预填表单，展示代理的草案信息，经用户确认后，使用 agent0-sdk 在链上完成注册过程。
---

# Basecred ERC-8004 注册

通过引导式聊天体验，在 [ERC-8004](https://8004.org) 链上注册 AI 代理。

## 注册流程

### 第一步：自动填充

当用户触发注册时，**自动填充以下所有可填充的字段**：
- 代理身份文件（IDENTITY.md、SOUL.md、USER.md）
- 环境配置（`.env` 文件——从私钥派生的钱包地址）
- 上次注册的上下文信息（A2A 端点、描述、图片等）
- 合理的默认值（版本：1.0.0，许可证：MIT，链：Base，存储方式：链上）

**不要逐一询问信息**。先自动填充，有需要时再询问。

### 第一步.5：解释配置默认值

在显示注册草稿之前，简要说明配置选项的默认设置，让用户了解哪些选项已被选中以及有哪些可选方案：

```
⚙️ Config defaults (you can change these later):

Chain:    Base (8453) — where your agent lives on-chain
          Others: Ethereum, Polygon, BNB, Arbitrum, Celo, Gnosis, Scroll

Storage:  Fully onchain — agent data stored directly on-chain
          Alternative: IPFS — data pinned to IPFS, hash stored on-chain

Trust:    Reputation — other agents/users rate your agent on-chain
          Others: Crypto-Economic (staking/slashing guarantees)
                  TEE Attestation (hardware-level trust proof)

x402:     Off — no payment protocol
          On: agent can charge for services via x402 payment protocol

Active:   On — agent is discoverable and accepting requests
          Off: registered but hidden from discovery

Wallet:   Your agent's on-chain identity address
          Two ways to set it:

          Option A: Paste your wallet address
          → Just paste your 0x... address
          → Agent will be linked to this address on-chain

          Option B: Add private key to .env (for signing)
          → Set PRIVATE_KEY=0x... in your .env file
          → Wallet auto-detected + can sign transactions
          → Enables setWallet() via EIP-712 after registration

          💡 Option A is easier. Option B is needed if you want
             the agent to sign transactions on your behalf.
```

仅在开始时显示一次，不要在每次显示草稿时都重复。

### 第二步：以单条消息的形式显示完整草稿及按钮

使用 `message` 工具将**整个注册草稿及按钮**作为一条消息发送。确保按钮直接显示在草稿下方。

**重要提示：** 使用 `message action=send` 同时发送 `message`（草稿文本）和 `buttons`（内联按钮）。**不要将消息拆分为回复和单独的按钮消息**。发送后，回复 `NO_REPLY` 以避免重复操作。

使用 ✅（已填写）和 ⚠️（缺失/需要关注）来标记字段：

```
📋 Agent Registration Draft

── Basic Info ──
✅ Name:        Mr. Tee
✅ Description: AI agent with a CRT monitor...
✅ Image:       pbs.twimg.com/...
✅ Version:     1.0.0
✅ Author:      0xdas
✅ License:     MIT

── Endpoints ──
✅ A2A:         a2a.teeclaw.xyz/a2a
⚠️ MCP:         (none)

── Skills & Domains ──
✅ Skills (5):  natural_language_processing/natural_language_processing, 
                natural_language_processing/natural_language_generation/summarization,
                natural_language_processing/information_retrieval_synthesis/question_answering,
                analytical_skills/coding_skills/coding_skills,
                images_computer_vision/images_computer_vision
✅ Domains (5): technology/blockchain/blockchain, technology/blockchain/defi,
                technology/technology, technology/software_engineering/software_engineering,
                technology/software_engineering/devops
✅ Custom:      agent_orchestration/agent_coordination, 
                social_media/content_management

── Config ──
✅ Chain:       Base (8453)
✅ Storage:     Fully onchain
✅ Active:      true
✅ Trust:       reputation
✅ x402:        false
✅ Wallet:      0x1348...e41 (auto .env)

Tap to edit a section or register:
```

按钮（与同一消息关联）：
```
Row 1: [✏️ Basic Info] [✏️ Endpoints]
Row 2: [✏️ Skills & Domains] [✏️ Config]
Row 3: [✅ Register] [❌ Cancel]
```

### 第三步：编辑相应部分（点击按钮后）

**即时反馈：** 当点击任何按钮时，先给出即时反馈，然后再进行其他操作：

| 按钮 | 即时反馈 |
|--------|-----------------|
| ✏️ 基本信息 | “📝 正在编辑基本信息...” |
| ✏️ 端点 | “🔗 正在编辑端点...” |
| ✏️ 技能与领域 | “🏷️ 正在编辑技能与领域...” |
| ✏️ 配置 | “⚙️ 正在编辑配置...” |
| ✅ 注册 | “⏳ 即将在 Base 链上开始注册...” |
| ❌ 取消 | “❌ 注册已取消。” |
| ↩️ 返回草稿 | “📋 返回草稿...” |

然后显示编辑表单。务必包含 **↩️ 返回草稿** 按钮。

#### 编辑基本信息
```
Current values:
• Name: Mr. Tee
• Description: AI agent with a CRT...
• Image: pbs.twimg.com/...
• Version: 1.0.0
• Author: 0xdas
• License: MIT

Type field name and new value, e.g. "name: CoolBot"
Or type "done" to go back.
```
按钮：`[↩️ 返回草稿]`

#### 编辑端点
```
Current:
• A2A: https://a2a.teeclaw.xyz/a2a
• MCP: (none)

Paste a URL to set, or "clear mcp" / "clear a2a" to remove.
```
按钮：`[↩️ 返回草稿]`

#### 编辑技能与领域
可切换的内联按钮（多选）。每个按钮显示**人类可读的标签**，但实际存储的是完整的 **OASF 分类路径**。

**技能：**（OASF 分类路径）
```
[NLP ✅] → natural_language_processing/natural_language_processing
[Summarization ✅] → natural_language_processing/natural_language_generation/summarization
[Q&A ✅] → natural_language_processing/information_retrieval_synthesis/question_answering
[Code Gen ✅] → analytical_skills/coding_skills/coding_skills
[CV ✅] → images_computer_vision/images_computer_vision
[Data Analysis] → analytical_skills/data_analysis/data_analysis
[Web Search] → natural_language_processing/information_retrieval_synthesis/web_search
[Image Gen] → images_computer_vision/image_generation/image_generation
[Translation] → natural_language_processing/natural_language_generation/translation
[Task Automation] → tool_interaction/workflow_automation
[+ Custom] [↩️ Back to Draft]
```

**领域：**（OASF 分类路径）
```
[Blockchain ✅] → technology/blockchain/blockchain
[DeFi ✅] → technology/blockchain/defi
[Technology ✅] → technology/technology
[SE ✅] → technology/software_engineering/software_engineering
[DevOps ✅] → technology/software_engineering/devops
[Finance] → finance/finance
[Healthcare] → healthcare/healthcare
[Education] → education/education
[Entertainment] → entertainment/entertainment
[Science] → science/science
[Creative Arts] → creative_arts/creative_arts
[Dev Tools] → technology/software_engineering/development_tools
[+ Custom] [↩️ Back to Draft]
```

**显示方式：**
- 按钮显示**简短标签**（例如：“NLP”、“Blockchain”）以便于阅读
- 实际存储的是**完整的 OASF 路径**（例如：`natural_language_processing/natural_language_processing`）
- 点击按钮可以切换选中/取消选中状态
- `+ 自定义` 按钮提示用户输入自定义的 OASF 路径或标签

#### 编辑配置
**信任模型**（多选）：
```
[Reputation ✅] [Crypto-Economic] [TEE Attestation]
```

**其他配置：**
```
[Chain: Base ▼] [Storage: Onchain ▼] [x402: Off ▼]
[↩️ Back to Draft]
```

| 信任模型 | 描述 |
|-------------|-------------|
| **声誉** | 链上反馈与评分。大多数代理的默认设置。 |
| **加密经济** | 用于金融代理的质押/销毁机制。 |
| **TEE 证明** | 用于高安全性代理的硬件级信任验证。 |

### 第四步：返回草稿

进行任何编辑后，将更新后的完整草稿以**单条消息的形式再次发送**（与步骤 2 相同）。重复此过程，直到用户点击 **✅ 注册**。

### 第五步：执行注册

只有在用户明确确认 **✅ 注册** 后，才执行注册操作：
1. 将注册信息写入临时文件
2. 运行注册脚本：

```bash
source /path/to/.env
node scripts/register.mjs --json /tmp/registration.json --chain 8453 --yes
```

脚本执行的操作包括：`register()` → `setA2A()`/`setMCP()` → `addSkill()`/`addDomain()` → `setWallet()`

### 第五步.5：注册进度更新

在注册过程中向用户发送进度更新：

```
⏳ Step 1/3: Minting agent NFT on Base...
✅ Agent minted! ID: 8453:42

⏳ Step 2/3: Setting endpoints & metadata...
✅ Endpoints configured

⏳ Step 3/3: Linking wallet via EIP-712...
✅ Wallet linked!
```

### 第六步：报告注册结果

```
✅ Agent Registered on Base!

  Agent ID:    8453:42
  Wallet:      0x1348...e41
  A2A:         a2a.teeclaw.xyz/a2a
  TX:          0xabc...def

  View: https://8004.org/agent/8453:42
```

## 错误处理

### 缺少必填字段
如果 **名称** 或 **描述** 在自动填充后为空，请标记为 ⚠️ 并阻止注册。显示提示：“请先填写必填字段。”

### 未找到钱包
```
⚠️ No wallet detected. You need one to register:
  Option A: Paste your 0x... address
  Option B: Add PRIVATE_KEY to your .env file
```

### 交易失败
清晰显示错误并提供重试选项：
```
❌ Registration failed: insufficient funds for gas
[🔄 Retry] [❌ Cancel]
```

### 设置钱包失败
公共 RPC（例如 mainnet.base.org）不支持 `eth_signTypedData_v4`。如果设置钱包失败：
```
⚠️ Wallet linking failed (public RPC limitation).
You can link your wallet manually at https://8004.org
```
这种情况下注册操作不会被阻塞——代理已经注册，只是钱包尚未链接到链上。

### 防止重复注册
脚本会在提交前检查钱包是否已经在目标链上拥有代理。如果检测到重复注册：
```
⚠️ Warning: This wallet already owns 1 agent(s) on Base.
   Registering again will create a duplicate.
   Use update.mjs to modify an existing agent instead.
```
在聊天界面中警告用户，并建议用户更新信息而非重新注册。如果传递了 `--yes` 参数，此检查操作是非阻塞的。

### 代理已注册
如果代理已经拥有代理 ID，建议用户**更新**现有代理信息而非重新注册。

## 技术说明

### 注册表覆盖
SDK 仅提供以太坊主链的注册表地址。对于 Base 及其他链，脚本会使用以下确定性合约地址：
- 身份注册表：`0x8004A169FB4a3325136EB29fA0ceB6D2e539a432`
- 声誉注册表：`0x8004BAa17C55a88189AE136b182e5fdA19dE9b63`

### 交易处理
SDK 会返回 `TransactionHandle` 对象。使用 `.waitMined()`（而非 `.wait()`）来等待交易确认。

## 所有字段参考

### 基本信息
| 字段 | 是否必填 | 默认值 | 数据来源 |
|-------|----------|---------|-------------|
| **代理名称** | ✅ | — | IDENTITY.md 文件 |
| **代理地址** | 自动填充 | — | 从 `.env` 文件中的私钥获取 |
| **描述** | ✅ | — | 从 IDENTITY.md 或 SOUL.md 文件获取 |
| **图片** | 可选 | — | 个人资料图片的 URL |
| **版本** | 可选 | `1.0.0` | — |
| **作者** | 可选 | — | 从 USER.md 文件获取 |
| **许可证** | 可选 | `MIT` | — |

### 端点
| 字段 | 是否必填 | 默认值 | 数据来源 |
|-------|----------|---------|-------------|
| **A2A 端点** | 可选 | — | 从 IDENTITY.md 文件获取 |
| **MCP 端点** | 可选 | — | — |

### 技能与领域
| 字段 | 是否必填 | 默认值 |
|-------|----------|---------|
| **选中的技能** | 可选 | `[]` |
| **选中的领域** | 可选 | `[]` |
| **自定义技能** | 可选 | `[]` |
| **自定义领域** | 可选 | `[]` |

### 高级配置
| 字段 | 是否必填 | 默认值 |
|-------|----------|---------|
| **信任模型** | 可选 | `[]`（建议使用默认的声誉模型） |
| **x402 支持** | 可选 | `false` |
| **存储方式** | 可选 | `http`（完全存储在链上） |
| **是否激活** | 可选 | `true` |
| **链** | 可选 | `8453`（Base 链） |

## 支持的链
| 链 | ID | 默认值 |
|-------|-----|---------|
| **Base** | 8453 | ✅ |
| 以太坊 | 1 | |
| Polygon | 137 | |
| BNB 链 | 56 | |
| Arbitrum | 42161 | |
| Celo | 42220 | |
| Gnosis | 100 | |
| Scroll | 534352 | |

所有链都使用相同的确定性合约地址。

## JSON 模板（8004.org 格式）

```json
{
  "basicInfo": {
    "agentName": "",
    "agentAddress": "",
    "description": "",
    "image": "",
    "version": "1.0.0",
    "author": "",
    "license": "MIT"
  },
  "endpoints": {
    "mcpEndpoint": "",
    "a2aEndpoint": ""
  },
  "skillsDomains": {
    "selectedSkills": [],
    "selectedDomains": [],
    "customSkills": [],
    "customDomains": []
  },
  "advancedConfig": {
    "supportedTrusts": [],
    "x402support": false,
    "storageMethod": "http",
    "active": true
  },
  "version": "1.0.0"
}
```

## 环境变量
| 变量 | 是否必填 | 描述 |
|----------|----------|-------------|
| `PRIVATE_KEY` / `AGENT_PRIVATE_KEY` / `MAIN_WALLET_PRIVATE_KEY` | 是 | 钱包私钥 |
| `RPC_URL` | 可选 | 根据链自动检测的 RPC 地址 |
| `CHAIN_ID` | 可选 | 默认链（8453） |

## 其他操作

```bash
# Search agents
node scripts/search.mjs --name "AgentName" --chain 8453

# Update agent
node scripts/update.mjs --agent-id "8453:42" --name "NewName" --yes

# Give feedback
node scripts/feedback.mjs --agent-id "8453:42" --value 5 --tag1 "reliable" --yes
```

## 设置

```bash
bash scripts/setup.sh
```