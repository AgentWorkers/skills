---
name: torch-prediction-market-bot
version: "2.0.3"
description: 这是一个基于自动化的预言机市场的机器人，专为Solana上的Torch Market设计。该机器人能够创建以Torch代币为交易媒介的二元预言市场：通过“绑定曲线”（bonding curve）来实现价格发现机制；交易费用被存入“金库”（treasury）以积累价值；而“金库”则负责管理所有的交易头寸。每个预言市场都配备了一个预言机（用于提供价格数据，可以是自动的，也可以是人工提供的），并在预设的截止日期前完成交易结算。代理（agent）的密钥对是在运行过程中生成的，属于一次性使用的密钥，不持有任何实际价值。所有与Torch相关的交易都会通过这个“金库”进行处理。人类操作者负责创建并资助这个“金库”，同时保留对其的完全控制权。该系统是基于Torch SDK v3.7.23和Torch Market协议构建的。
license: MIT
disable-model-invocation: true
requires:
  env:
    - name: SOLANA_RPC_URL
      required: true
    - name: VAULT_CREATOR
      required: true
    - name: SOLANA_PRIVATE_KEY
      required: false
metadata:
  clawdbot:
    requires:
      env:
        - name: SOLANA_RPC_URL
          required: true
        - name: VAULT_CREATOR
          required: true
        - name: SOLANA_PRIVATE_KEY
          required: false
  openclaw:
    requires:
      env:
        - name: SOLANA_RPC_URL
          required: true
        - name: VAULT_CREATOR
          required: true
        - name: SOLANA_PRIVATE_KEY
          required: false
    primaryEnv: SOLANA_RPC_URL
    install:
      - id: torch-prediction-market-kit
        kind: npm
        package: torch-prediction-market-kit@^2.0.2
        flags: []
        label: "Install Torch Prediction Market Kit (npm, optional -- SDK is bundled in lib/torchsdk/ and bot source is bundled under lib/kit on clawhub)"
  author: torch-market
  version: "2.0.3"
  clawhub: https://clawhub.ai/mrsirg97-rgb/torch-prediction-market-kit
  kit-source: https://github.com/mrsirg97-rgb/torch-prediction-market-kit
  website: https://torch.market
  program-id: 8hbUkonssSEEtkqzwM7ZcZrD9evacM92TcWSooVF4BeT
  keywords:
    - solana
    - defi
    - prediction-market
    - bonding-curve
    - vault-custody
    - ai-agents
    - agent-wallet
    - agent-safety
    - oracle
    - price-feed
    - token-2022
    - community-treasury
    - solana-agent-kit
    - escrow
    - anchor
    - pda
    - on-chain
    - autonomous-agent
    - torch-market
    - binary-market
    - market-resolution
  categories:
    - solana-protocols
    - defi-primitives
    - prediction-markets
    - agent-infrastructure
    - custody-solutions
compatibility: >-
  REQUIRED: SOLANA_RPC_URL (HTTPS Solana RPC endpoint)
  REQUIRED: VAULT_CREATOR (vault creator pubkey).
  OPTIONAL: SOLANA_PRIVATE_KEY -- the kit generates a fresh disposable keypair in-process if not provided. The agent wallet holds nothing of value (~0.01 SOL for gas). All token creation and seed liquidity SOL routes through the vault. The vault can be created and funded entirely by the human principal.
  This skill sets disable-model-invocation: true -- it must not be invoked autonomously without explicit user initiation.
  The Torch SDK is bundled in lib/torchsdk/ -- all source included for full auditability. No API server dependency.
  Oracle resolution uses CoinGecko public API (read-only, no key required). The vault can be created and funded entirely by the human principal -- the agent never needs access to funds.
---
# Torch预测市场套件

您之所以使用这个套件，是因为您希望在Torch市场上运行预测市场，并且希望这样做是安全的。

每个预测市场都对应一个Torch代币。代币的定价机制基于“绑定曲线”（bonding curve），这是一种自动市场做市（AMM）机制——无需设置流动性提供者（LP），价格确定且交易具有即时流动性。10%的交易费用会被累积到“金库”（treasury）中。用户购买代币来下注“是”（价格上涨），或者出售代币来下注“否”（价格下跌）。在截止日期时，预言机（oracle）会检查结果，并由机器人记录下来。

