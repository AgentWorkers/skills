---
name: gettr-transcribe-summarize
description: 从 GETTR 帖子中下载音频（通过 HTML 的 `og:video` 标签），使用 Apple Silicon 平台上的 MLX Whisper 工具在本地进行转录（同时添加时间戳，使用 VTT 格式），然后将转录结果整理成项目符号列表或带时间戳的提纲。当提供 GETTR 帖子链接并要求生成转录内容或摘要时，可以使用此方法。
homepage: https://gettr.com
metadata: {"clawdbot":{"emoji":"📺","requires":{"bins":["mlx_whisper","ffmpeg"]},"install":[{"id":"mlx-whisper","kind":"pip","package":"mlx-whisper","bins":["mlx_whisper"],"label":"Install mlx-whisper (pip)"},{"id":"ffmpeg","kind":"brew","formula":"ffmpeg","bins":["ffmpeg"],"label":"Install ffmpeg (brew)"}]}}
---

# Gettr转录与摘要（MLX Whisper）

## 快速入门

```bash
# 1. Parse the slug from the URL (just read it — no script needed)
#    https://gettr.com/post/p1abc2def  → slug = p1abc2def
#    https://gettr.com/streaming/p3xyz → slug = p3xyz

# 2. Get the video URL
#    For /post/ URLs: use the extraction script
python3 scripts/extract_gettr_og_video.py "<GETTR_POST_URL>"

#    For /streaming/ URLs: use browser automation directly (extraction script is unreliable)
#    See Step 1 below for browser automation instructions

# 3. Run download + transcription pipeline
bash scripts/run_pipeline.sh "<VIDEO_URL>" "<SLUG>"
```

**若需明确指定转录语言（建议用于非英语内容）：**
```bash
bash scripts/run_pipeline.sh --language zh "<VIDEO_URL>" "<SLUG>"
```

常见语言代码：`zh`（中文）、`en`（英语）、`ja`（日语）、`ko`（韩语）、`es`（西班牙语）、`fr`（法语）、`de`（德语）、`ru`（俄语）。

执行此操作后，系统会生成以下文件：
- `./out/gettr-transcribe-summarize/<slug>/audio.wav`
- `./out/gettr-transcribe-summarize/<slug>/audio.vtt`

接下来，请执行第3步（生成摘要），以获得最终结果。

---

## 工作流程（GETTR URL → 转录 → 摘要）

### 需要确认的输入信息：
- GETTR帖子URL
- 输出格式：**仅使用项目符号** 或 **项目符号 + 带时间戳的目录结构**
- 摘要长度：**简短**、**中等**（默认）或 **详细**
- 语言（可选）：如果视频为非英语且自动检测失败，请提供语言代码（例如，`zh`表示中文）

**注意：**
- 该工具不支持需要认证的GETTR帖子。
- 该工具不进行翻译；输出内容保持视频的原始语言。
- 如果转录质量较差或包含英语内容，请使用`--language`参数重新运行。

### 前置要求（本地环境）：
- 安装`mlx_whisper`并确保其在PATH环境中可用。
- 安装`ffmpeg`（推荐使用`brew install ffmpeg`）。

### 第0步 — 解析URL并选择输出目录
直接从GETTR URL中提取路径段作为输出目录：
- `https://gettr.com/post/p1abc2def` → 输出目录：`./out/gettr-transcribe-summarize/p1abc2def`
- `https://gettr.com/streaming/p3xyz789` → 输出目录：`./out/gettr-transcribe-summarize/p3xyz789`

**目录结构：**
- `./out/gettr-transcribe-summarize/<slug>/audio.wav`
- `./out/gettr-transcribe-summarize/<slug>/audio.vtt`
- `./out/gettr-transcribe-summarize/<slug>/summary.md`

### 第1步 — 获取视频URL
获取视频URL的方法取决于URL类型：

#### 对于 `/post/` 类型的URL：
使用提取脚本从帖子HTML中获取视频URL：
```bash
python3 scripts/extract_gettr_og_video.py "<GETTR_POST_URL>"
```

该脚本会将最佳的视频URL（通常是HLS格式的`.m3u8`文件）输出到标准输出。

如果提取失败，请让用户直接提供`.m3u8`或MP4文件链接（这种情况常见于私密帖子或动态生成的HTML页面）。

