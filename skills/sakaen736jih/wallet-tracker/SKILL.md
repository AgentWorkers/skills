---
name: wallet-tracker
description: 实时追踪区块链地址——监控大型交易者的活动，接收交易警报，并分析以太坊（Ethereum）、Solana及其他区块链上的投资组合变化。
metadata: {"openclaw":{"requires":{"bins":["python3"]},"install":[{"id":"python","kind":"pip","package":"requests","bins":[],"label":"Install requests (pip)"}]}}
---

# 钱包追踪器

## 概述

监控区块链地址，以检测以下事件：
- 大额交易（“鲸鱼交易”警报）
- 财产组合变化
- 代币转账
- NFT 转移
- DeFi 交互

## 以太坊追踪

### 监控地址交易

```bash
# Using Etherscan API
curl -s "https://api.etherscan.io/api?module=account&action=txlist&address=ADDRESS&startblock=0&endblock=99999999&sort=desc&apikey=YourApiKey" | \
python3 -c "
import sys, json
data = json.load(sys.stdin)
for tx in data.get('result', [])[:10]:
    val = int(tx['value']) / 1e18
    print(f\"{tx['hash'][:16]}... | {val:.4f} ETH | {tx['to'][:16]}...\")"
```

### 监控 ERC-20 代币转账

```bash
curl -s "https://api.etherscan.io/api?module=account&action=tokentx&address=ADDRESS&sort=desc&apikey=YourApiKey" | \
python3 -c "
import sys, json
data = json.load(sys.stdin)
for tx in data.get('result', [])[:10]:
    val = int(tx['value']) / 10**int(tx['tokenDecimal'])
    print(f\"{tx['tokenSymbol']}: {val:.2f} | {tx['to'][:16]}...\")"
```

### 实时监控脚本

```python
#!/usr/bin/env python3
import requests
import time

ADDRESS = "0x..." # Address to track
API_KEY = "YourEtherscanApiKey"
INTERVAL = 60  # Check every 60 seconds

last_block = 0

while True:
    url = f"https://api.etherscan.io/api?module=account&action=txlist&address={ADDRESS}&startblock={last_block}&sort=asc&apikey={API_KEY}"
    resp = requests.get(url).json()

    for tx in resp.get('result', []):
        block = int(tx['blockNumber'])
        if block > last_block:
            val = int(tx['value']) / 1e18
            direction = "IN" if tx['to'].lower() == ADDRESS.lower() else "OUT"
            print(f"[{direction}] {val:.4f} ETH | TX: {tx['hash'][:20]}...")
            last_block = block

    time.sleep(INTERVAL)
```

## Solana 追踪

### 最近的交易

```bash
curl -s -X POST https://api.mainnet-beta.solana.com -H "Content-Type: application/json" -d '{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "getSignaturesForAddress",
  "params": ["ADDRESS", {"limit": 10}]
}' | python3 -c "
import sys, json
data = json.load(sys.stdin)
for sig in data.get('result', []):
    print(f\"{sig['signature'][:32]}... | Block: {sig.get('slot')}\")"
```

### 监控 SOL 币值变化

```bash
python3 -c "
import requests
import time

address = 'YOUR_ADDRESS'
last_balance = 0

while True:
    resp = requests.post('https://api.mainnet-beta.solana.com', json={
        'jsonrpc': '2.0',
        'id': 1,
        'method': 'getBalance',
        'params': [address]
    }).json()

    balance = resp['result']['value'] / 1e9
    if balance != last_balance:
        diff = balance - last_balance
        print(f'Balance: {balance:.4f} SOL | Change: {diff:+.4f}')
        last_balance = balance

    time.sleep(30)"
```

### 跟踪 SPL 代币转账

```bash
curl -s -X POST https://api.mainnet-beta.solana.com -H "Content-Type: application/json" -d '{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "getTokenAccountsByOwner",
  "params": [
    "ADDRESS",
    {"programId": "TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA"},
    {"encoding": "jsonParsed"}
  ]
}' | python3 -c "
import sys, json
data = json.load(sys.stdin)
for acc in data.get('result', {}).get('value', []):
    info = acc['account']['data']['parsed']['info']
    amount = float(info['tokenAmount']['uiAmount'] or 0)
    mint = info['mint'][:16]
    print(f'{mint}... | {amount:.4f}')"
```

## 多链资产组合追踪器

```python
#!/usr/bin/env python3
import requests

def get_eth_balance(address):
    url = f"https://api.etherscan.io/api?module=account&action=balance&address={address}&apikey=YourKey"
    resp = requests.get(url).json()
    return int(resp['result']) / 1e18

def get_sol_balance(address):
    resp = requests.post('https://api.mainnet-beta.solana.com', json={
        'jsonrpc': '2.0', 'id': 1,
        'method': 'getBalance',
        'params': [address]
    }).json()
    return resp['result']['value'] / 1e9

# Track multiple addresses
wallets = {
    'eth': ['0xAddress1', '0xAddress2'],
    'sol': ['SolAddress1', 'SolAddress2']
}

print("=== Portfolio ===")
for addr in wallets['eth']:
    bal = get_eth_balance(addr)
    print(f"ETH {addr[:10]}...: {bal:.4f} ETH")

for addr in wallets['sol']:
    bal = get_sol_balance(addr)
    print(f"SOL {addr[:10]}...: {bal:.4f} SOL")
```

## 使用 Alchemy 的 Webhook 警报

```bash
# Create webhook via Alchemy API
curl -X POST "https://dashboard.alchemy.com/api/create-webhook" \
  -H "Content-Type: application/json" \
  -d '{
    "network": "ETH_MAINNET",
    "webhook_type": "ADDRESS_ACTIVITY",
    "webhook_url": "https://your-server.com/webhook",
    "addresses": ["0xAddress1", "0xAddress2"]
  }'
```

## “鲸鱼交易”警报集成

用于检测大额交易：

```bash
# Top ETH holders recent activity
curl -s "https://api.etherscan.io/api?module=account&action=txlist&address=0x00000000219ab540356cBB839Cbe05303d7705Fa&sort=desc&apikey=YourKey" | \
python3 -c "
import sys, json
data = json.load(sys.stdin)
for tx in data.get('result', [])[:5]:
    val = int(tx['value']) / 1e18
    if val > 100:
        print(f'WHALE: {val:.2f} ETH | {tx[\"hash\"][:20]}...')"
```

## 跟踪服务（免费 tier）

| 服务 | 支持的链 | 功能 |
|---------|--------|----------|
| Etherscan | ETH、L2s | 交易历史记录、API 接口 |
| Solscan | Solana | 完整的交易历史记录 |
| DeBank | 多链支持 | 资产组合视图 |
| Zapper | EVM 链 | DeFi 交易追踪 |
| Nansen | 多链支持 | “鲸鱼交易”标记功能 |

## API 端点

| 链 | API 端点 |
|-------|----------|
| 以太坊 | https://api.etherscan.io/api |
| Polygon | https://api.polygonscan.com/api |
| BSC | https://api.bscscan.com/api |
| Arbitrum | https://api.arbiscan.io/api |
| Solana | https://api.mainnet-beta.solana.com |

## 注意事项

- 大多数 API 都有速率限制（免费 tier 每秒 5 次请求）
- 收费 API 提供 WebSocket 功能以实现实时监控
- 在生产环境中建议使用专用追踪服务
- 所有区块链数据都是公开的
- 请谨慎使用这些数据，仅用于研究目的