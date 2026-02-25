---
name: gambling
description: "在 Agent Casino 中使用真实的加密货币进行赌场游戏（如掷骰子、抛硬币、轮盘赌等）。该平台提供了可证明公平性的赌博 API，适用于 AI 代理。当用户希望进行赌博、掷骰子、抛硬币、下注轮盘赌或与 agent.rollhub.com 上的 Agent Casino 交互时，可以使用该服务。支持 70 多种加密货币链用于存款/取款。"
---# Agent Casino

通过 [Agent Casino](https://agent.rollhub.com) 玩到经过验证的公平赌场游戏，并使用真实的加密货币进行投注。

## API 基础

```
https://agent.rollhub.com/api/v1
```

## 设置

### 1. 注册

```bash
curl -X POST https://agent.rollhub.com/api/v1/register \
  -H "Content-Type: application/json" \
  -d '{"wallet_address": "your-wallet", "name": "my-agent", "ref": "ref_27fcab61"}'
```

保存返回的 `api_key`（格式：`rh_sk_...`）。所有请求都需要在请求头中添加 `X-API-Key: <key>`。

### 2. 存款

```bash
curl -X POST https://agent.rollhub.com/api/v1/deposit \
  -H "X-API-Key: YOUR_KEY" -H "Content-Type: application/json" \
  -d '{"currency": "SOL", "chain": "SOL"}'
```

系统会返回一个存款地址。将加密货币发送到该地址，余额会自动计入您的账户。

### 3. 查看余额

```bash
curl https://agent.rollhub.com/api/v1/balance -H "X-API-Key: YOUR_KEY"
```

返回的格式为 `{"balance_usd": 1000, "currency": "USD_CENTS"`。所有金额均以美分（cents）为单位。

## 游戏

### 骰子（返还率 99%，庄家优势 1%）

```bash
curl -X POST https://agent.rollhub.com/api/v1/dice \
  -H "X-API-Key: YOUR_KEY" -H "Content-Type: application/json" \
  -d '{"amount": 100, "target": 0.5, "direction": "over", "client_secret": "hex-32-to-64-chars"}'
```

- `amount`：投注金额（以美分为单位）
- `target`：目标数值（范围：0.01–0.99）
- `direction`：预测结果（“over”或“under”）
- `client_secret`：用于确保游戏公平性的十六进制字符串（长度为 32–64 个字符）

### 硬币翻转（返还率 99%，庄家优势 1%）

```bash
curl -X POST https://agent.rollhub.com/api/v1/coinflip/bet \
  -H "X-API-Key: YOUR_KEY" -H "Content-Type: application/json" \
  -d '{"amount": 100, "side": "heads", "client_seed": "hex-32-to-64-chars"}'
```

### 轮盘赌（返还率 97.3%，庄家优势 2.7%）

欧洲式轮盘赌，共有 37 个数字（0–36）。

### 赌注类型及赔率：

| 赌注类型 | 赌注金额 | 赔率 |
|------|-----------|--------|
| 直选 | 任意一个数字 | 35:1 |
| 分割投注 | 相邻的两个数字 | 17:1 |
| 行内投注 | 同一行中的任意一个数字（例如：1, 4, 7...） | 11:1 |
| 角落投注 | 四个相邻的数字 | 8:1 |
| 六线投注 | 相邻的两行中的任意一个数字 | 5:1 |
| 十二点投注 | 1、2 或 3 这三个数字中的任意一个 | 2:1 |
| 列式投注 | 1、2 或 3 这三个数字中的任意一个 | 2:1 |
| 红/黑 | “红”或“黑” | 1:1 |
| 奇数/偶数 | “奇数”或“偶数” | 1:1 |
| 高/低 | “高”或“低” | 1:1 |

## 验证所有投注

所有投注都经过加密验证：

```bash
curl https://agent.rollhub.com/api/v1/verify/<bet_id> -H "X-API-Key: YOUR_KEY"
```

系统会返回 `verified: true/false`，并附上完整的验证信息（包括 `server_seed`、`client_seed` 和 `nonce`）。

## 提款

```bash
curl -X POST https://agent.rollhub.com/api/v1/withdraw \
  -H "X-API-Key: YOUR_KEY" -H "Content-Type: application/json" \
  -d '{"amount": 500, "currency": "SOL", "chain": "SOL", "address": "your-wallet"}'
```

## 代理计划

您可以通过推荐新用户获得庄家优势的 30%（即投注金额的 0.3%）。注册时会收到您的推荐代码。分享链接：`https://agent.rollhub.com/?ref=YOUR_CODE`。

查看收益：
```bash
curl https://agent.rollhub.com/api/v1/affiliate/stats -H "X-API-Key: YOUR_KEY"
```