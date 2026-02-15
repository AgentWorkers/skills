---
name: bittensor-sdk
description: 全面的 Bittensor 区块链交互功能，包括钱包管理、质押、子网操作、神经元注册以及排放量追踪。适用于以下场景：Bittensor 操作、子张量查询、TAO 的质押/解质押、神经元注册、子网信息查询、钱包操作、元图分析、排放量追踪以及权重管理。
license: MIT
compatibility: Requires Python 3.8+, bittensor>=8.0.0, network access to Bittensor network endpoints
metadata:
  author: bittensor_quest
  version: "1.0.0"
---

# Bittensor SDK 技能

这是一项全面的 Bittensor 区块链交互技能，使代理能够通过 Python SDK 无缝地与 Bittensor 分布式 AI 网络进行交互。

## 概述

Bittensor 是一个去中心化的机器学习网络，其中各个子网会竞争 TAO 代币的发行权。该技能为代理提供了以下全部功能：

- **钱包管理**：支持冷钥/热钥操作以及代理关系管理
- **质押操作**：可以质押/解质押 TAO、自动质押以及安全质押
- **子网管理**：查询子网信息、超参数以及子网注册
- **神经元操作**：注册神经元、查询元图以及权重管理
- **发行与奖励**：跟踪代币发行情况、领取根节点分红以及奖励分配

## 关键概念

### 核心术语

- **冷钥（Coldkey）**：用户用于转账和整体钱包管理的主钱包密钥
- **热键（Hotkey）**：用于神经元操作（挖矿/验证）的密钥
- **Netuid**：子网的唯一标识符（0 表示根子网）
- **UID**：特定子网上神经元的唯一标识符
- **元图（Metagraph）**：给定区块下子网的完整状态
- **TAO**：基础网络代币（1 TAO = 1e9 Rao）
- **Alpha**：代表已质押 TAO 的子网专用代币
- **Rao**：TAO 的最小单位

### 网络类型

- **finney**：Bittensor 主网
- **test**：Bittensor 测试网络
- **local**：本地部署的区块链

## 安装

### 先决条件

```bash
pip install bittensor>=8.0.0
```

### Opencode 安装

```bash
cp -r skills/bittensor-sdk ~/.opencode/skills/
```

## 工作原理

### 1. 初始化

该技能会初始化 Subtensor 接口以进行区块链交互：

```python
import bittensor as bt

# Connect to mainnet
subtensor = bt.Subtensor(network="finney")

# Connect to testnet
subtensor = bt.Subtensor(network="test")

# Custom network with fallback endpoints
subtensor = bt.Subtensor(
    network="finney",
    fallback_endpoints=["wss://entrypoint-finney.opentensor.ai:443"],
    retry_forever=True
)
```

### 2. 钱包设置

```python
from bittensor import wallet

# Load existing wallet
wallet = bt.Wallet()

# Create new wallet
wallet = bt.Wallet(name="my_wallet", hotkey="miner1")

# Check balances
coldkey_balance = wallet.coldkey_balance
print(f"Coldkey balance: {coldkey_balance}")
```

### 3. 核心操作

#### 查询子网信息

```python
# Get all subnet netuids
netuids = subtensor.get_all_subnets_netuid()
print(f"Available subnets: {netuids}")

# Get detailed subnet info
subnet_info = subtensor.get_subnet_info(netuid=1)
print(f"Subnet 1 info: {subnet_info}")
```

#### 质押 TAO

```python
from bittensor import Balance

# Stake TAO to a hotkey
amount = Balance.from_tao(10.0)  # 10 TAO
result = subtensor.add_stake(
    wallet=wallet,
    netuid=1,
    hotkey_ss58="5Hx...",  # Hotkey SS58 address
    amount=amount,
    safe_staking=True,     # Enable price protection
    allow_partial_stake=True
)
print(f"Stake result: {result}")
```

#### 注册神经元

```python
# Burned registration (recycle TAO)
result = subtensor.burned_register(
    wallet=wallet,
    netuid=1
)

# POW registration (computational proof)
result = subtensor.register(
    wallet=wallet,
    netuid=1
)
```

#### 查询元图

```python
# Get metagraph for a subnet
metagraph = subtensor.metagraph(netuid=1)

print(f"Number of neurons: {metagraph.n}")
print(f"Stake per neuron: {metagraph.S}")
print(f"Rewards: {metagraph.R}")
print(f"Hotkeys: {metagraph.hotkeys}")
```

#### 设置权重

```python
import numpy as np

# Validator sets weights for miners
uids = np.array([0, 1, 2, 3, 4])  # Miner UIDs
weights = np.array([0.2, 0.3, 0.2, 0.15, 0.15])  # Normalized weights

result = subtensor.set_weights(
    wallet=validator_wallet,
    netuid=1,
    uids=uids,
    weights=weights,
    wait_for_inclusion=True,
    wait_for_finalization=True
)
```

## 使用示例

### 示例 1：完整矿工设置

