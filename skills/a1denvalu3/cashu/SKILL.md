---
name: cashu
description: 使用 Nutshell (cashu) CLI 来管理 Cashu 的电子钱包、发送/接收代币以及支付 Lightning 账单。它也被称为 Cashu Nutshell。
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
  MINT_URL: https://8333.space:3338
---

# Nutshell（Cashu CLI）

Nutshell 是一个用于 Cashu 的命令行钱包工具。Cashu 是一种基于比特币的电子现金（ecash）协议，它允许您私密地发送和接收电子现金令牌，并与 Lightning Network 进行交互。

## 环境配置（必需）

为了正常使用该 CLI，需要设置两个环境变量：

1. `CASHU_DIR`：钱包数据的目录（通常为 `~/.cashu`）。
2. `MINT_URL`：您要使用的 Cashu 代币铸造服务的 URL。

**Linux / macOS：**
将这两个变量添加到命令前，或在您的 shell 配置文件中导出它们。
```bash
# Per-command
CASHU_DIR=~/.cashu MINT_URL=https://mint.example.com cashu balance

# Persistent (add to ~/.bashrc or ~/.zshrc)
export CASHU_DIR=~/.cashu
export MINT_URL=https://mint.example.com
```

**Windows（PowerShell）：**
```powershell
$env:CASHU_DIR = "$HOME\.cashu"
$env:MINT_URL = "https://mint.example.com"
cashu balance
```

## CLI 使用方法

以下所有示例均假设 `CASHU_DIR` 和 `MINT_URL` 已经设置。如果未在 shell 配置文件中保存这些变量，请在每个命令前添加它们。

**提示：** 始终使用 `--yes`（或 `-y`）标志来跳过交互式提示和确认。

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

**发送 Cashu 令牌：**

```bash
# Send amount (generates a token string to share)
CASHU_DIR=~/.cashu MINT_URL=<url> cashu --yes send <amount>
# Example: CASHU_DIR=~/.cashu MINT_URL=https://8333.space:3338 cashu --yes send 100
```

**接收 Cashu 令牌：**

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

**创建 Lightning 发票（mint）：**

```bash
# Create an invoice to receive funds into the wallet
CASHU_DIR=~/.cashu MINT_URL=<url> cashu --yes invoice <amount>
```

### Lightning 地址（LNURL）

管理您的 Nostr Lightning 地址（例如 `user@npubx.cash`）以接收付款。

```bash
# Create (or display) your static Lightning Address
CASHU_DIR=~/.cashu MINT_URL=<url> cashu --yes lnurl create

# Check for pending payments sent to your address
CASHU_DIR=~/.cashu MINT_URL=<url> cashu --yes lnurl check

# Mint (claim) the pending payments
CASHU_DIR=~/.cashu MINT_URL=<url> cashu --yes lnurl mint
```

### 高级功能

```bash
# Burn spent tokens
CASHU_DIR=~/.cashu MINT_URL=<url> cashu --yes burn

# View all invoices
CASHU_DIR=~/.cashu MINT_URL=<url> cashu --yes invoices
```

## 配置

Nutshell 使用位于 `CASHU_DIR` 目录下的 `.env` 文件进行额外配置。
如果未提供 `MINT_URL`，系统可能会默认使用公共测试代币铸造服务，从而导致问题。请始终使用您信任的代币铸造服务。

## 注意事项

- 令牌是由 `cashuA...`（V3 版本）或 `cashuB...`（V4 版本）开头的字符串。
- 如果使用大量资金，请务必备份您的助记词（参见 `cashu info` 命令）。