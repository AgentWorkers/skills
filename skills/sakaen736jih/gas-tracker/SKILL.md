---
name: gas-tracker
description: 实时监控以太坊的气体费用（gas prices）——获取当前的 gwei 价格，估算交易成本，找到最佳的交易时间，并跟踪气体费用的趋势。
metadata: {"openclaw":{"requires":{"bins":["cast"]},"install":[{"id":"foundry","kind":"shell","command":"curl -L https://foundry.paradigm.xyz | bash && foundryup","bins":["cast"],"label":"Install Foundry (cast)"}]}}
---

# 以太坊Gas费用追踪器

## 快速Gas费用查询

当前Gas费用：
```bash
cast gas-price --rpc-url https://eth.llamarpc.com | xargs -I {} cast --to-unit {} gwei
```

使用优先费用（EIP-1559）时：
```bash
cast base-fee --rpc-url https://eth.llamarpc.com | xargs -I {} cast --to-unit {} gwei
```

## 详细Gas费用信息

```bash
python3 << 'EOF'
import requests

resp = requests.post('https://eth.llamarpc.com', json={
    'jsonrpc': '2.0',
    'id': 1,
    'method': 'eth_gasPrice',
    'params': []
}).json()

gas_wei = int(resp['result'], 16)
gas_gwei = gas_wei / 1e9

print(f"Gas Price: {gas_gwei:.2f} Gwei")
print(f"Gas Price: {gas_wei} Wei")

# Estimate costs
gas_limits = {
    'ETH Transfer': 21000,
    'ERC-20 Transfer': 65000,
    'Uniswap Swap': 150000,
    'NFT Mint': 200000,
    'Contract Deploy': 500000
}

eth_price = 3000  # Update with current price

print(f"\n=== Estimated Costs (ETH @ ${eth_price}) ===")
for name, limit in gas_limits.items():
    cost_eth = (gas_wei * limit) / 1e18
    cost_usd = cost_eth * eth_price
    print(f"{name}: {cost_eth:.6f} ETH (${cost_usd:.2f})")
EOF
```

## EIP-1559 Gas费用估算

```bash
python3 << 'EOF'
import requests

# Get fee history
resp = requests.post('https://eth.llamarpc.com', json={
    'jsonrpc': '2.0',
    'id': 1,
    'method': 'eth_feeHistory',
    'params': ['0x5', 'latest', [25, 50, 75]]
}).json()

result = resp['result']
base_fees = [int(x, 16) / 1e9 for x in result['baseFeePerGas']]

print("=== Recent Base Fees (Gwei) ===")
for i, fee in enumerate(base_fees):
    print(f"Block -{len(base_fees)-i-1}: {fee:.2f}")

print(f"\nCurrent Base Fee: {base_fees[-1]:.2f} Gwei")
print(f"Average: {sum(base_fees)/len(base_fees):.2f} Gwei")

# Priority fee recommendations
print("\n=== Recommended Priority Fees ===")
print("🐢 Low (slow): 0.5-1 Gwei")
print("🚶 Medium: 1-2 Gwei")
print("🚀 Fast: 2-5 Gwei")
print("⚡ Urgent: 5-10+ Gwei")
EOF
```

## Gas费用相关API

### Etherscan Gas费用预测服务

```bash
curl -s "https://api.etherscan.io/api?module=gastracker&action=gasoracle&apikey=YourKey" | \
python3 -c "
import sys, json
data = json.load(sys.stdin)['result']
print('=== Etherscan Gas Oracle ===')
print(f\"🐢 Safe Low: {data['SafeGasPrice']} Gwei\")
print(f\"🚶 Average: {data['ProposeGasPrice']} Gwei\")
print(f\"🚀 Fast: {data['FastGasPrice']} Gwei\")
print(f\"📦 Base Fee: {data.get('suggestBaseFee', 'N/A')} Gwei\")"
```

### Blocknative Gas费用估算工具

