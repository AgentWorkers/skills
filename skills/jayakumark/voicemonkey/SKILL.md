---
name: voicemonkey
description: 通过 VoiceMonkey API v2 控制 Alexa 设备：发布公告、触发例程、启动操作流程以及播放媒体内容。
homepage: https://voicemonkey.io
metadata: {"clawdbot":{"emoji":"🐒","requires":{"env":["VOICEMONKEY_TOKEN"]},"primaryEnv":"VOICEMONKEY_TOKEN"}}
---

# VoiceMonkey

通过 VoiceMonkey API v2 控制 Alexa/Echo 设备。可以进行文本转语音（TTS）播报、触发 Alexa 任务、启动流程，并在 Echo Show 设备上显示图片/视频。

## 设置

1. 从 [Voice Monkey 控制台](https://console.voicemonkey.io) → 设置 → API 凭据中获取您的秘密令牌。
2. 设置环境变量：
   ```bash
   export VOICEMONKEY_TOKEN="your-secret-token"
   ```
   或将其添加到 `~/.clawdbot/clawdbot.json` 文件中：
   ```json
   {
     "skills": {
       "entries": {
         "voicemonkey": {
           "env": { "VOICEMONKEY_TOKEN": "your-secret-token" }
         }
       }
     }
   }
   ```
3. 在 Voice Monkey 控制台的设置 → 设备中查找您的设备 ID。

## API 基本 URL

```
https://api-v2.voicemonkey.io
```

## 播报 API

在 Alexa 设备上进行文本转语音播报、播放音频/视频或显示图片。

**端点：** `https://api-v2.voicemonkey.io/announcement`

### 基本文本转语音播报

```bash
curl -X GET "https://api-v2.voicemonkey.io/announcement?token=$VOICEMONKEY_TOKEN&device=YOUR_DEVICE_ID&text=Hello%20from%20Echo"
```

### 带授权头（推荐）

```bash
curl -X POST "https://api-v2.voicemonkey.io/announcement" \
  -H "Authorization: $VOICEMONKEY_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "device": "YOUR_DEVICE_ID",
    "text": "Hello from Echo the Fox!"
  }'
```

### 带语音和提示音

```bash
curl -X POST "https://api-v2.voicemonkey.io/announcement" \
  -H "Authorization: $VOICEMONKEY_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "device": "YOUR_DEVICE_ID",
    "text": "Dinner is ready!",
    "voice": "Brian",
    "chime": "soundbank://soundlibrary/alarms/beeps_and_bloops/bell_02"
  }'
```

### 在 Echo Show 上显示图片

```bash
curl -X POST "https://api-v2.voicemonkey.io/announcement" \
  -H "Authorization: $VOICEMONKEY_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "device": "YOUR_DEVICE_ID",
    "text": "Check out this image",
    "image": "https://example.com/image.jpg",
    "media_width": "100",
    "media_height": "100",
    "media_scaling": "best-fit"
  }'
```

### 播放音频文件

```bash
curl -X POST "https://api-v2.voicemonkey.io/announcement" \
  -H "Authorization: $VOICEMONKEY_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "device": "YOUR_DEVICE_ID",
    "audio": "https://example.com/sound.mp3"
  }'
```

### 在 Echo Show 上播放视频

```bash
curl -X POST "https://api-v2.voicemonkey.io/announcement" \
  -H "Authorization: $VOICEMONKEY_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "device": "YOUR_DEVICE_ID",
    "video": "https://example.com/video.mp4",
    "video_repeat": 1
  }'
```

### 在 Echo Show 上打开网页

```bash
curl -X POST "https://api-v2.voicemonkey.io/announcement" \
  -H "Authorization: $VOICEMONKEY_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "device": "YOUR_DEVICE_ID",
    "website": "https://example.com",
    "no_bg": "true"
  }'
```

### 播报参数

| 参数 | 是否必填 | 说明 |
|-----------|----------|-------------|
| `token` | 是* | 秘密令牌（*或使用授权头） |
| `device` | 是 | 来自 Voice Monkey 控制台的设备 ID |
| `text` | 否 | 文本内容（支持 SSML 格式） |
| `voice` | 否 | 用于文本转语音的语音（详情请参阅 API 测试平台） |
| `language` | 否 | 语言代码，用于优化发音 |
| `chime` | 否 | 提示音的音频 URL 或 Alexa 的内置声音 |
| `audio` | 否 | 需要播放的音频文件的 HTTPS URL |
| `background_audio` | 否 | 在文本转语音播放时背景音的音频 |
| `image` | 否 | 用于 Echo Show 的图片的 HTTPS URL |
| `video` | 否 | 用于 Echo Show 的 MP4 视频的 HTTPS URL |
| `video_repeat` | 否 | 视频循环播放的次数 |
| `website` | 否 | 在 Echo Show 上打开的网页 URL |
| `no_bg` | 否 | 设置为 "true" 可隐藏 Voice Monkey 的品牌标识 |
| `media_width` | 否 | 图片宽度 |
| `media_height` | 否 | 图片高度 |
| `media_scaling` | 否 | 图片缩放方式 |
| `media_align` | 否 | 图片对齐方式 |
| `media_radius` | 否 | 图片裁剪的圆角半径 |
| `var-[name]` | 否 | 更新 Voice Monkey 的内部变量 |

## 触发 Alexa 任务 API

触发 VoiceMonkey 设备以执行 Alexa 任务。

**端点：** `https://api-v2.voicemonkey.io/trigger`

```bash
curl -X POST "https://api-v2.voicemonkey.io/trigger" \
  -H "Authorization: $VOICEMONKEY_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "device": "YOUR_TRIGGER_DEVICE_ID"
  }'
```

| 参数 | 是否必填 | 说明 |
|-----------|----------|-------------|
| `token` | 是* | 秘密令牌（*或使用授权头） |
| `device` | 是 | 需要触发的设备 ID |

## 启动流程 API

启动 VoiceMonkey 的流程。

**端点：** `https://api-v2.voicemonkey.io/flows`

```bash
curl -X POST "https://api-v2.voicemonkey.io/flows" \
  -H "Authorization: $VOICEMONKEY_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "device": "YOUR_DEVICE_ID",
    "flow": 12345
  }'
```

| 参数 | 是否必填 | 说明 |
|-----------|----------|-------------|
| `token` | 是* | 秘密令牌（*或使用授权头） |
| `device` | 是 | 设备 ID |
| `flow` | 是 | 来自 Voice Monkey 控制台的流程 ID |

## 媒体要求

### 图片
- 支持常见的图片格式（JPG、PNG 等）
- **禁止使用动画 GIF**
- 优化文件大小以提高加载速度
- 必须托管在具有有效 SSL 证书的 HTTPS URL 上
- CORS 设置必须允许通配符：`Access-Control-Allow-Origin: *`

### 视频
- **仅支持 MP4 格式**（MPEG-4 Part-14）
- 音频编码格式：AAC、MP3
- 最大分辨率：1080p @30fps 或 @60fps
- 必须托管在具有有效 SSL 证书的 HTTPS URL 上

### 音频
- 格式：AAC、MP3、OGG、Opus、WAV
- 比特率：≤ 1411.20 kbps
- 样本率：≤ 48kHz
- 文件大小：≤ 10MB
- 总响应时长：≤ 240 秒

## SSML 示例

在 `text` 参数中使用 SSML 格式以实现更丰富的播报效果：

```xml
<speak>
  <amazon:emotion name="excited" intensity="high">
    This is exciting news!
  </amazon:emotion>
</speak>
```

```xml
<speak>
  The time is <say-as interpret-as="time">3:30pm</say-as>
</speak>
```

## 注意事项

- 请妥善保管您的秘密令牌；如果令牌被盗用，请通过控制台 → 设置 → API 凭据进行更换。
- 使用 [API 测试平台](https://console.voicemonkey.io) 测试和探索各种功能。
- 高级会员可以直接在 VoiceMonkey 控制台中上传媒体文件。
- 在发送播报内容前请务必确认，以避免意外出现噪音。