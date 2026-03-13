---
name: chainai
description: '以太坊与EVM区块链命令行工具（CLI）技能：签署消息、发送代币、通过1inch Fusion进行交易兑换、查询账户余额、广播交易，以及管理以太坊和BNB Smart Chain上的钱包。'
metadata:
  author: kvhnuke
  version: 0.0.10
  openclaw:
    requires:
      env:
        - CHAINAI_PRIVATE_KEY
      bins:
        - npx
        - node
    primaryEnv: CHAINAI_PRIVATE_KEY
    emoji: '⧫'
    homepage: https://github.com/kvhnuke/chainai
    install:
      - kind: node
        package: chainai
        bins: [chainai]
---
# chainai — 以太坊交易工具

> **⚠️ 免责声明 — 请自行承担风险**
>
> 本工具会与真实的区块链网络和资金进行交互。作者对因使用本工具而导致的任何资金损失、损害或意外后果概不负责。使用本工具即表示您完全承担所有操作的风险。

> **🔒 所有代理的强制性安全要求**
>
> 代理必须采取一切可能的措施来保护 `CHAINAI_PRIVATE_KEY` 及其他私钥的安全，防止其泄露。具体要求如下：
>
> 1. **严禁在任何面向用户的输出、日志、聊天消息或调试痕迹中记录、打印、显示私钥**。
> 2. **严禁将私钥存储在未经过加密且无访问控制的纯文本文件、版本控制系统中，或任何持久性存储中**。
> 3. **严禁通过未加密的渠道传输私钥，也不得将其包含在 URL、查询参数或发送给第三方服务的请求体中**。
> 4. **严禁在错误信息、堆栈跟踪或诊断输出中显示私钥**。
> 5. **始终优先使用 `CHAINAI_PRIVATE_KEY` 环境变量**，以减少私钥在 shell 历史记录和进程列表中的暴露风险。
> 6. **始终将私钥视为最高敏感度的机密信息**。私钥泄露将导致对相关钱包中所有资金的完全、不可撤销的控制权。

> **地址格式规则**
>
> 1. 在向任何命令传递地址时（钱包地址、代币合约地址、接收地址等），必须使用 ERC-55 校验和地址。
> 2. 如果不知道正确的校验和，请使用全小写的地址（例如 `0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2`），而不要猜测混合大小写的校验和。
> 3. **切勿猜测代币合约地址**。如果您不确定正确的代币合约地址，请务必询问用户提供。切勿伪造或假设代币地址。

> **� 在开始之前**
>
> 1. **验证您的私钥是否已设置**：运行 `npx chainai@0.0.10 who-am-i`，确认 `CHAINAI_PRIVATE_KEY` 已正确配置并能解析为预期的地址，然后再执行其他命令。
> 2. **没有私钥？** 使用 `npx chainai@0.0.10 gen-wallet` 生成一个新的钱包。请安全保存返回的私钥（例如作为环境变量）——该私钥将不再显示。
> 3. **充值您的账户**：在使用 `send`、`swap` 或任何交易提交命令之前，您必须向钱包地址充值所需的资金（包括用于 gas 的原生代币以及您打算发送或交换的代币）。如果账户余额不足，命令将失败。

## 概述

`chainai` 是一个非交互式的命令行工具，用于以太坊和兼容 EVM 的区块链操作。它支持签名、发送交易、广播交易、代币交换（1inch Fusion）、查询余额和生成钱包等功能。

## 调用方式

```
npx chainai@0.0.10 <command> [options]
```

- **运行时环境**：Node.js（版本 >= 18）
- **非交互式**：所有参数都必须以参数或标志的形式传递。系统不会提示用户输入。

## 认证

大多数命令接受私钥作为输入：
- 使用 `-k, --private-key <key>` 标志（以 `0x` 开头的十六进制字符串）
- `CHAINAI_PRIVATE_KEY` 环境变量（当未提供 `-k` 时作为备用）

## 支持的网络

| 名称            | 链路 ID | 别名                        | 原生代币            |
| --------------- | -------- | ---------------------------- | ------------------- |
| 以太坊        | 1        | `mainnet`, `ethereum`, `eth`       | ETH              |
| BNB 智能链     | 56       | `bsc`, `binance`, `bnb`      | BNB              |

使用 `-n, --network` 标志按名称、别名或链路 ID 指定网络。默认值为 `mainnet`。

## 退出代码

