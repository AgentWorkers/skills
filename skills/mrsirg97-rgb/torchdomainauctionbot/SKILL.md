---
name: torch-domain-auction-bot
version: "1.0.2"
description: Solana上的域名借贷协议：域名被转换为代币（tokens），这些代币可用作抵押品。持有最多代币的人可以控制相应的域名。用户可以借用SOL来维持自己的头寸（position），但如果头寸被清算（liquidated），用户将失去对应的域名。该协议基于Torch SDK v3.2.3和Torch Market协议构建。
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
      - id: npm-torch-domain-auction-bot
        kind: npm
        package: torch-domain-auction-bot@^1.0.2
        flags: []
        label: "Install Torch Domain Auction Bot (npm, optional -- SDK is bundled in lib/torchsdk/, kit is in lib/kit/)"
  author: torch-market
  version: "1.0.2"
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
compatibility: Requires SOLANA_RPC_URL and VAULT_CREATOR. SOLANA_PRIVATE_KEY optional. Agent wallet holds nothing. All value in vault. SDK bundled in lib/torchsdk/, kit (bot + scraper) in lib/kit/.
---

# Torch域名拍卖系统

在Torch系统中，域名被转化为代币，这些代币又可以作为抵押品。代币的持有者控制着相应的域名。

---

## 系统原理

每个域名都有一个名称，每个名称都有一个价格。但这个价格究竟由谁来决定呢？

在Torch市场上，域名以代币的形式发布，并附带一个“绑定曲线”（bonding curve）。价格由市场机制决定。一旦代币迁移到Raydium平台，域名就会与这些代币永久绑定。从那时起：

- **代币的持有者控制着域名**：持有足够数量的代币，就可以获得该域名；如果有人购买了更多的代币，他们就能获得域名。
- **持有者可以借用SOL（Torch的数字货币）**：将代币作为抵押品，从而获得流动性——最高杠杆率为50%，每周利息为2%。
- **违约会导致域名丢失**：如果贷款违约（杠杆率超过65%），任何人都可以强制清算你的资产，域名将转交给新的持有者。

这种机制在传统的域名市场中是不存在的：它创造了一种“价格持续波动、可借贷、具有流动性的域名资产”，并且对过度杠杆使用有明确的惩罚措施。

该工具中的机器人负责运行系统的基础设施部分。它负责发现具有潜力的域名，将其转化为代币，监控所有活跃的借贷交易，并通过Torch的清算机制处理违约情况。一旦发生违约，域名会自动重新分配给新的持有者。

---

## 域名的运作流程

### 第一阶段：发布（绑定曲线）

域名以Torch市场代币的形式发布。绑定曲线决定了初始价格——早期买家可以以较低的价格购买代币，随着需求增加，价格会逐渐上升。这是价格发现的过程。

```
domain "pixel.art"  →  token PIXEL  →  bonding curve  →  market cap grows
```

任何人都可以购买这些代币。价格由绑定曲线决定，交易费用会流入社区金库。

### 第二阶段：迁移（域名与代币的永久绑定）

当绑定曲线完成之后，代币会被迁移到Raydium的流动性池中。此时，域名与代币实现永久绑定。该域名不再被从市场上撤下，也没有到期日，也没有中央管理机构。代币本身就代表了域名。

### 第三阶段：借贷

迁移完成后，Torch内置的借贷市场开始运作。任何持有者都可以将代币作为抵押品，从社区金库中借款SOL。

```
holder locks 10,000 PIXEL tokens  →  borrows 0.5 SOL  →  LTV = 40%
```

借款的利息为每个时代周期（约一周）2%。只要借款人的杠杆率低于65%，他们就可以继续持有域名。

### 第四阶段：清算（域名重新分配）

如果代币价格下跌或利息累积导致杠杆率超过65%，借款人的头寸将被清算。清算者会使用金库中的SOL偿还债务，并以10%的折扣获取借款人的抵押代币。

```
PIXEL price drops  →  LTV hits 68%  →  keeper liquidates  →  collateral moves to vault
                                                            →  top holder changes
                                                            →  domain lease rotates
```

借款人将失去代币，域名将转交给新的最大持有者。清算者从交易中获得的10%折扣中获利。

**关键点在于：清算不仅有财务后果，还会导致借款人失去对域名的控制权。**这种机制使得借贷市场变得有意义，因为借款人有动力保持健康的借贷状态。

