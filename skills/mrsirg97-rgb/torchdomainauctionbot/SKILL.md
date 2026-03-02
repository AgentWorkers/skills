---
name: torch-domain-auction-bot
version: "2.0.1"
description: Solana平台上的域名借贷协议：域名被转换为代币（tokens），这些代币可用作抵押品。持有最多代币的人可以控制相应的域名。用户可以通过抵押代币来借款SOL（Solana加密货币），但如果未能按时偿还借款，其抵押的域名将被没收。该协议基于Torch SDK v3.7.23和Torch Market协议构建。
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
      - id: npm-torch-domain-auction-bot
        kind: npm
        package: torch-domain-auction-bot@^2.0.1
        flags: []
        label: "Install Torch Domain Auction Bot (npm, optional -- SDK is bundled in lib/torchsdk/, kit is in lib/kit/)"
  author: torch-market
  version: "2.0.1"
  clawhub: https://clawhub.ai/mrsirg97-rgb/torch-domain-auction-bot
  kit-source: https://github.com/mrsirg97-rgb/torch-domain-auction-bot
  website: https://torch.market
  program-id: 8hbUkonssSEEtkqzwM7ZcZrD9evacM92TcWSooVF4BeT
  keywords:
    - solana
    - defi
    - domains
    - domain-lending
    - domain-collateral
    - domain-lease
    - liquidation
    - vault-custody
    - ai-agents
    - torch-market
  categories:
    - solana-protocols
    - defi-primitives
    - lending-markets
    - domain-services
    - agent-infrastructure
compatibility: >-
  REQUIRED: SOLANA_RPC_URL (HTTPS Solana RPC endpoint)
  REQUIRED: VAULT_CREATOR (vault creator pubkey).
  OPTIONAL: SOLANA_PRIVATE_KEY -- the kit generates a fresh disposable keypair in-process if not provided. The agent wallet holds nothing of value (~0.01 SOL for gas). All token creation and seed liquidity SOL routes through the vault. The vault can be created and funded entirely by the human principal.
  This skill sets disable-model-invocation: true -- it must not be invoked autonomously without explicit user initiation.
  The Torch SDK is bundled in lib/torchsdk/ -- all source included for full auditability. No API server dependency.
  Oracle resolution uses CoinGecko public API (read-only, no key required). The vault can be created and funded entirely by the human principal -- the agent never needs access to funds.
---
# Torch域名拍卖系统

在Torch系统中，域名被转化为代币（tokens），这些代币又可以作为抵押品。代币的持有者控制着相应的域名。

---

## 系统原理

每个域名都有一个名称，每个名称都有一个价格。但这个价格究竟由谁来决定呢？

在Torch市场上，域名以代币的形式发布，并附带一个“绑定曲线”（bonding curve）。市场价格由市场本身决定。当代币迁移到Raydium平台后，域名就与这些代币永久绑定在一起。从那时起：

- **代币的持有者控制着域名**：持有足够数量的代币，就可以获得该域名；如果有人购买了更多的代币，他们就会成为新的域名持有者。
- **持有者可以借用SOL（Torch的加密货币）**：将代币作为抵押品，从而获得流动性——最高杠杆率为50%，年利率为2%。
- **违约会导致域名丢失**：如果借款人的杠杆率超过65%，任何人都可以强制清算他们的资产，域名将转移给新的持有者。

这种机制在传统的域名市场中是不存在的：它创造了一种“价格持续波动、可借贷、具有流动性的域名资产”，并且对过度杠杆使用有明确的惩罚机制。

该工具中的机器人负责管理系统的基础设施部分。它负责发现具有潜力的域名，将其转化为代币，监控所有活跃的借贷交易，并通过Torch的“保险库”（vault）执行违约清算。一旦发生清算，域名就会自动转移给新的持有者。

---

## 域名的运作流程

### 第一阶段：发布（绑定曲线）

