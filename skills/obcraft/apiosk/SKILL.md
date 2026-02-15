# Apiosk – 无需API密钥的API访问服务（支持USDC微支付）

**为使用USDC微支付的代理提供按请求计费的API访问服务。**

Apiosk允许代理通过x402协议在Base区块链上访问生产级API，无需管理API密钥，只需按实际使用量付费。

---

## 🎯 该工具的功能

- **发现API**：浏览15个以上的生产级API（包括天气、价格、新闻、地理编码等）
- **按请求计费**：自动使用USDC进行微支付（每次调用费用为0.001至0.10美元）
- **无需API密钥**：无需提供商账户或订阅
- **简单设置**：只需创建一次钱包，即可通过x402协议调用API

---

## 📦 安装

```bash
# Via ClawHub
clawhub install apiosk

# Or clone manually
git clone https://github.com/olivierbrinkman/apiosk-skill
```

---

## ⚙️ 配置

### 1. 设置钱包（一次性操作）

```bash
# Generate new wallet (or import existing)
./setup-wallet.sh

# This creates ~/.apiosk/wallet.json with:
# - Ethereum address (public)
# - Private key (stored locally, chmod 600)
# - Creation timestamp
#
# ⚠️ The private key is stored in plaintext with restrictive permissions.
# Only fund with small amounts for testing ($1-10).
# For production, use a hardware wallet or external KMS.
```

**重要提示：** 请在Base主网上为钱包充值USDC（建议最低充值1至10美元）。

**充值方法：**
1. 通过https://bridge.base.org将USDC桥接到Base区块链
2. 或者在Coinbase购买USDC后转存至Base区块链
3. 将USDC发送到您的Apiosk钱包地址

### 2. 发现可用API

```bash
# List all APIs
./list-apis.sh

# Output:
# weather       $0.001/req   Get current weather and forecasts
# prices        $0.002/req   Crypto/stock/forex prices  
# news          $0.005/req   Global news by topic/country
# company       $0.01/req    Company info, financials, news
# geocode       $0.001/req   Address → Coordinates
# ...
```

---

## 🚀 使用方法

### 基本API调用

```bash
# Call weather API
./call-api.sh weather --params '{"city": "Amsterdam"}'

# Output:
# {
#   "temperature": 12,
#   "condition": "Cloudy",
#   "forecast": [...]
# }
# 
# ✅ Paid: $0.001 USDC
```

### 从代理代码（Node.js）调用API

```javascript
const { callApiosk } = require('./apiosk-client');

// Call weather API
const weather = await callApiosk('weather', {
  city: 'Amsterdam'
});

console.log(`Temperature: ${weather.temperature}°C`);
// ✅ Automatically paid $0.001 USDC
```

### 从代理代码（Python）调用API

```python
from apiosk_client import call_apiosk

# Call prices API
prices = call_apiosk('prices', {
    'symbols': ['BTC', 'ETH']
})

print(f"BTC: ${prices['BTC']}")
# ✅ Automatically paid $0.002 USDC
```

---

## 📚 可用API列表

| API | 费用/请求 | 描述 | 示例 |
|-----|----------|-------------|---------|
| **weather** | 0.001美元 | 天气预报 | `{"city": "NYC"}` |
| **prices** | 0.002美元 | 加密货币/股票价格 | `{"symbols": ["BTC"]}` |
| **news** | 0.005美元 | 全球新闻文章 | `{"topic": "AI"}` |
| **company** | 0.01美元 | 公司信息 | `{"domain": "apple.com"}` |
| **geocode** | 0.001美元 | 地址转坐标 | `{"address": "Amsterdam"}` |
| **code-runner** | 0.05美元 | 执行代码沙盒 | `{"lang": "python", "code": "..."}` |
| **pdf-generator** | 0.02美元 | HTML转PDF | `{"html": "<h1>Hi</h1>"}` |
| **web-screenshot** | 0.03美元 | URL转截图 | `{"url": "example.com"}` |
| **file-converter** | 0.01美元 | 文件格式转换 | `{"from": "docx", "to": "pdf"}` |

