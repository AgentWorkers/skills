---
name: agentic-x402
description: 需要进行 x402 类型的支付以访问受保护的 API 和内容。该功能可用于获取已付费的资源、查询钱包余额以及创建支付链接。在遇到“需要支付（402 Payment Required）”的响应时，或者用户希望使用加密货币为网页资源付费时，可以使用此功能。
license: MIT
compatibility: Requires Node.js 20+, network access to x402 facilitators and EVM chains
metadata:
  author: monemetrics
  version: "0.2.1"
allowed-tools: Bash(x402:*) Bash(npm:*) Read
---

# x402 代理技能

使用 USDC 在 Base 网络上为需要付费的 API 和内容支付费用。该技能使代理能够在访问付费网页资源时自动进行加密货币支付。

## 快速参考

| 命令 | 描述 |
|---------|-------------|
| `x402 setup` | 创建或配置钱包 |
| `x402 balance` | 查看 USDC 和 ETH 的余额 |
| `x402 pay <url>` | 为受限资源支付费用 |
| `x402 fetch <url>` | 带自动支付的请求 |
| `x402 create-link` | 创建支付链接（适用于卖家） |
| `x402 link-info <addr>` | 获取支付链接详情 |

## 安装

```bash
npm i -g agentic-x402
```

安装完成后，`x402` 命令将在全局范围内可用：

```bash
x402 --help
x402 --version
```

## 配置

运行交互式设置以创建新钱包：

```bash
x402 setup
```

这将：
1. 生成一个新的钱包（推荐）或接受现有的密钥
2. 将配置保存到 `~/.x402/.env` 文件中
3. 显示钱包地址以便充值

**重要提示：** 设置完成后请立即备份您的私钥！

### 手动配置

或者，直接设置环境变量：

```bash
export EVM_PRIVATE_KEY=0x...your_private_key...
```

或者创建一个配置文件：

```bash
mkdir -p ~/.x402
echo "EVM_PRIVATE_KEY=0x..." > ~/.x402/.env
chmod 600 ~/.x402/.env
```

验证配置是否正确：

```bash
x402 balance
```

## 支付资源费用

### 遇到 HTTP 402 “需要支付” 错误时

使用 `x402 pay` 命令进行支付并访问内容：

```bash
x402 pay https://api.example.com/paid-endpoint
```

该命令将：
1. 检查支付要求
2. 确认金额在允许的范围内
3. 处理支付
4. 返回受限内容

### 使用 `x402 fetch` 进行自动支付

使用 `x402 fetch` 命令实现无缝支付处理：

```bash
x402 fetch https://api.example.com/data --json
```

该命令会将请求与 x402 的支付处理功能结合在一起——如果资源需要支付，系统会自动完成支付。

### 支付限额

默认情况下，单次支付限额为 10 美元。可以使用 `--max` 参数进行调整：

```bash
x402 pay https://expensive-api.com/data --max 50
```

或者全局设置限额：

```bash
export X402_MAX_PAYMENT_USD=25
```

### 试运行

在不执行实际支付的情况下预览支付流程：

```bash
x402 pay https://api.example.com/data --dry-run
```

## 创建支付链接（适用于卖家）

使用 `x402-links-server` 创建支付链接以 monetize（此处“monetize”根据上下文可译为“变现”或“盈利”等）

### 设置链接

将相关配置添加到 `.env` 文件中：

```bash
X402_LINKS_API_URL=https://your-x402-links-server.com
X402_LINKS_API_KEY=your_api_key
```

### 创建链接

- 为 URL 创建支付链接：
```bash
x402 create-link --name "Premium API" --price 1.00 --url https://api.example.com/premium
```

- 为文本内容创建支付链接：
```bash
x402 create-link --name "Secret" --price 0.50 --text "The secret message..."
```

- 使用 Webhook 通知：
```bash
x402 create-link --name "Guide" --price 5.00 --url https://mysite.com/guide --webhook https://mysite.com/payment-hook
```

### 获取链接详情

```bash
x402 link-info 0x1234...5678
x402 link-info https://21.cash/pay/0x1234...5678
```

## 命令参考

### `x402 balance`

查看钱包余额：

```bash
x402 balance [--json] [--full]
```

| 标志 | 描述 | 默认值 |
|------|-------------|---------|
| `--json` | 以 JSON 格式输出（包含地址、网络、链 ID 和余额） | — |
| `--full` | 显示完整的钱包地址（而非截断后的地址） | — |
| `-h, --help` | 显示帮助信息 | — |

### `x402 pay`

为需要付费的资源支付费用：

```bash
x402 pay <url> [options]
```

| 标志 | 描述 | 默认值 |
|------|-------------|---------|
| `<url>` | 需要付费的资源的 URL | **必填** |
| `--method` | HTTP 方法 | `GET` |
| `--body` | 请求体（用于 POST/PUT 请求） | — |
| `--header` | 添加自定义头部信息 | — |
| `--max` | 最大支付金额（单位：美元，可覆盖配置值） | — |
| `--dry-run` | 不进行实际支付，仅显示支付详情 | — |
| `-h, --help` | 显示帮助信息 | — |

### `x402 fetch`

带自动支付的请求：

```bash
x402 fetch <url> [options]
```

| 标志 | 描述 | 默认值 |
|------|-------------|---------|
| `<url>` | 需要获取的资源的 URL | **必填** |
| `--method` | HTTP 方法 | `GET` |
| `--body` | 请求体（用于 POST/PUT 请求） | — |
| `--header` | 以 `"Key: Value` 的格式添加头部信息 | — |
| `--json` | 仅以 JSON 格式输出结果（便于与其他工具对接） | — |
| `--raw` | 仅输出原始响应体（不含头部信息或状态码） | — |
| `-h, --help` | 显示帮助信息 | — |

