---
name: fal-ai
description: >
  **fal.ai API集成与管理的API密钥认证**  
  通过该功能，用户可以使用fal.ai提供的API来运行各种AI模型，实现图像生成、视频生成、音频处理等任务。  
  - **图像生成**：利用Flux或SDXL等工具生成图像。  
  - **视频制作**：使用Minimax等工具制作视频。  
  - **图像缩放**：对图像进行放大或缩小处理。  
  - **音频转录**：将音频内容转换为文本。  
  - **其他AI任务**：还可以运行fal.ai上的其他AI模型。  
  **使用说明**：  
  当用户需要执行上述操作时，建议使用此技能。  
  **注意**：  
  对于其他第三方应用程序，建议使用`api-gateway`技能（https://clawhub.ai/byungkyu/api-gateway）进行集成。
compatibility: Requires network access and valid Maton API key
metadata:
  author: maton
  version: "1.0"
  clawdbot:
    emoji: 🧠
    homepage: "https://maton.ai"
    requires:
      env:
        - MATON_API_KEY
---
# fal.ai

使用管理的API密钥进行认证，以访问fal.ai的队列API。该API支持运行1000多种AI模型，包括图像生成（Flux、SDXL）、视频生成（Minimax）、图像缩放、文本转语音等功能。

## 快速入门

```bash
# Generate an image with Flux Schnell
python <<'EOF'
import urllib.request, os, json

data = json.dumps({
    "prompt": "a tiny cute cat",
    "image_size": "square_hd",
    "num_images": 1
}).encode()

req = urllib.request.Request('https://gateway.maton.ai/fal-ai/fal-ai/flux/schnell', data=data, method='POST')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Content-Type', 'application/json')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

## 基本URL

```
https://gateway.maton.ai/fal-ai/{native-api-path}
```

该网关会将请求代理到`queue.fal.run`。模型推理的路径遵循以下格式：

```
/fal-ai/fal-ai/{model-id}
/fal-ai/fal-ai/{model-id}/requests/{request_id}/status
/fal-ai/fal-ai/{model-id}/requests/{request_id}
/fal-ai/fal-ai/{model-id}/requests/{request_id}/cancel
```

## 认证

所有请求都需要在`Authorization`头部包含Maton API密钥：

```
Authorization: Bearer $MATON_API_KEY
```

**环境变量：** 将您的API密钥设置为`MATON_API_KEY`：

```bash
export MATON_API_KEY="YOUR_API_KEY"
```

### 获取API密钥

1. 在[maton.ai](https://maton.ai)登录或创建账户。
2. 访问[maton.ai/settings](https://maton.ai/settings)。
3. 复制您的API密钥。

## 连接管理

您可以在`https://ctrl.maton.ai`管理您的fal.ai API密钥连接。

### 列出连接

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://ctrl.maton.ai/connections?app=fal-ai&status=ACTIVE')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### 创建连接

```bash
python <<'EOF'
import urllib.request, os, json
data = json.dumps({'app': 'fal-ai'}).encode()
req = urllib.request.Request('https://ctrl.maton.ai/connections', data=data, method='POST')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Content-Type', 'application/json')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

**响应：**
```json
{
  "connection": {
    "connection_id": "7355bd0b-8aaf-4c58-9122-a1e3d454414d",
    "status": "PENDING",
    "url": "https://connect.maton.ai/?session_token=...",
    "app": "fal-ai",
    "method": "API_KEY"
  }
}
```

在浏览器中打开返回的`url`，以输入您的fal.ai API密钥。

### 获取连接信息

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://ctrl.maton.ai/connections/{connection_id}')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### 删除连接

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://ctrl.maton.ai/connections/{connection_id}', method='DELETE')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

## API参考

### 队列API

fal.ai的队列API提供异步模型推理功能，并支持状态查询。

#### 提交请求

提交一个请求以运行模型。系统会立即返回请求ID。

```bash
POST /fal-ai/fal-ai/{model-id}
Content-Type: application/json

