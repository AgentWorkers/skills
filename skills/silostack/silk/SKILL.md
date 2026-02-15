---
name: silk
version: 1.0.4
description: 在Solana平台上，支持代理银行服务和支付功能。用户可以发送和接收稳定币（stablecoins），这些交易通过可撤销的托管（escrow）机制进行管理。此外，还提供了可选的链上账户（on-chain accounts），这些账户具备基于策略的支出限制功能，支持人工授权的自动化操作。
homepage: https://silkyway.ai
metadata: {"category":"payments","api_base":"https://api.silkyway.ai","author":"silkysquad","openclaw":{"requires":{"bins":["silk"]},"install":[{"id":"silk-npm","kind":"node","label":"Silk CLI","package":"@silkysquad/silk"}]}}
---

# SilkyWay

这是一个基于Solana的代理银行和支付服务，支持发送和接收稳定币（如USDC），且完全采用非托管（non-custodial）的方式，所有操作都在链上完成。

## 安装

```bash
npm install -g @silkysquad/silk
```

安装此服务需要Node.js 18及以上版本。

## 设置

```bash
# 1. Initialize (creates wallet and agent ID)
silk init

# 2. Check your wallet address
silk wallet list
```

您的钱包信息和代理ID会被保存在`~/.config/silk/config.json`文件中。您的私钥始终保存在您的设备上。执行`silk init`命令是安全的，可以多次执行。

### 集群配置

默认集群为`mainnet-beta`（使用真实的USDC）。如需使用测试用币，请切换到`devnet`集群。

```bash
silk config set-cluster devnet    # test tokens
silk config set-cluster mainnet-beta  # real USDC
silk config get-cluster           # show current
```

| 集群 | API基础URL | 网络 |
|---------|-------------|---------|
| `mainnet-beta` | `https://api.silkyway.ai` | 主网（使用真实的USDC） |
| `devnet` | `https://devnet-api.silkyway.ai` | 测试网（使用测试用USDC） |

### 为钱包充值（devnet）

在devnet集群上，可以使用内置的 faucet 功能进行充值。每次充值会获得0.1 SOL（用于交易手续费）以及100 USDC：

```bash
silk config set-cluster devnet
silk wallet fund
silk balance
```

在mainnet集群上，需要手动将SOL或USDC发送到您的钱包地址。SOL是进行Solana交易所必需的。

## 发送支付

```bash
silk pay <recipient> <amount> [--memo <text>]
```

发送支付后，USDC会被锁定在链上的托管账户中。接收者可以通过`silk claim`命令领取款项；如果您需要取消支付，可以使用`silk cancel`命令。

系统会生成一个**领取链接**（`claimUrl`），您可以将该链接分享给接收者。接收者只需在浏览器中打开链接，连接他们的钱包即可领取款项。这是非技术背景的接收者最简便的领取方式。

```bash
# Send 10 USDC
silk pay 7xKXz9BpR3mFVDg2Thh3AG6sFRPqNrDJ4bHUkR8Y7vNx 10 --memo "Payment for code review"

# Output includes claimUrl — share it with the recipient
# Example: https://app.silkyway.ai/transfers/9aE5kBqRvF3...?cluster=devnet

# Check your balance
silk balance

# View your transfers
silk payments list
silk payments get <transfer-pda>
```

### 领取支付

如果有人向您发送了付款：

```bash
silk payments list
silk claim <transfer-pda>
```

### 取消支付

如果您发送了付款但尚未被接收者领取，可以随时使用`silk cancel`命令取消该支付。

## 地址簿

您可以保存联系人的信息，以便以后可以通过姓名而不是地址来发送付款。

```bash
silk contacts add alice 7xKXz9BpR3mFVDg2Thh3AG6sFRPqNrDJ4bHUkR8Y7vNx
silk contacts list
silk contacts get alice
silk contacts remove alice
```

保存后，您可以在任何需要输入地址的地方使用这些联系人姓名。

```bash
silk pay alice 10 --memo "Thanks for the review"
silk account send alice 5
```

联系人姓名不区分大小写，并且以小写形式存储在`~/.config/silk/contacts.json`文件中。

## 多钱包支持

```bash
silk wallet create second-wallet
silk wallet fund --wallet second-wallet
silk wallet list
```

在任何命令前加上`--wallet <标签>`参数，即可选择非默认的钱包。

```bash
silk pay <address> 10 --wallet second-wallet
silk balance --wallet second-wallet
```

## 支持聊天

