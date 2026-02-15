---
name: bill-tracker
description: 访问账单追踪器的财务数据——包括即将到期的账单、账户余额以及 affordability checks（费用负担能力检查）。
metadata: {"openclaw":{"requires":{"env":["BILL_TRACKER_URL","BILL_TRACKER_SESSION_TOKEN"]},"primaryEnv":"BILL_TRACKER_SESSION_TOKEN","emoji":"💰"}}
---
# 账单追踪功能

当用户询问他们的账单、账户余额或是否能够负担某项费用时，可以使用 `bash` 工具来调用账单追踪 API。

## 所需环境

- `BILL TRACKER_URL`：基础 URL（例如：https://your-server.com 或 http://localhost:1337）
- `BILL TRACKER_SESSION_TOKEN`：用于身份验证的会话令牌（通过 POST /api/mcp/token 获取）

## 获取会话令牌

账单追踪系统使用“magic-link”认证方式（无需密码）。具体步骤如下：

1. 请求验证码（发送到用户的电子邮件）：
```bash
curl -s -X POST -H "Content-Type: application/json" \
  -d '{"email":"user@example.com"}' \
  "${BILL_TRACKER_URL}/api/mcp/request-code"
```

2. 用收到的验证码兑换会话令牌：
```bash
curl -s -X POST -H "Content-Type: application/json" \
  -d '{"code":"123456"}' \
  "${BILL_TRACKER_URL}/api/mcp/token"
```

将返回的 `sessionToken` 保存到 `BILL TRACKER_SESSION_TOKEN` 变量中。令牌的有效期较长，无需在每次请求时重新验证。（验证码在 10 分钟后失效。）

## API 端点

### 1. 即将发生的交易（即将到期的账单和收入）

```
POST ${BILL_TRACKER_URL}/api/mcp/upcoming-transactions
X-Parse-Session-Token: ${BILL_TRACKER_SESSION_TOKEN}
Body: { "days": 3 }
```

默认的 `days` 值为 3；如需查看更长时间内的交易记录，可修改该值（例如：`days=7`）。

### 2. 账户余额

```
POST ${BILL_TRACKER_URL}/api/mcp/account-balances
X-Parse-Session-Token: ${BILL_TRACKER_SESSION_TOKEN}
```

返回每个账户的名称、类型、余额以及总余额（现金减去债务）。

### 3. 我能负担得起 X 吗？

```
POST ${BILL_TRACKER_URL}/api/mcp/can-afford
X-Parse-Session-Token: ${BILL_TRACKER_SESSION_TOKEN}
Body: { "amount": 500, "horizonDays": 90 }
```

将 `500` 替换为所需的金额（单位：美元）。`horizonDays` 的默认值为 90。

API 会返回 `canAfford: true`（表示用户能够负担该费用，并附带可负担的日期），或 `canAfford: false`（并附带说明原因）。

## 调用方法

使用 `curl` 进行 POST 请求。在请求头中添加 `X-Parse-Session-Token`（或 `Authorization: Bearer $BILL TRACKER_SESSION_TOKEN`）以进行身份验证。令牌会自动识别用户身份，无需提供电子邮件或密码。解析 JSON 响应内容，并向用户清晰地展示结果。

**示例：**  
- 即将发生的交易：```bash
curl -s -X POST -H "X-Parse-Session-Token: $BILL_TRACKER_SESSION_TOKEN" -H "Content-Type: application/json" \
  -d '{"days": 3}' \
  "${BILL_TRACKER_URL}/api/mcp/upcoming-transactions"
```  
- 账户余额：```bash
curl -s -X POST -H "X-Parse-Session-Token: $BILL_TRACKER_SESSION_TOKEN" -H "Content-Type: application/json" \
  -d '{}' \
  "${BILL_TRACKER_URL}/api/mcp/account-balances"
```  
- 是否能负担得起某项费用：```bash
curl -s -X POST -H "X-Parse-Session-Token: $BILL_TRACKER_SESSION_TOKEN" -H "Content-Type: application/json" \
  -d '{"amount": 500}' \
  "${BILL_TRACKER_URL}/api/mcp/can-afford"
```