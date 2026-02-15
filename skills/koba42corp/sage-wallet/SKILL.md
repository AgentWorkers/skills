---
name: sage-wallet
description: 通过 RPC（远程过程调用）与 Sage Chia 区块链钱包进行交互。支持执行 XCH 交易、管理 CAT 代币、NFT（非同质化代币）、DID（去中心化身份标识符）、发布交易报价、管理硬币以及配置钱包设置。该钱包支持跨平台使用（Mac/Linux/Windows），并且允许用户自定义 RPC 端点和 SSL 证书。可以通过 `/sage` 命令或自然语言指令（如 “send XCH”（发送 XCH）、”check my NFTs”（查看我的 NFT）、”create an offer”（发布交易报价）、”mint a CAT token”（铸造 CAT 代币）等来操作钱包功能。
---

# Sage 钱包技能

这是一个用于 Chia 区块链操作的 Sage 钱包的 RPC（远程过程调用）接口。

## 配置

用户设置存储在 `{workspace}/config/sage-wallet.json` 文件中：

```json
{
  "platform": "auto",
  "rpc_url": "https://127.0.0.1:9257",
  "cert_path": null,
  "key_path": null,
  "fingerprint": null,
  "auto_login": false
}
```

### 平台默认值

| 平台 | 证书路径 | 密钥路径 |
|----------|-----------|----------|
| mac | `~/Library/Application Support/com.rigidnetwork.sage/ssl/wallet.crt` | `...wallet.key` |
| linux | `~/.local/share/sage/ssl/wallet.crt` | `...wallet.key` |
| windows | `%APPDATA%\com.rigidnetwork.sage\ssl\wallet.crt` | `...wallet.key` |

当 `platform` 设置为 `"auto"` 时，通过 `uname -s` 来自动检测平台。

## 命令行命令

### 配置

| 命令 | 功能 |
|---------|--------|
| `/sage status` | 显示配置并测试连接 |
| `/sage config` | 显示当前设置 |
| `/sage config platform <auto\|mac\|linux\|windows>` | 设置平台 |
| `/sage config rpc <url>` | 设置 RPC URL |
| `/sage config cert <path>` | 设置 SSL 证书路径 |
| `/sage config key <path>` | 设置 SSL 密钥路径 |
| `/sage config fingerprint <fp>` | 设置默认钱包指纹 |
| `/sage config autologin <on\|off>` | 切换自动登录状态 |
| `/sage config reset` | 重置为默认值 |

### 操作

根据域名路由到相应的子技能：

| 域名 | 子技能 | 示例命令 |
|--------|-----------|------------------|
| 认证与密钥 | `sage-auth` | `/sage login`, `/sage logout`, `/sage keys` |
| XCH | `sage-xch` | `/sage send xch`, `/sage balance`, `/sage combine` |
| CAT 代币 | `sage-cat` | `/sage cats`, `/sage send cat`, `/sage issue cat` |
| NFT | `sage-nft` | `/sage nfts`, `/sage mint nft`, `/sage transfer nft` |
| DID | `sage-did` | `/sage dids`, `/sage create did` |
| 出价 | `sage-offers` | `/sage offers`, `/sage make offer`, `/sage take offer` |
| 选项 | `sage-options` | `/sage options`, `/sage mint option` |
| 硬币 | `sage-coins` | `/sage coins`, `/sage check address` |
| 交易 | `sage-txn` | `/sage pending`, `/sage submit` |
| 网络 | `sage-network` | `/sage peers`, `/sage network` |
| 系统 | `sage-system` | `/sage sync`, `/sage version` |
| 钱包连接 | `sage-walletconnect` | `/sage wc sign` |

### 全局参数

所有命令都支持可选的参数覆盖：

- `--fingerprint <fp>` — 使用特定的钱包 |
- `--rpc <url>` — 覆盖 RPC URL |
- `--cert <path>` — 覆盖证书路径 |
- `--key <path>` — 覆盖密钥路径 |

## 脚本

- `scripts/sage-config.sh` — 配置管理脚本 |
- `scripts/sage-rpc.sh` — 使用 mTLS 的 RPC 调用脚本 |

### 发起 RPC 调用

```bash
# Source the RPC helper
source scripts/sage-rpc.sh

# Call an endpoint
sage_rpc "get_sync_status" '{}'
sage_rpc "send_xch" '{"address":"xch1...","amount":"1000000000000","fee":"100000000"}'
```

## 子技能

每个子技能负责处理特定的功能。根据操作类型加载相应的子技能：

| 子技能 | 加载时机 |
|-----------|--------------|
| [sage-auth](sub-skills/sage-auth/SKILL.md) | 登录、登出、密钥管理、助记词 |
| [sage-xch](sub-skills/sage-xch/SKILL.md) | 发送/接收 XCH、合并/拆分硬币 |
| [sage-cat](sub-skills/sage-cat/SKILL.md) | CAT 代币操作 |
| [sage-nft](sub-skills/sage-nft/SKILL.md) | NFT 铸造、转移、收藏 |
| [sage-did](sub-skills/sage-did/SKILL.md) | DID 的创建和管理 |
| [sage-offers](sub-skills/sage-offers/SKILL.md) | 出价的创建、接受、取消 |
| [sage-options](sub-skills/sage-options/SKILL.md) | 选项协议操作 |
| [sage-coins](sub-skills/sage-coins/SKILL.md) | 硬币查询、地址验证 |
| [sage-txn](sub-skills/sage-txn/SKILL.md) | 交易签名、提交 |
| [sage-network](sub-skills/sage-network/SKILL.md) | 对等节点和网络设置 |
| [sage-system](sub-skills/sage-system/SKILL.md) | 同步状态、版本信息、数据库 |
| [sage-walletconnect](sub-skills/sage-walletconnect/SKILL.md) | 钱包连接功能 |

## 首次运行

首次调用时：

1. 检查配置文件；如果不存在则创建。
2. 如果 `platform` 设置为 `"auto"`，则自动检测平台。
3. 验证证书和密钥文件是否存在。
4. 如果文件缺失，提示用户配置路径。
5. 使用 `GetVersion` 命令测试连接。

如果找不到证书，引导用户进行配置：
```
Sage certificates not found. Configure with:
  /sage config cert /path/to/wallet.crt
  /sage config key /path/to/wallet.key
```

## 错误处理

RPC 错误会返回 HTTP 状态码：
- `400` — 请求错误（参数无效）
- `401` — 未经授权（证书不匹配）
- `404` — 未找到
- `500` — 内部错误

在处理数据之前，务必检查响应中的错误字段。

## 金额格式

Sage 使用 mojos 作为计量单位（1 XCH = 1,000,000,000,000 mojos）。请求和响应中的 `Amount` 类型是一个表示 mojos 的字符串。在显示时需要进行转换：

```
1 XCH = "1000000000000"
0.001 XCH = "1000000000"
```