---
name: send-token
description: 在 Solana 或 Base 网络中转移代币。适用于用户需要发送、转移或支付代币的场景。支持按名称查询并使用原生货币（如 SOL、ETH）及代币（如 USDC），同时也支持通过代币的铸造地址或合约地址来转移任意代币。功能包括：“发送 SOL”、“转移 USDC”、“发送代币”、“向某人付款”、“在 Base 网络上发送 ETH”以及“转移至指定地址”。
user-invocable: true
disable-model-invocation: false
allowed-tools: ["Bash(npx @openant-ai/cli@latest wallet send *)", "Bash(npx @openant-ai/cli@latest wallet balance*)", "Bash(npx @openant-ai/cli@latest wallet addr*)", "Bash(npx @openant-ai/cli@latest status*)"]
---
# 在 OpenAnt 上发送代币

使用 `npx @openant-ai/cli@latest` 命令行工具在 Solana 或 Base 链上转移代币。该工具支持原生货币（SOL、ETH）、命名代币（USDC）以及通过铸造地址或合约地址指定的任意代币。

**请在每个命令后添加 `--json` 选项**，以获得结构化且可解析的输出结果。

## 确认身份验证和余额

```bash
npx @openant-ai/cli@latest status --json
npx @openant-ai/cli@latest wallet balance --json
```

如果未完成身份验证，请参考 `authenticate-openant` 功能。如果余额不足，请通知用户。

## 命令语法

```bash
npx @openant-ai/cli@latest wallet send <chain> <token> <amount> <to> [--json] [--rpc <url>]
```

### 参数

| 参数 | 说明 |
|--------|-------------|
| `chain` | 目标链：`solana`（或 `sol`）、`base`（或 `eth`） |
| `token` | 代币类型：`sol`、`eth`、`usdc`，或铸造地址/合约地址 |
| `amount` | 金额（显示单位，例如：`10` 表示 10 USDC，`0.5` 表示 0.5 SOL） |
| `to` | 目标地址（Solana 公钥或 EVM 地址） |

### 选项

| 选项 | 说明 |
|--------|-------------|
| `--json` | 生成机器可读的 JSON 格式输出 |
| `--rpc <url>` | 替换默认的 RPC 连接地址 |

## 支持的链和代币

| 链 | 命名代币 | 原生货币 |
|-------|-------------|-------------|
| `solana` / `sol` | `usdc` 或任何 SPL 铸造地址 | `sol` |
| `base` / `eth` | `usdc` 或任何 ERC20 合约地址 | `eth` |

对于任意代币，可以直接将铸造地址（Solana）或合约地址作为 `token` 参数传递。

## 示例

### 发送原生 SOL 代币

```bash
npx @openant-ai/cli@latest wallet send solana sol 1.5 7xKabc123... --json
# -> { "success": true, "data": { "chain": "solana", "txSignature": "5xYz..." } }
```

### 在 Solana 上发送 USDC 代币

```bash
npx @openant-ai/cli@latest wallet send solana usdc 100 7xKabc123... --json
# -> { "success": true, "data": { "chain": "solana", "txSignature": "3aBc..." } }
```

### 在 Base 上发送 ETH 代币

```bash
npx @openant-ai/cli@latest wallet send base eth 0.05 0xAbCdEf... --json
# -> { "success": true, "data": { "chain": "base", "txHash": "0x1a2b..." } }
```

### 在 Base 上发送 USDC 代币

```bash
npx @openant-ai/cli@latest wallet send base usdc 50 0xAbCdEf... --json
# -> { "success": true, "data": { "chain": "base", "txHash": "0x9f8e..." } }
```

### 通过铸造地址发送任意 SPL 代币

```bash
npx @openant-ai/cli@latest wallet send solana 4zMMC9srt5Ri5X14GAgXhaHii3GnPAEERYPJgZJDncDU 25 7xKabc123... --json
```

### 通过合约地址发送任意 ERC20 代币

```bash
npx @openant-ai/cli@latest wallet send base 0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913 10 0xAbCdEf... --json
```

## 自然语言映射

当用户输入如下指令时：

- “请将 10 USDC 从 Solana 转移到 Base 的 0xAbc...” → `wallet send base usdc 10 0xAbc... --json`
- “请将 1.5 SOL 从 Solana 转移到 Base 的 7xK...” → `wallet send solana sol 1.5 7xK... --json`
- “将 50 USDC 发送到 Base 的 0xDef...” → `wallet send base usdc 50 0xDef... --json`
- “请将 0.1 ETH 转移到 Base 的 0x123...” → `wallet send base eth 0.1 0x123... --json`
- “请将 10 <铸造地址> 的代币从 Solana 转移到 <接收者>...” → `wallet send solana <铸造地址> 10 <接收者> --json`

系统会自动提取以下信息：链、代币类型（名称或地址）、金额以及目标地址。

## 注意事项

**代币转移是不可逆的。** 在执行转移前，请务必与用户确认以下内容：

1. 与用户一起核实目标链、代币类型、金额和目标地址。
2. 先检查钱包余额，确保有足够的资金。
3. 只有在用户明确确认后才能执行转移操作。

以下命令为只读命令（`status`、`wallet balance`、`wallet addresses`），可以立即执行：

## 禁忌事项

- **绝对不要在用户未明确确认目标地址的情况下执行转移操作** — 区块链上的转移是不可逆的。请务必显示完整的地址并让用户再次确认。
- **绝对不要将 Solana 代币发送到 Base 链上，反之亦然** — 这两种链不兼容。Solana 地址是 base58 格式的字符串（32–44 个字符），而 Base 地址以 `0x` 开头。如果地址格式不符合链的规范，请停止操作并询问用户。
- **不要假设显示的余额已经包含了交易手续费** — Solana 交易需要支付少量 SOL 费用（约 0.000005 SOL）；Base 交易需要 ETH 作为手续费。如果用户要转移全部余额，请预留一部分资金，否则交易可能会失败。
- **不要仅根据代币类型来推断链的类型** — USDC 在 Solana 和 Base 链上都存在。在发送前请务必确认用户的目标链。
- **不要直接根据用户输入的地址执行转移操作** — 如果用户是在句子中间输入地址或使用了缩写形式，请让他们重新输入完整的地址以进行确认。

## 先决条件

- 必须完成身份验证（`npx @openant-ai/cli@latest status --json`）。
- 钱包中必须有足够的余额用于支付转移费用及手续费。
- 对于 SPL 代币的转移，发送者必须持有相应的代币。

## 错误处理

- “未找到所需的凭据” — 请先运行 `authenticate-openant` 功能。
- “余额不足” / “尝试扣款失败” — 钱包余额不足，请检查钱包余额。
- “未知的链” — 支持的链包括 `sol`、`base`、`eth`。
- “未找到 Base 钱包” / “未找到 Solana 钱包” — 请重新登录以配置钱包。
- “无法解析铸造地址” — 提供的铸造地址无效或不存在。
- 交易模拟失败 — 请检查余额和接收地址的合法性。