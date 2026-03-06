---
name: x-tweet-speedread-skill
description: **X 推文速读（高级版）** — 可即时获取任何 X 平台帖子的英文摘要。支持通过 SkillPay 进行先付费服务（每次调用费用为 0.001 美元）。
---
# X 推文速读（高级版）

只需粘贴 X 推文的链接，即可立即获得该推文的英文速读内容。

## 价格

- 每次调用费用：0.001 美元（1 个令牌）
- 先收费后使用服务
- 如果账户余额不足，系统将返回 `PAYMENT_URL`（支付链接）

## 返回内容

- 3–5 个关键要点
- 1 个核心信息
- 最多 3 个潜在风险
- 最多 3 个建议或行动建议

## 使用方法

```bash
node scripts/run.js --url "https://x.com/.../status/..." --user "<user-id>"
```

## 计费机制

- 在提取内容之前，系统会直接通过 SkillPay 进行计费。
- 如果账户余额不足，系统将返回 `PAYMENT_URL` 和 `PAYMENT_INFO`（支付相关信息）。
- 如果计费成功，系统将继续获取并总结 X 推文的内容。

## 可选配置参数

- `SKILLPAY_BILLING_URL`：SkillPay 计费接口的 URL
- `SKILL_BILLING_API_KEY`：SkillPay 计费 API 的密钥
- `SKILL_ID`：该技能的 ID
- `SKILLPAY_PRICE_TOKEN`：用于计费的令牌