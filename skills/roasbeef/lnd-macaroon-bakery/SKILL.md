---
name: macaroon-bakery
description: 通过最小权限代理（least-privilege agent）来烘焙、检查和管理 LND（Lightning Network Daemon）相关的 Macaroons（加密令牌）。适用于需要特定权限的代理，例如仅支付权限、仅发票权限、仅读取权限或自定义权限的场景。同时涵盖了 Macaroons 的权限设置（scoping）以及定期更新（rotation）机制。
---

# Macaroon 管理机制

我们专门制作自定义的 LND（Lightning Network）macaroons，以确保每个代理（agent）仅获得其所需的权限。在生产环境中，切勿直接使用 `admin.macaroon`，而应使用具有特定权限范围的 macaroons。

## 快速入门

```bash
# Bake a pay-only macaroon
skills/macaroon-bakery/scripts/bake.sh --role pay-only

# Bake an invoice-only macaroon
skills/macaroon-bakery/scripts/bake.sh --role invoice-only

# Bake a read-only macaroon
skills/macaroon-bakery/scripts/bake.sh --role read-only

# Inspect any macaroon
skills/macaroon-bakery/scripts/bake.sh --inspect ~/.lnd/data/chain/bitcoin/mainnet/admin.macaroon

# List all available lnd permissions
skills/macaroon-bakery/scripts/bake.sh --list-permissions
```

### Docker

`litd` 容器会自动被检测到；您也可以通过 `--container` 参数进行手动指定：

```bash
# Auto-detect litd container (default)
skills/macaroon-bakery/scripts/bake.sh --role pay-only

# Explicit container
skills/macaroon-bakery/scripts/bake.sh --role pay-only --container litd

# Inspect a macaroon inside a container
skills/macaroon-bakery/scripts/bake.sh --inspect /root/.lnd/data/chain/bitcoin/testnet/admin.macaroon --container litd
```

### 远程节点

若需在远程 LND 节点上生成 macaroons，请提供相应的连接凭据：

```bash
# Bake a pay-only macaroon on a remote node
skills/macaroon-bakery/scripts/bake.sh --role pay-only \
    --rpcserver remote-host:10009 \
    --tlscertpath ~/remote-tls.cert \
    --macaroonpath ~/remote-admin.macaroon \
    --save-to ~/remote-pay-only.macaroon
```

您需要在本机安装 `lncli`，并准备好该节点的 TLS 证书以及具有 `macaroon:generate` 权限的 macaroon 文件（通常为 `admin.macaroon`）。

## 预定义角色

| 角色 | 代理可以执行的操作 | 不能执行的操作 |
|------|----------------------|-----------|
| `pay-only` | 支付发票、解码发票、获取节点信息 | 创建发票、打开通道、查看余额 |
| `invoice-only` | 创建发票、查询发票、获取节点信息 | 支付、打开通道、查看钱包余额 |
| `read-only` | 查看信息、余额、列出通道/对等方/支付记录 | 支付、创建发票、打开/关闭通道 |
| `channel-admin` | 具有 `read-only` 的所有权限，以及打开/关闭通道、连接对等方的权限 | 支付发票、创建发票 |
| `signer-only` | 签署交易、生成密钥（适用于远程签名者） | 其他所有操作 |

## 自定义权限管理

对于未在预定义角色中涵盖的权限需求，您需要手动生成自定义 macaroons：

```bash
# Custom: agent can only pay and check wallet balance
skills/macaroon-bakery/scripts/bake.sh --custom \
    uri:/lnrpc.Lightning/SendPaymentSync \
    uri:/lnrpc.Lightning/DecodePayReq \
    uri:/lnrpc.Lightning/WalletBalance \
    uri:/lnrpc.Lightning/GetInfo

# Custom with explicit output path
skills/macaroon-bakery/scripts/bake.sh --custom \
    uri:/lnrpc.Lightning/AddInvoice \
    uri:/lnrpc.Lightning/GetInfo \
    --save-to ~/my-agent.macaroon
```

## 权限验证

```bash
# List all available URI permissions
skills/macaroon-bakery/scripts/bake.sh --list-permissions

# Filter for specific service
skills/macaroon-bakery/scripts/bake.sh --list-permissions | grep -i invoice

# Filter for routing-related permissions
skills/macaroon-bakery/scripts/bake.sh --list-permissions | grep -i router
```

