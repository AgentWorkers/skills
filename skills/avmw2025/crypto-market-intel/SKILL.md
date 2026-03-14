---
name: crypto-market-intel
description: **加密市场情报** – 适用于任何 OpenClaw 代理的免费市场数据管道。无需任何 API 密钥。可获取实时加密货币价格、市场指标、恐惧与贪婪指数（Fear & Greed index）、去中心化金融（DeFi）的总价值锁定（TVL）、股票指数以及宏观经济指标。当您需要加密货币价格、市场数据、市场分析、恐惧与贪婪情绪数据、去中心化金融的 TVL、股票价格、宏观经济信息或交易信号时，均可使用该服务。
---
# 加密市场情报

这是一个实时市场数据管道，可获取加密货币、股票和宏观经济指标的数据。无需任何API密钥，所有数据均来自免费的公共API。

## 使用场景

当您需要以下信息时，可以使用此功能：
- 当前加密货币的价格和市值
- 比特币/以太坊的市场主导地位
- 恐惧与贪婪指数
- 热门加密货币
- DeFi领域的总锁仓价值（TVL）
- 股票市场指数（如S&P 500、Nasdaq、Dow、VIX）
- 人工智能相关股票的股价（如NVDA、AMD、MSFT等）
- 宏观经济指标（如美元指数DXY、10年期国债收益率）
- 用于交易分析的预取数据
- 用于投资组合决策的市场情报

## 快速入门

**获取所有市场数据：**
```bash
cd ~/.openclaw/skills/crypto-market-intel/scripts
python3 market-data-fetcher.py all --output ~/market-data
```

**分析市场状况：**
```bash
./analyze-market.sh
```

## 核心功能

✅ **6个免费API，无需密钥**
- CoinGecko（加密货币信息、全球指标、热门加密货币）
- Alternative.me（恐惧与贪婪指数）
- DeFi Llama（DeFi领域的总锁仓价值）
- Yahoo Finance（股票、指数、债券）

✅ **加密货币相关功能**
- 市值排名前三的加密货币
- 全球市场指标（总市值、交易量、市场主导地位）
- 恐惧与贪婪指数（当前值及7天历史数据）
- 热门加密货币
- DeFi领域的总锁仓价值

✅ **股票与宏观经济指标**
- 主要股票市场指数（S&P 500、Nasdaq、Dow、VIX）
- 人工智能相关股票（NVDA、AMD、AVGO、MRVL、TSM、ASML、ARM、MSFT、AMZN、GOOG、META、ORCL）
- 人工智能相关能源股（VST、CEG、OKLO、SMR、TLN）
- 美元指数（DXY）
- 10年期国债收益率

✅ **适合代理程序使用的输出格式**
- 输出格式为JSON，便于解析
- 数据结构化，包含时间戳
- 可以作为定时任务运行，也可按需调用
- 提供的真实市场数据，无错误信息

## 使用方法

### 仅获取加密货币数据
```bash
python3 scripts/market-data-fetcher.py crypto --output ./data
```

输出：`data/crypto-latest.json`

### 仅获取股票/宏观经济数据
```bash
python3 scripts/market-data-fetcher.py stocks --output ./data
```

输出：`data/stocks-latest.json`

### 获取所有数据
```bash
python3 scripts/market-data-fetcher.py all --output ./data
```

### 自动化分析

运行分析脚本以获取数据并生成市场摘要：
```bash
./scripts/analyze-market.sh ~/market-data
```

该脚本会获取最新数据，并生成结构化的输出，供代理程序进行分析：
- 市场情绪（恐惧与贪婪指数）
- 行情波动最大的股票
- 宏观经济环境（美元指数DXY、收益率VIX）
- 重要市场信号

## 定时任务集成

您可以设置每小时自动获取一次市场数据：
```bash
crontab -e

# Fetch market data every hour
0 * * * * cd ~/.openclaw/skills/crypto-market-intel/scripts && python3 market-data-fetcher.py all --output ~/market-data
```

这样代理程序就可以在无需等待API响应的情况下，立即使用预取的数据进行分析。

## 数据结构

### 加密货币数据（`crypto-latest.json`）

