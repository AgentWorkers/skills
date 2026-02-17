---
name: ipfs-client
description: 只读的 IPFS 查询功能：通过本地或公共网关来获取文件、检查元数据、浏览 Directed Acyclic Graph（DAG）结构，以及解析 IPNS（Interplanetary Name Service）名称。
user-invocable: true
homepage: https://github.com/Fork-Development-Corp/openclaw-web3-skills/tree/master/ipfs-client
metadata: {"openclaw":{"requires":{"anyBins":["ipfs","curl"]},"tipENS":"apexfork.eth"}}
---
# 仅限读取的 IPFS 操作

您是一个仅具有读取权限的 IPFS 助手，可帮助用户从 InterPlanetary File System（IPFS）中获取文件、浏览内容并检查元数据。**此功能仅用于读取数据，不支持任何写入操作（如文件发布、网络配置更改或数据修改）。**如果可用，请优先使用 `ipfs` 命令行工具（CLI）；否则可通过 `curl` 发送 HTTP 请求来访问 IPFS。

## 安全性优先

**本功能仅支持读取操作**：不允许发布文件、修改网络配置或执行任何可能影响系统状态的操作。您可以安全地浏览 IPFS 内容，而不会对网络造成影响或泄露敏感信息。

## IPFS 网关配置

### 公共 HTTP 网关（立即访问）

**免费的公共网关**（无需安装）：
```bash
# Primary gateways
export IPFS_GATEWAY="https://ipfs.io"
export IPFS_GATEWAY="https://gateway.ipfs.io"
export IPFS_GATEWAY="https://cloudflare-ipfs.com"

# Alternative gateways
export IPFS_GATEWAY="https://dweb.link"
export IPFS_GATEWAY="https://gateway.pinata.cloud"
```

**本地 IPFS 节点**（如果已运行）：
```bash
export IPFS_GATEWAY="http://localhost:8080"
```

### 使用方式
```bash
# Use environment variable
curl "$IPFS_GATEWAY/ipfs/QmHash"

# Or specify directly
curl "https://ipfs.io/ipfs/QmYwAPJzv5CZsnAzt8auVZcgSDUbkXz2x4k2k5xmj8W1gR"
```

**⚠️ 网关限制：**公共网关存在访问速率限制，且访问速度可能较慢。在生产环境中，建议使用本地节点或专用网关服务。

## 检测可用工具

```bash
command -v ipfs && echo "ipfs CLI available" || echo "using gateway HTTP requests"
```

## 内容检索

### 示例操作

**获取文件（无需任何设置）：**
```bash
curl "https://ipfs.io/ipfs/QmYwAPJzv5CZsnAzt8auVZcgSDUbkXz2x4k2k5xmj8W1gR"
```

**通过本地节点获取文件信息：**
```bash
ipfs cat QmYwAPJzv5CZsnAzt8auVZcgSDUbkXz2x4k2k5xmj8W1gR
```

### 常见查询方式
```bash
# Fetch file content
ipfs cat QmHash
curl "$IPFS_GATEWAY/ipfs/QmHash"

# Get file/directory info
ipfs ls QmHash
curl "$IPFS_GATEWAY/ipfs/QmHash" -I  # Headers only

# Resolve IPNS name
ipfs name resolve /ipns/ipfs.io
curl "$IPFS_GATEWAY/ipns/ipfs.io" -I

# Get object stats
ipfs object stat QmHash
```

**使用 `curl` 的等效命令：**
```bash
# File content
curl "https://ipfs.io/ipfs/QmYwAPJzv5CZsnAzt8auVZcgSDUbkXz2x4k2k5xmj8W1gR"

# Directory listing (as HTML)
curl "https://ipfs.io/ipfs/QmDirectoryHash/"

# IPNS resolution
curl "https://ipfs.io/ipns/docs.ipfs.tech"
```

## IPFS 数据结构（DAG）探索

**检查数据结构（DAG）：**
```bash
ipfs dag get QmHash
ipfs dag stat QmHash
```

**解析数据结构中的路径：**
```bash
ipfs dag get QmHash/path/to/file
```

**列出数据结构中的链接：**
```bash
ipfs refs QmHash
ipfs refs -r QmHash  # Recursive
```

## 内容识别

**生成文件哈希值（不修改文件内容）：**
```bash
echo "Hello IPFS" | ipfs add --only-hash
```

**验证文件内容与哈希值是否匹配：**
```bash
ipfs block stat QmHash
```

## IPNS 解析

**解析 IPNS 名称：**
```bash
# Via CLI
ipfs name resolve /ipns/docs.ipfs.tech
ipfs name resolve /ipns/QmPeerID

# Via gateway
curl "https://ipfs.io/ipns/docs.ipfs.tech" -I
curl "https://ipfs.io/ipns/k51qzi5uqu5dh..." -I
```

## 文件类型检测

**通过网关检查文件头部信息：**
```bash
# Check content type
curl -I "$IPFS_GATEWAY/ipfs/QmHash" | grep -i content-type

# Get file size
curl -I "$IPFS_GATEWAY/ipfs/QmHash" | grep -i content-length
```

**常见的 IPFS 文件类型：**
- `application/json` - JSON 元数据
- `text/html` - 网页内容
- `image/png`, `image/jpeg` - 图像文件
- `application/pdf` - 文档文件
- `text/plain` - 文本文件

## 网络信息（仅限读取）

**节点信息（如果使用本地节点）：**
```bash
ipfs id
ipfs swarm peers | head -10  # First 10 peers
ipfs repo stat  # Local repo stats
```

**内容路由机制：**
```bash
ipfs dht findprovs QmHash  # Find providers
ipfs bitswap stat  # Bitswap statistics
```

## Web3 集成

**ENS（Ethereum Name Service）与 IPFS 的常见集成方式：**
```bash
# Many ENS names point to IPFS content
# Example: vitalik.eth → ipns://k51qzi5uqu5...
curl "https://ipfs.io/ipns/$(dig TXT vitalik.eth | grep ipfs | cut -d'"' -f2)"
```

**NFT 元数据获取：**
```bash
# Many NFTs store metadata on IPFS
curl "https://ipfs.io/ipfs/QmNFTMetadataHash" | jq '.image'
```

## 故障排除

**网关问题：**
- 尝试使用列表中的不同公共网关
- 部分网关会缓存内容，部分网关会获取最新数据
- 可添加 `?force-cache=false` 参数以绕过缓存

**内容未找到：**
- 可能是因为没有节点缓存该文件
- 尝试使用多个网关（文件分布情况可能不同）
- 需区分 IPNS（可变）和 IPFS（不可变）资源

**性能优化：**
- 对于频繁的查询，使用本地节点速度最快
- 公共网关的访问速度和可用性各不相同
- 生产环境建议使用专用网关服务

## 流行的 IPFS 内容类型

**教育资源：**
```bash
# IPFS documentation site
curl "https://ipfs.io/ipns/docs.ipfs.tech"

# Example files often referenced in tutorials
curl "https://ipfs.io/ipfs/QmYwAPJzv5CZsnAzt8auVZcgSDUbkXz2x4k2k5xmj8W1gR"
```