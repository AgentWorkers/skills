---
name: aioz-stream-audio-upload
description: 快速将音频文件上传至 AIOZ Stream API。可以使用默认或自定义的编码配置创建音频对象，上传文件，完成上传过程后，将音频文件的链接返回给用户。
metadata:
  openclaw:
    emoji: "🎵"
    requires:
      bins: 
        - curl
        - jq
        - md5sum
---

# AIOZ流媒体音频上传

使用API密钥认证，快速将音频文件上传到AIOZ Stream平台。整个上传流程需要执行3次API调用：创建音频对象 → 上传文件部分 → 完成上传。

## 适用场景

- 用户希望在AIOZ Stream平台上上传或创建音频文件
- 用户请求“上传音频”、“创建音频”或“获取音频的HLS流媒体链接”

## 认证方式

本功能采用API密钥认证。用户需要提供以下密钥：
- `stream-public-key`：AIOZ Stream平台的公钥
- `stream-secret-key`：AIOZ Stream平台的私钥
如果用户未提供这些密钥，请向他们索取。这些密钥将作为HTTP请求头的一部分被发送到所有API调用中。

## 使用选项

当用户需要上传音频时，可以选择以下两种方式之一：

### 选项1：默认上传（快速）

仅使用基本配置（如文件标题）创建音频对象，然后上传文件。

**示例用户提示：**
> “将音频文件 /path/to/audio.mp3 以‘My Podcast’为标题上传”

### 选项2：自定义上传（高级）

使用完整的编码配置（包括质量预设、比特率、采样率、元数据等）创建音频对象，然后上传文件。

**示例用户提示：**
> “使用自定义配置上传音频：标题为‘My Podcast’，选择最高质量的HLS流媒体格式，比特率为320kbps，采样率为48000Hz，并添加标签‘podcast,tech’”

## 完整上传流程（3个步骤）

### 第1步：创建音频对象

**默认方式：**
```bash
curl -s -X POST 'https://api-w3stream.attoaioz.cyou/api/videos/create' \
  -H 'stream-public-key: PUBLIC_KEY' \
  -H 'stream-secret-key: SECRET_KEY' \
  -H 'Content-Type: application/json' \
  -d '{
    "title": "AUDIO_TITLE",
    "type": "audio"
  }'
```

**自定义方式（包含编码配置）：**
```bash
curl -s -X POST 'https://api-w3stream.attoaioz.cyou/api/videos/create' \
  -H 'stream-public-key: PUBLIC_KEY' \
  -H 'stream-secret-key: SECRET_KEY' \
  -H 'Content-Type: application/json' \
  -d '{
    "title": "AUDIO_TITLE",
    "type": "audio",
    "description": "DESCRIPTION",
    "is_public": true,
    "tags": ["tag1", "tag2"],
    "metadata": [
      {"key": "KEY", "value": "VALUE"}
    ],
    "qualities": [
      {
        "resolution": "highest",
        "type": "hls",
        "container_type": "mpegts",
        "audio_config": {
          "codec": "aac",
          "bitrate": 320000,
          "channels": "2",
          "sample_rate": 48000,
          "language": "en",
          "index": 0
        }
      },
      {
        "resolution": "standard",
        "type": "hls",
        "container_type": "mpegts",
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

**注意：** 获取`data.id`，该ID将在后续步骤中用于识别音频对象。

### 第2步：上传文件部分

将音频文件的二进制数据上传到已创建的音频对象中。

首先，获取文件大小并计算其MD5哈希值：
```bash
# Get file size (cross-platform compatible)
FILE_SIZE=$(stat -f%z /path/to/audio.mp3 2>/dev/null || stat -c%s /path/to/audio.mp3)
END_POS=$((FILE_SIZE - 1))

# Compute MD5 hash
HASH=$(md5sum /path/to/audio.mp3 | awk '{print $1}')
```

然后通过multipart form-data方式上传文件，同时设置`Content-Range`头部：
```bash
curl -s -X POST "https://api-w3stream.attoaioz.cyou/api/videos/AUDIO_ID/part" \
  -H 'stream-public-key: PUBLIC_KEY' \
  -H 'stream-secret-key: SECRET_KEY' \
  -H "Content-Range: bytes 0-$END_POS/$FILE_SIZE" \
  -F "file=@/path/to/audio.mp3" \
  -F "index=0" \
  -F "hash=$HASH"
