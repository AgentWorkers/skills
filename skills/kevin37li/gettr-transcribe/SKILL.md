---
name: gettr-transcribe
description: 从 GETTR 的帖子或流媒体页面下载音频，并使用 MLX Whisper 在 Apple Silicon 设备上进行本地转录（同时添加时间戳，格式为 VTT）。当收到一个 GETTR URL 并要求生成转录文本时，可以使用此功能。文本的摘要部分由调用方自行处理。
homepage: https://gettr.com
metadata:
  {
    "clawdbot":
      {
        "emoji": "📺",
        "requires": { "bins": ["mlx_whisper", "ffmpeg"] },
        "install":
          [
            {
              "id": "mlx-whisper",
              "kind": "pip",
              "package": "mlx-whisper",
              "bins": ["mlx_whisper"],
              "label": "Install mlx-whisper (pip)",
            },
            {
              "id": "ffmpeg",
              "kind": "brew",
              "formula": "ffmpeg",
              "bins": ["ffmpeg"],
              "label": "Install ffmpeg (brew)",
            },
          ],
      },
  }
---
# Gettr转录（使用MLX Whisper技术）

## 快速入门

```bash
# 1. Parse the slug from the URL (just read it — no script needed)
#    https://gettr.com/post/p1abc2def  → slug = p1abc2def
#    https://gettr.com/streaming/p3xyz → slug = p3xyz

# 2. Get the audio/video URL via browser automation (see Step 1 below)
#    For /streaming/ URLs: extract the .m4a audio URL
#    For /post/ URLs: extract the og:video .m3u8 URL

# 3. Run download + transcription pipeline
bash scripts/run_pipeline.sh "<AUDIO_OR_VIDEO_URL>" "<SLUG>"
```

**如何明确指定转录语言（推荐用于非英语内容）：**

```bash
bash scripts/run_pipeline.sh --language zh "<AUDIO_OR_VIDEO_URL>" "<SLUG>"
```

常见的语言代码：`zh`（中文）、`en`（英语）、`ja`（日语）、`ko`（韩语）、`es`（西班牙语）、`fr`（法语）、`de`（德语）、`ru`（俄语）。

该脚本的输出结果为：
- `./out/gettr-transcribe/<slug>/audio.wav`
- `./out/gettr-transcribe/<slug>/audio.vtt`

视频的摘要功能由调用者单独处理（具体操作请参考相关提示）。

---

## 工作流程（从GETTR URL获取视频并转录）

### 需要提供的输入信息：
- GETTR视频的URL
- 语言（可选）：如果视频不是英语且自动检测失败，请提供相应的语言代码（例如，`zh`表示中文）

**注意事项：**
- 该脚本不支持需要身份验证的GETTR视频。
- 该脚本不进行翻译，输出内容将保持视频的原始语言。
- 如果转录质量较差或包含英语内容，请使用`--language`参数重新运行脚本。

### 前置要求（本地环境）：
- 确保已安装`mlx_whisper`并将其添加到系统路径中。
- 推荐安装`ffmpeg`（使用`brew install ffmpeg`命令安装）。

### 第0步：解析URL并确定输出目录
直接从GETTR URL中提取路径信息（无需编写脚本）：
- `https://gettr.com/post/p1abc2def` → 输出目录：`./out/gettr-transcribe/p1abc2def`
- `https://gettr.com/streaming/p3xyz789` → 输出目录：`./out/gettr-transcribe/p3xyz789`

**目录结构：**
- `./out/gettr-transcribe/<slug>/audio.wav`
- `./out/gettr-transcribe/<slug>/audio.vtt`

### 第1步：通过浏览器自动化获取音频/视频URL
使用浏览器自动化工具访问GETTR URL，并从页面中提取媒体文件的URL。

#### 对于 `/streaming/` 类型的URL：
这类页面会提供直接的`.m4a`音频文件下载链接。可以通过`og:video`元标签获取音频URL：
1. 访问GETTR视频页面，等待页面完全加载（确保JavaScript已执行）。
2. 通过JavaScript提取音频URL：
   ```javascript
   const ogVideo = document.querySelector('meta[property="og:video"]')?.getAttribute("content");
   // Replace .m3u8 with /audio.m4a to get the direct audio download URL
   const audioUrl = ogVideo.replace(".m3u8", "/audio.m4a");
   ```
3. 使用提取到的`.m4a` URL进行后续处理。

`.m4a`文件可以直接下载（无需HLS协议），因此下载速度更快且更可靠。

#### 对于 `/post/` 类型的URL：
这类页面没有“下载音频”按钮。需要从页面中提取`.og:video`元标签对应的视频URL：
1. 访问GETTR视频页面，等待页面完全加载。
2. 通过JavaScript提取视频URL：
   ```javascript
   document.querySelector('meta[property="og:video"]')?.getAttribute("content");
   ```
3. 使用提取到的`.m3u8` URL进行后续处理。

如果浏览器自动化工具不可用或出现故障，请参考`references/troubleshooting.md`以获取手动提取URL的指导。

### 第2步：执行转录流程
将提取到的URL和slug传递给转录脚本：
```bash
bash scripts/run_pipeline.sh "<AUDIO_OR_VIDEO_URL>" "<SLUG>"
```

**如何明确指定语言（推荐在自动检测失败时使用）：**
```bash
bash scripts/run_pipeline.sh --language zh "<AUDIO_OR_VIDEO_URL>" "<SLUG>"
```

该脚本执行以下两个操作：
1. 使用`ffmpeg`将音频文件下载为16kHz单声道WAV格式（支持`.m4a`和`.m3u8`格式）。
2. 使用MLX Whisper技术进行转录，生成带有时间戳的VTT文件。

#### 如果转录过程中出现HTTP 412错误（签名URL过期）：
这种情况通常发生在 `/streaming/` 类型的URL上，因为签名URL已过期。此时请重新运行浏览器自动化工具以获取新的URL，然后再尝试转录。

如果浏览器自动化工具不可用或出现故障，请参考`references/troubleshooting.md`以获取手动获取新URL的指导。

**注意事项：**
- 默认情况下，系统会自动检测语言；如果检测失败（针对非英语内容），请使用`--language`参数指定语言。
- 如果转录速度较慢或占用较多内存，可以尝试使用性能较低的模型：`mlx-community/whisper-medium`或`mlx-community/whisper-small`。
- 如果转录质量不佳，可以尝试使用性能更高的模型：`mlx-community/whisper-large-v3`（虽然速度较慢，但转录更准确）。
- 如果`--word-timestamps`参数导致问题，脚本会自动忽略该参数并重新尝试转录。

## 配置脚本：
- `scripts/run_pipeline.sh`：负责下载和转录操作（接受音频/视频URL及slug作为输入）。
- `scripts/download_audio.sh`：负责从HLS（`.m3u8`）或直接链接（`.m4a`）下载音频文件，并将其转换为16kHz单声道WAV格式。

### 错误处理：
- **无音频文件**：下载脚本会检查输出文件，如果文件中不存在音频内容会报告错误。
- **HTTP 412错误**：当`.m4a`音频文件的签名URL过期时可能发生此错误。此时请重新运行浏览器自动化工具以获取新的URL；如果仍然无法解决问题，请参考`references/troubleshooting.md`。

## 故障排除
请参阅`references/troubleshooting.md`以获取针对常见问题的解决方案，包括：
- HTTP 412错误（签名URL过期）
- 下载失败
- 转录质量问题