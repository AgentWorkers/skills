# Stripe CLI 技能 🧾

这是一个通用的 Moltbot 技能，集成了 Stripe CLI 的功能，用于处理支付、测试 Webhook 以及执行 API 操作。此外，还提供了针对 ShapeScale 的可选扩展功能，以支持诊所管理。

## 功能概述

- 处理支付、退款和订阅事务
- 管理客户和发票信息
- 在本地测试 Webhook
- 执行通用的 Stripe API 调用
- **ShapeScale 扩展功能**（可选）：诊所预设设置、订阅计划管理、订单集成

## 安装步骤

### 1. 安装 Stripe CLI

**macOS:**
```bash
brew install stripe/stripe-cli/stripe
```

**Linux:**
```bash
# Download from https://github.com/stripe/stripe-cli/releases
wget https://github.com/stripe/stripe-cli/releases/download/v1.34.0/stripe_1.34.0_linux_amd64.deb
sudo dpkg -i stripe_1.34.0_linux_amd64.deb
```

**身份验证:**
```bash
stripe login
```

### 2. 设置环境变量

```bash
export STRIPE_SECRET_KEY=sk_test_your_key_here
```

或使用 1Password 进行身份验证：
```bash
op read "op://Stripe/Secret Key" --vault Personal
```

### 3. 将技能克隆到 Moltbot 项目中

```bash
cd ~/.moltbot/skills/
git clone https://github.com/mkessler/stripe-cli-moltbot-skill.git stripe
```

## 使用方法

### 常用命令

| 命令          | 功能说明                |
|-----------------|----------------------|
| `Create a test customer for $50` | 创建一个金额为 $50 的测试付款请求 |
| `List my recent payments` | 列出最近的 10 笔付款请求 |
| `Check payment status for pi_xxx` | 查询付款请求的详细信息 |
| `Refund payment pi_xxx` | 退还全部付款金额 |
| `Trigger payment_intent.succeeded webhook` | 模拟 Webhook 事件触发 |
| `Listen for webhooks for 30s` | 将 Webhook 事件转发到本地服务器（localhost） |
| `Get customer details for cus_xxx` | 获取客户信息 |

### ShapeScale 扩展功能（可选）

需要 `config/shapescale-presets.json` 文件：

| 命令          | 功能说明                |
|-----------------|----------------------|
| `Create clinic deposit for PracticeXYZ` | 为诊所创建存款记录 |
| `Create monthly subscription for clinic` | 为诊所创建定期订阅计划 |
| `Generate invoice for order #1234` | 根据模板生成发票 |
| `Check order status 1234` | 根据订单状态更新数据库记录 |

## 配置设置

### 全局配置

无需额外配置，使用 `STRIPE_SECRET_KEY` 环境变量。

### ShapeScale 预设配置（可选）

创建 `config/shapescale-presets.json` 文件：

```json
{
  "clinic_templates": {
    "standard": { "deposit": 5000, "terms": "net30" },
    "premium": { "deposit": 10000, "terms": "net30" }
  },
  "subscription_plans": {
    "monthly": { "amount": 39900, "interval": "month" },
    "annual": { "amount": 399000, "interval": "year" }
  },
  "tax_rate": 0.0875,
  "default_currency": "usd"
}
```

### 必需的环境变量

| 变量          | 是否必需 | 说明                          |
|-----------------|-----------------------------|
| `STRIPE_SECRET_KEY` | 是       | Stripe 的秘密密钥（测试或生产环境使用） |
| `STRIPE_WEBHOOK_ENDPOINT` | 否       | Webhook 转发地址（默认：http://localhost:4242） |
| `SHAPESCALE_PRESETS_PATH` | 否       | ShapeScale 预设配置文件的路径         |

## 文件结构

```
stripe/
├── SKILL.md                    # This file
├── scripts/
│   ├── stripe.sh               # Universal CLI wrapper
│   └── shapescale-ext.sh       # ShapeScale extensions (optional)
├── config/
│   └── shapescale-presets.json # Clinic/subscription templates
├── patterns/
│   └── examples.md             # Usage examples
└── README.md                   # Installation guide (auto-generated)
```

## 状态管理

**无状态** — 该技能仅基于输入数据执行操作，所有状态信息存储在 Stripe 服务中。

## 与其他技能的集成

| 技能名称      | 集成方式                |
|--------------|----------------------|
| `shapescale-crm`   | 将 Stripe 客户 ID 与 CRM 记录关联 |
| `shapescale-sales` | 将订单信息转换为付款请求           |
| `campaign-orchestrator` | 在支付失败时触发后续处理流程 |
| `shapescale-db`   | 将支付信息与数据库订单匹配 |

## 发布方式

该技能已发布到 ClawdHub，可在以下链接查看：  
https://github.com/mkessler/stripe-cli-moltbot-skill

## 许可证

采用 MIT 许可协议，详细信息请参阅 LICENSE 文件。