---
name: okx-dex
description: OKX DEX聚合器（v6）：提供交易报价、交易/审批数据、代币信息以及相关区块链的信息。
homepage: https://web3.okx.com/build/dev-docs/wallet-api/dex-api-reference
metadata: {"clawdbot":{"emoji":"🧭","always":true,"requires":{"bins":["curl","jq","python3"]}}}
---

# OKX DEX 聚合器 🧭

OKX 钱包 DEX API 提供了跨多个链（EVM 和非 EVM）的聚合交易报价和交易数据。

## 环境变量

| 变量 | 描述 | 是否必需 |
|----------|-------------|----------|
| `OKX_API_KEY` | OKX API 密钥 | 是 |
| `OKX_SECRET_KEY` | OKX API 密码 | 是 |
| `OKX_PASSPHRASE` | OKX API 密码短语 | 是 |

## API 基本 URL

```
https://web3.okx.com
```

## 认证（必需的请求头）

所有请求都必须包含以下请求头：

- `OK-ACCESS-KEY`
- `OK-ACCESS-TIMESTAMP`（UTC ISO 时间）
- `OK-ACCESS-PASSPHRASE`
- `OK-ACCESS-SIGN`（Base64(HMAC_SHA256(prehash, secret)))`

预哈希字符串：

```
TIMESTAMP + METHOD + REQUEST_PATH_WITH_QUERY + BODY
```

- 对于 GET 请求，`BODY` 为空，`REQUEST_PATH_WITH_QUERY` 必须包含查询字符串。
- 对于 POST 请求，`BODY` 是原始的 JSON 字符串。

## 获取支持的链（聚合器）

```bash
API_KEY="${OKX_API_KEY}"
SECRET_KEY="${OKX_SECRET_KEY}"
PASSPHRASE="${OKX_PASSPHRASE}"

TIMESTAMP=$(python3 - <<'PY'
from datetime import datetime, timezone
print(datetime.now(timezone.utc).isoformat(timespec='milliseconds').replace('+00:00','Z'))
PY
)

METHOD="GET"
REQUEST_PATH="/api/v6/dex/aggregator/supported/chain"
QUERY="chainIndex=1"
PATH_WITH_QUERY="${REQUEST_PATH}?${QUERY}"

SIGN=$(python3 - <<PY
import hmac, hashlib, base64
import os
msg = f"${TIMESTAMP}${METHOD}${PATH_WITH_QUERY}"
secret = os.environ["SECRET_KEY"].encode()
print(base64.b64encode(hmac.new(secret, msg.encode(), hashlib.sha256).digest()).decode())
PY
)

curl -s "https://web3.okx.com${PATH_WITH_QUERY}" \
  -H "OK-ACCESS-KEY: ${API_KEY}" \
  -H "OK-ACCESS-TIMESTAMP: ${TIMESTAMP}" \
  -H "OK-ACCESS-PASSPHRASE: ${PASSPHRASE}" \
  -H "OK-ACCESS-SIGN: ${SIGN}" | jq '.'
```

## 获取代币信息

```bash
API_KEY="${OKX_API_KEY}"
SECRET_KEY="${OKX_SECRET_KEY}"
PASSPHRASE="${OKX_PASSPHRASE}"
CHAIN_INDEX="1"  # Ethereum

TIMESTAMP=$(python3 - <<'PY'
from datetime import datetime, timezone
print(datetime.now(timezone.utc).isoformat(timespec='milliseconds').replace('+00:00','Z'))
PY
)

METHOD="GET"
REQUEST_PATH="/api/v6/dex/aggregator/all-tokens"
QUERY="chainIndex=${CHAIN_INDEX}"
PATH_WITH_QUERY="${REQUEST_PATH}?${QUERY}"

SIGN=$(python3 - <<PY
import hmac, hashlib, base64
import os
msg = f"${TIMESTAMP}${METHOD}${PATH_WITH_QUERY}"
secret = os.environ["SECRET_KEY"].encode()
print(base64.b64encode(hmac.new(secret, msg.encode(), hashlib.sha256).digest()).decode())
PY
)

curl -s "https://web3.okx.com${PATH_WITH_QUERY}" \
  -H "OK-ACCESS-KEY: ${API_KEY}" \
  -H "OK-ACCESS-TIMESTAMP: ${TIMESTAMP}" \
  -H "OK-ACCESS-PASSPHRASE: ${PASSPHRASE}" \
  -H "OK-ACCESS-SIGN: ${SIGN}" | jq '.data[:5]'
```

## 获取交易报价（仅报价）

```bash
API_KEY="${OKX_API_KEY}"
SECRET_KEY="${OKX_SECRET_KEY}"
PASSPHRASE="${OKX_PASSPHRASE}"

CHAIN_INDEX="1"  # Ethereum
FROM_TOKEN="0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE"  # ETH (native)
TO_TOKEN="0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48"    # USDC
AMOUNT="1000000000000000000"  # 1 ETH in wei

