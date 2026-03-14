---
name: douyin-transcribe
description: 使用 Whisper 从抖音（TikTok China）视频中提取音频并将其转录为文本。当用户发送一个抖音链接（格式为 v.douyin.com 或 www.douyin.com/video/）并请求转录、分析视频内容或生成摘要时，系统应自动触发相应功能。
---
# 快手视频转录

从快手视频中提取语音并将其转换为文本。支持中文/英文，支持跨平台（Windows/macOS/Linux）。

## 核心原理

快手有严格的反爬虫机制。必须遵循以下步骤：
1. 在浏览器中加载视频页面，等待视频流加载。
2. 从DOM或网络请求中提取真实的CDN链接。
3. 使用带有`Referer: https://www.douyin.com/`头的请求进行下载（如果没有这个头，将会收到403错误）。
4. 将音频转换为16kHz单声道WAV格式，以便后续使用Whisper工具进行语音转文字处理。

## 先决条件

| 工具 | 用途 | 安装方式 |
|------|---------|---------|
| ffmpeg | 音频提取 | `brew install ffmpeg` / `winget install ffmpeg` / `apt install ffmpeg` |
| whisper | 语音转文字 | `pip install openai-whisper` |
| curl | 下载视频 | Windows系统内置（命令：`curl.exe`） |

## 工作流程

### 1. 解析短链接

快手的分享链接通常为`v.douyin.com/xxx`，需要将其解析为完整的URL：

```bash
# macOS/Linux
curl -sL -o /dev/null -w '%{url_effective}' "https://v.douyin.com/xxx/"

# Windows PowerShell
curl.exe -sL -o NUL -w "%{url_effective}" "https://v.douyin.com/xxx/"
```

输出：`https://www.douyin.com/video/7616020798351871284`

视频ID是URL中的19位数字。

### 2. 获取视频URL

在浏览器中打开视频页面，等待3-5秒后，执行JavaScript代码：

```javascript
(() => {
  const videos = document.querySelectorAll('video');
  for (const v of videos) {
    const src = v.currentSrc || v.src;
    if (src && src.startsWith('http') && !src.includes('uuu_265')) {
      return src;
    }
  }
  return null;
})()
```

**关键点：**
- 如果返回`null`，说明页面未加载，等待一段时间后重试。
- 如果URL中包含`uuu_265`，表示是占位符视频，等待一段时间后重试。
- 如果URL以`blob:`开头，表示视频正在流式传输中，需要等待真实的视频URL。
- CDN链接的有效期约为2小时，必要时需要重新获取。

### 3. 下载视频

```bash
# macOS/Linux
curl -L -H "Referer: https://www.douyin.com/" -o video.mp4 "<CDN_URL>"

# Windows
curl.exe -L -H "Referer: https://www.douyin.com/" -o video.mp4 "<CDN_URL>"
```

**必须使用带有`Referer: https://www.douyin.com/`头的请求，否则会收到403错误。**

### 4. 提取音频

```bash
ffmpeg -i video.mp4 -ar 16000 -ac 1 -c:a pcm_s16le audio.wav -y
```

参数说明：
- `-ar 16000`：采样率为16kHz（Whisper工具的要求）
- `-ac 1`：单声道
- `-c:a pcm_s16le`：16位PCM格式

### 5. 转录语音

```bash
python -m whisper audio.wav --model small --language zh
```

**模型选择：**

| 模型 | 大小 | 处理5分钟视频所需时间（CPU） | 精确度 | 适用场景 |
|-------|------|-------------------|----------|----------|
| tiny | 75MB | 约30秒 | 一般 | 快速预览 |
| base | 142MB | 约1分钟 | 良好 | 日常使用 |
| small | 466MB | 约3分钟 | 更好 | **推荐** |
| medium | 1.5GB | 约8分钟 | 最佳 | 高精度 |

**语言设置：**
- 中文：`--language zh`
- 英文：`--language en`
- 自动检测：省略此参数（但会降低处理速度）

转录后的文件保存在当前目录中，文件名为`audio.txt`、`audio.srt`和`audio.json`。

## 故障排除

| 问题 | 原因 | 解决方案 |
|-------|-----------|----------|
| 短链接解析失败 | 返回的URL非快手链接 | 检查链接是否完整，去除分享页面中的无关文本 |
| 无法获取视频URL | JavaScript返回`null` | 等待3-5秒后重试，最多尝试3次 |
| 视频为占位符 | URL中包含`uuu_265` | 页面未加载，等待一段时间后重试 |
| 下载失败（403错误） | `curl`命令返回403错误 | 检查`Referer`头；可能是因为链接已过期 |
| Whisper工具运行缓慢 | 长时间无输出 | 首次运行时下载较大模型的文件（例如`small`模型，大小约460MB） |
| 转录结果混乱 | 终端显示乱码 | 正常现象，直接查看`.txt`文件即可 |
| 内存不足 | 系统进程被终止 | 使用较小的模型（如`base`或`tiny`） |

## 输出格式

文件名以视频ID命名，保存到用户指定的目录中：

```
output/
├── 7616020798351871284.mp4   # Original video (optional)
├── 7616020798351871284.wav   # Audio (delete after)
├── 7616020798351871284.txt   # Transcript
└── 7616020798351871284.srt   # Subtitles (optional)
```

## 脚本（可选）

技能目录中包含以下辅助脚本：
- `scripts/get_video_url.js`：用于在浏览器中通过多种方法提取视频URL的脚本。
- `scripts/transcribe.py`：通过命令行实现一键转录功能（需要提供视频URL）。

这些脚本仅供参考，可以根据实际需求自行实现。

## 注意事项：
- **文章链接**：可以直接使用浏览器截图，无需进行转录。
- **快手AI摘要**：部分视频页面包含AI生成的章节摘要，可以从截图中提取这些摘要作为补充内容。
- **其他平台**：本技能仅适用于快手视频。对于YouTube或Bilibili视频，请使用`yt-dlp`工具。