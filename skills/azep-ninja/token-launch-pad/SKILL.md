---
name: token-launcher
description: >
  **Launch Tokens**  
  您可以100%保留自己作为创作者所获得的费用。**Direct Mode**提供了针对Clanker（7个EVM区块链）、Flaunch（Base）和Pump.fun（Solana）的完整SDK集成指南——无需中间商，也没有平台费用抽取。**Easy Mode**则通过Tator API提供了便捷的解决方案（费用分配比例为90%归创作者，10%归平台）。该模式包括策略评估、费用经济模型、费用领取、收款人信息更新以及税务/法律咨询等服务。  
  **可使用的触发词（Triggers）：**  
  - “token idea”（创建新代币的想法）  
  - “launch a coin”（发行新币）  
  - “launch a token”（发行代币）  
  - “deploy a token”（部署代币）  
  - “token strategy”（代币发行策略）  
  - “claim fees”（领取费用）  
  - “creator fees”（创作者费用）  
  - “update fee recipient”（更新收款人信息）  
  - “token launch on base”（在Base区块链上发行代币）  
  - “launch on solana”（在Solana区块链上发行代币）  
  - “clanker”  
  - “flaunch”  
  - “pump.fun”  
  - “token economics”（代币经济模型）  
  - “is this a good token?”（这个代币值得投资吗？）
metadata:
  openclaw:
    emoji: "🚀"
    requires:
      env: []
    notes: >
      This skill requires no API keys or environment variables. Easy Mode uses
      the x402 payment protocol (HTTP 402), where authentication and payment are
      handled by the user's wallet at request time via a signed PAYMENT-SIGNATURE
      header — no stored credentials needed. Direct Mode implementation guides
      are in REFERENCE.md for developers building in their own infrastructure.
publisher: Quick Intel / Web3 Collective
homepage: https://quickintel.io
source: https://github.com/Quick-Intel/openclaw-skills/tree/main/token-launcher
documentation: https://docs.tator.bot
---
# 代币发布工具

这个工具可以帮助你发布代币，并让你保留更多的收益。它是一个开源项目，旨在帮助你在发布代币时避免将30-50%的创作者收益交给发布平台。

---

## 问题所在

大多数代币发布平台会收取创作者收益的30-50%作为费用。有些平台还会额外收取预付款。还有一些平台会要求用户订阅、使用他们的平台代币或托管钱包来保管资金。你负责创建代币并推动其交易量，但大部分收益却落入了平台的口袋。

## 数字计算

在Clanker平台上，如果一个代币的交易量为50万美元，平台会收取约5,000美元的费用（交易量的1%）。以下是收益分配情况：

| 分配方式 | 你的收益 | 平台费用 | 你最终获得的收益 |
|------|-----------|-------------|----------|
| **直接模式（本工具提供）** | 5,000美元 | 0美元 | **5,000美元（100%）** |
| **简易模式（Tator API）** | 4,500美元 | 500美元（10%） | **4,500美元（90%）** |
| **传统发布平台** | 2,500-3,500美元 | 1,500-2,500美元（30-50%） | **2,500-3,500美元** |

这种差异会随着交易量的增加而扩大。在交易量为500万美元的情况下，使用直接模式可以让你多保留15,000-25,000美元的收益。

---

## 两种发布方式

本工具提供了两种发布代币的方法。直接模式是主要推荐的方式；简易模式则是为了方便用户而设计的备用选项。

### 直接模式 — 保留100%的费用（推荐）

直接模式提供了使用平台SDK发布代币的完整实现指南。你可以控制所有参数，并且完全保留创作者的费用，无需支付任何平台费用。

- 支持的平台：Clanker（Base、Arbitrum、Mainnet、Unichain、Abstract、Monad、BSC）、Flaunch（Base）、Pump.fun（Solana）
- 提供完整的部署、费用配置、收益领取和接收者管理的代码示例
- 生成的代币交易数据格式与所有钱包兼容
- 详细的费用结构说明，展示费用在各个平台上的分配情况

**实现指南：**
- [REFERENCE.md](./REFERENCE.md) — 直接模式概述、费用结构、操作步骤、钱包集成方法
- [references/clanker.md](./references/clanker.md) — Clanker v4 SDK：发布、奖励机制、狙击者防护、收益领取
- [references/flaunch.md](./references/flaunch.md) — Flaunch：发布、自定义费用分配、收益领取、接收者转移
- [references/pumpfun.md](./references/pumpfun.md) — Pump.fun：手动操作指南、费用分配、代币毕业处理

### 简易模式 — 便捷的发布方式

简易模式使用Tator API来处理代币的部署。Tator会从创作者的收益中抽取10%作为接口费用。

