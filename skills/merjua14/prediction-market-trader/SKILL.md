---
name: prediction-market-trader
description: Kalshi预测市场交易工具包：包含API认证（RSA-PSS签名）、市场扫描、Sofascore网球赔率分析、真实概率计算、Kelly准则下的投注金额确定以及订单执行功能。适用于在Kalshi平台上进行交易、分析预测市场赔率、计算预期收益、调整博彩公司的赔率、根据Kelly准则确定投注金额，或开发预测市场自动化交易程序。
---
# 预测市场交易工具——Kalshi交易套件

利用先进的技术优势进行预测市场交易：扫描市场数据、计算真实概率、确定交易头寸规模、执行交易指令。

## 工作流程：

1. **扫描市场**：通过Kalshi API按类别（体育、天气、政治、经济）获取市场数据。
2. **去除佣金**：从Sofascore获取博彩公司的赔率，并扣除佣金以获得真实概率。
3. **对比分析**：比较Kalshi提供的价格与真实概率，确保存在至少4%的利润空间。
4. **确定头寸规模**：使用Kelly准则来计算每笔交易的最大头寸比例（不超过总资金的15%）。
5. **执行交易**：通过Kalshi API使用RSA-PSS认证机制下达限价单。
6. **监控交易**：实时跟踪交易头寸、盈亏情况，并在达到盈利目标时平仓。

## 所需条件：

- **Kalshi API凭证**：`KALSHI_KEY_ID` 和 `KALSHI_PRIVATE_KEY`（RSA私钥，可以以字符串形式直接提供或保存为.pem文件）。
- **Node.js 18.0及以上版本**：用于使用RSA-PSS进行签名操作。

## 快速入门指南

```bash
# Set credentials
export KALSHI_KEY_ID=your_key_id
export KALSHI_PRIVATE_KEY="-----BEGIN RSA PRIVATE KEY-----\n...\n-----END RSA PRIVATE KEY-----"

# Scan for edges
node scripts/scan-edges.js --category tennis

# Place a trade (dry run)
node scripts/trade.js --ticker KXATPMATCH-26MAR12DRAMED-DRA --side yes --price 38 --count 10 --dry

# Check portfolio
node scripts/portfolio.js
```

## Kalshi API认证

Kalshi API支持RSA-PSS签名机制。签名信息包含：`timestamp + method + path`（签名过程中不包含请求体）。

```javascript
const crypto = require('crypto');
const timestamp = Math.floor(Date.now() / 1000).toString();
const message = timestamp + 'GET' + '/trade-api/v2/portfolio/balance';
const signature = crypto.sign('sha256', Buffer.from(message), {
  key: crypto.createPrivateKey(privateKey),
  padding: crypto.constants.RSA_PKCS1_PSS_PADDING,
  saltLength: 32
});
```

请求头信息：`KALSHI-ACCESS-KEY`、`KALSHI-ACCESS-TIMESTAMP`、`KALSHI-ACCESS-SIGNATURE`（均需使用base64编码）。

## 去除佣金的方法

博彩公司的赔率中包含佣金（vig），需要将其扣除以获得真实概率。

```
implied_prob_A = 1 / decimal_odds_A
implied_prob_B = 1 / decimal_odds_B
total = implied_prob_A + implied_prob_B  (always > 1.0)
true_prob_A = implied_prob_A / total
true_prob_B = implied_prob_B / total
```

## Kelly准则用于头寸规模计算

```
edge = true_probability - kalshi_price
odds = (1 / kalshi_price) - 1
kelly_fraction = (true_prob * odds - (1 - true_prob)) / odds
position_size = kelly_fraction * 0.25 * bankroll  (quarter-Kelly)
```

交易限制：每笔交易的最大头寸比例不超过总资金的15%，且必须确保存在至少4%的利润空间。

## 相关脚本：

- `scripts/kalshi-auth.js`：使用RSA-PSS认证的Kalshi API客户端。
- `scripts/scan-edges.js`：扫描市场数据并与Sofascore的赔率进行对比分析。
- `scripts/trade.js`：执行交易指令，并包含安全检查机制。
- `scripts/portfolio.js`：查询账户余额、交易头寸及盈亏情况。

## 参考资料：

- `references/market-categories.md`：Kalshi支持的各类市场及其最佳利润空间来源。
- `references/risk-rules.md`：头寸规模计算规则与风险管理指南。
- `references/lessons-learned.md`：常见错误及避免方法。

## 经过实战验证的关键要点：

- **网球预选赛/挑战赛**：最佳的利润空间来源（赔率差异通常在5-40%之间）。
- **NBA/NHL现场赛事**：赔率差极小（几乎无利润空间，不建议交易）。
- **NCAAB小型联盟赛事**：赔率差异约为4-9%。
- **印度威尔斯公开赛正赛**：赔率定价较为合理（与博彩公司报价相差在1-3%以内）。
- **实时交易机会通常在2-3分钟内出现**：速度至关重要。
- **天气相关市场**：价格波动较大，美国国家气象局（NWS）的数据有一定参考价值，但天气预报可能存在误差。
- **在交易时务必按名称匹配赔率数据，切勿使用数组索引**。

---

（注：由于代码块内容较长，实际翻译中可能需要对部分内容进行拆分或合并以保持流畅性。以上翻译遵循了提供的规则和要求。）