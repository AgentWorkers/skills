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
- 必须始终验证密钥与地址是否匹配：
  - 命令 `~/.foundry/bin/cast wallet address --private-key "$PRIVATE_KEY"` 的返回值必须与 `$FROM_ADDRESS` 相等。
- 在模拟或广播之前，必须立即从子图（subgraph）重新获取列表信息（因为列表信息可能会被取消、出售或价格更新）。
- 绝不允许打印或记录 `$PRIVATE_KEY`。

## Shell 输入安全（避免远程代码执行攻击，RCE）

本技能涉及 Shell 命令。来自用户或外部来源（如子图响应、聊天消息等）的所有值都应被视为不可信的。

规则：
- 绝不要将用户提供的字符串直接作为 Shell 代码执行（避免使用 `eval`、`bash -c`、`sh -c` 等命令）。
- 只能替换以 `0x` 开头、后跟 40 个十六进制字符的地址。
- 只能替换以十进制数字表示的 uint 值（不能包含逗号或小数）。
- 在下面的命令示例中，列表相关的输入被写成了带引号的占位符（如 `"<LISTING_ID>"`），以防止意外地被 Shell 解释。在验证这些值后，请用实际值替换它们。

快速验证工具（请替换占位符内容）：
```bash
python3 - <<'PY'
import re

listing_id = "<LISTING_ID>"  # digits only
token_contract = "<TOKEN_CONTRACT_ADDRESS>"  # 0x + 40 hex chars
price_in_wei = "<PRICE_IN_WEI>"  # digits only

if not re.fullmatch(r"[0-9]+", listing_id):
    raise SystemExit("LISTING_ID must be base-10 digits only")
if not re.fullmatch(r"0x[a-fA-F0-9]{40}", token_contract):
    raise SystemExit("TOKEN_CONTRACT_ADDRESS must be a 0x + 40-hex address")
if not re.fullmatch(r"[0-9]+", price_in_wei):
    raise SystemExit("PRICE_IN_WEI must be base-10 digits only")

print("ok")
PY
```

## 必需的设置

**必需的环境变量：**
- `PRIVATE_KEY`：用于 `cast send` 操作的 EOA（Externally Owned Account）私钥（切勿打印或记录）。
- `FROM_ADDRESS`：拥有资金/NFT 的 EOA 地址，该地址将提交交易。
- `BASE_MAINNET_RPC`：RPC（Remote Procedure Call）URL。如果未设置，则使用 `https://mainnet.base.org`。

**硬编码的基础主网常量（如需可通过环境变量覆盖）：**
```bash
export BASE_MAINNET_RPC="${BASE_MAINNET_RPC:-https://mainnet.base.org}"
export DIAMOND="${DIAMOND:-0xA99c4B08201F2913Db8D28e71d020c4298F29dBF}"
export GHST="${GHST:-0xcD2F22236DD9Dfe2356D7C543161D4d260FD9BcB}"
export USDC="${USDC:-0x833589fCD6eDb6E08f4c7C32D4f71b54BDA02913}"
export SUBGRAPH_URL="${SUBGRAPH_URL:-https://api.goldsky.com/api/public/project_cmh3flagm0001r4p25foufjtt/subgraphs/aavegotchi-core-base/prod/gn}"
```

**可选的环境变量：**
- `RECIPIENT_ADDRESS`：默认值为 `FROM_ADDRESS`。
- `DRY_RUN`：默认值为 `1`，表示仅通过 `cast call` 进行模拟；设置为 `0` 表示通过 `cast send` 进行广播。
- `SLIPPAGE_PCT`：默认值为 `1`，用于计算 USDC 的交换金额。
- `PAYMENT_FEE_PCT_USDC`：默认值为 `1`，用于计算 USDC 的交换金额。
- `GHST_USD_PRICE`：可选的覆盖值；如果未设置，则从 CoinGecko 获取当前 USDC 的价格。

**注意事项：**
- 下面的命令使用 `~/.foundry/bin/cast`（在 cron 或非交互式 Shell 环境中可正常工作）。如果 `cast` 已添加到 `PATH` 中，可以将 `~/.foundry/bin/cast` 替换为 `cast`。
- 标准地址和端点的详细信息请参阅：
  - `references/addresses.md`
  - `references/subgraph.md`

## 查看列表信息（子图）