- 只需要通过`x402.quickintel.io`发送一次API请求，提供代币信息和钱包地址
- Tator会为你完成代币的部署，无需你手动签名交易
- 每次API请求的费用为0.20美元（使用x402 USDC支付）
- 支持发布、领取费用、更新接收者信息、查看未领取的费用——所有操作都通过自然语言界面完成
- **费用分配：90%归你，10%归Tator**

### 如何向用户展示这两种方式

当用户想要发布代币时，首先向他们介绍直接模式：

- **直接模式（推荐）：** 你可以保留100%的创作者费用。参考指南中提供了完整的部署、费用配置和领取费用的代码示例。你可以使用自己的钱包生成未签名的交易并签名。无需支付任何平台费用。
- **简易模式（便捷）：** Tator会为你完成代币的部署。你需要提供钱包地址、代币信息，并通过x402支付0.20美元。这种方式启动更快，但Tator会抽取10%的费用。

两种方式都需要相同的参数：钱包地址、代币名称、代币代码和链地址。如果用户不确定该选择哪种方式，直接模式是更长期的最佳选择；简易模式适用于对速度要求较高的情况。

---

## 直接模式 — 操作步骤

有关直接模式的完整操作步骤、费用结构、未签名交易格式和钱包集成方法，请参阅[REFERENCE.md](./REFERENCE.md)。

### 快速入门

1. **根据目标链选择合适的平台**（详见下文“平台选择”）
2. **阅读所选平台的参考指南**——其中包含完整的代码示例
3. **将费用接收者设置为你的钱包**——这正是直接模式的核心所在
4. **生成未签名的交易数据**——参考文件中提供了每个平台的详细操作步骤
5. **使用任何钱包进行签名**——Lobster、AgentWallet、base-wallet、evm-wallet、MetaMask或其他签名工具均可
6. **发布后**：领取费用、查看未领取的费用、更新接收者信息——所有操作都有详细的文档说明

### 直接模式的平台选择

| 目标链 | 推荐平台 | 参考文档 |
|-------------|----------|-----------|
| Base | Clanker或Flaunch | [clanker.md](./references/clanker.md)或[flaunch.md] |
| Arbitrum、Mainnet、Unichain、Abstract、Monad、BSC | Clanker | [clanker.md](./references/clanker.md) |
| Solana | Pump.fun | [pumpfun.md](./references/pumpfun.md) |

**Clanker与Flaunch的比较：**
- **Clanker：** 支持Uniswap V4池、狙击者防护机制、稳定的代币对价（USDC）、多链兼容性
- **Flaunch：** 提供30分钟的公平发布窗口、自定义费用分配机制

---

## 平台选择（详细比较）

| 特点 | Clanker | Flaunch | Pump.fun |
|---------|---------|---------|----------|
| **支持的链** | Base、Arbitrum、Mainnet、Unichain、Abstract、Monad、BSC | Base | Solana |
| **池类型** | Uniswap V4 | Bonding curve | Bonding curve → Raydium |
| **交换费用** | 1.2%（1%的池费用 + 0.2%的协议费用） | 可配置 | 可变（代币毕业前后） |
| **创作者费用比例** | 通过收益接收者设置 | 通过费用分配器设置 | 通过配置设置 |
| **可配对的代币** | 默认为WETH，也可使用USDC/USDT | ETH | SOL |
| **狙击者防护** | 支持（费用在15秒内从66.7%降至4.2%） | 提供30分钟的公平发布窗口 | 使用Bonding curve机制 |
| **代币毕业** | 无延迟地进入Uniswap池 | 无延迟 | 达到市场价值阈值后进入Raydium |
| **代币标准** | ERC-20 | ERC-20 | SPL（Token-2022） |
| **发行量** | 10亿枚（固定） | 1000亿枚（可配置） | 根据Pump.fun规则调整 |
| **创建费用** | 免费 | 免费 | 需支付少量SOL作为费用 |

### 何时使用哪种方式

- **Clanker：** 适用于基于EVM的代币发布。支持最多的链（7个链），具有内置的狙击者防护机制和稳定的代币对价选项，流动性最佳，且与DEX集成良好。
- **Flaunch：** 适用于需要在Base链上进行公平发布的场景。30分钟的公平发布窗口可以有效防止恶意行为，自定义的费用分配机制让你能够精细控制费用分配。
- **Pump.fun：** 适用于Solana平台的代币发布。代币达到市场价值阈值后会自动进入Raydium池。

---

## 评估一个项目

在部署任何代币之前，先弄清楚你的项目真正需要什么。并非每个想法都需要代币，也不是每个代币都需要立即发布。

### 发布代币的必备组件

任何能够持续吸引关注的代币都需要四个方面的支持。这不是一个评分标准，而是一个诊断工具：

