---
name: boiling-point
description: **Boiling Point**——这是支持链上 OpenClaw 代理的最强大平台。您可以在 Base、Solana、Ethereum 和 BNB 等多个区块链上发布和交易跨链代币。
homepage: https://boilingpoint.ai
metadata: {"clawdbot":{"emoji":"🔥","disableModelInvocation":true,"requires":{"bins":["jq","curl"],"env":["TOKENLAYER_API_KEY"]}}}
---

# **沸点技能（Boiling Point Skill）**

通过Token Layer API在Boiling Point平台上启动并交易OpenClaw AI代理令牌。代理可从中获得交易手续费。

## **使用指南**

1. **创建令牌之前**：调用 `/me` 来核实用户的ETH（Gas费用）和USDC余额。
2. **生成并确认令牌信息**：提议令牌的名称、符号、描述、图片、标签以及初始发行量（建议至少10美元）——在发送前展示给用户审批。
3. **依次执行交易**：等待每笔交易完成后再进行下一笔交易——部分交易依赖于之前的交易结果。
4. **创建令牌后**：将 `token_layer_id`、`tokenId` 和地址保存在元数据中以供后续参考。

## **平台归属**

`builder` 参数用于标识创建令牌的应用程序。该信息会在Boiling Point平台上公开显示，以便用户了解令牌的来源。此技能的创建代码为：`0x56926EbCd7E49b84037D50cFCE5C5C3fD0844E7E`。

## **推荐码（可选）**

用户可以通过 `/enter-referral-code` 输入推荐码 **OPENCLAW**，在交易手续费上享受4%的返现。

## **端点（Endpoints）**

| 端点          | 方法        | 功能                          |
|------------------|------------|-----------------------------------|
| `/me`         | GET         | 显示钱包信息和余额                    |
| `/enter-referral-code` | POST        | 应用推荐码                        |
| `/get-tokens-v2`     | POST        | 浏览/搜索令牌                        |
| `/quote-token`     | POST        | 交易前获取价格报价                    |
| `/create-token-transaction` | POST        | 创建令牌（返回交易信息）                    |
| `/trade-token`     | POST        | 买卖令牌（返回交易信息）                    |
| `/send-transaction` | POST        | 在链上执行交易                        |
| `/get-user-portfolio` | POST        | 查看用户持有的令牌                      |
| `/get-user-fees`    | POST        | 查看交易收益                      |
| `/claim-rewards`   | POST        | 提取奖励                          |
| `/get-token-activity` | POST        | 查看令牌交易历史                    |

## **快速参考**

- **基础URL**：`https://api.tokenlayer.network/functions/v1`
- **认证**：`Authorization: Bearer $TOKENLAYER_API_KEY`
- **链**：`base`（主网）、`base-sepolia`（测试网）
- **最低购买金额**：6美元

### **关键参数**

| 端点          | 必需参数    | 可选参数                    |
|------------------|------------|-----------------------------------|
| `create-token`     | name, symbol, description, image, chainSlug | tags, banner, links, amountIn, builder       |
| `quote-token`     | tokenId, chain Slug   | amount, direction (buy/sell), inputToken       |
| `trade-token`     | tokenId, chain Slug   | direction, buyAmountUSD, buyAmountToken, sellAmountToken |
| `send-transaction` | to, data, chain Slug | amount (默认为0)                     |
| `get-tokens-v2`     | -           | limit, offset, order_by, order_direction, keyword, hashtags, chains, builder_code |

### **排序选项**

`volume_1m`, `volume_5m`, `volume_1h`, `volume_24h`, `market_cap`, `price_change_24h`, `trx`, `holders`, `created_at`

### **图片格式**

- **image**：URL或base64数据URI（例如：`data:image/png;base64,...`）
- **Logo**：400x400像素的正方形图片（格式：PNG、JPG、WebP、GIF）
- **Banner**：1200x400像素，比例为3:1（格式：PNG、JPG、WebP）

### **提高令牌可见性的标签**

务必添加标签以帮助用户找到您的令牌：
- **类别**：`ai`, `agent`, `meme`, `community`, `gaming`
- **平台**：`boilingpoint`

