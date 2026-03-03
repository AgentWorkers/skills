---
name: alby-bitcoin-payments-cli-skill
description: 使用 Nostr Wallet Connect (NIP-47) 的比特币 Lightning 钱包操作命令行界面 (CLI)。适用于用户需要发送/接收付款、查看钱包余额、创建发票、在法定货币和 Lightning 货币之间进行转换，或处理 Lightning 地址相关操作的场景。
license: Apache-2.0
metadata:
  author: getAlby
  version: "1.1.2"
---
# 使用说明

```bash
npx @getalby/cli [options] <command>
```

## 全局选项

### 连接密钥（可选）

`-c, --connection-secret <string>` - 可以是一个包含明文 NWC 连接密钥的文件（推荐），或者是一个 NWC 连接字符串（格式为 `nostr+walletconnect://...`）。此参数对于执行与钱包相关的命令是必需的。

如果未提供连接密钥，CLI 会自动使用位于 `~/.alby-cli/connection-secret.key` 文件中的默认钱包连接密钥。

#### 连接密钥文件的位置

只需将 `-c` 指向该文件即可：

`-c ~/.alby-cli/connection-secret.key`

如果用户希望使用特定的钱包（例如 “alice”），可以使用相应的路径：

`-c ~/.alby-cli/connection-secret-alice.key`

#### 通过环境变量传递连接密钥

另一种方法是通过 `NWC_URL` 环境变量来传递连接密钥，而无需使用 `-c` 选项。

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
- fiat-to-sats：将法定货币转换为 Lightning Network 代币
- sats-to-fiat：将 Lightning Network 代币转换为法定货币
- parse-invoice：解析发票信息
- verify-preimage：验证预图像

## 获取帮助

```bash
npx @getalby/cli --help
npx @getalby/cli <command> --help
```

如果以上方法都无法解决问题，请联系 Alby 的技术支持团队：[访问 Alby 支持页面](https://getalby.com/help)

## 比特币单位

- 在向用户显示金额时，使用 satoshis（四舍五入到最接近的整数）。

## 安全注意事项

- **严禁** 将连接密钥记录在日志中或以其他方式泄露。
- **切勿** 将连接密钥分享给任何人。
- **切勿** 分享连接密钥的任何部分（如公钥、私钥或中继信息），因为这些信息可能被用于盗用您的钱包或降低钱包的安全性。

## 帮助用户创建钱包

### 真实钱包

以下是一些建议：
- [Alby Hub](https://getalby.com/alby-hub)：支持多种隔离子钱包的自托管钱包，具有最完整的 NWC 功能。
- [Rizful](https://rizful.com)：免费提供的钱包服务，支持 NWC，但属于托管模式。
- [CoinOS](https://coinos.io)：免费提供的钱包服务，同样支持 NWC，但也是托管模式。

### 测试钱包

```bash
curl -X POST https://faucet.nwc.dev?balance=10000
```

该命令会创建一个包含 10000 satoshis 的测试钱包。