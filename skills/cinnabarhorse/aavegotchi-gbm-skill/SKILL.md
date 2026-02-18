---
name: aavegotchi-gbm-skill
description: 在 Base 主网（8453）上，您可以查看、创建、取消、出价以及竞购 Aavegotchi GBM 拍卖品。该拍卖系统采用 Subgraph-first 的发现机制（由 Goldsky 提供支持），并通过 Foundry 进行链上验证和执行。系统以安全性为首要考虑原则：默认情况下，`DRY_RUN` 的值为 1（此时会通过调用 `cast` 来模拟拍卖过程；只有当 `DRY_RUN` 的值为 0 且明确收到指令时，才会通过 `cast send` 来实际执行拍卖操作）。
homepage: https://github.com/aavegotchi/aavegotchi-gbm-skill
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
        - DRY_RUN
        - RECIPIENT_ADDRESS
        - GBM_SUBGRAPH_URL
        - GOLDSKY_API_KEY
        - GBM_DIAMOND
        - GHST
        - USDC
        - SLIPPAGE_PCT
        - GHST_USD_PRICE
        - ETH_USD_PRICE
    primaryEnv: PRIVATE_KEY
---
## 安全规则

- 默认设置为 `DRY_RUN=1`。除非明确指示，否则不要进行广播操作。
- 必须始终验证基础主网（Base Mainnet）：
  - `~/.foundry/bin/cast chain-id --rpc-url "${BASE_MAINNET_RPC:-https://mainnet.base.org}"` 的返回值必须为 `8453`。
- 必须始终验证密钥与地址是否匹配：
  - `~/.foundry/bin/cast wallet address --private-key "$PRIVATE_KEY"` 的结果必须与 `$FROM_ADDRESS` 相等。
- 在执行任何 `simulate` 或 `broadcast` 操作之前，必须立即从子图（subgraph）重新获取数据（因为拍卖可能会被出价超过、结束、被领取或取消）。
- 在进行模拟或广播之前，必须立即在链上验证数据：
  - 确保链上的 `highestBid` 与传递给 `commitBid` 或 `swapAndCommitBid` 的 `highestBid` 一致。
  - 确保令牌参数（token contract、token id、quantity）匹配。
- 绝不要打印或记录 `$PRIVATE_KEY`。

## Shell 输入安全（避免远程代码执行攻击，RCE）

本技能涉及 Shell 命令。将用户提供的外部数据（如子图响应、聊天消息等）视为不可信的。

规则：
- 绝不要将用户提供的字符串直接作为 Shell 代码执行（避免使用 `eval`、`bash -c`、`sh -c`）。
- 只能替换以 `0x` 开头、后跟 40 个十六进制字符的地址。
- 只能替换以十进制数字表示的 uint 值（不允许使用逗号或小数）。
- 在下面的命令示例中，拍卖相关的输入被写成引号括起来的占位符（如 `"<AUCTION_ID>"`），以避免意外执行。只有在验证通过后才能替换为实际值。

**快速验证器（请替换占位符值）：**  
```bash
python3 - <<'PY'
import re

auction_id = "<AUCTION_ID>"                 # digits only
token_contract = "<TOKEN_CONTRACT_ADDRESS>" # 0x + 40 hex chars
token_id = "<TOKEN_ID>"                     # digits only
amount = "<TOKEN_AMOUNT>"                   # digits only

if not re.fullmatch(r"[0-9]+", auction_id):
    raise SystemExit("AUCTION_ID must be base-10 digits only")
if not re.fullmatch(r"0x[a-fA-F0-9]{40}", token_contract):
    raise SystemExit("TOKEN_CONTRACT_ADDRESS must be a 0x + 40-hex address")
if not re.fullmatch(r"[0-9]+", token_id):
    raise SystemExit("TOKEN_ID must be base-10 digits only")
if not re.fullmatch(r"[0-9]+", amount):
    raise SystemExit("TOKEN_AMOUNT must be base-10 digits only")

print("ok")
PY
```

