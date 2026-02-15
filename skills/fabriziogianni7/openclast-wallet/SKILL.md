---
name: openclast-wallet
description: 本指南用于指导用户如何使用 Openclast/Openclaw 钱包，包括钱包的设置、余额查询、交易处理、审批流程以及安全规则。适用于用户咨询与钱包相关的问题，如钱包设置、余额查询、交易操作、审批流程或密钥导出等。

---

# Openclast 钱包代理指南

## 快速入门

- 使用命令行工具（CLI）进行初始化：
  - `openclast-wallet setup` 会在当前文件夹中创建 `wallet-config.json` 文件。
  - `openclast-wallet setup --config ./wallet-config.json` 会根据该文件初始化钱包。
- 建议将 `wallet-config.json` 文件放在项目根目录中，并在使用前自定义相关设置（如链路和交易限额）。
- 确保 `wallet-config.json` 与 `openclaw.json` 分开存放（`openclaw.json` 的配置文件不支持包含 `wallets` 键）。

## 批准流程（必填）

所有发送、批准或执行合约的操作都会生成一个待处理的交易（pending transaction），需要用户明确批准。

操作步骤如下：
1. 创建待处理的交易（无论是发送交易、ERC20 转移还是执行合约）。
2. 请求用户进行批准。
3. 只有在获得批准后，才能将交易广播并确认。

如果用户仅要求“直接发送”，除非配置设置为自动模式，否则仍需经过批准。

## 密钥导出警告（必填）

默认情况下，严禁暴露私钥。如果用户请求导出密钥：
- 必须获得用户的明确确认。
- 提醒用户密钥导出存在风险，应加以保护。
- 如果系统支持环境变量配置（例如 `MOLTBOT_ALLOW_WALLET_EXPORT=1`），请使用这些变量，并通过 CLI 获得用户的明确确认。
- 如果当前系统不支持密钥导出，请告知用户并提供更安全的替代方案。

## 常见操作

### 查看余额和代币
- 使用用户指定的链路 ID（chainId）进行操作。
- 如果某条链路未在配置中设置，仍可以通过通用的公开 RPC 接口查询只读余额。

### 发送交易
- 验证链路 ID 和接收地址是否正确。
- 遵守配置中规定的单次交易限额和每日交易限额。
- 交易确认后，务必提供区块浏览器链接。

### 链路名称与链路 ID 的对应关系
- Ethereum / Mainnet: `1`
- Sepolia: `11155111`
- Polygon: `137`
- Base: `8453`
- Arbitrum One: `42161`

当用户请求“查看 Sepolia 上的余额”或“在 Ethereum 上发送交易”时，请根据上述映射关系确定正确的链路 ID 并执行操作。

## 安全默认设置

- 默认模式下，系统会提示用户进行确认而非自动发送交易。
- 尽量限制与未经验证的合约的交易。
- 私钥应仅存储在操作系统的密钥链中（macOS 系统），切勿将其保存在配置文件中。

## 配置规则（如配置文件存在则适用）

- `walletsdefaults.spending.mode`: `"notify"`（默认值）或 `"auto"`（无需批准即可发送交易）。
- `walletsdefaults.spending.limitPerTx`、`dailyLimit`、`allowedChains`、`allowedRecipients`、`notifyChannels`：这些配置会应用于所有发送交易、ERC20 转移和执行合约的操作。
- `wallets.notify.primaryChannel`：指定待批准交易的通知渠道。
- `wallets.interactWithUnverifiedContracts`：如果设置为 `false`，则仅允许与经过验证的地址和合约进行交互。

## 区块浏览器链接（必填）

交易批准并广播后，务必提供相应的链接：
- 交易链接：`/tx/<txHash>`
- 地址链接：`/address/<address>`
- 区块浏览器链接的格式为 `wallets.chains.<chainId>.blockExplorerUrl`（如果已配置），否则使用通用的区块浏览器。

## 代理工具推荐

如果系统提供了相应的工具，建议使用以下工具：
- `wallet_send`、`wallet_balance`、`wallet_txStatus`、`wallet_approve`
- `wallet_erc20_approve`、`wallet_erc20_transfer`、`wallet_contract_call`

如果系统使用的是自定义的 CLI 工具，请使用系统的钱包 CLI 来执行创建地址、发送交易、批准交易以及恢复/导入密钥等操作。

## 相关文件和命令行工具

- 初始配置文件：`wallet-config.json`
- 在项目中安装该工具：`openclast-wallet install-skill`