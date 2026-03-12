---
name: openpump-solana-mcp
description: >
  **Solana代币发行与交易工具：通过OpenPump MCP服务器实现**  
  该工具支持在`pump.fun`平台上创建代币、买卖代币、运行做市策略、抢先购买新发行的代币、设置止损订单、生成虚拟地址（vanity addresses）、管理托管钱包、转移SOL和SPL代币、查询账户余额、获取价格报价、监控投资组合持仓及创作者费用等操作。  
  **适用场景：**  
  - 当用户需要发行代币、在`pump.fun`平台上交易代币、买卖代币、查询钱包余额、转移SOL代币、设置做市策略、创建钱包、获取价格报价、领取创作者费用时；  
  - 也适用于代币捆绑发行（bundle launches）、Jito捆绑包（Jito bundles）的管理、绑定曲线查询（bonding curve queries）以及批量代币发行（spam launches）等场景。  
  **注意事项：**  
  - 该工具专用于`pump.fun`平台的相关操作，不适用于一般的Solana RPC（Remote Procedure Call）查询、非`pump.fun`平台的DeFi服务（如Raydium、Jupiter、Orca）、NFT操作，也不支持导入外部私钥。
version: "2.0.0"
author: openpump
license: MIT
homepage: https://openpump.io
user-invocable: true

metadata:
  openclaw:
    emoji: "\U0001F680"
    requires:
      bins: ["node", "npx"]
      env: ["OPENPUMP_API_KEY"]
    primaryEnv: "OPENPUMP_API_KEY"
    install:
      - id: openpump-mcp
        kind: node
        package: "@openpump/mcp"
        bins: ["openpump-mcp"]
        label: "Install OpenPump MCP Server (npm)"
    os: ["linux", "darwin", "win32"]
    network: ["api.openpump.io", "mcp.openpump.io"]
    homepage: "https://openpump.io"

tags:
  - solana
  - crypto
  - trading
  - pump-fun
  - defi
  - mcp
  - token-launch
  - memecoin
  - jito
  - bonding-curve
  - market-making
  - sniper
  - stop-loss
---
# OpenPump MCP 服务器

通过 MCP 可以交易 pump.fun 代币、管理 Solana 钱包、运行做市机器人、抢购新代币以及监控持仓情况。

## 设置

### 1. 获取 API 密钥