首次使用时，系统会自动生成一个唯一的`agentId`（UUID），用于保持会话的连续性。

## 链上账户（可选）

SilkyWay账户是一个链上钱包，类似于银行账户，由人类所有者创建并充值。所有者可以为账户添加代理人（operator），并设置每笔交易的消费限额。这适用于自动化操作、定期付款或需要将消费权限委托给代理的场景。

使用SilkyWay时并不需要创建账户。即使没有账户，也可以通过`silk pay`命令进行支付。账户是可选的升级功能，适用于希望获得链上控制权限的情况。

**关键概念：**
- **所有者**：创建并充值账户的人类用户。拥有完全控制权，可以转移任意金额、暂停账户或添加/删除代理人。
- **代理人**：您（作为代理人）被授权从账户发送代币，但必须遵守所有者设定的每笔交易限额。
- **每笔交易限额**：单次交易的最大USDC金额限制。该限制由Solana系统强制执行；超过限额的交易会被拒绝。设置为0表示无限制。
- **暂停账户**：所有者可以暂停账户，阻止所有代理人的转账操作，直到账户被重新启用。

### 设置账户

账户必须由人类所有者创建：
1. 将设置URL分享给所有者（请使用`silk wallet list`命令获取您的钱包地址）：
   ```
   https://app.silkyway.ai/account/setup?agent=YOUR_WALLET_ADDRESS
   ```
   所有者会连接他们的钱包，设置您的消费限额并充值账户。
   **注意**：所有者在设置页面上必须选择与您的CLI集群相同的网络（mainnet或devnet）。如果您使用的是devnet，请告知他们先切换到devnet后再创建账户。
2. 创建账户后，需要同步账户信息：
   ```bash
   silk account sync
   ```
3. 检查账户状态并发送付款：
   ```bash
   silk account status
   silk account send <recipient> <amount>
   ```

如果转账金额超过您的每笔交易限额，交易会在链上被拒绝（错误代码：`ExceedsPerTxLimit`）。如果账户被暂停，系统会显示“AccountPaused”提示。
如果`silk account sync`命令返回“No account found”，说明所有者尚未创建账户，请再次分享设置URL。

### 账户与托管支付

| | 账户 | 托管支付（silk pay） |
|---|---|---|
| **是否需要设置** | 人类创建账户并添加您为代理人 | 无需设置——只需一个已充值的钱包 |
| **消费限制** | 每笔交易都有链上强制执行的限额 | 无限制 |
| **接收者能否领取？** | 不能——直接转移，代币立即到达接收者钱包 | 可以——接收者需要使用`silk claim`命令领取 |
| **能否取消？** | 不能——转移立即完成 | 可以——发送者可以在接收者领取前取消 |
| **适用场景** | 需要人类监督的持续性付款 | 双方之间的一次性付款 |

如果所有者为您设置了账户，建议使用`silk account send`命令，因为它更简单（无需领取步骤），且所有者可以控制消费限额。

## CLI参考

| 命令 | 描述 |
|---------|-------------|
| `silk init` | 初始化CLI（创建钱包、代理ID和联系人信息文件） |
| `silk wallet create [标签]` | 创建新钱包 |
| `silk wallet list` | 列出所有钱包及其地址 |
| `silk wallet fund [--sol] [--usdc] [--wallet <标签>]` | 从devnet faucet为钱包充值 |
| `silk balance [--wallet <标签>]` | 查看SOL和USDC余额 |
| `silk pay <接收者> <金额> [--memo <文本>] [--wallet <标签>]` | 将USDC发送到托管账户 |
| `silk claim <转移PDA> [--wallet <标签>]` | 领取收到的付款 |
| `silk cancel <转移PDA> [--wallet <标签>]` | 取消已发送的付款 |
| `silk payments list [--wallet <标签>]` | 查看所有转账记录 |
| `silk payments get <转移PDA>` | 获取转账详情 |
| `silk contacts add <名称> <地址>` | 将联系人信息保存到地址簿 |
| `silk contacts remove <名称>` | 从地址簿中删除联系人 |
| `silk contacts list` | 列出所有保存的联系人 |
| `silk contacts get <名称>` | 查找联系人的地址 |
| `silk account sync [--wallet <标签>] [--account <pda>]` | 发现并同步您的链上账户 |
| `silk account status [--wallet <标签>]` | 显示账户余额、消费限额和暂停状态 |
| `silk account send <接收者> <金额> [--memo <文本>]` | 从账户发送付款（遵循链上规则） |
| `silk chat <消息>` | 向SilkyWay支持团队提问 |
| `silk config set-cluster <集群>` | 设置集群（mainnet-beta或devnet） |
| `silk config get-cluster` | 显示当前集群和API地址 |
| `silk config reset-cluster` | 将集群重置为默认值（mainnet-beta） |

