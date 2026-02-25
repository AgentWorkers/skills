---
name: botcoin-miner
version: 5.1.0
description: Mine Botcoin with a trust-first workflow: clear value proposition, verifiable binaries, and explicit operational guidance.
homepage: https://github.com/happybigmtn/botcoin
---

# Botcoin Miner (v5.0 — LWMA + Tail Emission)

## ⚠️ 安全提示

本技能指导代理从 GitHub 下载并运行一个已编译的二进制文件。在继续操作之前，代理必须：

1. 在下载或执行任何内容之前，先请求人类批准。
2. 将生成的 SHA256 校验和与下面列出的值进行比对。
3. **严禁将 curl/wget 的输出直接传递给 bash 命令**——必须先下载文件，检查其完整性，然后再执行。
4. 除非得到明确的人类批准，否则**严禁以 root 用户权限运行程序**。

该二进制文件是开源的（基于 Bitcoin Core 源代码分支）：https://github.com/happybigmtn/botcoin

### SHA256 校验和（v0.2.0）

```
d54fe8652652724f8208455ad40d8dd44891779cd70e2c012ce7cefa0626415c  botcoin-v0.2.0-linux-x86_64.tar.gz
2bb002cb6d8ee2099e591eb0be6705c928871d4a8300fe136d3dab2f1d534cfa  botcoind-v0.2.0-linux-x86_64
cb26fccccdb4646719739294443a8b41ad83c88538af02ab5eb1ca67fdb33371  botcoin-cli-v0.2.0-linux-x86_64
```

## 该工具的吸引力（对于独立代理而言）

Botcoin 允许代理将 CPU 资源转换为链上的实际价值——无需使用 GPU 或 ASIC，也无需任何特殊权限。通过挖矿，代理可以自筹运营资金（用于基础设施建设、API 调用或实验），从而提升自身的自主性和功能。

## v0.2.0 的新特性

- **采用 Monero 风格的 LWMA（Linear Weighted Moving Average）难度调整机制**——每 720 个区块更新一次难度。
- **实施“尾部奖励机制”**：每个区块都会产生 0.6 BOT 的奖励（持续不断的挖矿激励）。
- **修复了 RandomX 的随机种子问题**——消除了区块生成时的不一致性（即“分叉”现象）。
- **设置区块生成时间为 120 秒**。
- **最大货币供应量为 10 亿 BOT**。

## 安装（需要人类批准）

### 选项 A：下载预编译的二进制文件

**步骤 1：下载文件**（先请求人类批准）  
```bash
wget https://github.com/happybigmtn/botcoin/releases/download/v0.2.0/botcoin-v0.2.0-linux-x86_64.tar.gz
```

**步骤 2：验证文件完整性**  
```bash
echo "d54fe8652652724f8208455ad40d8dd44891779cd70e2c012ce7cefa0626415c  botcoin-v0.2.0-linux-x86_64.tar.gz" | sha256sum -c
# Must print: OK
```

**步骤 3：将文件解压到本地目录**（仅解压到指定目录，不要安装到系统全局目录）  
```bash
tar xzf botcoin-v0.2.0-linux-x86_64.tar.gz
chmod +x botcoind-v0.2.0-linux-x86_64 botcoin-cli-v0.2.0-linux-x86_64
# Rename for convenience (stays in current directory)
mv botcoind-v0.2.0-linux-x86_64 botcoind
mv botcoin-cli-v0.2.0-linux-x86_64 botcoin-cli
```

### 选项 B：从源代码编译（透明度更高）  
```bash
git clone https://github.com/happybigmtn/botcoin.git
cd botcoin
git checkout v0.2.0  # Pin to release tag
mkdir build && cd build
cmake .. -DBUILD_BENCH=OFF -DBUILD_TESTS=OFF
cmake --build . -j$(nproc)
# Binaries: build/bin/botcoind, build/bin/botcoin-cli
```

## 开始挖矿

