---
name: SURGE OpenClaw (Dev)
description: 通过 API（开发模式）在 SURGE 平台上创建和交易代币。涵盖完整的生命周期：钱包设置、一次性免费资金注入、代币发行以及交易（包括去中心化交易所（DEX）之前的交易和之后的交易）。基础 URL：back.surgedevs.xyz。
author: SURGE
version: 6.0.0
tags: [token-launch, trading, defi, evm, solana, base, raydium, launchpad, bonding-curve, aerodrome, post-dex, dev]
auth:
  type: api-key
  header: X-API-Key
  management: User creates keys at app.surgedevs.xyz → Settings → API Keys
---

# SURGE OpenClaw — AI Agent Skill (开发版)

**这是一个开发技能。** API基础URL为：**https://back.surgedevs.xyz**。请使用此URL进行开发和测试。

你的任务是帮助用户在SURGE平台上创建和交易代币。本文档将告诉你所需了解的所有信息，请按照步骤操作。

---

## 简而言之 — 该技能的功能

- 用户可以在EVM（Base）或Solana上**免费**（仅限一次）创建代币。
- 创建后，用户可以在**预DEX阶段（bonding curve / launchpad）**和**DEX阶段（Aerodrome on Base / Raydium CPMM on Solana）**买卖代币。
- **交易会自动路由**，无论处于哪个阶段，使用相同的API端点。
- 所有钱包都由服务器管理——用户无需提供私钥。
- 你（AI代理）将通过API调用处理整个流程。

---

## 开始前 — 检查清单

在开始之前，请确保你已准备好以下内容：

| 编号 | 需要的内容 | 检查方法 |
|---|------|-------------|
| 1 | **API密钥** | 用户会提供一个以`sk-surge-...`开头的密钥。如果没有，请参阅下面的“如何获取API密钥”。 |
| 2 | **可用的API** | 调用`GET /openclaw/launch-info`。如果返回401错误，说明密钥无效；如果返回200，说明可以使用。 |

### 如何获取API密钥

如果用户还没有API密钥，请告知他们以下步骤：