## 必需的设置

**必需的环境变量：**
- `PRIVATE_KEY`：用于 `cast send` 操作的 EOA（Externally Owned Account）私钥（切勿打印或记录）。
- `FROM_ADDRESS`：拥有 NFT 并将提交交易的 EOA 地址。
- `BASE_MAINNET_RPC`：RPC 请求的 URL。如果未设置，使用 `https://mainnet.base.org`。
- `GBM_SUBGRAPH_URL`：用于拍卖的 Goldsky 子图端点。

**可选的环境变量：**
- `DRY_RUN`：默认值为 `1`，表示仅通过 `cast call` 进行模拟；设置为 `0` 表示通过 `cast send` 进行广播。
- `RECIPIENT_ADDRESS`：用于接收合约退还的多余 GHST 的地址。默认值为 `FROM_ADDRESS`。
- `GOLDSKY_API_KEY`：可选；如果设置，请在子图请求中包含 `Authorization: Bearer ...` 头部。
- `SLIPPAGE_PCT`：默认值为 `1`（百分比）；用于计算 `swapAmount`。
- `GHST_USD_PRICE`、`ETH_USD_PRICE`：可选的覆盖值；如果未设置，将在交换计算中从 CoinGecko 获取。

**推荐的默认值（如需可通过环境变量覆盖）：**  
```bash
export BASE_MAINNET_RPC="${BASE_MAINNET_RPC:-https://mainnet.base.org}"
export GBM_DIAMOND="${GBM_DIAMOND:-0x80320A0000C7A6a34086E2ACAD6915Ff57FfDA31}"
export GHST="${GHST:-0xcD2F22236DD9Dfe2356D7C543161D4d260FD9BcB}"
export USDC="${USDC:-0x833589fCD6eDb6E08f4c7C32D4f71b54BDA02913}"
export GBM_SUBGRAPH_URL="${GBM_SUBGRAPH_URL:-https://api.goldsky.com/api/public/project_cmh3flagm0001r4p25foufjtt/subgraphs/aavegotchi-gbm-baazaar-base/prod/gn}"
export DRY_RUN="${DRY_RUN:-1}"
export SLIPPAGE_PCT="${SLIPPAGE_PCT:-1}"
```

**注意事项：**
- 下面的命令使用了 `~/.foundry/bin/cast`，因此可以在 cron 或非交互式 Shell 中使用。

## 查看/列出拍卖（先查询子图）

有关标准查询方法，请参阅 `references/subgraph.md`。

**按 ID 查看拍卖（快速）：**  
```bash
curl -s "$GBM_SUBGRAPH_URL" -H 'content-type: application/json' ${GOLDSKY_API_KEY:+-H "Authorization: Bearer $GOLDSKY_API_KEY"} --data '{
  "query":"query($id:ID!){ auction(id:$id){ id type contractAddress tokenId quantity seller highestBid highestBidder totalBids startsAt endsAt claimAt claimed cancelled presetId category buyNowPrice startBidPrice } }",
  "variables":{"id":"<AUCTION_ID>"}
}'
```

**按结束时间排序的活跃拍卖（从最早结束的开始）：**  
```bash
NOW=$(date +%s)
curl -s "$GBM_SUBGRAPH_URL" -H 'content-type: application/json' ${GOLDSKY_API_KEY:+-H "Authorization: Bearer $GOLDSKY_API_KEY"} --data "{
  \"query\":\"query(\$now:BigInt!){ auctions(first:20, orderBy: endsAt, orderDirection: asc, where:{claimed:false, cancelled:false, startsAt_lte:\$now, endsAt_gt:\$now}){ id type contractAddress tokenId quantity highestBid highestBidder totalBids startsAt endsAt claimAt presetId category seller } }\",
  \"variables\":{\"now\":\"$NOW\"}
}"
```

## 在出价/发送前进行链上验证

