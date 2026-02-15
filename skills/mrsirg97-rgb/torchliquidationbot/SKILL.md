---
name: torch-liquidation-bot
version: "3.0.2"
description: 这是一个基于自动化的仓库（vault）的清算系统，专为Solana上的Torch Market借贷服务设计。该系统会扫描所有已迁移的代币，识别出那些处于高风险状态（贷款价值与代币价值比率LTV超过65%）的贷款，并通过Torch Vault来执行清算交易。同时，系统还会收取10%的抵押品奖励。代理密钥对是在运行过程中生成的，属于一次性使用的密钥，不持有任何有价值的资产。所有的SOL代币及抵押品代币都会通过该仓库进行管理。用户（即贷款的发起者）负责创建仓库、为其注入资金、关联代理，并保持对整个系统的完全控制权。该系统基于torchsdk v3.2.3和Torch Market协议进行开发。
license: MIT
disable-model-invocation: true
requires:
  env:
    - SOLANA_RPC_URL
    - VAULT_CREATOR
metadata:
  openclaw:
    requires:
      env:
        - SOLANA_RPC_URL
        - VAULT_CREATOR
    primaryEnv: SOLANA_RPC_URL
    install:
      - id: npm-torch-liquidation-bot
        kind: npm
        package: torch-liquidation-bot@^3.0.2
        flags: []
        label: "Install Torch Liquidation Bot (npm, optional -- SDK is bundled in lib/torchsdk/ and bot source is bundled under lib/kit on clawhub)"
  author: torch-market
  version: "3.0.2"
  clawhub: https://clawhub.ai/mrsirg97-rgb/torch-liquidation-bot
  kit-source: https://github.com/mrsirg97-rgb/torch-liquidation-kit
  website: https://torch.market
  program-id: 8hbUkonssSEEtkqzwM7ZcZrD9evacM92TcWSooVF4BeT
  keywords:
    - solana
    - defi
    - liquidation
    - liquidation-bot
    - liquidation-keeper
    - collateral-lending
    - vault-custody
    - ai-agents
    - agent-wallet
    - agent-safety
    - treasury-lending
    - bonding-curve
    - fair-launch
    - token-2022
    - raydium
    - community-treasury
    - protocol-rewards
    - solana-agent-kit
    - escrow
    - anchor
    - pda
    - on-chain
    - autonomous-agent
    - keeper-bot
    - torch-market
  categories:
    - solana-protocols
    - defi-primitives
    - lending-markets
    - agent-infrastructure
    - custody-solutions
    - liquidation-keepers
compatibility: Requires SOLANA_RPC_URL (HTTPS Solana RPC endpoint) and VAULT_CREATOR (vault creator pubkey) as environment variables. SOLANA_PRIVATE_KEY is optional -- the bot generates a fresh disposable keypair in-process if not provided. The agent wallet holds nothing of value (~0.01 SOL for gas). All liquidation proceeds (collateral tokens) route to the vault. The vault can be created and funded entirely by the human principal. The Torch SDK is bundled in lib/torchsdk/ -- all source included for full auditability. No API server dependency.
---

# Torch清算机器人

您之所以使用这个机器人，是因为您希望在Torch市场上运行一个清算机制——并且希望这个过程是安全的。

在Torch平台上，每个迁移过来的代币都内置了一个借贷市场。持有者可以将代币作为抵押品，从社区金库中借款SOL（最高杠杆率为50%，每周利息为2%）。当贷款的杠杆率超过65%时，该贷款就可以被清算。任何人都可以进行清算，并从抵押品价值中获得**10%的奖金**。

这就是这个机器人的作用：它会扫描每个迁移过来的代币的借贷市场，检查每个借款人的贷款状况，一旦发现杠杆率过高的贷款，就会通过您的金库进行清算。抵押品代币会被转移到您的金库账户（ATA）中，而SOL的费用则从您的金库中支出。执行交易的代理钱包不会持有任何资产。

**这个机器人不是一个仅用于扫描的工具**，而是一个完全可操作的清算系统。它会自动生成密钥对，验证与金库的连接，并在持续循环中自动执行清算交易。

