---
name: torch-liquidation-bot
version: "4.0.4"
description: 这是一个基于自动化的保险库的清算系统，专为Solana上的Torch Market借贷服务设计。该系统使用SDK内置的批量贷款扫描工具（getAllLoanPositions）来检测所有迁移过来的代币中是否存在“水下贷款”情况（即贷款价值超过代币总价值的65%）。一旦发现此类情况，系统会通过Torch Vault生成并执行清算交易，并从中收取10%的抵押品奖金。代理密钥对是在运行过程中生成的，属于一次性使用的密钥对，不持有任何有价值的资产。所有SOL代币及抵押品代币都会通过该保险库进行流转。用户（即贷款的发起者）负责创建保险库、为其提供资金、关联代理，并保留对该保险库的完全控制权。该系统基于torchsdk v3.7.22和Torch Market协议开发而成。
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
    install:
      - id: npm-torch-liquidation-bot
        kind: npm
        package: torch-liquidation-bot@^4.0.2
        flags: []
        label: "Install Torch Liquidation Bot (npm, optional -- SDK is bundled in lib/torchsdk/ and bot source is bundled under lib/kit on clawhub)"
  author: torch-market
  version: "4.0.4"
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
compatibility: >-
  REQUIRED: SOLANA_RPC_URL (HTTPS Solana RPC endpoint)
  REQUIRED: VAULT_CREATOR (vault creator pubkey).
  OPTIONAL: SOLANA_PRIVATE_KEY -- the bot generates a fresh disposable keypair in-process if not provided. The agent wallet holds nothing of value (~0.01 SOL for gas). All liquidation proceeds (collateral tokens) route to the vault. The vault can be created and funded entirely by the human principal. 
  This skill sets disable-model-invocation: true -- it must not be invoked autonomously without explicit user initiation.
  The Torch SDK is bundled in lib/torchsdk/ -- all source included for full auditability. No API server dependency.
  The vault can be created and funded entirely by the human principal -- the agent never needs access to funds.
---
# Torch 清算机器人

您使用本工具的原因是希望在 Torch 市场上运行清算机制，并且希望这一过程能够安全地进行。

Torch 上的每个迁移过来的代币都内置了借贷市场。持有者可以将代币作为抵押品，从社区金库中借入 SOL（最高杠杆率为 50%，年利率为 2%）。当贷款的杠杆率超过 65% 时，该贷款就可以被清算。任何人都可以进行清算，并从抵押品价值中获取 **10% 的奖金**。

这就是这个机器人的作用所在。

该机器人使用 SDK 的批量贷款扫描功能（`getAllLoanPositions`）来扫描每个迁移过来的代币的借贷市场——每个代币只需进行一次 RPC 调用，即可获取按健康状况排序的所有活跃贷款信息。一旦发现杠杆率过高的贷款，机器人就会通过您的金库进行清算。抵押品代币会被存入您的金库（ATA），而 SOL 的费用则从您的金库中支出。执行交易的代理钱包不会持有任何资产。

**这不仅仅是一个只读的扫描工具**，而是一个完全可操作的清算系统：它自动生成密钥对，验证与金库的连接，并在持续循环中自动执行清算交易。

---

## 工作原理

### 代理密钥对

机器人每次启动时都会在运行过程中生成一个新的 `密钥对`。没有私钥文件，也没有环境变量（除非您需要提供）。这个密钥对是一次性的——它用于签署交易，但本身不持有任何有价值的资产。

首次运行时，机器人会检查这个密钥对是否已与您的金库关联。如果没有关联，它会显示您需要使用的 SDK 调用命令，以便进行关联：

**从您的授权钱包（硬件钱包、多重签名钱包等）进行关联。** 代理永远不会需要授权者的密钥，授权者也永远不会需要代理的密钥。它们共享的是金库，而不是密钥。

### 金库

这个金库与完整的 Torch Market 协议中的金库相同，用于存储所有资产（SOL 和代币）。代理只是一个一次性的控制器。

