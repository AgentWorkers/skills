---
name: torch-prediction-market-bot
version: "2.0.2"
description: 这是一个基于自动保险库（vault）的预测市场机器人，专为Solana上的Torch Market平台设计。该机器人能够创建以Torch代币为交易对象的二元预测市场；保险库（vault）通过价格发现机制（bonding curve）来管理市场价格，同时通过交易费用积累价值，并负责管理用户的交易头寸。每个预测市场都配备了一个价格数据源（oracle，可以是自动提供的，也可以是手动设置的），并在预设的截止日期前完成交易结算。该机器人的代理密钥对（agent keypair）是在运行过程中生成的，属于一次性使用的密钥，不存储任何有价值的数据。所有与Solana相关的交易操作（SOL币的交易）都必须通过保险库进行。用户（人类操作者）负责创建保险库、为其注入资金、关联相应的代理，并保持对整个系统的完全控制权。该机器人是基于Torch SDK v3.7.23和Torch Market协议开发的。
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
        package: torch-prediction-market-kit@^2.0.1
        flags: []
        label: "Install Torch Prediction Market Kit (npm, optional -- SDK is bundled in lib/torchsdk/ and bot source is bundled under lib/kit on clawhub)"
  author: torch-market
  version: "2.0.2"
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

每个预测市场都对应一个Torch代币。代币的定价机制基于“绑定曲线”（bonding curve），这是一种自动做市商（AMM）机制——无需设置流动性提供者（LP），价格确定，且具有即时流动性。10%的交易费用会被累积到“金库”（treasury）中。用户购买代币来下注“是”（价格上升），或者出售代币来下注“否”（价格下降）。在截止日期时，预言机（oracle）会检查结果，并由机器人记录下来。

**结算方式：** 代币本身就是结算信号。没有额外的支付机制。代币的价格本身就是预测结果。整个结算过程由绑定曲线和金库来完成。

这就是这个机器人的作用：它读取您的`markets.json`文件，为待定的市场创建Torch代币，从您的金库中注入初始流动性，监控价格和交易量，并在截止日期时通过预言机（使用CoinGecko的价格数据）来结算市场。所有的资金流动都通过您的金库进行。处理交易的代理钱包（agent wallet）本身不持有任何代币。

**这不仅仅是一个只用于读取数据的工具。** 这是一个完全可操作的做市商，它可以生成自己的密钥对，验证与金库的连接，创建代币，并在持续循环中自动结算市场。

---

## 工作原理

### 代理密钥对（Agent Keypair）

机器人每次启动时都会生成一个新的密钥对。没有私钥文件，也没有环境变量（除非您特别指定）。这个密钥对是临时使用的——它用于签署交易，但本身不持有任何价值。

首次运行时，机器人会检查这个密钥对是否已经与您的金库关联。如果没有关联，它会显示您需要使用的SDK调用命令来建立连接。

**如何关联：** 从您的授权钱包（硬件钱包、多重签名钱包等）中导入密钥对。代理不需要授权钱包的密钥，授权钱包也不需要代理的密钥。它们共享同一个金库，但密钥是分开的。

### 金库（Vault）

这个金库与完整的Torch市场协议中的金库相同。它存储所有的资产——Solana令牌（SOL）和代币。代理只是一个临时使用的控制器。

当机器人创建一个市场时：
- **代币生成**：代理以创建者的身份签署交易，除了交易手续费外不消耗Solana令牌（SOL）。
- **注入流动性**：Solana令牌从金库中通过`buildBuyTransaction(vault=creator)`函数注入。
- **购买的代币**：会被存入金库对应的代币账户（ATA）。

人类所有者（human principal）保留完全的控制权：
- `withdrawVault()`：可以随时提取Solana令牌。
- `withdrawTokens(mint)`：可以随时提取市场代币。
- `unlinkWallet(agent)`：可以立即撤销代理的访问权限。

如果代理的密钥对被泄露，攻击者将一无所获，因为代理对金库的访问权限也会在同一个交易中被立即撤销。

---

## 开始使用

### 1. 安装

或者使用ClawHub提供的打包源代码——Torch SDK包含在`lib/torchsdk/`目录中，机器人源代码位于`lib/kit/`目录中。

