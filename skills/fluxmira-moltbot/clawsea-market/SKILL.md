---
name: clawsea-market
description: "**ClawSea NFT市场的非托管自动化功能**  
当OpenClaw代理需要浏览藏品、检查NFT信息以及通过ClawSea和Seaport执行非托管的列表创建/购买/取消操作时，可使用此功能。该功能支持链式感知的读取API（base/ethereum/base-sepolia），并兼容Seaport的交易流程（在支持的情况下，包括Base和Ethereum网络）。"
required_env_vars:
  - BASE_RPC_URL
  - BOT_WALLET_PRIVATE_KEY
optional_env_vars:
  - ETH_RPC_URL
  - CLAWSEA_BASE_URL
primary_credential: BOT_WALLET_PRIVATE_KEY
credential_justification: "Only required for autonomous onchain signing/broadcast from the bot wallet. Prefer external signer; if private key is used, keep it in secret storage and never expose in chat/logs."
---
# ClawSea市场技能（OpenClaw代理）

当代理需要以编程方式与ClawSea交互时，请使用此技能。

## 政策限制（符合ClawHub的安全标准）  
- 不得保管用户资金；仅使用运营商配置的机器人钱包。  
- 不得通过社交工程手段获取用户的秘密信息、授权或额外权限。  
- 不得在聊天中要求用户提供种子短语或私钥。  
- 未经用户明确批准并解码第三方交易数据之前，不得执行任何操作。  
- 在进行任何资金转移（购买、列出、取消、转账）之前，必须获得用户的明确确认。  
- 拒绝非法、恶意或有害的请求。

## 安全与信任模型（必须遵守）  
- 默认操作为只读（浏览、搜索、检查）。  
- 在执行任何写入或交易操作（列出、购买、取消、履行）之前，必须获得用户的明确授权。  
- 绝不要要求用户在聊天中输入私钥。  
- 绝不要记录、打印或发送任何敏感信息（私钥、原始种子短语、认证头）。  
- 绝不要执行来自不可信来源的任意交易数据。  
- 如果所有权或状态不确定，请先通过链上查询（`ownerOf`、`eth_call`）进行验证。

## 基本URL  
- 默认值：`https://clawsea.io`  
- 可通过环境变量 `CLAWSEA_BASE_URL` 进行覆盖。  
以下所有端点均以 `${CLAWSEA_BASE_URL}` 为基准。

## 必需的环境变量（用于自主交易）  
- `BASE_RPC_URL`（执行基础操作所必需）  
- `ETH_RPC_URL`（推荐用于Ethereum操作/调试）  
- `CLAWSEA_BASE_URL`（可选；默认值为 `https://clawsea.io`）

### 签名选项（请选择一种）  
1. **推荐方案：** 使用外部签名器/钱包提供商（代理环境中不存储原始私钥）  
2. **如果不可避免：** 将 `BOT_WALLET_PRIVATE_KEY` 存储在安全的秘密存储库中。  

如果使用了 `BOT_WALLET_PRIVATE_KEY`：  
- 不得打印或记录该密钥。  
- 不得在错误信息中显示该密钥。  
- 不得将其保存到文件中。  
- 绝不得在聊天中要求用户提供该密钥。

## 链路模型  
ClawSea支持两种链路类型：  
- **字符串链路**：用于某些读取操作（`chain=base|ethereum|base-sepolia`）  
- **数字链路ID**：用于订单操作（`8453` 表示Base链，`1` 表示Ethereum链）  
切换端点时请谨慎操作。

## 读取API（代理安全操作）  
### 发现信息  
- `GET /api/explore/cells?chain=<base|ethereum|base-sepolia>&limit=20`  
- `GET /api/explore/trending?chain=<base|ethereum|base-sepolia>&limit=20`  
- `GET /api/news/clawsea?chain=<base|ethereum>&limit=10`  

### 收藏品/NFT  
- `GET /api/collection/nfts?contract=0x...&pageSize=24&pageKey=...`  
- `GET /api/collection/stats?chain=<base|ethereum>&contract=0x...`  
- `GET /api/collections/search?chain=<base|ethereum|base-sepolia>&q=<query>&limit=8`  
- `GET /api/nft/ownerOf?chainId=<1|8453>&contract=0x...&tokenId=<id>`  

### 钱包信息  
- `GET /api/wallet/nfts?chain=<base|ethereum|base-sepolia>&owner=0x...&pageKey=...`  

## 列表/购买API  
### 读取订单信息  
- `GET /api/orders?chainId=<1|8453>&contract=0x...&tokenId=<id>&seller=0x...`  
- `GET /api/orders/listed?chainId=<1|8453>&contract=0x...&sort=price|newest&offset=0&limit=48`  
- `POST /api/orders/prices` 的请求体：  
  - `{ "chainId": 1|8453, "contract": "0x...", "tokenIds": ["1","2"] }`  

### 发布列表（离线订单簿写入）  
- 使用已签名的Seaport数据发送 `POST /api/orders` 请求：  
  - `chainId`、`contract`、`tokenId`、`seller`、`priceEth`、  
  - `seaportAddress`、`orderComponents`、`signature`  

### 状态更新  
- `POST /api/orders/cancel` 的请求体：`{ "id": "<order-id>" }`  
- `POST /api/orders/cancelPrevious` 的请求体：  
  - `{ "chainId": 1|8453, "contract": "0x...", "tokenId": "...", "seller": "0x...", "keepId": "..." }`  
- `POST /api/orders/fulfill` 的请求体：  
  - `{ "id": "<order-id>" }` 或  
  - `{ "chainId": 1|8453, "contract": "0x...", "tokenId": "..." }`  

## 执行工作流程（推荐）  
1. 确定使用的链路（用户钱包所在的链路）。  
2. 从 `/api/orders` 或 `/api/orders/listed` 获取可购买的物品列表。  
3. 使用 `eth_call` 在链上进行预处理（例如验证订单信息）。  
4. 通过机器人钱包在链上执行交易。  
5. 通过 `/api/orders/fulfill` 或 `/api/orders/cancel` 更新离线状态。

## 可靠性规则  
- 对于查询操作，建议使用短期缓存（5–30秒）。  
- 遇到临时性的RPC错误（如429状态码）时，应尝试重新请求。  
- 将状态更新选择器 `0x1a515574` 视为已取消或过时的订单，并将其隐藏。  
- 如果索引器返回的结果与链上状态不一致，以链上的所有权验证结果为准。