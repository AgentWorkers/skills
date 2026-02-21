---
name: agent-wallet
description: 适用于AI代理的自托管比特币闪电网络钱包。当代理需要发送或接收比特币付款、查询余额、生成发票或管理钱包时，可以使用该钱包。支持bolt11、bolt12、LNURL和闪电网络地址。无需任何配置——只需执行一个命令即可完成初始化。
homepage: https://docs.moneydevkit.com/agent-wallet
repository: https://github.com/anthropics/moneydevkit
metadata:
  {
    "openclaw":
      {
        "emoji": "₿",
        "requires": { "bins": ["node", "npx"] },
        "install":
          [
            {
              "id": "agent-wallet-npm",
              "kind": "npm",
              "package": "@moneydevkit/agent-wallet",
              "bins": ["agent-wallet"],
              "label": "Install @moneydevkit/agent-wallet (npm)",
            },
          ],
        "security":
          {
            "secrets": ["~/.mdk-wallet/config.json (BIP39 mnemonic)"],
            "network": ["localhost:3456 (daemon HTTP server)", "MDK Lightning infrastructure via outbound connections"],
            "persistence": ["~/.mdk-wallet/ (config, payment history)"],
            "notes": "The wallet stores a BIP39 mnemonic to disk and runs a local daemon. The mnemonic controls real funds on mainnet. Back it up and restrict file permissions on ~/.mdk-wallet/."
          }
      },
  }
---
# agent-wallet

