---
name: imagerouter
description: 使用 ImageRouter API 通过任何模型生成 AI 图像（需要 API 密钥）。
homepage: https://imagerouter.io
metadata: {"clawdbot":{"emoji":"🎨","requires":{"bins":["curl"]}}}
---

# ImageRouter 图像生成

可以使用 `curl` 命令，通过 ImageRouter 生成任何可用模型的图像。

## 可用模型
`test/test` 模型是一个免费的测试模型，用于测试 API。它不是一个真实的模型，因此建议使用其他模型来生成图像。

获取最受欢迎的 10 个模型：
```bash
curl -X POST 'https://backend.imagerouter.io/operations/get-popular-models'
```

按名称搜索可用模型：
```bash
curl "https://api.imagerouter.io/v1/models?type=image&sort=date&name=gemini"
```

获取所有可用模型：
```bash
curl "https://api.imagerouter.io/v1/models?type=image&sort=date&limit=1000"
```

## 快速入门 - 文本转图像
使用 JSON 端点进行基本图像生成：
```bash
curl 'https://api.imagerouter.io/v1/openai/images/generations' \
  -H 'Authorization: Bearer YOUR_API_KEY' \
  --json '{
    "prompt": "a serene mountain landscape at sunset",
    "model": "test/test",
    "quality": "auto",
    "size": "auto",
    "response_format": "url",
    "output_format": "webp"
  }'
```

## 统一端点（文本转图像 & 图像转图像）

### 使用 `multipart/form-data` 进行文本转图像：
```bash
curl 'https://api.imagerouter.io/v1/openai/images/edits' \
  -H 'Authorization: Bearer YOUR_API_KEY' \
  -F 'prompt=a cyberpunk city at night' \
  -F 'model=test/test' \
  -F 'quality=high' \
  -F 'size=1024x1024' \
  -F 'response_format=url' \
  -F 'output_format=webp'
```

### 图像转图像（需要输入图像）：
```bash
curl 'https://api.imagerouter.io/v1/openai/images/edits' \
  -H 'Authorization: Bearer YOUR_API_KEY' \
  -F 'prompt=transform this into a watercolor painting' \
  -F 'model=test/test' \
  -F 'quality=auto' \
  -F 'size=auto' \
  -F 'response_format=url' \
  -F 'output_format=webp' \
  -F 'image[]=@/path/to/your/image.webp'
```

### 多张图像（最多 16 张）：
```bash
curl 'https://api.imagerouter.io/v1/openai/images/edits' \
  -H 'Authorization: Bearer YOUR_API_KEY' \
  -F 'prompt=combine these images' \
  -F 'model=test/test' \
  -F 'image[]=@image1.webp' \
  -F 'image[]=@image2.webp' \
  -F 'image[]=@image3.webp'
```

### 带有遮罩的图像（某些模型需要遮罩进行修复）：
```bash
curl 'https://api.imagerouter.io/v1/openai/images/edits' \
  -H 'Authorization: Bearer YOUR_API_KEY' \
  -F 'prompt=fill the masked area with flowers' \
  -F 'model=test/test' \
  -F 'image[]=@original.webp' \
  -F 'mask[]=@mask.webp'
```

## 参数

- **model**（必填）：要使用的图像模型（详见：https://imagerouter.io/models）
- **prompt**（可选）：用于图像生成的文本描述。大多数模型需要文本提示，但并非所有模型都需要。
- **quality**（可选）：`auto`（默认值）、`low`、`medium`、`high`
- **size**（可选）：`auto`（默认值）或 `WIDTHxHEIGHT`（例如：`1024x1024`）
- **response_format**（可选）：
  - `url`（默认值）：返回托管的图像 URL
  - `b64_json`：返回 Base64 编码的图像
  - `b64_ephemeral`：不保存到日志中的 Base64 编码图像
- **output_format**（可选）：`webp`（默认值）、`jpeg`、`png`
- **image[]**（可选）：用于图像转图像的输入文件（仅限 `multipart` 格式）
- **mask[]**（可选）：用于图像修复的遮罩图像（仅限 `multipart` 格式）

## 响应格式
```json
{
  "created": 1769286389027,
  "data": [
    {
      "url": "https://storage.imagerouter.io/fffb4426-efbd-4bcc-87d5-47e6936bf0bb.webp"
    }
  ],
  "latency": 6942,
  "cost": 0.004
}
```

## 端点比较

| 功能 | 统一端点（/edits） | JSON 端点（/generations） |
|---------|------------------|---------------------|
| 文本转图像 | ✅ | ✅ |
| 图像转图像 | ✅ | ❌ |
| 编码方式 | `multipart/form-data` | `application/json` |

## 提示

- `/v1/openai/images/generations` 和 `/v1/openai/images/edits` 是同一个统一端点的不同路径
- 当不需要上传文件时，使用 JSON 端点进行简单的文本转图像操作
- 当需要图像转图像功能时，使用统一端点
- 请访问 https://imagerouter.io/models 查看各模型的具体功能（如质量支持、编辑支持等）
- 请在 https://imagerouter.io/api-keys 获取您的 API 密钥

## 按使用场景划分的示例

### 快速测试生成：
```bash
curl 'https://api.imagerouter.io/v1/openai/images/generations' \
  -H 'Authorization: Bearer YOUR_API_KEY' \
  --json '{"prompt":"test image","model":"test/test"}'
```

### 直接下载图像：
```bash
curl 'https://api.imagerouter.io/v1/openai/images/generations' \
  -H 'Authorization: Bearer YOUR_API_KEY' \
  --json '{"prompt":"abstract art","model":"test/test"}' \
  | jq -r '.data[0].url' \
  | xargs curl -o output.webp
```