当机器人清算某个贷款时：
- **SOL 的费用** 来自金库（用于偿还借款人的债务）
- **抵押品代币** 被存入金库的关联代币账户（ATA）
- **10% 的奖金** 意味着收到的抵押品价值比支出的 SOL 高出 10%

人类所有者保留完全的控制权：
- `withdrawVault()` — 随时提取 SOL
- `withdrawTokens(mint)` — 随时提取抵押品代币
- `unlinkWallet(agent)` — 立即撤销代理的访问权限

如果代理的密钥对被泄露，攻击者将一无所获，因为您可以通过一次交易立即撤销代理的访问权限。

---

## 开始使用

### 1. 安装

**或使用 ClawHub 提供的捆绑源代码** — Torch SDK 存放在 `lib/torchsdk/` 中，机器人源代码位于 `lib/kit/` 中。

### 2. 创建并资助金库（人类所有者）

从您的授权钱包开始操作：

---

### 3. 运行机器人

首次运行时，机器人会显示代理的密钥对以及关联说明。请从您的授权钱包进行关联，然后重新启动机器人。

### 4. 配置

| 变量 | 是否必需 | 默认值 | 说明 |
|----------|----------|---------|-------------|
| `SOLANA_RPC_URL` | 是 | -- | Solana RPC 端点（HTTPS）。备用：`RPC_URL` |
| `VAULT_CREATOR` | 是 | -- | 金库创建者的公钥 |
| `SOLANA_PRIVATE_KEY` | 否 | -- | 一次性使用的控制器密钥对（base58 或 JSON 字节数组）。如果省略，将在启动时生成新的密钥对（推荐） |
| `SCAN_INTERVAL_MS` | 否 | `30000` | 扫描周期之间的毫秒间隔（至少 5000 毫秒） |
| `LOG_LEVEL` | 否 | `info` | `debug`、`info`、`warn`、`error` |

---

## 架构

该机器人由大约 192 行 TypeScript 代码组成，它的唯一功能是查找杠杆率过高的贷款并通过金库进行清算。

### 依赖项

| 包 | 版本 | 用途 |
|---------|---------|---------|
| `@solana/web3.js` | 1.98.4 | Solana RPC、密钥对、交易处理 |
| `torchsdk` | 3.7.22 | 代币查询、批量贷款扫描、清算操作、金库查询 |

这两个依赖项都是固定版本的，没有使用 `^` 或 `~` 的版本范围。

---

## 金库安全模型

Torch Market 金库的所有七项安全保障同样适用于此机器人：

| 保障内容 | 保障措施 |
|----------|-----------|
| **全额托管** | 金库持有所有的 SOL 和抵押品代币。代理钱包不持有任何资产。 |
| **封闭循环** | 清算所需的 SOL 来自金库，抵押品代币也存入金库。没有信息泄露给代理。 |
| **权限分离** | 创建者（不可更改的 PDA 种子）与授权者（可转移的管理权限）与控制器（一次性使用的签名者）分离。 |
| **每个钱包只能关联一个金库** | 代理只能属于一个金库。PDA 的唯一性在链上得到了保障。 |
| **无需授权即可存款** | 任何人都可以向金库存款。代理负责执行清算操作。 |
| **即时撤销权限** | 授权者可以随时撤销代理的访问权限。只需一次交易即可完成。 |
| **仅授权者可提取资产** | 只有金库的授权者才能提取 SOL 或代币。代理无法提取任何资产。 |

### 清算的封闭经济循环

| 流向 | 交易流程 |
|-----------|------|
| **SOL 的去向** | 从金库支付给借款人的债务 |
| **抵押品代币的去向** | 借款人的抵押品代币存入金库（折价 10%） |
| **净收益** | 金库收到的抵押品价值是支出 SOL 的 110% |

该机器人的设计初衷是盈利的——每次成功的清算都会带来超过成本的收益。利润会累积在金库中。授权者可以在准备好的时候提取资金。

---

