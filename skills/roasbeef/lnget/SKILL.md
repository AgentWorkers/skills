---
name: lnget
description: 安装并使用 `lnget`——这是一个基于 Lightning 的原生 HTTP 客户端，具备自动处理 L402 支付的功能。您可以使用它来下载受 Lightning 支付墙保护的文件、管理 L402 令牌、检查 Lightning 后端状态，或者执行可能需要微支付的 HTTP 请求。
---

# lnget - 一个基于Lightning的HTTP客户端

lnget是一个类似wget/curl的命令行工具（CLI），它能够原生处理L402（Lightning HTTP 402）认证机制。当服务器返回HTTP 402状态码并附带L402认证挑战时，lnget会自动完成支付，并使用已支付的令牌重新发起请求。

**来源：** `github.com/lightninglabs/lnget`

## 快速入门

```bash
# 1. Install lnget
skills/lnget/scripts/install.sh

# 2. Initialize config (auto-detects local lnd)
lnget config init

# 3. Fetch an L402-protected resource
lnget --max-cost 1000 https://api.example.com/paid-data
```

## 安装

```bash
skills/lnget/scripts/install.sh
```

安装过程会：
- 检查Go环境是否已安装
- 运行 `go install github.com/lightninglabs/lnget/cmd/lnget@latest`
- 确保 `lnget` 已添加到系统的 `$PATH` 环境变量中

**手动安装方法：**

```bash
go install github.com/lightninglabs/lnget/cmd/lnget@latest
```

**或从源代码编译安装：**

```bash
git clone https://github.com/lightninglabs/lnget.git
cd lnget
make install
```

## 基本用法

### 下载文件

```bash
# Fetch URL (output to stdout)
lnget https://api.example.com/data.json

# Save to file
lnget -o data.json https://api.example.com/data.json

# Quiet mode for piping
lnget -q https://api.example.com/data.json | jq .

# Resume partial download
lnget -c -o largefile.zip https://api.example.com/largefile.zip

# Custom HTTP method with data
lnget -X POST -d '{"query":"test"}' https://api.example.com/search

# Custom headers
lnget -H "Accept: text/plain" https://api.example.com/data
```

### 支付控制

```bash
# Set maximum auto-pay amount (satoshis)
lnget --max-cost 5000 https://api.example.com/expensive.json

# Set maximum routing fee
lnget --max-fee 50 https://api.example.com/data.json

# Preview without paying (shows 402 challenge details)
lnget --no-pay https://api.example.com/data.json

# Custom payment timeout
lnget --payment-timeout 120s https://api.example.com/data.json
```

### 输出格式

```bash
# JSON output (default, best for programmatic use)
lnget --json https://api.example.com/data.json

# Human-readable output
lnget --human https://api.example.com/data.json

# Verbose mode (shows L402 flow details)
lnget -v https://api.example.com/data.json

# Disable progress bar
lnget --no-progress -o file.zip https://api.example.com/file.zip
```

## 子命令

### 令牌管理（`lnget tokens`）

令牌会按域名缓存在 `~/.lnget/tokens/<domain>/token.json` 文件中，并在后续请求中自动重用。

```bash
# List all cached tokens
lnget tokens list

# Show token for a specific domain
lnget tokens show api.example.com

# Remove token for a domain (forces re-authentication)
lnget tokens remove api.example.com

# Clear all tokens
lnget tokens clear --force
```

### 配置（`lnget config`）

```bash
# Initialize config file at ~/.lnget/config.yaml
lnget config init

# Show current configuration
lnget config show

# Show config file path
lnget config path
```

### 使用Lightning后端（`lnget ln`）

```bash
# Check backend connection status
lnget ln status

# Show detailed node info
lnget ln info
```

#### LNC（Lightning Node Connect）

```bash
# Pair with a node via LNC pairing phrase
lnget ln lnc pair "your-pairing-phrase"

# Ephemeral pairing (no session persistence)
lnget ln lnc pair "phrase" --ephemeral

# List saved LNC sessions
lnget ln lnc sessions

# Revoke a session
lnget ln lnc revoke <session-id>
```

