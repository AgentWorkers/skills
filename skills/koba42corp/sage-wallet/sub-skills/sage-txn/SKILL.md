---
name: sage-txn
description: Sage 交易操作：  
- 列出所有交易；  
- 签署硬币的支出记录；  
- 查看未签署的交易；  
- 提交交易。
---

# Sage Transactions

交易签名与提交

## 接口（Endpoints）

### 查询交易（Query Transactions）

| 接口 | 请求参数（Payload） | 描述 |
|----------|----------------|-------------------|
| `get_transactions` | 详见下文 | 列出所有交易记录 |
| `get_transaction` | `{"height": 1234567}` | 根据交易高度查询特定交易 |
| `get_pending_transactions` | `{}` | 获取待处理的交易记录 |

#### `get_transactions` 的请求参数（Payload）  

```json
{
  "offset": 0,
  "limit": 50,
  "ascending": false,
  "find_value": null
}
```

### 签名并提交交易（Sign & Submit）

| 接口 | 请求参数（Payload） | 描述 |
|----------|----------------|-------------------|
| `sign_coin_spends` | 详见下文 | 签名交易记录 |
| `view_coin_spends` | `{"coin_spends": [...]}` | 预览交易记录（不进行签名） |
| `submit_transaction` | `{"spend_bundle": {...}}` | 提交交易记录到网络 |

#### `sign_coin_spends` 的请求参数（Payload）  

```json
{
  "coin_spends": [
    {
      "coin": {
        "parent_coin_info": "0x...",
        "puzzle_hash": "0x...",
        "amount": 1000000000000
      },
      "puzzle_reveal": "0x...",
      "solution": "0x..."
    }
  ],
  "auto_submit": false,
  "partial": false
}
```

- `partial: true`：用于多签名交易流程中的部分签名操作

#### `submit_transaction` 的请求参数（Payload）  

```json
{
  "spend_bundle": {
    "coin_spends": [...],
    "aggregated_signature": "0x..."
  }
}
```

## 交易记录结构（Transaction Record Structure）  

```json
{
  "height": 1234567,
  "timestamp": 1700000000,
  "fee": "100000000",
  "inputs": [...],
  "outputs": [...]
}
```

## 待处理交易的结构（Pending Transaction Structure）  

```json
{
  "transaction_id": "0x...",
  "fee": "100000000",
  "submitted_at": 1700000000,
  "coin_spends": [...]
}
```

## 示例（Examples）  

```bash
# List recent transactions
sage_rpc get_transactions '{"limit": 20, "ascending": false}'

# Get pending
sage_rpc get_pending_transactions '{}'

# View coin spends (preview)
sage_rpc view_coin_spends '{"coin_spends": [...]}'

# Sign and submit
sage_rpc sign_coin_spends '{
  "coin_spends": [...],
  "auto_submit": true
}'

# Manual submit
sage_rpc submit_transaction '{"spend_bundle": {...}}'
```

## 工作流程（Workflow）

1. 通过其他接口构建交易记录（`auto_submit: false`）；
2. （可选）使用 `view_coin_spends` 预览交易记录；
3. 使用 `sign_coin_spends` 创建交易签名包；
4. 使用 `submit_transaction` 将交易记录提交到网络（或设置 `auto_submit: true` 以自动提交）。

## 注意事项（Notes）：

- 当 `auto_submit: true` 时，签名和提交操作会同时完成；
- `partial: true` 适用于需要多签名验证的交易流程；
- 待处理的交易记录会等待矿池的确认。