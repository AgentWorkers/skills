---
name: aavegotchi-baazaar
description: >
  View, add, and execute Aavegotchi Baazaar listings on Base mainnet (8453).
  Buy with GHST directly or buy with USDC using swapAndBuy*.
  Safety-first: dryRun defaults true (simulate with cast call; only broadcast with cast send when dryRun=false / DRY_RUN=0).
homepage: https://github.com/aavegotchi/aavegotchi-baazaar-skill
metadata:
  openclaw:
    requires:
      bins:
        - cast
        - curl
        - python3
      env:
        - FROM_ADDRESS
        - PRIVATE_KEY
        - BASE_MAINNET_RPC
        - RECIPIENT_ADDRESS
        - DRY_RUN
        - SLIPPAGE_PCT
        - PAYMENT_FEE_PCT_USDC
        - GHST_USD_PRICE
        - DIAMOND
        - GHST
        - USDC
        - SUBGRAPH_URL
    primaryEnv: PRIVATE_KEY
---

## 安全规则

- 默认设置为 `dryRun=true`（`DRY_RUN=1`）。除非明确指示，否则切勿进行广播操作。
- 必须始终验证基础主网（Base mainnet）：
  - 命令 `~/.foundry/bin/cast chain-id --rpc-url "${BASE_MAINNET_RPC:-https://mainnet.base.org}"` 的返回值必须为 `8453`。
- 必须始终验证密钥（key）与地址（address）是否匹配：
  - 命令 `~/.foundry/bin/cast wallet address --private-key $PRIVATE_KEY` 的结果必须与 `$FROM_ADDRESS` 相等。
- 在模拟或广播操作之前，必须立即从子图（subgraph）中重新获取列表信息（因为列表可能会被取消、出售或价格更新）。
- 绝不允许打印或记录 `$PRIVATE_KEY`。

## 必需的设置

- **必需的环境变量（Required env vars）**：
  - `PRIVATE_KEY`：用于执行 `cast send` 操作的 EOA（Externally Owned Account）私钥（严禁打印或记录）。
  - `FROM_ADDRESS`：拥有资金/NFT 的 EOA 地址，该地址将负责提交交易。
  - `BASE_MAINNET_RPC`：RPC（Remote Procedure Call）地址。如果未设置，则使用 `https://mainnet.base.org`。

- **基础主网的硬编码常量（Hardcoded Base mainnet constants）**（如有需要，可通过环境变量进行覆盖）：
```bash
export BASE_MAINNET_RPC="${BASE_MAINNET_RPC:-https://mainnet.base.org}"
export DIAMOND="${DIAMOND:-0xA99c4B08201F2913Db8D28e71d020c4298F29dBF}"
export GHST="${GHST:-0xcD2F22236DD9Dfe2356D7C543161D4d260FD9BcB}"
export USDC="${USDC:-0x833589fCD6eDb6E08f4c7C32D4f71b54BDA02913}"
export SUBGRAPH_URL="${SUBGRAPH_URL:-https://api.goldsky.com/api/public/project_cmh3flagm0001r4p25foufjtt/subgraphs/aavegotchi-core-base/prod/gn}"
```

- **可选的环境变量（Optional env vars）**：
  - `RECIPIENT_ADDRESS`：默认值为 `FROM_ADDRESS`。
  - `DRY_RUN`：默认值为 `1`，表示仅通过 `cast call` 进行模拟；设置为 `0` 表示通过 `cast send` 进行广播。
  - `SLIPPAGE_PCT`：默认值为 `1`，用于计算 USDC 的交换金额。
  - `PAYMENT_FEE_PCT_USDC`：默认值为 `1`，用于计算 USDC 的交换金额。
  - `GHST_USD_PRICE`：可选的环境变量；如果未设置，将在 USDC 交易过程中从 CoinGecko 获取相关价格。

- **注意事项**：
  - 下面的命令使用 `~/.foundry/bin/cast`（在 cron 或非交互式 shell 中可正常使用）。如果 `cast` 已添加到 `PATH` 中，可以直接使用 `cast` 代替 `~/.foundry/bin/cast`。
  - 相关的地址和端点信息请参阅 `references/addresses.md` 和 `references/subgraph.md`。

## 查看列表信息（子图）

