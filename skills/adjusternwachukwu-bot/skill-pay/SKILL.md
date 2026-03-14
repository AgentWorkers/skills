---
name: skill-pay
description: >
  您可以为任何 OpenClaw 技能添加基于信用的支付功能。具体步骤如下：
  1. **注册付费技能**：将某些技能设置为付费服务，以便用户在使用这些技能时需要支付费用。
  2. **按调用次数计费**：根据用户使用技能的次数来收取费用。
  3. **跟踪收入**：系统会自动记录用户的收入情况。
  4. **提取 USDC**：用户可以将赚取的 USDC 提取到自己的账户中。
  这些功能适用于以下场景：
  - 当用户希望将某个技能转化为盈利来源时。
  - 为代理服务设置支付机制时。
  - 检查用户的信用余额时。
  - 用户希望将自己的技能集成到代理的工作流程中，并实现按使用次数计费的模式时。
  请注意，这些功能需要您具备相应的系统配置和开发知识。如果您需要进一步的帮助或指导，请随时联系我们的技术支持团队。
---
# SkillPay — 为代理经济提供信用支持

这是一个用于 OpenClaw 技能的通用支付系统。开发者可以注册付费技能，用户可以购买信用点数，技能会根据每次调用进行收费。

## 设置

API 基础地址：`https://skillpay.gpupulse.dev/api/v1`

## 对于用户（购买者）

### 注册
```bash
curl -X POST "$BASE/user/register" \
  -H "Content-Type: application/json" \
  -d '{"name": "my-agent", "email": "optional@email.com"}'
```
返回 `sp_usr_...` API 密钥（请保存该密钥，仅显示一次）。

### 购买信用点数
```bash
curl -X POST "$BASE/user/deposit" \
  -H "Authorization: Bearer sp_usr_..." \
  -H "Content-Type: application/json" \
  -d '{"amount": 100}'
```

### 查看余额
```bash
curl "$BASE/user/balance" -H "Authorization: Bearer sp_usr_..."
```

## 对于开发者（卖家）

### 注册为开发者
```bash
curl -X POST "$BASE/builder/register" \
  -H "Content-Type: application/json" \
  -d '{"name": "my-company", "wallet_address": "SolanaWalletAddress"}'
```
返回 `sp_bld_...` API 密钥。

### 注册付费技能
```bash
curl -X POST "$BASE/builder/skill/register" \
  -H "Authorization: Bearer sp_bld_..." \
  -H "Content-Type: application/json" \
  -d '{"slug": "my-skill", "name": "My Skill", "description": "Does something useful", "price_credits": 10}'
```

### 查看收益
```bash
curl "$BASE/builder/earnings" -H "Authorization: Bearer sp_bld_..."
```

### 提现
```bash
curl -X POST "$BASE/builder/withdraw" \
  -H "Authorization: Bearer sp_bld_..." \
  -H "Content-Type: application/json" \
  -d '{"amount": 50}'
```

## 集成（关键部分）

将以下代码添加到您的技能中，以实现按调用收费的功能：
```python
import requests

def charge_user(user_key, skill_slug="my-skill"):
    resp = requests.post("https://skillpay.gpupulse.dev/api/v1/pay", json={
        "user_key": user_key,
        "skill_slug": skill_slug
    })
    if resp.status_code == 200:
        return True  # paid, execute skill
    elif resp.status_code == 402:
        return False  # insufficient credits
    return False
```

## 浏览技能
```bash
curl "$BASE/skills"  # no auth needed — public catalog of all paid skills
```

## 平台费用

每笔交易收取 2.5% 的费用。开发者自行设定技能的价格（以信用点数计），最终可获得 97.5% 的收益。

## 信用点数兑换比例

1 美元（USDC） = 1 信用点数（可根据技能类型进行调整）。