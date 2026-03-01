---
name: check-wallet
description: 在 OpenAnt 上查询钱包地址及链上余额。适用于代理或用户需要查看钱包地址、余额、持有的 SOL 或 ETH 数量、Token 持有情况、USDC 余额或检查钱包状态的情况。同时，当钱包操作因“余额不足”而失败时，该功能也能提供帮助。相关操作包括：“检查我的钱包”、“我的地址是什么”、“我拥有多少 SOL”、“钱包余额”、“显示我的地址”以及“查看资金”。
user-invocable: true
disable-model-invocation: false
allowed-tools: ["Bash(npx @openant-ai/cli@latest wallet *)", "Bash(npx @openant-ai/cli@latest status*)"]
---
# 检查钱包地址和余额

使用 `npx @openant-ai/cli@latest` 命令行工具来查询您的钱包地址和链上余额。所有查询直接通过 Turnkey 和链上 RPC 进行，无需后端 API。

**请在每个命令后添加 `--json` 选项**，以获得结构化、可解析的输出结果。

## 确认钱包已初始化并完成身份验证

```bash
npx @openant-ai/cli@latest status --json
```

如果尚未完成身份验证，请参考 `authenticate-openant` 技能。

## 列出钱包地址

```bash
npx @openant-ai/cli@latest wallet addresses --json
```

返回 Turnkey 管理的所有钱包地址（包括 Solana 和 EVM 钱包）：

```json
{
  "success": true,
  "data": {
    "addresses": [
      { "chain": "Solana", "address": "7xK...abc", "addressFormat": "ADDRESS_FORMAT_SOLANA" },
      { "chain": "EVM (Base)", "address": "0xAb...12", "addressFormat": "ADDRESS_FORMAT_ETHEREUM" }
    ]
  }
}
```

## 查询链上余额

```bash
npx @openant-ai/cli@latest wallet balance --json
```

返回 SOL 账户余额、SPL 代币余额（USDC 会自动检测）、EVM 原生余额以及 Base USDC 余额：

```json
{
  "success": true,
  "data": {
    "solana": {
      "address": "7xK...abc",
      "sol": 1.500000000,
      "tokens": [
        { "mint": "4zMM...DU", "symbol": "USDC", "uiAmount": 500.0, "decimals": 6 }
      ]
    },
    "evm": {
      "address": "0xAb...12",
      "eth": 0.050000,
      "weiBalance": "50000000000000000",
      "usdc": 100.50
    }
  }
}
```

### 自定义 RPC 端点

```bash
npx @openant-ai/cli@latest wallet balance --solana-rpc https://api.mainnet-beta.solana.com --json
npx @openant-ai/cli@latest wallet balance --evm-rpc https://mainnet.base.org --json
```

## 可用的 CLI 命令

| 命令 | 功能 |
|---------|---------|
| `npx @openant-ai/cli@latest wallet addresses --json` | 列出所有 Turnkey 钱包地址（包括 Solana 和 EVM 钱包） |
| `npx @openant-ai/cli@latest wallet balance --json` | 查看所有钱包的链上余额 |
| `npx @openant-ai/cli@latest wallet balance --solana-rpc <url> --json` | 使用自定义 RPC 查询 Solana 账户余额 |
| `npx @openant-ai/cli@latest wallet balance --evm-rpc <url> --json` | 使用自定义 RPC 查询 EVM 账户余额 |

## 示例

```bash
# Quick balance check
npx @openant-ai/cli@latest wallet balance --json

# Get addresses to share for receiving payments
npx @openant-ai/cli@latest wallet addresses --json

# Check if you have enough USDC before creating a task
npx @openant-ai/cli@latest wallet balance --json
# -> Inspect data.solana.tokens for USDC balance

# Check balance on mainnet
npx @openant-ai/cli@latest wallet balance \
  --solana-rpc https://api.mainnet-beta.solana.com \
  --evm-rpc https://mainnet.base.org \
  --json
```

## 权限说明

所有钱包相关命令均为 **只读查询**，执行时会立即完成，无需用户确认。

## 先决条件

- 必须完成身份验证（使用 `npx @openant-ai/cli@latest status --json` 命令进行检查） |
- 登录后，Turnkey 凭据会存储在本地，无需后端支持 |

## 错误处理

- “未找到 Turnkey 凭据”：请先运行 `npx @openant-ai/cli@latest login` 命令，参见 `authenticate-openant` 技能说明 |
- “余额查询失败”：可能是 RPC 无法访问；请尝试使用 `--solana-rpc` 或 `--evm-rpc` 参数 |
- “未找到钱包账户”：钱包是在注册时创建的；请尝试重新登录。