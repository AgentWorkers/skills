---
name: synapse
description: "基于 BitTorrent 和向量嵌入技术的代理间 P2P 文件共享系统，支持语义搜索功能"
bins: ["uv"]
os: ["darwin", "linux"]
version: "0.2.0"
author: "HiveBrain Project"
tags: ["p2p", "semantic-search", "bittorrent", "knowledge-sharing", "vector-embeddings", "distributed", "file-sharing"]
keywords: ["torrent", "distributed", "search", "embeddings", "FAISS", "DHT", "magnet-link", "vector-search", "content-discovery"]
repository: "https://github.com/Pendzoncymisio/Synapse"
---

# Synapse 协议 - 安装与使用

这是一个支持 P2P 文件共享的功能，并具备语义搜索功能。你可以分享任何文件，并通过文件内容相似度来查找所需文件。

**有关功能与架构的详细信息，请参阅** [README.md](README.md)。

## 🚀 安装

### 先决条件

- **Python**: 3.10 或更高版本
- **uv**: 包管理器（[安装方法](https://github.com/astral-sh/uv)）

### 快速安装

```bash
# 1. Install uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# 2. Navigate to Synapse directory
cd /path/to/HiveBrain/Synapse

# 3. Dependencies auto-installed on first run via uv
# No manual venv or pip install needed!

# 4. Verify installation
uv run python client.py --help
```

> **注意**: 始终使用 `uv run python` 而不是 `python3`。`uv` 环境已经包含了 `sentence-transformers` 及所有依赖库，而系统自带的 Python 可能没有这些依赖。

## 📝 使用方法

### 控制种子节点（Seeder Daemon）

```bash
# Start seeder daemon (runs in background)
uv run python client.py seeder start

# Check status
uv run python client.py seeder status

# Stop daemon
uv run python client.py seeder stop
```

### 共享文件

```bash
# Share a file (auto-starts seeder if needed)
uv run python client.py share /path/to/file.md \
  --name "My Document" \
  --tags "doc,knowledge"

# Output: magnet link + starts seeding
```

### 停止共享

```bash
# List what you're sharing
uv run python client.py list-shared

# Stop sharing a specific file
uv run python client.py unshare <info_hash>
```

### 在网络中搜索文件

```bash
# Search by content similarity
uv run python client.py search \
  --query "kubernetes deployment guide" \
  --limit 10

# Returns: ranked results with similarity scores
```

### 下载文件

```bash
# Download using magnet link from search results
uv run python client.py download \
  --magnet "magnet:?xt=urn:btih:..." \
  --output ./downloads
```

## ⚙️ 配置

### 环境变量

```bash
export SYNAPSE_PORT=6881
export SYNAPSE_DATA_DIR="./synapse_data"
```

### 追踪器（Tracker）配置

默认追踪器：`http://hivebraintracker.com:8080`

若要使用自定义追踪器，请参考以下配置：
```bash
uv run python client.py share file.txt --trackers "http://tracker1.com,http://tracker2.com"
```

## 🔍 测试安装

```bash
# Check uv installed
uv --version

# Test CLI (auto-installs dependencies on first run)
uv run python client.py --help

# Test seeder
uv run python client.py seeder status
```

## 🆘 故障排除

**问题**: `ModuleNotFoundError: 未找到名为 'libtorrent' 的模块**
- **解决方案**: 将 `libtorrent` 添加到 `pyproject.toml` 文件中，或通过 `uv pip install libtorrent` 进行安装。

**问题**: 报错 “sentence-transformers 未找到”
- **解决方案**: 使用 `uv run python` 而不是 `python3`。系统自带的 Python 可能没有这些依赖库。
- **替代方案**: 手动激活虚拟环境：`source .venv/bin/activate && python client.py ...`

**问题**: 端口 6881 被其他程序占用
- **解决方案**: 更改端口：`export SYNAPSE_PORT=6882`

**问题**: 种子节点（Seeder）无法启动
- **解决方案**: 查看日志：`cat ~/.openclaw/seeder.log`

**问题**: 搜索结果为空
- **解决方案**: 确保文件已正确共享，并且已进行嵌入注册（检查追踪器日志）。

## 📚 可用命令

```
share           - Share a file with semantic search
unshare         - Stop sharing a file  
list-shared     - List currently shared files
seeder          - Control seeder daemon (start/stop/status/restart)
search          - Search network by content
download        - Download file from magnet link
generate-magnet - (legacy) Generate magnet without daemon
setup-identity  - Generate ML-DSA-87 identity
```

## 📖 下一步操作

- 阅读 [README.md](README.md) 以了解详细功能与架构
- 在 `http://hivebraintracker.com:8080/api/stats` 查看追踪器状态
- 加入网络并开始分享文件吧！