```

**重要提示：** 必须设置`Content-Range`头部才能成功上传文件。格式为：`bytes {start}-{end}/{total_size}`，其中：
- 对于单部分上传：`start=0`，`end=file_size-1`，`total_size=file_size`
- 对于多部分上传：需要为每个文件部分调整`start`和`end`的值

**multipart form-data`字段说明：**
- `file`：音频文件的二进制数据（使用`@/path/to/file`路径）
- `index`：0（单部分上传时使用；多部分上传时递增）
- `hash`：文件部分的MD5哈希值

### 第3步：完成上传

上传文件部分后，调用完成上传的API接口以完成整个上传过程：
```bash
curl -s -X GET "https://api-w3stream.attoaioz.cyou/api/videos/AUDIO_ID/complete" \
  -H 'accept: application/json' \
  -H 'stream-public-key: PUBLIC_KEY' \
  -H 'stream-secret-key: SECRET_KEY'
```

此时系统将开始对音频文件进行转码，上传操作视为成功完成。

## 上传完成后：获取音频链接

上传完成后，获取音频文件的详细信息以获取流媒体链接：
```bash
curl -s 'https://api-w3stream.attoaioz.cyou/api/videos/AUDIO_ID' \
  -H 'stream-public-key: PUBLIC_KEY' \
  -H 'stream-secret-key: SECRET_KEY'
```

从响应中解析`assets`或`hls`字段，将流媒体链接返回给用户。

**重要提示：** 音频文件不包含`mp4_url`字段，仅提供HLS/DASH格式的流媒体链接。

## 自定义上传配置参考

### 质量预设（`resolution`字段）：
- `standard`：标准质量
- `good`：较好质量
- `highest`：最高质量
- `lossless`：无损质量

### 流媒体格式（`type`字段）：
- `hls`：HTTP Live Streaming（容器格式：`mpegts`或`mp4`）
- `dash`：Dynamic Adaptive Streaming（容器格式：`fmp4`）

### 音频配置：
- `codec`：仅支持`aac`编码格式
- `bitrate`：以比特/秒为单位（例如：128000、256000、320000）
- `channels`：“2”（立体声）
- `sample_rate`：8000、11025、16000、22050、32000、44100、48000、88200、96000
- `language`：BCP 47编码语言（例如：`en`、`vi`）
- `index`：0

### 推荐的比特率：
- 播客/语音：64000 - 128000 bps
- 标准音乐：128000 - 192000 bps
- 高质量音乐：192000 - 256000 bps
- 最高质量音乐：256000 - 320000 bps

### 推荐的采样率：
- 语音：22050或32000 Hz
- 音乐：44100或48000 Hz

## 响应处理流程：
1. 解析创建音频对象的API响应，提取`data.id`
2. 计算音频文件的MD5哈希值
3. 使用该哈希值上传文件部分
4. 调用完成上传的API接口
5. 获取音频文件的详细信息以获取流媒体链接
6. 将流媒体链接返回给用户
7. 如果音频文件仍在转码中（状态为“transcoding”），通知用户并建议稍后再尝试

## 错误处理：
- **401**：API密钥无效——请用户重新验证公钥和私钥
- **400**：请求格式错误——检查请求体格式
- **500**：服务器错误——建议用户重试

## 示例交互流程：
1. 用户：“将我的音频文件上传到AIOZ Stream”
2. 如果用户未提供API密钥，请求用户提供公钥和私钥
3. 询问用户音频文件的路径
4. 询问用户选择上传方式：“默认上传（快速）”或“自定义配置？”
   - 如果选择默认方式，仅询问文件标题
   - 如果选择自定义配置，询问文件标题、质量预设、比特率、采样率等参数
5. **步骤1**：创建音频对象 → 获取`AUDIO_ID`
6. **步骤2**：计算文件哈希值并上传文件部分
7. **步骤3**：调用完成上传的API接口
8. 获取音频文件的流媒体链接并返回给用户