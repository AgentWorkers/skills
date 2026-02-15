---
name: torch-prediction-market-bot
version: "1.0.2"
description: 这是一个基于自动化的预言机市场的机器人，专为Solana上的Torch Market平台设计。该机器人能够创建以Torch代币为交易对象的二元预言市场；通过“债券曲线”（bonding curve）机制实现价格发现，交易费用被存入“金库”（treasury）以积累价值，而“金库”则负责管理所有交易头寸。每个预言市场都配备有价格数据提供者（oracle，可以是自动的，也可以是人工提供的），并在预设的截止日期前完成交易结算。该机器人的代理密钥对（agent keypair）是在运行过程中生成的，属于一次性使用的密钥，不包含任何实际价值。所有与Solana相关的交易都会通过“金库”进行。用户（即人类操作者）负责创建“金库”、为其注入资金、关联相应的代理，并保留对整个系统的完全控制权。该机器人是基于Torch SDK v3.2.3及Torch Market协议开发的。
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
        package: torch-prediction-market-kit@^1.0.1
        flags: []
        label: "Install Torch Prediction Market Kit (npm, optional -- SDK is bundled in lib/torchsdk/ and bot source is bundled under lib/kit on clawhub)"
  author: torch-market
  version: "1.0.2"
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

您之所以使用这个套件，是因为您希望在Torch市场上运行预测市场，并且希望这一过程是安全的。

每个预测市场都对应一个Torch代币。Torch市场的定价机制基于“债券曲线”（bonding curve），这是一种自动做市商（AMM）机制——无需设置流动性提供者（LP），价格确定，且具有即时流动性。市场交易中收取的10%费用会被存入“国库”（treasury）。用户购买代币来下注“上涨”（价格上升）或“下跌”（价格下降）。在截止日期时，预言机（oracle）会检查结果，并由机器人（bot）记录下来。

**结算方式：** 代币本身就是预测结果。债券曲线和国库共同完成了整个结算过程。

这就是这个机器人的作用：它读取您的`markets.json`文件，为待定的市场创建Torch代币，从您的资金库中注入初始流动性，监控价格和交易量，并在截止日期通过预言机（可以使用CoinGecko的价格数据）来结算交易。所有资金流动都通过您的资金库进行。执行交易的代理钱包（agent wallet）本身不持有任何资产。

**注意：** 这不是一个仅用于查看数据的工具，而是一个完全可操作的做市商。它会生成自己的密钥对，验证与资金库的连接，创建代币，并在持续循环中自动结算市场。

---

## 工作原理

### 代理密钥对（Agent Keypair）

机器人每次启动时都会生成一个新的密钥对。没有私钥文件，也不需要环境变量（除非您特别指定）。这个密钥对是临时的——它用于签署交易，但本身不持有任何价值。

首次运行时，机器人会检查这个密钥对是否已与您的资金库关联。如果没有关联，它会显示您需要使用的SDK调用指令，以便进行关联。

**关联方法：** 请从您的授权钱包（硬件钱包、多重签名钱包等）中关联这个密钥对。代理无需知道授权钱包的密钥，授权钱包也不需要知道代理的密钥。它们共享的是资金库，而不是密钥。

### 资金库（Vault）

这个资金库与完整的Torch市场协议中的资金库相同，用于存储所有资产（SOL和代币）。代理只是一个临时的控制器。

当机器人创建市场时：
- **代币生成**：代理以创建者的身份签署交易，除了交易手续费外不消耗SOL。
- **注入流动性**：SOL来自资金库，通过`buildBuyTransaction(vault=creator)`操作注入。
- **购买的代币**：会存入资金库对应的代币账户（ATA）。

人类所有者（human principal）拥有完全的控制权：
- `withdrawVault()`：随时可以提取SOL。
- `withdrawTokens(mint)`：随时可以提取市场代币。
- `unlinkWallet(agent)`：可以立即撤销代理的访问权限。