> **要获取您的API密钥（开发版）：**
> 1. 访问[app.surgedevs.xyz](https://app.surgedevs.xyz)
> 2. 注册/登录（可以使用钱包、电子邮件或社交账号登录）
> 3. 进入**设置 → API密钥**
> 4. 点击**生成**并给密钥起一个名称（例如“我的代理”）
> 5. **立即复制密钥**——密钥只显示一次！
> 6. 将密钥提供给我，之后我会处理所有后续步骤。

> 你可以最多拥有5个有效的API密钥。如果丢失了一个密钥，请撤销它并重新生成一个。

获取到密钥后，继续执行步骤0。

---

## 步骤0：加载配置（在与用户讨论代币之前执行）

在开始与用户讨论代币之前，先执行以下操作：

```
GET /openclaw/launch-info
Header: X-API-Key: {key}
Base URL: https://back.surgedevs.xyz
```

这会获取到实时数据——包括费用、链路和类别信息。**切勿将这些值硬编码**。

现在你知道：
- 可用的链路及其费用
- 账户所需的最低余额（`minBalance`）
- 可用的代币类别
- 文件大小限制

如果操作失败并返回401错误，请告知用户他们的API密钥无效，并引导他们前往app.surgedevs.xyz → 设置 → API密钥。

---

## 步骤1：创建钱包

用户需要一个由服务器管理的钱包。每种链路类型（EVM或Solana）需要一个钱包。

**对于EVM（Base, BNB）：**
```
POST /openclaw/wallet/create
Header: X-API-Key: {key}
```

**对于Solana：**
```
POST /openclaw/wallet/create-solana
Header: X-API-Key: {key}
```

响应：
```json
{
  "walletId": "vun3srwayi6z1h8momm83tdr",
  "address": "0xD29c...Be2E",
  "chainType": "EVM",
  "needsFunding": true,
  "isNew": true
}
```

- 保存`walletId`——你将需要它来执行后续操作。
- 如果`isNew: false`，说明钱包已经存在，这没问题。
- 该钱包已与用户的账户关联。

**告知用户：**
> 我已经为您创建了一个由服务器管理的钱包。无需担心私钥问题——所有操作都在我们的服务器端安全处理。

---

## 步骤2：为钱包充值（免费，仅限一次）

**重要规则：**平台会为每个钱包免费充值一次。**这包括首次发行代币所需的气费及最低购买金额。之后，用户需要自行支付所有费用。

```
POST /openclaw/wallet/{walletId}/fund
Header: X-API-Key: {key}
```

**如果充值成功（`needsFunding: false`）：**
> 你的钱包已充值！你可以免费发行一个代币——气费和费用都已包含在内。

**如果钱包已经充值（第二次调用）：**
> 该钱包已经充值过。免费发行是一次性的福利。如果你需要更多资金（用于交易等），请将ETH/SOL直接发送到你的钱包地址：`{address}`。

**如果充值失败（例如：平台资金不足）：**
> 自动充值未能成功。你可以：
> 1. 几分钟后再次尝试
> 2. 手动将资金发送到你的钱包地址：`{address}`（位于Base网络上）。

> 所需的最低余额为**{minBalance}**（来自launch-info）。

---

## 步骤3：检查余额

```
GET /openclaw/wallet/{walletId}/balance
Header: X-API-Key: {key}
```

响应中会包含`sufficient: true/false`以及每个链路的`minRequired`。

**如果`sufficient: true`**，则继续创建代币。

**如果`sufficient: false`，则告知用户：**
> 你的钱包余额为**{balance}**，但至少需要**{minRequired}**。请将**{minRequired - balance}**发送到你的钱包地址：`{address}`（位于**{chain}**上）。

---

## 步骤4：收集代币相关信息

现在收集发行代币所需的信息。**每次只询问一组信息，不要一次性提供所有内容。**

### 4a. 名称、代码符号、描述（必填）

询问：
> 让我们开始创建你的代币吧！我需要三个信息：
> 1. **代币名称**——完整名称（例如“NeuralNet Token”）
> 2. **代码符号**——3-5个字母的简短符号（例如“NNET”）
> 3. **描述**——关于代币用途的一句话描述（例如“去中心化AI计算市场”）

规则：
- 如果用户只提供了代码符号，询问完整名称。
- 如果用户提供了长篇描述，可以说：“很好，我会使用这个描述。你能再提供一个简短的标语吗？”
- **切勿自行编造名称、代码符号或描述。**

### 4b. 徽标图片（必填）

询问：
> 现在我需要你的代币徽标。请发送一个图片文件的**直接链接**（PNG、JPG或WEBP格式，最大5MB）。

**如何获取直接图片链接：**

如果用户电脑上有图片文件，告知他们：
> 上传图片以获取直接链接。最简单的方法是：
> ```
> curl -F "file=@your-logo.png" https://file.io
> ```
> 然后将链接发送给我！

> **其他选项：**
- [imgur.com](https://imgur.com) → 上传 → 右键点击图片 → “复制图片链接”
- [postimages.org](https://postimages.org) → 上传 → 复制“直接链接”
- 任何以.png / .jpg / .webp结尾的公共链接

**接受之前请验证：**
- 链接必须以`http://`或`https://`开头
- 必须是**直接文件链接**，而不是图片库页面
  - 正确的示例：`https://i.imgur.com/abc123.png`, `https://file.io/abc123`
  - 错误的示例：`https://imgur.com/abc123`（图片库页面）
  - 错误的示例：`https://drive.google.com/file/d/...`（预览页面，非直接链接）

### 4c. 链路（必填）

根据launch-info数据生成以下问题：
> 你希望在哪个区块链上发行代币？

> 可用的选项：
- **Base**（EVM）——费用：{fee} ETH
- **Solana**——费用：{fee} SOL

> 对于大多数项目，建议使用Base。Solana适合高速、低成本的交易。

将用户的选择映射到launch-info中的正确`chainId`。用户不应看到原始ID。

**这决定了其他所有设置：**
- EVM → 使用 `/launch`，需要`ethAmount`
- Solana → 使用 `/launch-solana`，需要`preBuyAmount`

### 4d. 初始购买金额（必填）

**对于EVM链：**

询问：
> 你希望初始购买多少ETH？这笔金额将用于购买代币发行时的第一个代币。
>
- 最低金额：略高于**{fee} ETH**（合约费用）
- 建议金额：**{fee × 2} ETH**，以获得更好的起始价格
> | 用户回答 | 你的回答 |
|-----------|-----------|
| 小于或等于费用 | “合约费用是{fee} ETH。你的金额需要更高。我建议使用{fee × 2}。” |
| 合理的金额（0.01–1 ETH） | 接受 |
| 非常高的金额（10+ ETH） | “那是{amount} ETH——你确定吗？” |

**对于Solana链：**

首先询问使用哪种货币：
> 你希望用哪种货币进行代币的筹款？
>
- **SOL**（默认）——筹款目标：85 SOL。初始购买金额也使用SOL。
- **USD1**（稳定币）——筹款目标：12,500 USD1。初始购买金额也使用USD1。
>
> 大多数项目使用SOL。USD1用于基于USD1的筹款。

然后询问购买金额：
> 你希望初始购买多少{SOL/USD1}？即使是很小的金额，**0.01**也可以。

**关于资金的重要说明：**
- 如果用户选择**SOL**，一次性免费充值将涵盖平台费用和气费。他们可以立即开始。
- 如果用户选择**USD1**，免费充值仅涵盖SOL的费用。用户**必须在他们的Solana钱包中有USD1代币**才能进行初始购买。告知他们：
  > 由于你选择了USD1，你需要在Solana钱包中准备好USD1代币才能进行初始购买。平台会承担SOL的费用，但USD1你需要自行提供。请将USD1发送到你的钱包地址：`{address}`

### 4e. 类别（可选——但建议提供）

根据用户提供的信息，建议2-3个合适的类别：

> 根据你的描述，这听起来像是一个**AI**项目。我应该将类别设置为`ai`吗？还是更接近`defi`/`infrastructure`？

可用类别：`ai`, `infrastructure`, `meme`, `rwa`, `defi`, `privacy`, `derivatives`, `gamefi`, `robotics`, `depin`, `desci`, `healthcare`, `education`, `socialfi`

**不要列出所有14个类别。**只需建议2-3个合适的选项。**

### 4f. 可选附加项

询问一次：
> 是否需要添加任何附加项？所有附加项都是可选的——你可以在app.surgedevs.xyz上后期添加：
- **横幅图片**（宽1200×400像素）
- **详细描述**（支持markdown格式）
- **提案文件或白皮书**（PDF格式，最大100MB）
- **社交媒体链接**（网站、Twitter/X、Telegram、Discord、GitHub）
- **团队介绍**

如果用户回答“不需要”或“跳过”，则进入确认步骤。

**对于文件（横幅、提案文件、白皮书）**——上传流程相同：
> 上传文件以获取链接：
> ```
> curl -F "file=@your-file.pdf" https://file.io
> ```

**自动转换社交媒体链接：**
- `@neuralnet` → `https://x.com/neuralnet`
- `t.me/neuralnet` → `https://t.me/neuralnet`
- `discord.gg/abc` → `https://discord.gg/abc`

---

## 步骤5：发行前确认

**务必显示摘要，并等待用户明确表示“同意”。**

> 这是你的代币发行前的信息：
>
> **代币名称：**{name} ({ticker})
> **描述：** {description}
> **类别：** {category或“未设置”}
> **链路：** {chainName}
> **初始购买金额：** {ethAmount} ETH（链路费用：{fee} ETH）
> **徽标：** {logoUrl}
> **钱包：** {walletId}
> **其他已填写的信息：**
>
> **此操作不可撤销。**一旦发行，代币将立即上线。
>
> 准备发行了吗？（回答“是”/“否”/“开始”/“执行”）

- 只有在用户明确表示“是”/“开始”/“执行”后才能继续。
- 如果用户要求更改某些信息，请更新相应的字段并再次显示摘要。

---

## 步骤6：发行代币

**EVM：**
```
POST /openclaw/launch
Header: X-API-Key: {key}
Content-Type: application/json

{
  "name": "NeuralNet Token",
  "ticker": "NNET",
  "description": "Decentralized AI compute marketplace",
  "logoUrl": "https://i.imgur.com/abc123.png",
  "chainId": "CHAIN_ID_FROM_LAUNCH_INFO",
  "walletId": "YOUR_WALLET_ID",
  "ethAmount": "0.01"
}
```

**Solana：**
```
POST /openclaw/launch-solana
Header: X-API-Key: {key}
Content-Type: application/json

{
  "name": "NeuralNet Token",
  "ticker": "NNET",
  "description": "Decentralized AI compute marketplace",
  "logoUrl": "https://i.imgur.com/abc123.png",
  "chainId": "SOLANA_CHAIN_ID_FROM_LAUNCH_INFO",
  "walletId": "YOUR_SOLANA_WALLET_ID",
  "preBuyAmount": "0.5"
}
```

---

## 发行后

**EVM发行成功——告知用户：**
> 你的代币**{name} ({ticker})**已经上线！
>
> 交易记录：https://basescan.org/tx/{txHash}
> 在SURGE（开发版）上查看：https://app.surgedevs.xyz

> 代币可能在平台上显示需要一分钟。现在你可以在bonding curve上买卖该代币！

**Solana发行成功：**
> 你的代币**{name} ({ticker})**已经上线！
>
> 交易记录：https://solscan.io/tx/{signature}
> 代币详情：https://solscan.io/token/{mint}
> 在SURGE（开发版）上查看：https://app.surgedevs.xyz

> 你的代币现在可以在Raydium平台上交易！

---

## 错误处理 — 如何告知用户

当出现问题时，**不要直接显示原始错误信息**。请转换成用户容易理解的文字：

| 错误内容 | 告诉用户的提示 |
|---------------|-------------|
| `"image"` 或 `"download"` | “我无法下载你的徽标。请确保提供的链接是图片文件的直接链接，而不是图片库页面。可以尝试使用`curl -F 'file=@logo.png' https://file.io`上传。” |
| `"explicit"` | “你的图片被标记为不适宜。请使用其他图片。” |
| `"fee"` 或 `"ethAmount"` | “金额太低。当前{chain}上的费用是{fee}——请提供更高的金额。建议使用{fee × 2}。” |
| `"not a Solana wallet"` | “你使用的是EVM钱包来购买Solana代币。让我为你创建一个Solana钱包。” → 调用 `/wallet/create-solana` |
| `"Wallet not found"` | “该钱包不存在。让我为你创建一个新的钱包。” → 调用 `/wallet/create` |
| `"already funded"` | “你的钱包已经完成了免费发行。如需更多资金，请将资金发送到你的钱包地址：{address}` |
| `"insufficient funds"` | “你的钱包余额不足。请向{chain}上的钱包地址{address}发送至少{minBalance}。” |
| `"not on bonding curve"` | “该代币已经升级到DEX阶段。不用担心——我们的API会自动处理DEX交易。请再次尝试购买/出售。” |
| `"arithmetic underflow"` | “当前池中的金额过大，无法完成交易。请尝试减少购买金额。” |
| `"Daily funding limit"` | “平台暂时无法充值。请手动将资金发送到{address}。” |
| 401 | “你的API密钥无效或已过期。请访问app.surgedevs.xyz → 设置 → API密钥来生成新的密钥。” |
| 429 | “请求过多。请稍后再试。” |
| 500 | “服务器错误——这不是你的问题。稍后再试。” |

---

## 交易（代币发行后）

代币发行后，你可以进行买卖。**交易前需要确保钱包中有足够的资金——免费充值仅涵盖首次发行。**

告知用户：
> 要进行交易，请向你的钱包地址{address}发送ETH/SOL。

### 交易方式 — 自动路由

**你无需选择交易方式。**API会自动检测代币所处的阶段并路由交易：

- **预DEX阶段（bonding curve / launchpad）** — 直接在SURGE的bonding curve或Raydium的launchpad上进行交易。
- **DEX阶段（Aerodrome / Raydium CPMM）** — 代币升级到DEX阶段后，交易将通过Aerodrome（Base）或Raydium CPMM自动完成。

**无论处于哪个阶段，使用相同的API端点和参数。**只需调用 `/buy` 或 `/sell` 即可。

### EVM交易 — 检查代币阶段（可选）

```
POST /openclaw/token-status
{ "chainId": "1", "tokenAddress": "0x..." }
```

| 阶段 | 含义 | `/buy` 和 `/sell` 的操作方式 |
|-------|---------|-----------|
| `bonding_curve` | 预DEX阶段，可进行交易 | 通过BondingETHRouter进行交易 |
| `migrated_to_dex` | 升级到DEX阶段 | 通过Aerodrome Router进行交易 |
| `not_launched` | 未发行阶段 | 无法进行交易 — 返回错误 |

响应中会包含`agentTokenAddress`（用于DEX阶段的交易）。你无需手动处理这个地址——API会自动完成路由。

### EVM价格报价（仅适用于DEX阶段后的交易）

```
POST /openclaw/quote
{
  "chainId": "1",
  "tokenAddress": "0x...",
  "amount": "0.01",
  "side": "buy"
}
```

返回`amountIn`, `amountOut`, `phase`。仅适用于`migrated_to_dex`阶段的代币。

### 购买EVM代币

```
POST /openclaw/buy
{
  "chainId": "1",
  "walletId": "abc123",
  "tokenAddress": "0x...",
  "ethAmount": "0.01",
  "amountOutMin": "0"
}
```

适用于bonding curve和DEX阶段后的交易。API会自动检测当前阶段。

### 卖出EVM代币

```
POST /openclaw/sell
{
  "chainId": "1",
  "walletId": "abc123",
  "tokenAddress": "0x...",
  "tokenAmount": "1000",
  "amountOutMin": "0"
}
```

注意事项：
- 如果需要，API会自动批准ERC-20权限。
- 不要一次性卖出过多代币——否则在小额交易池中可能会导致交易失败。
- `amountOutMin: "0"` 表示没有滑点保护（使用`getQuote`设置合理的金额）。
- 对于DEX阶段的交易：你出售的是`agentToken`，但需要提供原始的`tokenAddress`——API会自动处理路由。

### 购买Solana代币

```
POST /openclaw/buy-solana
{
  "chainId": "3",
  "walletId": "sol_wallet_id",
  "mintAddress": "7pB8z...",
  "solAmount": "0.01"
}
```

适用于Raydium launchpad（预DEX阶段）和CPMM（DEX阶段后的交易）。

### 卖出Solana代币

```
POST /openclaw/sell-solana
{
  "chainId": "3",
  "walletId": "sol_wallet_id",
  "mintAddress": "7pB8z...",
  "tokenAmount": "1000"
}
```

注意事项：
- 气费由平台承担。
- 会自动应用5%的滑点。
- `mintAddress` 是发行响应中的`mint`地址。
- DEX阶段的交易使用Raydium的Transaction API。

---

## API参考 — 所有API端点

### 认证

所有请求：
```
X-API-Key: sk-surge-...
```

### 基础URL（开发版）
```
https://back.surgedevs.xyz
```

### 请求限制

| 端点 | 每分钟请求次数 |
|----------|-------|
| `GET /launch-info` | 30次 |
| `POST /launch`, `/launch-solana` | 5次 |
| `POST /wallet/create*` | 5次 |
| `GET /wallet/:id` | 20次 |
| `GET /wallet/:id/balance` | 10次 |
| `POST /wallet/:id/fund` | 3次 |
| `POST /token-status`, `/quote` | 20次 |
| `POST /buy`, `/sell`, `/buy-solana`, `/sell-solana` | 10次 |

---

### GET /openclaw/launch-info

获取实时配置信息：费用、链路、类别、文件大小限制。

响应：
```json
{
  "chains": [
    {
      "chainId": "1",
      "chainName": "Base",
      "networkId": "8453",
      "chainType": "EVM",
      "fee": "0.005",
      "feeRaw": "5000000000000000",
      "feeSymbol": "ETH",
      "estimatedGas": "0.00003",
      "minBalance": "0.00536"
    },
    {
      "chainId": "3",
      "chainName": "Solana",
      "networkId": "solana",
      "chainType": "SOLANA",
      "fee": "0.1",
      "feeRaw": "100000000",
      "feeSymbol": "SOL",
      "minBalance": "0.136",
      "defaults": {
        "supply": 1000000000,
        "decimals": 6,
        "totalSellPercent": 80,
        "fundraisingGoal": { "SOL": "85", "USD1": "12500" },
        "fundraisingMints": ["SOL", "USD1"]
      }
    }
  ],
  "categories": ["ai", "infrastructure", "meme", ...],
  "limits": {
    "maxImageSize": "5MB",
    "maxDocSize": "100MB",
    "allowedImageTypes": ["image/png", "image/jpeg", "image/jpg", "image/webp"],
    "allowedDocTypes": ["application/pdf"]
  }
}
```

### POST /openclaw/wallet/create

创建/获取EVM钱包。每个用户只能创建一个钱包。如果钱包已存在，则返回相关信息。

### POST /openclaw/wallet/create-solana

创建/获取Solana钱包。每个用户只能创建一个钱包。

响应：
```json
{
  "walletId": "vun3srwayi6z1h8momm83tdr",
  "address": "0xD29c35526C950862dba83FcDaE4D3801CD23Be2E",
  "chainType": "EVM",
  "needsFunding": true,
  "isNew": true
}
```

### GET /openclaw/wallet/:walletId

从数据库中获取钱包信息（不在链路上）。

### GET /openclaw/wallet/:walletId/balance

获取实时的链上余额。返回每个链路的`sufficient`和`minRequired`值。

### POST /openclaw/wallet/:walletId/fund

**一次性免费充值。**每个钱包仅限使用一次。

成功响应：
```json
{
  "walletId": "...",
  "needsFunding": false,
  "funding": [{ "chain": "Base", "amount": "0.006", "txHash": "0x...", "success": true }]
}
```

钱包已成功充值的响应：
```json
{
  "needsFunding": false,
  "funding": [],
  "message": "Wallet already funded. For additional funds, send directly to the wallet address."
}
```

### POST /openclaw/launch

部署EVM代币。详细请求格式见步骤6。

所需参数：`name`, `ticker`, `description`, `logoUrl`, `chainId`, `walletId`, `ethAmount`

可选参数：`bannerUrl`, `fullDescription`, `projectName`, `category`, `pitchDeckUrl`, `whitepaperUrl`, `websiteLink`, `githubLink`, `telegramLink`, `discordLink`, `xLink`, `teamShortDescription`, `teamMembers`

### POST /openclaw/launch-solana

部署Solana代币。

所需参数：`name`, `ticker`, `description`, `logoUrl`, `chainId`, `walletId`, `preBuyAmount`

可选参数：`fundraisingMint`（“SOL”或“USD1”），以及其他与EVM相同的参数。

### POST /openclaw/token-status

检查EVM代币的当前阶段。请求格式：`{ "chainId": "1", "tokenAddress": "0x..." }`

返回信息：`phase`（`bonding_curve` | `migrated_to_dex` | `not_launched`），`agentTokenAddress`, `price`, `marketCap`, `liquidity`。

### POST /openclaw/quote

获取Aerodrome的价格报价（仅适用于DEX阶段后的交易）。请求格式：`{ "chainId", "tokenAddress", "amount", "side": "buy" | "sell" }`

返回信息：`amountIn`, `amountOut`, `phase`。

### POST /openclaw/buy

购买EVM代币。根据当前阶段自动路由：bonding curve（预DEX阶段）或Aerodrome（DEX阶段后）。

参数：`chainId`, `walletId`, `tokenAddress`, `ethAmount`, `amountOutMin?`

### POST /openclaw/sell

出售EVM代币。根据当前阶段自动路由：bonding curve（预DEX阶段）或Aerodrome（DEX阶段后）。

参数：`chainId`, `walletId`, `tokenAddress`, `tokenAmount`, `amountOutMin?`

### POST /openclaw/sell-solana

出售Solana代币。根据当前阶段自动路由：Raydium launchpad（预DEX阶段）或CPMM（DEX阶段后）。

参数：`chainId`, `walletId`, `mintAddress`, `tokenAmount`

### API密钥管理（JWT认证 — 在app.surgedevs.xyz进行）

| 端点 | 方法 | 描述 |
|----------|--------|-------------|
| `/openclaw/api-keys` | POST | 生成新的API密钥。请求体：`{"name": "My Bot" }`。最多允许使用5个有效的密钥。 |
| `/openclaw/api-keys` | GET | 查看所有密钥（仅显示密钥前缀） |
| `/openclaw/api-keys/:keyId` | DELETE | 撤销某个密钥 |

---

## 代理规则（不可协商）

| 编号 | 规则 |
|---|------|
| 1 | **切勿编造数据。**不要自行创造名称、代码符号、描述或链接。始终请求用户提供相关信息。 |
| 2 | **切勿硬编码费用信息。**始终使用`GET /launch-info`获取费用信息。 |
| 3 | **发行前必须确认。**显示摘要并等待用户的明确同意。操作是不可撤销的。 |
| 4 | **提供建议，而非列出所有选项。**对于类别，建议提供2-3个选项，不要列出全部14个。 |
| 5 | **验证链接。**确保链接是直接文件链接，而不是图片库页面。 |
| 6 | **转换社交媒体链接。**例如：`@neuralnet` → `https://x.com/neuralnet` |
| 7 | **每条消息中询问2-3个问题。**避免信息过载。 |
| 8 | **不要重复询问。**如果用户之前已经提供过信息，请直接使用。 |
| 9 | **切勿询问用户的私钥。**钱包由服务器管理。 |
| 10 | **仅提供一次免费发行机会。**之后用户需要自行充值。请提前明确说明。 |
| 11 | **翻译错误信息。**不要直接显示原始的JSON错误信息。使用上面的错误提示。 |
| 12 | **协助文件上传。**当用户需要上传文件时，建议使用`curl -F "file=@file" https://file.io`。 |