在命令前加上`--wallet <标签>`参数，可以选择非默认的钱包。接收者可以接受联系人姓名或Solana地址作为收款地址。

## 交易流程

SilkyWay采用非托管模式，您的私钥始终保存在您的设备上。

所有交易都遵循“构建-签名-提交”的流程：
1. **构建**：SDK使用支付详情调用API端点，后端生成未签名的Solana交易并返回其Base64编码。
2. **签名**：SDK使用您的私钥对交易进行签名。
3. **提交**：SDK将签名后的交易发送到后端，后端再将其发送到Solana网络。

后端负责处理复杂的交易逻辑（如PDA生成、指令构建和区块哈希管理）。后端永远不会看到您的私钥，所有授权操作都由Solana系统在链上执行。

## API端点

基础URL：`https://api.silkyway.ai`（mainnet）或`https://devnet-api.silkyway.ai`（devnet）

所有请求均使用`Content-Type: application/json`格式。

### 托管支付相关端点

### POST /api/tx/create-transfer

创建一个未签名的创建转账交易，将USDC锁定在托管账户中。

**请求参数：**
```json
{
  "sender": "BrKz4GQN1sxZWoGLbNTojp4G3JCFLRkSYk3mSRWhKsXp",
  "recipient": "7xKXz9BpR3mFVDg2Thh3AG6sFRPqNrDJ4bHUkR8Y7vNx",
  "amount": 10.00,
  "token": "usdc",
  "memo": "Payment for code review"
}
```

| 字段 | 类型 | 是否必填 | 描述 |
|-------|------|----------|-------------|
| `sender` | string | 是 | 发送者的Solana公钥 |
| `recipient` | string | 是 | 接收者的Solana公钥 |
| `amount` | number | 是 | 代币数量（例如`10.00`表示10 USDC） |
| `token` | string | 是 | 代币符号（例如`"usdc"`） |
| `memo` | string | 否 | 供人类阅读的备注信息 |
| `claimableAfter` | number | 否 | Unix时间戳——接收者必须在指定时间之后才能领取款项 |

您也可以直接提供`mint`（代币的公钥）或`poolPda`，但`token`是更简单的选择。

**响应：**
```json
{
  "ok": true,
  "data": {
    "transaction": "AQAAAAAAAAAAAAAA...base64...AAAAAAA=",
    "transferPda": "9aE5kBqRvF3mNcXz8BpR3mFVDg2Thh3AG6sFRPqNrDJ4",
    "nonce": "1738900000000",
    "message": "Sign and submit via POST /api/tx/submit"
  }
}
```

`transferPda`是该托管交易的链上地址，用于后续的领取或取消操作。

### POST /api/tx/claim-transfer

创建一个未签名的领取转账交易，将USDC从托管账户转移到接收者的钱包。

只有指定的接收者才能领取款项。如果设置了`claimableAfter`时间限制，领取操作将在该时间之前失败。

**请求参数：**
```json
{
  "transferPda": "9aE5kBqRvF3mNcXz8BpR3mFVDg2Thh3AG6sFRPqNrDJ4",
  "claimer": "7xKXz9BpR3mFVDg2Thh3AG6sFRPqNrDJ4bHUkR8Y7vNx"
}
```

| 字段 | 类型 | 是否必填 | 描述 |
|-------|------|----------|-------------|
| `transferPda` | string | 是 | 转移交易的链上PDA地址 |
| `claimer` | string | 是 | 接收者的Solana公钥 |

**响应：**
```json
{
  "ok": true,
  "data": {
    "transaction": "AQAAAAAAAAAAAAAA...base64...AAAAAAA=",
    "message": "Sign and submit via POST /api/tx/submit"
  }
}
```

**常见错误：**
- `ClaimTooEarly`（6003）——领取时间未到 |
- `TransferAlreadyClaimed`（6000）——款项已被领取 |
- `TransferAlreadyCancelled`（6001）——发送者已取消交易 |
- `Unauthorized`（6004）——领取者未经授权 |

### POST /api/tx/cancel-transfer

创建一个未签名的取消转账交易，将USDC从托管账户退还给发送者。

只有原始发送者才能取消交易，且只能在交易尚未被领取的情况下取消。

