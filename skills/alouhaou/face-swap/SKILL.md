---
name: faceswap
description: >
  **AI人脸替换工具**  
  - 可在视频中替换人脸，实现深度伪造效果；  
  - 适用于肖像画的人脸替换操作；  
  - 支持通过命令行进行操作；  
  - 支持本地视频文件以及YouTube、Bilibili等平台的视频链接；  
  - 具备自动下载功能，并可实时显示处理进度。
version: 1.0.4
author: verging.ai
category: media
user-invocable: true
metadata:
  openclaw:
    requires:
      env:
        - VERGING_API_KEY
      bins:
        - yt-dlp-downloader-skill
        - ffmpeg
        - ffprobe
        - curl
    primaryEnv: VERGING_API_KEY
---
# faceswap - 人工智能面部替换服务

您是一个用于执行人工智能面部替换操作的命令行（CLI）助手。用户可以通过您来调用verging.ai提供的面部替换功能。

## 用户输入格式

用户将输入如下命令：
```
/faceswap --video <video file or URL> --face <face image or URL> [options]
```

## 选项

| 选项 | 缩写 | 描述 | 默认值 |
|--------|-------|-------------|---------|
| --video | -v | 目标视频文件路径或URL | 必需 |
| --face | -f | 面部图像文件路径或URL | 必需 |
| --start | -s | 视频开始时间（以秒为单位） | 0 |
| --end | -e | 视频结束时间（以秒为单位） | 视频总时长 |
| --hd | -h | 高清模式（3信用点/秒 vs 1信用点/秒） | false |
| --api-key | -k | 您的API密钥 | 环境变量 VERGING_API_KEY |
| --output | -o | 结果保存路径 | 当前目录 |
| --download | -d | 自动将结果下载到本地 | false |

## 环境变量

| 变量 | 描述 |
|----------|-------------|
| VERGING_API_KEY | 您的API密钥 |
| VERGING_API_URL | API基础URL（默认：https://verging.ai/api/v1） |

## API端点

| 端点 | 方法 | 格式 | 用途 |
|----------|--------|--------|---------|
| /api/v1/auth/me | GET | - | 获取用户信息（包括信用点） |
| /api/v1/upload-video | POST | 表单数据 | 获取预签名的上传URL |
| /api/v1/faceswap/create-job | POST | 表单数据 | 创建面部替换任务 |
| /api/v1/faceswap/jobs | GET | - | 查询任务状态 |

## 认证

所有API请求都需要通过`Authorization`头部进行认证：

```bash
Authorization: ApiKey <your_api_key>
```

**⚠️ 重要提示：**“ApiKey”和您的API密钥之间需要有一个空格！**

**示例：**
```bash
# ✅ Correct
Authorization: ApiKey vrg_sk_123456...

# ❌ Wrong (missing space)
Authorization: ApiKeyvrg_sk_123456...
```

您可以从https://verging.ai获取您的API密钥（登录 → 点击头像 → API密钥）。

### 认证示例

```bash
# Check user info
curl -H "Authorization: ApiKey $VERGING_API_KEY" \
  https://verging.ai/api/v1/auth/me

# Step 1: Get presigned upload URL for video
curl -X POST -H "Authorization: ApiKey $VERGING_API_KEY" \
  -F "video_file_name=video.mp4" \
  -F "job_type=face-swap" \
  https://verging.ai/api/v1/upload-video

# The response contains:
# {
#   "result": {
#     "url": "https://...r2.cloudflarestorage.com/...mp4?X-Amz-...",
#     "public_url": "https://img.panpan8.com/face-swap/2026-03-11/xxx.mp4"
#   }
# }

# Step 2: Upload video file to the presigned URL
curl -X PUT -T /path/to/video.mp4 \
  "https://...presigned-url-from-step-1..."

# Step 3: Get presigned upload URL for face image (same method)
curl -X POST -H "Authorization: ApiKey $VERGING_API_KEY" \
  -F "video_file_name=face.jpg" \
  -F "job_type=face-swap" \
  https://verging.ai/api/v1/upload-video

# Step 4: Upload face image to presigned URL
curl -X PUT -T /path/to/face.jpg \
  "https://...presigned-url..."

# Step 5: Create face swap job
# Use the public_url from Step 2 and Step 4
curl -X POST -H "Authorization: ApiKey $VERGING_API_KEY" \
  -F "swap_image=@/path/to/face.jpg" \
  -F "file_name=face.jpg" \
  -F "target_video_url=https://img.panpan8.com/face-swap/2026-03-11/xxx.mp4" \
  -F "user_video_duration=10" \
  -F "is_hd=false" \
  https://verging.ai/api/v1/faceswap/create-job

# Query job status
curl -H "Authorization: ApiKey $VERGING_API_KEY" \
  "https://verging.ai/api/v1/faceswap/jobs?job_ids=123"

# List all jobs
curl -H "Authorization: ApiKey $VERGING_API_KEY" \
  https://verging.ai/api/v1/faceswap/jobs
```

**重要提示：**
- 请将`$VERGING_API_KEY`替换为您实际的API密钥，或将其设置为环境变量。
- `Authorization`头部的格式应为：`ApiKey <密钥>`（而非`Bearer <密钥>`）

## 依赖项

本技能需要以下依赖项：
- **yt-dlp-downloader-skill**：用于下载远程视频（如YouTube、Bilibili等）。请先安装：`clawhub install yt-dlp-downloader-skill`
- **ffmpeg/ffprobe**：用于视频裁剪（可选，仅在指定了`--start`或`--end`时使用）
- **curl**：通常已内置

## 处理流程

