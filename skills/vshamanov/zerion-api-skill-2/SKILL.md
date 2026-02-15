---
name: zerion-api
description: >
  Query blockchain wallet data, token prices, and transaction history using the Zerion API
  via its MCP connector. Use this skill whenever the user asks about: crypto wallet balances,
  portfolio values, token holdings or positions, DeFi positions (staking, lending, LP),
  wallet PnL (profit and loss), transaction history, token/fungible asset prices or charts,
  NFT holdings or NFT portfolio value, or any web3 wallet analytics. Triggers on mentions of
  wallet addresses (0x...), ENS names, token names/symbols, "portfolio", "positions", "PnL",
  "transactions", "balance", "holdings", "NFTs", or any crypto/DeFi analytics queries.
  Also use when building artifacts or dashboards that display wallet or token data.
---

# Zerion API 技能

通过 Zerion MCP 连接器查询 web3 钱包数据、代币价格、NFT 信息以及交易历史。

## 认证

使用 Zerion API 需要一个密钥。该密钥 **不会** 存储在 MCP 连接器的设置中——用户必须在每次聊天会话中提供它。

### 工作流程

1. **在任何与 Zerion 相关的任务开始时**，如果尚未提供 API 密钥，请询问：
   *"要查询 Zerion，我需要您的 API 密钥。您可以在 https://dashboard.zerion.io/ 找到它。请将其粘贴到这里。"
2. **将密钥存储在内存中**，在整个对话期间使用。切勿将其写入文件、显示在输出结果中或记录在日志中。
3. **按照以下方式将密钥传递给 MCP 服务器或 REST 请求。**

### 认证格式

Zerion 使用 HTTP Basic Auth：API 密钥作为用户名，密码为空。

```
Authorization: Basic <base64(API_KEY + ":")>
```

示例：密钥 `zk_dev_abc123` → `zk_dev_abc123:` 的 Base64 编码 → `emtfZGV2X2FiYzEyMzo=`

## MCP 连接

Zerion API 的 MCP 服务器地址为 `https://developers.zerion.io/mcp`。

当直接使用 MCP 工具（不在输出结果中显示）时，按照工具参数的要求传递 API 密钥。

在构建调用 Anthropic API 的输出结果时，需要将密钥包含在内部提示中，以便内部 Claude 能够进行认证：

```javascript
mcp_servers: [
  { type: "url", url: "https://developers.zerion.io/mcp", name: "zerion-mcp" }
]
```

**重要提示**：在输出结果中，将 API 密钥作为属性或状态变量接收——切勿将其硬编码。示例模式：

```jsx
// User inputs key via a secure input field (type="password")
const [apiKey, setApiKey] = useState("");

// Pass key to inner Claude prompt so MCP calls authenticate
const prompt = `Using the Zerion API key: ${apiKey}, get portfolio for wallet 0x...`;
```

## 常见工作流程

### 1. 钱包资产概览

提示内部 Claude 调用 Zerion API 获取钱包的资产概况：

```
Get the portfolio for wallet {address} in USD. Include total value, daily changes,
and distribution by chain and position type.
```

**端点：** `GET /v1/wallets/{address}/portfolio`
- `currency`：usd（默认）、eth、btc、eur 等
- `filter[positions]`：`only_simple`（默认）、`only_complex`（DeFi）、`no_filter`（全部）

### 2. 钱包代币持仓

```
List all fungible positions for wallet {address}, sorted by value descending.
```

**端点：** `GET /v1/wallets/{address}/positions/`
- `filter[positions]`：`only_simple` | `only_complex` | `no_filter`
- `filter[chain_ids]`：用逗号分隔的链 ID（例如：`ethereum,polygon`
- `filter[position_types]`：`wallet`、`deposit`、`staked`、`loan`、`locked`、`reward`、`investment`
- `sort`：`-value`（降序）或 `value`（升序）
- `filter[trash]`：`only_non_trash`（默认）

### 3. 交易历史

```
Get recent transactions for wallet {address}, filter for trades only.
```

**端点：** `GET /v1/wallets/{address}/transactions/`
- `filter[operation_types]`：`trade`、`send`、`receive`、`deposit`、`withdraw`、`mint`、`burn`、`claim` 等
- `filter[chain_ids]`：按链过滤
- `filter[min_mined_at]` / `filter[max_mined_at]`：时间戳（以毫秒为单位）
- `page[size]`：最多显示 100 条记录

### 4. 盈亏（PnL）

```
Get PnL for wallet {address}. Show realized gain, unrealized gain, fees, and net invested.
```

**端点：** `GET /v1/wallets/{address}/pnl`
- 返回值：`realized_gain`（已实现收益）、`unrealized_gain`（未实现收益）、`total_fee`（总费用）、`net_invested`（总投资）、`received_external`（外部收入）、`sent_external`（外部支出）
- 使用 FIFO 方法
- `filter[chain_ids]`、`filter[fungible_ids]`：用于缩小搜索范围

