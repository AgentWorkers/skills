---
name: token-launcher
description: >
  您可以在任何区块链上发起代币发行，而无需放弃30-50%的费用。有两种方式可供选择：  
  1. **简单模式**：通过x402调用Tator API——适用于任何钱包提供商，无需设置环境变量；  
  2. **直接模式**：需要自行集成SDK，可以保留100%的费用——但需要使用签名密钥和RPC接口。  
  该工具支持以下区块链平台：  
  - Clanker（7个EVM区块链）  
  - Flaunch（Base）  
  - Pump.fun（Solana）  
  功能包括：  
  - 战略评估  
  - 费用管理  
  - 代币领取  
  - 受益人信息更新  
  - 税务/法律咨询  
  触发事件包括：  
  - “代币创意”  
  - “发行代币”  
  - “部署代币”  
  - “代币策略”  
  - “领取费用”  
  - “创作者费用”  
  - “更新费用接收者”  
  - “在Base区块链上发行代币”  
  - “在Solana区块链上发行代币”  
  - “Clanker”  
  - “Flaunch”  
  - “Pump.fun”  
  - “代币经济学”  
  - “这个代币是否具有投资价值？”
metadata:
  openclaw:
    emoji: "🚀"
    requires:
      env: []
    notes: >
      Easy Mode requires NO environment variables — it works with any x402-compatible
      wallet (Lobster, AgentWallet, Vincent, or local signer). Direct Mode requires
      WALLET_PRIVATE_KEY, RPC_URL, and an IPFS API key — see the credential table below.
publisher: Quick Intel / Web3 Collective
homepage: https://quickintel.io
source: https://github.com/Quick-Intel/openclaw-skills/tree/main/token-launcher
documentation: https://docs.tator.bot
---
# 代币发布工具

这个工具可以帮助你发布代币，并保留你应得的收益。有两种使用方式，但目标只有一个：不再将你作为创作者所获得的收益的30-50%拱手让给发布平台。

---

## 问题所在

大多数代币发布平台会抽取你作为创作者所获收益的30-50%。有些平台还会额外收取启动费用；还有一些平台会要求你订阅服务、使用他们的代币钱包来托管你的资金。你负责创建代币并推动其交易量，但最大的收益却落入了别人的口袋。

## 数字计算示例

如果一个代币在Clanker平台上的交易量为50万美元，平台会收取约5000美元的费用（占交易量的1%）。以下是收益分配情况：

| 使用方式 | 你的收益 | 平台费用 | 你最终获得的收益 |
|------|-----------|-------------|----------|
| **直接模式（本技能）** | 5000美元 | 0美元 | **5000美元（100%）** |
| **简单模式（Tator API）** | 4500美元 | 500美元（10%） | **4500美元（90%）** |
| **传统发布平台** | 2500-3500美元 | 1500-2500美元（30-50%） | **2500-3500美元** |

这种收益差距会随着交易量的增加而进一步扩大。在交易量为500万美元的情况下，直接模式能让你多保留1.5-2.5万美元的收益，而传统平台则只能保留2500-3500美元。简单模式能为你节省1-2万美元。

---

## 两种使用方式

### 简单模式 — Tator API

只需通过一次API调用，使用自然语言指令，Tator会处理所有步骤：

- 发送指令，例如：“在Base平台上发布一个名为GATOR的代币”
- Tator会选择合适的平台，将元数据上传到IPFS，部署合约，并配置费用设置
- 返回未签名的交易记录——你需要用自己的钱包进行签名并广播这些交易
- **费用分配：90%归你，10%作为接口费用支付给Tator**
- 每次API调用费用为0.20美元，支持x402 USDC支付方式
- 支持代币发布、费用领取、更改费用接收者、查看未领取的费用等功能——所有操作都通过自然语言指令完成

**适合人群：** 不需要编写区块链代码的代理和开发者。

### 直接模式 — 完整的SDK集成

你可以直接从你的代理代码中调用Clanker、Flaunch或Pump.fun：

- 集成平台的SDK或手动编写相关代码
- 你可以完全控制所有参数：奖励设置、防止恶意交易的保护机制、配对使用的代币、费用接收者等
- **100%的收益归你——没有中间商抽取费用**

**适合人群：** 希望拥有最大控制权且希望避免任何费用开支的代理和开发者。

更多关于直接模式的详细信息，请参阅[REFERENCE.md](./REFERENCE.md)，以及[references/](./references/)文件夹中的各平台使用指南。