**完整文档：** https://apiosk.com/#docs

---

## 🔧 辅助脚本

### `list-apis.sh`  
```bash
#!/bin/bash
# List all available APIs with pricing

curl -s https://gateway.apiosk.com/v1/apis | jq -r '.apis[] | "\(.id)\t$\(.price_usd)/req\t\(.description)"'
```

### `call-api.sh`  
```bash
#!/bin/bash
# Call any Apiosk API with automatic payment
# Usage: ./call-api.sh <api-id> --params '{"key":"value"}'

API_ID=$1
PARAMS=$3

# Load wallet
WALLET_ADDRESS=$(jq -r '.address' ~/.apiosk/wallet.json)

# Make request (x402 payment happens via on-chain verification)
# The gateway validates payment on-chain, no client-side signature needed
curl -X POST "https://gateway.apiosk.com/api/$API_ID" \
  -H "Content-Type: application/json" \
  -H "X-Wallet-Address: $WALLET_ADDRESS" \
  -d "$PARAMS"
```

### `check-balance.sh`  
```bash
#!/bin/bash
# Check USDC balance in your Apiosk wallet

WALLET_ADDRESS=$(jq -r '.address' ~/.apiosk/wallet.json)

curl -s "https://gateway.apiosk.com/v1/balance?address=$WALLET_ADDRESS" | jq
# Output: {"balance_usdc": 9.87, "spent_today": 0.13}
```

### `usage-stats.sh`  
```bash
#!/bin/bash
# View your API usage stats

WALLET_ADDRESS=$(jq -r '.address' ~/.apiosk/wallet.json)

curl -s "https://gateway.apiosk.com/v1/usage?address=$WALLET_ADDRESS" | jq
# Output:
# {
#   "total_requests": 142,
#   "total_spent_usdc": 1.89,
#   "by_api": {
#     "weather": {"requests": 87, "spent": 0.087},
#     "prices": {"requests": 55, "spent": 0.11}
#   }
# }
```

---

## 🎓 使用示例

### 示例1：天气信息机器人  
```javascript
const { callApiosk } = require('./apiosk-client');

async function getWeatherReport(city) {
  const weather = await callApiosk('weather', { city });
  
  return `🌤️ Weather in ${city}:
Temperature: ${weather.temperature}°C
Condition: ${weather.condition}
Forecast: ${weather.forecast.map(f => f.summary).join(', ')}
  
💰 Cost: $0.001 USDC`;
}

// Usage
console.log(await getWeatherReport('Amsterdam'));
```

### 示例2：加密货币价格追踪器  
```python
from apiosk_client import call_apiosk
import time

def track_prices(symbols, interval=60):
    """Track crypto prices with Apiosk"""
    while True:
        prices = call_apiosk('prices', {'symbols': symbols})
        
        for symbol, price in prices.items():
            print(f"{symbol}: ${price:,.2f}")
        
        print(f"✅ Paid: $0.002 USDC\n")
        time.sleep(interval)

# Track BTC and ETH every minute
track_prices(['BTC', 'ETH'])
```

### 示例3：新闻摘要代理  
```javascript
const { callApiosk } = require('./apiosk-client');

async function getDailyDigest(topics) {
  const articles = [];
  
  for (const topic of topics) {
    const news = await callApiosk('news', { 
      topic, 
      limit: 3 
    });
    articles.push(...news.articles);
  }
  
  return `📰 Daily Digest (${articles.length} articles)
${articles.map(a => `- ${a.title} (${a.source})`).join('\n')}

💰 Total cost: $${(topics.length * 0.005).toFixed(3)} USDC`;
}

// Get tech + business news
console.log(await getDailyDigest(['technology', 'business']));
```

---

## 🔐 x402的工作原理

**传统API：**  
```
1. Sign up for account
2. Get API key
3. Store securely
4. Include in requests
5. Monitor rate limits
6. Pay monthly subscription
```

**Apiosk（x402）：**  
```
1. Generate wallet (keypair stored locally)
2. Fund with USDC on Base
3. Make request — gateway returns 402
4. Client signs payment with your private key
5. Gateway verifies on-chain
6. You get response
```