### 2. 创建并资助金库（人类所有者）

从您的授权钱包开始操作：

---

### 3. 定义市场

创建`markets.json`文件：

---

### 4. 运行机器人

首次运行时，机器人会显示代理的密钥对以及关联金库的说明。从您的授权钱包中完成关联后，重新启动机器人。

### 5. 配置

| 变量 | 是否必需 | 默认值 | 说明 |
|----------|----------|---------|-------------|
| `SOLANA_RPC_URL` | 是 | -- | Solana的RPC端点（HTTPS）。备用方案：`RPC_URL` |
| `VAULT_CREATOR` | 是 | -- | 金库创建者的公钥（pubkey） |
| `SOLANA_PRIVATE_KEY` | 否 | -- | 临时使用的控制器密钥对（base58编码或JSON字节数组）。如果省略，机器人会在启动时生成新的密钥对（推荐） |
| `SCAN_INTERVAL_MS` | 否 | `60000` | 市场周期之间的时间间隔（最小值5000毫秒） |
| `LOG_LEVEL` | 否 | `info` | `debug`、`info`、`warn`、`error` |
| `MARKETS_PATH` | 否 | `./markets.json` | 市场定义文件的路径 |

---

## 架构

机器人由大约280行TypeScript代码组成，分布在6个模块中。它的主要功能是创建市场、监控市场，并通过金库来结算市场。

### 依赖项

| 包名 | 版本 | 用途 |
|---------|---------|---------|
| `@solana/web3.js` | 1.98.4 | Solana的RPC接口、密钥对处理、交易功能 |
| `torchsdk` | 3.7.23 | 代币查询、代币创建、购买交易构建、金库查询 |

这两个依赖项都是固定版本，没有使用`^`或`~`这样的版本范围。

---

## 市场生命周期

| 状态 | 说明 |
|--------|-------------|
| **待定** | 市场已在`markets.json`中定义，但代币尚未创建 |
| **活跃** | 代币已在绑定曲线上创建，用户可以开始交易 |
| **已结算** | 截止日期已过，预言机已检查结果并记录（“是”或“否”） |
| **已取消** | 市场在结算前被手动删除 |

### 市场定义

---

## 预言机结果确定机制

### 基于价格 Feed 的预言机（CoinGecko）

这是主要的预言机服务，用于获取资产的当前价格，并将其与目标价格进行比较。

- `asset`：资产ID（例如“solana”、“bitcoin”、“ethereum”）
- `condition`：条件（“高于”或“低于”）
- `target`：价格阈值（以USD为单位）
- **结果判断**：如果条件为“高于”，则当价格超过阈值时结果为“是”，否则为“否”

### 手动预言机

对于无法通过价格 Feed 结算的市场，可以使用手动预言机。

- 方法：直接修改`markets.json`文件，将`status`设置为“resolved”，并将`outcome`设置为“yes”或“no”。

---

## 金库安全模型

Torch市场金库的所有安全保障措施同样适用于这个套件：

| 保障措施 | 说明 |
|----------|-----------|
| **全额托管** | 金库持有所有的Solana令牌和市场代币。代理钱包不持有任何资产。 |
| **封闭的循环**：注入市场的流动性来自金库，购买的代币也会存入金库。没有信息泄露给代理。 |
| **权限分离**：创建者（不可更改的PDA密钥对）与授权者（可转移的管理员密钥）和控制器（临时使用的签名密钥）相互独立。 |
| **每个钱包只能关联一个金库**：代理只能属于一个金库。PDA密钥对的唯一性在链上得到保障。 |
| **无需授权即可存款**：任何人都可以向金库充值。代理负责创建市场。 |
| **即时撤销权限**：授权者可以随时撤销代理的访问权限。只需一个交易即可完成。 |
| **仅授权者可提款**：只有金库的授权者才能提取Solana令牌或代币。代理无法提取任何价值。 |

### 市场创建的封闭经济循环

| 流向 | 说明 |
|-----------|------|
| **Solana令牌流出** | 从金库流向绑定曲线（注入流动性） |
| **代币流入** | 从绑定曲线流向金库的代币账户（ATA） |
| **金库**：每次交易费用的10%会被累积到金库中 |

