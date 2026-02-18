# 技能：openvid

## 描述
这是一个用于生成AI动图视频的服务。您只需发送一个提示信息以及视频的URL，即可获得一个带有品牌标识的解释性视频。

**价格：** 每15秒5美元（时长范围：15秒至3分钟）

**注意：** 这是一项**服务型技能**，它仅调用外部API，不涉及任何代码执行或本地文件的修改。

---

## 隐私与数据安全

- **您需要提供的信息：** 提示文本以及（可选的）用于提取品牌信息的公共URL。
- **服务流程：** 该服务会获取您提供的URL，提取其中的品牌颜色、字体和Logo，并生成相应的视频。
- **数据存储：** 视频会存储在Cloudflare R2平台上，保留7天后被删除。
- **建议：** 仅发送**公共URL**，切勿发送内部/私有URL或敏感信息。

---

## x402支付流程

该技能使用**x402 HTTP支付协议**，这是一种用于按次计费的API标准。

### 工作原理

1. **请求**：您通过POST请求发送到API。
2. **402响应**：API会返回支付相关信息（金额、钱包地址、区块链类型）。
3. **支付**：您的代理或钱包会在区块链上完成支付（使用USDC或Solana的SOL进行支付）。
4. **重新发送请求并附加支付凭证**：需要再次发送请求，并在请求头中添加`X-Payment`字段，其中包含已签名的交易信息。
5. **任务创建**：API会返回一个`jobId`，您需要持续查询该ID以确认任务完成情况。

### 谁负责支付？

**支付操作由您的代理钱包完成，而非该技能本身。**  
支付流程的具体实现包括：
- 您的代理钱包系统（例如OpenClaw内置的钱包）。
- 兼容x402协议的库（如`@x402/fetch`、`@x402/client`）。
- 如果直接调用API，则可能需要手动完成签名操作。

**该技能无需也不要求您提供任何私钥。**

---

## API参考

**接口地址：** `https://gateway.openvid.app`

### 创建视频

```http
POST /v1/video/generate
Content-Type: application/json

{
  "prompt": "Make a video about Stripe https://stripe.com",
  "duration": 30
}
```

**首次请求时（系统返回402响应，提示需要支付）：**
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

**支付完成后，重新发送请求并添加`X-Payment`头部：**
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
|---------|-------|
| 15秒    | 5美元    |
| 30秒    | 10美元    |
| 45秒    | 15美元    |
| 60秒    | 20美元    |
| 90秒    | 30美元    |
| 2分钟    | 40美元    |
| 2分30秒  | 50美元    |
| 3分钟    | 60美元    |

---

## ACP（Virtuals协议）

**用于代理之间的交易：**
- **代理ID：** `1869`
- **钱包地址：** `0xc0A11946195525c5b6632e562d3958A2eA4328EE`

---

## 使用建议

- **务必提供公共URL**，以便准确提取品牌信息。
- **明确说明视频的主题和内容**。
- **视频时长越短，质量越好**——15至30秒的视频效果最佳。
- **切勿发送私有/内部URL**，所有视频资源均由系统自动获取。