---
name: agentwalletapi
description: OpenclawCash 是一个专为 AI 代理设计的加密货币钱包 API。当代理需要发送原生货币或代币、查询余额、列出钱包账户，或通过 OpenclawCash 以编程方式与 EVM（以太坊虚拟机）和 Solana 钱包进行交互时，可以使用该 API。
license: Proprietary
compatibility: Requires network access to https://openclawcash.com
metadata:
  author: agentwalletapi
  version: "1.9.1"
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

该API用于与OpenclawCash管理的钱包交互，支持发送原生资产和代币、查询余额以及在EVM和Solana网络中执行安全可靠的钱包操作。

## 必需条件

- 必需的环境变量：`AGENTWALLETAPI_KEY`
- 可选的环境变量：`AGENTWALLETAPI_URL`（默认值：`https://openclawcash.com`）
- 必需的本地工具：`curl`
- 可选的本地工具：`jq`（用于在CLI中生成格式化的JSON输出）
- 需要网络访问权限：`https://openclawcash.com`

## 安全模型

- 首先在测试网络上使用只读操作（`wallets`、`wallet`、`balance`、`tokens`）。
- 高风险操作需要额外的权限控制：
  - 通过控制面板设置API密钥权限（`allowWalletCreation`、`allowWalletImport`）
  - 对于写操作，需要通过CLI明确确认（使用`--yes`选项）

## 设置

1. 运行设置脚本以创建`.env`文件：
   ```
   bash scripts/setup.sh
   ```
2. 在该技能文件夹中编辑`.env`文件，并将占位符替换为你的实际API密钥：
   ```
   AGENTWALLETAPI_KEY=ag_your_real_key_here
   ```
3. 在https://openclawcash.com获取API密钥（注册、创建钱包，然后进入API密钥页面）。

## CLI工具

