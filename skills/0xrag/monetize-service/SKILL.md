---
name: monetize-service
description: 构建并部署一个付费API，其他代理可以通过x402协议来使用该API。当您或用户希望从API中获利、赚钱、提供服务、向其他代理出售服务、对API接口收取费用、创建付费接口或设置付费服务时，可以使用这种方法。涵盖的内容包括：“通过提供API接口来赚钱”、“出售服务”、“利用数据盈利”以及“创建付费API”。
user-invocable: true
disable-model-invocation: false
allowed-tools: ["Bash(npx awal@latest status*)", "Bash(npx awal@latest address*)", "Bash(npx awal@latest x402 details *)", "Bash(npx awal@latest x402 pay *)", "Bash(npm *)", "Bash(node *)", "Bash(curl *)", "Bash(mkdir *)"]
---

# 构建 x402 支付服务器

创建一个 Express 服务器，使用 x402 支付协议来收取 API 访问费用（费用以 USDC 计算）。调用者需要按请求次数支付 USDC；无需账户、API 密钥或订阅服务。

## 工作原理

x402 是一种基于 HTTP 的支付协议。当客户端未支付费用就访问受保护的接口时，服务器会返回 HTTP 402 错误，并要求客户端完成支付。客户端完成支付后，服务器会继续处理请求并返回响应。

## 确保钱包已初始化并完成身份验证

```bash
npx awal@latest status
```

如果钱包尚未完成身份验证，请参考 `authenticate-wallet` 技能。

## 第一步：获取支付地址

运行以下命令以获取用于接收支付的钱包地址：

```bash
npx awal@latest address
```

将此地址作为 `payTo` 参数使用。

## 第二步：设置项目

```bash
mkdir x402-server && cd x402-server
npm init -y
npm install express x402-express
```

创建 `index.js` 文件：

```js
const express = require("express");
const { paymentMiddleware } = require("x402-express");

const app = express();
app.use(express.json());

const PAY_TO = "<address from step 1>";

// x402 payment middleware — protects routes below
const payment = paymentMiddleware(PAY_TO, {
  "GET /api/example": {
    price: "$0.01",
    network: "base",
    config: {
      description: "Description of what this endpoint returns",
    },
  },
});

// Protected endpoint
app.get("/api/example", payment, (req, res) => {
  res.json({ data: "This costs $0.01 per request" });
});

app.listen(3000, () => console.log("Server running on port 3000"));
```

## 第三步：运行服务器

```bash
node index.js
```

使用 `curl` 命令进行测试——你应该会收到一个包含支付要求的 402 错误响应：

```bash
curl -i http://localhost:3000/api/example
```

## API 参考

### `paymentMiddleware`（`payTo`, `routes`, `facilitator`）

创建一个 Express 中间件，用于强制执行 x402 支付流程：

| 参数            | 类型        | 描述                                                                                          |
| ------------------------- | ------------ | ----------------------------------------------------------------------------- |
| `payTo`         | 字符串       | 接收 USDC 支付的以太坊地址（格式为 0x...）                                                                                   |
| `routes`        | 对象        | 路由配置，将路由模式与支付配置关联起来                                                                                   |
| `facilitator`     | 可选对象     | 自定义支付处理服务（默认为 x402.org）                                                                                   |

### 路由配置

`routes` 对象中的每个键都是 `"METHOD /path"` 的形式。其值可以是价格字符串，也可以是配置对象：

```js
// Simple — just a price
{ "GET /api/data": "$0.05" }

// Full config
{
  "POST /api/query": {
    price: "$0.25",
    network: "base",
    config: {
      description: "Human-readable description of the endpoint",
      inputSchema: {
        bodyType: "json",
        bodyFields: {
          query: { type: "string", description: "The query to run" },
        },
      },
      outputSchema: {
        type: "object",
        properties: {
          result: { type: "string" },
        },
      },
    },
  },
}
```

### 路由配置字段

| 字段            | 类型        | 描述                                                                                          |
| ------------------------- | ------------ | ----------------------------------------------------------------------------- |
| `price`         | 字符串       | USDC 支付价格（例如：“$0.01”或“$1.00”）                                                                                   |
| `network`        | 字符串       | 区块链网络：“base”或“base-sepolia”                                                                                   |
| `config.description` | 可选字符串 | 向客户端显示的接口说明                                                                                         |
| `config.inputSchema` | 可选对象     | 预期的请求体结构                                                                                         |
| `config.outputSchema` | 可选对象     | 响应体结构                                                                                         |
| `config.maxTimeoutSeconds` | 可选数字     | 支付结算的最大超时时间（以秒为单位）                                                                                   |

