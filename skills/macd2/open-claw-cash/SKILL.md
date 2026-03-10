---
name: agentwalletapi
description: OpenclawCash 是一个专为 AI 代理设计的加密钱包 API。当代理需要发送原生货币或代币、查询余额、列出钱包，或通过 OpenclawCash 以编程方式与 EVM（以太坊虚拟机）和 Solana 钱包进行交互时，可以使用该 API。
license: Proprietary
compatibility: Requires network access to https://openclawcash.com
metadata:
  author: agentwalletapi
  version: "1.12.0"
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

该 API 用于与 OpenclawCash 管理的钱包交互，支持发送原生资产和代币、查询余额、执行去中心化交易所（DEX）交易，以及通过 Polygon 钱包管理 Polymarket 账户和订单。

## 必需条件

- 必需的环境变量：`AGENTWALLETAPI_KEY`
- 可选的环境变量：`AGENTWALLETAPI_URL`（默认值：`https://openclawcash.com`）
- 必需的本地二进制程序：`curl`
- 可选的本地二进制程序：`jq`（用于在命令行界面（CLI）中生成格式化的 JSON 输出）
- 需要网络访问：`https://openclawcash.com`

## 推荐的集成方式

- 如果客户端支持 MCP（OpenclawCash 的管理工具），请优先使用公共的 OpenclawCash MCP 服务器：
  ```bash
  npx -y @openclawcash/mcp-server
  ```
  - 使用 MCP 作为主要执行路径，因为相关工具、数据结构和结果都是为此设计的。
- 仅在 MCP 不可用或客户端无法连接 MCP 服务器时，才使用附带的 CLI 脚本作为备用方案。
- MCP 和 CLI 脚本都针对同一个 OpenclawCash 代理 API，它们是两种不同的访问方式，而非两个独立的产品。

## 安全模型

- 首先在测试网络上使用只读操作（`wallets`、`wallet`、`balance`、`tokens`）。
- 高风险操作需要额外的权限验证：
  - 通过仪表板设置 API 密钥权限（`allowWalletCreation`、`allowWalletImport`）
  - 对于写入操作，需要用户在 CLI 中明确确认（使用 `--yes` 参数）
- 代理应在会话开始时设置写入操作的审批模式：
  - `confirm_each_write`：在每次写入操作前请求用户确认。
  - `operate_on_my_behalf`：在用户首次明确授权后，后续的写入操作无需再次确认，只要用户在同一会话中继续发出指令即可。
- 对于 `operate_on_my_behalf` 模式，代理应将用户后续的指令视为执行命令，并使用 `--yes` 参数来执行相应的写入操作。
- 仅在以下情况下重新请求确认：
  - 用户撤销或更改了审批模式
  - 会话重启或内存丢失
  - 操作超出了用户允许的范围
  - 代理无法确定目标钱包、代币、金额、接收方或链路
- 如果用户只给出了模糊的指令（如“继续执行”），应先收集缺失的详细信息，而不是重复请求权限。

## 设置步骤

1. 运行设置脚本以创建 `.env` 文件：
   ```
   bash scripts/setup.sh
   ```
2. 在此技能文件夹中编辑 `.env` 文件，并将占位符替换为你的实际 API 密钥：
   ```
   AGENTWALLETAPI_KEY=occ_your_api_key
   ```
3. 在 https://openclawcash.com 获取 API 密钥（注册、创建钱包，然后进入 API 密钥页面）。

## 备用方案（CLI）