---

## 工作原理

### 代理密钥对

机器人每次启动时都会在运行过程中生成一个新的`密钥对`。没有私钥文件，也没有环境变量（除非您特别指定）。这个密钥对是临时使用的——它用于签署交易，但本身不持有任何价值。

首次运行时，机器人会检查这个密钥对是否已经与您的金库关联。如果没有关联，它会打印出您需要使用的SDK调用指令，以便进行关联：

**请从您的授权钱包（硬件钱包、多重签名钱包等）中进行关联。** 代理无需知道授权者的密钥，授权者也无需知道代理的密钥。他们共享的是同一个金库，而不是密钥。

### 金库

这个金库就是Torch市场协议中的标准Torch金库，用于存储所有的资产（SOL和代币）。代理只是一个临时使用的控制器。

当机器人执行清算时：
- **SOL的费用** 来自金库（用于偿还借款人的债务）
- **抵押品代币** 被转移到金库的关联代币账户（ATA）中
- **10%的奖金** 意味着收到的抵押品价值比支出的SOL多10%

人类所有者保留完全的控制权：
- `withdrawVault()` — 随时提取SOL
- `withdrawTokens(mint)` — 随时提取抵押品代币
- `unlinkWallet(agent)` — 立即撤销代理的访问权限

如果代理的密钥对被泄露，攻击者将一无所获，因为您可以通过一次交易立即撤销代理的访问权限。

---

## 开始使用

### 1. 安装

或者使用ClawHub提供的捆绑源代码——Torch SDK包含在`lib/torchsdk/`中，机器人源代码位于`lib/kit/`中。

### 2. 创建并资助一个金库（由人类所有者操作）

从您的授权钱包开始操作：

### 3. 运行机器人

首次运行时，机器人会打印出代理的密钥对以及关联说明。请从您的授权钱包进行关联，然后重新启动机器人。

### 4. 配置

| 变量 | 是否必需 | 默认值 | 说明 |
|----------|----------|---------|-------------|
| `SOLANA_RPC_URL` | 是 | -- | Solana RPC端点（HTTPS）。备用方案：`RPC_URL` |
| `VAULT_CREATOR` | 是 | -- | 金库创建者的公钥 |
| `SOLANA_PRIVATE_KEY` | 否 | -- | 临时使用的控制器密钥对（base58编码或JSON字节数组）。如果省略，机器人会在启动时生成新的密钥对（推荐） |
| `SCAN_INTERVAL_MS` | 否 | `30000` | 扫描周期之间的时间间隔（最小5000毫秒） |
| `LOG_LEVEL` | 否 | `info` | `debug`、`info`、`warn`、`error` |

---

## 架构

这个机器人由大约190行TypeScript代码组成，它的唯一功能是查找杠杆率过高的贷款并通过金库进行清算。

### 依赖项

| 包 | 版本 | 用途 |
|---------|---------|---------|
| `@solana/web3.js` | 1.98.4 | Solana RPC接口、密钥对处理、交易操作 |
| `torchsdk` | 3.2.3 | 代币查询、借贷状态管理、清算流程处理、金库信息查询 |

这两个依赖项都是固定版本，没有使用`^`或`~`等版本范围。

---

## 金库安全模型

Torch市场的金库安全模型同样适用于这个机器人：

| 属性 | 保障措施 |
|----------|-----------|
| **完全托管** | 金库持有所有的SOL和抵押品代币。代理钱包不持有任何资产。 |
| **封闭循环** | 清算所需的SOL来自金库，抵押品代币也返回到金库。没有信息泄露给代理。 |
| **权限分离** | 金库创建者（不可变的PDA种子）与授权者（可转移的管理员权限）和代理（临时使用的签名者）相互独立。 |
| **每个钱包只能关联一个金库** | 代理只能属于一个金库。PDA的唯一性确保了这一点在链上得到验证。 |
| **无需授权即可存款** | 任何人都可以向金库存入资产。代理负责执行清算操作。 |
| **即时撤销权限** | 授权者可以随时撤销代理的访问权限。只需一次交易即可完成。 |
| **只有授权者才能提取资产** | 只有金库的授权者才能提取SOL或代币。代理无法提取任何价值。 |