- **子图端点（Subgraph endpoint）**（Goldsky）：
  - 默认值：`$SUBGRAPH_URL`（详见上面的导出配置）。
  - URL：`https://api.goldsky.com/api/public/project_cmh3flagm0001r4p25foufjtt/subgraphs/aavegotchi-core-base/prod/gn`

- **按 ID 获取 ERC721 列表信息**：
```bash
curl -s "$SUBGRAPH_URL" -H 'content-type: application/json' --data '{
  "query":"query($id: ID!){ erc721Listing(id:$id){ id category erc721TokenAddress tokenId seller priceInWei cancelled timeCreated timePurchased } }",
  "variables":{"id":"1"}
}'
```

- **按 ID 获取 ERC1155 列表信息**：
  - 子图中的字段名为 `erc1155TypeId`（该字段与链上的 `typeId` 或 `itemId` 参数相对应）。
```bash
curl -s "$SUBGRAPH_URL" -H 'content-type: application/json' --data '{
  "query":"query($id: ID!){ erc1155Listing(id:$id){ id category erc1155TokenAddress erc1155TypeId quantity seller priceInWei cancelled sold timeCreated } }",
  "variables":{"id":"1"}
}'
```

- **查找活跃的列表**：
  - ERC721：`where:{cancelled:false, timePurchased:\"0\"}`  
  - ERC1155：`where:{cancelled:false, sold:false}`

- **示例**（按最新时间顺序显示活跃的 ERC721 列表）：
```bash
curl -s "$SUBGRAPH_URL" -H 'content-type: application/json' --data '{
  "query":"query{ erc721Listings(first:20, orderBy:timeCreated, orderDirection:desc, where:{cancelled:false, timePurchased:\"0\"}){ id erc721TokenAddress tokenId priceInWei seller timeCreated } }"
}'
```

- **示例**（按最新时间顺序显示活跃的 ERC1155 列表）：
```bash
curl -s "$SUBGRAPH_URL" -H 'content-type: application/json' --data '{
  "query":"query{ erc1155Listings(first:20, orderBy:timeCreated, orderDirection:desc, where:{cancelled:false, sold:false}){ id erc1155TokenAddress erc1155TypeId quantity priceInWei seller timeCreated } }"
}'
```

## 执行购买操作（使用 GHST）

- **Diamond 上的链上方法（Onchain methods）**：
  - `executeERC721ListingToRecipient(uint256 listingId, address contractAddress, uint256 priceInWei, uint256 tokenId, address recipient)`
  - `executeERC1155ListingToRecipient(uint256 listingId, address contractAddress, uint256 itemId, uint256 quantity, uint256 priceInWei, address recipient)`

- **总成本计算**：
  - ERC721：`totalCostGhstWei = priceInWei`
  - ERC1155：`totalCostGhstWei = priceInWei * quantity`（但在调用方法时仍需分别传递 `quantity` 和 `priceInWei`）

- **购买前的准备**：
  1. 从子图中获取列表详情（包括 ID、代币合约地址、TokenId、类型 ID、数量和价格）。
  2. 检查用户的 GHST 余额和权限是否足够，并根据需要准备必要的批准操作（详见 `references/recipes.md`）。

- **ERC721 购买的模拟测试（Dry-run）**：
```bash
~/.foundry/bin/cast call "$DIAMOND" \
  'executeERC721ListingToRecipient(uint256,address,uint256,uint256,address)' \
  "$LISTING_ID" "$ERC721_TOKEN" "$PRICE_IN_WEI" "$TOKEN_ID" "${RECIPIENT_ADDRESS:-$FROM_ADDRESS}" \
  --from "$FROM_ADDRESS" \
  --rpc-url "${BASE_MAINNET_RPC:-https://mainnet.base.org}"
```

- **实际执行 ERC721 购买操作（仅当明确指示时）**：
```bash
~/.foundry/bin/cast send "$DIAMOND" \
  'executeERC721ListingToRecipient(uint256,address,uint256,uint256,address)' \
  "$LISTING_ID" "$ERC721_TOKEN" "$PRICE_IN_WEI" "$TOKEN_ID" "${RECIPIENT_ADDRESS:-$FROM_ADDRESS}" \
  --private-key "$PRIVATE_KEY" \
  --rpc-url "${BASE_MAINNET_RPC:-https://mainnet.base.org}"
```

