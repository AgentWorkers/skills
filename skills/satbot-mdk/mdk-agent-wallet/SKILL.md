---
name: agent-wallet
description: 适用于AI代理的自托管比特币Lightning钱包。当代理需要发送或接收比特币付款、查询余额、生成发票或管理钱包时，可以使用该钱包。支持bolt11、bolt12、LNURL和Lightning地址。无需任何配置——只需一条命令即可完成初始化。
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

该工具使用了 [MoneyDevKit] 发布的 npm 包 `@moneydevkit/agent-wallet`，其功能包括：

- **生成并存储 BIP39 密语**，该密语将作为您的私钥（请将其视为密码并妥善保管）。
- **在 `localhost:3456` 上运行本地守护进程**，作为钱包操作的 HTTP 服务器。该服务器仅允许本地访问，无法从外部访问。
- **与 MDK 的 Lightning 基础设施建立连接**。
- **将支付记录保存在 `~/.mdk-wallet/` 目录中**。

除了标准的 Lightning 协议操作外，没有任何数据会被发送到外部服务器。您可以通过查看 [源代码](https://github.com/anthropics/moneydevkit) 或发布的 npm 压缩包来验证这一点。

### 安全保障措施：

- **仅限本地访问**：守护进程的 HTTP 服务器仅绑定到 `127.0.0.1:3456`，无法通过网络或其他设备访问。
- **文件权限设置**：配置文件和支付相关文件的权限设置为 `0600`（仅所有者可读写），配置目录的权限设置为 `0700`。
- **无数据泄露风险**：守护进程仅通过标准 Lightning 协议与 MDK 的 Lightning 基础设施进行通信，不收集任何遥测数据或第三方报告信息。
- **Webhook URL 由用户配置**：支付通知的 webhook 仅发送到用户通过 `config-webhook` 显式设置的 URL；默认情况下，Webhook 是关闭的。
- **密语严格保存在本地**：BIP39 密语不会被传输、记录或包含在 webhook 数据中。
- **在生产环境中固定版本**：使用 `npx @moneydevkit/agent-wallet@0.12.0` 来锁定特定版本，以避免因使用 `@latest` 而导致的供应链风险。

## 快速入门

```bash
# Initialize wallet (generates mnemonic)
npx @moneydevkit/agent-wallet@0.12.0 init

# Get balance
npx @moneydevkit/agent-wallet@0.12.0 balance

# Create invoice
npx @moneydevkit/agent-wallet@0.12.0 receive 1000

# Pay someone
npx @moneydevkit/agent-wallet@0.12.0 send user@getalby.com 500
```

## 工作原理

首次执行命令时，CLI 会自动启动守护进程。该进程：
- 在 `localhost:3456` 上运行本地 HTTP 服务器。
- 连接到 MDK 的 Lightning 基础设施。
- 每 30 秒轮询一次新的支付请求。
- 将支付记录保存到 `~/.mdk-wallet/` 目录中。

您可以选择配置 webhook，以便在收到支付时立即收到通知。

## 设置

### 首次初始化

```bash
npx @moneydevkit/agent-wallet@0.12.0 init
```

执行此命令后：
- **生成一个 BIP39 密语**（12 个单词的助记短语，即您的钱包密钥）。
- 在 `~/.mdk-wallet/config.json` 中创建配置文件。
- 根据密语生成一个唯一的 8 位十六进制钱包 ID（`walletId`）。
- 启动守护进程（在端口 3456 上运行本地 Lightning 节点）。

钱包立即可用，无需 API 密钥或注册账户。代理自行管理其私钥。

### 查看现有配置

```bash
npx @moneydevkit/agent-wallet@0.12.0 init --show
```

执行此命令后，将返回以下内容：
```json
{
  "mnemonic": "...",
  "network": "mainnet",
  "walletId": "..."
}
```

**注意：** `init` 命令不会覆盖现有的钱包配置。如需重新初始化，请执行相应的命令。

## 命令列表

所有命令的输出均为 JSON 格式。成功时返回 0，失败时返回 1。

| 命令        | 描述                                      |
|-------------|-----------------------------------------|
| `init`       | 生成密语并创建配置文件                         |
| `init --show`    | 显示配置文件（密语部分会被隐藏）                         |
| `start`      | 启动守护进程                                   |
| `balance`     | 查看钱包余额（单位：sats）                         |
| `receive <amount>`  | 生成支付请求                             |
| `receive`     | 生成可变金额的支付请求                         |
| `receive <amount> --description "..."` | 生成带有自定义描述的支付请求                   |
| `receive-bolt12`  | 生成可重复使用的 BOLT12 支付请求                   |
| `send <destination> [amount]` | 向指定地址支付（支持 bolt11、bolt12、LNURL 或 Lightning 地址）     |
| `payments`     | 查看支付历史记录                             |
| `status`     | 检查守护进程是否正在运行                         |
| `config-webhook <url>` | 设置支付通知的 webhook URL                         |
| `config-webhook <url> --secret <token>` | 设置带有认证令牌的 webhook URL                         |
| `config-webhook --clear` | 删除 webhook URL 和认证令牌                         |
| `stop`      | 停止守护进程                                   |
| `restart`    | 重启守护进程                                   |

### 查看余额

```bash
npx @moneydevkit/agent-wallet@0.12.0 balance
```
执行此命令后，将返回以下内容：
```json
{
  "balance_sats": 3825
}
```

### 收到支付请求（生成支付请求）

```bash
# Fixed amount
npx @moneydevkit/agent-wallet@0.12.0 receive 1000

# Variable amount (payer chooses)
npx @moneydevkit/agent-wallet@0.12.0 receive

# With description
npx @moneydevkit/agent-wallet@0.12.0 receive 1000 --description "payment for service"
```
执行此命令后，将返回以下内容：
```json
{
  "invoice": "lnbc...", "payment_hash": "...", "expires_at": "..."
}
```

### 接收 BOLT12 支付请求

```bash
npx @moneydevkit/agent-wallet@0.12.0 receive-bolt12
```
执行此命令后，将返回以下内容：
```json
{
  "offer": "lno1..."
}
```

BOLT12 支付请求是可重复使用的，且没有有效期；您只需分享一次支付请求即可接收多次付款。与 BOLT11 不同，付款方可以自行选择付款金额。

### 发送支付请求

```bash
npx @moneydevkit/agent-wallet@0.12.0 send <destination> [amount_sats]
```

**发送方式说明：**
- **bolt11 支付请求**：格式为 `lnbc10n1...`（金额已编码，无需额外参数）。
- **bolt12 支付请求**：格式为 `lno1...`。
- **Lightning 地址**：例如 `user@example.com`。
- **LNURL**：格式为 `lnurl1...`。对于 Lightning 地址或 LNURL，需要提供付款金额。

### 查看支付历史记录

```bash
npx @moneydevkit/agent-wallet@0.12.0 payments
```
执行此命令后，将返回以下内容：
```json
{
  "payments": [
    {
      "paymentHash": "...",
      "amountSats": 1000,
      "direction": "inbound" || "outbound",
      "timestamp": "...",
      "destination": "..."
    }
  ]
}
```

## 升级

```bash
# Stop the running daemon
npx @moneydevkit/agent-wallet@0.12.0 stop

# Run with @latest to pull the newest version
npx @moneydevkit/agent-wallet@0.12.0 start
```

您的钱包配置和支付记录会保存在 `~/.mdk-wallet/` 目录中，升级过程中这些数据不会丢失。

## Webhook 功能

收到支付请求时，系统会立即通知您（无需轮询或手动确认）。

### 设置 webhook

**设置完成后，请重启守护进程**，以便 webhook 能够生效：

```bash
npx @moneydevkit/agent-wallet@0.12.0 restart
```

### Webhook 数据传输

当收到支付请求时，守护进程会向配置的 URL 发送 POST 请求：

```json
{
  "message": "Lightning payment received: 1000 sats (payment_hash: abc123...). Your new wallet balance is 50000 sats.",
  "name": "agent-wallet",
  "deliver": true,
  "event": "payment_received",
  "payment_hash": "abc123...",
  "amount_sats": 1000,
  "payer_note": "optional note from sender",
  "new_balance_sats": 50000,
  "timestamp": 1709123456789
}
```

Webhook 采用“一次使用即失效”的机制（超时时间为 5 秒，操作是异步的），不会阻塞支付处理流程。如果守护进程重启，重复的支付通知会被自动忽略。

### 高级功能：`webhookBody` 的使用

您可以在 `~/.mdk-wallet/config.json` 中添加 `webhookBody` 对象，以指定消息的传输渠道。这样无需修改钱包代码即可灵活控制消息的发送方式：

```json
{
  "webhookBody": {
    "channel": "signal",
    "to": "group:your-group-id-here"
  }
}
```

### 与 OpenClaw 的集成

要将支付通知发送到聊天平台，可以按照以下步骤操作：

**1. 启用 OpenClaw 的 webhook 功能**（只需执行一次）：

```bash
openclaw config set hooks.enabled true
openclaw config set hooks.token "$(openssl rand -hex 16)"
openclaw gateway restart
```

**2. 将 agent-wallet 配置为指向 `/hooks/agent`：**

```bash
# Get your hooks token
openclaw config get hooks.token

# Configure agent-wallet
npx @moneydevkit/agent-wallet@0.12.0 config-webhook http://127.0.0.1:18789/hooks/agent --secret <your-hooks-token>
```

**3. 在 `~/.mdk-wallet/config.json` 中设置接收地址：**

在配置文件中添加包含目标渠道和接收者的 `webhookBody` 对象：

```json
{
  "webhookBody": {
    "channel": "signal",
    "to": "group:your-signal-group-id"
  }
}
```

其他可用的渠道包括：`telegram`、`discord`、`slack`、`whatsapp`、`imessage`。`to` 字段表示接收者的标识（例如群组 ID、聊天 ID 或电话号码）。

**4. 重启守护进程**：

```bash
npx @moneydevkit/agent-wallet@0.12.0 restart
```

现在，每当有支付请求时，OpenClaw 会自动在指定聊天平台中通知您。代理会显示支付详情并发送确认消息，无需用户进行额外确认。

**内部工作原理：**
- agent-wallet 通过 `/hooks/agent` 发送带有 `deliver: true` 标志的 POST 请求。
- OpenClaw 会启动一个独立的代理会话来处理支付通知。
- 代理的响应会被发送到指定的渠道或接收者。
- 从接收到支付到通知显示整个过程大约需要 5 秒。

### 环境变量

- `MDK_WALLET_WEBHOOK_URL`：用于覆盖 webhook URL。
- `MDK_WALLET_WEBHOOK_SECRET`：用于覆盖 webhook 的认证令牌。

## 使用注意事项：

- **金额单位**：使用 `₿` 前缀表示 sat（例如 `₿1,000`，而不是 “1,000 sats”）。
- **自托管模式**：密语即为钱包的私钥，请务必妥善备份。丢失密语意味着资金也会丢失。
- **守护进程**：在 `:3456` 端口上运行本地 Lightning 节点，会自动启动并保存配置到磁盘。
- **代理间支付**：使用此钱包的任何代理都可以向其他代理的账户或 Lightning 地址进行支付。

## 下一步？

**希望接收客户的付款吗？** 可以使用 [moneydevkit 工具](https://clawhub.ai/satbot-mdk/moneydevkit) 将支付功能集成到您的网站中。`agent-wallet` 负责代理间的支付处理，而 `moneydevkit` 负责处理客户向代理的支付。两者结合使用，可以让您的 AI 代理具备完整的支付处理能力。