如果 MCP 不可用，可以使用附带的工具脚本直接进行 API 调用：
```bash
# Read-only (recommended first)
bash scripts/agentwalletapi.sh wallets
bash scripts/agentwalletapi.sh user-tag-get
bash scripts/agentwalletapi.sh user-tag-set my-agent-tag --yes
bash scripts/agentwalletapi.sh wallet Q7X2K9P
bash scripts/agentwalletapi.sh wallet "Trading Bot"
bash scripts/agentwalletapi.sh balance Q7X2K9P
bash scripts/agentwalletapi.sh transactions Q7X2K9P
bash scripts/agentwalletapi.sh tokens mainnet

# Write actions (require explicit --yes)
export WALLET_EXPORT_PASSPHRASE_OPS='your-strong-passphrase'
bash scripts/agentwalletapi.sh create "Ops Wallet" sepolia WALLET_EXPORT_PASSPHRASE_OPS --yes
bash scripts/agentwalletapi.sh import "Treasury Imported" mainnet --yes
bash scripts/agentwalletapi.sh import "Poly Ops" polygon-mainnet --yes
# Automation-safe import: read private key from stdin instead of command args
printf '%s' '<private_key>' | bash scripts/agentwalletapi.sh import "Treasury Imported" mainnet - --yes
bash scripts/agentwalletapi.sh transfer Q7X2K9P 0xRecipient 0.01 --yes
bash scripts/agentwalletapi.sh transfer Q7X2K9P 0xRecipient 100 USDC --yes
bash scripts/agentwalletapi.sh quote mainnet WETH USDC 10000000000000000
bash scripts/agentwalletapi.sh quote solana-mainnet SOL USDC 10000000 solana
bash scripts/agentwalletapi.sh swap Q7X2K9P WETH USDC 10000000000000000 0.5 --yes
# Checkout escrow lifecycle
bash scripts/agentwalletapi.sh checkout-payreq-create Q7X2K9P 30000000 --yes
bash scripts/agentwalletapi.sh checkout-payreq-get pr_a1b2c3
bash scripts/agentwalletapi.sh checkout-escrow-get es_d4e5f6
bash scripts/agentwalletapi.sh checkout-quick-pay es_d4e5f6 Q7X2K9P --yes
bash scripts/agentwalletapi.sh checkout-swap-and-pay-quote es_d4e5f6 Q7X2K9P
bash scripts/agentwalletapi.sh checkout-swap-and-pay-confirm es_d4e5f6 Q7X2K9P 1 --yes
bash scripts/agentwalletapi.sh checkout-release es_d4e5f6 --yes
bash scripts/agentwalletapi.sh checkout-refund es_d4e5f6 --yes
bash scripts/agentwalletapi.sh checkout-cancel es_d4e5f6 --yes
bash scripts/agentwalletapi.sh checkout-webhooks-list
# Polymarket setup is user-managed in dashboard Venues settings
# Direct setup page: https://openclawcash.com/venues/polymarket
bash scripts/agentwalletapi.sh polymarket-market Q7X2K9P 123456 BUY 25 FAK 0.65 --yes
bash scripts/agentwalletapi.sh polymarket-account Q7X2K9P
bash scripts/agentwalletapi.sh polymarket-orders Q7X2K9P OPEN 50
bash scripts/agentwalletapi.sh polymarket-activity Q7X2K9P 50
bash scripts/agentwalletapi.sh polymarket-positions Q7X2K9P 100
bash scripts/agentwalletapi.sh polymarket-cancel Q7X2K9P order_id_here --yes
```

### 基本单位规则（重要）

- `quote.amountIn`、`swap.amountIn`、`approve.amount` 和 `transfer.value` 必须是 **以基本单位表示的整数字符串**（仅包含数字）。
- **不要** 在这些字段中输入小数字符串（例如 `0.001`），否则验证会立即失败。
- 示例：
  - `0.001 ETH` -> `1000000000000000` wei
  - `1 USDC`（6 位小数） -> `1000000`
- 对于转账操作，如果需要人类可读的单位，可以使用 `amount`，让 API 进行转换。

### 输入安全

- 钱包导入是可选的，对于常规的钱包操作（列表、余额查询、转账、交易）不是必需的。
- 只有在用户通过仪表板设置明确启用 `allowWalletImport` API 密钥权限时，导入功能才会生效。
- 导入操作需要在 CLI 中明确确认（自动化时使用 `--yes`，或交互式提示 `YES`）。
- 尽量避免将敏感信息作为 CLI 参数传递（可能存在 shell 历史记录/进程日志风险）。
- 推荐的选项：
  - 交互式隐藏提示：省略私钥参数。
  - 自动化：使用 `-` 并通过标准输入（stdin）传递输入。

## 基本 URL

```
https://openclawcash.com
```

## 故障排除

如果请求因主机/URL 问题失败，请按照以下步骤进行排查：

1. 打开 `agentwalletapi/.env` 文件，确认 `AGENTWALLETAPI_KEY` 已设置且没有多余的空白字符。
2. 如果 API 主机错误或无法访问，请在同一 `.env` 文件中修改相关设置：
   ```
   AGENTWALLETAPI_URL=https://openclawcash.com
   ```