**时间：** 毫秒级响应。**费用：** 按实际使用量计费。**设置：** 完全免费。

---

## 🛠️ 高级配置

### 自定义RPC端点  
```bash
# Edit ~/.apiosk/config.json
{
  "rpc_url": "https://mainnet.base.org",
  "chain_id": 8453,
  "usdc_contract": "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913"
}
```

### 设置消费限额  
```bash
# Set daily spending limit
./set-limit.sh --daily 10.00

# Set per-request max
./set-limit.sh --per-request 0.10
```

### 启用通知  
```bash
# Get notified when balance is low
./configure.sh --alert-balance 1.00 --alert-webhook "https://hooks.slack.com/..."
```

---

## 📊 监控与分析

### 查看消费记录  
```bash
# Today's spending
./usage-stats.sh --today

# This month
./usage-stats.sh --month

# Per API breakdown
./usage-stats.sh --by-api
```

### 导出使用数据  
```bash
# Export to CSV for accounting
./export-usage.sh --start 2026-01-01 --end 2026-01-31 --format csv > january_usage.csv
```

---

## 🆘 常见问题解答

### “USDC余额不足”  
```bash
# Check balance
./check-balance.sh

# If low, fund your wallet:
# 1. Bridge USDC to Base: https://bridge.base.org
# 2. Send to: [your wallet address]
```

### “支付验证失败”  
```bash
# Verify wallet signature is working
./test-signature.sh

# If fails, regenerate wallet:
./setup-wallet.sh --regenerate
```

### “API未找到”  
```bash
# Refresh API list
./list-apis.sh --refresh

# Check if API is available
curl https://gateway.apiosk.com/v1/apis | jq '.apis[] | select(.id=="weather")'
```

---

## 🌐 开发者指南：如何将自己的API接入Apiosk  

想通过Apiosk实现API盈利吗？  
```bash
# 1. Sign up
curl -X POST https://dashboard.apiosk.com/api/register \
  -d '{"email":"you@example.com","api_name":"My API"}'

# 2. Add your API endpoint
curl -X POST https://dashboard.apiosk.com/api/add \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "name": "my-api",
    "endpoint": "https://my-api.com",
    "price_usd": 0.01,
    "description": "My awesome API"
  }'

# 3. Start earning!
# Agents call your API via Apiosk gateway
# You get 90-95% of revenue, automatically
```

**更多信息：** https://docs.apiosk.com/developers

---

## 📖 资源链接

- **官方网站：** https://apiosk.com  
- **控制面板：** https://dashboard.apiosk.com  
- **文档：** https://docs.apiosk.com  
- **GitHub仓库：** https://github.com/olivierbrinkman/apiosk-skill  
- **支持邮箱：** support@apiosk.com  
- **社交媒体：** @ApioskAgent

---

## 💡 为什么选择Apiosk？

**对于代理来说：**  
- ✅ 无需管理API密钥  
- ✅ 仅按使用量付费  
- ✅ 即时访问9个以上的API  
- ✅ 透明定价  
- ✅ 提供链上支付凭证  

**对于开发者来说：**  
- ✅ 可将任何API变现  
- ✅ 无需处理支付流程  
- ✅ 收入分成高达90-95%  
- ✅ 即时结算  
- ✅ 全球覆盖  

**网络效应：** 越多API → 越多代理 → 越多收入 → 越多API  

---

## 🦞 关于Apiosk  

由Apiosk团队专为代理经济打造。  
**x402协议：** 无需API密钥的加密微支付方案。  
**使命：** 让所有API都能被所有代理即时使用。  

**“停止管理API密钥，开始按请求付费吧。”**

---

## 📝 许可证  

MIT许可证——您可以在自己的代理服务中自由使用Apiosk！  

---

## 🔗 快速链接  

```bash
# Install
clawhub install apiosk

# Setup
cd ~/.openclaw/skills/apiosk && ./setup-wallet.sh

# Use
./call-api.sh weather --params '{"city": "Amsterdam"}'

# Monitor
./usage-stats.sh
```

**祝您开发顺利！🚀**