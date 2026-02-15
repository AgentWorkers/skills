---
name: lnd
description: 安装并运行 Lightning Terminal (litd)——该工具将 lnd、loop、pool、tapd 和 faraday 集合在一个 Docker 容器中。默认使用 neutrino 后端，并在测试网络 (testnet) 上采用 SQLite 作为存储方式。支持仅查看模式 (watch-only mode) 以及远程签名器 (remote signer) 的功能；同时具备独立运行模式 (standalone mode) 和用于 Regtest 开发的功能。适用于设置 Lightning 节点以进行支付、通道管理、流动性管理 (loop)、通道市场 (pool)、Taproot 资产管理 (tapd)，或启用 L402 商业功能。
---

# Lightning Terminal (litd) — Lightning Network 节点

安装并运行 Lightning Terminal (litd) 节点，以实现代理驱动的支付功能。litd 将 lnd 与 loop、pool、tapd 和 faraday 集成在一起，使代理能够在一个容器中访问流动性管理、通道市场以及 Taproot 资产。

**默认配置：** 使用 Docker 容器、neutrino 后端、SQLite 数据库，并连接到测试网络 (testnet)。无需完整的 Bitcoin 节点。如需使用主网络 (mainnet)，请使用 `--network mainnet` 参数。

**默认模式：** 仅用于监控 (watch-only)，签名操作由远程签名器 (remote signer) 完成。私钥存储在单独的签名器容器中，代理无法直接访问这些私钥。如需快速测试，可使用 `--mode standalone` 模式（私钥存储在本地磁盘上，但安全性较低）。

## 快速入门（推荐使用容器）

### 仅用于监控（生产环境）

```bash
# 1. Install litd image
skills/lnd/scripts/install.sh

# 2. Start litd + signer containers
skills/lnd/scripts/start-lnd.sh --watchonly

# 3. Set up signer wallet (first run only)
skills/lightning-security-module/scripts/setup-signer.sh --container litd-signer

# 4. Import credentials and create watch-only wallet
skills/lnd/scripts/import-credentials.sh --bundle ~/.lnget/signer/credentials-bundle
skills/lnd/scripts/create-wallet.sh

# 5. Check status
skills/lnd/scripts/lncli.sh getinfo
```

### 独立运行（仅用于测试）

```bash
# 1. Install litd image
skills/lnd/scripts/install.sh

# 2. Start litd container
skills/lnd/scripts/start-lnd.sh

# 3. Create standalone wallet (generates seed — keys on disk)
skills/lnd/scripts/create-wallet.sh --mode standalone

# 4. Check status
skills/lnd/scripts/lncli.sh getinfo
```

> **警告：** 独立运行模式会将助记词 (seed mnemonic) 和钱包密码存储在本地磁盘上。请勿在主网络环境中使用此模式，因为丢失这些信息可能导致资金损失。

### Regtest 开发模式

```bash
# Start litd + bitcoind for local development
skills/lnd/scripts/start-lnd.sh --regtest

# Create wallet and mine some blocks
skills/lnd/scripts/create-wallet.sh --container litd --mode standalone
docker exec litd-bitcoind bitcoin-cli -regtest -generate 101
```

## 容器运行模式

| 模式          | 命令                | 容器组成              | 适用场景                |
|---------------|------------------|------------------|----------------------|
| 独立运行        | `start-lnd.sh`         | litd                | 测试、开发                |
| 仅用于监控       | `start-lnd.sh --watchonly`     | litd + litd-signer         | 生产环境                |
| Regtest        | `start-lnd.sh --regtest`     | litd + litd-bitcoind         | 本地开发环境              |

## 配置文件（Profiles）

配置文件允许在不修改原始 compose 文件的情况下自定义 litd 的行为：

```bash
# List available profiles
skills/lnd/scripts/docker-start.sh --list-profiles

# Start with a profile
skills/lnd/scripts/start-lnd.sh --profile taproot
skills/lnd/scripts/start-lnd.sh --profile debug
```

| 配置文件名     | 功能                        |
|--------------|-------------------------|
| `default`      | 标准运行模式                    |
| `debug`      | 详细日志记录                  |
| `taproot`      | 启用简单的 Taproot 通道           |
| `wumbo`      | 支持最大 10 BTC 的大容量通道         |
| `regtest`      | 配置为 Regtest 网络环境         |

## 网络选择

默认使用测试网络 (testnet)。可通过 `--network` 参数进行更改：

```bash
# Testnet (default — no real coins)
skills/lnd/scripts/start-lnd.sh

# Mainnet (real coins — use with remote signer)
skills/lnd/scripts/start-lnd.sh --network mainnet --watchonly

# Signet (testing network)
skills/lnd/scripts/start-lnd.sh --network signet
```

## litd 的子进程（Sub-Daemons）

litd 包含多个子进程，可以通过 `--cli` 参数进行管理：

