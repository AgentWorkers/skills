---
name: webhook-gen
description: 使用 AI 生成具有重试逻辑的 Webhook 处理程序。在集成 Stripe、GitHub 或任何 Webhook 提供商时可以使用该功能。
---

# Webhook 生成器

本工具用于生成处理 Webhook 请求的函数。生成的函数支持签名验证、重试逻辑以及完善的错误处理机制，适用于 Stripe、GitHub、Twilio 等常见的 Webhook 提供商。

**只需一个命令，无需任何配置，即可立即使用。**

## 快速入门

```bash
npx ai-webhook "stripe payment succeeded"
```

## 功能介绍

- 生成完整的 Webhook 处理函数
- 支持对常见提供商的签名验证
- 实现幂等性检查，防止重复处理请求
- 采用安全的重试机制，并返回相应的状态码
- 支持处理来自 Stripe、GitHub、Shopify 等平台的 Webhook 请求

## 使用示例

```bash
# Stripe payment webhook
npx ai-webhook "stripe checkout.session.completed"

# GitHub push events
npx ai-webhook "github push event to trigger deployment"

# Generic webhook with retry
npx ai-webhook "order created webhook with idempotency" 

# Specify provider explicitly
npx ai-webhook "new subscriber notification" --provider convertkit

# TypeScript output
npx ai-webhook "invoice paid" --typescript
```

## 最佳实践

- **始终验证签名**：切勿直接信任原始的 Webhook 数据
- **快速返回 200 状态码**：异步处理请求，避免让服务提供商等待过久
- **处理重复请求**：Webhook 通常会重发，因此处理函数应具备幂等性
- **记录所有操作**：没有日志将难以排查 Webhook 相关问题

## 适用场景

- 集成 Stripe 或 Paddle 等支付服务
- 通过 Webhook 实现 GitHub Actions 的自动化流程
- 构建由外部服务触发的通知系统
- 任何需要发送 Webhook 的第三方集成场景

## 本工具属于 LXGIC 开发工具包的一部分

LXGIC Studios 提供了 110 多款免费开发工具，本工具是其中之一。免费版本无使用限制、无需注册，也不需要 API 密钥，只需使用 `npx` 命令即可运行。

**了解更多：**
- GitHub: https://github.com/LXGIC-Studios
- Twitter: https://x.com/lxgicstudios
- Substack: https://lxgicstudios.substack.com
- 官网: https://lxgic.dev

## 系统要求

无需安装任何软件，只需使用 `npx` 命令即可运行。建议使用 Node.js 18 及更高版本。

```bash
npx ai-webhook --help
```

## 工作原理

该工具会根据用户提供的描述，自动生成相应的 Webhook 处理函数，包括签名验证、事件解析和响应代码。通过人工智能技术，确保处理函数遵循最佳实践，从而保证系统的可靠性和安全性。

## 许可协议

采用 MIT 许可协议，永久免费使用，可自由支配。