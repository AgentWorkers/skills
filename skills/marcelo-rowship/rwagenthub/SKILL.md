---
name: agenthub
description: 调用32个真实世界的API——包括航班、酒店、天气、加密货币价格、去中心化金融（DeFi）收益、股票行情、网络搜索、地理编码、IP信誉、区块链数据、代码执行以及电子邮件服务——每次调用均按USDC计费，通过x402接口进行支付。该功能需要Node.js 20.0及以上版本，以及一个装有USDC的Base钱包。
homepage: https://agents-production-73c1.up.railway.app
user-invocable: true
metadata: '{"openclaw": {"requires": {"env": ["MCP_WALLET_PRIVATE_KEY"], "bins": ["node", "npm"], "primaryCredential": "MCP_WALLET_PRIVATE_KEY"}}}'
---
# AgentHub — 提供32个AI API服务，按调用次数计费（使用USDC）

您可以使用**AgentHub**这个网关来调用各种实际数据API。支付过程通过x402协议自动处理，使用Base Mainnet上的USDC进行无gas（无需额外费用）支付。

**网关地址：** `https://agents-production-73c1.up.railway.app`

---

## 设置（仅需一次）

### 1. 安装SDK

```bash
npm install --prefix ~/.openclaw/workspace/skills/rwagenthub rwagenthub-sdk
```

该操作会将SDK安装到技能（skill）所在的文件夹中，无需全局安装，也不会涉及权限问题，适用于任何操作系统。