3. 先尝试一个简单的读取操作：
   ```bash
   bash scripts/agentwalletapi.sh wallets
   ```
4. 如果仍然失败，请报告具体的错误信息，并在尝试转账/交易操作之前停止操作。

## 认证

API 密钥从此技能文件夹中的 `.env` 文件中加载。对于直接的 HTTP 请求，需要将其作为请求头的一部分：

```
X-Agent-Key: occ_your_api_key
Content-Type: application/json
```

## API 接口

- **代理 API（需要 API 密钥进行认证）：** `/api/agent/*`
  - 使用 `X-Agent-Key` 进行认证
  - 用于自主执行代理操作（钱包列表/创建/导入、交易、余额查询、转账、交易报价、审批、结算托管流程以及 Polymarket 相关操作）
- 公开文档中仅包含 `/api/agent/*` 端点。

## 工作流程

1. `GET /api/agent/wallets` - 查找可用的钱包（ID、标签、地址、网络、链路）。可选参数 `?includeBalances=true` 可显示原生余额和代币信息。
2. `GET /api/agent/wallet?walletId=...` 或 `?walletLabel=...` 或 `?walletAddress=...` - 获取指定钱包的原生/代币余额信息。
3. 可选的钱包生命周期操作：
   - `POST /api/agent/wallets/create` - 在 API 密钥的权限控制下创建新钱包
   - `POST /api/agent/wallets/import` - 通过 API 密钥导入 mainnet、polygon-mainnet 或 solana-mainnet 钱包
4. `GET /api/agent/transactions?walletId=...`（或 `walletLabel`/`walletAddress`） - 查看钱包的交易历史记录（包括链上和应用程序记录的交易）
5. `GET /api/agent/supported-tokens?network=...` 或 `?chain=evm|solana` - 获取推荐的常见代币列表及相关信息（需要 `X-Agent-Key`）
6. `POST /api/agent/token-balance` - 查询钱包余额（包括原生代币和代币余额；支持按符号/地址查询）
7. `POST /api/agent/quote` - 在 Uniswap（EVM）或 Jupiter（Solana mainnet）上执行交易报价。
8. `POST /api/agent/swap` - 在 Uniswap（EVM）或 Jupiter（Solana mainnet）上执行代币交易。
9. `POST /api/agent/transfer` - 在钱包所在的链路上发送原生货币或代币（可选参数 `chain`）。
10. `GET /api/agent/user-tag` 和 `PUT /api/agent/user-tag` - 读取/设置全局结算用户标签（设置后不可更改）。
11. 可选的结算流程（通过全局用户标签进行托管）：
   - `POST /api/agent/checkout/payreq` - 创建结算请求并设置托管
   - `GET /api/agent/checkout/payreq/:id` - 查看结算请求详情
   - `POST /api/agent/checkout/escrows/:id/funding-confirm` - 通过交易哈希确认托管资金
   - `POST /api/agent/checkout/escrows/:id/quick-pay` - 直接从买家钱包支付托管资金
   - `POST /api/agent/checkout/escrows/:id/swap-and-pay` - 报价/执行交易并支付托管资金
   - `GET /api/agent/checkout/escrows/:id` - 查看托管状态
   - `POST /api/agent/checkout/escrows/:id/accept` - 作为买家接受托管
   - `POST /api/agent/checkout/escrows/:id/proof` - 提交买家证明
   - `POST /api/agent/checkout/escrows/:id/dispute` - 提起托管争议
   - `POST /api/agent/checkout/escrows/:id/release` - 释放托管资金
   - `POST /api/agent/checkout/escrows/:id/refund` - 退还托管资金
   - `POST /api/agent/checkout/escrows/:id/cancel` - 取消托管
   - `GET|POST /api/agent/checkout/webhooks` 和 `PATCH|DELETE /api/agent/checkout/webhooks/:id` - 管理结算通知
