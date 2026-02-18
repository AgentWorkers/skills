---
name: sparkbtcbot-proxy
description: 通过 HTTP API，使用 Spark Bitcoin L2 钱包代理来为 AI 代理提供服务。支持查询余额、发送付款、创建发票以及处理 L402 支付墙相关操作——所有这些操作均无需用户持有助记词（mnemonic）。当用户提到“Spark 代理”、“钱包 API”、“L402”、“代理支付”或“bearer token 身份验证”时，或者需要为代理提供安全的比特币功能时，均可使用该服务。
argument-hint: "[Optional: specify operation - balance, pay, invoice, l402, transfer, or setup]"
homepage: https://github.com/echennells/sparkbtcbot-proxy
source: https://github.com/echennells/sparkbtcbot-proxy
requires:
  env:
    - name: PROXY_URL
      description: HTTPS URL of your deployed sparkbtcbot-proxy instance (e.g., https://your-app.vercel.app)
      sensitive: false
    - name: PROXY_TOKEN
      description: Bearer token for proxy authentication. Create via POST /api/tokens with an admin token. Use least-privilege roles — prefer 'read-only', 'invoice', or 'pay-only' over 'admin' for agents.
      sensitive: true
model-invocation: autonomous
model-invocation-reason: This skill enables agents to call a wallet proxy API. Autonomous invocation is intentional for payment workflows, but the proxy enforces spending limits and role-based access. Always use least-privilege tokens and set per-tx/daily caps on the proxy side.
---
# Spark Bitcoin L2 代理——专为 AI 代理设计

您是使用 `sparkbtcbot-proxy` 的专家，这是一个无服务器的 HTTP API，它允许 AI 代理在无需暴露私钥的情况下访问 Spark Bitcoin L2 钱包。

## 为什么使用代理而不是直接使用 SDK

| 关注点 | 直接使用 SDK (sparkbtcbot-skill) | 使用代理 (本文档) |
|---------|-------------------------------|-------------------|
| 动机词的位置 | 由代理持有 | 由服务器持有 |
| 支出限制 | 无（由代理决定） | 每笔交易和每日限额 |
| 访问权限的撤销 | 将资金转移到新钱包 | 撤销承载令牌 |
| 基于角色的访问控制 | 无 | 有（管理员、开票、仅支付、只读） |
| 设置复杂性 | 使用 npm 安装并输入动机词 | 通过 HTTP 请求和承载令牌进行设置 |

**在以下情况下使用代理：**
- 您不信任代理完全控制钱包 |
- 您需要设置支出限制或审计日志 |
- 您希望在不转移资金的情况下撤销访问权限 |
- 多个代理共享一个钱包，但具有不同的权限 |

**在以下情况下直接使用 SDK：**
- 测试或开发 |
- 代理需要离线签名 |
- 您正在自己构建代理 |

## 在开始之前

1. **部署您自己的代理** — 请参阅 [sparkbtcbot-proxy](https://github.com/echennells/sparkbtcbot-proxy) 以获取设置说明。该代理运行在 Vercel 上（免费 tier 可用），并使用 Upstash Redis 作为缓存。

2. **仅使用 HTTPS** — 绝不要通过普通 HTTP 连接到代理。所有 Vercel 部署默认使用 HTTPS。

3. **创建最小权限的令牌** — 不要给代理管理员权限。使用最严格的角色：
   - `只读`：用于监控/仪表板代理 |
   `开票`：用于接收付款但不进行支付的代理 |
   `仅支付`：用于支付 L402 费用的代理，但不创建发票 |
   `管理员`：仅用于您的管理脚本 |

4. **设置支出限制** — 在创建令牌时配置 `maxTxSats` 和 `dailyBudgetSats`。代理会在服务器端强制执行这些限制。

5. **从小额金额开始测试** — 先从几百 sat 开始，直到您信任代理的行为。

6. **制定撤销计划** — 知道如何通过 `DELETE /api/tokens` 撤销令牌，以防代理被入侵。

## 令牌角色及其权限

| 角色 | 权限 |
|------|-------------|
| `管理员` | 完全访问：读取、创建发票、支付、转账、管理令牌 |
| `开票` | 读取 + 创建发票。无法支付或转账 |
| `仅支付` | 读取 + 支付发票和 L402 费用。无法创建发票或转账 |
| `只读` | 仅读取（余额、信息、交易、日志）。无法支付或创建发票 |

## 基础 URL

代理运行在 Vercel 上。您的基础 URL 将如下所示：
```
https://your-deployment.vercel.app
```

所有请求都需要身份验证：
```
Authorization: Bearer <your-token>
```

## API 参考

### 读取操作（任何角色）

#### 获取余额

```bash
curl -H "Authorization: Bearer $TOKEN" \
  "$PROXY_URL/api/balance"
```

响应：
```json
{
  "success": true,
  "data": {
    "balance": "50000",
    "tokenBalances": {
      "btkn1...": {
        "balance": "1000",
        "tokenMetadata": {
          "tokenName": "Example Token",
          "tokenTicker": "EXT",
          "decimals": 0
        }
      }
    }
  }
}
```

#### 获取钱包信息

```bash
curl -H "Authorization: Bearer $TOKEN" \
  "$PROXY_URL/api/info"
```

响应：
```json
{
  "success": true,
  "data": {
    "sparkAddress": "sp1p...",
    "identityPublicKey": "02abc..."
  }
}
```

#### 获取存款地址（L1 Bitcoin）

```bash
curl -H "Authorization: Bearer $TOKEN" \
  "$PROXY_URL/api/deposit-address"
```

响应：
```json
{
  "success": true,
  "data": {
    "address": "bc1p..."
  }
}
```

#### 获取交易历史

```bash
curl -H "Authorization: Bearer $TOKEN" \
  "$PROXY_URL/api/transactions?limit=10&offset=0"
```

#### 获取费用估算

```bash
curl -H "Authorization: Bearer $TOKEN" \
  "$PROXY_URL/api/fee-estimate?invoice=lnbc..."
```

响应：
```json
{
  "success": true,
  "data": {
    "feeSats": 5
  }
}
```

#### 获取活动日志

```bash
curl -H "Authorization: Bearer $TOKEN" \
  "$PROXY_URL/api/logs?limit=20"
```

### 开票操作（管理员或开票角色）

#### 创建 Lightning 发票（BOLT11）

```bash
curl -X POST -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"amountSats": 1000, "memo": "Payment for service", "expirySeconds": 3600}' \
  "$PROXY_URL/api/invoice/create"
```

响应：
```json
{
  "success": true,
  "data": {
    "encodedInvoice": "lnbc10u1p..."
  }
}
```

#### 创建 Spark 发票

```bash
curl -X POST -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"amount": 1000, "memo": "Spark payment"}' \
  "$PROXY_URL/api/invoice/spark"
```

### 支付操作（管理员或仅支付角色）

#### 支付 Lightning 发票

```bash
curl -X POST -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"invoice": "lnbc10u1p...", "maxFeeSats": 10}' \
  "$PROXY_URL/api/pay"
```

响应：
```json
{
  "success": true,
  "data": {
    "id": "payment-id-123",
    "status": "LIGHTNING_PAYMENT_SUCCEEDED",
    "paymentPreimage": "abc123..."
  }
}
```

#### 转账到 Spark 地址

```bash
curl -X POST -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"receiverSparkAddress": "sp1p...", "amountSats": 1000}' \
  "$PROXY_URL/api/transfer"
```

### L402 支付墙操作（管理员或仅支付角色）

L402 允许您使用 Lightning 支付 API 访问。代理会自动处理整个流程。

#### 支付 L402 并获取内容

```bash
curl -X POST -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"url": "https://lightningfaucet.com/api/l402/joke", "maxFeeSats": 50}' \
  "$PROXY_URL/api/l402"
```

响应（立即成功）：
```json
{
  "success": true,
  "data": {
    "status": 200,
    "paid": true,
    "priceSats": 21,
    "preimage": "be2ebe7c...",
    "data": {"setup": "Why do programmers...", "punchline": "..."}
  }
}
```

响应（缓存令牌被重用）：
```json
{
  "success": true,
  "data": {
    "status": 200,
    "paid": false,
    "cached": true,
    "data": {"setup": "...", "punchline": "..."}
  }
}
```

#### 预览 L402 费用（任何角色）

查看 L402 资源的费用，而无需支付：

```bash
curl -X POST -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"url": "https://lightningfaucet.com/api/l402/joke"}' \
  "$PROXY_URL/api/l402/preview"
```

响应：
```json
{
  "success": true,
  "data": {
    "requires_payment": true,
    "invoice_amount_sats": 21,
    "invoice": "lnbc210n1p...",
    "macaroon": "AgELbGlnaHRuaW5n..."
  }
}
```

#### 处理待处理的 L402 支付（非常重要）

Lightning 支付是异步的。如果预图像在约 7.5 秒内无法获取，代理会返回待处理状态：

```json
{
  "success": true,
  "data": {
    "status": "pending",
    "pendingId": "a1b2c3d4...",
    "message": "Payment sent but preimage not yet available. Poll GET /api/l402/status?id=<pendingId> to complete.",
    "priceSats": 21
  }
}
```

**您必须处理这种情况。** 支付已经发送——如果您不进行轮询，您将失去 sat 而无法获取内容。

轮询完成情况：

```bash
curl -H "Authorization: Bearer $TOKEN" \
  "$PROXY_URL/api/l402/status?id=a1b2c3d4..."
```

**推荐的重试逻辑：**

```javascript
async function fetchL402(proxyUrl, token, targetUrl, maxFeeSats = 50) {
  const response = await fetch(`${proxyUrl}/api/l402`, {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ url: targetUrl, maxFeeSats }),
  });

  const result = await response.json();

  if (result.data?.status === 'pending') {
    const pendingId = result.data.pendingId;
    for (let i = 0; i < 10; i++) {
      await new Promise(r => setTimeout(r, 3000));
      const statusResponse = await fetch(
        `${proxyUrl}/api/l402/status?id=${pendingId}`,
        { headers: { 'Authorization': `Bearer ${token}` } }
      );
      const statusResult = await statusResponse.json();
      if (statusResult.data?.status !== 'pending') {
        return statusResult;
      }
    }
    throw new Error('L402 payment timed out');
  }

  return result;
}
```

### 令牌管理（仅管理员角色）

#### 列出令牌

```bash
curl -H "Authorization: Bearer $TOKEN" \
  "$PROXY_URL/api/tokens"
```

#### 创建令牌

```bash
curl -X POST -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"role": "invoice", "label": "merchant-bot", "maxTxSats": 5000, "dailyBudgetSats": 50000}' \
  "$PROXY_URL/api/tokens"
```

响应中包含完整的令牌字符串——请保存它，因为它只显示一次：
```json
{
  "success": true,
  "data": {
    "token": "sbp_abc123...",
    "role": "invoice",
    "label": "merchant-bot"
  }
}
```

#### 撤销令牌

```bash
curl -X DELETE -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"token": "sbp_abc123..."}' \
  "$PROXY_URL/api/tokens"
```

## 完整的代理类（JavaScript）

```javascript
export class SparkProxyAgent {
  #baseUrl;
  #token;

  constructor(baseUrl, token) {
    this.#baseUrl = baseUrl.replace(/\/$/, '');
    this.#token = token;
  }

  async #request(method, path, body = null) {
    const options = {
      method,
      headers: {
        'Authorization': `Bearer ${this.#token}`,
        'Content-Type': 'application/json',
      },
    };
    if (body) {
      options.body = JSON.stringify(body);
    }

    const response = await fetch(`${this.#baseUrl}${path}`, options);
    const result = await response.json();

    if (!result.success) {
      throw new Error(result.error || 'Request failed');
    }
    return result.data;
  }

  async getBalance() {
    return this.#request('GET', '/api/balance');
  }

  async getInfo() {
    return this.#request('GET', '/api/info');
  }

  async getDepositAddress() {
    return this.#request('GET', '/api/deposit-address');
  }

  async getTransactions(limit = 10, offset = 0) {
    return this.#request('GET', `/api/transactions?limit=${limit}&offset=${offset}`);
  }

  async getFeeEstimate(invoice) {
    return this.#request('GET', `/api/fee-estimate?invoice=${encodeURIComponent(invoice)}`);
  }

  async createLightningInvoice(amountSats, memo = '', expirySeconds = 3600) {
    return this.#request('POST', '/api/invoice/create', {
      amountSats,
      memo,
      expirySeconds,
    });
  }

  async createSparkInvoice(amount, memo = '') {
    return this.#request('POST', '/api/invoice/spark', { amount, memo });
  }

  async payLightningInvoice(invoice, maxFeeSats = 10) {
    return this.#request('POST', '/api/pay', { invoice, maxFeeSats });
  }

  async transfer(receiverSparkAddress, amountSats) {
    return this.#request('POST', '/api/transfer', {
      receiverSparkAddress,
      amountSats,
    });
  }

  async previewL402(url) {
    return this.#request('POST', '/api/l402/preview', { url });
  }

  async fetchL402(url, options = {}) {
    const { method = 'GET', headers = {}, body, maxFeeSats = 50 } = options;

    const result = await this.#request('POST', '/api/l402', {
      url,
      method,
      headers,
      body,
      maxFeeSats,
    });

    // Handle pending status with polling
    if (result.status === 'pending') {
      const pendingId = result.pendingId;
      for (let i = 0; i < 10; i++) {
        await new Promise(r => setTimeout(r, 3000));
        const status = await this.#request('GET', `/api/l402/status?id=${pendingId}`);
        if (status.status !== 'pending') {
          return status;
        }
      }
      throw new Error('L402 payment timed out');
    }

    return result;
  }
}

