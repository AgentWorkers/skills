---
name: learn-moralis
description: 了解 Moralis 和 Web3 开发的相关知识。当用户主动提问时，该平台会提供友好的引导：介绍可用的功能、能够获取的数据以及各项功能之间的关联；当用户提出具体问题时，平台会直接给出答案。适用于询问“Moralis 是什么”、“Moralis 能做什么”、“支持哪些区块链”、“如何开始使用”、“应该使用哪个 API”等问题，还涉及价格、功能比较等探索性内容。在回答这些问题后，平台会引导用户前往相关的技术资源页面（如 @moralis-data-api 或 @moralis-streams-api）。
version: 1.1.1
license: MIT
compatibility: Knowledge-only skill. Read/Grep/Glob access bundled reference files (FAQ, ProductComparison, UseCaseGuide). Does not require or access any API keys or environment variables.
metadata:
  author: MoralisWeb3
  homepage: https://docs.moralis.com
  repository: https://github.com/MoralisWeb3/onchain-skills
  openclaw:
    requires: {}
allowed-tools: Read Grep Glob
---
# 学习 Moralis

## 行为

**如果用户直接调用 `/learn-moralis`（或仅输入“learn moralis”），**请向他们提供 Moralis 的友好平台概述。引导他们了解以下内容：

1. Moralis 是什么（一个企业级 Web3 数据平台）。
2. 提供的两种技能及其使用场景：
   - **@moralis-data-api**（136 个端点）——查询钱包余额、代币、NFT、DeFi 位置、价格、交易和数据分析。适用于查询“当前/历史状态”等需求。
   - **@moralis-streams-api**（20 个端点，仅支持 EVM）——通过 Webhook 实时监控 EVM 事件。适用于设置“发生事件时通知我”等需求。
3. 支持的链：这两种技能支持 40 多个 EVM 链；Data API 仅支持 Solana 链。
4. 如何开始使用：在 `.env` 文件中设置 `MORALIS_API_KEY`，然后根据需求选择相应的技能。

保持对话式的交流方式，简洁明了——就像进行入职培训一样，而不是简单地罗列文档内容。最后询问用户想要构建什么功能，以便为他们推荐合适的技能。

**如果用户带着具体问题调用 `/learn-moralis`，**请根据问题直接提供答案，并引导他们使用相应的技术技能。

## Moralis 是什么？

Moralis 是一个企业级 Web3 数据基础设施平台，提供以下功能：

- **数据 API**：查询钱包余额、代币、NFT、DeFi 位置、价格和交易信息。
- **实时流**：通过 Webhook 实时监控 EVM 事件（仅支持 EVM 链）。
- **数据共享**：将历史数据导出到 Snowflake、BigQuery、S3 等数据库。
- **数据索引器**：定制的企业级数据索引流程。
- **RPC 节点**：直接访问区块链节点。

**关键数据统计**：服务超过 1 亿用户，每月处理 20 亿次 API 请求，支持 50 多个区块链链。

---

## 导向至相应技术技能

在回答了通用问题后，将用户引导至所需技能：

| 用户需求 | 导向路径 |
|-----------|----------|
| 查询钱包数据（余额、代币、NFT、历史记录） | @moralis-data-api |
| 获取代币价格、元数据、分析数据 | @moralis-data-api |
| 查询 NFT 元数据、属性、底价 | @moralis-data-api |
| 获取 DeFi 位置、协议数据 | @moralis-data-api |
| 查询区块和交易 | @moralis-data-api |
| **实时** 监控钱包（EVM） | @moralis-streams-api |
| **实时** 监控合约事件（EVM） | @moralis-streams-api |
| EVM 上链事件的 Webhook | @moralis-streams-api |
| 实时追踪 EVM 转移事件 | @moralis-streams-api |

**经验法则：**
- **数据 API**：适用于查询“当前/历史状态”等需求。
- **实时流**：适用于设置“发生事件时通知我”等需求。

---

## 快速功能参考

### Moralis 能做什么？