```bash
# lnd CLI (default)
skills/lnd/scripts/lncli.sh getinfo

# Loop — liquidity management (submarine swaps)
skills/lnd/scripts/lncli.sh --cli loop quote out 100000

# Pool — channel marketplace
skills/lnd/scripts/lncli.sh --cli pool accounts list

# Taproot Assets (tapd)
skills/lnd/scripts/lncli.sh --cli tapcli assets list

# Lightning Terminal (litd)
skills/lnd/scripts/lncli.sh --cli litcli getinfo

# Faraday — channel analytics
skills/lnd/scripts/lncli.sh --cli frcli revenue
```

## 安装

默认情况下，litd 会从 Docker Hub 下载 `lightninglabs/lightning-terminal:v0.16.0-alpha` 镜像，并对其进行验证。该镜像包含了 lncli、litcli、loop、pool 和 frcli 等组件。

### 从源代码构建（备用方案）

```bash
skills/lnd/scripts/install.sh --source
```

需要 Go 开发环境。可以从源代码构建 lnd 和 lncli，并设置相应的构建标签。

## 本地运行模式（Native Mode）

如需不使用 Docker 运行 litd，可使用 `--native` 参数：

```bash
# Start natively
skills/lnd/scripts/start-lnd.sh --native --mode standalone

# Stop natively
skills/lnd/scripts/stop-lnd.sh --native
```

本地运行模式会使用 `skills/lnd/templates/lnd.conf.template` 配置文件，并将 lnd 作为后台进程运行。

## 远程节点连接

可以使用连接凭据连接到远程的 lnd 节点：

```bash
skills/lnd/scripts/lncli.sh \
    --rpcserver remote-host:10009 \
    --tlscertpath ~/remote-tls.cert \
    --macaroonpath ~/remote-admin.macaroon \
    getinfo
```

## MCP / Lightning Node Connect

如需仅进行读取操作（无需直接使用 gRPC），可以使用 `lightning-mcp-server` 技能与 Lightning Node Connect (LNC) 连接。LNC 支持加密的 WebSocket 隧道，无需 TLS 证书、macaroons 或开放端口，只需提供 Lightning Terminal 提供的配对短语即可。

```bash
skills/lightning-mcp-server/scripts/install.sh
skills/lightning-mcp-server/scripts/configure.sh
skills/lightning-mcp-server/scripts/setup-claude-config.sh
```

## 钱包设置

### 仅用于监控的钱包（默认配置）

从远程签名器导入账户的公钥（xpub），本地设备上不存储助记词或私钥：

```bash
# Import credentials bundle from signer
skills/lnd/scripts/import-credentials.sh --bundle <credentials-bundle>

# Create watch-only wallet (auto-detects litd container)
skills/lnd/scripts/create-wallet.sh
```

### 独立运行的钱包

在本地生成助记词，仅用于测试环境。

```bash
skills/lnd/scripts/create-wallet.sh --mode standalone
```

钱包的创建流程通过 REST API 完成：
1. 生成安全的随机密码短语
2. 调用 `/v1/genseed` 生成 24 个字符的助记词
3. 使用密码短语和助记词调用 `/v1/initwallet` 函数
4. 安全存储凭据：
   - `~/.lnget/lnd/wallet-password.txt`（权限设置为 0600）
   - `~/.lnget/lnd/seed.txt`（权限设置为 0600）

### 解锁钱包

默认情况下，容器会自动解锁钱包（通过 `--wallet-unlock-password-file` 参数）。只有在自动解锁功能被禁用时才需要手动解锁。

### 从助记词恢复钱包（仅适用于独立运行模式）

```bash
skills/lnd/scripts/create-wallet.sh --mode standalone --recover --seed-file ~/.lnget/lnd/seed.txt
```

## 启动与停止

### 启动 litd

```bash
# Docker standalone (default)
skills/lnd/scripts/start-lnd.sh

# Docker watch-only (production)
skills/lnd/scripts/start-lnd.sh --watchonly

# Docker with profile
skills/lnd/scripts/start-lnd.sh --profile taproot

# Mainnet
skills/lnd/scripts/start-lnd.sh --network mainnet
```

### 停止 litd

```bash
# Stop (preserve data)
skills/lnd/scripts/stop-lnd.sh

# Stop and clean (remove volumes)
skills/lnd/scripts/stop-lnd.sh --clean

# Stop all litd containers
skills/lnd/scripts/stop-lnd.sh --all
```

## 节点操作

所有相关命令都能自动识别 litd 容器。

### 节点信息

```bash
skills/lnd/scripts/lncli.sh getinfo
skills/lnd/scripts/lncli.sh walletbalance
skills/lnd/scripts/lncli.sh channelbalance
```

### 资金注入（Funding）

```bash
skills/lnd/scripts/lncli.sh newaddress p2tr
skills/lnd/scripts/lncli.sh walletbalance
```

### 通道管理

```bash
skills/lnd/scripts/lncli.sh connect <pubkey>@<host>:9735
skills/lnd/scripts/lncli.sh openchannel --node_key=<pubkey> --local_amt=1000000
skills/lnd/scripts/lncli.sh listchannels
skills/lnd/scripts/lncli.sh closechannel --funding_txid=<txid> --output_index=<n>
```

### 支付操作