---

## 机器人的功能

### 扫描循环

机器人持续运行以下循环：
1. **扫描**：发现所有已迁移且仍有活跃借贷交易的域名代币。
2. **评分**：根据四个因素为每个借款人计算风险评分：
   - 杠杆率（35%）：距离违约阈值65%的距离。
   - 价格走势（25%）：代币的最新价格走势（价格下跌会增加风险）。
   - 钱包信誉（20%）：SAID协议的验证状态和交易历史。
   - 利息负担（20%）：累计利息与本金的比例。
3. **清算**：对风险评分超过阈值的头寸执行清算。
4. **重新分配域名**：检查当前的代币持有者，并更新域名的所有权。
5. **等待下一个周期**。

### 代理密钥对

机器人每次启动时都会生成一个新的密钥对。无需使用私钥文件。这个密钥对仅用于签名交易，本身没有价值（签名费用约为0.01 SOL）。

首次运行时，机器人会验证与金库的连接情况。如果代理未正确连接，它会显示相应的操作指南。

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

### 金库

所有经济活动都通过Torch的金库进行处理：
- **清算**：金库使用SOL偿还借款人的债务。
- **抵押品转移**：借款人的抵押代币以10%的折扣转入金库。
- **每次清算的净收益**：金库获得的抵押品价值是支出SOL的110%。
- **域名重新分配**：抵押品转移后，域名所有权和租赁权也会相应变更。

人类管理者可以完全控制金库：
- 随时从金库中提取SOL。
- 随时提取被清算的代币。
- 通过一次交易撤销代理的访问权限。

如果代理的密钥对被盗，攻击者将无法获取任何资产，同时管理者可以立即撤销代理的访问权限。

---

## 使用说明

### 1. 安装

### 2. 创建并资助金库

### 3. 运行机器人

首次运行时，机器人会生成代理的钱包信息，并将其与管理员的钱包连接后重新启动。

### 配置参数

| 参数 | 是否必需 | 默认值 | 说明 |
|---------|---------|---------|-------------|
| `SOLANA_RPC_URL` | 是 | -- | Solana的RPC接口地址（默认为`BOT_RPC_URL`） |
| `VAULT_CREATOR` | 是 | -- | 金库创建者的公钥 |
| `SOLANA_PRIVATE_KEY` | 否 | -- | 代理的密钥对（Base58编码或JSON格式）。省略此参数可生成新的密钥对 |
| `BOT_SCAN_INTERVAL_MS` | 否 | `60000` | 扫描周期（最小值5000毫秒） |
| `BOTSCORE_INTERVAL_MS` | 否 | 评分周期（15000毫秒） |
| `BOT_MIN_PROFIT_LAMPORTS` | 否 | 最小清算利润（0.01 SOL） |
| `BOT_RISK_THRESHOLD` | 否 | 最小风险评分（0-100） |
| `BOT PRICE_HISTORY_DEPTH` | 否 | 保留的价格历史记录数量（20条） |
| `BOT_LOG_LEVEL` | 否 | 日志级别（`info`、`warn`、`error`） |

---

## 系统架构

---

## 域名借贷机制

该工具展示了如何使用Torch市场的组件来构建一个可扩展的系统：

### 组件说明

每个步骤都使用了Torch的不同基础设施：
- **绑定曲线**：用于价格发现。
- **Raydium迁移**：确保代币的流动性。
- **社区金库**：提供借贷资金。
- **借贷市场**：支持基于抵押品的借贷。
- **金库**：确保系统安全自主运行。
- **清算机制**：维护市场稳定并实现域名重新分配。

其他开发者可以利用这一模式来处理各种资产类型——不仅仅是域名，还包括NFT、实物资产、预测市场或治理代币。基本流程是：**将资产代币化 → 提供借贷 → 清算 → 重新分配所有权**。

---

## 金库的安全性

- **全托管**：金库持有所有的SOL和抵押品，代理没有任何控制权。
- **闭环管理**：清算过程中，SOL和抵押品代币都会回到金库，确保没有信息泄露。
- **权限分离**：金库的创建者、管理员和操作者之间的权限明确分离。
- **即时撤销**：管理员可以通过一次交易立即撤销代理的访问权限。
- **仅管理员可操作**：代理无法从金库中提取任何资产。

---

## 借贷参数

