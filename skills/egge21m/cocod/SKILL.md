---
name: cocod
skill_version: 0.0.13
requires_cocod_version: 0.0.13
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

Cocod 是一个用于管理 ecash 代币并执行 Bitcoin/Lightning 支付的 Cashu 钱包。它基于 Cashu 协议来实现保护用户隐私的 ecash 交易。

如果 Web 或 API 请求返回 HTTP `402 Payment Required` 状态码，并且带有 `X-Cashu` 标头，那么可以使用此技能来解析并处理该请求。

## 代理安全政策（必读）

在使用此技能作为代理时，请遵守以下规则：
- 在执行任何可能消耗钱包资金的命令之前，务必先获得用户的明确许可；除非用户已经明确指示您执行该操作。
- 在可能的情况下，建议先使用预览/检查命令（例如：`cocod x-cashu parse <request>`）来查看费用和所需信息，然后再执行实际操作（例如：`cocod x-cashu handle <request>`）。
- 将 `~/.cocod` 目录视为敏感文件，切勿记录、打印或公开其内容（包括配置文件、助记词、钱包状态、套接字文件以及进程 ID 文件），除非用户特别要求您提供部分内容。

## 什么是 Cashu？

Cashu 是一种基于 Chaumian 技术的 ecash 协议，允许用户私密地持有和转移由 Bitcoin 支持的代币。该协议利用盲签名技术实现不可追踪的交易。

## 安装

```bash
# Install cocod CLI
bun install -g cocod
```

## 版本兼容性

此技能依赖于特定的 `cocod` CLI 版本：
- `skill_version` 必须与 npm 包的版本相匹配。
- `requires_cocod_version` 也必须与该版本保持一致。

请检查您安装的 CLI 版本是否与文件中指定的版本相符：
```bash
cocod --version
```

如果版本不匹配，请在使用此技能之前更新 `cocod`。

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

### 核心钱包操作

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

**代理规则：**本节中的命令会消耗钱包资金。除非用户已明确授权，否则在执行前请先获得许可。

```bash
# Create Cashu token to send to someone
cocod send cashu <amount> [--mint-url <url>]

# Pay a Lightning invoice
cocod send bolt11 <invoice> [--mint-url <url>]
```

### 处理 HTTP 402 状态码的 Web 支付请求（NUT-24）

当服务器返回 HTTP `402` 状态码并带有 `X-Cashu` 标头时，请使用以下命令：
**代理规则：**`cocod x-cashu handle <request>` 可以用于执行付款操作。建议先使用 `cocod x-cashu parse <request>` 来查看付款金额和所需信息，然后再获取用户许可。

```bash
# Parse an encoded X-Cashu request from a 402 response header
cocod x-cashu parse <request>

# Settle the request and get an X-Cashu payment header value
cocod x-cashu handle <request>
```

**典型操作流程：**
1. 从服务器的 `402` 响应中提取 `X-Cashu` 标头信息。
2. 运行 `cocod x-cashu parse <request>` 来查看付款金额和所需信息。
3. 运行 `cocod x-cashu handle <request>` 以生成付款令牌。
4. 使用包含 `X-Cashu: cashuB...` 标头的请求重新发送原始 Web 请求。

### 新建代币（Mint）

```bash
# Add a mint URL
cocod mints add <url>

# List configured mints
cocod mints list

# Get mint information
cocod mints info <url>
```

### Lightning 地址（NPC）

Lightning 地址是一种类似电子邮件地址的标识符（例如：`name@npubx.cash`），用于接收 Lightning 支付。如果您尚未购买用户名，NPC 会为您提供一个免费的 Lightning 地址；购买用户名后，您将获得一个更易于识别的地址。购买用户名需要两个步骤：首先查看所需费用，然后确认支付。

**代理规则：**`cocod npc username <name> --confirm` 是一个消耗钱包资金的操作。除非用户已明确授权，否则在运行 `--confirm` 命令前请先获得许可。

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

**使用加密方式初始化钱包：**

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

**向朋友转账 Cashu：**

```bash
cocod send cashu 1000
# Returns: cashuAeyJ0b2tlbiI6...
# Friend receives with: cocod receive cashu cashuAeyJ0b2tlbiI6...
```

**查看钱包状态和余额：**

```bash
cocod status
cocod balance
```

**查看近期交易记录：**

```bash
cocod history --limit 10
```

## 相关概念：
- **Cashu**：一种使用盲签名技术的隐私保护型 ecash 协议。
- **Mint**：负责发行和赎回 Cashu 代币的服务器。
- **Token**：可转让的 Cashu 代币，代表特定数量的 Satoshi 价值。
- **Bolt11**：Lightning Network 的发票格式。
- **NPC**：用于接收 Lightning 支付的地址服务。
- **Mnemonic**：用于恢复钱包账户的助记词。