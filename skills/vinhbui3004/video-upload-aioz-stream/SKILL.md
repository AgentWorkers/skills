---
name: aioz-stream-video-upload
description: **快速将视频上传至 AIOZ Stream API**：  
1. 使用默认或自定义的编码配置创建视频对象；  
2. 上传视频文件；  
3. 完成上传过程；  
4. 最后将视频链接返回给用户。
metadata:
  openclaw:
    emoji: "🎬"
    requires:
      bins: 
        - curl
        - jq
        - md5sum
---

# AIOZ Stream 视频上传

使用 API 密钥认证，快速将视频上传到 AIOZ Stream。完整的上传流程需要执行 3 次 API 调用：创建视频对象 → 上传文件部分 → 完成上传。

## 适用场景

- 用户希望在 AIOZ Stream 上上传或创建视频。
- 用户提到“上传视频”、“创建视频”或“AIOZ Stream 视频”。
- 用户需要获取视频的 HLS/DASH 流媒体链接。

## 认证

本功能使用 API 密钥进行认证。用户需要提供以下密钥：
- `stream-public-key`：AIOZ Stream 的公钥。
- `stream-secret-key`：AIOZ Stream 的私钥。
如果用户未提供这些密钥，请向他们索取。这些密钥将作为 HTTP 请求头在所有 API 调用中传递。

## 使用选项

当用户需要上传视频时，可以选择以下方式：

### 选项 1：默认上传（快速）

仅使用最基本的配置（例如视频标题）创建视频对象，然后上传文件。
示例用户提示：
> “上传视频文件 /path/to/video.mp4，标题为‘我的视频’。”

### 选项 2：自定义上传（高级）

使用完整的编码配置创建视频对象，包括分辨率（240p、360p、480p、720p、1080p、1440p、2160p、4320p）、编码格式（h264、h265）、比特率、容器类型、标签、元数据等，然后上传文件。
示例用户提示：
> “使用自定义配置上传视频：标题为‘我的教程’，分辨率设置为 720p 和 1080p，编码格式为 h264，标签为 tutorial、education。”

## 完整上传流程（3 步）

### 第 1 步：创建视频对象

**默认方式：**
```bash
curl -s -X POST 'https://api-w3stream.attoaioz.cyou/api/videos/create' \
  -H 'stream-public-key: PUBLIC_KEY' \
  -H 'stream-secret-key: SECRET_KEY' \
  -H 'Content-Type: application/json' \
  -d '{
    "title": "VIDEO_TITLE"
  }'
```

**自定义方式（包含编码配置）：**
```bash
curl -s -X POST 'https://api-w3stream.attoaioz.cyou/api/videos/create' \
  -H 'stream-public-key: PUBLIC_KEY' \
  -H 'stream-secret-key: SECRET_KEY' \
  -H 'Content-Type: application/json' \
  -d '{
    "title": "VIDEO_TITLE",
    "description": "DESCRIPTION",
    "is_public": true,
    "tags": ["tag1", "tag2"],
    "metadata": [
      {"key": "KEY", "value": "VALUE"}
    ],
    "qualities": [
      {
        "resolution": "1080p",
        "type": "hls",
        "container_type": "mpegts",
        "video_config": {
          "codec": "h264",
          "bitrate": 5000000,
          "index": 0
        },
        "audio_config": {
          "codec": "aac",
          "bitrate": 192000,
          "channels": "2",
          "sample_rate": 48000,
          "language": "en",
          "index": 0
        }
      },
      {
        "resolution": "720p",
        "type": "hls",
        "container_type": "mpegts",
        "video_config": {
          "codec": "h264",
          "bitrate": 3000000,
          "index": 0
        },
        "audio_config": {
          "codec": "aac",
          "bitrate": 128000,
          "channels": "2",
          "sample_rate": 44100,
          "language": "en",
          "index": 0
        }
      }
    ]
  }'
```

响应中会返回 `data.id`，这是后续步骤中使用的 `VIDEO_ID`。

### 第 2 步：上传文件部分

将实际的视频文件二进制数据上传到已创建的视频对象中。

首先，获取文件大小并计算其 MD5 哈希值：
```bash
# Get file size (cross-platform compatible)
FILE_SIZE=$(stat -f%z /path/to/video.mp4 2>/dev/null || stat -c%s /path/to/video.mp4)
END_POS=$((FILE_SIZE - 1))

# Compute MD5 hash
HASH=$(md5sum /path/to/video.mp4 | awk '{print $1}')
```