链上的真实数据来源于 GBM diamond。

**确认核心拍卖字段（完整结构解码）：**  
```bash
~/.foundry/bin/cast call "$GBM_DIAMOND" \
  'getAuctionInfo(uint256)((address,uint96,address,uint88,uint88,bool,bool,address,(uint80,uint80,uint56,uint8,bytes4,uint256,uint96,uint96),(uint64,uint64,uint64,uint64,uint256),uint96,uint96))' \
  "<AUCTION_ID>" \
  --rpc-url "$BASE_MAINNET_RPC"
```

**有用的单独获取函数：**  
```bash
~/.foundry/bin/cast call "$GBM_DIAMOND" 'getAuctionHighestBid(uint256)(uint256)' "<AUCTION_ID>" --rpc-url "$BASE_MAINNET_RPC"
~/.foundry/bin/cast call "$GBM_DIAMOND" 'getAuctionHighestBidder(uint256)(address)' "<AUCTION_ID>" --rpc-url "$BASE_MAINNET_RPC"
~/.foundry/bin/cast call "$GBM_DIAMOND" 'getAuctionStartTime(uint256)(uint256)' "<AUCTION_ID>" --rpc-url "$BASE_MAINNET_RPC"
~/.foundry/bin/cast call "$GBM_DIAMOND" 'getAuctionEndTime(uint256)(uint256)' "<AUCTION_ID>" --rpc-url "$BASE_MAINNET_RPC"
~/.foundry/bin/cast call "$GBM_DIAMOND" 'getContractAddress(uint256)(address)' "<AUCTION_ID>" --rpc-url "$BASE_MAINNET_RPC"
~/.foundry/bin/cast call "$GBM_DIAMOND" 'getTokenId(uint256)(uint256)' "<AUCTION_ID>" --rpc-url "$BASE_MAINNET_RPC"
~/.foundry/bin/cast call "$GBM_DIAMOND" 'getTokenKind(uint256)(bytes4)' "<AUCTION_ID>" --rpc-url "$BASE_MAINNET_RPC"
```

## 创建拍卖

**链上方法：**
```solidity
createAuction((uint80, uint80, uint56, uint8, bytes4, uint256, uint96, uint96), address, uint256) -> uint256
```

**高级步骤：**
1. 确保令牌合约已在 GBM diamond 上被列入白名单（否则会返回 `ContractNotAllowed`）。
2. 确保该令牌已获得 GBM diamond 的批准：
   - 对于 ERC721/1155 合约，使用 `setApprovalForAll(GBM_DIAMOND, true)`。
3. 选择 `InitiatorInfo`：
   - `startTime` 必须在未来某个时间点。
   - `endTime - startTime` 必须在 3600 到 604800 秒之间（1 小时到 7 天）。
   - `tokenKind` 必须为 `0x73ad2146`（ERC721）或 `0x973bb640`（ERC1155）。
   - `buyItNowPrice` 是可选的；`startingBid` 也是可选的（如果非零，则需要批准 4% 的预付费费用）。
4. 使用 `cast call` 并指定 `--from "$FROM_ADDRESS"` 进行模拟。
5. 仅当明确指示时（`DRY_RUN=0`），才使用 `cast send` 进行广播。
6. 交易完成后：查询子图以获取最新的卖家拍卖信息，并匹配 `(contractAddress, tokenId)`。

**模拟创建拍卖（以 ERC721 合约为例）：**  
```bash
~/.foundry/bin/cast call "$GBM_DIAMOND" \
  'createAuction((uint80,uint80,uint56,uint8,bytes4,uint256,uint96,uint96),address,uint256)(uint256)' \
  "(<START_TIME>,<END_TIME>,1,<CATEGORY>,0x73ad2146,<TOKEN_ID>,<BUY_NOW_GHST_WEI>,<STARTING_BID_GHST_WEI>)" \
  "<ERC721_CONTRACT_ADDRESS>" "<PRESET_ID>" \
  --from "$FROM_ADDRESS" \
  --rpc-url "$BASE_MAINNET_RPC"
```

