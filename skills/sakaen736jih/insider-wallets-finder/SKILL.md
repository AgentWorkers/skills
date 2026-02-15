---
name: insider-wallets-finder
description: **功能概述：**  
- **寻找并分析“聪明资金”的交易地址**：识别早期买入者（即那些具备专业投资能力的投资者）。  
- **追踪成功交易者的行为**：监测那些在市场中表现优异的交易者的交易记录。  
- **分析“大户”（鲸鱼投资者）的资产积累模式**：研究这些大型投资者如何进行资产配置。  
- **研究链上的投资机会**：探索区块链平台上存在的潜在投资机会（即“链上阿尔法效应”）。  

**技术实现细节：**  
- **数据来源与整合**：从多个可靠的数据源收集相关信息，并对这些数据进行整合和处理。  
- **智能分析算法**：运用先进的机器学习算法对收集到的数据进行深度分析，以发现潜在的投资趋势和模式。  
- **可视化工具**：提供直观的可视化界面，帮助用户更轻松地理解和解读分析结果。  

**应用场景：**  
- **投资策略制定**：帮助投资者制定更明智的投资策略。  
- **市场研究**：为研究人员提供有价值的市场洞察。  
- **风险管理**：帮助金融机构识别潜在的风险点。  

**优势：**  
- **实时更新**：数据实时更新，确保分析结果的准确性。  
- **高度定制化**：用户可以根据自己的需求定制分析参数和范围。  
- **安全性**：所有数据传输和存储均经过加密处理，确保用户隐私安全。
metadata: {"openclaw":{"requires":{"bins":["python3"]},"install":[{"id":"python","kind":"pip","package":"requests","bins":[],"label":"Install requests (pip)"}]}}
---

# 内部钱包查找器（Insider Wallets Finder）

## 概述

通过分析以下信息来识别盈利地址：
- 早期代币购买者
- 表现稳定的盈利交易者
- 大额资金持有者的积累模式
- DEX（去中心化交易所）的交易模式
- NFT（非同质化代币）的交易者

## 查找代币的早期购买者

### 以太坊（ERC-20）

```bash
# Get first 100 transfers of a token
TOKEN="0xTokenContractAddress"
curl -s "https://api.etherscan.io/api?module=account&action=tokentx&contractaddress=${TOKEN}&page=1&offset=100&sort=asc&apikey=YourKey" | \
python3 -c "
import sys, json
from collections import Counter
data = json.load(sys.stdin)
buyers = Counter()
for tx in data.get('result', []):
    buyers[tx['to']] += 1
print('=== Early Buyers ===')
for addr, count in buyers.most_common(20):
    print(f'{addr} | {count} buys')"
```

### Solana（SPL代币）

```bash
# Find early holders using Birdeye API
curl -s "https://public-api.birdeye.so/public/token_holder?address=TOKEN_MINT&offset=0&limit=20" \
  -H "X-API-KEY: your-birdeye-key" | python3 -m json.tool
```

## 分析部署者活动

```bash
# Find what else deployer created
DEPLOYER="0xDeployerAddress"
curl -s "https://api.etherscan.io/api?module=account&action=txlist&address=${DEPLOYER}&sort=desc&apikey=YourKey" | \
python3 -c "
import sys, json
data = json.load(sys.stdin)
contracts = []
for tx in data.get('result', []):
    if tx['to'] == '' and tx['contractAddress']:
        contracts.append(tx['contractAddress'])
print('Deployed contracts:')
for c in contracts[:10]:
    print(c)"
```

## 跟踪大额资金持有者的积累情况

```bash
python3 << 'EOF'
import requests

TOKEN = "0xTokenAddress"
API_KEY = "YourEtherscanKey"

# Get top holders
url = f"https://api.etherscan.io/api?module=token&action=tokenholderlist&contractaddress={TOKEN}&page=1&offset=50&apikey={API_KEY}"
resp = requests.get(url).json()

print("=== Top Holders ===")
for holder in resp.get('result', [])[:20]:
    addr = holder['TokenHolderAddress']
    qty = float(holder['TokenHolderQuantity']) / 1e18
    print(f"{addr[:20]}... | {qty:,.2f}")
EOF
```

## 找到盈利的DEX交易者

### 分析Uniswap交易

```bash
python3 << 'EOF'
import requests

# GraphQL query for top traders
query = """
{
  swaps(first: 100, orderBy: amountUSD, orderDirection: desc, where: {amountUSD_gt: "10000"}) {
    sender
    amountUSD
    token0 { symbol }
    token1 { symbol }
  }
}
"""

resp = requests.post(
    "https://api.thegraph.com/subgraphs/name/uniswap/uniswap-v3",
    json={"query": query}
).json()

from collections import Counter
traders = Counter()
for swap in resp.get('data', {}).get('swaps', []):
    traders[swap['sender']] += float(swap['amountUSD'])

print("=== High Volume Traders ===")
for addr, vol in traders.most_common(10):
    print(f"{addr[:20]}... | ${vol:,.0f}")
EOF
```

