---
name: send-email
description: >
  **使用场景：**  
  在通过 Resend API 发送交易相关邮件（欢迎邮件、订单确认邮件、密码重置邮件、收据）以及通知邮件或批量邮件时使用。
inputs:
    - name: RESEND_API_KEY
      description: Resend API key for sending emails. Get yours at https://resend.com/api-keys
      required: true
    - name: RESEND_WEBHOOK_SECRET
      description: Webhook signing secret for verifying delivery event payloads (bounced, delivered, opened). Found in the Resend dashboard under Webhooks.
      required: false
---
# 使用 Resend 功能发送电子邮件

## 概述

Resend 提供了两个用于发送电子邮件的接口：

| 方法 | 接口 | 使用场景 |
|----------|----------|----------|
| **单次发送** | `POST /emails` | 单个交易性邮件、带附件的邮件、定时发送的邮件 |
| **批量发送** | `POST /emails/batch` | 一次请求中发送多封不同的邮件（最多 100 封） |

**在以下情况下选择批量发送：**
- 同时发送 2 封或更多不同的邮件 |
- 需要减少 API 调用次数（默认每秒请求限制为 2 次） |
- 不需要附件或定时发送 |

**在以下情况下选择单次发送：**
- 只发送一封邮件 |
- 需要附件 |
- 需要定时发送邮件 |
- 不同收件人有不同的发送时间要求 |

## 快速入门

1. 从配置文件（`package.json`、`requirements.txt`、`go.mod` 等）中检测项目使用的语言 |
2. 安装 SDK（推荐）或使用 cURL - 请参阅 [references/installation.md](references/installation.md) |
3. 根据上述决策矩阵选择单次发送或批量发送 |
4. 实施最佳实践 - 例如使用幂等性键、错误处理和重试机制 |

## 最佳实践（生产环境必备）

在生产环境中发送电子邮件时，请务必遵循这些最佳实践。详细实现请参阅 [references/best-practices.md](references/best-practices.md)。

### 幂等性键

在重试失败请求时，防止发送重复邮件。

| 关键信息 | |
|-----------|---|
| **格式（单次发送）** | `<事件类型>/<实体ID>`（例如：`welcome-email/user-123`） |
| **格式（批量发送）** | `batch-<事件类型>/<批次ID>`（例如：`batch-orders/batch-456`） |
| **有效期** | 24 小时 |
| **最大长度** | 256 个字符 |
| **重复的请求数据** | 会返回原始响应，不会重新发送 |
| **不同的请求数据** | 会返回 409 错误 |

### 错误处理

| 错误代码 | 处理方式 |
|------|--------|
| 400, 422 | 修复请求参数，不要重试 |
| 401, 403 | 检查 API 密钥/验证域名，不要重试 |
| 409 | 幂等性冲突 - 使用新的键或修复请求数据 |
| 429 | 超过请求限制 - 使用指数级退避策略重试（默认每秒请求限制为 2 次） |
| 500 | 服务器错误 - 使用指数级退避策略重试 |

### 重试策略

- **退避策略**：指数级退避（1 秒、2 秒、4 秒……） |
- **最大重试次数**：大多数情况下为 3-5 次 |
- **仅重试以下情况**：429（请求限制）和 500（服务器错误） |
- **重试时务必使用**：幂等性键

## 单次发送邮件

**接口：`POST /emails`（建议使用 SDK，而非 cURL）**

### 必需参数

| 参数 | 类型 | 说明 |
|-----------|------|-------------|
| `from` | 字符串 | 发件人地址。格式：`"Name <email@domain.com>"` |
| `to` | 字符串数组 | 收件人地址（最多 50 个） |
| `subject` | 字符串 | 邮件主题行 |
| `html` 或 `text` | 字符串 | 邮件正文内容 |

### 可选参数

