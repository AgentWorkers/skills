---
name: agentwalletapi
description: OpenclawCash 是一个专为 AI 代理设计的加密钱包 API。当代理需要发送原生货币或代币、查询余额、列出钱包账户，或通过 OpenclawCash 以编程方式与 EVM（以太坊虚拟机）和 Solana 钱包进行交互时，可以使用该 API。
license: Proprietary
compatibility: Requires network access to https://openclawcash.com
metadata:
  author: agentwalletapi
  version: "1.9.4"
  required_env_vars:
    - AGENTWALLETAPI_KEY
  optional_env_vars:
    - AGENTWALLETAPI_URL
  required_binaries:
    - curl
  optional_binaries:
    - jq
---
# OpenclawCash 代理 API

该 API 可用于与 OpenclawCash 管理的钱包交互，执行发送原生资产和代币、查询余额以及跨 EVM 和 Solana 网络的安全钱包操作。

## 必需条件

- 必需的环境变量：`AGENTWALLETAPI_KEY`
- 可选的环境变量：`AGENTWALLETAPI_URL`（默认值：`https://openclawcash.com`）
- 必需的本地工具：`curl`
- 可选的本地工具：`jq`（用于在 CLI 中生成格式化的 JSON 输出）
- 需要网络访问权限：`https://openclawcash.com`

## 推荐的集成方式

- 如果客户端支持 MCP（OpenclawCash 的管理平台），建议使用公共的 OpenclawCash MCP 服务器：
  ```bash
  npx -y @openclawcash/mcp-server
  ```
  - 优先使用 MCP 作为主要执行路径，因为相关工具、数据结构和结果都是为 MCP 设计的。
  - 仅在 MCP 不可用或客户端无法连接 MCP 服务器时，才使用附带的 CLI 脚本作为备用方案。
  - MCP 和 CLI 脚本都基于相同的 OpenclawCash 代理 API，它们是两种不同的访问方式，但属于同一系统。

## 安全模型

- 首先在测试网络上使用只读操作（`wallets`、`wallet`、`balance`、`tokens`）。
- 高风险操作需要额外的授权：
  - 通过仪表板设置 API 密钥权限（`allowWalletCreation`、`allowWalletImport`）
  - 对写操作需要用户通过 CLI 明确确认（使用 `--yes`）
- 代理应在会话开始时设置写操作的授权模式：
  - `confirm_each_write`：每次执行写操作前都需要用户确认。
  - `operate_on_my_behalf`：在用户首次确认后，后续的写操作无需再次确认，只要用户在同一会话中继续发出指令即可。
  - 对于 `operate_on_my_behalf` 模式，代理应将用户的后续指令视为执行命令，并使用 `--yes` 来执行相应的写操作。
- 仅在以下情况下重新请求确认：
  - 用户撤销或更改授权模式
  - 会话重启或内存丢失
  - 操作超出了用户授权的范围
  - 代理无法确定目标钱包、代币、金额、接收者或链路
- 如果用户只给出了类似“继续”的模糊指令，应先收集缺失的详细信息，而不是重复请求权限。

## 设置步骤

1. 运行设置脚本以创建 `.env` 文件：
   ```
   bash scripts/setup.sh
   ```
2. 在该技能文件夹中编辑 `.env` 文件，并将占位符替换为你的实际 API 密钥：
   ```
   AGENTWALLETAPI_KEY=occ_your_api_key
   ```
3. 在 https://openclawcash.com 上获取 API 密钥（注册、创建钱包，然后进入 API 密钥页面）。

## 备用方案（CLI）

如果 MCP 不可用，可以使用附带的工具脚本直接进行 API 调用：
```bash
# Read-only (recommended first)
bash scripts/agentwalletapi.sh wallets
bash scripts/agentwalletapi.sh wallet 2
bash scripts/agentwalletapi.sh wallet "Trading Bot"
bash scripts/agentwalletapi.sh balance 2
bash scripts/agentwalletapi.sh transactions 2
bash scripts/agentwalletapi.sh tokens mainnet

# Write actions (require explicit --yes)
export WALLET_EXPORT_PASSPHRASE_OPS='your-strong-passphrase'
bash scripts/agentwalletapi.sh create "Ops Wallet" sepolia WALLET_EXPORT_PASSPHRASE_OPS --yes
bash scripts/agentwalletapi.sh import "Treasury Imported" mainnet --yes
# Automation-safe import: read private key from stdin instead of command args
printf '%s' '<private_key>' | bash scripts/agentwalletapi.sh import "Treasury Imported" mainnet - --yes
bash scripts/agentwalletapi.sh transfer 2 0xRecipient 0.01 --yes
bash scripts/agentwalletapi.sh transfer 2 0xRecipient 100 USDC --yes
bash scripts/agentwalletapi.sh quote mainnet WETH USDC 10000000000000000
bash scripts/agentwalletapi.sh swap 2 WETH USDC 10000000000000000 0.5 --yes
```

