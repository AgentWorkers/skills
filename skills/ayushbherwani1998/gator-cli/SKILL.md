---
name: gator-cli
description: >
  **使用说明：**  
  当您需要使用 `@metamask/gator-cli` 来初始化账户配置、将账户权限（EOA, External Owned Account）升级为 EIP-7702 标准、授予或赎回 ERC-7710 类型的委托权限、以及查询账户余额和委托状态时，请参考本文档。本文档涵盖了相关命令、必需的参数（flags）、权限授予的范围、赎回操作类型、配置文件的存放位置以及常见的使用流程。
metadata:
  openclaw:
    emoji: "🐊"
    homepage: "https://docs.metamask.io/smart-accounts-kit"
    requires:
      bins: ["gator"]
    install:
      - id: "node"
        kind: "node"
        package: "@metamask/gator-cli"
        bins: ["gator"]
        label: "Install gator CLI"
---
## 快速参考

使用此技能可以从仓库中运行 `gator` CLI，并选择正确的命令/参数来执行委托工作流程。

## 安装

```sh
npm install -g @metamask/gator-cli
```

## CLI 概述

- 可执行文件名：`gator`
- 默认配置文件：`default`
- 配置文件路径：`~/.gator-cli/permissions.json`（或 `~/.gator-cli/profiles/<profile-name>.json`）
- 当未配置存储时，委托操作的本地缓存文件为：`~/.gator-cli/delegations/<profile-name>.json`

## 配置要求

在运行 `gator init` 之后，请编辑配置文件：

```json
{
  "delegationStorage": {
    "apiKey": "your-api-key",
    "apiKeyId": "your-api-key-id"
  },
  "rpcUrl": "https://your-rpc-url.com"
}
```

- `delegationStorage` 是可选参数；如果未设置，则委托操作将存储在本地。
- `rpcUrl` 是执行链上操作所必需的参数。

## 命令

### init

生成私钥并保存配置文件。如果配置文件已存在，则会报错。

- `gator init [--chain <chain>] [--profile <profile-name>]`
- `--chain` 可选值：`base`（默认值）、`baseSepolia`、`sepolia`
- `--profile` 默认值为 `default`
- 输出：地址、链名以及配置文件的路径。

### create

将一个 EOA（Externally Owned Account）升级为 EIP-7702 智能合约账户。使用配置文件中指定的链名。

- `gator create [--profile <profile-name>]`
- 需要确保账户已充值了相应的原生代币。
- 输出：账户地址、链名以及升级交易的哈希值。

### show

显示指定配置文件的 EOA 地址。

- `gator show [--profile <profile-name>]`

### status

检查配置文件以及链上账户的状态。

- `gator status [--profile <profile-name>]`
- 输出：账户地址、链名、配置文件升级状态、链上代码的存在情况、存储地址以及 RPC URL。

### balance

显示账户的原生代币余额以及可选的 ERC-20 代币余额。

- `gator balance [--tokenAddress <address>] [--profile <profile-name>]`
- 如果提供了 `--tokenAddress`，则还会显示 ERC-20 代币余额及其对应的十进制单位。

### grant

创建、签署并存储具有预定义范围的委托操作。

- `gator grant --to <to-address> --scope <type> [scope flags] [--profile <profile-name>]`

**委托范围相关参数：**
- **代币委托**：`--tokenAddress <token-address>`, `--maxAmount <amount>`, `--tokenId <id>`
- **周期性委托**：`--periodAmount <amount>`, `--periodDuration <seconds>`, `--startDate <timestamp>`
- **流式委托**：`--amountPerSecond <amount>`, `--initialAmount <amount>`, `--startTime <timestamp>`
- **函数调用委托**：`--targets <addresses>`, `--selectors <sigs>`, `--valueLte <ether>`
- **所有权转让委托**：`--contractAddress <contract-address>`

**支持的委托类型：**
- `erc20TransferAmount`
- `erc20PeriodTransfer`
- `erc721Transfer`
- `nativeTokenTransferAmount`
- `nativeTokenPeriodTransfer`
- `nativeTokenStreaming`
- `functionCall`
- `ownershipTransfer`

**每个委托类型对应的可选参数：**
| 委托类型 | 必需参数 | 可选参数 |
| --------- | -------- | -------- |
| erc20TransferAmount | `--tokenAddress`, `--maxAmount` |         |
| erc20PeriodTransfer | `--tokenAddress`, `--periodAmount`, `--periodDuration` |         |
| erc20Streaming | `--tokenAddress`, `--amountPerSecond`, `--initialAmount`, `--startTime` |         |
| erc721Transfer | `--tokenAddress`, `--tokenId`       |         |
| nativeTokenTransferAmount | `--maxAmount`         |         |
| nativeTokenPeriodTransfer | `--periodAmount`, `--periodDuration` |         |         |
| nativeTokenStreaming | `--amountPerSecond`, `--initialAmount`, `--startTime` |         |
| functionCall   | `--targets`, `--selectors`      | `--valueLte`    |
| ownershipTransfer | `--contractAddress`     |         |

