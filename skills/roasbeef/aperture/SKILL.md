---
name: aperture
description: 安装并运行 Aperture——这是一款来自 Lightning Labs 的 L402 Lightning 反向代理工具。您可以在创建 L402 访问控制墙、配置付费 API 端点、为其他代理托管付费内容，或测试 L402 认证流程时使用它。
---

# Aperture - L402 转发代理

Aperture 是一个基于 L402 协议的转发代理，它允许通过 Lightning Network 实现基于支付的 API 访问。该代理位于您的后端服务之前，在允许访问之前会要求客户端进行 Lightning 微支付。

**来源：** `github.com/lightninglabs/aperture`

## 快速入门

```bash
# 1. Install aperture
skills/aperture/scripts/install.sh

# 2. Generate config (connects to local lnd)
skills/aperture/scripts/setup.sh

# 3. Ensure invoice.macaroon exists (required for L402 invoice creation)
#    If not present, bake one with the macaroon-bakery skill:
skills/macaroon-bakery/scripts/bake.sh --role invoice-only \
    --save-to ~/.lnd/data/chain/bitcoin/mainnet/invoice.macaroon

# 4. Start aperture
skills/aperture/scripts/start.sh

# 5. Test with lnget
lnget -k --no-pay https://localhost:8081/api/test
```

## Aperture 的工作原理

1. 客户端通过 Aperture 请求受保护的资源。
2. Aperture 返回 HTTP 402 响应，并附带 `WWW-Authenticate: L402` 标头，其中包含一个 macaroon 和一个 Lightning 发票。
3. 客户端支付该发票并获取预图像（preimage）。
4. 客户端再次发起请求，此时请求头中包含 `Authorization: L402 <macaroon>:<preimage>`。
5. Aperture 验证令牌（token）后，将请求转发给后端服务。

## 安装

```bash
skills/aperture/scripts/install.sh
```

安装过程如下：
- 确保已安装 Go 语言。
- 运行 `go install github.com/lightninglabs/aperture/cmd/aperture@latest` 命令。
- 确保 `aperture` 命令已添加到系统的 `$PATH` 环境变量中。

**手动安装方式：**

```bash
go install github.com/lightninglabs/aperture/cmd/aperture@latest
```

**或从源代码编译安装：**

```bash
git clone https://github.com/lightninglabs/aperture.git
cd aperture
make install
```

## 设置

```bash
skills/aperture/scripts/setup.sh
```

运行 `setup` 脚本后，系统会自动生成 `~/.aperture/aperture.yaml` 配置文件（使用默认配置）。该脚本会自动检测本地的 lnd 节点路径。

**可选配置项：**

```bash
# Custom network
setup.sh --network testnet

# Custom lnd paths
setup.sh --lnd-host localhost:10009 \
         --lnd-tls ~/.lnd/tls.cert \
         --lnd-macdir ~/.lnd/data/chain/bitcoin/mainnet

# Custom listen port
setup.sh --port 8081

# Disable TLS (development only)
setup.sh --insecure

# Disable auth (no payments required)
setup.sh --no-auth
```

## 运行 Aperture

### 启动

```bash
skills/aperture/scripts/start.sh
```

将 Aperture 作为后台进程运行，它会读取 `~/.aperture/aperture.yaml` 配置文件。

**启动选项：**

```bash
start.sh --foreground         # Run in foreground
start.sh --config /path/to   # Custom config path
```

### 停止

```bash
skills/aperture/scripts/stop.sh
```

## 配置文件

配置文件位于 `~/.aperture/aperture.yaml`。

### 发票所需的 macaroon

Aperture 需要在配置的 `macdir` 目录下找到 `invoice.macaroon` 文件，以便生成用于 L402 访问请求的 Lightning 发票。此文件与 `admin.macaroon` 不同。如果缺少 `invoice.macaroon`，Aperture 无法启动，或者在客户端请求受保护资源时会返回错误。

**使用 `macaroon-bakery` 工具生成发票 macaroon：**

```bash
skills/macaroon-bakery/scripts/bake.sh --role invoice-only \
    --save-to ~/.lnd/data/chain/bitcoin/mainnet/invoice.macaroon
```

如果系统找不到 `invoice.macaroon` 文件，`setup.sh` 脚本会发出警告。

### 最小化代理配置

以下是使用本地 lnd 节点托管付费服务的最小化代理配置：

```yaml
listenaddr: "localhost:8081"
insecure: true
debuglevel: "info"
dbbackend: "sqlite"
sqlite:
  dbfile: "~/.aperture/aperture.db"

authenticator:
  network: "mainnet"
  lndhost: "localhost:10009"
  tlspath: "~/.lnd/tls.cert"
  macdir: "~/.lnd/data/chain/bitcoin/mainnet"

services:
  - name: "my-api"
    hostregexp: ".*"
    pathregexp: "^/api/.*$"
    address: "127.0.0.1:8080"
    protocol: http
    price: 100
```

