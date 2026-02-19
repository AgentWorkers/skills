---
name: renzo
description: 查询 Renzo 加密货币的流动性重置协议：DeFi 金库的收益、TVL（总价值锁定）、ezETH 的交易汇率、EigenLayer 运营商、支持的区块链网络、用户代币余额以及提款状态。
homepage: https://github.com/Renzo-Protocol/openclaw-skill
metadata:
  clawdbot:
    emoji: "\U0001F7E2"
    requires:
      bins: ["curl", "jq"]
    files: ["renzo-mcp.sh"]
---
# Renzo 协议

该技能可用于查询 Renzo 液态重置（liquid restaking）协议的相关数据，包括 ezETH 指标、保险库信息、协议统计信息、支持的区块链网络以及运营商详情。

## 使用场景

当用户询问以下内容时，可激活此技能：
- Renzo 协议、ezETH、pzETH、ezSOL 或任何 Renzo 保险库代币的相关信息
- Renzo 上的液态重置收益、年化收益率（APR）或质押回报
- Renzo 的总锁定价值（TVL）或协议统计数据
- Renzo 保险库的详细信息、性能或对比
- Renzo 支持的区块链网络
- 通过 Renzo 委托的 EigenLayer 运营商
- Renzo 上的机构保险库管理
- 用户的 Renzo 代币余额或投资组合（提供以太坊地址）
- ezETH 提现请求、解质押状态或冷却时间
- 保险库策略、AVS（Asset Allocation Strategy）分配情况以及保险库资本的投资方向
- 保留保险库（如 ezCompETH1、ezUSCC1）的 LTV（贷款价值）比率、杠杆率或风险参数

## 可用工具

辅助脚本 `renzo-mcp.sh`（位于该技能的目录中）会调用 Renzo MCP 服务器，并返回格式化的 JSON 数据。

| 工具 | 功能 | 参数 |
|------|---------|-----------|
| `get_ezeth_info` | 获取 ezETH 指标：年化收益率（APR）、供应量、TVL、价格、汇率 | 无 |
| `get_protocol_stats` | 获取协议统计信息：总 TVL、APR、支持的区块链网络数量 | 无 |
| `get_supported_chains` | 列出 Renzo 支持的区块链网络 | 无 |
| `get_vaults` | 列出带有 TVL 和 APR 的保险库 | 可选参数：`{"ecosystem":"eigenlayer"}`（eigenlayer、symbiotic、jito、generic） |
| `get_vault_details` | 获取单个保险库的详细信息（包括保留保险库的实时 LTV） | 必需参数：`{"vaultId":"<符号或地址>"}` |
| `get_vault_strategy` | 获取 EigenLayer 保险库的 AVS 分配情况、质押百分比及运营商信息 | 必需参数：`{"vaultId":"<符号>"}`（ezETH、ezEIGEN、ezREZ） |
| `get_operators` | 获取协议运营商列表 | 可选参数：`{"product":"ezETH"}`（ezETH、pzETH、ezSOL 等） |
| `get_token_balances` | 获取用户的 Renzo 代币余额（ezETH、pzETH、保险库 LP）及对应的 ETH/USD 价值 | 必需参数：`{"address":"0x..."}`（以太坊地址） |
| `get_withdrawal_requests` | 获取用户的待处理 ezETH 提现请求，包括可领取状态及剩余时间 | 必需参数：`{"address":"0x..."}`（以太坊地址） |

## 使用方法

通过 Bash 工具运行辅助脚本。脚本路径相对于该技能的目录。

### 数据展示规则

- **年化收益率/年化收益（APR/APY）**：以百分比形式显示，保留两位小数（例如：“2.84%”）
- **TVL**：以美元为单位，保留两位小数并使用逗号分隔（例如：“$430,813,580.01”）。对于超过 100 万美元的数值，可使用简写形式（例如：“$430.8M”）
- **汇率**：保留 4-6 位小数（例如：“1.0721 ETH 每 ezETH”）
- **代币数量**：保留 2-4 位小数，并显示代币符号
- **表格**：在比较保险库或列出多个项目时使用 Markdown 表格
- **说明**：对于不熟悉液态重置机制的用户，需简要解释各项数据的含义

### 示例：ezETH 信息响应

`get_ezeth_info` 工具的返回结果如下：
```json
{
  "token": "ezETH",
  "aprPercent": 2.83,
  "aprAvgPeriodDays": 30,
  "totalSupplyEth": 215986.82,
  "lpTotalSupply": 201461.43,
  "tvlUsd": 430813580.00,
  "ethPriceUsd": 2138.44,
  "exchangeRate": 1.0721
}
```

展示方式：
> **ezETH** 当前获得的年化收益为 **2.83%**（30 天平均值）。汇率为 **1.0721 ETH 每 ezETH**，总 TVL 为 **$430.8M**，总供应量为 **215,987 ETH**。

### 保险库对比示例