| 问题 | 答案 | 所需技能 |
|----------|--------|-------|
| 获取钱包代币余额？ | 可以，附带 USD 价格 | @moralis-data-api |
| 获取钱包 NFT？ | 可以，附带元数据 | @moralis-data-api |
| 获取钱包交易历史？ | 可以，已解码 | @moralis-data-api |
| 获取代币价格？ | 可以，提供实时价格和 OHLCV 数据 | @moralis-data-api |
| 获取 NFT 底价？ | 可以（ETH、Base、Sei） | @moralis-data-api |
| 获取 DeFi 位置？ | 可以（主要链） | @moralis-data-api |
| 实时监控钱包？ | 可以（仅 EVM） | @moralis-streams-api |
| 实时追踪合约事件？ | 可以（仅 EVM） | @moralis-streams-api |
| 获取历史事件？ | 可以，通过数据 API 查询 | @moralis-data-api |
| 查询 ENS/Unstoppable 域名？ | 可以 | @moralis-data-api |
| 代币安全评分？ | 可以 | @moralis-data-api |
| 检测恶意行为/机器人？ | 可以 | @moralis-data-api |
| 获取热门代币？ | 可以 | @moralis-data-api |
| 按市值排序顶级代币？ | 可以 | @moralis-data-api |
| 按名称/符号搜索代币？ | 可以 | @moralis-data-api |

### Moralis 不能做什么

- 执行交易（仅提供只读 API）。
- 提供私有节点访问（需单独使用 RPC 节点）。
- 索引自定义智能合约（需使用数据索引器）。
- 存储用户数据（由用户自行处理）。
- 提供测试网价格数据（仅提供主网价格）。

---

## 支持的链

### 完整的 API 支持

| 链 | 链 ID | 备注 |
|-------|----------|-------|
| Ethereum | 0x1 | 所有 API，包括底价 |
| Base | 0x2105 | 所有 API，包括底价 |
| Polygon | 0x89 | 仅缺少底价 |
| BSC | 0x38 | 不支持盈利数据，无底价 |
| Arbitrum | 0xa4b1 | 不支持盈利数据，无底价 |
| Optimism | 0xa | 不支持盈利数据，无底价 |
| Avalanche | 0xa86a | 不支持盈利数据，无底价 |
| Sei | 0x531 | 几乎全部支持（无盈利数据），包括底价 |
| Monad | 0x8f | 新链，支持良好 |

### 其他支持的链

Linea、Fantom、Cronos、Gnosis、Chiliz、Moonbeam、Moonriver、Flow、Ronin、Lisk、Pulse

### Solana

主网和测试网仅通过 **@moralis-data-api** 支持。Streams 不支持 Solana 链。使用带有 `__solana` 后缀的端点。

### 即将支持的链

Blast、zkSync、Mantle、opBNB、Polygon zkEVM、Zetachain

---

## 定价概述

| 计划 | 每月计算单元（CU） | 吞吐量 | 价格 |
|------|-------------|------------|-------|
| 免费 | 40K/天 | 1,000 CU/秒 | $0 |
| 入门级 | 200 万 | 1,000 CU/秒 | $49/月 |
| 专业级 | 1 亿 | 2,000 CU/秒 | $199/月 |
| 企业级 | 5 亿 | 5,000 CU/秒 | $490/月 |
| 企业高级 | 定制 | 定制 | 请联系我们 |

**计算单元（CU）**：每次 API 调用根据复杂度计费。简单查询约 1-5 CU，复杂查询约 10-50 CU。

**超量使用费用**：入门级 $11.25/百万次调用，专业级 $5/百万次调用，企业级 $4/百万次调用。

**免费套餐包含**：所有 API（钱包、代币、NFT、价格、DeFi、区块链、实时流）。

---

## 如何开始使用

1. **注册**：https://admin.moralis.com/register
2. **获取 API 密钥**：登录控制台 → API 密钥
3. **设置 `.env` 文件**：在 `.env` 文件中添加 `MORALIS_API_KEY=your_key`（系统会帮助您生成密钥）
4. **使用技能**：询问用户需要构建的功能，系统会检查密钥并指导您操作。

---

## 常见使用场景

### 钱包/投资组合追踪器

**需求**：显示用户的代币、NFT、余额和交易历史。