| 代码 | 含义                                      |
| ---- | -------------------------------------- |
| `0`  | 操作成功完成。                                |
| `1`  | 操作失败。请查看 `stderr` 以获取详细的错误信息。         |

## 消息合约

### 成功（标准输出）

```
CHAINAI_OK: <description>
{ ... }
```

### 错误（标准错误输出）

```
CHAINAI_ERR: <ERROR_CODE> — <description>
```

| 错误代码         | 描述                                      | 代理应采取的措施                                      |
| ------------------ | ------------------------------------------------ | ---------------------------------------- |
| `INVALID_INPUT`    | 输入格式不正确或缺少必要字段。                         | 重新验证输入参数并重试。                         |
| `EXECUTION_FAILED` | 操作无法完成。错误信息中包含失败原因。                   | 检查错误信息并调整操作方式。                         |
| `TIMEOUT`          | 操作超时。                                   | 增加超时时间或简化请求。                         |
| `UNKNOWN`          | 发生未知错误。                                   | 请报告给协调者以便手动处理。                         |

## 重试策略

对于 `TIMEOUT` 和 `EXECUTION_FAILED` 错误，最多尝试 2 次，并采用指数级退避策略，然后再进行升级。

---

## 命令列表

### `gen-wallet`

生成一个新的随机钱包（包括私钥和地址）。

```bash
npx chainai@0.0.10 gen-wallet
```

**选项**：无。

**输出（标准输出）**：

```json
{
  "address": "0x...",
  "privateKey": "0x..."
}
```

使用说明会打印到 `stderr`。

---

### `who-am-i`

根据私钥返回对应的以太坊地址。

```bash
npx chainai@0.0.10 who-am-i -k 0xKEY
# or
CHAINAI_PRIVATE_KEY=0xKEY npx chainai@0.0.10 who-am-i
```

**选项**：

| 标志                | 是否必需 | 描述                                              |
| ------------------------- | ----------------------------- | -------------------------------------- |
| `-k, --private-key <key>` | 否               | 使用指定的私钥。否则使用 `CHAINAI_PRIVATE_KEY`。           |

**输出（标准输出）**：

```json
{
  "address": "0x..."
}
```

---

### `sign-message`

使用 EIP-191 签名机制对消息进行签名。

```bash
npx chainai@0.0.10 sign-message -k 0xKEY -m "Hello World"
npx chainai@0.0.10 sign-message -k 0xKEY -m 0x68656c6c6f --raw
```

**选项**：

| 标志                | 是否必需 | 描述                                              |
| ------------------------- | ----------------------------- | -------------------------------------- |
| `-k, --private-key <key>` | 否               | 使用指定的私钥。否则使用 `CHAINAI_PRIVATE_KEY`。           |
| `-m, --message <message>` | 是               | 需要签名的消息。                                   |
| `-r, --raw`            | 否               | 将消息视为原始十六进制数据（以 `0x` 开头）。                   |

**输出（标准输出）**：

```json
{
  "address": "0x...",
  "message": "<original message>",
  "signature": "0x..."
}
```

---

### `sign`

> **⚠️ 严重安全警告**：直接对原始哈希值（secp256k1）进行签名，可能会导致任何链上操作的授权。**除非确实需要原始哈希签名，否则请使用 `sign-message`。** 在使用前，请确认哈希值的合法性，并确认没有更安全的替代方法。

```bash
npx chainai@0.0.10 sign -k 0xKEY -h 0xHASH
```

**选项**：

| 标志                | 是否必需 | 描述                                              |
| ------------------------- | ----------------------------- | -------------------------------------- |
| `-k, --private-key <key>` | 否               | 使用指定的私钥。否则使用 `CHAINAI_PRIVATE_KEY`。           |
| `-h, --hash <hash>`       | 是               | 需要签名的哈希值（以 `0x` 开头的十六进制字符串）。           |

**输出（标准输出）**：

```json
{
  "address": "0x...",
  "hash": "0x...",
  "signature": "0x..."
}
```

---

### `sign-typed-data`

对 EIP-712 格式的数据进行签名。

```bash
npx chainai@0.0.10 sign-typed-data -k 0xKEY -d '<json>'
```

**选项**：

| 标志                | 是否必需 | 描述                                              |
| ------------------------- | ----------------------------- | -------------------------------------- |
| `-k, --private-key <key>` | 否               | 使用指定的私钥。否则使用 `CHAINAI_PRIVATE_KEY`。           |
| `-d, --data <json>`       | 是               | EIP-712 格式的数据（格式为 JSON，包含 `domain`, `types`, `primaryType`, `message`）。 |

