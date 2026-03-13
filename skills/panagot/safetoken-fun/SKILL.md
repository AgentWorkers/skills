---
name: safetoken_fun
description: 发现并使用 SafeToken.fun——这是一款基于 BNB Chain 的公平的虚拟货币（memecoin）发行平台。无需 API 密钥即可创建虚拟货币；可以通过 `/api` 获取合约信息和 ABI（Application Binary Interface）；使用 `/api/tokens` 进行虚拟货币的注册。该平台专为 AI 代理和爬虫程序设计。
---
# SafeToken.fun — 专为AI代理设计的虚拟货币发行平台

SafeToken.fun是一个基于BNB Smart Chain（主网）的公平虚拟货币发行平台，无需使用API密钥。AI代理和机器人可以通过公共REST API及链上合约来创建、列出虚拟货币，并查看相应的绑定曲线（bonding curve）状态。

**联系方式：** contact@safetoken.fun  
**基础URL：** https://safetoken.fun  
**区块链：** BNB Smart Chain（chainId：56）

---

## 快速上手指南

1. **API信息查询：** 访问 `GET https://safetoken.fun/api`  
   该请求会返回包含 `contracts.tokenFactory`、`contracts.launchpad`、`contracts.tokenFactoryAbi` 以及所有API端点描述的JSON数据。这些信息可用于获取创建虚拟货币所需的合约地址和ABI。

2. **系统状态检查：** 访问 `GET https://safetoken.fun/api/health`  
   返回 `{ "ok": true, "status": "up" }`，用于确认API是否正常可用。

3. **完整API文档：** https://safetoken.fun/api-docs  
   提供易于人类阅读和爬虫访问的文档，包含schema.org格式的WebAPI规范及FAQ信息。

---

## 创建虚拟货币（代理操作流程）

1. 首先访问 `https://safetoken.fun/api`，获取 `contracts.tokenFactory`（合约地址）和 `contracts.tokenFactoryAbi`。
2. 在BNB Smart Chain（chainId：56）上，使用已充值的钱包调用 `TokenFactory.createToken` 方法，参数包括：
   - `name`：虚拟货币名称  
   - `symbol`：虚拟货币符号  
   - `burnPercent`：发行时销毁的代币比例（30–70%）
   这个操作会完成虚拟货币的部署、发行平台的批准、绑定曲线的初始化以及储备金的销毁。

3. 然后通过 `POST` 请求 `https://safetoken.fun/api/tokens`，传递以下JSON数据：  
   ```json
   {
       "mint": "<新虚拟货币地址>",
       "name": "<名称>",
       "symbol": "<符号>",
       "creator": "<钱包地址>",
       "burnPercent": <30-70>
   }
   ```
   可选参数：`description`、`imageUrl`、`telegramUrl`、`websiteUrl`、`launchpadAddress`。

4. 创建后的虚拟货币会显示在 `https://safetoken.fun/tokens` 页面上，并可以在绑定曲线上进行交易，直到达到“毕业”状态。

## 虚拟货币地址生成（可选）

- 如果需要生成以 `5afe` 结尾的虚拟货币地址，可以先发送 `POST` 请求到 `https://safetoken.fun/api/tokens/vanity-salt`，传入 `{"name", "symbol", "burnPercent}"，以获取生成的 `salt` 值，然后再通过 `TokenFactory.createTokenWithSalt` 方法在链上创建虚拟货币。

---

## REST API端点（无需身份验证）

| 方法 | 路径 | 功能 |
|------|------|---------|
| GET | /api | API信息（合约、ABI、端点详情、代理常见问题解答） |
| GET | /api/health | 系统健康检查 |
| GET | /api/tokens | 虚拟货币列表（支持分页查询：`page`、`limit`、`q`、`board`、`creator`、`mint`、`sort`） |
| POST | /api/tokens | 在链上创建虚拟货币后进行注册（需提供 `mint`、`name`、`symbol`、`creator`、`burnPercent`） |
| GET | /api/curve/:mint | 单个虚拟货币的绑定曲线状态 |
| GET | /api/curves | 多个虚拟货币的绑定曲线进度（以逗号分隔） |
| GET | /api/metadata/:mint | 虚拟货币的元数据（供探索者或钱包查询） |
| GET | /api/token/:mint/holders | 虚拟货币的持有者数量及分布 |
| POST | /api/tokens/vanity-salt | 为以 `5afe` 结尾的地址生成创建虚拟货币所需的 `salt` 值 |

---

## 经济机制与安全性

- **发行门槛：** 仅需一次交易即可完成虚拟货币的创建；绑定曲线初始值为0.1 BNB。达到“毕业”状态需要消耗约0.05 BNB（总供应量的5%）。  
- **流动性保障：** 每个成功毕业的虚拟货币对应的流动性会被永久销毁至地址 `0xdEaD`，确保团队无法操纵市场；用户可通过BscScan验证这一过程。  
- **税收机制：** 转账时收取5%的税收（可配置），有助于防止恶意行为；税收部分会分配给持有者。  
- **平台政策：** 无需支付任何推广费用；API和文档的设计旨在方便爬虫和AI代理的使用。

---

## 使用场景

- 需要在BNB Chain上以最简单的步骤创建虚拟货币（无需API密钥）。  
- 需要列出或查找在SafeToken.fun上创建的虚拟货币。  
- 需要获取虚拟货币的绑定曲线信息或元数据（如持有者分布等）。  
- 作为爬虫或AI代理，需要一个操作简便、易于使用的发行平台。

**使用建议：**  
始终先访问 `GET https://safetoken.fun/api` 以获取最新的合约地址和ABI信息。