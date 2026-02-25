---
name: Paddle
slug: paddle
version: 1.0.0
homepage: https://clawic.com/skills/paddle
description: 将 Paddle 支付系统与订阅服务、Webhook、结账流程以及税务合规性要求集成在一起。
changelog: Initial release with API reference, webhook handling, and checkout integration.
metadata: {"clawdbot":{"emoji":"🏓","requires":{"bins":[]},"os":["linux","darwin","win32"]}}
---
## 设置

首次使用时，请阅读 `setup.md` 以获取集成指南。

## 使用场景

当用户需要将 Paddle 用于 SaaS 支付时，该技能便派上用场。代理程序负责处理 API 调用、Webhook 验证、结账设置、订阅管理以及税务合规配置。

## 架构

所有与内存相关的数据存储在 `~/paddle/` 目录下。具体结构请参阅 `memory-template.md`。

```
~/paddle/
├── memory.md     # API keys, environment, product IDs
└── webhooks.md   # Webhook endpoints and event handling
```

## 快速参考

| 主题 | 文件 |
|-------|------|
| 设置流程 | `setup.md` |
| 内存模板 | `memory-template.md` |
| API 端点 | `api.md` |
| Webhook 处理 | `webhooks.md` |

## 核心规则

### 1. 始终先在沙箱环境中进行测试
- 在正式生产环境之前，务必在沙箱环境中测试所有集成功能。
- 沙箱 API：`https://sandbox-api.paddle.com`
- 正式生产 API：`https://api.paddle.com`
- 对于支付流程，切勿跳过沙箱测试。

### 2. 验证 Webhook 签名
- 在处理任何 Webhook 请求之前，必须对其进行签名验证。
- 使用 Paddle 仪表板提供的 Webhook 密钥进行验证。
- 对于签名无效的请求，应立即拒绝。
- 记录验证失败的情况以供调试使用。

### 3. 正确处理订阅状态
| 状态 | 含义 | 操作 |
|-------|---------|--------|
| `active` | 客户正在支付 | 授予访问权限 |
| `trialing` | 处于试用期 | 授予访问权限，并在试用期结束前提醒用户 |
| `past_due` | 支付失败 | 提供重试机会，并提醒用户 |
| `paused` | 用户暂停了订阅 | 限制访问权限，允许用户恢复订阅 |
| `canceled` | 订阅已取消 | 在订阅周期结束时撤销访问权限 |

### 4. 正确存储 Paddle 相关标识符
- `customer_id` (ctm_xxx) — 每位客户唯一的标识符 |
- `subscription_id` (sub_xxx) — 每个订阅唯一的标识符 |
- `transaction_id` (txn_xxx) — 每笔支付唯一的标识符 |
- `price_id` (pri_xxx) — 你的定价配置信息 |
- 将这些标识符与你的内部用户/订阅记录进行关联。

### 5. 使用 Paddle 的自动催款功能
- 在仪表板中启用 Paddle 的自动催款功能，以处理支付失败的情况。
- 该功能负责处理重试逻辑和与客户的沟通。
- 跟踪 `subscription.past_due` 事件，但优先让 Paddle 自动尝试催收。
- 仅在 `subscription.canceled` 时才采取进一步行动。

## 常见错误

- **硬编码价格 ID** → 应使用环境变量，因为价格可能在沙箱环境和生产环境中有所不同。
- **未经验证直接处理 Webhook 请求** → 这会带来安全风险，因为任何人都可以伪造事件。
- **忽略 `past_due` 状态** → 会导致用户在重试期间失去访问权限，影响用户体验。
- **未正确处理费用分摊** → 会导致用户在升级/降级订阅时产生费用混淆。
- **使用生产环境密钥进行测试** → 会导致实际收费，引发客户投诉和退款问题。

## 外部接口

| 接口 | 发送的数据 | 用途 |
|----------|-----------|---------|
| https://api.paddle.com | 客户数据和订阅信息 | 用于处理支付 |
| https://sandbox-api.paddle.com | 测试用客户数据 | 用于沙箱环境测试 |

**注意：** 不会向外部发送任何其他数据。

## 安全与隐私

**会离开您系统的数据：**
- 客户的电子邮件和姓名会被发送给 Paddle 用于计费。
- 支付金额和订阅详情。
- IP 地址用于税务计算。

**保留在本地的数据：**
- API 密钥存储在环境变量中。
- Webhook 密钥永远不会被记录到日志中。
- 内部用户信息仅限于系统内部使用。

**本技能不涉及以下操作：**
- 存储信用卡号码（Paddle 负责处理 PCI 合规性相关事宜）。
- 直接访问支付方式的相关信息。
- 与 Paddle 以外的第三方共享客户数据。

## 信任问题

使用本技能意味着客户和支付数据将会被发送给 Paddle。只有在您信任 Paddle 并愿意将其用于计费处理的情况下，才应安装该技能。

## 相关技能

如果用户确认需要，可以使用以下命令进行安装：
- `clawhub install billing` — 用于处理通用计费逻辑。
- `clawhub install payments` — 用于处理支付流程。
- `clawhub install subscriptions` — 用于管理订阅信息。

## 反馈

- 如果觉得本技能有用，请给它打星（`clawhub star paddle`）。
- 为了获取最新信息，请使用 `clawhub sync` 命令保持同步。