使用提供的工具脚本直接发起API请求：

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
# Automation-safe import: read private key from stdin instead of command args
printf '%s' '<private_key>' | bash scripts/agentwalletapi.sh import "Treasury Imported" mainnet - --yes
bash scripts/agentwalletapi.sh transfer 2 0xRecipient 0.01 --yes
bash scripts/agentwalletapi.sh transfer 2 0xRecipient 100 USDC --yes
bash scripts/agentwalletapi.sh quote mainnet WETH USDC 10000000000000000
bash scripts/agentwalletapi.sh swap 2 WETH USDC 10000000000000000 0.5 --yes
```

### 输入安全

- 导入钱包是可选的，对于常规钱包操作（如列表、查询余额、转账、交换）并非必需。
- 只有在用户通过控制面板启用`allowWalletImport`权限后，导入功能才会生效。
- 执行导入操作时需要在CLI中明确确认（自动化时使用`--yes`，或交互式提示`YES`）。
- 尽量避免将敏感信息作为CLI参数传递（可能存在shell历史记录或进程日志泄露风险）。
- 推荐的选项：
  - 交互式隐藏提示：省略私钥参数。
  - 自动化：使用`-`并通过stdin传递输入。

## 基本URL

```
https://openclawcash.com
```

## 故障排除

如果请求因主机/URL问题失败，请按照以下步骤进行排查：

1. 打开`agentwalletapi/.env`文件，确认`AGENTWALLETAPI_KEY`已设置且没有多余的空白字符。
2. 如果API主机地址错误或无法访问，请在`.env`文件中修正该地址：
   ```
   AGENTWALLETAPI_URL=https://openclawcash.com
   ```
3. 先尝试执行一个简单的读取请求：
   ```bash
   bash scripts/agentwalletapi.sh wallets
   ```
4. 如果仍然失败，请报告具体的错误信息，并在尝试转账/交换操作前停止。

## 身份验证

API密钥从该技能文件夹中的`.env`文件中读取。对于直接HTTP请求，需将其作为请求头的一部分进行传递：

```
X-Agent-Key: ag_your_key_here
Content-Type: application/json
```

## API接口

- **代理API（API密钥认证）：** `/api/agent/*`
  - 使用`X-Agent-Key`进行认证
  - 用于执行代理相关的操作（如钱包列表/创建/导入、交易、查询余额、转账、交换、报价、批准）

- **控制面板/用户API（会话认证）：** `/api/wallets/*`
  - 使用bearer token或`aw_session` cookie进行认证
  - 用于用户管理的控制面板操作（包括钱包导入和创建）
  - 创建钱包时现在需要提供`exportPassphrase`（至少12个字符）
  - 导出私钥时也需要`exportPassphrase`，并受到速率限制和临时锁定的保护

## 工作流程

1. `GET /api/agent/wallets` - 查看可用的钱包信息（ID、标签、地址、网络、链；不包含余额）
2. `GET /api/agent/wallet?walletId=...` 或 `?walletLabel=...` - 获取指定钱包的原生/代币余额信息
3. 可选的钱包生命周期操作：
   - `POST /api/agent/wallets/create` - 在API密钥的权限控制下创建新钱包
   - `POST /api/agent/wallets/import` - 通过API密钥导入`mainnet`或`solana-mainnet`钱包
4. `GET /api/agent/transactions?walletId=...` - 查看钱包的交易历史记录（包括链上记录和应用程序记录）
5. `GET /api/agent/supported-tokens?network=...` 或 `?chain=evm|solana` - 获取推荐的常见代币列表及相关信息
6. `POST /api/agent/token-balance` - 查询钱包余额（包括原生代币和代币；支持按符号/地址查询）
7. `POST /api/agent/quote` - 在执行交易前获取Uniswap报价（仅限EVM）
8. `POST /api/agent/swap` - 在Uniswap（EVM）或Jupiter（Solana）上执行代币交换
9. `POST /api/agent/transfer` - 在钱包所在的链上发送原生货币或代币（可选参数`chain`用于指定链）
10. 使用返回的`txHash`值来确认交易结果

## 快速参考

| 接口 | 方法 | 认证方式 | 功能 |
|---|---|---|---|
| `/api/agent/wallets` | GET | 是 | 列出钱包信息（仅用于发现，不包含余额） |
| `/api/agent/wallet` | GET | 是 | 获取指定钱包的详细信息及余额（包括原生代币） |
| `/api/agent/wallets/create` | POST | 是 | 使用API密钥创建新钱包 |
| `/api/agent/wallets/import` | POST | 是 | 通过API密钥导入`mainnet`或`solana-mainnet`钱包 |
| `/api/agent/transactions` | GET | 是 | 查看每个钱包的交易历史记录 |
| `/api/agent/transfer` | POST | 是 | 发送原生货币或代币（支持EVM和Solana） |
| `/api/agent/swap` | POST | 是 | 在Uniswap（EVM）或Jupiter（Solana）上执行代币交换 |
| `/api/agent/quote` | POST | 否 | 获取Uniswap报价（仅限EVM） |
| `/api/agent/token-balance` | POST | 是 | 查询余额 |
| `/api/agent/supported-tokens` | GET | 否 | 获取每个网络推荐的常见代币列表 |
| `/api/agent/approve` | POST | 是 | 批准ERC-20代币的支出方（仅限EVM） |

## 代理钱包创建/导入（代理API）

代理端相关的钱包生命周期操作：

- `POST /api/agent/wallets/create`
- `POST /api/agent/wallets/import`

**操作说明：**
- 两个操作都需要`X-Agent-Key`。
- 两个操作都受控制面板中配置的API密钥权限限制：
  - `allowWalletCreation`用于创建钱包
  - `allowWalletImport`用于导入钱包
- 两个操作都受到API密钥的速率限制。超出限制会返回429错误代码，需要重新尝试。
- 代理钱包导入支持`mainnet`和`solana-mainnet`网络。
- 创建代理钱包时需要：
  - 提供`exportPassphrase`（至少12个字符）
  - 确认`confirmExportPassphraseSaved`为`true`
- 代理钱包创建的流程：
  - 首先将导出的密码保存到安全存储中。
  - 然后使用该密码和确认信息调用`POST /api/agent/wallets/create`。

## 转账示例

- 如果未指定代币，默认发送原生货币：
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
{ "walletId": "Q7X2K9P", "to": "SolanaRecipientWalletAddress...", "token": "SOL", "amount": "0.01" }
```
- 按备注信息发送SOL（仅限Solana）：
   ```json
{ "walletId": "Q7X2K9P", "to": "SolanaRecipientWalletAddress...", "token": "SOL", "amount": "0.01", "memo": "payment verification note" }
```
- 使用`amount`参数输入可读的值（例如，“100”表示100 USDC）；使用`value`参数输入基础单位（每个链的最小单位）。
- 可以在代理端请求中指定`chain: "evm" | "solana"以进行链路由和验证。
- Solana转账支持`memo`参数，但必须通过安全验证（最多5个单词，最多256个UTF-8字节，不允许包含控制字符或不可见字符）。
- 对于原生SOL转账，API会自动调整请求金额以包含平台费和网络费。
- 转账响应中包含`requestedValue`、`adjustedValue`、`requestedAmount`和`adjustedAmount`字段。

## 代币支持模型

- `GET /api/agent/supported-tokens`返回推荐的常见代币列表及相关信息。
- EVM相关的转账/交换/余额接口支持任何有效的ERC-20代币合约地址。
- Solana相关的转账/余额接口支持任何有效的SPL代币地址。
- 在EVM上，原生代币显示为`ETH`；在Solana上显示为`SOL`（余额信息中包含特定链的原生代币ID）。

## 错误代码

- 200：成功
- 400：输入无效、资金不足、代币未知或违反政策
- 400 `chain_mismatch`：请求的链与选定的钱包不匹配
- 400 `insufficient_balance`：请求的转账金额加上费用超过了钱包余额
- 401：API密钥缺失或无效
- 404：钱包未找到
- 500：内部错误（请使用正确的参数或减少金额后重试）

## 政策限制

钱包可能具有以下治理策略：
- **白名单**：仅允许向预先批准的地址转账
- **消费限制**：每笔交易的最大金额（由钱包策略配置）

违反这些规则会导致401错误，并附带错误信息。

## 重要提示

- 所有POST请求都需要设置`Content-Type: application/json`
- EVM代币转账需要钱包中持有ETH作为Gas费用
- Solana代币转账需要钱包中持有SOL作为费用
- Solana转账的备注信息是可选的，仅适用于Solana网络（最多5个单词，最多256个UTF-8字节，不允许包含控制字符或不可见字符）
- Solana的原生转账会自动调整转账金额以包含网络费用
- 如果请求的金额加上平台费和网络费超过了钱包余额，API会返回400 `insufficient_balance`错误
- 支持在EVM（Uniswap）和Solana（Jupiter）上进行代币交换；报价和批准功能仅限于EVM
- 会从代币金额中扣除平台费用（默认为1%）
- 为简化操作，建议使用`amount`参数；如需精确控制基础单位，请使用`value`参数
- 为了确保代理操作的稳定性：
  - 先调用`wallets`，然后是`wallet`（或`token-balance`），接着是`quote`，最后是`swap`。
- 如果遇到400 `insufficient_token_balance`错误，请减少转账金额或更换代币。
- 该技能文件夹中的`.env`文件存储了你的API密钥——切勿将其提交到版本控制系统

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