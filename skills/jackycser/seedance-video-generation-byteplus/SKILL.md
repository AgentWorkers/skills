---
name: seedance-video-byteplus
description: "使用 BytePlus Seedance API（国际版）生成 AI 视频。适用于以下场景：  
1. 根据文本提示生成视频；  
2. 根据图片（第一帧、首尾帧或参考图片）生成视频；  
3. 查询或管理视频生成任务。  
该 API 支持 Seedance 1.5 Pro（支持音频和草图模式）、1.0 Pro、1.0 Pro Fast 以及 1.0 Lite 模型。"
version: 1.0.0
category: file-generation
argument-hint: "[text prompt or task ID]"
---

# Seedance 视频生成（BytePlus International）

通过 **BytePlus Ark API**（国际版本）使用 ByteDance Seedance 模型生成 AI 视频。

## 先决条件

用户必须设置 `ARK_API_KEY` 环境变量，该变量应包含 BytePlus API 密钥。您可以通过运行以下命令来设置它：

```bash
export ARK_API_KEY="your-byteplus-api-key-here"
```

请从 [BytePlus API 密钥管理](https://console.byteplus.com/ark/region:ark+ap-southeast-1/apiKey) 页面获取您的 API 密钥。

**基础 URL**：`https://ark.ap-southeast.bytepluses.com/api/v3`

## 支持的模型

| 模型 | 模型 ID | 功能 |
|-------|----------|-------------|
| Seedance 1.5 Pro | `seedance-1-5-pro-251215` | 文本转视频、图片转视频（第一帧、首尾帧）、音频支持、草图模式 |
| Seedance 1.0 Pro | `seedance-1-0-pro-250428` | 文本转视频、图片转视频（第一帧、首尾帧） |
| Seedance 1.0 Pro Fast | `seedance-1-0-pro-fast-250528` | 文本转视频、图片转视频（仅第一帧） |
| Seedance 1.0 Lite T2V | `seedance-1-0-lite-t2v-250219` | 仅文本转视频 |
| Seedance 1.0 Lite I2V | `seedance-1-0-lite-i2v-250219` | 图片转视频（第一帧、首尾帧、参考图片 1-4） |

**默认模型**：`seedance-1-5-pro-251215`（最新版本，支持音频）

## 执行方式（推荐：Python CLI 工具）

提供了一个名为 `~/.claude/skills/seedance-video-byteplus/seedance_byteplus.py` 的 Python CLI 工具，该工具具有强大的执行能力，包括适当的错误处理、自动轮询和本地图片的 Base64 转换功能。**建议使用此工具，而非原始的 curl 命令。**

### 使用 Python CLI 的快速示例

```bash
# Text-to-video (create + wait + download)
python3 ~/.claude/skills/seedance-video-byteplus/seedance_byteplus.py create --prompt "A kitten yawning at the camera" --wait --download ~/Desktop

# Image-to-video from local file
python3 ~/.claude/skills/seedance-video-byteplus/seedance_byteplus.py create --prompt "The person slowly turns and smiles" --image /path/to/photo.jpg --wait --download ~/Desktop

# Image-to-video from URL
python3 ~/.claude/skills/seedance-video-byteplus/seedance_byteplus.py create --prompt "The landscape slowly zooms in" --image "https://example.com/image.jpg" --wait --download ~/Desktop

# First + last frame
python3 ~/.claude/skills/seedance-video-byteplus/seedance_byteplus.py create --prompt "A flower blooming from bud to full bloom" --image first.jpg --last-frame last.jpg --wait --download ~/Desktop

# Reference images (Lite I2V only)
python3 ~/.claude/skills/seedance-video-byteplus/seedance_byteplus.py create --prompt "[Image 1] person is dancing" --ref-images ref1.jpg ref2.jpg --model seedance-1-0-lite-i2v-250219 --wait --download ~/Desktop

# Custom parameters
python3 ~/.claude/skills/seedance-video-byteplus/seedance_byteplus.py create --prompt "City night scene time-lapse" --ratio 21:9 --duration 8 --resolution 1080p --generate-audio false --wait --download ~/Desktop

# Draft mode (cheaper preview, Seedance 1.5 Pro only)
python3 ~/.claude/skills/seedance-video-byteplus/seedance_byteplus.py create --prompt "Waves crashing on the beach" --draft true --wait --download ~/Desktop

# Generate final video from a draft
python3 ~/.claude/skills/seedance-video-byteplus/seedance_byteplus.py create --draft-task-id <DRAFT_TASK_ID> --resolution 720p --wait --download ~/Desktop

# Query task status
python3 ~/.claude/skills/seedance-video-byteplus/seedance_byteplus.py status <TASK_ID>

# Wait for an existing task
python3 ~/.claude/skills/seedance-video-byteplus/seedance_byteplus.py wait <TASK_ID> --download ~/Desktop

# List tasks
python3 ~/.claude/skills/seedance-video-byteplus/seedance_byteplus.py list --status succeeded

# Delete/cancel task
python3 ~/.claude/skills/seedance-video-byteplus/seedance_byteplus.py delete <TASK_ID>
```

## 替代方案：原始的 curl 命令

### 第 1 步：创建视频生成任务

根据用户输入确定生成模式，然后调用 API。

#### 模式 A：文本转视频

```bash
TASK_RESULT=$(curl -s -X POST "https://ark.ap-southeast.bytepluses.com/api/v3/contents/generations/tasks" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $ARK_API_KEY" \
  -d '{
    "model": "seedance-1-5-pro-251215",
    "content": [
      {
        "type": "text",
        "text": "YOUR_PROMPT_HERE"
      }
    ],
    "ratio": "16:9",
    "duration": 5,
    "resolution": "720p",
    "generate_audio": true
  }')

TASK_ID=$(echo "$TASK_RESULT" | python3 -c "import sys,json; print(json.load(sys.stdin)['id'])")
echo "Task created: $TASK_ID"
```

#### 模式 B：图片转视频（仅第一帧）

用户提供一张图片作为第一帧。图片可以是 URL 或本地文件路径（需要转换为 Base64 格式）。

**使用图片 URL：**
```bash
TASK_RESULT=$(curl -s -X POST "https://ark.ap-southeast.bytepluses.com/api/v3/contents/generations/tasks" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $ARK_API_KEY" \
  -d '{
    "model": "seedance-1-5-pro-251215",
    "content": [
      {
        "type": "text",
        "text": "YOUR_PROMPT_HERE"
      },
      {
        "type": "image_url",
        "image_url": { "url": "IMAGE_URL_HERE" },
        "role": "first_frame"
      }
    ],
    "ratio": "adaptive",
    "duration": 5,
    "resolution": "720p",
    "generate_audio": true
  }')

TASK_ID=$(echo "$TASK_RESULT" | python3 -c "import sys,json; print(json.load(sys.stdin)['id'])")
echo "Task created: $TASK_ID"
```

**使用本地图片文件（转换为 Base64 格式）：**
```bash
IMG_PATH="/path/to/image.png"
IMG_EXT="${IMG_PATH##*.}"
IMG_EXT_LOWER=$(echo "$IMG_EXT" | tr '[:upper:]' '[:lower:]')
IMG_BASE64=$(base64 < "$IMG_PATH" | tr -d '\n')
IMG_DATA_URL="data:image/${IMG_EXT_LOWER};base64,${IMG_BASE64}"

TASK_RESULT=$(curl -s -X POST "https://ark.ap-southeast.bytepluses.com/api/v3/contents/generations/tasks" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $ARK_API_KEY" \
  -d '{
    "model": "seedance-1-5-pro-251215",
    "content": [
      {
        "type": "text",
        "text": "YOUR_PROMPT_HERE"
      },
      {
        "type": "image_url",
        "image_url": { "url": "'"$IMG_DATA_URL"'" },
        "role": "first_frame"
      }
    ],
    "ratio": "adaptive",
    "duration": 5,
    "resolution": "720p",
    "generate_audio": true
  }')

TASK_ID=$(echo "$TASK_RESULT" | python3 -c "import sys,json; print(json.load(sys.stdin)['id'])")
echo "Task created: $TASK_ID"
```

#### 模式 C：图片转视频（首尾帧）

需要两张图片。支持模型：Seedance 1.5 Pro、1.0 Pro、1.0 Lite I2V。

```bash
TASK_RESULT=$(curl -s -X POST "https://ark.ap-southeast.bytepluses.com/api/v3/contents/generations/tasks" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $ARK_API_KEY" \
  -d '{
    "model": "seedance-1-5-pro-251215",
    "content": [
      {
        "type": "text",
        "text": "YOUR_PROMPT_HERE"
      },
      {
        "type": "image_url",
        "image_url": { "url": "FIRST_FRAME_IMAGE_URL" },
        "role": "first_frame"
      },
      {
        "type": "image_url",
        "image_url": { "url": "LAST_FRAME_IMAGE_URL" },
        "role": "last_frame"
      }
    ],
    "ratio": "adaptive",
    "duration": 5,
    "resolution": "720p",
    "generate_audio": true
  }')

TASK_ID=$(echo "$TASK_RESULT" | python3 -c "import sys,json; print(json.load(sys.stdin)['id'])")
echo "Task created: $TASK_ID"
```

#### 模式 D：参考图片转视频（仅支持 Seedance 1.0 Lite I2V）

提供 1-4 张参考图片。在提示中使用 `[图片 1]`、`[图片 2]` 来引用特定的图片。

```bash
TASK_RESULT=$(curl -s -X POST "https://ark.ap-southeast.bytepluses.com/api/v3/contents/generations/tasks" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $ARK_API_KEY" \
  -d '{
    "model": "seedance-1-0-lite-i2v-250219",
    "content": [
      {
        "type": "text",
        "text": "A boy from [Image 1] and a corgi from [Image 2], sitting on the lawn"
      },
      {
        "type": "image_url",
        "image_url": { "url": "REF_IMAGE_URL_1" },
        "role": "reference_image"
      },
      {
        "type": "image_url",
        "image_url": { "url": "REF_IMAGE_URL_2" },
        "role": "reference_image"
      }
    ],
    "ratio": "16:9",
    "duration": 5,
    "resolution": "720p"
  }')

TASK_ID=$(echo "$TASK_RESULT" | python3 -c "import sys,json; print(json.load(sys.stdin)['id'])")
echo "Task created: $TASK_ID"
```

### 第 2 步：轮询任务完成情况

视频生成是异步的。需要轮询任务状态，直到任务完成。

```bash
echo "Waiting for video generation to complete..."
while true; do
  STATUS_RESULT=$(curl -s -X GET "https://ark.ap-southeast.bytepluses.com/api/v3/contents/generations/tasks/${TASK_ID}" \
    -H "Authorization: Bearer $ARK_API_KEY")

  STATUS=$(echo "$STATUS_RESULT" | python3 -c "import sys,json; print(json.load(sys.stdin)['status'])")

  if [ "$STATUS" = "succeeded" ]; then
    echo "Video generation succeeded!"
    VIDEO_URL=$(echo "$STATUS_RESULT" | python3 -c "import sys,json; print(json.load(sys.stdin)['content']['video_url'])")
    echo "Video URL: $VIDEO_URL"
    break
  elif [ "$STATUS" = "failed" ]; then
    ERROR_MSG=$(echo "$STATUS_RESULT" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('error',{}).get('message','Unknown error'))" 2>/dev/null || echo "Unknown error")
    echo "Video generation failed: $ERROR_MSG"
    break
  elif [ "$STATUS" = "expired" ]; then
    echo "Video generation task expired."
    break
  else
    echo "Status: $STATUS - still processing..."
    sleep 15
  fi
done
```

### 第 3 步：下载并打开视频

```bash
OUTPUT_PATH="$HOME/Desktop/seedance_video_$(date +%Y%m%d_%H%M%S).mp4"
curl -s -o "$OUTPUT_PATH" "$VIDEO_URL"
echo "Video saved to: $OUTPUT_PATH"
open "$OUTPUT_PATH"
```

## 可选参数参考

| 参数 | 类型 | 默认值 | 描述 |
|-----------|------|---------|-------------|
| `model` | 字符串 | `seedance-1-5-pro-251215` | 要使用的模型 ID |
| `ratio` | 字符串 | `16:9`（T2V）/ `adaptive`（I2V） | 宽高比：`16:9`、`4:3`、`1:1`、`3:4`、`9:16`、`21:9`、`adaptive` |
| `duration` | 整数 | `5` | 视频时长（秒）（1.5 Pro 为 4-12 秒，其他模型为 2-12 秒）。设置 `-1` 为自动选择（仅限 1.5 Pro） |
| `resolution` | 字符串 | `720p` | 分辨率：`480p`、`720p`、`1080p` |
| `seed` | 整数 | `-1` | 用于保证结果一致性的随机种子值。-1 表示随机生成 |
| `camera_fixed` | 布尔值 | `false` | 固定摄像机位置 |
| `watermark` | 布尔值 | `false` | 在视频中添加水印 |
| `generate_audio` | 布尔值 | `true` | 生成同步音频（仅限 Seedance 1.5 Pro） |
| `draft` | 布尔值 | `false` | 生成草图/预览视频（成本较低，仅限 Seedance 1.5 Pro，强制使用 480p 分辨率） |
| `return_last_frame` | 布尔值 | `false` | 返回最后一帧图片的 URL（用于连续生成视频） |
| `service_tier` | 字符串 | `default` | `default`（在线）或 `flex`（离线，价格便宜 50%，但速度较慢） |
| `execution_expires_after` | 整数 | `172800` | 任务超时时间（秒）（3600-259200） |

## 其他操作

### 查询任务状态

```bash
curl -s -X GET "https://ark.ap-southeast.bytepluses.com/api/v3/contents/generations/tasks/${TASK_ID}" \
  -H "Authorization: Bearer $ARK_API_KEY" | python3 -m json.tool
```

### 列出任务

```bash
# List all tasks (paginated)
curl -s -X GET "https://ark.ap-southeast.bytepluses.com/api/v3/contents/generations/tasks?page_num=1&page_size=10" \
  -H "Authorization: Bearer $ARK_API_KEY" | python3 -m json.tool

# Filter by status
curl -s -X GET "https://ark.ap-southeast.bytepluses.com/api/v3/contents/generations/tasks?page_num=1&page_size=10&filter.status=succeeded" \
  -H "Authorization: Bearer $ARK_API_KEY" | python3 -m json.tool
```

### 取消或删除任务

```bash
curl -s -X DELETE "https://ark.ap-southeast.bytepluses.com/api/v3/contents/generations/tasks/${TASK_ID}" \
  -H "Authorization: Bearer $ARK_API_KEY"
```

注意：已排队的任务将被取消；已完成、失败或过期的任务将从历史记录中删除。正在执行和已取消的任务无法被删除。

### 生成连续视频（使用上一帧）

在第一个任务中设置 `return_last_frame: true`，然后使用返回的 `last_frame_url` 作为下一个任务的第一帧。

```bash
# Get last frame URL from completed task
LAST_FRAME_URL=$(curl -s -X GET "https://ark.ap-southeast.bytepluses.com/api/v3/contents/generations/tasks/${TASK_ID}" \
  -H "Authorization: Bearer $ARK_API_KEY" | python3 -c "import sys,json; print(json.load(sys.stdin)['content']['last_frame_url'])")

# Use it as first frame for the next video
# ... (use Mode B with LAST_FRAME_URL as the image URL)
```

### 草图模式（仅限 Seedance 1.5 Pro）

首先生成一个低成本的预览视频，如果满意后再生成最终版本：

```bash
# Step 1: Create draft (forces 480p)
DRAFT_RESULT=$(curl -s -X POST "https://ark.ap-southeast.bytepluses.com/api/v3/contents/generations/tasks" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $ARK_API_KEY" \
  -d '{
    "model": "seedance-1-5-pro-251215",
    "content": [
      { "type": "text", "text": "YOUR_PROMPT_HERE" }
    ],
    "draft": true,
    "resolution": "480p"
  }')
DRAFT_TASK_ID=$(echo "$DRAFT_RESULT" | python3 -c "import sys,json; print(json.load(sys.stdin)['id'])")

# Step 2: After draft succeeds, generate final video from draft
FINAL_RESULT=$(curl -s -X POST "https://ark.ap-southeast.bytepluses.com/api/v3/contents/generations/tasks" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $ARK_API_KEY" \
  -d '{
    "model": "seedance-1-5-pro-251215",
    "content": [
      {
        "type": "draft_task",
        "draft_task": { "id": "'"$DRAFT_TASK_ID"'" }
      }
    ],
    "resolution": "720p"
  }')
```

## 图片要求

- 格式：JPEG、PNG、WebP、BMP、TIFF、GIF（Seedance 1.5 Pro 还支持 HEIC、HEIF）
- 宽高比：介于 0.4 和 2.5 之间
- 较短边必须大于 300 像素，较长边必须小于 6000 像素
- 最大文件大小：30 MB

## 分辨率和宽高比

| 分辨率 | 宽高比 | Seedance 1.0 系列（宽度 x 高度） | Seedance 1.5 Pro（宽度 x 高度） |
|-----------|-------|------------------------------|---------------------------|
| 480p | 16:9 | 864x480 | 864x496 |
| 480p | 1:1 | 640x640 | 640x640 |
| 480p | 9:16 | 480x864 | 496x864 |
| 720p | 16:9 | 1248x704 | 1280x720 |
| 720p | 1:1 | 960x960 | 960x960 |
| 720p | 9:16 | 704x1248 | 720x1280 |
| 1080p | 16:9 | 1920x1088 | 1920x1080 |
| 1080p | 1:1 | 1440x1440 | 1440x1440 |
| 1080p | 9:16 | 1088x1920 | 1080x1920 |

## 通过 Feishu 应用发送视频（OpenClaw）

请参阅 [how_to_send_video_via_feishu_app.md](how_to_send_video_via_feishu_app.md)

## 规则

1. **在执行 API 调用之前**，务必检查 `ARK_API_KEY` 是否已设置：`[ -z "$ARK_API_KEY" ] && echo "Error: ARK_API_KEY not set" && exit 1`
2. **默认使用 Seedance 1.5 Pro`（`seedance-1-5-pro-251215`），除非用户请求特定的模型。
3. **文本转视频时，默认分辨率为 720p、16:9、时长 5 秒，并包含音频**。
4. **图片转视频时，默认使用自适应宽高比**（根据输入图片自动调整）。
5. **状态检查间隔**：每 15 秒轮询一次。
6. **视频 URL 在 24 小时后失效**——生成后立即下载。
7. **任务历史记录仅保留 7 天**。
8. 对于本地图片文件，在发送之前需要将其转换为 Base64 数据 URL 格式。
9. 始终向用户显示任务 ID，以便他们稍后查看任务状态。
10. 如果生成失败，要清晰显示错误信息并提供可能的解决方法。