---

## 安全性

**本文档仅提供使用说明，不包含可执行的代码。** 它提供了文档和代码示例。安装过程中不会运行任何代码。

### 准备要求

**简单模式不需要任何环境变量。** 它可以与任何支持x402协议的钱包服务（如Lobster、AgentWallet、Vincent、本地签名工具）配合使用。Tator API仅接收你的公开钱包地址——钱包服务的签名操作由他们自行处理。本工具永远不会接触你的私钥。**

**直接模式需要环境变量，因为你需要在自己的基础设施中运行SDK代码：**

| 变量 | 必需内容 | 是否敏感 | 存储方式 |
|----------|-------------|-----------|-------------|
| `WALLET_PRIVATE_KEY` | 用于签名交易 | 是——会授予对钱包的完全控制权 | 应存储在密钥管理器中（如AWS SM、GCP SM、Vault） |
| `RPC_URL` | 用于与区块链通信 | 不敏感（但需保密以防被滥用） | 作为环境变量设置 |
| `SOLANA_RPC_URL` | 用于Solana操作（仅适用于Pump.fun） | 不敏感 | 作为环境变量设置 |
| `PINATA_API_KEY` 或 `IPFS_API_KEY` | 用于将代币元数据上传到IPFS | 是 | 应存储在密钥管理器中 |

**如果你只使用简单模式，这些变量都不需要。** 本工具安装后无需配置任何环境变量即可使用。

### 简单模式的数据流程

当你调用Tator的x402 API（`POST https://x402.quickintel.io/v1/tator/prompt`）时：

1. **发送给Tator的信息：** `walletAddress`（公开地址）、`prompt`（你的指令）、`provider`（你的代理名称）
2. **不会发送给Tator的信息：** 你的私钥、助记词或任何签名相关资料
3. **支付方式：** 你的钱包服务会在本地签署USDC支付请求；API会在链上验证签名——Tator永远不会获取你的私钥 |
4. **返回给你的信息：** 未签名的交易记录——你需要在本机签名并自行广播这些交易

**在简单模式下，私钥永远不会离开你的设备。本工具本身无法访问你的私钥——签名操作由你的钱包服务独立完成。**

### 直接模式的数据流程

直接模式的代码完全在你的基础设施中运行：

1. **发送到区块链的请求：** 已签名的交易记录（由你选择的RPC服务处理，例如Alchemy、QuickNode或Helius）
2. **发送到IPFS的记录：** 代币的元数据（名称、符号、描述、图片）——这些信息是公开的
3. **发送到平台SDK的请求：** Clanker SDK的请求发送到Clanker的基础设施；Flaunch的请求发送到Base合约；Pump.fun的请求发送到Solana |
4. **不会发送的信息：** 你的私钥——它只会保存在你的设备上，用于本地签名操作

### 关键管理（仅适用于直接模式）

- **使用专用的发布钱包。** 不要使用你的主钱包或持有大量资金的钱包
- **将密钥存储在密钥管理器中。** 可以使用AWS Secrets Manager、GCP Secret Manager、HashiCorp Vault等工具。切勿将密钥硬编码在源代码中，也切勿以明文形式存储在`.env`文件中
- **只需少量资金**：在Base平台上大约需要0.01 ETH，在Solana平台上大约需要0.05 SOL——仅够支付交易费用
- **建议有人监督。** 如果你的代理是自动运行的，应在任何交易签名操作前进行人工审核。不要让自动代理未经监督地访问签名密钥
- **Pump.fun的机器人钱包：** Solana平台要求使用专门的机器人钱包进行签名；与EVM不同，Pump.fun的机器人钱包需要持有SOLANA代币作为交易费用。详情请参阅[references/pumpfun.md]**
- **撤销策略：** 如果发布钱包被泄露，确保你可以立即更换新的钱包**

### 关于SDK上下文字段的隐私注意事项

一些平台SDK（如Clanker）会接受一个可选的`context`对象用于数据分析。**这些字段完全是可选的。** 如果使用它们，请注意：
- `context.interface` — 你的代理/应用程序名称（发送给Clanker）
- `context.platform` — 用户使用的平台（例如“Telegram”）（发送给Clanker）
- `context.messageId` — 触发发布的消息ID（发送给Clanker）
- `context.id` — 用户标识符（发送给Clanker）