域名以Torch市场代币的形式发布。绑定曲线决定了初始价格——早期买家可以以较低的价格购买代币，随着需求增加，价格会逐渐上升。这是价格发现的过程。

```
domain "pixel.art"  →  token PIXEL  →  bonding curve  →  market cap grows
```

任何人都可以购买这些代币。价格由市场决定，交易费用会流入社区金库。

### 第二阶段：迁移（域名与代币永久绑定）

当绑定曲线完成时，代币会被迁移到Raydium的流动性池中。此时，域名就与代币永久绑定，没有退市或到期日期，也没有中央管理机构。代币本身就代表了域名。

### 第三阶段：借贷（用域名作为抵押品借款）

迁移完成后，Torch内置的借贷市场就会启动。持有者可以将代币作为抵押品，从社区金库中借款SOL。

```
holder locks 10,000 PIXEL tokens  →  borrows 0.5 SOL  →  LTV = 40%
```

借款会产生2%的利息（按周期计算）。只要借款人的杠杆率低于65%，他们就能继续持有域名。

### 第四阶段：清算（域名转移）

如果代币价格下跌或利息累积导致杠杆率超过65%，借款人的头寸就会被清算。清算方会使用保险库中的SOL来偿还债务，并以10%的折扣获取借款人的抵押品代币。

```
PIXEL price drops  →  LTV hits 68%  →  keeper liquidates  →  collateral moves to vault
                                                            →  top holder changes
                                                            →  domain lease rotates
```

借款人会失去代币，域名将转移给新的持有者。清算方会从这次交易中获得10%的利润。

**关键点在于：清算不仅有财务后果，还会导致域名控制权的转移。**借款人不仅会损失资金，还会失去对域名的控制权。这种机制使得借贷市场更加有意义，因为借款人有动力保持健康的头寸。

---

## 机器人的功能

### 扫描循环

机器人持续运行以下循环：
1. **扫描**：发现所有已迁移且仍有活跃借贷交易的域名代币。
2. **评分**：根据四个因素为每个借款人计算风险评分：
   - 杠杆率（35%）：距离清算阈值65%的距离。
   - 价格走势（25%）：最近的代币价格变化。
   - 钱包信誉（20%）：SAID协议的验证状态和交易历史。
   - 利息负担（20%）：累积的利息与本金的比例。
3. **清算**：对风险评分超过阈值的头寸执行清算。
4. **更新域名持有者**：检查当前的最大代币持有者，并更新域名的租赁权。
5. **等待下一次循环**。

### 代理密钥对

机器人会在每次启动时生成一个新的密钥对。不需要私钥文件。这个密钥对是一次性的，用于签名交易，但本身没有价值（大约0.01 SOL的Gas费用）。

首次运行时，机器人会验证与保险库的连接。如果代理未连接，它会显示相应的操作说明。

```
=== torch domain auction bot ===
agent wallet: 7xK9...
vault creator: 4yN2...
scan interval: 60000ms

--- ACTION REQUIRED ---
agent wallet is NOT linked to the vault.
link it by running (from your authority wallet):

  buildLinkWalletTransaction(connection, {
    authority: "<your-authority-pubkey>",
    vault_creator: "4yN2...",
    wallet_to_link: "7xK9..."
  })

then restart the bot.
-----------------------
```

### 保险库

所有经济活动都通过Torch的保险库进行：
- **清算**：保险库使用SOL偿还借款人的债务。
- **抵押品转移**：借款人的抵押品代币以10%的折扣转移至保险库。
- **每次清算的净收益**：保险库获得的抵押品价值是借款金额的110%。
- **域名转移**：抵押品转移后，域名控制权会转移给新的持有者。

人类管理者可以完全控制保险库：
- 随时从保险库中提取SOL。
- 随时提取抵押品代币。
- 通过一次交易撤销代理的访问权限。

如果代理的密钥对被泄露，攻击者将无法获取任何信息，且管理者的访问权限也会立即被撤销。