然后使用 `multipart form-data` 方式上传文件，并设置 `Content-Range` 头：
```bash
curl -s -X POST "https://api-w3stream.attoaioz.cyou/api/videos/VIDEO_ID/part" \
  -H 'stream-public-key: PUBLIC_KEY' \
  -H 'stream-secret-key: SECRET_KEY' \
  -H "Content-Range: bytes 0-$END_POS/$FILE_SIZE" \
  -F "file=@/path/to/video.mp4" \
  -F "index=0" \
  -F "hash=$HASH"
```

**注意：** 必须设置 `Content-Range` 头才能成功上传。格式为：`bytes {start}-{end}/{total_size}`，其中：
- 对于单部分上传：`start=0`，`end=file_size-1`，`total_size=file_size`。
- 对于多部分上传（文件大于 50MB）：为每个文件块调整 `start` 和 `end` 的值（每个文件块的大小通常为 50MB 至 200MB）。
`multipart form-data` 的字段包括：
- `file`：视频文件二进制数据（使用 `@/path/to/file`）。
- `index`：0（单部分上传时使用；多部分上传时递增）。
- `hash`：文件部分的 MD5 哈希值。

### 第 3 步：完成上传

上传文件部分后，调用完成上传的 API 端点：
```bash
curl -s -X GET "https://api-w3stream.attoaioz.cyou/api/videos/VIDEO_ID/complete" \
  -H 'accept: application/json' \
  -H 'stream-public-key: PUBLIC_KEY' \
  -H 'stream-secret-key: SECRET_KEY'
```

这将触发视频的转码过程，此时上传视为成功完成。

## 上传完成后获取视频链接

上传完成后，获取视频详细信息以获取流媒体链接：
```bash
curl -s 'https://api-w3stream.attoaioz.cyou/api/videos/VIDEO_ID' \
  -H 'stream-public-key: PUBLIC_KEY' \
  -H 'stream-secret-key: SECRET_KEY'
```

解析响应，从 `assets` 或 `hls` 字段中提取 HLS/DASH 链接，并将其返回给用户。

## 自定义上传配置参考

### 支持的分辨率：
- `240p` — 426 × 240（最大比特率：700,000 bps）
- `360p` — 640 × 360（最大比特率：1,200,000 bps）
- `480p` — 854 × 480（最大比特率：2,000,000 bps）
- `720p` — 1280 × 720（高清）（最大比特率：4,000,000 bps）
- `1080p` — 1920 × 1080（全高清）（最大比特率：6,000,000 bps）
- `1440p` — 2560 × 1440（2K/QHD）（最大比特率：12,000,000 bps）
- `2160p` — 3840 × 2160（4K/UHD）（最大比特率：30,000,000 bps）
- `4320p` — 7680 × 4320（8K/UHD-2）（最大比特率：60,000,000 bps）

### 流媒体格式（`type` 字段）：
- `hls` — HTTP 直播流（容器格式：`mpegts` 或 `mp4`）
- `dash` — 动态自适应流媒体（容器格式：`fmp4`）

### 容器类型：
- HLS：`mpegts` 或 `mp4`
- DASH：`fmp4`

**Apple HLS 兼容性：**
- H.265/HEVC 仅支持 `mp4` 容器的 HLS 格式（使用 fMP4/CMAF 分段）。
- H.265 使用 `mpegts` 格式在 Apple 平台上不支持。
- H.264 支持 `mpegts` 和 `mp4` 两种容器格式。

### 视频配置：
- `codec`：`h264`（最高支持 4K）或 `h265`（最高支持 8K）。
- `bitrate`：以比特/秒为单位（具体数值参见分辨率表）。
- `index`：0（默认视频轨道）。

### 音频配置：
- `codec`：`aac`（唯一支持的编码格式）。
- `bitrate`：建议使用 128,000 至 256,000 bps。
- `channels`：`2`（立体声）。
- `sample_rate`：8000、11025、16000、22050、32000、44100、48000、88200、96000。
- `language`：BCP 47 语言代码（例如 `en`、`vi`）。
- `index`：0（默认音频轨道）。
- **推荐音频比特率：**
  - 标准：128,000 – 192,000 bps。
  - 高质量：192,000 – 256,000 bps。