**子图端点（Goldsky）：**
- 默认值：`$SUBGRAPH_URL`（请参见上面的导出设置）
- URL：`https://api.goldsky.com/api/public/project_cmh3flagm0001r4p25foufjtt/subgraphs/aavegotchi-core-base/prod/gn`

**通过 ID 获取 ERC721 列表信息：**
```bash
curl -s "$SUBGRAPH_URL" -H 'content-type: application/json' --data '{
  "query":"query($id: ID!){ erc721Listing(id:$id){ id category erc721TokenAddress tokenId seller priceInWei cancelled timeCreated timePurchased } }",
  "variables":{"id":"1"}
}'
```

**通过 ID 获取 ERC1155 列表信息：**
- 子图中的字段名为 `erc1155TypeId`（该字段与链上的 `typeId` 或 `itemId` 参数相对应）。
```bash
curl -s "$SUBGRAPH_URL" -H 'content-type: application/json' --data '{
  "query":"query($id: ID!){ erc1155Listing(id:$id){ id category erc1155TokenAddress erc1155TypeId quantity seller priceInWei cancelled sold timeCreated } }",
  "variables":{"id":"1"}
}'
```

**查找活跃的列表：**
- ERC721：`where:{cancelled:false, timePurchased:\"0\"}`  
- ERC1155：`where:{cancelled:false, sold:false}`

**示例（按最新时间排序的活跃 ERC721 列表）：**
```bash
curl -s "$SUBGRAPH_URL" -H 'content-type: application/json' --data '{
  "query":"query{ erc721Listings(first:20, orderBy:timeCreated, orderDirection:desc, where:{cancelled:false, timePurchased:\"0\"}){ id erc721TokenAddress tokenId priceInWei seller timeCreated } }"
}'
```

**示例（按最新时间排序的活跃 ERC1155 列表）：**
```bash
curl -s "$SUBGRAPH_URL" -H 'content-type: application/json' --data '{
  "query":"query{ erc1155Listings(first:20, orderBy:timeCreated, orderDirection:desc, where:{cancelled:false, sold:false}){ id erc1155TokenAddress erc1155TypeId quantity priceInWei seller timeCreated } }"
}'
```

## 执行列表操作（使用 GHST 购买）

**Diamond** 上的链上方法：**
- `executeERC721ListingToRecipient(uint256 listingId, address contractAddress, uint256 priceInWei, uint256 tokenId, address recipient)`  
- `executeERC1155ListingToRecipient(uint256 listingId, address contractAddress, uint256 itemId, uint256 quantity, uint256 priceInWei, address recipient)`  

**总成本计算：**
- ERC721：`totalCostGhstWei = priceInWei`  
- ERC1155：`totalCostGhstWei = priceInWei * quantity`（但在调用方法时仍需分别传递 `quantity` 和 `priceInWei` 参数）  

**购买前步骤：**
1. 从子图获取列表详细信息（ID、代币合约地址、TokenId、类型ID、数量、价格）。
2. 检查 GHST 的余额/权限，并在需要时准备批准操作（请参阅 `references/recipes.md`）。

**模拟 ERC721 购买操作：**
```bash
~/.foundry/bin/cast call "$DIAMOND" \
  'executeERC721ListingToRecipient(uint256,address,uint256,uint256,address)' \
  "<LISTING_ID>" "<ERC721_TOKEN_ADDRESS>" "<PRICE_IN_WEI>" "<TOKEN_ID>" "${RECIPIENT_ADDRESS:-$FROM_ADDRESS}" \
  --from "$FROM_ADDRESS" \
  --rpc-url "${BASE_MAINNET_RPC:-https://mainnet.base.org}"
```

**实际执行 ERC721 购买操作（仅当明确指示时）：**
```bash
~/.foundry/bin/cast send "$DIAMOND" \
  'executeERC721ListingToRecipient(uint256,address,uint256,uint256,address)' \
  "<LISTING_ID>" "<ERC721_TOKEN_ADDRESS>" "<PRICE_IN_WEI>" "<TOKEN_ID>" "${RECIPIENT_ADDRESS:-$FROM_ADDRESS}" \
  --private-key "$PRIVATE_KEY" \
  --rpc-url "${BASE_MAINNET_RPC:-https://mainnet.base.org}"
```