**第一层：吸引力** — 能够吸引用户注意力的元素，比如名称、视觉设计或简短有力的宣传语。试着大声说出这个代币的名字，它能否立即引起人们的兴趣？如果需要多句话来解释这个代币的存在理由，那么它的吸引力就不够强。
**第二层：持续运营的机制** — 发布后能够持续吸引用户的原因，比如文化价值、实用的产品功能、特殊的机制（如燃烧、空投、质押）或社交影响力。如果没有这些机制，代币在发布后很快就会失去吸引力。
**第三层：故事背景** — 能够解释代币价格上涨的理由。好的故事背景是：“这个代币用于资助某个具体的项目，所有持有者都在支持它。” 而弱的故事背景则是：“这是一个社区代币”（但这个社区是什么？为什么选择这个代币？）。
**第四层：护城河** — 使代币难以被复制的原因，比如先发优势、创建者的信誉、整合的产品、社区的忠诚度或技术优势。如果没有这些护城河，快速发布反而可能成为劣势。

### 在做出判断前先进行调查

永远不要在孤立的环境中评估一个项目。在给出意见之前，先搜索一下是否有类似名称/故事背景的现有代币，了解它们的市场表现以及创建者的背景信息。

---

## ⚠️ 发布前：税务和法律方面的注意事项

**代币的发布是不可逆的。创作者的费用属于收入。大多数平台都会忽略这一点。**

### 何时需要特别关注税务问题

如果你只是为了娱乐而发布一个代币，税务影响相对简单——主要是在出售代币时需要缴纳资本利得税。

但一旦你的代币具有实际价值，比如能够持续产生费用，或者你的代币被用于实际产品，那么税务和法律问题就会变得复杂，此时你需要专业的法律咨询。

### 每个开发者都应该了解的内容

- 这些信息仅供参考，并非税务或法律建议。不同地区的税务法规可能有所不同，请咨询专业人士。
- **创作者的费用通常被视为应税收入**。在大多数地区，持续产生的费用被视为收入，而非资本利得。
- **任何交易都可能触发税务义务**——出售代币、进行交易、接收费用支付或分发空投都会产生税务责任。
- **你需要在收到收入时缴税**——即使你将所有费用重新投资，代币价格下跌，你仍然需要缴纳相应的税款。
- **记录保存从发布开始**——记录代币的创建日期、每次费用支付的金额（包括收到的法定货币价值）、每次交易和交易费用。
- **全球范围内的监管力度正在加强**——各国政府都在加强对区块链领域的监管。

### 各地区的税务规定

**🇺🇸 美国** — 数字资产被视为财产（IRS Notice 2014-21）。创作者的费用通常被视为普通收入，从2025年起需要提交1099-DA表格。
**🇬🇧 英国** — 英国税务部门将加密货币视为财产，代币费用属于应税收入，目前免税额度为3,000英镑。
**🇩🇪 德国** — 持有时间超过1年的加密货币在处置时免税；持有时间少于1年的，税率最高可达45%。
**🇦🇺 澳大利亚** — 澳大利亚税务局将加密货币视为财产，持有时间超过12个月的收益可享受50%的免税优惠。
**🇸🇬 新加坡** — 个人无需缴纳资本利得税（现行规定）。企业的代币收入可能需纳税。
**🇦🇪 阿联酋** — 目前个人无需缴纳联邦所得税，相关法规正在制定中。
**🇨🇦 加拿大** — 加拿大税务局将加密货币视为商品，资本利得税率为50%。

## ⛔ 发布前需要确认的事项

在发布代币之前，开发者需要了解并确认以下几点：

1. **代币的发布是不可逆的** — 一旦发布，代币将永久存在于链上。
2. **创作者的费用属于应税收入** — 在大多数地区需要缴税，请咨询税务专业人士。
3. **你需要负责记录保存** — 从发布之日起，记录所有的费用收入、交易和法定货币价值。
4. **预留税款** — 预留30-40%的费用作为可能的税务支出。
5. **无法保证收益** — 大多数代币的价值会下降；创作者的费用取决于交易量。
6. **本工具不提供税务或法律建议** — 它只提供工具和信息，并不提供法律建议。

开发者应在继续之前确认自己理解这些内容。

---

## 发布前的准备事项

- [ ] 已评估发布所需的全部组件：吸引力、持续运营的机制、故事背景和护城河
- [ ] 代币名称和宣传内容已确定
- [ ] 选择了合适的平台和链
- [ ] 钱包已准备好，并配备了足够的代币用于支付交易费用
- [ ] 收费接收者已确认
- [ ] 宣传图片和品牌设计已完成
- [ ] 发布前的所有事项都已确认
- [ ] 已计划发布后的安全检查

---

## 简易模式的完整操作步骤

### 先决条件

