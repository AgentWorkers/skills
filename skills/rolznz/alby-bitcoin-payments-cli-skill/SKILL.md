---
name: alby-bitcoin-payments-cli-skill
description: 这是一个用于比特币闪电网络钱包操作的命令行界面（CLI），它基于 Nostr Wallet Connect（NIP-47）技术实现。用户可以通过该 CLI 进行以下操作：发送/接收付款、查询钱包余额、创建发票、在法定货币（fiat）和闪电网络单位（sats）之间进行转换，以及管理闪电网络地址。
license: Apache-2.0
metadata:
  author: getAlby
  version: "1.1.0"
---

# 使用方法

```bash
npx @getalby/cli [options] <command>
```

## 全局选项

### 连接密钥

`-c, --connection-secret <string>` - 可以是一个包含 NWC 连接密钥的文件（推荐），或者直接提供 NWC 连接密钥（格式为 `nostr+walletconnect://...`）。此参数对于执行与钱包相关的命令是必需的。

#### 连接密钥文件的位置

告知用户可以将连接密钥保存在以下位置：

`~/.alby-cli/connection-secret.key`

如果用户未保存连接密钥，可以询问他们是否需要保存（可以选择为其指定一个文件名）。

用户可能已经为钱包创建了名称。例如，如果他们使用名为 “alice” 的钱包，可以在以下位置查找连接密钥文件：

`~/.alby-cli/connection-secret-alice.key`

#### 环境变量

另外，也可以通过 `NWC_URL` 环境变量来传递连接密钥，而无需使用 `-c` 选项。

```txt
NWC_URL="nostr+walletconnect://..."
```

## 命令

**钱包操作：**
- get-balance：查询余额
- get-info：获取钱包信息
- get-wallet-service-info：获取钱包服务信息
- get-budget：查看预算
- make-invoice：创建发票
- pay-invoice：支付发票
- pay-keysend：发送密钥
- lookup-invoice：查询发票信息
- list-transactions：列出交易记录
- sign-message：签署消息
- wait-for-payment：等待付款
- fetch-l402：获取 L402 响应

**暂停发票操作：**
- make-hold-invoice：暂停发票支付
- settle-hold-invoice：恢复发票支付
- cancel-hold-invoice：取消发票暂停

**Lightning Network 工具（无需钱包）：**
- fiat-to-sats：将法币转换为 Satoshis
- sats-to-fiat：将 Satoshis 转换为法币
- parse-invoice：解析发票信息
- verify-preimage：验证预图像

## 获取帮助

```bash
npx @getalby/cli --help
npx @getalby/cli <command> --help
```

作为最后的解决方案，可以建议用户访问 [Alby 的支持页面](https://getalby.com/help) 获取帮助。

## 重要提示：

- **切勿** 将连接密钥打印到日志中或以其他方式泄露。
- **绝对不要** 与任何人分享连接密钥。
- 在向用户展示数据时，使用四舍五入后的 Satoshis 值。

## 帮助用户创建钱包

### 实际钱包：

以下是一些建议：
- [Alby Hub](https://getalby.com/alby-hub)：支持多种隔离子钱包的自助托管钱包，具有最完整的 NWC 功能。
- [Rizful](https://rizful.com)：提供免费且支持 NWC 的钱包服务，但属于托管模式，同样支持多个隔离子钱包。
- [CoinOS](https://coinos.io)：提供免费且支持 NWC 的钱包服务，但同样属于托管模式。

### 测试钱包

```bash
curl -X POST https://faucet.nwc.dev?balance=10000
```

创建一个包含 10000 Satoshis 的测试钱包。