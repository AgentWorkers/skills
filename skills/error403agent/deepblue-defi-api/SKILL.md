---
name: deepblue-defi-api
description: **使用场景：** 当代理需要实时获取来自 Base 的 DeFi 数据时（例如 ETH 价格、热门交易池信息、代币评分或钱包扫描结果）。无需进行身份验证。
homepage: https://deepbluebase.xyz
---
# DeepBlue DeFi 研究 API

## 概述

这是一个由 DeepBlue 团队开发的公共、只读的 REST API。DeepBlue 是一个由 4 个自主 AI 代理组成的团队，基于 Base 平台运行。该 API 提供实时的链上 DeFi 研究数据，包括来自 Chainlink 的 ETH 价格、来自 GeckoTerminal 的热门交易池信息、代币购买质量分析，以及通过 Blockscout 进行的钱包 ERC20 代币扫描。

**免费使用限制：** 每天 10 次请求，无需身份验证。

源代码和完整项目请访问：[github.com/ERROR403agent/clawford](https://github.com/ERROR403agent/clawford)。

## 使用场景

- 需要从链上来源（Chainlink）获取当前的 ETH/USD 价格。
- 希望发现 Base 平台上热门的代币/交易池。
- 需要对代币的购买质量（动能、交易量、购买压力、流动性）进行评估。
- 需要扫描钱包中 ERC20 代币的持有情况，并获取其对应的 USD 价值。

**不适用场景：**
- 需要其他链上的数据（目前仅支持 Base 链）。
- 需要历史数据（本 API 提供的仅为实时数据）。
- 需要交易执行功能（本 API 仅提供只读研究数据）。

## API 参考

**基础 URL：** `https://deepbluebase.xyz`

所有接口均支持只读的 GET 请求，无需身份验证、钱包签名或代币。

### ETH/USD 价格

```bash
curl https://deepbluebase.xyz/price/eth
```
```json
{"eth_usd": 1966.77, "source": "chainlink+coingecko", "cached_ttl": 60}
```

### Base 平台上的热门交易池

```bash
curl https://deepbluebase.xyz/trending
```
```json
{"pools": [{"name": "TOKEN / WETH", "symbol": "TOKEN", "token_address": "0x...", "price_usd": "0.001", "price_change_24h": 42.5, "volume_24h": 150000, "score": 0.68}], "tier": "free", "showing": "5/10"}
```

### 代币购买质量评分（0.0–1.0）

```bash
curl https://deepbluebase.xyz/token/0xTOKEN_ADDRESS/score
```
```json
{"token": "0x...", "symbol": "FELIX", "score": 0.41, "price_usd": "0.00012", "pool_data": {"raw_price_change_24h": 56.1, "raw_liquidity_usd": 150000, "raw_volume_24h": 500000, "raw_buys_24h": 1200, "raw_sells_24h": 900}, "tier": "free"}
```

评分标准：
- **0.7+**：强烈的购买信号（高动能、健康的交易量/流动性、看涨压力）
- **0.5–0.7**：中等——部分指标表现良好
- **低于 0.5**：购买信号较弱——建议谨慎操作

### 钱包 ERC20 代币扫描

```bash
curl https://deepbluebase.xyz/wallet/0xWALLET_ADDRESS/scan
```
```json
{"wallet": "0x...", "tokens": [{"symbol": "USDC", "balance": "500.0", "value_usd": 500.0}], "tier": "free", "showing": "3/15"}
```

### DEEP 代币信息

```bash
curl https://deepbluebase.xyz/deep/info
```

### 系统健康检查

```bash
curl https://deepbluebase.xyz/health
```

## Python 集成方式

```python
import requests

BASE = "https://deepbluebase.xyz"

# Get ETH price
price = requests.get(f"{BASE}/price/eth").json()["eth_usd"]

# Get trending pools with scores
trending = requests.get(f"{BASE}/trending").json()
for pool in trending["pools"]:
    print(f"{pool['symbol']}: ${pool['price_usd']} ({pool['price_change_24h']:+.1f}%)")

# Score a specific token
token = "0xf30bf00edd0c22db54c9274b90d2a4c21fc09b07"
result = requests.get(f"{BASE}/token/{token}/score").json()
print(f"{result['symbol']} buy score: {result['score']}")

# Scan a wallet
wallet = "0x47ffc880cfF2e8F18fD9567faB5a1fBD217B5552"
holdings = requests.get(f"{BASE}/wallet/{wallet}/scan").json()
for t in holdings["tokens"]:
    print(f"{t['symbol']}: ${t['value_usd']:.2f}")
```

## 响应格式

所有接口返回 JSON 格式的数据。出现错误时，会返回 `{"detail": "错误信息"}` 以及相应的 HTTP 状态码（400、404、429）。

## 请求限制

每个 IP 每天最多 10 次请求。`/trending` 和 `/health` 接口不受此限制。

如需更多功能？在 Base 平台上持有任意数量的 `$DEEP` 代币，即可每天获得 100 次请求权限，并享受 AI 提供的代币诊断和实时交易信号服务。详情请访问：`GET /pricing`

## 隐私与数据管理

- **无状态 API**：不存储或记录任何钱包地址、查询信息或 IP 地址。所有请求均会被处理后丢弃。
- **仅使用公开数据**：所有响应内容均来源于链上公开数据（通过 Blockscout、Chainlink 价格数据源和 GeckoTerminal 提供的交易池数据）。不会访问或返回任何私有或链下数据。
- **无需身份验证或钱包签名**：API 从不请求用户的私钥、签名、助记词或钱包连接信息。所有请求均为匿名 GET 请求。
- **$DEEP 持有者特权**：对于 $DEEP 持有者，系统会通过检查请求 IP 关联地址的链上余额来提供更高的请求限制（如果通过 `/token/.../score` 路径提供该地址）。此过程不涉及钱包识别、认证令牌或会话跟踪。

## 运营者与技术背景

- **运营方：** DeepBlue——一个由 4 个自主 AI 代理组成的团队（EXEC、Mr. Clawford、Dr. ZoidClaw、Fishy），由 FlippersPad 构建和维护。
- **源代码：** 完全开源，位于 [github.com/ERROR403agent/clawford](https://github.com/ERROR403agent/clawford)。API 服务器（`deep_api.py`）、评分引擎（`defi_engine.py）以及本 API 的详细说明均包含在该仓库中。
- **基础设施：** 托管在 AWS EC2（us-east）上。该 API 仅作为代理服务器，用于转发公共区块链数据，不存储资金、执行交易或访问任何钱包。
- **联系方式：** [Discord](https://discord.gg/wpSKuA57bq) 或通过 GitHub 提交问题。

## 相关链接

- [代币扫描工具](https://deepbluebase.xyz/scan.html)
- [价格与等级信息](https://deepbluebase.xyz/pricing)
- [交互式 API 文档](https://deepbluebase.xyz/docs)
- [源代码 / GitHub](https://github.com/ERROR403agent/clawford)
- [Discord](https://discord.gg/wpSKuA57bq)