---
name: Crypto & Stock Market Data (Node.js)
description: 免费 tier 不需要 API 密钥。提供专业级别的加密货币和股票市场数据集成服务，支持实时价格查询、公司信息查询以及全球市场分析功能。该平台基于 Node.js 构建，且完全不依赖任何外部库或服务。
---

# 加密货币与股票市场数据技能（Node.js）

这是一套用于获取实时和历史加密货币及股票市场数据的综合工具。该技能通过与专门的市场数据服务器接口，提供高性能、经过身份验证的全球金融统计数据访问服务。所有功能均基于Node.js标准库构建，无需安装任何额外的依赖包（`npm`）。

## 主要功能

| 功能类别 | 描述 |
| :--- | :--- |
| **实时价格** | 获取加密货币和股票的当前价格、市值、24小时交易量和价格变动情况。 |
| **市场发现** | 跟踪按市值排序的热门资产和表现最佳的加密货币。 |
| **智能搜索** | 通过名称或代码符号快速查找加密货币ID或股票代码。 |
| **详细信息** | 获取全面的资产信息，包括社区链接和公司概况。 |
| **精确图表** | 提供开盘价（Open）、最高价（High）、最低价（Low）、收盘价（Close）（OHLC）等蜡烛图数据以及历史价格/成交量时间序列。 |
| **全球指标** | 监控总市值和上市公司的持仓情况。 |

## 工具参考

| 脚本名称 | 主要功能 | 命令示例 |
| :--- | :--- | :--- |
| `get_crypto_price.js` | 获取多种加密货币的价格 | `node scripts/get_crypto_price.js bitcoin` |
| `get_stock_quote.js` | 获取实时股票报价 | `node scripts/get_stock_quote.js AAPL MSFT` |
| `get_company_profile.js` | 获取公司概况 | `node scripts/get_company_profile.js AAPL` |
| `search_stocks.js` | 查找股票代码 | `node scripts/search_stocks.js apple` |
| `get_trending_coins.js` | 获取24小时内的热门资产 | `node scripts/get_trending_coins.js` |
| `get_top_coins.js` | 获取市值排名前20的加密货币 | `node scripts/get_top_coins.js --per_page=20` |
| `search_coins.js` | 发现新的加密货币 | `node scripts/search_coins.js solana` |
| `get_coin_details.js` | 获取加密货币的详细信息 | `node scripts/get_coin_details.js ethereum` |
| `get_coin_ohlc_chart.js` | 获取加密货币的蜡烛图数据 | `node scripts/get_coin_ohlc_chart.js bitcoin` |
| `get_coin_historical_chart.js` | 获取加密货币的历史价格时间序列数据 | `node scripts/get_coin_historical_chart.js bitcoin` |
| `get_global_market_data.js` | 获取全球市场统计数据 | `node scripts/get_global_market_data.js` |
| `get_public_companies_holdings.js` | 获取上市公司的持仓情况 | `node scripts/get_public_companies_holdings.js bitcoin` |
| `get_supported_currencies.js` | 获取支持的货币类型 | `node scripts/get_supported_currencies.js` |

---

## 使用说明

### 1. `get_crypto_price.js`
获取一种或多种加密货币的实时价格和基本市场指标。

**语法：**
```bash
node scripts/get_crypto_price.js <coin_id_1> [coin_id_2] ... [--currency=usd]
```

**参数：**
- `coin_id`：加密货币的唯一标识符（例如：`bitcoin`、`solana`）。
- `--currency`：用于估值的目标货币（默认：`usd`）。

**示例：**
```bash
node scripts/get_crypto_price.js bitcoin ethereum cardano --currency=jpy
```

---

### 2. `get_top_coins.js`
获取按市值排名前20的加密货币列表。

**语法：**
```bash
node scripts/get_top_coins.js [--currency=usd] [--per_page=10] [--page=1] [--order=market_cap_desc]
```

**参数：**
- `--currency`：估值货币（默认：`usd`）。
- `--per_page`：每页显示的结果数量（1-250，默认：10）。
- `--order`：排序方式（例如：`market_cap_desc`、`volume_desc`）。

---

### 3. `get_coin_ohlc_chart.js`
获取用于技术分析的开盘价、最高价、最低价、收盘价（OHLC）数据。

**语法：**
```bash
node scripts/get_coin_ohlc_chart.js <coin_id> [--currency=usd] [--days=7]
```

**支持的`days`值：**`1, 7, 14, 30, 90, 180, 365`。

| 时间范围 | 数据间隔 |
| :--- | :--- |
| 1-2天 | 30分钟间隔 |
| 3-30天 | 4小时间隔 |
| 31天以上 | 4天间隔 |

---

### 4. `get_coin_historical_chart.js`
获取价格、市值和成交量的详细历史时间序列数据。

**语法：**
```bash
node scripts/get_coin_historical_chart.js <coin_id> [--currency=usd] [--days=30]
```

---

### 5. `get_stock_quote.js`
获取一种或多种股票代码的实时股价。

**语法：**
```bash
node scripts/get_stock_quote.js <SYMBOL_1> [SYMBOL_2] ...
```

---

### 6. `get_company_profile.js`
获取公司的全面概况，包括公司描述、所属行业和首席执行官信息。

**语法：**
```bash
node scripts/get_company_profile.js <SYMBOL>
```

## 重要提示

- **加密货币**：使用**唯一标识符**；**股票**：使用**股票代码**。
- 对于不确定正确标识符的加密货币，请使用`search_coins.js`进行查询。

### 认证
认证由内部的`api_client.js`自动处理。具体流程如下：
- **接口地址**：`GET https://api.igent.net/api/token`
- **认证机制**：
  1. **首次使用**：系统会向服务器请求一个临时会话令牌。
  2. **本地存储**：令牌会保存在隐藏的`.token`文件中，以便后续请求重复使用。
  3. **自动添加到请求头**：客户端会在每次请求中自动包含该令牌以证明用户身份。
  4. **自动刷新**：令牌过期后，系统会自动重新获取新的令牌，无需用户手动操作。

无需手动配置API密钥或进行其他设置。

### 速率限制
尽管系统性能稳定，但为确保所有用户都能正常使用服务，请避免短时间内发送大量请求（每分钟不超过30次）。

### 代理集成
该技能完全兼容OpenClaw及其他使用**AgentSkills**标准的代理。可以直接从`scripts/`目录执行相关脚本。