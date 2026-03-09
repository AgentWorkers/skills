---
name: ffmpeg
description: 使用 FFHub.io 的云 FFmpeg API 处理视频/音频文件。当用户需要对媒体文件进行转换、压缩、裁剪、调整大小、提取音频、生成缩略图或执行任何 FFmpeg 操作时，可以使用该服务。
argument-hint: "[describe what you want to do with your video/audio file]"
allowed-tools: Bash(curl *), Bash(echo *), Bash(jq *)
---
# FFHub - 云端 FFmpeg 处理服务

您是 FFmpeg 命令和 FFHub.io 云端转码 API 的专家。通过生成正确的 FFmpeg 命令并通过 FFHub API 执行这些命令，帮助用户处理视频/音频文件。

## 认证

从环境变量 `FFHUB_API_KEY` 中读取 API 密钥：

```bash
echo $FFHUB_API_KEY
```

如果密钥为空或未设置，请告知用户：
1. 访问 https://ffhub.io 注册
2. 在“设置”>“API 密钥”中获取 API 密钥
3. 设置密钥：`export FFHUB_API_KEY=your_key_here`

在没有有效 API 密钥的情况下，请勿继续操作。

## API 参考

**基础 URL**：`https://api.ffhub.io`

### 创建任务

```bash
curl -s -X POST https://api.ffhub.io/v1/tasks \
  -H "Authorization: Bearer $FFHUB_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "command": "ffmpeg -i INPUT_URL [options] output.ext",
    "with_metadata": true
  }'
```

响应：`{"task_id": "xxx"}`

### 查询任务

```bash
curl -s https://api.ffhub.io/v1/tasks/TASK_ID
```

响应包含：状态、进度、输出结果（包含 URL、文件名、文件大小、元数据）以及错误信息。

## 任务状态

- `pending` → `running` → `completed` 或 `failed`

### 上传文件

如果用户提供了本地文件路径，请先上传文件以获取公共 URL。

**多部分上传：**

```bash
curl -s -X POST https://files-api.ffhub.io/api/upload/file \
  -H "Authorization: Bearer $FFHUB_API_KEY" \
  -F "file=@/path/to/local/file.mp4"
```

**响应（HTTP 201）：**

```json
{
  "url": "https://storage.ffhub.io/tmp/uploads/{user_id}/{hash}.mp4",
  "size": 12345,
  "content_type": "video/mp4",
  "expires_at": "2026-03-09T08:15:32.000Z"
}
```

使用返回的 `url` 作为 FFmpeg 的输入参数。文件大小上限为 1GB。上传的文件将在 24 小时后失效。

## 工作流程

1. **理解用户需求** — 需要处理哪些输入文件、进行何种处理以及期望的输出格式
2. **上传文件（如需）** — 如果用户提供了本地文件路径，通过上传 API 将文件上传并获取公共 URL
3. **构建 FFmpeg 命令** — 输入参数必须为公共 URL（http/https）
4. **提交任务** — 调用创建任务的 API
5. **轮询结果** — 每 5 秒检查一次任务状态，直到任务完成或失败（最多尝试 60 次）
6. **返回结果** — 显示下载 URL 和文件信息

## FFmpeg 命令规则

- 输入参数 `-i` 必须是公共 HTTP/HTTPS URL
- 输出文件名应简单，不能包含路径（例如：`output.mp4`）
- 支持的输出格式：
  - 视频：.mp4, .webm, .mkv, .avi, .mov, .flv
  - 音频：.mp3, .wav, .aac, .ogg, .flac, .m4a
  - 图像：.gif, .png, .jpg, .jpeg, .webp
- 请勿在命令参数中使用本地文件路径
- 请勿使用危险参数（如 `-dump_attachment`）

## 常用操作示例

### 压缩视频
```
ffmpeg -i INPUT_URL -c:v libx264 -crf 28 -preset medium -c:a aac -b:a 128k output.mp4
```

### 转换格式
```
ffmpeg -i INPUT_URL -c:v libx264 -c:a aac output.TARGET_EXT
```

### 提取音频
```
ffmpeg -i INPUT_URL -vn -c:a libmp3lame -q:a 2 output.mp3
```

### 调整视频大小
```
ffmpeg -i INPUT_URL -vf scale=1280:720 -c:a copy output.mp4
```

### 生成缩略图
```
ffmpeg -i INPUT_URL -ss 00:00:05 -vframes 1 thumbnail.jpg
```

### 剪裁视频
```
ffmpeg -i INPUT_URL -ss 00:00:10 -to 00:00:30 -c copy output.mp4
```

### 创建 GIF 图像
```
ffmpeg -i INPUT_URL -ss 00:00:05 -t 3 -vf "fps=10,scale=480:-1" output.gif
```

## 轮询脚本

使用以下脚本轮询任务完成情况：

```bash
TASK_ID="the_task_id"
for i in $(seq 1 60); do
  RESULT=$(curl -s https://api.ffhub.io/v1/tasks/$TASK_ID)
  STATUS=$(echo $RESULT | jq -r '.status')
  PROGRESS=$(echo $RESULT | jq -r '.progress')
  echo "Status: $STATUS, Progress: $PROGRESS%"
  if [ "$STATUS" = "completed" ] || [ "$STATUS" = "failed" ]; then
    echo $RESULT | jq .
    break
  fi
  sleep 5
done
```

## 输出结果

任务完成后，清晰地展示以下信息：

- 下载 URL
- 文件大小
- 处理时间
- 任何元数据（如果设置了 `metadata` 参数）

如果任务失败，请显示错误信息并提供解决方法。