**结算方式：** 代币本身即作为结算信号。没有额外的支付机制。代币的价格本身就是预测结果。整个结算过程由“绑定曲线”和“金库”来完成。

这就是这个机器人的作用：它读取您的`markets.json`文件，为待创建的市场生成Torch代币，使用您的资金库（vault）为这些市场提供初始流动性，监控价格和交易量，并在截止日期时通过预言机（可以使用CoinGecko的价格数据）来结算交易。所有资金流动都经过您的资金库。执行交易的代理钱包（agent wallet）本身不持有任何资产。

**注意：** 这不是一个仅用于读取数据的工具，而是一个完全可操作的做市商。它会生成自己的密钥对，验证与资金库的连接，创建代币，并在连续的循环中自动完成市场的创建和结算。

---

## 工作原理

### 代理密钥对（Agent Keypair）

机器人每次启动时都会生成一个新的密钥对。没有私钥文件，也没有环境变量需要设置（除非您有特殊需求）。这个密钥对是临时使用的——它用于签署交易，但本身不持有任何价值。

首次运行时，机器人会检查这个密钥对是否已经与您的资金库关联。如果没有关联，它会显示您需要使用的SDK调用命令来建立连接。

**如何关联：** 请从您的权限钱包（硬件钱包、多重签名钱包等）中关联这个密钥对。代理不需要权限钱包的私钥，权限钱包也不需要代理的私钥。它们共享的是资金库，而不是密钥。

### 资金库（Vault）

这个资金库与完整的Torch市场协议中的资金库相同。它存储所有的资产——Solana币（SOL）和代币。代理只是一个临时使用的控制组件。

当机器人创建一个市场时：
- **代币生成**：代理以创建者的身份签署交易，除了交易手续费外不产生额外的Solana币成本。
- **提供初始流动性**：所需的Solana币来自资金库，通过`buildBuyTransaction(vault=creator)`函数提供。
- **购买的代币**：会存入资金库对应的代币账户（ATA）。

人类所有者拥有完全的控制权：
- `withdrawVault()`：可以随时提取Solana币。
- `withdrawTokens(mint)`：可以随时提取市场代币。
- `unlinkWallet(agent)`：可以立即撤销代理的访问权限。

如果代理的密钥对被泄露，攻击者只能得到无价值的代币，并且您可以通过一次交易立即撤销代理的访问权限。

---

## 开始使用

### 1. 安装

或者使用ClawHub提供的打包源代码——Torch SDK包含在`lib/torchsdk/`目录中，机器人源代码位于`lib/kit/`目录下。

### 2. 创建并资助资金库（由人类所有者操作）

从您的权限钱包开始操作：

### 3. 定义市场

创建`markets.json`文件：

### 4. 运行机器人

首次运行时，机器人会显示代理的密钥对以及关联说明。请从您的权限钱包中完成关联，然后重新启动机器人。

### 5. 配置

| 变量 | 是否必需 | 默认值 | 说明 |
|----------|----------|---------|-------------|
| `SOLANA_RPC_URL` | 是 | —— | Solana的RPC端点（HTTPS）。备用值：`RPC_URL` |
| `VAULT_CREATOR` | 是 | —— | 资金库创建者的公钥（pubkey） |
| `SOLANA_PRIVATE_KEY` | 否 | —— | 临时使用的控制器密钥对（base58编码或JSON字节数组）。如果省略，机器人会在启动时生成新的密钥对（推荐） |
| `SCAN_INTERVAL_MS` | 否 | `60000` | 市场周期之间的时间间隔（最小值5000毫秒） |
| `LOG_LEVEL` | 否 | `info` | 日志级别：`debug`、`info`、`warn`、`error` |
| `MARKETS_PATH` | 否 | `./markets.json` | 市场定义文件的路径 |

---

## 架构

这个机器人由大约280行TypeScript代码组成，分布在6个模块中。它的主要功能是创建市场、监控市场状态，并通过资金库完成市场的结算。