1. 在 [openpump.io](https://openpump.io) 注册账号。
2. 进入仪表板 > API 密钥。
3. 创建一个新的密钥（以 `op_sk_live_` 开头）。

### 2. 设置环境变量

```bash
export OPENPUMP_API_KEY="op_sk_live_YOUR_KEY_HERE"
```

### 3. 添加 MCP 服务器

**Claude 代码（HTTP 传输方式——无需本地进程）：**

```bash
claude mcp add --transport http openpump https://openpump.io/api/mcp \
  --header "Authorization: Bearer op_sk_live_YOUR_KEY_HERE"
```

**Claude 桌面版 / 任何 MCP 客户端（通过 npx 使用标准输出）：**

```json
{
  "mcpServers": {
    "openpump": {
      "command": "npx",
      "args": ["-y", "@openpump/mcp@latest"],
      "env": {
        "OPENPUMP_API_KEY": "op_sk_live_YOUR_KEY_HERE"
      }
    }
  }
}
```

**HTTP 传输方式（远程传输，无需本地进程）：**

```json
{
  "mcpServers": {
    "openpump": {
      "url": "https://mcp.openpump.io/mcp",
      "headers": {
        "Authorization": "Bearer ${OPENPUMP_API_KEY}"
      }
    }
  }
}
```

## 可用工具（共 57 个）

### 代币创建（2 个工具）

| 工具 | 描述 |
|------|-------------|
| `create-token` | 在 pump.fun 平台上创建新的代币，可设置名称、符号、描述和图片。 |
| `bundle-launch` | 通过 Jito 包同时创建代币并协调多个钱包的购买操作。 |

### 交易（7 个工具）

| 工具 | 描述 |
|------|-------------|
| `buy-token` | 用 SOL 购买 pump.fun 代币。`amountSol` 为小数形式的 SOL 字符串（例如 `"0.1"`）。 |
| `sell-token` | 将代币卖出并换回 SOL。使用 `tokenAmount: "all"` 可卖出全部余额。 |
| `bundle-buy` | 通过 Jito 包批量购买现有代币。 |
| `bundle-sell` | 将代币批量卖出并打包成 Jito 包（仅适用于基于 bonding curve 的代币）。 |
| `get-token-quote` | 获取买卖报价，不执行交易。`solAmount` 以 lamports 字符串形式输入。 |
| `estimate-bundle-cost` | 在执行前预览创建代币包所需的总 SOL 金额。 |
| `claim-creator-fees` | 提取特定钱包地址的累积 pump.fun 创建者费用。 |

### 转账（2 个工具）

| 工具 | 描述 |
|------|-------------|
| `transfer-sol` | 将 SOL 转账到任意 Solana 地址。`amountSol` 为小数形式的 SOL 字符串。每次转账上限为 10 SOL。支持 `dryRun` 模式。 |
| `transfer-token` | 将 SPL 代币转账到任意 Solana 地址。`tokenAmount` 可以使用原始单位或 `"all"` 表示全部代币。 |

### 钱包管理（5 个工具）

| 工具 | 描述 |
|------|-------------|
| `create-wallet` | 创建一个新的 HD 衍生托管钱包，可选设置标签。 |
| `batch-create-wallets` | 一次性创建 2-50 个钱包，并自动分配标签。 |
| `get-aggregate-balance` | 统计所有钱包的 SOL 总余额。 |
| `get-wallet-deposit-address` | 获取钱包的存款地址和资金转账说明。 |
| `get-wallet-transactions` | 分页显示钱包的转账历史记录（买入/卖出/转账）。 |

### 做市（13 个工具）

| 工具 | 描述 |
|------|-------------|
| `mm-create-pool` | 创建一个钱包池，包含 N 个钱包（2-50 个）。 |
| `mm-list-pools` | 列出用户所有的钱包池。 |
| `mm-pool-status` | 显示每个钱包的 SOL 和代币余额及总数。 |
| `mm-fund-pool` | 将资金从源钱包分配到所有池中的钱包。支持多跳转账（最多 3 跳）。 |
| `mm-consolidate-pool` | 将所有池中的资金回收到目标钱包。 |
| `mm-start-session` | 启动具有可配置策略的自动做市会话。 |
| `mm-stop-session` | 停止正在运行的会话。持仓不会自动清算。 |
| `mm-pause-session` | 暂停会话（保留当前持仓和设置）。 |
| `mm-resume-session` | 从暂停状态恢复会话。 |
| `mm-session-status` | 显示会话详细信息：配置、实时数据、最近的交易记录。 |
| `mm-list-sessions` | 列出所有会话，可按状态筛选。 |
| `mm-update-strategy` | 在运行中或暂停的会话中动态更新策略参数。 |
| `mm-get-pnl` | 提供盈亏报告：基于 WAC 成本的计算方式，包括已实现/未实现的盈亏、滑点调整后的卖出结果以及 ROI%。 |

### 抢购（7 个工具）

| 工具 | 描述 |
|------|-------------|
| `snipe-start` | 创建一个监控器，自动购买符合特定条件的新代币（如价格模式、市值、风险筛选）。 |
| `snipe-stop` | 永久停止抢购监控器。 |
| `snipe-pause` | 暂停抢购监控器（稍后可恢复）。 |
| `snipe-resume` | 恢复暂停的抢购监控器。 |
| `snipe-update` | 更新正在运行或暂停的监控器的购买条件。 |
| `snipe-status` | 显示详细状态，包括购买数量和当前状态。 |
| `snipe-list` | 列出所有抢购监控器，可按状态筛选。 |

### 止损（4 个工具）

| 工具 | 描述 |
|------|-------------|
| `stop-loss-set` | 创建止损监控器。当市值低于设定值时自动卖出。 |
| `stop-loss-remove` | 删除止损监控器。 |
| `stop-loss-list` | 列出所有止损监控器。 |
| `stop-loss-status` | 显示特定止损监控器的详细状态。 |

### 虚拟地址（4 个工具）

| 工具 | 描述 |
|------|-------------|
| `estimate-vanity-cost` | 在下单前估算虚拟地址的信用价值。 |
| `order-vanity-address` | 下单创建虚拟地址或挖矿地址（可指定前缀、后缀或包含的字符）。 |
| `list-vanity-jobs` | 列出所有虚拟地址的挖矿任务（最新任务优先显示）。 |
| `get-vanity-job` | 检查特定虚拟地址任务的进度。任务完成后钱包会自动添加。 |

### 垃圾邮件式发行（3 个工具）

| 工具 | 描述 |
|------|-------------|
| `spam-launch` | 从一个钱包快速连续发行多个代币（1-100 个）。 |
| `estimate-spam-cost` | 估算垃圾邮件式发行操作的总 SOL 和信用价值。 |
| `cancel-spam-launch` | 取消正在进行的垃圾邮件式发行任务。 |

### 信息查询（9 个工具）

| 工具 | 描述 |
|------|-------------|
| `get-token-info` | 查看代币的 bonding curve 状态（价格、市值、毕业状态）。 |
| `get-token-market-info` | 提供丰富的分析数据：交易量、买卖数量、风险指标（包括抢购者和打包者）。 |
| `list-my-tokens` | 显示用户发行的所有代币。 |
| `get-token-holdings` | 查看持有特定代币的钱包。可选择不显示铸造信息以查看所有持仓。 |
| `get-wallet-balance` | 显示单个钱包的 SOL 和代币余额。 |
| `list-wallets` | 列出所有钱包的信息（包括公钥、标签和派生索引）。 |
| `get-creator-fees` | 查看累积的 pump.fun 创建者费用。可选择不显示具体地址以查看所有钱包的费用。 |
| `get-jito-tip-levels` | 获取当前 Jito MEV 提示金额（每 20 秒更新一次）。 |

### 任务管理（2 个工具）

| 工具 | 描述 |
|------|-------------|
| `poll-job` | 检查异步操作的状态。每 2 秒查询一次，直到任务完成或失败。 |
| `cancel-job` | 取消正在运行的异步任务。 |

## 工作流程

### 1. 发行代币

```
1. create-wallet (label: "launch-wallet")
2. Fund the wallet with SOL (use get-wallet-deposit-address for the address)
3. create-token (name, symbol, description, imageUrl)
4. poll-job (wait for "completed")
5. get-token-info (verify token is live)
```

### 2. 创建代币包并批量购买

```
1. create-wallet (dev wallet)
2. batch-create-wallets (count: 5, labelPrefix: "buyer")
3. Fund all wallets with SOL
4. estimate-bundle-cost (buyWalletCount: 5, devBuyAmountSol: "0.1", walletBuyAmounts)
5. bundle-launch (devWalletId, buyWalletIds, tokenParams, amounts, confirm: true)
6. poll-job (wait for "completed")
7. get-token-holdings (mint) -- verify all wallets hold the token
```

### 3. 买入和卖出流程

```
1. list-wallets (find walletId with SOL balance)
2. get-token-quote (action: "buy", solAmount: "100000000") -- 0.1 SOL in lamports
3. buy-token (mint, walletId, amountSol: "0.1") -- decimal SOL string
4. get-token-holdings (mint) -- verify purchase
5. get-token-quote (action: "sell", tokenAmount from holdings)
6. sell-token (mint, walletId, tokenAmount or "all")
```

### 4. 做市

```
1. mm-create-pool (label: "mm-pool", walletCount: 10)
2. mm-fund-pool (poolId, sourceWalletId, totalAmountSol: 2.5, hops: 2)
3. mm-pool-status (poolId) -- verify funding
4. mm-start-session (mint, walletPoolId, config: {
     amountRange: ["5000000", "50000000"],  -- 0.005 to 0.05 SOL in lamports
     maxPositionSol: "1000000000",           -- 1 SOL max
     netBias: 0.5,                           -- balanced buys/sells
     intervalRange: [10, 45],                -- 10-45s between trades
     confirm: true
   })
5. mm-session-status (sessionId) -- monitor
6. mm-get-pnl (sessionId) -- check profitability
7. mm-stop-session (sessionId) -- when done
8. mm-consolidate-pool (poolId, targetWalletId) -- recover funds
```

### 5. 抢购新代币

```
1. list-wallets -- pick a funded wallet
2. snipe-start (walletId, tickerPattern: "PEPE*", buyAmountSol: 0.05, {
     maxDevPercent: 10,       -- filter rugs
     maxSniperCount: 5,       -- avoid crowded launches
     maxBuys: 3,              -- stop after 3 buys
     confirm: true
   })
3. snipe-status (monitorId) -- check matches
4. snipe-update (monitorId, ...) -- adjust criteria live
5. snipe-stop (monitorId) -- when done
```

### 6. 设置止损保护

```
1. get-token-holdings (mint) -- confirm position
2. get-token-market-info (mint) -- check current market cap
3. stop-loss-set (walletId, mint, triggerMarketCapSol: 5.0, confirm: true)
4. stop-loss-status (stopLossId) -- verify active
5. stop-loss-remove (stopLossId) -- cancel if no longer needed
```

### 7. 检查投资组合

```
1. list-wallets -- see all wallets
2. get-aggregate-balance -- total SOL across wallets
3. get-token-holdings -- all token positions (omit mint for everything)
4. get-token-market-info (per mint) -- current prices and risk metrics
```

### 8. 提取创建者费用

```
1. get-creator-fees -- check all wallets for accumulated fees
2. claim-creator-fees (creatorAddress)
3. get-wallet-balance (walletId) -- verify SOL increased
```

### 9. 转出 SOL

```
1. get-wallet-balance (walletId) -- check available SOL
2. transfer-sol (walletId, toAddress, amountSol: "1.0", dryRun: true) -- preview
3. transfer-sol (walletId, toAddress, amountSol: "1.0", confirm: true) -- execute
```

### 10. 虚拟地址

```
1. estimate-vanity-cost (pattern: "PUMP", patternType: "prefix")
2. order-vanity-address (pattern: "PUMP", patternType: "prefix")
3. get-vanity-job (jobId) -- poll until "completed"
4. list-wallets -- new vanity wallet appears automatically
```

## 安全保障措施

**所有交易操作在执行前都需要用户的明确确认。**

1. **始终先查看余额。** 在进行任何交易或转账前，运行 `get-wallet-balance` 或 `get-aggregate-balance` 命令。 |
2. **交易前获取报价。** 调用 `get-token-quote` 命令预览预期结果和价格影响。 |
3. **对大额交易进行明确确认。** 包装操作、做市会话和抢购监控器都需要设置 `confirm: true`。交易前请仔细核对参数。 |
4. **验证转账地址。** 仔细核对收款地址。在 Solana 上转账是不可逆的操作。 |
5. **使用 `dryRun` 模式进行转账。`transfer-sol` 和 `transfer-token` 都支持 `dryRun: true`。 |
6. **检查风险指标。** 在购买前使用 `get-token-market-info` 命令查看抢购数量、打包者活动和内部人士的交易情况。 |
7. **设置止损。** 使用 `stop-loss-set` 命令保护持仓免受价格突然下跌的影响。 |
8. **考虑交易滑点。`bundle-launch` 操作每次交易会涉及多个钱包，建议设置滑点为 2500 bps（25%）。 |
9. **做市会话的止损机制。** 做市会话设有 `maxDrawdownPercent` 限制（默认为 15%）。如果损失超过该限制，会话会自动停止。 |
10. **转账限额。`transfer-sol` 每次转账上限为 10 SOL。建议将大额资金分多次转账。 |
11. **监控异步操作。** 在执行 `create-token`、`bundle-launch` 或 `spam-launch` 操作后，每 2 秒查询一次任务进度。任务会在 10 分钟后自动结束。 |

## 关键概念

- **SOL 金额：** `amountSol` 参数接受小数形式的 SOL 字符串（例如 `"0.1"` 表示 0.1 SOL），不使用 lamports。 |
- **Lamports：** 某些参数（如 `get-token-quote` 的 `solAmount`、`mm-start-session` 的 `amountRange`）使用 lamports 作为整数字符串（1 SOL = 1,000,000,000）。 |
- **代币单位：** 代币金额使用原始单位。请使用 `get-token-holdings` 返回的 `amount` 字符串。 |
- **托管钱包：** 由平台管理的 HD 衍生钱包，无法导入外部密钥。 |
- **Bonding curve：** pump.fun 代币在 bonding curve 上交易，直到达到毕业条件后方可转移到 PumpSwap。`bundle-sell` 仅适用于基于 bonding curve 的代币。 |
- **Jito 包：** 执行操作是原子的，同一区块内完成。第一个包保证原子性；超出数量的代币会被分摊到后续包中。 |
- **钱包池：** 用于做市的钱包组。多跳转账会在链上实现资金分配。 |

## 链接

- 网站：[openpump.io](https://openpump.io)
- npm：[@openpump/mcp](https://www.npmjs.com/package/@openpump/mcp)