// Usage
const agent = new SparkProxyAgent(
  process.env.PROXY_URL,
  process.env.PROXY_TOKEN
);

const balance = await agent.getBalance();
console.log('Balance:', balance.balance, 'sats');

const invoice = await agent.createLightningInvoice(1000, 'Test payment');
console.log('Invoice:', invoice.encodedInvoice);

const l402Result = await agent.fetchL402('https://lightningfaucet.com/api/l402/joke');
console.log('Joke:', l402Result.data);
```

## 代理的环境变量

```
PROXY_URL=https://your-deployment.vercel.app
PROXY_TOKEN=sbp_your_token_here
```

## 错误处理

所有错误都会返回以下响应：
```json
{
  "success": false,
  "error": "Error message here"
}
```

常见错误：
- **401 未经授权** — 无效或缺失的承载令牌 |
- **403 禁止访问** — 令牌角色不允许此操作 |
- **400 错误请求** — 缺少必需的参数 |
- **429 请求过多** — 超过了每日预算 |
- **500 内部服务器错误** — Spark SDK 或服务器错误

## 支出限制

代理执行两种类型的限制：

1. **全局限制**（来自环境变量）：
   - `MAX_TRANSACTION_SATS` — 每笔交易的限额 |
   - `DAILY_BUDGET_SATS` — 每日的总限额（在 UTC 午夜重置）

2. **每个令牌的限制**（在创建令牌时设置）：
   - `maxTxSats` — 该令牌的每笔交易限额 |
   - `dailyBudgetSats` — 该令牌的每日限额

应用全局限制和每个令牌限制中较低的一个。

## 安全注意事项

1. **将承载令牌视为密码** — 它们根据角色授予钱包访问权限 |
2. **使用最严格的角色** — 如果代理仅用于创建发票，使用 `开票` 角色 |
3. **设置每个令牌的支出限制** — 不要完全依赖全局限制 |
4. **监控日志** — 检查 `/api/logs` 以发现异常活动 |
5. **立即撤销被入侵的令牌** — 无需转移资金 |

## 资源

- 代理仓库：https://github.com/echennells/sparkbtcbot-proxy
- 直接使用 SDK：https://github.com/echennells/sparkbtcbot-skill
- Spark 文档：https://docs.spark.money
- L402 规范：https://docs.lightning.engineering/the-lightning-network/l402