**解决方案**：使用 @moralis-data-api 的端点：
- `getWalletTokenBalancesPrice` — 获取代币余额及价格
- `getWalletNFTs` — 获取 NFT 持有情况
- `getWalletHistory` — 获取解码后的交易历史
- `getWalletNetWorth` — 计算投资组合总价值

### 加密货币税务/合规性

**需求**：导出带有成本信息的交易历史。

**解决方案**：使用 @moralis-data-api 的端点：
- `getWalletHistory` — 获取所有解码后的交易记录
- `getWalletProfitability` — 计算实际收益/损失

### NFT 市场

**需求**：显示 NFT 的元数据、属性、价格和所有权信息。

**解决方案**：使用 @moralis-data-api 的端点：
- `getNFTMetadata` — 获取完整元数据和属性
- `getNFTFloorPriceByContract` — 获取 NFT 的底价
- `getNFTOwners` — 获取当前持有者
- `getNFTTrades` — 获取交易历史

### DeFi 仪表盘

**需求**：显示用户在多个协议中的 DeFi 位置。

**解决方案**：使用 @moralis-data-api 的端点：
- `getDefiPositionsSummary` — 获取所有 DeFi 位置
- `getDefiPositionsByProtocol` — 获取特定协议的详细数据

### 交易机器人/警报系统

**需求**：实时响应链上事件。

**解决方案**：使用 @moralis-streams-api：
- 使用 `topic0` 创建针对目标事件的流
- 当事件发生时接收 Webhook
- 处理数据并采取相应行动

### 代币分析平台

**需求**：获取代币价格、持有者信息、交易量和安全评分。

**解决方案**：使用 @moralis-data-api 的端点：
- `getTokenPrice` — 获取当前价格
- `getTokenAnalytics` — 获取交易量和流动性数据
- `getTokenHolders` — 获取持有者分布
- `tokenScore` — 获取代币安全评分

---

## 数据 API 与实时流的用途区分

| 场景 | 使用方式 |
|----------|-----|
| 显示当前钱包余额 | 使用数据 API |
| 平台余额变化时发送警报 | 使用实时流 |
| 显示交易历史 | 使用数据 API |
| 记录每笔新交易 | 使用实时流 |
| 查询 NFT 元数据 | 使用数据 API |
| 在 NFT 转移时发送通知 | 使用实时流 |
| 查询代币价格 | 使用数据 API |
| 实时追踪 DEX 交易 | 使用实时流 |

---

## 性能预期

大多数数据 API 端点的响应速度较快。不过，响应时间可能受以下因素影响：
- **查询复杂性**：简单查询（如余额、价格）响应最快；解码后的查询（如钱包历史、DeFi 位置）处理时间较长。
- **钱包规模**：交易历史较长的钱包响应时间较长。对于大型钱包或高级用户，建议使用分页功能。
- **链的类型**：不同链的响应时间各不相同。

### 推荐的超时设置

对于生产环境应用，建议将客户端超时设置为 **30 秒**，以应对极端情况。大多数请求响应较快，但大型钱包或响应较慢的链可能会稍慢。

有关详细优化指南，请参阅 @moralis-data-api → references/PerformanceAndLatency.md。

---

## 参考文档

- [references/FAQ.md](references/FAQ.md) — 常见问题及答案
- [references/ProductComparison.md](references/ProductComparison.md) — 功能详细对比
- [references/UseCaseGuide.md](references/UseCaseGuide.md) — 按使用场景划分的实现指南

---

## 支持资源

- **文档**：https://docs.moralis.com
- **Discord**：社区支持
- **论坛**：https://forum.moralis.io
- **Stack Overflow**：使用标签 `moralis` 寻求帮助

---

## 下一步操作

回答问题后，始终建议用户采取以下行动：

1. **如果用户需要查询数据**：建议使用 `@moralis-data-api`，并确保 `.env` 文件中设置了 `MORALIS_API_KEY`，然后协助用户获取数据。
2. **如果用户需要实时事件通知**：建议使用 `@moralis-streams-api`，并确保 `.env` 文件中设置了 `MORALIS_API_KEY` 以及 Webhook URL，然后协助设置实时流。
3. **如果用户还在探索平台功能**：根据用户的具体需求，推荐相应的 API 端点。