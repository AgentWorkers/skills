---
name: gate-dex-wallet
version: "2026.3.12-1"
updated: "2026-03-12"
description: "Gate DEX 是一款功能全面的钱包工具。它提供了一个统一的入口点，支持以下操作：身份验证与登录、资产查询、转账执行、DApp（去中心化应用）交互，以及通过命令行（CLI）进行操作。该工具涵盖了五个主要模块。当用户需要执行登录、查询余额、转账、与DApp交互、签名、使用命令行（CLI）等与钱包相关的操作时，都可以使用 Gate DEX。通过子功能路由机制，可以快速定位到相应的操作参考文件。"
---
# Gate DEX 钱包

> **综合钱包功能** — 提供统一的入口点，支持身份验证、资产管理、转账、DApp交互以及 CLI 命令行操作。通过子功能路由分配，实现了5个主要模块的功能。

**触发场景**：当用户提及“登录”、“查看余额”、“转账”、“DApp”、“签名”、“钱包”、“资产”、“gate-wallet”、“CLI”、“命令行”、“openapi-swap”等与钱包相关的操作时，可使用此功能。

---

## 核心模块

| 模块 | 描述 | 典型场景 |
|------|------|---------|
| 🔐 **身份验证** | Google OAuth 登录、Token 管理 | “登录”、“注销”、“Token 过期” |
| 💰 **资产** | 查看余额、地址查询、交易历史 | “查看余额”、“总资产”、“交易历史” |
| 💸 **转账** | 计算 Gas 费用、构建交易、广播签名 | “转账”、“发送 Token”、“批量转账” |
| 🎯 **DApp** | 连接钱包、签署消息、与合约交互 | “连接 DApp”、“签署消息”、“批准” |
| 🖥️ **CLI** | 支持 Gate-Wallet CLI 双通道（MCP 保管式签名 + OpenAPI 混合模式） | “gate-wallet”、“CLI”、“命令行”、“openapi-swap”、“混合模式交易” |

---

## 路由规则

根据用户意图，将请求路由到相应的子功能参考文件：

| 用户意图 | 关键词 | 参考文件 |
|---------|-----------|---------|
| **身份验证登录** | “登录”、“auth”、“token expired”、“session” | [references/auth.md](./references/auth.md) |
| **资产查询** | “查看余额”、“总资产”、“钱包地址”、“交易历史”、“交易记录” | 保持当前 SKILL.md 的主要流程 |
| **转账操作** | “转账”、“发送”、“批量转账”、“Gas 费用” | [references/transfer.md](./references/transfer.md) |
| **DApp 交互** | “DApp”、“签署消息”、“批准”、“连接钱包”、“调用合约” | [references/dapp.md](./references/dapp.md) |
| **CLI 操作** | “gate-wallet”、“CLI”、“命令行”、“openapi-swap”、“混合模式交易” | [references/cli.md](./references/cli.md) |

---

## MCP 服务器连接检测

### 初始会话检测

在会话中首次调用 MCP 工具之前，执行一次连接探测，以确认 Gate Wallet MCP 服务器是否可用。后续操作无需重复检测。

```text
CallMcpTool(server="gate-wallet", toolName="chain.config", arguments={chain: "eth"})
```

| 结果 | 处理方式 |
|------|------|
| 成功 | MCP 服务器可用，继续执行用户请求的具体操作 |
| 失败 | 根据错误类型显示配置指导（详见错误处理部分） |

### 运行时错误处理

对于后续操作，如果业务工具调用失败（连接错误、超时等），请按照以下规则进行处理：

| 错误类型 | 关键词 | 处理方式 |
|---------|--------|------|
| MCP 服务器未配置 | `server not found`、`unknown server` | 显示 MCP 服务器配置指导 |
| 远程服务无法访问 | `connection refused`、`timeout`、`DNS error` | 建议检查服务器状态和网络连接 |
| 身份验证失败 | `401`、`unauthorized`、`x-api-key` | 建议联系管理员获取 API Key |

---

## 身份验证状态管理

所有需要身份验证的操作（资产查询、转账、DApp 交互）都需要有效的 `mcp_token`：

- 如果当前没有 `mcp_token` → 指导用户参考 [references/auth.md] 完成登录后再继续操作 |
- 如果 `mcp_token` 过期（MCP 服务器返回 token 过期错误） → 首先尝试使用 `auth.refresh_token` 进行静默刷新；如果失败，则引导用户重新登录 |

---

## MCP 工具调用规范（资产查询模块）

### 1. `wallet.get_token_list` — 查询指定链或所有链的 Token 余额

| 参数 | 描述 |
|------|------|
| **工具名称** | `wallet.get_token_list` |
| **参数** | `{ chain?: string, network_keys?: string, account_id?: string, mcp_token: string, page?: number, page_size?: number }` |
| **返回值** | Token 数组，每个元素包含 `symbol`、`balance`、`price`、`value`、`chain`、`contract_address` 等信息 |

调用示例：

```text
CallMcpTool(
  server="gate-wallet",
  toolName="wallet.get_token_list",
  arguments={ chain: "ETH", mcp_token: "<mcp_token>" }
)
```