12. 可选的 Polymarket 操作（仅适用于 polygon-mainnet 钱包）：
   - 先决条件：用户在仪表板的 Venues 设置中配置了相应的钱包
   - `POST /api/agent/venues/polymarket/orders/limit` - 下单限价单
   - `POST /api/agent/venues/polymarket/orders/market` - 下单市价单
   - `GET /api/agent/venues/polymarket/account` - 查看账户概览
   - `GET /api/agent/venues/polymarket/orders` - 查看未完成的订单
   - `POST /api/agent/venues/polymarket/orders/cancel` - 取消订单
   - `GET /api/agent/venues/polymarket/activity` - 查看交易活动
   - `GET /api/agent/venues/polymarket/positions` - 查看未完成的订单（包括 PnL 信息）

## 代理的写入操作处理规则

对于写入操作，请遵循以下模式：

1. 在会话中的第一次写入操作时，询问用户一个简短的确认问题：
   - “您是否希望每次写入操作都获得您的确认，还是让我代表您执行？”
2. 将用户选择的模式存储在会话内存中。
3. 如果模式为 `confirm_each_write`：
   - 在每次转账、交易、审批或钱包创建操作前请求用户确认。
   - 确认后，使用 MCP 写入工具或 CLI 脚本（带 `--yes` 参数）执行操作。
4. 如果模式为 `operate_on_my_behalf`：
   - 之后无需再次请求确认。
   - 当用户后续发出如“将 100 USDC 从 wallet Q7X2K9P 转移到 0xabc...” 的指令时，使用 MCP 写入工具或 CLI 脚本（带 `--yes` 参数）执行操作。
5. 无论采用哪种模式：
   - 如果缺少执行细节，只需询问缺失的细节。
   - 如果用户更改了模式或撤销了权限，更新内存并遵循新的规则。

**推荐的引导语：**
- “请选择本次会话的写入操作模式：`confirm_each_write` 或 `operate_on_my_behalf`。”

**示例：**
- 用户选择：`operate_on_my_behalf`
- 用户后续指令：`将 100 USDC 从 wallet Q7X2K9P 转移到以太坊上的 0xabc...`
- 如果 MCP 可用，代理应直接调用相应的 MCP 写入工具。
- 如果 MCP 不可用，代理应执行以下操作：
  ```bash
  bash scripts/agentwalletapi.sh transfer Q7X2K9P 0xabc... 100 USDC evm --yes
  ```
- 除非用户撤销模式或指令不明确，否则代理在同一会话中不应再次请求转账权限。

## 快速参考

| 端点 | 方法 | 认证方式 | 功能 |
|---|---|---|---|
| `/api/agent/wallets` | GET | 是 | 列出钱包（包含原生余额，可选参数 `includeBalances=true`） |
| `/api/agent/wallet` | GET | 是 | 获取单个钱包的详细信息（包括原生/代币余额） |
| `/api/agent/wallets/create` | POST | 是 | 创建新的 API 密钥管理的钱包 |
| `/api/agent/wallets/import` | POST | 是 | 通过 API 密钥导入 mainnet/polygon-mainnet/solana-mainnet 钱包 |
| `/api/agent/transactions` | GET | 是 | 查看每个钱包的交易历史记录 |
| `/api/agent/transfer` | POST | 是 | 发送原生/代币转账（EVM 和 Solana） |
| `/api/agent/swap` | POST | 是 | 在 Uniswap（EVM）或 Jupiter（Solana mainnet）上执行交易 |
| `/api/agent/quote` | POST | 是 | 获取交易报价（Uniswap（EVM）或 Jupiter（Solana mainnet） |
| `/api/agent/token-balance` | POST | 是 | 查询余额 |
| `/api/agent/supported-tokens` | GET | 获取每个网络推荐的常见代币列表 |
| `/api/agent/user-tag` | GET | 查读 API 密钥所有者的全局结算用户标签 |
| `/api/agent/user-tag` | PUT | 设置全局结算用户标签（设置后不可更改） |
| `/api/agent/approve` | POST | 批准 ERC-20 代币的接收方（仅限 EVM） |
| `/api/agent/checkout/payreq` | POST | 创建结算请求并设置托管 |
| `/api/agent/checkout/payreq/:id` | GET | 查看结算请求详情 |
| `/api/agent/checkout/escrows/:id/funding-confirm` | POST | 确认托管资金交易 |
| `/api/agent/checkout/escrows/:id/quick-pay` | POST | 直接从买家钱包支付托管资金 |
| `/api/agent/checkout/escrows/:id/swap-and-pay` | POST | 报价/执行交易并支付托管资金 |
| `/api/agent/checkout/escrows/:id` | GET | 查看托管状态 |
| `/api/agent/checkout/escrows/:id/accept` | POST | 作为买家接受托管 |
| `/api/agent/checkout/escrows/:id/proof` | POST | 提交买家证明 |
| `/api/agent/checkout/escrows/:id/dispute` | POST | 提起托管争议 |
| `/api/agent/checkout/escrows/:id/release` | POST | 释放托管资金 |
| `/api/agent/checkout/escrows/:id/refund` | POST | 退还托管资金 |
| `/api/agent/checkout/escrows/:id/cancel` | POST | 取消托管 |
| `/api/agent/checkout/webhooks` | GET | 查看结算通知 |
| `/api/agent/checkout/webhooks` | POST | 创建结算通知 |
| `/api/agent/checkout/webhooks/:id` | PATCH | 更新结算通知 |
| `/api/agent/checkout/webhooks/:id` | DELETE | 删除结算通知 |
| `/api/agent/venues/polymarket/orders/limit` | POST | 下单限价单 |
| `/api/agent/venues/polymarket/orders/market` | POST | 下单市价单 |
| `/api/agent/venues/polymarket/account` | GET | 查看 Polymarket 账户概览 |
| `/api/agent/venues/polymarket/orders` | GET | 查看未完成的订单 |
| `/api/agent/venues/polymarket/orders/cancel` | POST | 取消订单 |
| `/api/agent/venues/polymarket/activity` | GET | 查看交易活动 |
| `/api/agent/venues/polymarket/positions` | GET | 查看未完成的订单（包括 PnL 信息） |