| 参数 | 类型 | 说明 |
|-----------|------|-------------|
| `cc` | 字符串数组 | 抄送收件人地址 |
| `bcc` | 字符串数组 | 密件抄送收件人地址 |
| `reply_to`* | 字符串数组 | 回复收件人地址 |
| `scheduled_at`* | 字符串 | 定时发送时间（ISO 8601 格式） |
| `attachments` | 数组 | 文件附件（总大小不超过 40MB） |
| `tags` | 数组 | 用于追踪的键值对（详见 [Tags](#tags)） |
| `headers` | 对象 | 自定义头部信息 |

*参数名称可能因 SDK 而异（例如，在 Node.js 中为 `replyTo`，在 Python 中为 `reply_to`）。

### 最小示例（Node.js）

```typescript
import { Resend } from 'resend';

const resend = new Resend(process.env.RESEND_API_KEY);

const { data, error } = await resend.emails.send(
  {
    from: 'Acme <onboarding@resend.dev>',
    to: ['delivered@resend.dev'],
    subject: 'Hello World',
    html: '<p>Email body here</p>',
  },
  { idempotencyKey: `welcome-email/${userId}` }
);

if (error) {
  console.error('Failed:', error.message);
  return;
}
console.log('Sent:', data.id);
```

有关包含错误处理和重试逻辑的所有 SDK 实现，请参阅 [references/single-email-examples.md](references/single-email-examples.md)。

## 批量发送邮件

**接口：`POST /emails/batch`（建议使用 SDK，而非 cURL）**

### 限制

- **不支持附件** - 带附件的邮件请使用单次发送 |
- **不支持定时发送** - 定时发送的邮件请使用单次发送 |
- **原子性**：如果其中一封邮件验证失败，整个批次都会失败 |
- **每次请求最多发送 100 封邮件** |
- **每封邮件最多 50 个收件人**

### 预验证

由于任何验证错误都会导致整个批次失败，因此在发送前请验证所有邮件：
- 检查必填字段（`from`、`to`、`subject`、`html`/`text`）
- 验证邮件格式 |
- 确保批次大小不超过 100 封

### 最小示例（Node.js）

```typescript
import { Resend } from 'resend';

const resend = new Resend(process.env.RESEND_API_KEY);

const { data, error } = await resend.batch.send(
  [
    {
      from: 'Acme <notifications@acme.com>',
      to: ['delivered@resend.dev'],
      subject: 'Order Shipped',
      html: '<p>Your order has shipped!</p>',
    },
    {
      from: 'Acme <notifications@acme.com>',
      to: ['delivered@resend.dev'],
      subject: 'Order Confirmed',
      html: '<p>Your order is confirmed!</p>',
    },
  ],
  { idempotencyKey: `batch-orders/${batchId}` }
);

if (error) {
  console.error('Batch failed:', error.message);
  return;
}
console.log('Sent:', data.map(e => e.id));
```

有关包含验证、错误处理和重试逻辑的所有 SDK 实现，请参阅 [references/batch-email-examples.md](references/batch-email-examples.md)。

## 大批量发送（100 封以上邮件）

对于超过 100 封邮件的发送，请分批处理：

1. **将邮件分成每批 100 封** |
2. **为每批使用唯一的幂等性键**：`<batch-prefix>/chunk-<index>` |
3. **并行发送各批邮件以提高吞吐量** |
4. **跟踪每批的发送结果**，以处理部分失败的情况 |

有关分批发送的完整实现，请参阅 [references/batch-email-examples.md](references/batch-email-examples.md)。

## 邮件送达率优化

遵循以下最佳实践以提高邮件送达率。

如需更多关于邮件送达率的帮助，请使用 `npx skills add resend/email-best-practices` 安装 `email-best-practices` 技能。

### 必需遵循的实践

| 实践 | 原因 |
|----------|-----|
| **有效的 SPF、DKIM、DMARC 记录** | 验证邮件真实性，防止垃圾邮件 |
| **链接与发送域名一致** | 如果从 `@acme.com` 发送邮件，链接应指向 `https://acme.com`；域名不匹配会触发垃圾邮件过滤器 |
| **提供纯文本版本** | 同时使用 `html` 和 `text` 参数以提高可访问性和送达率（Resend 会在未提供纯文本版本时自动生成） |
| **避免使用“no-reply”地址** | 使用真实地址（例如 `support@`）以提高信任度 |
| **保持邮件正文大小在 102KB 以下** | Gmail 会截断过长的邮件 |

### 推荐的实践

| 实践 | 原因 |
|----------|-----|
| **使用子域名** | 交易性邮件从 `notifications.acme.com` 发送，营销邮件从 `mail.acme.com` 发送 - 有助于维护邮件服务提供商的声誉 |
| **禁用交易性邮件的追踪** | 对于密码重置、确认邮件等敏感邮件，禁用打开/点击追踪 |

## 追踪（打开和点击）

追踪功能在 Resend 的控制面板中按域名级别配置，而不是针对单封邮件配置。

| 设置 | 功能 | 建议 |
|---------|--------------|----------------|
| **打开追踪** | 插入 1x1 的透明像素 | 对于交易性邮件请禁用此功能，否则会影响送达率 |
| **点击追踪** | 通过重定向链接来追踪点击行为 | 对于敏感邮件（如密码重置、安全提醒邮件）请禁用此功能 |

**何时启用追踪：**
- 需要跟踪用户互动情况的营销邮件 |
- 新闻通讯和公告邮件

**何时禁用追踪：**
- 交易性邮件（如确认邮件、密码重置邮件） |
- 敏感安全邮件 |
- 当优先考虑送达率时 |

**配置方法：** 控制面板 → 配置 → 点击/打开追踪

## Webhook（事件通知）

使用 Webhook 实时跟踪邮件送达状态。当事件发生时，Resend 会向您的接口发送 HTTP POST 请求。

| 事件 | 使用场景 |
|-------|-------------|
| `email.delivered` | 确认邮件成功送达 |
| `email.bounced` | 从邮件列表中移除用户 |
| `email.complained` | 用户投诉垃圾邮件 |
| `email.opened` / `email.clicked` | 跟踪用户互动情况（仅限营销邮件） |

**重要提示：** 必须验证 Webhook 签名。** 如果不验证，攻击者可能会向您的接口发送伪造的事件。

有关设置、签名验证代码和所有事件类型的详细信息，请参阅 [references/webhooks.md](references/webhooks.md)。

## 标签

标签是用于追踪和过滤邮件的键值对。

```typescript
tags: [
  { name: 'user_id', value: 'usr_123' },
  { name: 'email_type', value: 'welcome' },
  { name: 'plan', value: 'enterprise' }
]
```

**使用场景：**
- 将邮件与系统中的客户关联 |
- 按邮件类型分类（欢迎邮件、确认邮件、密码重置邮件） |
- 在 Resend 控制面板中过滤邮件 |
- 将 Webhook 事件与您的应用程序关联 |

**注意事项：** 标签名称和值只能包含 ASCII 字母、数字、下划线或短横线。每个标签的最大长度为 256 个字符。

## 模板

请使用预构建的模板，而不是在每次请求时都发送 HTML 内容。

```typescript
const { data, error } = await resend.emails.send({
  from: 'Acme <hello@acme.com>',
  to: ['delivered@resend.dev'],
  subject: 'Welcome!',
  template: {
    id: 'tmpl_abc123',
    variables: {
      USER_NAME: 'John',      // Case-sensitive!
      ORDER_TOTAL: '$99.00'
    }
  }
});
```

**重要提示：** 变量名称区分大小写，必须与模板编辑器中定义的名称完全匹配。例如，`USER_NAME` 不能与 `user_name` 混淆。

| 信息 | 详情 |
|------|--------|
| **每个模板最多可使用的变量数量** | 20 个 |
| **保留的变量名称** | `FIRST_NAME`、`LAST_NAME`、`EMAIL`、`RESEND_UNSUBSCRIBE_URL`、`contact`、`this` |
| **默认值** | 可选 - 如果未设置且变量缺失，发送将失败 |
| **不能与以下参数组合使用** | `html`、`text` 或 `react` |

模板必须在控制面板中**发布**后才能使用。未发布的模板将无法使用。

## 测试

**警告：** 切勿使用虚假地址进行测试。**

使用 `test@gmail.com`、`example@outlook.com` 或 `fake@yahoo.com` 等地址会导致以下问题：
- 邮件会被退回 |
- 损害您的发件人声誉（高退回率会触发垃圾邮件过滤器） |
- 您的域名可能会被列入黑名单（发送方声誉较低会导致此情况） |

### 安全的测试方法

| 方法 | 使用的地址 | 结果 |
|--------|---------|--------|
| **Delivered** | `delivered@resend.dev` | 模拟成功送达 |
| **Bounced** | `bounced@resend.dev` | 模拟邮件被退回 |
| **Complained** | `complained@resend.dev` | 模拟用户投诉垃圾邮件 |
| **您自己的电子邮件地址** | 您的实际地址 | 进行真实的送达测试 |

**开发环境：** 使用 `resend.dev` 测试地址来模拟不同场景，而不会影响您的声誉。 |
**测试环境：** 将邮件发送到您控制的真实地址（团队成员或测试账户）。

## 域名预热

新域名在开始发送邮件前，必须逐步增加发送量以建立良好的声誉。

**原因：** 新域名突然大量发送邮件会触发垃圾邮件过滤器。邮件服务提供商通常要求逐步增加发送量。

### 推荐的发送计划

**现有域名**

| 天数 | 每天发送的邮件数量 | 每小时发送的邮件数量 |
|-----|---------------------|---------------------|
| 1   | 最多 1,000 封邮件 | 每小时最多 100 封 |
| 2   | 最多 2,500 封邮件 | 每小时最多 300 封 |
| 3   | 最多 5,000 封邮件 | 每小时最多 600 封 |
| 4   | 最多 5,000 封邮件 | 每小时最多 800 封 |
| 5   | 最多 7,500 封邮件 | 每小时最多 1,000 封 |
| 6   | 最多 7,500 封邮件 | 每小时最多 1,500 封 |
| 7   | 最多 10,000 封邮件 | 每小时最多 2,000 封 |

**新域名**

| 天数 | 每天发送的邮件数量 | 每小时发送的邮件数量 |
|-----|---------------------|---------------------|
| 1   | 最多 150 封邮件 |                |
| 2   | 最多 250 封邮件 |                |
| 3   | 最多 400 封邮件 |                |
| 4   | 最多 700 封邮件 | 每小时最多 50 封 |
| 5   | 最多 1,000 封邮件 | 每小时最多 75 封 |
| 6   | 最多 1,500 封邮件 | 每小时最多 100 封 |
| 7   | 最多 2,000 封邮件 | 每小时最多 150 封 |

### 监控这些指标

| 指标 | 目标值 | 超过目标值时的处理方式 |
|--------|--------|-------------------|
| **退回率** | < 4% | 减慢发送速度，清理邮件列表 |
| **垃圾邮件投诉率** | < 0.08% | 减慢发送速度，检查邮件内容 |

**请勿使用第三方预热服务。** 请确保向真实且愿意接收邮件的用户发送相关内容。

## 抑制列表

Resend 会自动管理一个不应接收邮件的地址列表。

**地址会被添加到抑制列表的情况：**
- 邮件被退回（地址不存在） |
- 收件人将邮件标记为垃圾邮件 |
- 您通过控制面板手动将地址添加到列表中 |

**后果：** Resend 会停止向被抑制的地址发送邮件。此时会触发 `email.suppressed` Webhook 事件。

**重要性：** 继续向被退回或投诉的地址发送邮件会损害您的声誉。抑制列表可以自动保护您的邮件服务提供商的声誉。**

**管理方式：** 在 Resend 控制面板的“Suppressions”部分查看和管理被抑制的地址。

## 常见错误及解决方法

| 错误 | 解决方法 |
|---------|-----|
| 重试时未使用幂等性键 | 必须使用幂等性键，以防止重复发送 |
| 对带附件的邮件使用批量发送 | 批量发送不支持附件，请使用单次发送 |
| 发送前未验证邮件 | 首先验证所有邮件，因为一封无效邮件会导致整个批次失败 |
| 重试 400/422 错误 | 这些是验证错误，请修复请求，不要重试 |
| 使用相同的幂等性键但发送不同的内容 | 会导致 409 错误，请为每封邮件使用唯一的键 |
| 为交易性邮件启用追踪 | 对于密码重置、确认邮件等邮件，禁用打开/点击追踪，以免影响送达率 |
| 使用“no-reply”作为发件人地址 | 使用真实的地址（如 `support@`）以提高信任度 |
| 未验证 Webhook 签名 | 必须验证签名，否则攻击者可能会向您的接口发送伪造事件 |
| 使用虚假地址进行测试 | 使用 `delivered@resend.dev` 进行测试，避免使用虚假地址导致问题 |

## 注意事项

- `from` 地址必须使用经过验证的域名 |
- 如果发件人地址无法接收回复，请将 `reply_to` 参数设置为有效的地址 |
- 将 API 密钥存储在 `RESEND_API_KEY` 环境变量中 |
- Node.js SDK 支持用于 React 邮件组件的 `react` 参数 |
- Resend 会在响应中返回 `error`、`data`、`headers` |
- 成功时，数据返回 `{ id: "email-id" }`（单次发送）或 ID 数组（批量发送） |
- 对于大规模营销活动，请使用 Resend Broadcast 功能。