### 服务配置

每个服务条目都定义了需要保护的后端服务。

```yaml
services:
  - name: "service-name"
    # Match requests by host (regex).
    hostregexp: "^api.example.com$"

    # Match requests by path (regex).
    pathregexp: "^/paid/.*$"

    # Backend address to proxy to.
    address: "127.0.0.1:8080"

    # Protocol: http or https.
    protocol: http

    # Static price in satoshis.
    price: 100

    # Macaroon capabilities granted at base tier.
    capabilities: "read,write"

    # Token expiry in seconds (31557600 = 1 year).
    timeout: 31557600

    # Paths exempt from payment.
    authwhitelistpaths:
      - "^/health$"
      - "^/public/.*$"

    # Per-endpoint rate limits (token bucket).
    ratelimits:
      - pathregexp: "^/api/query.*$"
        requests: 10
        per: 1s
        burst: 20
```

### 认证后端

#### 直接连接 lnd 节点

```yaml
authenticator:
  network: "mainnet"
  lndhost: "localhost:10009"
  tlspath: "~/.lnd/tls.cert"
  macdir: "~/.lnd/data/chain/bitcoin/mainnet"
```

#### 连接 Lightning 节点（LNC）

```yaml
authenticator:
  network: "mainnet"
  passphrase: "your-pairing-phrase"
  mailboxaddress: "mailbox.terminal.lightning.today:443"
```

#### 禁用认证

```yaml
authenticator:
  disable: true
```

### 数据库后端

- **推荐使用 SQLite：**

```yaml
dbbackend: "sqlite"
sqlite:
  dbfile: "~/.aperture/aperture.db"
```

- **PostgreSQL：**

```yaml
dbbackend: "postgres"
postgres:
  host: "localhost"
  port: 5432
  user: "aperture"
  password: "secret"
  dbname: "aperture"
```

### TLS 配置

如果未设置数据库后端，Aperture 会在 `~/.aperture/` 目录下生成自签名证书。

### 动态定价

您可以连接到一个 gRPC 价格服务器以获取动态价格信息，而不是使用固定价格。

```yaml
services:
  - name: "my-api"
    dynamicprice:
      enabled: true
      grpcaddress: "127.0.0.1:10010"
      insecure: false
      tlscertpath: "/path/to/pricer/tls.cert"
```

## 为代理托管付费内容

一种常见的用途是托管需要付费才能访问的信息。

```bash
# 1. Start a simple HTTP backend with your content
mkdir -p /tmp/paid-content
echo '{"data": "valuable information"}' > /tmp/paid-content/info.json
cd /tmp/paid-content && python3 -m http.server 8080 &

# 2. Configure aperture to protect it
skills/aperture/scripts/setup.sh --insecure --port 8081

# 3. Start aperture
skills/aperture/scripts/start.sh

# 4. Other agents can now pay and fetch
lnget --max-cost 100 https://localhost:8081/api/info.json
```

## 与 lnget 和 lnd 的集成

当所有组件都运行正常时，您可以实现以下集成：

```bash
# Verify lnd is running
skills/lnd/scripts/lncli.sh getinfo

# Start aperture (uses same lnd for invoice generation)
skills/aperture/scripts/start.sh

# Fetch a paid resource
lnget --max-cost 1000 https://localhost:8081/api/data

# Check tokens
lnget tokens list
```

## 文件位置

| 文件路径 | 用途 |
|------|---------|
| `~/.aperture/aperture.yaml` | 配置文件 |
| `~/.aperture/aperture.db` | SQLite 数据库 |
| `~/.aperture/tls.cert` | TLS 证书 |
| `~/.aperture/tls.key` | TLS 私钥 |
| `~/.aperture/aperture.log` | 日志文件 |

## 故障排除

### 端口已被占用
请将配置文件中的 `listenaddr` 更改为其他端口，或使用 `setup.sh --port` 命令指定端口号。

### 无法连接到 lnd 节点
请确认 lnd 服务正在运行且钱包已解锁。检查配置文件中的 `lndhost`、`tlspath` 和 `macdir` 是否指向正确的 lnd 实例。

### 未返回 402 响应
请确认请求路径与服务的 `pathregexp` 匹配，并且不在 `authwhitelistpaths` 列表中。同时确认 `authenticator.disable` 的值不是 `true`。

### 令牌验证失败
客户端必须提供与挑战中要求的 macaroon 完全匹配的令牌，以及正确的预图像（preimage）。请确认预图像与支付哈希值一致。