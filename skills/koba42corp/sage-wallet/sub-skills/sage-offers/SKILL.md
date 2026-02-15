---
name: sage-offers
description: Sage 提供了用于点对点交易的报价功能。用户可以创建报价、查看报价、接受报价、合并报价、导入报价以及取消报价。
---

# Sage 提供的功能

基于区块链的点对点交易系统。

## 端点（Endpoints）

### 创建交易报价（Create Offer）

```json
{
  "requested_assets": [
    {"asset_id": null, "amount": "1000000000000"}
  ],
  "offered_assets": [
    {"asset_id": "a628c1c2...", "amount": "1000"}
  ],
  "fee": "100000000",
  "receive_address": null,
  "expires_at_second": null,
  "auto_import": true
}
```

- `asset_id: null` = XCH
- 返回值：`{"offer": "offer1...", "offer_id": "..."}`

### 接受交易报价（Accept Offer）

```json
{
  "offer": "offer1...",
  "fee": "100000000",
  "auto_submit": true
}
```

### 查看交易报价（不接受）（View Offer, without accepting）

```json
{
  "offer": "offer1..."
}
```

返回报价的摘要和状态。

### 查询交易报价（Query Offers）

| 端点 | 请求参数 | 描述 |
|----------|---------|-------------|
| `get_offers` | `{}` | 列出所有交易报价 |
| `get_offer` | `{"offer_id": "..."}` | 获取特定的交易报价 |
| `get_offers_for_asset` | `{"asset_id": "..."}` | 按资产过滤交易报价 |
| `import_offer` | `{"offer": "offer1..."}` | 导入外部交易报价 |

### 取消/删除交易报价（Cancel/Delete Offer）

| 端点 | 请求参数 | 描述 |
|----------|---------|-------------|
| `delete_offer` | `{"offer_id": "..."}` | 删除本地（非链上）的交易报价 |
| `cancel_offer` | `{"offer_id": "...", "fee": "...", "auto_submit": true}` | 在链上取消交易报价 |
| `cancel_offers` | `{"offer_ids": [...], "fee": "...", "auto_submit": true}` | 批量取消交易报价 |

### 合并交易报价（Combine Offers）

合并多个兼容的交易报价：

```json
{
  "offers": ["offer1...", "offer1..."]
}
```

## 交易报价金额结构（Offer Amount Structure）

```json
{
  "asset_id": "a628c1c2...",
  "hidden_puzzle_hash": null,
  "amount": "1000"
}
```

## 交易报价记录结构（Offer Record Structure）

```json
{
  "offer_id": "...",
  "offer": "offer1...",
  "status": "pending",
  "requested": [...],
  "offered": [...],
  "expires_at_second": null
}
```

状态值：`"pending"`（待处理）、`"completed"`（已完成）、`"cancelled"`（已取消）、`"expired"`（已过期）

## 示例（Examples）

```bash
# Create offer: 1 XCH for 1000 SBX
sage_rpc make_offer '{
  "requested_assets": [{"asset_id": null, "amount": "1000000000000"}],
  "offered_assets": [{"asset_id": "a628c1c2...", "amount": "1000"}],
  "fee": "100000000",
  "auto_import": true
}'

# View offer
sage_rpc view_offer '{"offer": "offer1abc..."}'

# Accept offer
sage_rpc take_offer '{
  "offer": "offer1abc...",
  "fee": "100000000",
  "auto_submit": true
}'

# Cancel offer
sage_rpc cancel_offer '{
  "offer_id": "abc123",
  "fee": "100000000",
  "auto_submit": true
}'
```

## 注意事项（Notes）

- 交易报价为以 `offer1` 开头的 bech32 编码字符串。
- `delete_offer` 仅删除本地数据库中的交易报价。
- `cancel_offer` 会在链上花费相应的代币来取消交易报价。
- 可以合并多个交易报价以完成复杂的多方交易。