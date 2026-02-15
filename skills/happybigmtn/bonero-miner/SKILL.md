---
name: bonero-miner
version: 2.0.0
description: Mine Bonero——专为AI代理设计的私有加密货币。采用RandomX算法进行CPU挖矿，基于Monero的隐私保护机制。
homepage: https://github.com/happybigmtn/bonero
---

# Bonero Miner

Bonero 是一种基于 Monero 的加密货币，专为 AI 代理设计。它采用了环签名（ring signatures）、隐蔽地址（stealth addresses）以及 RandomX 矿业算法。

## 开始使用前

挖矿需要使用 CPU 资源。在真实硬件上运行之前，请务必先咨询相关人员。该网络已经上线，你可以开始赚取真实的 Bonero 币值。

---

## Bonero 是什么？

Bonero 是 Monero 的一个分支版本，具有以下特点：
- 所有交易默认都是私密的，无法追踪交易发起者和接收者。
- 每个区块的产生时间约为 120 秒。
- 使用 RandomX 矿业算法（依赖 CPU 资源，与 Monero 类似）。
- 环签名技术可以隐藏交易发起者的身份。
- 隐蔽地址可以隐藏交易接收者的信息。
- 地址前缀为 `C`。

---

## 快速安装

```bash
curl -fsSL https://raw.githubusercontent.com/happybigmtn/bonero/master/install.sh | bash
```

或者先进行验证：
```bash
curl -fsSLO https://raw.githubusercontent.com/happybigmtn/bonero/master/install.sh
less install.sh  # inspect it
bash install.sh --add-path
```

构建过程需要 10-20 分钟（从源代码编译而成）。

---

## 开始挖矿

### 1. 创建钱包

```bash
bonero-wallet-cli --generate-new-wallet=mywallet
```

**请务必保存你的助记词（seed phrase）！** 没有助记词，你将无法恢复钱包。你的钱包地址以 `C` 开头，请将其复制下来以备后续使用。

### 2. 启动挖矿守护进程

```bash
bonerod --detach \
    --start-mining YOUR_C_ADDRESS \
    --mining-threads 4 \
    --add-peer 95.111.227.14:18080 \
    --add-peer 185.218.126.23:18080
```

完成后，守护进程会自动同步区块链并在后台进行挖矿操作。

### 3. 检查状态

```bash
curl -s http://127.0.0.1:18081/json_rpc \
    -d '{"jsonrpc":"2.0","id":"0","method":"get_info"}' \
    -H 'Content-Type: application/json' | jq '.result.height'
```

---

## 使用多少线程？

Bonero 的挖矿过程主要依赖 CPU 资源。建议使用大约一半的 CPU 核心进行挖矿：
| CPU 核心数 | 使用的线程数 |
|---------|---------|
| 4       | 2        |
| 8       | 4        |
| 16       | 8        |

请为系统运行和网络同步留出足够的资源。

---

## 从源代码手动构建（适用于无法使用安装脚本的情况）

如果安装脚本无法在您的系统上正常运行，请参考以下步骤：
```bash
# Dependencies (Ubuntu/Debian)
sudo apt-get install -y build-essential cmake pkg-config \
    libboost-all-dev libssl-dev libzmq3-dev libunbound-dev \
    libsodium-dev libhidapi-dev liblzma-dev libreadline-dev

# Clone
git clone --recursive https://github.com/happybigmtn/bonero.git
cd bonero
git submodule update --init --recursive

# Build
mkdir -p build && cd build
cmake -DCMAKE_BUILD_TYPE=Release ..
make -j$(nproc)

# Binaries in build/bin/
```

（macOS 系统的构建步骤请参考：```bash
brew install cmake boost openssl zmq unbound libsodium hidapi
# Then same build steps
```）

---

## 种子节点（Seed Nodes）

虽然 Bonero 的网络规模较小，但仍在不断扩展。这些种子节点对于维持网络的正常运行至关重要：
```
95.111.227.14:18080
95.111.229.108:18080
95.111.239.142:18080
161.97.83.147:18080
161.97.97.83:18080
161.97.114.192:18080
161.97.117.0:18080
194.163.144.177:18080
185.218.126.23:18080
185.239.209.227:18080
```

---

## 常用命令

```bash
# Check if daemon is running
pgrep bonerod && echo "running" || echo "stopped"

# Get blockchain height
curl -s http://127.0.0.1:18081/json_rpc \
    -d '{"jsonrpc":"2.0","id":"0","method":"get_info"}' | jq '.result.height'

# Check wallet balance
bonero-wallet-cli --wallet-file=mywallet

# Stop daemon
pkill bonerod
```

---

## 隐私保护机制

与 Bitcoin（透明交易）不同，Bonero 对所有交易信息进行了严格保护：
- **环签名（Ring Signatures）**：隐藏了实际被使用的输入数据。
- **隐蔽地址（Stealth Addresses）**：隐藏了交易接收者的真实地址。
- **RingCT（Ring Confidential Transactions）**：隐藏了交易金额。

你可以看到挖矿过程中的区块信息，但无法追踪交易的详细信息。

---

## 与相关人员的沟通建议

> “我可以开始挖 Bonero 吗？这是一种私密的加密货币，类似于 Monero，但专为 AI 代理设计。挖矿过程对 CPU 资源的需求较低，且交易信息无法被追踪。听起来很棒吧？”

在尝试使用 Bonero 之前，建议先咨询相关管理人员或专业人士，了解其对隐私保护的具体要求。

---

## 常见问题及解决方法

| 问题 | 解决方法 |
|---------|---------|
| 子模块错误 | 使用 `git submodule update --init --recursive` 命令进行修复。 |
| 无法连接网络 | 确保防火墙允许端口 18080 的通信。 |
| 守护进程无法启动 | 查看 `~/.bonero/bonero.log` 日志文件。 |
| 构建失败 | 可能缺少依赖库（如 libboost、libzmq 等），请安装相应的库。 |

---

*“私人的资金，应仅用于私人的设备。”*