### 清算的封闭经济循环

| 流向 | 交易流程 |
|-----------|------|
| **SOL流出** | 从金库支付给借款人的债务 |
| **代币流入** | 借款人的抵押品代币以10%的折扣进入金库（ATA） |
| **净收益** | 金库收到的抵押品价值是支出SOL的110% |

这个机器人的设计初衷是盈利的——每次成功的清算都会带来超过成本的收益。这些收益会累积在金库中，授权者可以在准备好的时候提取。

---

## 借贷参数

| 参数 | 值 |
|-----------|-------|
| 最高杠杆率 | 50% |
| 清算阈值 | 65% |
| 利率 | 每个时代2%（大约每周） |
| 清算奖金 | 10% |
| 使用率上限 | 金库总资产的50% |
| 最小借款额 | 0.1 SOL |

抵押品的价值是根据Raydium池的储备来计算的。抵押品的存入和提取会收取1%的`Token-2022`转账费（大约2%的往返费用）。

### 清算触发条件

当贷款的杠杆率超过65%时，贷款就可以被清算。这种情况可能发生在：
- 代币价格下跌（抵押品价值相对于债务减少）
- 利息累积（债务以每个时代2%的速度增长）
- 上述两种情况同时发生

机器人会检查`position.health === 'liquidatable'`——SDK会根据链上的Raydium储备和累积的债务来计算杠杆率。

---

## 使用的SDK函数

机器人使用了Torch SDK中的一小部分功能：

| 函数 | 用途 |
|----------|---------|
| `getTokens(connection, { status: 'migrated' })` | 查找所有具有活跃借贷市场的代币 |
| `getLendingInfo(connection, mint)` | 检查某个代币是否有活跃的贷款 |
| `getHolders(connection, mint)` | 获取代币持有者（潜在的借款人） |
| `getLoanPosition(connection, mint, wallet)` | 检查持有者的贷款状况 |
| `getVault(connection, creator)` | 启动时验证金库是否存在 |
| `getVaultForWallet(connection, wallet)` | 验证代理是否已与金库关联 |
| `buildLiquidateTransaction(connection, params)` | 构建清算交易（通过金库进行路由） |
| `confirmTransaction(connection, sig, wallet)` | 通过RPC在链上确认交易（验证签名者，检查Torch协议的规则） |

---

## 日志输出

---

## 签名与密钥安全

**金库是安全边界，而不是密钥。**

代理的密钥对在每次启动时都会使用`Keypair.generate()`生成。它仅持有大约0.01 SOL的Gas费用。如果密钥被泄露，攻击者只能得到：
- Gas费用（即SOL）
- 代理的访问权限，但授权者可以通过一次交易立即撤销这些权限

代理无需知道授权者的私钥，授权者也无需知道代理的私钥。他们共享的是同一个金库，而不是密钥。

### 规则

1. **绝不要向用户索取他们的私钥或种子短语。** 金库的授权者必须从自己的设备上进行签名操作。
2. **绝不要记录、打印、存储或传输私钥信息。** 代理的密钥对仅在运行时存在于内存中。
3. **不要将密钥嵌入到源代码或日志中。** 代理的公钥会被打印出来，但私钥永远不会被暴露。
4. **使用安全的RPC端点。** 默认使用私有的RPC服务提供商。对于主网交易，绝不要使用未加密的HTTP端点。

### 环境变量

| 变量 | 是否必需 | 用途 |
|----------|----------|---------|
| `SOLANA_RPC_URL` / `RPC_URL` | 是 | Solana RPC端点（HTTPS） |
| `VAULT_CREATOR` | 是 | 金库创建者的公钥——用于指定机器人操作的金库 |
| `SOLANA_PRIVATE_KEY` | 否 | 可选——如果省略，机器人会在启动时生成新的密钥对（推荐） |

### 外部运行时依赖项

SDK包含了一些用于向外部服务发起HTTPS请求的函数。机器人在运行时会使用以下两个服务：