### 输入安全

- 导入钱包是可选的，对于常规的钱包操作（如列表、查询余额、转账、交换）并非必需。
- 只有在用户通过仪表板设置启用 `allowWalletImport` 权限后，导入功能才会生效。
- 执行导入操作时需要用户在 CLI 中明确确认（自动化时使用 `--yes`，或交互式提示 `YES`）。
- 尽量避免将敏感信息作为 CLI 参数传递（可能存在shell历史记录/进程日志安全风险）。
- 推荐的选项：
  - 交互式隐藏提示：省略私钥参数。
  - 自动化：传递 `-` 并通过 stdin 传递输入。

## 基本 URL

```
https://openclawcash.com
```

## 故障排除

如果请求因主机/URL 问题失败，请按照以下步骤进行排查：

1. 打开 `agentwalletapi/.env` 文件，确认 `AGENTWALLETAPI_KEY` 已设置且没有多余的空格。
2. 如果 API 主机地址错误或无法访问，请在 `.env` 文件中修改该地址：
   ```
   AGENTWALLETAPI_URL=https://openclawcash.com
   ```
3. 先尝试执行一个简单的读取请求：
   ```bash
   bash scripts/agentwalletapi.sh wallets
   ```
4. 如果仍然失败，请报告具体的错误信息，并在尝试转账/交换操作前停止。

## 认证

API 密钥从该技能文件夹中的 `.env` 文件中加载。对于直接通过 HTTP 的请求，需要将其作为请求头的一部分：

```
X-Agent-Key: occ_your_api_key
Content-Type: application/json
```

## API 接口

- **代理 API（基于 API 密钥的认证）：** `/api/agent/*`
  - 使用 `X-Agent-Key` 进行认证
  - 用于代理的自主操作（如钱包列表/创建/导入、交易、查询余额、转账、交换、报价、批准）
- **仪表板/用户 API（基于会话认证）：** `/api/wallets/*`
  - 使用 bearer token 或 `aw_session` cookie 进行认证
  - 用于用户管理的仪表板操作（包括钱包导入和创建）
  - 创建钱包时现在需要提供 `exportPassphrase`（至少 12 个字符）
  - 导出私钥时需要 `exportPassphrase`，并且会受到速率限制和临时锁定的保护。

## 工作流程

1. `GET /api/agent/wallets` - 查找可用的钱包（ID、标签、地址、网络、链路）。可选参数 `?includeBalances=true` 可显示原生余额和代币余额。
2. `GET /api/agent/wallet?walletId=...` 或 `?walletLabel=...` 或 `?walletAddress=...` - 获取指定钱包的原生/代币余额信息。
3. 可选的钱包生命周期操作：
   - `POST /api/agent/wallets/create` - 在 API 密钥的权限控制下创建新钱包
   - `POST /api/agent/wallets/import` - 通过 API 密钥导入主网或 Solana 主网的钱包
4. `GET /api/agent/transactions?walletId=...`（或 `walletLabel`/`walletAddress`） - 查看钱包的交易历史（包括链上和应用程序记录的交易）
5. `GET /api/agent/supported-tokens?network=...` 或 `?chain=evm|solana` - 获取推荐的常见代币列表及相关信息
6. `POST /api/agent/token-balance` - 查询钱包余额（包括原生代币和代币余额；支持特定代币和地址）
7. `POST /api/agent/quote` - 在执行前获取 Uniswap 的报价（仅限 EVM）
8. `POST /api/agent/swap` - 在 Uniswap（EVM）或 Jupiter（Solana）上执行代币交换
9. `POST /api/agent/transfer` - 在钱包所在的链路上发送原生货币或代币（可选参数 `chain`）
10. 使用返回的 `txHash` 值来确认交易结果

### 代理的授权处理

对于写操作，请遵循以下模式：

