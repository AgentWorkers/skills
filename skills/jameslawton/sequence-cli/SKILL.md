---
name: sequence-builder
description: "使用 Sequence Builder CLI 管理 Sequence 智能钱包、项目、API 密钥、ERC20 转移以及查询区块链数据。当用户需要创建钱包、发送代币、查看余额、管理 Sequence 项目或与 EVM 区块链交互时，可以使用该工具。"
homepage: https://github.com/0xsequence/builder-cli
metadata:
  clawdbot:
    emoji: "⛓️"
    os:
      - darwin
      - linux
    requires:
      bins:
        - node
        - npx
---

# Sequence Builder CLI

Sequence Builder 的命令行界面（CLI）专为 AI 代理和自动化任务设计。用户可以通过命令行创建钱包、进行身份验证、管理项目、查询区块链数据以及发送 ERC20 代币转账。

所有命令都支持使用 `--json` 选项来生成机器可读的输出格式。在程序化解析结果时，请务必使用 `--json`。

## 前提条件

- Node.js 18 及更高版本
- 已注册 Sequence Builder 账户（首次登录时会自动创建）

## 快速入门

```bash
# 1. Create a wallet
npx @0xsequence/builder-cli create-wallet --json

# 2. Login with the private key from step 1
npx @0xsequence/builder-cli login -k <private-key> --json

# 3. Create a project and get an access key
npx @0xsequence/builder-cli projects create "My Project" --json

# 4. Get wallet addresses (EOA + Sequence smart wallet)
npx @0xsequence/builder-cli wallet-info -k <private-key> -a <access-key> --json

# 5. Fund the Sequence wallet via the Trails link from step 4

# 6. Send an ERC20 transfer
npx @0xsequence/builder-cli transfer \
  -k <private-key> -a <access-key> \
  -t <token-address> -r <recipient> \
  -m <amount> -c <chain-id> --json
```

## 加密密钥存储

将 `SEQUENCE_PASSPHRASE` 设置为自动加密并本地存储私钥。一旦私钥被存储，后续的所有命令中就无需再指定 `-k` 参数。

```bash
export SEQUENCE_PASSPHRASE="your-strong-secret"
npx @0xsequence/builder-cli create-wallet --json
# Private key is now encrypted in ~/.sequence-builder/config.json
# All subsequent commands will use the stored key automatically
```

## 了解钱包地址

该 CLI 使用 **Sequence 智能钱包** 来执行转账操作：

- **EOA（Externally Owned Account）地址**：由私钥生成的标准以太坊地址，用于登录和项目所有权管理。
- **Sequence 钱包地址**：一种智能合约钱包，可以使用 ERC20 代币来支付交易手续费（无需使用原生代币）。所有转账操作均需通过此地址进行。

**请务必将代币发送到 Sequence 钱包地址**，才能使用 `transfer` 命令。可以使用 `wallet-info` 命令查看这两个地址。

## 命令参考

### create-wallet

生成一个新的 EOA（Externally Owned Account）密钥对。

```bash
npx @0xsequence/builder-cli create-wallet --json
```

JSON 输出：
```json
{
  "privateKey": "0x4c0883a...",
  "address": "0x89D9F8f...",
  "keyStored": true
}
```

### wallet-info

显示 EOA 地址和 Sequence 智能钱包地址。

```bash
npx @0xsequence/builder-cli wallet-info -k <private-key> -a <access-key> --json
```

选项：
- `-k, --private-key <key>` — 钱包私钥（如果已存储，则可选）
- `-a, --access-key <key>` — 项目访问密钥（必需）

JSON 输出：
```json
{
  "eoaAddress": "0x742BDb3...",
  "sequenceWalletAddress": "0xA71506...",
  "fundingUrl": "https://demo.trails.build/..."
}
```

### login

使用 Sequence Builder 进行身份验证。

```bash
npx @0xsequence/builder-cli login -k <private-key> --json
```

选项：
- `-k, --private-key <key>` — 钱包私钥（如果已存储，则可选）
- `-e, --email <email>` — 与账户关联的电子邮件地址
- `--env <environment>` — 环境：`prod`（默认）或 `dev`
- `--api-url <url>` — 自定义 API 地址

JSON 输出：
```json
{
  "success": true,
  "address": "0x742BDb3...",
  "expiresAt": "2026-02-07T12:00:00Z"
}
```

### projects

管理 Sequence Builder 项目（需要登录后使用）。

```bash
# List all projects
npx @0xsequence/builder-cli projects --json

# Create a new project
npx @0xsequence/builder-cli projects create "My Game" --json

# Create with specific chains
npx @0xsequence/builder-cli projects create "My Game" --chain-ids 137,8453 --json

# Get project details
npx @0xsequence/builder-cli projects get <project-id> --json
```