TIMESTAMP=$(python3 - <<'PY'
from datetime import datetime, timezone
print(datetime.now(timezone.utc).isoformat(timespec='milliseconds').replace('+00:00','Z'))
PY
)

METHOD="GET"
REQUEST_PATH="/api/v6/dex/aggregator/quote"
QUERY="chainIndex=${CHAIN_INDEX}&fromTokenAddress=${FROM_TOKEN}&toTokenAddress=${TO_TOKEN}&amount=${AMOUNT}&swapMode=exactIn"
PATH_WITH_QUERY="${REQUEST_PATH}?${QUERY}"

SIGN=$(python3 - <<PY
import hmac, hashlib, base64
import os
msg = f"${TIMESTAMP}${METHOD}${PATH_WITH_QUERY}"
secret = os.environ["SECRET_KEY"].encode()
print(base64.b64encode(hmac.new(secret, msg.encode(), hashlib.sha256).digest()).decode())
PY
)

curl -s "https://web3.okx.com${PATH_WITH_QUERY}" \
  -H "OK-ACCESS-KEY: ${API_KEY}" \
  -H "OK-ACCESS-TIMESTAMP: ${TIMESTAMP}" \
  -H "OK-ACCESS-PASSPHRASE: ${PASSPHRASE}" \
  -H "OK-ACCESS-SIGN: ${SIGN}" | jq '{
    fromTokenAmount: .data[0].fromTokenAmount,
    toTokenAmount: .data[0].toTokenAmount,
    tradeFee: .data[0].tradeFee,
    router: .data[0].router
  }'
```

## 获取交易详情（路由器调用数据）

注意：`slippagePercent` 是交易端点必需的参数，以小数百分比表示（例如，`0.01` = 1%）。

```bash
API_KEY="${OKX_API_KEY}"
SECRET_KEY="${OKX_SECRET_KEY}"
PASSPHRASE="${OKX_PASSPHRASE}"

CHAIN_INDEX="1"  # Ethereum
FROM_TOKEN="0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE"
TO_TOKEN="0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48"
AMOUNT="1000000000000000000"  # 1 ETH in wei
slippagePercent="0.01"  # 1%
WALLET="<YOUR_WALLET_ADDRESS>"

TIMESTAMP=$(python3 - <<'PY'
from datetime import datetime, timezone
print(datetime.now(timezone.utc).isoformat(timespec='milliseconds').replace('+00:00','Z'))
PY
)

METHOD="GET"
REQUEST_PATH="/api/v6/dex/aggregator/swap"
QUERY="chainIndex=${CHAIN_INDEX}&fromTokenAddress=${FROM_TOKEN}&toTokenAddress=${TO_TOKEN}&amount=${AMOUNT}&swapMode=exactIn&slippagePercent=${slippagePercent}&userWalletAddress=${WALLET}"
PATH_WITH_QUERY="${REQUEST_PATH}?${QUERY}"

SIGN=$(python3 - <<PY
import hmac, hashlib, base64
import os
msg = f"${TIMESTAMP}${METHOD}${PATH_WITH_QUERY}"
secret = os.environ["SECRET_KEY"].encode()
print(base64.b64encode(hmac.new(secret, msg.encode(), hashlib.sha256).digest()).decode())
PY
)

curl -s "https://web3.okx.com${PATH_WITH_QUERY}" \
  -H "OK-ACCESS-KEY: ${API_KEY}" \
  -H "OK-ACCESS-TIMESTAMP: ${TIMESTAMP}" \
  -H "OK-ACCESS-PASSPHRASE: ${PASSPHRASE}" \
  -H "OK-ACCESS-SIGN: ${SIGN}" | jq '{
    tx: .data[0].tx,
    router: .data[0].routerResult.router,
    priceImpactPercent: .data[0].routerResult.priceImpactPercent,
    dexRouterList: (.data[0].routerResult.dexRouterList // [])
  }'
```

## 获取批准交易（EVM）

注意：某些响应可能省略 `to`/`value` 参数。如果 `to` 为空，请使用“获取支持的链”响应中的 `dexTokenApproveAddress` 作为目标地址。

```bash
API_KEY="${OKX_API_KEY}"
SECRET_KEY="${OKX_SECRET_KEY}"
PASSPHRASE="${OKX_PASSPHRASE}"

CHAIN_INDEX="1"  # Ethereum
TOKEN_ADDRESS="0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48"  # USDC
AMOUNT="1000000000"  # 1,000,000 USDC (6 decimals)

TIMESTAMP=$(python3 - <<'PY'
from datetime import datetime, timezone
print(datetime.now(timezone.utc).isoformat(timespec='milliseconds').replace('+00:00','Z'))
PY
)

METHOD="GET"
REQUEST_PATH="/api/v6/dex/aggregator/approve-transaction"
QUERY="chainIndex=${CHAIN_INDEX}&tokenContractAddress=${TOKEN_ADDRESS}&approveAmount=${AMOUNT}"
PATH_WITH_QUERY="${REQUEST_PATH}?${QUERY}"

