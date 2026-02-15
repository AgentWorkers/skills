---
name: flyworks-avatar-video
description: 使用 Flyworks（又名 HiFly）数字人类技术生成视频。可以从图片中创建带语音的图片视频，使用带有文本转语音（TTS）功能的公共头像，或者克隆声音以生成自定义音频。
license: MIT
compatibility: Requires Python 3 and network access to hfw-api.hifly.cc
---

# 虚拟形象视频生成技能

该技能允许您使用 Flyworks（又名 HiFly 飞影数字人）来生成视频。支持的功能包括：
1. **公共虚拟形象视频**：使用预先制作的高逼真虚拟形象，根据文本或音频生成视频。
2. **“会说话的照片”**：根据单张图片以及文本/音频生成“会说话的照片”视频。
3. **语音克隆**：从音频样本中克隆语音，用于文本转语音（TTS）功能。

有关详细文档，请参阅 [references/](references/) 文件夹：
- [authentication.md](references/authentication.md) - API 令牌设置
- [avatars.md](references/avatars.md) - 虚拟形象的使用方法
- [voices.md](references/voices.md) - 语音选择与克隆
- [video-generation.md](references/video-generation.md) - 视频生成流程

## API 令牌与限制

该技能支持默认的免费级令牌，但存在以下限制：
- **水印**：生成的视频会带有水印。
- **时长限制**：视频时长最多为 30 秒。

**如需解除这些限制**：
1. 在 [hifly.cc](https://hifly.cc) 或 [flyworks.ai](https://flyworks.ai) 注册。
2. 从 [用户设置](https://hifly.cc/setting) 获取您的 API 密钥。
3. 设置环境变量：`export HIFLY_API_TOKEN="your_token_here"`

## 工具

### `scripts/hifly_client.py`

所有操作的主要入口脚本。

#### 使用方法

```bash
# List available public avatars
python scripts/hifly_client.py list_public_avatars

# List available public voices
python scripts/hifly_client.py list_public_voices

# Create a video with a public avatar (TTS)
python scripts/hifly_client.py create_video --type tts --text "Hello world" --avatar "avatar_id_or_alias" --voice "voice_id_or_alias"

# Create a video with a public avatar (Audio URL or File)
python scripts/hifly_client.py create_video --audio "https://... or path/to/audio.mp3" --avatar "avatar_id_or_alias"

# Create a talked photo video using bundled assets
python scripts/hifly_client.py create_talking_photo --image assets/avatar.png --title "Bundled Avatar"

# Clone a voice using bundled assets
python scripts/hifly_client.py clone_voice --audio assets/voice.MP3 --title "Bundled Voice"

# Check status of generated tasks
python scripts/hifly_client.py check_task --id "TASK_ID"

# Manage local aliases (saved in memory.json)
python scripts/hifly_client.py manage_memory add my_avatar "av_12345"
python scripts/hifly_client.py manage_memory list
```

## 示例

### 1. 创建一个简单的问候视频
```bash
# First find a voice and avatar
python scripts/hifly_client.py list_public_avatars
python scripts/hifly_client.py list_public_voices

# Generate
python scripts/hifly_client.py create_video --type tts --text "Welcome to our service." --avatar "av_public_01" --voice "voice_public_01"
```

### 2. 使用自定义的“会说话的照片”
```bash
# Create the avatar from an image URL
python scripts/hifly_client.py create_talking_photo --image "https://mysite.com/photo.jpg" --title "CEO Photo"
# Output will give you an Avatar ID, e.g., av_custom_99

# Save it to memory
python scripts/hifly_client.py manage_memory add ceo av_custom_99

# Generate video using the new avatar
python scripts/hifly_client.py create_video --type tts --text "Here is the quarterly report." --avatar ceo --voice "voice_public_01"
```

## 代理行为指南

在协助用户生成视频时，请遵循以下指南：

### 必须选择语音

**视频生成需要同时提供文本和语音。** 如果用户提供了文本但未提供语音：
1. **首先检查本地内存**：运行 `manage_memory list` 查看用户是否保存了任何语音文件。
2. **询问用户选择**：
   - “您希望使用文本 '[text]' 来生成视频。选择哪种语音？”
   - 如果用户保存了语音文件： “您已保存的语音文件有：[list]。或者您想使用公共语音吗？”
   - 如果没有保存的语音文件： “您想使用公共语音，还是先从音频样本中克隆自己的语音？”
3. **帮助用户选择**：
   - 查看公共语音文件：`list_public_voices`
   - 克隆语音：`clone_voice --audio [file] --title [name]`

### 完整的工作流程示例

对于类似 “根据我的照片生成一句‘这是我的 AI 分身’的‘会说话的照片’视频” 的请求：
1. 询问用户： “您希望为您的 AI 分身选择哪种语音？您可以使用公共语音，或者克隆自己的语音。”
2. 如果用户选择克隆语音： 帮助他们使用 `clone_voice` 功能。
3. 结合文本和语音生成“会说话的照片”视频：
   ```bash
   python scripts/hifly_client.py create_talking_photo \
     --image user_photo.jpg \
     --text "this is my AI twin" \
     --voice SELECTED_VOICE_ID \
     --title "My AI Twin"
   ```

### 保存结果以供后续使用

在生成虚拟形象或克隆语音后，可以提供保存选项：
```bash
python scripts/hifly_client.py manage_memory add my_avatar AVATAR_ID --kind avatar
python scripts/hifly_client.py manage_memory add my_voice VOICE_ID --kind voice
```