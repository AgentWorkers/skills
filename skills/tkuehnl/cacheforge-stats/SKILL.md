---
name: cacheforge-stats
version: 1.0.0
description: CacheForge 终端控制台——提供使用情况、节省的数据量以及性能指标的详细信息。您可以清楚地了解自己的代币（tokens）被用在了哪里。
author: CacheForge
license: MIT
homepage: https://app.anvil-ai.io
user-invocable: true
tags:
  - cacheforge
  - metrics
  - dashboard
  - ai-agents
  - token-optimization
  - llm
  - observability
  - discord
  - discord-v2
metadata: {"openclaw":{"emoji":"📊","homepage":"https://app.anvil-ai.io","primaryEnv":"CACHEFORGE_API_KEY","requires":{"bins":["python3"],"env":["CACHEFORGE_API_KEY"]}}}
---
## 何时使用此技能

当用户需要执行以下操作时，请使用此技能：
- 查看自己在 CacheForge 中的使用情况及节省的费用；
- 查看包含图表的终端控制台界面；
- 检查令牌的减少率；
- 查看费用节省的详细信息；
- 监控缓存性能。

## 命令

```bash
# Full terminal dashboard
python3 skills/cacheforge-stats/dashboard.py dashboard

# Usage summary
python3 skills/cacheforge-stats/dashboard.py usage --window 7d

# Breakdown by model/provider/key
python3 skills/cacheforge-stats/dashboard.py breakdown --by model

# Savings-focused view
python3 skills/cacheforge-stats/dashboard.py savings
```

## 环境变量

- `CACHEFORGE_BASE_URL` — CacheForge API 的基础地址（默认值：https://app.anvil-ai.io）
- `CACHEFORGE_API_KEY` — 你的 CacheForge API 密钥（必需）

## API 接口（当前版本）

此技能使用的 API 接口包括：
- `GET /v1/account/billing`  
- `GET /v1/account/info`  
- `GET /v1/account/usage`  
- `GET /v1/account/usage/breakdown`