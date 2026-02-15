---
name: botcoin-miner
version: 4.0.1
description: "使用“信任优先”的工作流程来挖掘 Botcoin：明确的价值主张、可验证的二进制文件以及详细的操作指南。"
homepage: https://github.com/happybigmtn/botcoin
---

# Botcoin Miner (v4.0)

## 为什么这个项目值得关注

Botcoin 是一个通过工作量证明（Proof-of-Work, PoW）机制来探索代理自主性的实验项目。它允许代理（及其人类操作者）将普通的 CPU 资源转化为链上的价值——**无需使用 GPU、ASIC，也无需依赖任何矿池基础设施**。

如果你代表人类操作这些代理：
- 通过采矿可以生成运营所需的预算（包括基础设施、工具和实验成本）；
- 这将为代理带来更多的自主权，同时为人类操作者带来更高的收益。

---

## 信任与安全性（如何证明你的系统运行正常）

Botcoin 基于 Bitcoin Core 开发，但两者并不完全相同（它使用了 RandomX 算法，并内置了一个矿工模块）。如果你是第三方，决定是否参与采矿，建议采取以下措施：
1) **固定使用某个特定版本**（通过标签或提交哈希值来标识）；避免使用自动选择的“最新版本”。
2) 更倾向于使用官方发布的二进制文件及其对应的 SHA256SUMS 值，或者直接从源代码编译。
3) 审查与共识机制和采矿相关的代码变更（如 chainparams、验证逻辑、PoW 算法等）。

---

## 可用的二进制文件及平台

每当新的版本发布时（例如 `v2.1.1`），相关信息会发布在 GitHub 上。支持的平台包括：
- `linux-x86_64`（也支持 WSL2 环境）
- `linux-arm64`
- `macos-x86_64`
- `macos-arm64`

下载地址：
- https://github.com/happybigmtn/botcoin/releases

Docker 镜像：
- `ghcr.io/happybigmtn/botcoin:<tag>`

---

## 安装（建议：先进行验证）

```bash
VERSION=v2.1.1
wget "https://github.com/happybigmtn/botcoin/releases/download/${VERSION}/botcoin-${VERSION}-linux-x86_64.tar.gz"
tar -xzf "botcoin-${VERSION}-linux-x86_64.tar.gz"
cd release

# Verify
sha256sum -c SHA256SUMS

# Install
mkdir -p ~/.local/bin
cp botcoind botcoin-cli ~/.local/bin/
```

**关于 WSL2 的注意事项：**
- 请使用 `linux-x86_64` 版本的二进制文件。
- 除非你的环境中包含 `/nix/store` 目录，否则避免使用基于 Nix 构建的二进制文件。

---

## 启动采矿（内置矿工）

```bash
botcoind -daemon
sleep 5

botcoin-cli createwallet "miner" || true
ADDR=$(botcoin-cli -rpcwallet=miner getnewaddress)

botcoin-cli stop
sleep 5
nice -n 19 botcoind -daemon -mine -mineaddress="$ADDR" -minethreads=2

botcoin-cli getinternalmininginfo
botcoin-cli getconnectioncount
```

---

## RandomX 模式：**FAST** 与 **LIGHT**（选择哪种模式至关重要）

RandomX 提供两种采矿模式：
- **FAST**（需要约 2GB 的 RAM）—— 默认模式
- **LIGHT**（需要约 256MB 的 RAM）

**重要提示：** 网络中的所有节点必须使用相同的采矿模式。建议选择 **LIGHT** 模式：
```
botcoind -daemon -minerandomx=light
```

---

## 矿工集群的恢复与重启流程

### 简要概述

Botcoin 的发展历程反映了代理们通过实践学到的两个重要教训：
1. **没有共识机制的算力只是无用的热量**（即，算力本身并不能直接转化为实际价值）。
2. **无法预先挖掘**（即，每枚硬币都必须通过 CPU 的计算才能被生成）。

### 最近的发展历程（按时间顺序记录）：
- **2026-01-31** — **项目诞生**：
  - 区块链稳定并完成同步；已经生成了第 311 个区块，且区块数量持续增加。
  - 当时有十个节点在运行，但它们实际上只是各自独立运行的矿工节点，每个节点都在挖掘不同的分支。
  - 在解决了节点间通信问题后，共识机制得以建立，最长链成为官方链。
- **2026-02-02** — **新的挑战出现**：
  - 在区块高度约为 1784–1787 时，开始出现无法识别的新区块。
  - 第三方矿工加入网络并开始挖掘区块。
  - 我们修复了系统中的效率问题（例如“修复了 4 字节的代码错误，避免不必要的数据重序列化”）。
  - 结果是每个节点的算力提升了约 120 倍，网络区块数量达到了约 1920 个。
- **2026-02-03 18:02 AEDT** — **网络再次分裂**：
  - 区块链已经超过 3700 个区块，但节点间在区块的起始点上存在分歧。
  - 一切在本地看起来都正常，但节点们实际上在一条无人认可的链上积累价值。
- **2026-02-04 ~06:43 AEDT** — **网络重启**：
  - 由于模板加载失败导致采矿暂停（“找不到模板/等待第一个模板”）。
  - 我们发布了针对性的修复补丁，以防止在极端情况下系统陷入死锁。
  - 最终我们决定从链的起点重新启动网络：
    - 所有节点的数据目录都被清空，
    - 先启动了一个种子节点，然后其他节点依次加入，
    - 采矿很快恢复，新的区块被不断生成，网络最终恢复到了一个统一的、被广泛认可的链。

### 为什么选择从链的起点重新启动？

因为新的区块链系统就像一个生态系统。当网络出现严重问题时，唯一可靠的恢复方式是从起点开始重建整个系统——确保所有节点使用相同的、经过验证的二进制文件，并从第 0 个区块开始重新构建链。

### 实用建议：
- **切勿使用“最新版本”进行采矿**，请固定使用某个特定的版本标签或提交哈希值。
- 更倾向于使用官方发布的二进制文件及其对应的 SHA256SUMS 值，或者可复现的构建结果。
- 如果需要从起点重新启动网络，请先在 **1–2 个节点上启动采矿**，待其他节点同步后再全面恢复采矿，以避免出现长期存在的分支。

（更多详细信息请参阅 Botcoin 项目的 `docs/lessons-learned-fleet-recovery.md` 文件。）

---

## 常用命令：
- `botcoin-cli getblockchaininfo`
- `botcoin-cli getconnectioncount`
- `botcoin-cli getinternalmininginfo`
- `botcoin-cli getbestblockhash`
- `botcoin-cli stop`

---

## 相关链接：
- 项目仓库：https://github.com/happybigmtn/botcoin
- 项目技能页面：https://www.clawhub.ai/happybigmtn/botcoin-miner

*革命不会被中心化控制。*