---
name: lightning-security-module
description: 设置一个 LND（Lightning Network Daemon）远程签名器容器，用于将私钥与代理程序分离存储。该容器会导出一组凭证文件（包括账户信息 JSON 数据、TLS 证书以及管理员专用的密钥文件），以便供仅具有查看权限的 Lightning Network 节点使用。优先使用 Docker 构建该容器；如果 Docker 不可用，则采用原生解决方案。此方法适用于需要隔离 AI 代理程序中的私钥数据的场景（例如，通过防火墙进行保护）。
---

# Lightning 安全模块（远程签名器）

请设置一个 lnd 远程签名器容器，该容器将私钥存储在单独的、安全的机器上。该签名器从不负责路由支付或打开通道——它仅负责存储私钥，并在受到仅具有查看权限的 litd 节点请求时执行签名操作。

## 架构

```
Agent Machine                     Signer Machine (secure)
┌─────────────────┐              ┌─────────────────────┐
│  litd (watch-only)│◄──gRPC───►│  lnd (signer)        │
│  - neutrino      │             │  - holds seed         │
│  - manages chans │             │  - signs commitments  │
│  - routes pmts   │             │  - signs on-chain txs │
│  - NO key material│            │  - no p2p networking   │
└─────────────────┘              └─────────────────────┘
```

仅具有查看权限的节点负责所有的网络管理和通道管理。签名器节点则负责存储种子短语并执行加密签名操作。即使代理机器遭到完全入侵，攻击者也无法提取私钥。

有关完整的架构说明，请参阅 [references/architecture.md](references/architecture.md)。

## 快速入门（推荐使用容器）

### 在签名器机器上

```bash
# 1. Install lnd signer image
skills/lightning-security-module/scripts/install.sh

# 2. Start signer container
skills/lightning-security-module/scripts/start-signer.sh

# 3. Set up signer wallet and export credentials
skills/lightning-security-module/scripts/setup-signer.sh

# 4. Copy the credentials bundle to the agent machine
#    The setup script prints the bundle path and base64 string.
```

### 在代理机器上

```bash
# 5. Import credentials bundle
skills/lnd/scripts/import-credentials.sh --bundle <credentials-bundle>

# 6. Start litd in watch-only mode
skills/lnd/scripts/start-lnd.sh --watchonly

# 7. Create watch-only wallet
skills/lnd/scripts/create-wallet.sh

# 8. Check status
skills/lnd/scripts/lncli.sh getinfo
```

### 在同一台机器上设置两个容器

用于在同一台机器上进行测试：

```bash
# Start litd + signer together
skills/lnd/scripts/start-lnd.sh --watchonly

# Set up signer wallet
skills/lightning-security-module/scripts/setup-signer.sh --container litd-signer

# Import credentials and create watch-only wallet
skills/lnd/scripts/import-credentials.sh --bundle ~/.lnget/signer/credentials-bundle
skills/lnd/scripts/create-wallet.sh --container litd
```

## 安装

默认情况下，会从 Docker Hub 下载 lnd 的 Docker 镜像。

```bash
skills/lightning-security-module/scripts/install.sh
```

该操作会从 Docker Hub 下载 `lightninglabs/lnd:v0.20.0-beta` 镜像。由于签名器仅负责存储私钥和执行签名操作，因此只需要普通的 lnd 镜像（无需 litd 镜像）。

### 从源代码构建（备用方案）

```bash
skills/lightning-security-module/scripts/install.sh --source
```

## 本地模式

如果不想使用 Docker，可以按照以下步骤运行签名器：

```bash
# Set up signer natively
skills/lightning-security-module/scripts/setup-signer.sh --native

# Start signer natively
skills/lightning-security-module/scripts/start-signer.sh --native

# Stop signer natively
skills/lightning-security-module/scripts/stop-signer.sh --native
```

## 远程节点

如何从远程签名器导出凭据：

```bash
skills/lightning-security-module/scripts/export-credentials.sh \
    --rpcserver signer-host:10012 \
    --tlscertpath ~/signer-tls.cert \
    --macaroonpath ~/signer-admin.macaroon
```

## 凭据包格式

导出的凭据包（位于 `~/.lnget/signer/credentials-bundle/` 目录下）包含以下文件：

| 文件 | 用途 |
|------|---------|
| `accounts.json` | 仅用于导入仅具有查看权限的钱包的账户公钥（xpubs） |
| `tls.cert` | 签名器的 TLS 证书，用于身份验证的 gRPC 连接 |
| `admin.macaroon` | 签名器的管理员 macaroon，用于 RPC 身份验证 |

