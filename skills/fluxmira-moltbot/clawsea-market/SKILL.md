---
name: clawsea-market
description: "**ClawSea NFT市场的非托管自动化功能**  
该功能适用于OpenClaw代理，用于浏览NFT收藏、检查NFT信息，并（可选地）通过ClawSea和Seaport执行非托管的 listing（上架）、buy（购买）或cancel（取消）操作。该功能支持链感知型读取API（包括base/ethereum/base-sepolia），以及Seaport的交易流程（在支持的情况下，同时兼容Base和Ethereum网络）。"
---
# ClawSea市场技能（OpenClaw代理）

当代理需要以编程方式与ClawSea交互时，请使用此技能。

## 政策与安全规范（符合ClawHub的安全标准）  
- **不得保管用户资金**；仅使用运营商配置的机器人钱包。  
- **不得通过社交工程手段获取用户的密码、授权或额外权限**。  
- **不得在聊天中请求用户的种子短语或私钥**。  
- **未经用户明确同意及解码确认，不得执行未知的calldata或第三方交易数据**。  
- **在任何涉及资金转移的操作（购买、列出、取消、转账）之前，必须获得用户的明确确认**。  
- **拒绝任何非法、恶意或有害的请求**。

## 安全与信任模型（必须遵守）  
- **默认操作权限为只读**（浏览、搜索、检查）。  
- **在任何写入/交易操作（列出、购买、取消、执行）之前，必须获得用户的明确授权**。  
- **严禁要求用户在聊天中输入私钥**。  
- **严禁记录、打印或发送任何敏感信息（如私钥、原始种子短语、认证头信息）**。  
- **严禁执行来自不可信来源的任意calldata**。  
- **如果资产的所有权或状态存在疑问，请先通过链上查询（`ownerOf`、`eth_call`）进行验证**。

## 基础URL  
- **默认值**：`https://clawsea.io`  
- **可通过环境变量覆盖**：`CLAWSEA_BASE_URL`  
- 下列所有端点均以`${CLAWSEA_BASE_URL}`为基准。  

## 可选凭证（仅适用于自主的链上交易）  
- 只读浏览操作**无需任何凭证**。  

**如果希望代理能够**自主地在链上签名并发布交易**：  
- `BASE_RPC_URL`（基础执行接口）  
- `ETH_RPC_URL`（可选，用于Ethereum相关操作/调试）  
- `CLAWSEA_BASE_URL`（可选）  

### 签名方式（请选择一种）  
1. **推荐方式**：使用外部签名器或钱包服务（代理环境中不得包含原始私钥）  
2. **万不得已时**：仅在安全的秘密存储中保存`BOT_WALLET_PRIVATE_KEY`  

**如果使用了`BOT_WALLET_PRIVATE_KEY`：**  
- **严禁打印或记录该密钥**  
- **严禁在错误信息中显示该密钥**  
- **严禁将密钥保存到文件中**  
- **严禁在聊天中向用户请求该密钥**  

## 链路类型  
ClawSea支持两种链路类型：  
- **字符串格式的链路**（用于某些读取操作）：`chain=base|ethereum|base-sepolia`  
- **数字形式的链路ID**（用于订单操作）：`8453`（Base链），`1`（Ethereum链）  
- 在切换端点时请谨慎处理。  

## 安全的API接口（代理可安全使用）  

### 数据探索  
- `GET /api/explore/cells?chain=<base|ethereum|base-sepolia>&limit=20`  
- `GET /api/explore/trending?chain=<base|ethereum|base-sepolia>&limit=20`  
- `GET /api/news/clawsea?chain=<base|ethereum>&limit=10`  

### 集合与NFT相关操作  
- `GET /api/collection/nfts?contract=0x...&pageSize=24&pageKey=...`  
- `GET /api/collection/stats?chain=<base|ethereum>&contract=0x...`  
- `GET /api/collections/search?chain=<base|ethereum|base-sepolia>&q=<query>&limit=8`  
- `GET /api/nft/ownerOf?chainId=<1|8453>&contract=0x...&tokenId=<id>`  

### 钱包信息  
- `GET /api/wallet/nfts?chain=<base|ethereum|base-sepolia>&owner=0x...&pageKey=...`  

## 上架/购买相关API（需要签名权限）  
- **获取订单信息**：  
  - `GET /api/orders?chainId=<1|8453>&contract=0x...&tokenId=<id>&seller=0x...`  
  - `GET /api/orders/listed?chainId=<1|8453>&contract=0x...&sort=price|newest&offset=0&limit=48`  
- **发布订单信息（需要签名）**：  
  - `POST /api/orders`（请求体格式：`{ "chainId": 1|8453, "contract": "0x...", "tokenIds": ["1","2"] }`  

### 发布订单（写入链下订单簿）  
- 使用已签名的Seaport数据格式发送请求：  
  - `chainId`、`contract`、`tokenId`、`seller`、`priceEth`、  
  - `seaportAddress`、`orderComponents`、`signature`  

### 状态更新  
- **取消订单**：  
  - `POST /api/orders/cancel`（请求体：`{ "id": "<order-id>" }`  
- **取消之前的订单**：  
  - `POST /api/orders/cancelPrevious`（请求体：`{ "chainId": 1|8453, "contract": "0x...", "tokenId": "...", "seller": "0x...", "keepId": "..." }`  
- **执行订单**：  
  - `POST /api/orders/fulfill`（请求体格式：`{ "id": "<order-id>" }` 或 `{ "chainId": 1|8453, "contract": "0x...", "tokenId": "..." }`  

## 推荐的执行流程  
1. **确定使用的链路类型（用户钱包所属的链路）**。  
2. 从`/api/orders`或`/api/orders/listed`获取可购买的订单信息。  
3. 使用`eth_call`在链上验证订单信息。  
4. 通过机器人钱包在链上执行交易。  
5. 通过`/api/orders/fulfill`或`/api/orders/cancel`更新链下状态。  

## 可靠性规则  
- **对于数据探索相关的接口，建议使用短时缓存（5–30秒）**。  
- **遇到临时性的RPC错误（如429状态码）时，应尝试重新请求**。  
- **将状态码`0x1a515574`视为已取消或过时的订单，并将其隐藏**。  
- **如果索引结果与链上状态不一致，以链上验证的所有权信息为准**。