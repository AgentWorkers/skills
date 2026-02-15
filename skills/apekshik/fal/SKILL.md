---
name: fal
version: 1.0.1
description: 搜索、探索并运行 fal.ai 的生成式 AI 模型（包括图像生成、视频生成、音频生成和 3D 模型）。当用户需要使用 AI 模型来生成图像、视频或其他媒体内容时，可以使用该功能。
allowed-tools: Bash(curl *), Bash(jq *), Bash(mkdir *), Read, Write
argument-hint: "<command> [model_id] [--param value]"
---

# fal.ai 模型 API 功能

在 fal.ai 上运行 1000 多个生成式 AI 模型。

## 参数

- **命令:** `$0` (search | schema | run | status | result | upload)
- **参数 1:** `$1` (model_id, 搜索查询或文件路径)
- **参数 2+:** `$2`, `$3`, 等 (其他参数)
- **所有参数:** `$ARGUMENTS`

## 会话输出

将生成的文件保存到会话文件夹中：
```bash
mkdir -p ~/.fal/sessions/${CLAUDE_SESSION_ID}
```

下载的图片/视频将被保存到：`~/.fal/sessions/${CLAUDE_SESSION_ID}/`

---

## 认证

需要 `FAL_KEY` 环境变量。如果请求失败并返回 401 错误，请告知用户：
```
Get an API key from https://fal.ai/dashboard/keys
Then: export FAL_KEY="your-key-here"
```

---

## 命令: `$0`

### 如果 $0 = "search"

搜索与 `$1` 匹配的模型：

```bash
curl -s "https://api.fal.ai/v1/models?q=$1&limit=15" \
  -H "Authorization: Key $FAL_KEY" | jq -r '.models[] | "• \(.endpoint_id) — \(.metadata.display_name) [\(.metadata.category)]"'
```

进行类别搜索时，请使用：
```bash
curl -s "https://api.fal.ai/v1/models?category=$1&limit=15" \
  -H "Authorization: Key $FAL_KEY" | jq -r '.models[] | "• \(.endpoint_id) — \(.metadata.display_name)"'
```

可用类别：`text-to-image` (文本转图像), `image-to-video` (图像转视频), `text-to-3d` (文本转 3D), `training` (训练), `speech-to-text` (语音转文本), `text-to-speech` (语音转文本)

---

## 命令: `$0 = "schema"

获取模型 `$1` 的输入格式：

```bash
curl -s "https://api.fal.ai/v1/models?endpoint_id=$1&expand=openapi-3.0" \
  -H "Authorization: Key $FAL_KEY" | jq '.models[0].openapi.components.schemas.Input.properties'
```

显示必填字段和可选字段，以帮助用户了解所需输入内容。

---

## 命令: `$0 = "run"

使用剩余参数运行模型 `$1`。

**步骤 1：解析参数**
从 `$ARGUMENTS` 中提取模型 ID 后的 `--key value` 对，并构建 JSON 数据包。

示例：`/fal run fal-ai/flux-2 --prompt "a cat" --image_size landscape_16_9`
→ 模型：`fal-ai/flux-2`
→ 数据包：`{"prompt": "a cat", "image_size": "landscape_16_9"}`

**步骤 2：提交到队列**
```bash
curl -s -X POST "https://queue.fal.run/$1" \
  -H "Authorization: Key $FAL_KEY" \
  -H "Content-Type: application/json" \
  -d '<JSON_PAYLOAD>'
```

**步骤 3：等待任务完成**
```bash
# Get request_id from response, then poll:
while true; do
  STATUS=$(curl -s "https://queue.fal.run/$1/requests/$REQUEST_ID/status" \
    -H "Authorization: Key $FAL_KEY" | jq -r '.status')
  echo "Status: $STATUS"
  if [ "$STATUS" = "COMPLETED" ]; then break; fi
  if [ "$STATUS" = "FAILED" ]; then echo "Job failed"; break; fi
  sleep 3
done
```

**步骤 4：获取结果并保存**
```bash
# Fetch result
RESULT=$(curl -s "https://queue.fal.run/$1/requests/$REQUEST_ID" \
  -H "Authorization: Key $FAL_KEY")

# Create session output folder
mkdir -p ~/.fal/sessions/${CLAUDE_SESSION_ID}

# Download images/videos
# For images: jq -r '.images[0].url' and curl to download
# Save as: ~/.fal/sessions/${CLAUDE_SESSION_ID}/<timestamp>_<model>.png
```

---

## 命令: `$0 = "status"

检查模型 `$1` 的请求状态：

```bash
curl -s "https://queue.fal.run/$1/requests/$2/status?logs=1" \
  -H "Authorization: Key $FAL_KEY" | jq '{status: .status, queue_position: .queue_position, logs: .logs}'
```

---

## 命令: `$0 = "result"

获取模型 `$1` 的请求结果：

```bash
curl -s "https://queue.fal.run/$1/requests/$2" \
  -H "Authorization: Key $FAL_KEY" | jq '.'
```

---

## 命令: `$0 = "upload"

将文件 `$1` 上传到 fal CDN：

```bash
curl -s -X POST "https://fal.run/fal-ai/storage/upload" \
  -H "Authorization: Key $FAL_KEY" \
  -F "file=@$1"
```

返回用于模型请求的 URL。

---

## 快速参考

**常用模型：**
- `fal-ai/flux-2` — 快速文本转图像
- `fal-ai/flux-2-pro` — 高质量文本转图像
- `fal-ai/kling-video/v2/image-to-video` — 图像转视频
- `fal-ai/minimax/video-01/image-to-video` — 图像转视频
- `fal-ai/whisper` — 语音转文本

**文本转图像的常用参数：**
- `--prompt "description"` — 生成内容
- `--image_size landscape_16_9` — 长宽比（正方形, portrait_4_3, landscape_16_9）
- `--num_images 1` — 生成图像的数量

**示例用法：**
- `/fal search video` — 查找视频模型
- `/fal schema fal-ai/flux-2` — 查看输入选项
- `/fal run fal-ai/flux-2 --prompt "a sunset over mountains"` — 运行模型并指定提示
- `/fal status fal-ai/flux-2 abc-123` — 查看模型状态
- `/fal upload ./photo.png` — 上传图片到 fal.ai

---