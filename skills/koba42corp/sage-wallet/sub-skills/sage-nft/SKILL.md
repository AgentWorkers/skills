---
name: sage-nft
description: Sage NFT操作：列出NFT和收藏集、铸造NFT、转移NFT、添加URL、将NFT关联到DID（Digital Identifiers）、管理NFT的可见性。
---

# Sage NFTs

提供针对Chia NFT1标准的NFT操作功能。

## 端点（Endpoints）

### 查询NFTs

| 端点          | 报文格式（Payload） | 描述                          |
|--------------|-----------------|-------------------------------------------|
| `get_nfts`     | 见下文           | 使用过滤器列出NFTs                   |
| `get_nft`     | `{"nft_id": "nft1..."}`    | 获取NFT详细信息                   |
| `get_nft_icon`   | `{"nft_id": "nft1..."}`    | 获取NFT图标（base64编码）                 |
| `get_nft_thumbnail` | `{"nft_id": "nft1..."}`    | 获取NFT缩略图（base64编码）                 |
| `get_nft_data`   | `{"nft_id": "nft1..."}`    | 获取NFT原始数据                     |

#### `get_nfts` 的报文格式（Payload）

支持以下排序方式：`"name"`、`"recent"`

### 集合（Collections）

| 端点          | 报文格式（Payload） | 描述                          |
|--------------|-----------------|-------------------------------------------|
| `get_nft_collections` | `{"offset": 0, "limit": 50, "include_hidden": false}` | 列出所有集合                     |
| `get_nft_collection` | `{"collection_id": "col1..."}` | 获取特定集合                     |
| `update_nft_collection` | `{"collection_id": "col1...", "visible": true}` | 更新集合的可见性                     |

### 铸造NFTs（Mint NFTs）

```json
{
  "mints": [
    {
      "address": null,
      "edition_number": 1,
      "edition_total": 100,
      "data_hash": "0x...",
      "data_uris": ["https://..."],
      "metadata_hash": "0x...",
      "metadata_uris": ["https://..."],
      "license_hash": null,
      "license_uris": [],
      "royalty_address": "xch1...",
      "royalty_ten_thousandths": 300
    }
  ],
  "did_id": "did:chia:...",
  "fee": "100000000",
  "auto_submit": true
}
```

响应中包含一个 `nft_ids` 数组。

### 转移与管理（Transfer & Manage）

| 端点          | 报文格式（Payload） | 描述                          |
|--------------|-----------------|-------------------------------------------|
| `transfer_nfts` | `{"nft_ids": [...], "address": "xch1...", "fee": "...", "auto_submit": true}` | 转移NFTs                     |
| `add_nft_uri`   | `{"nft_id": "...", "uri": "https://...", "kind": "data", "fee": "..."}` | 添加NFT的URI                     |
| `assign_nfts_to_did` | `{"nft_ids": [...], "did_id": "did:chia:...", "fee": "..."}` | 将NFTs分配给DID                     |
| `update_nft`     | `{"nft_id": "...", "visible": true}` | 更新NFT的可见性                     |
| `redownload_nft`   | `{"nft_id": "..."}`     | 重新获取NFT数据                     |

URI类型：`"data"`, `"metadata"`, `"license"`

## NFT记录结构（NFT Record Structure）

```json
{
  "nft_id": "nft1...",
  "launcher_id": "0x...",
  "collection_id": "col1...",
  "owner_did_id": "did:chia:...",
  "minter_did_id": "did:chia:...",
  "name": "My NFT",
  "description": "...",
  "data_uris": ["https://..."],
  "metadata_uris": ["https://..."],
  "royalty_address": "xch1...",
  "royalty_ten_thousandths": 300,
  "visible": true
}
```

## 示例（Examples）

```bash
# List NFTs
sage_rpc get_nfts '{"limit": 20, "sort_mode": "recent"}'

# Mint NFT
sage_rpc bulk_mint_nfts '{
  "mints": [{
    "data_uris": ["ipfs://Qm..."],
    "data_hash": "0xabc...",
    "metadata_uris": ["ipfs://Qm..."],
    "metadata_hash": "0xdef...",
    "royalty_ten_thousandths": 500
  }],
  "did_id": "did:chia:1abc...",
  "fee": "100000000",
  "auto_submit": true
}'

# Transfer NFT
sage_rpc transfer_nfts '{
  "nft_ids": ["nft1abc..."],
  "address": "xch1recipient...",
  "fee": "100000000",
  "auto_submit": true
}'
```

## 注意事项（Notes）

- 版权费用以万分之一为单位：300表示3%，500表示5%
- 在 `assign_nfts_to_did` 请求中，如果 `did_id` 为 `null`，则表示将NFT从指定的DID中解绑
- 铸造NFT需要使用DID来记录其来源信息