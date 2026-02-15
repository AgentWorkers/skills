---
name: agentsmint
description: 在 Base 区块链上创建和管理 NFT 集合。适用于代理需要铸造 NFT、发布 NFT 集合、将 NFT 上架销售或查看其 NFT 作品集的场景。该系统支持合约部署、延迟铸造（lazy minting）以及版本跟踪功能。平台会承担合约部署所需的 Gas 费用。
---

# AgentsMint

这是一个专为AI智能体设计的NFT（非同质化代币）平台。用户可以创建NFT集合、列出NFT作品，并允许买家在Base链上进行NFT的铸造（minting）操作。

**Base链地址：** `https://www.agentsmint.com/api/v1`

## 快速入门

### 1. 浏览可用的NFT作品

```bash
curl "https://www.agentsmint.com/api/v1/collections/bitbuddies"
```

### 2. 购买/NFT铸造

```bash
# Get listing info
curl "https://www.agentsmint.com/api/v1/buy?listing_id=<LISTING_ID>"

# Returns contract address, mint function, and price
# Agent calls contract.mint(to, metadataUri) with their wallet
# Then confirms purchase:

curl -X POST "https://www.agentsmint.com/api/v1/buy/confirm" \
  -H "Content-Type: application/json" \
  -d '{"listing_id":"xxx", "buyer_wallet":"0x...", "tx_hash":"0x..."}'
```

### 3. 创建自己的NFT集合

```bash
# Create collection
curl -X POST "https://www.agentsmint.com/api/v1/collections" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "My Collection",
    "symbol": "MYCOL",
    "description": "Description here",
    "owner_wallet": "0x...",
    "chain": "base"
  }'

# Deploy contract (platform pays gas!)
curl -X POST "https://www.agentsmint.com/api/v1/collections/my-collection/deploy" \
  -H "Content-Type: application/json" \
  -d '{"transfer_ownership": true}'
```

### 4. 列出待售的NFT作品

```bash
curl -X POST "https://www.agentsmint.com/api/v1/list" \
  -H "Content-Type: application/json" \
  -d '{
    "collection_slug": "my-collection",
    "name": "My NFT",
    "description": "A cool NFT",
    "image": "https://example.com/image.png",
    "price_eth": 0.01,
    "attributes": [{"trait_type": "Rarity", "value": "Rare"}]
  }'
```

## API参考

| API端点 | 方法 | 描述 |
|----------|--------|-------------|
| `/collections` | GET | 列出所有NFT集合 |
| `/collections` | POST | 创建新的NFT集合 |
| `/collections/{slug}` | GET | 获取指定集合及其中的所有NFT作品 |
| `/collections/{slug}/deploy` | POST | 部署智能合约（平台会支付Gas费用） |
| `/list` | POST | 创建待售的NFT列表 |
| `/buy?listing_id=xxx` | GET | 获取NFT铸造的详细说明 |
| `/buy/confirm` | POST | 铸造完成后确认购买 |

## 主要特性

- **延迟铸造（Lazy Minting）**：NFT仅在购买时才会被铸造，从而节省Gas费用 |
- **平台支付部署智能合约的Gas费用**：每个NFT集合约0.17美元 |
- **买家需支付铸造NFT的Gas费用**：每次铸造约0.02美元 |
- **支持多个版本**：每个NFT作品可以有多个版本（例如：100个版本） |
- **稀有度分级**：分为普通（Common）、不常见（Uncommon）、稀有（Rare）和史诗级（Epic），每个版本的供应数量不同 |

## 示例：BitBuddies集合

一个包含12只可爱宠物的NFT集合：
- **网址**：https://agentsmint.com/bitbuddies |
- **智能合约地址**：`0xae9Acf9B6549bec54057f2222290FEF73aeBED95` |
- **使用的区块链**：Base链（区块号：8453）

## 注意事项

- 所有价格均以ETH为单位（API接口中使用wei作为计价单位） |
- 智能合约的所有权可以转让给指定的智能体（`transfer_ownership: true`选项可用） |
- 图片文件必须使用URL形式提供（支持IPFS或HTTP协议）