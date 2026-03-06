---
name: stripe-webhook-replay-lab
description: 将经过签名的Stripe Webhook数据包重放到本地或测试（staging）端点，以实现幂等性（idempotency）和便于进行重试调试（retry debugging）。
version: 1.0.0
metadata: {"openclaw":{"requires":{"bins":["bash","curl","openssl","python3"]}}}
---
# Stripe Webhook 重放实验室

使用此技能可以将同一个已签名的 Stripe Webhook 事件多次发送到您的端点，以验证其幂等性（即多次发送相同事件不会产生不同的结果）。

## 该技能的功能：
- 从 JSON 文件或内联环境变量中加载 Stripe 事件数据。
- 使用您的 Webhook 密钥（`whsec_...`）生成有效的 `Stripe-Signature` 标头。
- 重复发送相同的事件数据 N 次，以模拟重复发送或重试的情况。
- 打印每次尝试的 HTTP 状态码和延迟时间，并提供成功/失败的总结。

## 输入参数：
- **必填参数：**
  - `STRIPE_WEBHOOK_URL`（目标端点地址）
  - `STRIPE_WEBHOOK_SECRET`（用于验证签名的 Stripe 端点密钥）

- **事件数据来源（请选择一个）：**
  - `STRIPE_EVENT_PATH`（默认值：`fixtures/sample-checkout-session-completed.json`）
  - `STRIPE_EVENT_JSON`（内联 JSON 数据；会覆盖 `STRIPE_EVENT_PATH` 的设置）

- **可选参数：**
  - `REPLAY_COUNT`（重放次数；默认值：`2`）
  - `REPLAY_DELAY_SECONDS`（每次重放之间的延迟时间；默认值：`0`）
  - `REQUEST_TIMEOUT_SECONDS`（请求超时时间；默认值：`15`）
  - `ACCEPT_HTTP_CODES`（接受为成功的 HTTP 状态码；默认值为空，表示接受所有 2xx 状态码）

## 运行方式：
```bash
STRIPE_WEBHOOK_URL=http://localhost:8000/webhooks/stripe \
STRIPE_WEBHOOK_SECRET=whsec_test_123 \
bash scripts/replay-stripe-webhook.sh
```

**示例：** 强制执行五次带有短暂延迟的重复发送：

```bash
STRIPE_WEBHOOK_URL=http://localhost:8000/webhooks/stripe \
STRIPE_WEBHOOK_SECRET=whsec_test_123 \
REPLAY_COUNT=5 \
REPLAY_DELAY_SECONDS=0.2 \
bash scripts/replay-stripe-webhook.sh
```

**示例：** 使用内联 JSON 数据发送事件：

```bash
STRIPE_WEBHOOK_URL=http://localhost:8000/webhooks/stripe \
STRIPE_WEBHOOK_SECRET=whsec_test_123 \
STRIPE_EVENT_JSON='{"id":"evt_test","type":"checkout.session.completed","object":"event","data":{"object":{"id":"cs_test"}}}' \
bash scripts/replay-stripe-webhook.sh
```

## 输出结果：
- 如果事件数据可用，会打印事件 ID 和类型。
- 会记录每次重试的 HTTP 状态码及耗时。
- 如果所有尝试都满足成功条件，则程序以 `0` 退出。
- 如果有任何尝试失败或输入参数无效，则程序以 `1` 退出。