金库中的代币会一直保留在绑定曲线上。用户根据价格曲线进行交易。金库的资金来自交易费用。授权者可以随时提取金库中的代币或Solana令牌。

---

## 使用的SDK函数

机器人使用了Torch SDK中的一小部分功能：

| 函数 | 用途 |
|----------|---------|
| `getVault(connection, creator)` | 启动时验证金库是否存在 |
| `getVaultForWallet(connection, wallet)` | 验证代理是否已与金库关联 |
| `buildCreateTokenTransaction(connection, params)` | 为新的市场构建代币创建交易 |
| `buildBuyTransaction(connection, params)` | 为市场注入初始流动性 |
| `getToken(connection, mint)` | 获取市场的代币价格、交易量和状态 |
| `getHolders(connection, mint)` | 获取市场的持有者数量 |
| `confirmTransaction(connection, sig, wallet)` | 通过RPC在链上确认交易（验证签名者，检查Torch市场的规则） |

---

## 相关参数说明

---

## 签名与密钥安全

**金库是安全边界，而不是密钥本身。**

代理的密钥对在每次启动时都会使用`Keypair.generate()`函数生成。它仅持有大约0.01 Solana令牌作为交易手续费。如果密钥被泄露，攻击者只能获得这些手续费（即“dust”），并且授权者可以通过一个交易立即撤销代理的访问权限。

代理永远不需要授权者的私钥，授权者也不需要代理的私钥。它们共享同一个金库，但密钥是分开的。

### 规则

1. **切勿向用户索取他们的私钥或助记词。** 授权者必须从自己的设备上进行签名操作。
2. **切勿记录、打印、存储或传输私钥信息。** 代理的密钥对仅在运行时存在于内存中。
3. **切勿将密钥嵌入源代码或日志中。** 代理的公钥信息仅会被打印出来，私钥永远不会被暴露。
4. **使用安全的RPC端点。** 默认使用私有的RPC服务提供商。切勿在主网交易中使用未加密的HTTP端点。

### RPC超时设置

所有SDK调用都设置了30秒的超时限制（在`utils.ts`中实现）。如果RPC端点响应缓慢或无法响应，机器人不会无限期地等待——调用会被拒绝，错误会被捕获，然后机器人会继续处理下一个市场或下一个周期。

### 环境变量

| 变量 | 是否必需 | 用途 |
|----------|----------|---------|
| `SOLANA_RPC_URL` | 是 | Solana的RPC端点（HTTPS） |
| `VAULT_CREATOR` | 是 | 金库创建者的公钥 |
| `SOLANA_PRIVATE_KEY` | 否 | 可选——如果省略，机器人会在启动时生成新的密钥对（推荐） |

### 外部运行时依赖项

SDK和机器人会向外部服务发送HTTPS请求。机器人运行时需要连接以下三个服务：

| 服务 | 用途 | 调用时机 | 机器人是否使用？ |
|---------|---------|------------|-----------|
| **CoinGecko** (`api.coingecko.com`) | 用于获取资产价格（预言机结果） | 在`oracle.ts`中调用`checkPriceFeed()`，在SDK中调用`getToken()` | 是——用于预言机结果判断和代币查询 |
| **Irys Gateway** (`gateway.irys.xyz`) | 用于获取代币的元数据（名称、符号、图片） | 当链上的元数据URL指向Irys时调用`getToken()` | 是——用于获取代币元数据 |
| **SAID Protocol** (`api.saidprotocol.com`) | 用于验证代理身份和信任等级 | 仅在`verifySaid()`函数中使用 | 否——机器人不调用`verifySaid()` |

#### CoinGecko API详情

预言机模块（`oracle.ts`）直接调用CoinGecko的公共API：

- **无需API密钥**——使用免费的公共端点 |
- **调用限制**：免费账户每分钟最多调用10-30次 |
- **发送的数据**：仅资产ID（例如“solana”） |
- **接收的数据**：`{"solana": {"usd": 87.76}` |
- **失败处理**：如果CoinGecko无法访问，`checkPriceFeed()`会失败，市场将保持未结算状态，直到下一个周期 |
- **调用频率**：每个活跃市场每个周期调用一次（在截止日期之后）