- **ERC1155 购买的模拟测试（Dry-run）**：
```bash
~/.foundry/bin/cast call "$DIAMOND" \
  'executeERC1155ListingToRecipient(uint256,address,uint256,uint256,uint256,address)' \
  "$LISTING_ID" "$ERC1155_TOKEN" "$TYPE_ID" "$QUANTITY" "$PRICE_IN_WEI" "${RECIPIENT_ADDRESS:-$FROM_ADDRESS}" \
  --from "$FROM_ADDRESS" \
  --rpc-url "${BASE_MAINNET_RPC:-https://mainnet.base.org}"
```

- **实际执行 ERC1155 购买操作（仅当明确指示时）**：
```bash
~/.foundry/bin/cast send "$DIAMOND" \
  'executeERC1155ListingToRecipient(uint256,address,uint256,uint256,uint256,address)' \
  "$LISTING_ID" "$ERC1155_TOKEN" "$TYPE_ID" "$QUANTITY" "$PRICE_IN_WEI" "${RECIPIENT_ADDRESS:-$FROM_ADDRESS}" \
  --private-key "$PRIVATE_KEY" \
  --rpc-url "${BASE_MAINNET_RPC:-https://mainnet.base.org}"
```

## 执行购买操作（使用 USDC 进行交换和购买）

- **Diamond 上的链上方法（Onchain methods）**：
  - `swapAndBuyERC721(address tokenIn, uint256 swapAmount, uint256 minGhstOut, uint256 swapDeadline, uint256 listingId, address contractAddress, uint256 priceInWei, uint256 tokenId, address recipient)`
  - `swapAndBuyERC1155(address tokenIn, uint256 swapAmount, uint256 minGhstOut, uint256 swapDeadline, uint256 listingId, address contractAddress, uint256 itemId, uint256 quantity, uint256 priceInWei, address recipient)`

- **必需的计算参数**：
  - `swapDeadline = now + 600`  
  - `minGhstOut = totalCostGhstWei`（必须精确计算）
  - `swapAmount`（以 USDC 为单位，保留 6 位小数）：具体计算方法请参阅 `references/usdc-swap-math.md`

- **购买前的准备**：
  1. 从子图中获取列表详情，并计算 `totalCostGhstWei`。
  2. 将 `swapAmount` 计算为 USDC 单位（结果需四舍五入）。
  3. 确保用户的 Diamond 账户中有足够的 GHST（至少等于 `swapAmount`，详见 `references/recipes.md`）。

- **ERC721 的 USDC 交换+购买操作模拟测试**：
```bash
~/.foundry/bin/cast call "$DIAMOND" \
  'swapAndBuyERC721(address,uint256,uint256,uint256,uint256,address,uint256,uint256,address)' \
  "$USDC" "$SWAP_AMOUNT" "$MIN_GHST_OUT" "$SWAP_DEADLINE" "$LISTING_ID" "$ERC721_TOKEN" "$PRICE_IN_WEI" "$TOKEN_ID" "${RECIPIENT_ADDRESS:-$FROM_ADDRESS}" \
  --from "$FROM_ADDRESS" \
  --rpc-url "${BASE_MAINNET_RPC:-https://mainnet.base.org}"
```

- **ERC1155 的 USDC 交换+购买操作模拟测试**：
```bash
~/.foundry/bin/cast call "$DIAMOND" \
  'swapAndBuyERC1155(address,uint256,uint256,uint256,uint256,address,uint256,uint256,uint256,address)' \
  "$USDC" "$SWAP_AMOUNT" "$MIN_GHST_OUT" "$SWAP_DEADLINE" "$LISTING_ID" "$ERC1155_TOKEN" "$TYPE_ID" "$QUANTITY" "$PRICE_IN_WEI" "${RECIPIENT_ADDRESS:-$FROM_ADDRESS}" \
  --from "$FROM_ADDRESS" \
  --rpc-url "${BASE_MAINNET_RPC:-https://mainnet.base.org}"
```