如果代理的密钥对被泄露，攻击者将无法获取任何资产，因为代理的访问权限可以通过一次交易被立即撤销。

---

## 开始使用

### 1. 安装

或者使用ClawHub提供的捆绑源代码：Torch SDK位于`lib/torchsdk/`目录下，机器人源代码位于`lib/kit/`目录下。

### 2. 创建并资助资金库（人类所有者）

从您的授权钱包开始操作：

---

### 3. 定义市场

创建`markets.json`文件：

---

### 4. 运行机器人

首次运行时，机器人会显示代理的密钥对以及关联说明。请从您的授权钱包中完成关联操作，然后重新启动机器人。

### 5. 配置

| 参数 | 是否必需 | 默认值 | 说明 |
|----------|----------|---------|-------------|
| `SOLANA_RPC_URL` | 是 | -- | Solana的RPC端点（HTTPS）。默认值：`RPC_URL` |
| `VAULT_creATOR` | 是 | -- | 资金库创建者的公钥 |
| `SOLANA_PRIVATE_KEY` | 否 | -- | 临时的控制器密钥对（base58编码或JSON字节数组）。如果省略，机器人会在启动时生成新的密钥对（推荐） |
| `SCAN_INTERVAL_MS` | 否 | `60000` | 市场周期之间的时间间隔（最小值5000毫秒） |
| `LOG_LEVEL` | 否 | `info` | 日志级别：`debug`、`info`、`warn`、`error` |
| `MARKETS_PATH` | 否 | `./markets.json` | 市场定义文件的路径 |

---

## 架构

机器人由大约280行TypeScript代码组成，分布在6个模块中。它的主要功能是创建市场、监控市场状态，并通过资金库进行结算。

### 依赖项

| 包名 | 版本 | 用途 |
|---------|---------|---------|
| `@solana/web3.js` | 1.98.4 | Solana的RPC接口、密钥对处理、交易操作 |
| `torchsdk` | 3.2.3 | 代币查询、代币生成、交易构建功能 |

这两个依赖项都固定为特定版本，没有使用`^`或`~`的范围表示版本范围。

---

## 市场生命周期

| 状态 | 说明 |
|--------|-------------|
| **待定** | 市场已在`markets.json`中定义，但代币尚未生成 |
| **活跃** | 代币已在债券曲线上生成，用户可以开始交易 |
| **已结算** | 截止日期已过，预言机已检查结果并记录下来 |
| **已取消** | 市场在结算前被手动删除 |

### 市场定义

---

## 预言机结果确定机制

### 基于价格数据的预言机（CoinGecko）

主要使用的预言机服务是CoinGecko。它获取资产的当前价格，并与预设的目标价格进行比较。

- `asset`：资产ID（例如“solana”、“bitcoin”、“ethereum”）
- `condition`：价格条件（“高于”或“低于”）
- `target`：价格阈值（以USD为单位）
- **结果判断**：如果条件为“高于”，则结果为“yes”（价格高于目标价格）；否则为“no”。

### 手动预言机

对于无法通过价格数据确定结果的市场，可以使用手动预言机。

- 方法：直接修改`markets.json`文件，将`status`设置为“resolved”，并将`outcome`设置为“yes”或“no”。

---

## 资金库的安全机制

Torch市场资金库的安全机制同样适用于这个套件：

- **完全托管**：资金库持有所有SOL和代币。代理钱包不持有任何资产。
- **封闭的循环**：注入市场的流动性来自资金库，购买的代币也会存入资金库。没有信息泄露给代理。
- **权限分离**：创建者（不可更改的PDA密钥）负责生成交易，授权者（可转移的管理员）负责管理资金库，代理（临时的签署者）负责执行交易。
- **每个钱包只能关联一个资金库**：代理只能属于一个资金库。PDA密钥的唯一性确保了这一点。
- **无需授权即可存款**：任何人都可以向资金库充值。代理负责创建市场。
- **即时撤销权限**：授权者可以随时撤销代理的访问权限，只需一次交易即可完成。
- **只有授权者才能提款**：只有资金库的授权者才能提取SOL或代币。