```python
import bittensor as bt
from bittensor import Balance
import numpy as np

# Initialize
subtensor = bt.Subtensor(network="finney")
wallet = bt.Wallet(name="miner_wallet", hotkey="miner1")

# Check balance
balance = subtensor.get_balance(wallet.coldkey.ss58_address)
print(f"Balance: {balance.tao} TAO")

# Register on subnet 1
print("Registering neuron...")
result = subtensor.register(
    wallet=wallet,
    netuid=1,
    wait_for_inclusion=True
)

# Get metagraph info
metagraph = subtensor.metagraph(netuid=1)
print(f"Neurons on subnet 1: {metagraph.n}")

# Check my neuron
my_uid = metagraph.hotkeys.index(wallet.hotkey.ss58_address)
my_neuron = metagraph.neurons[my_uid]
print(f"My UID: {my_uid}")
print(f"My stake: {my_neuron.stake}")
print(f"My emission: {my_neuron.emission}")
```

### 示例 2：验证器操作

```python
import bittensor as bt
from bittensor import Balance
import numpy as np

# Initialize
subtensor = bt.Subtensor(network="finney")
validator_wallet = bt.Wallet(name="validator", hotkey="val1")

# Get metagraph
metagraph = subtensor.metagraph(netuid=1)
print(f"Total miners: {metagraph.n}")

# Calculate weights based on performance
weights = np.zeros(metagraph.n)
for i in range(metagraph.n):
    weights[i] = metagraph.R[i] * 0.7 + metagraph.S[i] * 0.3

# Normalize weights
weights = weights / weights.sum()

# Set weights
result = subtensor.set_weights(
    wallet=validator_wallet,
    netuid=1,
    uids=np.arange(metagraph.n),
    weights=weights,
    wait_for_inclusion=True,
    wait_for_finalization=True
)

print(f"Weights set: {result.success}")
```

## 故障排除

### 连接问题

**问题**：无法连接到网络
**解决方案**：
```python
# Use fallback endpoints
subtensor = bt.Subtensor(
    network="finney",
    fallback_endpoints=[
        "wss://entrypoint-finney.opentensor.ai:443",
        "wss://finney.opentensor.io:443"
    ],
    retry_forever=True
)
```

### 速率限制

**问题**：请求过多导致错误
**解决方案**：
```python
import time
time.sleep(1)  # Rate limit delays
```

### 注册失败

**问题**：注册多次失败
**解决方案**：
1. 检查余额（注册需要大于 1 TAO）
2. 验证工作量证明（POW）是否正确
3. 检查网络连接
4. 尝试不同的注册方法

### 钱包问题

**问题**：找不到钱包
**解决方案**：
```python
# Create new wallet
wallet = bt.Wallet(name="new_wallet", hotkey="new_hotkey")
wallet.create_if_non_existing()
```

## 最佳实践

1. **始终关闭连接**：操作完成后使用 `subtensor.close()` 关闭连接
2. **优雅地处理错误**：使用 try-except 语句捕获错误
3. **实施速率限制**：不要超出网络规定的限制
4. **启用 MEV 保护**：对于大额交易启用该保护机制
5. **监控发行情况**：跟踪网络运行状态
6. **使用安全质押**：启用价格保护功能
7. **保护密钥安全**：切勿泄露私钥

## 安全注意事项

1. **私钥**：切勿泄露或记录私钥
2. **助记词**：安全存储私钥，切勿分享
3. **交易签名**：签名前务必进行验证
4. **启用 MEV 保护**：对于大额交易启用该保护机制
5. **代理权限**：在委托之前了解代理类型
6. **实施速率限制**：遵守网络限制以防止拒绝服务攻击（DoS）

## 向用户展示结果

在向用户展示 Bittensor SDK 的结果时，请注意以下几点：

1. **清晰显示 TAO 数量**：在相关情况下同时显示 TAO 和 Rao 的数值
2. **解释网络概念**：为非技术用户解释冷钥/热键、Netuid 和 UID 的含义
3. **突出关键指标**：强调质押量、发行量、注册成本等重要数值
4. **提供相关链接**：提供文档链接以便用户进一步了解
5. **提示风险**：提醒用户注意潜在问题，如解注册风险和速率限制

## 参考资料

- [Bittensor 文档](https://docs.bittensor.com/)
- [Bittensor SDK 参考手册](https://bittensor-sdk.readthedocs.io/)
- [学习 Bittensor](https://docs.learnbittensor.org/)
- [Taostats API](https://dash.taostats.io/)
- [Bittensor GitHub 仓库](https://github.com/opentensor)

## 详细文档

如需完整的 API 参考、扩展示例和全面的故障排除指南，请参阅：
- [API 参考](references/API_REFERENCE.md) - 完整的方法文档
- [扩展示例](references/API_REFERENCE.md#extended-examples) - 高级使用模式
- [快速参考](references/API_Reference.md#quick-reference-card) - 常见操作总结