## Solana DEX分析

### 找到Raydium/Jupiter的交易者

```bash
# Using Birdeye API
curl -s "https://public-api.birdeye.so/public/txs/token?address=TOKEN_MINT&tx_type=swap&limit=50" \
  -H "X-API-KEY: your-key" | \
python3 -c "
import sys, json
from collections import Counter
data = json.load(sys.stdin)
traders = Counter()
for tx in data.get('data', {}).get('items', []):
    traders[tx.get('owner', '')] += 1
print('Active Traders:')
for addr, count in traders.most_common(10):
    print(f'{addr[:20]}... | {count} trades')"
```

## NFT交易者分析

```bash
python3 << 'EOF'
import requests

# OpenSea API - find profitable flippers
collection = "boredapeyachtclub"
url = f"https://api.opensea.io/api/v1/events?collection_slug={collection}&event_type=successful&limit=50"

resp = requests.get(url, headers={"Accept": "application/json"}).json()

from collections import defaultdict
profits = defaultdict(float)

for event in resp.get('asset_events', []):
    seller = event.get('seller', {}).get('address', '')
    price = float(event.get('total_price', 0)) / 1e18
    profits[seller] += price

print("=== Top Sellers ===")
for addr, total in sorted(profits.items(), key=lambda x: -x[1])[:10]:
    print(f"{addr[:20]}... | {total:.2f} ETH")
EOF
```

## 跨多个代币进行对比分析

```bash
python3 << 'EOF'
import requests
from collections import Counter

API_KEY = "YourKey"
tokens = [
    "0xToken1",
    "0xToken2",
    "0xToken3"
]

all_early_buyers = Counter()

for token in tokens:
    url = f"https://api.etherscan.io/api?module=account&action=tokentx&contractaddress={token}&page=1&offset=50&sort=asc&apikey={API_KEY}"
    resp = requests.get(url).json()

    for tx in resp.get('result', []):
        all_early_buyers[tx['to']] += 1

print("=== Addresses in Multiple Early Buys ===")
for addr, count in all_early_buyers.most_common(20):
    if count >= 2:
        print(f"{addr} | {count} tokens")
EOF
```

## 标记地址数据库

### 检查已知地址

```bash
# Etherscan labels
curl -s "https://api.etherscan.io/api?module=account&action=balance&address=ADDRESS&tag=latest&apikey=YourKey"
```

### Arkham Intelligence（API）

```bash
curl -s "https://api.arkhamintelligence.com/intelligence/address/ADDRESS" \
  -H "API-Key: your-arkham-key" | python3 -m json.tool
```

## 模式检测

### 找到行为相似的地址

```bash
python3 << 'EOF'
import requests
from datetime import datetime

TOKEN = "0xTokenAddress"
API_KEY = "YourKey"

# Get all transfers
url = f"https://api.etherscan.io/api?module=account&action=tokentx&contractaddress={TOKEN}&sort=asc&apikey={API_KEY}"
resp = requests.get(url).json()

# Group by timing
from collections import defaultdict
timing = defaultdict(list)

for tx in resp.get('result', []):
    block = int(tx['blockNumber'])
    timing[block // 100].append(tx['to'])  # Group by ~100 blocks

# Find coordinated buying
print("=== Potential Coordinated Buys ===")
for block_group, buyers in timing.items():
    if len(buyers) >= 3:
        unique = set(buyers)
        if len(unique) >= 3:
            print(f"Block ~{block_group * 100}: {len(unique)} unique buyers")
            for b in list(unique)[:5]:
                print(f"  {b}")
EOF
```

## 研究工具

| 工具 | 用途 | 链接 |
|------|---------|------|
| Nansen | 标记地址 | nansen.ai |
| Arkham | 智能分析平台 | arkhamintelligence.com |
| Bubblemaps | 持有者可视化工具 | bubblemaps.io |
| DeBank | 投资组合跟踪工具 | debank.com |
| Dune | 自定义查询工具 | dune.com |
| Birdeye | Solana数据分析工具 | birdeye.so |

## Dune数据分析查询

在Dune平台上查找“聪明资金”的交易行为：
```sql
-- Top profitable traders
SELECT
  trader,
  SUM(profit_usd) as total_profit,
  COUNT(*) as trade_count
FROM dex.trades
WHERE block_time > now() - interval '7 days'
GROUP BY trader
HAVING SUM(profit_usd) > 10000
ORDER BY total_profit DESC
LIMIT 50
```

## 注意事项：

- 所有区块链数据都是公开的
- 仅用于研究和学习目的
- 需要跨多个来源进行数据对比分析
- 模式分析不能保证未来的投资回报
- 计算利润时需考虑交易费用
- 部分“内部人士”可能是套利机器人
- 必须手动验证分析结果