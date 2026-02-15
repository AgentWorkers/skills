---
name: near-batch-sender
description: NEAR代币的批量操作功能：支持发送给多个接收者、转移NFTs（非同质化代币），以及进行奖励领取，并提供费用估算。
---
# NEAR 批量发送技能

该技能支持对 NEAR 进行批量操作，包括发送 NEAR 代币、转移 NFT 以及领取奖励，并提供操作前的成本估算。

## 描述

该技能提供了批量发送 NEAR 代币、转移 NFT 以及领取奖励的功能，同时会在执行前进行成本估算。

## 特点

- 批量向多个地址发送 NEAR 代币
- 批量转移 NFT
- 批量领取奖励
- 执行前进行成本估算
- 支持批量操作的进度跟踪

## 命令

### `near-batch send <sender_account> <file.json>`
批量向多个接收者发送 NEAR 代币。

**JSON 格式：**
```json
{
  "recipients": [
    {"account": "account1.near", "amount": "1.5"},
    {"account": "account2.near", "amount": "0.5"}
  ]
}
```

### `near-batch nft <sender_account> <file.json>`
批量转移 NFT。

**JSON 格式：**
```json
{
  "transfers": [
    {"token_id": "123", "receiver": "account1.near", "contract": "nft.near"},
    {"token_id": "456", "receiver": "account2.near", "contract": "nft.near"}
  ]
}
```

### `near-batch estimate <sender_account> <file.json> [type]`
估算批量操作所需的gas费用。

**参数：**
- `type` - 操作类型：send（发送）、nft（转移 NFT）、claim（领取奖励）（默认值为 send）

### `near-batch claim <file.json>`
批量领取奖励/空投。

## 参考资料

- NEAR 命令行界面（CLI）：https://docs.near.org/tools/near-cli
- NEAR 批量操作接口：https://docs.near.org/api/rpc/transactions/batch-actions