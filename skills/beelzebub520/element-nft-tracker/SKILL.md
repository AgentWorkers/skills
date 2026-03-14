---
name: element-nft
description: Element Market集成用于NFT作品集和市场的监控。需要使用`ELEMENT_API_KEY`环境变量。在用户明确授权的情况下，该凭证允许该技能访问个人账户级别的数据（如私人资产列表、销售历史以及收到的报价）。
metadata: {"openclaw":{"emoji":"🌊","always":false,"requires":{"bins":["curl","jq"],"envs":["ELEMENT_API_KEY"]}}}
---
# Element NFT市场 🌊

本技能用于查询Element市场上的NFT集合统计信息、投资组合以及监控活跃的交易事件。

## 🚀 设置

### 环境变量
请确保已在您的环境变量或`.env`文件中设置API密钥：
```bash
export ELEMENT_API_KEY="your_api_key_here"

```

## 📊 查询与监控

### 获取集合统计信息
使用此功能可查询特定NFT集合的详细交易量、最低价格、24小时平均价格以及最新交易价格（通过其 slug 来识别）。
```bash
SLUG="boredapeyachtclub"
CHAIN="eth"

curl -s --request GET \
  --url "[https://api.element.market/openapi/v1/collection/stats?chain=$](https://api.element.market/openapi/v1/collection/stats?chain=$){CHAIN}&collection_slug=${SLUG}" \
  --header "X-Api-Key: ${ELEMENT_API_KEY}" \
  --header "accept: application/json" | jq '{volume24h: .data.stats1D.volume, saleCount24h: .data.stats1D.saleCount, floorPrice: .data.collectionFloorPrice.floorPriceSource, avgPrice24h: .data.stats1D.avgPrice, lastTradePrice: .data.lastTradePrice}'

```

### 获取排行榜
使用此功能可获取特定链上最热门的NFT集合。
```bash
SORTTYPE="TOP"
CHAIN="eth"
LEVEL="L1D"
LIMIT="10"

curl -s --request GET \
     --url "[https://api.element.market/openapi/v1/collection/ranking?chain=$](https://api.element.market/openapi/v1/collection/ranking?chain=$){CHAIN}&sort_type=${SORTTYPE}&level=${LEVEL}&limit=${LIMIT}" \
     --header "X-Api-Key: ${ELEMENT_API_KEY}" \
     --header "accept: application/json" | jq '[.data.rankingList[].collectionRank | {name: .collection.name, slug: .collection.slug, floorPrice: .floorPrice, volume: .volume}]' 

```

### 获取钱包中的NFT投资组合（资产列表）
使用此功能可获取特定钱包地址所拥有的NFT列表。
* `CHAIN` 可以是 "eth"、"bsc" 等。
* `WALLET_ADDRESS` 是钱包的0x地址。仅当用户明确要求查看自己的钱包时才需要填写此字段。
* `LIMIT` 是返回的资产数量（默认为10，以节省Token）。
```bash
CHAIN="eth"
WALLET_ADDRESS="" 
LIMIT="10"

curl -s --request GET \
  --url "[https://api.element.market/openapi/v1/account/assetList?chain=$](https://api.element.market/openapi/v1/account/assetList?chain=$){CHAIN}&wallet_address=${WALLET_ADDRESS}&limit=${LIMIT}" \
  --header "X-Api-Key: ${ELEMENT_API_KEY}" \
  --header "accept: application/json" | jq '[.data.assetList[].asset | {name: .name, collection: .collection.name, tokenId: .tokenId, type: .tokenType, quantity: .ownedQuantity, image: .imagePreviewUrl}]'

```

### 查看收到的报价（针对用户拥有的NFT）
使用此功能可查看用户拥有的NFT收到的最高报价（出价）。系统会自动返回包括最低价格和最后交易价格在内的详细信息。
* `CHAIN` 可以是 "eth"、"bsc" 等。
* `WALLET_ADDRESS` 是钱包的0x地址。仅当用户明确要求查看自己的钱包时才需要填写此字段。
* 🚨 输出规则：使用Markdown格式将 `image` URL 显示为实际的链接（例如：`![NFT名称](image_url)`。下方需清晰显示报价价格、报价者、最低价格、24小时平均价格和最后交易价格，并简要说明该报价是否划算！
```bash
CHAIN="bsc"
WALLET_ADDRESS="" 
LIMIT="10"

curl -s --request GET \
  --url "[https://api.element.market/openapi/v1/account/offerReceived?chain=$](https://api.element.market/openapi/v1/account/offerReceived?chain=$){CHAIN}&wallet_address=${WALLET_ADDRESS}&limit=${LIMIT}" \
  --header "X-Api-Key: ${ELEMENT_API_KEY}" \
  --header "accept: application/json" | jq '[.data.assetList[] | select(.orderData.bestBid != null) | {name: .asset.name, collection: .asset.collection.name, slug: .asset.collection.slug, image: .asset.imagePreviewUrl, offerPrice: .orderData.bestBid.price, offerUSD: .orderData.bestBid.priceUSD, offerer: .orderData.bestBid.maker}]'

```