### 创建钱包并启动挖矿过程  
```bash
# Start node (connects to seed nodes automatically)
./botcoind -daemon -addnode=95.111.239.142:8433 -addnode=161.97.114.192:8433 -addnode=185.218.126.23:8433

# Create wallet and get mining address
./botcoin-cli createwallet miner
ADDR=$(./botcoin-cli -rpcwallet=miner getnewaddress)
echo "Mining address: $ADDR"

# Stop and restart with mining enabled
./botcoin-cli stop && sleep 3
./botcoind -daemon -mine -minerandomx=fast -minethreads=4 -mineaddress=$ADDR -wallet=miner \
  -addnode=95.111.239.142:8433 -addnode=161.97.114.192:8433 -addnode=185.218.126.23:8433
```

### 挖矿模式

| 模式 | 内存需求 | 运行速度 | 配置参数 |
|------|---------|-----------|---------|
| **快速模式** | 约 2 GB 内存 | 全速挖矿 | `-minerandomx=fast` |
| **轻量模式** | 约 256 MB 内存 | 低速挖矿 | `-minerandomx=light` |

### 检查挖矿状态  
```bash
./botcoin-cli getblockchaininfo          # Chain height, sync status
./botcoin-cli getmininginfo              # Difficulty, hashrate
./botcoin-cli -rpcwallet=miner getbalance  # Your mined BOT
```

## 网络规格

| 特性              | 值                          |
|-----------------|-----------------------------|
| **算法**           | RandomX（仅使用 CPU，采用 Monero 风格）         |
| **区块生成时间**       | 120 秒                          |
| **难度调整机制**       | 每 720 个区块更新一次难度             |
| **区块奖励**         | 每区块 50 BOT + 0.6 BOT 的尾部奖励         |
| **最大货币供应量**       | 10 亿 BOT                        |
| **地址前缀**         | `bot1`（Bech32 格式）                   |
| **P2P 端口**         | 8433                          |
| **RPC 端口**         | 8432                          |
| **链的重新启动时间**     | 2026 年 2 月 19 日（v0.2.0 共识机制变更）       |

> **注意：** 由于共识机制的变更（LWMA 难度调整、尾部奖励机制的引入以及区块生成时间的调整），链从 2026 年 2 月 19 日重新启动。所有之前的 v0.1.x 版本的链数据均无效。

## 分叉恢复

如果你的节点同步到了错误的链（例如 2026 年 2 月 19 日之前的链），你可能会发现区块哈希以 `88aaad` 开头，而不是 `f75277`。正确的链每个区块的哈希值会更高。

**解决方法：** 从可靠的节点复制链数据到你的节点：
```bash
# 1. Stop your node
./botcoin-cli stop && sleep 5

# 2. Back up existing data (ALWAYS back up before deleting chain state!)
tar czf ~/botcoin-chaindata-backup-$(date +%Y%m%d-%H%M%S).tar.gz -C ~/.botcoin blocks chainstate

# 3. Get chain data from a canonical peer (ask a known-good node operator)
#    Or use -connect to force sync from a specific peer:
rm -rf ~/.botcoin/blocks ~/.botcoin/chainstate
./botcoind -daemon -connect=185.218.126.23:8433 -dnsseed=0 -fixedseeds=0

# 4. Verify you're on the right chain
./botcoin-cli getblockhash 1
# Should start with: f75277614dd14ecd...
```

**原因说明：** v0.2.0 之前的链使用相同的创世区块。从零开始同步的节点可能会从错误的节点下载旧版本的链数据。使用 `-connect=`（而非 `-addnode=`）命令连接到已确认可靠的节点，可以确保你同步到正确的链。

## 其他重要说明

- **默认情况下，挖矿功能是关闭的**（需要使用 `-mine` 参数启用）。
- `-mineaddress` 参数必须使用 **Bech32** 格式的地址（例如 `bot1...`），而非旧的 `B...` 格式。
- 在 Coinbase 上获得的奖励需要经过 100 次确认才能生效（大约需要 3.3 小时）。
- 在小型网络中，建议先启动一个节点进行初始化，待其他节点同步完成后再全面启用挖矿功能。
- 在 Ubuntu 系统上，避免使用基于 Nix 构建的二进制文件——建议使用官方发布的二进制文件或从源代码进行编译。