```bash
skills/lnd/scripts/lncli.sh addinvoice --amt=1000 --memo="test payment"
skills/lnd/scripts/lncli.sh decodepayreq <bolt11_invoice>
skills/lnd/scripts/lncli.sh sendpayment --pay_req=<bolt11_invoice>
skills/lnd/scripts/lncli.sh listpayments
```

### 使用 `macaroon-bakery` 技能

`macaroon-bakery` 技能允许代理使用最低权限进行操作：

```bash
skills/macaroon-bakery/scripts/bake.sh --role pay-only
skills/macaroon-bakery/scripts/bake.sh --role invoice-only
skills/macaroon-bakery/scripts/bake.sh --inspect <path-to-macaroon>
```

## 配置设置

### 容器配置

Docker compose 模板通过命令行参数传递配置信息。如需进行高级定制，可以挂载自定义的 `litd.conf` 文件：
- **litd 配置文件：** `skills/lnd/templates/litd.conf.template`
- **lnd 配置文件（本地运行模式）：** `skills/lnd/templates/lnd.conf.template`

**注意：** 在 lnd 的配置参数前需要加上 `lnd.` 前缀（例如 `lnd.bitcoin.active`）。独立运行的 lnd 不需要使用此前缀。

### 默认配置参数

- **后端服务：** neutrino（BIP 157/158 轻量级客户端）
- **数据库：** SQLite
- **网络：** 测试网络（可通过 `--network mainnet` 修改）
- **自动解锁：** 通过密码文件启用

## 容器命名与端口设置

| 容器名称       | 功能                          | 使用的端口                |
|--------------|------------------|----------------------|
| `litd`         | 主 Lightning Terminal            | 8443, 10009, 9735, 8080         |
| `litd-signer`     | 远程签名器容器                | 10012, 10013               |
| `litd-bitcoind`     | Bitcoin Core（仅用于 Regtest 环境）    | 18443, 28332, 28333            |

## 端口说明

| 端口           | 服务                          | 功能描述                        |
|---------------|------------------|-----------------------------------|
| 8443          | Lightning Terminal 用户界面        | Web 界面                          |
| 9735          | Lightning Network             | 对等点对点通信                    |
| 10009          | lncli 和程序化接口                | 用于与 lnd 通信                   |
| 8080          | REST API                        | 钱包管理等接口                      |
| 10012          | 远程签名器 RPC                    | 用于与签名器通信                   |
| 10013          | 远程签名器 REST API                | 用于与签名器通信                   |

## 文件位置

| 文件路径        | 功能                          | 说明                          |
|----------------|------------------|--------------------------------------------|
| `~/.lnget/lnd/wallet-password.txt` | 钱包解锁密码（权限设置为 0600）          |
| `~/.lnget/lnd/seed.txt` | 24 个字符的助记词备份文件（仅适用于独立运行模式） |
| `~/.lnget/lnd/signer-credentials/` | 远程签名器的凭据文件（仅用于监控模式）     |
| `versions.env`     | 容器镜像版本信息                  |
| `skills/lnd/templates/`     | Docker compose 和配置文件模板           |
| `skills/lnd/profiles/`     | 配置文件模板                      |

## 镜像版本管理

容器镜像的版本信息存储在仓库根目录下的 `versions.env` 文件中：

```bash
LITD_VERSION=v0.16.0-alpha
LND_VERSION=v0.20.0-beta
```

运行时也可以手动修改版本信息：

```bash
LITD_VERSION=v0.17.0-alpha skills/lnd/scripts/start-lnd.sh
```

## 与 lnget 的集成

在 litd 正常运行且钱包已充值、通道已建立的情况下，可以与其进行集成：

```bash
lnget config init
lnget ln status
lnget --max-cost 1000 https://api.example.com/paid-data
```

## 安全性注意事项

请参阅 [references/security.md](references/security.md) 以获取详细的安全指南。

**默认配置（仅用于监控，使用远程签名器）：**
- 代理设备上不存储助记词或私钥
- 签名操作由远程签名器容器通过 gRPC 完成
- 需要使用 `lightning-security-module` 技能进行安全配置

**独立运行模式（仅用于测试）：**
- 钱包密码和助记词存储在本地磁盘上
- 适用于测试环境和快速测试

**关于 Macaroon 的安全性：**
- 在生产环境中严禁将管理员权限的 macaroon 提供给代理
- 使用 `macaroon-bakery` 技能生成受限权限的 macaroon

## 常见问题解决方法

### “钱包未找到”
运行 `skills/lnd/scripts/create-wallet.sh` 命令来创建钱包。

### “钱包被锁定”
运行 `skills/lnd/scripts/unlock-wallet.sh` 命令。默认情况下钱包是自动解锁的。

### “链后端仍在同步”
Neutrino 需要时间来同步数据：

```bash
skills/lnd/scripts/lncli.sh getinfo | jq '{synced_to_chain, block_height}'
```

### 容器无法启动
检查 Docker 配置和网络连接是否正确。

### “无法连接到远程签名器”
确认远程签名器的地址和端口是否正确设置。

```bash
docker ps | grep litd-signer
docker logs litd-signer
```