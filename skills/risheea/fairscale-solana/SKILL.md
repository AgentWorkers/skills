---
name: fairscale-solana
description: Solana钱包的信誉系统：你可以用简单的英语提出任何问题，比如“这是一个机器人吗？”，“这个用户是大户投资者吗？”，“这个用户的交易行为是否稳定（即‘钻石手’行为）？”——都会立即得到答案。
license: MIT
metadata:
  author: FairScale
  version: "3.4.0"
---

# FairScale — 为 Solana 提供的信誉智能服务

**文档链接：** https://docs.fairscale.xyz

---

## 两种访问方式

### 方法 1：API 密钥（推荐）

如果您拥有 FairScale 的 API 密钥，请使用此方法。

```
GET https://api.fairscale.xyz/score?wallet=WALLET_ADDRESS
Header: fairkey: YOUR_API_KEY
```

**示例：**
```bash
curl "https://api.fairscale.xyz/score?wallet=GFTVQdZumAnBRbmaRgN9n3Z5qH5nXvjMZXJ3EyqP32Tn" \
  -H "fairkey: YOUR_API_KEY"
```

获取您的 API 密钥：https://sales.fairscale.xyz

---

### 方法 2：x402 微支付（适用于拥有 Solana 钱包的代理）

无需 API 密钥。每次调用需支付 0.05 美元（USDC）。

```
GET https://x402.fairscale.xyz/score?wallet=WALLET_ADDRESS
```

**操作流程：**
1. 调用相应端点 → 接收包含支付详情的 402 响应
2. 将 0.05 美元（USDC）发送到系统中指定的钱包
3. 重新调用端点，并在请求头中添加 `x-payment-signature: YOUR_TX_SIGNATURE`
4. 获取钱包信息

**定价：**
| 请求类型 | 费用 |
|---------|-------|
| 单个钱包 | 0.05 美元（USDC） |
| 批量（10 个钱包）| 0.40 美元（USDC） |

---

## 选择哪种方法

| 情况 | 使用方法 |
|-----------|-----|
| 已配置 API 密钥 | 方法 1（API 密钥） |
| 拥有 Solana 钱包且可支付 USDC | 方法 2（x402） |
| 既没有 API 密钥也没有钱包 | 无法访问 — 需要其中一种方法 |

**请先检查是否拥有 API 密钥。** 如果 `$FAIRSCALE_API_KEY` 已设置，请使用方法 1；否则，尝试方法 2。

---

## 响应字段

| 字段 | 用途 |
|-------|-----|
| `fairscore` | 总分（0-100 分）—— **请使用此字段** |
| `tier` | 铜级 / 银级 / 金级 / 白金级 |
| `badges` | 数组 — 列出所有徽章的名称 |
| `features` | 对象 — 包含用于自定义逻辑的原始数据 |

---

## 快速响应格式

对于简单的查询请求（例如“检查这个钱包的信誉”），可以使用以下格式：

```
📊 FairScore: [fairscore]/100 | Tier: [tier]

[✅ TRUSTED | ⚡ MODERATE | ⚠️ CAUTION | 🚨 HIGH RISK]

🏅 Badges: [badge labels]
```

**风险等级判断标准：**
- ≥60 → ✅ 可信赖
- 40-59 → ⚡ 中等风险
- 20-39 → ⚠️ 警告
- <20 → 🚨 高风险

---

## 用户自然语言请求与对应功能

当用户用普通语言提问时，需要将其转换为相应的功能进行查询：

