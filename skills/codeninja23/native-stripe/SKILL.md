---
name: stripe
description: "通过 Stripe API 查询和管理 Stripe 数据。当您需要列出费用、客户、发票、订阅信息、支付请求、退款、产品或价格时，可以使用此功能。支持过滤、分页操作，以及创建/更新客户和退款信息。直接调用 api.stripe.com，无需使用第三方代理。"
metadata:
  openclaw:
    requires:
      env:
        - STRIPE_SECRET_KEY
      bins:
        - python3
    primaryEnv: STRIPE_SECRET_KEY
    files:
      - "scripts/*"
---
# Stripe

您可以通过 Stripe API (`api.stripe.com`) 直接与您的 Stripe 账户进行交互。

## 设置（一次性操作）

1. 从 https://dashboard.stripe.com/apikeys 获取您的秘密密钥。
2. 设置环境变量：
   ```
   STRIPE_SECRET_KEY=sk_live_...
   ```
   使用 `sk_test_...` 以测试模式运行。

## 查询

### 列出最近的收费记录
```bash
python3 /mnt/skills/user/stripe/scripts/stripe_query.py charges --limit 10
```

### 列出客户信息
```bash
python3 /mnt/skills/user/stripe/scripts/stripe_query.py customers --limit 20
```

### 按电子邮件搜索客户
```bash
python3 /mnt/skills/user/stripe/scripts/stripe_query.py customers --email user@example.com
```

### 列出订阅信息
```bash
python3 /mnt/skills/user/stripe/scripts/stripe_query.py subscriptions --limit 20
```

### 列出活跃的订阅
```bash
python3 /mnt/skills/user/stripe/scripts/stripe_query.py subscriptions --status active --limit 20
```

### 列出发票
```bash
python3 /mnt/skills/user/stripe/scripts/stripe_query.py invoices --limit 20
```

### 列出支付意图
```bash
python3 /mnt/skills/user/stripe/scripts/stripe_query.py payment_intents --limit 20
```

### 列出产品信息
```bash
python3 /mnt/skills/user/stripe/scripts/stripe_query.py products --limit 20
```

### 列出价格信息
```bash
python3 /mnt/skills/user/stripe/scripts/stripe_query.py prices --limit 20
```

### 列出退款记录
```bash
python3 /mnt/skills/user/stripe/scripts/stripe_query.py refunds --limit 20
```

### 获取特定对象
```bash
python3 /mnt/skills/user/stripe/scripts/stripe_query.py get charges ch_abc123
python3 /mnt/skills/user/stripe/scripts/stripe_query.py get customers cus_abc123
python3 /mnt/skills/user/stripe/scripts/stripe_query.py get subscriptions sub_abc123
```

### 创建退款
```bash
python3 /mnt/skills/user/stripe/scripts/stripe_query.py create refunds --charge ch_abc123
python3 /mnt/skills/user/stripe/scripts/stripe_query.py create refunds --charge ch_abc123 --amount 1000
```

### 更新客户信息
```bash
python3 /mnt/skills/user/stripe/scripts/stripe_query.py update customers cus_abc123 --email new@example.com --name "New Name"
```

## 输出格式

- 列表数据以表格形式输出；
- 单个对象以 JSON 格式输出。
- 使用 `--json` 标志可获取原始 JSON 数据。

## 资源

- 收费记录（charges）、客户信息（customers）、发票（invoices）、订阅信息（subscriptions）、支付意图（payment_intents）、退款记录（refunds）、产品信息（products）、价格信息（prices）、余额交易记录（balance_transactions）