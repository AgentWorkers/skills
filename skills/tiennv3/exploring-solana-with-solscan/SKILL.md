---
name: exploring-solana-with-solscan
description: 使用此技能通过 Solscan Pro API 查询 Solana 区块链数据。支持的功能包括：查找钱包地址、查询代币价格、分析 NFT 收藏、检查交易记录、探索去中心化金融（DeFi）活动、获取账户元数据/标签、获取区块信息、监控 API 使用情况以及按关键词搜索代币。
version: 2.0.0
license: MIT
---
# Solscan Pro 技能

该技能使 AI 代理能够检索 Solana 区块链上的专业级数据，涵盖账户、代币、NFT、交易、区块、市场和程序等信息。

## 何时使用此技能

- 当用户询问 Solana 钱包地址、余额、投资组合或质押情况时
- 当用户需要了解代币价格、持有者、市场信息或热门代币时
- 当用户需要检查交易签名或解码交易指令时
- 当用户询问 NFT 收藏、项目或最近的 NFT 活动时
- 当用户需要查看 DeFi 活动、转账历史或奖励出口信息时
- 当用户想要查看程序分析或热门平台时

## 先决条件

## 认证

进行私有操作需要 API 密钥和 Omni 种子：
- `SOLSCAN_API_KEY`

所有请求都必须在 HTTP 标头中包含 API 密钥：

## 配置

### API 密钥（私有操作所需）

```bash
export SOLSCAN_API_KEY=YOUR_SOLSCAN_API_KEY
```
**或使用 `.env` 文件**（出于安全考虑推荐）：
```bash
cd exploring-solana-with-solscan
cp .env.example .env
# Edit .env with your credentials
nano .env
```

```http
token: <YOUR_SOLSCAN_API_KEY>
```

基础 URL：`https://pro-api.solscan.io/v2.0`

---

## 工具

### 工具 1 — 直接 API 命令行界面（精确数据）

**使用场景**：当你需要针对特定地址、签名、区块或代币获取精确的、结构化的数据时。

**语法**：`python3 scripts/solscan.py <资源> <操作> [--参数 值]`

### 工具 2 — MCP 自然语言工具

**使用场景**：在用户未提供具体地址时，用于回答一般性的探索性问题。

可用的 MCP 工具：
- `search_transaction_by_signature` — 根据签名查找交易
- `get_account_balance` — 获取钱包的 SOL 余额
- `get_token_metadata` — 获取代币的名称、符号和 decimal 数

---

## API 参考

### 账户

| 操作 | 关键参数 | 返回值 |
|---|---|---|
| `account detail` | `--address` | Lamports、所有者、可执行标志 |
| `account transfers` | `--address` | SPL + SOL 转账历史 |
| `account defi` | `--address` | DeFi 协议交互记录 |
| `account balance-change` | `--address` | 历史 SOL 余额变化 |
| `account transactions` | `--address` | 最近的交易列表 |
| `account portfolio` | `--address` | 带有 USD 价值的代币持有情况 |
| `account tokens` | `--address` | 关联的代币账户 |
| `account stake` | `--address` | 活跃的质押账户 |
| `account reward-export` | `--address` | 质押奖励历史 CSV 文件 |
| `account transfer-export` | `--address` | 转账历史 CSV 文件 |
| `account metadata` | `--address` | 标签、图标、标签、域名、出资者 |
| `account metadata-multi` | `--addresses` | 批量元数据（逗号分隔） |
| `account leaderboard` | — | 按活动量排名的顶级账户 |
| `account defi-export` | `--address` | DeFi 活动 CSV 文件 |

> **`account metadata` 响应字段**：`account_address`, `account_label`, `account_icon`, `account_tags`, `account_type`, `account_domain`, `funded_by`, `tx_hash`, `block_time`

### 代币