**模拟 ERC1155 购买操作：**
```bash
~/.foundry/bin/cast call "$DIAMOND" \
  'executeERC1155ListingToRecipient(uint256,address,uint256,uint256,uint256,address)' \
  "<LISTING_ID>" "<ERC1155_TOKEN_ADDRESS>" "<TYPE_ID>" "<QUANTITY>" "<PRICE_IN_WEI>" "${RECIPIENT_ADDRESS:-$FROM_ADDRESS}" \
  --from "$FROM_ADDRESS" \
  --rpc-url "${BASE_MAINNET_RPC:-https://mainnet.base.org}"
```

**实际执行 ERC1155 购买操作（仅当明确指示时）：**
```bash
~/.foundry/bin/cast send "$DIAMOND" \
  'executeERC1155ListingToRecipient(uint256,address,uint256,uint256,uint256,address)' \
  "<LISTING_ID>" "<ERC1155_TOKEN_ADDRESS>" "<TYPE_ID>" "<QUANTITY>" "<PRICE_IN_WEI>" "${RECIPIENT_ADDRESS:-$FROM_ADDRESS}" \
  --private-key "$PRIVATE_KEY" \
  --rpc-url "${BASE_MAINNET_RPC:-https://mainnet.base.org}"
```

## 执行列表操作（使用 USDC 进行交换和购买）

**Diamond** 上的链上方法：**
- `swapAndBuyERC721(address tokenIn, uint256 swapAmount, uint256 minGhstOut, uint256 swapDeadline, uint256 listingId, address contractAddress, uint256 priceInWei, uint256 tokenId, address recipient)`  
- `swapAndBuyERC1155(address tokenIn, uint256 swapAmount, uint256 minGhstOut, uint256 swapDeadline, uint256 listingId, address contractAddress, uint256 itemId, uint256 quantity, uint256 priceInWei, address recipient)`  

**必需的计算参数：**
- `swapDeadline = now + 600`  
- `minGhstOut = totalCostGhstWei`（必须精确计算）  
- `swapAmount`（以 USDC 为单位，保留 6 位小数）：具体计算方法请参阅 `references/usdc-swap-math.md`  

**购买前步骤：**
1. 从子图获取列表详细信息（并计算 `totalCostGhstWei`）。
2. 将 `swapAmount` 计算为 USDC 单位（结果需四舍五入）。
3. 确保 Diamond 账户的 USDC 余额至少为 `swapAmount`（请参阅 `references/recipes.md`）。  

**模拟 ERC721 的 USDC 交换和购买操作：**
```bash
~/.foundry/bin/cast call "$DIAMOND" \
  'swapAndBuyERC721(address,uint256,uint256,uint256,uint256,address,uint256,uint256,address)' \
  "$USDC" "<SWAP_AMOUNT_USDC_6DP>" "<MIN_GHST_OUT_GHST_WEI>" "<SWAP_DEADLINE_UNIX>" "<LISTING_ID>" "<ERC721_TOKEN_ADDRESS>" "<PRICE_IN_WEI>" "<TOKEN_ID>" "${RECIPIENT_ADDRESS:-$FROM_ADDRESS}" \
  --from "$FROM_ADDRESS" \
  --rpc-url "${BASE_MAINNET_RPC:-https://mainnet.base.org}"
```

**模拟 ERC1155 的 USDC 交换和购买操作：**
```bash
~/.foundry/bin/cast call "$DIAMOND" \
  'swapAndBuyERC1155(address,uint256,uint256,uint256,uint256,address,uint256,uint256,uint256,address)' \
  "$USDC" "<SWAP_AMOUNT_USDC_6DP>" "<MIN_GHST_OUT_GHST_WEI>" "<SWAP_DEADLINE_UNIX>" "<LISTING_ID>" "<ERC1155_TOKEN_ADDRESS>" "<TYPE_ID>" "<QUANTITY>" "<PRICE_IN_WEI>" "${RECIPIENT_ADDRESS:-$FROM_ADDRESS}" \
  --from "$FROM_ADDRESS" \
  --rpc-url "${BASE_MAINNET_RPC:-https://mainnet.base.org}"
```

