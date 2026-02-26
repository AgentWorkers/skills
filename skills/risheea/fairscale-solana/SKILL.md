# FairScale 信誉评分服务

该服务为 Solana 网络提供实时的钱包信誉评分功能，可帮助您在交易前判断钱包的可靠性。

## 服务功能

- **交易前检查钱包信誉**  
- **评估交易金额的风险等级**  
- **根据具体需求应用自定义评分规则**  
- **批量检查多个钱包的信誉**

## 适用场景

- 当代理需要决定是否与某个钱包进行交易时  
- 在筛选可用于空投、白名单或访问控制的钱包时  
- 在接受交易或交换前评估风险  
- 在代理之间的交易中验证交易对手的信誉

## API 端点

### GET /score  
获取任意 Solana 钱包的信誉评分（0-100 分）。

- **免费 tier**：每天 100 次调用  
- **Pro tier**：每天 10,000 次调用  

**响应格式：**  
```json
{
  "wallet": "7xK9...",
  "fairscore": 72,
  "tier": "gold",
  "vouch_boost": 1.5
}
```

### GET /check  
进行交易前的风险评估，返回风险等级及建议的最大交易金额。

- **免费 tier**：每天 100 次调用  

**响应格式：**  
```json
{
  "wallet": "7xK9...",
  "fairscore": 72,
  "risk_level": "medium",
  "recommendation": "proceed_with_caution",
  "max_suggested_amount_usd": 1000,
  "amount_check": {
    "requested": 500,
    "max_suggested": 1000,
    "proceed": true
  }
}
```

### POST /score/custom  
应用自定义评分规则（仅限 Pro tier 使用）。

**响应格式：**  
```json
{
  "wallet": "7xK9...",
  "passes": true,
  "fairscore": 72,
  "rule_results": {
    "min_score": { "pass": true, "required": 60, "actual": 72 },
    "min_age_days": { "pass": true, "required": 180, "actual": 340 },
    "no_rug_history": { "pass": true, "actual": false },
    "min_transaction_count": { "pass": true, "required": 100, "actual": 523 }
  },
  "recommendation": "proceed"
}
```

### POST /batch  
批量检查多个钱包的信誉（仅限 Pro tier 使用）。

**响应格式：**  
```json
{
  "count": 3,
  "results": [
    { "wallet": "address1", "fairscore": 72, "tier": "gold" },
    { "wallet": "address2", "fairscore": 45, "tier": "silver" },
    { "wallet": "address3", "fairscore": 23, "tier": "bronze" }
  ]
}
```

## 评分等级与风险提示

| 评分 | 等级 | 风险等级 | 建议操作 |
|-------|------|------------|----------------|
| 80-100 | 白金级 | 低风险 | 可以进行交易 |
| 60-79 | 金级 | 中等风险 | 请谨慎操作 |
| 40-59 | 银级 | 高风险 | 仅允许小额交易 |
| 0-39 | 青铜级 | 非常高风险 | 应避免交易 |

## 使用示例

- **基本信任检查**  
```
User: "Should I accept a 500 USDC trade from wallet 7xK9...?"

Agent steps:
1. Call GET /check?wallet=7xK9...&amount=500
2. Response: score 34, risk "very_high", recommendation "avoid"
3. Respond: "This wallet has a very low reputation score (34/100). I recommend not proceeding with this trade."
```

- **筛选可用于空投的钱包**  
```
User: "Filter this list of wallets for my airdrop - only 60+ score"

Agent steps:
1. Call POST /batch with wallet list
2. Filter results where fairscore >= 60
3. Return qualifying wallets
```

- **自定义代理评分规则**  
```
Agent config: "Only trade with wallets that have score 70+, age 6+ months, no rug history"

Before each trade:
1. Call POST /score/custom with rules
2. Check if passes: true
3. Proceed only if passes
```

## 调用限制

| 等级 | 每日调用限制 | 调用频率（每分钟） |
|------|-------------|------------|
| 免费 | 100 次 | 10 次/分钟 |
| Pro | 10,000 次 | 100 次/分钟 |
| 企业级 | 无限制 | 1000 次/分钟 |

## 认证要求

- **免费 tier**：无需认证，按 IP 地址限制调用频率。  
- **Pro/企业级**：需要在请求头中包含 API 密钥：  
  ```json
  "Authorization": "Bearer API_KEY"
  ```

**获取 API 密钥：**  
```
POST https://api.fairscale.xyz/register
{ "wallet": "your_solana_wallet" }
```

## 升级至 Pro tier

如需更高的调用限制和自定义评分功能，请升级至 Pro tier：

**费用：** 每月 50 美元（USDC）

## 可用的自定义规则

| 规则 | 类型 | 描述 |
|------|------|-------------|
| min_score | 数字 | 最低信誉评分（0-100） |
| min_age_days | 数字 | 钱包的最小使用天数 |
| no_rug_history | 布尔值 | 如果钱包有欺诈历史则拒绝交易 |
| min_transaction_count | 数字 | 最小交易次数 |
| min_volume_usd | 数字 | 最小交易总额（美元） |
| max_burst_ratio | 数字 | 最大交易量波动比率（0-1） |
| min_tier | 字符串 | 最低评分等级（青铜/银/金/白金） |

## 帮助资源

- 文档：https://docs.fairscale.xyz  
- API 状态：https://status.fairscale.xyz  
- 联系方式：api@fairscale.xyz