### apikeys

管理项目的 API 密钥（需要登录后使用）。

```bash
# List all API keys
npx @0xsequence/builder-cli apikeys <project-id> --json

# Get the default API key
npx @0xsequence/builder-cli apikeys default <project-id> --json
```

### transfer

使用 Sequence 智能钱包发送 ERC20 代币转账。交易手续费由所转移的代币本身支付（无需使用其他代币）。

```bash
npx @0xsequence/builder-cli transfer \
  -k <private-key> \
  -a <access-key> \
  -t <token-address> \
  -r <recipient-address> \
  -m <amount> \
  -c <chain-id> \
  --json
```

选项：
- `-k, --private-key <key>` — 钱包私钥（如果已存储，则可选）
- `-a, --access-key <key>` — 项目访问密钥（必需）
- `-t, --token <address>` — ERC20 代币的合约地址（必需）
- `-r, --recipient <address>` — 收件人地址（必需）
- `-m, --amount <amount>` — 代币数量（例如：`10.5`）（必需）
- `-c, --chain-id <chainId>` — 链路 ID（必需）

JSON 输出：
```json
{
  "success": true,
  "transactionHash": "0xabc123...",
  "from": "0xA71506...",
  "to": "0x123456...",
  "token": "0x833589...",
  "amount": "10.5",
  "symbol": "USDC",
  "chainId": 8453
}
```

### indexer

使用 Sequence Indexer 查询区块链数据。

```bash
# Get token balances
npx @0xsequence/builder-cli indexer balances <address> \
  -a <access-key> -c <chain-id> --include-metadata --json

# Get native token balance (ETH, MATIC, etc.)
npx @0xsequence/builder-cli indexer native-balance <address> \
  -a <access-key> -c <chain-id> --json

# Get transaction history
npx @0xsequence/builder-cli indexer history <address> \
  -a <access-key> -c <chain-id> --limit 20 --json

# Get token contract info
npx @0xsequence/builder-cli indexer token-info <contract-address> \
  -a <access-key> -c <chain-id> --json
```

## 支持的网络

| 网络 | 链路 ID |
|---------|----------|
| Ethereum | 1 |
| Polygon | 137 |
| Base | 8453 |
| Arbitrum | 42161 |
| Optimism | 10 |
| BSC | 56 |
| Avalanche | 43114 |

完整网络列表：https://status.sequence.info/

## 错误代码

| 代码 | 含义 |
|------|---------|
| 0 | 操作成功 |
| 1 | 一般错误 |
| 10 | 未登录 |
| 11 | 私钥无效 |
| 20 | 资金不足 |
| 30 | 未找到项目 |
| 31 | 项目未找到 |
| 40 | API 错误 |

## 常见工作流程

### 从零开始的全方位设置

```bash
export SEQUENCE_PASSPHRASE="my-secret"
npx @0xsequence/builder-cli create-wallet --json
# Save the output — privateKey and address
npx @0xsequence/builder-cli login --json
npx @0xsequence/builder-cli projects create "My App" --json
# Note the accessKey from the output
npx @0xsequence/builder-cli wallet-info -a <access-key> --json
# Fund the sequenceWalletAddress via the fundingUrl
```

### 先查看余额再转账

```bash
# Check balance first
npx @0xsequence/builder-cli indexer balances <your-sequence-wallet> \
  -a <access-key> -c 8453 --json

# Send transfer
npx @0xsequence/builder-cli transfer \
  -a <access-key> -t <token> -r <recipient> -m 10 -c 8453 --json
```

### 多链余额查询

```bash
# Check across multiple chains
npx @0xsequence/builder-cli indexer balances <address> -a <key> -c 1 --json
npx @0xsequence/builder-cli indexer balances <address> -a <key> -c 137 --json
npx @0xsequence/builder-cli indexer balances <address> -a <key> -c 8453 --json
```

## 配置信息

配置信息存储在 `~/.sequence-builder/config.json` 文件中：
- 用于身份验证的 JWT 令牌
- 环境设置（prod/dev）
- 加密后的私钥（当设置了 `SEQUENCE_PASSPHRASE` 时）

## 故障排除

- **“未登录”错误**：请先运行 `login` 命令。JWT 令牌可能已过期，请重新登录。
- **“私钥无效”错误**：私钥必须是一个 64 位的十六进制字符串（可以带有 `0x` 前缀，也可以不带）。如果使用已存储的私钥，请确认 `SEQUENCE_PASSPHRASE` 设置正确。
- **“资金不足”错误**：请将代币发送到 **Sequence 钱包地址**，而非 EOA 地址。可以使用 `wallet-info` 命令获取正确的地址。
- **转账失败**：确保 Sequence 钱包中有足够的代币用于支付手续费，并且使用的代币类型与转账所需的代币类型一致。