1. 在会话中的第一次写操作时，询问用户一个简短的授权问题：
   - “您是否希望每次写操作都获得授权，还是希望我代表您执行？”
2. 将用户选择的授权模式存储在会话内存中。
3. 如果授权模式为 `confirm_each_write`：
   - 在每次转账、交换、批准或创建钱包操作前都需要用户确认
   - 确认后，使用 MCP 的写工具或备用 CLI 脚本（`--yes`）来执行操作
4. 如果授权模式为 `operate_on_my_behalf`：
   - 之后的转账操作无需再次确认
   - 当用户后续发出如“将 100 USDC 从钱包 2 转移到以太坊上的 0xabc...”这样的指令时，使用 MCP 的写工具或备用 CLI 脚本（`--yes`）来执行操作
5. 无论哪种模式：
   - 如果缺少执行细节，只需询问缺失的细节
   - 如果用户更改授权模式或撤销权限，更新内存并遵循新的规则

**推荐的引导语：**
- “请选择本次会话的写操作授权模式：`confirm_each_write` 或 `operate_on_my_behalf`。”

**示例：**
- 用户选择：`operate_on_my_behalf`
- 用户后续指令：“将 100 USDC 从钱包 2 转移到以太坊上的 0xabc...”
- 如果 MCP 可用，代理应直接调用相应的 MCP 写操作工具。
- 如果 MCP 不可用，代理应执行以下操作：
  ```bash
  bash scripts/agentwalletapi.sh transfer 2 0xabc... 100 USDC evm --yes
  ```
- 在同一会话中，除非用户撤销授权模式或指令不明确，否则代理不应再次请求转账权限。

## 快速参考

| 端点 | 方法 | 认证方式 | 功能 |
|---|---|---|---|
| `/api/agent/wallets` | GET | 是 | 列出钱包（包含原生余额信息） |
| `/api/agent/wallet` | GET | 是 | 获取单个钱包的详细信息（包括原生/代币余额） |
| `/api/agent/wallets/create` | POST | 是 | 创建新的 API 密钥管理的钱包 |
| `/api/agent/wallets/import` | POST | 是 | 通过 API 密钥导入主网或 Solana 主网的钱包 |
| `/api/agent/transactions` | GET | 是 | 查看每个钱包的交易历史 |
| `/api/agent/transfer` | POST | 是 | 发送原生货币或代币（支持 EVM 和 Solana） |
| `/api/agent/swap` | POST | 是 | 在 Uniswap（EVM）或 Jupiter（Solana）上执行代币交换 |
| `/api/agent/quote` | POST | 否 | 获取 Uniswap 的报价（仅限 EVM） |
| `/api/agent/token-balance` | POST | 是 | 查询余额 |
| `/api/agent/supported-tokens` | GET | 否 | 获取每个网络推荐的常见代币列表 |
| `/api/agent/approve` | POST | 是 | 为 ERC-20 代币的接收者进行授权（仅限 EVM） |

## 代理钱包的创建/导入（代理 API）

代理端相关的钱包生命周期操作端点：

- `POST /api/agent/wallets/create`
- `POST /api/agent/wallets/import`

**操作说明：**
- 两者都需要 `X-Agent-Key`。
- 两者都受仪表板中配置的 API 密钥权限限制：
  - `allowWalletCreation` 用于创建钱包
  - `allowWalletImport` 用于导入钱包
- 两者都受到 API 密钥的速率限制。超出限制会返回错误码 `429`，并提示“Retry-After”。
- 代理导入支持主网（mainnet）和 Solana 主网（solana-mainnet）钱包。
- 创建钱包时需要提供：
  - `exportPassphrase`（至少 12 个字符）
  - `exportPassphraseStorageType`
  - `exportPassphraseStorageRef`
  - `confirmExportPassphraseSaved: true`
- 安全的创建流程：
  - 首先将导出的密码保存到安全存储中。
  - 对于本地代理，建议使用环境变量支持的存储方式。
  - 记录存储的位置。
  - 然后使用以下参数调用 `POST /api/agent/wallets/create`：
    - 密码
    - `exportPassphraseStorageType`
    - `exportPassphraseStorageRef`
    - `confirmExportPassphraseSaved: true`
- 对于 MCP 和备用 CLI，使用环境变量支持的存储方式是最安全的，因为本地工具可以在创建钱包之前验证环境变量的存在。