### 2. `wallet.get_total_asset` — 查询总资产价值

| 参数 | 描述 |
|------|------|
| **工具名称** | `wallet.get_total_asset` |
| **参数** | `{ account_id: string, mcp_token: string }` |
| **返回值** | `{ total_value_usd: number, chains: Array<{chain: string, value_usd: number}> }` |

### 3. `wallet.get_addresses` — 获取钱包地址

| 参数 | 描述 |
|------|------|
| **工具名称** | `wallet.get_addresses` |
| **参数** | `{ account_id: string, mcp_token: string }` |
| **返回值** | 每个链的钱包地址对象 |

### 4. `chain.config` — 链路配置信息

| 参数 | 描述 |
|------|------|
| **工具名称** | `chain.config` |
| **参数** | `{ chain: string, mcp_token: string }` |
| **返回值** | 链路配置信息（RPC、区块浏览器等） |

### 5. `tx.list` — 钱包综合交易列表（包含身份验证、资产、转账、DApp 交易）

| 参数 | 描述 |
|------|------|
| **工具名称** | `tx.list` |
| **参数** | `{ account_id: string, chain?: string, page?: number, limit?: number, mcp_token: string }` |
| **返回值** | 交易历史记录数组 |

### 6. `tx.detail` — 交易详情

| 参数 | 描述 |
|------|------|
| **工具名称** | `tx.detail` |
| **参数** | `{ hash_id: string, chain: string, mcp_token: string }` |
| **返回值** | 详细的交易信息 |

### 7. `tx.history_list` — 交易历史记录

| 参数 | 描述 |
|------|------|
| **工具名称** | `tx.history_list` |
| **参数** | `{ account_id: string, chain?: string, page?: number, limit?: number, mcp_token: string }` |
| **返回值** | 交易历史记录数组 |

---

## 操作流程

### 流程 A：查询 Token 余额

```text
Step 0: MCP Server connection detection
  ↓ Success

Step 1: Authentication check
  Confirm holding valid mcp_token and account_id
  No token → Route to references/auth.md
  ↓

Step 2: Execute query
  Call wallet.get_token_list({ chain?, network_keys?, mcp_token })
  ↓

Step 3: Format display
  Group by chain, sort by value, filter zero balances
```

### 流程 B：查询总资产价值

```text
Step 0-1: Same as Flow A
  ↓

Step 2: Execute query
  Call wallet.get_total_asset({ account_id, mcp_token })
  ↓

Step 3: Format display
  Total value + distribution by chain
```

### 流程 C-G：其他资产查询流程

具体流程与上述类似，详细规范请参考原始 SKILL.md 文档。

---

## 操作流程指导

查看资产信息后的后续操作指南：

| 用户意图 | 目标功能 |
|---------|------|
| 查看 Token 价格、K 线图 | `gate-dex-market` |
| 查看 Token 安全审计报告 | `gate-dex-market` |
| 转账/发送 Token | 参考 [references/transfer.md] |
| 交易/兑换 Token | `gate-dex-trade` |
| 与 DApp 交互 | 参考 [references/dapp.md] |
| 登录/验证失败 | 参考 [references/auth.md] |
| 使用 CLI/命令行操作/混合模式交易 | 参考 [references/cli.md] |

---

## 跨技能协作

此功能作为 **钱包数据中心**，被其他功能调用：

| 调用者 | 场景 | 使用的工具 |
|--------|------|---------|
| `gate-dex-trade` | 交易前余额验证、Token 地址解析 | `wallet.get_token_list` |
| `gate-dex-trade` | 获取特定链路的钱包地址 | `wallet.get_addresses` |
| `gate-dex-market` | 市场数据查询后查看持有情况 | `wallet.get_token_list` |
| CLI 子模块 | CLI 双通道操作（MCP 保管式签名 / OpenAPI 混合模式交易） | `references/cli.md` |

---

## 支持的链路

| 链路 ID | 网络名称 | 类型 |
|--------|----------|------|
| `eth` | Ethereum | EVM |
| `bsc` | BNB 智能链 | EVM |
| `polygon` | Polygon | EVM |
| `arbitrum` | Arbitrum One | EVM |
| `optimism` | Optimism | EVM |
| `avax` | Avalanche C-Chain | EVM |
| `base` | Base | EVM |
| `sol` | Solana | 非 EVM |

---

## 安全规则

1. **身份验证检查**：在所有操作前检查 `mcp_token` 的有效性 |
2. **敏感信息**：`mcp_token` 不得以明文形式在对话中显示 |
3. **自动刷新**：Token 过期时优先进行静默刷新 |
4. **引导机制**：身份验证失败时引导用户参考 [references/auth.md] |
5. **跨技能安全**：为其他功能提供安全的余额验证和地址查询服务 |

---

（注：由于提供的 SKILL.md 文件内容较为冗长，部分代码块（如 ````text
CallMcpTool(server="gate-wallet", toolName="chain.config", arguments={chain: "eth"})
````）在实际翻译中可能不会被直接包含在最终结果中。这些代码块用于表示代码示例或注释，因此在翻译时已省略。）