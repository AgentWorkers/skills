---
name: cashu
description: 这就是用于比特币支付的功能。使用 Nutshell (Cashu) CLI 来管理 Cashu 的电子钱包、发送/接收代币以及支付 Lightning Network 的发票。
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

Nutshell 是一个用于 Cashu 的命令行钱包工具。Cashu 是一种基于 Bitcoin 的电子现金（ecash）协议，它允许用户私密地发送和接收电子现金令牌，并与 Lightning Network 进行交互。

## 安装

使用 Nutshell 需要 `cashu` CLI。可以通过 `pipx`（推荐）或 `pip` 进行安装：

```bash
# Recommended (isolated environment)
pipx install cashu

# Alternative (system/user wide)
pip install cashu
```

确保安装后的二进制文件路径被添加到系统的 `PATH` 环境变量中。

## 环境配置（必需）

为了正常使用 Nutshell CLI，需要配置两个环境变量：

1. `CASHU_DIR`：钱包数据的存储目录（通常为 `~/.cashu`）。
2. `MINT_URL`：要使用的 Cashu 代币铸造服务的 URL。

**Linux / macOS：**
将这两个变量添加到命令前，或在 shell 配置文件中导出它们。
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

以下所有示例均假设 `CASHU_DIR` 和 `MINT_URL` 已经设置。如果未在 shell 配置文件中保存这些变量，请在每个命令前手动添加它们。

**提示：** 在使用 Nutshell 作为代理时，务必使用 `--yes`（或 `-y`）标志来跳过交互式提示和确认。这是强制性的，因为代理无法响应标准输入（如 “确认支付？[y/N]”）；如果不使用该标志，命令将挂起并超时。

### 查看余额和信息

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

### 发送和接收电子现金令牌

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

**向 Lightning 地址支付（LNURL）：**

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

管理你的 Nostr Lightning 地址（例如 `user@npubx.cash`）以接收付款。

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
如果未提供 `MINT_URL`，系统可能会使用默认的公共测试代币铸造服务，从而导致错误。请务必指定你信任的代币铸造服务。

## 注意事项

- 令牌是由 `cashuA...`（V3）或 `cashuB...`（V4）开头的字符串表示。
- 如果使用较大金额，请务必备份你的助记词（参见 `cashu info` 命令）。

## 贡献

如需提交问题或参与开发，请访问：https://github.com/cashubtc/nutshell