### 依赖项

| 包名 | 版本 | 用途 |
|---------|---------|---------|
| `@solana/web3.js` | 1.98.4 | Solana的RPC接口、密钥对处理和交易功能 |
| `torchsdk` | 3.7.23 | 代币查询、代币生成、交易构建和资金库查询功能 |

这两个依赖项都是固定版本的，没有使用`^`或`~`这样的版本范围表示。

---

## 市场生命周期

| 状态 | 说明 |
|--------|-------------|
| **待创建** | 市场已在`markets.json`中定义，但代币尚未生成 |
| **活跃** | 代币已在绑定曲线上生成，用户可以开始交易 |
| **已结算** | 截止日期已过，预言机已检查结果并记录下来（“是”或“否”） |
| **已取消** | 市场在结算前被手动删除 |

### 市场定义

### 输入验证

所有待创建的市场在加载时都会进行验证。任何输入无效的市场都会在进入链上操作之前被拒绝。

| 字段 | 约束条件 | 反例 |
|-------|-----------|-----------------|
| `id` | 必须在所有市场中唯一 | 例如：“sol-200-mar”这样的重复ID |
| `metadataUri` | 域名必须在允许的列表中：`arweave.net`、`gateway.irys.xyz`、`ipfs.io`、`cloudflare-ipfs.com`、`nftstorage.link`、`dweb.link` | 例如：`https://evil.com/payload.json` |
| `initialLiquidityLamports` | 最大为10个Solana币（10,000,000,000 lamports），非负值 | 例如：`50000000000`（50 Solana币） |
| `oracle.asset` | 必须是CoinGecko支持的资产类型（如Solana、Bitcoin、Ethereum等） | 例如：“arbitrary-string” |

这些约束确保了即使`markets.json`文件被泄露，也不会触发不必要的操作（如随意的API调用或资产流失）。

---

## 预言机解决方案

### 基于CoinGecko的价格预言机

这是主要的预言机服务。它用于获取资产的当前价格，并与预设的目标价格进行比较。

- **`asset`**：资产ID（例如：“solana”、“bitcoin”、“ethereum”） |
- **`condition`**：价格条件（“高于”或“低于”） |
- **`target`**：价格阈值（以USD计） |
- **结果**：如果条件满足（例如价格高于目标价格），则结果为“是”；否则为“否” |

### 手动预言机

对于无法通过价格预言机解决的市场，可以使用手动方式。

- 直接修改`markets.json`文件，将`status`字段设置为“resolved”，并将`outcome`字段设置为“yes”或“no”即可。

---

## 资金库的安全模型

Torch市场资金库的安全机制同样适用于这个套件：

- **完全托管**：资金库持有所有的Solana币和代币。代理钱包不持有任何资产。
- **封闭的循环**：用于提供初始流动性的Solana币来自资金库，购买的代币也会存入资金库。没有信息泄露给代理。
- **权限分离**：创建者（使用不可变的PDA密钥对）、权限所有者（可转移的管理员密钥）和代理（临时使用的签名密钥）之间有明确的职责划分。
- **每个钱包只能关联一个资金库**：代理只能属于一个资金库。PDA密钥的唯一性在链上得到了保障。
- **任何人都可以向资金库充值**：任何人都可以向资金库添加资金。代理负责创建市场。
- **即时撤销权限**：权限所有者可以随时撤销代理的访问权限。只需一次交易即可完成。

### 市场创建的封闭经济循环

- **资金流动方向**：
  - Solana币从资金库流向绑定曲线（用于提供初始流动性）。
  - 购买的代币会存入资金库对应的代币账户（ATA）。
- **费用积累**：每次交易会有10%的费用被累积到资金库中。

机器人使用了Torch SDK中的部分功能：