**如果担心隐私问题，可以完全省略`context`对象或使用匿名值。** 这些字段对操作的成功与否没有影响。详情请参阅Clanker的官方文档。**

### 验证外部端点

在使用任何端点之前，请确认你连接的是正确的服务：

| 服务 | 官方端点 | 验证方式 |
|---------|------------------|-----------|
| Tator x402 API | `https://x402.quickintel.io` | 检查TLS证书，调用`GET /accepted` |
| Quick Intel Scan | `https://x402.quickintel.io/v1/scan/full` | 通过相同的网关验证 |
| Clanker SDK | 通过npm安装`clanker-sdk`进行验证 | 在npmjs.com上验证包信息 |
| Flaunch合约 | 在Base平台上验证 | 通过Basescan验证 |
| Pump.fun程序 | 在Solana平台上验证 | 通过Solscan验证 | 程序ID：`6EF8rrecthR5Dkzon8Nwu78hRvfCKubJ14M5uBEwF6P` |

---

## 简单模式的详细使用步骤

### 先决条件

- 一个由你控制的钱包（适用于EVM或Solana平台）
- 用于支付x402 API费用的USDC（每次调用费用为0.20美元）
- 用于支付交易费用的代币（EVM平台使用ETH，Solana平台使用SOL）

### 发布代币

```bash
curl -X POST https://x402.quickintel.io/v1/tator/prompt \
  -H "Content-Type: application/json" \
  -H "PAYMENT-SIGNATURE: <x402_payment>" \
  -d '{
    "prompt": "launch a token called Galaxy Cat with ticker GCAT on base",
    "walletAddress": "0xYourWallet",
    "provider": "my-agent"
  }'
```

**使用自定义图片时：**
```json
{
  "prompt": "launch a token called Moon Dog with ticker MDOG on base with image https://example.com/dog.png",
  "walletAddress": "0xYourWallet",
  "provider": "my-agent"
}
```

**在Solana平台上：**
```json
{
  "prompt": "launch a token called Cyber Frog with ticker CYFR on solana via pump.fun",
  "walletAddress": "YourSolanaWallet",
  "provider": "my-agent"
}
```

**设置自定义的费用接收者（将费用发送到其他钱包）：**
```json
{
  "prompt": "launch a token called DAO Token with ticker DAOT on base, send creator fees to 0xTreasuryAddress",
  "walletAddress": "0xYourWallet",
  "provider": "my-agent"
}
```

响应中会包含未签名的交易记录，你需要用自己的钱包进行签名并广播。确认后，你会收到代币的地址、交易哈希值和费用配置信息。

### 查看未领取的费用

```json
{
  "prompt": "check my unclaimed fees for token 0xTokenAddress on base",
  "walletAddress": "0xYourWallet",
  "provider": "my-agent"
}
```

### 领取创作者收益

```json
{
  "prompt": "claim my creator fees for token 0xTokenAddress on base",
  "walletAddress": "0xYourWallet",
  "provider": "my-agent"
}
```

对于已经迁移到Raydium平台的Pump.fun代币，Tator会自动处理费用分配的流程（将WSOL从AMM钱包转移至Pump.fun钱包）。

### 更改费用接收者

```json
{
  "prompt": "update the fee recipient for token 0xTokenAddress on base to 0xNewRecipientAddress",
  "walletAddress": "0xYourWallet",
  "provider": "my-agent"
}
```

### 发布后的安全检查

使用Quick Intel（每次扫描费用为0.03美元）来验证你的代币是否安全：

```json
{
  "chain": "base",
  "tokenAddress": "0xYourDeployedToken"
}
```

调用`POST https://x402.quickintel.io/v1/scan/full`来检查是否存在潜在的安全风险（如钓鱼攻击、税收问题等）。

### 发现工具

调用`GET https://x402.quickintel.io/accepted`来获取所有支持的支付网络、价格信息以及自动配置所需的输入/输出格式。

---

## 平台选择

