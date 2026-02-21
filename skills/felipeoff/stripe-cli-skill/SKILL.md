---
name: stripe-cli
description: Stripe CLI（命令行接口）支持多种操作，适用于本地开发、Webhook测试、基于测试用例的事件模拟、API检查以及沙箱环境中的资源管理。这些功能包括：安装或验证Stripe CLI、登录、转发Webhook事件（`stripe listen --forward-to`）、触发测试事件（`stripe trigger`）、重放/重新发送事件、查看请求日志，以及在Stripe沙箱环境中进行安全的订阅/结账调试。
---
# Stripe CLI

## 概述

使用此技能可以安全且可重复地运行Stripe CLI工作流程，适用于本地和测试环境。

默认的安全策略为：**先使用沙箱环境（sandbox-first），最小权限原则，禁止泄露任何敏感信息，禁止在实时模式下执行破坏性操作**。

## 快速入门

```bash
# check install
stripe version

# authenticate (browser flow)
stripe login

# verify account context
stripe config --list
```

如果在持续集成（CI）或本地自动化环境中使用API密钥进行身份验证，请参考以下代码示例：

```bash
export STRIPE_API_KEY=sk_test_...
stripe customers list --limit 3
```

## 工作流程决策树

1. **需要在本地上调试接收到的Webhook事件吗？**
   - 使用命令：`stripe listen --forward-to ...`
   - 详情请参阅：`references/workflows.md` → Webhook本地循环（Webhook Local Loop）

2. **需要快速测试某些事件（如结账、订阅、发票等）吗？**
   - 使用命令：`stripe trigger ...` 或 `stripe fixtures ...`
   - 详情请参阅：`references/workflows.md` → 触发器与测试用例（Trigger & Fixtures）

3. **需要检查API的行为或错误吗？**
   - 使用命令：`stripe logs tail`、`stripe events list`、`stripe events resend`
   - 详情请参阅：`references/commands.md`

4. **需要查看计划变更或费用分摊的相关信息吗？**
   - 可通过CLI直接调用API（例如：`stripe subscriptions update ...`、`stripe invoices create_preview ...`）
   - 请务必先在测试模式下进行操作。

## 安全默认设置（强制要求）

- 建议使用**测试密钥**（如 `sk_test_...`）和沙箱账户环境。
- 绝不要在日志或代码提交中显示完整的敏感信息。
- 除非仅在本地环境中使用，否则请避免使用 `--skip-verify` 选项。
- 在执行敏感操作之前，请确认账户上下文：
  - `stripe config --list`
  - `stripe whoami`（如果可用）
- 注意：`stripe trigger` 命令会在沙箱环境中创建对象并产生副作用。

## 常见任务

### 1) 将Webhook事件转发到本地应用程序

```bash
stripe listen --forward-to localhost:4242/webhook
```

根据需要过滤事件：

```bash
stripe listen \
  --events checkout.session.completed,invoice.paid,invoice.payment_failed,customer.subscription.updated \
  --forward-to localhost:4242/webhook
```

从仪表板上的Webhook端点加载事件配置：

```bash
stripe listen --load-from-webhooks-api --forward-to localhost:4242
```

### 2) 触发测试事件

```bash
stripe trigger checkout.session.completed
stripe trigger invoice.paid
stripe trigger customer.subscription.updated
```

对于复杂的场景，建议使用测试用例（fixtures）来模拟实际操作：

```bash
stripe fixtures path/to/fixture.json
```

### 3) 查看日志并检查事件

```bash
stripe logs tail
stripe events list --limit 10
stripe events resend evt_... --webhook-endpoint=we_...
```

### 4) 测试API版本

```bash
stripe products create --name "Test Product" --latest
stripe products create --name "Pinned Version" --stripe-version 2026-01-28.clover
```

## 安全防护措施

在运行可能修改系统状态的命令之前，请确保：
- 确保处于沙箱或测试环境中。
- 使用正确的账户和项目信息。
- 避免意外地针对生产环境的Webhook端点。
- 确保shell历史记录和文档中不包含任何明文的敏感信息。

如果用户请求在实时模式下执行操作，请要求用户明确确认，并向其解释可能产生的影响范围。

## 配置好的脚本

- `scripts/stripe-dev-listen.sh`：以更安全的默认设置启动 `stripe listen` 命令，并对事件进行过滤。
- `scripts/stripe-sanitize.sh`：从日志和文件中删除API密钥和Webhook密钥，以便共享。

## 参考资料

- `references/workflows.md`：适用于生产环境的Stripe CLI工作流程指南。
- `references/commands.md`：高价值命令参考手册。
- `references/security.md`：社区使用的安全与合规性检查清单。