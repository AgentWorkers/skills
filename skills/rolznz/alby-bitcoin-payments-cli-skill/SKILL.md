---
name: alby-bitcoin-payments-cli-skill
description: 这是一个用于比特币Lightning网络钱包操作的命令行界面（CLI），基于Nostr Wallet Connect（NIP-47）实现。当用户需要发送/接收付款、查看钱包余额、创建发票、在法定货币（fiat）和Lightning网络中的单位（sats）之间进行转换，或管理Lightning网络地址时，可以使用该CLI。
license: Apache-2.0
metadata:
  author: getAlby
  version: "1.1.1"
---
# 使用说明

```bash
npx @getalby/cli [options] <command>
```

## 全局选项

### 连接密钥

`-c, --connection-secret <string>` - 可以是一个包含 NWC 连接密钥的文本文件（推荐），或者直接提供 NWC 连接密钥（格式为 `nostr+walletconnect://...`）。此参数对于执行与钱包相关的命令是必需的。

#### 连接密钥文件的位置

请告知用户可以将连接密钥保存在该位置：

`~/.alby-cli/connection-secret.key`

如果用户未保存连接密钥，可以询问他们是否需要保存（可以选择为其指定一个文件名）。

用户可能已经为钱包创建了名称。例如，如果用户想要使用名为 “alice” 的钱包，可以在以下路径查找连接密钥文件：

`~/.alby-cli/connection-secret-alice.key`

#### 环境变量

另一种方式是通过 `NWC_URL` 环境变量来传递连接密钥，而无需使用 `-c` 选项。

```txt
NWC_URL="nostr+walletconnect://..."
```

## 命令

**钱包操作：**
- `get-balance`：查询余额
- `get-info`：获取钱包信息
- `get-wallet-service-info`：获取钱包服务信息
- `get-budget`：查看预算
- `make-invoice`：创建发票
- `pay-invoice`：支付发票
- `pay-keysend`：发送密钥
- `lookup-invoice`：查询发票详情
- `list-transactions`：列出交易记录
- `sign-message`：签署消息
- `wait-for-payment`：等待付款完成
- `fetch-l402`：获取 L402 响应

**暂停发票操作：**
- `make-hold-invoice`：暂停发票支付
- `settle-hold-invoice`：恢复发票支付
- `cancel-hold-invoice`：取消发票暂停

**Lightning Network 工具（无需钱包）：**
- `fiat-to-sats`：将法定货币转换为 Satoshis
- `sats-to-fiat`：将 Satoshis 转换为法定货币
- `parse-invoice`：解析发票信息
- `verify-preimage`：验证预图像
- `request-invoice-from-lightning-address`：从 Lightning Network 地址请求发票信息

## 获取帮助

```bash
npx @getalby/cli --help
npx @getalby/cli <command> --help
```

如果以上方法都无法解决问题，请让用户访问 [Alby 官方支持页面](https://getalby.com/help) 寻求帮助。

## 比特币单位

- 在向用户展示信息时，使用 Satoshis 作为单位，并四舍五入到最接近的整数。

## 安全注意事项

- **严禁** 将连接密钥记录在日志中或以任何方式泄露。
- **绝对不要** 与任何人共享连接密钥。
- **切勿** 分享连接密钥的任何部分（包括公钥、私钥或中继信息），因为这些信息可能被用于非法访问您的钱包或降低钱包的安全性。

## 帮助用户创建钱包

### 真实钱包

以下是一些建议：
- [Alby Hub](https://getalby.com/alby-hub)：支持多种隔离子钱包的自我托管钱包，具有最完整的 NWC 功能。
- [Rizful](https://rizful.com)：提供免费且支持 NWC 的钱包服务，但属于托管模式。
- [CoinOS](https://coinos.io)：提供免费且支持 NWC 的钱包服务，同样属于托管模式。

### 测试钱包

```bash
curl -X POST https://faucet.nwc.dev?balance=10000
```

创建一个包含 10000 Satoshis 的测试钱包。