---
name: torch-prediction-market-bot
version: "1.0.0"
description: 这是一个基于自动化的预言机市场的机器人，专为Solana上的Torch Market平台设计。该机器人能够创建以Torch代币为交易对象的二元预言市场；通过“债券曲线”（bonding curve）来实现价格发现机制，交易费用被累积到“金库”（treasury）中，而“金库”则负责管理所有交易头寸。每个预言市场都配备了一个预言机（可以提供价格数据或采用手动定价方式），并在预设的截止日期前完成交易结算。机器人的密钥对是在运行过程中生成的，属于一次性使用的密钥对，不存储任何有价值的信息。所有与Solana相关的交易都会通过该“金库”进行。人类操作者负责创建“金库”、为其注入资金、连接机器人，并保持对其的完全控制权。该机器人基于Torch SDK v3.2.3和Torch Market协议进行开发。
license: MIT
disable-model-invocation: true
requires:
  env:
    - SOLANA_RPC_URL
    - VAULT_CREATOR
metadata:
  clawdbot:
    requires:
      env:
        - SOLANA_RPC_URL
        - VAULT_CREATOR
    primaryEnv: SOLANA_RPC_URL
  openclaw:
    requires:
      env:
        - SOLANA_RPC_URL
        - VAULT_CREATOR
    primaryEnv: SOLANA_RPC_URL
    install:
      - id: torch-prediction-market-kit
        kind: npm
        package: torch-prediction-market-kit@^1.0.0
        flags: []
        label: "Install Torch Prediction Market Kit (npm, optional -- SDK is bundled in lib/torchsdk/ and bot source is bundled under lib/kit on clawhub)"
  author: torch-market
  version: "1.0.0"
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
compatibility: Requires SOLANA_RPC_URL (HTTPS Solana RPC endpoint) and VAULT_CREATOR (vault creator pubkey) as environment variables. SOLANA_PRIVATE_KEY is optional -- the kit generates a fresh disposable keypair in-process if not provided. The agent wallet holds nothing of value (~0.01 SOL for gas). All token creation and seed liquidity SOL routes through the vault. The vault can be created and funded entirely by the human principal. The Torch SDK is bundled in lib/torchsdk/ -- all source included for full auditability. No API server dependency. Oracle resolution uses CoinGecko public API (read-only, no key required).
---

# Torch预测市场套件

您之所以使用这个套件，是因为您希望在Torch市场上运行预测市场，并且希望确保操作的安全性。

每个预测市场都对应一个Torch代币。Torch市场的定价机制基于“债券曲线”（bonding curve），这是一种自动做市商（AMM）机制——无需设置流动性提供者（LP），价格确定且交易具有即时流动性。市场交易中会收取10%的费用，这些费用会进入“资金库”（treasury）。用户购买代币来下注“价格上涨”或“价格下跌”。在截止日期时，预言机（oracle）会检查结果，并由机器人（bot）记录下来。

**结算方式：** 代币本身就是预测结果。整个结算过程由债券曲线和资金库来完成。

这就是这个机器人的作用：它会读取您的`markets.json`文件，为待创建的市场生成Torch代币，从您的资金库中注入初始流动性，监控价格和交易量，并在截止日期时通过预言机（可以使用CoinGecko的价格数据）来决定最终结果。

---

## 工作原理

### 代理密钥对（Agent Keypair）

机器人每次启动时都会生成一个新的密钥对。没有私钥文件，也不需要设置环境变量（除非您有特殊需求）。这个密钥对是临时使用的——它用于签署交易，但本身不持有任何价值。

首次运行时，机器人会检查该密钥对是否已与您的资金库关联。如果没有关联，它会显示您需要使用的SDK调用命令来建立连接：

**连接方法：** 从您的权限钱包（硬件钱包、多重签名钱包等）中建立连接。代理无需知道权限钱包的私钥，权限钱包也无需知道代理的私钥。它们共享的是同一个资金库，而不是密钥。

### 资金库（Vault）

这个资金库与完整的Torch市场协议中的资金库相同，用于存储所有资产（SOLANA代币和Torch代币）。代理只是一个临时使用的控制器。

当机器人创建市场时：
- **代币生成**：代理以创建者的身份签署交易，除了交易手续费外不产生额外的SOLANA费用。
- **注入流动性**：所需的SOLANA代币来自资金库，通过`buildBuyTransaction(vault=creator)`操作注入。
- **购买的代币**：会存入资金库对应的代币账户（ATA）。

人类所有者（principal）拥有完全的控制权：
- `withdrawVault()`：可以随时提取SOLANA代币。
- `withdrawTokens(mint)`：可以随时提取市场生成的代币。
- `unlinkWallet(agent)`：可以立即撤销代理的访问权限。

如果代理的密钥对被泄露，攻击者只能得到无价值的代币，并且您可以通过一次交易立即撤销代理的访问权限。

---

## 开始使用

### 1. 安装

或者直接使用ClawHub提供的捆绑源代码——Torch SDK位于`lib/torchsdk/`目录下，机器人源代码位于`lib/kit/`目录下。