#### Neutrino（嵌入式钱包）

```bash
# Initialize embedded neutrino wallet
lnget ln neutrino init

# Get address to fund wallet
lnget ln neutrino fund

# Check wallet balance
lnget ln neutrino balance

# Show sync status
lnget ln neutrino status
```

## 配置文件

配置文件位于 `~/.lnget/config.yaml`。运行 `lnget config init` 可以创建该文件。

**注意：** 由于lnget源代码中缺少某些YAML结构标签，`lnget config init` 可能会生成错误的键名（例如 `tlscertpath` 和 `macaroonpath` 代替 `tls_cert` 和 `macaroon`）。请参考下面的示例配置格式。如果你的配置文件是通过 `lnget config init` 生成的，请确认其中的键名与示例一致。

```yaml
l402:
  max_cost_sats: 1000       # Max invoice to auto-pay
  max_fee_sats: 10           # Max routing fee
  payment_timeout: 60s       # Payment timeout
  auto_pay: true             # Enable auto-payment

http:
  timeout: 30s
  max_redirects: 10
  user_agent: "lnget/0.1.0"
  allow_insecure: false

ln:
  mode: lnd                  # Options: lnd, lnc, neutrino
  lnd:
    host: localhost:10009
    tls_cert: ~/.lnd/tls.cert
    macaroon: ~/.lnd/data/chain/bitcoin/mainnet/admin.macaroon
    network: mainnet

output:
  format: json
  progress: true
  verbose: false

tokens:
  dir: ~/.lnget/tokens
```

环境变量可以通过 `LNGET_` 前缀覆盖配置文件中的设置：

```bash
export LNGET_L402_MAX_COST_SATS=5000
export LNGET_LN_MODE=lnc
export LNGET_LN_LND_HOST=localhost:10009
```

## 错误代码

| 代码 | 含义 |
|------|---------|
| 0 | 成功 |
| 1 | 一般错误 |
| 2 | 支付金额超过最大限制 |
| 3 | 支付失败 |
| 4 | 网络/连接错误 |

## L402认证流程

当lnget收到HTTP 402响应时，它会执行以下操作：
1. 解析 `WWW-Authenticate: L402 macaroon="...", invoice="..."` 头部信息
2. 解码macaroon令牌和BOLT11发票信息
3. 检查发票金额是否超过 `--max-cost` 配置的限制
4. 生成一个待支付的令牌（用于恢复请求）
5. 通过配置的Lightning后端完成支付
6. 将已支付的令牌及其预图像（preimage）存储在 `~/.lnget/tokens/<domain>/` 文件中
7. 重新发起请求时添加 `Authorization: L402 <macaroon>:<preimage>` 头部信息

对同一域名的后续请求将直接使用缓存的令牌，无需再次支付。

## 代理集成示例

### 考虑预算的文件下载策略

```bash
# Check cost before committing
result=$(lnget --no-pay --json https://api.example.com/data.json)
cost=$(echo "$result" | jq -r '.invoice_amount_sat // 0')

if [ "$cost" -le "$BUDGET" ]; then
    lnget --max-cost "$BUDGET" -q https://api.example.com/data.json
fi
```

### 解析JSON输出

```bash
# Extract just the response body
lnget --json -q https://api.example.com/data.json | jq '.body'

# Check if payment was required
lnget --json https://api.example.com/data.json | jq '.l402_paid'
```

### 在不安全的网络环境下进行测试

```bash
# For local development with aperture (no TLS)
lnget -k https://localhost:8081/api/data
```

## 文件路径说明

| 路径 | 用途 |
|------|---------|
| `~/.lnget/config.yaml` | 配置文件 |
| `~/.lnget/tokens/<domain>/` | 按域名存储令牌 |
| `~/.lnget/lnc/sessions/` | LNC会话数据 |
| `~/.lnget/neutrino/` | 嵌入式钱包数据 |