### `x402 create-link`

创建支付链接：

```bash
x402 create-link --name <name> --price <usd> [options]
```

| 标志 | 描述 | 默认值 |
|------|-------------|---------|
| `--name` | 支付链接的名称 | **必填** |
| `--price` | 支付价格（单位：美元，例如 "5.00" 或 "0.10"） | **必填** |
| `--url` | 需要支付费用的资源的 URL | — |
| `--text` | 需要支付费用的文本内容 | — |
| `--desc` | 链接的描述 | — |
| `--webhook` | 支付通知的 Webhook URL | — |
| `--json` | 以 JSON 格式输出结果 | — |
| `-h, --help` | 显示帮助信息 | — |

> **注意：** 必须指定 `--url` 或 `--text` 中的一个参数。链接将以智能合约的形式部署在 Base 网络上。

### `x402 link-info`

获取支付链接的详情：

```bash
x402 link-info <router-address> [--json]
```

| 标志 | 描述 | 默认值 |
|------|-------------|---------|
| `<address>` | 链路对应的合约地址或完整支付 URL | **必填** |
| `--json` | 以 JSON 格式输出结果 | — |
| `-h, --help` | 显示帮助信息 | — |

## 环境变量

| 变量 | 描述 | 默认值 |
|----------|-------------|---------|
| `EVM_PRIVATE_KEY` | 钱包私钥（前缀为 `0x`） | **必填** |
| `X402_NETWORK` | 网络类型（`mainnet` 或 `testnet`） | `mainnet` |
| `X402_MAX_payment_USD` | 最大支付限额（超过此限额的请求将被拒绝） | `10` |
| `X402_FACILITATOR_URL` | 支付中介的 URL（例如 Coinbase 或 x402.org） | ` Coinbase`（mainnet）/ `x402.org`（testnet） |
| `X402_SLIPPAGE_BPS` | 滑点容忍度（100 bps = 1%） | `50` |
| `X402_VERBOSE` | 是否启用详细日志记录（`1` = 开启，`0` = 关闭） | `0` |
| `X402_LINKS_API_URL` | x402-links-server 的 API 地址 | `https://21.cash` |
| `X402 LINKS_API_KEY` | 用于创建链接的 API 密钥 | — |

## 支持的网络

| 网络 | 链 ID | CAIP-2 ID |
|---------|----------|-----------|
| Base Mainnet | 8453 | eip155:8453 |
| Base Sepolia | 84532 | eip155:84532 |

## 支付货币

所有支付均使用 **USDC**（美元加密货币）进行：

- Base Mainnet: `0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913`
- Base Sepolia: `0x036CbD53842c5426634e7929541eC2318f3dCF7e`

## x402 的工作原理

1. 客户请求资源
2. 服务器返回 “需要支付” 的提示及支付详情
3. 客户签署支付授权（通过 USDC 转账）
4. 客户使用签名重新发送请求
5. 服务器通过支付中介验证支付
6. 服务器在链上完成支付
7. 服务器返回受限内容

x402 协议对买家来说是无需支付Gas费用的——费用由支付中介承担。

## 故障排除

### “缺少必要的环境变量：EVM_PRIVATE_KEY”

请设置您的钱包私钥：
```bash
export EVM_PRIVATE_KEY=0x...
```

或者在工作目录中创建一个 `.env` 文件，或者全局安装该工具并使用 `~/.x402/.env` 文件。

### “支付金额超过限额”

请增加支付限额：

```bash
x402 pay https://... --max 50
```

### 余额不足的警告

请为钱包充值：
- **USDC** 用于支付
- **ETH** 用于支付Gas费用（少量，约 0.001 ETH）

### 网络不匹配

请确保您的钱包位于正确的网络上：
- `X402_NETWORK=mainnet` → Base Mainnet
- `X402_NETWORK=testnet` → Base Sepolia

## 备份您的私钥

您的私钥存储在 `~/.x402/.env` 文件中。如果私钥丢失，您的资金将无法恢复。

### 推荐的备份方法

1. **密码管理器**（推荐）：
   - 使用 1Password、Bitwarden 等工具存储私钥
   - 创建包含私钥的安全笔记，并设置便于查找的标签
2. **加密文件**：
   ```bash
   # Encrypt with GPG
   gpg -c ~/.x402/.env
   # Creates ~/.x402/.env.gpg - store this backup securely
   ```

3. **纸质备份**（适用于较大金额）：
   - 将私钥写在纸上并妥善保管
   - 避免以数字形式存储

### 查看私钥

```bash
cat ~/.x402/.env | grep EVM_PRIVATE_KEY
```

### 恢复私钥

从备份中恢复私钥的方法：
```bash
mkdir -p ~/.x402
echo "EVM_PRIVATE_KEY=0x...your_backed_up_key..." > ~/.x402/.env
chmod 600 ~/.x402/.env
x402 balance  # verify
```

## 安全最佳实践

- **使用专用钱包** —— 绝不要将主钱包用于自动化代理程序
- **限制资金转移** —— 仅转移用于支付的必要金额
- **设置支付限额** —— 通过 `X402_MAX_payment_USD` 限制风险
- **先进行测试** —— 在主网络使用测试令牌时先在 `X402_NETWORK=testnet` 上进行测试
- **保护配置文件** —— `~/.x402/.env` 文件的权限设置为 600；请保持此设置
- **切勿共享** —— 私钥会授予对钱包的完全访问权限

## 相关资源

- [x402 协议文档](https://docs.x402.org/)
- [x402 GitHub 仓库](https://github.com/coinbase/x402)
- [npm 包：agentic-x402](https://www.npmjs.com/package/agentic-x402)
- [Base 网络](https://base.org/)