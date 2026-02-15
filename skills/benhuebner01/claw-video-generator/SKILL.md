---
name: json2video-pinterest
description: 使用 JSON2Video API 生成适合 Pinterest 的竖版视频。该 API 支持使用 AI 生成的图片或 URL 提供的图片、AI 生成或用户提供的旁白、可选的字幕以及缩放效果。适用于为 Pinterest 联盟营销创建视频内容、制作竖版社交媒体视频、通过 JSON2Video API 自动化视频制作过程，或生成带有旁白和字幕的视频。
---

# JSON2Video Pinterest 插件

使用 JSON2Video API 生成适合 Pinterest 的竖版视频（1080x1920 像素）。

## 先决条件

1. **JSON2Video API 密钥**：请在 [https://json2video.com/get-api-key/](https://json2video.com/get-api-key/) 注册获取。
2. **设置环境变量**：
   ```bash
   export JSON2VIDEO_API_KEY="your_api_key_here"
   ```

## 快速入门

使用 JSON 配置文件创建视频：

```bash
python3 scripts/generate_video.py --config my-video.json --wait
```

## 配置格式

视频由多个场景组成。每个场景包含以下属性：

| 属性 | 类型 | 说明 |
|----------|------|-------------|
| `image` | 对象 | 图像配置（AI 生成或 URL 提供） |
| `voice` | 对象 | 语音配置（AI 生成的语音或 URL 提供的音频） |
| `text-overlay` | 字符串 | 可选：在场景中显示的文本 |
| `subtitles` | 布尔值 | 是否启用字幕 |
| `zoom_effect` | 布尔值 | 是否应用肯·伯恩斯（Ken Burns）缩放效果 |
| `duration` | 数字 | 场景持续时间（秒） |

### 图像配置

**AI 生成图像：**
```json
{
  "image": {
    "source": "ai",
    "ai_provider": "flux-schnell",
    "ai_prompt": "A minimalist workspace with laptop..."
  }
}
```

**可用的 AI 提供商：**
- `flux-pro`：最高质量、最逼真的图像
- `flux-schnell`：生成速度快、质量不错
- `freepik-classic`：数字艺术风格

**基于 URL 的图像：**
```json
{
  "image": {
    "source": "https://example.com/image.jpg"
  }
}
```

### 语音配置

**AI 生成的语音（TTS）：**
```json
{
  "voice": {
    "source": "generated",
    "text": "Your voiceover text here",
    "voice_id": "en-US-EmmaMultilingualNeural",
    "model": "azure"
  }
}
```

**提供的音频文件：**
```json
{
  "voice": {
    "source": "https://example.com/voiceover.mp3"
  }
}
```

**关于场景持续时间**：旁白会自动确定场景的长度。每个场景的持续时间与其音频长度相匹配。如果使用提供的音频文件，请确保音频时长符合您的需求。

### 完整示例**

```json
{
  "resolution": "instagram-story",
  "quality": "high",
  "cache": true,
  "scenes": [
    {
      "image": {
        "source": "ai",
        "ai_provider": "flux-schnell",
        "ai_prompt": "Affiliate marketing workspace with laptop and coffee"
      },
      "voice": {
        "source": "generated",
        "text": "Here's how to make money with affiliate marketing",
        "voice_id": "en-US-Neural2-F"
      },
      "text_overlay": "Affiliate Marketing 101",
      "subtitles": true,
      "zoom_effect": true
    }
  ]
}
```

## 高级用法：将长语音分割成多个场景

对于较长的语音内容，可以将其分割成多个场景：

```json
{
  "scenes": [
    {
      "image": { "source": "ai", "ai_prompt": "Hook image" },
      "voice": { "source": "generated", "text": "Attention-grabbing hook..." },
      "zoom_effect": true
    },
    {
      "image": { "source": "ai", "ai_prompt": "Step 1 image" },
      "voice": { "source": "generated", "text": "Step one is to..." },
      "zoom_effect": true
    },
    {
      "image": { "source": "ai", "ai_prompt": "CTA image" },
      "voice": { "source": "generated", "text": "Click the link in bio..." },
      "zoom_effect": false
    }
  ]
}
```

## 命令参考

**根据配置创建视频：**
```bash
python3 scripts/generate_video.py --config video.json --wait
```

**立即创建视频（无需等待）：**
```bash
python3 scripts/generate_video.py --config video.json --no-wait
```

**检查现有项目的状态：**
```bash
python3 scripts/generate_video.py --project-id YOUR_PROJECT_ID
```

## 分辨率选项

| 分辨率 | 尺寸 | 适用场景 |
|------------|------------|----------|
| `instagram-story` | 1080x1920 | **Pinterest/Reels/Stories**（推荐） |
| `instagram-feed` | 1080x1000 | 方形图片帖子 |
| `full-hd` | 1920x1080 | 横屏 YouTube 视频 |
| `hd` | 1280x720 | 标准高清 |
| `custom` | 任意尺寸 | 自定义尺寸 |

## 语音模型与 ID

### Azure（默认选项 - 免费，不消耗信用点）

**语音格式：`en-US-EmmaMultilingualNeural`

常见的 Azure 语音模型：
- `en-US-EmmaMultilingualNeural`：女性，自然音色（推荐）
- `en-US-GuyNeural`：男性，专业音色 |
- `en-US-JennyNeural`：女性，友好音色 |
- `en-GB-SoniaNeural`：英国女性 |
- `en-GB-RyanNeural`：英国男性 |

更多语音模型请参阅 [Microsoft Azure Speech Voices](https://learn.microsoft.com/en-us/azure/ai-services/speech-service/language-support?tabs=tts)。

### ElevenLabs（高级选项 - 需消耗信用点）

**语音名称**：例如 `Bella`、`Antoni`、`Nova`、`Shimmer` 等。

更多语音模型请参阅 [ElevenLabs Voice Library](https://elevenlabs.io/app/voice-library)。

## 安全性

- **API 密钥绝不会存储在插件文件中** |
- 必须将 API 密钥设置为环境变量 `JSON2VIDEO_API_KEY` |
- 脚本会在调用 API 之前验证密钥是否存在。

## 示例文件

- `scripts/example-config.json`：包含一个场景的基本示例 |
- `scripts/example-advanced.json`：包含多个场景的联盟营销视频示例 |

## 高级用法

请参阅 [ADVANCED.md](ADVANCED.md)，了解以下内容：
- 多场景视频架构模式 |
- 图像来源策略（AI 生成、URL 提供或混合使用） |
- 旁白制作的最佳实践 |
- 字幕样式选项 |
- 针对 Pinterest 的内容优化建议 |
- 批量处理工作流程 |
- 信用点消耗优化方法

## 故障排除

**错误：“JSON2VIDEO_API_KEY 环境变量未设置”**  
→ 执行命令：`export JSON2VIDEO_API_KEY="your_key"`  

**错误：“渲染失败”**  
→ 检查：图像 URL 是否可公开访问 |
→ 检查：AI 生成的文本是否违反内容政策 |
→ 检查：音频文件是否为有效的 MP3/WAV 格式 |

**视频生成时间过长**  
→ 在配置中启用 `cache: true` 以加速生成 |
→ 使用 `flux-schnell` 替代 `flux-pro` 以加快生成速度 |
→ 预先生成 AI 生成的图像并使用 URL 作为图像来源。

## Python API 使用方法

如需在其他脚本中编程使用该插件，请参考以下代码示例：  
```python
from scripts.generate_video import create_pinterest_video

scenes = [
    {
        "image": {"source": "ai", "ai_prompt": "..."},
        "voice": {"source": "generated", "text": "..."},
        "subtitles": True,
        "zoom_effect": True
    }
]

video_url = create_pinterest_video(scenes, wait=True)
print(f"Video ready: {video_url}")
```