| 操作 | 关键参数 | 返回值 |
|---|---|---|
| `token meta` | `--address` | 名称、符号、decimal 数、总供应量 |
| `token meta-multi` | `--addresses` | 批量元数据 |
| `token price` | `--address` | 当前 USD 价格 |
| `token price-multi` | `--addresses` | 批量价格 |
| `token holders` | `--address` | 持有量最高的持有者列表 |
| `token markets` | `--address` | 交易该代币的 DEX 市场 |
| `token transfers` | `--address` | 转账历史 |
| `token defi` | `--address` | DeFi 活动记录 |
| `token defi-export` | `--address` | DeFi 活动 CSV 文件 |
| `token historical` | `--address --type line` | 价格历史图表数据 |
| `token search` | `--query` | 按关键词/名称搜索 |
| `token trending` | — | 当前热门代币 |
| `token list` | — | 所有代币列表 |
| `token top` | — | 按市值排名的顶级代币 |
| `token latest` | — | 新上市的代币 |

### 交易

| 操作 | 关键参数 | 返回值 |
|---|---|---|
| `transaction detail` | `--signature` | 完整的交易详情 |
| `transaction detail-multi` | `--signatures` | 批量交易详情 |
| `transaction last` | — | 最近的交易记录 |
| `transaction actions` | `--signature` | 可读化的解码后的交易操作 |
| `transaction actions-multi` | `--signatures` | 批量解码后的交易操作 |
| `transaction fees` | `--signature` | 费用明细 |

### NFT

| 操作 | 关键参数 | 返回值 |
|---|---|---|
| `nft news` | — | 最新的 NFT 活动信息 |
| `nft activities` | `--address` | NFT 转让/销售历史 |
| `nft collections` | — | 热门 NFT 收藏 |
| `nft items` | `--address` | 收藏中的项目 |

### 区块

| 操作 | 关键参数 | 返回值 |
|---|---|---|
| `block last` | — | 最新的区块 |
| `block detail` | `--block` | 按区块编号获取区块元数据 |
| `block transactions` | `--block` | 区块内的所有交易 |

### 市场

| 操作 | 关键参数 | 返回值 |
|---|---|---|
| `market list` | — | 所有交易池/市场 |
| `market info` | — | 市场概览 |
| `market volume` | — | 24 小时交易量数据 |

### 程序

| 操作 | 关键参数 | 返回值 |
|---|---|---|
| `program list` | — | 所有索引的程序 |
| `program popular` | — | 最常用的程序 |
| `program analytics` | `--address` | 程序的使用情况统计 |

### 监控

| 操作 | 关键参数 | 返回值 |
|---|---|---|
| `monitor usage` | — | 你的 API 密钥使用情况和速率限制 |

---

## 错误处理

| HTTP 代码 | 含义 | 代理操作 |
|---|---|---|
| `400` | 请求错误/地址无效 | 验证地址格式，重试 |
| `401` | 认证失败 | 确保 `token` 标头设置正确 |
| `429` | 超过速率限制 | 等待一段时间后重试 |
| `500` | 内部服务器错误 | 重试一次；如果问题持续存在，请报告 |

所有错误响应都包含 `success: false`, `code` 和 `message` 字段。

---

## 示例工作流程

### 钱包研究工作流程
- [ ] 第一步：`account metadata --address <ADDR>` → 确认钱包标签和类型
- [ ] 第二步：`account portfolio --address <ADDR>` → 获取代币持有情况
- [ ] 第三步：`account transfers --address <ADDR>` → 查看最近的交易记录
- [ ] 第四步：`account defi --address <ADDR>` → 检查 DeFi 协议交互记录

### 代币分析工作流程
- [ ] 第一步：`token meta --address <MINT>` → 确认代币信息
- [ ] 第二步：`token price --address <MINT>` → 获取当前价格
- [ ] 第三步：`token holders --address <MINT>` | 检查持有集中度风险
- [ ] 第四步：`token markets --address <MINT>` | 查找最佳流动性市场

---

## 评估

| 查询 | 预期行为 |
|---|---|
| “钱包 `ABC123` 持有哪些代币？” | 调用 `account portfolio --address ABC123`，返回带有 USD 价值的代币列表 |
| “BONK 的当前价格是多少？” | 调用 `token meta` 确认代币信息，然后调用 `token price`，返回 USD 价格 |
| “解码交易 `XYZ...`” | 调用 `transaction actions --signature XYZ`，返回可读化的交易操作列表 |
| “这是一个已知的钱包吗？” | 调用 `account metadata --address`，如果可用则返回标签/域名 |

---

*资源：[Solscan Pro API 文档](https://pro-api.solscan.io/pro-api-docs/v2.0)*