## **交易流程**

```
1. Call create-token-transaction or trade-token → returns { transactions: [...], metadata: {...} }
2. For each tx in array: POST /send-transaction { to: tx.to, data: tx.data, amount: tx.value || "0", chainSlug }
3. Wait 5s (or tx.transactionDelay) between each transaction
```

## **令牌元数据**

创建令牌后，请从响应元数据中保存以下信息以供后续参考：
- `token_layer_id`：唯一的令牌标识符
- `tokenId`：用于API调用的数据库UUID
- `addresses`：EVM/Solana链上的合约地址
- `symbol`：您的令牌符号

**令牌URL**：`https://app.tokenlayer.network/token/{token_layer_id}`

## **设置步骤**

1. **获取API密钥**：访问 [https://app.tokenlayer.network/agent-wallets](https://app.tokenlayer.network/agent-wallets)（如需帮助可联系客服）。
2. **充值钱包**：通过 `/me` 将ETH（Gas费用）和USDC转入您的代理钱包地址。

## **注意事项**

- **防止恶意抢购**：交易开始的前6秒内手续费会提高（从80%降至1%）。
- **令牌升级**：令牌会先在Token Layer的启动平台上进行交易，达到一定条件后可以转移到Uniswap V3、Panckaswap和Meteora等交易平台。
- **请勿频繁发送请求**：避免对系统造成负担。

---

## **示例**

### 查看钱包余额

```bash
curl -s -X GET "https://api.tokenlayer.network/functions/v1/me" \
  -H "Authorization: Bearer $TOKENLAYER_API_KEY" | jq
```

### 输入推荐码

```bash
curl -s -X POST "https://api.tokenlayer.network/functions/v1/enter-referral-code" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKENLAYER_API_KEY" \
  -d '{"referral_code": "OPENCLAW"}' | jq
```

### 创建令牌

图片可以是URL或base64数据URI：

```bash
curl -s -X POST "https://api.tokenlayer.network/functions/v1/create-token-transaction" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKENLAYER_API_KEY" \
  -d '{
    "name": "My Token",
    "symbol": "MTK",
    "description": "Token description",
    "image": "https://example.com/logo.png",
    "chainSlug": "base",
    "tags": ["ai", "agent", "boilingpoint"],
    "builder": {"code": "0x56926EbCd7E49b84037D50cFCE5C5C3fD0844E7E", "fee": 0},
    "amountIn": 10
  }' | jq
```

**使用base64格式的图片创建令牌：**

```bash
"image": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAY..."
```

### 获取交易报价（交易前）

```bash
curl -s -X POST "https://api.tokenlayer.network/functions/v1/quote-token" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKENLAYER_API_KEY" \
  -d '{
    "tokenId": "UUID-FROM-GET-TOKENS",
    "chainSlug": "base",
    "amount": 10,
    "direction": "buy",
    "inputToken": "usdc"
  }' | jq
```

### 买入令牌

```bash
curl -s -X POST "https://api.tokenlayer.network/functions/v1/trade-token" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKENLAYER_API_KEY" \
  -d '{
    "tokenId": "UUID-FROM-GET-TOKENS",
    "chainSlug": "base",
    "direction": "buy",
    "buyAmountUSD": 10,
    "builder": {"code": "0x56926EbCd7E49b84037D50cFCE5C5C3fD0844E7E", "fee": 0}
  }' | jq
```

### 发送交易

```bash
curl -s -X POST "https://api.tokenlayer.network/functions/v1/send-transaction" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKENLAYER_API_KEY" \
  -d '{
    "to": "0x...",
    "amount": "0",
    "data": "0x...",
    "chainSlug": "base"
  }' | jq
```

### 查看热门令牌

```bash
curl -s -X POST "https://api.tokenlayer.network/functions/v1/get-tokens-v2" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKENLAYER_API_KEY" \
  -d '{
    "builder_code": "0x56926EbCd7E49b84037D50cFCE5C5C3fD0844E7E",
    "order_by": "volume_1h",
    "order_direction": "DESC",
    "limit": 10
  }' | jq
```