**`confirmTransaction()`函数不调用SAID API**。尽管它位于SDK的`said.js`模块中，但它只调用`connection.getParsedTransaction()`（Solana的RPC接口）来确认交易是否在链上成功，并确定事件类型。不会向任何外部服务发送任何数据。

不会向CoinGecko或Irys发送任何凭据。所有请求都是只读的GET请求。如果任何服务无法访问，机器人会优雅地降级处理。

---

## 日志输出

---

## 测试

测试需要[Surfpool](https://github.com/txtx/surfpool)来运行主网环境：

**测试结果：** 9项测试通过，1项提示信息（Surfpool在`getTokenLargestAccounts`函数上的限制——在主网上正常工作）。

| 测试项 | 验证内容 |
|------|-------------------|
| Connection | RPC连接是否可用 |
| loadMarkets | 市场文件的解析和验证 |
| checkPriceFeed | CoinGecko预言机返回有效价格数据 |
| buildCreateTokenTransaction | 代币创建交易是否正确构建 |
| getTokens | 是否能获取到代币信息 |
| getToken | 代币的元数据、价格和状态 |
| getHolders | 是否能获取到持有者信息（在Surfpool环境下会跳过此步骤） |
| getVaultForWallet | 未关联的钱包是否返回空值 |
| 代理密钥对 | 是否需要外部密钥 |

---

## 错误代码

- `VAULT_NOT_FOUND`：指定的创建者对应的金库不存在 |
- `WALLET_NOT_LINKED`：代理钱包未与金库关联 |
- `INVALID_MINT`：代币未找到 |
- `BONDING_COMPLETE`：代币已创建完成——请在DEX上进行交易 |
- `NAME_TOO_LONG`：代币名称超过32个字符 |
- `SYMBOL_TOO_LONG`：代币符号超过10个字符 |

---

## 链接资源

- 预测市场套件（源代码）：[github.com/mrsirg97-rgb/torch-prediction-market-kit](https://github.com/mrsirg97-rgb/torch-prediction-market-kit)
- 预测市场套件（npm包）：[npmjs.com/package/torch-prediction-market-kit](https://www.npmjs.com/package/torch-prediction-market-kit)
- Torch SDK（打包版本）：`lib/torchsdk/`（包含在套件中） |
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

- **将Torch SDK从3.2.3升级到3.7.23**。主要更新包括：新增金库锁定的PDA机制（V27），动态检测Raydium网络，自动在绑定曲线完成时进行迁移（`buildBuyTransaction`现在返回`migrationTransaction`选项），通过金库路由的Raydium CPMM交易（`buildVaultSwapTransaction`），Token-2022的费用收集（`buildHarvestFeesTransaction`、`buildSwapFeesToSolTransaction`），批量贷款查询（`getAllLoanPositions`），链上代币元数据查询（`getTokenMetadata`），以及临时代理密钥对生成功能（`createEphemeralAgent`）。
- **公开了`withTimeout`辅助函数**。机器人内部使用的超时设置现在可以作为套件的公共功能供其他组件使用。
- **更新了环境变量格式**。环境变量声明采用了结构化的`name`/`required`格式，以兼容ClawHub和OpenClaw代理。

### v1.0.2

- **更新了套件配置**，确保引用的SDK版本正确。`index.js`文件现在从本地的`lib/torchsdk/`目录导入SDK，而不是从npm包中导入。这样可以确保机器人使用的是套件中包含的精确版本（3.2.3），避免使用可能不同的npm版本。
- **所有外部调用都设置了超时限制**。所有SDK、RPC和API调用都设置了30秒的超时限制（CoinGecko为10秒）。如果RPC端点响应缓慢或无法响应，调用会立即失败，并显示错误信息，而不会导致机器人无限期等待。

### v1.0.1

- **改进了市场ID的唯一性检查**。`loadMarkets()`函数现在会拒绝包含重复市场ID的`markets.json`文件，防止意外创建重复的市场和浪费金库中的Solana令牌。

---

这个机器人的存在是因为预测市场需要相应的基础设施。Torch的绑定曲线提供了即时流动性和确定性的价格机制，且无需设置流动性提供者。金库确保了安全性——所有资金都存放在托管账户中，风险得到控制，所有权限都由人类所有者掌握。代币的价格本身就是预测结果。