| 函数 | 用途 |
|----------|---------|
| `getVault(connection, creator)` | 启动时验证资金库是否存在 |
| `getVaultForWallet(connection, wallet)` | 验证代理是否已与资金库关联 |
| `buildCreateTokenTransaction(connection, params)` | 为新市场构建代币生成交易 |
| `buildBuyTransaction(connection, params)` | 通过资金库路由构建购买交易以提供初始流动性 |
| `getToken(connection, mint)` | 获取市场的代币价格、交易量和状态信息 |
| `getHolders(connection, mint)` | 获取市场的持有者数量信息 |
| `confirmTransaction(connection, sig, wallet)` | 通过RPC在链上确认交易（验证签名者并检查Torch协议的指令） |

---

## 签名和密钥安全

**资金库是安全边界，而不是密钥本身。**

代理的密钥对在每次启动时都会使用`Keypair.generate()`函数生成。它仅持有大约0.01 Solana币作为交易手续费。如果密钥被泄露，攻击者只能得到这些手续费，且权限所有者可以通过一次交易立即撤销代理的访问权限。

**重要规则：**
1. **绝不要向用户索取他们的私钥或助记词。** 权限所有者始终在自己的设备上进行签名操作。
2. **不要记录、打印、存储或传输私钥信息。** 代理的密钥对仅在运行时存在于内存中。
3. **不要将密钥嵌入源代码或日志中。** 代理的公钥信息仅用于显示，私钥永远不会被暴露。
4. **使用安全的RPC端点。** 默认使用私有的RPC服务提供商。在主网交易中绝不要使用未加密的HTTP端点。

### RPC超时设置

所有SDK调用都设置了30秒的超时限制（在`utils.ts`中实现）。如果RPC端点响应延迟或无法响应，机器人会立即停止当前操作并切换到下一个市场或下一个处理周期。

### 环境变量

| 变量 | 是否必需 | 用途 |
|----------|----------|---------|
| `SOLANA_RPC_URL` | 是 | Solana的RPC端点（HTTPS） |
| `VAULT_CREATOR` | 是 | 资金库创建者的公钥 |
| `SOLANA_PRIVATE_KEY` | 否 | 可选：如果省略，机器人会在启动时生成新的密钥对（推荐） |

### 外部依赖服务

机器人会向外部服务发送HTTPS请求。其中三个服务的使用情况如下：

| 服务 | 用途 | 调用时机 | 机器人是否使用？ |
|---------|---------|------------|-----------|
| **CoinGecko** (`api.coingecko.com`) | 用于获取资产价格（预言机功能） | 在`oracle.ts`中调用`checkPriceFeed()`和`getToken()` | 是 |
| **Irys Gateway** (`gateway.irys.xyz`) | 用于获取代币元数据（名称、符号、图片） | 当链上元数据URL指向Irys时调用`getToken()` | 是 |
| **SAID Protocol** (`api.saidprotocol.com`) | 用于验证代理身份和信任等级 | 仅在`verifySaid()`函数中使用 | 否 |

#### CoinGecko API详情

预言机模块`oracle.ts`直接调用CoinGecko的公共API：

- **无需API密钥**：使用免费的公共端点。
- **调用限制**：免费账户每分钟最多调用10-30次。
- **发送的数据**：仅包含资产ID（例如“solana”）。
- **返回的数据**：`{"solana": "87.76"}`。
- **异常处理**：如果CoinGecko无法访问，`checkPriceFeed()`会失败，市场将进入等待状态，直到下一个周期。

`confirmTransaction()`函数不会调用SAID API。尽管它位于SDK的`said.js`模块中，但它仅使用`connection.getParsedTransaction()`（Solana的RPC接口）来确认交易是否成功，并确定事件类型。不会向CoinGecko发送任何数据。

**注意：** 没有任何敏感信息（如私钥）会被发送到CoinGecko或Irys。

---

## 日志输出

---

## 测试说明