## 借贷参数

| 参数 | 值 |
|-----------|-------|
| 最高杠杆率 | 50% |
| 清算阈值 | 65% |
| 利率 | 每个时代（约每周）2% |
| 清算奖金 | 10% |
| 使用率上限 | 金库总资产的 70% |
| 最小借款金额 | 0.1 SOL |

抵押品的价值是根据 Raydium 池的储备来计算的。抵押品的存取会收取 0.03% 的 `Token-2022` 转移费（每枚代币 3 个基点，固定不变）。

### 清算触发条件

当贷款的杠杆率超过 65% 时，贷款就可以被清算。这种情况可能发生在：
- 代币价格下跌（抵押品价值相对于债务减少）
- 利息累积（债务以每个时代 2% 的速度增长）
- 上述两种情况同时发生

机器人会检查 `position.health === 'liquidatable'` — SDK 会根据链上的 Raydium 储备和贷款的累积债务来计算杠杆率。

---

## 使用的 SDK 函数

机器人使用了 Torch SDK 的部分功能：

| 函数 | 用途 |
|----------|---------|
| `getTokens(connection, { status: 'migrated' })` | 查找所有具有活跃借贷市场的代币 |
| `getAllLoanPositions(connection, mint)` | 批量扫描某个代币的所有活跃贷款——按健康状况排序（杠杆率过高的贷款优先显示），并获取一次池中的价格 |
| `getVault(connection, creator)` | 启动时验证金库是否存在 |
| `getVaultForWallet(connection, wallet)` | 验证代理是否已与金库关联 |
| `buildLiquidateTransaction(connection, params)` | 构建清算交易（通过金库路由） |
| `confirmTransaction(connection, sig, wallet)` | 通过 RPC 在链上确认交易（验证签名者，检查 Torch 的指令） |

---

## 扫描和清算流程

---

## 日志输出

---

## 签名与密钥安全

**金库是安全边界，而不是密钥。**

代理的密钥对在每次启动时都会使用 `Keypair.generate()` 生成。它持有大约 0.01 SOL 作为 gas 费用。如果密钥被泄露，攻击者只能得到：
- 用于支付 gas 费用的 SOL
- 代理的访问权限，但该权限可以通过一次交易被授权者立即撤销

代理永远不会需要授权者的私钥，授权者也永远不会需要代理的私钥。它们共享的是金库，而不是密钥。

### 规则

1. **永远不要向用户索取他们的私钥或种子短语。** 授权者必须从自己的设备上进行签名操作。
2. **永远不要记录、打印、存储或传输私钥信息。** 代理的密钥对仅在运行时存在于内存中。
3. **永远不要将密钥嵌入源代码或日志中。** 代理的公钥会被显示出来，但私钥永远不会被暴露。
4. **使用安全的 RPC 端点。** 默认使用私有的 RPC 提供者。对于主网交易，绝不要使用未加密的 HTTP 端点。

### RPC 超时设置

所有 SDK 调用都设置了 30 秒的超时限制（`utils.ts` 中的 `withTimeout`）。如果 RPC 端点挂起或无响应，机器人不会无限期地等待——调用会被拒绝，错误会被扫描循环捕获，然后机器人会继续处理下一个代币或下一个扫描周期。

### 环境变量

| 变量 | 是否必需 | 用途 |
|----------|----------|---------|
| `SOLANA_RPC_URL` / `RPC_URL` | 是 | Solana RPC 端点（HTTPS） |
| `VAULT_CREATOR` | 是 | 金库创建者的公钥 — 用于标识机器人操作的金库 |
| `SOLANA_PRIVATE_KEY` | 否 | 可选 — 如果省略，机器人将在启动时生成新的密钥对（推荐） |

### 外部运行时依赖项

SDK 包含了一些用于发起外部 HTTPS 请求的函数。机器人的运行时路径会调用 **两个** 外部服务：