### 支持的网络

| 网络            | 描述                                                                                          |
| ------------------------- | ----------------------------------------------------------------------------- |
| `base`         | Base 主网（使用真实的 USDC）                                                                                   |
| `base-sepolia`    | Base Sepolia 测试网（使用测试版的 USDC）                                                                                   |

## 多个端点的价格设置

```js
const payment = paymentMiddleware(PAY_TO, {
  "GET /api/cheap": { price: "$0.001", network: "base" },
  "GET /api/expensive": { price: "$1.00", network: "base" },
  "POST /api/query": { price: "$0.25", network: "base" },
});

app.get("/api/cheap", payment, (req, res) => { /* ... */ });
app.get("/api/expensive", payment, (req, res) => { /* ... */ });
app.post("/api/query", payment, (req, res) => { /* ... */ });
```

## 通配符路由

```js
const payment = paymentMiddleware(PAY_TO, {
  "GET /api/*": { price: "$0.05", network: "base" },
});

app.use(payment);
app.get("/api/users", (req, res) => { /* ... */ });
app.get("/api/posts", (req, res) => { /* ... */ });
```

## 健康检查（无需支付）

在应用支付中间件之前，先注册一些无需支付的测试端点：

```js
app.get("/health", (req, res) => res.json({ status: "ok" }));

// Payment middleware only applies to routes registered after it
app.get("/api/data", payment, (req, res) => { /* ... */ });
```

## 带请求体数据的 POST 请求

```js
const payment = paymentMiddleware(PAY_TO, {
  "POST /api/analyze": {
    price: "$0.10",
    network: "base",
    config: {
      description: "Analyze text sentiment",
      inputSchema: {
        bodyType: "json",
        bodyFields: {
          text: { type: "string", description: "Text to analyze" },
        },
      },
      outputSchema: {
        type: "object",
        properties: {
          sentiment: { type: "string" },
          score: { type: "number" },
        },
      },
    },
  },
});

app.post("/api/analyze", payment, (req, res) => {
  const { text } = req.body;
  // ... your logic
  res.json({ sentiment: "positive", score: 0.95 });
});
```

## 使用 CDP 支付处理服务（已认证）

在生产环境中，可以使用 Coinbase 提供的 CDP 支付处理服务（支持主网）：

```bash
npm install @coinbase/x402
```

```js
const { facilitator } = require("@coinbase/x402");

const payment = paymentMiddleware(PAY_TO, routes, facilitator);
```

使用 CDP 服务需要设置 `CDP_API_KEY_ID` 和 `CDP_API_KEY_SECRET` 环境变量。这些信息可以从 [https://portal.cdp.coinbase.com](https://portal.cdp.coinbase.com) 获取。

## 使用 `pay-for-service` 技能进行测试

在服务器运行完成后，可以使用 `pay-for-service` 技能来测试支付功能：

```bash
# Check the endpoint's payment requirements
npx awal@latest x402 details http://localhost:3000/api/example

# Make a paid request
npx awal@latest x402 pay http://localhost:3000/api/example
```

## 定价指南

| 使用场景          | 建议价格                |
| ---------------------- | ----------------------------- |
| 简单数据查询       | $0.001 – $0.01                        |
| API 代理/数据增强     | $0.01 – $0.10                        |
| 计算密集型查询      | $0.10 – $0.50                        |
| AI 模型推理       | $0.05 – $1.00                        |

## 检查清单

- [ ] 使用 `npx awal@latest address` 获取钱包地址
- [ ] 安装 `express` 和 `x402-express` 包
- [ ] 定义带有价格和描述的路由
- [ ] 在受保护的路由之前注册支付中间件
- [ ] 在支付中间件之前保留用于检查服务器状态的端点
- [ ] 使用 `curl` 进行测试（应收到 402 错误响应）；使用 `npx awal@latest x402 pay` 进行测试（应收到 200 成功响应）
- [ ] 公开你的服务，以便其他系统能够找到并使用它