这是一个由 [MoneyDevKit](https://moneydevkit.com) 开发的、专为 AI 代理设计的自托管 Lightning 钱包。只需执行一个命令即可完成初始化，所有输出结果均为 JSON 格式。

**来源：** [@moneydevkit/agent-wallet 在 npm 上](https://www.npmjs.com/package/@moneydevkit/agent-wallet) · [GitHub](https://github.com/anthropics/moneydevkit)

## 安全性与透明度

该工具使用了 [MoneyDevKit] 发布的 npm 包 `@moneydevkit/agent-wallet`。其主要功能包括：

- **生成并存储一个 BIP39 密码短语**，该短语即为您的私钥（请将其视为密码并妥善保管）。
- **在 `localhost:3456` 上运行一个本地守护进程**，作为钱包操作的 HTTP 服务器（仅允许本地访问，无法从外部访问）。
- **与 MDK 的 Lightning 基础设施建立连接**。
- **将支付历史记录保存在 `~/.mdk-wallet/` 目录中**。

除标准的 Lightning 协议操作外，没有任何数据会被发送到外部服务器。您可以通过查看 [源代码](https://github.com/anthropics/moneydevkit) 或发布的 npm 压缩包来验证这一点。

**建议：** 在生产环境中固定使用某个特定版本（例如 `npx @moneydevkit/agent-wallet@0.11.0`）。

## 快速入门

```bash
# Initialize wallet (generates mnemonic)
npx @moneydevkit/agent-wallet init

# Get balance
npx @moneydevkit/agent-wallet balance

# Create invoice
npx @moneydevkit/agent-wallet receive 1000

# Pay someone
npx @moneydevkit/agent-wallet send user@getalby.com 500
```

## 工作原理

首次执行命令时，CLI 会自动启动守护进程。该守护进程：
- 在 `localhost:3456` 上运行本地 HTTP 服务器。
- 与 MDK 的 Lightning 基础设施建立连接。
- 每 30 秒轮询一次是否有新的支付请求。
- 将支付历史记录保存到 `~/.mdk-wallet/` 目录中。

无需使用 Webhook 端点，所有操作均由守护进程在本地处理。

## 设置

### 首次初始化

```bash
npx @moneydevkit/agent-wallet init
```

执行此命令后：
- 生成一个 BIP39 密码短语（即您的钱包密钥）。
- 在 `~/.mdk-wallet/config.json` 文件中创建钱包配置。
- 根据密码短语生成一个唯一的 8 位十六进制 ID（`walletId`）。
- 启动守护进程（在端口 3456 上运行本地 Lightning 节点）。

钱包立即可以使用。无需 API 密钥、无需注册账户，代理自身负责管理其钱包密钥。

### 查看现有配置

```bash
npx @moneydevkit/agent-wallet init --show
```

执行此命令后，将返回以下信息：
```json
{
  "mnemonic": "...",
  "network": "mainnet",
  "walletId": "..."
}
```

**注意：** `init` 命令不会覆盖已存在的钱包配置。如需重新初始化，请执行相应的命令。

## 命令列表

所有命令的输出均为 JSON 格式。成功时返回 0，失败时返回 1。

| 命令          | 描述                          |
|-----------------|---------------------------------------------|
| `init`        | 生成密码短语并创建钱包配置                   |
| `init --show`     | 显示钱包配置（密码短语会被隐藏）                   |
| `start`        | 启动守护进程                         |
| `balance`       | 查看钱包余额（单位：sats）                    |
| `receive <amount>`    | 生成支付请求                        |
| `receive`       | 生成可变金额的支付请求                    |
| `receive <amount> --description "..."` | 生成带有自定义描述的支付请求                |
| `receive-bolt12`    | 生成可重复使用的 BOLT12 支付请求                |
| `send <destination> [amount]` | 向指定地址发送支付（支持 bolt11、bolt12、LNURL 或 Lightning 地址） |
| `payments`      | 查看支付历史记录                        |
| `status`       | 检查守护进程是否正在运行                     |
| `stop`        | 停止守护进程                         |
| `restart`      | 重新启动守护进程                         |

### 查看余额

执行 `balance` 命令后，将返回以下信息：
```json
{
  "balance_sats": 3825
}
```

### 收款（生成支付请求）

执行 `receive` 命令后，将返回以下信息：
```json
{
  "invoice": "lnbc...", "payment_hash": "...", "expires_at": "..."
}
```

### 接收 BOLT12 支付请求

执行 `receive-bolt12` 命令后，将返回以下信息：
```json
{
  "offer": "lno1..."
}
```

BOLT12 支付请求是可重复使用的，且不会过期；您只需分享一次支付请求即可接收多次付款。与 BOLT11 不同，付款方可以自行选择支付金额。

### 发送支付

执行 `send` 命令后，根据不同的支付方式，需要提供不同的参数：

- **bolt11 支付请求**：格式为 `lnbc10n1...`（金额已编码，无需额外参数）。
- **bolt12 支付请求**：格式为 `lno1...`。
- **Lightning 地址**：格式为 `user@example.com`。
- **LNURL**：格式为 `lnurl1...`（发送到 Lightning 地址时需要提供金额）。

### 查看支付历史记录

执行 `payments` 命令后，将返回以下信息：
```json
{
  "payments": [
    {
      "paymentHash": "...",
      "amountSats": 1000,
      "direction": "inbound" | "outbound",
      "timestamp": "...",
      "destination": "..."
    }
  ]
}
```

## 升级

在升级过程中，`~/.mdk-wallet/` 目录中的钱包配置和支付历史记录会得到保留。

## 使用注意事项：

- **单位说明**：金额应使用 `₿` 前缀加上 sats（例如：`₿1,000`，而非 “1,000 sats”）。
- **自托管**：该钱包的私钥由您自己保管，务必备份。丢失私钥可能导致资金丢失。
- **守护进程**：在 `:3456` 端口上运行本地 Lightning 节点，会自动启动并保存在磁盘上。
- **代理间支付**：使用此钱包的任何代理都可以向其他代理的账户或 Lightning 地址进行支付。

## 下一步？

**希望接受客户付款吗？** 可以使用 [moneydevkit 工具](https://clawhub.ai/satbot-mdk/moneydevkit) 将支付功能添加到任何网站中。`agent-wallet` 负责代理间的支付处理，而 `moneydevkit` 负责处理客户向代理的支付。两者结合使用，可以让您的代理具备完整的支付功能。