## 转账示例

- 如果未指定代币，默认发送原生货币：
   ```json
{ "walletId": 2, "to": "0xRecipient...", "amount": "0.01" }
```
- 按代币符号发送 100 USDC：
   ```json
{ "walletLabel": "Trading Bot", "to": "0xRecipient...", "token": "USDC", "amount": "100" }
```
- 按合约地址发送 ERC-20 代币：
   ```json
{ "walletId": 2, "to": "0xRecipient...", "token": "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48", "amount": "100" }
```
- 按代币符号发送 SOL：
   ```json
{ "walletId": "Q7X2K9P", "to": "SolanaRecipientWalletAddress...", "token": "SOL", "amount": "0.01" }
```
- 按备注信息发送 SOL（仅限 Solana）：
   ```json
{ "walletId": "Q7X2K9P", "to": "SolanaRecipientWalletAddress...", "token": "SOL", "amount": "0.01", "memo": "payment verification note" }
```
- 使用 `amount` 参数表示可读的金额（例如，“100”表示 100 USDC）；使用 `value` 参数表示基础单位（每个链路的最小单位）。
- 在代理请求中可以使用 `chain: "evm" | "solana"` 来指定链路并进行验证。
- 备注信息（`memo`）仅支持 Solana 转账，且必须通过安全验证（最多 5 个单词，最多 256 字节 UTF-8 字符）。
- 对于原生货币转账（EVM 和 Solana），系统会自动调整请求金额以包含平台费和网络费；对于 Solana，新接收地址可能需要额外的初始资金。
- 转账响应中会包含 `requestedValue`、`adjustedValue`、`requestedAmount` 和 `adjustedAmount`。

## 代币支持模型

- `GET /api/agent/supported-tokens` 返回推荐的常见代币列表及相关信息。
- EVM 的转账/交换/查询余额接口支持任何有效的 ERC-20 代币合约地址。
- Solana 的转账/查询余额接口支持任何有效的 SPL 代币地址。
- 在 EVM 上，原生代币显示为 `ETH`；在 Solana 上显示为 `SOL`（余额信息中包含链路特定的代币 ID）。

## 错误代码

- 200：成功
- 400：输入无效、资金不足、代币未知或违反政策
- 400 `chain_mismatch`：请求的链路与选定的钱包不匹配
- 400 `amount_below_min_transfer`：请求的转账金额低于平台费和网络费后的最低可转移金额
- 400 `insufficient_balance`：请求的转账金额加上费用超过了可用余额
- 401：API 密钥缺失或无效
- 404：钱包未找到
- 500：内部错误（请使用正确的参数或减少金额后重试）

## 政策限制

钱包可能有以下治理规则：
- **白名单**：仅允许向预先批准的地址转账
- **消费限制**：每次交易的最大金额（由钱包策略配置）

违反规则会导致 HTTP 401 错误，并附带错误信息。

## 重要提示

- 所有 POST 请求都需要设置 `Content-Type: application/json`
- EVM 代币转账需要钱包中包含 ETH 作为 gas 费用
- Solana 代币转账需要钱包中包含 SOL 作为费用
- Solana 的转账备注信息是可选的，仅适用于 Solana：最多 5 个单词，最多 256 字节 UTF-8 字符
- Solana 的原生转账会自动调整请求金额以包含平台费和网络费
- 对于原生货币转账，如果请求的金额过低（无法满足平台费和网络费），API 会返回 `400 amount_below_min_transfer`
- 如果请求的 Solana 原生代币金额加上平台费和网络费超过了钱包余额，API 会返回 `400 insufficient_balance`
- 支持在 EVM（Uniswap）和 Solana（Jupiter）上进行代币交换；报价/批准功能仅限于 EVM
- 平台费用（默认为 1%）会从代币金额中扣除
- 为简化操作，可以使用 `amount` 参数；如需精确控制金额，可以使用 `value` 参数
- 为了确保代理行为的正确性，请按照以下顺序操作：
  - 先调用 `wallets`，然后 `wallet`（或 `token-balance`），然后 `quote`，最后 `swap`。
- 如果遇到 `insufficient_token_balance` 错误，应减少金额或更改代币类型。
- 该技能文件夹中的 `.env` 文件存储了你的 API 密钥——切勿将其提交到版本控制系统中

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

有关完整的端点详情和请求/响应示例，请参阅 [references/api-endpoints.md]。