- 如果省略 `--startDate` 和 `--startTime`，则默认使用当前时间（以秒为单位）。
- `--valueLte` 用于设置 `functionCall` 类型委托的最大代币价值。

### redeem

使用指定的操作类型赎回已存储的委托操作。

- `gator redeem --from <from-address> --action <type> [action flags] [--profile <profile-name>]`

**支持的操作类型：** `erc20Transfer`, `erc721Transfer`, `nativeTransfer`, `functionCall`, `ownershipTransfer`, `raw`

**操作类型相关的参数：**
- `erc20Transfer`：`--tokenAddress`, `--to`, `--amount`
- `erc721Transfer`：`--tokenAddress`, `--to`, `--tokenId`
- `nativeTransfer`：`--to`, `--amount`
- `functionCall`：`--target`, `--function`, `--args`, `--value`
- `ownershipTransfer`：`--contractAddress`, `--to`
- `raw`：`--target`, `--callData`, `--value`

### revoke

在链上撤销委托操作。系统会撤销第一个匹配的委托。

- `gator revoke --to <to-address> [--profile <profile-name>]`

### inspect

检查您账户的委托操作记录。

- `gator inspect [--from <from-address>] [--to <to-address>] [--profile <profile-name>]`
- 如果不指定筛选条件，会显示所有委托的详细信息（包括“给予方”和“接收方”）。
- 输出字段包括：给予方地址、接收方地址、授权信息以及委托操作的详细信息。

## 操作说明

- **私钥安全提示**：当前版本仍处于测试阶段（alpha 阶段），私钥以明文 JSON 格式存储。请勿在涉及大量资金的账户中使用此工具。
- `--from` 表示委托方地址；`--to` 表示接收方地址。
- `--targets` 和 `--selectors` 以逗号分隔的列表形式提供。
- `--function` 参数接受人类可读的 Solidity 函数签名（例如 `"approve(address,uint256)"`）。**不要** 直接传递 4 字节的函数签名（例如 `0x095ea7b3`）——CLI 会自动从签名中生成正确的函数签名。
- `--startDate` 和 `--startTime` 接受以秒为单位的 Unix 时间戳；如果省略，系统会使用当前时间。
- `redeem` 操作必须指定操作类型（`erc20Transfer`、`erc721Transfer`、`nativeTransfer`、`functionCall`、`ownershipTransfer`、`raw`）。

## 示例操作流程

- 初始化并升级账户：```bash
gator init --profile <profile-name>
gator create --profile <profile-name>
```
- 授予 ERC-20 代币委托：```bash
gator grant --profile <profile-name> --to <to-address> --scope erc20TransferAmount \
  --tokenAddress <token-address> --maxAmount 50
```
- 赎回 ERC-20 代币：```bash
gator redeem --profile <profile-name> --from <from-address> --action erc20Transfer \
  --tokenAddress <token-address> --to <to-address> --amount 10
```
- 赎回原生代币：```bash
gator redeem --profile <profile-name> --from <from-address> --action nativeTransfer \
  --to <to-address> --amount 0.5
```
- 以原始数据格式赎回委托：```bash
gator redeem --profile <profile-name> --from <from-address> --action raw \
  --target <contract-address> --callData 0xa9059cbb...
```
- 检查委托记录：```bash
gator inspect --profile <profile-name>
gator inspect --profile <profile-name> --from <from-address>
gator inspect --profile <profile-name> --to <to-address>
```
- 撤销委托：```bash
gator revoke --profile <profile-name> --to <to-address>
```

## 运营注意事项

- **私钥安全**：由于当前版本仍处于测试阶段，私钥以明文形式存储在 JSON 文件中。请勿在涉及重要资金的账户中使用此工具。
- `--from` 参数表示委托方地址；`--to` 参数表示接收方地址。
- `--targets` 和 `--selectors` 参数以逗号分隔的列表形式提供。
- `--function` 参数接受人类可读的 Solidity 函数签名（例如 `"approve(address,uint256)"`）。**不要** 直接传递 4 字节的函数签名。
- `--startDate` 和 `--startTime` 参数接受以秒为单位的 Unix 时间戳；如果省略，系统会使用当前时间。
- `redeem` 操作必须指定操作类型（`erc20Transfer`、`erc721Transfer`、`nativeTransfer`、`functionCall`、`ownershipTransfer`、`raw`）。

---

（注：由于文档内容较长，部分代码块（如 ````sh
npm install -g @metamask/gator-cli
```` 等）在翻译时被省略以保持简洁性。实际使用中，请根据需要补充完整的代码内容。）