**数据格式**：

```json
{
  "domain": {
    "name": "AppName",
    "version": "1",
    "chainId": 1,
    "verifyingContract": "0x..."
  },
  "types": { "TypeName": [{ "name": "fieldName", "type": "fieldType" }] },
  "primaryType": "TypeName",
  "message": { "fieldName": "value" }
}
```

**输出（标准输出）**：

```json
{
  "address": "0x...",
  "signature": "0x..."
}
```

---

### `sign-transaction`

签名交易（支持 legacy、EIP-2930 和 EIP-1559 格式）。返回已签名的交易序列化版本，可直接广播。

```bash
npx chainai@0.0.10 sign-transaction -k 0xKEY -t '<json>'
```

**选项**：

| 标志                | 是否必需 | 描述                                              |
| ------------------------- | ----------------------------- | -------------------------------------- |
| `-k, --private-key <key>` | 否               | 使用指定的私钥。否则使用 `CHAINAI_PRIVATE_KEY`。           |
| `-t, --transaction <json>` | 是               | 交易对象（格式为 JSON 字符串）。                         |

**交易格式**：

- Legacy 格式：

```json
{
  "to": "0x...",
  "value": "1000000000000000000",
  "gasPrice": "20000000000",
  "gas": "21000",
  "nonce": 0,
  "chainId": 1
}
```

- EIP-1559 格式：

```json
{
  "to": "0x...",
  "value": "1000000000000000000",
  "maxFeePerGas": "30000000000",
  "maxPriorityFeePerGas": "1000000000",
  "gas": "21000",
  "nonce": 0,
  "chainId": 1
}
```

省略 `-to` 参数即可部署合约。数值可以是字符串或数字。

**输出（标准输出）**：

```json
{
  "address": "0x...",
  "serializedTransaction": "0x..."
}
```

---

### `get-balance`

查询原生代币或 ERC-20 代币的余额。

```bash
npx chainai@0.0.10 get-balance -a 0xADDRESS
npx chainai@0.0.10 get-balance -a 0xADDRESS -n bsc
npx chainai@0.0.10 get-balance -a 0xADDRESS -t 0xTOKEN_CONTRACT
npx chainai@0.0.10 get-balance -a 0xADDRESS --all
```

**选项**：

| 标志                | 是否必需 | 描述                                              |
| ------------------------- | ----------------------------- | -------------------------------------- |
| `-a, --address <address>` | 否               | 使用 `CHAINAI_PRIVATE_KEY` 导出的地址。                   |
| `-n, --network <network>` | 否               | 网络（默认：`mainnet`）。                         |
| `-t, --token <token>`     | 否               | 代币合约地址（默认：`0xeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee`）。         |
| `--all`               | 是               | 返回所有代币的余额（包括原生代币和 ERC-20 代币）。忽略 `-t` 参数。         |

**输出（标准输出）**：返回单个代币的余额。

---

### `send`

构建并签名交易，以发送原生代币或 ERC-20 代币。系统会自动从网络获取随机数（nonce）、gas 费用等信息。

```bash
npx chainai@0.0.10 send -k 0xKEY --to 0xRECIPIENT --amount 1.5 -t 0xeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee
npx chainai@0.0.10 send -k 0xKEY --to 0xRECIPIENT --amount 100 -t 0xTOKEN_CONTRACT -n bsc
```

**选项**：

| 标志                | 是否必需 | 描述                                              |
| ------------------------- | ----------------------------- | -------------------------------------- |
| `-k, --private-key <key>` | 否               | 使用指定的私钥。否则使用 `CHAINAI_PRIVATE_KEY`。           |
| `--to <address>`          | 是               | 收件人地址。                                         |
| `-t, --token <token>`     | 是               | 代币合约地址（原生代币使用 `0xeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee`）。         |
| `-amount <amount>`       | 是               | 交易金额（以人类可读单位表示，例如 `"1.5"`）。                   |
| `-n, --network <network>` | 否               | 网络（默认：`mainnet`）。                         |
| `-b, --broadcast`         | 否               | 签名完成后自动广播交易。                         |

**输出（标准输出）**：

```json
{
  "from": "0x...",
  "to": "0x...",
  "token": "0xeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee",
  "amount": "1.5",
  "network": "Ethereum",
  "serializedTransaction": "0x..."
}
```

---

### `broadcast`

将已签名的交易序列化版本广播到网络。

