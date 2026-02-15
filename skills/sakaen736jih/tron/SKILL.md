---
name: tron
description: 与 TRON 区块链交互：可以查询 TRX 账户余额、查看 TRC-20 代币信息、交易记录以及账户资源。支持使用 TronLink 地址进行操作。
metadata: {"openclaw":{"requires":{"bins":["python3"]},"install":[{"id":"python","kind":"pip","package":"tronpy","bins":[],"label":"Install tronpy (pip)"}]}}
---

# TRON 钱包 CLI

## 设置

安装 tronpy：
```bash
pip install tronpy
```

## 查看 TRX 余额

```bash
python3 -c "
from tronpy import Tron
client = Tron()
balance = client.get_account_balance('ADDRESS')
print(f'{balance} TRX')"
```

## 账户信息

```bash
python3 -c "
from tronpy import Tron
import json
client = Tron()
acc = client.get_account('ADDRESS')
print(json.dumps(acc, indent=2))"
```

## 账户资源（能量与带宽）

```bash
python3 -c "
from tronpy import Tron
client = Tron()
res = client.get_account_resource('ADDRESS')
print(f\"Bandwidth: {res.get('freeNetLimit', 0)}\")
print(f\"Energy: {res.get('EnergyLimit', 0)}\")"
```

## TRC-20 代币余额

```bash
python3 -c "
from tronpy import Tron
from tronpy.contract import Contract

client = Tron()
# USDT TRC-20 contract
contract = client.get_contract('TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t')
balance = contract.functions.balanceOf('ADDRESS')
decimals = contract.functions.decimals()
print(f'{balance / 10**decimals} USDT')"
```

## 代币信息

```bash
python3 -c "
from tronpy import Tron
client = Tron()
contract = client.get_contract('CONTRACT_ADDRESS')
print(f\"Name: {contract.functions.name()}\")
print(f\"Symbol: {contract.functions.symbol()}\")
print(f\"Decimals: {contract.functions.decimals()}\")
print(f\"Total Supply: {contract.functions.totalSupply()}\")"
```

## 交易历史（通过 API）

```bash
curl -s "https://api.trongrid.io/v1/accounts/ADDRESS/transactions?limit=10" | \
python3 -c "
import sys, json
data = json.load(sys.stdin)
for tx in data.get('data', []):
    print(f\"{tx['txID'][:16]}... | {tx.get('raw_data', {}).get('contract', [{}])[0].get('type', 'Unknown')}\")"
```

## TRC-20 转账

```bash
curl -s "https://api.trongrid.io/v1/accounts/ADDRESS/transactions/trc20?limit=10" | \
python3 -c "
import sys, json
data = json.load(sys.stdin)
for tx in data.get('data', []):
    val = int(tx.get('value', 0)) / 10**int(tx.get('token_info', {}).get('decimals', 6))
    sym = tx.get('token_info', {}).get('symbol', '?')
    print(f\"{tx['transaction_id'][:16]}... | {val:.2f} {sym}\")"
```

## 获取交易记录

```bash
python3 -c "
from tronpy import Tron
import json
client = Tron()
tx = client.get_transaction('TX_HASH')
print(json.dumps(tx, indent=2))"
```

## 当前区块

```bash
python3 -c "
from tronpy import Tron
client = Tron()
block = client.get_latest_block()
print(f\"Block: {block['block_header']['raw_data']['number']}\")"
```

## 检查合约

```bash
python3 -c "
from tronpy import Tron
client = Tron()
try:
    contract = client.get_contract('ADDRESS')
    print('This is a contract')
    print(f'Name: {contract.name}')
except:
    print('This is a regular account')"
```

## 使用 TronGrid API

账户信息：
```bash
curl -s "https://api.trongrid.io/v1/accounts/ADDRESS" | python3 -m json.tool
```

账户余额：
```bash
curl -s "https://api.trongrid.io/v1/accounts/ADDRESS" | \
python3 -c "import sys,json; d=json.load(sys.stdin); print(f\"{d['data'][0].get('balance',0)/1e6:.2f} TRX\")"
```

## 常见的 TRC-20 合约

| 代币 | 合约地址          |
|-------|-------------------|
| USDT | TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t |
| USDC | TEkxiTehnzSmSe2XqrBj4w32RUN966rdz8 |
| WTRX | TNUC9Qb1rRpS5CbWLmNMxXBjyFoydXjWFR |
| BTT | TAFjULxiVgT4qWk6UZwjqwZXTSaGaqnVp4 |
| JST | TCFLL5dx5ZJdKnWuesXxi1VPwjLVmWZZy9 |

## 地址格式

- TRON 使用 Base58Check 编码
- 地址以 ‘T’ 开头
- 长度为 34 个字符
- 例如：TJYeasTPa6gpBZWqTcP4u1Q7bhLMWBL7ox

## 注意事项

- 1 TRX = 1,000,000 SUN
- 每天免费带宽为 1500
- 智能合约调用需要消耗能量
- TronGrid API 有使用率限制
- 测试时请使用 Shasta 测试网