| 功能 | Clanker | Flaunch | Pump.fun |
|---------|---------|---------|----------|
| **支持的区块链** | Base、Arbitrum、Mainnet、Unichain、Abstract、Monad、BSC | Base | Solana |
| **池类型** | Uniswap V4 | 使用Bonding曲线 | 使用Bonding曲线 |
| **交易费用** | 1.2%（1%的池费用 + 0.2%的协议费用） | 可配置 | 可配置（根据代币是否达到市场价值阈值） |
| **创作者收益分配** | 可通过奖励接收者设置 | 可通过费用分配管理器设置 | 可通过配置文件设置 |
| **配对使用的代币** | 默认使用WETH，也支持USDC/USDT | 使用ETH | 使用SOL |
| **防止恶意交易的保护机制** | 有（费用会在15秒内逐渐减少） | 提供公平的发布窗口（默认为30分钟） | 使用Bonding曲线机制 |
| **代币的后续发展** | 无需等待特定条件即可立即加入Uniswap池 | 需要达到市场价值阈值才能加入Raydium池 | 发布后自动迁移到Raydium平台 |
| **代币标准** | ERC-20 | ERC-20 | SPL（Token-2022标准） |
| **代币总量** | 10亿枚（固定） | 可配置 | 根据Pump.fun的设置调整 |
| **创建费用** | 免费 | 免费 | 需支付少量SOL作为交易费用 |

### 何时选择哪种工具

**Clanker**：适用于EVM平台的代币发布。支持最多的区块链（7个平台），具有内置的防止恶意交易的机制，支持灵活的费用分配选项，流动性较好，DEX集成完善。

**Flaunch**：适用于希望在Base平台上进行公平发布的代币。30分钟的公平发布窗口可以有效防止恶意交易；自定义的费用分配机制让你能精细控制费用分配。

**Pump.fun**：适用于Solana平台的代币发布。使用Bonding曲线机制，代币达到市场价值阈值后自动迁移到Raydium平台；在Pump.fun的发现系统中可见。

---

## 评估一个代币发布方案

在部署任何代币之前，先明确你的目标。并非每个想法都需要通过代币来实现，也不是每个代币都需要立即发布。

### 代币发布的核心要素

每个能够持续吸引关注的代币背后都有四个关键要素在共同发挥作用。这并不是一个评分标准，而是一个诊断工具：

**第一层：吸引力** — 能够吸引人们关注的元素（名称、视觉效果、简短有力的描述）。大声念出这个代币的名字，它能立刻引起人们的兴趣吗？如果需要多句话来解释它的存在目的，那么它的吸引力就不够强。一个名字普通但执行得当的代币，其效果仍然不如一个名字出色但执行得当的代币。

**第二层：运营机制** — 发布后能够持续产生收益的机制。常见的运营机制包括：
- 文化相关的内容：能引发持续的讨论
- 实际有用的产品：能满足用户需求
- 持续推动活动的机制（如燃烧代币、空投、质押等）
- 社交互动：能与用户或社区产生互动

如果没有这些机制，代币在发布后可能会迅速失去价值。不过如果你能理解这一点，那也没关系。

**第三层：故事背景** — 能解释代币价值的理由。一个有力的故事背景会让人们相信“这个代币能用于特定用途”，从而支撑其价格。如果无法回答“为什么有人在三个月后还会购买这个代币？”这个问题，那么这个故事就需要改进。

**第四层：竞争优势** — 使代币难以被复制的原因。这可能包括：你是第一个推出这个代币的人、构建者的信誉、产品的实用性、社区的参与度、技术的先进性等。如果没有这些竞争优势，快速发布可能也无济于事。

### 在评估之前先进行搜索

在做出决定之前，先搜索以下信息：
- 是否有名称、代码或故事类似的现有代币
- 这个代币是否基于现有的文化趋势
- 类似的代币发布案例及其成败原因
- 构建者可能忽略的潜在问题

---

## ⚠️ 发布前务必注意：税务和法律问题

**代币发布是不可逆的操作。** 作为创作者，你获得的费用属于收入。大多数平台都会忽略这一点。

### 何时需要特别关注税务问题

如果你只是为了娱乐而发布一个代币，税务影响相对简单——主要是在出售代币时需要缴纳资本利得税。

但一旦你的代币具有实际价值（例如能够持续产生费用），那么税务和法律问题就会变得复杂。在发布之前，你必须寻求专业建议。

### 每个开发者都应该了解的内容

**这里提供的只是一般性信息，并非税务或法律建议。** 各地区的税务规定可能有所不同，请咨询专业人士。
- **作为创作者获得的费用通常被视为应税收入**。在大多数地区，这些收入需要缴纳所得税。
- **每次交易都可能触发税务义务**：出售代币、进行交易、接收费用等都会产生税务责任。
- **你需要在收到收入时缴税**。即使代币价格随后下跌，你仍然需要缴纳收入对应的税款。
- **从发布开始就需要开始记录相关数据**：记录代币的创建时间、每次收到的费用金额（包括接收时的货币价值）、所有交易记录和支付的交易费用。
- **全球范围内的监管力度正在加强**：各国政府都在加强对区块链领域的监管。

