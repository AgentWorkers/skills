---
name: quiverai
description: 通过 QuiverAI API（Arrow 模型）生成并矢量化 SVG 图形。适用于用户需要创建 SVG 标志、图标或插图的情况，或者将光栅图像（PNG/JPEG/WebP）转换为 SVG，以及从文本提示生成矢量图形的需求。
metadata:
  {
    "openclaw":
      {
        "emoji": "🖋️",
        "requires": { "env": ["QUIVERAI_API_KEY"] },
        "primaryEnv": "QUIVERAI_API_KEY",
      },
  }
---
# QuiverAI — 人工智能矢量图形生成工具

QuiverAI 可以根据文本描述或栅格图像生成可直接用于生产的 SVG 文件。

- 网站：https://quiver.ai  
- 文档：https://docs.quiver.ai  
- API 接口：`https://api.quiver.ai/v1`  
- 使用的模型：`arrow-preview`  
- 认证方式：通过 `QUIVERAI_API_KEY` 使用 bearer token 进行身份验证  
- 计费方式：每次请求消耗 1 个信用点（无论输出数量 `n` 为多少）。  

## 设置  

请在 [https://app.quiver.ai/settings/api-keys](https://app.quiver.ai/settings/api-keys) 获取 API 密钥（首先需要注册账户：[https://quiver.ai/start](https://quiver.ai/start)）。  

## 将文本转换为 SVG  

根据文本描述生成 SVG 文件。  
**接口端点：`POST /v1/svgs/generations`**  

**Node.js SDK 示例（使用 `npm install @quiverai/sdk` 安装 SDK）：**  
```bash
curl -X POST https://api.quiver.ai/v1/svgs/generations \
  -H "Authorization: Bearer $QUIVERAI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "arrow-preview",
    "prompt": "A minimalist monogram logo using the letter Q",
    "n": 1,
    "stream": false
  }'
```  

### 参数说明  

| 参数 | 类型 | 默认值 | 说明 |  
| --- | --- | --- | --- |  
| `model` | string | — | 必填参数。使用 `arrow-preview` 模型。  
| `prompt` | string | — | 必填参数。用于描述所需的 SVG 图形样式。  
| `instructions` | string | — | 可选参数。提供额外的样式指导（例如：“扁平单色、圆角”等）。  
| `references` | array | — | 最多可提供 4 张参考图片（格式为 `{ url }` 或 `{ base64 }`）。  
| `n` | int | 1 | 输出 SVG 文件的数量（1–16 个）。  
| `temperature` | float | 1 | 采样精度参数（0–2）。数值越低，生成结果越稳定。  
| `top_p` | float | 1 | 核心采样参数（0–1）。  
| `max_output_tokens` | int | — | 输出文本的最大字符数限制（最多 131072 个）。  
| `stream` | bool | false | 是否启用 SSE 流式传输（响应类型包括 `reasoning`、`draft`、`content`）。  

### 响应内容  

```json
{
  "id": "resp_01J...",
  "created": 1704067200,
  "data": [{ "svg": "<svg ...>...</svg>", "mime_type": "image/svg+xml" }],
  "usage": { "total_tokens": 1640, "input_tokens": 1200, "output_tokens": 440 }
}
```  

## 将图像转换为 SVG （矢量化）  

可以将 PNG/JPEG/WebP 格式的图像转换为 SVG 文件。  
**接口端点：`POST /v1/svgs/vectorizations`**  

**SDK 示例（使用 `npm install @quiverai/sdk` 安装 SDK）：**  
```typescript
const result = await client.vectorizeSVG.vectorizeSVG({
  model: "arrow-preview",
  image: { url: "https://example.com/logo.png" },
});
```  

### 额外参数（针对图像转换功能）  

| 参数 | 类型 | 默认值 | 说明 |  
| --- | --- | --- | --- |  
| `image` | object | — | 必填参数。图片路径格式为 `{ url: "..." }` 或 `{ base64: "..." }`。  
| `auto_crop` | bool | false | 是否在矢量化前裁剪图片中的主要元素。  
| `target_size` | int | — | 转换后的图像目标尺寸（以像素为单位，范围 128–4096）。  

响应格式与文本转换为 SVG 的响应格式相同。  

## 错误代码  

| 状态码 | 代码 | 含义 |  
| --- | --- | --- |  
| 400 | `invalid_request` | 请求格式错误或缺少必要参数。  
| 401 | `unauthorized` | API 密钥无效或未授权。  
| 402 | `insufficient_credits` | 信用点不足。  
| 429 | `rate_limit_exceeded` | 请求次数过多，请稍后重试。  

## 使用建议：  

- 将生成的 SVG 文件保存为 `.svg` 格式以便立即使用。  
- 使用 `instructions` 参数来调整 SVG 的样式，而无需修改原始文本描述。  
- 对于徽标设计，建议使用较低的 `temperature` 值（0.3–0.5），以获得更清晰、风格统一的输出效果。  
- 如需使用参考图片，可以通过 `references` 参数提供参考样本。  
- 如果源图片包含过多空白区域，建议在矢量化时启用 `auto_crop: true` 选项。