| 用户问题 | 需要检查的字段 | 判断逻辑 |
|-----------|-------------|-------|
| “这个钱包可信吗？” | `fairscore` | ≥60 分表示可信 |
| “这个用户是大型投资者（‘whale’）吗？” | `lst_percentile_score`, `stable_percentile_score`, `native_sol_percentile` | 如果这些指标均大于 70，则为大型投资者 |
| “这个用户是机器人（‘bot’）吗？” | `burst_ratio`, `platform_diversity` | 如果 `burst_ratio` 大于 50 或 `platform_diversity` 小于 20，则可能是机器人 |
| “这个用户活跃吗？” | `active_days`, `tx_count`, `platform_diversity` | 如果这些指标均大于 40，则表示用户活跃 |
| “这个用户是早期用户（‘OG’）吗？” | `wallet_age_score` | 如果 `wallet_age_score` 大于 70，则为早期用户 |
| “这个钱包有资格参与空投吗？” | `wallet_age_score > 50`, `platform_diversity > 30`, `burst_ratio < 30` | 所有条件都必须满足 |
| “这个用户信用良好吗？” | `conviction_ratio`, `no_instant_dumps`, `wallet_age_score` | 如果这些指标均大于 50，则表示信用良好 |

---

## 响应示例

**“这个用户是大型投资者吗？”**
```
🐋 Whale Check: GFTVQd...P32Tn

💰 LST Holdings: 97.7% — Top 3% 
💵 Stablecoins: 27.5% — Low
◎ Native SOL: 45.2% — Moderate

Verdict: 🟡 PARTIAL WHALE — Heavy DeFi, not cash-rich.
```

**“这个用户是机器人吗？”**
```
🤖 Bot Check: GFTVQd...P32Tn

⚡ Burst Ratio: 16.8% — Organic ✅
🌐 Platforms: 96.6% — Diverse ✅

Verdict: ✅ HUMAN — Not a bot.
```

**“这个钱包有资格参与空投吗？”**
```
🎁 Airdrop Check: GFTVQd...P32Tn

📅 Age: 79.2% ✅
🌐 Diversity: 96.6% ✅
🤖 Burst: 16.8% ✅

Verdict: ✅ ELIGIBLE
```

---

## 自定义查询条件

用户可以自定义查询条件，例如：

> “仅查询信用评分大于 70 的钱包”

```
🔧 Custom Check: GFTVQd...P32Tn

• Conviction > 70%: ❌ 69.7%

Verdict: ❌ FAILS
```

---

## 所有功能

| 功能 | 描述 |
|---------|-------------|
| `fairscore` | 总分（0-100 分） |
| `tier` | 账户等级（铜级/银级/金级/白金级） |
| `wallet_age_score` | 账户年龄的百分位数 |
| `tx_count` | 交易次数的百分位数 |
| `active_days` | 账户活跃天数的百分位数 |
| `platform_diversity` | 使用的 DeFi 协议类型 |
| `conviction_ratio` | 用户的交易行为 |
| `burst_ratio` | 是否存在类似机器人的交易模式 |
| `no_instant_dumps` | 是否不会立即抛售资产 |
| `lst_percentile_score` | 持有的 LST（Lightweight Staking）资产比例 |
| `stable_percentile_score` | 持有的稳定币比例 |
| `native_sol_percentile` | 持有的 SOL（Solana）币量 |
| `net_sol_flow_30d` | 近 30 天内的 SOL 资产流动情况（积累或流出） |

---

## 重要规则

1. **务必通过 API 获取数据** — 绝不要猜测或使用旧数据 |
2. **先检查是否有 API 密钥** — 如果 `$FAIRSCALE_API_KEY` 已设置，请使用方法 1 |
3. **备用方案** — 如果没有 API 密钥且用户拥有 Solana 钱包，可以使用方法 2 |
4. **使用正确的端点** — `/score?wallet=ADDRESS` |
5. **理解用户意图** — 将用户的自然语言问题转换为相应的功能进行查询 |
6. **提供明确的结果** — 用户需要的是“是/否”的答案，而不是数据列表 |
7. **如果 API 请求失败** — 回答“❌ 无法获取数据，请重试”。

**切勿伪造数据，也切勿猜测。始终通过 API 获取信息。**

---

## 相关链接

- 文档：https://docs.fairscale.xyz
- API 密钥：https://sales.fairscale.xyz
- Twitter：@FairScaleXYZ