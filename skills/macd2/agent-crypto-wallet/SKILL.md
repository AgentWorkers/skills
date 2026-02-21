---
name: agentwalletapi
description: OpenclawCash 是一款专为 AI 代理设计的加密钱包 API。当代理需要发送原生货币或代币、查询余额、列出钱包账户，或通过 OpenclawCash 以编程方式与 EVM（以太坊虚拟机）和 Solana 网络中的钱包进行交互时，可以使用该 API。
license: Proprietary
compatibility: Requires network access to https://openclawcash.com
metadata:
  author: agentwalletapi
  version: "1.9.0"
  required_env_vars:
    - AGENTWALLETAPI_KEY
  optional_env_vars:
    - AGENTWALLETAPI_URL
  required_binaries:
    - curl
  optional_binaries:
    - jq
---
# OpenclawCash Agent API

该API用于与OpenclawCash管理的钱包交互，支持发送原生资产和代币、查询余额以及在EVM和Solana网络上执行安全的钱包操作。

## 必需条件

- 必需的环境变量：`AGENTWALLETAPI_KEY`
- 可选的环境变量：`AGENTWALLETAPI_URL`（默认值：`https://openclawcash.com`）
- 必需的本地工具：`curl`
- 可选的本地工具：`jq`（用于在CLI中生成格式化的JSON输出）
- 需要网络访问权限：`https://openclawcash.com`

## 安全模型

- 首先在测试网络上使用只读操作（`wallets`、`wallet`、`balance`、`tokens`）。
- 高风险操作需要额外的权限控制：
  - 通过仪表板设置API密钥权限（`allowWalletCreation`、`allowWalletImport`）
  - 对于写入操作，需要通过CLI明确确认（`--yes`）
- 导入钱包时，私钥会发送到OpenclawCash进行加密存储和管理。请确保您理解并接受这种信任模型。

## 设置

1. 运行设置脚本以创建`.env`文件：
   ```
   bash scripts/setup.sh
   ```
2. 在该技能文件夹中编辑`.env`文件，并将占位符替换为实际的API密钥：
   ```
   AGENTWALLETAPI_KEY=ag_your_real_key_here
   ```
3. 在https://openclawcash.com获取您的API密钥（注册、创建钱包，然后进入API Keys页面）。

## CLI工具

使用随附的工具脚本直接发起API请求：

```bash
# Read-only (recommended first)
bash scripts/agentwalletapi.sh wallets
bash scripts/agentwalletapi.sh wallet 2
bash scripts/agentwalletapi.sh wallet "Trading Bot"
bash scripts/agentwalletapi.sh balance 2
bash scripts/agentwalletapi.sh transactions 2
bash scripts/agentwalletapi.sh tokens mainnet

# Write actions (require explicit --yes)
bash scripts/agentwalletapi.sh create "Ops Wallet" sepolia --yes
bash scripts/agentwalletapi.sh import "Treasury Imported" mainnet --yes
bash scripts/agentwalletapi.sh transfer 2 0xRecipient 0.01 --yes
bash scripts/agentwalletapi.sh transfer 2 0xRecipient 100 USDC --yes
bash scripts/agentwalletapi.sh quote mainnet WETH USDC 10000000000000000
bash scripts/agentwalletapi.sh swap 2 WETH USDC 10000000000000000 0.5 --yes
```

## 基本URL

```
https://openclawcash.com
```

## 故障排除

如果请求因主机/URL问题失败，请按照以下步骤进行排查：

1. 打开`agentwalletapi/.env`文件，确认`AGENTWALLETAPI_KEY`已设置且没有多余的空白字符。
2. 如果API主机地址错误或无法访问，请在`.env`文件中修改该地址：
   ```
   AGENTWALLETAPI_URL=https://openclawcash.com
   ```
3. 首先尝试一个简单的读取请求：
   ```bash
   bash scripts/agentwalletapi.sh wallets
   ```
4. 如果仍然失败，请报告具体的错误信息，并在尝试转账/交换操作前停止。

## 认证

API密钥从该技能文件夹中的`.env`文件中读取。对于直接发起的HTTP请求，需要将密钥作为请求头的一部分进行传递：

```
X-Agent-Key: ag_your_key_here
Content-Type: application/json
```

## API接口

- **代理API（需要API密钥认证）：** `/api/agent/*`
  - 使用`X-Agent-Key`进行认证
  - 用于执行代理相关的操作（如钱包列表/创建/导入、交易、查询余额、转账、交换、报价、批准）
- **仪表板/用户API（需要会话认证）：** `/api/wallets/*`
  - 使用bearer token或`aw_session` cookie进行认证
  - 用于用户管理的操作（包括钱包导入）

## 工作流程

1. `GET /api/agent/wallets` - 查看可用的钱包（ID、标签、地址、网络、链；不显示余额）
2. `GET /api/agent/wallet?walletId=...` 或 `?walletLabel=...` - 获取指定钱包的原生资产/代币余额
3. 可选的钱包生命周期操作：
   - `POST /api/agent/wallets/create` - 在API密钥的权限控制下创建新钱包
   - `POST /api/agent/wallets/import` - 通过API密钥导入`mainnet`或`solana-mainnet`钱包