### 2. 创建并资助资金库（由人类所有者操作）

使用您的权限钱包完成相关操作。

### 3. 定义市场规则

创建`markets.json`文件。

### 4. 运行机器人

首次运行时，机器人会显示代理的密钥对以及连接说明。请使用权限钱包完成连接，然后重新启动机器人。

### 5. 配置参数

| 参数 | 是否必填 | 默认值 | 说明 |
|----------|----------|---------|-------------|
| `SOLANA_RPC_URL` | 是 | -- | Solana的RPC接口地址（HTTPS）。默认使用`RPC_URL` |
| `VAULT_CREATOR` | 是 | -- | 资金库创建者的公钥 |
| `SOLANA_PRIVATE_KEY` | 否 | -- | 代理的临时密钥对（格式为base58或JSON字节数组）。如果省略，机器人会在启动时生成新的密钥对（推荐） |
| `SCAN_INTERVAL_MS` | 否 | `60000` | 市场周期之间的间隔时间（最小值5000毫秒） |
| `LOG_LEVEL` | 否 | `info` | 日志级别：`debug`、`info`、`warn`、`error` |
| `MARKETS_PATH` | 否 | `./markets.json` | 市场规则文件的路径 |

---

## 架构

该机器人由大约280行TypeScript代码组成，分为6个模块。它的主要功能包括：创建市场、监控市场状态以及通过资金库来结算交易。

### 依赖库

| 库名 | 版本 | 用途 |
|---------|---------|---------|
| `@solana/web3.js` | 1.98.4 | 提供Solana的RPC接口、密钥对管理和交易功能 |
| `torchsdk` | 3.2.3 | 用于代币查询、代币生成和交易构建 |

这两个依赖库的版本都是固定的，没有使用`^`或`~`等范围表示版本范围。

---

## 市场生命周期

| 状态 | 说明 |
|--------|-------------|
| **pending** | 市场规则已定义，但代币尚未生成 |
| **active** | 代币已生成并上线，用户可以开始交易 |
| **resolved** | 截止日期已过，预言机已检查结果并记录 |
| **cancelled** | 市场被手动取消 |

### 市场规则定义

---

## 预言机结果确定机制

### 基于CoinGecko的价格预言机

主要使用的预言机服务。它获取资产的当前价格，并与预设的目标价格进行比较：

- `asset`：资产ID（例如“solana”、“bitcoin”、“ethereum”）
- `condition`：比较条件（“above”或“below”）
- `target`：价格阈值（以USD为单位）
- **结果判断**：如果条件为“above”，则当价格高于目标价格时结果为“yes”，否则为“no”。

### 手动预言机

对于无法通过价格预言机确定结果的市场，可以使用手动预言机机制：

- 直接修改`markets.json`文件，将`status`设置为“resolved”，并将`outcome`设置为“yes”或“no”。

---

## 资金库的安全机制

Torch市场的资金库安全机制同样适用于这个套件：

- **资产完全由资金库保管**：所有SOLANA代币和市场代币都存储在资金库中，代理钱包不持有任何资产。
- **封闭的经济循环**：用于注入流动性的SOLANA代币来自资金库，购买的代币也会存入资金库。
- **权限分离**：创建者（拥有不可更改的私钥对）、权限管理者（可转移的管理员权限）和代理（临时使用的签名者）之间有明确的职责划分。
- **每个钱包只能关联一个资金库**：代理只能属于一个资金库，这一规则通过区块链上的唯一性机制得到保障。
- **任何人都可以向资金库充值**：任何人都可以向资金库添加资金，代理负责创建市场。
- **即时撤销权限**：权限管理者可以随时撤销代理的访问权限，只需一次交易即可完成。

### 市场创建的封闭经济循环

- **资金流动方向**：
  - SOLANA代币从资金库流入债券曲线，用于注入市场流动性。
  - 购买的代币会存入资金库对应的代币账户（ATA）。
- **费用处理**：每次交易会收取10%的费用，这些费用会进入资金库。

---

## 机器人使用的SDK函数

机器人仅使用了Torch SDK中的一小部分功能：

| 函数 | 用途 |
|----------|---------|
| `getVault(connection, creator)` | 启动时检查资金库是否存在 |
| `getVaultForWallet(connection, wallet)` | 检查代理是否已与资金库关联 |
| `buildCreateTokenTransaction(connection, params)` | 为新市场生成代币创建交易 |
| `buildBuyTransaction(connection, params)` | 为市场注入初始流动性 |
| `getToken(connection, mint)` | 获取市场的代币价格、交易量和状态信息 |
| `getHolders(connection, mint)` | 获取市场持有者的数量 |
| `confirmTransaction(connection, sig, wallet)` | 通过RPC在区块链上确认交易（验证签名者并检查市场规则）

---

## 安全措施

**资金库是安全的核心**：代理的密钥对在每次启动时都会使用`Keypair.generate()`生成，仅用于签署交易，不会持有任何价值。如果密钥被泄露，攻击者只能得到无价值的代币和资金库的访问权限（这些权限也可以通过一次交易立即撤销）。