### 市场创建的封闭经济循环

- **资金流动方向**：
  - SOL从资金库流向债券曲线（用于注入流动性）。
  - 代币从债券曲线流向资金库的代币账户（ATA）。
- **费用处理**：每次交易中收取的10%费用会被存入资金库。

资金库中的代币会一直留在债券曲线上。用户根据债券曲线进行交易。资金库的资金来自交易手续费。授权者可以随时提取SOL或代币。

---

## 机器人使用的SDK函数

机器人仅使用了Torch SDK中的一小部分功能：

| 函数 | 用途 |
|----------|---------|
| `getVault(connection, creator)` | 启动时验证资金库是否存在 |
| `getVaultForWallet(connection, wallet)` | 验证代理是否已与资金库关联 |
| `buildCreateTokenTransaction(connection, params)` | 为新的市场构建代币生成交易 |
| `buildBuyTransaction(connection, params)` | 为市场注入初始流动性 |
| `getToken(connection, mint)` | 获取市场的代币价格、交易量和状态信息 |
| `getHolders(connection, mint)` | 获取市场的持有者数量 |
| `confirmTransaction(connection, sig, wallet)` | 通过RPC在链上确认交易（验证签名者并检查Torch协议的规则） |

---

## 相关参数说明

---

## 签名与密钥安全

**资金库是安全边界，而非密钥本身。**

代理的密钥对在每次启动时都会通过`Keypair.generate()`生成。它仅持有约0.01 SOL作为交易手续费。如果密钥被泄露，攻击者只能获取到用于支付手续费的SOL，并且无法获取资金库的访问权限（该权限可以通过一次交易被撤销）。

**重要规则：**
1. **切勿向用户索取私钥或助记词。** 授权者必须从自己的设备上进行签名操作。
2. **切勿记录、打印、存储或传输私钥信息。** 代理的密钥对仅在运行时存在于内存中。
3. **切勿将密钥嵌入源代码或日志中。** 代理的公钥会被打印出来，但私钥永远不会被暴露。
4. **使用安全的RPC端点。** 默认使用私有的RPC服务。切勿在主网交易中使用未加密的HTTP端点。

### 环境变量

| 参数 | 是否必需 | 用途 |
|----------|----------|---------|
| `SOLANA_RPC_URL` | 是 | Solana的RPC端点（HTTPS） |
| `VAULT_creATOR` | 是 | 资金库创建者的公钥 |
| `SOLANA_PRIVATE_KEY` | 否 | 可选：如果省略，机器人会在启动时生成新的密钥对（推荐） |

### 外部依赖项

机器人需要通过HTTPS与外部服务进行通信。机器人运行时需要调用以下三个服务：

- **CoinGecko**（`api.coingecko.com`）：用于获取资产价格和显示价格（预言机功能）：`checkPriceFeed()`、`getToken()` |
- **Irys Gateway**（`gateway.irys.xyz`）：用于获取代币的元数据（名称、符号、图片）：在链上元数据指向Irys时调用`getToken()` |
- **SAID Protocol**（`api.saidprotocol.com`）：用于验证代理身份和信任等级：仅用于`verifySaid()`函数 |

#### CoinGecko API详情

预言机模块`oracle.ts`直接调用CoinGecko的公共API：

- **无需API密钥**：使用免费的公共端点。
- **调用限制**：免费账户每分钟最多调用10-30次。
- **发送的数据**：仅资产ID（例如“solana”）。
- **接收的数据**：`{"solana": {"usd": 87.76}`。
- **故障处理**：如果CoinGecko无法访问，`checkPriceFeed()`会失败，市场状态将保持未解决状态，直到下一个周期。
- **调用频率**：每个活跃市场每个周期（截止日期过后）调用一次。

`confirmTransaction()`函数不会调用SAID API。尽管它位于SDK的`said.js`模块中，但它仅通过`connection.getParsedTransaction()`（Solana RPC）来确认交易是否在链上成功，并确定事件类型。不会向CoinGecko发送任何数据。