- **实际执行 ERC721 的 USDC 交换+购买操作（仅当明确指示时）**：
```bash
~/.foundry/bin/cast send "$DIAMOND" \
  'swapAndBuyERC721(address,uint256,uint256,uint256,uint256,address,uint256,uint256,address)' \
  "$USDC" "$SWAP_AMOUNT" "$MIN_GHST_OUT" "$SWAP_DEADLINE" "$LISTING_ID" "$ERC721_TOKEN" "$PRICE_IN_WEI" "$TOKEN_ID" "${RECIPIENT_ADDRESS:-$FROM_ADDRESS}" \
  --private-key "$PRIVATE_KEY" \
  --rpc-url "${BASE_MAINNET_RPC:-https://mainnet.base.org}"
```

- **实际执行 ERC1155 的 USDC 交换+购买操作（仅当明确指示时）**：
```bash
~/.foundry/bin/cast send "$DIAMOND" \
  'swapAndBuyERC1155(address,uint256,uint256,uint256,uint256,address,uint256,uint256,uint256,address)' \
  "$USDC" "$SWAP_AMOUNT" "$MIN_GHST_OUT" "$SWAP_DEADLINE" "$LISTING_ID" "$ERC1155_TOKEN" "$TYPE_ID" "$QUANTITY" "$PRICE_IN_WEI" "${RECIPIENT_ADDRESS:-$FROM_ADDRESS}" \
  --private-key "$PRIVATE_KEY" \
  --rpc-url "${BASE_MAINNET_RPC:-https://mainnet.base.org}"
```

## 添加列表信息

- **Diamond 上的链上方法（Onchain methods）**：
  - `getListingFeeInWei()`
  - `addERC721Listing(address erc721TokenAddress, uint256 tokenId, uint256 category, uint256 priceInWei)`
  - `setERC1155Listing(address erc1155TokenAddress, uint256TypeId, uint256 quantity, uint256 category, uint256 priceInWei)`

- **操作步骤**：
  1. 检查列表费用：
    - 命令 `~/.foundry/bin/cast call "$DIAMOND" 'getListingFeeInWei()(uint256)' --rpc-url "${BASE_MAINNET_RPC:-https://mainnet.base.org}"`
  - 在添加列表之前，确保 NFT 合约具有 `setApprovalForAll($DIAMOND, true)`（适用于 ERC721/ERC1155）权限。
  - 提交列表交易（当 `dryRun=true` 时使用 `cast call` 进行模拟；仅当明确指示时使用 `cast send` 进行广播）。
  - 添加列表后，通过子图查找最新的列表 ID（条件为 `seller=$FROM_ADDRESS`，并按 `timeCreated` 降序排序），确认其与代币/类型 ID 匹配。

- **ERC721 列表的模拟添加**：
```bash
~/.foundry/bin/cast call "$DIAMOND" \
  'addERC721Listing(address,uint256,uint256,uint256)' \
  "$ERC721_TOKEN" "$TOKEN_ID" "$CATEGORY" "$PRICE_IN_WEI" \
  --from "$FROM_ADDRESS" \
  --rpc-url "${BASE_MAINNET_RPC:-https://mainnet.base.org}"
```

- **ERC1155 列表的模拟添加**：
```bash
~/.foundry/bin/cast call "$DIAMOND" \
  'setERC1155Listing(address,uint256,uint256,uint256,uint256)' \
  "$ERC1155_TOKEN" "$TYPE_ID" "$QUANTITY" "$CATEGORY" "$PRICE_IN_WEI" \
  --from "$FROM_ADDRESS" \
  --rpc-url "${BASE_MAINNET_RPC:-https://mainnet.base.org}"
```

## 常见故障情况

- **Diamond：函数不存在**：可能是合约地址错误或函数签名错误（或使用的链路错误）。
- **ERC1155Marketplace：GHST 不足**：用户的余额或权限不足，或者计算出的 `totalCostGhstWei` 有误。
- **ERC1155Marketplace：未获得批准**/批准错误**：可能是因为未执行 `setApprovalForAll` 操作，或者购买操作缺少 ERC20 的批准。
- **交换错误**（例如 `LibTokenSwap：swapAmount 必须大于 0`）：可能是交换金额计算错误或输入信息缺失。
- **列表被取消/出售或价格变更**：在广播之前，需要重新从子图中获取信息并重新进行模拟。