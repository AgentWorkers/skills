---
name: sage-did
description: Sage DID（去中心化标识符）相关操作：列出现有的DIDs、创建新的DIDs、转移所有权、更新元数据以及进行数据规范化处理。
---

# Sage DIDs

DID（去中心化标识符）相关操作

## 终端点（Endpoints）

### 查询 DIDs

| 终端点 | 数据格式 | 描述 |
|----------|---------|-------------|
| `get_dids` | `{}` | 列出所有 DIDs |
| `get_minter_did_ids` | `{"offset": 0, "limit": 50}` | 列出矿工的 DIDs |

### 创建 DID

```json
{
  "name": "My Identity",
  "fee": "100000000",
  "auto_submit": true
}
```

### 更新 DID

```json
{
  "did_id": "did:chia:1abc...",
  "name": "Updated Name",
  "visible": true
}
```

### 转移 DIDs

```json
{
  "did_ids": ["did:chia:1abc..."],
  "address": "xch1...",
  "fee": "100000000",
  "clawback": null,
  "auto_submit": true
}
```

### 规范化 DIDs

将 DID 记录更新为最新的链上状态：

```json
{
  "did_ids": ["did:chia:1abc..."],
  "fee": "100000000",
  "auto_submit": true
}
```

## DID 记录结构

```json
{
  "did_id": "did:chia:1abc...",
  "launcher_id": "0x...",
  "name": "My Identity",
  "visible": true,
  "coin_id": "0x..."
}
```

## 示例（Examples）

```bash
# List DIDs
sage_rpc get_dids '{}'

# Create DID
sage_rpc create_did '{
  "name": "Artist Profile",
  "fee": "100000000",
  "auto_submit": true
}'

# Transfer DID
sage_rpc transfer_dids '{
  "did_ids": ["did:chia:1abc..."],
  "address": "xch1newowner...",
  "fee": "100000000",
  "auto_submit": true
}'

# Update name
sage_rpc update_did '{
  "did_id": "did:chia:1abc...",
  "name": "New Profile Name",
  "visible": true
}'
```

## 使用场景（Use Cases）

- **NFT 铸造**：DIDs 为铸造的 NFT 提供可验证的出处信息。
- **身份验证**：DIDs 作为链上的身份标识。
- **作品集管理**：将 NFT 集合与矿工的 DID 关联起来。
- **消息认证**：使用 DID 密钥对消息进行签名以供验证。