## 代理钱包的创建/导入操作（代理 API）

代理端的钱包生命周期相关端点：

- `POST /api/agent/wallets/create`
- `POST /api/agent/wallets/import`

**操作说明：**
- 两者都需要 `X-Agent-Key`。
- 两者都受仪表板中配置的 API 密钥权限的限制：
  - `allowWalletCreation` 用于创建钱包
  - `allowWalletImport` 用于导入钱包
- 两者都受到 API 密钥使用次数的限制。超出限制会返回错误代码 `429`，并提示用户 `Retry-After`。
- 代理导入支持 `mainnet`、`polygon-mainnet` 和 `solana-mainnet` 钱包。
- 创建钱包时需要提供：
  - `exportPassphrase`（至少 12 个字符）
  - `exportPassphraseStorageType`
  - `exportPassphraseStorageRef`
  - `confirmExportPassphraseSaved: true`
- 安全的创建流程：
  - 首先将导出的密码保存到安全存储中。
  - 建议本地代理使用环境变量支持的存储方式。
  - 记录存储位置。
  - 然后使用以下参数调用 `POST /api/agent/wallets/create`：
    - 密码
    - `exportPassphraseStorageType`
    - `exportPassphraseStorageRef`
    - `confirmExportPassphraseSaved: true`
- 对于 MCP 和 CLI 脚本，使用环境变量支持的存储方式是最安全的，因为本地工具可以在创建钱包之前验证环境变量的存在。

## Polymarket 操作（代理 API）

- Polymarket 操作仅适用于 `polygon-mainnet` 上的 EVM 钱包。
- 设置需要在仪表板的 Venues 设置中进行配置（代理端的设置功能被禁用）。
- 下单操作如下：
  - `POST /api/agent/venues/polymarket/orders/limit`：输入 `tokenId`、`side`、`price`、`size`
  - `POST /api/agent/venues/polymarket/orders/market`：输入 `tokenId`、`side`、`amount`、可选参数 `orderType` 和 `worstPrice`
- 查看和更新操作相关端点：
  - `GET /api/agent/venues/polymarket/account`
  - `GET /api/agent/venues/polymarket/orders`
  - `POST /api/agent/venues/polymarket/orders/cancel`：输入 `orderId`
  - `GET /api/agent/venues/polymarket/activity`
  - `GET /api/agent/venues/polymarket/positions`：获取未完成的订单信息（包括 PnL 信息）
- 位置信息来自 Polymarket，并且仅显示未完成的订单。
- 位置信息包括 `cashPnl`、`percentPnl` 和 `currentValue`（如果上游字段缺失，会使用默认值）。
- 在执行订单前，系统会进行钱包策略的检查。

