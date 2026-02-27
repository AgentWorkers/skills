---
name: kash
description: 通过您的代理的Kash钱包来支付API、工具和服务的费用。如果费用低于5美元，系统会自动完成支付；如果费用超过5美元，则需要用户明确表示同意（通过系统确认）。支付时需要使用从kash.dev获取的KASH_KEY和KASH_AGENT_ID。
homepage: https://kash.dev
user-invocable: true
metadata: {"openclaw": {"emoji": "💳", "primaryEnv": "KASH_KEY", "requires": {"env": ["KASH_KEY", "KASH_AGENT_ID"]}, "homepage": "https://kash.dev"}}
---
# Kash支付技能

该技能允许您的OpenClaw代理访问Kash钱包，从而在您配置的预算范围内自主支付外部服务费用。

## 安全模型

- 必须提供`KASH_KEY`和`KASH_AGENT_ID`。如果缺少其中任何一个，技能在加载时将失败，而不会默默地继续执行。
- `KASH_API_URL`在启动时会与允许列表（仅限api.kash.dev和localhost）进行验证。将其设置为其他域名会被立即拒绝，以防止`KASH_KEY`被发送到不受信任的服务器。
- `KASH_BUDGET`在代码中被作为会话限制来执行。这不仅仅是一个指导原则——每次调用前，支出函数都会检查这一限制。
- 当支出金额超过`KASH_SPEND_CONFIRMATION_THRESHOLD`（默认值为5.00美元）时，需要设置`confirmed=true`，并且代理只有在当前对话中收到用户的明确同意后才能设置该值。
- 预算限制在两个层面进行验证：本地（`KASH_BUDGET`）和服务器端（Kash仪表板预算）。两者都必须通过才能完成支付。

## 提供的工具

### `kash_spend`

在发起付费API调用之前，从Kash代理钱包中支出费用。

参数：
- `amount`（数字，必填）——支出金额（以美元为单位）
- `description`（字符串，必填）——支出用途
- `merchant`（字符串，可选）——服务名称
- `confirmed`（布尔值，可选）——仅在支出金额超过阈值时，且用户明确同意后设置为true

返回值：
- `OK. 已花费$X用于“...”`——支出成功
- `CONFIRMATION_REQUIRED: ...`——请求用户确认，然后重新尝试并设置`confirmed=true`
- `LOCAL_BUDGET_EXCEEDED: ...`——达到本地会话限制，停止操作并通知用户
- `BUDGET_EXCEEDED: ...`——达到服务器端预算限制，停止操作并通知用户
- `AGENT_PAUSED: ...`——代理在Kash仪表板中被用户暂停
- `UNAUTHORIZED: ...`——`KASH_KEY`无效或已过期
- `ERROR: ...`——发生意外错误

### `kash_balance`

检查剩余预算（不进行任何支出）。返回服务器端余额和本地会话限制。

## 何时使用此技能

- 在发起任何付费外部调用之前（如API调用、网络搜索、数据购买或按请求收费的服务）使用`kash_spend`。务必在付费操作之前调用该技能，切勿在之后调用。
- 在开始需要多次付费操作的多步骤任务之前使用`kash_balance`。

## 代理必须遵守的规则

1. 必须在发起付费调用之前调用`kash_spend`，切勿在之后调用。
2. 如果返回`CONFIRMATION_REQUIRED`，请请求用户的明确同意；切勿绕过此步骤。
3. 如果返回`BUDGET_EXCEEDED`或`LOCAL_BUDGET_EXCEEDED`，立即停止任务并通知用户。
4. 未经当前对话中用户的确认，切勿设置`confirmed=true`。
5. 绝不允许绕过预算限制。
6. 如果`kash_spend`返回任何错误，请勿继续进行付费调用。

# 使用Kash支付技能

使用此技能可以从您的Kash代理钱包支付外部API、工具和服务的费用。

## 设置

在`~/.openclaw/openclaw.json`中进行配置：

```json
{
  "skills": {
    "entries": {
      "kash": {
        "enabled": true,
        "apiKey": "ksh_live_...",
        "env": {
          "KASH_KEY": "ksh_live_...",
          "KASH_AGENT_ID": "your-agent-id",
          "KASH_BUDGET": "50",
          "KASH_SPEND_CONFIRMATION_THRESHOLD": "5.00"
        }
      }
    }
  }
}
```

在注册代理后，从kash.dev/dashboard/agents获取`KASH_KEY`和`KASH_AGENT_ID`。

## 工具

### `kash_spend`

在发起任何付费API调用或服务之前调用此函数。切勿在之后调用。

参数：
- `amount`（数字，必填）——支出金额（以美元为单位）
- `description`（字符串，必填）——支出用途
- `merchant`（字符串，可选）——服务名称
- `confirmed`（布尔值，可选）——仅在支出金额超过阈值且用户明确同意后设置为true

返回值：
- `OK. 已花费$X用于“...”`——允许继续进行付费调用
- `CONFIRMATION_REQUIRED: ...`——请求用户确认，然后重新尝试并设置`confirmed=true`
- `LOCAL_BUDGET_EXCEEDED: ...`——停止操作，并提示用户前往kash.dev充值
- `BUDGET_EXCEEDED: ...`——停止操作，并提示用户前往kash.dev充值
- `AGENT_PAUSED: ...`——提示用户前往kash.dev/dashboard/agents恢复代理
- `UNAUTHORIZED: ...`——提示用户的`KASH_KEY`可能无效
- `ERROR: ...`——无法继续进行付费调用

### `kash_balance`

检查剩余预算。在开始需要多次付费操作的多步骤任务之前使用此函数。

无需参数。

## 规则

1. 必须在发起付费调用之前调用`kash_spend`，切勿在之后调用。
2. 如果返回`CONFIRMATION_REQUIRED`，请请求用户的明确同意，然后再尝试。
3. 如果返回`BUDGET_EXCEEDED`或`LOCAL_BUDGET_EXCEEDED`，立即停止操作并通知用户。
4. 未经当前对话中用户的确认，切勿设置`confirmed=true`。
5. 绝不允许绕过预算限制。
6. 严禁在任何消息或日志中泄露`KASH_KEY`的值。