在列出保险库时，可以使用表格格式：
| 保险库 | 基础资产 | 年化收益率（APR） | TVL | 生态系统 |
|-------|-----------|-----|-----|-----------|
| ezSOL | SOL | 6.41% | $6.4M | Jito |
| ezEIGEN | EIGEN | 18.23% | $329.6K | EigenLayer |
| ezREZ | REZ | 1.64% | $2.5M | EigenLayer |

### 协议概述示例

对于一般性的关于 Renzo 的查询，可以同时调用 `get_protocol_stats` 和 `get_ezeth_info`，然后进行总结：
> Renzo 是一个液态重置协议，总 TVL 为 **$469.5M**，支持 **8 个区块链网络**。旗舰产品 ezETH 的年化收益为 **2.84%**，而 pzETH 的年化收益为 **2.34%**。该协议支持 EVM 系统（Ethereum、Arbitrum、Base、Linea、BNB Chain、Mode、Blast）和 Solana。

### 保留保险库的实时 LTV 示例

`get_vault_details` 工具现在会为保留保险库（如 ezCompETH1、ezUSCC1）返回实时 LTV 数据：
```json
{
  "symbol": "ezCompETH1",
  "tvlUsd": 965393.86,
  "aprPercent": 3.78,
  "strategy": {
    "protocols": ["Renzo", "Compound V3"],
    "description": "Automates leveraged looping on Compound Finance to amplify ezETH staking and restaking rewards.",
    "parameters": [
      { "label": "Current LTV", "value": "80.00%" },
      { "label": "Target LTV", "value": "80%" },
      { "label": "Maximum LTV", "value": "89.90%" }
    ]
  }
}
```

展示方式：
> **ezCompETH1** 通过 Compound V3 的杠杆机制获得 **3.78%** 的年化收益，TVL 为 **$965.4K**。
>
> | 参数 | 值 |
|-------|-------|
| | 当前 LTV | 80.00% |
| | 目标 LTV | 80% |
| | 最大 LTV（清算） | 89.90% |
>
> 该保险库的 LTV 已达到目标值，并有 9.9% 的缓冲空间。

对于 ezUSCC1（Aave Horizon），会返回类似的策略数据，包括有效 LTV、持仓 LTV、市场目标 LTV 和最大资产利用率等字段。

### 保险库策略示例（AVS 分配）

`get_vault_strategy` 工具会显示 EigenLayer 保险库的资本分配情况：
```json
{
  "vault": { "symbol": "ezETH", "ecosystem": "eigenlayer" },
  "underlyingTvl": 212785.80,
  "allocations": [
    {
      "avs": "EigenDA",
      "description": "EigenDA is a data availability store...",
      "stakedAmount": 128772.95,
      "percentOfTvl": 60.52,
      "operators": ["0xdfcb...", "0x5cd6...", "0x5dcd..."]
    },
    {
      "avs": "Aligned",
      "stakedAmount": 181405.06,
      "percentOfTvl": 85.25,
      "operators": ["0xdfcb...", "0x3f98...", "0x5cd6...", "0x5dcd..."]
    }
  ],
  "operators": [
    { "id": "luganodes", "name": "Luganodes", "link": "https://www.luganodes.com/" },
    { "id": "figment", "name": "Figment", "link": "https://figment.io/" }
  ]
}
```

展示方式：
> **ezETH 策略** — 该 EigenLayer 保险库在 16 个 AVS（Asset Allocation Service）中质押了 **212,786 ETH**。
>
> 主要的 AVS 分配情况：
>
| AVS | 抵押金额（ETH） | 占 TVL 的百分比 |
|-----|-------------|----------|
| Aligned | 181,405 | 85.25% |
| EigenDA | 128,773 | 60.52% |
| AltLayer | 74,516 | 35.02% |
| Witness Chain | 54,591 | 25.66% |
>
> 运营商包括：Figment、Luganodes、Pier Two、HashKey Cloud
>
> 注意：由于资金同时分配到多个 AVS 中，百分比之和可能超过 100%。

### 代币余额示例

`get_token_balances` 工具的返回结果如下：
```json
{
  "address": "0xABC...123",
  "network": "Ethereum Mainnet",
  "tokens": [
    {
      "symbol": "ezETH",
      "balance": "12.5432",
      "balanceEth": "13.4476",
      "balanceUsd": 28751.23
    },
    {
      "symbol": "pzETH",
      "balance": "5.0000",
      "balanceEth": "5.2100",
      "balanceUsd": 11134.02
    }
  ],
  "totalValueUsd": 39885.25
}
```

展示方式：
> **0xABC...123** 在以太坊主网上的 Renzo 投资组合：
>
| 代币 | 余额 | ETH 价值 | USD 价值 |
|-------|---------|-------------|-------------|
| ezETH | 12.5432 | 13.4476 | $28,751.23 |
| pzETH | 5.0000 | 5.2100 | $11,134.02 |
>
> **总价值：$39,885.25**

如果 `tokens` 为空，需告知用户该地址在以太坊主网上没有 Renzo 代币。

### 提现请求示例

