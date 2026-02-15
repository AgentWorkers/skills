---
name: clawsea-market
description: "**ClawSea（仅支持Base类型的NFT市场）的非托管自动化技能**  
适用于需要代理/机器人浏览ClawSea数据（热门收藏、收藏物品、列表信息、可立即购买的NFT）的情况，以及使用机器人自身的钱包自主发布、购买或取消Seaport订单的场景。  
触发条件包括：  
- 机器人执行交易操作  
- 自动发布/购买NFT  
- 设置最低购买价格  
- 发布自己的NFT  
- 取消NFT列表  
- 查询NFT列表信息  
- 签署Seaport订单  
- 使用ClawSea的API进行交互"
---

# ClawSea NFT市场 — 专为人类设计，同时优化了代理程序的使用体验。

**启用代理程序自主使用ClawSea的功能：**
- 从`https://clawsea.io/api/*`读取市场数据。
- 使用代理程序自己的钱包（非托管式）在**Base主网**上创建/取消NFT列表并购买NFT。

## 必需的环境变量

- `CLAWSEA_BASE_URL`（可选）
  - 默认值：`https://clawsea.io`
  - 用于将机器人指向测试环境（staging）。

- `BASE_RPC_URL`（必需，用于链上操作）
  - 用于读取数据和广播交易信息的RPC端点。

- `BOT_WALLET_PRIVATE_KEY`（必需，用于自主交易）
  - 机器人钱包的私钥，用于签署消息和交易。
  - 请勿公开此密钥，应妥善保管。

## 核心工作流程

### 1) 浏览/发现市场信息

除非另有说明，所有API请求均为**GET**请求。建议使用“cells”端点进行浏览。

**常用端点（默认配置）：**

- 热门收藏品：
  - `GET /api/explore/cells`

- 热门NFT列表（排名信息）：
  - `GET /api/explore/trending`

- 收藏品详情（分页查询）：
  - `GET /api/collection/nfts?contract=0x...`

- NFT列表：
  - `GET /api/orders?contract=0x...&tokenId=...`

- 在收藏品中购买NFT（已上架的代币，按价格排序）：
  - `GET /api/orders/listed?contract=0x...`

**可选的查询参数（服务器端进行限制）：**

- `/api/explore/cells`
  - `limit`（默认值：20）

- `/api/explore/trending`
  - `limit`（默认值：20）

- `/api/collection/nfts`
  - `pageKey`（可选）
  `pageSize`（默认值：24）

- `/api/orders/listed`
  - `sort=price|newest`（默认排序方式：`price`）
  - `offset`（默认值：0）
  - `limit`（默认值：48）

**公平使用指南（重要提示）：**
- 请短暂缓存响应结果，避免频繁的轮询请求。
- 如果收到HTTP `429`错误，请稍后重试。

### 2) 创建NFT列表

**操作步骤：**
1. 确保机器人拥有该NFT，并且该NFT存在于Base主网上。
2. 为NFT合约授权**OpenSea导管**（仅一次）。
3. 设置固定价格的Seaport订单参数（包括Base Seaport地址和导管密钥）。
4. 使用机器人钱包签署EIP-712格式的数据。
5. 将订单信息发布到ClawSea：
  - `POST /api/orders`（提交订单详情、签名以及交易费用）

### 3) 购买NFT（Seaport订单完成）

**操作步骤：**
1. 从`/api/orders`获取目标订单信息。
2. （建议）在花费Gas之前，先模拟`Seaport.validate`和`fulfillOrder`操作。
3. 使用`value`参数在链上提交`fulfillOrder`请求。
4. 尽力更新订单状态为“已完成”：
  - `POST /api/orders/fulfill`（更新订单状态）

### 4) 取消NFT列表

**操作步骤：**
- **链上操作**：调用Seaport的`cancel([OrderComponents])`方法取消订单。
- **链下操作**：通过`POST /api/orders/cancel { id }`在ClawSea用户界面中隐藏该NFT列表。

## 配置资源文件

- `references/endpoints.md` — ClawSea的HTTP端点及常见的响应格式。
- `references/seaport-base.md` — Base Seaport的详细信息及OpenSea导管配置。
- `scripts/clawsea_bot_skeleton.mjs` — 最基本的Node.js脚本框架（仅用于读取链上数据）。

在实现自主购买/列表功能之前，请先阅读相关参考文档。