```bash
npx chainai@0.0.10 broadcast -s 0xSERIALIZED_TX
npx chainai@0.0.10 broadcast -s 0xSERIALIZED_TX -n bsc
```

**选项**：

| 标志                | 是否必需 | 描述                                              |
| ------------------------------------ | ----------------------------- | -------------------------------------- |
| `-s, --serialized-transaction <hex>` | 是               | 已签名的交易序列化版本（以 `0x` 开头）。                 |
| `-n, --network <network>`         | 否               | 网络（默认：`mainnet`）。                         |

**输出（标准输出）**：

```json
{
  "transactionHash": "0x...",
  "network": "Ethereum",
  "explorerUrl": "https://etherscan.io/tx/0x..."
}
```

---

### `tx-status`

根据哈希值查询交易的状态。

```bash
npx chainai@0.0.10 tx-status -h 0xTX_HASH
npx chainai@0.0.10 tx-status -h 0xTX_HASH -n bsc
```

**选项**：

| 标志                | 是否必需 | 描述                                              |
| ------------------------- | ----------------------------- | -------------------------------------- |
| `-h, --hash <hash>`       | 是               | 交易哈希值（以 `0x` 开头，长度为 32 字节）。                   |
| `-n, --network <network>` | 否               | 网络（默认：`mainnet`）。                         |

**输出（标准输出）**：

--- 

对于待处理的交易，`status` 为 `"pending"`，`blockNumber`、`from`、`to`、`gasUsed` 和 `effectiveGasPrice` 均为 `null`。

---

### `swap`

通过 1inch Fusion 进行代币交换。首先获取报价，然后可以选择是否立即提交订单。使用 `-y` 可跳过确认步骤并立即提交。

```bash
npx chainai@0.0.10 swap -k 0xKEY --from-token 0xFROM --to-token 0xTO --amount 1.5
npx chainai@0.0.10 swap -k 0xKEY --from-token 0xFROM --to-token 0xTO --amount 1.5 -y
npx chainai@0.0.10 swap -k 0xKEY --from-token 0xFROM --to-token 0xTO --amount 0.5 -n bsc
```

使用 `0xeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee` 代表原生代币。

**选项**：

| 标志                | 是否必需 | 描述                                              |
| ------------------------- | ----------------------------- | -------------------------------------- |
| `-k, --private-key <key>` | 否               | 使用指定的私钥。否则使用 `CHAINAI_PRIVATE_KEY`。           |
| `--from-token <address>`     | 是               | 源代币合约地址。                         |
| `--to-token <address>`     | 是               | 目标代币合约地址。                         |
| `--amount <amount>`       | 是               | 交易金额（以人类可读单位表示，例如 `"1.5"`）。                   |
| `-n, --network <network>` | 否               | 网络（默认：`mainnet`）。                         |
| `-y, --yes`               | 是               | 跳过确认提示并立即提交订单。                         |

**输出（标准输出）**：显示报价信息。

--- 

**输出（标准输出）**：显示订单提交结果。

```json
{
  "from": "0x...",
  "fromToken": "0x...",
  "toToken": "0x...",
  "amount": "1.5",
  "estimatedReturn": "1500",
  "estimatedReturnMin": "1400",
  "estimatedReturnAvg": "1450",
  "network": "Ethereum",
  "orderHash": "0x...",
  "approvalTxHash": "0x..."
}
```

`approvalTxHash` 参数仅在需要 ERC-20 代币批准时非空。对于原生代币交换或已批准的交易，该参数为 `null`。

---

### `swap-order-status`

根据订单哈希值查询 1inch Fusion 交换订单的状态。

```bash
npx chainai@0.0.10 swap-order-status -k 0xKEY --order-hash 0xORDER_HASH
npx chainai@0.0.10 swap-order-status -k 0xKEY --order-hash 0xORDER_HASH -n bsc
```

**选项**：

| 标志                | 是否必需 | 描述                                              |
| ------------------------- | ----------------------------- | -------------------------------------- |
| `-k, --private-key <key>` | 否               | 使用指定的私钥。否则使用 `CHAINAI_PRIVATE_KEY`。           |
| `--order-hash <hash>`     | 是               | 从 `swap` 命令返回的订单哈希值。                         |
| `-n, --network <network>` | 否               | 网络（默认：`mainnet`）。                         |

**输出（标准输出）**：

--- 

可能的 `status` 值：`pending`、`filled`、`cancelled`。对于待处理/已取消的订单，`finalToAmount` 为 `null`，`fills` 为空。