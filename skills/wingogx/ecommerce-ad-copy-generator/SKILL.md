---
name: ecommerce-ad-copy-generator
description: 使用 SkillPay 支付功能，批量生成付费的电子商务广告文案。当用户需要 5 条包含产品名称、销售亮点和目标受众信息的广告文案时，可通过 `/billing/charge` 接口按每条请求 0.10 美元的价格进行收费；若账户余额不足，系统会返回 `payment_url`；同时需严格执行输入验证和错误处理机制。
---
# 电子商务广告文案生成器

## 概述

该工具可以根据结构化产品信息生成5条针对`Facebook`、`Google`或`TikTok`平台的转化型广告文案。在生成广告内容之前，会收取0.10美元（USDT）的费用。

## 工作流程

1. 解析并验证输入字段：
   - `user_id`
   - `product_name`
   - `selling_points`（列表形式或用逗号分隔的字符串）
   - `target_audience`
2. 调用SkillPay的`POST /billing/charge`接口，支付0.10美元。
3. 如果支付成功，生成5条适配各平台的广告文案。
4. 如果支付余额不足，返回`INSUFFICIENT_BALANCE`以及支付链接(`payment_url`)。
5. 返回结构化的JSON格式输出结果，供后续使用。

## 运行方式

- 核心脚本：`scripts/ecommerce_ad_copy_generator.py`
- 测试脚本：`scripts/test_ecommerce_ad_copy_generator.py`

**使用直接参数运行：**
```bash
python3 scripts/ecommerce_ad_copy_generator.py \
  --user-id user_001 \
  --product-name "CloudBoost 智能投放器" \
  --selling-points 智能出价 多平台同步 分钟级报表 \
  --target-audience "跨境电商运营团队"
```

**使用JSON文件运行：**
```bash
python3 scripts/ecommerce_ad_copy_generator.py --input-file ./payload.json
```

**运行测试：**
```bash
python3 -m unittest scripts/test_ecommerce_ad_copy_generator.py -v
```

## 输出结果

**成功情况：**
- `success: true`
- `pricing.amount: "0.10"`
- `pricing_currency: "USDT"`
- `copies`: 包含5条广告文案，每条文案包含以下信息：
  - `platform`（平台名称）
  - `headline`（标题）
  - `body`（正文）
  - `cta`（行动号召）

**失败情况：**
- 如果输入无效，返回`VALIDATION_ERROR`。
- 如果余额不足，返回`INSUFFICIENT_BALANCE`以及支付链接(`payment_url`)。
- 如果支付失败（例如余额不足），返回`BILLING_ERROR`。

## 环境变量

- `SKILLPAY_CHARGE_ENDPOINT`（默认值：`https://skillpay.me/billing/charge`）
- `SKILLPAY_API_KEY`（可选的bearer token）
- `SKILLPAY_payment_URL_TEMPLATE`（可选；支持 `{user_id}` 格式）
- `SKILLPAY_TOPUP_BASE_URL`（默认值：`https://skillpay.me/pay`）

## 参考资料

- SkillPay的请求/响应规范及异常处理方式：`references/skillpay-api-contract.md`