**请求参数：**
```json
{
  "transferPda": "9aE5kBqRvF3mNcXz8BpR3mFVDg2Thh3AG6sFRPqNrDJ4",
  "canceller": "BrKz4GQN1sxZWoGLbNTojp4G3JCFLRkSYk3mSRWhKsXp"
}
```

| 字段 | 类型 | 是否必填 | 描述 |
|-------|------|----------|-------------|
| `transferPda` | string | 是 | 转移交易的链上PDA地址 |
| `canceller` | string | 是 | 发送者的Solana公钥 |

**响应：**
```json
{
  "ok": true,
  "data": {
    "transaction": "AQAAAAAAAAAAAAAA...base64...AAAAAAA=",
    "message": "Sign and submit via POST /api/tx/submit"
  }
}
```

**常见错误：**
- `TransferAlreadyClaimed`（6000）——款项已被领取 |
- `TransferAlreadyCancelled`（6001）——交易已被取消 |
- `Unauthorized`（6004）——取消操作者未经授权 |

### POST /api/tx/submit

将签名后的交易提交到Solana网络。

**请求参数：**
```json
{
  "signedTx": "AQAAAAAAAAAAAAAA...base64-signed...AAAAAAA="
}
```

**响应：**
```json
{
  "ok": true,
  "data": {
    "txid": "5UfDuXsrhFnxGZmyJxNR8z7Ee5JDFrgWHKPdTEJvoTpB3Qw8mKz4GQN1sxZWoGL"
  }
}
```

### GET /api/transfers/:pda

获取单笔交易的详细信息。

**示例：`GET /api/transfers/9aE5kBqRvF3mNcXz8BpR3mFVDg2Thh3AG6sFRPqNrDJ4`

**响应：**
```json
{
  "ok": true,
  "data": {
    "transfer": {
      "id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
      "transferPda": "9aE5kBqRvF3mNcXz8BpR3mFVDg2Thh3AG6sFRPqNrDJ4",
      "sender": "BrKz4GQN1sxZWoGLbNTojp4G3JCFLRkSYk3mSRWhKsXp",
      "recipient": "7xKXz9BpR3mFVDg2Thh3AG6sFRPqNrDJ4bHUkR8Y7vNx",
      "amount": "10000000",
      "amountRaw": "10000000",
      "status": "ACTIVE",
      "memo": "Payment for code review",
      "createTxid": "5UfDuXsrhFnxGZmyJxNR8z7Ee5JDFrgWHKPdTEJvoTpB",
      "claimTxid": null,
      "cancelTxid": null,
      "claimableAfter": null,
      "claimableUntil": null,
      "createdAt": "2025-02-07T12:00:00.000Z",
      "updatedAt": "2025-02-07T12:00:00.000Z",
      "token": { "mint": "4zMMC9srt5Ri5X14GAgXhaHii3GnPAEERYPJgZJDncDU", "symbol": "USDC", "decimals": 6 },
      "pool": { "poolPda": "3Fk8vMYJbCbEB2jzRCdRG9rFJhN2TCmPia9BjEKpTk5R", "feeBps": 50 }
    }
  }
}
```

**注意**：`amount`字段以原始代币单位显示。USDC有6位小数，因此`10000000`表示10.00 USDC。

### GET /api/transfers?wallet=\<pubkey\>

列出所有发送者或接收者为该钱包的交易记录。

**示例：`GET /api/transfers?wallet=BrKz4GQN1sxZWoGLbNTojp4G3JCFLRkSYk3mSRWhKsXp`

**响应：**
```json
{
  "ok": true,
  "data": {
    "transfers": [
      {
        "transferPda": "9aE5kBqRvF3mNcXz8BpR3mFVDg2Thh3AG6sFRPqNrDJ4",
        "sender": "BrKz4GQN1sxZWoGLbNTojp4G3JCFLRkSYk3mSRWhKsXp",
        "recipient": "7xKXz9BpR3mFVDg2Thh3AG6sFRPqNrDJ4bHUkR8Y7vNx",
        "amount": "10000000",
        "status": "ACTIVE",
        "memo": "Payment for code review",
        "createdAt": "2025-02-07T12:00:00.000Z",
        "token": { "mint": "4zMMC9srt5Ri5X14GAgXhaHii3GnPAEERYPJgZJDncDU", "symbol": "USDC", "decimals": 6 },
        "pool": { "poolPda": "3Fk8vMYJbCbEB2jzRCdRG9rFJhN2TCmPia9BjEKpTk5R", "feeBps": 50 }
      }
    ]
  }
}
```