| 服务 | 用途 | 调用时机 | 机器人是否使用？ |
|---------|---------|------------|-----------|
| **CoinGecko** (`api.coingecko.com`) | 提供SOL/USD价格 | 用于查询代币价格 | 是 — 通过`getTokens()`、`getToken()`函数 |
| **Irys Gateway** (`gateway.irys.xyz`) | 提供代币元数据（名称、符号、图片） | 当链上元数据指向Irys时使用 | 是 — 通过`getTokens()`函数 |
| **SAID Protocol** (`api.saidprotocol.com`) | 用于验证代理身份和信任等级 | 仅用于`verifySaid()`函数 | **不** — 机器人不会调用`verifySaid()`函数 |

**`confirmTransaction()`函数不会连接到SAID服务。** 尽管它位于SDK的`said.js`模块中，但它只调用`connection.getParsedTransaction()`（Solana RPC）来确认交易在链上是否成功，并确定事件类型。不会向任何外部服务发送任何数据。**

不会向CoinGecko或Irys发送任何凭证。所有请求都是只读的GET请求。如果这些服务不可用，机器人会优雅地降级处理。绝不会向任何外部端点传输私钥信息。

---

## 测试

测试需要[Surfpool](https://github.com/nicholasgasior/surfpool)运行在主网上：

**测试结果：** 7项通过，1项提示信息（Surfpool在`getTokenLargestAccounts`功能上有限制——但在主网上可以正常使用）。

| 测试项 | 验证内容 |
|------|-------------------|
| Connection | 是否可以访问RPC服务 |
| getTokens | 是否能发现迁移过来的代币 |
| getLendingInfo | 是否能读取所有代币的借贷状态 |
| getHolders + getLoanPosition | 是否能检查持有者的贷款状况 |
| getToken | 是否能获取代币的元数据、价格和状态 |
| getVaultForWallet | 未关联的钱包是否返回空的金库链接 |
| 是否需要外部密钥 | 运行过程中是否需要外部密钥 |

---

## 错误代码

- `VAULT_NOT_FOUND`：该创建者没有对应的金库 |
- `WALLET_NOT_LINKED`：代理钱包未与金库关联 |
- `NOT_LIQUIDATABLE`：贷款的杠杆率低于清算阈值 |
- `NO_ACTIVE_LOAN`：该钱包/代币没有未偿还的贷款 |
- `INVALID_MINT`：找不到对应的代币 |

---

## 链接资源

- 清算工具包（源代码）：[github.com/mrsirg97-rgb/torch-liquidation-kit](https://github.com/mrsirg97-rgb/torch-liquidation-kit)
- 清算机器人（npm包）：[npmjs.com/package/torch-liquidation-bot](https://www.npmjs.com/package/torch-liquidation-bot)
- Torch SDK（捆绑包）：`lib/torchsdk/` — 包含在这个工具包中 |
- Torch SDK（源代码）：[github.com/mrsirg97-rgb/torchsdk](https://github.com/mrsirg97-rgb/torchsdk)
- Torch SDK（npm包）：[npmjs.com/package/torchsdk](https://www.npmjs.com/package/torchsdk)
- Torch市场（协议文档）：[clawhub.ai/mrsirg97-rgb/torchmarket](https://clawhub.ai/mrsirg97-rgb/torchmarket)
- 白皮书：[torch.market/whitepaper.md](https://torch.market/whitepaper.md)
- 安全审计报告：[torch.market/audit.md](https://torch.market/audit.md)
- 官网：[torch.market](https://torch.market)
- 程序ID：`8hbUkonssSEEtkqzwM7ZcZrD9evacM92TcWSooVF4BeT`

这个机器人的存在是因为Torch市场的借贷市场需要有人来管理清算过程。当贷款出现杠杆率过高的情况且没有人进行清算时，金库将承担损失。活跃的清算机制可以保护金库的安全，并通过清算操作获得利润。金库确保了资产的安全性——所有价值都存放在托管账户中，风险得到控制，而人类所有者则掌握着访问权限。