{
  "prompt": "model-specific parameters",
  ...
}
```

**响应：**
```json
{
  "status": "IN_QUEUE",
  "request_id": "3229f185-a99a-48c0-a292-e25bf9baaeba",
  "response_url": "https://queue.fal.run/fal-ai/flux/requests/3229f185-a99a-48c0-a292-e25bf9baaeba",
  "status_url": "https://queue.fal.run/fal-ai/flux/requests/3229f185-a99a-48c0-a292-e25bf9baaeba/status",
  "cancel_url": "https://queue.fal.run/fal-ai/flux/requests/3229f185-a99a-48c0-a292-e25bf9baaeba/cancel",
  "queue_position": 0
}
```

#### 检查状态

持续查询请求状态，直到任务完成。

```bash
GET /fal-ai/fal-ai/{model-id}/requests/{request_id}/status
```

**响应（IN_PROGRESS）：**
```json
{
  "status": "IN_PROGRESS",
  "request_id": "3229f185-a99a-48c0-a292-e25bf9baaeba"
}
```

**响应（COMPLETED）：**
```json
{
  "status": "COMPLETED",
  "request_id": "3229f185-a99a-48c0-a292-e25bf9baaeba",
  "metrics": {
    "inference_time": 0.3334658145904541
  }
}
```

#### 获取结果

检索已完成的任务结果。

```bash
GET /fal-ai/fal-ai/{model-id}/requests/{request_id}
```

**响应（图像生成）：**
```json
{
  "images": [
    {
      "url": "https://v3b.fal.media/files/...",
      "width": 1024,
      "height": 1024,
      "content_type": "image/jpeg"
    }
  ],
  "timings": {
    "inference": 0.1587670766748488
  },
  "seed": 761506470,
  "prompt": "a tiny cute cat"
}
```

#### 取消请求

取消已排队或正在进行的请求。

```bash
PUT /fal-ai/fal-ai/{model-id}/requests/{request_id}/cancel
```

### 流行模型

#### Flux Schnell（快速图像生成）

```bash
python <<'EOF'
import urllib.request, os, json

data = json.dumps({
    "prompt": "a serene mountain landscape at sunset",
    "image_size": "landscape_16_9",
    "num_images": 1,
    "num_inference_steps": 4
}).encode()

req = urllib.request.Request('https://gateway.maton.ai/fal-ai/fal-ai/flux/schnell', data=data, method='POST')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Content-Type', 'application/json')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

**参数：**
- `prompt`（必填）：图像的文字描述
- `image_size`：`square_hd`、`square`、`portrait_4_3`、`portrait_16_9`、`landscape_4_3`、`landscape_16_9`
- `num_images`：要生成的图像数量（默认：1）
- `num_inference_steps`：推理步骤的数量（默认：4）
- `seed`：用于保证结果一致性的随机种子

#### Fast SDXL（Stable Diffusion XL）

```bash
python <<'EOF'
import urllib.request, os, json

data = json.dumps({
    "prompt": "a futuristic city skyline at night",
    "negative_prompt": "blurry, low quality",
    "image_size": "landscape_16_9",
    "num_images": 1
}).encode()

req = urllib.request.Request('https://gateway.maton.ai/fal-ai/fal-ai/fast-sdxl', data=data, method='POST')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Content-Type', 'application/json')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

**参数：**
- `prompt`（必填）：图像的文字描述
- `negative_prompt`：图像中应避免的内容
- `image_size`：输出图像的尺寸
- `num_images`：要生成的图像数量
- `guidance_scale`：CFG缩放比例（默认：7.5）
- `num_inference_steps`：推理步骤的数量

#### Clarity Upscaler（图像缩放）

```bash
python <<'EOF'
import urllib.request, os, json

data = json.dumps({
    "image_url": "https://example.com/image.jpg",
    "scale": 2
}).encode()

req = urllib.request.Request('https://gateway.maton.ai/fal-ai/fal-ai/clarity-upscaler', data=data, method='POST')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Content-Type', 'application/json')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

**参数：**
- `image_url`（必填）：需要缩放的图像URL
- `scale`：缩放比例（2、4）

#### Minimax视频生成

```bash
python <<'EOF'
import urllib.request, os, json

data = json.dumps({
    "prompt": "A cat playing with a ball in slow motion"
}).encode()

req = urllib.request.Request('https://gateway.maton.ai/fal-ai/fal-ai/minimax/video-01', data=data, method='POST')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Content-Type', 'application/json')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

#### F5-TTS（文本转语音）

```bash
python <<'EOF'
import urllib.request, os, json

data = json.dumps({
    "gen_text": "Hello world, this is a test of fal ai text to speech."
}).encode()

req = urllib.request.Request('https://gateway.maton.ai/fal-ai/fal-ai/f5-tts', data=data, method='POST')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Content-Type', 'application/json')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### 请求状态代码

| 状态 | 说明 |
|--------|-------------|
| `IN_QUEUE` | 请求已接收，正在等待执行 |
| `IN_PROGRESS` | 模型正在处理请求 |
| `COMPLETED` | 处理完成，结果可用 |
| `FAILED` | 处理失败（请查看错误详情） |

### 请求头

| 头部字段 | 说明 |
|--------|-------------|
| `X-Fal-Request-Timeout` | 服务器端的超时时间（秒） |
| `X-Fal-Runner-Hint` | 用于路由的会话标识 |
| `X-Fal-Queue-Priority` | `normal`（默认）或`low` |
| `X-Fal-No-Retry` | 禁用自动重试 |

## 完整工作流程示例