| 参数 | 值 |
|---------|-------|
| 最高杠杆率 | 50% |
| 清算阈值 | 65% |
| 利息率 | 每个时代周期2% |
| 清算折扣 | 10% |
| 借贷上限 | 金库资金的50% |
| 最小借款金额 | 0.1 SOL |

---

## 使用的SDK函数

| 函数 | 功能 |
|---------|---------|
| `getTokens({ status: 'migrated' })` | 查找已迁移的域名代币 |
| `getToken(mint)` | 获取代币详情（价格、元数据） |
| `getLendingInfo(mint)` | 获取借贷市场信息 |
| `getHolders(mint)` | 获取代币持有者信息（潜在借款人） |
| `getLoanPosition(mint, wallet)` | 检查借款人的借贷状况 |
| `getVault(creator)` | 验证金库是否存在 |
| `getVaultForWallet(wallet)` | 验证代理是否已连接到金库 |
| `buildLiquidateTransaction(params)` | 执行清算交易 |
| `buildCreateTokenTransaction(params)` | 发布新的域名代币 |
| `verifySaid(wallet)` | 检查借款人的信誉 |

---

## 外部API调用

该工具会向以下服务发送HTTPS请求。所有请求均为只读的GET或HEAD请求，不会传输任何私钥信息。如果某个服务不可用，系统会优雅地降级（捕获错误并继续运行）。

### 外部服务说明

| 服务 | URL | 功能 | 发送的数据 |
|---------|-----|---------|-----------|
| **ExpiredDomains.net** | `https://www.expireddomains.net/domain-name-search/` | 获取即将到期的域名列表 | 仅发送请求头（GET请求） |
| **RDAP** | `https://rdap.org/domain/{name}.{tld}` | 检查域名是否可用（404表示可用） | 域名作为URL参数（公开信息） |

### 通过Torch SDK的间接调用

| 服务 | URL | 功能 | 发送的数据 |
|---------|-----|---------|-----------|
| **Solana RPC** | 使用用户提供的`SOLANA_RPC_URL` | 执行所有链上操作和交易提交 | 包括公钥和签名交易信息 |
| **CoinGecko** | `https://api.coingecko.com/api/v3/simple/price` | 获取代币的SOL/USD价格 | 仅发送GET请求 |
| **SAID Protocol** | `https://api.saidprotocol.com/api/verify/{wallet}` | 验证钱包信誉 | 包含钱包地址（非敏感信息） |
| **Irys Gateway** | `https://gateway.irys.xyz/...` | 获取代币元数据 | 仅发送GET请求 |

---

## 安全注意事项

- **金库是安全的核心**：切勿请求或存储私钥或种子短语。
- **严禁记录、存储或传输私钥信息**。
- **不要在源代码中嵌入私钥**。
- **使用HTTPS进行主网通信**。

代理的密钥对仅在运行时存在于内存中。如果被泄露，攻击者将无法获取任何资产，管理员可以通过一次交易立即撤销代理的访问权限。

---

## 测试要求

测试需要使用[Surfpool](https://github.com/nicholasgasior/surfpool)的主网分支：

- 测试内容包括：创建借款人账户、扫描域名、评估风险、执行清算、查看价格历史记录等。
- 还包括与模拟服务集成进行域名验证等测试。

---

## 重要性

传统的域名市场缺乏透明度：价格通常由注册商或私下协商决定，缺乏流动性——你购买域名后，它只能留在你的账户中，直到你出售。

该工具将域名转化为可借贷、价格持续波动的资产。市场机制决定了价格，任何人都可以购买域名。持有者可以在不出售的情况下获取流动性。如果他们过度杠杆使用，域名将转交给更愿意支付的人。

这就是Torch系统各组件的强大之处：绑定曲线、借贷市场、金库和清算机制共同构成了一个高效、安全的系统。

---

## 链接资源

- 项目源代码：[github.com/mrsirg97-rgb/torch-domain-auction-bot](https://github.com/mrsirg97-rgb/torch-domain-auction-bot)
- Torch SDK（打包版本）：`lib/torchsdk/`
- Torch SDK（npm安装包）：[npmjs.com/package/torchsdk](https://www.npmjs.com/package/torchsdk)
- Torch市场：[torch.market](https://torch.market)
- 项目ID：`8hbUkonssSEEtkqzwM7ZcZrD9evacM92TcWSooVF4BeT`