**重要规则：**
1. **切勿向用户索取私钥或助记词。** 权限管理者始终在自己的设备上进行操作。
2. **切勿记录、打印、存储或传输私钥信息。** 代理的密钥对仅在运行时存在于内存中。
3. **切勿将密钥嵌入源代码或日志中。** 代理的公钥仅用于显示，私钥永远不会被暴露。
4. **使用安全的RPC接口。** 默认使用私有的RPC服务提供商，切勿在主网交易中使用未加密的HTTP接口。

### 环境变量设置

| 参数 | 是否必填 | 说明 |
|----------|----------|---------|
| `SOLANA_RPC_URL` | 是 | Solana的RPC接口地址（HTTPS） |
| `VAULT_CREATOR` | 是 | 资金库创建者的公钥 |
| `SOLANA_PRIVATE_KEY` | 否 | 可选：如果省略，机器人会在启动时生成新的密钥对（推荐） |

### 外部依赖服务

机器人需要通过HTTPS与外部服务进行通信。机器人会调用以下三个服务：

- **CoinGecko**：用于获取资产价格并显示结果（仅用于预言机功能）。
- **Irys Gateway**：用于获取代币的元数据（名称、符号、图片等）。
- **SAID Protocol**：用于验证代理的身份和信任等级。

#### CoinGecko API详情

- **无需API密钥**：直接使用CoinGecko的公共API。
- **调用频率限制**：免费账户每分钟最多调用10-30次。
- **传输的数据**：仅包含资产ID（例如“solana”）。
- **异常处理**：如果CoinGecko无法访问，`checkPriceFeed()`函数会抛出错误，市场状态将保持未解决状态，直到下一个周期。

**注意：`confirmTransaction()`函数不使用SAID Protocol。** 尽管它位于SDK的`said.js`模块中，但它仅通过`connection.getParsedTransaction()`（Solana RPC）来确认交易是否成功，并确定事件类型。不会向任何外部服务发送任何数据。

---

## 测试说明

测试需要使用[Surfpool](https://github.com/txtx/surfpool)来运行主网环境：

- **测试结果**：9项测试通过，1项提示信息（由于Surfpool在`getTokenLargestAccounts`函数上的限制，但在主网上可以正常工作）。

| 测试项目 | 需要验证的内容 |
|------|-------------------|
| Connection | 是否能成功连接到Solana RPC接口 |
| loadMarkets | 是否能正确解析和验证市场规则文件 |
| checkPriceFeed | 是否能从CoinGecko获取有效的价格数据 |
| buildCreateTokenTransaction | 是否能正确生成代币创建交易 |
| getTokens | 是否能获取代币的元数据、价格和状态 |
| getHolders | 是否能获取市场持有者信息 |
| getVaultForWallet | 未关联的钱包是否返回正确的资金库信息 |
| 代理密钥对的处理 | 是否不需要外部密钥 |

---

## 错误代码

- `VAULT_NOT_FOUND`：指定的创建者对应的资金库不存在。
- `WALLET_NOT_LINKED`：代理钱包未与资金库关联。
- `INVALID_MINT`：未找到对应的代币。
- `BONDING_COMPLETE`：代币已生成完毕，用户应通过DEX进行交易。
- `NAME_TOO_LONG`：代币名称超过32个字符。
- `SYMBOL_TOO_LONG`：代币符号超过10个字符。

---

## 相关资源链接

- Torch预测市场套件源代码：[github.com/mrsirg97-rgb/torch-prediction-market-kit](https://github.com/mrsirg97-rgb/torch-prediction-market-kit)
- Torch预测市场套件（npm包）：[npmjs.com/package/torch-prediction-market-kit](https://www.npmjs.com/package/torch-prediction-market-kit)
- Torch SDK（包含在本套件中）：`lib/torchsdk/`
- Torch SDK源代码：[github.com/mrsirg97-rgb/torchsdk](https://github.com/mrsirg97-rgb/torchsdk)
- Torch SDK（npm包）：[npmjs.com/package/torchsdk](https://www.npmjs.com/package/torchsdk)
- Torch市场协议文档：[clawhub.ai/mrsirg97-rgb/torchmarket](https://clawhub.ai/mrsirg97-rgb/torchmarket)
- 官方白皮书：[torch.market/whitepaper.md](https://torch.market/whitepaper.md)
- 安全审计报告：[torch.market/audit.md](https://torch.market/audit.md)
- 官方网站：[torch.market](https://torch.market)
- 程序ID：`8hbUkonssSEEtkqzwM7ZcZrD9evacM92TcWSooVF4BeT`

这个机器人的存在是因为预测市场需要相应的基础设施。Torch市场的债券曲线机制提供了即时流动性和确定性的价格机制，且无需设置流动性提供者。资金库确保了交易的安全性——所有资产都由资金库保管，风险得到控制，所有权限都由人类所有者掌握。代币的价格本身就是市场的预测结果。