- 你控制的钱包（适用于EVM或Solana）
- 用于支付x402 API费用的USDC（每次调用费用为0.20美元）
- 用于支付交易费用的代币（EVM链使用ETH，Solana链使用SOL）

**不需要API密钥或存储的凭证。** x402支付协议（HTTP 402）同时处理认证和支付：API返回402响应，你的钱包会在本地签名USDC支付授权，然后你可以使用签名后的`PAYMENT-SIGNATURE`头信息重新发送请求。API会在链上验证支付信息，不会获取你的私钥。详情请参阅[x402.org](https://www.x402.org)。

### 调用API之前的准备

在发送API请求之前，需要收集用户的以下信息：

1. **公开钱包地址** — 用于接收创作者费用的地址。
2. **代币名称和代码**  
3. **目标链** — Base、Solana、Arbitrum等
4. **首选平台**（可选）——Clanker、Flaunch或Pump.fun
5. **宣传图片链接**（可选）
6. **自定义费用接收者**（可选）——如果费用需要支付给其他账户

### API安全说明

Tator API接受`prompt`字段——这是指向Tator交易服务的API调用参数，而非用于代理模型的提示信息。该字段的值会被发送到`x402.quickintel.io`，Tator的服务器会解析并执行相应的操作。API仅在服务器端进行验证，不会执行任意代码或访问文件系统。

### 发布代币的API调用

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

**参数说明：**
- `prompt` — 发送给Tator API的交易指令。
- `walletAddress` — 你的公开钱包地址，用于设置为你作为费用接收者。
- `provider` — 你的代理或集成服务的名称。

**在Solana链上的调用示例：**
```json
{
  "prompt": "launch a token called Cyber Frog with ticker CYFR on solana via pump.fun",
  "walletAddress": "YourSolanaWallet",
  "provider": "my-agent"
}
```

**如果设置了自定义费用接收者：**
```json
{
  "prompt": "launch a token called DAO Token with ticker DAOT on base, send creator fees to 0xTreasuryAddress",
  "walletAddress": "0xYourWallet",
  "provider": "my-agent"
}
```

Tator会完成代币的部署，并返回部署结果，包括代币地址、交易哈希和费用配置信息。

### 发布后的操作

**检查未领取的费用：**
```json
{
  "prompt": "check my unclaimed fees for token 0xTokenAddress on base",
  "walletAddress": "0xYourWallet",
  "provider": "my-agent"
}
```

**领取创作者的费用：**
```json
{
  "prompt": "claim my creator fees for token 0xTokenAddress on base",
  "walletAddress": "0xYourWallet",
  "provider": "my-agent"
}
```

**更新费用接收者：**
```json
{
  "prompt": "update the fee recipient for token 0xTokenAddress on base to 0xNewRecipientAddress",
  "walletAddress": "0xYourWallet",
  "provider": "my-agent"
}
```

### 发布后的安全检查

使用Quick Intel（每次扫描费用为0.03美元）来验证你的代币是否安全：

调用`POST https://x02.quickintel.io/v1/scan/full`，传入`{"chain": "base", "tokenAddress": "0xYourDeployedToken"}`，以检查是否存在潜在的安全风险或错误。

### 获取支付网络信息

调用`GET https://x02.quickintel.io/accepted`，以获取支持的支付网络、价格信息和相关规则。

---

## 发布后的操作

1. **进行安全检查** — 在推广代币之前，确保代币没有安全问题。
2. **定期检查未领取的费用** — 定期领取未领取的费用。
3 **定期领取费用** — 定期领取费用有助于更好地管理税务。
4 **注意再投资风险** — 无论是否进行再投资，你都需要缴纳相应的税款。
5 **重新评估发布流程** — 如果交易量下降，需要分析问题出在哪个环节。

## 文件结构

| 文件 | 内容 |
|------|--------------|
| **SKILL.md** | 发布策略、平台选择、项目评估、税务/法律信息、简易模式API操作步骤 |
| **[REFERENCE.md](./REFERENCE.md)** | 直接模式概述、费用结构、操作步骤、钱包集成示例、代码模板 |
| **[references/clanker.md](./references/clanker.md)** | Clanker v4 SDK：发布、费用领取、接收者更新、狙击者防护设置 |
| **[references/flaunch.md](./references/flaunch.md)** | Flaunch：发布、费用分配、收益领取、接收者转移 |
| **[references/pumpfun.md](./references/pumpfun.md)** | Pump.fun：手动操作指南、费用分配、代币毕业处理 |

---

## 本工具的作用

- **本工具不提供税务建议**。仅提供一般性信息供参考。
- **本工具不提供法律建议**。代币发布可能涉及证券法相关问题。
- **本工具不能保证盈利**。大多数代币的价值会下降。
- **本工具不是快速致富的工具**。它旨在帮助开发者负责任地发布代币，并保留更多的收益。