4. `GET /api/agent/transactions?walletId=...` - 查看钱包的交易历史（包括链上和应用程序记录的交易）
5. `GET /api/agent/supported-tokens?network=...` 或 `?chain=evm|solana` - 获取推荐的常见代币列表及相关信息
6. `POST /api/agent/token-balance` - 查询钱包余额（包括原生资产和代币余额；支持特定代币）
7. `POST /api/agent/quote` - 在执行交易前获取Uniswap报价（仅限EVM）
8. `POST /api/agent/swap` - 在Uniswap（EVM）或Jupiter（Solana）上执行代币交换
9. `POST /api/agent/transfer` - 在钱包所在的链上发送原生资产或代币（可选参数`chain`用于指定链）
10. 使用返回的`txHash`值来确认交易结果

## 快速参考

| 接口 | 方法 | 认证方式 | 功能 |
|---|---|---|---|
| `/api/agent/wallets` | GET | 是 | 列出钱包信息（仅用于发现，不显示余额） |
| `/api/agent/wallet` | GET | 是 | 获取指定钱包的详细信息及余额 |
| `/api/agent/wallets/create` | POST | 是 | 创建新的钱包 |
| `/api/agent/wallets/import` | POST | 通过API密钥导入钱包 |
| `/api/agent/transactions` | GET | 是 | 查看钱包的交易历史 |
| `/api/agent/transfer` | POST | 是 | 发送原生资产或代币 |
| `/api/agent/swap` | POST | 在Uniswap（EVM）或Jupiter（Solana）上执行代币交换 |
| `/api/agent/quote` | POST | 否 | 获取Uniswap报价（仅限EVM） |
| `/api/agent/token-balance` | POST | 是 | 查询余额 |
| `/api/agent/supported-tokens` | GET | 是 | 获取每个网络上推荐的常见代币列表 |
| `/api/agent/approve` | POST | 是 | 批准ERC-20代币的支出操作（仅限EVM） |

## 代理钱包的创建/导入（代理API）

代理端相关的钱包操作接口：

- `POST /api/agent/wallets/create`
- `POST /api/agent/wallets/import`

**注意事项：**
- 这两个操作都需要`X-Agent-Key`。
- 这两个操作都受到仪表板中配置的API密钥权限的限制：
  - `allowWalletCreation`用于创建新钱包
  - `allowWalletImport`用于导入钱包
- 这两个操作都受到API密钥使用次数的限制。超出限制会返回429错误码，并提示“Retry-After”。
- 代理钱包支持`mainnet`和`solana-mainnet`网络。

## 转账示例

- 发送原生资产（未指定代币时默认使用此方法）：
   ```json
{ "walletId": 2, "to": "0xRecipient...", "amount": "0.01" }
```
- 按代币符号发送100 USDC：
   ```json
{ "walletLabel": "Trading Bot", "to": "0xRecipient...", "token": "USDC", "amount": "100" }
```
- 按合约地址发送任意ERC-20代币：
   ```json
{ "walletId": 2, "to": "0xRecipient...", "token": "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48", "amount": "100" }
```
- 按代币符号发送SOL：
   ```json
{ "walletId": 7, "to": "9xQeWvG816bUx9EPfHmaT23yvVMY6sX3uA9wX6kM3cVG", "token": "SOL", "amount": "0.01" }
```
- 使用`amount`参数输入人类可读的值（例如，“100”表示100 USDC）；使用`value`参数输入最小单位。
- 可以在代理请求中指定`chain: "evm" | "solana"以指定传输的链。

## 代币支持模型

- `GET /api/agent/supported-tokens`返回推荐的常见代币列表及相关信息。
- EVM相关的转账/交换/查询余额接口支持任何有效的ERC-20代币合约地址。
- Solana相关的转账/查询余额接口支持任何有效的SPL代币地址。
- 在EVM上，原生代币显示为`ETH`；在Solana上显示为`SOL`（余额信息中包含特定链的原生代币ID）。

## 错误代码

- 200：操作成功
- 400：输入无效、资金不足、代币未知或违反政策
- 400 `chain_mismatch`：请求的链与选定的钱包不匹配
- 401：API密钥缺失或无效
- 404：钱包未找到
- 500：内部错误（请使用正确的参数或减少转账金额后重试）

## 政策限制

钱包可能具有以下治理策略：
- **白名单**：仅允许向预先批准的地址转账
- **消费限额**：每次交易的最大金额（由钱包策略设置）

违反这些规则会导致401错误，并附带错误信息。

## 重要提示

- 所有POST请求都需要设置`Content-Type: application/json`
- EVM上的代币转账需要钱包中持有ETH作为交易手续费
- Solana上的代币转账需要钱包中持有SOL作为手续费
- 交换操作支持EVM（Uniswap）和Solana（Jupiter）；报价和批准操作仅限于EVM
- 平台会收取1%的费用（默认）
- 为简化操作，建议使用`amount`参数；如需精确控制金额，请使用`value`参数
- 为了确保代理操作的正确性，请按照以下顺序执行操作：`wallets` → `wallet` → `token-balance` → `quote` → `swap`
- 如果遇到400错误（提示“insufficient_token_balance”），请减少转账金额或更换代币
- 请将`.env`文件中的API密钥妥善保管，切勿将其提交到版本控制系统中

## 文件结构

```
agentwalletapi/
├── SKILL.md                    # This file
├── .env                        # Your API key (created by setup.sh)
├── scripts/
│   ├── setup.sh                # Creates .env with API key placeholder
│   └── agentwalletapi.sh       # CLI tool for making API calls
└── references/
    └── api-endpoints.md        # Full endpoint documentation
```

有关完整的接口详情和请求/响应示例，请参阅[references/api-endpoints.md]。