### POST /api/tx/faucet

在devnet集群上发放SOL或USDC。

**请求参数：**
```json
{
  "wallet": "BrKz4GQN1sxZWoGLbNTojp4G3JCFLRkSYk3mSRWhKsXp",
  "token": "usdc"
}
```

`token`字段可选。输入`sol`表示发放SOL，输入`usdc`表示发放USDC。

**响应：**
```json
{
  "ok": true,
  "data": {
    "amount": 0.1,
    "txid": "5UfDuXsrhFnxGZmyJxNR8z7Ee5JDFrgWHKPdTEJvoTpB3Qw8mKz4GQN1sxZWoGL"
  }
}
```

### 账户相关端点

#### GET /api/account/by-operator/:pubkey

查找您的钱包作为代理人参与的账户。

**示例：`GET /api/account/by-operator/7xKXz9BpR3mFVDg2Thh3AG6sFRPqNrDJ4bHUkR8Y7vNx`

**响应：**
```json
{
  "ok": true,
  "data": {
    "accounts": [
      {
        "pda": "9aE5kBqRvF3mNcXz8BpR3mFVDg2Thh3AG6sFRPqNrDJ4",
        "owner": "BrKz4GQN1sxZWoGLbNTojp4G3JCFLRkSYk3mSRWhKsXp",
        "mint": "4zMMC9srt5Ri5X14GAgXhaHii3GnPAEERYPJgZJDncDU",
        "mintDecimals": 6,
        "isPaused": false,
        "balance": 10000000,
        "operatorSlot": {
          "index": 0,
          "perTxLimit": 5000000,
          "dailyLimit": 0
        }
      }
    ]
  }
}
```

如果未找到账户，将返回空数组——说明所有者尚未为您设置账户。

#### GET /api/account/:pda

获取账户的完整信息。

**示例：`GET /api/account/9aE5kBqRvF3mNcXz8BpR3mFVDg2Thh3AG6sFRPqNrDJ4`

**响应：**
```json
{
  "ok": true,
  "data": {
    "pda": "9aE5kBqRvF3mNcXz8BpR3mFVDg2Thh3AG6sFRPqNrDJ4",
    "owner": "BrKz4GQN1sxZWoGLbNTojp4G3JCFLRkSYk3mSRWhKsXp",
    "mint": "4zMMC9srt5Ri5X14GAgXhaHii3GnPAEERYPJgZJDncDU",
    "mintDecimals": 6,
    "isPaused": false,
    "balance": 10000000,
    "operators": [
      {
        "pubkey": "7xKXz9BpR3mFVDg2Thh3AG6sFRPqNrDJ4bHUkR8Y7vNx",
        "perTxLimit": 5000000,
        "dailyLimit": 0
      }
    ]
  }
}
```

**注意**：`balance`和`perTxLimit`字段以原始代币单位显示。USDC有6位小数，因此`5000000`表示5.00 USDC。

#### POST /api/account/transfer

创建一个未签名的转账交易。

**请求参数：**
```json
{
  "signer": "7xKXz9BpR3mFVDg2Thh3AG6sFRPqNrDJ4bHUkR8Y7vNx",
  "accountPda": "9aE5kBqRvF3mNcXz8BpR3mFVDg2Thh3AG6sFRPqNrDJ4",
  "recipient": "Dg2Thh3AG6sFRPqNrDJ4bHUkR8Y7vNx7xKXz9BpR3mFV",
  "amount": 3000000
}
```

| 字段 | 类型 | 是否必填 | 描述 |
|-------|------|----------|-------------|
| `signer` | string | 是 | 您的钱包地址（即代理人地址） |
| `accountPda` | string | 是 | 账户的链上PDA地址 |
| `recipient` | string | 是 | 接收者的Solana公钥 |
| `amount` | number | 是 | 代币数量（以原始单位表示） |

**响应：**
```json
{
  "ok": true,
  "data": {
    "transaction": "AQAAAAAAAAAAAAAA...base64...AAAAAAA="
  }
}
```

使用`POST /api/tx/submit`命令对交易进行签名和提交。

**常见错误：**
- `ExceedsPerTxLimit`——转账金额超过每笔交易的限额 |
- `AccountPaused`——账户被暂停，所有代理人的转账操作被阻止 |
- `Unauthorized`——签名者不是账户的所有者或代理人 |

#### POST /api/account/create

创建一个未签名的账户。