**实际执行 ERC721 的 USDC 交换和购买操作（仅当明确指示时）：**
```bash
~/.foundry/bin/cast send "$DIAMOND" \
  'swapAndBuyERC721(address,uint256,uint256,uint256,uint256,address,uint256,uint256,address)' \
  "$USDC" "<SWAP_AMOUNT_USDC_6DP>" "<MIN_GHST_OUT_GHST_WEI>" "<SWAP_DEADLINE_UNIX>" "<LISTING_ID>" "<ERC721_TOKEN_ADDRESS>" "<PRICE_IN_WEI>" "<TOKEN_ID>" "${RECIPIENT_ADDRESS:-$FROM_ADDRESS}" \
  --private-key "$PRIVATE_KEY" \
  --rpc-url "${BASE_MAINNET_RPC:-https://mainnet.base.org}"
```

**实际执行 ERC1155 的 USDC 交换和购买操作（仅当明确指示时）：**
```bash
~/.foundry/bin/cast send "$DIAMOND" \
  'swapAndBuyERC1155(address,uint256,uint256,uint256,uint256,address,uint256,uint256,uint256,address)' \
  "$USDC" "<SWAP_AMOUNT_USDC_6DP>" "<MIN_GHST_OUT_GHST_WEI>" "<SWAP_DEADLINE_UNIX>" "<LISTING_ID>" "<ERC1155_TOKEN_ADDRESS>" "<TYPE_ID>" "<QUANTITY>" "<PRICE_IN_WEI>" "${RECIPIENT_ADDRESS:-$FROM_ADDRESS}" \
  --private-key "$PRIVATE_KEY" \
  --rpc-url "${BASE_MAINNET_RPC:-https://mainnet.base.org}"
```

## 添加列表信息

**Diamond** 上的链上方法：**
- `getListingFeeInWei()`  
- `addERC721Listing(address erc721TokenAddress, uint256 tokenId, uint256 category, uint256 priceInWei)`  
- `setERC1155Listing(address erc1155TokenAddress, uint256TypeId, uint256 quantity, uint256 category, uint256 priceInWei)`  

**操作步骤：**
1. 检查列表费用：
  - 命令 `~/.foundry/bin/cast call "$DIAMOND" 'getListingFeeInWei()(uint256)' --rpc-url "${BASE_MAINNET_RPC:-https://mainnet.base.org}"`
2. 在发布列表之前，确保 NFT 合约具有 `setApprovalForAll($DIAMOND, true)`（适用于 ERC721/1155）权限。
3. 提交列表交易（当 `dryRun=true` 时使用 `cast call` 进行模拟；仅当明确指示时使用 `cast send` 进行广播）。
4. 列表发布后，通过子图查找最新的列表 ID（条件为 `seller=$FROM_ADDRESS`，并按 `timeCreated` 降序排序），并确认其与 TokenId 和类型ID 匹配。

**模拟 ERC721 列表的添加过程：**
```bash
~/.foundry/bin/cast call "$DIAMOND" \
  'addERC721Listing(address,uint256,uint256,uint256)' \
  "<ERC721_TOKEN_ADDRESS>" "<TOKEN_ID>" "<CATEGORY>" "<PRICE_IN_WEI>" \
  --from "$FROM_ADDRESS" \
  --rpc-url "${BASE_MAINNET_RPC:-https://mainnet.base.org}"
```

**模拟 ERC1155 列表的添加过程：**
```bash
~/.foundry/bin/cast call "$DIAMOND" \
  'setERC1155Listing(address,uint256,uint256,uint256,uint256)' \
  "<ERC1155_TOKEN_ADDRESS>" "<TYPE_ID>" "<QUANTITY>" "<CATEGORY>" "<PRICE_IN_WEI>" \
  --from "$FROM_ADDRESS" \
  --rpc-url "${BASE_MAINNET_RPC:-https://mainnet.base.org}"
```

## 常见故障模式：**
- **Diamond：函数不存在**：可能是合约地址错误或函数签名错误（或链路错误）。
- **ERC1155Marketplace：GHST 不足**：余额或权限不足（或计算出的 `totalCostGhstWei` 有误）。
- **ERC1155Marketplace：未获得批准**/批准错误**：缺少列表的 `setApprovalForAll` 操作，或购买操作缺少 ERC20 的 `approve` 操作。
- **交换错误**（例如 `LibTokenSwap：swapAmount 必须大于 0`）：交换金额计算错误或输入信息缺失。
- **列表被取消/出售或价格更改**：在广播之前，需要从子图重新获取信息并重新进行模拟。