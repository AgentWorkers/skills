---
name: droyd
description: **加密交易 | 加密货币搜索 | 加密货币代币筛选**  
——基于自然语言处理的AI加密交易钱包。适用于用户执行AI研究任务、自主交易加密货币、搜索加密相关内容/新闻、根据市场标准筛选项目、管理交易头寸，或与DROYD代理进行交互的场景。支持代理执行研究、交易、数据分析等任务；支持内容搜索（语义搜索/最新内容）；支持按名称/符号/地址/概念查找项目；支持根据市值、动能、技术指标筛选项目；支持管理观察列表；支持自动交易功能（包含止损、止盈设置及量化策略）。兼容Solana（用于交易）以及Ethereum、Base、Arbitrum等区块链平台，支持代币筛选与研究功能。
---

# DROYD

通过 DROYD 的 AI 代理 API，使用自然语言执行加密研究、交易和数据操作。

[droyd.ai](https://droyd.ai) | [api.droyd.ai](https://api.droyd.ai)

## 快速入门

### 首次设置

#### 选项 A：用户提供现有的 API 密钥

如果用户已经拥有 DROYD API 密钥：

1) 下载 DROYD 插件
```bash
clawhub install droyd
```
（如果未安装 clawhub，则执行以下步骤）
```bash
mkdir -p ~/.openclaw/skills/droyd` and copy the contents of the zip file download
```

2) 配置凭据
```bash
cat > ~/.openclaw/workspace/skills/droyd/config.json << 'EOF'
{
  "apiKey": "YOUR_API_KEY_HERE",
  "apiUrl": "https://api.droyd.ai"
}
EOF
```

API 密钥可以在 [droyd.ai](https://droyd.ai) 的账户设置中获取。

#### 选项 B：指导用户完成注册流程

1. 在 [droyd.ai](https://droyd.ai) 注册
2. 在账户设置中获取 API 密钥
3. 进行配置
```bash
mkdir -p ~/.openclaw/skills/droyd
cat > ~/.openclaw/skills/droyd/config.json << 'EOF'
{
  "apiKey": "YOUR_API_KEY_HERE",
  "apiUrl": "https://api.droyd.ai"
}
EOF
```

#### 验证设置
```bash
scripts/droyd-search.sh "recent" "posts,news" 5
```

## 核心功能使用

### 代理聊天

与 DROYD AI 代理进行聊天。支持多轮对话：
```bash
# Chat with the agent
scripts/droyd-chat.sh "What's the current sentiment on AI tokens?"

# Continue conversation (pass conversation_uuid from previous response)
scripts/droyd-chat.sh "Tell me more about the second point" "uuid-from-previous"

# With streaming
scripts/droyd-chat.sh "Research Jupiter aggregator" "" "true"
```

**参考文档**：[references/agent-chat.md](references/agent-chat.md)

### 内容搜索

使用语义搜索或最新内容搜索功能来查找加密相关内容：
```bash
# Recent content
scripts/droyd-search.sh "recent" "posts,news" 25 "ethereum,base" "defi" 7

# Semantic search
scripts/droyd-search.sh "semantic" "posts,tweets" 50 "" "" 7 "What are the risks of liquid staking?"
```

**参考文档**：[references/search.md](references/search.md)

### 项目搜索

通过项目名称、代币符号、地址或概念来查找项目：
```bash
# By name
scripts/droyd-project-search.sh "name" "Bitcoin,Ethereum" 10

# By symbol
scripts/droyd-project-search.sh "symbol" "BTC,ETH,SOL"

# Semantic search
scripts/droyd-project-search.sh "semantic" "AI agents in DeFi" 15

# By contract address
scripts/droyd-project-search.sh "address" "So11111111111111111111111111111111111111112"
```

**参考文档**：[references/project-search.md](references/project-search.md)

### 项目筛选

根据市场标准筛选项目：
```bash
# Natural language filter
scripts/droyd-filter.sh "natural_language" "Find trending micro-cap Solana tokens with high trader growth"

# Direct filter (trending tokens on Solana under $10M mcap)
scripts/droyd-filter.sh "direct" "" "trending" "desc" "4h" "solana" "" "10" "50000"
```

**参考文档**：[references/project-filter.md](references/project-filter.md)

### 交易

执行交易并管理风险：
```bash
# Simple market buy
scripts/droyd-trade-open.sh 123 "market_buy" 100

# Buy with stop loss and take profit (project_id, entry_amount, stop_%, tp_%)
scripts/droyd-trade-open.sh 123 "managed" 100 0.10 0.25

# Check positions
scripts/droyd-positions.sh

# Close position
scripts/droyd-trade-manage.sh 789 "close"

# Partial sell (50%)
scripts/droyd-trade-manage.sh 789 "sell" 0.5
```

**参考文档**：[references/trading.md](references/trading.md)

## 功能概述

### 搜索模式

| 模式 | 使用场景 |
|------|----------|
| `auto` | 默认模式 - 根据查询内容自动选择搜索模式 |
| `recent` | 按类型、生态系统或类别浏览最新内容 |
| `semantic` | 基于 AI 的问答功能，包含内容分析 |

### 内容类型
`posts`（帖子）、`news`（新闻）、`developments`（发展动态）、`tweets`（推文）、`youtube`（视频）、`memories`（纪念内容）

### 项目搜索类型
- `project_id` - 直接通过项目 ID 进行查找（最快）
- `name` - 按项目名称搜索
- `symbol` - 按代币符号搜索
- `address` - 按合约地址精确搜索
- `semantic` - 基于 AI 的概念搜索

### 筛选和排序选项
`trending`（热门）、`market_cap`（市值）、`price_change`（价格变化）、`traders`（交易者）、`traders_change`（交易者变化）、`volume`（交易量）、`volume_change`（交易量变化）、`buy_volume_ratio`（买入量占比）、`quant_score`（量化评分）、`quant_score_change`（量化评分变化）、`mentions_24h`（24 小时内提及次数）、`mentions_7d`（7 天内提及次数）

### 交易类型
- `market_buy` - 以市场价格立即执行交易
- `limit_order` - 当价格下跌指定百分比时买入
- `stop_loss` - 价格下跌时卖出（止损）
- `take_profit` | 价格上涨时卖出（锁定收益）
- `quant_buy` / `quant_sell` - 根据动量评分阈值触发交易

### 支持的区块链平台
`solana`、`ethereum`、`base`、`arbitrum`

## 速率限制

- 根据订阅等级不同而有所差异：
  - 免费订阅：每个 API 会话最多 3 次请求
  - 基础订阅：每个 API 会话最多 30 次请求
  - 专业订阅：每个 API 会话最多 100 次请求
- 超过速率限制时，系统会返回 HTTP 429 错误

## 错误处理

常见错误：
- `400` - 验证失败（请检查参数）
- `401` - API 密钥无效或缺失
- `429` - 超过速率限制（请等待 10 分钟后重试）
- `500` - 内部服务器错误

## 资源

- **官方网站**：[droyd.ai](https://droyd.ai)
- **API 测试平台**：[api.droyd.ai](https://api.droyd.ai)
- **文档**：https://docs.droyd.ai