`get_withdrawal_requests` 工具的返回结果如下：
```json
{
  "address": "0xABC...123",
  "requests": [
    {
      "withdrawRequestId": 42,
      "ezEthAmount": "2.5000",
      "ethAmount": "2.6803",
      "claimable": false,
      "createdAt": "2025-02-10T14:30:00Z",
      "claimableAt": "2025-02-17T14:30:00Z",
      "timeRemainingSeconds": 172800
    }
  ],
  "totalRequests": 1,
  "cooldownPeriodSeconds": 604800
}
```

展示方式：
> **0xABC...123** 的待处理提款请求：
>
| 提款编号 | ezETH 数量 | 预计收到的 ETH 数量 | 状态 | 可领取时间 |
|---|-------|---------------|--------|-------------|
| 42 | 2.5000 | 2.6803 | 待处理（剩余 2 天） | 2025 年 2 月 17 日 |
>
> 提款请求的冷却期为 **7 天**。一旦满足条件，用户可以从 WithdrawQueue 合同中领取 ETH。

如果 `requests` 为空，需告知用户该地址没有待处理的 ezETH 提款请求。

## 选择合适的工具

| 用户询问的内容 | 应使用的工具 |
|-------------------|------|
| ezETH 的价格、汇率、收益、APR、TVL | `get_ezeth_info` |
| Renzo 的总体统计信息、总 TVL | `get_protocol_stats` |
| Renzo 支持的区块链网络 | `get_supported_chains` |
| 可用的保险库、保险库收益、保险库对比 | `get_vaults` |
| 特定保险库的详细信息（按名称或符号） | `get_vault_details`（提供保险库符号） |
| EigenLayer 运营商、验证者、委托信息 | `get_operators` |
| AVS 分配情况、资本投资方向、重置策略 | `get_vault_strategy`（提供保险库符号） |
| 保险库的 LTV、杠杆率、风险参数（保留保险库） | `get_vault_details`（提供保险库符号） |
| Renzo 的总体概述 | `get_protocol_stats` + `get_ezeth_info` |
| “我能获得多少收益？” | `get_vaults`（显示所有保险库的 APR） |
| “我的 Renzo 余额是多少？”（提供地址） | `get_token_balances`（提供地址） |
| “检查我的提款状态”（提供地址） | `get_withdrawal_requests`（提供地址） |
| 完整的投资组合概览（提供地址） | `get_token_balances` + `get_withdrawal_requests` |

当用户按名称查询特定保险库时，首先调用 `get_vaults` 获取保险库的符号，然后使用该符号调用 `get_vault_details`。

当用户提供以太坊地址（0x...，共 42 个十六进制字符）时，可以直接使用 `get_token_balances` 或 `get_withdrawal_requests`。如果用户询问“我的持仓”或“我的余额”但未提供地址，请先询问用户的以太坊地址。

## 外部接口

| 接口 | 方法 | 发送的数据 | 用途 |
|----------|--------|-----------|---------|
| `https://mcp.renzoprotocol.com/mcp` | POST | JSON-RPC 请求的名称和参数（例如：保险库 ID、生态系统过滤器、以太坊地址） | 所有 Renzo MCP 查询 |

该辅助脚本仅调用上述列出的 Renzo MCP 服务器。

## 安全性与隐私

- **无需凭证**：Renzo MCP 接口是公开的，无需 API 密钥或认证令牌。
- **不访问本地文件**：脚本不会读取或写入用户的任何文件。
- **无持久化数据**：每次调用之间不会保留任何数据。
- **输入验证**：工具名称会与预定义的白名单进行比对；JSON 参数在发送前会使用 `jq` 进行验证。用户提供的值通过 `jq --argjson` 安全传递（不会将用户输入插入 URL 或命令中）。
- **数据传输**：在查询用户特定工具（`get_token_balances`、`get_withdrawal_requests`）时，会将用户提供的以太坊地址发送到 Renzo MCP 服务器；不会传输其他个人数据。
- **接收的数据**：所有返回的数据均为只读的协议信息（代币余额、APR、TVL 数值），不会返回或处理可执行内容。

## 信任声明

使用此技能时，查询请求会发送到 `https://mcp.renzoprotocol.com/mcp` 的 Renzo 协议 MCP 服务器。对于用户特定的查询，系统会共享用户的以太坊地址。仅在你信任 Renzo 协议并同意共享这些信息的情况下，才应安装此技能。源代码可在 [https://github.com/Renzo-Protocol/openclaw-skill](https://github.com/Renzo-Protocol/openclaw-skill) 获取。

## 错误处理

如果脚本执行失败：
- **网络故障**：告知用户 Renzo MCP 服务器无法访问，建议稍后再试。
- **未知工具**：这可能是技能中的错误，请报告尝试使用的工具名称。
- **无效的 JSON 参数**：检查参数格式是否与工具要求一致。
- **服务器错误**：显示服务器返回的错误信息。

切勿向用户显示原始的 JSON 错误信息，而是用简洁的语言说明问题。