```json
{
  "fetched_at": "2026-03-13T15:45:00Z",
  "source": "coingecko+alternative.me",
  "top_coins": [
    {
      "symbol": "BTC",
      "name": "Bitcoin",
      "price": 68500.0,
      "market_cap": 1340000000000,
      "volume_24h": 28000000000,
      "change_24h_pct": 2.5,
      "change_7d_pct": -1.2,
      "change_1h_pct": 0.3,
      "ath": 69000.0,
      "ath_change_pct": -0.7,
      "rank": 1
    }
  ],
  "global": {
    "total_market_cap_usd": 2400000000000,
    "total_volume_24h_usd": 85000000000,
    "btc_dominance": 55.8,
    "eth_dominance": 17.2,
    "active_cryptocurrencies": 13245,
    "market_cap_change_24h_pct": 1.8
  },
  "fear_greed": [
    {
      "value": 62,
      "label": "Greed",
      "date": "1710346800"
    }
  ],
  "trending": [
    {
      "name": "Solana",
      "symbol": "SOL",
      "rank": 5,
      "score": 0
    }
  ],
  "defi_tvl": {
    "total_tvl": 95800000000,
    "date": 1710288000,
    "change_1d": 2.1
  }
}
```

### 股票数据（`stocks-latest.json`）

```json
{
  "fetched_at": "2026-03-13T15:45:00Z",
  "stocks": {
    "indices": [
      {
        "symbol": "^GSPC",
        "price": 5200.5,
        "prev_close": 5180.0,
        "change_pct": 0.4
      }
    ],
    "ai_chips": [
      {
        "symbol": "NVDA",
        "price": 890.25,
        "prev_close": 885.0,
        "change_pct": 0.59
      }
    ]
  },
  "dxy": {
    "price": 103.45,
    "prev_close": 103.2
  },
  "treasury_10y": {
    "yield": 4.25,
    "prev_close": 4.22
  }
}
```

## 使用限制与公平使用

| API | 使用频率 | 备注 |
|-----|------------|-------|
| CoinGecko | 每分钟10-50次请求 | 免费使用，无需密钥 |
| Alternative.me | 无限制 | 公开API |
| DeFi Llama | 无限制 | 公开API |
| Yahoo Finance | 每小时约2000次请求 | 非官方API，请合理使用 |

**建议：** 每小时运行一次数据获取任务，避免频繁请求。虽然API是免费的，但请遵守公平使用原则。

## 常见问题及解决方法

**问题：** 数据获取失败（超时）  
**解决方法：** 检查网络连接，几分钟后重试。部分API可能会暂时中断服务。

**问题：** Yahoo Finance无法获取某只股票的数据  
**解决方法：** 可能该股票已退市或数据不可用。请核对股票代码的准确性（使用`^`前缀，例如`^GSPC`）。

**问题：** DeFi领域的总锁仓价值（TVL）为null  
**解决方法：** 可能是DeFi Llama API正在更新，历史数据有时会有延迟。稍后再试。

**问题：** 恐惧与贪婪指数返回空值  
**解决方法：** 可能是Alternative.me网站暂时无法访问。可以直接访问https://alternative.me/crypto/fear-and-greed-index/查看。

## 架构说明

- **无需认证**：所有API均为公开接口，无需管理密钥  
- **仅使用HTTP请求**：基于Python内置的`urllib`库（无需额外依赖）  
- **容错机制**：即使某个API失败，其他API仍能正常工作  
- **跨平台兼容**：支持任何安装了Python 3.7及以上的操作系统  
- **输出配置灵活**：使用`--output`参数指定数据输出目录

## 集成示例

- **Discord机器人提醒**  
```bash
#!/bin/bash
python3 scripts/market-data-fetcher.py crypto --output /tmp
FEAR=$(jq '.fear_greed[0].value' /tmp/crypto-latest.json)
if [ "$FEAR" -lt 25 ]; then
  echo "🚨 Extreme Fear detected: $FEAR — potential buy opportunity"
fi
```

- **交易机器人预分析**  
```python
import json

# Load pre-fetched data
with open("~/market-data/crypto-latest.json") as f:
    data = json.load(f)

# Extract top movers
top_coins = data["top_coins"]
gainers = sorted(top_coins, key=lambda x: x["change_24h_pct"], reverse=True)[:5]

print("Top 5 Gainers (24h):")
for coin in gainers:
    print(f"{coin['symbol']}: +{coin['change_24h_pct']:.2f}%")
```

## 参考资料

详细API文档、接口地址、响应格式及使用限制请参阅`references/api-sources.md`。

---

**最后更新时间：** 2026-03-13