```bash
curl -s "https://api.blocknative.com/gasprices/blockprices" \
  -H "Authorization: YOUR_API_KEY" | \
python3 -c "
import sys, json
data = json.load(sys.stdin)
prices = data['blockPrices'][0]['estimatedPrices']
print('=== Blocknative Estimates ===')
for p in prices:
    print(f\"{p['confidence']}% confidence: {p['price']} Gwei | Priority: {p['maxPriorityFeePerGas']} Gwei\")"
```

## 实时监控

```bash
python3 << 'EOF'
import requests
import time
from datetime import datetime

print("=== Gas Price Monitor (Ctrl+C to stop) ===\n")

history = []

while True:
    try:
        resp = requests.post('https://eth.llamarpc.com', json={
            'jsonrpc': '2.0',
            'id': 1,
            'method': 'eth_gasPrice',
            'params': []
        }).json()

        gas_gwei = int(resp['result'], 16) / 1e9
        history.append(gas_gwei)

        if len(history) > 60:
            history.pop(0)

        avg = sum(history) / len(history)
        trend = "📈" if gas_gwei > avg else "📉" if gas_gwei < avg else "➡️"

        now = datetime.now().strftime("%H:%M:%S")
        print(f"[{now}] {gas_gwei:.2f} Gwei {trend} (avg: {avg:.2f})")

        time.sleep(10)
    except KeyboardInterrupt:
        break
    except Exception as e:
        print(f"Error: {e}")
        time.sleep(10)
EOF
```

## Gas费用计算器

```bash
python3 << 'EOF'
import requests

# Get current gas price
resp = requests.post('https://eth.llamarpc.com', json={
    'jsonrpc': '2.0',
    'id': 1,
    'method': 'eth_gasPrice',
    'params': []
}).json()

gas_wei = int(resp['result'], 16)
gas_gwei = gas_wei / 1e9

# Get ETH price (using CoinGecko)
try:
    eth_resp = requests.get('https://api.coingecko.com/api/v3/simple/price?ids=ethereum&vs_currencies=usd').json()
    eth_price = eth_resp['ethereum']['usd']
except:
    eth_price = 3000

print(f"Current Gas: {gas_gwei:.2f} Gwei")
print(f"ETH Price: ${eth_price:,.2f}\n")

operations = [
    ("ETH Transfer", 21000),
    ("ERC-20 Approve", 46000),
    ("ERC-20 Transfer", 65000),
    ("Uniswap V2 Swap", 150000),
    ("Uniswap V3 Swap", 185000),
    ("OpenSea NFT Buy", 200000),
    ("NFT Mint (single)", 150000),
    ("NFT Mint (batch 5)", 400000),
    ("Bridge Deposit", 100000),
    ("Contract Deploy (small)", 300000),
    ("Contract Deploy (large)", 1000000),
]

print("=== Transaction Cost Estimates ===")
print(f"{'Operation':<25} {'Gas':>10} {'ETH':>12} {'USD':>10}")
print("-" * 60)

for name, gas_limit in operations:
    cost_eth = (gas_wei * gas_limit) / 1e18
    cost_usd = cost_eth * eth_price
    print(f"{name:<25} {gas_limit:>10,} {cost_eth:>12.6f} ${cost_usd:>9.2f}")
EOF
```

## 历史Gas费用分析