**仅当明确指示时进行广播：**  
```bash
~/.foundry/bin/cast send "$GBM_DIAMOND" \
  'createAuction((uint80,uint80,uint56,uint8,bytes4,uint256,uint96,uint96),address,uint256)(uint256)' \
  "(<START_TIME>,<END_TIME>,1,<CATEGORY>,0x73ad2146,<TOKEN_ID>,<BUY_NOW_GHST_WEI>,<STARTING_BID_GHST_WEI>)" \
  "<ERC721_CONTRACT_ADDRESS>" "<PRESET_ID>" \
  --private-key "$PRIVATE_KEY" \
  --rpc-url "$BASE_MAINNET_RPC"
```

**创建拍卖后的操作（查找最新的拍卖并确认结果）：**  
```bash
curl -s "$GBM_SUBGRAPH_URL" -H 'content-type: application/json' ${GOLDSKY_API_KEY:+-H "Authorization: Bearer $GOLDSKY_API_KEY"} --data '{
  "query":"query($seller:Bytes!){ auctions(first:10, orderBy: createdAt, orderDirection: desc, where:{seller:$seller}){ id type contractAddress tokenId quantity createdAt startsAt endsAt claimed cancelled } }",
  "variables":{"seller":"<FROM_ADDRESS_LOWERCASE>"}
}'
```

## 取消拍卖

**链上方法：**
```solidity
cancelAuction(uint256)
```

**步骤：**
1. 在子图中检查 `claimed`、`cancelled`、`endsAt`、`highestBid` 等字段。
2. 在链上调用 `getAuctionInfo(auctionId)` 以验证所有权和状态。
3. 使用 `cast call` 进行模拟（指定 `--from "$FROM_ADDRESS"`）。
4. 仅当明确指示时才进行广播。

**模拟取消操作：**  
```bash
~/.foundry/bin/cast call "$GBM_DIAMOND" 'cancelAuction(uint256)' "<AUCTION_ID>" \
  --from "$FROM_ADDRESS" \
  --rpc-url "$BASE_MAINNET_RPC"
```

**仅当明确指示时进行广播：**  
```bash
~/.foundry/bin/cast send "$GBM_DIAMOND" 'cancelAuction(uint256)' "<AUCTION_ID>" \
  --private-key "$PRIVATE_KEY" \
  --rpc-url "$BASE_MAINNET_RPC"
```

## 使用 GHST 出价（commitBid）

**链上方法：**
```solidity
commitBid(uint256, uint256, uint256, address, uint256, bytes) // 最后的 `bytes` 字段可以忽略；传递 `0x` 作为默认值
```

**步骤：**
1. 在子图中获取拍卖信息（id、contractAddress、tokenId、quantity、highestBid、startsAt、endsAt、claimed/cancelled）。
2. 在链上重新获取 `highestBid` 和令牌参数；必须传递当前的链上 `highestBid`，否则会返回 `UnmatchedHighestBid`。
3. 使用 `references/bid-math.md` 计算安全的最低出价（考虑链上的 `bidDecimals` 和 `stepMin`）。
4. 确保你有足够的 GHST 来支付 `bidAmount`。
5. 可以选择使用 `cast call` 进行模拟（推荐）。
6. 仅当明确指示时才进行广播。

**模拟出价过程：**  
```bash
~/.foundry/bin/cast call "$GBM_DIAMOND" \
  'commitBid(uint256,uint256,uint256,address,uint256,uint256,bytes)' \
  "<AUCTION_ID>" "<BID_AMOUNT_GHST_WEI>" "<HIGHEST_BID_GHST_WEI>" "<TOKEN_CONTRACT_ADDRESS>" "<TOKEN_ID>" "<TOKEN_AMOUNT>" 0x \
  --from "$FROM_ADDRESS" \
  --rpc-url "$BASE_MAINNET_RPC"
```

