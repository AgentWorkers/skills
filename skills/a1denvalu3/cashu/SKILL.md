---
name: cashu
description: 这就是用于比特币支付的功能。请使用 Nutshell (Cashu) CLI 来管理 Cashu 的电子钱包、发送/接收代币以及支付 Lightning 账单。
compatibility: Requires `cashu` CLI (installed via pipx).
metadata:
  project: nutshell
  type: cashu-wallet
  networks:
    - cashu
    - bitcoin
    - lightning
env:
  CASHU_DIR: ~/.cashu
---
# Nutshell（Cashu CLI）

Nutshell 是一个用于 Cashu 的命令行钱包工具。Cashu 是基于比特币的电子现金（ecash）协议，它允许用户私密地发送和接收电子现金令牌，并与 Lightning Network 进行交互。

## 安装

使用 Nutshell 需要 `cashu` CLI。可以通过 `pipx`（推荐）或 `pip` 进行安装：

```bash
# Recommended (isolated environment)
pipx install cashu

# Alternative (system/user wide)
pip install cashu
```

请确保该二进制文件的路径已添加到您的 `PATH` 环境变量中。

## 环境配置（必需）

CLI 正常运行需要两个环境变量：

1. `CASHU_DIR`：钱包数据所在的目录（通常为 `~/.cashu`）。
2. `MINT_URL`：您要使用的 Cashu 造币服务器的 URL。

**Linux / macOS：**
将变量添加到命令前，或在您的 shell 配置文件中导出它们。
```bash
# Per-command
CASHU_DIR=~/.cashu MINT_URL=https://mint.example.com cashu balance

# Persistent (add to ~/.bashrc or ~/.zshrc)
export CASHU_DIR=~/.cashu
export MINT_URL=https://mint.example.com
```

**Windows (PowerShell：**
```powershell
$env:CASHU_DIR = "$HOME\.cashu"
$env:MINT_URL = "https://mint.example.com"
cashu balance
```

## CLI 使用方法

以下所有示例均假设 `CASHU_DIR` 和 `MINT_URL` 已设置。如果未在 shell 配置文件中设置这些变量，请在每个命令前加上它们。

**提示：** 在使用 Nutshell 作为代理时，务必使用 `--yes`（或 `-y`）标志以跳过交互式提示和确认。这是强制性的，因为代理无法响应标准输入（如 “确认支付？[y/N]”）；省略此标志会导致命令挂起或超时。

### 账户余额与信息查询

```bash
# Check wallet balance
CASHU_DIR=~/.cashu MINT_URL=<url> cashu --yes balance

# Check pending tokens
CASHU_DIR=~/.cashu MINT_URL=<url> cashu --yes pending

# Get wallet info
CASHU_DIR=~/.cashu MINT_URL=<url> cashu --yes info

# List wallets
CASHU_DIR=~/.cashu MINT_URL=<url> cashu --yes wallets
```

### 发送与接收电子现金令牌

**发送电子现金令牌：**

```bash
# Send amount (generates a token string to share)
CASHU_DIR=~/.cashu MINT_URL=<url> cashu --yes send <amount>
# Example: CASHU_DIR=~/.cashu MINT_URL=https://8333.space:3338 cashu --yes send 100
```

**接收电子现金令牌：**

```bash
# Receive a token string
CASHU_DIR=~/.cashu MINT_URL=<url> cashu --yes receive <token_string>
```

### Lightning Network

**支付 Lightning 发票（melt）：**

```bash
# Pay an invoice
CASHU_DIR=~/.cashu MINT_URL=<url> cashu --yes pay <bolt11_invoice>
```

**支付 Lightning 地址（LNURL）：**

```bash
# Pay an LNURL/Lightning Address (automatically resolves the invoice)
CASHU_DIR=~/.cashu MINT_URL=<url> cashu --yes pay <user@domain.com> <amount_sats>
# Example: CASHU_DIR=~/.cashu MINT_URL=<url> cashu --yes pay user@npubx.cash 100
```

**创建 Lightning 发票（mint）：**

```bash
# Create an invoice to receive funds into the wallet
CASHU_DIR=~/.cashu MINT_URL=<url> cashu --yes invoice <amount>
```

### Lightning 地址（LNURL）

管理您的 Nostr Lightning 地址（例如 `user@npubx.cash`）以接收支付。

```bash
# Create (or display) your static Lightning Address
CASHU_DIR=~/.cashu MINT_URL=<url> cashu --yes lnurl create

# Check for pending payments sent to your address
CASHU_DIR=~/.cashu MINT_URL=<url> cashu --yes lnurl check

# Mint (claim) the pending payments
CASHU_DIR=~/.cashu MINT_URL=<url> cashu --yes lnurl mint
```

### 支付 Cashu 402 错误（代理模式）

支持 Cashu 的 API 在收到支付请求时可能会返回 402 “Payment Required” 错误，其中包含 `X-Cashu` 标头。这种情况常见于计费 API 或需要付费的接口。

**处理流程：**
1. 发送 HTTP 请求。
2. 如果收到带有 `X-Cashu: creqA...` 标头的 402 错误，提取支付请求信息。
3. （可选）解码该请求以查看可接受的造币服务器：`cashu decode <payment_request>`
4. 进行支付：`cashu --yes pay <payment_request>`
5. 从响应中获取令牌。
6. 重新发送原始请求，并在 `X-Cashu` 标头中包含该令牌。

**造币服务器兼容性：** 支付请求可能会指定可接受电子现金的造币服务器。如果尝试使用不受支持的造币服务器进行支付，将会出错。可以使用 `cashu decode <creq>` 查看可接受的造币服务器列表。

**示例：**
```bash
# 1. Initial request (returns 402)
curl -s -i https://api.example.com/data

# Response includes:
# HTTP/1.1 402 Payment Required
# X-Cashu: creqA1...

# 2. Pay the payment request
CASHU_DIR=~/.cashu MINT_URL=<url> cashu --yes pay "creqA1..."

# Returns a token like: cashuA...

# 3. Retry with token
curl -s -H "X-Cashu: cashuA..." https://api.example.com/data
```

这种处理方式对代理非常友好：自动处理 402 错误、进行支付并重试——就像处理速率限制或身份验证重定向一样。

### 高级功能

```bash
# Burn spent tokens
CASHU_DIR=~/.cashu MINT_URL=<url> cashu --yes burn

# View all invoices
CASHU_DIR=~/.cashu MINT_URL=<url> cashu --yes invoices
```

## 配置

Nutshell 使用位于 `CASHU_DIR` 目录下的 `.env` 文件进行额外配置。
如果未提供 `MINT_URL`，系统可能会默认使用公共测试造币服务器，从而导致错误。请始终指定您信任的造币服务器。

## 注意事项

- 令牌是格式为 `cashuA...`（V3）或 `cashuB...`（V4）的长字符串。
- 如果使用大量资金，请务必备份您的助记词（参见 `cashu info`）。

## 贡献

您可以在 [https://github.com/cashubtc/nutshell](https://github.com/cashubtc/nutshell) 提交问题或贡献代码。