### 通过合约地址获取集合slug（地址解析器）
当用户提供智能合约地址（例如：0x...）时，使用此工具来查找该集合的 `slug`，以便在其他查询中使用。系统会自动调用 `Get Collection Stats` 并使用解析出的 `slug` 提供完整信息。
```bash
CHAIN="bsc"
CONTRACT_ADDRESS="0xed5af388653567af2f388e6224dc7c4b3241c544"

curl -s --request GET \
  --url "[https://api.element.market/openapi/v1/contract?chain=$](https://api.element.market/openapi/v1/contract?chain=$){CHAIN}&contract_address=${CONTRACT_ADDRESS}" \
  --header "X-Api-Key: ${ELEMENT_API_KEY}" \
  --header "accept: application/json" | jq '{name: .data.collection.name, slug: .data.collection.slug, image: .data.collection.imageUrl}'

```

### 查看最近的交易活动（一站式监控）
🔴 当用户询问“我最近卖出了哪些NFT？”或“查看我的近期交易记录”时，必须使用此工具来监控钱包的最近交易活动。
使用此功能可获取特定钱包的最新交易记录，并在后台自动解析集合统计信息。
* `CHAIN` 可以是 "eth"、"bsc" 等。
* `WALLET_ADDRESS` 是钱包的0x地址。仅当用户明确要求查看自己的钱包时才需要填写此字段。
* `LIMIT` 是显示的最近交易记录数量（默认为5条）。
* 🚨 输出规则（重要）：
  1. 动作逻辑：将 `from` 和 `to` 与 `WALLET_ADDRESS`（或默认用户）进行比较。如果 `from` 是用户，则表示“出售”；如果 `to` 是用户，则表示“购买”。
  2. 货币逻辑：根据 `CHAIN` 参数动态确定货币符号。
  3. 格式化模板：必须严格按照以下Markdown格式输出每笔交易的提醒信息：