SIGN=$(python3 - <<PY
import hmac, hashlib, base64
import os
msg = f"${TIMESTAMP}${METHOD}${PATH_WITH_QUERY}"
secret = os.environ["SECRET_KEY"].encode()
print(base64.b64encode(hmac.new(secret, msg.encode(), hashlib.sha256).digest()).decode())
PY
)

curl -s "https://web3.okx.com${PATH_WITH_QUERY}" \
  -H "OK-ACCESS-KEY: ${API_KEY}" \
  -H "OK-ACCESS-TIMESTAMP: ${TIMESTAMP}" \
  -H "OK-ACCESS-PASSPHRASE: ${PASSPHRASE}" \
  -H "OK-ACCESS-SIGN: ${SIGN}" | jq '{
    data: .data[0].data,
    dexContractAddress: .data[0].dexContractAddress,
    gasLimit: .data[0].gasLimit,
    gasPrice: .data[0].gasPrice
  }'
```

## 使用“获取支持的链”中的 `to` 参数获取批准交易（EVM）

```bash
API_KEY="${OKX_API_KEY}"
PASSPHRASE="${OKX_PASSPHRASE}"

CHAIN_INDEX="1"  # Ethereum
TOKEN_ADDRESS="0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48"  # USDC
AMOUNT="1000000000"  # 1,000,000 USDC (6 decimals)

TIMESTAMP=$(python3 - <<'PY'
from datetime import datetime, timezone
print(datetime.now(timezone.utc).isoformat(timespec='milliseconds').replace('+00:00','Z'))
PY
)

METHOD="GET"
REQUEST_PATH="/api/v6/dex/aggregator/supported/chain"
QUERY="chainIndex=${CHAIN_INDEX}"
PATH_WITH_QUERY="${REQUEST_PATH}?${QUERY}"

SIGN=$(python3 - <<PY
import hmac, hashlib, base64
import os
msg = f"${TIMESTAMP}${METHOD}${PATH_WITH_QUERY}"
secret = os.environ["OKX_SECRET_KEY"].encode()
print(base64.b64encode(hmac.new(secret, msg.encode(), hashlib.sha256).digest()).decode())
PY
)

APPROVE_TO=$(curl -s "https://web3.okx.com${PATH_WITH_QUERY}" \
  -H "OK-ACCESS-KEY: ${API_KEY}" \
  -H "OK-ACCESS-TIMESTAMP: ${TIMESTAMP}" \
  -H "OK-ACCESS-PASSPHRASE: ${PASSPHRASE}" \
  -H "OK-ACCESS-SIGN: ${SIGN}" | jq -r '.data[0].dexTokenApproveAddress')

TIMESTAMP=$(python3 - <<'PY'
from datetime import datetime, timezone
print(datetime.now(timezone.utc).isoformat(timespec='milliseconds').replace('+00:00','Z'))
PY
)

METHOD="GET"
REQUEST_PATH="/api/v6/dex/aggregator/approve-transaction"
QUERY="chainIndex=${CHAIN_INDEX}&tokenContractAddress=${TOKEN_ADDRESS}&approveAmount=${AMOUNT}"
PATH_WITH_QUERY="${REQUEST_PATH}?${QUERY}"

SIGN=$(python3 - <<PY
import hmac, hashlib, base64
import os
msg = f"${TIMESTAMP}${METHOD}${PATH_WITH_QUERY}"
secret = os.environ["OKX_SECRET_KEY"].encode()
print(base64.b64encode(hmac.new(secret, msg.encode(), hashlib.sha256).digest()).decode())
PY
)

curl -s "https://web3.okx.com${PATH_WITH_QUERY}" \
  -H "OK-ACCESS-KEY: ${API_KEY}" \
  -H "OK-ACCESS-TIMESTAMP: ${TIMESTAMP}" \
  -H "OK-ACCESS-PASSPHRASE: ${PASSPHRASE}" \
  -H "OK-ACCESS-SIGN: ${SIGN}" | jq --arg to "${APPROVE_TO}" '{
    data: .data[0].data,
    dexContractAddress: (.data[0].dexContractAddress // $to),
    gasLimit: .data[0].gasLimit,
    gasPrice: .data[0].gasPrice
  }'
```

## 安全规则

1. 在执行交易前，务必显示交易详情。
2. 如果价格影响较大或超过了 `priceImpactProtectionPercent`，则发出警告。
3. 在执行交易前，检查用户的代币余额。
4. 验证滑点设置（`slippagePercent`）。
5. 对于批准响应，如果 `to` 为空，请使用该链的 `dexTokenApproveAddress` 作为目标地址。
6. 未经用户明确确认，切勿执行任何交易。

## 链接

- [OKX DEX API 参考（v6）](https://web3.okx.com/build/dev-docs/wallet-api/dex-api-reference)