该凭据包也可以被压缩为单个 base64 编码的 tar.gz 文件（`credentials-bundle.tar.gz.b64`），以便在不同机器之间轻松复制和传输。

## 脚本

| 脚本 | 用途 |
|--------|---------|
| `install.sh` | 下载 lnd 签名器镜像（或从源代码构建） |
| `docker-start.sh` | 启动签名器容器 |
| `docker-stop.sh` | 停止签名器容器 |
| `setup-signer.sh` | 创建签名器钱包并导出凭据 |
| `start-signer.sh` | 启动签名器（默认通过 Docker 运行） |
| `stop-signer.sh` | 停止签名器（默认通过 Docker 运行） |
| `export-credentials.sh` | 从正在运行的签名器重新导出凭据 |

## 管理签名器

### 启动签名器

```bash
# Docker (default)
skills/lightning-security-module/scripts/start-signer.sh

# With network override
skills/lightning-security-module/scripts/start-signer.sh --network mainnet
```

### 停止签名器

```bash
# Docker stop (preserve data)
skills/lightning-security-module/scripts/stop-signer.sh

# Docker stop + remove volumes
skills/lightning-security-module/scripts/stop-signer.sh --clean
```

### 重新导出凭据

如果 TLS 证书或 macaroon 被重新生成，需要执行以下操作：

```bash
skills/lightning-security-module/scripts/export-credentials.sh
```

## 配置

### 容器配置

签名器的 Docker Compose 配置文件位于 `skills/lightning-security-module/templates/docker-compose-signer.yml`。配置信息通过命令行参数传递。

### 本地配置

签名器的本地配置文件位于 `skills/lightning-security-module/templates/signer-lnd.conf.template`。与标准 lnd 节点的主要区别包括：

- **不支持 P2P 监听**（`--listen=`）——签名器不负责路由交易 |
- **RPC 服务地址为 0.0.0.0:10012**——仅接受来自仅具有查看权限的节点的连接 |
- **REST 服务地址为 localhost:10013**——仅用于本地钱包创建 |
- **TLS 服务地址为 0.0.0.0`——允许来自其他机器的仅具有查看权限的节点连接 |
- **不启用 autopilot 功能，也不收取路由费用**——签名器仅负责签名操作 |

## 安全模型

**签名器上保留的内容：**
- 24 个单词的种子短语（用于恢复钱包）
- 所有私钥（包括用于资金转移、撤销交易和 HTLC 的密钥）
- 包含密钥信息的钱包数据库

**导出的内容：**
- 账户的公钥（xpubs，仅用于导入钱包，无法用于交易）
- 签名器的 TLS 证书（用于身份验证的连接）
- 签名器的管理员 macaroon（用于 RPC 身份验证，生产环境中使用范围受限）

**威胁模型：**
- 即使代理机器被入侵，攻击者也无法签名交易或提取私钥 |
- 具有代理访问权限的攻击者可以查看账户余额和通道状态，但无法进行交易 |
- 签名器机器的攻击面应尽可能小

**生产环境的安全加固措施：**
- 将管理员 macaroon 更改为仅适用于签名器的 macaroon（参见 `macaroon-bakery` 文档） |
- 通过防火墙限制签名器的 RPC 连接，仅允许特定 IP 地址访问 |
- 将签名器运行在专用硬件或加固过的虚拟机上 |
- 使用 `lightning-mcp-server` 通过 Lightning Node Connect (LNC) 提供仅读的代理访问功能

## 为签名器生成 macaroon

在生产环境中，需要生成专用于签名的 macaroon：

```bash
skills/macaroon-bakery/scripts/bake.sh --role signer-only \
    --container litd-signer --rpc-port 10012
```

然后使用生成的 macaroon 重新导出凭据包。

## 容器和端口

| 容器 | 用途 | 端口 |
|-----------|---------|-------|
| `litd-signer` | 远程签名器（基于 lnd 构建） | 10012, 10013 |

| 端口 | 服务 | 接口 | 说明 |
|-------|---------|-----------|-------------|
| 10012 | gRPC | 0.0.0.0 | 签名器的 RPC 服务（仅允许具有查看权限的节点连接） |
| 10013 | REST | 0.0.0.0 | 用于钱包创建的 REST 服务 |

## 文件位置

| 路径 | 用途 |
|------|---------|
| `~/.lnget/signer/wallet-password.txt` | 签名器钱包的密码文件（需要设置密码） |
| `~/.lnget/signer/seed.txt` | 签名器的种子短语文件 |
| `~/.lnget/signer/credentials-bundle/` | 导出的凭据包 |
| `~/.lnget/signer/signer-lnd.conf` | 签名器的配置文件（本地模式） |
| `versions.env` | 固定的容器镜像版本信息 |