```bash
python <<'EOF'
import urllib.request, os, json, time

api_key = os.environ["MATON_API_KEY"]
base_url = "https://gateway.maton.ai/fal-ai"

# 1. Submit request
data = json.dumps({
    "prompt": "a beautiful sunset over the ocean",
    "image_size": "landscape_16_9",
    "num_images": 1
}).encode()

req = urllib.request.Request(f'{base_url}/fal-ai/flux/schnell', data=data, method='POST')
req.add_header('Authorization', f'Bearer {api_key}')
req.add_header('Content-Type', 'application/json')
submit_response = json.load(urllib.request.urlopen(req))
request_id = submit_response['request_id']
print(f"Submitted: {request_id}")

# 2. Poll for completion
while True:
    req = urllib.request.Request(f'{base_url}/fal-ai/flux/requests/{request_id}/status')
    req.add_header('Authorization', f'Bearer {api_key}')
    status_response = json.load(urllib.request.urlopen(req))
    print(f"Status: {status_response['status']}")

    if status_response['status'] == 'COMPLETED':
        break
    elif status_response['status'] == 'FAILED':
        print("Request failed")
        exit(1)

    time.sleep(1)

# 3. Get result
req = urllib.request.Request(f'{base_url}/fal-ai/flux/requests/{request_id}')
req.add_header('Authorization', f'Bearer {api_key}')
result = json.load(urllib.request.urlopen(req))
print(f"Image URL: {result['images'][0]['url']}")
EOF
```

## 代码示例

### JavaScript

```javascript
const submitRequest = async () => {
  // Submit
  const submitRes = await fetch('https://gateway.maton.ai/fal-ai/fal-ai/flux/schnell', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${process.env.MATON_API_KEY}`
    },
    body: JSON.stringify({
      prompt: 'a tiny cute cat',
      image_size: 'square_hd',
      num_images: 1
    })
  });
  const { request_id } = await submitRes.json();

  // Poll
  let status = 'IN_QUEUE';
  while (status !== 'COMPLETED') {
    await new Promise(r => setTimeout(r, 1000));
    const statusRes = await fetch(
      `https://gateway.maton.ai/fal-ai/fal-ai/flux/requests/${request_id}/status`,
      { headers: { 'Authorization': `Bearer ${process.env.MATON_API_KEY}` } }
    );
    status = (await statusRes.json()).status;
  }

  // Get result
  const resultRes = await fetch(
    `https://gateway.maton.ai/fal-ai/fal-ai/flux/requests/${request_id}`,
    { headers: { 'Authorization': `Bearer ${process.env.MATON_API_KEY}` } }
  );
  return await resultRes.json();
};
```

### Python（使用requests库）

```python
import os
import time
import requests

api_key = os.environ["MATON_API_KEY"]
headers = {"Authorization": f"Bearer {api_key}"}

# Submit
response = requests.post(
    "https://gateway.maton.ai/fal-ai/fal-ai/flux/schnell",
    headers=headers,
    json={"prompt": "a tiny cute cat", "image_size": "square_hd", "num_images": 1}
)
request_id = response.json()["request_id"]

# Poll
while True:
    status = requests.get(
        f"https://gateway.maton.ai/fal-ai/fal-ai/flux/requests/{request_id}/status",
        headers=headers
    ).json()["status"]
    if status == "COMPLETED":
        break
    time.sleep(1)

# Get result
result = requests.get(
    f"https://gateway.maton.ai/fal-ai/fal-ai/flux/requests/{request_id}",
    headers=headers
).json()
print(result["images"][0]["url"])
```

## 注意事项

- 网关会将请求代理到`queue.fal.run`以执行模型推理。
- 所有模型请求都会被放入队列中，需要持续查询状态直到任务完成。
- 不同模型的参数可能有所不同，请参考fal.ai的官方文档获取详细信息。
- fal.ai提供的图像URL为临时链接，请下载或保存这些图像。
- 视频生成模型可能需要更长的时间来完成。
- 对于长时间运行的任务，建议使用Webhook（在请求中添加`?fal_webhook=URL`）。
- 重要提示：当将curl的输出结果传递给`jq`时，环境变量可能无法正确解析。建议使用Python代码进行处理。

## 错误处理

| 状态代码 | 含义 |
|--------|---------|
| 400 | 未建立与fal-ai的连接或请求无效 |
| 401 | Maton API密钥无效或缺失 |
| 422 | 模型参数错误 |
| 429 | 请求频率受限 |
| 4xx/5xx | 来自fal.ai API的传递错误 |

### 故障排除

1. **检查连接是否正常：**
```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://ctrl.maton.ai/connections?app=fal-ai&status=ACTIVE')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

2. **验证路径格式**：路径必须以`/fal-ai/fal-ai/{model-id}`开头。

3. **确认模型是否存在**：某些模型ID包含组织前缀（例如`fal-ai/flux/schnell`）。

## 资源

- [fal.ai文档](https://fal.ai/docs)
- [模型库](https://fal.ai/models)
- [队列API参考](https://fal.ai/docs/model-endpoints/queue)
- [Maton社区](https://discord.com/invite/dBfFAcefs2)
- [Maton支持团队](mailto:support@maton.ai)