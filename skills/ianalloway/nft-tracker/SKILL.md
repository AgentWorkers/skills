---
name: nft-tracker
description: "跟踪NFT收藏品的价格、最低售价以及销售数据。支持包括BAYC、MAYC、CryptoPunks在内的以太坊收藏品。"
homepage: https://docs.opensea.io/reference/api-overview
metadata:
  {
    "openclaw":
      {
        "emoji": "🖼️",
        "requires": { "bins": ["curl", "jq"] },
        "credentials":
          [
            {
              "id": "opensea-api-key",
              "name": "OpenSea API Key",
              "description": "API key from https://docs.opensea.io/reference/api-keys",
              "env": "OPENSEA_API_KEY",
            },
          ],
      },
  }
---
# NFT 价格追踪器

使用免费的 API 来追踪 NFT 收藏品的统计数据、底价以及近期销售情况。

## 免费 API（无需密钥）

### Reservoir API（推荐）

获取收藏品的底价：

```bash
curl -s "https://api.reservoir.tools/collections/v6?slug=boredapeyachtclub" | jq '.collections[0] | {name, floorAsk: .floorAsk.price.amount.native, volume24h: .volume["1day"], volumeChange: .volumeChange["1day"]}'
```

### 热门收藏品名称：

- `boredapeyachtclub` - Bored Ape Yacht Club (BAYC)
- `mutant-ape-yacht-club` - Mutant Ape Yacht Club (MAYC)
- `cryptopunks` - CryptoPunks
- `azuki` - Azuki
- `pudgypenguins` - Pudgy Penguins
- `doodles-official` - Doodles
- `clonex` - CloneX

## 收藏品统计数据

获取详细的藏品统计数据：

```bash
curl -s "https://api.reservoir.tools/collections/v6?slug=mutant-ape-yacht-club" | jq '.collections[0] | {
  name: .name,
  floor_eth: .floorAsk.price.amount.native,
  floor_usd: .floorAsk.price.amount.usd,
  volume_24h: .volume["1day"],
  volume_7d: .volume["7day"],
  volume_30d: .volume["30day"],
  owners: .ownerCount,
  supply: .tokenCount
}'
```

## 最近的销售记录

获取某个收藏品的近期销售记录：

```bash
curl -s "https://api.reservoir.tools/sales/v6?collection=0xbc4ca0eda7647a8ab7c2061c2e118a18a936f13d&limit=10" | jq '.sales[] | {token_id: .token.tokenId, price_eth: .price.amount.native, timestamp: .timestamp, marketplace: .orderSource}'
```

合约地址：
- BAYC: `0xbc4ca0eda7647a8ab7c2061c2e118a18a936f13d`
- MAYC: `0x60e4d786628fea6478f785a6d7e704777c86a7c6`
- CryptoPunks: `0xb47e3cd837ddf8e4c57f05d70ab865de6e193bbb`

## 底价历史

获取藏品底价的变化趋势：

```bash
curl -s "https://api.reservoir.tools/collections/daily-volumes/v1?collection=0x60e4d786628fea6478f785a6d7e704777c86a7c6&limit=30" | jq '.[] | {date: .timestamp, floor: .floorAskPrice, volume: .volume}'
```

## 热门收藏品

按交易量获取热门收藏品列表：

```bash
curl -s "https://api.reservoir.tools/collections/v6?sortBy=1DayVolume&limit=10" | jq '.collections[] | {name: .name, floor: .floorAsk.price.amount.native, volume_24h: .volume["1day"]}'
```

## NFT 详情查询

获取特定 NFT 的详细信息：

```bash
# MAYC #1234
curl -s "https://api.reservoir.tools/tokens/v7?tokens=0x60e4d786628fea6478f785a6d7e704777c86a7c6:1234" | jq '.tokens[0] | {name: .token.name, image: .token.image, lastSale: .token.lastSale.price.amount.native, owner: .token.owner}'
```

## 价格警报（脚本示例）

监控底价，当底价低于设定阈值时触发警报：

```bash
#!/bin/bash
COLLECTION="mutant-ape-yacht-club"
THRESHOLD=5  # ETH

FLOOR=$(curl -s "https://api.reservoir.tools/collections/v6?slug=$COLLECTION" | jq -r '.collections[0].floorAsk.price.amount.native')

if (( $(echo "$FLOOR < $THRESHOLD" | bc -l) )); then
  echo "ALERT: $COLLECTION floor is $FLOOR ETH (below $THRESHOLD ETH)"
fi
```

## OpenSea API（需要密钥）

如果您拥有 OpenSea API 密钥：

```bash
curl -s "https://api.opensea.io/api/v2/collections/mutant-ape-yacht-club/stats" \
  -H "X-API-KEY: $OPENSEA_API_KEY" | jq '.'
```

## 提示：

- Reservoir API 是免费的，基本查询无需认证。
- 请注意 API 的使用频率限制，尽可能使用缓存结果。
- 除非另有说明，价格单位均为 ETH。
- 使用合约地址进行精确查询，使用收藏品名称（slug）以便于识别。