## 转账示例

- 如果未指定代币，默认使用原生货币进行转账：
   ```json
{ "walletId": "Q7X2K9P", "to": "0xRecipient...", "amount": "0.01" }
```

- 按代币符号发送 100 USDC：
   ```json
{ "walletLabel": "Trading Bot", "to": "0xRecipient...", "token": "USDC", "amount": "100" }
```

- 按合约地址发送 ERC-20 代币：
   ```json
{ "walletId": "Q7X2K9P", "to": "0xRecipient...", "token": "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48", "amount": "100" }
```

- 按代币符号发送 SOL：
   ```json
{ "walletId": "Q7X2K9P", "to": "SolanaRecipientWalletAddress...", "token": "SOL", "amount": "0.01" }
```

- 按 Solana 的要求发送 SOL 代币（需要提供备注）：
   ```json
{ "walletId": "Q7X2K9P", "to": "SolanaRecipientWalletAddress...", "token": "SOL", "amount": "0.01", "memo": "payment verification note" }
```

- 使用 `amount` 表示人类可读的金额（例如，“100” 表示 100 USDC）。使用 `value` 表示基本单位（每个链路的最低单位）。
- 在代理请求中可以使用 `chain: "evm" | "solana"` 来指定链路并进行验证。
- Solana 的转账操作支持备注字段（最多 5 个单词，256 字节 UTF-8 编码，不允许特殊字符）。
- 原生货币转账（EVM 和 Solana）会预先扣除平台费和网络费；Solana 的转账可能还需要额外的初始资金。
- 转账响应中会包含 `requestedValue`、`adjustedValue`、`requestedAmount` 和 `adjustedAmount`。

## 代币支持模型

- `GET /api/agent/supported-tokens`：返回推荐的常见代币列表及相关信息。
- EVM 转账/交易/余额接口支持任何有效的 ERC-20 代币合约地址。
- Solana 转账/余额接口支持任何有效的 SPL 发行地址。
- 在 EVM 上，原生代币显示为 `ETH`；在 Solana 上显示为 `SOL`（余额字段中包含特定链路的代币 ID）。

## 错误代码

- 200：成功
- 400：输入无效、资金不足、代币未知或违反政策
- 400 `chain_mismatch`：请求的链路与选定的钱包不匹配
- 400 `amount_below_min_transfer`：请求的转账金额低于平台费和网络费后的最低可转移金额
- 400 `insufficient_balance`：请求的转账金额加上费用超过了可用余额
- 401：API 密钥缺失/无效
- 404：钱包未找到
- 500：内部错误（请使用正确的参数或减少金额重试）

## 政策限制

钱包可能有以下治理规则：
- **白名单**：仅允许向预先批准的地址转账
- **消费限额**：每笔交易的最大金额（根据钱包设置）

违反规则时会返回 HTTP 401 错误，并附带错误信息。

## 重要提示

- 所有 POST 请求都需要设置 `Content-Type: application/json`。
- EVM 代币转账需要钱包中有 ETH 作为交易费用
- Solana 代币转账需要钱包中有 SOL 作为费用
- Solana 的转账备注是可选的，且仅适用于 Solana：最多 5 个单词，256 字节 UTF-8 编码，不允许特殊字符
- Solana 的原生转账会预先扣除平台费；如果请求的金额过低，可能会返回错误 `400 amount_below_min_transfer`
- 如果请求的金额加上平台费和网络费超过了钱包余额，API 会返回错误 `400 insufficient_balance`
- 支持在 EVM（Uniswap）和 Solana mainnet（Jupiter）上进行交易；报价功能仅支持 EVM
- 平台费用默认为 1%
- 为简化操作，可以使用 `amount`；如需精确控制基本单位，可以使用 `value`
- 为了确保代理操作的稳定性：
  - 先调用 `wallets`，然后 `wallet`（或 `token-balance`），接着 `quote`，最后 `swap`。
- 如果遇到错误代码 `400 insufficient_token_balance`，请减少金额或更换代币。
- 此技能文件夹中的 `.env` 文件存储了你的 API 密钥——切勿将其提交到版本控制系统中。

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

有关完整的端点详情和请求/响应示例，请参考 [references/api-endpoints.md]。