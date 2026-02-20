# 技能：openvid

## 描述
openvid 是一款用于生成 AI 动态图形视频的服务。您只需发送一个提示文本以及视频的 URL，即可获得一个带有品牌标识的解释性视频。

**价格：** 5 至 20 美元，支持批量购买（15 秒、30 秒、60 秒、90 秒时长版本）。

**注意：** 这是一项基于外部 API 的服务——不涉及任何代码执行或本地文件的修改。

---

## 隐私与数据安全

- **您需要提供的信息：** 提示文本以及（可选的）用于提取品牌信息的公共 URL。
- **服务流程：** 该服务会获取提供的 URL，提取其中的品牌颜色、字体和 logo，然后生成视频。
- **数据存储：** 视频会存储在 Cloudflare R2 服务器上 7 天后自动删除。
- **建议：** 仅提供 **公共 URL**，切勿发送内部/私有 URL 或敏感信息。

---

## x402 支付流程

该技能使用 **x402 HTTP 支付协议**（一种按调用次数计费的 API 标准）。

### 工作原理

1. **请求**：您向 API 发送 POST 请求。
2. **402 响应**：API 返回支付相关信息（金额、钱包地址、区块链类型）。
3. **支付**：您的代理或钱包会在区块链上完成支付（使用 USDC（Base Chain）或 SOL（Solana Chain）。
4. **重新请求并附加支付证明**：在请求中添加 `X-Payment` 标头，其中包含已签名的交易信息。
5. **任务创建**：API 返回 `jobId`，您需要持续查询任务状态直至完成。

### 谁负责支付签名？

**支付签名由您的代理钱包完成，而非 openvid 服务本身。** openvid 仅负责记录 API 的使用情况。支付签名工作由以下方式处理：
- 您的代理钱包系统（例如 OpenClaw 内置钱包）
- 兼容 x402 协议的库（如 `@x402/fetch`、`@x402/client`）
- 如果直接调用 API，则需要手动完成钱包签名操作。

**该服务不要求您提供或使用任何私钥。**

---

## API 参考

**API 端点：** `https://gateway.openvid.app`

### 创建视频

```http
POST /v1/video/generate
Content-Type: application/json

{
  "prompt": "Make a video about Stripe https://stripe.com",
  "duration": 30
}
```

**首次请求时（返回 402 响应，提示需要支付）：**
```json
{
  "error": "Payment Required",
  "price": "$10",
  "duration": 30,
  "options": {
    "baseUsdc": {
      "network": "eip155:8453",
      "asset": "USDC",
      "amount": "10000000",
      "payTo": "0xc0A11946195525c5b6632e562d3958A2eA4328EE"
    },
    "solanaSol": {
      "network": "solana:mainnet",
      "asset": "SOL",
      "amount": "116000000",
      "payTo": "DzQB5aqnq8myCGm166v6AfWkJ4fsEq9HdWqhFLX6LQfi"
    }
  }
}
```

**支付完成后，重新发送请求并附加 X-Payment 标头：**
```http
POST /v1/video/generate
Content-Type: application/json
X-Payment: <base64-encoded-payment-proof>

{
  "prompt": "Make a video about Stripe https://stripe.com",
  "duration": 30
}
```

**成功响应：**
```json
{
  "jobId": "abc-123",
  "status": "processing",
  "pollUrl": "https://gateway.openvid.app/v1/jobs/abc-123"
}
```

### 查询任务状态

```http
GET /v1/jobs/{jobId}
```

**任务完成后的响应：**
```json
{
  "jobId": "abc-123",
  "status": "completed",
  "videoUrl": "https://api.openvid.app/api/renders/...",
  "productName": "Stripe",
  "duration": 30
}
```

---

## 价格表

| 视频时长 | 价格 |
|----------|-------|
| 15 秒    | 5 美元 |
| 30 秒    | 10 美元 |
| 60 秒    | 15 美元 |
| 90 秒    | 20 美元 |

---

## ACP（Virtuals 协议）

**通过 Virtuals 协议进行代理间交易时：**
- **代理 ID：** `1869`
- **钱包地址：** `0xc0A11946195525c5b6632e562d3958A2eA4328EE`

---

## 使用建议

- **务必提供公共 URL**，以便准确提取品牌信息。
- 明确说明视频需要传达的核心内容。
- 视频时长越短，画质越好（15-30 秒的视频质量最佳）。
- **切勿发送私有/内部 URL**——所有视频资源均由服务自动获取。