### 5. 钱包余额图表

```
Get the balance chart for wallet {address} over the past month.
```

**端点：** `GET /v1/wallets/{address}/charts/{chart_period}`
- `chart_period`：`hour`（小时）、`day`（天）、`week`（周）、`month`（月）、`3months`（3 个月）、`6months`（6 个月）、`year`（年）、`5years`（5 年）、`max`（全部）
- 返回类型为 `[timestamp, balance]` 的数组

### 6. 代币价格与搜索

```
Search for the fungible asset "ethereum" and return its price and market data.
```

**端点：** `GET /v1/fungibles/`
- `filter[search_query]`：文本搜索（例如：“ethereum”、“USDC”）
- `sort`：`-market_data.market_cap`、`-market_data.price.last` 等
- 返回值：`name`（名称）、`symbol`（代币符号）、`price`（价格）、`market_cap`（市值）、`circulating_supply`（流通供应量）、`changes`（过去 1 天/30 天/90 天/365 天的变动量）

### 7. 代币价格图表

```
Get the price chart for fungible {fungible_id} over the past week.
```

**端点：** `GET /v1/fungibles/{fungible_id}/charts/{chart_period}`
- 图表周期与钱包图表相同
- 返回类型为 `[timestamp, price]` 的数组

### 8. NFT 持仓

```
List all NFT positions for wallet {address}, sorted by floor price descending.
```

**端点：** `GET /v1/wallets/{address}/nft-positions/`
- `sort`：`-floor_price`、`created_at`（创建时间）
- `filter[chain_ids]`：按链过滤
- `include`：`nfts`、`nft_collections`、`wallet_nft_collections`（获取更详细的数据）

### 9. NFT 资产组合价值

**端点：** `GET /v1/wallets/{address}/nft-portfolio`
- 返回 NFT 资产组合的总价值

## 使用 Zerion 数据构建输出结果

在构建显示 Zerion 数据的 React/HTML 输出结果时：

1. **通过类型为 “password” 的输入字段安全地收集 API 密钥**
2. **切勿在用户界面中显示或记录** 密钥
3. **通过 MCP 提示将密钥传递给内部 Claude 进行认证**

```javascript
// apiKey comes from a password input, never hardcoded
const response = await fetch("https://api.anthropic.com/v1/messages", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({
    model: "claude-sonnet-4-20250514",
    max_tokens: 1000,
    messages: [
      {
        role: "user",
        content: `Use the Zerion API with key "${apiKey}" to get the portfolio
                  overview for wallet ${walletAddress} in USD.
                  Return ONLY a JSON object with: totalValue, dailyChangePercent,
                  dailyChangeAbsolute, topChains (array of {chain, value}),
                  positionBreakdown (wallet, deposited, staked, borrowed, locked).`
      }
    ],
    mcp_servers: [
      { type: "url", url: "https://developers.zerion.io/mcp", name: "zerion-mcp" }
    ]
  })
});
```

### 处理 MCP 响应

MCP 响应包含多个数据块。根据数据类型提取所需信息：

```javascript
const data = await response.json();

// Get tool results (actual Zerion data)
const toolResults = data.content
  .filter(item => item.type === "mcp_tool_result")
  .map(item => item.content?.[0]?.text || "")
  .join("\n");

// Get Claude's text analysis
const textResponses = data.content
  .filter(item => item.type === "text")
  .map(item => item.text)
  .join("\n");
```

## 关键注意事项

- **地址格式**：支持 EVM 地址（0x...）和 Solana 地址。ENS 名称可能需要先进行解析。
- **Solana 的限制**：Solana 地址无法查询协议持仓或 NFT 交易。
- **货币选项**：`usd`、`eth`、`btc`、`eur`、`krw`、`rub`、`gbp`、`aud`、`cad`、`inr`、`jpy`、`nzd`、`try`、`zar`、`cny`、`chf`
- **分页**：使用响应中的 `links.next` 进行分页；切勿手动构造 `page[after]`。
- **速率限制**：API 在达到速率限制时会返回 429 错误。在输出结果中实现带有退避机制的重试逻辑。
- **将 ID 视为不可预测的字符串**：不要假设 ID 的固定格式，因为它们可能会发生变化。
- **DeFi 持仓**：使用 `filter[positions]=no_filter` 以同时显示协议持仓和钱包持仓。
- **LP 分组**：流动性池持仓共享 `group_id` 属性——根据该属性对池进行正确分组显示。

## 详细端点参考

有关完整的参数详情、响应格式和边缘情况，请参阅：
- **钱包端点**：[references/wallet-endpoints.md](references/wallet-endpoints.md)
- **Fungible 和 NFT 端点**：[references/fungible-nft-endpoints.md](references/fungible-nft-endpoints.md)