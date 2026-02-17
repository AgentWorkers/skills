---
name: minimax-to-telegram
description: >
  使用 MiniMax MCP 生成图片、音频和视频，并将其发送到 Telegram。  
  适用于用户希望使用 MiniMax 创建媒体内容并通过 Telegram 进行传输的场景。
---
# 设置（先决条件）

## 1. 安装 mcporter

```bash
# 如果未有 npm/npx
npm install -g mcporter
```

或者使用 `npx` 直接运行：
```bash
npx mcporter --help
```

## 2. 设置 MiniMax API 密钥

在终端中设置环境变量：

```bash
export MINIMAX_API_KEY="your-api-key-here"
```

或者在 `~/.mcporter/config.json` 文件中设置：

```json
{
  "env": {
    "MINIMAX_API_KEY": "your-api-key-here",
    "MINIMAX_RESOURCE_MODE": "url"
  }
}
```

## 3. 添加 MiniMax MCP 服务器

```bash
mcporter mcp add minimax-mcp
```

---

# MiniMax MCP 功能

使用 `mcporter` 来调用 MiniMax MCP 服务器提供的工具。

## 先决条件

- 已安装 `mcporter` 命令行工具
- `mcporter` 中已配置 MiniMax MCP 服务器

## 可用工具

| 工具 | 描述 |
|------|-------------|
| text_to_image | 根据文本提示生成图片 |
| text_to_audio | 将文本转换为语音（TTS） |
| generate_video | 根据文本提示生成视频 |
| image_to_video | 根据图片生成视频 |
| music_generation | 根据提示和歌词生成音乐 |
| voice_clone | 从音频文件中克隆声音 |
| voice_design | 根据描述生成声音 |
| list_voices | 列出可用的声音 ID |
| play_audio | 播放音频文件 |

## 基本用法

### 图片生成

```bash
mcporter call minimax-mcp.text_to_image prompt:"your prompt" aspectRatio:"4:3"
```

### 音频生成（TTS）

```bash
mcporter call minimax-mcp.text_to_audio text:"Hello world" voiceId:"male-qn-qingse"
```

### 视频生成

```bash
mcporter call minimax-mcp.generate_video prompt:"your video description"
```

## 发送到 Telegram

**重要提示**：当 MiniMax 返回一个 URL 时，该 URL 包含一个带有认证令牌的查询字符串。你必须使用包含所有查询参数的完整 URL。

**正确示例**（包含令牌的完整 URL）：
```
<MINIMAX_OUTPUT_URL>?Expires=xxx&OSSAccessKeyId=xxx&Signature=xxx
```

**错误示例**（不包含令牌的 URL）：
```
<MINIMAX_OUTPUT_URL>
```

### 将图片发送到 Telegram

1. 调用 `text_to_image` 并获取完整的 URL（包括查询字符串）。
2. 使用带有媒体参数的消息工具直接发送到 Telegram：

```python
message(
  action="send",
  channel="telegram",
  target="<chat_id>",
  media="<full_url_with_token>",
  message="Your caption"
)
```

### 将音频发送到 Telegram

方法相同——使用包含令牌的完整 URL：

```python
message(
  action="send",
  channel="telegram",
  target="<chat_id>",
  media="<full_url_with_token>",
  message="Your caption"
)
```

**重要提示**：在发送音频时，务必在音频下方添加文本内容作为消息标题！

示例：
```python
# Generate audio
audio_url = "<MINIMAX_AUDIO_URL>?Expires=xxx&Signature=xxx"
text_content = "呢段係你想既文字內容..."

# Send with both audio and text
message(
  action="send",
  channel="telegram",
  target="<chat_id>",
  media=audio_url,
  message=text_content  # Always include the text!
)
```

## 常见参数

### text_to_image
- prompt：所需图片的文本描述
- aspectRatio："1:1", "16:9", "4:3", "3:2", "2:3", "3:4", "9:16", "21:9"
- n：生成的图片数量（1-9）
- model：使用的模型（默认："image-01")

### text_to_audio
- text：要转换为语音的文本
- voiceId：声音 ID（例如："male-qn-qingse", "female-shaonv")
- speed：语音速度（0.5-2）
- emotion：情感类型（"happy", "sad", "angry", "fearful", "disgusted", "surprised", "neutral")
- format：音频格式（"mp3", "wav", "pcm", "flac")
- languageBoost：针对特定语言/方言增强识别效果
  - Cantonese："Chinese,Yue" 或 "Chinese"
  - Mandarin："Chinese" 或 "Chinese,Mandarin"
  - English："English"
  **生成粤语音频时必须添加此参数！**

### generate_video
- prompt：视频描述
- model：使用的模型（例如："T2V-01", "T2V-01-Director", "I2V-01", "I2V-01-Director", "I2V-01-live", "MiniMax-Hailuo-02"
- duration：视频时长（6 秒或 10 秒）
- resolution：视频分辨率（"768P", "1080P")

## 优化与故障排除

- **超时管理**：视频生成可能需要较长时间（高质量视频可能长达 20-30 分钟）。请始终为 `mcporter` 提供较大的 `--timeout` 值（例如 `--timeout 1800000`）以防止过早终止。
- **网关超时限制**：大多数 OpenClaw 配置的网关超时时间为 10 分钟（600000 毫秒）。为了避免被网关终止，请始终使用 `background: true` 参数运行 `generate_video`，或将其放在后台进程中执行。
- **模型选择**：使用 `MiniMax-Hailuo-02` 可生成更高质量的 10 秒视频。

## 错误处理

如果在发送到 Telegram 时遇到 403 Forbidden 错误：
- 确保使用包含查询字符串的完整 URL。
- 令牌（Signature）可能已过期——如有需要，请重新生成令牌。

## 注意事项

- 必须在 `mcporter` 配置文件中设置 `MINIMAX_RESOURCE_MODE`=url`。
- 生成的媒体文件 URL 包含会过期的认证令牌。
- 请始终使用 MCP 调用返回的完整 URL。

## 粤语（廣東話）使用技巧

生成粤语音频时：
- 使用粤语类别中的声音 ID（例如："Cantonese_PlayfulMan", "Cantonese_CuteGirl"）。
- **必须添加**：`languageBoost:"Chinese,Yue"` 或 `languageBoost:"Chinese"`。
- 示例：
  ```bash
  mcporter call minimax-mcp.text_to_audio text:"新年快樂" voiceId:"Cantonese_PlayfulMan" languageBoost:"Chinese,Yue"
  ```