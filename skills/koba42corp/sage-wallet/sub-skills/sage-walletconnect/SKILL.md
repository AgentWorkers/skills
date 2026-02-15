---
name: sage-walletconnect
description: Sage WalletConnect集成：支持筛选货币、获取资产信息、签名消息以及发送交易，以实现与去中心化应用（dApp）的互联互通。
---

# Sage WalletConnect

Sage WalletConnect 提供了一种用于 dApp（去中心化应用程序）与钱包之间通信的协议集成方案。

## 端点（Endpoints）

### 硬币操作（Coin Operations）

| 端点 | 有效载荷（Payload） | 描述 |
|----------|-----------------|-------------------|
| `filter_unlocked_coins` | `{"coin_ids": [...]}` | 过滤已解锁的硬币 |
| `get_asset_coins` | 见下文 | 获取可花费的硬币 |

#### `get_asset_coins` 的有效载荷（Payload）

可支持的资产类型：`"cat"`、`"did"`、`"nft"`

### 消息签名（Message Signing）

| 端点 | 有效载荷 | 描述 |
|----------|-----------------|-------------------|
| `sign_message_with_public_key` | `{"message": "...", "public_key": "0x..."}` | 使用公钥签名消息 |
| `sign_message_by_address` | `{"message": "...", "address": "xch1..."}` | 使用地址密钥签名消息 |

### 交易（Transactions）

| 端点 | 有效载荷 | 描述 |
|----------|-----------------|-------------------|
| `send_transaction_immediately` | `{"spend_bundle": {...}}` | 直接广播交易请求 |

## 可花费硬币的结构（Structure of Spendable Coins）

```json
{
  "coin": {
    "parent_coin_info": "0x...",
    "puzzle_hash": "0x...",
    "amount": 1000000000000
  },
  "coin_name": "0x...",
  "puzzle": "0x...",
  "confirmed_block_index": 1234567,
  "locked": false,
  "lineage_proof": {
    "parent_name": "0x...",
    "inner_puzzle_hash": "0x...",
    "amount": 1000
  }
}
```

## 消息签名响应（Message Signing Response）

```json
{
  "public_key": "0x...",
  "signature": "0x..."
}
```

## 交易发送响应（Transaction Sending Response）

```json
{
  "status": 1,
  "error": null
}
```

状态码说明：
- `1`：成功
- 其他值：错误

## 示例（Examples）

```bash
# Filter unlocked coins
sage_rpc filter_unlocked_coins '{"coin_ids": ["0xabc...", "0xdef..."]}'

# Get CAT coins for WalletConnect
sage_rpc get_asset_coins '{
  "type": "cat",
  "asset_id": "a628c1c2...",
  "limit": 20
}'

# Sign message with address
sage_rpc sign_message_by_address '{
  "message": "Login to MyDApp",
  "address": "xch1abc..."
}'

# Sign with specific pubkey
sage_rpc sign_message_with_public_key '{
  "message": "Verify ownership",
  "public_key": "0x89abcdef..."
}'

# Send transaction directly
sage_rpc send_transaction_immediately '{
  "spend_bundle": {
    "coin_spends": [...],
    "aggregated_signature": "0x..."
  }
}'
```

## WalletConnect 的工作流程（WalletConnect Workflow）

1. dApp 请求与钱包建立连接。
2. 用户在 Sage 平台上进行身份验证并批准连接。
3. dApp 调用 `get_asset_coins` 函数来获取可花费的硬币。
4. dApp 构建交易请求。
5. 用户通过 `sign_message_*` 或其他签名方法对交易进行签名。
6. dApp 将签名后的交易请求广播到网络，或直接调用 `send_transaction_immediately` 函数来发送交易。

## 注意事项（Notes）

- WalletConnect 支持 dApp 与钱包之间的双向通信。
- 对于涉及 CAT（特定类型的资产）的交易，`lineage_proof` 是必需的。
- 消息签名功能可以在不进行实际交易的情况下验证地址的所有权。