**仅当明确指示时进行广播：**  
```bash
~/.foundry/bin/cast send "$GBM_DIAMOND" \
  'commitBid(uint256,uint256,uint256,address,uint256,uint256,bytes)' \
  "<AUCTION_ID>" "<BID_AMOUNT_GHST_WEI>" "<HIGHEST_BID_GHST_WEI>" "<TOKEN_CONTRACT_ADDRESS>" "<TOKEN_ID>" "<TOKEN_AMOUNT>" 0x \
  --private-key "$PRIVATE_KEY" \
  --rpc-url "$BASE_MAINNET_RPC"
```

## 使用 USDC 进行交换并提交出价（swapAndCommitBid）

**链上方法：**
```solidity
swapAndCommitBid(address, uint256, uint256, address, uint256, uint256, address, uint256, bytes)
```

**结构字段（按顺序）：**
1. `tokenIn`（USDC）
2. `swapAmount`（USDC 金额，保留 6 位小数）
3. `minGhstOut`（GHST 数量，单位为 wei；必须大于或等于 `bidAmount`）
4. `swapDeadline`（Unix 时间戳；必须在当前时间加上 86400 秒内）
5. `recipient`（接收多余 GHST 的地址）
6. `auctionID`
7. `bidAmount`（GHST 数量）
8. `highestBid`（必须与链上值一致）
9. `tokenContract`
10. `tokenID`
11. `amount`（令牌数量）
12. `_signature`（可以忽略；传递 `0x` 作为默认值）

**计算 `swapAmount` 的方法：**  
参见 `references/swap-math.md`。

**仅当明确指示时进行广播：**  
```bash
~/.foundry/bin/cast call "$GBM_DIAMOND" \
  'swapAndCommitBid((address,uint256,uint256,uint256,address,uint256,uint256,uint256,address,uint256,uint256,bytes))' \
  "($USDC,<SWAP_AMOUNT_USDC_6DP>,<MIN_GHST_OUT_GHST_WEI>,<SWAP_DEADLINE_UNIX>,${RECIPIENT_ADDRESS:-$FROM_ADDRESS},<AUCTION_ID>,<BID_AMOUNT_GHST_WEI>,<HIGHEST_BID_GHST_WEI>,<TOKEN_CONTRACT_ADDRESS>,<TOKEN_ID>,<TOKEN_AMOUNT>,0x)" \
  --from "$FROM_ADDRESS" \
  --rpc-url "$BASE_MAINNET_RPC"
```

## 使用 ETH 进行交换并提交出价（swapAndCommitBid）

**方法与上述相同，但：**
- `tokenIn` 的值为 `0x0000000000000000000000000000000000000000`
- `--value <SWAP_AMOUNT_WEI>` 必须等于你在元组中传递的 `swapAmount` 值。

**仅当明确指示时进行广播：**  
```bash
~/.foundry/bin/cast send "$GBM_DIAMOND" \
  'swapAndCommitBid((address,uint256,uint256,uint256,address,uint256,uint256,uint256,address,uint256,uint256,bytes))' \
  "(0x0000000000000000000000000000000000000000,<SWAP_AMOUNT_WEI>,<MIN_GHST_OUT_GHST_WEI>,<SWAP_DEADLINE_UNIX>,${RECIPIENT_ADDRESS:-$FROM_ADDRESS},<AUCTION_ID>,<BID_AMOUNT_GHST_WEI>,<HIGHEST_BID_GHST_WEI>,<TOKEN_CONTRACT_ADDRESS>,<TOKEN_ID>,<TOKEN_AMOUNT>,0x)" \
  --value "<SWAP_AMOUNT_WEI>" \
  --private-key "$PRIVATE_KEY" \
  --rpc-url "$BASE_MAINNET_RPC"
```

## 领取拍卖物品

**链上方法：**
```solidity
claim(uint256)
batchClaim(uint256[])
```