#### 对于 `/streaming/` 类型的URL：
**请勿使用提取脚本**。从静态HTML中提取的`og:video`链接对于流媒体内容是不可靠的——要么无法下载，要么下载过程中会出错。

**解决方法：** 使用浏览器自动化工具获取最新的、动态生成的URL：
1. 打开GETTR流媒体URL，等待页面完全加载（确保JavaScript已执行）。
2. 从渲染后的DOM中提取`og:video`元标签内容：
   ```javascript
   document.querySelector('meta[property="og:video"]').getAttribute('content')
   ```
3. 使用该最新URL继续执行后续步骤。

如果浏览器自动化工具不可用或失败，请参考`references/troubleshooting.md`以获取手动提取URL的指导。

### 第2步 — 运行处理流程（下载 + 转录）
将提取到的视频URL和slug传递给处理流程：
```bash
bash scripts/run_pipeline.sh "<VIDEO_URL>" "<SLUG>"
```

**若需明确指定语言（建议在自动检测失败时使用）：**
```bash
bash scripts/run_pipeline.sh --language zh "<VIDEO_URL>" "<SLUG>"
```

处理流程包括以下两个步骤：
1. 使用`ffmpeg`以16kHz单声道格式下载音频文件。
2. 使用MLX Whisper进行转录，并生成带时间戳的VTT文件。

#### 如果处理流程因HTTP 412错误（URL过期）而失败
当处理`/streaming/`类型的URL时，如果URL已过期，会出现此错误。此时请重新运行浏览器自动化工具以获取新的URL，然后再尝试处理流程。

如果浏览器自动化工具不可用或失败，请参考`references/troubleshooting.md`以获取手动提取URL的指导。

**注意：**
- 默认情况下，系统会自动检测语言。对于非英语内容且自动检测失败的情况，请使用`--language`参数。
- 如果处理速度较慢或占用过多内存，可以尝试使用较小的模型：`mlx-community/whisper-medium`或`mlx-community/whisper-small`。
- 如果转录质量较差，可以使用较大的模型：`mlx-community/whisper-large-v3`（虽然速度较慢，但准确性更高）。
- 如果`--word-timestamps`参数导致问题，系统会自动忽略该参数并重新尝试。

### 第3步 — 生成摘要
将最终结果保存到`./out/gettr-transcribe-summarize/<slug>/summary.md`文件中。

**摘要长度可选：**
- **简短**：5–8条项目符号；（若包含目录结构）4–6个部分
- **中等（默认）：8–20条项目符号；（若包含目录结构）6–15个部分
- **详细**：20–40条项目符号；（若包含目录结构）15–30个部分

**摘要内容包括：**
- **项目符号**（根据上述长度要求）
- **可选的时间戳目录结构**（根据上述长度要求）

**时间戳目录结构格式（默认标题样式）：**
```
[00:00 - 02:15] Section heading
- 1–3 sub-bullets
```

**从VTT文件中生成目录结构时：**
- 将相邻的音频片段合并为逻辑上连贯的部分。
- 使用第一个音频片段的开始时间和最后一个音频片段的结束时间来划分部分。

## 配置脚本：
- `scripts/run_pipeline.sh`：负责下载和转录处理流程（接受视频URL和slug作为参数）。
- `scripts/extract_gettr_og_video.py`：从GETTR HTML页面中提取`og:video` URL（支持重试和退避机制）。
- `scripts/download_audio.sh`：从HLS或MP4文件下载音频，并将其转换为16kHz单声道WAV格式。

### 错误处理：
- **非视频帖子**：提取脚本会识别图片或文本帖子，并提供相应的错误提示。
- **网络错误**：系统会自动尝试多次下载（采用指数级退避策略，最多尝试3次）。
- **无音频轨道**：下载脚本会验证输出文件，若文件中不存在音频则会报告错误。
- **HTTP 412错误**：当处理`/streaming/`类型的URL时，如果URL已过期，系统会提示重新运行浏览器自动化工具以获取新的URL；如果仍然失败，请参考`references/troubleshooting.md`。

## 故障排除
请参考`references/troubleshooting.md`以获取常见问题的解决方案，包括：
- HTTP 412错误（URL过期）
- 提取失败
- 下载失败
- 转录质量问题