| 服务 | 用途 | 调用时机 | 机器人是否使用？ |
|---------|---------|------------|-----------|
| **CoinGecko** (`api.coingecko.com`) | 提供 SOL/USD 价格 | 用于显示价格 | 是 — 通过 `getTokens()`、`getToken()` 调用 |
| **Irys Gateway** (`gateway.irys.xyz`) | 代币元数据备用信息（名称、符号、图片） | 当链上元数据 URI 指向 Irys 时使用 | 是 — 通过 `getTokens()` 调用 |
| **SAID Protocol** (`api.saidprotocol.com`) | 用于代理身份验证和信任等级查询 | 仅 `verifySaid()` 调用 | **不** — 机器人不会调用 `verifySaid()` |

**`confirmTransaction()` 不会调用 SAID。** 尽管它位于 SDK 的 `said.js` 模块中，但它只调用 `connection.getParsedTransaction()`（Solana RPC）来确认交易在链上是否成功，并确定事件类型。不会向任何外部服务发送任何数据。**

不会向 CoinGecko 或 Irys 发送任何凭证。所有请求都是只读的 GET 请求。如果任一服务不可用，SDK 会优雅地降级处理。永远不会向任何外部端点传输私钥信息。

---

## 测试

需要运行 [Surfpool](https://github.com/nicholasgasior/surfpool) 的主网分支来进行测试：

**测试结果：** 9 项通过，0 项失败（Surfpool 主网分支）。

| 测试项 | 验证内容 |
|------|-------------------|
| Connection | 是否可以访问 RPC 端点 |
| getTokens | 是否能发现迁移过来的代币 |
| getLendingInfo | 是否能读取所有代币的借贷状态 |
| getAllLoanPositions | 是否能批量扫描活跃贷款，并验证排序顺序（杠杆率过高的贷款优先显示） |
| getToken | 是否能获取代币的元数据、价格和状态 |
| getVaultForWallet | 未关联的钱包是否返回空的金库信息 |
| 是否需要外部密钥 | 运行过程中是否需要外部密钥 |

---

## 错误代码

- `VAULT_NOT_FOUND`：该创建者没有对应的金库 |
- `WALLET_NOT_LINKED`：代理钱包未与金库关联 |
- `NOT_LIQUIDATABLE`：贷款的杠杆率低于清算阈值 |
- `NO_ACTIVE_LOAN`：该钱包/代币没有未偿还的贷款 |
- `INVALID_MINT`：找不到对应的代币

---

## 链接

- 清算工具包（源代码）：[github.com/mrsirg97-rgb/torch-liquidation-kit](https://github.com/mrsirg97-rgb/torch-liquidation-kit)
- 清算机器人（npm 包）：[npmjs.com/package/torch-liquidation-bot](https://www.npmjs.com/package/torch-liquidation-bot)
- Torch SDK（捆绑包）：`lib/torchsdk/` — 包含在本技能中 |
- Torch SDK（源代码）：[github.com/mrsirg97-rgb/torchsdk](https://github.com/mrsirg97-rgb/torchsdk)
- Torch SDK（npm 包）：[npmjs.com/package/torchsdk](https://www.npmjs.com/package/torchsdk)
- Torch Market（协议相关技能）：[clawhub.ai/mrsirg97-rgb/torchmarket](https://clawhub.ai/mrsirg97-rgb/torchmarket)
- 白皮书：[torch.market/whitepaper.md](https://torch.market/whitepaper.md)
- 安全审计报告：[torch.market/audit.md](https://torch.market/audit.md)
- 官网：[torch.market](https://torch.market)
- 程序 ID：`8hbUkonssSEEtkqzwM7ZcZrD9evacM92TcWSooVF4BeT`

这个机器人的存在是因为 Torch 的借贷市场需要专门的清算机制。当贷款出现杠杆率过高的情况且没有人进行清算时，金库将承担损失。活跃的清算机制可以保护金库的安全，并通过清算操作获得利润。金库确保了安全性——所有资产都存放在托管账户中，风险得到控制，而人类所有者则掌握着密钥。