**领取条件：**
- 拍卖物品的所有者可以在 `now >= endsAt` 时领取。
- 最高出价者可以在 `now >= endsAt + cancellationTime` 时领取。
  - `cancellationTime` 可以从存储槽 12 中获取（详见 `references/recipes.md`）。
- 子图可能会提供 `claimAt` 参数，但必须始终在链上验证其准确性。

**模拟领取过程：**  
```bash
~/.foundry/bin/cast call "$GBM_DIAMOND" 'claim(uint256)' "<AUCTION_ID>" \
  --from "$FROM_ADDRESS" \
  --rpc-url "$BASE_MAINNET_RPC"
```

**仅当明确指示时进行广播：**  
```bash
~/.foundry/bin/cast send "$GBM_DIAMOND" 'claim(uint256)' "<AUCTION_ID>" \
  --private-key "$PRIVATE_KEY" \
  --rpc-url "$BASE_MAINNET_RPC"
```

## 可选：立即购买**

**链上方法：**
```solidity
buyNow(uint256)
swapAndBuyNow(address, uint256, uint256, address, uint256)
```

这些功能不是主要使用场景的必需部分，但与出价流程相关。如果使用它们，请遵循相同的安全措施：
- 从子图重新获取数据。
- 在链上验证价格和状态。
- 使用 `cast call` 进行模拟。
- 仅当明确指示时才进行广播。

## 测试（无需资金）

1. 确保子图可访问（使用 `introspection` 命令可以列出 `auction`、`auctions`、`bid`、`bids` 等信息）：  
```bash
curl -s "$GBM_SUBGRAPH_URL" -H 'content-type: application/json' ${GOLDSKY_API_KEY:+-H "Authorization: Bearer $GOLDSKY_API_KEY"} --data '{ "query":"{ __schema { queryType { fields { name } } } }" }' \
  | python3 -c 'import json,sys; f=[x[\"name\"] for x in json.load(sys.stdin)[\"data\"][\"__schema\"][\"queryType\"][\"fields\"]]; print([n for n in f if n in (\"auction\",\"auctions\",\"bid\",\"bids\")])'
```

2. 确保子图数据完整且无误：  
```bash
curl -s "$GBM_SUBGRAPH_URL" -H 'content-type: application/json' ${GOLDSKY_API_KEY:+-H "Authorization: Bearer $GOLDSKY_API_KEY"} --data '{\"query\":\"query($id:ID!){ auction(id:$id){ id contractAddress tokenId } }\",\"variables\":{\"id\":\"0\"}}'
```

3. 确保链上数据与子图数据一致：  
```bash
~/.foundry/bin/cast call "$GBM_DIAMOND" \
  'getAuctionInfo(uint256)((address,uint96,address,uint88,uint88,bool,bool,address,(uint80,uint80,uint56,uint8,bytes4,uint256,uint96,uint96),(uint64,uint64,uint64,uint64,uint256),uint96,uint96))' \
  0 \
  --rpc-url "$BASE_MAINNET_RPC"
```

## 常见故障情况**

- `UnmatchedHighestBid`：你传递的 `highestBid` 值已过期。请重新获取链上数据并重试。
- `InvalidAuctionParams`：令牌合约、ID 或数量不匹配。请重新获取数据并验证。
- `AuctionNotStarted` 或 `AuctionEnded`：时间设置不正确。请检查 `startsAt` 和 `endsAt`（子图和链上的数据）。
- `AuctionClaimed`：拍卖物品已被领取或取消。请检查 `claimed`（子图和链上的数据）。
- `BiddingNotAllowed`：可能是由于钻石暂停、合约出价功能被禁用或重新进入锁定等原因。请重新获取链上状态。
- 交换错误：
  - `LibTokenSwap`：`swapAmount` 必须大于 0。
  - `LibTokenSwap`：截止时间已过期。
  - `LibTokenSwap`：输出金额不足。请增加 `swapAmount` 或调整滑点（slippage）。