## macaroons 的检查与验证

```bash
# See what permissions a macaroon has
skills/macaroon-bakery/scripts/bake.sh --inspect <path-to-macaroon>

# Inspect the admin macaroon to see full permissions
skills/macaroon-bakery/scripts/bake.sh --inspect ~/.lnd/data/chain/bitcoin/mainnet/admin.macaroon
```

## 签名者角色的权限设置

在使用 `lightning-security-module` 时，凭据包默认包含 `admin.macaroon`。在生产环境中，应在签名者机器上生成仅用于签名的 macaroon：

```bash
# On the signer container
skills/macaroon-bakery/scripts/bake.sh --role signer-only \
    --container litd-signer --rpc-port 10012

# Or on a native signer
skills/macaroon-bakery/scripts/bake.sh --role signer-only \
    --rpc-port 10012 --lnddir ~/.lnd-signer

# Then re-export the credentials bundle with the scoped macaroon
```

## macaroons 的定期更新

为降低权限泄露的风险，应定期更新 macaroons：

```bash
# 1. Bake a new macaroon with the same role
skills/macaroon-bakery/scripts/bake.sh --role pay-only --save-to ~/pay-only-v2.macaroon

# 2. Update your agent config to use the new macaroon

# 3. Delete the old macaroon's root key (invalidates it)
skills/lnd/scripts/lncli.sh bakemacaroon --root_key_id 0
# Note: use lncli listmacaroonids and deletemacaroonid for fine-grained control
```

## 最佳实践：

- **每个代理角色对应一个 macaroon**：不要将 macaroons 共享给具有不同职责的代理。
- **切勿在生产环境中使用 `admin.macaroon`**，因为它属于“ master key”（最高权限）。
- **部署前务必验证**：务必确认生成的 macaroons 具备正确的权限。
- **定期更新 macaroons**：生产环境建议每月更新一次；一旦发现安全问题，应立即更新。
- **为签名者角色设置特定权限**：远程签名者的凭据包应使用 `signer-only` 权限，而非 `admin`。
- **以严格权限设置存储 macaroons**：macaroons 是基于持有者的令牌，应像处理密码一样谨慎管理。

## 常见权限 URI

| 权限 | 描述 |
|-----------|-------------|
| `uri:/lnrpc.Lightning/GetInfo` | 节点信息（版本、公钥、同步状态） |
| `uri:/lnrpc.Lightning/WalletBalance` | 链上钱包余额 |
| `uri:/lnrpc.Lightning/ChannelBalance` | Lightning 通道余额 |
| `uri:/lnrpc.Lightning/ListChannels` | 列出已打开的通道 |
| `uri:/lnrpc.Lightning/ListPeers` | 列出连接的对等方 |
| `uri:/lnrpc.Lightning/SendPaymentSync` | 支付 Lightning 发票 |
| `uri:/lnrpc.Lightning/DecodePayReq` | 解码 BOLT11 格式的发票 |
| `uri:/lnrpc.Lightning/AddInvoice` | 创建 Lightning 发票 |
| `uri:/lnrpc.Lightning/LookupInvoice` | 根据哈希值查询发票 |
| `uri:/lnrpc.Lightning/ListInvoices` | 列出所有发票 |
| `uri:/lnrpc.Lightning/ListPayments` | 列出所有支付记录 |
| `uri:/lnrpc.Lightning/ConnectPeer` | 连接到对等方 |
| `uri:/lnrpc.Lightning/OpenChannelSync` | 打开通道 |
| `uri:/lnrpc.Lightning/CloseChannel` | 关闭通道 |
| `uri:/signrpc.Signer/SignOutputRaw` | 签署交易输出 |
| `uri:/signrpc.Signer/ComputeInputScript` | 计算签名所需的输入脚本 |
| `uri:/signrpc.Signer/MuSig2Sign` | 使用 MuSig2 算法进行签名 |
| `uri:/walletrpc.WalletKit/DeriveKey` | 生成密钥 |
| `uri:/walletrpc.WalletKit/DeriveNextKey` | 顺序生成下一个密钥 |