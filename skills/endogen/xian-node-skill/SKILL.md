---
name: xian-node
description: **设置和管理 Xian 区块链节点**  
本文档介绍了如何设置和管理 Xian 区块链节点，适用于将节点部署到主网/测试网、创建新的 Xian 网络或监控已运行的节点的场景。内容涵盖了基于 Docker 的部署方式（使用 xian-stack）、CometBFT 协议的配置以及节点监控的相关步骤。
---

# Xian节点技能

部署和管理[Xian](https://xian.org)区块链节点——这是一个基于CometBFT框架的L1（Layer 1）区块链，支持原生Python智能合约。

## 快速参考

| 任务 | 命令 |
|------|---------|
| 加入主网 | `make setup && make core-build && make core-up && make init && make configure CONFIGURE_ARGS='--genesis-file-name genesis-mainnet.json --seed-node-address <seed> --copy-genesis'` |
| 启动节点 | 先运行`make core-shell`，然后在容器内运行`make up` |
| 查看日志 | 在容器内运行`pm2 logs --lines 100` |
| 停止节点 | 在容器内运行`make down`，或直接停止容器：`make core-down` |
| 检查同步状态 | `curl -s localhost:26657/status \| jq '.result.sync_info'` |

## 设置：加入现有网络

### 1. 克隆并构建项目

```bash
git clone https://github.com/xian-network/xian-stack.git
cd xian-stack
make setup CORE_BRANCH=mainnet CONTRACTING_BRANCH=mainnet
make core-build
make core-up
```

### 2. 初始化CometBFT

```bash
make init
```

### 3. 配置节点

**主网：**
```bash
make configure CONFIGURE_ARGS='--moniker "my-node" --genesis-file-name "genesis-mainnet.json" --seed-node-address "c3861ffd16cf6708aef6683d3d0471b6dedb3116@152.53.18.220" --copy-genesis'
```

**测试网：**
```bash
make configure CONFIGURE_ARGS='--moniker "my-node" --genesis-file-name "genesis-testnet.json" --seed-node-address "<testnet-seed>" --copy-genesis'
```

**验证节点**（需要添加私钥）：
```bash
make configure CONFIGURE_ARGS='--moniker "my-validator" --genesis-file-name "genesis-mainnet.json" --validator-privkey "<your-privkey>" --seed-node-address "..." --copy-genesis'
```

**服务节点**（启用BDS - 区块链数据服务）：
```bash
make configure CONFIGURE_ARGS='--moniker "my-service" --genesis-file-name "genesis-mainnet.json" --seed-node-address "..." --copy-genesis --service-node'
```

### 4. 启动节点

```bash
make core-shell   # Enter container
make up           # Start pm2 processes
pm2 logs          # Watch sync progress
exit              # Leave shell (node keeps running)
```

## 设置：创建新网络

### 1. 构建项目依赖

```bash
git clone https://github.com/xian-network/xian-stack.git
cd xian-stack
make setup CORE_BRANCH=mainnet CONTRACTING_BRANCH=mainnet
make core-build
make core-up
make init
```

### 2. 生成验证节点密钥

在容器内运行`make core-shell`后执行以下命令：
```bash
# Generate new validator key
python -c "
from nacl.signing import SigningKey
import secrets
sk = SigningKey(secrets.token_bytes(32))
print(f'Private key: {sk.encode().hex()}')
print(f'Public key:  {sk.verify_key.encode().hex()}')
"
```

### 3. 创建创世文件

使用`genesis-template.md`作为模板，创建`genesis.json`文件，其中包含初始的验证节点信息。**

### 4. 配置为创世验证节点

```bash
make configure CONFIGURE_ARGS='--moniker "genesis-validator" --genesis-file-name "genesis-custom.json" --validator-privkey "<privkey>"'
```

### 5. 启动新网络

```bash
make core-shell
make up
```

其他节点会以你的节点为种子节点来加入新网络。

## 节点管理

### 在容器内的命令

| 命令 | 描述 |
|---------|-------------|
| `make up` | 通过pm2启动Xian和CometBFT服务 |
| `make down` | 停止所有与pm2相关的进程 |
| `make restart` | 重启节点 |
| `make logs` | 查看pm2日志 |
| `make wipe` | 清除节点数据（保留配置文件） |
| `make dwu` | 完全重置节点（包括停止、清除数据和重新初始化） |

### 监控

**同步状态：**
```bash
curl -s localhost:26657/status | jq '.result.sync_info'
```

**响应字段：**
- `latest_block_height`：当前区块高度
- `catching_up`：如果仍在同步，则显示`true`
- `earliest_block_height`：可用的最低区块高度

**节点信息：**
```bash
curl -s localhost:26657/status | jq '.result.node_info'
make node-id   # Get node ID for peering
```

**验证节点信息：**
```bash
curl -s localhost:26657/validators | jq '.result.validators'
```

### Docker命令

| 命令 | 描述 |
|---------|-------------|
| `make core-up` | 启动容器 |
| `make core-down` | 停止容器 |
| `make core-shell` | 进入容器 shell |
| `make core-bds-up` | 启动包含BDS（PostgreSQL + GraphQL）的服务 |

## 端口

| 端口 | 服务 |  
|------|---------|
| 26656 | P2P（节点间通信） |
| 26657 | RPC（请求/响应） |
| 26660 | Prometheus指标服务 |
| 5000 | GraphQL（仅用于BDS服务） |

## 故障排除

**数据库锁定错误**（`resource temporarily unavailable`）：
```bash
# Duplicate pm2 processes - clean up:
pm2 delete all
make up
```

**同步失败**：
```bash
# Check peer connections
curl -s localhost:26657/net_info | jq '.result.n_peers'

# Verify seed node is reachable
make wipe
make init
# Re-run configure with correct seed
```

**容器无法启动**：
```bash
make core-down
make core-build --no-cache
make core-up
```

## 文件位置

| 路径 | 文件内容 |
|------|----------|
| `.cometbft/` | CometBFT数据及配置文件 |
| `.cometbft/config/genesis.json` | 网络创世文件 |
| `.cometbft/config/config.toml` | 节点配置文件 |
| `.cometbft/data/` | 区块链数据 |
| `xian-core/` | Xian ABCI应用程序 |
| `xian-contracting/` | Python合约引擎 |

## 测试节点

同步完成后，使用[xian-py](https://github.com/xian-network/xian-py)验证节点是否正常工作：

```bash
pip install xian-py
```

```python
from xian_py import Xian, Wallet

# Connect to your local node
xian = Xian('http://localhost:26657')

# Query balance
balance = xian.get_balance('your_address')
print(f"Balance: {balance}")

# Get contract state
state = xian.get_state('currency', 'balances', 'some_address')
print(f"State: {state}")

# Create wallet and send transaction
wallet = Wallet()  # or Wallet('your_private_key')
xian = Xian('http://localhost:26657', wallet=wallet)
result = xian.send(amount=10, to_address='recipient_address')
```

有关完整的SDK文档（包括合约、HD钱包和异步功能），请参阅[xian-py](https://github.com/xian-network/xian-py)。

## 资源链接

- [xian-network/xian-stack](https://github.com/xian-network/xian-stack) — Docker部署指南 |
- [xian-network/xian-core](https://github.com/xian-network/xian-core) — 核心节点代码 |
- [xian-network/xian-py](https://github.com/xian-network/xian-py) — Python SDK |
- [CometBFT文档](https://docs.cometbft.com/) — 共识机制说明 |
- [xian.org](https://xian.org) — 项目官方网站 |