🚨 **NFT出售提醒！**
**集合：** [collection]
**Token ID：** [tokenId]
💰 **交易详情：**
* **操作：** [Buy / Sell]
* **价格：** [salePrice] [Currency]
* **交易对手：** `[from/to]`
* **时间：** [time]
* **交易记录：** [https://[Chain_Scan_Domain]/tx/txHash]


📊 **最新集合统计信息：**
* **当前最低价格：** [floorPrice] [Currency]
* **24小时平均价格：** [avgPrice24h] [Currency]
* **最后交易价格：** [lastTradePrice] [Currency]


💡 **专家分析：** （用英文提供一段简短的分析，比较 `salePrice` 与 `floorPrice`/`lastTradePrice`。）

```bash
CHAIN="bsc"
WALLET_ADDRESS="" 
LIMIT="5"

ACTIVITIES=$(curl -s --request GET \
  --url "[https://api.element.market/openapi/v1/account/activity?chain=$](https://api.element.market/openapi/v1/account/activity?chain=$){CHAIN}&wallet_address=${WALLET_ADDRESS}&event_names=Sale&limit=${LIMIT}" \
  --header "X-Api-Key: ${ELEMENT_API_KEY}" \
  --header "accept: application/json" | jq -c '.data.activityList[].accountActivity | select(. != null)')

JSON_RESULT="["

while IFS= read -r activity; do
  if [ -z "$activity" ]; then continue; fi
  
  CONTRACT=$(echo "$activity" | jq -r '.contractAddress')
  TOKEN_ID=$(echo "$activity" | jq -r '.tokenId')
  PRICE_ETH=$(echo "$activity" | jq -r 'if .price != null then ((.price | tonumber) / 1000000000000000000) else 0 end')
  FROM_ADDR=$(echo "$activity" | jq -r '.fromAddress')
  TO_ADDR=$(echo "$activity" | jq -r '.toAddress')
  TIME=$(echo "$activity" | jq -r '.eventTime')
  TX_HASH=$(echo "$activity" | jq -r '.txHash')

  CONTRACT_RES=$(curl -s --request GET \
    --url "[https://api.element.market/openapi/v1/contract?chain=$](https://api.element.market/openapi/v1/contract?chain=$){CHAIN}&contract_address=${CONTRACT}" \
    --header "X-Api-Key: ${ELEMENT_API_KEY}" \
    --header "accept: application/json")
  
  COLLECTION_NAME=$(echo "$CONTRACT_RES" | jq -r '.data.collection.name // "Unknown"')
  SLUG=$(echo "$CONTRACT_RES" | jq -r '.data.collection.slug // empty')
  IMAGE_URL=$(echo "$CONTRACT_RES" | jq -r '.data.collection.imageUrl // ""')

  FLOOR_PRICE=0
  AVG_PRICE=0
  LAST_PRICE=0
  
  if [ -n "$SLUG" ] && [ "$SLUG" != "null" ]; then
    STATS_RES=$(curl -s --request GET \
      --url "[https://api.element.market/openapi/v1/collection/stats?chain=$](https://api.element.market/openapi/v1/collection/stats?chain=$){CHAIN}&collection_slug=${SLUG}" \
      --header "X-Api-Key: ${ELEMENT_API_KEY}" \
      --header "accept: application/json")
      
    FLOOR=$(echo "$STATS_RES" | jq -r '.data.collectionFloorPrice.floorPriceSource // empty')
    AVG=$(echo "$STATS_RES" | jq -r '.data.stats1D.avgPrice // empty')
    LAST=$(echo "$STATS_RES" | jq -r '.data.lastTradePrice // empty')
    
    [ -n "$FLOOR" ] && [ "$FLOOR" != "null" ] && FLOOR_PRICE=$FLOOR
    [ -n "$AVG" ] && [ "$AVG" != "null" ] && AVG_PRICE=$AVG
    [ -n "$LAST" ] && [ "$LAST" != "null" ] && LAST_PRICE=$LAST
  fi

  ITEM=$(jq -n \
    --arg name "$COLLECTION_NAME" \
    --arg image "$IMAGE_URL" \
    --arg tokenId "$TOKEN_ID" \
    --arg price "$PRICE_ETH" \
    --arg from "$FROM_ADDR" \
    --arg to "$TO_ADDR" \
    --arg time "$TIME" \
    --arg txHash "$TX_HASH" \
    --arg floor "$FLOOR_PRICE" \
    --arg avg "$AVG_PRICE" \
    --arg last "$LAST_PRICE" \
    '{collection: $name, tokenId: $tokenId, image: $image, salePrice: $price, from: $from, to: $to, time: $time, txHash: $txHash, floorPrice: $floor, avgPrice24h: $avg, lastTradePrice: $last}')
    
  JSON_RESULT="${JSON_RESULT}${ITEM},"
done <<< "$ACTIVITIES"

if [ "$JSON_RESULT" = "[" ]; then
  echo "[]"
else
  echo "${JSON_RESULT%?}]"
fi

```

### 查看收到的新报价（报价监控）
🔴 当用户询问“我收到了新的报价吗？”或“监控我的新出价”时，必须使用此工具来查看用户NFT收到的最新报价，并自动添加实时集合统计信息。
* `CHAIN` 可以是 "eth"、"bsc" 等。
* `WALLET_ADDRESS` 是钱包的0x地址。仅当用户明确要求查看自己的钱包时才需要填写此字段。
* `LIMIT` 是要获取的报价数量（默认为10条）。
* 🚨 输出规则（重要）：
  1. 时间过滤：检查每个报价的 `listingTime`，仅显示最近收到的报价。
  2. 货币逻辑：根据 `CHAIN` 参数动态确定货币符号。
  3. 格式化模板：必须严格按照以下Markdown格式输出每条新报价的提醒信息：


🔔 **新NFT报价提醒！**
**物品：** [name]
**集合：** [collection]
💰 **报价详情：**
* **报价价格：** [offerPrice] [Currency]
* **报价者：** `[maker]`
* **报价时间：** [listingTime]


📊 **集合统计信息（24小时）：**
* **当前最低价格：** [floorPrice] [Currency]
* **24小时平均价格：** [avgPrice24h] [Currency]
* **最后交易价格：** [lastTradePrice] [Currency]
* **24小时交易数量：** [saleCount24h]


💡 **专家分析：** （用英文提供一段简短的分析，比较 `offerPrice` 与 `floorPrice` 和 `lastTradePrice`。）

## 🔗 链接
* [API文档](https://element.readme.io/reference/api-overview)
* [创建API密钥](https://element.market/apikeys)
* [主网](https://element.market)