测试需要运行[Surfpool](https://github.com/txtx/surfpool)主网分支：

**测试结果：** 9项测试通过，1项提示信息（Surfpool在`getTokenLargestAccounts`函数上存在限制，但在主网上可以正常使用）。

| 测试项 | 需要验证的内容 |
|------|-------------------|
| Connection | 是否能连接到RPC服务器 |
| loadMarkets | 是否能正确解析和验证市场文件 |
| checkPriceFeed | 是否能从CoinGecko获取有效的价格数据 |
| buildCreateTokenTransaction | 是否能正确构建代币生成交易 |
| getTokens | 是否能获取代币的元数据、价格和状态 |
| getHolders | 是否能获取市场持有者信息（在Surfpool的限制下可能会失败） |
| getVaultForWallet | 未关联的钱包是否返回空值 |
| 是否需要外部密钥对 | 运行过程中是否需要外部密钥对 |

---

## 错误代码

- `VAULT_NOT_FOUND`：指定的创建者对应的资金库不存在。
- `WALLET_NOT_LINKED`：代理钱包未与资金库关联。
- `INVALID_MINT`：找不到对应的代币。
- `BONDING_COMPLETE`：代币已经生成完成，应通过DEX进行交易。
- `NAME_TOO_LONG`：代币名称超过32个字符。
- `SYMBOL_TOO_LONG`：代币符号超过10个字符。

---

## 链接资源

- 预测市场套件（源代码）：[github.com/mrsirg97-rgb/torch-prediction-market-kit](https://github.com/mrsirg97-rgb/torch-prediction-market-kit)
- 预测市场套件（npm包）：[npmjs.com/package/torch-prediction-market-kit](https://www.npmjs.com/package/torch-prediction-market-kit)
- Torch SDK（打包版本）：`lib/torchsdk/`（包含在套件中）
- Torch SDK（源代码）：[github.com/mrsirg97-rgb/torchsdk](https://github.com/mrsirg97-rgb/torchsdk)
- Torch SDK（npm包）：[npmjs.com/package/torchsdk](https://www.npmjs.com/package/torchsdk)
- Torch市场协议相关资源：[clawhub.ai/mrsirg97-rgb/torchmarket](https://clawhub.ai/mrsirg97-rgb/torchmarket)
- 白皮书：[torch.market/whitepaper.md](https://torch.market/whitepaper.md)
- 安全审计报告：[torch.market/audit.md](https://torch.market/audit.md)
- 官网：[torch.market](https://torch.market)
- 程序ID：`8hbUkonssSEEtkqzwM7ZcZrD9evacM92TcWSooVF4BeT`

---

## 更新日志

### v2.0.0

- **将Torch SDK版本从3.2.3升级到3.7.23**。主要更新包括：新增金库锁定机制（V27）、动态检测Raydium网络、在绑定曲线完成时自动迁移代币（`buildBuyTransaction`现在返回`migrationTransaction`参数）、通过资金库路由的Raydium CPMM交易（`buildVaultSwapTransaction`）、Token-2022版本的费用收集功能（`buildHarvestFeesTransaction`、`buildSwapFeesToSolTransaction`）、批量查询贷款信息（`getAllLoanPositions`）、链上代币元数据查询（`getTokenMetadata`）以及临时代理密钥对生成功能（`createEphemeralAgent`）。
- **新增`withTimeout`辅助函数**：机器人内部使用的超时设置现在作为套件的公开功能，可供其他开发者使用。
- **更新了环境变量格式**：环境变量声明采用了结构化的`name`/`required`格式，以兼容ClawHub和OpenClaw等平台。

### v1.0.2

- **更新了套件配置**：`index.js`文件现在从本地的`lib/torchsdk/`目录导入SDK，确保使用的是套件中包含的特定版本（3.2.3）。
- **修复了审计问题L-3**。

### v1.0.1

- **为所有外部调用设置了超时限制**：所有SDK调用、RPC请求和API调用都设置了30秒的超时限制（CoinGecko请求为10秒）。如果RPC端点响应延迟或无法响应，系统会立即失败并显示错误信息，而不会无限期地停滞。
- **修复了审计问题L-2**：`loadMarkets()`函数现在会拒绝包含重复市场ID的`markets.json`文件，防止重复创建市场或浪费资金库中的Solana币。

这个机器人的存在是因为预测市场需要相应的基础设施。Torch的绑定曲线提供了即时流动性和确定性的价格机制，且无需设置流动性提供者。资金库确保了交易的安全性——所有资金都存放在托管账户中，风险得到控制，且所有密钥都由人类所有者保管。代币的价格本身就是预测结果。