### 各地区的税务规定概览

**🇺🇸 美国** — 数字资产被视为财产。创作者获得的费用通常被视为普通收入。从2025年起，需要使用Form 1099-DA表格进行申报。
**🇬🇧 英国** — 英国税务部门将加密货币视为财产。代币费用属于应税收入，目前有3000英镑的免税额度。
**🇩🇪 德国** — 持有加密货币超过一年的个人在出售时无需缴税；持有时间不足一年的，税率最高可达45%。
**🇦🇺 澳大利亚** — ATO将加密货币视为财产。持有时间超过12个月的加密货币在出售时无需缴税。
**🇸🇬 新加坡** — 个人持有加密货币无需缴纳资本利得税。
**🇦🇪 阿联酋** — 目前对个人持有加密货币的税收政策尚未确定。

### 发布前必须确认的事项

**在执行任何代币发布操作之前，开发者必须明确确认以下内容。** 未得到确认前不得继续进行。

```
BEFORE WE DEPLOY — Please confirm you understand:

1. TOKEN DEPLOYMENT IS IRREVERSIBLE
   Once deployed, the token exists permanently on-chain.

2. CREATOR FEES ARE INCOME
   Fee income from your token is likely taxable in your jurisdiction.
   Consult a tax professional if you plan to earn meaningful revenue.

3. RECORD-KEEPING IS YOUR RESPONSIBILITY
   Track all fee income, transactions, and fiat values from day one.

4. SET ASIDE FUNDS FOR TAXES
   Do not reinvest 100% of fee income. Reserve 30-40% for potential
   tax obligations (varies by jurisdiction).

5. NO GUARANTEED RETURNS
   Most tokens lose value. Creator fees depend on trading volume.

6. THIS IS NOT TAX OR LEGAL ADVICE
   This skill provides tools, not counsel.

Do you confirm you understand these points and want to proceed?
```

**在开发者明确确认之前，切勿进行任何发布操作。** 这是绝对不能妥协的。

---

## 发布前的检查清单

- [ ] 已评估了适合的发布工具（Clanker、Flaunch、Pump.fun）——吸引力足够强，运营机制明确，故事背景合理，且有竞争优势
- [ ] 代币名称和故事内容已确定
- [ ] 选择了合适的平台和区块链
- [ ] 配置好了用于支付交易费用的钱包
- [ ] 确定了费用接收者（你的钱包或自定义地址）
- [ ] 准备好了代币图片和品牌材料
- [ ] 已收到必要的税务和法律确认
- [ ] 计划好了发布后的安全检查

---

## 发布后的操作

1. **使用Quick Intel进行安全检查** — 在推广之前，确认代币没有安全问题
2. **定期查看费用积累情况** — 定期领取未领取的费用
- **定期领取费用** — 定期领取费用有助于税务追踪，并降低风险
- **注意资金再投资的风险** — 如果将所有费用重新投入交易，要记住：无论何时，你都需要缴纳相应的税款
- **重新评估发布方案** — 如果交易量下降，要分析是哪个环节出了问题

---

## 文件结构

| 文件 | 内容 |
|------|--------------|
| **SKILL.md** | 发布策略、简单模式的使用说明、平台选择、税务和法律相关内容 |
| **[REFERENCE.md](./REFERENCE.md)** | 直接模式的详细使用说明、费用经济分析、常见模式介绍 |
| **[references/clanker.md](./references/clanker.md)** | Clanker v4 SDK的使用指南（包括发布、费用领取、费用接收者设置等） |
| **[references/flaunch.md](./references/flaunch.md)** | Flaunch的使用指南（包括发布流程、费用分配、费用领取等） |
| **[references/pumpfun.md](./references/pumpfun.md)** | Pump.fun的使用指南（包括手动操作步骤、费用分配、代币后续处理等） |

## 本文档的作用

- **不提供税务建议。** 仅提供通用信息供参考。
- **不提供法律建议。** 代币发布可能涉及证券法相关问题。
- **不能保证盈利。** 大多数代币的价值会随时间下降。
- **不是快速致富的工具。** 本文档旨在帮助开发者负责任地发布代币，并保留更多的收益。