---
name: send-email
description: 通过 SendGrid v3 的 Mail Send API 发送交易性电子邮件和通知。该 API 支持发送简单的电子邮件、HTML/文本内容、附件、抄送/密送（CC/BCC）、动态模板以及个性化内容。适用于发送欢迎邮件、密码重置邮件、收据、通知等程序化生成的电子邮件。相关事件触发条件包括：发送电子邮件、交易性电子邮件、SendGrid 发送操作、电子邮件通知、欢迎邮件、密码重置邮件以及使用动态模板的情况。
---

# 使用 SendGrid 发送电子邮件

## 概述

SendGrid 提供了一个统一的 **发送邮件** 端点，支持通过 v3 API 发送电子邮件。Node.js 开发者推荐使用其官方 SDK（`@sendgrid/mail`）进行集成。

**适用场景：**
- 发送交易类邮件（欢迎邮件、密码重置邮件、收据等）
- 发送简单通知
- 需要发送纯文本或 HTML 格式的邮件，并可添加附件
- 需要使用动态模板来生成个性化内容

## 快速入门

### 先测试配置
```bash
# Validate API key and send test email
../scripts/send-test-email.sh recipient@example.com
```

**然后进行集成：**
1. **确定项目使用的语言**（通过 `package.json`、`requirements.txt`、`go.mod` 等文件判断）
2. **安装 SDK**（推荐方式）或使用 cURL（详见 [references/installation.md]）
3. **准备邮件内容**，包括 `from`（发件人邮箱）、`to`（收件人邮箱）、`subject`（邮件主题）以及 `text`（邮件正文）或 `html`（HTML 内容）
4. **发送邮件并处理可能出现的错误**（对于 429 或 5xx 状态码的错误，应进行重试）

## 必需参数

| 参数 | 类型 | 说明 |
|------|------|-------------|
| `from` | 字符串 | 发件人邮箱（必须经过验证） |
| `to` | 字符串或字符串数组 | 收件人邮箱 |
| `subject` | 字符串 | 邮件主题 |
| `text` 或 `html` | 字符串 | 邮件正文内容 |

## 可选参数

| 参数 | 类型 | 说明 |
|------|------|-------------|
| `cc` | 字符串或字符串数组 | 抄送收件人 |
| `bcc` | 字符串或字符串数组 | 密送收件人 |
| `reply_to` | 字符串 | 回复邮箱 |
| `attachments` | 数组 | 基于 Base64 编码的附件 |
| `template_id` | 字符串 | 动态模板 ID（如果使用模板） |
| `dynamic_template_data` | 对象 | 模板数据（如果使用模板） |

## 最小示例（Node.js 代码）
```ts
import sgMail from '@sendgrid/mail';

sgMail.setApiKey(process.env.SENDGRID_API_KEY!);

await sgMail.send({
  from: 'Support <support@winkintel.com>',
  to: 'vince@winkintel.com',
  subject: 'Hello from SendGrid',
  text: 'This is a test email.',
  html: '<p>This is a test email.</p>',
});
```

## 模板（动态模板）

如果使用 SendGrid 的动态模板功能，请提供 `template_id` 和 `dynamic_template_data`，而不是 `html` 或 `text`。

```ts
await sgMail.send({
  from: 'Support <support@winkintel.com>',
  to: 'vince@winkintel.com',
  templateId: 'd-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx',
  dynamicTemplateData: { first_name: 'Vince' },
});
```

## 选择：使用纯文本邮件还是动态模板？

**使用纯文本邮件的情况：**
- 需要发送快速、简单的邮件
- 内容每次发送都会变化
- 不需要重复使用相同的设计

**使用动态模板的情况：**
- 需要在多封邮件中保持设计一致性
- 需要替换变量内容（如姓名、日期等）
- 非技术团队负责编写邮件内容
- 需要对邮件设计进行 A/B 测试

## 常见问题及解决方法

- **“401 Unauthorized”**：API 密钥无效或缺失
  - 检查 `SENDGRID_API_KEY` 环境变量是否设置正确
  - 确保密钥具有发送邮件的权限

- **“403 Forbidden”**：发件人邮箱未经过验证
  - 登录 SendGrid 控制台 → 设置 → 发件人认证
  - 确认发件人邮箱是否已通过验证

- **“429 Too Many Requests”**：请求次数超过限制
  - 实施指数级重试策略（每 1 秒、2 秒、4 秒后重试一次）
  - 考虑升级 SendGrid 的使用计划

- **“500/503 Service Errors”**：SendGrid 服务暂时出现问题
  - 使用指数级重试策略进行重试
  - 查看 SendGrid 的状态页面以获取更多信息

- **邮件无法送达**：
  - 检查收件人的垃圾邮件文件夹
  - 确认发件人域名的 SPF/DKIM 认证是否通过
  - 同时使用 `text` 和 `html` 格式以提高邮件送达率
  - 避免在邮件主题或正文中使用可能触发垃圾邮件过滤器的关键词

## 最佳实践（简要说明）：
- 尽可能同时设置 `text` 和 `html` 内容（以提高邮件送达率和可访问性）
- 仅在遇到 429 或 5xx 错误时进行重试，并采用指数级重试策略
- 使用经过验证的发件人邮箱；未经验证的域名可能导致邮件发送失败
- 避免使用虚假地址；使用自己控制的邮箱地址进行测试

更多详细信息，请参阅：
- [references/best-practices.md](references/best-practices.md)
- [references/single-email-examples.md](references/single-email-examples.md)

## 自动化脚本

- **快速测试脚本：**
  - `scripts/send-test-email.sh`：发送纯文本测试邮件（用于验证 API 密钥）
  - `scripts/send-html-email.sh`：发送 HTML 格式的邮件（例如新闻邮件、报告等）

使用方法请参见 [scripts/README.md](../scripts/README.md)。

## 相关技能

- **接收邮件回复**：
  - 可通过 `sendgrid-inbound` 模块利用 Inbound Parse Webhook 处理收到的邮件
  - 常见应用场景：自动回复系统、根据邮件内容创建支持工单等