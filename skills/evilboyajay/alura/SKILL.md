---
name: alura-backend-api
description: Integrate with Alura Trading backend API. Use when calling Alura testnet API, trading sessions, user auth, indicators, or leaderboard. Base URL: https://testnet-api.alura.fun
---

# Alura 后端 API

在集成或调用 Alura Trading 后端 API 时，请使用此技能。测试网 API 的基础 URL 为 **https://testnet-api.alura.fun**。

## 基础 URL

```
https://testnet-api.alura.fun
```

- Swagger 文档：`https://testnet-api.alura.fun/api/docs`
- 所有需要身份验证的接口端点都需要使用 `Authorization: Bearer <JWT>` 进行授权。

## 身份验证（EVM 钱包）

### 1. 获取挑战信息

```
POST /auth/evm/challenge
Content-Type: application/json

{ "address": "0x..." }
```

返回 `{ address, nonce, message }`。

### 2. 签名与验证

用户使用 MetaMask 对 `message` 进行签名（使用 `personal_sign` 功能）。之后：

```
POST /auth/evm/verify
Content-Type: application/json

{ "address": "0x...", "signature": "0x...", "referralCode": "OPTIONAL" }
```

返回 `{ ok: true, accessToken, tokenType: "Bearer", expiresIn: 86400, ... }`。使用 `accessToken` 进行后续请求。

## 交易会话

基础路径：`/trading-sessions`。所有请求都需要使用 Bearer 令牌。

### 快速交易 – 创建会话

```
POST /trading-sessions
Authorization: Bearer <token>
Content-Type: application/json

{
  "budget": 100,
  "profitTarget": 40,
  "lossThreshold": 5,
  "maxPositions": 3,
  "assetIndex": 0
}
```

**必需参数**：`budget`（最低 10），`profitTarget`（最高 500），`assetIndex`（Hyperliquid 的资产索引：0=BTC，1=ETH，2=SOL 等）。

### 高级交易 – 创建会话

```
POST /trading-sessions/advance
Authorization: Bearer <token>
Content-Type: application/json

{
  "amount": 100,
  "executionStrategy": "Conservative" | "Aggressive" | "Degen",
  "strategyDuration": "1D" | "3D" | "7D" | "30D" | "90D" | "365D",
  "assetIndex": 0,
  "maxWalletBudget": false
}
```

### 其他交易接口

| 方法 | 路径 | 描述 |
|--------|------|-------------|
| GET | /trading-sessions/active | 列出活跃的交易会话 |
| GET | /trading-sessions/current-trade | 当前的交易及持仓情况 |
| GET | /trading-sessions/:sessionId/logs | 会话日志 |
| GET | /trading-sessions/trades/:tradeId/logs | 交易日志（分页显示） |
| POST | /trading-sessions/positions/:positionId/close | 平仓某个持仓 |
| POST | /trading-sessions/positions/:positionId/close-signature | 为前端获取已签名的平仓交易信息 |
| POST | /trading-sessions/trades/:tradeId/close | 平仓所有持仓 |
| POST | /trading-sessions/trigger-cron | 手动触发定时任务（测试用） |

## 用户

基础路径：`/user`。所有请求都需要使用 Bearer 令牌。

| 方法 | 路径 | 描述 |
|--------|------|-------------|
| GET | /user/profile | 当前用户资料 |
| POST | /user/fills/sync | 从 Hyperliquid 同步交易信息 |
| POST | /user/withdraw | 提取资金 |
| POST | /user/close-position | 按资产索引平仓 |
| POST | /user/close-all-positions | 平仓所有持仓 |
| POST | /user/send-usdc | 发送 USDC |
| GET | /auth/evm/trading-key | 获取交易代理密钥（用于身份验证） |
| POST | /user/claim-reward | 申请奖励 |

## 指标与市场数据

基础路径：`/api/indicators`。大部分指标数据是公开的。

| 方法 | 路径 | 描述 |
|--------|------|-------------|
| GET | /api/indicators/health | 服务运行状态 |
| GET | /api/indicators/candles/latest | 最新的蜡烛图数据 |
| GET | /api/indicators/candles/history/:symbol | 历史蜡烛图数据 |
| GET | /api/indicators/candles/:symbol/:interval | 按符号和间隔查询蜡烛图数据 |
| GET | /api/indicators/candles/aggregated/symbols | 可用的符号指标 |
| GET | /api/indicators/signals/:symbol/:interval | 按符号和间隔查询交易信号 |
| GET | /api/indicators/signals/all/:interval | 所有符号的交易信号 |

## 排名榜

基础路径：`/api/leaderboard`。

| 方法 | 路径 | 描述 |
|--------|------|-------------|
| GET | /api/leaderboard/stats | 排名榜统计信息 |
| GET | /api/leaderboard/rankings | 用户排名 |
| GET | /api/leaderboard/user/:userId | 用户排名信息 |
| GET | /api/leaderboard/analytics | 分析数据 |
| GET | /api/leaderboard/health | 服务健康状况 |

## 推荐系统

基础路径：`/referrals`。

| 方法 | 路径 | 描述 |
|--------|------|-------------|
| GET | /referrals/:userId | 用户推荐信息 |
| GET | /referrals/:userId/stats | 推荐系统统计信息 |
| POST | /referrals/:userId/code | 创建推荐代码 |
| POST | /referrals/check | 核对推荐代码的有效性 |

## USDC 验证

基础路径：`/usdc-verification`。

| 方法 | 路径 | 描述 |
|--------|------|-------------|
| POST | /usdc-verification/verify | 验证 USDC 存款 |
| GET | /usdc-verification/my-transactions | 我的交易记录 |
| GET | /usdc-verification/total-deposited | 总存款金额 |

## 服务健康状况

| 方法 | 路径 | 描述 |
|--------|------|-------------|
| GET | /health | 服务基本健康状况 |
| GET | /health/kafka | Kafka 服务健康状况 |

## 资产索引（Hyperliquid Perps）

常见的资产索引：

| 符号 | 索引 |
|--------|-------|
| BTC | 0 |
| ETH | 1 |
| SOL | 2 |
| XRP | 3 |
| DOGE | 4 |
| AVAX | 5 |

## 错误处理

- 401：缺少或无效的 Bearer 令牌。请通过 `/auth/evm/challenge` 和 `/auth/evm/verify` 重新授权。
- 400：验证错误。请检查响应正文中的 `message`。
- 429：请求频率限制。请稍后重试。
- 常见错误信息：`Duplicate asset index: 你已为该资产打开了一个活跃的交易会话`、`Builder fee approval failed: HTTP 请求失败（状态码 429）`。