SDK包：[npmjs.com/package/rwagenthub-sdk](https://www.npmjs.com/package/rwagenthub-sdk)

### 2. 配置您的钱包私钥

> ⚠️ 请使用仅用于存储USDC的专用钱包，切勿使用您的主钱包。

```bash
openclaw config set env.MCP_WALLET_PRIVATE_KEY "0xYOUR_PRIVATE_KEY_HERE"
```

**安全提示：** 私钥永远不会离开您的设备。SDK会使用该私钥在本地生成EIP-3009格式的授权请求（无需支付gas费用），只有授权请求会被发送到支付网络；私钥仅用于在Base Mainnet上进行USDC微支付。

### 3. 向Base Mainnet钱包中充值USDC

- 最低推荐金额：1美元（足够进行100次以上每次0.01美元的调用）
- 可通过[Coinbase](https://coinbase.com)或其他交易所购买USDC并充值到Base Mainnet钱包。

---

## 在每次调用API之前，请确认SDK已安装

在进行任何API调用之前，请运行以下检查。如果SDK未安装，系统会自动进行安装：

```bash
[ -f "$HOME/.openclaw/workspace/skills/rwagenthub/node_modules/rwagenthub-sdk/index.js" ] || \
  npm install --prefix "$HOME/.openclaw/workspace/skills/rwagenthub" rwagenthub-sdk --silent
```

如果`MCP_WALLET_PRIVATE_KEY`未设置，请告知用户：
> “请运行：`openclaw config set env.MCP_WALLET_PRIVATE_KEY \"0xYOUR_PRIVATE_KEY\"`”

---

## 如何调用API

对于每个API调用，您需要创建一个临时脚本并通过Node.js来执行它：

```bash
cat > /tmp/agenthub-call.mjs << SCRIPT
import AgentHub from '$HOME/.openclaw/workspace/skills/rwagenthub/node_modules/rwagenthub-sdk/index.js';

const hub = new AgentHub({ privateKey: process.env.MCP_WALLET_PRIVATE_KEY });
const result = await hub.call('API_NAME', { ...inputs... });
console.log(JSON.stringify(result, null, 2));
SCRIPT

node /tmp/agenthub-call.mjs
```

请将`API_NAME`和`{ ...inputs... }`替换为下表中的API名称及相应的参数。

---

## 可用的API服务

### ✈️ 旅行相关

**`flight_search`** — 费用：0.01美元
```js
await hub.call('flight_search', { from: 'EZE', to: 'JFK', date: '2026-04-15', adults: 1, cabin_class: 'economy' })
```

**`flight_search_pro`** — 费用：0.01美元
```js
await hub.call('flight_search_pro', { from: 'MAD', to: 'NYC', date: '2026-06-01', adults: 1, cabin_class: 'ECONOMY' })
```

**`flight_status`** — 费用：0.01美元
```js
await hub.call('flight_status', { carrier_code: 'AA', flight_number: '100', date: '2026-06-01' })
```

**`seat_map`** — 费用：0.01美元
```js
await hub.call('seat_map', { offer_id: 'off_...' })
```

**`airport_search`** — 费用：0.01美元
```js
await hub.call('airport_search', { country_code: 'AR', limit: 10 })
```

**`hotel_search`** — 费用：0.06美元
```js
await hub.call('hotel_search', { city_code: 'NYC', check_in: '2026-04-01', check_out: '2026-04-03', adults: 2, ratings: '4,5' })
```

**`activities_search`** — 费用：0.01美元
```js
await hub.call('activities_search', { latitude: 40.7128, longitude: -74.006, radius: 5 })
```

---

### 🌐 网页搜索

**`web_search`** — 费用：0.02美元
```js
await hub.call('web_search', { query: 'best hotels in Paris 2026', type: 'search', num: 10 })
```

**`web_search_ai`** — 费用：0.02美元
```js
await hub.call('web_search_ai', { query: 'latest AI agent news', count: 5, freshness: 'Week' })
```

**`web_search_full`** — 费用：0.02美元
```js
await hub.call('web_search_full', { query: 'x402 protocol guide', limit: 3 })
```

**`places_search`** — 费用：0.02美元
```js
await hub.call('places_search', { query: 'coffee shops', location: 'Tokyo, Japan', num: 5 })
```

**`image_search`** — 费用：0.01美元
```js
await hub.call('image_search', { query: 'Patagonia landscape', num: 5 })
```

**`shopping_search`** — 费用：0.02美元
```js
await hub.call('shopping_search', { query: 'carry-on luggage 40L', num: 5 })
```

**`url_extract`** — 费用：0.02美元
```js
await hub.call('url_extract', { url: 'https://en.wikipedia.org/wiki/Patagonia', format: 'markdown' })
```

**`url_scrape`** — 费用：0.01美元
```js
await hub.call('url_scrape', { url: 'https://example.com', only_main_content: true })
```

**`url_scrape_json`** — 费用：0.02美元
```js
await hub.call('url_scrape_json', { url: 'https://news.ycombinator.com', prompt: 'extract top 3 story titles and point counts' })
```

---

### 🌤️ 天气与位置信息

**`weather_forecast`** — 费用：0.01美元
```js
await hub.call('weather_forecast', { location: 'Buenos Aires', days: 7, units: 'metric' })
```

**`geocode`** — 费用：0.01美元
```js
await hub.call('geocode', { query: 'Eiffel Tower, Paris', mode: 'forward' })
// reverse: { lat: 48.8584, lon: 2.2945, mode: 'reverse' }
```

---

### 💰 加密货币与去中心化金融（DeFi）

**`crypto_price`** — 费用：0.01美元
```js
await hub.call('crypto_price', { coins: 'btc,eth,sol', vs_currency: 'usd' })
```

**`exchange_rate` — 费用：0.01美元
```js
await hub.call('exchange_rate', { from: 'USD', to: 'EUR,GBP,JPY', amount: 100 })
```

**`defi_market_snapshot` — 费用：0.02美元
```js
await hub.call('defi_market_snapshot', { top: 10 })
```

**`defi_yields` — 费用：0.02美元
```js
await hub.call('defi_yields', { stablecoin_only: true, no_il_risk: true, min_apy: 5, top: 10 })
```

---

### 📈 股票与市场

**`stock_quote`** — 费用：0.01美元
```js
await hub.call('stock_quote', { symbol: 'AAPL' })
```

**`stock_profile` — 费用：0.01美元
```js
await hub.call('stock_profile', { symbol: 'NVDA' })
```

**`stock_search` — 费用：0.01美元
```js
await hub.call('stock_search', { query: 'Apple', limit: 5 })
```

**`market_news` — 费用：0.01美元
```js
await hub.call('market_news', { category: 'general', limit: 10 })
// category options: 'general', 'forex', 'crypto', 'merger'
// add symbol: 'AAPL' for company-specific news
```

**`earnings_calendar` — 费用：0.01美元
```js
await hub.call('earnings_calendar', { from: '2026-04-01', to: '2026-04-30' })
```

---

### ⛓️ 区块链与安全

**`alchemy_portfolio` — 费用：0.02美元
```js
await hub.call('alchemy_portfolio', { address: '0x...', networks: ['eth-mainnet', 'base-mainnet'] })
// networks: eth-mainnet, base-mainnet, arb-mainnet, opt-mainnet, polygon-mainnet, bnb-mainnet, avax-mainnet
```

**`alchemy_tx_history` — 费用：0.02美元
```js
await hub.call('alchemy_tx_history', { address: '0x...', networks: ['eth-mainnet'], page_size: 20, order: 'desc' })
```

**`opensky_flights` — 费用：0.01美元
```js
await hub.call('opensky_flights', { mode: 'live', limit: 20 })
// mode: 'live' | 'arrivals' | 'departures' — add airport: 'KJFK' for airport modes
```

**`ip_reputation` — 费用：0.01美元
```js
await hub.call('ip_reputation', { ip: '8.8.8.8', max_age_days: 90 })
```

---

### 🛠️ 实用工具

**`code_exec` — 费用：0.05美元
```js
await hub.call('code_exec', { code: 'print(sum(range(1, 101)))', language: 'python', timeout: 30 })
// language: 'python' | 'javascript' | 'r' | 'bash'
```

**`email_send` — 费用：0.01美元
```js
await hub.call('email_send', { to: 'user@example.com', subject: 'Hello', text: 'Message body.' })
```

---

## 完整示例

示例：询问“比特币的价格是多少？”

```bash
cat > /tmp/agenthub-call.mjs << SCRIPT
import AgentHub from '$HOME/.openclaw/workspace/skills/rwagenthub/node_modules/rwagenthub-sdk/index.js';
const hub = new AgentHub({ privateKey: process.env.MCP_WALLET_PRIVATE_KEY });
const result = await hub.call('crypto_price', { coins: 'btc', vs_currency: 'usd' });
console.log(JSON.stringify(result, null, 2));
SCRIPT

node /tmp/agenthub-call.mjs
```

---

## 错误处理

| 错误类型 | 原因 | 解决方案 |
|---|---|---|
| `payment failed` | Base Mainnet上的USDC余额不足 | 请充值钱包 |
| `AgentHub: API error — unknown_api` | API名称错误 | 请核对API名称是否正确 |
| `AgentHub: API error — invalid_inputs` | 参数缺失或错误 | 请检查相关API的参数 |
| `Cannot find module` / `ERR_MODULE_NOT_FOUND` | SDK未安装 | 请运行 `npm install --prefix ~/.openclaw/workspace/skills/rwagenthub rwagenthub-sdk` 进行安装 |