### 推荐采样率：
- 语音：22050 或 32000。
- 音乐/视频：44100 或 48000。

## 高级配置

### 仅视频输出
仅指定 `video_config`，不指定 `audio_config`：
```json
{
  "resolution": "720p",
  "type": "hls",
  "container_type": "mpegts",
  "video_config": {
    "codec": "h264",
    "bitrate": 3000000,
    "index": 0
  }
}
```

### 仅音频输出
仅指定 `audio_config`，不指定 `video_config`：
```json
{
  "resolution": "audio",
  "type": "hls",
  "container_type": "mpegts",
  "audio_config": {
    "codec": "aac",
    "bitrate": 192000,
    "channels": "2",
    "sample_rate": 48000,
    "language": "en",
    "index": 0
  }
}
```

## 响应处理
1. 解析创建视频对象的 JSON 响应，提取 `data.id`。
2. 计算视频文件的 MD5 哈希值。
3. 使用哈希值上传文件部分。
4. 调用完成上传的 API 端点。
5. 获取视频详细信息以获取流媒体链接。
6. 将视频链接返回给用户。
7. 如果视频仍在转码中（状态显示为“transcoding”），通知用户并建议稍后再试。

## 错误处理
- **401**：API 密钥无效——请用户验证其公钥和私钥。
- **400**：请求格式错误——检查请求体格式，确保分辨率不超过源视频的分辨率。
- **500**：服务器错误——建议重试。

## 示例交互流程
1. 用户：“将我的视频上传到 AIOZ Stream。”
2. 如果用户未提供 API 密钥，请求公钥和私钥。
3. 询问视频文件路径。
4. 询问用户：“选择默认上传（快速）还是自定义配置？”
   - 如果选择默认方式：询问视频标题。
   - 如果选择自定义配置：询问视频标题、分辨率（如 720p、1080p）、编码格式偏好、标签等。
5. **第 1 步**：创建视频对象 → 获取 `VIDEO_ID`。
6. **第 2 步**：计算文件哈希值并上传文件部分。
7. **第 3 步**：调用完成上传的 API 端点。
8. 获取视频详细信息并返回流媒体链接。

## 其他功能

### 计算转码费用
在上传前，估算转码成本：
```bash
curl -s 'https://api-w3stream.attoaioz.cyou/api/videos/cost?duration=60&qualities=360p,1080p' \
  -H 'stream-public-key: PUBLIC_KEY' \
  -H 'stream-secret-key: SECRET_KEY'
```

### 上传缩略图
创建视频后，上传自定义缩略图：
```bash
curl -s -X POST "https://api-w3stream.attoaioz.cyou/api/videos/VIDEO_ID/thumbnail" \
  -H 'stream-public-key: PUBLIC_KEY' \
  -H 'stream-secret-key: SECRET_KEY' \
  -F 'file=@/path/to/thumbnail.jpg'
```

支持的格式：`.png`、`.jpg`。

### 更新视频对象
创建视频后修改其元数据：
```bash
curl -s -X PATCH "https://api-w3stream.attoaioz.cyou/api/videos/VIDEO_ID" \
  -H 'stream-public-key: PUBLIC_KEY' \
  -H 'stream-secret-key: SECRET_KEY' \
  -H 'Content-Type: application/json' \
  -d '{
    "title": "Updated Title",
    "description": "Updated description",
    "tags": ["new", "tags"],
    "is_public": true
  }'
```

### 列出所有视频
根据条件筛选并列出所有视频：
```bash
curl -s -X POST 'https://api-w3stream.attoaioz.cyou/api/videos' \
  -H 'stream-public-key: PUBLIC_KEY' \
  -H 'stream-secret-key: SECRET_KEY' \
  -H 'Content-Type: application/json' \
  -d '{
    "limit": 10,
    "offset": 0,
    "sort_by": "created_at",
    "order_by": "desc",
    "status": "done"
  }'
```

### 删除视频
删除视频：
```bash
curl -s -X DELETE "https://api-w3stream.attoaioz.cyou/api/videos/VIDEO_ID" \
  -H 'stream-public-key: PUBLIC_KEY' \
  -H 'stream-secret-key: SECRET_KEY'
```