**请求参数：**
```json
{
  "owner": "BrKz4GQN1sxZWoGLbNTojp4G3JCFLRkSYk3mSRWhKsXp",
  "mint": "4zMMC9srt5Ri5X14GAgXhaHii3GnPAEERYPJgZJDncDU",
  "operator": "7xKXz9BpR3mFVDg2Thh3AG6sFRPqNrDJ4bHUkR8Y7vNx",
  "perTxLimit": 5000000
}
```

#### POST /api/account/deposit

创建一个用于充值账户的未签名交易。

**请求参数：**
```json
{
  "depositor": "BrKz4GQN1sxZWoGLbNTojp4G3JCFLRkSYk3mSRWhKsXp",
  "accountPda": "9aE5kBqRvF3mNcXz8BpR3mFVDg2Thh3AG6sFRPqNrDJ4",
  "amount": 10000000
}
```

### POST /chat

向SilkyWay支持团队发送消息，系统会返回AI生成的回复。

**请求参数：**
```json
{
  "agentId": "uuid-v4",
  "message": "How do I send a payment?"
}
```

| 字段 | 类型 | 是否必填 | 描述 |
|-------|------|----------|-------------|
| `agentId` | string | 是 | 由SDK生成的唯一标识符（UUID） |
| `message` | string | 需要咨询的问题 |

**响应（状态码200）：**
```json
{
  "ok": true,
  "data": {
    "message": "Use silk pay...",
    "agentId": "uuid-v4"
  }
}
```

## 转移状态

| 状态 | 描述 |
|--------|-------------|
| `ACTIVE` | 代币被锁定在托管账户中，等待领取或取消 |
| `CLAIMED` | 接收者已领取款项 |
| `CANCELLED` | 发送者已取消交易并取回了款项 |
| `EXPIRED` | 转移交易已超出领取时间限制 |

## 错误代码

### 托管相关错误（握手阶段）

| 代码 | 名称 | 描述 |
|------|------|-------------|
| 6000 | `TransferAlreadyClaimed` | 交易已被领取 |
| 6001 | `TransferAlreadyCancelled` | 交易已被取消 |
| 6002 | `TransferAlreadyCancelled` | 交易已被取消 |
| 6003 | `ClaimTooEarly` | 领取时间未到 |
| 6004 | `Unauthorized` | 签名者未经授权 |
| 6005 | `PoolPaused` | 代币的托管池暂时暂停——请稍后再试 |
| 6006 | `InsufficientFunds` | 发送者账户余额不足 |

### 账户相关错误（Silkysig）

| 代码 | 名称 | 描述 |
|------|------|-------------|
| 6000 | `Unauthorized` | 签名者不是账户的所有者或代理人 |
| 6001 | `ExceedsPerTxLimit` | 转移金额超过每笔交易的限额 |
| 6002 | `ExceedsDailyLimit` | 转移金额超过每日限额（尚未生效） |
| 6003 | `AccountPaused` | 账户被暂停，代理人无法进行转账 |
| 6004 | `MaxOperators Reached` | 账户已拥有最多3个代理人 |
| 6005 | `OperatorNotFound` | 指定的代理人不存在 |
| 6006 | `OperatorAlreadyExists` | 该账户已存在多个代理人 |
| 6008 | `InsufficientBalance` | 账户余额不足 |

### API相关错误

| 代码 | HTTP状态码 | 描述 |
|-------|------|-------------|
| 400 | `INVALID_PUBKEY` | 提供的Solana公钥格式无效 |
| 400 | `INVALID_AMOUNT` | 金额必须为正数 |
| 400 | `MISSING_FIELD` | 必需字段未提供 |
| 404 | `TRANSFER_NOT_FOUND` | 未找到对应的转账记录 |
| 404 | `POOL_NOT_FOUND` | 未找到对应的托管池 |
| 400 | `TOKEN_NOT_FOUND` | 未识别到的代币符号 |
| 400 | `TX_FAILED` | 交易模拟或提交失败 |
| 429 | 请求次数过多 |
| 400 | 发放失败 |

## 响应格式

**成功**：
```json
{
  "ok": true,
  "data": { ... }
}
```

**错误**：
```json
{
   "ok": false,
   "error": "ERROR_CODE",
   "message": "Human-readable description"
}
```

## 安全性说明：
- **非托管模式**：后端仅生成未签名的交易，您需要使用私钥在本地进行签名后再提交。
- 私钥永远不会传输到服务器。
- 所有授权操作都由Solana系统在链上执行，后端不会处理私钥。
- 私钥保存在`~/.config/silk/config.json`文件中，请勿泄露此文件。