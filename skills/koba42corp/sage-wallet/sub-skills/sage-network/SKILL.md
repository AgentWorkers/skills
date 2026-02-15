---
name: sage-network
description: Sage网络及对等节点设置：管理对等节点、切换网络、配置同步设置、设置地址变更规则。
---

# Sage Network与对等节点

网络配置及对等节点管理。

## 端点（Endpoints）

### 对等节点管理（Peer Management）

| 端点 | 数据格式 | 描述 |
|----------|---------|-------------|
| `get_peers` | `{}` | 列出已连接的对等节点 |
| `add_peer` | `{"ip": "node.example.com:8444"}` | 添加对等节点 |
| `remove_peer` | `{"ip": "...", "ban": false}` | 移除/禁止对等节点 |
| `set_discover_peers` | `{"discover_peers": true}` | 切换自动发现模式 |
| `set_target_peers` | `{"target_peers": 8}` | 设置目标对等节点数量 |

### 网络设置（Network Settings）

| 端点 | 数据格式 | 描述 |
|----------|---------|-------------|
| `get_network` | `{}` | 获取当前网络信息 |
| `get_networks` | `{}` | 列出可用的网络 |
| `set_network` | `{"name": "mainnet"}` | 切换网络 |
| `set_network_override` | `{"fingerprint": ..., "name": "testnet11"}` | 为每个钱包设置网络覆盖值 |

### 同步设置（Sync Settings）

| 端点 | 数据格式 | 描述 |
|----------|---------|-------------|
| `set_delta_sync` | `{"delta_sync": true}` | 切换差异同步模式 |
| `set_delta_sync_override` | `{"fingerprint": ..., "delta_sync": true}` | 为每个钱包设置差异同步覆盖值 |

### 地址设置（Address Settings）

| 端点 | 数据格式 | 描述 |
|----------|---------|-------------|
| `set_change_address` | `{"fingerprint": ..., "change_address": "xch1..."}` | 设置变更地址 |

## 对等节点记录结构（Peer Record Structure）

```json
{
  "ip": "192.168.1.100:8444",
  "port": 8444,
  "peak_height": 1234567,
  "synced": true
}
```

## 网络响应结构（Network Response Structure）

```json
{
  "network": {
    "name": "mainnet",
    "prefix": "xch",
    "default_port": 8444,
    "genesis_challenge": "0x..."
  },
  "kind": "mainnet"
}
```

网络类型：`"mainnet"`、`"testnet"`、`"unknown"`

## 示例（Examples）

```bash
# List peers
sage_rpc get_peers '{}'

# Add peer
sage_rpc add_peer '{"ip": "node.chia.net:8444"}'

# Remove and ban peer
sage_rpc remove_peer '{"ip": "192.168.1.50:8444", "ban": true}'

# Get current network
sage_rpc get_network '{}'

# Switch to testnet
sage_rpc set_network '{"name": "testnet11"}'

# Enable delta sync
sage_rpc set_delta_sync '{"delta_sync": true}'

# Set custom change address
sage_rpc set_change_address '{
  "fingerprint": 1234567890,
  "change_address": "xch1mychange..."
}'
```

## 网络覆盖（Network Override）

多网络环境下的每个钱包网络覆盖设置：

```bash
# Use testnet for specific wallet
sage_rpc set_network_override '{
  "fingerprint": 1234567890,
  "name": "testnet11"
}'

# Reset to default
sage_rpc set_network_override '{
  "fingerprint": 1234567890,
  "name": null
}'
```

## 注意事项（Notes）

- 差异同步（delta sync）速度更快，但可能会遗漏某些边缘情况。
- `target_peers` 参数用于控制保持的连接数量。
- 网络覆盖（network override）功能允许在不切换全局网络的情况下进行测试。