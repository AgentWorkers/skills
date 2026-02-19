# 技能：openvid

## 描述  
openvid 是一项用于生成 AI 动画视频的服务。用户只需提交提示文本和视频的 URL，即可获得一个带有品牌标识的解释性视频。  

**定价：** 每 15 秒收费 5 美元（支持 15 秒、30 秒、60 秒、90 秒的视频时长）。  

**注意：** 这是一项基于外部 API 的服务——不涉及任何代码执行或本地文件修改。  

---

## 隐私与数据安全  

- **用户需提供的信息：** 提示文本以及（可选的）用于提取品牌信息的公共 URL。  
- **服务流程：** 服务会获取该 URL，提取其中的品牌颜色、字体和 logo，然后生成视频。  
- **数据存储：** 视频会存储在 Cloudflare R2 服务器上 7 天后自动删除。  
- **建议：** 仅提交公共 URL，切勿发送内部/私有 URL 或敏感信息。  

---

## x402 支付流程  
openvid 使用 **x402 HTTP 支付协议**（一种按请求计费的 API 标准）。  

### 工作原理：  
1. **请求**：用户向 API 发送 POST 请求。  
2. **402 响应**：API 返回支付相关信息（金额、钱包地址、区块链类型）。  
3. **支付**：用户通过钱包在区块链上进行支付（支持 USDC 或 SOL）。  
4. **重新请求并附带支付证明**：用户需在请求头中添加 `X-Payment` 字段，其中包含已签名的交易信息。  
5. **任务创建**：API 返回任务 ID，用户需要持续查询任务状态直至视频生成完成。  

### 谁负责支付签名？  
支付签名由用户的钱包完成，而非 openvid 服务本身。支付签名流程由以下组件处理：  
- 用户的钱包基础设施（例如 OpenClaw 的内置钱包）  
- 兼容 x402 协议的库（`@x402/fetch`、`@x402/client`）  
- 若直接调用 API，则需要手动完成签名操作。  
**请注意：** openvid 服务不要求用户提供或使用任何私钥。  

---

## API 参考  
**API 端点：** `https://gateway.openvid.app`  

### 视频生成流程  

**首次请求（需要支付）：**  
```http
POST /v1/video/generate
Content-Type: application/json

{
  "prompt": "Make a video about Stripe https://stripe.com",
  "duration": 30
}
```  

**支付完成后，重新发送请求并添加 `X-Payment` 头部信息：**  
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
| 15 秒   | 5 美元 |
| 30 秒   | 10 美元 |
| 60 秒   | 20 美元 |
| 90 秒   | 30 美元 |

---

## ACP（Virtuals 协议）  
对于通过 Virtuals 协议进行的代理间交易：  
- **代理 ID：** `1869`  
- **钱包地址：** `0xc0A11946195525c5b6632e562d3958A2eA4328EE`  

---

## 使用建议：  
- **务必提供公共 URL**，以便准确提取品牌信息。  
- 明确说明视频需要传达的核心内容。  
- 视频时长越短（15–30 秒），画质越好。  
- **严禁发送私有/内部 URL**——所有视频资源均由服务自动获取。