```bash
python3 << 'EOF'
import requests

# Get last 100 blocks fee history
resp = requests.post('https://eth.llamarpc.com', json={
    'jsonrpc': '2.0',
    'id': 1,
    'method': 'eth_feeHistory',
    'params': ['0x64', 'latest', [10, 50, 90]]
}).json()

result = resp['result']
base_fees = [int(x, 16) / 1e9 for x in result['baseFeePerGas']]

print("=== Last 100 Blocks Gas Analysis ===")
print(f"Minimum: {min(base_fees):.2f} Gwei")
print(f"Maximum: {max(base_fees):.2f} Gwei")
print(f"Average: {sum(base_fees)/len(base_fees):.2f} Gwei")
print(f"Current: {base_fees[-1]:.2f} Gwei")

# Find optimal times (lowest gas)
sorted_fees = sorted(enumerate(base_fees), key=lambda x: x[1])
print("\n=== Lowest Gas Periods ===")
for idx, fee in sorted_fees[:5]:
    blocks_ago = len(base_fees) - idx - 1
    print(f"{blocks_ago} blocks ago: {fee:.2f} Gwei")
EOF
```

## Gas费用提醒

```bash
python3 << 'EOF'
import requests
import time

TARGET_GWEI = 20  # Alert when gas drops below this
CHECK_INTERVAL = 30

print(f"Waiting for gas to drop below {TARGET_GWEI} Gwei...")

while True:
    try:
        resp = requests.post('https://eth.llamarpc.com', json={
            'jsonrpc': '2.0',
            'id': 1,
            'method': 'eth_gasPrice',
            'params': []
        }).json()

        gas_gwei = int(resp['result'], 16) / 1e9

        if gas_gwei < TARGET_GWEI:
            print(f"\n🔔 ALERT! Gas is now {gas_gwei:.2f} Gwei!")
            print("Good time to transact!")
            # Add notification here (telegram, discord, etc.)
            break
        else:
            print(f"Current: {gas_gwei:.2f} Gwei (waiting for < {TARGET_GWEI})")

        time.sleep(CHECK_INTERVAL)
    except KeyboardInterrupt:
        break
EOF
```

## 第二层网络（L2）Gas费用比较

```bash
python3 << 'EOF'
import requests

chains = {
    'Ethereum': 'https://eth.llamarpc.com',
    'Arbitrum': 'https://arb1.arbitrum.io/rpc',
    'Optimism': 'https://mainnet.optimism.io',
    'Polygon': 'https://polygon-rpc.com',
    'Base': 'https://mainnet.base.org',
}

print("=== Gas Prices Across Chains ===\n")

for name, rpc in chains.items():
    try:
        resp = requests.post(rpc, json={
            'jsonrpc': '2.0',
            'id': 1,
            'method': 'eth_gasPrice',
            'params': []
        }, timeout=5).json()

        gas_gwei = int(resp['result'], 16) / 1e9
        print(f"{name:<12}: {gas_gwei:>10.4f} Gwei")
    except Exception as e:
        print(f"{name:<12}: Error")
EOF
```

## 最佳交易时间

| 时间（UTC） | Gas费用水平 | 原因 |
|------------|-----------|--------|
| 00:00-06:00 | 低 | 美国处于睡眠时间，亚洲地区开始活跃 |
| 06:00-12:00 | 中等 | 欧洲地区活跃 |
| 12:00-18:00 | 高 | 美国和欧洲地区同时活跃 |
| 18:00-00:00 | 中等 | 美国交易高峰期，欧洲地区处于睡眠时间 |
| 周末 | 低 | 交易活动较少 |

## Gas费用相关代币

| 选项 | 说明 |
|--------|-------------|
| Flashbots | 提供MEV（Minimizes Emission Vulnerability）保护，通常Gas费用较低 |
| Gas费用代币（已弃用） | CHI、GST2在伦敦硬分叉后不再适用 |
| 批量交易 | 合并多个操作以降低费用 |
| 第二层网络解决方案（L2） | Arbitrum、Optimism等方案提供更低的费用 |

## 注意事项

- Gas费用会随网络需求波动 |
- 基础费用会被烧毁（即被销毁），优先费用归验证者所有 |
- EIP-1559规定：maxFeePerGas = 基础费用 + 优先费用 |
- 使用Flashbots可以有效保护MEV |
- 第二层网络（L2）的多数操作费用比主网便宜10-100倍 |
- 周末的交易费用通常较低 |