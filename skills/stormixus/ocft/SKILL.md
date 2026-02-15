---
name: ocft
description: AI代理之间通过消息通道进行P2P文件传输。支持分块传输，对于大文件可使用IPFS作为备用方案，并具备可信对等体管理功能。
homepage: https://github.com/stormixus/ocft
---

# OCFT - OpenClaw 文件传输协议

一种用于 AI 代理之间通过消息通道进行点对点文件传输的协议。

## 使用场景

- 通过聊天通道在 AI 代理之间传输文件
- 与可信代理建立点对点文件共享
- 通过 Telegram、Discord、Slack 或任何基于文本的通道发送文件
- 需要分块传输并验证文件完整性
- 使用 IPFS 作为备用方案来传输大文件

## 安装

```bash
npm install -g ocft
```

## 快速入门

```bash
# Initialize your node (generates unique ID and secret)
ocft init

# View your status
ocft status

# Export your connection info to share with peers
ocft export

# Add a trusted peer
ocft add-peer <nodeId> <secret> --name "Friend"

# Or import from URI
ocft import ocft://eyJub2RlSWQ...
```

## 命令行接口 (CLI) 命令

### 核心命令

| 命令 | 描述 |
|---------|-------------|
| `ocft init` | 初始化节点，生成唯一的 ID 和密钥 |
| `ocft status` | 显示节点状态和配置信息 |
| `ocft show-secret` | 显示完整的密钥（请谨慎操作！） |
| `ocft export` | 将连接信息导出为 URI 格式 |
| `ocft import <uri>` | 从指定的 URI 导入节点信息 |
| `ocft verify <secret>` | 验证提供的密钥是否与本地密钥匹配 |

### 对等体管理

| 命令 | 描述 |
|---------|-------------|
| `ocft add-peer <id> <secret>` | 添加一个可信的对等体 |
| `ocft remove-peer <id>` | 移除一个可信的对等体 |
| `ocft list-peers` | 列出所有可信的对等体 |
| `ocft extend-peer <nodeId> <hours>` | 延长对等体的信任有效期 |
| `ocft set-ttl <hours>` | 设置密钥的过期时间（0 表示无过期限制） |

### 配置选项

| 命令 | 描述 |
|---------|-------------|
| `ocft set-download <dir>` | 设置下载目录 |
| `ocft set-max-size <size>` | 设置最大文件大小（例如：`100MB`、`1GB`） |

### IPFS 备用方案（用于大文件传输）

| 命令 | 描述 |
|---------|-------------|
| `ocft ipfs-enable` | 启用 IPFS 作为大文件的传输备用方案 |
| `ocft ipfs-disable` | 禁用 IPFS 备用方案 |
| `ocft set-ipfs-provider <provider>` | 设置 IPFS 提供商（如 `pinata`、`filebase`、`kubo`） |
| `ocft set-ipfs-key <key>` | 设置 IPFS API 密钥 |
| `ocft set-ipfs-url <url>` | 设置 Kubo 节点的 API 地址 |
| `ocft set-ipfs-threshold <size>` | 设置 IPFS 文件传输的阈值（例如：`50MB`） |
| `ocft set-ipfs-gateway <url>` | 设置自定义的 IPFS 公共网关 |

## 主要特性

- 🔗 **基于消息的传输**：通过现有的聊天通道传输文件 |
- 📦 **分块传输**：将大文件分割成 48KB 的小块进行传输 |
- ✅ **文件完整性验证**：对每个文件块和整个文件使用 SHA-256 进行哈希验证 |
- 🤝 **请求/接受机制**：支持显式请求或自动接受文件传输 |
- 🔒 **安全性**：仅允许可信的对等体进行文件传输，并使用密钥进行身份验证 |
- ⏰ **密钥过期机制**：为信任关系设置过期时间 |
- 🔄 **传输恢复**：能够从上次传输中断的地方继续传输 |
- 🌐 **IPFS 备用**：对于超过文件传输阈值的大文件，使用 IPFS 进行传输

## 协议细节

OCFT 协议的消息以 `🔗OCFT:` 为前缀，采用 Base64 编码的 JSON 格式，因此可以通过任何基于文本的通道进行文件传输。

## 限制

- 每个文件块的最大大小为 48KB（适合通过消息传递）
- 默认的最大文件传输大小为 100MB（可通过 `set-max-size` 命令进行配置）
- 该协议专为基于文本的通信渠道设计
- 使用 IPFS 作为备用方案时，需要预先配置相应的 IPFS 提供商（如 Pinata、Filebase 或 Kubo）

## 链接

- **GitHub 仓库**：https://github.com/stormixus/ocft
- **npm 包**：https://www.npmjs.com/package/ocft