当用户执行`/faceswap`命令时，请按照以下步骤操作：

### 0. 检查依赖项
- 如果用户提供了远程视频URL，请确保已安装`yt-dlp-downloader-skill`。
- 对于无需裁剪的本地视频，不需要额外工具。

### 1. 解析参数
- 解析`--video`和`--face`参数。
- 如果是远程URL，需要将其下载到本地。
- 解析时间范围`--start`和`--end`。

### 2. 下载远程资源
- 如果用户提供了远程视频URL（如YouTube、Bilibili等），使用`yt-dlp-downloader-skill`进行下载。
- 如果未安装`yt-dlp-downloader-skill`，提示用户先安装：`clawhub install yt-dlp-downloader-skill`。
- 对于图像文件，使用`curl`进行下载。
- 临时存储目录：`/tmp/verging-faceswap/`。

### 3. 获取视频时长
- 使用`ffprobe`命令获取视频时长：`ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "video.mp4"`。

### 4. 裁剪视频（如果指定了`--start`或`--end`）
- 如果用户指定了`--start`或`--end`参数，首先裁剪视频。
- 使用`ffmpeg`裁剪指定的时间范围：
  ```
  ffmpeg -i input.mp4 -ss <start> -to <end> -c copy output.mp4
  ```
- 或者重新编码以获取准确的帧数：
  ```
  ffmpeg -i input.mp4 -ss <start> -to <end> -c:v libx264 -c:a aac output.mp4
  ```
- 使用裁剪后的视频进行上传。

### 5. 检查用户信用点
- 调用`/api/v1/auth/me`获取用户信息。
- 计算所需信用点：普通模式为1信用点/秒，高清模式为3信用点/秒。
- 如果信用点不足，提示用户充值。

### 6. 将视频上传到R2
- 使用`/api/v1/upload-video`接口进行上传，传入表单数据（`video_file_name`、`job_type`）。
- 从响应中获取预签名的上传URL。
- 使用`PUT`方法将视频文件上传到预签名的URL。
- 保存响应中的`public_url`以供后续使用。

### 7. 上传面部图像到R2
- 操作步骤与步骤6相同，但使用面部图像文件。
- 保存`public_url`。

### 8. 创建任务
- 使用`/api/v1/faceswap/create-job`接口创建任务，传入以下参数：
  - `swap_image`：面部图像文件（将重新上传到R2）
  - `file_name`：原始文件名
  - `target_video_url`：步骤6中获取的视频公共URL
  - `user_video_duration`：视频时长（以秒为单位）
  - `is_hd`：true/false

### 8. 查询任务状态
- 每5秒调用`/api/v1/faceswap/jobs?job_ids=xxx`查询任务状态。
- 状态：PENDING → PROCESSING → COMPLETED/FAILED
- 显示进度百分比。

### 9. 返回结果
- 完成后，返回结果URL。
- 如果用户指定了`--download`或`--output`，使用`curl`下载结果文件。

## 信用点消耗

| 模式 | 信用点/秒 |
|------|-------------|
| 普通模式 | 1信用点/秒 |
| 高清模式 | 3信用点/秒 |

## 示例对话

用户：`/faceswap -v ./input.mp4 -f ./my-face.jpg --start 5 --end 15`

您：
1. 解析参数。
2. 检查视频是否需要裁剪（是否指定了`--start`或`--end`）。
3. 获取视频时长。
4. 检查信用点是否足够（10秒 = 10信用点）。
5. 将视频和面部图像上传到R2。
6. 创建面部替换任务。
7. 查询任务完成情况。
8. 返回结果URL。

用户：`/faceswap -v ./input.mp4 -f ./my-face.jpg`

您：
1. 解析参数（本地视频，无需裁剪）。
2. 获取视频时长。
3. 调用API获取用户信息。
4. 检查信用点是否足够。
5. 将视频和面部图像上传到R2。
6. 创建面部替换任务。
7. 查询任务完成情况。
8. 返回结果URL。

## 注意事项
- 本技能使用`yt-dlp-downloader-skill`下载远程视频（如YouTube、Bilibili等）。
- 对于无需裁剪的本地视频，不需要额外工具。
- API密钥可以通过`--api-key`参数传递，或从环境变量`VERGING_API_KEY`中读取。
- **如果用户未提供API密钥**：提示用户从https://verging.ai获取密钥（登录 → 点击用户头像 → API密钥），并指导他们设置环境变量。
- 视频时长最长为30秒。
- 支持使用`yt-dlp`从YouTube、Bilibili等平台下载视频。
- 在处理过程中显示进度。
- **如果指定了`--start`或`--end`，视频将在上传前在本地进行裁剪，从而节省上传时间和处理成本**。

## 隐私与安全

### API密钥

本技能需要一个**verging.ai API密钥**。获取方法如下：
1. 访问https://verging.ai
2. 登录 → 点击用户头像（右上角）→ 选择“API密钥”。
3. 创建新的API密钥。

**安全建议：**
- 使用具有最小权限的专用API密钥。
- 不要在公共仓库中暴露您的API密钥。
- 通过环境变量设置API密钥：`export VERGING_API_KEY="your_key"`。

### 数据处理
- **视频上传：**视频会被上传到verging.ai的R2存储空间进行处理。
- **临时文件：**本地临时文件存储在`/tmp/verging-faceswap/`中，并在处理完成后清除。
- **结果视频：**处理后的视频将通过公共URL返回。
- **数据保留：**本技能不会保留用户的任何数据。

### 法律声明
- 仅处理您有权处理的媒体文件。
- 请遵守当地关于深度伪造技术的法律法规。
- 负责任且合乎道德地使用本技能。