### 日志输出

---

## 测试说明

测试需要运行[Surfpool](https://github.com/txtx/surfpool)来模拟主网环境：

**测试结果：** 9项测试通过，1项提示信息（Surfpool在`getTokenLargestAccounts`函数上的限制，适用于Token-2022市场——在主网上可以正常运行）。

| 测试项 | 验证内容 |
|------|-------------------|
| Connection | 是否能连接到RPC服务器 |
| loadMarkets | 是否能正确解析和验证市场文件 |
| checkPriceFeed | 是否能从CoinGecko获取有效的价格数据 |
| buildCreateTokenTransaction | 是否能正确构建代币生成交易 |
| getTokens | 是否能获取代币信息 |
| getToken | 是否能获取代币的元数据、价格和状态 |
| getHolders | 是否能获取市场持有者信息（Surfpool有相关限制） |
| getVaultForWallet | 未关联的钱包是否返回空值 |
| 在运行时生成密钥对 | 是否不需要外部密钥 |

---

## 错误代码

- `VAULT_NOT_FOUND`：指定的创建者对应的资金库不存在。
- `WALLET_NOT_LINKED`：代理钱包未与资金库关联。
- `INVALID_MINT`：找不到对应的代币。
- `BONDING COMPLETE`：代币已生成完成，应通过DEX进行交易。
- `NAME_TOO_LONG`：代币名称超过32个字符。
- `SYMBOL_TOO_LONG`：代币符号超过10个字符。

---

## 链接资源

- 预测市场套件源代码：[github.com/mrsirg97-rgb/torch-prediction-market-kit](https://github.com/mrsirg97-rgb/torch-prediction-market-kit)
- 预测市场套件（npm包）：[npmjs.com/package/torch-prediction-market-kit](https://www.npmjs.com/package/torch-prediction-market-kit)
- Torch SDK（捆绑包）：`lib/torchsdk/`（包含在套件中）
- Torch SDK（源代码）：[github.com/mrsirg97-rgb/torchsdk](https://github.com/mrsirg97-rgb/torchsdk)
- Torch SDK（npm包）：[npmjs.com/package/torchsdk](https://www.npmjs.com/package/torchsdk)
- Torch市场协议文档：[clawhub.ai/mrsirg97-rgb/torchmarket](https://clawhub.ai/mrsirg97-rgb/torchmarket)
- 白皮书：[torch.market/whitepaper.md](https://torch.market/whitepaper.md)
- 安全审计报告：[torch.market/audit.md](https://torch.market/audit.md)
- 官网：[torch.market](https://torch.market)
- 程序ID：`8hbUkonssSEEtkqzwM7ZcZrD9evacM92TcWSooVF4BeT`

---

## 更新日志

### v1.0.2

- **更新了SDK的引用路径。** `index.js`文件现在从本地的`lib/torchsdk/`目录导入SDK，而不是通过npm包。这样可以确保机器人使用的是套件中包含的精确版本（3.2.3），避免使用可能不同的npm版本。解决了审计报告中的问题L-3。**
- **添加了超时机制。** 所有的SDK、RPC和API调用都设置了30秒的超时限制（CoinGecko为10秒）。如果RPC端点或CoinGecko无法响应，调用会立即失败并显示错误信息，避免机器人无限期等待。解决了审计报告中的问题L-1。**
- **增加了市场ID的唯一性检查。** `loadMarkets()`函数现在会拒绝包含重复市场ID的`markets.json`文件，防止意外创建重复市场或浪费资金库中的SOL。解决了审计报告中的问题L-2。**

这个机器人的存在是因为预测市场需要相应的基础设施。Torch市场的债券曲线提供了即时流动性和确定性的价格机制，且无需设置流动性提供者。资金库确保了安全性——所有资产都存放在托管账户中，风险得到控制，且所有权限都由人类所有者掌握。代币的价格本身就是预测结果。