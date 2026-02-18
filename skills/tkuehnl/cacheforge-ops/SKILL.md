---
name: cacheforge-ops
description: CacheForge 操作 — 检查余额、充值、管理上游服务、API 密钥。
license: MIT
homepage: https://app.anvil-ai.io
user-invocable: true
metadata: {"openclaw":{"emoji":"💰","homepage":"https://app.anvil-ai.io","primaryEnv":"CACHEFORGE_API_KEY","requires":{"bins":["python3"],"env":["CACHEFORGE_API_KEY"]}}}
---
## 何时使用此技能

当用户需要执行以下操作时，请使用此技能：
- 查看他们的 CacheForge 帐户余额
- 充值（支持 Stripe 或加密货币支付方式）
- 启用/配置自动充值功能
- 查看或更改上游服务提供商
- 管理 API 密钥
- 处理 402（“需要付款”）错误

## 自动计费协议

当您收到来自 CacheForge 的 402 错误时，请按照以下步骤操作：
1. 运行 `ops.py balance` 命令以查看当前余额。
2. 如果余额为 0 或负数，运行 `ops.py topup --amount 10` 命令生成支付链接。
3. 将支付链接分享给用户。
4. 支付完成后，重新尝试原始请求。

## 命令

```bash
# Check balance and billing status
python3 skills/cacheforge-ops/ops.py balance

# Create a top-up payment link ($10 USD)
python3 skills/cacheforge-ops/ops.py topup --amount 10

# Enable auto top-up ($10 when balance drops below $2)
python3 skills/cacheforge-ops/ops.py auto-topup --enable --threshold 200 --amount 1000

# View upstream provider config
python3 skills/cacheforge-ops/ops.py upstream

# Set upstream provider
python3 skills/cacheforge-ops/ops.py upstream --set --kind openrouter --api-key sk-or-...

# List API keys
python3 skills/cacheforge-ops/ops.py keys

# Create a new API key
python3 skills/cacheforge-ops/ops.py keys --create

# View tenant info
python3 skills/cacheforge-ops/ops.py info
```

## 环境变量

- `CACHEFORGE_BASE_URL` — CacheForge API 的基础地址（默认：https://app.anvil-ai.io）
- `CACHEFORGE_API_KEY` — 您的 CacheForge API 密钥（必需）

## API 接口（当前版本）

此技能使用的 API 接口包括：
- `GET /v1/account/billing`  
- `POST /v1/account/billing/topup`  
- `PATCH /v1/account/billing/auto-topup`  
- `GET /v1/account/info`  
- `GET /v1/account/upstream`, `POST /v1/account/upstream`  
- `GET /v1/account/keys`, `POST /v1/account/keys`, `POST /v1/account/keys/{keyID}/revoke`