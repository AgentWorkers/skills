---
name: cocod
skill_version: 0.0.12
requires_cocod_version: 0.0.12
description: 这是一个用于比特币和Lightning支付的Cashu ecash钱包命令行工具（CLI）。它可以用于管理Cashu代币、通过Lightning（bolt11）或ecash发送/接收支付、处理HTTP 402 X-Cashu支付请求，以及查看钱包历史记录。
compatibility: Requires cocod CLI to be installed. Supports Cashu ecash protocol, Lightning Network payments, and NUT-24 HTTP 402 X-Cashu flows.
metadata:
  project: cocod
  type: cashu-wallet
  networks:
    - cashu
    - bitcoin
    - lightning
---
# Cocod – Cashu 钱包 CLI

Cocod 是一个用于管理 ecash 代币并进行 Bitcoin/Lightning 支付的 Cashu 钱包。它使用 Cashu 协议来实现保护隐私的 ecash 交易。

如果 Web 或 API 请求返回 HTTP `402 Payment Required` 错误，并带有 `X-Cashu` 标头，可以使用此技能来解析并处理该请求。

## 什么是 Cashu？

Cashu 是一种基于 Chaumian 技术的 ecash 协议，允许用户私下持有和转移由 Bitcoin 支持的代币。该协议通过盲签名技术实现不可追踪的交易。

## 安装

```bash
# Install cocod CLI
bun install -g cocod
```

## 版本兼容性

此技能依赖于特定的 `cocod` CLI 版本：

- `skill_version` 必须与 npm 包的版本相匹配。
- `requires_cocod_version` 也必须与该版本保持一致。

请检查您安装的 CLI 版本：

```bash
cocod --version
```

如果您的 CLI 版本与文件中指定的版本不匹配，请在使用此技能之前更新 `cocod`。

## 快速入门

```bash
# Initialize your wallet (generates mnemonic automatically)
cocod init

# Or with a custom mint
cocod init --mint-url https://mint.example.com

# Check balance
cocod balance
```

## 命令

### 核心钱包功能

```bash
# Check daemon and wallet status
cocod status

# Initialize wallet with optional mnemonic
cocod init [mnemonic] [--passphrase <passphrase>] [--mint-url <url>]

# Unlock encrypted wallet (only required when initialised with passphrase)
cocod unlock <passphrase>

# Get wallet balance
cocod balance

# Test daemon connection
cocod ping
```

### 接收付款

```bash
# Receive Cashu token
cocod receive cashu <token>

# Create Lightning invoice to receive
cocod receive bolt11 <amount> [--mint-url <url>]
```

### 发送付款

```bash
# Create Cashu token to send to someone
cocod send cashu <amount> [--mint-url <url>]

# Pay a Lightning invoice
cocod send bolt11 <invoice> [--mint-url <url>]
```

### 处理 HTTP 402 错误（NUT-24）

当服务器返回 HTTP `402` 错误且带有 `X-Cashu` 标头时，使用以下命令：

```bash
# Parse an encoded X-Cashu request from a 402 response header
cocod x-cashu parse <request>

# Settle the request and get an X-Cashu payment header value
cocod x-cashu handle <request>
```

**典型操作流程：**
1. 从响应中提取 `X-Cashu` 标头信息。
2. 运行 `cocod x-cashu parse <request>` 以检查付款金额和所需条件。
3. 运行 `cocod x-cashu handle <request>` 生成付款令牌的头部信息。
4. 使用返回的 `X-Cashu: cashuB...` 标头重新发起原始 Web 请求。

### 发行 Cashu 代币

```bash
# Add a mint URL
cocod mints add <url>

# List configured mints
cocod mints list

# Get mint information
cocod mints info <url>
```

### Lightning 地址（NPC）

Lightning 地址是一种类似电子邮件地址的标识符（例如 `name@npubx.cash`），可用于接收 Lightning 支付。如果您尚未购买用户名，NPC 会为您提供一个免费的地址；购买用户名后，您可以获得一个更易于阅读的地址。购买用户名需要两个步骤，以便在确认付款前查看所需的费用（satoshi）。

```bash
# Get your NPC Lightning Address
cocod npc address

# Reserve/buy an NPC username (two-step)
cocod npc username <name>
cocod npc username <name> --confirm
```

### 历史记录

```bash
# View wallet history
cocod history

# With pagination
cocod history --offset 0 --limit 20

# Watch for real-time updates
cocod history --watch

# Limit with watch
cocod history --limit 50 --watch
```

### 守护进程控制

```bash
# Start the background daemon (started automatically when not running when required)
cocod daemon

# Stop the daemon
cocod stop
```

## 示例

**使用加密初始化钱包：**

```bash
cocod init --passphrase "my-secret"
```

**通过 Lightning 接收付款：**

```bash
cocod receive bolt11 5000
# Returns: lnbc50u1... (share this invoice to receive)
```

**支付 Lightning 发票：**

```bash
cocod send bolt11 lnbc100u1p3w7j3...
```

**向朋友发送 Cashu：**

```bash
cocod send cashu 1000
# Returns: cashuAeyJ0b2tlbiI6...
# Friend receives with: cocod receive cashu cashuAeyJ0b2tlbiI6...
```

**查看账户状态和余额：**

```bash
cocod status
cocod balance
```

**查看最近的交易记录：**

```bash
cocod history --limit 10
```

## 相关概念：
- **Cashu**：一种使用盲签名技术的隐私保护型 ecash 协议。
- **Mint**：负责发行和赎回 Cashu 代币的服务器。
- **Token**：可转移的 Cashu 代币，代表一定的 Satoshi 值。
- **Bolt11**：Lightning 网络中的发票格式。
- **NPC**：用于接收付款的 Lightning 地址服务。
- **Mnemonic**：用于恢复钱包的助记词。