---

## 使用说明

### 1. 安装

### 2. 创建并资助保险库

### 3. 运行机器人

首次运行时，机器人会生成代理的钱包信息，并将其与管理者钱包关联后重新启动。

### 配置参数

| 参数 | 是否必需 | 默认值 | 说明 |
|----------|----------|---------|-------------|
| `SOLANA_RPC_URL` | 是 | -- | Solana的RPC接口地址（默认使用`BOT_RPC_URL`） |
| `VAULT_CREATOR` | 是 | -- | 保险库创建者的公钥 |
| `SOLANA_PRIVATE_KEY` | 否 | -- | 代理的密钥对（Base58编码或JSON格式）。省略此参数可在启动时生成新的密钥对 |
| `BOT_SCAN_INTERVAL_MS` | 否 | `60000` | 扫描周期（最小5000毫秒） |
| `BOTSCORE_INTERVAL_MS` | 否 | `15000` | 评分周期 |
| `BOT_MIN_PROFIT_LAMPORTS` | 否 | 最小清算利润（0.01 SOL） |
| `BOT_RISK_THRESHOLD` | 否 | 最小风险评分（0-100） |
| `BOT PRICE_HISTORY_DEPTH` | 否 | 保留的价格快照数量 |
| `BOT_LOG_LEVEL` | 否 | 日志级别（`info`, `warn`, `error`） |

---

## 系统架构

---

## 域名借贷机制

该工具展示了如何使用Torch市场的组件来实现这一功能：
- **绑定曲线**用于价格发现。
- **Raydium迁移**确保代币的流动性。
- **社区金库**提供借贷资金。
- **借贷市场**支持基于抵押品的借贷。
- **保险库**确保操作的安全性。
- **清算机制**维护市场秩序并实现域名转移。

其他开发者也可以将这一模式应用于其他资产类型——不仅仅是域名，例如NFT、实物资产、预测市场或治理代币。基本流程是：**代币化 → 借贷 → 清算 → 权限转移**。

---

## 保险库的安全性

- **完全托管**：保险库保管所有SOL和抵押品，代理没有任何控制权。
- **闭环系统**：清算时，SOL会从保险库中支付，抵押品代币也会返回保险库，确保没有信息泄露。
- **权限分离**：创建者（PDA种子密钥）、管理者（管理员）和操作代理（一次性使用的签名者）之间有明确的权限划分。
- **即时撤销**：管理者可以通过一次交易立即撤销代理的访问权限。
- **仅管理者可提取资金**：代理无法从保险库中提取任何资金。

---

## 借贷参数

| 参数 | 值 |
|---------|-------|
| 最高杠杆率 | 50% |
| 清算阈值 | 65% |
| 利率 | 每周期2%（约每周） |
| 清算折扣 | 10% |
| 借贷上限 | 金库资金的50% |
| 最小借款金额 | 0.1 SOL |

---

## 使用的SDK函数

| 函数 | 功能 |
|----------|---------|
| `getTokens({ status: 'migrated' })` | 获取已迁移的域名代币 |
| `getToken(mint)` | 获取代币详情（价格、元数据） |
| `getLendingInfo(mint)` | 获取借贷市场信息 |
| `getHolders(mint)` | 获取代币持有者（潜在借款人） |
| `getLoanPosition(mint, wallet)` | 检查借款人的借贷状况 |
| `getVault(creator)` | 验证保险库是否存在 |
| `getVaultForWallet(wallet)` | 验证代理是否已连接 |
| `buildLiquidateTransaction(params)` | 通过保险库执行清算 |
| `buildCreateTokenTransaction(params)` | 发布新的域名代币 |
| `verifySaid(wallet)` | 检查借款人的信誉 |

---

## 外部API调用

该工具会向以下服务发送HTTPS请求。机器人运行时会使用其中五个服务。不会向任何外部服务发送敏感信息，所有请求都是只读的（GET或HEAD请求）。如果某个服务不可用，机器人会优雅地处理错误并继续处理下一个代币。

### 外部服务列表

| 服务 | URL | 功能 | 发送的数据 |
|---------|-----|---------|-----------|
| **ExpiredDomains.net** | `https://www.expireddomains.net/domain-name-search/` | 获取即将到期的域名列表 | 仅发送请求头（GET请求） |
| **RDAP** | `https://rdap.org/domain/{name}.{tld}` | 检查域名是否可用 | 域名（公开信息） |
| **Solana RPC** | 使用用户提供的`SOLANA_RPC_URL` | 执行链上操作 | 公开密钥、签名交易信息 |
| **CoinGecko** | `https://api.coingecko.com/api/v3/simple/price` | 获取代币价格 | 仅发送请求（GET请求） |
| **SAID Protocol** | `https://api.saidprotocol.com/api/verify/{wallet}` | 验证钱包信誉 | 钱包地址（公开信息） |

---

## 安全措施

**保险库是安全的核心**：
- 代理的密钥对在每次启动时都会重新生成。它仅用于支付Gas费用（大约0.01 SOL）。
- 如果密钥被泄露，攻击者只能获得少量的Gas费用，并且管理者的访问权限会被立即撤销。
- 代理不需要管理者的私钥，管理者也不需要代理的私钥。两者共享同一个保险库，但各自持有不同的密钥。

### 安全规则

- **切勿向用户索取私钥或种子短语**：管理者始终在自己的设备上进行操作。
- **切勿记录、打印或传输私钥**：代理的密钥对仅在运行时存在于内存中。
- **不要将密钥嵌入源代码或日志中**：代理的公钥会被打印出来，但私钥永远不会被暴露。
- **使用安全的RPC接口**：默认使用加密的RPC服务。

### RPC超时设置

所有SDK调用都设置了30秒的超时限制。如果RPC接口响应延迟或无法响应，机器人会立即停止当前操作并继续处理下一个代币。

---

## 测试要求

测试需要使用[Surfpool](https://github.com/nicholasgasior/surfpool)的主网分支。

### 测试内容

包括：创建借款人账户、扫描系统、评估风险、执行清算、查看价格历史、管理借贷信息等。此外还包括模拟数据源的测试。

---

## 重要性

传统的域名市场缺乏透明度：价格由注册商或私下协商决定，缺乏流动性——用户购买域名后，域名会一直保留在账户中直到出售。

该工具将域名转化为可借贷、价格波动的资产。市场价格由市场决定，任何人都可以购买。持有者可以在不出售的情况下获取流动性。如果过度杠杆使用，域名会转移给更愿意持有它的人。

这就是Torch系统各组件的强大之处：绑定曲线、借贷市场、保险库和清算机制共同构成了一个完整、高效的系统。

---

## 链接

- 项目源代码：[github.com/mrsirg97-rgb/torch-domain-auction-bot](https://github.com/mrsirg97-rgb/torch-domain-auction-bot)
- Torch SDK：`lib/torchsdk/`
- Torch SDK（npm包）：[npmjs.com/package/torchsdk](https://www.npmjs.com/package/torchsdk)
- Torch市场：[torch.market](https://torch.market)
- 项目ID：`8hbUkonssSEEtkqzwM7ZcZrD9evacM92TcWSooVF4BeT`

## 更新日志

### v2.0.1

- **将Torch SDK升级至3.7.23**：新增了金库锁定功能、动态检测Raydium网络状态、在绑定曲线完成时自动执行迁移操作、通过保险库进行Raydium交易、收集费用、批量处理借贷请求、查询链上代币元数据等功能。
- **更新了环境配置格式**：环境变量声明采用了结构化的`name`/`required`格式，以兼容ClawHub和OpenClaw等工具。
- **新增了关于ClawBot的配置信息**：ClawBot的运行环境要求现在也有明确说明。